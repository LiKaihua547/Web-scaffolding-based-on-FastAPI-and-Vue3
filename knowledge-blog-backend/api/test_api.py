from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
async def test_get():
    return {"msg": "GET 请求测试成功", "data": [1, 2, 3]}