from app.services.rate_limit_service import (
    build_rate_limit_key,
    check_simple_rate_limit,
)


def test_build_rate_limit_key() -> None:
    assert build_rate_limit_key("user_001", "chat") == "rate_list:chat:user_001"


def test_rate_limit_allows_within_threshold() -> None:
    user_id = "user_limit_ok"

    results = [
        check_simple_rate_limit(
            user_id=user_id,
            route="chat",
            limit=3,
            window_seconds=60,
        )
        for _ in range(3)
    ]

    assert results == [(True, 1), (True, 2), (True, 3)]


def test_rate_limit_blocks_after_threshold() -> None:
    user_id = "user_limit_block"

    first = check_simple_rate_limit(
        user_id=user_id,
        route="chat",
        limit=2,
        window_seconds=60,
    )
    second = check_simple_rate_limit(
        user_id=user_id,
        route="chat",
        limit=2,
        window_seconds=60,
    )
    third = check_simple_rate_limit(
        user_id=user_id,
        route="chat",
        limit=2,
        window_seconds=60,
    )

    assert first == (True, 1)
    assert second == (True, 2)
    assert third == (False, 3)
