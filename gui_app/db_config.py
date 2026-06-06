"""
db_config.py - Quản lý kết nối MySQL với Connection Pool
"""
import os
import pymysql
import pandas as pd
from dotenv import load_dotenv

# 1. Lấy đường dẫn lùi ra 1 cấp (thư mục citibike_tool_stack) để tìm file .env chung
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT_DIR, ".env")

# Nạp file .env từ thư mục gốc
load_dotenv(dotenv_path=ENV_PATH)

# 2. Cấu hình DB lấy từ file .env chung
DB_CONFIG = {
    # Chạy Streamlit ngoài container nên gọi thẳng vào localhost:3307
    "host":   "localhost",
    "port":   3307,
    # Các biến cấu hình MySQL (Khớp với file .env chung)
    "db":     os.getenv("MYSQL_DATABASE", "testdb"),
    "user":   os.getenv("MYSQL_USER", "testuser"),
    "passwd": os.getenv("MYSQL_PASSWORD", "testpass"),
    
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


def get_connection():
    """Tạo và trả về một kết nối MySQL mới."""
    return pymysql.connect(**DB_CONFIG)


def run_query(sql: str, params=None) -> pd.DataFrame:
    """Chạy SELECT query, trả về DataFrame."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            rows = cur.fetchall()
        return pd.DataFrame(rows)
    finally:
        conn.close()


def run_write(sql: str, params=None) -> int:
    """Chạy INSERT / UPDATE / DELETE, trả về số dòng bị ảnh hưởng."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            affected = cur.rowcount
        conn.commit()
        return affected
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def run_many(sql: str, data: list) -> int:
    """executemany cho bulk insert."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.executemany(sql, data)
            affected = cur.rowcount
        conn.commit()
        return affected
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def check_connection() -> bool:
    """Kiểm tra kết nối DB có hoạt động không."""
    try:
        conn = get_connection()
        conn.ping()
        conn.close()
        return True
    except Exception:
        return False