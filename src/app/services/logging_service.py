from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

LOG_FILE = Path("logs/app.log")


def write_access_log(line: str) -> None:
    """
    学习版日志写入函数。

    为什么用普通 def：
    这里主要是文件写入，先保持最简单。
    FastAPI 的 BackgroundTasks 可以处理普通 def。
    """
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with LOG_FILE.open(mode="a", encoding="utf-8") as f:
        f.write(line)


def format_access_log(
    *,
    path: str,
    method: str,
    user_id: str | None,
    request_id: str | None,
) -> str:
    """
    统一拼接日志内容，避免在路由里手写字符串。
    """
    now = datetime.now(UTC).isoformat()
    return (
        f"[{now}] method={method} path={path} "
        f"user_id={user_id or 'anonymous'} request_id={request_id or 'unknown'}\n"
    )
