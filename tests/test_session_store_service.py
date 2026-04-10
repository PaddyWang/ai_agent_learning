from app.services.session_store_service import (
    build_chat_runtime_key,
    delete_chat_runtime_state,
    get_chat_runtime_state,
    save_chat_runtime_state,
)


def test_build_chat_runtime_key() -> None:
    assert build_chat_runtime_key(123) == "chat:runtime:123"


def test_chat_runtime_state_set_get_delete() -> None:
    session_id = 123
    payload = {
        "last_message": "你好",
        "model": "default",
        "stream": True,
    }

    save_chat_runtime_state(session_id, payload, ttl=120)
    assert get_chat_runtime_state(session_id) == payload

    delete_chat_runtime_state(session_id)
    assert get_chat_runtime_state(session_id) is None
