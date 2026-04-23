from common import response
from model.User import User
from dao.UserDao import UserDao
from common import auth
user_dao = UserDao()
def register_user(user):
    user_info = user_dao.find_by_username(user.get_username())
    if( user_info!=None ):return response.error(msg="账号已存在")
    else:
        return response.success(msg="注册成功") if user_dao.save(user) else response.error()


def login_user(username: str, password: str):
    user_info = user_dao.find_by_username(username)
    if user_info is None:
        return response.error(msg="账号不存在")
    if user_info.get_password() != password:
        return response.error(msg="密码错误")
    token_data = {
        "sub": user_info.get_username(),
        "user_id": user_info.get_id(),
        "is_superuser": user_info.get_is_superuser() or False
    }
    token = auth.create_access_token(token_data)
    user_data = {
        "id": user_info.get_id(),
        "username": user_info.get_username(),
        "email": user_info.get_email(),
        "avatar": user_info.get_avatar(),
        "is_superuser": user_info.get_is_superuser()
    }
    return response.success(msg="登录成功", data={
        "token": token,
        "user": user_data
    })