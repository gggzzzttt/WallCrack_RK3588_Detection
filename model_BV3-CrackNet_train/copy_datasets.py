#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据集一键复制脚本 - RKNN 转换专用

功能：
- 将训练数据集自动复制到 rk3588_deploy/datasets/ 目录
- 智能检测数据源位置
- 默认复制300张图片（分割300张 + 分类每类300张）
- 可直接在 PyCharm 中运行

默认配置：
- 分割数据集：300张（随机采样）
- 分类数据集：每类300张（共1500张）

使用方法：
    # 直接运行（PyCharm 或命令行）
    python copy_datasets.py

    # 自定义数量
    python copy_datasets.py --max-images 500

    # 指定路径
    python copy_datasets.py --seg-path "D:/data/Images" --cls-path "D:/data/mobile_date"

作者: AI Assistant
日期: 2026-06-20
版本: v2.0 (开箱即用版)
"""

import os
import sys
import shutil
import argparse
import random
from pathlib import Path
from typing import List, Tuple, Optional


# ============================================================
# 全局配置 - 可根据需要修改
# ============================================================
DEFAULT_MAX_IMAGES = 300  # 默认复制数量：分割300张，分类每类300张
RANDOM_SEED = 42         # 随机种子，保证可重复性


class DatasetCopier:
    """数据集复制器"""

    def __init__(self, max_images: int = DEFAULT_MAX_IMAGES):
        # 获取当前脚本所在目录 (rk3588_deploy/)
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        # 项目根目录
        self.project_root = os.path.dirname(self.script_dir)
        # 目标数据集目录
        self.target_base = os.path.join(self.script_dir, 'datasets')
        # 最大图片数量
        self.max_images = max_images

        # 类别名称
        self.class_names = ["无裂缝", "轻度裂缝", "中度裂缝", "重度裂缝", "严重裂缝"]

        print("=" * 70)
        print("  RK3588 部署工具包 - 数据集复制助手 v2.0")
        print("=" * 70)
        print(f"\n当前目录: {self.script_dir}")
        print(f"目标目录: {self.target_base}")
        print(f"复制数量: 分割 {self.max_images} 张 + 分类 每类 {self.max_images} 张")

    def _get_search_roots(self) -> List[str]:
        """
        获取搜索根目录列表（按优先级排序）

        数据集实际位置: D:\learn_self\BiSeNet-master\date\Images
                      D:\learn_self\BiSeNet-master\mobile_date\
        项目代码位置:   D:\learn_self\BiSeNet-master\BiSeNet-master\
        """
        roots = []

        # 优先级1: 项目根目录 (BiSeNet-master/BiSeNet-master/)
        roots.append(self.project_root)

        # 优先级2: 项目根目录的上级 (BiSeNet-master/)
        # 这是数据集实际所在的位置
        parent_root = os.path.dirname(self.project_root)
        if parent_root != self.project_root:
            roots.append(parent_root)

        # 优先级3: config.json 中记录的路径
        config_path = os.path.join(self.project_root, 'crack_classifier', 'data_splits', 'config.json')
        if os.path.exists(config_path):
            try:
                import json
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 从 image_dir 推断根目录
                    image_dir = config.get('image_dir', '')
                    if image_dir:
                        # image_dir = "D:/coding/BiSeNet-master/date/Images"
                        # 推断根目录 = 去掉 date/Images 部分
                        for suffix in ['date/Images', 'date\\Images']:
                            if image_dir.replace('\\', '/').endswith(suffix.replace('\\', '/')):
                                inferred_root = image_dir[:-(len(suffix))].rstrip('/\\')
                                if inferred_root not in roots:
                                    roots.append(inferred_root)
                                break
                    # 从 data_root 推断根目录
                    data_root = config.get('data_root', '')
                    if data_root:
                        for suffix in ['mobile_date', 'mobile_date\\']:
                            if data_root.replace('\\', '/').endswith(suffix.replace('\\', '/')):
                                inferred_root = data_root[:-(len(suffix))].rstrip('/\\')
                                if inferred_root not in roots:
                                    roots.append(inferred_root)
                                break
            except Exception:
                pass

        return roots

    def find_segmentation_sources(self) -> List[str]:
        """
        查找分割训练数据集的候选位置

        分割数据集结构:
          date/
          └── Images/     ← 原图 (9159张)
          └── Final_Masks/
              └── Masks/  ← 掩码

        Returns:
            候选路径列表（按优先级排序）
        """
        candidates = []
        search_roots = self._get_search_roots()

        # 在每个搜索根目录下查找
        for root in search_roots:
            common_paths = [
                'date/Images',
                'data/images',
                'images',
                'train_data/images',
                'dataset/images',
            ]

            for path in common_paths:
                full_path = os.path.join(root, path)
                if os.path.exists(full_path) and self._has_images(full_path):
                    if full_path not in candidates:
                        candidates.append(full_path)

        return candidates

    def find_classification_sources(self) -> List[str]:
        """
        查找分类训练数据集的候选位置

        分类数据集结构:
          mobile_date/
          ├── 0/  (无裂缝, 1414张)
          ├── 1/  (轻度裂缝, 2204张)
          ├── 2/  (中度裂缝, 2921张)
          ├── 3/  (重度裂缝, 1681张)
          └── 4/  (严重裂缝, 939张)

        Returns:
            候选路径列表（按优先级排序）
        """
        candidates = []
        search_roots = self._get_search_roots()

        # 在每个搜索根目录下查找
        for root in search_roots:
            common_paths = [
                'mobile_date',
                'data/classification',
                'classification_data',
                'cls_data',
            ]

            for path in common_paths:
                full_path = os.path.join(root, path)
                if os.path.exists(full_path) and self._is_classification_dataset(full_path):
                    if full_path not in candidates:
                        candidates.append(full_path)

        return candidates

    def _has_images(self, directory: str, min_count: int = 10) -> bool:
        """检查目录中是否有足够的图片"""
        if not os.path.isdir(directory):
            return False

        extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}
        count = sum(1 for f in os.listdir(directory)
                   if os.path.splitext(f)[1].lower() in extensions)

        return count >= min_count

    def _is_classification_dataset(self, directory: str) -> bool:
        """检查是否是分类数据集（包含类别子文件夹）"""
        if not os.path.isdir(directory):
            return False

        # 检查是否有数字命名的子文件夹（0-4）
        class_dirs = [d for d in os.listdir(directory)
                     if d.isdigit() and os.path.isdir(os.path.join(directory, d))]

        return len(class_dirs) >= 3  # 至少有3个类别

    def copy_segmentation_dataset(self, source_path: str, max_images: Optional[int] = None) -> bool:
        """
        复制分割训练数据集

        Args:
            source_path: 源数据集路径
            max_images: 最大复制数量（None表示全部）

        Returns:
            是否成功
        """
        target_path = os.path.join(self.target_base, 'date', 'Images')

        print("\n" + "-" * 50)
        print("[分割数据集]")
        print("-" * 50)
        print(f"源路径: {source_path}")
        print(f"目标:   {target_path}")

        # 创建目标目录
        os.makedirs(target_path, exist_ok=True)

        # 收集所有图片
        extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}
        all_files = [f for f in os.listdir(source_path)
                    if os.path.splitext(f)[1].lower() in extensions]

        if len(all_files) == 0:
            print("[ERR] 错误: 未找到任何图片")
            return False

        # 限制数量
        if self.max_images and self.max_images < len(all_files):
            random.seed(RANDOM_SEED)  # 保证可重复性
            files_to_copy = random.sample(all_files, self.max_images)
            print(f"随机选择 {self.max_images}/{len(all_files)} 张图片")
        else:
            files_to_copy = all_files

        # 执行复制
        success_count = 0
        skip_count = 0

        for i, filename in enumerate(files_to_copy, 1):
            src_file = os.path.join(source_path, filename)
            dst_file = os.path.join(target_path, filename)

            # 跳过已存在的文件
            if os.path.exists(dst_file):
                skip_count += 1
                continue

            try:
                shutil.copy2(src_file, dst_file)
                success_count += 1

                # 显示进度
                if i % 50 == 0 or i == len(files_to_copy):
                    progress = i / len(files_to_copy) * 100
                    print(f"  进度: [{i}/{len(files_to_copy)}] ({progress:.1f}%)", end='\r')

            except Exception as e:
                print(f"\n  [ERR] 复制失败: {filename} - {e}")

        print(f"\n[OK] 复制完成!")
        print(f"  - 新增: {success_count} 张")
        print(f"  - 跳过: {skip_count} 张 (已存在)")
        print(f"  - 总计: {success_count + skip_count} 张")

        return True

    def copy_classification_dataset(self, source_path: str, max_images_per_class: Optional[int] = None) -> bool:
        """
        复制分类训练数据集（掩码 + 对应原图）

        分类模型输入是4通道 (RGB + Mask)，所以需要同时复制：
        1. 掩码: mobile_date/{class_id}/{filename} -> datasets/mobile_date/{class_id}/
        2. 原图: date/Images/{filename}            -> datasets/date/Images/

        掩码和原图通过文件名配对（文件名一致）

        Args:
            source_path: 源数据集路径 (mobile_date/)
            max_images_per_class: 每个类别的最大复制数量（默认使用 self.max_images）

        Returns:
            是否成功
        """
        # 使用传入的参数或默认值
        max_per_class = max_images_per_class or self.max_images
        target_base = os.path.join(self.target_base, 'mobile_date')

        # 原图目标目录（分类模型需要原图+掩码配对）
        target_images = os.path.join(self.target_base, 'date', 'Images')

        print("\n" + "-" * 50)
        print("[分类数据集] (掩码 + 原图配对)")
        print("-" * 50)
        print(f"掩码源路径: {source_path}")
        print(f"掩码目标:   {target_base}")
        print(f"原图目标:   {target_images}")

        # 查找原图目录
        image_source_dir = self._find_image_source_dir()
        if image_source_dir:
            print(f"原图源路径: {image_source_dir}")
        else:
            print("[!!] 警告: 未找到原图目录，将只复制掩码（分类量化可能不完整）")

        # 创建目标目录
        os.makedirs(target_images, exist_ok=True)

        total_mask_success = 0
        total_mask_skip = 0
        total_img_success = 0
        total_img_skip = 0
        total_img_missing = 0

        # 遍历每个类别
        class_ids = sorted([d for d in os.listdir(source_path) if d.isdigit()], key=int)

        if len(class_ids) == 0:
            print("[ERR] 错误: 未找到类别目录 (0/, 1/, ...)")
            return False

        for class_id in class_ids:
            class_name = self.class_names[int(class_id)] if int(class_id) < 5 else f"类别{class_id}"
            source_class_dir = os.path.join(source_path, class_id)
            target_class_dir = os.path.join(target_base, class_id)

            print(f"\n  >> 类别 {class_id}: {class_name}")

            # 创建目标目录
            os.makedirs(target_class_dir, exist_ok=True)

            # 收集该类别的所有图片
            extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}
            all_files = [f for f in os.listdir(source_class_dir)
                        if os.path.splitext(f)[1].lower() in extensions]

            if len(all_files) == 0:
                print(f"    [!!] 空目录，跳过")
                continue

            # 限制数量
            if max_per_class and max_per_class < len(all_files):
                random.seed(RANDOM_SEED)
                files_to_copy = random.sample(all_files, max_per_class)
            else:
                files_to_copy = all_files

            # 执行复制
            mask_success = 0
            mask_skip = 0
            img_success = 0
            img_skip = 0
            img_missing = 0

            for filename in files_to_copy:
                # 1. 复制掩码
                src_file = os.path.join(source_class_dir, filename)
                dst_file = os.path.join(target_class_dir, filename)

                if os.path.exists(dst_file):
                    mask_skip += 1
                else:
                    try:
                        shutil.copy2(src_file, dst_file)
                        mask_success += 1
                    except Exception as e:
                        pass

                # 2. 复制对应的原图（文件名相同）
                if image_source_dir:
                    src_img = os.path.join(image_source_dir, filename)
                    dst_img = os.path.join(target_images, filename)

                    if os.path.exists(dst_img):
                        img_skip += 1
                    elif os.path.exists(src_img):
                        try:
                            shutil.copy2(src_img, dst_img)
                            img_success += 1
                        except Exception as e:
                            pass
                    else:
                        img_missing += 1

            total_mask_success += mask_success
            total_mask_skip += mask_skip
            total_img_success += img_success
            total_img_skip += img_skip
            total_img_missing += img_missing

            print(f"    [OK] 掩码: 新增{mask_success}, 跳过{mask_skip} | 原图: 新增{img_success}, 跳过{img_skip}, 缺失{img_missing}")

        print(f"\n[OK] 分类数据集复制完成!")
        print(f"  - 掩码: 新增{total_mask_success}, 跳过{total_mask_skip}, 总计{total_mask_success + total_mask_skip}")
        print(f"  - 原图: 新增{total_img_success}, 跳过{total_img_skip}, 缺失{total_img_missing}")
        print(f"  - 类别数: {len(class_ids)} 个")

        return True

    def _find_image_source_dir(self) -> Optional[str]:
        """
        查找原图目录 (date/Images/)

        Returns:
            原图目录路径，找不到返回 None
        """
        search_roots = self._get_search_roots()

        for root in search_roots:
            img_dir = os.path.join(root, 'date', 'Images')
            if os.path.exists(img_dir) and self._has_images(img_dir):
                return img_dir

        return None

    def run_auto(self):
        """
        自动运行模式（默认）- 无需交互

        自动查找数据集并复制，使用默认配置：
        - 分割：300张
        - 分类：每类300张
        """
        print("\n" + "=" * 70)
        print("  [OK] 自动模式启动 - 使用默认配置")
        print("=" * 70)
        print(f"\n配置信息:")
        print(f"  - 分割数据集: {self.max_images} 张 (随机采样)")
        print(f"  - 分类数据集: 每类 {self.max_images} 张 (随机采样)")
        print(f"  - 随机种子: {RANDOM_SEED} (保证可重复性)")

        success_seg = False
        success_cls = False

        # ====== 复制分割数据集 ======
        seg_sources = self.find_segmentation_sources()
        if seg_sources:
            print(f"\n{'='*50}")
            print(f"[OK] 找到分割数据集源:")
            for i, src in enumerate(seg_sources, 1):
                count = len([f for f in os.listdir(src) if os.path.splitext(f)[1].lower() in {'.png', '.jpg'}])
                print(f"  [{i}] {src}")
                print(f"      图片数量: {count} 张")

            # 自动选择第一个找到的源
            selected_source = seg_sources[0]
            print(f"\n>> 自动选择: {selected_source}")
            success_seg = self.copy_segmentation_dataset(selected_source)
        else:
            print("\n" + "!" * 50)
            print("[!!] 未找到分割数据集")
            print("  跳过分割数据集复制...")
            print("  提示: 可使用 --seg-path 手动指定路径")

        # ====== 复制分类数据集 ======
        cls_sources = self.find_classification_sources()
        if cls_sources:
            print(f"\n{'='*50}")
            print(f"[OK] 找到分类数据集源:")
            for i, src in enumerate(cls_sources, 1):
                class_dirs = [d for d in os.listdir(src) if d.isdigit()]
                print(f"  [{i}] {src}")
                print(f"      类别数: {len(class_dirs)} 个")

            # 自动选择第一个找到的源
            selected_source = cls_sources[0]
            print(f"\n>> 自动选择: {selected_source}")
            success_cls = self.copy_classification_dataset(selected_source)
        else:
            print("\n" + "!" * 50)
            print("[!!] 未找到分类数据集")
            print("  跳过分类数据集复制...")
            print("  提示: 可使用 --cls-path 手动指定路径")

        # ====== 结果汇总 ======
        print("\n" + "=" * 70)
        if success_seg or success_cls:
            print("  [OK] 数据集准备完成!")
        else:
            print("  [!!] 未复制任何数据集")
            print("  请检查数据集路径或使用 --seg-path / --cls-path 指定")
        print("=" * 70)

        return success_seg or success_cls

    def interactive_mode(self):
        """交互式模式：让用户选择数据源"""
        print("\n" + "=" * 70)
        print("  [MENU] 请选择要执行的操作:")
        print("=" * 70)
        print()
        print("  [1] 复制分割数据集 + 分类数据集 (推荐)")
        print("  [2] 仅复制分割数据集")
        print("  [3] 仅复制分类数据集")
        print("  [4] 自定义路径")
        print("  [q] 退出")
        print()

        choice = input("  请输入选项 [1/2/3/4/q]: ").strip()

        if choice == 'q':
            print("\n[EXIT] 已取消操作")
            sys.exit(0)

        elif choice == '1':
            self._copy_both_auto()

        elif choice == '2':
            self._copy_segmentation_auto()

        elif choice == '3':
            self._copy_classification_auto()

        elif choice == '4':
            self._custom_path_mode()

        else:
            print("\n[ERR] 无效选项，请重新运行")
            sys.exit(1)

    def _copy_both_auto(self):
        """自动查找并复制两种数据集"""
        max_imgs = self._ask_max_images()

        # 分割数据集
        seg_sources = self.find_segmentation_sources()
        if seg_sources:
            print(f"\n找到分割数据集候选:")
            for i, src in enumerate(seg_sources, 1):
                count = len([f for f in os.listdir(src) if os.path.splitext(f)[1].lower() in {'.png', '.jpg'}])
                print(f"  [{i}] {src} ({count} 张)")

            choice = input(f"选择哪个? [1-{len(seg_sources)}]: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(seg_sources):
                self.copy_segmentation_dataset(seg_sources[idx], max_imgs)
        else:
            print("\n[!!] 未找到分割数据集")
            print("请使用选项 [4] 手动指定路径")

        # 分类数据集
        cls_sources = self.find_classification_sources()
        if cls_sources:
            print(f"\n找到分类数据集候选:")
            for i, src in enumerate(cls_sources, 1):
                class_dirs = [d for d in os.listdir(src) if d.isdigit()]
                print(f"  [{i}] {src} ({len(class_dirs)} 个类别)")

            choice = input(f"选择哪个? [1-{len(cls_sources)}]: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(cls_sources):
                self.copy_classification_dataset(cls_sources[idx], max_imgs)
        else:
            print("\n[!!] 未找到分类数据集")
            print("请使用选项 [4] 手动指定路径")

    def _copy_segmentation_auto(self):
        """仅复制分割数据集"""
        max_imgs = self._ask_max_images()
        seg_sources = self.find_segmentation_sources()

        if not seg_sources:
            print("\n[ERR] 未找到分割数据集")
            print("提示: 请确保 date/Images/ 目录存在且包含图片")
            sys.exit(1)

        print(f"\n找到 {len(seg_sources)} 个候选:")
        for i, src in enumerate(seg_sources, 1):
            count = len([f for f in os.listdir(src)])
            print(f"  [{i}] {src} ({count} 张)")

        choice = input(f"选择 [1-{len(seg_sources)}]: ").strip()
        idx = int(choice) - 1
        self.copy_segmentation_dataset(seg_sources[idx], max_imgs)

    def _copy_classification_auto(self):
        """仅复制分类数据集"""
        max_imgs = self._ask_max_images()
        cls_sources = self.find_classification_sources()

        if not cls_sources:
            print("\n[ERR] 未找到分类数据集")
            print("提示: 请确保 mobile_date/ 目录存在且包含 0/, 1/, ... 子目录")
            sys.exit(1)

        print(f"\n找到 {len(cls_sources)} 个候选:")
        for i, src in enumerate(cls_sources, 1):
            class_dirs = [d for d in os.listdir(src) if d.isdigit()]
            print(f"  [{i}] {src} ({len(class_dirs)} 个类别)")

        choice = input(f"选择 [1-{len(cls_sources)}]: ").strip()
        idx = int(choice) - 1
        self.copy_classification_dataset(cls_sources[idx], max_imgs)

    def _custom_path_mode(self):
        """自定义路径模式"""
        print("\n" + "-" * 50)
        print("自定义路径模式")
        print("-" * 50)

        seg_path = input("\n分割数据集路径 (留空跳过): ").strip().strip('"')
        cls_path = input("分类数据集路径 (留空跳过): ").strip().strip('"')
        max_imgs = self._ask_max_images()

        if seg_path and os.path.exists(seg_path):
            self.copy_segmentation_dataset(seg_path, max_imgs)
        elif seg_path:
            print(f"\n[ERR] 路径不存在: {seg_path}")

        if cls_path and os.path.exists(cls_path):
            self.copy_classification_dataset(cls_path, max_imgs)
        elif cls_path:
            print(f"\n[ERR] 路径不存在: {cls_path}")

        if not seg_path and not cls_path:
            print("\n[ERR] 至少需要指定一个路径")
            sys.exit(1)

    def _ask_max_images(self) -> Optional[int]:
        """询问最大图片数量"""
        answer = input("\n限制每个类别/总数量? [直接回车=不限制, 输入数字=限制数量]: ").strip()
        if answer.isdigit():
            return int(answer)
        return None

    def show_summary(self):
        """显示最终摘要"""
        print("\n" + "=" * 70)
        print("  [OK] 数据集复制完成!")
        print("=" * 70)

        # 统计信息
        seg_target = os.path.join(self.target_base, 'date', 'Images')
        cls_target = os.path.join(self.target_base, 'mobile_date')

        print("\n[STAT] 目标目录统计:")
        print("-" * 50)

        # 分割数据集
        if os.path.exists(seg_target):
            seg_count = len([f for f in os.listdir(seg_target)
                           if os.path.splitext(f)[1].lower() in {'.png', '.jpg', '.jpeg'}])
            size_mb = sum(os.path.getsize(os.path.join(seg_target, f))
                         for f in os.listdir(seg_target)) / (1024*1024)
            print(f"  [OK] 分割数据集: {seg_count} 张 ({size_mb:.1f} MB)")
            print(f"    路径: datasets/date/Images/")
        else:
            print(f"  -- 分割数据集: 未创建")

        # 分类数据集
        if os.path.exists(cls_target):
            cls_total = 0
            class_dirs = [d for d in os.listdir(cls_target) if d.isdigit()]
            for class_id in sorted(class_dirs, key=int):
                class_dir = os.path.join(cls_target, class_id)
                count = len(os.listdir(class_dir))
                cls_total += count
                name = self.class_names[int(class_id)] if int(class_id) < 5 else f"类别{class_id}"
                print(f"    - {name} ({class_id}/): {count} 张")

            print(f"  [OK] 分类数据集: {cls_total} 张 ({len(class_dirs)} 个类别)")
            print(f"    路径: datasets/mobile_date/")
        else:
            print(f"  -- 分类数据集: 未创建")

        print("\n[NEXT] 下一步:")
        print("  1. 运行 deploy.bat 开始转换模型")
        print("  2. 或手动运行 prepare_quantization_data.py 准备量化数据")
        print()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='数据集一键复制工具 v2.0 - 将训练数据复制到 rk3588_deploy/datasets/\n\n'
                    '默认行为: 直接运行即可自动复制300张数据（分割+分类）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # ========== 最简单：直接运行 ==========
  python copy_datasets.py
  # 或在 PyCharm 中右键运行

  # ========== 自定义数量 ==========
  python copy_datasets.py --max-images 500

  # ========== 指定路径 ==========
  python copy_datasets.py --seg-path "D:/data/Images" --cls-path "D:/data/mobile_date"

  # ========== 交互式模式（可选）==========
  python copy_datasets.py --interactive

  # ========== 仅复制一种类型 ==========
  python copy_datasets.py --type segmentation
  python copy_datasets.py --type classification
        """
    )

    parser.add_argument('--seg-path', type=str,
                       help='分割数据集源路径 (date/Images/)')
    parser.add_argument('--cls-path', type=str,
                       help='分类数据集源路径 (mobile_date/)')
    parser.add_argument('--type', type=str, choices=['segmentation', 'classification', 'both'],
                       default='both',
                       help='要复制的数据集类型 (默认: both)')
    parser.add_argument('--max-images', type=int, default=DEFAULT_MAX_IMAGES,
                       help=f'最大复制图片数量 (默认: {DEFAULT_MAX_IMAGES})')
    parser.add_argument('--interactive', action='store_true',
                       help='启用交互式模式（需要手动选择）')

    args = parser.parse_args()

    # 创建复制器实例（使用指定的或默认的数量）
    copier = DatasetCopier(max_images=args.max_images)

    # 判断运行模式
    if args.interactive:
        # 交互式模式
        copier.interactive_mode()
    elif args.seg_path or args.cls_path:
        # 命令行模式：使用指定路径
        print("\n[命令行模式]\n")

        if args.type in ['segmentation', 'both'] and args.seg_path:
            copier.copy_segmentation_dataset(args.seg_path, args.max_images)

        if args.type in ['classification', 'both'] and args.cls_path:
            copier.copy_classification_dataset(args.cls_path)

        copier.show_summary()
    else:
        # ========== 默认：自动运行模式 ==========
        print("\n[自动模式] 直接运行，使用默认配置\n")
        success = copier.run_auto()
        if success:
            copier.show_summary()


if __name__ == '__main__':
    main()
