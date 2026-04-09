from __future__ import annotations

from datetime import UTC, datetime

from app.db import Base
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ChatSession(Base):
    """
    会话表。

    注意：
    ORM 类名故意不用 Session，
    因为那会和 sqlalchemy.orm.Session 重名，后面很容易混淆。
    """

    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # 当前会话属于哪个用户。
    # 现在先存字符串，后面接真实用户表再升级成外键。
    user_id: Mapped[str] = mapped_column(String(64), index=True)

    # 会话标题，后面你可以做“自动会话命名”
    title: Mapped[str] = mapped_column(String(200), default="New Chat")

    # 会话状态：active / archived / deleted
    status: Mapped[str] = mapped_column(String(20), default="active")

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    update_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    # 一个会话对应多条消息
    messages: Mapped[list[Message]] = relationship(back_populates="session")

    # 一个会话对应多个任务
    tasks: Mapped[list[Task]] = relationship(back_populates="session")


class Message(Base):
    """
    消息表。

    用来存用户消息、助手回复、系统提示等。
    """

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # 外键指向 sessions.id
    session_id: Mapped[str] = mapped_column(ForeignKey("sessions.id"), index=True)

    # user / assistant / system
    role: Mapped[str] = mapped_column(String(20))

    # 消息正文
    content: Mapped[str] = mapped_column(Text)

    # 可选：记录模型名，后面接真实 LLM 时会用到
    model: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # 可选：记录消息顺序
    sequence: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    # 反向关系：每条消息属于一个会话
    session: Mapped[ChatSession] = relationship(back_populates="messages")


class Task(Base):
    """
    任务表。

    这里的任务可以理解为：
    一次智能体执行过程中的子任务、后台任务、工具调用任务。
    后面做 Agent / 工作流 / 任务状态跟踪时会非常有用。
    """

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    session_id: Mapped[str] = mapped_column(ForeignKey("sessions.id"), index=True)

    # 比如 summary / retrieval / planning / tool_call
    task_type: Mapped[str] = mapped_column(String(50))

    # pending / running / success / failed
    status: Mapped[str] = mapped_column(String(20), default="pending")

    # 简单记录输入和输出，学习期先用文本
    input_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    output_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    update_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    session: Mapped[ChatSession] = relationship(back_populates="tasks")
