import pytest
from app.schemas import ChatRequest, ChatResponse, UserCreate
from pydantic import ValidationError


def test_user_create_success() -> None:
    user = UserCreate(
        username="tom_123",
        email="tom@gmail.com",
        password="abc12345",
    )

    assert user.username == "tom_123"
    assert user.email == "tom@gmail.com"


def text_user_create_rejects_invalid_username() -> None:
    with pytest.raises(ValidationError):
        UserCreate(
            username="tom@123",
            email="tom@gmail.com",
            password="abc12345",
        )


def test_user_create_rejects_weak_password_letters_only() -> None:
    with pytest.raises(ValidationError):
        UserCreate(
            username="tom123",
            email="tom@gmail.com",
            password="abcdefg",
        )


def test_user_create_rejects_weak_password_digits_only() -> None:
    with pytest.raises(ValidationError):
        UserCreate(
            username="tom123",
            email="tom@gmail.com",
            password="12345678",
        )


def test_chat_request_success() -> None:
    payload = ChatRequest(
        message="请总计归纳一下这段内容",
        session_id="session_001",
        model="gpt-demo",
        temperature=0.5,
        stream=False,
    )

    assert payload.message == "请总计归纳一下这段内容"
    assert payload.session_id == "session_001"
    assert payload.temperature == 0.5


def test_chat_request_empty_session_id_becomes_none() -> None:
    payload = ChatRequest(
        message="你好",
        session_id="",
    )

    assert payload.session_id is None


def test_chat_request_rejects_blank_message() -> None:
    with pytest.raises(ValidationError):
        ChatRequest(message="   ")


def test_chat_response_rejects_blank_answer() -> None:
    with pytest.raises(ValidationError):
        ChatResponse(
            session_id="session_001",
            answer="   ",
            model="default",
        )


def test_chat_response_model_dump_excludes_none() -> None:
    response = ChatResponse(
        session_id="session_001",
        answer="你好，我可以帮你规划行程",
        model="default",
    )

    data = response.model_dump(exclude_none=True)

    assert data["session_id"] == "session_001"
    assert data["answer"] == "你好，我可以帮你规划行程"
    assert data["model"] == "default"
    assert "created_at" in data
