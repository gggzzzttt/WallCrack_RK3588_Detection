#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
测试数据集加载
"""

import sys
sys.path.insert(0, '.')

import os
import os.path as osp
import cv2
import numpy as np

from lib.data.customer_dataset import CustomerDataset
from lib.data.transform_cv2 import TransformationTrain


def test_dataset():
    data_root = r'd:\coding\BiSeNet-master\date'
    train_ann = osp.join(data_root, 'Final_Masks', 'train.txt')

    print("=" * 60)
    print("测试数据集加载")
    print("=" * 60)

    # 创建数据集
    trans_func = TransformationTrain(scales=[0.75, 2.], cropsize=[512, 512])
    ds = CustomerDataset(data_root, train_ann, trans_func=trans_func, mode='train')

    print(f"\n数据集大小: {len(ds)}")

    # 测试加载几个样本
    print("\n加载测试样本...")
    for i in range(3):
        img, label = ds[i]
        print(f"\n样本 {i}:")
        print(f"  图像 shape: {img.shape}, dtype: {img.dtype}")
        print(f"  标签 shape: {label.shape}, dtype: {label.dtype}")
        print(f"  标签唯一值: {np.unique(label.numpy())}")

    print("\n数据集加载测试成功!")
    return True


if __name__ == '__main__':
    test_dataset()
