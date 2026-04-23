# model/User.py
# 自动生成的 Pydantic 模型类，对应表：user

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class User(BaseModel):
    """user 表模型"""

    id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    address: Optional[str] = None
    nickname: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[int] = None
    is_superuser: Optional[int] = None
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def get_id(self) -> Optional[int]:
        return self.id

    def set_id(self, value: Optional[int]):
        self.id = value

    def get_username(self) -> Optional[str]:
        return self.username

    def set_username(self, value: Optional[str]):
        self.username = value

    def get_password(self) -> Optional[str]:
        return self.password

    def set_password(self, value: Optional[str]):
        self.password = value

    def get_email(self) -> Optional[str]:
        return self.email

    def set_email(self, value: Optional[str]):
        self.email = value

    def get_phone(self) -> Optional[str]:
        return self.phone

    def set_phone(self, value: Optional[str]):
        self.phone = value

    def get_avatar(self) -> Optional[str]:
        return self.avatar

    def set_avatar(self, value: Optional[str]):
        self.avatar = value

    def get_address(self) -> Optional[str]:
        return self.address

    def set_address(self, value: Optional[str]):
        self.address = value

    def get_nickname(self) -> Optional[str]:
        return self.nickname

    def set_nickname(self, value: Optional[str]):
        self.nickname = value

    def get_bio(self) -> Optional[str]:
        return self.bio

    def set_bio(self, value: Optional[str]):
        self.bio = value

    def get_is_active(self) -> Optional[int]:
        return self.is_active

    def set_is_active(self, value: Optional[int]):
        self.is_active = value

    def get_is_superuser(self) -> Optional[int]:
        return self.is_superuser

    def set_is_superuser(self, value: Optional[int]):
        self.is_superuser = value

    def get_last_login(self) -> Optional[datetime]:
        return self.last_login

    def set_last_login(self, value: Optional[datetime]):
        self.last_login = value

    def get_created_at(self) -> Optional[datetime]:
        return self.created_at

    def set_created_at(self, value: Optional[datetime]):
        self.created_at = value

    def get_updated_at(self) -> Optional[datetime]:
        return self.updated_at

    def set_updated_at(self, value: Optional[datetime]):
        self.updated_at = value
