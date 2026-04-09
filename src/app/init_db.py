# 关键点：
# Base.metadata 会收集所有继承 Base 的 ORM 模型。
# 但前提是这些模型文件已经被 import 进来了。
import app.models  # noqa: F401
from app.db import Base, engine


def init_db() -> None:
    """
    创建所有表。

    学习阶段先用 create_all()，
    后面再切到 Alembic 管理迁移。
    """
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
