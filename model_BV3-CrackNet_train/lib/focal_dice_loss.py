#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
Focal Loss + Dice Loss 组合损失函数
用于解决裂缝分割中的类别不均衡问题
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class FocalLoss(nn.Module):
    """
    Focal Loss
    自动降低简单样本权重，聚焦困难样本

    Args:
        alpha: 类别权重，None 表示不使用
        gamma: 困难样本聚焦参数，默认 2.0
        lb_ignore: 忽略的标签值
    """

    def __init__(self, alpha=None, gamma=2.0, lb_ignore=255):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.lb_ignore = lb_ignore

    def forward(self, logits, labels):
        # 计算交叉熵（不进行 reduction）
        ce_loss = F.cross_entropy(logits, labels, ignore_index=self.lb_ignore, reduction='none')

        # 计算 pt（预测正确的概率）
        with torch.no_grad():
            pt = torch.exp(-ce_loss)

        # Focal Loss: 降低简单样本权重
        focal_loss = ((1 - pt) ** self.gamma) * ce_loss

        # 如果有类别权重，应用权重
        if self.alpha is not None:
            alpha_t = self.alpha[labels]
            focal_loss = alpha_t * focal_loss

        # 忽略无效标签
        valid_mask = labels != self.lb_ignore
        focal_loss = focal_loss[valid_mask]

        return focal_loss.mean()


class DiceLoss(nn.Module):
    """
    Dice Loss
    直接优化 IoU 指标，提升裂缝连续性

    Args:
        smooth: 平滑参数，防止除零
        lb_ignore: 忽略的标签值
    """

    def __init__(self, smooth=1.0, lb_ignore=255):
        super(DiceLoss, self).__init__()
        self.smooth = smooth
        self.lb_ignore = lb_ignore

    def forward(self, logits, labels):
        # 获取有效区域
        valid_mask = labels != self.lb_ignore

        # Softmax 获取概率
        probs = F.softmax(logits, dim=1)

        # 对每个类别计算 Dice
        n_classes = logits.shape[1]
        total_loss = 0.0

        for c in range(n_classes):
            # 当前类别的预测和标签
            pred_c = probs[:, c, :, :]
            target_c = (labels == c).float()

            # 只在有效区域计算
            pred_c = pred_c * valid_mask.float()
            target_c = target_c * valid_mask.float()

            # 计算 Dice 系数
            intersection = (pred_c * target_c).sum()
            union = pred_c.sum() + target_c.sum()

            dice = (2.0 * intersection + self.smooth) / (union + self.smooth)
            total_loss += (1.0 - dice)

        return total_loss / n_classes


class FocalDiceLoss(nn.Module):
    """
    Focal Loss + Dice Loss 组合损失

    Args:
        alpha: Focal Loss 的类别权重
        gamma: Focal Loss 的聚焦参数
        focal_weight: Focal Loss 的权重
        dice_weight: Dice Loss 的权重
        lb_ignore: 忽略的标签值
    """

    def __init__(self, alpha=None, gamma=2.0, focal_weight=1.0, dice_weight=1.0, lb_ignore=255):
        super(FocalDiceLoss, self).__init__()
        self.focal_loss = FocalLoss(alpha=alpha, gamma=gamma, lb_ignore=lb_ignore)
        self.dice_loss = DiceLoss(lb_ignore=lb_ignore)
        self.focal_weight = focal_weight
        self.dice_weight = dice_weight

    def forward(self, logits, labels):
        focal = self.focal_loss(logits, labels)
        dice = self.dice_loss(logits, labels)
        return self.focal_weight * focal + self.dice_weight * dice


if __name__ == '__main__':
    # 测试
    logits = torch.randn(2, 2, 256, 256).cuda()
    labels = torch.randint(0, 2, (2, 256, 256)).cuda()

    loss_fn = FocalDiceLoss(gamma=2.0, focal_weight=1.0, dice_weight=1.0).cuda()
    loss = loss_fn(logits, labels)
    print(f'Focal + Dice Loss: {loss.item():.4f}')
