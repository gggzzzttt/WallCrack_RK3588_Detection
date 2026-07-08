"""
数据集划分脚本
将分类数据集划分为训练集、验证集、测试集（分层抽样）
"""

import os
import json
import random
from collections import defaultdict

def split_dataset(
    data_root="D:/coding/BiSeNet-master/mobile_date",
    output_dir="D:/coding/BiSeNet-master/crack_classifier/data_splits",
    train_ratio=0.8,
    val_ratio=0.1,
    test_ratio=0.1,
    seed=42
):
    """
    划分数据集

    Args:
        data_root: 分类数据根目录（包含0-4个子文件夹）
        output_dir: 输出目录
        train_ratio: 训练集比例
        val_ratio: 验证集比例
        test_ratio: 测试集比例
        seed: 随机种子
    """

    # 设置随机种子
    random.seed(seed)

    # 确保比例之和为1
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, "比例之和必须为1"

    # 收集每个类别的文件
    class_files = defaultdict(list)
    for class_id in range(5):
        class_dir = os.path.join(data_root, str(class_id))
        if os.path.exists(class_dir):
            files = [f for f in os.listdir(class_dir) if f.endswith('.png')]
            class_files[class_id] = files
            print(f"类别 {class_id}: {len(files)} 张")

    # 分层抽样
    splits = {"train": [], "val": [], "test": []}

    for class_id in range(5):
        files = class_files[class_id]
        random.shuffle(files)

        n = len(files)
        n_train = int(n * train_ratio)
        n_val = int(n * val_ratio)
        # 剩余的给测试集

        splits["train"].extend([(f, class_id) for f in files[:n_train]])
        splits["val"].extend([(f, class_id) for f in files[n_train:n_train+n_val]])
        splits["test"].extend([(f, class_id) for f in files[n_train+n_val:]])

    # 打乱顺序
    for split_name in splits:
        random.shuffle(splits[split_name])

    # 统计信息
    print("\n=== 划分结果 ===")
    for split_name in ["train", "val", "test"]:
        print(f"\n{split_name}: {len(splits[split_name])} 张")
        class_counts = defaultdict(int)
        for _, label in splits[split_name]:
            class_counts[label] += 1
        for cls_id in sorted(class_counts.keys()):
            print(f"  类别 {cls_id}: {class_counts[cls_id]} 张")

    # 保存划分结果
    os.makedirs(output_dir, exist_ok=True)
    for split_name in ["train", "val", "test"]:
        output_file = os.path.join(output_dir, f"{split_name}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(splits[split_name], f, ensure_ascii=False, indent=2)
        print(f"\n已保存: {output_file}")

    # 保存配置信息
    config = {
        "data_root": data_root,
        "image_dir": "D:/coding/BiSeNet-master/date/Images",  # 原图目录
        "mask_dir": data_root,  # 掩码目录
        "train_ratio": train_ratio,
        "val_ratio": val_ratio,
        "test_ratio": test_ratio,
        "seed": seed,
        "num_classes": 5,
        "class_names": ["无裂缝", "轻度裂缝", "中度裂缝", "重度裂缝", "严重裂缝"]
    }
    config_file = os.path.join(output_dir, "config.json")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(f"\n已保存配置: {config_file}")

    return splits


if __name__ == "__main__":
    split_dataset()
