from __future__ import annotations

import json
from typing import Any

from app.core.redis_client import redis_client


def build_session_cache_key(user_id: str) -> str:
    return f"session:list:{user_id}"


def set_session_list_cache(
    user_id: str, data: list[dict[str, Any]], ttl: int = 300
) -> None:
    """
    缓存某个用户的会话列表。
    ttl 默认 5 分钟。
    """
    key = build_session_cache_key(user_id)
    redis_client.set(key, json.dumps(data, ensure_ascii=False), ex=ttl)


def get_session_list_cache(user_id: str) -> list[dict[str, Any]] | None:
    """
    读取会话列表缓存。
    """
    key = build_session_cache_key(user_id)
    value = redis_client.get(key)
    if value is None:
        return None
    return json.loads(value)


def delete_session_list_cache(user_id: str) -> None:
    """
    当会话新增或修改时，主动删掉旧缓存。
    """
    key = build_session_cache_key(user_id)
    redis_client.delete(key)
