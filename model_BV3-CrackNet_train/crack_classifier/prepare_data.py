#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
数据准备脚本
将现有的裂缝数据转换为分类器期望的格式

现有数据结构:
- date/Images/ - 原图
- date/Final_Masks/Masks/ - 掩码
- crack_classifier/data_splits/train.json - 数据划分（包含标签信息）

期望的数据结构:
- mobile_date/0/ - 无裂缝的掩码
- mobile_date/1/ - 轻度裂缝的掩码
- mobile_date/2/ - 中度裂缝的掩码
- mobile_date/3/ - 重度裂缝的掩码
- mobile_date/4/ - 严重裂缝的掩码
"""

import os
import json
import shutil
from pathlib import Path


def prepare_classification_data():
    """准备分类数据"""

    # 项目根目录
    project_root = Path(__file__).parent.parent

    # 输入路径
    image_dir = project_root / "date" / "Images"
    mask_dir = project_root / "date" / "Final_Masks" / "Masks"
    split_dir = project_root / "crack_classifier" / "data_splits"

    # 输出路径
    output_dir = project_root / "mobile_date"

    print("=" * 60)
    print("准备裂缝分类数据")
    print("=" * 60)
    print(f"原图目录: {image_dir}")
    print(f"掩码目录: {mask_dir}")
    print(f"划分文件: {split_dir}")
    print(f"输出目录: {output_dir}")
    print("=" * 60)

    # 创建输出目录
    for class_id in range(5):
        class_dir = output_dir / str(class_id)
        class_dir.mkdir(parents=True, exist_ok=True)
        print(f"创建目录: {class_dir}")

    # 统计信息
    stats = {i: 0 for i in range(5)}

    # 处理每个划分文件
    for split_name in ["train", "val", "test"]:
        split_file = split_dir / f"{split_name}.json"

        if not split_file.exists():
            print(f"\n警告: 划分文件不存在: {split_file}")
            continue

        print(f"\n处理 {split_name} 数据...")

        with open(split_file, 'r', encoding='utf-8') as f:
            samples = json.load(f)

        for filename, label in samples:
            # 源掩码路径
            src_mask = mask_dir / filename

            # 目标掩码路径
            dst_mask = output_dir / str(label) / filename

            # 复制文件
            if src_mask.exists():
                shutil.copy2(src_mask, dst_mask)
                stats[label] += 1
            else:
                print(f"  警告: 掩码文件不存在: {src_mask}")

    # 打印统计信息
    print("\n" + "=" * 60)
    print("数据准备完成！")
    print("=" * 60)
    print("各类别数据统计:")
    class_names = ["无裂缝", "轻度裂缝", "中度裂缝", "重度裂缝", "严重裂缝"]
    for class_id in range(5):
        print(f"  类别 {class_id} ({class_names[class_id]}): {stats[class_id]} 张")

    print(f"\n总计: {sum(stats.values())} 张掩码")
    print(f"输出目录: {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    prepare_classification_data()
