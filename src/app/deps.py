from __future__ import annotations

from collections.abc import AsyncGenerator

from app.core.security import fake_decode_token
from app.db import AsyncSessionLocal
from fastapi import Depends, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

# 告诉 FastAPI：
# 以后如果某个依赖需要 token，
# 就从 Authorization: Bearer <token> 里取。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI 异步数据库依赖。

    这就是把 FastAPI 官方同步版 `yield session`
    改造成 AsyncSession 版的关键位置。
    """
    async with AsyncSessionLocal() as session:
        yield session


async def get_request_id(x_request_id: str | None = Header(default=None)) -> str:
    """
    从请求头中读取 request id。

    作用：
    1. 方便日志追踪
    2. 方便后面接 tracing / observability
    3. 如果调用方没传，就给一个默认值，避免接口逻辑里到处判空
    """
    return x_request_id or "req-demo-001"


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    解析 Bearer Token，得到当前用户。

    为什么特别适合做依赖：
    因为很多接口都需要“当前用户”，
    如果每个接口都自己解析 token，会非常重复。
    """
    return fake_decode_token(token)
