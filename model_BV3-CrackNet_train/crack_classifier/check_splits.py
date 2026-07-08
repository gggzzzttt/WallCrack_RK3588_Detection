#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
检查并清理数据划分文件
移除不存在的文件
"""

import os
import json
from pathlib import Path


def check_and_clean_splits():
    """检查并清理数据划分文件"""

    # 项目根目录
    project_root = Path(__file__).parent.parent

    # 路径
    image_dir = project_root / "date" / "Images"
    mask_dir = project_root / "date" / "Final_Masks" / "Masks"
    split_dir = project_root / "crack_classifier" / "data_splits"

    print("=" * 60)
    print("检查数据划分文件")
    print("=" * 60)
    print(f"原图目录: {image_dir}")
    print(f"掩码目录: {mask_dir}")
    print(f"划分文件目录: {split_dir}")
    print("=" * 60)

    # 统计信息
    total_stats = {
        'total': 0,
        'valid': 0,
        'missing_image': 0,
        'missing_mask': 0
    }

    # 处理每个划分文件
    for split_name in ["train", "val", "test"]:
        split_file = split_dir / f"{split_name}.json"

        if not split_file.exists():
            print(f"\n警告: 划分文件不存在: {split_file}")
            continue

        print(f"\n检查 {split_name} 数据...")

        with open(split_file, 'r', encoding='utf-8') as f:
            samples = json.load(f)

        valid_samples = []
        missing_image = 0
        missing_mask = 0

        for filename, label in samples:
            total_stats['total'] += 1

            # 检查原图
            image_path = image_dir / filename
            if not image_path.exists():
                missing_image += 1
                total_stats['missing_image'] += 1
                continue

            # 检查掩码
            mask_path = mask_dir / filename
            if not mask_path.exists():
                missing_mask += 1
                total_stats['missing_mask'] += 1
                continue

            # 文件都存在，保留
            valid_samples.append([filename, label])
            total_stats['valid'] += 1

        # 保存清理后的划分文件
        if len(valid_samples) < len(samples):
            print(f"  原始样本数: {len(samples)}")
            print(f"  有效样本数: {len(valid_samples)}")
            print(f"  缺失原图: {missing_image}")
            print(f"  缺失掩码: {missing_mask}")

            # 备份原文件
            backup_file = split_dir / f"{split_name}_backup.json"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(samples, f, ensure_ascii=False, indent=2)
            print(f"  已备份原文件: {backup_file}")

            # 保存清理后的文件
            with open(split_file, 'w', encoding='utf-8') as f:
                json.dump(valid_samples, f, ensure_ascii=False, indent=2)
            print(f"  已保存清理后的文件: {split_file}")
        else:
            print(f"  所有文件都存在: {len(samples)} 张")

    # 打印总统计
    print("\n" + "=" * 60)
    print("总统计")
    print("=" * 60)
    print(f"总样本数: {total_stats['total']}")
    print(f"有效样本数: {total_stats['valid']}")
    print(f"缺失原图: {total_stats['missing_image']}")
    print(f"缺失掩码: {total_stats['missing_mask']}")
    print("=" * 60)


if __name__ == "__main__":
    check_and_clean_splits()
