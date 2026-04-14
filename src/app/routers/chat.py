import json
from collections.abc import AsyncGenerator

from app.deps import get_current_user
from app.llm.types import LLMResponse
from app.schemas import ChatRequest, ChatResponse
from app.services.llm_gateway import LLMGateway
from app.services.logging_service import format_access_log, write_access_log
from app.services.rate_limit_service import check_simple_rate_limit
from app.services.session_store_service import save_chat_runtime_state
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/chat", tags=["chat"])


def build_chat_instructions() -> str:
    return (
        "你是一个专业、简洁的中文 AI 助手。"
        "请优先直接回答用户问题，必要时再补充说明。"
    )


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

    user_id = current_user["user_id"]

    # 新增：限流
    allowed, current_count = check_simple_rate_limit(
        user_id=user_id,
        route="chat",
        limit=10,
        window_seconds=60,
    )
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"rate limit exceeded, current_count={current_count}",
        )

    session_id = payload.session_id or f"session_{current_user['user_id']}"

    # 新增：保存运行时状态
    save_chat_runtime_state(
        session_id=0 if isinstance(session_id, str) else session_id,
        data={
            "last_message": payload.message,
            "model": payload.model,
            "stream": payload.stream,
        },
        ttl=1800,
    )

    log_line = format_access_log(
        path=str(request.url.path),
        method=request.method,
        user_id=current_user["user_id"],
        request_id=getattr(request.state, "request_id", None),
    )
    background_tasks.add_task(write_access_log, log_line)

    gateway = LLMGateway()
    llm_response: LLMResponse = await gateway.generate(
        prompt=payload.message,
        instructions=build_chat_instructions(),
        model=payload.model if payload.model != "default" else None,
    )

    return ChatResponse(
        session_id=session_id,
        answer=llm_response.text,
        model=llm_response.model,
    )


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
    user_id = current_user["user_id"]

    # 新增：限流
    allowed, current_count = check_simple_rate_limit(
        user_id=user_id,
        route="chat_stream",
        limit=20,
        window_seconds=60,
    )
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"rate limit exceeded, current_count={current_count}",
        )

    session_id = payload.session_id or f"session_{current_user['user_id']}"

    # 新增：保存运行时状态
    save_chat_runtime_state(
        session_id=0 if isinstance(session_id, str) else session_id,
        data={
            "last_message": payload.message,
            "model": payload.model,
            "stream": True,
        },
        ttl=1800,
    )

    gateway = LLMGateway()

    async def llm_stream() -> AsyncGenerator[str, None]:
        index = 0
        response_model = payload.model

        async for chunk in gateway.stream(
            prompt=payload.message,
            instructions=build_chat_instructions(),
            model=response_model if response_model != "default" else None,
        ):
            index += 1
            sse_payload = {
                "type": "chunk",
                "index": index,
                "session_id": session_id,
                "model": response_model,
                "content": chunk,
            }
            yield f"data: {json.dumps(sse_payload, ensure_ascii=False)}\n\n"

        done_payload = {
            "type": "done",
            "session_id": session_id,
            "model": response_model,
        }
        yield f"data: {json.dumps(done_payload, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        llm_stream(),
        media_type="text/event-stream",
        headers={
            # 告诉客户端这是一条持续流，不要缓存
            "Cache-Control": "no-cache",
            # 某些代理层会缓冲响应，学习阶段先显式关掉
            "X-Accel-Buffering": "no",
        },
    )
