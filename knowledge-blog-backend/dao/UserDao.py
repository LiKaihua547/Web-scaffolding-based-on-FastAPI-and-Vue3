# dao/UserDao.py
# 自动生成的 DAO 类，对应表：user

from database.connection import get_db_connection
from model.User import User

class UserDao:
    """user 表数据访问对象"""

    def _row_to_obj(self, row, columns):
        data = {col: row[i] for i, col in enumerate(columns)}
        return User.model_validate(data)

    def find_by_id(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM user WHERE id = %s", (id,))
            row = cursor.fetchone()
            if not row:
                return None
            columns = [col[0] for col in cursor.description]
            return self._row_to_obj(row, columns)
        finally:
            cursor.close()
            conn.close()

    def find_by_username(self, username):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            row = cursor.fetchone()
            if not row:
                return None
            columns = [col[0] for col in cursor.description]
            return self._row_to_obj(row, columns)
        finally:
            cursor.close()
            conn.close()
    def find_all(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM user")
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [self._row_to_obj(row, columns) for row in rows]
        finally:
            cursor.close()
            conn.close()

    def save(self, obj: User):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO user (username, password, email, phone, avatar, address, nickname, bio, is_active, is_superuser, last_login, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (obj.get_username(), obj.get_password(), obj.get_email(), obj.get_phone(), obj.get_avatar(), obj.get_address(), obj.get_nickname(), obj.get_bio(), obj.get_is_active(), obj.get_is_superuser(), obj.get_last_login(), obj.get_created_at(), obj.get_updated_at()))
            conn.commit()
            return True
        except Exception as e:
            print(f"插入失败: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def update(self, obj: User):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            sql = "UPDATE user SET username = %s, password = %s, email = %s, phone = %s, avatar = %s, address = %s, nickname = %s, bio = %s, is_active = %s, is_superuser = %s, last_login = %s, created_at = %s, updated_at = %s WHERE id = %s"
            cursor.execute(sql, (obj.get_username(), obj.get_password(), obj.get_email(), obj.get_phone(), obj.get_avatar(), obj.get_address(), obj.get_nickname(), obj.get_bio(), obj.get_is_active(), obj.get_is_superuser(), obj.get_last_login(), obj.get_created_at(), obj.get_updated_at(), obj.get_id()))
            conn.commit()
            return True
        except Exception as e:
            print(f"更新失败: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_by_id(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM user WHERE id = %s", (id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"删除失败: {e}")
            return False
        finally:
            cursor.close()
            conn.close()