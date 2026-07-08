"""
分割模型导出ONNX
BiSeNetV2 → ONNX
"""

import os
import sys
import argparse
import torch
import torch.nn as nn

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.models.bisenetv2 import BiSeNetV2


def load_segmentation_model(weight_path, num_classes=2, device='cpu'):
    """
    加载分割模型
    
    Args:
        weight_path: 权重文件路径
        num_classes: 类别数
        device: 设备
    
    Returns:
        model: 加载好的模型
    """
    print(f"加载分割模型: {weight_path}")
    
    # 创建模型
    model = BiSeNetV2(num_classes)
    
    # 加载权重
    checkpoint = torch.load(weight_path, map_location=device)
    if 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)
    
    model.to(device)
    model.eval()
    
    print("模型加载成功")
    return model


def export_segmentation_onnx(model, output_path, input_size=(1024, 1024), opset_version=11):
    """
    导出分割模型为ONNX格式
    
    Args:
        model: PyTorch模型
        output_path: 输出路径
        input_size: 输入尺寸 (H, W)
        opset_version: ONNX opset版本
    """
    print(f"导出ONNX模型: {output_path}")
    print(f"输入尺寸: {input_size}")
    
    # 创建dummy输入
    dummy_input = torch.randn(1, 3, input_size[0], input_size[1])
    
    # 导出ONNX
    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        export_params=True,
        opset_version=opset_version,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )
    
    print(f"ONNX模型导出成功: {output_path}")
    
    # 验证ONNX模型
    verify_onnx_model(output_path, dummy_input, model)


def verify_onnx_model(onnx_path, dummy_input, pytorch_model):
    """
    验证ONNX模型
    
    Args:
        onnx_path: ONNX模型路径
        dummy_input: 测试输入
        pytorch_model: PyTorch模型
    """
    print("验证ONNX模型...")
    
    import onnx
    import onnxruntime as ort
    
    # 检查ONNX模型格式
    onnx_model = onnx.load(onnx_path)
    onnx.checker.check_model(onnx_model)
    print("ONNX模型格式检查通过")
    
    # 对比PyTorch和ONNX输出
    pytorch_model.eval()
    with torch.no_grad():
        pytorch_output = pytorch_model(dummy_input)
    
    # ONNX推理
    ort_session = ort.InferenceSession(onnx_path)
    onnx_output = ort_session.run(None, {'input': dummy_input.numpy()})
    
    # 对比结果
    if isinstance(pytorch_output, (list, tuple)):
        pytorch_output = pytorch_output[0]
    
    diff = abs(pytorch_output.numpy() - onnx_output[0]).max()
    print(f"PyTorch vs ONNX 最大差异: {diff:.6f}")
    
    if diff < 1e-5:
        print("✅ ONNX模型验证通过")
    else:
        print("⚠️ ONNX模型输出有差异，请检查")


def main():
    parser = argparse.ArgumentParser(description='导出分割模型为ONNX格式')
    parser.add_argument('--weight', type=str, 
                        default=None,
                        help='模型权重路径')
    parser.add_argument('--output', type=str, 
                        default='bisenetv2_crack.onnx',
                        help='输出ONNX文件路径')
    parser.add_argument('--input-size', type=int, nargs=2, 
                        default=[1024, 1024],
                        help='输入尺寸 (H W)')
    parser.add_argument('--num-classes', type=int, default=2,
                        help='类别数')
    parser.add_argument('--opset', type=int, default=11,
                        help='ONNX opset版本')
    parser.add_argument('--device', type=str, default='cpu',
                        help='设备 (cpu/cuda)')
    
    args = parser.parse_args()
    
    # 获取项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # 设置默认权重路径
    if args.weight is None:
        args.weight = os.path.join(project_root, 'res_3', 'crack_bisenetv2', 'model_best.pth')
    
    # 检查权重文件是否存在
    if not os.path.exists(args.weight):
        print(f"❌ 模型权重文件不存在: {args.weight}")
        return
    
    # 加载模型
    model = load_segmentation_model(
        args.weight, 
        num_classes=args.num_classes,
        device=args.device
    )
    
    # 导出ONNX
    export_segmentation_onnx(
        model,
        args.output,
        input_size=tuple(args.input_size),
        opset_version=args.opset
    )


if __name__ == '__main__':
    main()
