"""
检查RKNN转换环境
"""

import sys


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("❌ Python版本过低，需要 >= 3.6")
        return False
    print("✅ Python版本符合要求")
    return True


def check_rknn_toolkit():
    """检查RKNN-Toolkit2"""
    try:
        from rknn.api import RKNN
        print("✅ RKNN-Toolkit2 已安装")
        return True
    except ImportError:
        print("❌ RKNN-Toolkit2 未安装")
        print("   安装命令: pip install rknn-toolkit2")
        return False


def check_onnx():
    """检查ONNX"""
    try:
        import onnx
        print(f"✅ ONNX 已安装 (版本: {onnx.__version__})")
        return True
    except ImportError:
        print("❌ ONNX 未安装")
        print("   安装命令: pip install onnx")
        return False


def check_onnxruntime():
    """检查ONNX Runtime"""
    try:
        import onnxruntime as ort
        print(f"✅ ONNX Runtime 已安装 (版本: {ort.__version__})")
        return True
    except ImportError:
        print("❌ ONNX Runtime 未安装")
        print("   安装命令: pip install onnxruntime")
        return False


def check_numpy():
    """检查NumPy"""
    try:
        import numpy as np
        print(f"✅ NumPy 已安装 (版本: {np.__version__})")
        return True
    except ImportError:
        print("❌ NumPy 未安装")
        print("   安装命令: pip install numpy")
        return False


def check_opencv():
    """检查OpenCV"""
    try:
        import cv2
        print(f"✅ OpenCV 已安装 (版本: {cv2.__version__})")
        return True
    except ImportError:
        print("❌ OpenCV 未安装")
        print("   安装命令: pip install opencv-python")
        return False


def check_model_files():
    """检查模型文件"""
    import os
    
    print("\n检查模型文件:")
    
    # 检查ONNX文件
    onnx_dir = os.path.join(os.path.dirname(__file__), '..', 'onnx_export')
    seg_onnx = os.path.join(onnx_dir, 'bisenetv2_crack.onnx')
    cls_onnx = os.path.join(onnx_dir, 'mobilenetv3_small_crack.onnx')
    
    if os.path.exists(seg_onnx):
        print(f"✅ 分割模型ONNX: {seg_onnx}")
    else:
        print(f"❌ 分割模型ONNX不存在: {seg_onnx}")
    
    if os.path.exists(cls_onnx):
        print(f"✅ 分类模型ONNX: {cls_onnx}")
    else:
        print(f"❌ 分类模型ONNX不存在: {cls_onnx}")
    
    # 检查校准数据
    calib_dir = os.path.join(onnx_dir, 'calibration_data')
    seg_calib = os.path.join(calib_dir, 'segmentation_calib_list.txt')
    cls_calib = os.path.join(calib_dir, 'classifier_calib_list.txt')
    
    if os.path.exists(seg_calib):
        print(f"✅ 分割模型校准数据: {seg_calib}")
    else:
        print(f"❌ 分割模型校准数据不存在: {seg_calib}")
    
    if os.path.exists(cls_calib):
        print(f"✅ 分类模型校准数据: {cls_calib}")
    else:
        print(f"❌ 分类模型校准数据不存在: {cls_calib}")


def main():
    print("="*60)
    print("RKNN转换环境检查")
    print("="*60)
    
    print("\n[1/6] 检查Python版本...")
    check_python_version()
    
    print("\n[2/6] 检查RKNN-Toolkit2...")
    check_rknn_toolkit()
    
    print("\n[3/6] 检查ONNX...")
    check_onnx()
    
    print("\n[4/6] 检查ONNX Runtime...")
    check_onnxruntime()
    
    print("\n[5/6] 检查NumPy...")
    check_numpy()
    
    print("\n[6/6] 检查OpenCV...")
    check_opencv()
    
    check_model_files()
    
    print("\n" + "="*60)
    print("环境检查完成")
    print("="*60)


if __name__ == '__main__':
    main()
