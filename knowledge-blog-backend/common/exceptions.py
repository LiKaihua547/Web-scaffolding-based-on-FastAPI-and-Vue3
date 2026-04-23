# common/exceptions.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from common.response import error

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # 可以在这里记录日志
        return JSONResponse(
            status_code=500,
            content=error(msg=f"服务器内部错误: {str(exc)}", code=500)
        )