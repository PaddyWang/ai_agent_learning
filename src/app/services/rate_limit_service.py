from __future__ import annotations

from app.core.redis_client import redis_client


def build_rate_limit_key(user_id: str, route: str) -> str:
    return f"rate_list:{route}:{user_id}"


def check_simple_rate_limit(
    user_id: str, route: str, limit: int = 10, window_seconds: int = 60
) -> tuple[bool, str]:
    """
    最简单的固定窗口限流。

    返回：
    - 是否允许请求
    - 当前计数
    """
    key = build_rate_limit_key(user_id, route)

    # 用 pipeline 把 incr 和 expire 放一起发，减少网络往返。
    pipe = redis_client.pipeline()
    pipe.incr(key)
    pipe.ttl(key)
    current_count, ttl = pipe.execute()

    # 如果这是第一次访问，补上过期时间
    if ttl == -1:
        redis_client.expire(key, window_seconds)

    allowed = current_count <= limit
    return allowed, current_count
