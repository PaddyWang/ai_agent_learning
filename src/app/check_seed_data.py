from app.db import SessionLocal
from app.models import ChatSession
from sqlalchemy import select
from sqlalchemy.orm import Session


def check_seed_data() -> None:
    db: Session = SessionLocal()

    try:
        stmt = select(ChatSession).order_by(ChatSession.id.desc())
        session = db.execute(stmt).scalars().first()

        if not session:
            print("no session found")
            return

        print(">" * 50)
        print("session:", session.id, session.title, session.user_id)
        print("messages:", len(session.messages))
        print("tasks:", len(session.tasks))

        for message in session.messages:
            print("message:", message.id, message.role, message.content)

        for task in session.tasks:
            print("task:", task.id, task.task_type, task.status)

    finally:
        db.close()


if __name__ == "__main__":
    check_seed_data()
