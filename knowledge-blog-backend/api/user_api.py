from fastapi import APIRouter
from pydantic import BaseModel
from services.user_service import register_user, login_user
from model.User import User

router = APIRouter()
user = User
class LoginReq(BaseModel):
    username: str
    password: str

@router.post("/register", response_model=None)
async def register(user: User):
    print(user.dict())  # 查看实际接收到的数据
    return register_user(user)


@router.post("/login",response_model=None)
async def login(req: LoginReq):
    return login_user(req.username,req.password)