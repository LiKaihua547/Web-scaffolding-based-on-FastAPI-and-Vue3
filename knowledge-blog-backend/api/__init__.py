import pkgutil
import importlib
from fastapi import APIRouter

api_router = APIRouter()

# 遍历当前包下的所有模块
for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
    if module_name.startswith("_"):   # 跳过 __init__ 自身
        continue
    module = importlib.import_module(f"api.{module_name}")
    if hasattr(module, "router"):
        api_router.include_router(module.router)