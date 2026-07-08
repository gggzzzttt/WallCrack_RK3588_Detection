#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
墙体裂缝检测上位机 - 主程序
功能:接收RK3588板卡上传的裂缝识别数据，可视化展示、存储、分析
硬件:PC上位机TCP服务端，RK3588 WiFi上传数据，无外接传感器
"""

# ============================================================
# 第一部分:库导入
# ============================================================

import os
import json
import threading
import requests
import base64
import shutil
from datetime import timedelta, datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton, QLineEdit, QTextEdit,
    QTableWidget, QTableWidgetItem, QComboBox, QSpinBox,
    QDoubleSpinBox, QDateEdit, QGroupBox, QSplitter, QScrollArea,
    QFileDialog, QMessageBox, QProgressBar, QCheckBox
)
from PyQt5.QtCore import Qt, QDate, QTimer, QThread, pyqtSignal, QObject, QCoreApplication
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor

import pyqtgraph as pg
import numpy as np
# 导入数据库操作模块
from db_operator import DatabaseOperator

# 导入TCP服务端模块
from tcp_server import TCPServer

# ============================================================
# 第二部分:全局常量定义
# ============================================================

# 应用信息
APP_NAME = "墙体裂缝检测上位机"
APP_VERSION = "V1.0.0"

# 默认配置
DEFAULT_TCP_PORT = 8888
DEFAULT_API_KEY = ""

# 文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# 数据库路径
DB_PATH = os.path.join(DATA_DIR, "crack_detection.db")

# 日志路径
LOG_PATH = os.path.join(LOGS_DIR, "app.log")

# 告警阈值
CRACK_WIDTH_ALARM_THRESHOLD = 5.0  # 裂缝宽度告警阈值(mm)
DAILY_CRACK_COUNT_ALARM_THRESHOLD = 50  # 单日裂缝数量告警阈值

# ============================================================
# 第三部分:Tab1 - 实时监控页面
# ============================================================

class RealTimeMonitorTab(QWidget):
    """
    Tab1:实时监控页面
    功能:显示在线设备列表、实时裂缝缩略图、今日裂缝统计仪表盘
    """

    def __init__(self, db=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.online_devices = {}  # 在线设备字典 {device_id: {'ip': str, 'last_seen': timestamp}}
        self.init_ui()
        # 绑定按钮信号
        # self.bind_signals()
        # 创建定时器，定时刷新统计信息
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.update_today_stats)
        self.refresh_timer.start(5000)  # 每5秒刷新一次
        # 初始化加载数据
        self.update_today_stats()
        self.refresh_device_list()

    def init_ui(self):
        """初始化UI布局"""
        # 主布局 - 水平分割
        main_layout = QHBoxLayout(self)

        # 创建分割器:左侧设备列表，右侧监控面板
        splitter = QSplitter(Qt.Horizontal)

        # ========== 左侧:在线设备列表 ==========
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # 设备列表标题
        device_title = QLabel("在线设备列表")
        device_title.setFont(QFont("Arial", 12, QFont.Bold))
        left_layout.addWidget(device_title)

        # 设备列表表格占位
        self.device_table = QTableWidget()
        self.device_table.setColumnCount(3)
        self.device_table.setHorizontalHeaderLabels(["设备ID", "IP地址", "状态"])
        self.device_table.setMinimumWidth(200)
        left_layout.addWidget(self.device_table)

        # 设备统计信息
        device_stats_group = QGroupBox("设备统计")
        device_stats_layout = QHBoxLayout()
        self.online_device_label = QLabel("在线设备: 0")
        self.total_device_label = QLabel("总设备数: 0")
        device_stats_layout.addWidget(self.online_device_label)
        device_stats_layout.addWidget(self.total_device_label)
        device_stats_group.setLayout(device_stats_layout)
        left_layout.addWidget(device_stats_group)

        splitter.addWidget(left_widget)

        # ========== 右侧:监控面板 ==========
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # 顶部:今日统计仪表盘
        stats_group = QGroupBox("今日裂缝统计")
        stats_layout = QHBoxLayout()

        # 统计卡片占位
        self.today_count_label = QLabel("今日裂缝数: 0")
        self.today_count_label.setStyleSheet("font-size: 18px; color: #2196F3; font-weight: bold;")

        self.max_width_label = QLabel("最大裂缝宽: 0.0mm")
        self.max_width_label.setStyleSheet("font-size: 18px; color: #FF5722; font-weight: bold;")

        self.max_length_label = QLabel("最大裂缝长: 0.0mm")
        self.max_length_label.setStyleSheet("font-size: 18px; color: #4CAF50; font-weight: bold;")

        self.avg_confidence_label = QLabel("平均置信度: 0.0%")
        self.avg_confidence_label.setStyleSheet("font-size: 18px; color: #9C27B0; font-weight: bold;")

        stats_layout.addWidget(self.today_count_label)
        stats_layout.addWidget(self.max_width_label)
        stats_layout.addWidget(self.max_length_label)
        stats_layout.addWidget(self.avg_confidence_label)
        stats_group.setLayout(stats_layout)
        right_layout.addWidget(stats_group)

        # 中部:实时裂缝缩略图区域
        images_group = QGroupBox("实时裂缝缩略图")
        images_layout = QVBoxLayout()

        # 滚动区域用于显示图片
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.image_container = QWidget()
        self.image_layout = QVBoxLayout(self.image_container)
        scroll_area.setWidget(self.image_container)
        images_layout.addWidget(scroll_area)

        # 图片控制按钮
        image_control_layout = QHBoxLayout()
        self.refresh_images_btn = QPushButton("刷新图片")
        self.clear_images_btn = QPushButton("清空显示")
        image_control_layout.addWidget(self.refresh_images_btn)
        image_control_layout.addWidget(self.clear_images_btn)
        images_layout.addLayout(image_control_layout)

        images_group.setLayout(images_layout)
        right_layout.addWidget(images_group)

        splitter.addWidget(right_widget)

        # 设置分割器比例
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        main_layout.addWidget(splitter)

        # ========== 底部:日志窗口占位 ==========
        log_group = QGroupBox("系统运行日志")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        right_layout.addWidget(log_group)

    def bind_signals(self):
        """绑定按钮信号"""
        self.refresh_images_btn.clicked.connect(self.refresh_images)
        self.clear_images_btn.clicked.connect(self.clear_images)

    # ================= 功能函数实现 =================

    def refresh_device_list(self):
        """刷新在线设备列表：优先展示在线设备，再补充数据库历史设备"""
        # 清空设备表格
        self.device_table.setRowCount(0)

        # 合并设备列表：在线设备 + 数据库历史设备（去重）
        db_devices = self.db.get_all_devices() if self.db else []
        seen = set()
        all_devices = []

        # 在线设备优先
        for device_id in self.online_devices:
            if device_id not in seen:
                all_devices.append(device_id)
                seen.add(device_id)

        # 补充数据库中不在线的设备
        for device_id in db_devices:
            if device_id not in seen:
                all_devices.append(device_id)
                seen.add(device_id)

        # 填充设备表格
        for row, device_id in enumerate(all_devices):
            self.device_table.insertRow(row)

            # 设备ID
            self.device_table.setItem(row, 0, QTableWidgetItem(device_id))

            # IP地址和状态（从在线设备字典获取）
            if device_id in self.online_devices:
                ip = self.online_devices[device_id]['ip']
                status = "在线"
                status_color = "#4CAF50"  # 绿色
            else:
                ip = "-"
                status = "离线"
                status_color = "#F44336"  # 红色

            self.device_table.setItem(row, 1, QTableWidgetItem(ip))

            # 状态
            status_item = QTableWidgetItem(status)
            status_item.setForeground(Qt.white)
            status_item.setBackground(QColor(status_color))
            self.device_table.setItem(row, 2, status_item)

        # 调整列宽
        self.device_table.resizeColumnsToContents()

        # 更新设备统计信息
        online_count = len(self.online_devices)
        total_devices = len(all_devices)
        self.online_device_label.setText(f"在线设备: {online_count}")
        self.total_device_label.setText(f"总设备数: {total_devices}")

    def update_device_status(self, device_id, ip, status="online"):
        """
        更新设备状态

        Args:
            device_id (str): 设备ID
            ip (str): 设备IP地址
            status (str): 状态，"online"或"offline"
        """
        from datetime import datetime

        if status == "online":
            self.online_devices[device_id] = {
                'ip': ip,
                'last_seen': datetime.now().timestamp()
            }
            self.log_message(f"设备 {device_id} ({ip}) 上线", "INFO")
        else:
            if device_id in self.online_devices:
                del self.online_devices[device_id]
            self.log_message(f"设备 {device_id} 离线", "WARNING")

        # 刷新设备列表显示
        self.refresh_device_list()

    def add_crack_image(self, image_path, crack_info):
        """
        添加裂缝缩略图到显示区域

        Args:
            image_path (str): 图片路径
            crack_info (dict): 裂缝信息字典
        """
        if not os.path.exists(image_path):
            self.log_message(f"图片不存在: {image_path}", "ERROR")
            return

        # 创建图片容器
        image_container = QWidget()
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(5, 5, 5, 5)

        # 加载并缩放图片
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # 创建图片标签
        image_label = QLabel()
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(image_label)

        # 创建信息标签
        info_text = (f"设备: {crack_info.get('device_id', 'N/A')} | "
                    f"裂缝数: {crack_info.get('crack_count', 0)} | "
                    f"最大宽度: {crack_info.get('max_width', 0):.2f}mm | "
                    f"置信度: {crack_info.get('confidence', 0):.1f}%")
        info_label = QLabel(info_text)
        info_label.setStyleSheet("font-size: 10px; color: #666;")
        info_label.setWordWrap(True)
        image_layout.addWidget(info_label)

        # 添加到图片容器
        self.image_layout.insertWidget(0, image_container)  # 插入到顶部

        # 限制显示的图片数量（最多显示20张）
        while self.image_layout.count() > 20:
            widget = self.image_layout.takeAt(self.image_layout.count() - 1).widget()
            widget.deleteLater()

        self.log_message(f"添加裂缝图片: {image_path}", "INFO")

    def update_today_stats(self):
        """更新今日统计信息"""
        if not self.db:
            return

        try:
            # 获取今日统计数据
            stats = self.db.get_today_statistics()

            # 更新标签显示
            self.today_count_label.setText(f"今日裂缝数: {stats['total_cracks']}")
            self.max_width_label.setText(f"最大裂缝宽: {stats['max_width']:.2f}mm")

            # 计算最大长度（从今日记录中获取）
            from datetime import datetime
            today = datetime.now().strftime('%Y-%m-%d')
            today_records = self.db.query_by_date(today, device_id=None)

            max_length = 0.0
            if today_records:
                max_length = max(r['max_length'] for r in today_records)

            self.max_length_label.setText(f"最大裂缝长: {max_length:.2f}mm")
            self.avg_confidence_label.setText(f"平均置信度: {stats['avg_confidence']:.1f}%")

            # 检查告警条件
            self.check_crack_alarm(stats)

        except Exception as e:
            self.log_message(f"更新今日统计失败: {str(e)}", "ERROR")

    def refresh_images(self):
        """刷新图片显示（加载今日最新图片）"""
        if not self.db:
            return

        # 清空当前图片显示
        self.clear_images()

        # 获取今日记录（倒序，最新的在前）
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')

        conditions = {
            'start_date': today,
            'end_date': today,
            'has_image': True
        }

        result = self.db.query_records(
            conditions=conditions, page=1, page_size=10,
            order_by='id', order='DESC'
        )

        # 添加图片到显示区域
        for record in result['records']:
            if record['image_path']:
                crack_info = {
                    'device_id': record['device_id'],
                    'crack_count': record['crack_count'],
                    'max_width': record['max_width'],
                    'confidence': record['confidence']
                }
                self.add_crack_image(record['image_path'], crack_info)

        self.log_message(f"已刷新 {len(result['records'])} 张今日图片", "INFO")

    def clear_images(self):
        """清空图片显示"""
        # 清空图片容器
        while self.image_layout.count():
            widget = self.image_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        self.log_message("已清空图片显示", "INFO")

    def log_message(self, message, level="INFO"):
        """
        写入日志消息

        Args:
            message (str): 日志消息
            level (str): 日志级别
        """
        from datetime import datetime

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 根据级别设置颜色
        color_map = {
            "INFO": "#2196F3",      # 蓝色
            "WARNING": "#FF9800",   # 橙色
            "ERROR": "#F44336",     # 红色
            "SUCCESS": "#4CAF50"    # 绿色
        }

        color = color_map.get(level, "#000000")

        # 添加日志到文本框
        log_entry = f'<span style="color: {color};">[{timestamp}] [{level}] {message}</span><br>'
        self.log_text.insertHtml(log_entry)

        # 自动滚动到底部
        cursor = self.log_text.textCursor()
        cursor.movePosition(cursor.End)
        self.log_text.setTextCursor(cursor)

        # 同时写入文件
        try:
            with open(LOG_PATH, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] [{level}] {message}\n")
        except Exception:
            pass

    def show_alarm(self, message, alarm_type="WARNING"):
        """
        显示告警弹窗

        Args:
            message (str): 告警消息
            alarm_type (str): 告警类型，"WARNING"或"ERROR"
        """
        # 在日志中记录
        self.log_message(f"告警: {message}", alarm_type)

        # 显示弹窗
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning if alarm_type == "WARNING" else QMessageBox.Critical)
        msg_box.setWindowTitle("告警提醒")
        msg_box.setText(message)
        msg_box.exec_()

        # 更新系统状态
        if self.parent():
            self.parent().update_status(f"告警: {message}")

    def check_crack_alarm(self, stats):
        """
        检查裂缝告警条件

        Args:
            stats (dict): 今日统计数据
        """
        # 检查单日裂缝数量告警
        if stats['total_cracks'] >= DAILY_CRACK_COUNT_ALARM_THRESHOLD:
            message = (f"今日裂缝数量突增！\n"
                      f"当前裂缝数: {stats['total_cracks']}\n"
                      f"告警阈值: {DAILY_CRACK_COUNT_ALARM_THRESHOLD}")
            self.show_alarm(message, "WARNING")

        # 检查超大裂缝告警
        if stats['max_width'] >= CRACK_WIDTH_ALARM_THRESHOLD:
            message = (f"检测到超大裂缝！\n"
                      f"最大宽度: {stats['max_width']:.2f}mm\n"
                      f"告警阈值: {CRACK_WIDTH_ALARM_THRESHOLD}mm")
            self.show_alarm(message, "ERROR")


# ============================================================
# 第四部分:Tab2 - 历史记录查询页面
# ============================================================

class HistoryQueryTab(QWidget):
    """
    Tab2:历史记录查询页面
    功能:数据表格展示识别记录，条件筛选，双击查看原图
    """
    def __init__(self, db, main_window):
        super().__init__()
        self.db = db
        self.main_window = main_window  # 保存主窗口引用
    # ... 其余原有代码 ...
    #def __init__(self, db=None, parent=None):
      #  super().__init__(parent)
      #  self.db = db
        self.init_ui()
        # 绑定按钮信号
        self.bind_signals()
        # 初始化加载数据
        self.refresh_device_combo()
        #self.refresh_table()

    def init_ui(self):
        """初始化UI布局"""
        # 主布局 - 垂直
        main_layout = QVBoxLayout(self)

        # ========== 顶部:条件筛选区 ==========
        filter_group = QGroupBox("查询条件")
        filter_layout = QHBoxLayout()

        # 时间段筛选
        filter_layout.addWidget(QLabel("起始日期:"))
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate().addDays(-30))
        self.start_date_edit.setCalendarPopup(True)
        filter_layout.addWidget(self.start_date_edit)

        filter_layout.addWidget(QLabel("结束日期:"))
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setCalendarPopup(True)
        filter_layout.addWidget(self.end_date_edit)

        # 设备筛选
        filter_layout.addWidget(QLabel("设备ID:"))
        self.device_combo = QComboBox()
        self.device_combo.addItem("全部设备")
        filter_layout.addWidget(self.device_combo)

        # 裂缝宽度筛选
        filter_layout.addWidget(QLabel("最小宽度(mm):"))
        self.min_width_spin = QDoubleSpinBox()
        self.min_width_spin.setRange(0, 100)
        self.min_width_spin.setDecimals(2)
        self.min_width_spin.setValue(0)
        filter_layout.addWidget(self.min_width_spin)

        filter_layout.addWidget(QLabel("最大宽度(mm):"))
        self.max_width_spin = QDoubleSpinBox()
        self.max_width_spin.setRange(0, 100)
        self.max_width_spin.setDecimals(2)
        self.max_width_spin.setValue(10)
        filter_layout.addWidget(self.max_width_spin)

        # 置信度筛选
        filter_layout.addWidget(QLabel("最小置信度(%):"))
        self.min_confidence_spin = QDoubleSpinBox()
        self.min_confidence_spin.setRange(0, 100)
        self.min_confidence_spin.setValue(50)
        filter_layout.addWidget(self.min_confidence_spin)

        # 查询按钮
        self.query_btn = QPushButton("查询")
        filter_layout.addWidget(self.query_btn)

        # 重置按钮
        self.reset_btn = QPushButton("重置")
        filter_layout.addWidget(self.reset_btn)

        filter_group.setLayout(filter_layout)
        main_layout.addWidget(filter_group)

        # ========== 中部:数据表格 ==========
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(10)
        self.data_table.setHorizontalHeaderLabels([
            "记录ID", "设备ID", "时间", "裂缝条数",
            "最大宽度", "最大长度", "平均宽度",
            "置信度", "图片路径", "AI分析"
        ])
        self.data_table.setAlternatingRowColors(True)
        self.data_table.setSelectionBehavior(QTableWidget.SelectRows)
        main_layout.addWidget(self.data_table)

        # ========== 底部:操作按钮区 ==========
        button_layout = QHBoxLayout()

        self.export_excel_btn = QPushButton("导出Excel")
        self.batch_view_btn = QPushButton("批量查看原图")
        self.delete_selected_btn = QPushButton("删除选中记录")
        self.refresh_table_btn = QPushButton("刷新表格")

        button_layout.addWidget(self.export_excel_btn)
        button_layout.addWidget(self.batch_view_btn)
        button_layout.addWidget(self.delete_selected_btn)
        button_layout.addWidget(self.refresh_table_btn)

        main_layout.addLayout(button_layout)

    def bind_signals(self):
        """绑定按钮信号"""
        self.query_btn.clicked.connect(self.query_records)
        self.reset_btn.clicked.connect(self.reset_filters)
        self.data_table.doubleClicked.connect(self.on_table_double_click)
        self.data_table.itemSelectionChanged.connect(self.on_selection_changed)  # 新增：选中记录变化时更新AI Tab
        self.export_excel_btn.clicked.connect(self.export_to_excel)
        self.batch_view_btn.clicked.connect(self.batch_view_images)
        self.delete_selected_btn.clicked.connect(self.delete_selected_records)
        self.refresh_table_btn.clicked.connect(self.refresh_table)

    def on_table_double_click(self, index):
        """表格双击事件"""
        row = index.row()
        record_id = self.data_table.item(row, 0).text()
        image_path = self.data_table.item(row, 8).text()
        record_info = {
            'id': record_id,
            'device_id': self.data_table.item(row, 1).text(),
            'time': self.data_table.item(row, 2).text(),
            'crack_count': self.data_table.item(row, 3).text(),
            'max_width': self.data_table.item(row, 4).text(),
            'max_length': self.data_table.item(row, 5).text(),
            'avg_width': self.data_table.item(row, 6).text(),
            'confidence': self.data_table.item(row, 7).text(),
            'image_path': image_path,
            'ai_analysis': self.data_table.item(row, 9).text()
        }
        self.show_image_dialog(image_path, record_info)

    def on_selection_changed(self):
        """表格选中记录变化时，更新AI Tab的选中记录"""
        selected_rows = self.get_selected_rows()
        records = []
        for row in selected_rows:
            try:
                # 解析表格单元格数据为记录格式
                timestamp_str = self.data_table.item(row, 2).text()
                from datetime import datetime
                # 尝试解析时间字符串
                try:
                    ts = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S').timestamp()
                except:
                    ts = int(datetime.now().timestamp())

                record = {
                    'id': int(self.data_table.item(row, 0).text()),
                    'device_id': self.data_table.item(row, 1).text(),
                    'timestamp': ts,
                    'crack_count': int(self.data_table.item(row, 3).text()),
                    'max_width': float(self.data_table.item(row, 4).text()),
                    'max_length': float(self.data_table.item(row, 5).text()),
                    'avg_width': float(self.data_table.item(row, 6).text()),
                    'confidence': float(self.data_table.item(row, 7).text().replace('%', '')),
                    'image_path': self.data_table.item(row, 8).text(),
                    'ai_analysis': self.data_table.item(row, 9).text()
                }
                records.append(record)
            except Exception as e:
                print(f"解析选中记录行{row}失败: {e}")
                continue

        # 使用 self.window() 获取 MainWindow，兼容 Tab 组件的 parent 机制
        main_win = self.window()
        if main_win and hasattr(main_win, 'ai_tab'):
            main_win.ai_tab.update_selected_records(records)
            print(f"[历史记录] 已更新AI Tab选中记录: {len(records)}条")
        else:
            print(f"[历史记录] 无法访问AI Tab - main_win: {main_win}")

    # ================= 功能函数实现 =================

    def query_records(self):
        """根据条件查询历史记录"""
        if not self.db:
            return

        # 构建查询条件
        conditions = {}

        # 起始日期
        start_date = self.start_date_edit.date().toString('yyyy-MM-dd')
        conditions['start_date'] = start_date

        # 结束日期
        end_date = self.end_date_edit.date().toString('yyyy-MM-dd')
        conditions['end_date'] = end_date

        # 设备ID
        device_index = self.device_combo.currentIndex()
        if device_index > 0:  # 0是"全部设备"
            device_id = self.device_combo.currentText()
            conditions['device_id'] = device_id

        # 最小宽度
        min_width = self.min_width_spin.value()
        if min_width > 0:
            conditions['min_width'] = min_width

        # 最大宽度
        max_width = self.max_width_spin.value()
        if max_width < 100:  # 默认最大值100
            conditions['max_width'] = max_width

        # 最小置信度
        min_confidence = self.min_confidence_spin.value()
        if min_confidence > 0:
            conditions['min_confidence'] = min_confidence

        # 执行查询
        result = self.db.query_records(conditions=conditions, page=1, page_size=1000)
        self.load_records_to_table(result['records'])

        # 显示查询结果信息
        #self.parent().status_bar.showMessage(f"查询完成，共找到 {result['total']} 条记录")
        self.main_window.status_bar.showMessage(f"查询完成，共找到 {result['total']} 条记录")
    def reset_filters(self):
        """重置筛选条件"""
        self.start_date_edit.setDate(QDate.currentDate().addDays(-30))
        self.end_date_edit.setDate(QDate.currentDate())
        self.device_combo.setCurrentIndex(0)
        self.min_width_spin.setValue(0)
        self.max_width_spin.setValue(10)
        self.min_confidence_spin.setValue(50)
        self.refresh_table()

    def load_records_to_table(self, records):
        """加载记录到表格"""
        self.data_table.setRowCount(0)

        for row, record in enumerate(records):
            self.data_table.insertRow(row)

            # 记录ID
            self.data_table.setItem(row, 0, QTableWidgetItem(str(record['id'])))

            # 设备ID
            self.data_table.setItem(row, 1, QTableWidgetItem(record['device_id']))

            # 时间（从timestamp转换）
            from datetime import datetime
            time_str = datetime.fromtimestamp(record['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            self.data_table.setItem(row, 2, QTableWidgetItem(time_str))

            # 裂缝条数
            self.data_table.setItem(row, 3, QTableWidgetItem(str(record['crack_count'])))

            # 最大宽度
            self.data_table.setItem(row, 4, QTableWidgetItem(f"{record['max_width']:.2f}"))

            # 最大长度
            self.data_table.setItem(row, 5, QTableWidgetItem(f"{record['max_length']:.2f}"))

            # 平均宽度
            self.data_table.setItem(row, 6, QTableWidgetItem(f"{record['avg_width']:.2f}"))

            # 置信度
            self.data_table.setItem(row, 7, QTableWidgetItem(f"{record['confidence']:.1f}%"))

            # 图片路径
            image_path = record['image_path'] or ''
            self.data_table.setItem(row, 8, QTableWidgetItem(image_path))

            # AI分析
            ai_analysis = record['ai_analysis'] or ''
            display_text = ai_analysis[:20] + '...' if len(ai_analysis) > 20 else ai_analysis
            self.data_table.setItem(row, 9, QTableWidgetItem(display_text))

        # 调整列宽
        self.data_table.resizeColumnsToContents()

    def show_image_dialog(self, image_path, record_info):
        """显示原图弹窗"""
        dialog = QMessageBox(self)
        dialog.setWindowTitle("裂缝原图")

        # 检查图片是否存在
        if not image_path or not os.path.exists(image_path):
            dialog.setText(f"图片不存在或未指定\n\n记录ID: {record_info['id']}\n"
                          f"设备ID: {record_info['device_id']}\n"
                          f"时间: {record_info['time']}\n"
                          f"裂缝条数: {record_info['crack_count']}\n"
                          f"最大宽度: {record_info['max_width']}mm\n"
                          f"最大长度: {record_info['max_length']}mm\n"
                          f"置信度: {record_info['confidence']}")
        else:
            # 创建自定义弹窗显示图片
            from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
            image_dialog = QDialog(self)
            image_dialog.setWindowTitle(f"裂缝原图 - 记录ID: {record_info['id']}")
            image_dialog.setMinimumSize(800, 600)

            layout = QVBoxLayout(image_dialog)

            # 显示图片
            pixmap = QPixmap(image_path)
            image_label = QLabel()
            image_label.setPixmap(pixmap.scaled(700, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            image_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(image_label)

            # 显示信息
            info_text = (f"设备ID: {record_info['device_id']} | "
                        f"时间: {record_info['time']} | "
                        f"裂缝条数: {record_info['crack_count']} | "
                        f"最大宽度: {record_info['max_width']}mm | "
                        f"最大长度: {record_info['max_length']}mm | "
                        f"置信度: {record_info['confidence']}")
            info_label = QLabel(info_text)
            info_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(info_label)

            image_dialog.exec_()
            return

        dialog.exec_()

    def export_to_excel(self):
        """导出Excel报表"""
        if not self.db:
            QMessageBox.warning(self, "导出失败", "数据库未连接")
            return

        # 获取导出文件路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出Excel报表", os.path.join(REPORTS_DIR, "crack_records.xlsx"),
            "Excel文件 (*.xlsx *.xls)"
        )

        if not file_path:
            return

        try:
            # 获取当前表格中的所有记录
            records = []
            for row in range(self.data_table.rowCount()):
                record = {
                    'id': self.data_table.item(row, 0).text(),
                    'device_id': self.data_table.item(row, 1).text(),
                    'time': self.data_table.item(row, 2).text(),
                    'crack_count': self.data_table.item(row, 3).text(),
                    'max_width': self.data_table.item(row, 4).text(),
                    'max_length': self.data_table.item(row, 5).text(),
                    'avg_width': self.data_table.item(row, 6).text(),
                    'confidence': self.data_table.item(row, 7).text(),
                    'image_path': self.data_table.item(row, 8).text(),
                    'ai_analysis': self.data_table.item(row, 9).text()
                }
                records.append(record)

            # 导出为CSV格式（如需.xlsx可安装openpyxl库）
            import csv
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                # 写入表头
                writer.writerow(['记录ID', '设备ID', '时间', '裂缝条数',
                               '最大宽度', '最大长度', '平均宽度', '置信度', '图片路径', 'AI分析'])
                # 写入数据
                for record in records:
                    writer.writerow([
                        record['id'], record['device_id'], record['time'],
                        record['crack_count'], record['max_width'], record['max_length'],
                        record['avg_width'], record['confidence'], record['image_path'], record['ai_analysis']
                    ])

            QMessageBox.information(self, "导出成功", f"已导出 {len(records)} 条记录到:\n{file_path}")
            self.parent().status_bar.showMessage(f"Excel导出成功: {os.path.basename(file_path)}")

        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出Excel失败:\n{str(e)}")

    def batch_view_images(self):
        """批量查看原图"""
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            QMessageBox.warning(self, "提示", "请先选择要查看的记录")
            return

        # 显示确认对话框
        reply = QMessageBox.question(
            self, "确认查看", f"确定要查看选中的 {len(selected_rows)} 张图片吗？",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            for row in selected_rows:
                image_path = self.data_table.item(row, 8).text()
                if image_path and os.path.exists(image_path):
                    # 获取记录信息
                    record_info = {
                        'id': self.data_table.item(row, 0).text(),
                        'device_id': self.data_table.item(row, 1).text(),
                        'time': self.data_table.item(row, 2).text(),
                        'crack_count': self.data_table.item(row, 3).text(),
                        'max_width': self.data_table.item(row, 4).text(),
                        'max_length': self.data_table.item(row, 5).text(),
                        'confidence': self.data_table.item(row, 7).text()
                    }
                    self.show_image_dialog(image_path, record_info)

    def delete_selected_records(self):
        """删除选中记录"""
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            QMessageBox.warning(self, "提示", "请先选择要删除的记录")
            return

        # 获取要删除的记录ID
        record_ids = []
        for row in selected_rows:
            record_id = int(self.data_table.item(row, 0).text())
            record_ids.append(record_id)

        # 显示确认对话框
        reply = QMessageBox.question(
            self, "确认删除", f"确定要删除选中的 {len(record_ids)} 条记录吗？\n此操作不可恢复！",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            result = self.db.batch_delete_records(record_ids)
            if result['success']:
                QMessageBox.information(self, "删除成功",
                                      f"成功删除 {result['deleted_count']} 条记录")
                self.refresh_table()
                self.parent().status_bar.showMessage(f"删除成功: {result['deleted_count']} 条记录")
            else:
                QMessageBox.warning(self, "删除部分成功",
                                  f"成功删除 {result['deleted_count']} 条\n失败 {result['failed_count']} 条")
                self.refresh_table()

    def refresh_table(self):
        """刷新表格数据"""
        if not self.db:
            return
        self.query_records()

    def refresh_device_combo(self):
        """刷新设备下拉列表"""
        if not self.db:
            return

        # 保存当前选中的设备
        current_device = self.device_combo.currentText()

        # 清空并重新填充
        self.device_combo.clear()
        self.device_combo.addItem("全部设备")

        # 获取所有设备ID
        devices = self.db.get_all_devices()
        for device_id in devices:
            self.device_combo.addItem(device_id)

        # 恢复之前选中的设备（如果还存在）
        index = self.device_combo.findText(current_device)
        if index >= 0:
            self.device_combo.setCurrentIndex(index)

    def get_selected_rows(self):
        """获取选中行"""
        selected_items = self.data_table.selectedItems()
        selected_rows = set()
        for item in selected_items:
            selected_rows.add(item.row())
        return sorted(list(selected_rows))

    def get_selected_records(self):
        """获取选中记录"""
        selected_rows = self.get_selected_rows()
        records = []
        for row in selected_rows:
            record = {
                'id': int(self.data_table.item(row, 0).text()),
                'device_id': self.data_table.item(row, 1).text(),
                'timestamp': int(self.data_table.item(row, 2).text()),
                'crack_count': int(self.data_table.item(row, 3).text()),
                'max_width': float(self.data_table.item(row, 4).text()),
                'max_length': float(self.data_table.item(row, 5).text()),
                'avg_width': float(self.data_table.item(row, 6).text()),
                'confidence': float(self.data_table.item(row, 7).text()),
                'image_path': self.data_table.item(row, 8).text(),
                'ai_analysis': self.data_table.item(row, 9).text()
            }
            records.append(record)
        return records


# ============================================================
# 第五部分:Tab3 - 统计图表页面
# ============================================================

class StatisticsTab(QWidget):
    """
    Tab3:统计图表页面
    功能:每日裂缝数量折线图、裂缝宽度分布直方图
    """

    def __init__(self, db=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()
        # 绑定按钮信号
        self.bind_signals()
        # 初始化加载数据
        self.refresh_device_combo()
        self.generate_charts()

    def init_ui(self):
        """初始化UI布局"""
        # 主布局 - 垂直
        main_layout = QVBoxLayout(self)

        # ========== 顶部:图表参数选择 ==========
        param_group = QGroupBox("图表参数")
        param_layout = QHBoxLayout()

        param_layout.addWidget(QLabel("统计周期:"))
        self.period_combo = QComboBox()
        self.period_combo.addItems(["最近7天", "最近30天", "最近90天", "自定义"])
        param_layout.addWidget(self.period_combo)

        param_layout.addWidget(QLabel("设备:"))
        self.device_combo = QComboBox()
        self.device_combo.addItem("全部设备")
        param_layout.addWidget(self.device_combo)

        self.generate_chart_btn = QPushButton("生成图表")
        param_layout.addWidget(self.generate_chart_btn)

        self.export_chart_btn = QPushButton("导出图表")
        param_layout.addWidget(self.export_chart_btn)

        param_group.setLayout(param_layout)
        main_layout.addWidget(param_group)

        # ========== 中部:图表展示区 ==========
        chart_layout = QVBoxLayout()

        # 折线图
        line_chart_group = QGroupBox("每日裂缝数量趋势")
        line_chart_layout = QVBoxLayout()
        self.line_chart_widget = pg.PlotWidget()
        self.line_chart_widget.setBackground('#FFFFFF')
        self.line_chart_widget.setTitle("每日裂缝数量", color='#2196F3')
        self.line_chart_widget.setLabel('left', '裂缝数量', color='#666')
        self.line_chart_widget.setLabel('bottom', '日期', color='#666')
        self.line_chart_widget.showGrid(x=True, y=True, alpha=0.3)
        self.line_chart_widget.setMinimumHeight(300)
        line_chart_layout.addWidget(self.line_chart_widget)
        line_chart_group.setLayout(line_chart_layout)
        chart_layout.addWidget(line_chart_group)

        # 直方图
        hist_chart_group = QGroupBox("裂缝宽度分布")
        hist_chart_layout = QVBoxLayout()
        self.hist_chart_widget = pg.PlotWidget()
        self.hist_chart_widget.setBackground('#FFFFFF')
        self.hist_chart_widget.setTitle("裂缝宽度分布", color='#FF9800')
        self.hist_chart_widget.setLabel('left', '频数', color='#666')
        self.hist_chart_widget.setLabel('bottom', '宽度 (mm)', color='#666')
        self.hist_chart_widget.showGrid(x=True, y=True, alpha=0.3)
        self.hist_chart_widget.setMinimumHeight(300)
        hist_chart_layout.addWidget(self.hist_chart_widget)
        hist_chart_group.setLayout(hist_chart_layout)
        chart_layout.addWidget(hist_chart_group)

        main_layout.addLayout(chart_layout)

        # ========== 底部:统计数据汇总 ==========
        stats_group = QGroupBox("统计汇总")
        stats_layout = QHBoxLayout()

        self.total_records_label = QLabel("总记录数: 0")
        self.total_cracks_label = QLabel("总裂缝数: 0")
        self.avg_width_label = QLabel("平均宽度: 0.0mm")
        self.max_width_label = QLabel("最大宽度: 0.0mm")
        self.device_count_label = QLabel("涉及设备: 0台")

        # 设置标签样式
        label_style = "font-size: 14px; font-weight: bold;"
        self.total_records_label.setStyleSheet(label_style)
        self.total_cracks_label.setStyleSheet(label_style)
        self.avg_width_label.setStyleSheet(label_style)
        self.max_width_label.setStyleSheet(label_style)
        self.device_count_label.setStyleSheet(label_style)

        stats_layout.addWidget(self.total_records_label)
        stats_layout.addWidget(self.total_cracks_label)
        stats_layout.addWidget(self.avg_width_label)
        stats_layout.addWidget(self.max_width_label)
        stats_layout.addWidget(self.device_count_label)

        stats_group.setLayout(stats_layout)
        main_layout.addWidget(stats_group)

    def bind_signals(self):
        """绑定按钮信号"""
        self.generate_chart_btn.clicked.connect(self.generate_charts)
        self.export_chart_btn.clicked.connect(self.export_charts)
        self.period_combo.currentIndexChanged.connect(self.on_period_changed)

    def on_period_changed(self, index):
        """周期变化时重新生成图表"""
        self.generate_charts()

    # ================= 功能函数实现 =================

    def generate_charts(self):
        """生成统计图表"""
        if not self.db:
            return

        try:
            # 获取查询参数
            start_date, end_date = self.get_date_range()
            device_id = self.get_selected_device()

            # 获取每日统计数据
            daily_stats = self.db.get_daily_statistics(start_date, end_date)

            # 更新折线图
            if daily_stats:
                self.update_line_chart(daily_stats)
            else:
                self.clear_line_chart()

            # 获取所有裂缝宽度数据用于直方图
            records = self.db.query_by_date(start_date, end_date, device_id)

            if records:
                width_data = [r['max_width'] for r in records]
                self.update_histogram(width_data)
            else:
                self.clear_histogram()

            # 计算并显示统计汇总
            self.calculate_statistics(records, daily_stats)

        except Exception as e:
            import traceback
            print(f"生成图表失败: {e}\n{traceback.format_exc()}")

    def get_date_range(self):
        """
        根据选择的周期获取日期范围

        Returns:
            tuple: (start_date, end_date) 格式为 'YYYY-MM-DD'
        """
        from datetime import datetime, timedelta

        period_index = self.period_combo.currentIndex()
        end_date = datetime.now()

        if period_index == 0:  # 最近7天
            start_date = end_date - timedelta(days=6)
        elif period_index == 1:  # 最近30天
            start_date = end_date - timedelta(days=29)
        elif period_index == 2:  # 最近90天
            start_date = end_date - timedelta(days=89)
        else:  # 自定义，默认显示全部
            # 获取数据库中的日期范围
            date_range = self.db.get_date_range()
            if date_range['min_date']:
                start_date = datetime.strptime(date_range['min_date'], '%Y-%m-%d')
            else:
                start_date = end_date - timedelta(days=30)

        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    def get_selected_device(self):
        """
        获取选中的设备ID

        Returns:
            str or None: 设备ID，None表示全部设备
        """
        device_index = self.device_combo.currentIndex()
        if device_index > 0:  # 0是"全部设备"
            return self.device_combo.currentText()
        return None

    def update_line_chart(self, daily_stats):
        """
        更新折线图数据

        Args:
            daily_stats (list): 每日统计数据列表
                每个元素包含: date, total_cracks, max_width, record_count
        """
        if not daily_stats:
            self.clear_line_chart()
            return

        # 提取日期和裂缝数量
        dates = []
        crack_counts = []

        for stat in daily_stats:
            dates.append(stat['date'])
            crack_counts.append(stat['total_cracks'])

        # 清空图表
        self.line_chart_widget.clear()

        # 转换日期为x坐标（天数差）
        from datetime import datetime

        if len(dates) > 1:
            start_date = datetime.strptime(dates[0], '%Y-%m-%d')
            x_coords = [(datetime.strptime(d, '%Y-%m-%d') - start_date).days for d in dates]
        else:
            x_coords = list(range(len(dates)))

        # 创建折线图
        self.line_chart_widget.plot(x_coords, crack_counts,
                                   pen=pg.mkPen(color='#2196F3', width=2),
                                   symbol='o',
                                   symbolBrush='#2196F3',
                                   symbolSize=8,
                                   name='裂缝数量')

        # 设置x轴标签为实际日期
        axis = self.line_chart_widget.getAxis('bottom')
        ticks = []
        tick_labels = {}

        # 只显示部分日期标签以避免拥挤
        step = max(1, len(dates) // 10)
        for i in range(0, len(dates), step):
            date_str = dates[i]
            # 简化日期格式 (例如: 07-01)
            short_date = date_str[5:]  # 去掉年份
            ticks.append(x_coords[i])
            tick_labels[x_coords[i]] = short_date

        axis.setTicks([list(zip(ticks, [tick_labels[t] for t in ticks]))])

        # 添加图例
        self.line_chart_widget.addLegend()

    def clear_line_chart(self):
        """清空折线图"""
        self.line_chart_widget.clear()
        txt = pg.TextItem("暂无数据", color='#999', anchor=(0.5, 0.5))
        txt.setPos(0.5, 0.5)
        self.line_chart_widget.addItem(txt)

    def update_histogram(self, width_data):
        """
        更新直方图数据

        Args:
            width_data (list): 裂缝宽度列表
        """
        if not width_data:
            self.clear_histogram()
            return

        # 清空图表
        self.hist_chart_widget.clear()

        # 计算直方图数据
        try:
            import numpy as np
            hist, bin_edges = np.histogram(width_data, bins=20, range=(0, max(width_data)))
        except Exception:
            # 如果numpy不可用，使用手动计算
            hist, bin_edges = self.manual_histogram(width_data, bins=20)

        # 获取bin中心点作为x坐标
        bin_centers = []
        for i in range(len(bin_edges) - 1):
            bin_centers.append((bin_edges[i] + bin_edges[i + 1]) / 2)

        # 创建直方图
        bar_item = pg.BarGraphItem(x=bin_centers, height=hist, width=0.9 *
                                  (bin_edges[1] - bin_edges[0]), brush='#FF9800')
        self.hist_chart_widget.addItem(bar_item)

        # 添加图例
        self.hist_chart_widget.addLegend()

    def clear_histogram(self):
        """清空直方图"""
        self.hist_chart_widget.clear()
        txt = pg.TextItem("暂无数据", color='#999', anchor=(0.5, 0.5))
        txt.setPos(0.5, 0.5)
        self.hist_chart_widget.addItem(txt)

    def manual_histogram(self, data, bins=20):
        """
        手动计算直方图（不依赖numpy）

        Args:
            data (list): 数据列表
            bins (int): 分箱数量

        Returns:
            tuple: (hist_counts, bin_edges)
        """
        if not data:
            return [], []

        min_val = min(data)
        max_val = max(data)

        # 计算bin边界
        bin_width = (max_val - min_val) / bins if max_val > min_val else 1
        bin_edges = [min_val + i * bin_width for i in range(bins + 1)]

        # 计算每个bin的计数
        hist = [0] * bins

        for value in data:
            bin_index = int((value - min_val) / bin_width)
            if bin_index >= bins:
                bin_index = bins - 1
            hist[bin_index] += 1

        return hist, bin_edges

    def calculate_statistics(self, records, daily_stats):
        """
        计算统计数据并更新界面标签

        Args:
            records (list): 记录列表
            daily_stats (list): 每日统计数据列表
        """
        if not records:
            # 清空所有统计标签
            self.total_records_label.setText("总记录数: 0")
            self.total_cracks_label.setText("总裂缝数: 0")
            self.avg_width_label.setText("平均宽度: 0.0mm")
            self.max_width_label.setText("最大宽度: 0.0mm")
            self.device_count_label.setText("涉及设备: 0台")
            return

        # 总记录数
        total_records = len(records)

        # 总裂缝数
        total_cracks = sum(r['crack_count'] for r in records)

        # 平均宽度
        avg_width = sum(r['max_width'] for r in records) / total_records

        # 最大宽度
        max_width = max(r['max_width'] for r in records)

        # 涉及设备数
        devices = set(r['device_id'] for r in records)
        device_count = len(devices)

        # 更新标签
        self.total_records_label.setText(f"总记录数: {total_records}")
        self.total_cracks_label.setText(f"总裂缝数: {total_cracks}")
        self.avg_width_label.setText(f"平均宽度: {avg_width:.2f}mm")
        self.max_width_label.setText(f"最大宽度: {max_width:.2f}mm")
        self.device_count_label.setText(f"涉及设备: {device_count}台")

    def refresh_device_combo(self):
        """刷新设备下拉列表"""
        if not self.db:
            return

        # 保存当前选中的设备
        current_device = self.device_combo.currentText()

        # 清空并重新填充
        self.device_combo.clear()
        self.device_combo.addItem("全部设备")

        # 获取所有设备ID
        devices = self.db.get_all_devices()
        for device_id in devices:
            self.device_combo.addItem(device_id)

        # 恢复之前选中的设备（如果还存在）
        index = self.device_combo.findText(current_device)
        if index >= 0:
            self.device_combo.setCurrentIndex(index)

    def export_charts(self):
        """导出图表"""
        if not self.db:
            QMessageBox.warning(self, "导出失败", "数据库未连接")
            return

        try:
            # 获取保存路径
            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出图表", os.path.join(REPORTS_DIR, "charts.png"),
                "图片文件 (*.png *.jpg *.pdf)"
            )

            if not file_path:
                return

            # 导出图表
            exporter = pg.exporters.ImageExporter(self.line_chart_widget.plotItem)
            exporter.export(file_path)

            QMessageBox.information(self, "导出成功",
                                  f"图表已导出到:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出图表失败:\n{str(e)}")


# ============================================================
# 第六部分:Tab4 - AI智能分析面板
# ============================================================

class AIAnalysisTab(QWidget):
    """
    Tab4:AI智能分析面板
    功能:自动日报生成、手动交互问答、分析结果存储与回溯
    """

    def __init__(self, db=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.selected_records = []  # 当前选中的记录
        self.current_api_result = None  # 当前API结果
        self.api_key = ""  # API密钥，通过 load_api_key 从配置页加载
        self.api_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        self.init_ui()
        # 绑定按钮信号
        self.bind_signals()
        # 加载API密钥（从配置页）
        self.load_api_key()
        # 刷新历史记录
        self.refresh_analysis_history()

    def init_ui(self):
        """初始化UI布局"""
        # 主布局 - 水平分割
        main_layout = QHBoxLayout(self)

        # ========== 左侧:操作面板 ==========
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # 自动日报区域
        daily_report_group = QGroupBox("自动日报")
        daily_report_layout = QVBoxLayout()

        self.auto_report_label = QLabel("生成每日裂缝检测工程分析报告")
        daily_report_layout.addWidget(self.auto_report_label)

        self.generate_report_btn = QPushButton("生成今日日报")
        daily_report_layout.addWidget(self.generate_report_btn)

        self.last_report_label = QLabel("上次生成: 未生成")
        self.last_report_label.setStyleSheet("color: #666; font-size: 10px;")
        daily_report_layout.addWidget(self.last_report_label)

        daily_report_group.setLayout(daily_report_layout)
        left_layout.addWidget(daily_report_group)

        # 手动交互问答区域
        qa_group = QGroupBox("手动交互问答")
        qa_layout = QVBoxLayout()

        qa_layout.addWidget(QLabel("选择要分析的裂缝记录:"))
        self.selected_records_text = QTextEdit()
        self.selected_records_text.setMaximumHeight(80)
        self.selected_records_text.setPlaceholderText("从历史记录Tab选中记录后自动填充...")
        qa_layout.addWidget(self.selected_records_text)

        qa_layout.addWidget(QLabel("自定义提问:"))
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("请输入问题，如:分析这些裂缝的严重程度...")
        qa_layout.addWidget(self.question_input)

        self.send_question_btn = QPushButton("发送问题")
        qa_layout.addWidget(self.send_question_btn)

        qa_group.setLayout(qa_layout)
        left_layout.addWidget(qa_group)

        # 历史分析记录区域
        history_group = QGroupBox("历史分析记录")
        history_layout = QVBoxLayout()

        self.analysis_history_list = QTextEdit()
        self.analysis_history_list.setReadOnly(True)
        self.analysis_history_list.setMaximumHeight(200)
        history_layout.addWidget(self.analysis_history_list)

        self.refresh_history_btn = QPushButton("刷新历史记录")
        history_layout.addWidget(self.refresh_history_btn)

        history_group.setLayout(history_layout)
        left_layout.addWidget(history_group)

        main_layout.addWidget(left_widget)

        # ========== 右侧:分析结果展示区 ==========
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        result_group = QGroupBox("AI分析结果")
        result_layout = QVBoxLayout()

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("AI分析结果将在此显示...")
        result_layout.addWidget(self.result_text)

        # 操作按钮
        result_button_layout = QHBoxLayout()
        self.copy_result_btn = QPushButton("复制结果")
        self.save_result_btn = QPushButton("保存到数据库")
        self.export_pdf_btn = QPushButton("导出PDF报告")
        result_button_layout.addWidget(self.copy_result_btn)
        result_button_layout.addWidget(self.save_result_btn)
        result_button_layout.addWidget(self.export_pdf_btn)
        result_layout.addLayout(result_button_layout)

        result_group.setLayout(result_layout)
        right_layout.addWidget(result_group)

        main_layout.addWidget(right_widget)

        # 设置分割器比例
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 2)

    def bind_signals(self):
        """绑定按钮信号"""
        self.generate_report_btn.clicked.connect(self.generate_daily_report)
        self.send_question_btn.clicked.connect(self.send_question)
        self.copy_result_btn.clicked.connect(self.copy_result)
        self.save_result_btn.clicked.connect(self.save_result_to_db)
        self.export_pdf_btn.clicked.connect(self.export_pdf)
        self.refresh_history_btn.clicked.connect(self.refresh_analysis_history)

    def load_api_key(self):
        """加载API密钥"""
        # 1. 尝试从配置页UI读取
        main_win = self.window()
        if main_win and hasattr(main_win, 'config_tab'):
            key = main_win.config_tab.api_key_input.text().strip()
            if key:
                self.api_key = key
                return
        # 2. UI读取失败，直接从config.json文件读取
        try:
            config_path = os.path.join(BASE_DIR, "config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    key = config.get('api_key', '').strip()
                    if key:
                        self.api_key = key
        except Exception:
            pass

    def get_api_key(self):
        """获取API密钥，优先从配置页面实时读取，其次从config.json文件读取"""
        # 1. 从配置页面UI实时读取
        main_win = self.window()
        if main_win and hasattr(main_win, 'config_tab'):
            key = main_win.config_tab.api_key_input.text().strip()
            if key:
                self.api_key = key
                return key
        # 2. 回退到已缓存的密钥
        if self.api_key:
            return self.api_key
        # 3. 最后尝试从config.json文件直接读取
        try:
            config_path = os.path.join(BASE_DIR, "config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    key = config.get('api_key', '').strip()
                    if key:
                        self.api_key = key
                        return key
        except Exception:
            pass
        return None

    # ================= 功能函数实现 =================

    def generate_daily_report(self):
        """生成今日日报"""
        if not self.db:
            QMessageBox.warning(self, "错误", "数据库未连接")
            return

        try:
            # 获取今日数据
            from datetime import datetime
            today = datetime.now().strftime('%Y-%m-%d')

            # 获取今日统计数据
            print(f"[AI日报] 查询今日数据: {today}")
            stats = self.db.get_today_statistics()
            print(f"[AI日报] 统计结果: total_cracks={stats.get('total_cracks', 0)}, record_count={stats.get('record_count', 0)}")
            daily_records = self.db.query_by_date(today, device_id=None)
            print(f"[AI日报] 今日记录数: {len(daily_records)}")

            if not daily_records:
                # 调试：检查数据库是否有数据
                all_records = self.db.query_records(conditions={}, page=1, page_size=10)
                total_records = all_records['total']
                msg = f"今日({today})暂无裂缝检测记录\n\n"
                if total_records > 0:
                    msg += f"数据库共有 {total_records} 条记录\n"
                    if all_records['records']:
                        rec = all_records['records'][0]
                        msg += f"第一条记录日期: {datetime.fromtimestamp(rec['timestamp']).strftime('%Y-%m-%d')}\n"
                        msg += f"entry_date: {rec.get('entry_date', 'N/A')}"
                else:
                    msg += "数据库为空\n请检查：\n1. RK3588仿真客户端是否正常发送数据\n2. TCP服务是否启动（8888端口）"
                QMessageBox.information(self, "提示", msg)
                return

            # 准备上下文数据
            context_data = {
                'date': today,
                'total_cracks': stats['total_cracks'],
                'max_width': stats['max_width'],
                'avg_confidence': stats['avg_confidence'],
                'record_count': stats['record_count'],
                'devices': list(set(r['device_id'] for r in daily_records)),
                'records': daily_records[:10]  # 限制最多10条记录
            }

            # 构建提示词
            prompt = f"""请基于以下今日墙体裂缝检测数据，生成一份工程分析日报:

【检测日期】{today}

【统计数据】
- 总裂缝数:{stats['total_cracks']} 条
- 最大裂缝宽度:{stats['max_width']:.2f} mm
- 平均识别置信度:{stats['avg_confidence']:.1f}%
- 检测记录数:{stats['record_count']} 条
- 涉及设备:{len(context_data['devices'])} 台 ({', '.join(context_data['devices'])})

【详细记录】（前10条）
"""
            for i, record in enumerate(daily_records[:10], 1):
                prompt += f"""
{i}. 设备:{record['device_id']}
   裂缝数:{record['crack_count']} 条
   最大宽度:{record['max_width']:.2f} mm
   最大长度:{record['max_length']:.2f} mm
   平均宽度:{record['avg_width']:.2f} mm
   置信度:{record['confidence']:.1f}%
"""

            prompt += """
【分析要求】
1. 评估整体裂缝严重程度（低/中/高/严重）
2. 识别主要风险点和关注区域
3. 提供具体的处置建议
4. 给出后续巡检计划建议
5. 用简明扼要的语言，突出重点

请以专业工程报告的格式生成分析结果。"""

            # 显示加载状态
            self.result_text.setText("正在生成日报，请稍候...")
            QApplication.processEvents()  # 立即刷新UI

            # 调用API
            print(f"[AI日报] 准备调用API，记录数={len(daily_records)}, 总裂缝数={stats['total_cracks']}")
            result = self.call_doubao_api(prompt, context_data)
            print(f"[AI日报] API返回: {bool(result)}")

            if result:
                # 显示结果
                self.display_result(result)
                self.current_api_result = result

                # 更新上次生成时间
                self.last_report_label.setText(
                    f"上次生成: {datetime.now().strftime('%H:%M:%S')}"
                )

                # 写入日志
                if self.parent() and hasattr(self.parent(), 'realtime_tab'):
                    self.parent().realtime_tab.log_message(
                        f"已生成今日日报，共 {stats['total_cracks']} 条裂缝", "SUCCESS"
                    )

            else:
                # 不覆盖call_doubao_api已设置的具体错误信息
                current_text = self.result_text.toPlainText()
                if not current_text or "正在生成日报" in current_text:
                    self.result_text.setText("日报生成失败，请检查API密钥和网络连接")

        except Exception as e:
            self.result_text.setText(f"生成日报时出错: {str(e)}")
            QMessageBox.critical(self, "错误", f"生成日报失败:\n{str(e)}")

    def send_question(self):
        """发送问题到AI"""
        question = self.question_input.text().strip()

        if not question:
            QMessageBox.warning(self, "提示", "请输入问题")
            return

        if not self.selected_records:
            # 如果没有选中记录，提示用户
            reply = QMessageBox.question(
                self, "确认", "未选择任何裂缝记录，是否继续？（将基于今日数据回答）",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        try:
            # 准备上下文数据
            context_data = self.prepare_context_data(self.selected_records, question)

            # 构建提示词
            prompt = question

            # 添加上下文信息
            if self.selected_records:
                prompt += "\n\n【参考数据】\n"
                for i, record in enumerate(self.selected_records, 1):
                    prompt += f"""
{i}. 设备:{record['device_id']}
   裂缝数:{record['crack_count']} 条
   最大宽度:{record['max_width']:.2f} mm
   最大长度:{record['max_length']:.2f} mm
   平均宽度:{record['avg_width']:.2f} mm
   置信度:{record['confidence']:.1f}%
   图片路径:{record.get('image_path', '无')}
"""
            else:
                # 使用今日数据
                from datetime import datetime
                today = datetime.now().strftime('%Y-%m-%d')
                stats = self.db.get_today_statistics()
                prompt += f"""
【今日数据参考】
日期:{today}
总裂缝数:{stats['total_cracks']} 条
最大裂缝宽度:{stats['max_width']:.2f} mm
平均识别置信度:{stats['avg_confidence']:.1f}%
检测记录数:{stats['record_count']} 条
"""

            # 显示加载状态
            self.result_text.setText("正在分析，请稍候...")

            # 调用API
            result = self.call_doubao_api(prompt, context_data)

            if result:
                # 显示结果
                self.display_result(result)
                self.current_api_result = result
            else:
                self.result_text.setText("分析失败，请检查API密钥和网络连接")

        except Exception as e:
            self.result_text.setText(f"分析时出错: {str(e)}")
            QMessageBox.critical(self, "错误", f"分析失败:\n{str(e)}")

    def call_doubao_api(self, prompt, context_data):
        """
        调用豆包API

        Args:
            prompt (str): 提示词
            context_data (dict): 上下文数据

        Returns:
            str: AI分析结果，失败返回None
        """
        api_key = self.get_api_key()

        if not api_key:
            # 详细提示，帮助排查密钥读取问题
            main_win = self.window()
            has_main_win = main_win is not None
            has_config = has_main_win and hasattr(main_win, 'config_tab')
            config_key = ""
            if has_config:
                config_key = main_win.config_tab.api_key_input.text().strip()
            detail = (f"调试信息:\n"
                     f"- MainWindow存在: {has_main_win}\n"
                     f"- config_tab存在: {has_config}\n"
                     f"- API Key: {'已填写' if config_key else '为空'}\n\n"
                     f"请在系统配置页面填入API Key（ark-开头）")
            QMessageBox.warning(
                self, "API密钥未配置",
                detail
            )
            return None

        try:
            # 获取模型端点ID（从配置页实时读取，回退到默认值）
            model_id = 'ep-20260707231008-5l2xg'
            main_win = self.window()
            if main_win and hasattr(main_win, 'config_tab'):
                cfg_model = main_win.config_tab.model_id_input.text().strip()
                if cfg_model:
                    model_id = cfg_model

            print(f"[API调用] 模型ID={model_id}, prompt长度={len(prompt)}")
            print(f"[API调用] 密钥前20位={api_key[:20]}, 密钥长度={len(api_key)}, 是否ark开头={api_key.startswith('ark-')}")

            # 构建请求头
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }

            # 构建请求体
            payload = {
                'model': model_id,
                'messages': [
                    {
                        'role': 'system',
                        'content': '你是一位专业的建筑结构工程师，擅长分析墙体裂缝检测数据，提供专业的风险评估和处置建议。'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.7,
                'max_tokens': 2000
            }

            # 发送请求（使用urllib替代requests，避免app环境下的超时问题）
            print(f"[API调用] 发送请求到: {self.api_url}")
            import urllib.request
            import urllib.error
            req_data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(self.api_url, data=req_data, headers=headers, method='POST')
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    resp_data = resp.read().decode('utf-8')
                    print(f"[API调用] 响应状态码: {resp.status}")
                    # 构造类response对象给parse_api_response
                    class _FakeResponse:
                        def __init__(self, status_code, text):
                            self.status_code = status_code
                            self.text = text
                        def json(self):
                            return json.loads(self.text)
                    fake_resp = _FakeResponse(resp.status, resp_data)
                    result = self.parse_api_response(fake_resp)
                    return result
            except urllib.error.HTTPError as e:
                error_body = e.read().decode('utf-8') if e.fp else ''
                print(f"[API调用] HTTP错误: {e.code}, {error_body[:500]}")
                self.result_text.setPlainText(f"API请求失败 (状态码: {e.code})\n{error_body[:500]}")
                return None
            except urllib.error.URLError as e:
                print(f"[API调用] URL错误: {e.reason}")
                self.result_text.setPlainText(f"网络连接失败: {str(e.reason)}")
                return None

        except requests.exceptions.Timeout:
            print(f"[API调用] 请求超时!")
            self.result_text.setPlainText("API请求超时，请检查网络连接")
            return None
        except (urllib.error.URLError, requests.exceptions.ConnectionError) as e:
            print(f"[API调用] 连接错误: {e}")
            self.result_text.setPlainText(f"网络连接失败: {str(e)[:200]}")
            return None
        except Exception as e:
            print(f"[API调用] 异常: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            self.result_text.setPlainText(f"调用豆包API出错: {str(e)}")
            return None

    def parse_api_response(self, response):
        """
        解析API响应

        Args:
            response: API响应对象

        Returns:
            str: 解析后的文本内容
        """
        try:
            result = response.json()

            # 根据豆包API的实际响应格式解析
            # 这里假设返回格式为 {"choices": [{"message": {"content": "..."}}]}
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                return content
            elif 'data' in result:
                # 其他可能的响应格式
                return str(result['data'])
            else:
                return str(result)

        except Exception as e:
            print(f"解析API响应失败: {e}")
            return None

    def display_result(self, result):
        """
        显示分析结果

        Args:
            result (str): 分析结果文本
        """
        self.result_text.clear()
        self.result_text.setPlainText(result)

        # 添加时间戳
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.result_text.append(f"\n\n--- 生成时间: {timestamp} ---")

    def copy_result(self):
        """复制分析结果"""
        text = self.result_text.toPlainText()

        if not text:
            QMessageBox.information(self, "提示", "没有可复制的内容")
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        QMessageBox.information(self, "成功", "结果已复制到剪贴板")

    def save_result_to_db(self):
        """保存分析结果到数据库"""
        if not self.db:
            QMessageBox.warning(self, "错误", "数据库未连接")
            return

        result_text = self.result_text.toPlainText()

        if not result_text or not self.current_api_result:
            QMessageBox.warning(self, "提示", "没有可保存的分析结果")
            return

        try:
            # 如果有选中的记录，更新第一条记录的AI分析字段
            if self.selected_records:
                record_id = self.selected_records[0]['id']
                success = self.db.update_ai_analysis(record_id, self.current_api_result)

                if success:
                    QMessageBox.information(self, "成功", "分析结果已保存到数据库")
                    self.refresh_analysis_history()
                else:
                    QMessageBox.warning(self, "失败", "保存分析结果失败")
            else:
                # 保存到日志文件
                from datetime import datetime
                log_file = os.path.join(LOGS_DIR, "ai_analysis.log")
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n\n{'='*60}\n")
                    f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"类型: 手动问答\n")
                    f.write(f"{'='*60}\n")
                    f.write(self.current_api_result)

                QMessageBox.information(self, "成功",
                                      "分析结果已保存到日志文件（未关联具体记录）")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存分析结果失败:\n{str(e)}")

    def export_pdf(self):
        """导出PDF报告"""
        result_text = self.result_text.toPlainText()

        if not result_text:
            QMessageBox.information(self, "提示", "没有可导出的内容")
            return

        try:
            # 获取保存路径
            from datetime import datetime
            default_name = f"AI分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出报告", os.path.join(REPORTS_DIR, default_name),
                "文本文件 (*.txt);;所有文件 (*.*)"
            )

            if not file_path:
                return

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("墙体裂缝检测 - AI分析报告\n")
                f.write("="*60 + "\n\n")
                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("-"*60 + "\n")
                f.write(result_text)
                f.write("\n" + "-"*60 + "\n")
                f.write(f"\n此报告由 {APP_NAME} {APP_VERSION} 自动生成\n")

            QMessageBox.information(self, "成功", f"报告已导出到:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出报告失败:\n{str(e)}")

    def refresh_analysis_history(self):
        """刷新历史分析记录"""
        if not self.db:
            return

        try:
            # 查询有AI分析的记录
            conditions = {'has_analysis': True}
            result = self.db.query_records(conditions=conditions, page=1, page_size=20,
                                          order_by='id', order='DESC')

            self.analysis_history_list.clear()

            if not result['records']:
                self.analysis_history_list.setPlainText("暂无历史分析记录")
                return

            # 显示历史记录
            from datetime import datetime
            history_text = "历史分析记录 (最新20条):\n\n"

            for i, record in enumerate(result['records'], 1):
                timestamp_str = datetime.fromtimestamp(record['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                analysis_preview = record['ai_analysis'][:100] + '...' if len(
                    record['ai_analysis']) > 100 else record['ai_analysis']

                history_text += f"{i}. [{timestamp_str}] 设备:{record['device_id']} "
                history_text += f"裂缝:{record['crack_count']}条 最大宽:{record['max_width']:.2f}mm\n"
                history_text += f"   分析: {analysis_preview}\n\n"

            self.analysis_history_list.setPlainText(history_text)

        except Exception as e:
            self.analysis_history_list.setPlainText(f"刷新历史记录失败: {str(e)}")

    def load_analysis_result(self, record_id):
        """
        加载历史分析结果

        Args:
            record_id (int): 记录ID
        """
        if not self.db:
            return

        try:
            record = self.db.get_record_by_id(record_id)

            if record and record['ai_analysis']:
                self.display_result(record['ai_analysis'])
                self.current_api_result = record['ai_analysis']
                self.result_text.append(f"\n\n--- 加载的历史记录 ID: {record_id} ---")
            else:
                QMessageBox.information(self, "提示", "该记录没有AI分析结果")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载分析结果失败:\n{str(e)}")

    def update_selected_records(self, records):
        """
        更新选中记录显示

        Args:
            records (list): 选中记录列表
        """
        self.selected_records = records

        if not records:
            self.selected_records_text.clear()
            return

        # 显示选中记录摘要
        summary = f"已选中 {len(records)} 条记录:\n"
        from datetime import datetime

        for i, record in enumerate(records[:5], 1):  # 最多显示5条
            timestamp_str = datetime.fromtimestamp(record['timestamp']).strftime('%Y-%m-%d %H:%M')
            summary += f"{i}. [{timestamp_str}] 设备:{record['device_id']} "
            summary += f"裂缝:{record['crack_count']}条 最大宽:{record['max_width']:.2f}mm\n"

        if len(records) > 5:
            summary += f"... 还有 {len(records) - 5} 条记录"

        self.selected_records_text.setPlainText(summary)

    def prepare_context_data(self, records, question):
        """
        准备上下文数据发送给AI

        Args:
            records (list): 选中记录列表
            question (str): 用户问题

        Returns:
            dict: 上下文数据
        """
        context_data = {
            'question': question,
            'record_count': len(records),
            'records': records[:10] if records else []  # 限制记录数
        }

        # 添加统计信息
        if records:
            context_data['total_cracks'] = sum(r['crack_count'] for r in records)
            context_data['max_width'] = max(r['max_width'] for r in records)
            context_data['avg_width'] = sum(r['avg_width'] for r in records) / len(records)
            context_data['avg_confidence'] = sum(r['confidence'] for r in records) / len(records)

        return context_data


# ============================================================
# 第七部分:Tab5 - 系统配置与导出页面
# ============================================================

class SystemConfigTab(QWidget):
    """
    Tab5:系统配置与导出页面
    功能:API密钥配置、TCP端口配置、数据导出
    """

    def __init__(self, db=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()
        # 绑定按钮信号
        self.bind_signals()
        # 加载已保存的配置
        self.load_config()

    def bind_signals(self):
        """绑定按钮信号"""
        self.test_api_btn.clicked.connect(self.test_api_connection)
        self.save_config_btn.clicked.connect(self.save_config)
        self.start_tcp_btn.clicked.connect(self.start_tcp_server)
        self.stop_tcp_btn.clicked.connect(self.stop_tcp_server)
        self.backup_db_btn.clicked.connect(self.backup_database)
        self.restore_db_btn.clicked.connect(self.restore_database)
        self.clean_now_btn.clicked.connect(self.clean_old_images)
        self.export_all_excel_btn.clicked.connect(self.export_all_to_excel)
        self.export_all_pdf_btn.clicked.connect(self.export_all_to_pdf)


    def init_ui(self):
        """初始化UI布局"""
        # 主布局 - 垂直
        main_layout = QVBoxLayout(self)

        # ========== 系统配置区 ==========
        config_group = QGroupBox("系统配置")
        config_layout = QVBoxLayout()

        # AI配置 - API Key
        api_config_layout = QHBoxLayout()
        api_config_layout.addWidget(QLabel("API Key:"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("如: ark-834668da-813c-4ad9-9a15-cbc4ec6fc8a0-987b4")
        self.api_key_input.setEchoMode(QLineEdit.Password)
        api_config_layout.addWidget(self.api_key_input)
        self.test_api_btn = QPushButton("测试连接")
        api_config_layout.addWidget(self.test_api_btn)
        self.save_config_btn = QPushButton("保存配置")
        api_config_layout.addWidget(self.save_config_btn)
        config_layout.addLayout(api_config_layout)

        # 模型端点ID配置
        model_config_layout = QHBoxLayout()
        model_config_layout.addWidget(QLabel("模型端点ID:"))
        self.model_id_input = QLineEdit()
        self.model_id_input.setPlaceholderText("如: ep-20260707231008-xxxxx")
        self.model_id_input.setText("ep-20260707231008-5l2xg")
        model_config_layout.addWidget(self.model_id_input)
        config_layout.addLayout(model_config_layout)

        # TCP配置
        tcp_config_layout = QHBoxLayout()
        tcp_config_layout.addWidget(QLabel("TCP监听端口:"))
        self.tcp_port_spin = QSpinBox()
        self.tcp_port_spin.setRange(1024, 65535)
        self.tcp_port_spin.setValue(DEFAULT_TCP_PORT)
        tcp_config_layout.addWidget(self.tcp_port_spin)

        self.tcp_status_label = QLabel("TCP状态: 未启动")
        self.tcp_status_label.setStyleSheet("color: #999;")
        tcp_config_layout.addWidget(self.tcp_status_label)

        self.start_tcp_btn = QPushButton("启动TCP服务")
        tcp_config_layout.addWidget(self.start_tcp_btn)

        self.stop_tcp_btn = QPushButton("停止TCP服务")
        self.stop_tcp_btn.setEnabled(False)
        tcp_config_layout.addWidget(self.stop_tcp_btn)

        config_layout.addLayout(tcp_config_layout)

        # 告警阈值配置
        alarm_config_layout = QHBoxLayout()

        alarm_config_layout.addWidget(QLabel("裂缝宽度告警阈值(mm):"))
        self.width_threshold_spin = QDoubleSpinBox()
        self.width_threshold_spin.setRange(0, 100)
        self.width_threshold_spin.setValue(CRACK_WIDTH_ALARM_THRESHOLD)
        alarm_config_layout.addWidget(self.width_threshold_spin)

        alarm_config_layout.addWidget(QLabel("单日裂缝数告警阈值:"))
        self.count_threshold_spin = QSpinBox()
        self.count_threshold_spin.setRange(0, 1000)
        self.count_threshold_spin.setValue(DAILY_CRACK_COUNT_ALARM_THRESHOLD)
        alarm_config_layout.addWidget(self.count_threshold_spin)

        alarm_config_layout.addWidget(QCheckBox("启用声音告警"))
        alarm_config_layout.addWidget(QCheckBox("启用弹窗告警"))

        config_layout.addLayout(alarm_config_layout)

        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)

        # ========== 数据管理区 ==========
        data_group = QGroupBox("数据管理")
        data_layout = QVBoxLayout()

        # 数据库操作
        db_layout = QHBoxLayout()
        self.db_info_label = QLabel(f"数据库: {DB_PATH}")
        db_layout.addWidget(self.db_info_label)
        self.backup_db_btn = QPushButton("备份数据库")
        db_layout.addWidget(self.backup_db_btn)
        self.restore_db_btn = QPushButton("恢复数据库")
        db_layout.addWidget(self.restore_db_btn)
        data_layout.addLayout(db_layout)

        # 图片清理
        image_layout = QHBoxLayout()
        image_layout.addWidget(QLabel("自动清理"))
        self.auto_clean_check = QCheckBox("启用自动清理30天前图片")
        image_layout.addWidget(self.auto_clean_check)
        self.clean_now_btn = QPushButton("立即清理")
        image_layout.addWidget(self.clean_now_btn)
        data_layout.addLayout(image_layout)

        # 数据导出
        export_layout = QHBoxLayout()
        self.export_all_excel_btn = QPushButton("导出全部数据(Excel)")
        self.export_all_pdf_btn = QPushButton("导出全部AI报告(PDF)")
        export_layout.addWidget(self.export_all_excel_btn)
        export_layout.addWidget(self.export_all_pdf_btn)
        data_layout.addLayout(export_layout)

        data_group.setLayout(data_layout)
        main_layout.addWidget(data_group)

        # ========== 系统信息区 ==========
        info_group = QGroupBox("系统信息")
        info_layout = QVBoxLayout()

        info_text = f"""
        应用名称: {APP_NAME}
        应用版本: {APP_VERSION}
        工作目录: {BASE_DIR}
        数据目录: {DATA_DIR}
        图片目录: {IMAGES_DIR}
        日志目录: {LOGS_DIR}
        """
        self.system_info_label = QLabel(info_text.strip())
        self.system_info_label.setStyleSheet("font-family: monospace;")
        info_layout.addWidget(self.system_info_label)

        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)

    # ================= 功能函数实现 =================

    def save_config(self):
        """保存配置到 config.json"""
        try:
            config = {
                'api_key': self.api_key_input.text(),
                'model_id': self.model_id_input.text().strip(),
                'tcp_port': self.tcp_port_spin.value(),
                'width_threshold': self.width_threshold_spin.value(),
                'count_threshold': self.count_threshold_spin.value(),
                'enable_audio_alarm': self.auto_clean_check.isChecked(),
                'enable_popup_alarm': False  # 暂未实现弹窗告警
            }

            config_path = os.path.join(BASE_DIR, "config.json")
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            # 通知 AI Tab 刷新缓存的 API 密钥
            main_win = self.window()
            if main_win and hasattr(main_win, 'ai_tab'):
                main_win.ai_tab.api_key = self.api_key_input.text().strip()

            QMessageBox.information(self, "配置保存成功", f"配置已保存到:\n{config_path}")

        except Exception as e:
            QMessageBox.critical(self, "保存失败", f"配置保存失败:\n{e}")

    def load_config(self):
        """加载配置从 config.json"""
        try:
            config_path = os.path.join(BASE_DIR, "config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    api_key = config.get('api_key', '')
                    self.api_key_input.setText(api_key)
                    self.model_id_input.setText(config.get('model_id', 'ep-20260707231008-5l2xg'))
                    self.tcp_port_spin.setValue(config.get('tcp_port', DEFAULT_TCP_PORT))
                    self.width_threshold_spin.setValue(config.get('width_threshold', CRACK_WIDTH_ALARM_THRESHOLD))
                    self.count_threshold_spin.setValue(config.get('count_threshold', DAILY_CRACK_COUNT_ALARM_THRESHOLD))
                    # 加载成功后同步到 AI Tab 缓存
                    main_win = self.window()
                    if main_win and hasattr(main_win, 'ai_tab') and api_key.strip():
                        main_win.ai_tab.api_key = api_key.strip()
            else:
                print(f"[配置] 配置文件不存在: {config_path}")
        except Exception as e:
            print(f"[配置] 加载配置失败: {e}")

    def test_api_connection(self):
        """测试API密钥"""
        api_key = self.api_key_input.text().strip()
        model_id = self.model_id_input.text().strip() or 'ep-20260707231008-5l2xg'

        if not api_key:
            QMessageBox.warning(self, "提示", "请先输入API Key")
            return False

        try:
            import requests
            api_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            payload = {
                'model': model_id,
                'messages': [{'role': 'user', 'content': '测试'}],
                'max_tokens': 100
            }
            response = requests.post(api_url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                # 测试成功，自动保存配置
                self.save_config()
                QMessageBox.information(self, "测试成功", "API密钥配置正确，连接成功\n配置已自动保存")
                return True
            else:
                QMessageBox.warning(self, "测试失败", f"API返回错误: {response.status_code}\n{response.text[:500]}")
                return False

        except Exception as e:
            QMessageBox.critical(self, "测试失败", f"测试失败:\n{e}")
            return False

    def start_tcp_server(self):
        """启动TCP服务"""
        try:
            self.tcp_status_label.setText("TCP状态: 正在启动...")
            self.tcp_status_label.setStyleSheet("color: #FFA500")
            self.tcp_status_label.setStyleSheet("color: #FFA500")
            self.tcp_status_label.repaint()
            QCoreApplication.processEvents()
            self.parent().tcp_server.start()
            self.tcp_status_label.setText("TCP状态: 运行中")
            self.tcp_status_label.setStyleSheet("color: #4CAF50")
            self.tcp_status_label.setStyleSheet("color: #4CAF50")
            self.tcp_status_label.repaint()
            self.start_tcp_btn.setEnabled(False)
            self.stop_tcp_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "启动失败", f"启动TCP服务失败:\n{e}")
            self.tcp_status_label.setText("TCP状态: 启动失败")
            self.tcp_status_label.setStyleSheet("color: #F44336")

    def stop_tcp_server(self):
        """停止TCP服务"""
        try:
            self.tcp_status_label.setText("TCP状态: 正在停止...")
            self.tcp_status_label.setStyleSheet("color: #FFA500")
            self.tcp_status_label.setStyleSheet("color: #FFA500")
            self.tcp_status_label.repaint()
            QCoreApplication.processEvents()
            self.parent().tcp_server.stop()
            self.tcp_status_label.setText("TCP状态: 已停止")
            self.tcp_status_label.setStyleSheet("color: #999")
            self.tcp_status_label.setStyleSheet("color: #999")
            self.tcp_status_label.repaint()
            self.stop_tcp_btn.setEnabled(True)
            self.start_tcp_btn.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "停止失败", f"停止TCP服务失败:\n{e}")
            self.tcp_status_label.setText("TCP状态: 停止失败")
            self.tcp_status_label.setStyleSheet("color: #F44336")

    def update_tcp_status(self, status):
        """更新TCP状态显示"""
        self.tcp_status_label.setText(f"TCP状态: {status}")
        if "运行中" in status:
            self.tcp_status_label.setStyleSheet("color: #4CAF50")
        elif "失败" in status or "错误" in status:
            self.tcp_status_label.setStyleSheet("color: #F44336")
        else:
            self.tcp_status_label.setStyleSheet("color: #999")

    def backup_database(self):
        """备份数据库"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"crack_detection_backup_{timestamp}.db"
            backup_path = os.path.join(REPORTS_DIR, backup_name)
            shutil.copy2(DB_PATH, backup_path)
            QMessageBox.information(self, "备份成功", f"数据库已备份到:\n{backup_path}")
        except Exception as e:
            QMessageBox.critical(self, "备份失败", f"备份数据库失败:\n{e}")

    def restore_database(self):
        """恢复数据库"""
        backup_path, _ = QFileDialog.getOpenFileName(
            self, "选择备份文件", REPORTS_DIR, "数据库文件 (*.db)"
        )
        if not backup_path:
            return

        try:
            # 备份当前数据库
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"crack_detection_backup_{timestamp}.db"
            backup_path_current = os.path.join(REPORTS_DIR, backup_name)
            shutil.copy2(DB_PATH, backup_path_current)

            # 关闭数据库连接
            self.parent().db.close()

            # 恢复选择的备份
            shutil.copy2(backup_path, DB_PATH)

            # 重新连接
            self.parent().db.connect()
            self.parent().db.init_database()

            QMessageBox.information(self, "恢复成功", f"数据库已恢复，原数据库已备份到:\n{backup_path_current}")
        except Exception as e:
            QMessageBox.critical(self, "恢复失败", f"恢复数据库失败:\n{e}")

    def clean_old_images(self):
        """清理过期图片"""
        try:
            threshold_days = 30
            cutoff_time = datetime.now() - timedelta(days=threshold_days)
            cleaned = 0

            # 扫遍所有日期目录
            if os.path.exists(IMAGES_DIR):
                for date_dir in os.listdir(IMAGES_DIR):
                    date_path = os.path.join(IMAGES_DIR, date_dir)
                    if not os.path.isdir(date_path):
                        continue

                    for device_dir in os.listdir(date_path):
                        device_path = os.path.join(date_path, device_dir)
                        if not os.path.isdir(device_path):
                            continue

                        for filename in os.listdir(device_path):
                            file_path = os.path.join(device_path, filename)
                            if os.path.isfile(file_path):
                                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                                if file_time < cutoff_time:
                                    os.remove(file_path)
                                    cleaned += 1

            QMessageBox.information(self, "清理完成", f"清理完成，删除 {cleaned} 张30天前的图片")

        except Exception as e:
            QMessageBox.critical(self, "清理失败", f"清理过期图片失败:\n{e}")

    def export_all_to_excel(self):
        """导出全部数据到Excel"""
        try:
            all_records = []
            if self.db:
                # 分页查询全部数据
                page = 1
                page_size = 1000
                while True:
                    result = self.db.query_records(
                        conditions={}, page=page, page_size=page_size,
                        order_by='id', order='ASC'
                    )
                    all_records.extend(result['records'])
                    if len(result['records']) < page_size:
                        break
                    page += 1

            if not all_records:
                QMessageBox.information(self, "提示", "数据库中没有可导出的记录")
                return

            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出Excel报表", os.path.join(REPORTS_DIR, "crack_records.xlsx"),
                "Excel文件 (*.xlsx *.xls)"
            )
            if not file_path:
                return

            import csv
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                # 写入表头
                writer.writerow(['记录ID', '设备ID', '时间', '裂缝条数',
                               '最大宽度', '最大长度', '平均宽度', '置信度', '图片路径', 'AI分析'])
                # 写入数据
                for record in all_records:
                    writer.writerow([
                        record['id'], record['device_id'], datetime.fromtimestamp(record['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                        record['crack_count'], f"{record['max_width']:.2f}",
                        f"{record['max_length']:.2f}", f"{record['avg_width']:.2f}",
                        f"{record['confidence']:.1f}%", record['image_path'] or '', record['ai_analysis'] or ''
                    ])

            QMessageBox.information(self, "导出成功", f"已导出 {len(all_records)} 条记录到:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出Excel失败:\n{e}")

    def export_all_to_pdf(self):
        """导出全部AI报告到PDF"""
        try:
            all_records = []
            if self.db:
                result = self.db.query_records(
                    conditions={'has_analysis': True}, page=1, page_size=1000,
                    order_by='id', order='ASC'
                )
                all_records = result['records']

            if not all_records:
                QMessageBox.information(self, "提示", "数据库中没有AI分析记录可导出")
                return

            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出AI报告", os.path.join(REPORTS_DIR, "ai_analysis.txt"),
                "文本文件 (*.txt);;所有文件 (*.*)"
            )
            if not file_path:
                return

            timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# 墙体裂缝检测 - AI分析报告\n")
                f.write(f"# 导出时间: {timestamp}\n\n")
                for record in all_records:
                    f.write(f"设备: {record['device_id']}\n")
                    f.write(f"时间: {datetime.fromtimestamp(record['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"裂缝: {record['crack_count']}条\n")
                    f.write(f"最大宽度: {record['max_width']}mm\n")
                    f.write(f"置信度: {record['confidence']}%\n")
                    f.write(f"AI分析:\n{record['ai_analysis']}\n")
                    f.write("-" * 60 + "\n\n")

            QMessageBox.information(self, "导出成功", f"AI报告已导出到:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出AI报告失败:\n{e}")



# ============================================================
# 第八部分:主窗口类
# ============================================================

class MainWindow(QMainWindow):
    """
    主窗口类 - 整合所有Tab页面
    """

    # 信号：TCP子线程通过此信号将数据转发到主线程入库，规避SQLite跨线程限制
    new_crack_record = pyqtSignal(dict, bytes)

    def __init__(self):
        super().__init__()

        # 数据库初始化
        self.db = DatabaseOperator()
        self.db.connect()
        self.db.init_database()

        # TCP服务端初始化
        self.tcp_server = TCPServer(port=DEFAULT_TCP_PORT, db=self.db, ui_callback=self.tcp_ui_callback)

        # 绑定信号：子线程数据 → 主线程入库+刷新UI
        self.new_crack_record.connect(self.save_and_refresh_ui)

        # 把主窗口引用传给TCP服务端，便于发射信号
        self.tcp_server.main_win = self

        # 初始化主窗口
        self.init_window()

        # 初始化UI
        self.init_ui()

# 标签切换事件：切到历史记录页时才加载数据
        #self.tabWidget.currentChanged.connect(self.on_tab_changed)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        # 初始化目录
        self.init_directories()

        # 启动TCP服务
        self.tcp_server.start()
        self.update_status("TCP服务已启动，等待连接...")

    def init_window(self):
        """初始化主窗口属性"""
        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

    def init_ui(self):
        """初始化UI布局"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)

        # ========== 顶部标题栏 ==========
        title_layout = QHBoxLayout()
        title_label = QLabel(APP_NAME)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2196F3;")
        title_layout.addWidget(title_label)

        title_layout.addStretch()

        # 系统状态显示
        self.system_status_label = QLabel("系统状态: 正常")
        self.system_status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        title_layout.addWidget(self.system_status_label)

        main_layout.addLayout(title_layout)

        # ========== 创建5个Tab页面 ==========
        self.tab_widget = QTabWidget()

        # Tab1: 实时监控
        self.realtime_tab = RealTimeMonitorTab(db=self.db)
        self.tab_widget.addTab(self.realtime_tab, "实时监控")

        # Tab2: 历史记录查询
        #self.history_tab = HistoryQueryTab(db=self.db)
        self.history_tab = HistoryQueryTab(db=self.db, main_window=self)
        self.tab_widget.addTab(self.history_tab, "历史记录")

        # Tab3: 统计图表
        self.statistics_tab = StatisticsTab(db=self.db)
        self.tab_widget.addTab(self.statistics_tab, "统计图表")

        # ★ Tab5 先于 Tab4 创建，以便 AIAnalysisTab 的 load_api_key 能找到 config_tab
        # Tab5: 系统配置与导出
        self.config_tab = SystemConfigTab(db=self.db, parent=self)
        self.tab_widget.addTab(self.config_tab, "系统配置")

        # Tab4: AI智能分析面板
        self.ai_tab = AIAnalysisTab(db=self.db, parent=self)
        self.tab_widget.addTab(self.ai_tab, "AI分析")

        main_layout.addWidget(self.tab_widget)

        # ========== 底部状态栏 ==========
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("系统启动成功，等待连接...")
    def on_tab_changed(self, index):
            # index=1 对应历史记录标签（索引从0开始数）
            # 0=实时监控, 1=历史记录, 2=统计图表, 4=AI分析, 3=系统配置
        if index == 1:
            self.history_tab.refresh_table()

    def init_directories(self):
        """初始化工作目录"""
        directories = [DATA_DIR, IMAGES_DIR, LOGS_DIR, REPORTS_DIR]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

    # ================= 主窗口功能函数实现 =================

    def show_message(self, message, level="INFO"):
        """显示系统消息"""
        # 在状态栏显示
        self.status_bar.showMessage(message, 5000)  # 显示5秒

        # 可选:在日志窗口也显示
        if hasattr(self, 'realtime_tab'):
            self.realtime_tab.log_message(message, level)

    def update_status(self, status):
        """
        更新系统状态

        Args:
            status (str): 状态文本
        """
        self.system_status_label.setText(f"系统状态: {status}")

        if "正常" in status or "成功" in status:
            self.system_status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        elif "告警" in status or "失败" in status or "错误" in status:
            self.system_status_label.setStyleSheet("color: #F44336; font-weight: bold;")
        elif "警告" in status:
            self.system_status_label.setStyleSheet("color: #FF9800; font-weight: bold;")
        else:
            self.system_status_label.setStyleSheet("color: #2196F3; font-weight: bold;")

    def save_and_refresh_ui(self, record_data, img_bytes):
        """
        主线程槽函数：接收TCP子线程发来的裂缝数据，在主线程保存图片、入库、刷新UI。
        由 new_crack_record 信号触发，运行在GUI主线程，sqlite对象安全可用。

        Args:
            record_data (dict): 入库所需的完整记录字段（image_path待回填）
            img_bytes (bytes): 图片二进制数据（裸包传入，标准协议为b''）
        """
        try:
            device_id = record_data.get('device_id', 'UNKNOWN')

            # ---- 保存图片到磁盘（主线程执行，安全） ----
            if img_bytes:
                image_path = self._save_image_to_disk(img_bytes, device_id)
                if image_path:
                    record_data['image_path'] = image_path
            # 标准协议图片已有 image_path（由 _handle_image_packet 保存）

            # ---- 入库 ----
            record_id = self.db.add_record(record_data)

            if record_id > 0:
                image_path = record_data.get('image_path')

                # ---- 构建UI刷新摘要 ----
                crack_info = {
                    'device_id': device_id,
                    'crack_count': record_data.get('crack_count', 0),
                    'max_width': record_data.get('max_width', 0),
                    'confidence': record_data.get('confidence', 0),
                }

                # ---- 刷新实时监控统计 ----
                self.realtime_tab.update_today_stats()

                # ---- 显示缩略图 ----
                if image_path and os.path.exists(image_path):
                    self.realtime_tab.add_crack_image(image_path, crack_info)

                # ---- 刷新历史记录表格（如当前在历史页） ----
                if self.tab_widget.currentIndex() == 1:
                    self.history_tab.refresh_table()

                self.update_status("收到新记录")
                self.status_bar.showMessage(
                    f"收到新记录: {device_id}", 3000
                )
            else:
                self.realtime_tab.log_message("数据存入数据库失败", "ERROR")

        except Exception as e:
            self.realtime_tab.log_message(f"入库/刷新UI异常: {e}", "ERROR")

    def _save_image_to_disk(self, image_data, device_id):
        """
        在主线程保存图片到磁盘

        Args:
            image_data (bytes): 图片二进制数据
            device_id (str): 设备ID

        Returns:
            str: 保存路径，失败返回None
        """
        try:
            from datetime import datetime as dt
            today = dt.now().strftime('%Y-%m-%d')
            device_dir = os.path.join(IMAGES_DIR, today, device_id)
            os.makedirs(device_dir, exist_ok=True)

            timestamp = dt.now().strftime('%H%M%S')
            filename = f"crack_{timestamp}.jpg"
            file_path = os.path.join(device_dir, filename)

            with open(file_path, 'wb') as f:
                f.write(image_data)

            return file_path

        except Exception as e:
            self.realtime_tab.log_message(f"保存图片失败: {e}", "ERROR")
            return None

    def tcp_ui_callback(self, callback_type, *args):
        """
        TCP服务端UI回调函数

        Args:
            callback_type (str): 回调类型
                - 'device_online': 设备上线 (device_id, ip)
                - 'device_offline': 设备离线 (device_id, ip)
                - 'new_image': 新图片 (image_path, crack_info)
                - 'new_record': 新记录 (image_path, crack_info)
            *args: 回调参数
        """
        # 使用QTimer.singleShot将UI操作投递到主线程事件循环，线程安全且无需@pyqtSlot
        if callback_type == 'device_online':
            device_id, ip = args
            QTimer.singleShot(0, lambda: self.on_device_online(device_id, ip))

        elif callback_type == 'device_offline':
            device_id, ip = args
            QTimer.singleShot(0, lambda: self.on_device_offline(device_id, ip))

        elif callback_type == 'new_image':
            image_path, crack_info = args
            QTimer.singleShot(0, lambda: self.on_new_image(image_path, crack_info))

        elif callback_type == 'new_record':
            image_path, crack_info = args
            QTimer.singleShot(0, lambda: self.on_new_record(image_path, crack_info))

    def on_device_online(self, device_id, ip):
        """设备上线回调（在主线程执行）"""
        # 更新实时监控Tab的设备状态
        self.realtime_tab.update_device_status(device_id, ip, "online")
        self.update_status(f"设备 {device_id} 上线")
        self.status_bar.showMessage(f"设备 {device_id} ({ip}) 上线", 3000)

    def on_device_offline(self, device_id, ip):
        """设备离线回调（在主线程执行）"""
        # 更新实时监控Tab的设备状态
        self.realtime_tab.update_device_status(device_id, ip, "offline")
        self.update_status(f"设备 {device_id} 离线")
        self.status_bar.showMessage(f"设备 {device_id} ({ip}) 离线", 3000)

    def on_new_image(self, image_path, crack_info):
        """新图片回调（在主线程执行）"""
        # 在实时监控Tab显示图片
        if os.path.exists(image_path):
            self.realtime_tab.add_crack_image(image_path, crack_info)

    def on_new_record(self, image_path, crack_info):
        """新记录回调（在主线程执行）"""
        # 刷新实时监控统计
        self.realtime_tab.update_today_stats()

        # 如果有图片，显示在实时监控Tab
        if image_path and os.path.exists(image_path):
            self.realtime_tab.add_crack_image(image_path, crack_info)

        # 刷新历史记录Tab（如果当前在历史记录页面）
        current_index = self.tab_widget.currentIndex()
        if current_index == 1:  # Tab2是历史记录
            self.history_tab.refresh_table()

        self.update_status("收到新记录")
        self.status_bar.showMessage(f"收到新记录: {crack_info.get('device_id', 'N/A')}", 3000)

    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止TCP服务
        if self.tcp_server:
            self.tcp_server.stop()

        # 关闭数据库
        if self.db:
            self.db.close()

        event.accept()


# ============================================================
# 第九部分:程序入口
# ============================================================

def main():
    """程序入口函数"""
    # 创建应用程序实例
    app = QApplication([])
    app.setStyle('Fusion')  # 使用Fusion风格

    # 创建主窗口
    window = MainWindow()
    window.show()

    # 运行应用程序
    app.exec_()


if __name__ == "__main__":
    main()