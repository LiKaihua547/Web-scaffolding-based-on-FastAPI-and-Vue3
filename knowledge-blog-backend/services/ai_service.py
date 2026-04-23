# service/ai_service.py
import httpx
from config.config import OLLAMA_CONFIG
from common import response

async def generate_chat_response(messages: list, model: str = None) -> str:
    """
    调用 Ollama 的 Chat 接口生成回复
    :param messages: 消息列表，格式为 [{"role": "user", "content": "你好"}]
    :param model: 模型名称，默认使用配置中的 default_model
    :return: AI 的回复文本
    """
    url = f"{OLLAMA_CONFIG['base_url']}/api/chat"
    payload = {
        "model": model or OLLAMA_CONFIG["default_model"],
        "messages": messages,
        "stream": False  # 设置为 False 代表等待 AI 生成完毕后一次性返回。如果需要打字机效果，这里要改为 True 并使用 StreamingResponse
    }

    async with httpx.AsyncClient(timeout=OLLAMA_CONFIG["timeout"]) as client:
        try:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()  # 检查 HTTP 状态码

            data = resp.json()
            data_content = data.get("message", {}).get("content", "")
            print('回复内容',data_content)
            # Ollama 返回的结构中，回复内容在 data["message"]["content"]
            return response.success(data=data_content)

        except httpx.TimeoutException:
            raise Exception("AI 思考超时，请稍后再试")
        except Exception as e:
            raise Exception(f"调用 Ollama 失败: {str(e)}")