from __future__ import annotations

from app.models import ChatSession, Message, Task
from app.services.cache_service import delete_session_list_cache
from services.cache_service import get_session_list_cache, set_session_list_cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_chat_session(
    db: AsyncSession,
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
    await db.commit()
    await db.refresh(chat_session)

    # 新增：会话列表缓存失效
    delete_session_list_cache(user_id)

    return chat_session


async def get_chat_session_by_id(
    db: AsyncSession,
    session_id: int,
) -> ChatSession | None:
    """
    按主键查询会话。

    db.get() 适合主键查询，写法最直接。
    """
    return await db.get(ChatSession, session_id)


async def list_chat_sessions_by_user(
    db: AsyncSession,
    user_id: str,
) -> list[ChatSession]:
    """
    查询某个用户的所有会话。
    """
    # 新增：先查缓存
    cached = get_session_list_cache(user_id)
    if cached is not None:
        # 这里你后续可以决定是否直接返回 dict 结构
        # 学习阶段先保留“这里只展示改动点”
        pass

    stmt = (
        select(ChatSession)
        .where(ChatSession.user_id == user_id)
        .order_by(ChatSession.id.desc())
    )
    result = await db.execute(stmt)
    sessions = list(result.scalars().all())

    # 新增：写缓存
    cache_payload = [
        {
            "id": item.id,
            "user_id": item.user_id,
            "title": item.title,
            "status": item.status,
        }
        for item in sessions
    ]
    set_session_list_cache(user_id, cache_payload, ttl=300)

    return sessions


async def update_chat_session_title(
    db: AsyncSession,
    *,
    session_id: int,
    title: str,
) -> ChatSession | None:
    """
    更新会话标题。
    """
    # 原来：
    # chat_session = db.get(ChatSession, session_id)
    # 改成：
    chat_session = await db.get(ChatSession, session_id)
    if chat_session is None:
        return None

    chat_session.title = title
    await db.commit()
    await db.refresh(chat_session)

    # 新增：会话列表缓存失效
    delete_session_list_cache(chat_session.user_id)

    return chat_session


async def create_message(
    db: AsyncSession,
    *,
    session_id: int,
    role: str,
    content: str,
    model: str | None = None,
    sequence: int = 0,
    # 新增
    metadata_json: dict | None = None,
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
        # 新增
        metadata_json=metadata_json,
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


async def list_messages_by_session(
    db: AsyncSession,
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
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_task(
    db: AsyncSession,
    *,
    session_id: int,
    task_type: str,
    status: str = "pending",
    input_text: str | None = None,
    output_text: str | None = None,
    # 新增
    metadata_json: dict | None = None,
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
        # 新增
        metadata_json=metadata_json,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def list_tasks_by_session(
    db: AsyncSession,
    session_id: int,
) -> list[Task]:
    """
    查询某个会话下的所有任务。
    """
    stmt = select(Task).where(Task.session_id == session_id).order_by(Task.id.asc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_session_detail(
    db: AsyncSession,
    session_id: int,
) -> ChatSession | None:
    """
    获取某个会话详情。

    这里先返回 ChatSession ORM 对象本身。
    因为模型里已经声明了 relationship，
    所以后面可以通过 session.messages / session.tasks 继续访问关联数据。
    """
    return await db.get(ChatSession, session_id)
