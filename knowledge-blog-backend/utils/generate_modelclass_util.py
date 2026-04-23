# utils/generate_code.py
import os
import sys
import pymysql
from config.config import DB_CONFIG

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

TYPE_MAPPING = {
    'int': 'int', 'tinyint': 'int', 'smallint': 'int', 'mediumint': 'int', 'bigint': 'int',
    'varchar': 'str', 'char': 'str', 'text': 'str', 'longtext': 'str',
    'datetime': 'datetime', 'timestamp': 'datetime', 'date': 'date',
    'float': 'float', 'double': 'float', 'decimal': 'float',
}

def get_table_columns(table_name):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
            ORDER BY ORDINAL_POSITION
        """, (DB_CONFIG['database'], table_name))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def generate_model(table_name):
    columns = get_table_columns(table_name)
    if not columns:
        print(f"表 '{table_name}' 不存在或无字段")
        return

    class_name = table_name.capitalize()
    file_name = f"{class_name}.py"
    output_dir = os.path.join(BASE_DIR, 'model')
    file_path = os.path.join(output_dir, file_name)
    os.makedirs(output_dir, exist_ok=True)

    lines = [
        f"# model/{file_name}",
        f"# 自动生成的 Pydantic 模型类，对应表：{table_name}",
        "",
        "from pydantic import BaseModel",
        "from typing import Optional",
        "from datetime import datetime, date",
        "",
        f"class {class_name}(BaseModel):",
        f'    """{table_name} 表模型"""',
        ""
    ]

    # ---------- 字段全部设为 Optional，默认 None ----------
    for col in columns:
        col_name = col[0]
        data_type = col[1]
        py_type = TYPE_MAPPING.get(data_type, 'str')
        # 全部字段设为 Optional，默认 None
        if py_type in ('datetime', 'date'):
            field_type = py_type
        else:
            field_type = py_type
        lines.append(f"    {col_name}: Optional[{field_type}] = None")

    lines.append("")

    # ---------- getter / setter 方法 ----------
    for col in columns:
        col_name = col[0]
        py_type = TYPE_MAPPING.get(col[1], 'str')
        if py_type in ('datetime', 'date'):
            return_type = py_type
        else:
            return_type = py_type

        # getter
        lines.append(f"    def get_{col_name}(self) -> Optional[{return_type}]:")
        lines.append(f"        return self.{col_name}")
        lines.append("")
        # setter
        lines.append(f"    def set_{col_name}(self, value: Optional[{return_type}]):")
        lines.append(f"        self.{col_name} = value")
        lines.append("")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"✅ 生成 Model：{file_path}")
def generate_dao(table_name, force=False):
    """
    生成 DAO 文件。如果文件已存在且 force=False，则跳过。
    """
    columns = get_table_columns(table_name)
    if not columns:
        return

    class_name = table_name.capitalize()
    dao_class_name = f"{class_name}Dao"
    file_name = f"{dao_class_name}.py"
    output_dir = os.path.join(BASE_DIR, 'dao')
    file_path = os.path.join(output_dir, file_name)
    os.makedirs(output_dir, exist_ok=True)
    #
    # if os.path.exists(file_path) and not force:
    #     print(f"⏭️  DAO 文件已存在，跳过生成：{file_path}")
    #     return

    pk_column = None
    for col in columns:
        if col[4] == 'PRI':
            pk_column = col[0]
            break
    if not pk_column:
        print(f"警告：表 '{table_name}' 没有主键，部分方法可能无法生成。")
        pk_column = 'id'

    all_cols = [col[0] for col in columns]
    non_pk_cols = [col for col in all_cols if col != pk_column]
    insert_cols = non_pk_cols
    insert_placeholders = ', '.join(['%s'] * len(insert_cols))
    update_set = ', '.join([f"{col} = %s" for col in non_pk_cols])

    lines = [
        f"# dao/{file_name}",
        f"# 自动生成的 DAO 类，对应表：{table_name}",
        "",
        "from database.connection import get_db_connection",
        f"from model.{class_name} import {class_name}",
        "",
        f"class {dao_class_name}:",
        f'    """{table_name} 表数据访问对象"""',
        ""
    ]

    # 修改 _row_to_obj：使用字典构建，然后 model_validate 避免逐个 setter 触发校验
    lines.append("    def _row_to_obj(self, row, columns):")
    lines.append("        data = {col: row[i] for i, col in enumerate(columns)}")
    lines.append(f"        return {class_name}.model_validate(data)")
    lines.append("")

    lines.append(f"    def find_by_id(self, {pk_column}):")
    lines.append("        conn = get_db_connection()")
    lines.append("        cursor = conn.cursor()")
    lines.append("        try:")
    lines.append(f"            cursor.execute(\"SELECT * FROM {table_name} WHERE {pk_column} = %s\", ({pk_column},))")
    lines.append("            row = cursor.fetchone()")
    lines.append("            if not row:")
    lines.append("                return None")
    lines.append("            columns = [col[0] for col in cursor.description]")
    lines.append("            return self._row_to_obj(row, columns)")
    lines.append("        finally:")
    lines.append("            cursor.close()")
    lines.append("            conn.close()")
    lines.append("")

    lines.append("    def find_all(self):")
    lines.append("        conn = get_db_connection()")
    lines.append("        cursor = conn.cursor()")
    lines.append("        try:")
    lines.append(f"            cursor.execute(\"SELECT * FROM {table_name}\")")
    lines.append("            rows = cursor.fetchall()")
    lines.append("            columns = [col[0] for col in cursor.description]")
    lines.append("            return [self._row_to_obj(row, columns) for row in rows]")
    lines.append("        finally:")
    lines.append("            cursor.close()")
    lines.append("            conn.close()")
    lines.append("")

    lines.append(f"    def save(self, obj: {class_name}):")
    lines.append("        conn = get_db_connection()")
    lines.append("        cursor = conn.cursor()")
    lines.append("        try:")
    lines.append(f"            sql = \"INSERT INTO {table_name} ({', '.join(insert_cols)}) VALUES ({insert_placeholders})\"")
    getters = ', '.join([f"obj.get_{col}()" for col in insert_cols])
    lines.append(f"            cursor.execute(sql, ({getters}))")
    lines.append("            conn.commit()")
    lines.append("            return True")
    lines.append("        except Exception as e:")
    lines.append("            print(f\"插入失败: {e}\")")
    lines.append("            return False")
    lines.append("        finally:")
    lines.append("            cursor.close()")
    lines.append("            conn.close()")
    lines.append("")

    lines.append(f"    def update(self, obj: {class_name}):")
    lines.append("        conn = get_db_connection()")
    lines.append("        cursor = conn.cursor()")
    lines.append("        try:")
    lines.append(f"            sql = \"UPDATE {table_name} SET {update_set} WHERE {pk_column} = %s\"")
    getters = ', '.join([f"obj.get_{col}()" for col in non_pk_cols])
    lines.append(f"            cursor.execute(sql, ({getters}, obj.get_{pk_column}()))")
    lines.append("            conn.commit()")
    lines.append("            return True")
    lines.append("        except Exception as e:")
    lines.append("            print(f\"更新失败: {e}\")")
    lines.append("            return False")
    lines.append("        finally:")
    lines.append("            cursor.close()")
    lines.append("            conn.close()")
    lines.append("")

    lines.append(f"    def delete_by_id(self, {pk_column}):")
    lines.append("        conn = get_db_connection()")
    lines.append("        cursor = conn.cursor()")
    lines.append("        try:")
    lines.append(f"            cursor.execute(\"DELETE FROM {table_name} WHERE {pk_column} = %s\", ({pk_column},))")
    lines.append("            conn.commit()")
    lines.append("            return True")
    lines.append("        except Exception as e:")
    lines.append("            print(f\"删除失败: {e}\")")
    lines.append("            return False")
    lines.append("        finally:")
    lines.append("            cursor.close()")
    lines.append("            conn.close()")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"✅ 生成 DAO：{file_path}")

def generate_all(table_name, force_dao=False):
    generate_model(table_name)
    generate_dao(table_name, force=force_dao)

if __name__ == '__main__':
    generate_all('user')