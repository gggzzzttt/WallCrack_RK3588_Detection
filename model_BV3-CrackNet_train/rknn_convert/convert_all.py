"""
一键转换所有模型为RKNN格式
"""

import os
import subprocess
import sys


def run_command(cmd):
    """运行命令"""
    print(f"\n{'='*60}")
    print(f"执行: {cmd}")
    print('='*60)
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ 命令执行失败: {cmd}")
        return False
    return True


def main():
    print("="*60)
    print("一键转换RKNN模型")
    print("="*60)
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 检查ONNX文件是否存在
    onnx_dir = os.path.join(os.path.dirname(current_dir), 'onnx_export')
    seg_onnx = os.path.join(onnx_dir, 'bisenetv2_crack.onnx')
    cls_onnx = os.path.join(onnx_dir, 'mobilenetv3_small_crack.onnx')
    
    if not os.path.exists(seg_onnx):
        print(f"❌ 分割模型ONNX不存在: {seg_onnx}")
        print("   请先运行 onnx_export/export_all.py 导出ONNX模型")
        return
    
    if not os.path.exists(cls_onnx):
        print(f"❌ 分类模型ONNX不存在: {cls_onnx}")
        print("   请先运行 onnx_export/export_all.py 导出ONNX模型")
        return
    
    # 检查校准数据是否存在
    calib_dir = os.path.join(onnx_dir, 'calibration_data')
    seg_calib = os.path.join(calib_dir, 'segmentation_calib_list.txt')
    cls_calib = os.path.join(calib_dir, 'classifier_calib_list.txt')
    
    if not os.path.exists(seg_calib) or not os.path.exists(cls_calib):
        print(f"❌ 校准数据不存在")
        print("   请先运行 onnx_export/prepare_calibration_data.py 准备校准数据")
        return
    
    # 1. 转换分割模型
    print("\n[1/2] 转换分割模型...")
    seg_cmd = f'python "{os.path.join(current_dir, "convert_segmentation.py")}"'
    if not run_command(seg_cmd):
        print("分割模型转换失败")
        return
    
    # 2. 转换分类模型
    print("\n[2/2] 转换分类模型...")
    cls_cmd = f'python "{os.path.join(current_dir, "convert_classifier.py")}"'
    if not run_command(cls_cmd):
        print("分类模型转换失败")
        return
    
    print("\n" + "="*60)
    print("✅ 所有模型转换完成！")
    print("="*60)
    print("\n转换后的RKNN模型:")
    print(f"  - 分割模型: {os.path.join(current_dir, 'bisenetv2_crack.rknn')}")
    print(f"  - 分类模型: {os.path.join(current_dir, 'mobilenetv3_small_crack.rknn')}")
    print("\n下一步: 将RKNN模型部署到RK3588设备")


if __name__ == '__main__':
    main()
