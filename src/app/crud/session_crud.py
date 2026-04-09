from __future__ import annotations

from app.models import ChatSession, Message, Task
from sqlalchemy import select
from sqlalchemy.orm import Session


def create_chat_session(
    db: Session,
    *,
    user_id: str,
    title: str = "New Chat",
    status: str = "active",
) -> ChatSession:
    """
    创建一个新的聊天会话。

    流程：
    1. 创建 ORM 对象
    2. add 到 Session
    3. commit 提交事务
    4. refresh 拿到数据库里的最终状态
    """
    chat_session = ChatSession(
        user_id=user_id,
        title=title,
        status=status,
    )
    db.add(chat_session)
    db.commit()
    db.refresh(chat_session)
    return chat_session


def get_chat_session_by_id(db: Session, session_id: int) -> ChatSession | None:
    """
    按主键查询会话。

    db.get() 适合主键查询，写法最直接。
    """
    return db.get(ChatSession, session_id)


def list_chat_sessions_by_user(db: Session, user_id: str) -> list[ChatSession]:
    """
    查询某个用户的所有会话。
    """
    stmt = (
        select(ChatSession)
        .where(ChatSession.user_id == user_id)
        .order_by(ChatSession.id.desc())
    )
    return list(db.execute(stmt).scalars().all())


def update_chat_session_title(
    db: Session,
    *,
    session_id: int,
    title: str,
) -> ChatSession | None:
    """
    更新会话标题。
    """
    chat_session = db.get(ChatSession, session_id)
    if chat_session is None:
        return None

    chat_session.title = title
    db.commit()
    db.refresh(chat_session)
    return chat_session


def create_message(
    db: Session,
    *,
    session_id: int,
    role: str,
    content: str,
    model: str | None = None,
    sequence: int = 0,
) -> Message:
    """
    为某个会话创建一条消息。
    """
    message = Message(
        session_id=session_id,
        role=role,
        content=content,
        model=model,
        sequence=sequence,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def list_messages_by_session(
    db: Session,
    session_id: int,
) -> list[Message]:
    """
    查询某个会话下的所有消息。
    """
    stmt = (
        select(Message)
        .where(Message.session_id == session_id)
        .order_by(Message.sequence.asc(), Message.id.asc())
    )
    return list(db.execute(stmt).scalars().all())


def create_task(
    db: Session,
    *,
    session_id: int,
    task_type: str,
    status: str = "pending",
    input_text: str | None = None,
    output_text: str | None = None,
) -> Task:
    """
    为某个会话创建一个任务。
    """
    task = Task(
        session_id=session_id,
        task_type=task_type,
        status=status,
        input_text=input_text,
        output_text=output_text,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks_by_session(
    db: Session,
    session_id: int,
) -> list[Task]:
    """
    查询某个会话下的所有任务。
    """
    stmt = select(Task).where(Task.session_id == session_id).order_by(Task.id.asc())
    return list(db.execute(stmt).scalars().all())


def get_session_detail(
    db: Session,
    session_id: int,
) -> ChatSession | None:
    """
    获取某个会话详情。

    这里先返回 ChatSession ORM 对象本身。
    因为模型里已经声明了 relationship，
    所以后面可以通过 session.messages / session.tasks 继续访问关联数据。
    """
    return db.get(ChatSession, session_id)
