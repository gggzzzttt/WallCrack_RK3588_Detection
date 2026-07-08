#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RK3588 TCP客户端测试脚本
功能：测试向PC上位机发送裂缝识别数据（JSON + 图片二进制流）
使用tcp_server模块的TCPSender类发送数据
"""

import sys
import os
from datetime import datetime

# 添加父目录到路径，以便导入tcp_server模块
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from tcp_server import TCPSender, PACKET_TYPE_COMPLETE, PACKET_TYPE_JSON, PROTOCOL_HEADER


# ============================================================
# 配置参数
# ============================================================

# PC上位机IP和端口
SERVER_IP = "192.168.137.1"  # 修改为实际PC IP
SERVER_PORT = 8888

# 设备信息
DEVICE_ID = "RK3588_001"


# ============================================================
# 裂缝数据结构
# ============================================================

class CrackData:
    """裂缝数据结构"""

    def __init__(self):
        self.device_id = DEVICE_ID
        self.timestamp = int(datetime.now().timestamp())
        self.crack_count = 0
        self.max_width = 0.0
        self.max_length = 0.0
        self.avg_width = 0.0
        self.confidence = 0.0
        self.entry_date = datetime.now().strftime('%Y-%m-%d')
        self.image_path = ""

    def to_dict(self):
        """转换为字典"""
        return {
            'device_id': self.device_id,
            'timestamp': self.timestamp,
            'crack_count': self.crack_count,
            'max_width': self.max_width,
            'max_length': self.max_length,
            'avg_width': self.avg_width,
            'confidence': self.confidence,
            'image_path': self.image_path,
            'entry_date': self.entry_date
        }


# ============================================================
# 模拟数据生成函数
# ============================================================

def generate_mock_crack_data():
    """
    生成模拟裂缝数据

    Returns:
        CrackData: 裂缝数据对象
    """
    import random

    crack_data = CrackData()
    crack_data.crack_count = random.randint(1, 10)
    crack_data.max_width = round(random.uniform(0.5, 5.0), 2)
    crack_data.max_length = round(random.uniform(5.0, 30.0), 2)
    crack_data.avg_width = round(crack_data.max_width * random.uniform(0.3, 0.8), 2)
    crack_data.confidence = round(random.uniform(70.0, 99.0), 1)

    return crack_data


def generate_mock_image(image_path):
    """
    生成模拟图片

    Args:
        image_path (str): 图片保存路径

    Returns:
        bool: 生成成功返回True
    """
    try:
        # 创建目录
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        # 生成简单的测试图片（灰色背景）
        from PIL import Image, ImageDraw, ImageFont

        width, height = 640, 480
        image = Image.new('RGB', (width, height), color='#E0E0E0')
        draw = ImageDraw.Draw(image)

        # 绘制模拟裂缝（黑色线条）
        crack_data = generate_mock_crack_data()
        for i in range(crack_data.crack_count):
            start_x = random.randint(50, width - 50)
            start_y = random.randint(50, height - 50)
            end_x = start_x + random.randint(20, 100)
            end_y = start_y + random.randint(20, 80)
            draw.line([(start_x, start_y), (end_x, end_y)],
                     fill='black', width=int(crack_data.max_width * 2))

        # 添加文字标签
        text = f"Device: {DEVICE_ID} | Cracks: {crack_data.crack_count}"
        draw.text((10, 10), text, fill='black')

        # 保存图片
        image.save(image_path, 'JPEG')
        print(f"模拟图片已生成: {image_path}")

        return True

    except ImportError:
        # 如果没有PIL库，创建一个空的图片文件
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, 'wb') as f:
            f.write(b'')  # 空文件
        print(f"模拟图片已创建（空文件）: {image_path}")
        return True

    except Exception as e:
        print(f"生成模拟图片失败: {e}")
        return False


# ============================================================
# TCP通信函数
# ============================================================

def test_connection(server_ip, server_port):
    """
    测试服务器连接

    Args:
        server_ip (str): 服务器IP
        server_port (int): 服务器端口

    Returns:
        bool: 连接成功返回True
    """
    try:
        sender = TCPSender(server_ip, server_port)
        if sender.connect():
            print(f"✓ 成功连接到服务器: {server_ip}:{server_port}")
            sender.disconnect()
            return True
        else:
            print(f"✗ 连接服务器失败: {server_ip}:{server_port}")
            return False

    except Exception as e:
        print(f"✗ 连接测试出错: {e}")
        return False


def send_json_data(server_ip, server_port, crack_data):
    """
    发送JSON数据到服务器

    Args:
        server_ip (str): 服务器IP
        server_port (int): 服务器端口
        crack_data (CrackData): 裂缝数据

    Returns:
        bool: 发送成功返回True
    """
    try:
        sender = TCPSender(server_ip, server_port)
        if sender.connect():
            json_data = crack_data.to_dict()
            if sender.send_json(json_data):
                print(f"✓ JSON数据已发送: {json_data}")
                sender.disconnect()
                return True

        sender.disconnect()
        return False

    except Exception as e:
        print(f"✗ 发送JSON数据出错: {e}")
        return False


def send_complete_packet(server_ip, server_port, crack_data, image_path):
    """
    发送完整数据包（JSON数据包含图片路径）

    Args:
        server_ip (str): 服务器IP
        server_port (int): 服务器端口
        crack_data (CrackData): 裂缝数据
        image_path (str): 图片路径

    Returns:
        bool: 发送成功返回True
    """
    try:
        sender = TCPSender(server_ip, server_port)
        if sender.connect():
            # 设置图片路径
            crack_data.image_path = image_path

            # 发送完整数据
            complete_data = crack_data.to_dict()
            if sender.send_complete_data(complete_data):
                print(f"✓ 完整数据包已发送")
                print(f"  设备ID: {crack_data.device_id}")
                print(f"  裂缝数: {crack_data.crack_count}")
                print(f"  最大宽度: {crack_data.max_width}mm")
                print(f"  最大长度: {crack_data.max_length}mm")
                print(f"  置信度: {crack_data.confidence}%")
                print(f"  图片路径: {image_path}")

                sender.disconnect()
                return True

        sender.disconnect()
        return False

    except Exception as e:
        print(f"✗ 发送完整数据包出错: {e}")
        return False


# ============================================================
# 批量测试函数
# ============================================================

def batch_send_test(count=5, interval=1):
    """
    批量发送测试数据

    Args:
        count (int): 发送次数
        interval (int): 发送间隔（秒）
    """
    print(f"\n开始批量发送测试，共 {count} 次，间隔 {interval} 秒...")
    print("=" * 60)

    import time

    success_count = 0
    fail_count = 0

    for i in range(1, count + 1):
        print(f"\n[{i}/{count}] 发送测试数据...")

        # 生成模拟数据
        crack_data = generate_mock_crack_data()

        # 生成模拟图片
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_path = f"test_images/test_{timestamp}.jpg"

        # 发送完整数据包
        if send_complete_packet(SERVER_IP, SERVER_PORT, crack_data, image_path):
            success_count += 1
            print(f"✓ 第 {i} 次发送成功")
        else:
            fail_count += 1
            print(f"✗ 第 {i} 次发送失败")

        # 等待间隔
        if i < count:
            time.sleep(interval)

    print("\n" + "=" * 60)
    print(f"批量测试完成！")
    print(f"成功: {success_count} 次")
    print(f"失败: {fail_count} 次")
    print(f"成功率: {success_count / count * 100:.1f}%")


# ============================================================
# 主测试函数
# ============================================================

def main():
    """主测试函数"""
    print("=" * 60)
    print("RK3588 TCP客户端测试脚本")
    print(f"目标服务器: {SERVER_IP}:{SERVER_PORT}")
    print(f"设备ID: {DEVICE_ID}")
    print("=" * 60)

    # 测试连接
    print("\n[1] 测试服务器连接...")
    if not test_connection(SERVER_IP, SERVER_PORT):
        print("\n✗ 无法连接到服务器，请检查网络和IP配置")
        return

    print("\n[2] 发送单次测试数据...")
    crack_data = generate_mock_crack_data()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    image_path = f"test_images/test_{timestamp}.jpg"
    send_complete_packet(SERVER_IP, SERVER_PORT, crack_data, image_path)

    # 询问是否进行批量测试
    print("\n是否进行批量测试？")
    choice = input("输入数量（默认5），或按Enter跳过: ").strip()

    if choice:
        try:
            count = int(choice) if choice else 5
            count = max(1, min(100, count))  # 限制在1-100之间
            batch_send_test(count=count, interval=1)
        except ValueError:
            print("输入无效，跳过批量测试")

    print("\n测试完成！")


if __name__ == "__main__":
    main()