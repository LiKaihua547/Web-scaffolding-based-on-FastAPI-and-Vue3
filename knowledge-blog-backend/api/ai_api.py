# api/ai_api.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import subprocess
import os
import httpx
import asyncio
from config.config import OLLAMA_CONFIG
from common import response
from services import ai_service


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = None


router = APIRouter(prefix="/ai", tags=["AI"])

async def is_ollama_online():
    """网络层面检测 Ollama 接口是否存活"""
    try:
        async with httpx.AsyncClient(proxies=None, trust_env=False) as client:
            resp = await client.get(f"{OLLAMA_CONFIG['base_url']}/api/tags", timeout=1.0)
            return resp.status_code == 200
    except:
        return False

def is_ollama_process_running():
    """系统进程层面检测 Windows 任务管理器中是否有 ollama.exe"""
    try:
        # 使用 tasklist 查找进程，忽略命令行弹窗
        output = subprocess.check_output(
            'tasklist /FI "IMAGENAME eq ollama.exe"',
            shell=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        ).decode('gbk', errors='ignore')
        return "ollama.exe" in output.lower()
    except:
        return False

async def warmup_model():
    """发送一条测试信息，将模型提前加载到显存/内存中"""
    try:
        async with httpx.AsyncClient(proxies=None, trust_env=False, timeout=30.0) as client:
            test_payload = {
                "model": OLLAMA_CONFIG["default_model"],
                "messages": [{"role": "user", "content": "hi"}],
                "stream": False
            }
            resp = await client.post(f"{OLLAMA_CONFIG['base_url']}/api/chat", json=test_payload)
            return resp.status_code == 200
    except Exception:
        return False

@router.get("/start")
async def start_ollama_service():
    # 记得确保 config 里的 base_url 是 http://127.0.0.1:11434
    bin_dir = OLLAMA_CONFIG["bin_dir"]
    exe_path = os.path.join(bin_dir, "ollama.exe")

    # ================= 1. 第一重判断：直接拿来用 =================
    if await is_ollama_online():
        # 如果已经在线，直接唤醒模型预热
        await warmup_model()
        return response.success(msg="检测到后台已有 Ollama 运行，已直接连接并就绪！")

    # ================= 2. 第二重判断：清理卡死的僵尸进程 =================
    if is_ollama_process_running():
        # 走到这里说明：进程存在，但接口调不通（卡死了或者占错了端口）
        # 果断杀掉进程，防止占用 11434 端口
        os.system('taskkill /F /IM ollama.exe')
        await asyncio.sleep(1) # 等待操作系统释放端口

    # ================= 3. 全新启动服务 =================
    try:
        subprocess.Popen(
            [exe_path, "serve"],
            cwd=bin_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception as e:
        return response.error(msg=f"引擎程序启动失败: {str(e)}")

    # ================= 4. 轮询等待接口上线 =================
    max_retries = 15
    for i in range(max_retries):
        await asyncio.sleep(1)
        if await is_ollama_online():
            break
        if i == max_retries - 1:
            return response.error(msg="服务启动超时，可能是由于权限或端口冲突导致")

    # ================= 5. 模型预热 =================
    if await warmup_model():
        return response.success(msg="AI 引擎已全新唤醒，模型已就绪！")
    else:
        return response.error(msg="引擎已启动，但模型预热失败，请确保已下载 qwen2:latest")
@router.get("/status")
async def check_ollama_status():
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{OLLAMA_CONFIG['base_url']}/api/tags", timeout=2.0)
            if resp.status_code == 200:
                return {"status": "running", "models": resp.json().get("models", [])}
            else:
                return {"status": "not running"}
    except Exception:
        return {"status": "not running"}


# ==================== 新增的对话接口 ====================
@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        # 将 Pydantic 对象转换为字典列表，适配 Ollama 接口格式
        messages_dict = [{"role": msg.role, "content": msg.content} for msg in req.messages]

        # 调用 service 层获取回复
        reply = await ai_service.generate_chat_response(messages_dict, req.model)

        return response.success(data={"reply": reply})
    except Exception as e:
        return response.error(msg=str(e))