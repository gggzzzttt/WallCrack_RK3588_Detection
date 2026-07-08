"""
准备RKNN量化校准数据
从数据集中随机抽取图片用于量化校准
"""

import os
import sys
import random
import argparse
import json
import shutil

import cv2
import numpy as np


def prepare_segmentation_calibration(image_dir, output_dir, num_images=100):
    """
    准备分割模型校准数据
    
    Args:
        image_dir: 图片目录
        output_dir: 输出目录
        num_images: 校准图片数量
    """
    print(f"准备分割模型校准数据...")
    
    # 创建输出目录
    seg_calib_dir = os.path.join(output_dir, 'segmentation')
    os.makedirs(seg_calib_dir, exist_ok=True)
    
    # 获取所有图片
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
        image_files.extend(
            [os.path.join(image_dir, f) for f in os.listdir(image_dir) 
             if f.lower().endswith(ext.replace('*', ''))]
        )
    
    print(f"找到 {len(image_files)} 张图片")
    
    # 随机选择
    selected = random.sample(image_files, min(num_images, len(image_files)))
    
    # 复制图片
    for i, img_path in enumerate(selected):
        # 读取并预处理
        img = cv2.imread(img_path)
        img = cv2.resize(img, (1024, 1024))
        
        # 保存
        output_path = os.path.join(seg_calib_dir, f'calib_{i:04d}.jpg')
        cv2.imwrite(output_path, img)
    
    # 生成校准数据列表文件
    list_file = os.path.join(output_dir, 'segmentation_calib_list.txt')
    with open(list_file, 'w') as f:
        for img_file in os.listdir(seg_calib_dir):
            f.write(os.path.join(seg_calib_dir, img_file) + '\n')
    
    print(f"✅ 分割模型校准数据准备完成: {len(selected)} 张")
    print(f"   保存路径: {seg_calib_dir}")
    print(f"   列表文件: {list_file}")


def prepare_classifier_calibration(image_dir, mask_dir, split_file, output_dir, num_images=100):
    """
    准备分类模型校准数据
    
    Args:
        image_dir: 原图目录
        mask_dir: 掩码目录
        split_file: 数据划分文件
        output_dir: 输出目录
        num_images: 校准图片数量
    """
    print(f"准备分类模型校准数据...")
    
    # 创建输出目录
    cls_calib_dir = os.path.join(output_dir, 'classifier')
    os.makedirs(cls_calib_dir, exist_ok=True)
    
    # 加载数据划分
    with open(split_file, 'r') as f:
        data = json.load(f)
    
    train_data = data['train']
    print(f"训练集大小: {len(train_data)}")
    
    # 随机选择
    selected = random.sample(train_data, min(num_images, len(train_data)))
    
    # 处理图片
    for i, item in enumerate(selected):
        # 读取原图
        img_path = os.path.join(image_dir, item['image'])
        img = cv2.imread(img_path)
        img = cv2.resize(img, (224, 224))
        
        # 读取掩码
        mask_path = os.path.join(mask_dir, item['mask'])
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        mask = cv2.resize(mask, (224, 224))
        
        # 合并为4通道
        img_rgb = img[:, :, ::-1]  # BGR -> RGB
        combined = np.concatenate([img_rgb, mask[:, :, np.newaxis]], axis=2)
        
        # 保存为npy格式
        output_path = os.path.join(cls_calib_dir, f'calib_{i:04d}.npy')
        np.save(output_path, combined.astype(np.float32) / 255.0)
    
    # 生成校准数据列表文件
    list_file = os.path.join(output_dir, 'classifier_calib_list.txt')
    with open(list_file, 'w') as f:
        for npy_file in os.listdir(cls_calib_dir):
            f.write(os.path.join(cls_calib_dir, npy_file) + '\n')
    
    print(f"✅ 分类模型校准数据准备完成: {len(selected)} 张")
    print(f"   保存路径: {cls_calib_dir}")
    print(f"   列表文件: {list_file}")


def main():
    parser = argparse.ArgumentParser(description='准备RKNN量化校准数据')
    parser.add_argument('--image-dir', type=str, 
                        default='../date/Images',
                        help='原图目录')
    parser.add_argument('--mask-dir', type=str, 
                        default='../mobile_date',
                        help='掩码目录')
    parser.add_argument('--split-file', type=str, 
                        default='../crack_classifier/data_splits/train.json',
                        help='数据划分文件')
    parser.add_argument('--output-dir', type=str, 
                        default='./calibration_data',
                        help='输出目录')
    parser.add_argument('--num-images', type=int, default=100,
                        help='校准图片数量')
    
    args = parser.parse_args()
    
    # 准备分割模型校准数据
    prepare_segmentation_calibration(
        args.image_dir,
        args.output_dir,
        args.num_images
    )
    
    # 准备分类模型校准数据
    prepare_classifier_calibration(
        args.image_dir,
        args.mask_dir,
        args.split_file,
        args.output_dir,
        args.num_images
    )
    
    print("\n" + "="*60)
    print("✅ 所有校准数据准备完成！")
    print("="*60)
    print("\n使用方法:")
    print("  RKNN量化时指定校准数据列表文件:")
    print(f"  - 分割模型: {os.path.join(args.output_dir, 'segmentation_calib_list.txt')}")
    print(f"  - 分类模型: {os.path.join(args.output_dir, 'classifier_calib_list.txt')}")


if __name__ == '__main__':
    main()
