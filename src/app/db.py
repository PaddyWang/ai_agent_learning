from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 学习阶段先用 SQLite，阻力最小。
# 等你 Day 10 / Day 11 再切 PostgreSQL 和 Alembic，会更顺。
DATABASE_URL = "sqlite:///./app.db"


class Base(DeclarativeBase):
    """
    所有 ORM 模型的共同父类。

    作用：
    1. 让 SQLAlchemy 知道哪些类是 ORM 模型
    2. 统一收集 metadata
    3. 后面可以通过 Base.metadata.create_all() 一次性建表
    """

    pass


# Engine 是 SQLAlchemy 和数据库之间的总入口。
# echo=True 适合学习期打开，你能直接看到 SQLAlchemy 发出的 SQL。
engine = create_engine(
    DATABASE_URL,
    echo=True,
)


# SessionLocal 是一个“会话工厂”，不是数据库表里的 session。
# 后面每次需要数据库会话时，都从这里拿一个 Session 实例。
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
