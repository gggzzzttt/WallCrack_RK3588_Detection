#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
检查数据集并生成正确格式的标注文件
"""

import os
import os.path as osp
from pathlib import Path


def check_dataset(data_root):
    """检查数据集图像和掩码的对应关系"""
    images_dir = osp.join(data_root, 'Images')
    masks_dir = osp.join(data_root, 'Final_Masks', 'Masks')

    # 获取所有图像文件
    image_files = sorted([f for f in os.listdir(images_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
    mask_files = sorted([f for f in os.listdir(masks_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])

    print(f"图像目录: {images_dir}")
    print(f"掩码目录: {masks_dir}")
    print(f"图像数量: {len(image_files)}")
    print(f"掩码数量: {len(mask_files)}")

    # 检查对应关系
    matched = []
    missing_masks = []

    for img_file in image_files:
        img_name = Path(img_file).stem
        # 尝试不同的掩码命名方式
        possible_mask_names = [
            f"{img_name}.png",
            f"{img_name}_mask.png",
            f"{img_name}_label.png",
        ]

        mask_found = False
        for mask_name in possible_mask_names:
            mask_path = osp.join(masks_dir, mask_name)
            if osp.exists(mask_path):
                matched.append((img_file, mask_name))
                mask_found = True
                break

        if not mask_found:
            missing_masks.append(img_file)

    print(f"\n匹配成功: {len(matched)} 对")
    print(f"缺少掩码: {len(missing_masks)} 个")

    if missing_masks:
        print("\n缺少掩码的图像 (前10个):")
        for f in missing_masks[:10]:
            print(f"  - {f}")

    return matched, missing_masks


def check_mask_values(data_root, sample_files=None, num_samples=5):
    """检查掩码的像素值分布 (需要 cv2 和 numpy)"""
    try:
        import cv2
        import numpy as np
        
        masks_dir = osp.join(data_root, 'Final_Masks', 'Masks')

        if sample_files is None:
            mask_files = sorted([f for f in os.listdir(masks_dir) if f.endswith('.png')])[:num_samples]
        else:
            mask_files = [m for _, m in sample_files[:num_samples]]

        print("\n掩码像素值分析:")
        print("-" * 50)

        unique_values = set()
        for mask_file in mask_files:
            mask_path = osp.join(masks_dir, mask_file)
            mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
            if mask is not None:
                values = np.unique(mask)
                unique_values.update(values)
                print(f"{mask_file}: shape={mask.shape}, unique_values={values}")

        print(f"\n所有掩码的唯一像素值: {sorted(unique_values)}")
        return unique_values
    except ImportError:
        print("\n注意: 未安装 cv2/numpy，跳过掩码像素值检查")
        print("可运行: pip install opencv-python numpy")
        return {0, 255}  # 默认二值分割


def generate_annotation_files(data_root, matched_pairs, train_ratio=0.8):
    """生成正确格式的标注文件"""
    import random

    # 随机打乱
    random.seed(42)
    random.shuffle(matched_pairs)

    # 划分训练集和测试集
    split_idx = int(len(matched_pairs) * train_ratio)
    train_pairs = matched_pairs[:split_idx]
    test_pairs = matched_pairs[split_idx:]

    output_dir = osp.join(data_root, 'Final_Masks')

    # 生成 train.txt
    train_file = osp.join(output_dir, 'train.txt')
    with open(train_file, 'w') as f:
        for img_file, mask_file in train_pairs:
            # 格式: Images/xxx.png,Final_Masks/Masks/xxx.png
            line = f"Images/{img_file},Final_Masks/Masks/{mask_file}\n"
            f.write(line)
    print(f"\n生成训练集标注: {train_file} ({len(train_pairs)} 对)")

    # 生成 test.txt
    test_file = osp.join(output_dir, 'test.txt')
    with open(test_file, 'w') as f:
        for img_file, mask_file in test_pairs:
            line = f"Images/{img_file},Final_Masks/Masks/{mask_file}\n"
            f.write(line)
    print(f"生成测试集标注: {test_file} ({len(test_pairs)} 对)")

    return train_pairs, test_pairs


def main():
    data_root = r'd:\coding\BiSeNet-master\date'

    print("=" * 60)
    print("CrackSeg9k 数据集检查与标注文件生成")
    print("=" * 60)

    # 1. 检查数据集
    matched, missing = check_dataset(data_root)

    if not matched:
        print("\n错误: 没有找到匹配的图像-掩码对!")
        return

    # 2. 检查掩码值
    check_mask_values(data_root, matched)

    # 3. 生成标注文件
    print("\n" + "=" * 60)
    print("生成标注文件...")
    print("=" * 60)
    train_pairs, test_pairs = generate_annotation_files(data_root, matched)

    # 4. 验证生成的文件
    print("\n" + "=" * 60)
    print("验证生成的标注文件")
    print("=" * 60)

    train_file = osp.join(data_root, 'Final_Masks', 'train.txt')
    test_file = osp.join(data_root, 'Final_Masks', 'test.txt')

    print("\ntrain.txt 前5行:")
    with open(train_file, 'r') as f:
        for i, line in enumerate(f.readlines()[:5]):
            print(f"  {line.strip()}")

    print("\ntest.txt 前5行:")
    with open(test_file, 'r') as f:
        for i, line in enumerate(f.readlines()[:5]):
            print(f"  {line.strip()}")

    print("\n完成!")


if __name__ == '__main__':
    main()
