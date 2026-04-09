from app.db import engine
from sqlalchemy import text


def check_tables() -> None:
    """
    用最简单的 SQL 检查表是否真的建出来了。
    """
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        )
        for row in result:
            print(row[0])


if __name__ == "__main__":
    check_tables()
