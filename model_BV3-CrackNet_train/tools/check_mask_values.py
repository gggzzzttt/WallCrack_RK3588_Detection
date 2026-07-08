#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
详细检查掩码像素值分布
"""

import os
import os.path as osp
import cv2
import numpy as np
from collections import Counter


def analyze_masks(data_root, num_samples=20):
    """详细分析掩码像素值分布"""
    masks_dir = osp.join(data_root, 'Final_Masks', 'Masks')
    mask_files = sorted([f for f in os.listdir(masks_dir) if f.endswith('.png')])[:num_samples]

    print("=" * 60)
    print("掩码像素值详细分析")
    print("=" * 60)

    all_unique_values = set()
    value_counts = Counter()

    for mask_file in mask_files:
        mask_path = osp.join(masks_dir, mask_file)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        if mask is not None:
            unique_values = np.unique(mask)
            all_unique_values.update(unique_values)

            # 统计每个值的像素数量
            for v in unique_values:
                count = np.sum(mask == v)
                value_counts[v] += count

            print(f"\n{mask_file}:")
            print(f"  Shape: {mask.shape}")
            print(f"  Unique values: {unique_values}")
            print(f"  Min: {mask.min()}, Max: {mask.max()}")

            # 检查是否是二值图像
            if len(unique_values) == 2:
                print(f"  -> 二值图像 (可能是裂缝分割)")
            elif len(unique_values) <= 5:
                print(f"  -> 多类别图像 ({len(unique_values)} 类)")
            else:
                print(f"  -> 灰度图像 (需要二值化)")

    print("\n" + "=" * 60)
    print("总体统计")
    print("=" * 60)
    print(f"所有出现的像素值: {sorted(all_unique_values)}")
    print(f"像素值数量: {len(all_unique_values)}")

    # 判断掩码类型
    if len(all_unique_values) == 2:
        print("\n结论: 掩码是二值图像")
    elif 0 in all_unique_values and 255 in all_unique_values and len(all_unique_values) <= 10:
        print("\n结论: 掩码可能是带有噪声的二值图像")
    else:
        print("\n结论: 掩码是灰度图像，需要二值化处理")


def check_binary_conversion(data_root, threshold=127):
    """检查二值化转换效果"""
    masks_dir = osp.join(data_root, 'Final_Masks', 'Masks')
    mask_files = sorted([f for f in os.listdir(masks_dir) if f.endswith('.png')])[:5]

    print("\n" + "=" * 60)
    print(f"二值化测试 (阈值={threshold})")
    print("=" * 60)

    for mask_file in mask_files:
        mask_path = osp.join(masks_dir, mask_file)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        if mask is not None:
            # 二值化
            binary_mask = (mask > threshold).astype(np.uint8)
            unique_binary = np.unique(binary_mask)

            print(f"\n{mask_file}:")
            print(f"  原始: min={mask.min()}, max={mask.max()}, unique={len(np.unique(mask))}")
            print(f"  二值化后: unique={unique_binary}")
            print(f"  裂缝像素占比: {np.sum(binary_mask == 1) / binary_mask.size * 100:.2f}%")


if __name__ == '__main__':
    data_root = r'd:\coding\BiSeNet-master\date'

    analyze_masks(data_root, num_samples=10)
    check_binary_conversion(data_root, threshold=127)
