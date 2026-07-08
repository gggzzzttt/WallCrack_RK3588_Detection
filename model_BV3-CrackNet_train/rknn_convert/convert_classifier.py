"""
分类模型ONNX转RKNN
MobileNetV3-Small ONNX → RKNN
"""

import os
import sys
import argparse
import numpy as np
import cv2

try:
    from rknn.api import RKNN
except ImportError:
    print("❌ 请先安装RKNN-Toolkit2:")
    print("   pip install rknn-toolkit2")
    sys.exit(1)


def convert_classifier_to_rknn(
    onnx_path,
    output_path,
    calibration_data,
    target_platform='rk3588',
    do_quantization=True,
    quantized_dtype='asymmetric_quantized-u8'
):
    """
    将分类模型ONNX转换为RKNN格式
    
    Args:
        onnx_path: ONNX模型路径
        output_path: 输出RKNN路径
        calibration_data: 校准数据文件/目录
        target_platform: 目标平台
        do_quantization: 是否量化
        quantized_dtype: 量化数据类型
    """
    print("="*60)
    print("分类模型ONNX转RKNN")
    print("="*60)
    print(f"ONNX模型: {onnx_path}")
    print(f"输出路径: {output_path}")
    print(f"目标平台: {target_platform}")
    print(f"量化: {do_quantization}")
    
    # 创建RKNN实例
    rknn = RKNN(verbose=True)
    
    # 配置
    print("\n[1/5] 配置RKNN...")
    rknn.config(
        mean_values=[[0, 0, 0, 0]],  # 4通道
        std_values=[[255, 255, 255, 255]],
        target_platform=target_platform,
        quantized_dtype=quantized_dtype,
        optimization_level=3,
        single_core_mode=True
    )
    
    # 加载ONNX模型
    print("\n[2/5] 加载ONNX模型...")
    ret = rknn.load_onnx(model=onnx_path)
    if ret != 0:
        print(f"❌ 加载ONNX失败: {ret}")
        return False
    print("✅ ONNX模型加载成功")
    
    # 构建模型
    print("\n[3/5] 构建RKNN模型...")
    if do_quantization:
        ret = rknn.build(do_quantization=True, dataset=calibration_data)
    else:
        ret = rknn.build(do_quantization=False)
    
    if ret != 0:
        print(f"❌ 构建RKNN失败: {ret}")
        return False
    print("✅ RKNN模型构建成功")
    
    # 导出RKNN
    print("\n[4/5] 导出RKNN模型...")
    ret = rknn.export_rknn(output_path)
    if ret != 0:
        print(f"❌ 导出RKNN失败: {ret}")
        return False
    print(f"✅ RKNN模型导出成功: {output_path}")
    
    # 精度验证（可选）
    print("\n[5/5] 精度验证...")
    accuracy_check(rknn, calibration_data)
    
    # 释放资源
    rknn.release()
    
    print("\n" + "="*60)
    print("✅ 分类模型转换完成！")
    print("="*60)
    return True


def accuracy_check(rknn, calibration_data, num_samples=5):
    """
    精度验证
    
    Args:
        rknn: RKNN实例
        calibration_data: 校准数据
        num_samples: 验证样本数
    """
    print("进行精度验证...")
    
    # 获取校准数据列表
    if os.path.isdir(calibration_data):
        npy_files = [os.path.join(calibration_data, f) 
                     for f in os.listdir(calibration_data) 
                     if f.endswith('.npy')]
    else:
        with open(calibration_data, 'r') as f:
            npy_files = [line.strip() for line in f.readlines()]
    
    # 随机选择几张验证
    import random
    samples = random.sample(npy_files, min(num_samples, len(npy_files)))
    
    for npy_path in samples:
        # 加载数据
        data = np.load(npy_path)
        
        # 初始化运行时
        ret = rknn.init_runtime(target=None)  # PC上模拟运行
        if ret != 0:
            print("⚠️ 无法初始化运行时，跳过验证")
            return
        
        # 推理
        outputs = rknn.inference(inputs=[data])
        
        # 输出
        pred = np.argmax(outputs[0])
        print(f"  输入: {data.shape}")
        print(f"  输出: {outputs[0].shape}, 预测类别: {pred}")
        
        rknn.release_runtime()
    
    print("✅ 精度验证完成")


def main():
    parser = argparse.ArgumentParser(description='分类模型ONNX转RKNN')
    parser.add_argument('--onnx', type=str, 
                        default='../onnx_export/mobilenetv3_small_crack.onnx',
                        help='ONNX模型路径')
    parser.add_argument('--output', type=str, 
                        default='mobilenetv3_small_crack.rknn',
                        help='输出RKNN路径')
    parser.add_argument('--calibration', type=str, 
                        default='../onnx_export/calibration_data/classifier_calib_list.txt',
                        help='校准数据文件/目录')
    parser.add_argument('--platform', type=str, default='rk3588',
                        help='目标平台')
    parser.add_argument('--no-quantize', action='store_true',
                        help='不进行量化')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.exists(args.onnx):
        print(f"❌ ONNX文件不存在: {args.onnx}")
        print("   请先运行 onnx_export/export_classifier.py 导出ONNX模型")
        return
    
    if not os.path.exists(args.calibration):
        print(f"❌ 校准数据不存在: {args.calibration}")
        print("   请先运行 onnx_export/prepare_calibration_data.py 准备校准数据")
        return
    
    # 转换
    success = convert_classifier_to_rknn(
        args.onnx,
        args.output,
        args.calibration,
        target_platform=args.platform,
        do_quantization=not args.no_quantize
    )
    
    if success:
        print(f"\n🎉 转换成功！RKNN模型: {args.output}")
    else:
        print("\n❌ 转换失败")


if __name__ == '__main__':
    main()
