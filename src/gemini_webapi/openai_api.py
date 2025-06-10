from fastapi import FastAPI, Request
from pydantic import BaseModel
from gemini_webapi.client import GeminiClient
from gemini_webapi.constants import Model
import asyncio
import os
import time
from fastapi.responses import StreamingResponse
import json

app = FastAPI()

# 多客户端支持
clients = []
client_status = []  # True=可用，False=故障
client_fail_count = []  # 记录每个客户端的失败次数
client_index = 0
access_tokens = []

@app.on_event("startup")
async def startup_event():
    global clients, client_status, client_fail_count,access_tokens
    psids = os.getenv("SECURE_1PSID", "").split(",")
    psidts = os.getenv("SECURE_1PSIDTS", "").split(",")
    access_tokens = os.getenv("access_token", "").split(",")
    clients = []
    client_status = []
    client_fail_count = []
    for psid, psidts_val,access_token in zip(psids, psidts,access_tokens):
        c = GeminiClient(psid.strip(), psidts_val.strip())
        await c.init()
        clients.append(c)
        client_status.append(True)
        client_fail_count.append(0)

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[Message]
    stream: bool = False
    temperature: float = 1.0
    top_p: float = 1.0
    n: int = 1
    max_tokens: int | None = None
    stop: list[str] | None = None
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    user: str | None = None

class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list[Choice]

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    prompt = "\n".join([f"{msg.role}: {msg.content}" for msg in request.messages]) if request.messages else ""
    global client_index
    tried = 0
    total = len(clients)
    last_exc = None
    while tried < total:
        idx = (client_index + tried) % total
        try:
            # 根据请求中的 model 字符串获取 Model 枚举
            model_enum = Model.from_name(request.model)
            # await clients[idx].init(access_token=access_tokens[idx].strip())

            response = await clients[idx].generate_content(prompt, model=model_enum)
            break
        except Exception as e:
            print(f"GeminiClient {idx} 错误: {e}")
            last_exc = e
            tried += 1
            clients[idx].init()
    else:
        raise RuntimeError(f"所有 GeminiClient 实例均不可用: {last_exc}")
    if request.stream:
        async def event_generator():
            data = {
                "id": "chatcmpl-xxx",
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": request.model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {"role": "assistant", "content": response.text},
                        "finish_reason": "stop"
                    }
                ]
            }
            yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(event_generator(), media_type="text/event-stream")
    else:
        return ChatCompletionResponse(
            id="chatcmpl-xxx",
            object="chat.completion",
            created=int(time.time()),
            model=request.model,
            choices=[
                Choice(
                    index=0,
                    message=Message(role="assistant", content=response.text),
                    finish_reason="stop"
                )
            ]
        )

@app.get("/v1/models")
async def list_models():
    # 过滤掉 UNSPECIFIED 和已废弃模型（名称含 deprecated 或 advanced）
    models = [
        m for m in Model
        if m != Model.UNSPECIFIED and not m.name.endswith("ADVANCED") and not m.name.startswith("G_2_0")
    ]
    return {
        "object": "list",
        "data": [
            {
                "id": m.model_name,
                "object": "model",
                "created": 0,
                "owned_by": "google",
                "permission": []
            } for m in models
        ]
    }
