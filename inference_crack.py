#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
裂缝分割+分类推理脚本
流程：
1. 使用BiSeNetV2进行裂缝分割
2. 将原图+分割掩码组合成4通道输入
3. 使用MobileNetV3进行裂缝等级分类
4. 可视化并保存结果

使用方法:
    python inference_crack.py --image image.png
"""

import sys
import os
import argparse
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
import numpy as np
import cv2
import json
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lib.data.transform_cv2 as T
from lib.models import model_factory
from configs import set_cfg_from_file
from crack_classifier.model import MobileNetV3Classifier


# 禁用梯度计算
torch.set_grad_enabled(False)
np.random.seed(123)


class CrackInferencePipeline:
    """裂缝分割+分类推理管道"""

    def __init__(self,
                 seg_config='configs/bisenetv2_crack.py',
                 seg_weight='res_3/crack_bisenetv2/model_best.pth',
                 cls_weight='crack_classifier/res/crack_classifier/mobilenetv3_small/model_best.pth',
                 device='cuda'):
        """
        初始化推理管道

        Args:
            seg_config: 分割模型配置文件
            seg_weight: 分割模型权重
            cls_weight: 分类模型权重
            device: 运行设备
        """
        self.device = device

        # 类别名称
        self.class_names = ["无裂缝", "轻度裂缝", "中度裂缝", "重度裂缝", "严重裂缝"]

        # 颜色调色板（分割可视化）
        self.palette = np.array([
            [0, 0, 0],        # 背景 - 黑色
            [255, 255, 255],  # 裂缝 - 白色
        ], dtype=np.uint8)

        print("=" * 60)
        print("初始化裂缝分割+分类推理管道")
        print("=" * 60)

        # 加载分割模型
        self.load_segmentation_model(seg_config, seg_weight)

        # 加载分类模型
        self.load_classification_model(cls_weight)

        print("✓ 所有模型加载完成！")
        print("=" * 60)

    def load_segmentation_model(self, config_path, weight_path):
        """加载分割模型"""
        print(f"\n[1/2] 加载分割模型...")
        print(f"  配置文件: {config_path}")
        print(f"  权重文件: {weight_path}")

        # 加载配置
        self.seg_cfg = set_cfg_from_file(config_path)

        # 创建模型（不加载预训练backbone，直接使用用户训练好的权重）
        self.seg_model = model_factory[self.seg_cfg.model_type](
            self.seg_cfg.n_cats,
            aux_mode='eval',
            load_pretrain_backbone=False  # 不下载预训练权重
        )

        # 加载权重
        state_dict = torch.load(weight_path, map_location='cpu')
        self.seg_model.load_state_dict(state_dict, strict=False)
        self.seg_model.eval()
        self.seg_model.to(self.device)

        print(f"  ✓ 分割模型加载成功 (类别数: {self.seg_cfg.n_cats})")

    def load_classification_model(self, weight_path):
        """加载分类模型"""
        print(f"\n[2/2] 加载分类模型...")
        print(f"  权重文件: {weight_path}")

        # 创建模型（4通道输入：RGB + Mask）
        self.cls_model = MobileNetV3Classifier(
            num_classes=5,
            in_channels=4,
            pretrained=False
        )

        # 加载权重
        checkpoint = torch.load(weight_path, map_location='cpu')

        # 检查是否是checkpoint格式
        if 'model_state_dict' in checkpoint:
            # 是checkpoint格式，提取模型权重
            state_dict = checkpoint['model_state_dict']
            print(f"  权重文件是checkpoint格式")
            if 'epoch' in checkpoint:
                print(f"  训练轮数: {checkpoint['epoch']}")
            if 'best_acc' in checkpoint:
                print(f"  最佳准确率: {checkpoint['best_acc']:.4f}")
        else:
            # 是纯模型权重格式
            state_dict = checkpoint
            print(f"  权重文件是纯模型权重格式")

        # 打印权重信息
        print(f"  模型权重包含 {len(state_dict)} 个参数")

        # 加载权重
        missing_keys, unexpected_keys = self.cls_model.load_state_dict(state_dict, strict=False)

        if missing_keys:
            print(f"  警告: 缺失的参数 ({len(missing_keys)} 个):")
            for key in missing_keys[:5]:
                print(f"    - {key}")
            if len(missing_keys) > 5:
                print(f"    ... 还有 {len(missing_keys) - 5} 个")

        if unexpected_keys:
            print(f"  警告: 多余的参数 ({len(unexpected_keys)} 个):")
            for key in unexpected_keys[:5]:
                print(f"    - {key}")
            if len(unexpected_keys) > 5:
                print(f"    ... 还有 {len(unexpected_keys) - 5} 个")

        if not missing_keys and not unexpected_keys:
            print(f"  ✓ 权重加载完全成功")

        self.cls_model.eval()
        self.cls_model.to(self.device)

        print(f"  ✓ 分类模型加载成功 (类别数: 5)")

    def preprocess_image(self, image_path):
        """
        图像预处理

        Args:
            image_path: 图像路径

        Returns:
            original_image: 原始图像 (H, W, 3)
            tensor_image: 张量图像 (1, 3, H, W)
        """
        # 读取图像
        original_image = cv2.imread(image_path)
        if original_image is None:
            raise ValueError(f"无法读取图像: {image_path}")

        # BGR -> RGB
        original_image = original_image[:, :, ::-1]

        # 转换为张量
        to_tensor = T.ToTensor(
            mean=(0.3257, 0.3690, 0.3223),  # city, rgb
            std=(0.2112, 0.2148, 0.2115),
        )
        tensor_image = to_tensor(dict(im=original_image, lb=None))['im'].unsqueeze(0)

        return original_image, tensor_image

    def segment(self, tensor_image):
        """
        执行分割

        Args:
            tensor_image: 输入张量 (1, 3, H, W)

        Returns:
            mask: 分割掩码 (H, W) - 二值化掩码
        """
        # 移到设备
        tensor_image = tensor_image.to(self.device)

        # 记录原始尺寸
        org_size = tensor_image.size()[2:]

        # 调整到32的倍数
        new_size = [math.ceil(el / 32) * 32 for el in org_size]
        tensor_image = F.interpolate(
            tensor_image,
            size=new_size,
            align_corners=False,
            mode='bilinear'
        )

        # 推理
        with torch.cuda.amp.autocast():
            out = self.seg_model(tensor_image)[0]

        # 恢复原始尺寸
        out = F.interpolate(
            out,
            size=org_size,
            align_corners=False,
            mode='bilinear'
        )

        # 获取预测结果（二值掩码）
        mask = out.argmax(dim=1).squeeze().cpu().numpy()

        return mask

    def classify(self, original_image, mask):
        """
        执行分类

        Args:
            original_image: 原始图像 (H, W, 3)
            mask: 分割掩码 (H, W) - 二值掩码 (0或1)

        Returns:
            class_id: 类别ID
            confidence: 置信度
        """
        # 调整图像大小到分类模型输入尺寸
        target_size = (224, 224)

        # 调整原图
        image_resized = cv2.resize(original_image, target_size, interpolation=cv2.INTER_LINEAR)

        # 调整掩码（二值掩码，转换为0-255）
        mask_resized = cv2.resize((mask * 255).astype(np.uint8), target_size, interpolation=cv2.INTER_NEAREST)

        # 归一化
        image_normalized = image_resized.astype(np.float32) / 255.0
        image_normalized = (image_normalized - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])

        # 掩码归一化到 [0, 1]
        mask_normalized = mask_resized.astype(np.float32) / 255.0

        # 组合成4通道输入 (H, W, 4)
        combined = np.concatenate([
            image_normalized,
            mask_normalized[:, :, np.newaxis]
        ], axis=2)

        # 转换为张量 (1, 4, H, W)
        tensor = torch.from_numpy(combined.transpose(2, 0, 1)).unsqueeze(0).float().to(self.device)

        # 推理
        with torch.cuda.amp.autocast():
            logits = self.cls_model(tensor)

        # 获取预测结果
        probs = torch.softmax(logits, dim=1)
        confidence, class_id = torch.max(probs, dim=1)

        # 打印详细的分类信息
        print(f"  所有类别概率分布:")
        for i, prob in enumerate(probs[0].cpu().numpy()):
            print(f"    {self.class_names[i]}: {prob:.4f} ({prob*100:.2f}%)")

        return class_id.item(), confidence.item()

    def visualize_results(self, original_image, mask, class_id, confidence, save_path):
        """
        可视化结果

        Args:
            original_image: 原始图像 (H, W, 3)
            mask: 分割掩码 (H, W)
            class_id: 类别ID
            confidence: 置信度
            save_path: 保存路径
        """
        # 创建可视化图像
        h, w = original_image.shape[:2]

        # 1. 分割掩码可视化
        mask_colored = self.palette[mask]

        # 2. 叠加结果
        overlay = original_image.copy()
        overlay[mask == 1] = (overlay[mask == 1] * 0.5 + np.array([255, 0, 0]) * 0.5).astype(np.uint8)

        # 3. 创建结果画布
        canvas = np.zeros((h, w * 3 + 20, 3), dtype=np.uint8)
        canvas[:, :w] = original_image
        canvas[:, w+10:w*2+10] = mask_colored
        canvas[:, w*2+20:] = overlay

        # 4. 使用PIL绘制中文（解决OpenCV不支持中文的问题）
        from PIL import ImageFont, ImageDraw

        # 转换为PIL图像
        canvas_pil = Image.fromarray(canvas)

        # 尝试加载中文字体（Windows系统）
        try:
            font_path = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑
            font_large = ImageFont.truetype(font_path, 24)
            font_medium = ImageFont.truetype(font_path, 18)
            font_small = ImageFont.truetype(font_path, 14)
        except:
            try:
                font_path = "C:/Windows/Fonts/simhei.ttf"  # 黑体
                font_large = ImageFont.truetype(font_path, 24)
                font_medium = ImageFont.truetype(font_path, 18)
                font_small = ImageFont.truetype(font_path, 14)
            except:
                # 如果找不到字体文件，使用默认字体
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()

        draw = ImageDraw.Draw(canvas_pil)

        # 添加顶部背景条
        title_height = 60
        canvas_with_bg = Image.new('RGB', (canvas_pil.width, canvas_pil.height + title_height), color=(255, 255, 255))
        canvas_with_bg.paste(canvas_pil, (0, title_height))
        draw = ImageDraw.Draw(canvas_with_bg)

        # 添加主标题
        class_name = self.class_names[class_id]
        text = f"Class: {class_name} (Level {class_id}) - Confidence: {confidence:.2%}"
        draw.text((10, 15), text, fill=(0, 0, 0), font=font_large)

        # 添加分类等级标签（大字体，醒目）
        level_text = f"Level {class_id}: {class_name}"

        # 根据分类等级选择颜色
        level_colors = {
            0: (0, 128, 0),      # 绿色 - 无裂缝
            1: (0, 139, 139),    # 青色 - 轻度裂缝
            2: (255, 140, 0),    # 橙色 - 中度裂缝
            3: (220, 20, 60),    # 红色 - 重度裂缝
            4: (139, 0, 0)       # 深红色 - 严重裂缝
        }
        color = level_colors.get(class_id, (0, 0, 0))

        # 在叠加图上添加分类等级标注
        overlay_x = w * 2 + 20 + 10
        overlay_y = title_height + 90
        draw.text((overlay_x, overlay_y), level_text, fill=color, font=font_large)

        # 添加置信度标注
        conf_text = f"Confidence: {confidence:.2%}"
        draw.text((overlay_x, overlay_y + 35), conf_text, fill=(50, 50, 50), font=font_medium)

        # 添加子图标签
        labels = ["Original", "Segmentation Mask", "Overlay"]
        for i, label in enumerate(labels):
            x = i * (w + 10) + w // 2 - 40
            draw.text((x, h + title_height + 80), label, fill=(100, 100, 100), font=font_small)

        # 转换回numpy数组并保存
        result_array = np.array(canvas_with_bg)
        cv2.imwrite(save_path, cv2.cvtColor(result_array, cv2.COLOR_RGB2BGR))  # RGB -> BGR
        print(f"\n✓ 可视化结果已保存: {save_path}")

        return result_array

    def inference(self, image_path, output_dir='inference_results'):
        """
        完整推理流程

        Args:
            image_path: 输入图像路径
            output_dir: 输出目录

        Returns:
            result: 推理结果字典
        """
        print(f"\n处理图像: {image_path}")

        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)

        # 1. 预处理
        print("\n[步骤 1/4] 图像预处理...")
        original_image, tensor_image = self.preprocess_image(image_path)
        print(f"  图像尺寸: {original_image.shape[:2]}")

        # 2. 分割
        print("\n[步骤 2/4] 执行裂缝分割...")
        mask = self.segment(tensor_image)
        crack_pixels = np.sum(mask == 1)
        total_pixels = mask.size
        crack_ratio = crack_pixels / total_pixels
        print(f"  裂缝像素: {crack_pixels}/{total_pixels} ({crack_ratio:.2%})")

        # 3. 分类
        print("\n[步骤 3/4] 执行裂缝分类...")
        class_id, confidence = self.classify(original_image, mask)
        class_name = self.class_names[class_id]
        print(f"  预测类别: {class_name} (Level {class_id})")
        print(f"  置信度: {confidence:.2%}")

        # 4. 可视化
        print("\n[步骤 4/4] 生成可视化结果...")
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(output_dir, f"{base_name}_result_{timestamp}.jpg")
        self.visualize_results(original_image, mask, class_id, confidence, save_path)

        # 保存分割掩码
        mask_path = os.path.join(output_dir, f"{base_name}_mask_{timestamp}.png")
        cv2.imwrite(mask_path, mask * 255)
        print(f"✓ 分割掩码已保存: {mask_path}")

        # 保存JSON结果
        result = {
            'image_path': image_path,
            'image_size': list(original_image.shape[:2]),
            'segmentation': {
                'mask_path': mask_path,
                'crack_pixels': int(crack_pixels),
                'total_pixels': int(total_pixels),
                'crack_ratio': float(crack_ratio)
            },
            'classification': {
                'class_id': int(class_id),
                'class_name': class_name,
                'confidence': float(confidence)
            },
            'result_image': save_path
        }

        json_path = os.path.join(output_dir, f"{base_name}_result_{timestamp}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✓ JSON结果已保存: {json_path}")

        # 打印摘要
        print("\n" + "=" * 60)
        print("推理结果摘要")
        print("=" * 60)
        print(f"图像路径: {image_path}")
        print(f"图像尺寸: {original_image.shape[1]} x {original_image.shape[0]}")
        print(f"裂缝占比: {crack_ratio:.2%}")
        print(f"裂缝等级: {class_name} (Level {class_id})")
        print(f"置信度: {confidence:.2%}")
        print("=" * 60)

        return result


def parse_args():
    parser = argparse.ArgumentParser(description='裂缝分割+分类推理脚本')
    parser.add_argument('--image', type=str, required=True, help='输入图像路径')
    parser.add_argument('--seg-config', type=str,
                       default='configs/bisenetv2_crack.py',
                       help='分割模型配置文件')
    parser.add_argument('--seg-weight', type=str,
                       default='res_3/crack_bisenetv2/model_best.pth',
                       help='分割模型权重')
    parser.add_argument('--cls-weight', type=str,
                       default='crack_classifier/res/crack_classifier/mobilenetv3_small/model_best.pth',
                       help='分类模型权重')
    parser.add_argument('--output', type=str,
                       default='inference_results',
                       help='输出目录')
    parser.add_argument('--device', type=str,
                       default='cuda',
                       help='运行设备 (cuda/cpu)')
    return parser.parse_args()


def main():
    # ============ 配置参数 ============
    # 图片路径（单张图片）
    image_path = 'as_test.png'  # 修改为你要识别的图片路径

    # 模型权重路径
    seg_config = 'configs/bisenetv2_crack.py'
    seg_weight = 'res_3/crack_bisenetv2/model_best.pth'
    cls_weight = 'crack_classifier/res/crack_classifier/mobilenetv3_small/model_best.pth'

    # 输出目录
    output_dir = 'inference_results'

    # 运行设备
    device = 'cuda'
    # ================================

    # 检查CUDA是否可用
    if device == 'cuda' and not torch.cuda.is_available():
        print("警告: CUDA不可用，将使用CPU")
        device = 'cpu'

    # 创建推理管道
    pipeline = CrackInferencePipeline(
        seg_config=seg_config,
        seg_weight=seg_weight,
        cls_weight=cls_weight,
        device=device
    )

    # 执行推理
    result = pipeline.inference(image_path, output_dir)

    print("\n✓ 推理完成！")


if __name__ == '__main__':
    main()
