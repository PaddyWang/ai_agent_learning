from __future__ import annotations

from app.db import SessionLocal
from app.models import ChatSession, Message, Task
from sqlalchemy.orm import Session


def seed_demo_data() -> None:
    """
    插入一组最小演示数据，用来验证三张表和关系是否正常。
    """
    db: Session = SessionLocal()

    try:
        # 1. 先创建会话
        chat_session = ChatSession(
            user_id="user_demo_user",
            title="Demo Session",
            status="active",
        )
        db.add(chat_session)
        # flush 的作用：
        # 先把 INSERT 发出去，但还不提交事务。
        # 这样 chat_session.id 会被数据库生成出来，
        # 后面 Message / Task 就能引用这个 session_id。
        db.flush()

        # 2. 创建一条消息
        message = Message(
            session_id=chat_session.id,
            role="user",
            content="你好，帮我规划一个杭州 3 天旅行。",
            model="default",
            sequence=1,
        )
        db.add(message)

        # 3. 创建一个任务
        task = Task(
            session_id=chat_session.id,
            task_type="planning",
            status="padding",
            input_text="destination=杭州, days=3",
            output_text=None,
        )
        db.add(task)

        # 4. 提交事务
        db.commit()

        print("seed success")
        print(f"session_id={chat_session.id}")
        print(f"message_id={message.id}")
        print(f"task_id={task.id}")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
