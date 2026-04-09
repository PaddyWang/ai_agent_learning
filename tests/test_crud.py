from __future__ import annotations

from app.crud.session_crud import (
    create_chat_session,
    create_message,
    create_task,
    get_chat_session_by_id,
    get_session_detail,
    list_chat_sessions_by_user,
    list_messages_by_session,
    list_tasks_by_session,
    update_chat_session_title,
)
from app.db import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def make_test_db(tmp_path):
    """
    创建一个临时 SQLite 数据库。

    每个测试都用独立数据库，
    这样测试之间不会互相污染。
    """
    db_file = tmp_path / "test_crud.db"
    engine = create_engine(f"sqlite:///{db_file}", echo=False)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal


def test_create_and_get_chat_session(tmp_path) -> None:
    TestingSessionLocal = make_test_db(tmp_path)
    db: Session = TestingSessionLocal()

    try:
        chat_session = create_chat_session(
            db,
            user_id="user_001",
            title="My First Chat",
        )

        saved = get_chat_session_by_id(db, chat_session.id)

        assert saved is not None
        assert saved.user_id == "user_001"
        assert saved.title == "My First Chat"
        assert saved.status == "active"

    finally:
        db.close()


def test_list_chat_sessions_by_user(tmp_path) -> None:
    TestingSessionLocal = make_test_db(tmp_path)
    db: Session = TestingSessionLocal()

    try:
        create_chat_session(db, user_id="user_001", title="Chat A")
        create_chat_session(db, user_id="user_001", title="Chat B")
        create_chat_session(db, user_id="user_002", title="Other User Chat")

        sessions = list_chat_sessions_by_user(db, user_id="user_001")

        assert len(sessions) == 2
        assert all(item.user_id == "user_001" for item in sessions)

    finally:
        db.close()


def test_update_chat_session_title(tmp_path) -> None:
    TestingSessionLocal = make_test_db(tmp_path)
    db: Session = TestingSessionLocal()

    try:
        chat_session = create_chat_session(db, user_id="user_001", title="Old Title")

        updated = update_chat_session_title(
            db, session_id=chat_session.id, title="New Title"
        )

        assert updated is not None
        assert updated.title == "New Title"

    finally:
        db.close()


def test_create_message_and_list_by_session(tmp_path) -> None:
    TestingSessionLocal = make_test_db(tmp_path)
    db: Session = TestingSessionLocal()

    try:
        chat_session = create_chat_session(db, user_id="user_001", title="Message Test")

        create_message(
            db,
            session_id=chat_session.id,
            role="user",
            content="第一条消息",
            model="default",
            sequence=1,
        )
        create_message(
            db,
            session_id=chat_session.id,
            role="assistant",
            content="第二条消息",
            model="default",
            sequence=2,
        )

        messages = list_messages_by_session(db, session_id=chat_session.id)
        assert len(messages) == 2
        assert messages[0].sequence == 1
        assert messages[0].role == "user"
        assert messages[1].sequence == 2
        assert messages[1].role == "assistant"

    finally:
        db.close()


def test_create_task_and_list_by_session(tmp_path) -> None:
    TestingSessionLocal = make_test_db(tmp_path)
    db: Session = TestingSessionLocal()

    try:
        chat_session = create_chat_session(db, user_id="user_001", title="Task Test")

        create_task(
            db,
            session_id=chat_session.id,
            task_type="retrieval",
            status="pending",
            input_text="query=杭州天气",
        )
        create_task(
            db,
            session_id=chat_session.id,
            task_type="planning",
            status="success",
            input_text="destination=杭州",
            output_text="生成完成",
        )
        tasks = list_tasks_by_session(db, session_id=chat_session.id)
        assert len(tasks) == 2
        assert tasks[0].task_type == "retrieval"
        assert tasks[1].task_type == "planning"

    finally:
        db.close()


def test_get_session_detail_with_relationships(tmp_path) -> None:
    TestingSessionLocal = make_test_db(tmp_path)
    db: Session = TestingSessionLocal()

    try:
        chat_session = create_chat_session(
            db,
            user_id="user_001",
            title="Detail Test",
        )
        create_message(
            db,
            session_id=chat_session.id,
            role="user",
            content="你好",
            model="default",
            sequence=1,
        )
        create_task(
            db,
            session_id=chat_session.id,
            task_type="summary",
            status="pending",
            input_text="hello",
        )

        detail = get_session_detail(db, session_id=chat_session.id)
        assert detail is not None
        assert detail.id == chat_session.id
        assert len(detail.messages) == 1
        assert len(detail.tasks) == 1
        assert detail.messages[0].content == "你好"
        assert detail.tasks[0].task_type == "summary"

    finally:
        db.close()
