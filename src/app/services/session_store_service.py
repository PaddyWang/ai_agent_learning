from __future__ import annotations

import json
from typing import Any

from app.core.redis_client import redis_client


def build_chat_runtime_key(session_id: int) -> str:
    return f"chat:runtime:{session_id}"


def save_chat_runtime_state(
    session_id: int, data: dict[str, Any], ttl: int = 1800
) -> None:
    """
    保存会话运行时状态，比如：
    - 当前正在生成什么
    - 临时上下文
    - 前端选中的模式
    """
    key = build_chat_runtime_key(session_id)
    redis_client.set(key, json.dumps(data, ensure_ascii=False), ex=ttl)


def get_chat_runtime_state(session_id: int) -> dict[str, Any] | None:
    key = build_chat_runtime_key(session_id)
    value = redis_client.get(key)
    if value is None:
        return None
    return json.loads(value)


def delete_chat_runtime_state(session_id: int) -> None:
    key = build_chat_runtime_key(session_id)
    redis_client.delete(key)
