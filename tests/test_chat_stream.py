from fastapi.testclient import TestClient


def test_chat_stream_success(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    """
    验证流式接口能成功返回，并且 content-type 正确。
    """
    response = client.post(
        "/chat/stream",
        headers=auth_headers,
        json={
            "message": "请帮我介绍一下你自己",
            "model": "default",
            "temperature": 0.7,
            "stream": True,
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")

    text = response.text
    assert "data:" in text
    assert '"type": "chunk"' in text
    assert '"type": "done"' in text
    assert "请帮我介绍一下你自己" in text


def test_chat_stream_requires_token(client: TestClient) -> None:
    """
    验证流式接口同样需要鉴权。
    """
    response = client.post(
        "/chat/stream",
        json={
            "message": "你好",
            "temperature": 0.7,
        },
    )

    assert response.status_code == 401


def test_chat_stream_rejects_invalid_message(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    """
    验证 schema 校验仍然生效。
    """
    response = client.post(
        "/chat/stream",
        headers=auth_headers,
        json={
            "message": "   ",
            "temperature": 0.7,
        },
    )

    assert response.status_code == 422
