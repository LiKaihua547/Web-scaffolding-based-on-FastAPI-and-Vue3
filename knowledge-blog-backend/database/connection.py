import pymysql
from config.config import DB_CONFIG

def get_db_connection():
    """返回一个 MySQL 数据库连接"""
    return pymysql.connect(**DB_CONFIG)