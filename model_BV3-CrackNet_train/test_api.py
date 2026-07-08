#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
API服务测试脚本
用于快速测试裂缝检测API的各个接口
"""

import requests
import os
import sys
from pathlib import Path

# API基础地址
BASE_URL = "http://localhost:8000"



def test_health_check():
    """测试健康检查接口"""
    print("\n" + "=" * 60)
    print("1. 测试健康检查接口 (GET /health)")
    print("=" * 60)

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        data = response.json()

        print(f"状态码: {response.status_code}")
        print(f"响应内容:")
        print(f"  - 服务状态: {data.get('status')}")
        print(f"  - 运行设备: {data.get('device')}")
        print(f"  - 模型已加载: {data.get('model_loaded')}")
        print(f"  - 时间戳: {data.get('timestamp')}")

        return response.status_code == 200

    except Exception as e:
        print(f"错误: {e}")
        return False


def test_root():
    """测试根路径"""
    print("\n" + "=" * 60)
    print("2. 测试根路径 (GET /)")
    print("=" * 60)

    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        data = response.json()

        print(f"状态码: {response.status_code}")
        print(f"响应内容:")
        for key, value in data.items():
            print(f"  - {key}: {value}")

        return response.status_code == 200

    except Exception as e:
        print(f"错误: {e}")
        return False


def test_single_inference(image_path: str):
    """
    测试单张图片推理接口

    Args:
        image_path: 图片文件路径
    """
    print("\n" + "=" * 60)
    print("3. 测试单张图片推理 (POST /infer)")
    print("=" * 60)

    if not os.path.exists(image_path):
        print(f"错误: 图片不存在 - {image_path}")
        return None

    try:
        # 准备上传文件
        filename = os.path.basename(image_path)
        with open(image_path, 'rb') as f:
            files = {'file': (filename, f, 'image/png')}
            
            print(f"上传图片: {filename}")
            print(f"正在推理...")
            
            response = requests.post(
                f"{BASE_URL}/infer",
                files=files,
                timeout=120  # 长超时，因为推理需要时间
            )

        data = response.json()
        
        print(f"\n状态码: {response.status_code}")
        print(f"成功: {data.get('success')}")
        print(f"消息: {data.get('message')}")

        if data.get('success'):
            result_data = data['data']
            print(f"\n原始文件名: {result_data.get('original_filename')}")
            print(f"图像尺寸: {result_data.get('image_size')}")
            
            seg_info = result_data.get('segmentation', {})
            print(f"\n分割结果:")
            print(f"  - 裂缝像素: {seg_info.get('crack_pixels')}/{seg_info.get('total_pixels')}")
            print(f"  - 裂缝占比: {seg_info.get('crack_ratio')}")
            print(f"  - 掩码路径: {seg_info.get('mask_path')}")
            
            cls_info = result_data.get('classification', {})
            print(f"\n分类结果:")
            print(f"  - 等级: Level {cls_info.get('class_id')} ({cls_info.get('class_name')})")
            print(f"  - 置信度: {cls_info.get('confidence')}")
            
            output_files = result_data.get('output_files', {})
            print(f"\n输出文件:")
            print(f"  - 结果图片: {output_files.get('result_image')}")
            print(f"  - 分割掩码: {output_files.get('mask_image')}")
            print(f"  - JSON结果: {output_files.get('json_result', 'N/A')}")

            return data
        else:
            print(f"错误详情: {data}")
            return None

    except Exception as e:
        print(f"错误: {e}")
        return None


def test_batch_inference(image_paths: list):
    """
    测试批量图片推理接口

    Args:
        image_paths: 图片文件路径列表
    """
    print("\n" + "=" * 60)
    print("4. 测试批量图片推理 (POST /infer/batch)")
    print("=" * 60)

    if len(image_paths) == 0:
        print("错误: 未提供任何图片")
        return None

    if len(image_paths) > 20:
        print("警告: 超过20张限制，只使用前20张")
        image_paths = image_paths[:20]

    try:
        # 准备上传文件（保持文件句柄打开）
        files = []
        file_handles = []  # 保存文件句柄以便后续关闭
        valid_count = 0

        for img_path in image_paths[:10]:  # 测试时限制为10张
            if os.path.exists(img_path):
                filename = os.path.basename(img_path)
                f = open(img_path, 'rb')  # 打开文件但不关闭
                files.append(('files', (filename, f, 'image/png')))
                file_handles.append(f)  # 保存句柄
                valid_count += 1
                print(f"  + {filename}")

        if valid_count == 0:
            print("错误: 所有图片都不存在")
            return None

        print(f"\n共 {valid_count} 张图片")
        print("正在批量推理...")

        try:
            response = requests.post(
                f"{BASE_URL}/infer/batch",
                files=files,
                timeout=300  # 批量推理需要更长时间
            )
        finally:
            # 关闭所有文件句柄
            for fh in file_handles:
                fh.close()

        data = response.json()
        
        print(f"\n状态码: {response.status_code}")
        print(f"成功: {data.get('success')}")
        print(f"消息: {data.get('message')}")
        print(f"总计: {data.get('total')}")
        print(f"成功: {data.get('success_count')}")
        print(f"失败: {data.get('failed_count')}")

        if data.get('results'):
            print(f"\n详细结果:")
            for r in data['results'][:5]:  # 只显示前5个
                status = "✓" if r['success'] else "✗"
                print(f"  {status} [{r['index']}] {r['filename']}", end="")
                
                if r['success']:
                    cls_info = r['data']['classification']
                    seg_info = r['data']['segmentation']
                    print(f" -> {cls_info['class_name']} "
                          f"(置信度: {cls_info['confidence']}, "
                          f"裂缝占比: {seg_info['crack_ratio']})")
                else:
                    print(f" -> 错误: {r['error']}")

            if len(data['results']) > 5:
                print(f"  ... 还有 {len(data['results']) - 5} 个结果")

        return data

    except Exception as e:
        print(f"错误: {e}")
        return None


def test_list_results():
    """测试列出结果文件接口"""
    print("\n" + "=" * 60)
    print("5. 测试列出结果文件 (GET /list-results)")
    print("=" * 60)

    try:
        response = requests.get(
            f"{BASE_URL}/list-results",
            params={'limit': 5},
            timeout=5
        )

        data = response.json()
        
        print(f"状态码: {response.status_code}")
        print(f"总文件数: {data.get('total', 0)}")
        print(f"本次返回: {len(data.get('results', []))} 个")
        
        if data.get('results'):
            print(f"\n最近的结果文件:")
            for i, file_info in enumerate(data['results'], 1):
                size_kb = file_info['size'] / 1024
                print(f"  {i}. {file_info['filename']}")
                print(f"     大小: {size_kb:.2f} KB | 创建时间: {file_info['created_time']}")
                print(f"     URL: {BASE_URL}{file_info['url']}")

        return response.status_code == 200

    except Exception as e:
        print(f"错误: {e}")
        return False


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("裂缝检测API服务 - 测试工具")
    print("=" * 80)
    
    # 检查服务是否运行
    print("\n检查服务连接...")
    if not test_health_check():
        print("\n错误: 无法连接到API服务!")
        print("请先启动服务:")
        print("  python api_server.py")
        print("或:")
        print("  uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload")
        sys.exit(1)

    # 测试根路径
    test_root()




    # 获取项目根目录下的图片用于测试
    project_root = Path(__file__).parent
    test_images_dir = project_root / 'date' / 'Images'
    
    test_images = []
    if test_images_dir.exists():
        # 获取一些测试图片
        all_images = list(test_images_dir.glob('*.png'))[:3]
        test_images = [str(p) for p in all_images]
    
    # 也尝试查找微信图片
    wechat_images = list(project_root.glob('微信图片_*.png'))
    if wechat_images:
        test_images.insert(0, str(wechat_images[0]))

    # 单图推理测试
    if test_images:
        test_image = test_images[0]
        print(f"\n使用测试图片: {test_image}")
        test_single_inference(test_image)
    else:
        print("\n警告: 未找到测试图片，跳过单图推理测试")
        print("提示: 可以手动指定图片路径进行测试")

    # 批量推理测试（如果有足够多的图片）
    if len(test_images) >= 2:
        test_batch_inference(test_images[:3])
    else:
        print("\n跳过批量推理测试（需要至少2张图片）")

    # 列出结果文件
    test_list_results()

    print("\n" + "=" * 80)
    print("测试完成!")
    print("=" * 80)


if __name__ == '__main__':
    main()
