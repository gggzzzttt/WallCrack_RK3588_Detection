#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
裂缝分割训练脚本
支持: 检查点保存、最佳模型保存、TensorBoard 日志、断点续训

使用方法:
  1. PyCharm 直接运行: 右键 -> Run 'train_crack'
  2. 命令行运行: python tools/train_crack.py --config configs/bisenetv2_crack.py
"""

import sys
import os

# 自动设置工作目录 (PyCharm 直接运行时需要)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# 切换到项目根目录
os.chdir(project_dir)

import os.path as osp
import random
import logging
import time
import json
import argparse
import numpy as np
from datetime import datetime
from tabulate import tabulate

import torch
import torch.nn as nn
import torch.distributed as dist
from torch.utils.data import DataLoader
import torch.cuda.amp as amp

from lib.models import model_factory
from configs import set_cfg_from_file
from lib.data import get_data_loader
from lib.ohem_ce_loss import OhemCELoss
from lib.focal_dice_loss import FocalDiceLoss
from lib.lr_scheduler import WarmupPolyLrScheduler
from lib.meters import TimeMeter, AvgMeter
from lib.logger import setup_logger, log_msg


def parse_args():
    parser = argparse.ArgumentParser(description='裂缝分割训练脚本')
    parser.add_argument('--config', type=str, default='configs/bisenetv2_crack.py',
                        help='配置文件路径')
    parser.add_argument('--resume', type=str, default=None,
                        help='恢复训练的检查点路径')
    parser.add_argument('--finetune-from', type=str, default=None,
                        help='预训练权重路径')
    parser.add_argument('--no-tensorboard', action='store_true',
                        help='禁用 TensorBoard')
    return parser.parse_args()


args = parse_args()
cfg = set_cfg_from_file(args.config)


class Trainer:
    """训练器类"""

    def __init__(self, cfg, args):
        self.cfg = cfg
        self.args = args
        self.local_rank = int(os.environ.get('LOCAL_RANK', 0))
        self.is_main_process = (self.local_rank == 0)

        # 创建保存目录
        if self.is_main_process:
            self.setup_directories()
            self.setup_logging()
            self.save_config()
            if not args.no_tensorboard:
                self.setup_tensorboard()

        # 初始化训练组件
        self.setup_model()
        self.setup_dataloader()
        self.setup_optimizer()
        self.setup_loss()
        self.setup_meters()

        # 训练状态
        self.start_iter = 0
        self.best_miou = 0.0
        self.best_f1 = 0.0

        # 恢复训练
        if args.resume:
            self.load_checkpoint(args.resume)

    def setup_directories(self):
        """创建保存目录"""
        self.res_dir = self.cfg.respth
        self.ckpt_dir = osp.join(self.res_dir, 'checkpoints')
        self.log_dir = osp.join(self.res_dir, 'logs')
        self.tb_dir = osp.join(self.res_dir, 'tensorboard')

        os.makedirs(self.res_dir, exist_ok=True)
        os.makedirs(self.ckpt_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
        if not self.args.no_tensorboard:
            os.makedirs(self.tb_dir, exist_ok=True)

    def setup_logging(self):
        """设置日志"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = osp.join(self.log_dir, f'train_{timestamp}.log')
        setup_logger(f'{self.cfg.model_type}-train', self.log_dir)
        self.logger = logging.getLogger()

        self.logger.info('=' * 60)
        self.logger.info('裂缝分割训练')
        self.logger.info('=' * 60)
        self.logger.info(f'配置文件: {self.args.config}')
        self.logger.info(f'保存目录: {self.res_dir}')
        self.logger.info(f'时间戳: {timestamp}')

    def save_config(self):
        """保存训练配置"""
        config_path = osp.join(self.res_dir, 'config.json')
        config_dict = {
            'model_type': self.cfg.model_type,
            'n_cats': self.cfg.n_cats,
            'lr_start': self.cfg.lr_start,
            'weight_decay': self.cfg.weight_decay,
            'max_iter': self.cfg.max_iter,
            'warmup_iters': self.cfg.warmup_iters,
            'cropsize': self.cfg.cropsize,
            'ims_per_gpu': self.cfg.ims_per_gpu,
            'use_fp16': self.cfg.use_fp16,
            'dataset': self.cfg.dataset,
        }
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)

    def setup_tensorboard(self):
        """设置 TensorBoard"""
        try:
            from torch.utils.tensorboard import SummaryWriter
            self.writer = SummaryWriter(self.tb_dir)
            self.logger.info(f'TensorBoard 日志目录: {self.tb_dir}')
        except ImportError:
            self.logger.warning('未安装 tensorboard，跳过 TensorBoard 日志')
            self.writer = None

    def setup_model(self):
        """设置模型"""
        self.logger.info(f'创建模型: {self.cfg.model_type}')
        self.net = model_factory[self.cfg.model_type](self.cfg.n_cats)

        # 加载预训练权重
        if self.args.finetune_from:
            self.logger.info(f'加载预训练权重: {self.args.finetune_from}')
            state = torch.load(self.args.finetune_from, map_location='cpu')
            msg = self.net.load_state_dict(state, strict=False)
            self.logger.info(f'\tmissing keys: {msg.missing_keys}')
            self.logger.info(f'\tunexpected keys: {msg.unexpected_keys}')

        # 同步 BN
        if self.cfg.use_sync_bn:
            self.net = nn.SyncBatchNorm.convert_sync_batchnorm(self.net)

        self.net.cuda()
        self.net.train()

    def setup_dataloader(self):
        """设置数据加载器"""
        self.logger.info('加载数据集...')
        self.dl = get_data_loader(self.cfg, mode='train')
        self.logger.info(f'训练集大小: {len(self.dl.dataset)}')

    def setup_optimizer(self):
        """设置优化器"""
        if hasattr(self.net, 'get_params'):
            wd_params, nowd_params, lr_mul_wd_params, lr_mul_nowd_params = self.net.get_params()
            wd_val = 0
            params_list = [
                {'params': wd_params},
                {'params': nowd_params, 'weight_decay': wd_val},
                {'params': lr_mul_wd_params, 'lr': self.cfg.lr_start * 10},
                {'params': lr_mul_nowd_params, 'weight_decay': wd_val, 'lr': self.cfg.lr_start * 10},
            ]
        else:
            wd_params, non_wd_params = [], []
            for name, param in self.net.named_parameters():
                if param.dim() == 1:
                    non_wd_params.append(param)
                elif param.dim() == 2 or param.dim() == 4:
                    wd_params.append(param)
            params_list = [
                {'params': wd_params},
                {'params': non_wd_params, 'weight_decay': 0},
            ]

        self.optim = torch.optim.SGD(
            params_list,
            lr=self.cfg.lr_start,
            momentum=0.9,
            weight_decay=self.cfg.weight_decay,
        )

        # 混合精度
        self.scaler = amp.GradScaler(enabled=self.cfg.use_fp16)

        # 学习率调度器
        # 注意：手动设置 initial_lr，避免 PyTorch 自动调用 step()
        # 这样确保 step() 在 optimizer.step() 之后调用
        for param_group in self.optim.param_groups:
            param_group['initial_lr'] = self.cfg.lr_start

        self.lr_schdr = WarmupPolyLrScheduler(
            self.optim, power=0.9,
            max_iter=self.cfg.max_iter,
            warmup_iter=self.cfg.warmup_iters,
            warmup_ratio=0.1,
            warmup='exp',
            last_epoch=0,
        )

    def setup_loss(self):
        """设置损失函数"""
        lb_ignore = self.dl.dataset.lb_ignore

        # 检查是否使用 Focal + Dice Loss
        use_focal_dice = getattr(self.cfg, 'use_focal_dice', False)

        if use_focal_dice:
            # 使用 Focal Loss + Dice Loss 组合
            self.logger.info('使用 Focal Loss + Dice Loss 组合损失函数')
            gamma = getattr(self.cfg, 'focal_gamma', 2.0)
            focal_weight = getattr(self.cfg, 'focal_weight', 1.0)
            dice_weight = getattr(self.cfg, 'dice_weight', 1.0)

            self.criteria_pre = FocalDiceLoss(
                gamma=gamma,
                focal_weight=focal_weight,
                dice_weight=dice_weight,
                lb_ignore=lb_ignore
            )
            self.criteria_aux = [FocalDiceLoss(
                gamma=gamma,
                focal_weight=focal_weight,
                dice_weight=dice_weight,
                lb_ignore=lb_ignore
            ) for _ in range(self.cfg.num_aux_heads)]
        else:
            # 使用默认的 OhemCELoss
            self.logger.info('使用 OhemCELoss 损失函数')
            self.criteria_pre = OhemCELoss(0.7, lb_ignore)
            self.criteria_aux = [OhemCELoss(0.7, lb_ignore)
                                 for _ in range(self.cfg.num_aux_heads)]

    def setup_meters(self):
        """设置指标记录器"""
        self.time_meter = TimeMeter(self.cfg.max_iter)
        self.loss_meter = AvgMeter('loss')
        self.loss_pre_meter = AvgMeter('loss_pre')
        self.loss_aux_meters = [AvgMeter(f'loss_aux{i}')
                                for i in range(self.cfg.num_aux_heads)]

    def set_distributed(self):
        """设置分布式训练"""
        torch.cuda.set_device(self.local_rank)
        dist.init_process_group(backend='nccl')
        self.net = nn.parallel.DistributedDataParallel(
            self.net,
            device_ids=[self.local_rank],
            output_device=self.local_rank
        )

    def save_checkpoint(self, iter_num, is_best=False, filename=None):
        """保存检查点"""
        if not self.is_main_process:
            return

        if filename is None:
            filename = f'checkpoint_{iter_num}.pth'

        ckpt_path = osp.join(self.ckpt_dir, filename)

        # 获取模型状态
        if hasattr(self.net, 'module'):
            model_state = self.net.module.state_dict()
        else:
            model_state = self.net.state_dict()

        checkpoint = {
            'iter': iter_num,
            'model_state_dict': model_state,
            'optimizer_state_dict': self.optim.state_dict(),
            'lr_scheduler_state_dict': self.lr_schdr.state_dict(),
            'scaler_state_dict': self.scaler.state_dict(),
            'best_miou': self.best_miou,
            'best_f1': self.best_f1,
            'loss_meter': self.loss_meter.avg,
        }

        torch.save(checkpoint, ckpt_path)
        self.logger.info(f'保存检查点: {ckpt_path}')

        # 保存最佳模型
        if is_best:
            best_path = osp.join(self.res_dir, 'model_best.pth')
            torch.save(model_state, best_path)
            self.logger.info(f'保存最佳模型: {best_path} (mIoU: {self.best_miou:.4f})')

    def load_checkpoint(self, ckpt_path):
        """加载检查点"""
        self.logger.info(f'加载检查点: {ckpt_path}')
        checkpoint = torch.load(ckpt_path, map_location='cpu')

        # 加载模型
        if hasattr(self.net, 'module'):
            self.net.module.load_state_dict(checkpoint['model_state_dict'])
        else:
            self.net.load_state_dict(checkpoint['model_state_dict'])

        # 加载优化器
        self.optim.load_state_dict(checkpoint['optimizer_state_dict'])
        self.lr_schdr.load_state_dict(checkpoint['lr_scheduler_state_dict'])
        self.scaler.load_state_dict(checkpoint['scaler_state_dict'])

        # 恢复训练状态
        self.start_iter = checkpoint['iter'] + 1
        self.best_miou = checkpoint.get('best_miou', 0.0)
        self.best_f1 = checkpoint.get('best_f1', 0.0)

        self.logger.info(f'从迭代 {self.start_iter} 恢复训练')
        self.logger.info(f'历史最佳 mIoU: {self.best_miou:.4f}')

    def train_iter(self, im, lb):
        """单次训练迭代"""
        im = im.cuda()
        lb = lb.cuda()
        lb = torch.squeeze(lb, 1)

        self.optim.zero_grad()

        with amp.autocast(enabled=self.cfg.use_fp16):
            logits, *logits_aux = self.net(im)
            loss_pre = self.criteria_pre(logits, lb)
            loss_aux = [crit(lgt, lb) for crit, lgt in zip(self.criteria_aux, logits_aux)]
            loss = loss_pre + sum(loss_aux)

        self.scaler.scale(loss).backward()
        self.scaler.step(self.optim)
        self.scaler.update()

        torch.cuda.synchronize()

        # 更新指标
        self.loss_meter.update(loss.item())
        self.loss_pre_meter.update(loss_pre.item())
        for mter, lss in zip(self.loss_aux_meters, loss_aux):
            mter.update(lss.item())

        return loss.item()

    def log_tensorboard(self, iter_num, lr):
        """记录 TensorBoard"""
        if self.writer is None:
            return

        self.writer.add_scalar('Loss/total', self.loss_meter.avg, iter_num)
        self.writer.add_scalar('Loss/pre', self.loss_pre_meter.avg, iter_num)
        for i, mter in enumerate(self.loss_aux_meters):
            self.writer.add_scalar(f'Loss/aux{i}', mter.avg, iter_num)
        self.writer.add_scalar('Train/lr', lr, iter_num)

    @torch.no_grad()
    def evaluate(self):
        """评估模型"""
        self.logger.info('开始评估...')
        self.net.eval()

        # 获取模型
        if hasattr(self.net, 'module'):
            model = self.net.module
        else:
            model = self.net

        # 评估
        from evaluate import eval_model
        iou_heads, iou_content, f1_heads, f1_content = eval_model(self.cfg, model)

        self.logger.info('\n评估结果 (F1 Score):')
        self.logger.info('\n' + tabulate(f1_content, headers=f1_heads, tablefmt='orgtbl'))
        self.logger.info('\n评估结果 (mIoU):')
        self.logger.info('\n' + tabulate(iou_content, headers=iou_heads, tablefmt='orgtbl'))

        # 提取 mIoU 和 F1（从字符串转换为 float）
        miou = float(iou_content[-1][-1])  # 最后一行的最后一个值是 mIoU
        f1 = float(f1_content[-1][-1])  # 最后一行的最后一个值是 F1

        self.net.train()
        return miou, f1

    def train(self):
        """训练主循环"""
        self.logger.info('开始训练...')
        self.logger.info(f'总迭代次数: {self.cfg.max_iter}')
        self.logger.info(f'起始迭代: {self.start_iter}')

        # 训练循环
        for it, (im, lb) in enumerate(self.dl, start=self.start_iter):
            if it >= self.cfg.max_iter:
                break

            # 训练迭代
            loss = self.train_iter(im, lb)
            self.time_meter.update()

            # 学习率更新
            self.lr_schdr.step()

            # 打印日志
            if (it + 1) % 100 == 0:
                lr = self.lr_schdr.get_lr()
                lr = sum(lr) / len(lr)
                msg = log_msg(it, self.cfg.max_iter, lr, self.time_meter,
                              self.loss_meter, self.loss_pre_meter, self.loss_aux_meters)
                self.logger.info(msg)

                # TensorBoard
                if self.is_main_process:
                    self.log_tensorboard(it, lr)

            # 保存检查点
            save_interval = getattr(self.cfg, 'save_interval', 2000)
            if (it + 1) % save_interval == 0 and self.is_main_process:
                self.save_checkpoint(it + 1)

            # 评估
            eval_interval = getattr(self.cfg, 'eval_interval', 1000)
            if (it + 1) % eval_interval == 0 and self.is_main_process:
                miou, f1 = self.evaluate()

                # 更新最佳模型
                is_best = miou > self.best_miou
                if is_best:
                    self.best_miou = miou
                    self.best_f1 = f1

                self.save_checkpoint(it + 1, is_best=is_best)

                # TensorBoard
                if self.writer:
                    self.writer.add_scalar('Eval/mIoU', miou, it)
                    self.writer.add_scalar('Eval/F1', f1, it)

        # 训练结束
        self.logger.info('=' * 60)
        self.logger.info('训练完成!')
        self.logger.info(f'最佳 mIoU: {self.best_miou:.4f}')
        self.logger.info(f'最佳 F1: {self.best_f1:.4f}')

        # 保存最终模型
        if self.is_main_process:
            final_path = osp.join(self.res_dir, 'model_final.pth')
            if hasattr(self.net, 'module'):
                torch.save(self.net.module.state_dict(), final_path)
            else:
                torch.save(self.net.state_dict(), final_path)
            self.logger.info(f'保存最终模型: {final_path}')

        if self.writer:
            self.writer.close()


def main():
    # 初始化分布式训练
    if 'RANK' in os.environ and 'WORLD_SIZE' in os.environ:
        trainer = Trainer(cfg, args)
        trainer.set_distributed()
        trainer.train()
    else:
        # 单 GPU 训练
        trainer = Trainer(cfg, args)
        trainer.train()


if __name__ == "__main__":
    main()
