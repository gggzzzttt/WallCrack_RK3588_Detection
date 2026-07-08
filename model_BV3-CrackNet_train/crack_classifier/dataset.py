"""
裂缝分类数据集
支持原图 + 掩码组合输入（4通道）
"""

import os
import json
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms


class CrackClassificationDataset(Dataset):
    """
    裂缝分类数据集

    输入：原图(RGB) + 掩码(灰度) = 4通道
    标签：0-4级裂缝等级
    """

    def __init__(
        self,
        split_file,
        image_dir,
        mask_dir,
        transform=None,
        mask_transform=None,
        use_mask=True,
        mode="train"
    ):
        """
        Args:
            split_file: 划分文件路径 (json)
            image_dir: 原图目录
            mask_dir: 掩码目录
            transform: 原图变换
            mask_transform: 掩码变换
            use_mask: 是否使用掩码
            mode: train/val/test
        """
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform
        self.mask_transform = mask_transform or transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ])
        self.use_mask = use_mask
        self.mode = mode

        # 加载划分文件
        with open(split_file, 'r', encoding='utf-8') as f:
            self.samples = json.load(f)

        print(f"[{mode}] 加载数据: {len(self.samples)} 张")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        filename, label = self.samples[idx]

        # 加载原图
        image_path = os.path.join(self.image_dir, filename)
        try:
            image = Image.open(image_path).convert('RGB')
        except Exception as e:
            # 如果原图不存在，返回一个黑色图像
            print(f"警告: 无法加载原图 {image_path}: {e}")
            image = Image.new('RGB', (224, 224), (0, 0, 0))

        # 加载掩码
        if self.use_mask:
            mask_path = os.path.join(self.mask_dir, str(label), filename)
            try:
                mask = Image.open(mask_path).convert('L')  # 灰度图

                # 二值化掩码（参考分割训练的方式）
                # > 127 的像素为裂缝(1), 否则为背景(0)
                mask_array = np.array(mask)
                mask_binary = (mask_array > 127).astype(np.uint8) * 255
                mask = Image.fromarray(mask_binary)

            except Exception as e:
                # 如果掩码不存在，返回一个全黑掩码
                print(f"警告: 无法加载掩码 {mask_path}: {e}")
                mask = Image.new('L', (224, 224), 0)

            # 应用变换
            if self.transform:
                image = self.transform(image)
            if self.mask_transform:
                mask = self.mask_transform(mask)

            # 组合为4通道输入 [B, 4, H, W]
            combined = torch.cat([image, mask], dim=0)  # [4, H, W]

            return combined, label
        else:
            # 仅使用原图
            if self.transform:
                image = self.transform(image)

            return image, label


def get_train_transforms():
    """训练集数据增强"""
    return transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomCrop((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(
            brightness=0.2,
            contrast=0.2,
            saturation=0.2,
            hue=0.1
        ),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])


def get_val_transforms():
    """验证/测试集变换"""
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])


def get_dataloaders(config, batch_size=None):
    """
    获取数据加载器

    Args:
        config: 配置对象
        batch_size: 批大小，默认使用config中的值

    Returns:
        train_loader, val_loader, test_loader
    """
    if batch_size is None:
        batch_size = config.batch_size

    # 获取划分文件
    train_split = os.path.join(config.split_dir, "train.json")
    val_split = os.path.join(config.split_dir, "val.json")
    test_split = os.path.join(config.split_dir, "test.json")

    # 创建数据集
    train_dataset = CrackClassificationDataset(
        split_file=train_split,
        image_dir=config.image_dir,
        mask_dir=config.mask_dir,
        transform=get_train_transforms() if config.train_augmentation else get_val_transforms(),
        use_mask=config.use_mask,
        mode="train"
    )

    val_dataset = CrackClassificationDataset(
        split_file=val_split,
        image_dir=config.image_dir,
        mask_dir=config.mask_dir,
        transform=get_val_transforms(),
        use_mask=config.use_mask,
        mode="val"
    )

    test_dataset = CrackClassificationDataset(
        split_file=test_split,
        image_dir=config.image_dir,
        mask_dir=config.mask_dir,
        transform=get_val_transforms(),
        use_mask=config.use_mask,
        mode="test"
    )

    # 创建数据加载器
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=config.num_workers,
        pin_memory=True,
        drop_last=True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=config.num_workers,
        pin_memory=True
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=config.num_workers,
        pin_memory=True
    )

    return train_loader, val_loader, test_loader
