from __future__ import annotations

import asyncio

from app.crud.session_crud import (
    create_chat_session,
    create_message,
    create_task,
    list_messages_by_session,
    list_tasks_by_session,
)
from app.db import AsyncSessionLocal


async def check_async_crud() -> None:
    """
    验证 AsyncSession 版 CRUD 是否正常工作。
    """
    async with AsyncSessionLocal() as db:
        session = await create_chat_session(
            db,
            user_id="user_demo_user",
            title="Async Chat",
        )

        await create_message(
            db,
            session_id=session.id,
            role="user",
            content="帮我规划一个杭州三日游",
            model="default",
            sequence=1,
        )

        await create_task(
            db,
            session_id=session.id,
            task_type="planning",
            status="pending",
            input_text="destination=杭州, days=3",
        )

        messages = await list_messages_by_session(db, session.id)
        tasks = await list_tasks_by_session(db, session.id)

        print("session:", session.id, session.title)
        print("messages:", len(messages))
        print("tasks:", len(tasks))


if __name__ == "__main__":
    asyncio.run(check_async_crud())
