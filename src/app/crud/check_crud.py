from __future__ import annotations

import asyncio

from app.crud.session_crud import (
    create_chat_session,
    create_message,
    create_task,
)
from app.db import AsyncSessionLocal
from app.models import ChatSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload


async def check_crud() -> None:
    """
    验证今天写的 CRUD 是否正常工作。
    """
    async with AsyncSessionLocal() as db:
        try:
            # 1. 创建会话
            session = await create_chat_session(
                db,
                user_id="user_demo_user",
                title="杭州旅游规划",
            )

            # 2. 创建消息
            await create_message(
                db,
                session_id=session.id,
                role="user",
                content="帮我规划一个杭州三日游",
                model="default",
                sequence=1,
                metadata_json={"source": "check_crud"},
            )
            await create_message(
                db,
                session_id=session.id,
                role="assistant",
                content="好的，我先帮你确认预算和出行时间",
                model="default",
                sequence=2,
                metadata_json={"source": "check_crud"},
            )

            # 3. 创建任务
            await create_task(
                db,
                session_id=session.id,
                task_type="planning",
                status="pending",
                input_text="destination=杭州, days=3",
                metadata_json={"trace_id": "trace_check_crud"},
            )

            # 4. 查详情
            # saved = get_session_detail(db, session_id=session.id)
            stmt = (
                select(ChatSession)
                .options(
                    selectinload(ChatSession.messages),
                    selectinload(ChatSession.tasks),
                )
                .where(ChatSession.id == session.id)
            )
            result = await db.execute(stmt)
            saved = result.scalars().first()

            assert saved is not None

            print("session:", saved.id, saved.title, saved.user_id)
            print("messages:", len(saved.messages))
            print("tasks:", len(saved.tasks))

            for item in saved.messages:
                print("message:", item.sequence, item.role, item.content)

            for item in saved.tasks:
                print("task:", item.id, item.task_type, item.status)

        finally:
            db.close()


if __name__ == "__main__":
    asyncio.run(check_crud())
