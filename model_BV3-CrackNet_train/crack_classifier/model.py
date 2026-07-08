"""
MobileNetV3-Small 裂缝分类模型
支持4通道输入（RGB + 掩码）
"""

import torch
import torch.nn as nn
import torchvision.models as models


class MobileNetV3Classifier(nn.Module):
    """
    MobileNetV3-Small 分类器
    支持多通道输入（3通道或4通道）
    """

    def __init__(self, num_classes=5, in_channels=4, pretrained=False):
        """
        Args:
            num_classes: 分类数
            in_channels: 输入通道数（3=仅RGB, 4=RGB+Mask）
            pretrained: 是否使用预训练权重
        """
        super(MobileNetV3Classifier, self).__init__()

        # 加载预训练模型
        if pretrained:
            # 使用ImageNet预训练权重
            weights = models.MobileNet_V3_Small_Weights.IMAGENET1K_V1
            backbone = models.mobilenet_v3_small(weights=weights)
        else:
            backbone = models.mobilenet_v3_small(weights=None)

        # 修改第一层卷积以支持不同通道数
        original_conv = backbone.features[0][0]
        if in_channels != 3:
            backbone.features[0][0] = nn.Conv2d(
                in_channels,
                original_conv.out_channels,
                kernel_size=original_conv.kernel_size,
                stride=original_conv.stride,
                padding=original_conv.padding,
                bias=False
            )
            # 初始化新通道的权重（复制RGB通道的平均权重）
            if pretrained and in_channels > 3:
                with torch.no_grad():
                    # 对于第4通道（掩码），初始化为较小的权重
                    new_weight = backbone.features[0][0].weight
                    # 复制前3个通道的预训练权重
                    new_weight[:, :3] = original_conv.weight
                    # 第4通道用较小的随机值初始化
                    nn.init.kaiming_normal_(new_weight[:, 3:], mode='fan_out', nonlinearity='relu')

        # 保存特征提取器
        self.features = backbone.features

        # 全局平均池化
        self.avgpool = backbone.avgpool

        # 分类头
        classifier = []
        in_features = backbone.classifier[0].in_features
        classifier.extend([
            nn.Linear(in_features, 1280),
            nn.Hardswish(inplace=True),
            nn.Dropout(p=0.5, inplace=True),  # 增加Dropout
            nn.Linear(1280, num_classes)
        ])
        self.classifier = nn.Sequential(*classifier)

        # 初始化分类头
        for m in self.classifier.modules():
            if isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    def forward(self, x):
        """前向传播"""
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x


def build_model(num_classes=5, in_channels=4, pretrained=True, device='cuda'):
    """
    构建模型

    Args:
        num_classes: 分类数
        in_channels: 输入通道数
        pretrained: 是否使用预训练
        device: 设备

    Returns:
        model: 模型实例
    """
    model = MobileNetV3Classifier(
        num_classes=num_classes,
        in_channels=in_channels,
        pretrained=pretrained
    )

    model = model.to(device)

    # 打印模型信息
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"模型总参数量: {total_params / 1e6:.2f}M")
    print(f"可训练参数量: {trainable_params / 1e6:.2f}M")
    print(f"输入通道数: {in_channels}")
    print(f"分类数: {num_classes}")

    return model
