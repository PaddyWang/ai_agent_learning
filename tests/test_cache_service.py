from app.services.cache_service import (
    build_session_cache_key,
    delete_session_list_cache,
    get_session_list_cache,
    set_session_list_cache,
)


def test_build_session_cache_key() -> None:
    assert build_session_cache_key("user_001") == "session:list:user_001"


def test_session_cache_set_get_delete() -> None:
    user_id = "user_cache_test"
    payload = [
        {"id": 1, "title": "Chat A"},
        {"id": 2, "title": "Chat B"},
    ]

    set_session_list_cache(user_id, payload, ttl=300)
    assert get_session_list_cache(user_id) == payload

    delete_session_list_cache(user_id)
    assert get_session_list_cache(user_id) is None
