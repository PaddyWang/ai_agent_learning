from __future__ import annotations

import redis

# 学习阶段先用本地 Redis
REDIS_URL = "redis://localhost:6379/0"

# decode_responses=True 可以直接拿到 str，而不是 bytes
redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
)
