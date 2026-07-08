#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
墙体裂缝检测上位机 - TCP服务端模块
功能：接收RK3588板卡上传的裂缝识别数据（JSON + 图片二进制流）
说明：独立子线程监听，收到数据自动存入库并刷新实时界面
"""

import socket
import json
import threading
import os
import traceback
from datetime import datetime


# ============================================================
# 导入全局配置
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
LOG_PATH = os.path.join(LOGS_DIR, "app.log")


# ============================================================
# TCP协议定义
# ============================================================

# 协议头标识
PROTOCOL_HEADER = b'CRACK_DATA'
HEADER_SIZE = 10

# 数据包类型
PACKET_TYPE_JSON = 1
PACKET_TYPE_IMAGE = 2
PACKET_TYPE_COMPLETE = 3

# RK3588裸包协议：[4字节JSON长度][JSON][4字节图片长度][图片]
RAW_JSON_LEN_SIZE = 4
RAW_IMAGE_LEN_SIZE = 4


# ============================================================
# 日志工具函数
# ============================================================

def write_log(message, level="INFO"):
    """
    写入日志

    Args:
        message (str): 日志消息
        level (str): 日志级别
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{level}] TCP_SERVER: {message}\n"

    print(log_entry.strip())  # 控制台输出

    try:
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception:
        pass


# ============================================================
# TCP服务端类
# ============================================================

class TCPServer:
    """
    TCP服务端类
    负责监听端口，接收RK3588上传的裂缝数据
    """

    def __init__(self, host='0.0.0.0', port=8888, db=None, ui_callback=None):
        """
        初始化TCP服务端

        Args:
            host (str): 监听地址，默认为所有网卡
            port (int): 监听端口
            db: 数据库操作实例
            ui_callback: UI回调函数，用于刷新界面
        """
        self.host = host
        self.port = port
        self.db = db
        self.ui_callback = ui_callback

        self.server_socket = None
        self.is_running = False
        self.client_threads = []
        self.online_devices = {}  # 在线设备 {address: {'device_id': str, 'last_seen': timestamp}}

        write_log(f"TCP服务端初始化完成，监听地址: {host}:{port}")

    def start(self):
        """启动TCP服务端"""
        if self.is_running:
            write_log("TCP服务端已在运行", "WARNING")
            return False

        try:
            # 创建Socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # 绑定地址和端口
            self.server_socket.bind((self.host, self.port))

            # 开始监听
            self.server_socket.listen(10)

            self.is_running = True
            write_log(f"TCP服务端启动成功，监听 {self.host}:{self.port}", "SUCCESS")

            # 启动接收线程
            accept_thread = threading.Thread(target=self._accept_clients, daemon=True)
            accept_thread.start()

            # 启动心跳检测线程
            heartbeat_thread = threading.Thread(target=self._check_heartbeat, daemon=True)
            heartbeat_thread.start()

            return True

        except Exception as e:
            write_log(f"TCP服务端启动失败: {e}", "ERROR")
            return False

    def stop(self):
        """停止TCP服务端"""
        write_log("正在停止TCP服务端...")

        self.is_running = False

        # 关闭所有客户端线程
        for thread in self.client_threads:
            thread.join(timeout=1.0)

        # 关闭服务端Socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass

        write_log("TCP服务端已停止", "SUCCESS")

    def _accept_clients(self):
        """接受客户端连接"""
        write_log("等待客户端连接...")

        while self.is_running:
            try:
                # 设置超时，避免永久阻塞
                self.server_socket.settimeout(1.0)

                try:
                    client_socket, client_address = self.server_socket.accept()
                except socket.timeout:
                    continue

                write_log(f"新客户端连接: {client_address}", "INFO")

                # 创建客户端处理线程
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                )
                client_thread.start()
                self.client_threads.append(client_thread)

            except Exception as e:
                if self.is_running:
                    write_log(f"接受客户端连接出错: {e}", "ERROR")

    def _handle_client(self, client_socket, client_address):
        """
        处理客户端连接

        Args:
            client_socket: 客户端Socket
            client_address: 客户端地址 (ip, port)
        """
        write_log(f"开始处理客户端 {client_address}")

        buffer = b''
        device_id = None

        try:
            while self.is_running:
                # 设置超时
                client_socket.settimeout(60.0)

                # ---- 接收数据（独立 try-except） ----
                try:
                    data = client_socket.recv(4096)
                except ConnectionResetError:
                    write_log(f"客户端 {client_address} 重置连接（对端强制关闭）", "WARNING")
                    break
                except ConnectionAbortedError:
                    write_log(f"客户端 {client_address} 连接被中止", "WARNING")
                    break
                except socket.timeout:
                    write_log(f"客户端 {client_address} 接收超时", "WARNING")
                    break
                except OSError as e:
                    write_log(f"客户端 {client_address} Socket错误: {e}", "ERROR")
                    break

                if not data:
                    # 对端正常关闭连接
                    write_log(f"客户端 {client_address} 主动关闭连接 (recv返回空)", "INFO")
                    break

                write_log(f"收到客户端 {client_address} 数据: {len(data)} 字节", "DEBUG")
                buffer += data

                # ---- 解析并处理数据包（独立 try-except） ----
                while len(buffer) > 0:
                    try:
                        result = self._parse_packet(buffer)
                    except Exception as e:
                        write_log(f"数据包解析异常: {e}\n{traceback.format_exc()}", "ERROR")
                        # 打印前64字节便于排查数据格式问题
                        write_log(f"异常时缓冲区前64字节(hex): {buffer[:64].hex()}", "ERROR")
                        buffer = b''
                        break

                    if result is None:
                        # 数据不完整，等待更多数据
                        break

                    packet_type, packet_data, consumed = result

                    # 协议头对齐 / 数据无法识别时 packet_type 为 None
                    if packet_type is None:
                        # 仅丢弃前缀垃圾数据，继续解析后续内容
                        buffer = buffer[consumed:]
                        continue

                    buffer = buffer[consumed:]

                    # 处理数据包（每个包独立捕获，一个包出错不影响后续）
                    try:
                        if packet_type == PACKET_TYPE_JSON:
                            device_id = self._handle_json_packet(packet_data, client_address)

                        elif packet_type == PACKET_TYPE_IMAGE:
                            self._handle_image_packet(packet_data, device_id, client_address)

                        elif packet_type == PACKET_TYPE_COMPLETE:
                            self._handle_complete_packet(packet_data, client_address)

                        else:
                            write_log(f"未知数据包类型: {packet_type}", "WARNING")

                    except Exception as e:
                        write_log(f"数据包处理异常 (type={packet_type}): {e}\n{traceback.format_exc()}", "ERROR")
                        # 不跳出，继续处理下一个包

        except Exception as e:
            # 兜底：未预期的异常，打印完整堆栈
            write_log(f"处理客户端 {client_address} 严重错误: {e}\n{traceback.format_exc()}", "ERROR")

        finally:
            # 客户端断开
            write_log(f"客户端 {client_address} 断开连接")

            # 从在线设备中移除
            if client_address in self.online_devices:
                device_info = self.online_devices[client_address]
                write_log(f"设备离线: {device_info['device_id']}")

                # 通知UI
                if self.ui_callback:
                    self.ui_callback('device_offline', device_info['device_id'], client_address[0])

                del self.online_devices[client_address]

            # 关闭Socket
            try:
                client_socket.close()
            except Exception:
                pass

    def _parse_packet(self, buffer):
        """
        解析数据包，同时支持两种协议格式：
        - 标准协议：[CRACK_DATA 10字节][4字节类型][4字节长度][数据]
        - RK3588裸包：[4字节JSON长度][JSON][4字节图片长度][图片]

        Args:
            buffer: 数据缓冲区

        Returns:
            tuple: (packet_type, packet_data, consumed_bytes) 或 None (数据不完整)
        """
        # ---- 路径1: 标准CRACK_DATA协议 ----
        if len(buffer) >= HEADER_SIZE and buffer[:HEADER_SIZE] == PROTOCOL_HEADER:
            #return self._parse_standard_packet(buffer)
                    # 匹配到CRACK_DATA头后，跳过头部，按RK3588裸包格式解析后续内容
            raw_buffer = buffer[HEADER_SIZE:]
            result = self._parse_raw_packet(raw_buffer)
            if result is not None:
                pkt_type, pkt_data, raw_consumed = result
                total_consumed = HEADER_SIZE + raw_consumed
                return (pkt_type, pkt_data, total_consumed)
            else:
                return None
        # ---- 路径2: 缓冲区有CRACK_DATA但偏移了 ----
        if len(buffer) >= HEADER_SIZE:
            idx = buffer.find(PROTOCOL_HEADER)
            if idx > 0:
                write_log(f"协议头偏移 {idx} 字节，丢弃前缀数据", "WARNING")
                return (None, None, idx)

        # ---- 路径3: 没有CRACK_DATA头 → 尝试RK3588裸包格式 ----
        result = self._parse_raw_packet(buffer)
        if result is not None:
            return result

        # _parse_raw_packet 返回 None 有两种含义：
        #   1) 格式不识别 → 需要更多数据才能判断
        #   2) 格式已识别（JSON解析通过）但图片不完整 → 需要继续recv
        # 两种情况都不应丢弃缓冲区，返回None让_handle_client继续recv攒数据
        # 安全阀：缓冲区超过10MB仍未识别则丢弃防内存泄漏
        if len(buffer) > 10 * 1024 * 1024:
            write_log(f"缓冲区过大 ({len(buffer)} 字节)，强制丢弃", "WARNING")
            return (None, None, len(buffer))

        return None

    def _parse_standard_packet(self, buffer):
        """
        解析标准CRACK_DATA协议包

        Args:
            buffer: 数据缓冲区（已确认以CRACK_DATA开头）

        Returns:
            tuple: (packet_type, packet_data, consumed_bytes) 或 None (数据不完整)
        """
        # 检查是否有类型字段
        if len(buffer) < HEADER_SIZE + 4:
            return None

        # 获取数据包类型
        packet_type = int.from_bytes(buffer[HEADER_SIZE:HEADER_SIZE + 4], byteorder='big')

        # 检查是否有长度字段
        if len(buffer) < HEADER_SIZE + 4 + 4:
            return None

        # 获取数据长度
        data_length = int.from_bytes(buffer[HEADER_SIZE + 4:HEADER_SIZE + 8], byteorder='big')

        # 安全检查：数据长度异常大则判定为非法包
        if data_length > 10 * 1024 * 1024:  # 10MB
            write_log(f"标准包数据长度异常: {data_length} 字节，丢弃", "ERROR")
            return (None, None, len(buffer))

        # 检查是否有完整的数据
        if len(buffer) < HEADER_SIZE + 8 + data_length:
            return None

        # 提取数据
        packet_data = buffer[HEADER_SIZE + 8:HEADER_SIZE + 8 + data_length]
        consumed = HEADER_SIZE + 8 + data_length

        return (packet_type, packet_data, consumed)

    def _parse_raw_packet(self, buffer):
        """
        解析RK3588裸包格式：[4字节JSON长度][JSON][4字节图片长度][图片]
        整个裸包必须完整（JSON+图片全部收齐）才消费，图片不完整时返回None等待更多数据。
        图片bytes暂存到 self._pending_raw_image，由 _handle_complete_packet 通过信号转发给主线程保存。

        Args:
            buffer: 数据缓冲区

        Returns:
            tuple: (PACKET_TYPE_COMPLETE, json_bytes, consumed_bytes) 或 None
        """
        # 至少需要4字节才能读取JSON长度
        if len(buffer) < RAW_JSON_LEN_SIZE:
            return None

        json_length = int.from_bytes(buffer[:RAW_JSON_LEN_SIZE], byteorder='big')

        # 安全检查：长度合理性
        if json_length == 0 or json_length > 10 * 1024 * 1024:
            return None

        # JSON长度字段后的数据不足
        if len(buffer) < RAW_JSON_LEN_SIZE + json_length:
            return None

        # 提取JSON部分
        json_bytes = buffer[RAW_JSON_LEN_SIZE:RAW_JSON_LEN_SIZE + json_length]

        # 快速验证：JSON部分是否确实以 { 或 [ 开头
        if json_bytes and json_bytes[0:1] not in (b'{', b'['):
            return None

        # 尝试解析JSON以进一步确认格式正确
        try:
            json.loads(json_bytes)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None

        # ---- JSON 解析通过，计算整个裸包所需的总长度 ----
        offset_after_json = RAW_JSON_LEN_SIZE + json_length  # 4 + json_length
        image_data = b''
        image_length = 0

        if len(buffer) >= offset_after_json + RAW_IMAGE_LEN_SIZE:
            image_length = int.from_bytes(
                buffer[offset_after_json:offset_after_json + RAW_IMAGE_LEN_SIZE],
                byteorder='big'
            )

            # 图片长度合理性检查
            if image_length > 50 * 1024 * 1024:  # 50MB
                write_log(f"裸包图片长度异常: {image_length} 字节，仅处理JSON", "WARNING")
                consumed = offset_after_json
            elif image_length == 0:
                # 无图片数据
                consumed = offset_after_json + RAW_IMAGE_LEN_SIZE
            else:
                total_needed = offset_after_json + RAW_IMAGE_LEN_SIZE + image_length

                # ★ 图片数据不完整时返回None，等缓冲区攒够再一次性消费
                if len(buffer) < total_needed:
                    write_log(
                        f"裸包图片不完整: 需要 {total_needed} 字节, "
                        f"已有 {len(buffer)} 字节, 等待更多数据...",
                        "DEBUG"
                    )
                    return None

                image_data = buffer[
                    offset_after_json + RAW_IMAGE_LEN_SIZE:
                    offset_after_json + RAW_IMAGE_LEN_SIZE + image_length
                ]
                consumed = total_needed
        else:
            # 连图片长度字段都没收齐，等待更多数据
            return None

        # ★ 图片bytes暂存，由 _handle_complete_packet 通过信号转发到主线程保存
        self._pending_raw_image = image_data

        write_log(
            f"RK3588裸包解析成功: JSON {json_length} 字节"
            + (f", 图片 {len(image_data)} 字节" if image_data else ""),
            "SUCCESS"
        )

        # 返回原始JSON字节（不含image_path），主线程保存图片后补上
        return (PACKET_TYPE_COMPLETE, json_bytes, consumed)

    def _handle_json_packet(self, json_data, client_address):
        """
        处理JSON数据包

        Args:
            json_data: JSON数据
            client_address: 客户端地址

        Returns:
            str: 设备ID
        """
        try:
            # 解析JSON
            json_str = json_data.decode('utf-8')
            data = json.loads(json_str)

            device_id = data.get('device_id', 'UNKNOWN')

            write_log(f"收到JSON数据: 设备={device_id}, 裂缝数={data.get('crack_count', 0)}")

            # 更新在线设备
            self.online_devices[client_address] = {
                'device_id': device_id,
                'last_seen': datetime.now().timestamp()
            }

            # 通知UI设备上线
            if self.ui_callback:
                self.ui_callback('device_online', device_id, client_address[0])

            return device_id

        except json.JSONDecodeError as e:
            write_log(f"JSON解析失败: {e}", "ERROR")
            return None

        except Exception as e:
            write_log(f"处理JSON数据包失败: {e}", "ERROR")
            return None

    def _handle_image_packet(self, image_data, device_id, client_address):
        """
        处理图片数据包

        Args:
            image_data: 图片二进制数据
            device_id: 设备ID
            client_address: 客户端地址
        """
        try:
            if not device_id:
                write_log("未指定设备ID，忽略图片数据", "WARNING")
                return

            # 生成保存路径
            today = datetime.now().strftime('%Y-%m-%d')
            device_dir = os.path.join(IMAGES_DIR, today, device_id)
            os.makedirs(device_dir, exist_ok=True)

            # 生成文件名
            timestamp = datetime.now().strftime('%H%M%S')
            filename = f"crack_{timestamp}.jpg"
            file_path = os.path.join(device_dir, filename)

            # 保存图片
            with open(file_path, 'wb') as f:
                f.write(image_data)

            write_log(f"图片已保存: {file_path}")

            # 通知UI（可选，如果需要显示新图片）
            if self.ui_callback:
                self.ui_callback('new_image', file_path, {})

        except Exception as e:
            write_log(f"处理图片数据包失败: {e}", "ERROR")

    def _handle_complete_packet(self, complete_data, client_address):
        """
        处理完整数据包（JSON + 图片信息）
        解析JSON后通过Qt信号转发到主线程入库+保存图片，不在TCP子线程直接操作SQLite或写文件。

        Args:
            complete_data: 完整数据
            client_address: 客户端地址
        """
        try:
            # 解析JSON
            json_str = complete_data.decode('utf-8')
            data = json.loads(json_str)

            device_id = data.get('device_id', 'UNKNOWN')
            timestamp = data.get('timestamp', int(datetime.now().timestamp()))
            crack_count = data.get('crack_count', 0)
            max_width = data.get('max_width', 0.0)
            max_length = data.get('max_length', 0.0)
            avg_width = data.get('avg_width', 0.0)
            confidence = data.get('confidence', 0.0)
            image_path = data.get('image_path', '')
            entry_date = data.get('entry_date', datetime.now().strftime('%Y-%m-%d'))

            write_log(f"收到完整数据: 设备={device_id}, 裂缝数={crack_count}, "
                     f"最大宽度={max_width}mm, 置信度={confidence}%")

            # 更新在线设备（dict操作，线程安全）
            self.online_devices[client_address] = {
                'device_id': device_id,
                'last_seen': datetime.now().timestamp()
            }

            # 通知UI设备上线
            if self.ui_callback:
                self.ui_callback('device_online', device_id, client_address[0])

            # 构建入库记录字典（image_path由主线程保存图片后回填）
            record_data = {
                'device_id': device_id,
                'timestamp': timestamp,
                'crack_count': crack_count,
                'max_width': max_width,
                'max_length': max_length,
                'avg_width': avg_width,
                'confidence': confidence,
                'image_path': image_path if image_path else None,
                'ai_analysis': None,
                'entry_date': entry_date
            }

            # 取出裸包暂存的图片bytes（标准协议走image_path，裸包走bytes）
            img_bytes = getattr(self, '_pending_raw_image', b'')
            self._pending_raw_image = b''  # 用完即清

            # ★ 通过Qt信号转发到主线程：入库 + 保存图片 + 刷新UI
            if hasattr(self, 'main_win') and self.main_win is not None:
                self.main_win.new_crack_record.emit(record_data, img_bytes)
                write_log(f"数据已转发至主线程入库: 设备={device_id}, 图片{len(img_bytes)}字节", "SUCCESS")
            elif self.db:
                # 降级：无主窗口时直接写入（可能触发跨线程报错）
                record_id = self.db.add_record(record_data)
                if record_id > 0:
                    write_log(f"数据已存入数据库，记录ID: {record_id}", "SUCCESS")
                    crack_info = {
                        'device_id': device_id,
                        'crack_count': crack_count,
                        'max_width': max_width,
                        'confidence': confidence
                    }
                    if self.ui_callback:
                        self.ui_callback('new_record', image_path, crack_info)
                else:
                    write_log("数据存入数据库失败", "ERROR")

        except json.JSONDecodeError as e:
            write_log(f"完整数据包JSON解析失败: {e}", "ERROR")

        except Exception as e:
            write_log(f"处理完整数据包失败: {e}", "ERROR")

    def _check_heartbeat(self):
        """心跳检测，检查在线设备状态"""
        while self.is_running:
            try:
                current_time = datetime.now().timestamp()
                timeout = 300  # 5分钟超时

                # 检查每个在线设备
                offline_devices = []
                for address, device_info in list(self.online_devices.items()):
                    last_seen = device_info['last_seen']
                    if current_time - last_seen > timeout:
                        offline_devices.append((address, device_info['device_id']))

                # 移除超时设备
                for address, device_id in offline_devices:
                    write_log(f"设备心跳超时离线: {device_id}", "WARNING")
                    del self.online_devices[address]

                    # 通知UI
                    if self.ui_callback:
                        self.ui_callback('device_offline', device_id, address[0])

            except Exception as e:
                write_log(f"心跳检测出错: {e}", "ERROR")

            # 每30秒检查一次
            import time
            time.sleep(30)


# ============================================================
# TCP客户端发送工具（测试用）
# ============================================================

class TCPSender:
    """
    TCP客户端发送工具类
    用于RK3588端发送数据到PC上位机
    """

    def __init__(self, server_host, server_port):
        """
        初始化TCP发送工具

        Args:
            server_host (str): 服务器IP地址
            server_port (int): 服务器端口
        """
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = None

    def connect(self):
        """连接服务器"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_host, self.server_port))
            print(f"已连接到服务器: {self.server_host}:{self.server_port}")
            return True
        except Exception as e:
            print(f"连接服务器失败: {e}")
            return False

    def disconnect(self):
        """断开连接"""
        if self.client_socket:
            try:
                self.client_socket.close()
            except Exception:
                pass

    def send_json(self, json_data):
        """
        发送JSON数据

        Args:
            json_data (dict): JSON数据字典
        """
        if not self.client_socket:
            print("未连接到服务器")
            return False

        try:
            # 序列化JSON
            json_str = json.dumps(json_data, ensure_ascii=False)
            json_bytes = json_str.encode('utf-8')

            # 构建数据包
            packet = self._build_packet(PACKET_TYPE_JSON, json_bytes)

            # 发送
            self.client_socket.sendall(packet)
            print(f"JSON数据已发送: {json_data}")
            return True

        except Exception as e:
            print(f"发送JSON数据失败: {e}")
            return False

    def send_image(self, image_path):
        """
        发送图片数据

        Args:
            image_path (str): 图片路径
        """
        if not self.client_socket:
            print("未连接到服务器")
            return False

        if not os.path.exists(image_path):
            print(f"图片不存在: {image_path}")
            return False

        try:
            # 读取图片
            with open(image_path, 'rb') as f:
                image_data = f.read()

            # 构建数据包
            packet = self._build_packet(PACKET_TYPE_IMAGE, image_data)

            # 发送
            self.client_socket.sendall(packet)
            print(f"图片已发送: {image_path}")
            return True

        except Exception as e:
            print(f"发送图片失败: {e}")
            return False

    def send_complete_data(self, complete_data):
        """
        发送完整数据（JSON）

        Args:
            complete_data (dict): 完整数据字典
        """
        if not self.client_socket:
            print("未连接到服务器")
            return False

        try:
            # 序列化JSON
            json_str = json.dumps(complete_data, ensure_ascii=False)
            json_bytes = json_str.encode('utf-8')

            # 构建数据包
            packet = self._build_packet(PACKET_TYPE_COMPLETE, json_bytes)

            # 发送
            self.client_socket.sendall(packet)
            print(f"完整数据已发送: {complete_data}")
            return True

        except Exception as e:
            print(f"发送完整数据失败: {e}")
            return False

    def _build_packet(self, packet_type, data):
        """
        构建数据包

        Args:
            packet_type (int): 数据包类型
            data (bytes): 数据

        Returns:
            bytes: 完整数据包
        """
        # 协议头
        header = PROTOCOL_HEADER

        # 数据包类型
        type_bytes = packet_type.to_bytes(4, byteorder='big')

        # 数据长度
        length_bytes = len(data).to_bytes(4, byteorder='big')

        return header + type_bytes + length_bytes + data


# ============================================================
# 模块测试代码
# ============================================================

if __name__ == "__main__":
    print("墙体裂缝检测上位机 - TCP服务端模块测试")
    print("=" * 60)

    # 启动TCP服务端（测试模式）
    server = TCPServer(host='0.0.0.0', port=8888)

    if server.start():
        print("TCP服务端已启动，按Ctrl+C停止...")

        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n正在停止...")
            server.stop()

    # 测试TCP发送工具
    print("\n" + "=" * 60)
    print("测试TCP发送工具")

    sender = TCPSender('127.0.0.1', 8888)

    if sender.connect():
        # 发送测试JSON
        test_json = {
            'device_id': 'RK3588_001',
            'timestamp': int(datetime.now().timestamp()),
            'crack_count': 3,
            'max_width': 2.5,
            'max_length': 15.8,
            'avg_width': 1.2,
            'confidence': 95.5,
            'entry_date': datetime.now().strftime('%Y-%m-%d')
        }
        sender.send_json(test_json)

        # 发送完整数据
        test_complete = {
            'device_id': 'RK3588_001',
            'timestamp': int(datetime.now().timestamp()),
            'crack_count': 2,
            'max_width': 1.8,
            'max_length': 12.3,
            'avg_width': 0.9,
            'confidence': 92.0,
            'image_path': '',
            'entry_date': datetime.now().strftime('%Y-%m-%d')
        }
        sender.send_complete_data(test_complete)

        sender.disconnect()

    print("\n测试完成！")