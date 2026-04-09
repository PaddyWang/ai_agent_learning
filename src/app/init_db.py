from __future__ import annotations

import asyncio

import app.models  # noqa: F401

from .db import Base, async_engine


async def init_db() -> None:
    """
    异步建表。

    create_all() 本身是同步风格 API，
    所以在 AsyncEngine 下需要通过 run_sync() 包一层。
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
