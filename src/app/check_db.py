from __future__ import annotations

import asyncio

from app.db import async_engine
from sqlalchemy import text


async def check_tables() -> None:
    """
    用最简单的 SQL 检查表是否真的建出来了。
    """
    async with async_engine.connect() as conn:
        result = await conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        )
        for row in result:
            print(row[0])


if __name__ == "__main__":
    asyncio.run(check_tables())
