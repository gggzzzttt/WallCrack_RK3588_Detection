"""
一键导出所有模型为ONNX格式
"""

import os
import subprocess
import sys


def run_command(script_path):
    """运行命令"""
    print(f"\n{'='*60}")
    print(f"执行: {script_path}")
    print('='*60)
    
    # 使用当前Python解释器
    python_exe = sys.executable
    cmd = [python_exe, script_path]
    
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"❌ 命令执行失败")
        return False
    return True


def main():
    print("="*60)
    print("一键导出ONNX模型")
    print("="*60)
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. 导出分割模型
    print("\n[1/2] 导出分割模型...")
    seg_script = os.path.join(current_dir, "export_onnx.py")
    if not run_command(seg_script):
        print("分割模型导出失败")
        return
    
    # 2. 导出分类模型
    print("\n[2/2] 导出分类模型...")
    cls_script = os.path.join(current_dir, "export_classifier.py")
    if not run_command(cls_script):
        print("分类模型导出失败")
        return
    
    print("\n" + "="*60)
    print("✅ 所有模型导出完成！")
    print("="*60)
    print("\n导出的ONNX模型:")
    print(f"  - 分割模型: {os.path.join(current_dir, 'bisenetv2_crack.onnx')}")
    print(f"  - 分类模型: {os.path.join(current_dir, 'mobilenetv3_small_crack.onnx')}")
    print("\n下一步: 使用RKNN-Toolkit2将ONNX转换为RKNN格式")


if __name__ == '__main__':
    main()
