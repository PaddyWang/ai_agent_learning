from fastapi.testclient import TestClient


def test_redis_check_success(client: TestClient) -> None:
    response = client.get("/users/redis-check")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_rate_limit_returns_429_after_threshold(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    for _ in range(10):
        response = client.post(
            "/chat",
            headers=auth_headers,
            json={
                "message": "hello",
                "model": "default",
                "temperature": 0.7,
                "stream": False,
            },
        )
        assert response.status_code == 200

    blocked = client.post(
        "/chat",
        headers=auth_headers,
        json={
            "message": "hello again",
            "model": "default",
            "temperature": 0.7,
            "stream": False,
        },
    )

    assert blocked.status_code == 429
    assert "rate limit exceeded" in blocked.json()["detail"]


def test_chat_stream_rate_limit_returns_429_after_threshold(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    for _ in range(20):
        response = client.post(
            "/chat/stream",
            headers=auth_headers,
            json={
                "message": "stream hello",
                "model": "default",
                "temperature": 0.7,
                "stream": True,
            },
        )
        assert response.status_code == 200

    blocked = client.post(
        "/chat/stream",
        headers=auth_headers,
        json={
            "message": "stream blocked",
            "model": "default",
            "temperature": 0.7,
            "stream": True,
        },
    )

    assert blocked.status_code == 429
    assert "rate limit exceeded" in blocked.json()["detail"]
