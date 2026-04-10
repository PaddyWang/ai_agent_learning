from __future__ import annotations

import asyncio

from app.db import AsyncSessionLocal
from app.models import ChatSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload


async def check_seed_data() -> None:
    async with AsyncSessionLocal() as db:
        try:
            stmt = (
                select(ChatSession)
                .options(
                    selectinload(ChatSession.messages),
                    selectinload(ChatSession.tasks),
                )
                .order_by(ChatSession.id.desc())
            )
            result = await db.execute(stmt)
            session = result.scalars().first()

            if not session:
                print("no session found")
                return

            print(">" * 50)
            print("session:", session.id, session.title, session.user_id)
            print("messages:", len(session.messages))
            print("tasks:", len(session.tasks))
            # 新增打印 metadata_json
            print("session_metadata:", session.metadata_json)

            for message in session.messages:
                print("message:", message.id, message.role, message.content)

            for task in session.tasks:
                print("task:", task.id, task.task_type, task.status)

        finally:
            db.close()


if __name__ == "__main__":
    asyncio.run(check_seed_data())
