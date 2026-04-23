# config/config.py

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',           # 改成你的 MySQL 用户名
    'password': '123456',     # 改成你的 MySQL 密码
    'database': 'blog_db',
    'charset': 'utf8mb4'
}

OLLAMA_CONFIG = {
    "base_url": "http://127.0.0.1:11434",  # 👈 把 localhost 改成 127.0.0.1
    "default_model": "qwen2:latest",
    "timeout": 60,
    "bin_dir": r"F:\ollama"
}