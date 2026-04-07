import asyncio
import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.responses import StreamingResponse

from ..deps import get_current_user
from ..schemas import ChatRequest, ChatResponse
from ..services.logging_service import format_access_log, write_access_log

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
) -> ChatResponse:
    """
    受保护聊天接口。

    现在先做 echo，
    后面你接 LLM、RAG、Agent 时，这里就是主入口。
    """
    session_id = payload.session_id or f"session_{current_user['user_id']}"

    log_line = format_access_log(
        path=str(request.url.path),
        method=request.method,
        user_id=current_user["user_id"],
        request_id=getattr(request.state, "request_id", None),
    )
    background_tasks.add_task(write_access_log, log_line)

    return ChatResponse(
        session_id=session_id,
        answer=f"Echo: {payload.message}",
        model=payload.model,
    )


async def fake_stream_answer(
    message: str,
    session_id: str,
    model: str,
) -> AsyncGenerator[str, None]:
    """
    一个学习版的“假流式生成器”。

    它的目标不是模拟真实 LLM SDK，
    而是先把 SSE 协议和前后端交互跑通。

    每次 yield 一条符合 SSE 格式的消息：
    data: {...}\n\n
    """
    chunks = [
        "我正在理解你的问题。",
        "接下来我会给你一个初步回答。",
        f"你刚才说的是：{message}",
        "这是一个流式接口演示版本。",
    ]

    for index, chunk in enumerate(chunks, start=1):
        payload = {
            "type": "chunk",
            "index": index,
            "session_id": session_id,
            "model": model,
            "content": chunk,
        }

        # SSE 最常见格式：
        # data: <json string>\n\n
        yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"

        # 模拟 LLM 逐段吐内容的感觉
        await asyncio.sleep(0.3)

    done_payload = {
        "type": "done",
        "session_id": session_id,
        "model": model,
    }

    yield f"data: {json.dumps(done_payload, ensure_ascii=False)}\n\n"


@router.post("/stream")
async def chat_stream(
    payload: ChatRequest,
    current_user: dict = Depends(get_current_user),
) -> StreamingResponse:
    """
    流式聊天接口。

    关键点：
    1. 仍然复用 ChatRequest 做请求体验证
    2. 仍然要求当前用户已登录
    3. 返回值从普通 JSON 改成 StreamingResponse
    4. media_type 必须是 text/event-stream
    """
    session_id = payload.session_id or f"session_{current_user['user_id']}"
    generator = fake_stream_answer(
        message=payload.message,
        session_id=session_id,
        model=payload.model,
    )

    return StreamingResponse(
        generator,
        media_type="text/event-stream",
        headers={
            # 告诉客户端这是一条持续流，不要缓存
            "Cache-Control": "no-cache",
            # 某些代理层会缓冲响应，学习阶段先显式关掉
            "X-Accel-Buffering": "no",
        },
    )
