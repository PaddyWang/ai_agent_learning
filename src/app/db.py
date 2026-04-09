from __future__ import annotations

# from sqlalchemy import create_engine
# from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# 今天先继续用 SQLite，降低切换成本。
# 注意：异步版 SQLite URL 要带 aiosqlite 方言。
DATABASE_URL = "sqlite+aiosqlite:///./app.db"


class Base(DeclarativeBase):
    """
    所有 ORM 模型的共同父类。

    作用：
    1. 收集 metadata
    2. 让 SQLAlchemy 知道哪些类是 ORM 模型
    """

    pass


# 异步 Engine
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


# AsyncSession 工厂
# 官方文档推荐在 asyncio 场景下使用 expire_on_commit=False，
# 这样提交后对象属性不会立刻失效，后续访问更稳定。
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)
