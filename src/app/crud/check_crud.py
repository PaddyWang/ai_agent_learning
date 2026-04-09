from app.crud.session_crud import (
    create_chat_session,
    create_message,
    create_task,
    get_session_detail,
)
from app.db import SessionLocal
from sqlalchemy.orm import Session


def check_crud() -> None:
    """
    验证今天写的 CRUD 是否正常工作。
    """
    db: Session = SessionLocal()

    try:
        # 1. 创建会话
        session = create_chat_session(
            db,
            user_id="user_demo_user",
            title="杭州旅游规划",
        )

        # 2. 创建消息
        create_message(
            db,
            session_id=session.id,
            role="user",
            content="帮我规划一个杭州三日游",
            model="default",
            sequence=1,
        )
        create_message(
            db,
            session_id=session.id,
            role="assistant",
            content="好的，我先帮你确认预算和出行时间",
            model="default",
            sequence=2,
        )

        # 3. 创建任务
        create_task(
            db,
            session_id=session.id,
            task_type="planning",
            status="pending",
            input_text="destination=杭州, days=3",
        )

        # 4. 查详情
        saved = get_session_detail(db, session_id=session.id)
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
    check_crud()
