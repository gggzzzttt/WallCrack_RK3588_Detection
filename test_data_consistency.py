#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
测试训练和推理时的数据处理是否一致
"""

import torch
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
import cv2

# 测试图像路径
image_path = 'date/Images/a_0_10.png'
mask_path = 'inference_results/a_0_10_mask_20260619_205321.png'

print("=" * 60)
print("测试训练和推理时的数据处理一致性")
print("=" * 60)

# ============ 训练时的处理方式 ============
print("\n1. 训练时的处理方式:")
print("-" * 60)

# 加载原图
image_train = Image.open(image_path).convert('RGB')
print(f"原图尺寸: {image_train.size}, 模式: {image_train.mode}")

# 加载掩码
mask_train = Image.open(mask_path).convert('L')
print(f"掩码尺寸: {mask_train.size}, 模式: {mask_train.mode}")

# 二值化掩码（训练时的处理）
mask_array = np.array(mask_train)
mask_binary = (mask_array > 127).astype(np.uint8) * 255
mask_train_binary = Image.fromarray(mask_binary)
print(f"二值化后唯一值: {np.unique(np.array(mask_train_binary))}")

# 应用训练时的变换
image_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                       std=[0.229, 0.224, 0.225])
])

mask_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

image_tensor_train = image_transform(image_train)
mask_tensor_train = mask_transform(mask_train_binary)

print(f"\n训练时图像张量:")
print(f"  形状: {image_tensor_train.shape}")
print(f"  数据类型: {image_tensor_train.dtype}")
print(f"  最小值: {image_tensor_train.min():.4f}, 最大值: {image_tensor_train.max():.4f}")
print(f"  均值: {image_tensor_train.mean():.4f}, 标准差: {image_tensor_train.std():.4f}")

print(f"\n训练时掩码张量:")
print(f"  形状: {mask_tensor_train.shape}")
print(f"  数据类型: {mask_tensor_train.dtype}")
print(f"  最小值: {mask_tensor_train.min():.4f}, 最大值: {mask_tensor_train.max():.4f}")
print(f"  均值: {mask_tensor_train.mean():.4f}, 标准差: {mask_tensor_train.std():.4f}")
print(f"  唯一值: {torch.unique(mask_tensor_train)}")

# 组合为4通道输入
combined_train = torch.cat([image_tensor_train, mask_tensor_train], dim=0)
print(f"\n训练时组合张量:")
print(f"  形状: {combined_train.shape}")
print(f"  第4通道（掩码）统计:")
print(f"    最小值: {combined_train[3].min():.4f}, 最大值: {combined_train[3].max():.4f}")
print(f"    均值: {combined_train[3].mean():.4f}")

# ============ 推理时的处理方式 ============
print("\n\n2. 推理时的处理方式:")
print("-" * 60)

# 加载原图
original_image = cv2.imread(image_path)
original_image = original_image[:, :, ::-1]  # BGR -> RGB
print(f"原图尺寸: {original_image.shape}")

# 加载掩码（分割模型输出）
mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
print(f"掩码尺寸: {mask.shape}")
print(f"掩码唯一值: {np.unique(mask)}")

# 调整大小
image_resized = cv2.resize(original_image, (224, 224), interpolation=cv2.INTER_LINEAR)
mask_resized = cv2.resize(mask, (224, 224), interpolation=cv2.INTER_NEAREST)

# 归一化
image_normalized = image_resized.astype(np.float32) / 255.0
image_normalized = (image_normalized - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])

mask_normalized = mask_resized.astype(np.float32) / 255.0

print(f"\n推理时图像张量:")
image_tensor_infer = torch.from_numpy(image_normalized.transpose(2, 0, 1))
print(f"  形状: {image_tensor_infer.shape}")
print(f"  数据类型: {image_tensor_infer.dtype}")
print(f"  最小值: {image_tensor_infer.min():.4f}, 最大值: {image_tensor_infer.max():.4f}")
print(f"  均值: {image_tensor_infer.mean():.4f}, 标准差: {image_tensor_infer.std():.4f}")

print(f"\n推理时掩码张量:")
mask_tensor_infer = torch.from_numpy(mask_normalized).unsqueeze(0)
print(f"  形状: {mask_tensor_infer.shape}")
print(f"  数据类型: {mask_tensor_infer.dtype}")
print(f"  最小值: {mask_tensor_infer.min():.4f}, 最大值: {mask_tensor_infer.max():.4f}")
print(f"  均值: {mask_tensor_infer.mean():.4f}, 标准差: {mask_tensor_infer.std():.4f}")
print(f"  唯一值: {torch.unique(mask_tensor_infer)}")

# 组合为4通道输入
combined_infer = torch.cat([image_tensor_infer, mask_tensor_infer], dim=0)
print(f"\n推理时组合张量:")
print(f"  形状: {combined_infer.shape}")
print(f"  第4通道（掩码）统计:")
print(f"    最小值: {combined_infer[3].min():.4f}, 最大值: {combined_infer[3].max():.4f}")
print(f"    均值: {combined_infer[3].mean():.4f}")

# ============ 比较差异 ============
print("\n\n3. 比较差异:")
print("-" * 60)

diff_image = torch.abs(image_tensor_train - image_tensor_infer)
diff_mask = torch.abs(mask_tensor_train - mask_tensor_infer)

print(f"图像张量差异:")
print(f"  最大差异: {diff_image.max():.6f}")
print(f"  平均差异: {diff_image.mean():.6f}")

print(f"\n掩码张量差异:")
print(f"  最大差异: {diff_mask.max():.6f}")
print(f"  平均差异: {diff_mask.mean():.6f}")

print(f"\n组合张量差异:")
diff_combined = torch.abs(combined_train - combined_infer)
print(f"  最大差异: {diff_combined.max():.6f}")
print(f"  平均差异: {diff_combined.mean():.6f}")

print("\n" + "=" * 60)
