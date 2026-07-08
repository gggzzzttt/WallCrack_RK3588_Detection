"""
裂缝分类训练主程序
使用 MobileNetV3-Small 进行5级裂缝分类

用法:
    python train.py [--resume PATH] [--eval]
"""

import os
import sys
import time
import argparse
import json
from datetime import datetime

import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from dataset import get_dataloaders
from model import build_model


class AverageMeter:
    """计算并存储平均值和当前值"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count if self.count > 0 else 0


class Trainer:
    """裂缝分类训练器"""

    def __init__(self, config, args):
        self.config = config
        self.args = args
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # 设置随机种子
        self._set_seed(config.seed)

        # 创建保存目录
        self.save_dir = config.get_save_path()
        print(f"保存目录: {self.save_dir}")

        # 初始化 TensorBoard
        log_dir = os.path.join(self.save_dir, 'tensorboard', datetime.now().strftime('%Y%m%d_%H%M%S'))
        self.writer = SummaryWriter(log_dir)
        print(f"TensorBoard 日志: {log_dir}")

        # 构建模型
        self.model = build_model(
            num_classes=config.num_classes,
            in_channels=4 if config.use_mask else 3,
            pretrained=True,
            device=self.device
        )

        # 数据加载器
        print("加载数据集...")
        self.train_loader, self.val_loader, self.test_loader = get_dataloaders(config)

        # 损失函数（使用类别加权和标签平滑）
        class_weights = torch.tensor(config.class_weights, dtype=torch.float32).to(self.device)
        self.criterion = nn.CrossEntropyLoss(
            weight=class_weights,
            label_smoothing=config.label_smoothing
        )

        # 优化器
        self.optimizer = self._setup_optimizer()

        # 学习率调度器
        self.scheduler = self._setup_scheduler()

        # 最佳指标
        self.best_acc = 0.0
        self.best_epoch = 0

        # 早停参数
        self.patience = config.early_stopping_patience
        self.counter = 0

        # 恢复训练
        if args.resume:
            self.load_checkpoint(args.resume)

    def _set_seed(self, seed):
        """设置随机种子"""
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)

    def _setup_optimizer(self):
        """设置优化器"""
        if self.config.optimizer.lower() == 'adam':
            return torch.optim.Adam(
                self.model.parameters(),
                lr=self.config.lr,
                weight_decay=self.config.weight_decay
            )
        elif self.config.optimizer.lower() == 'sgd':
            return torch.optim.SGD(
                self.model.parameters(),
                lr=self.config.lr,
                momentum=0.9,
                weight_decay=self.config.weight_decay
            )
        else:
            raise ValueError(f"不支持的优化器: {self.config.optimizer}")

    def _setup_scheduler(self):
        """设置学习率调度器"""
        if self.config.scheduler == 'cosine':
            return torch.optim.lr_scheduler.CosineAnnealingLR(
                self.optimizer,
                T_max=self.config.epochs,
                eta_min=self.config.min_lr
            )
        elif self.config.scheduler == 'step':
            return torch.optim.lr_scheduler.StepLR(
                self.optimizer,
                step_size=30,
                gamma=0.1
            )
        elif self.config.scheduler == 'plateau':
            return torch.optim.lr_scheduler.ReduceLROnPlateau(
                self.optimizer,
                mode='max',
                factor=0.5,
                patience=5
            )
        else:
            raise ValueError(f"不支持的学习率调度器: {self.config.scheduler}")

    def train_one_epoch(self, epoch):
        """训练一个epoch"""
        self.model.train()

        loss_meter = AverageMeter()
        acc_meter = AverageMeter()

        for batch_idx, (data, target) in enumerate(self.train_loader):
            data, target = data.to(self.device), target.to(self.device)

            # 前向传播
            output = self.model(data)
            loss = self.criterion(output, target)

            # 反向传播
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            # 统计
            pred = output.argmax(dim=1)
            acc = (pred == target).float().mean()

            loss_meter.update(loss.item(), data.size(0))
            acc_meter.update(acc.item(), data.size(0))

            # 打印进度
            if (batch_idx + 1) % self.config.print_freq == 0:
                lr = self.optimizer.param_groups[0]['lr']
                print(f"Epoch [{epoch+1}/{self.config.epochs}] "
                      f"[{batch_idx+1}/{len(self.train_loader)}] "
                      f"Loss: {loss_meter.avg:.4f} "
                      f"Acc: {acc_meter.avg:.4f} "
                      f"LR: {lr:.6f}")

        # 更新学习率
        if self.config.scheduler != 'plateau':
            self.scheduler.step()

        return loss_meter.avg, acc_meter.avg

    @torch.no_grad()
    def validate(self, loader, epoch, split='val'):
        """验证/测试"""
        self.model.eval()

        loss_meter = AverageMeter()
        correct = 0
        total = 0

        # 各类别统计
        class_correct = [0] * self.config.num_classes
        class_total = [0] * self.config.num_classes

        for data, target in loader:
            data, target = data.to(self.device), target.to(self.device)

            output = self.model(data)
            loss = self.criterion(output, target)

            pred = output.argmax(dim=1)
            correct += (pred == target).sum().item()
            total += target.size(0)

            loss_meter.update(loss.item(), data.size(0))

            # 各类别统计
            for i in range(target.size(0)):
                label = target[i].item()
                pred_label = pred[i].item()
                class_total[label] += 1
                if label == pred_label:
                    class_correct[label] += 1

        avg_loss = loss_meter.avg
        accuracy = correct / total if total > 0 else 0

        # 打印各类别准确率
        print(f"\n{split.upper()} 结果:")
        print(f"总体准确率: {accuracy:.4f}")
        for i in range(self.config.num_classes):
            if class_total[i] > 0:
                class_acc = class_correct[i] / class_total[i]
                print(f"  类别 {i} ({Config.get_class_names()[i]}): "
                      f"{class_acc:.4f} ({class_correct[i]}/{class_total[i]})")

        # 更新学习率（仅对 ReduceLROnPlateau）
        if self.config.scheduler == 'plateau' and split == 'val':
            self.scheduler.step(accuracy)

        return avg_loss, accuracy

    def save_checkpoint(self, epoch, is_best=False):
        """保存检查点"""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'best_acc': self.best_acc,
            'config': {
                'num_classes': self.config.num_classes,
                'use_mask': self.config.use_mask
            }
        }

        # 保存最新检查点
        latest_path = os.path.join(self.save_dir, 'checkpoint_latest.pth')
        torch.save(checkpoint, latest_path)

        # 定期保存
        if (epoch + 1) % 10 == 0:
            period_path = os.path.join(self.save_dir, f'checkpoint_{epoch+1}.pth')
            torch.save(checkpoint, period_path)

        # 保存最佳模型
        if is_best:
            best_path = os.path.join(self.save_dir, 'model_best.pth')
            torch.save(checkpoint, best_path)
            print(f"\n保存最佳模型: {best_path} (Acc: {self.best_acc:.4f})")

    def load_checkpoint(self, path):
        """加载检查点"""
        print(f"加载检查点: {path}")
        checkpoint = torch.load(path, map_location=self.device)

        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        self.best_acc = checkpoint.get('best_acc', 0.0)

        start_epoch = checkpoint['epoch'] + 1
        print(f"从 Epoch {start_epoch} 继续训练")
        print(f"最佳准确率: {self.best_acc:.4f}")

        return start_epoch

    def train(self):
        """完整训练流程"""
        print("\n" + "="*60)
        print("开始训练")
        print("="*60)
        print(f"设备: {self.device}")
        print(f"总 epochs: {self.config.epochs}")
        print(f"Batch size: {self.config.batch_size}")
        print(f"使用掩码: {self.config.use_mask}")
        print("="*60 + "\n")

        start_time = time.time()

        for epoch in range(self.config.epochs):
            # 训练
            train_loss, train_acc = self.train_one_epoch(epoch)

            # 验证
            val_loss, val_acc = self.validate(self.val_loader, epoch, 'val')

            # 打印 epoch 总结
            lr = self.optimizer.param_groups[0]['lr']
            print(f"\nEpoch [{epoch+1}/{self.config.epochs}] 总结:")
            print(f"  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
            print(f"  Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
            print(f"  LR: {lr:.6f}\n")

            # TensorBoard 日志
            self.writer.add_scalar('Train/Loss', train_loss, epoch)
            self.writer.add_scalar('Train/Accuracy', train_acc, epoch)
            self.writer.add_scalar('Val/Loss', val_loss, epoch)
            self.writer.add_scalar('Val/Accuracy', val_acc, epoch)
            self.writer.add_scalar('Train/LR', lr, epoch)

            # 保存最佳模型
            is_best = val_acc > self.best_acc
            if is_best:
                self.best_acc = val_acc
                self.best_epoch = epoch + 1
                self.counter = 0
            else:
                self.counter += 1

            self.save_checkpoint(epoch, is_best)

            # 早停
            if self.counter >= self.patience:
                print(f"\n早停触发！连续 {self.patience} 个 epoch 无提升")
                break

        # 训练结束
        total_time = time.time() - start_time
        print("\n" + "="*60)
        print("训练完成！")
        print(f"总耗时: {total_time/60:.2f} 分钟")
        print(f"最佳验证准确率: {self.best_acc:.4f} (Epoch {self.best_epoch})")
        print("="*60)

        # 最终测试
        print("\n在测试集上评估...")
        test_loss, test_acc = self.validate(self.test_loader, 0, 'test')
        print(f"\n测试集准确率: {test_acc:.4f}")

        self.writer.close()


def main():
    parser = argparse.ArgumentParser(description='裂缝分类训练')
    parser.add_argument('--resume', type=str, default=None,
                        help='恢复训练的检查点路径')
    parser.add_argument('--eval', action='store_true',
                        help='仅评估模式')

    args = parser.parse_args()
    config = Config()

    trainer = Trainer(config, args)

    if args.eval:
        # 仅评估模式
        test_loss, test_acc = trainer.validate(trainer.test_loader, 0, 'test')
        print(f"测试集准确率: {test_acc:.4f}")
    else:
        # 训练模式
        trainer.train()


if __name__ == '__main__':
    main()
