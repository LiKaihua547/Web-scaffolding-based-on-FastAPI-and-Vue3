import os

# 需要创建的目录列表（相对于脚本所在目录）
DIRS = [
    "app",
    "app/models",
    "app/schemas",
    "app/crud",
    "app/services",
    "app/api",
    "app/api/v1",
    "app/api/v1/endpoints",
    "app/utils",
]

# 需要创建的空白文件列表
FILES = [
    ".env",
    "requirements.txt",
    "app/__init__.py",
    "app/config.py",
    "app/database.py",
    "app/main.py",
    "app/models/__init__.py",
    "app/models/article.py",
    "app/schemas/__init__.py",
    "app/schemas/article.py",
    "app/crud/__init__.py",
    "app/crud/article.py",
    "app/services/__init__.py",
    "app/services/article.py",
    "app/api/__init__.py",
    "app/api/v1/__init__.py",
    "app/api/v1/endpoints/__init__.py",
    "app/api/v1/endpoints/article.py",
    "app/utils/__init__.py",
    "app/utils/response.py",
    "app/utils/exceptions.py",
]


def setup():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 创建目录
    for d in DIRS:
        path = os.path.join(base_dir, d)
        os.makedirs(path, exist_ok=True)
        print(f"创建目录: {path}")

    # 创建空白文件
    for f in FILES:
        path = os.path.join(base_dir, f)
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as fp:
                pass  # 创建空文件
            print(f"创建文件: {path}")
        else:
            print(f"文件已存在，跳过: {path}")


if __name__ == "__main__":
    setup()
    print("\n✅ 所有目录和空白文件已生成！")