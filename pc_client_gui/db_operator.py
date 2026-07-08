#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
墙体裂缝检测上位机 - 数据库操作模块
功能：SQLite数据库的封装操作类
说明：纯数据库工具类，无UI代码，返回标准列表字典格式
"""

import sqlite3
import os
import shutil
from datetime import datetime, timedelta


# ============================================================
# 数据库路径（与main.py保持一致）
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "crack_detection.db")


# ============================================================
# 数据库操作类
# ============================================================

class DatabaseOperator:
    """
    数据库操作工具类
    封装所有SQLite数据库操作，返回标准列表/字典格式
    """

    def __init__(self, db_path=None):
        """
        初始化数据库操作类

        Args:
            db_path (str, optional): 数据库文件路径，默认使用DB_PATH常量
        """
        self.db_path = db_path if db_path else DB_PATH
        self.conn = None

    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()

    def connect(self):
        """
        连接数据库

        Returns:
            bool: 连接成功返回True，失败返回False
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # 返回字典格式
            return True
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return False

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None

    def init_database(self):
        """
        初始化数据库，创建数据表

        表结构: crack_records
        - id: 记录ID（自增主键）
        - device_id: 设备ID
        - timestamp: 时间戳（UNIX时间戳）
        - crack_count: 裂缝条数
        - max_width: 最大裂缝宽度(mm)
        - max_length: 最大裂缝长度(mm)
        - avg_width: 平均裂缝宽度(mm)
        - confidence: 识别置信度(0-100)
        - image_path: 图片本地路径
        - ai_analysis: AI分析文本
        - entry_date: 录入日期(YYYY-MM-DD)
        - create_time: 创建时间

        Returns:
            bool: 初始化成功返回True，失败返回False
        """
        try:
            if not self.conn:
                self.connect()

            cursor = self.conn.cursor()

            # 创建裂缝记录表
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS crack_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                crack_count INTEGER NOT NULL,
                max_width REAL NOT NULL,
                max_length REAL NOT NULL,
                avg_width REAL NOT NULL,
                confidence REAL NOT NULL,
                image_path TEXT,
                ai_analysis TEXT,
                entry_date TEXT NOT NULL,
                create_time DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """

            cursor.execute(create_table_sql)

            # 创建索引以提高查询性能
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_device_id ON crack_records(device_id)",
                "CREATE INDEX IF NOT EXISTS idx_timestamp ON crack_records(timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_entry_date ON crack_records(entry_date)",
                "CREATE INDEX IF NOT EXISTS idx_device_date ON crack_records(device_id, entry_date)"
            ]

            for index_sql in indexes:
                cursor.execute(index_sql)

            self.conn.commit()
            print("数据库初始化成功")
            return True

        except Exception as e:
            print(f"数据库初始化失败: {e}")
            if self.conn:
                self.conn.rollback()
            return False

    def add_record(self, record_data):
        """
        新增一条识别记录

        Args:
            record_data (dict): 记录数据字典，包含以下字段：
                - device_id (str): 设备ID
                - timestamp (int): 时间戳
                - crack_count (int): 裂缝条数
                - max_width (float): 最大裂缝宽度
                - max_length (float): 最大裂缝长度
                - avg_width (float): 平均裂缝宽度
                - confidence (float): 识别置信度
                - image_path (str, optional): 图片路径
                - ai_analysis (str, optional): AI分析文本
                - entry_date (str, optional): 录入日期

        Returns:
            int: 新增记录的ID，失败返回-1
        """
        try:
            if not self.conn:
                self.connect()

            cursor = self.conn.cursor()

            insert_sql = """
            INSERT INTO crack_records (
                device_id, timestamp, crack_count, max_width,
                max_length, avg_width, confidence, image_path,
                ai_analysis, entry_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            values = (
                record_data.get('device_id'),
                record_data.get('timestamp'),
                record_data.get('crack_count'),
                record_data.get('max_width'),
                record_data.get('max_length'),
                record_data.get('avg_width'),
                record_data.get('confidence'),
                record_data.get('image_path'),
                record_data.get('ai_analysis'),
                record_data.get('entry_date')
            )

            cursor.execute(insert_sql, values)
            self.conn.commit()

            return cursor.lastrowid

        except Exception as e:
            print(f"新增记录失败: {e}")
            if self.conn:
                self.conn.rollback()
            return -1

    def get_record_by_id(self, record_id):
        """
        根据记录ID查询单条记录

        Args:
            record_id (int): 记录ID

        Returns:
            dict: 记录数据字典，未找到返回None
        """
        try:
            if not self.conn:
                self.connect()

            cursor = self.conn.cursor()

            query_sql = "SELECT * FROM crack_records WHERE id = ?"
            cursor.execute(query_sql, (record_id,))

            row = cursor.fetchone()

            if row:
                return dict(row)
            return None

        except Exception as e:
            print(f"查询记录失败: {e}")
            return None

    def query_records(self, conditions=None, page=1, page_size=20, order_by='id', order='DESC'):
        """
        多条件分页查询记录

        Args:
            conditions (dict, optional): 查询条件字典，支持以下字段：
                - device_id (str): 设备ID
                - start_date (str): 起始日期 (YYYY-MM-DD)
                - end_date (str): 结束日期 (YYYY-MM-DD)
                - min_width (float): 最小裂缝宽度
                - max_width (float): 最大裂缝宽度
                - min_confidence (float): 最小置信度
                - has_image (bool): 是否有图片
                - has_analysis (bool): 是否有AI分析
            page (int): 页码，从1开始
            page_size (int): 每页记录数
            order_by (str): 排序字段
            order (str): 排序方式，ASC或DESC

        Returns:
            dict: 包含以下字段的字典：
                - records (list): 记录列表
                - total (int): 总记录数
                - page (int): 当前页码
                - page_size (int): 每页记录数
                - total_pages (int): 总页数
        """
        try:
            if not self.conn:
                self.connect()

            cursor = self.conn.cursor()

            # 构建WHERE条件
            where_clauses = []
            params = []

            if conditions:
                if 'device_id' in conditions and conditions['device_id']:
                    where_clauses.append("device_id = ?")
                    params.append(conditions['device_id'])

                if 'start_date' in conditions and conditions['start_date']:
                    where_clauses.append("entry_date >= ?")
                    params.append(conditions['start_date'])

                if 'end_date' in conditions and conditions['end_date']:
                    where_clauses.append("entry_date <= ?")
                    params.append(conditions['end_date'])

                if 'min_width' in conditions and conditions['min_width'] is not None:
                    where_clauses.append("max_width >= ?")
                    params.append(conditions['min_width'])

                if 'max_width' in conditions and conditions['max_width'] is not None:
                    where_clauses.append("max_width <= ?")
                    params.append(conditions['max_width'])

                if 'min_confidence' in conditions and conditions['min_confidence'] is not None:
                    where_clauses.append("confidence >= ?")
                    params.append(conditions['min_confidence'])

                if 'has_image' in conditions:
                    if conditions['has_image']:
                        where_clauses.append("image_path IS NOT NULL AND image_path != ''")
                    else:
                        where_clauses.append("(image_path IS NULL OR image_path = '')")

                if 'has_analysis' in conditions:
                    if conditions['has_analysis']:
                        where_clauses.append("ai_analysis IS NOT NULL AND ai_analysis != ''")
                    else:
                        where_clauses.append("(ai_analysis IS NULL OR ai_analysis = '')")

            # 构建SQL查询
            where_sql = ""
            if where_clauses:
                where_sql = "WHERE " + " AND ".join(where_clauses)

            # 查询总数
            count_sql = f"SELECT COUNT(*) as total FROM crack_records {where_sql}"
            cursor.execute(count_sql, params)
            total = cursor.fetchone()['total']

            # 计算分页
            offset = (page - 1) * page_size
            total_pages = (total + page_size - 1) // page_size if total > 0 else 0

            # 查询记录
            query_sql = f"""
            SELECT * FROM crack_records {where_sql}
            ORDER BY {order_by} {order}
            LIMIT ? OFFSET ?
            """

            cursor.execute(query_sql, params + [page_size, offset])
            rows = cursor.fetchall()

            records = [dict(row) for row in rows]

            return {
                'records': records,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': total_pages
            }

        except Exception as e:
            print(f"分页查询失败: {e}")
            return {
                'records': [],
                'total': 0,
                'page': page,
                'page_size': page_size,
                'total_pages': 0
            }

    def query_by_device(self, device_id, start_date=None, end_date=None, limit=None):
        """
        按设备ID筛选记录

        Args:
            device_id (str): 设备ID
            start_date (str, optional): 起始日期 (YYYY-MM-DD)
            end_date (str, optional): 结束日期 (YYYY-MM-DD)
            limit (int, optional): 限制返回记录数

        Returns:
            list: 记录列表
        """
        conditions = {
            'device_id': device_id,
            'start_date': start_date,
            'end_date': end_date
        }

        result = self.query_records(conditions=conditions, page=1, page_size=limit if limit else 1000)
        return result['records']

    def query_by_date(self, start_date, end_date=None, device_id=None):
        """
        按日期范围筛选记录

        Args:
            start_date (str): 起始日期 (YYYY-MM-DD)
            end_date (str, optional): 结束日期 (YYYY-MM-DD)，默认为起始日期
            device_id (str, optional): 设备ID，为空则查询所有设备

        Returns:
            list: 记录列表
        """
        conditions = {
            'start_date': start_date,
            'end_date': end_date if end_date else start_date,
            'device_id': device_id
        }

        result = self.query_records(conditions=conditions, page=1, page_size=1000)
        return result['records']

    def get_today_statistics(self):
        """
        统计今日裂缝总数和最大宽度

        Returns:
            dict: 包含以下字段的字典：
                - total_cracks (int): 今日裂缝总数
                - max_width (float): 今日最大裂缝宽度
                - record_count (int): 今日识别记录数
                - avg_confidence (float): 今日平均置信度
        """
        try:
            if not self.conn:
                self.connect()

            cursor = self.conn.cursor()

            today = datetime.now().strftime('%Y-%m-%d')

            # 统计今日裂缝总数
            crack_count_sql = """
            SELECT SUM(crack_count) as total_cracks
            FROM crack_records
            WHERE entry_date = ?
            """
            cursor.execute(crack_count_sql, (today,))
            total_cracks = cursor.fetchone()['total_cracks'] or 0

            # 统计今日最大裂缝宽度
            max_width_sql = """
            SELECT MAX(max_width) as max_width
            FROM crack_records
            WHERE entry_date = ?
            """
            cursor.execute(max_width_sql, (today,))
            max_width = cursor.fetchone()['max_width'] or 0.0

            # 统计今日识别记录数
            record_count_sql = """
            SELECT COUNT(*) as record_count
            FROM crack_records
            WHERE entry_date = ?
            """
            cursor.execute(record_count_sql, (today,))
            record_count = cursor.fetchone()['record_count'] or 0

            # 统计今日平均置信度
            avg_confidence_sql = """
            SELECT AVG(confidence) as avg_confidence
            FROM crack_records
            WHERE entry_date = ?
            """
            cursor.execute(avg_confidence_sql, (today,))
            avg_confidence = cursor.fetchone()['avg_confidence'] or 0.0

            return {
                'total_cracks': total_cracks,
                'max_width': max_width,
                'record_count': record_count,
                'avg_confidence': avg_confidence
            }

        except Exception as e:
            print(f"统计今日数据失败: {e}")
            return {
                'total_cracks': 0,
                'max_width': 0.0,
                'record_count': 0,
                'avg_confidence': 0.0
            }

    def get_daily_statistics(self, start_date, end_date=None):
        """
        获取指定日期范围内的每日统计数据

        Args:
            start_date (str): 起始日期 (YYYY-MM-DD)
            end_date (str, optional): 结束日期 (YYYY-MM-DD)，默认为起始日期

        Returns:
            list: 每日统计数据列表，每个元素包含以下字段：
                - date (str): 日期
                - total_cracks (int): 裂缝总数
                - max_width (float): 最大裂缝宽度
                - record_count (int): 识别记录数
        """
        try:
            if not self.conn:
                self.connect()

            cursor = self.conn.cursor()

            end_date = end_date if end_date else start_date

            query_sql = """
            SELECT
                entry_date as date,
                SUM(crack_count) as total_cracks,
                MAX(max_width) as max_width,
                COUNT(*) as record_count
            FROM crack_records
            WHERE entry_date >= ? AND entry_date <= ?
            GROUP BY entry_date
            ORDER BY entry_date ASC
            """

            cursor.execute(query_sql, (start_date, end_date))
            rows = cursor.fetchall()

            return [dict(row) for row in rows]

        except Exception as e:
            print(f"获取每日统计失败: {e}")
            return []

    def get_device_statistics(self, start_date=None, end_date=None):
        """
        获取设备统计数据

        Args:
            start_date (str, optional): 起始日期 (YYYY-MM-DD)
            end_date (str, optional): 结束日期 (YYYY-MM-DD)

        Returns:
            list: 设备统计数据列表，每个元素包含以下字段：
                - device_id (str): 设备ID
                - total_cracks (int): 裂缝总数
                - max_width (float): 最大裂缝宽度
                - record_count (int): 识别记录数
        """
        try:
            if not self.conn:
                self.connect()

            cursor = self.conn.cursor()

            where_clauses = []
            params = []

            if start_date:
                where_clauses.append("entry_date >= ?")
                params.append(start_date)

            if end_date:
                where_clauses.append("entry_date <= ?")
                params.append(end_date)

            where_sql = ""
            if where_clauses:
                where_sql = "WHERE " + " AND ".join(where_clauses)

            query_sql = f"""
            SELECT
                device_id,
                SUM(crack_count) as total_cracks,
                MAX(max_width) as max_width,
                COUNT(*) as record_count
            FROM crack_records
            {where_sql}
            GROUP BY device_id
            ORDER BY device_id ASC
            """

            cursor.execute(query_sql, params)
            rows = cursor.fetchall()

            return [dict(row) for row in rows]

        except Exception as e:
            print(f"获取设备统计失败: {e}")
            return []

    def get_all_devices(self):
        """
        获取所有设备ID列表

        Returns:
            list: 设备ID列表
        """
        try:
            if not self.conn:
                self.connect()

            cursor = self.conn.cursor()

            query_sql = "SELECT DISTINCT device_id FROM crack_records ORDER BY device_id ASC"
            cursor.execute(query_sql)
            rows = cursor.fetchall()

            return [row['device_id'] for row in rows]

        except Exception as e:
            print(f"获取设备列表失败: {e}")
            return []

    def delete_record(self, record_id):
        """
        删除单条记录

        Args:
            record_id (int): 记录ID

        Returns:
            bool: 删除成功返回True，失败返回False
        """
        try:
            if not self.conn:
                self.connect()

            cursor = self.conn.cursor()

            delete_sql = "DELETE FROM crack_records WHERE id = ?"
            cursor.execute(delete_sql, (record_id,))

            self.conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            print(f"删除记录失败: {e}")
            if self.conn:
                self.conn.rollback()
            return False

    def batch_delete_records(self, record_ids):
        """
        批量删除记录

        Args:
            record_ids (list): 记录ID列表

        Returns:
            dict: 包含以下字段的字典：
                - success (bool): 是否全部成功
                - deleted_count (int): 成功删除的数量
                - failed_count (int): 失败的数量
                - failed_ids (list): 失败的记录ID列表
        """
        if not record_ids:
            return {
                'success': True,
                'deleted_count': 0,
                'failed_count': 0,
                'failed_ids': []
            }

        try:
            if not self.conn:
                self.connect()

            cursor = self.conn.cursor()

            delete_sql = "DELETE FROM crack_records WHERE id = ?"
            deleted_count = 0
            failed_ids = []

            for record_id in record_ids:
                try:
                    cursor.execute(delete_sql, (record_id,))
                    if cursor.rowcount > 0:
                        deleted_count += 1
                    else:
                        failed_ids.append(record_id)
                except Exception:
                    failed_ids.append(record_id)

            self.conn.commit()

            return {
                'success': len(failed_ids) == 0,
                'deleted_count': deleted_count,
                'failed_count': len(failed_ids),
                'failed_ids': failed_ids
            }

        except Exception as e:
            print(f"批量删除记录失败: {e}")
            if self.conn:
                self.conn.rollback()
            return {
                'success': False,
                'deleted_count': 0,
                'failed_count': len(record_ids),
                'failed_ids': record_ids
            }

    def delete_by_date_range(self, start_date, end_date=None, device_id=None):
        """
        按日期范围删除记录

        Args:
            start_date (str): 起始日期 (YYYY-MM-DD)
            end_date (str, optional): 结束日期 (YYYY-MM-DD)，默认为起始日期
            device_id (str, optional): 设备ID，为空则删除所有设备

        Returns:
            int: 删除的记录数
        """
        try:
            if not self.conn:
                self.connect()

            cursor = self.conn.cursor()

            end_date = end_date if end_date else start_date

            where_clauses = ["entry_date >= ? AND entry_date <= ?"]
            params = [start_date, end_date]

            if device_id:
                where_clauses.append("device_id = ?")
                params.append(device_id)

            delete_sql = f"DELETE FROM crack_records WHERE {' AND '.join(where_clauses)}"
            cursor.execute(delete_sql, params)

            self.conn.commit()
            return cursor.rowcount

        except Exception as e:
            print(f"按日期范围删除记录失败: {e}")
            if self.conn:
                self.conn.rollback()
            return 0

    def update_ai_analysis(self, record_id, ai_analysis_text):
        """
        更新记录的AI分析文本

        Args:
            record_id (int): 记录ID
            ai_analysis_text (str): AI分析文本

        Returns:
            bool: 更新成功返回True，失败返回False
        """
        try:
            if not self.conn:
                self.connect()

            cursor = self.conn.cursor()

            update_sql = "UPDATE crack_records SET ai_analysis = ? WHERE id = ?"
            cursor.execute(update_sql, (ai_analysis_text, record_id))

            self.conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            print(f"更新AI分析失败: {e}")
            if self.conn:
                self.conn.rollback()
            return False

    def backup_database(self, backup_path=None):
        """
        备份数据库

        Args:
            backup_path (str, optional): 备份文件路径，默认生成带时间戳的备份

        Returns:
            bool: 备份成功返回True，失败返回False
        """
        try:
            # 关闭当前连接
            if self.conn:
                self.close()

            # 生成默认备份路径
            if not backup_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_dir = os.path.join(os.path.dirname(self.db_path), 'backups')
                os.makedirs(backup_dir, exist_ok=True)
                backup_path = os.path.join(backup_dir, f'crack_detection_backup_{timestamp}.db')

            # 复制数据库文件
            shutil.copy2(self.db_path, backup_path)

            # 重新连接
            self.connect()

            print(f"数据库备份成功: {backup_path}")
            return True

        except Exception as e:
            print(f"数据库备份失败: {e}")
            return False

    def restore_database(self, backup_path):
        """
        恢复数据库

        Args:
            backup_path (str): 备份文件路径

        Returns:
            bool: 恢复成功返回True，失败返回False
        """
        try:
            if not os.path.exists(backup_path):
                print(f"备份文件不存在: {backup_path}")
                return False

            # 关闭当前连接
            if self.conn:
                self.close()

            # 复制备份文件覆盖当前数据库
            shutil.copy2(backup_path, self.db_path)

            # 重新连接
            self.connect()

            print(f"数据库恢复成功: {backup_path}")
            return True

        except Exception as e:
            print(f"数据库恢复失败: {e}")
            return False

    def get_all_records_for_export(self, start_date=None, end_date=None, device_id=None):
        """
        获取所有记录用于导出

        Args:
            start_date (str, optional): 起始日期 (YYYY-MM-DD)
            end_date (str, optional): 结束日期 (YYYY-MM-DD)
            device_id (str, optional): 设备ID

        Returns:
            list: 记录列表
        """
        conditions = {
            'start_date': start_date,
            'end_date': end_date,
            'device_id': device_id
        }

        result = self.query_records(conditions=conditions, page=1, page_size=10000)
        return result['records']

    def get_total_record_count(self):
        """
        获取数据库总记录数

        Returns:
            int: 总记录数
        """
        try:
            if not self.conn:
                self.connect()

            cursor = self.conn.cursor()

            query_sql = "SELECT COUNT(*) as total FROM crack_records"
            cursor.execute(query_sql)
            return cursor.fetchone()['total']

        except Exception as e:
            print(f"获取总记录数失败: {e}")
            return 0

    def get_date_range(self):
        """
        获取数据库中记录的日期范围

        Returns:
            dict: 包含以下字段的字典：
                - min_date (str): 最早日期
                - max_date (str): 最晚日期
        """
        try:
            if not self.conn:
                self.connect()

            cursor = self.conn.cursor()

            query_sql = """
            SELECT
                MIN(entry_date) as min_date,
                MAX(entry_date) as max_date
            FROM crack_records
            """
            cursor.execute(query_sql)
            result = cursor.fetchone()

            return {
                'min_date': result['min_date'],
                'max_date': result['max_date']
            }

        except Exception as e:
            print(f"获取日期范围失败: {e}")
            return {
                'min_date': None,
                'max_date': None
            }

    def clear_all_data(self):
        """
        清空所有数据（谨慎使用）

        Returns:
            bool: 清空成功返回True，失败返回False
        """
        try:
            if not self.conn:
                self.connect()

            cursor = self.conn.cursor()

            cursor.execute("DELETE FROM crack_records")
            self.conn.commit()

            # 重置自增ID
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='crack_records'")
            self.conn.commit()

            print("数据库已清空")
            return True

        except Exception as e:
            print(f"清空数据库失败: {e}")
            if self.conn:
                self.conn.rollback()
            return False


# ============================================================
# 便捷函数（全局使用）
# ============================================================

def init_db():
    """
    便捷函数：初始化数据库

    Returns:
        DatabaseOperator: 数据库操作实例
    """
    db = DatabaseOperator()
    db.init_database()
    return db


def get_db():
    """
    便捷函数：获取数据库操作实例

    Returns:
        DatabaseOperator: 数据库操作实例
    """
    return DatabaseOperator()


# ============================================================
# 模块测试代码
# ============================================================

if __name__ == "__main__":
    print("墙体裂缝检测上位机 - 数据库操作模块测试")
    print("=" * 60)

    # 使用上下文管理器自动管理连接
    with DatabaseOperator() as db:
        # 初始化数据库
        print("\n[1] 初始化数据库...")
        db.init_database()

        # 测试新增记录
        print("\n[2] 测试新增记录...")
        test_record = {
            'device_id': 'RK3588_001',
            'timestamp': int(datetime.now().timestamp()),
            'crack_count': 3,
            'max_width': 2.5,
            'max_length': 15.8,
            'avg_width': 1.2,
            'confidence': 95.5,
            'image_path': '/images/2026-07-05/RK3588_001/crack_001.jpg',
            'ai_analysis': '检测到3条裂缝，建议及时处理',
            'entry_date': datetime.now().strftime('%Y-%m-%d')
        }

        record_id = db.add_record(test_record)
        print(f"新增记录ID: {record_id}")

        # 测试查询记录
        print("\n[3] 测试查询记录...")
        record = db.get_record_by_id(record_id)
        print(f"查询结果: {record}")

        # 测试分页查询
        print("\n[4] 测试分页查询...")
        conditions = {
            'device_id': 'RK3588_001',
            'start_date': datetime.now().strftime('%Y-%m-%d')
        }
        result = db.query_records(conditions=conditions, page=1, page_size=10)
        print(f"分页查询结果: 总记录数={result['total']}, 记录数={len(result['records'])}")

        # 测试今日统计
        print("\n[5] 测试今日统计...")
        today_stats = db.get_today_statistics()
        print(f"今日统计: {today_stats}")

        # 测试获取设备列表
        print("\n[6] 测试获取设备列表...")
        devices = db.get_all_devices()
        print(f"设备列表: {devices}")

        # 测试删除记录
        print("\n[7] 测试删除记录...")
        deleted = db.delete_record(record_id)
        print(f"删除结果: {deleted}")

        # 测试备份数据库
        print("\n[8] 测试备份数据库...")
        backup_success = db.backup_database()
        print(f"备份结果: {backup_success}")

    print("\n测试完成！")