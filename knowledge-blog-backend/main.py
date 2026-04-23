from fastapi import FastAPI
from api import api_router
from fastapi.middleware.cors import CORSMiddleware
from common.exceptions import register_exception_handlers
app = FastAPI()
register_exception_handlers(app)
app.include_router(api_router, prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],      # 允许所有 HTTP 方法，包括 OPTIONS
    allow_headers=["*"],      # 允许所有请求头
)