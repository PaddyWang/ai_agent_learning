import app.routers.chat as chat_router_module
from app.llm.types import LLMResponse
from fastapi.testclient import TestClient


class FakeGateway:
    async def generate(
        self,
        *,
        prompt: str,
        instructions: str | None = None,
        model: str | None = None,
    ) -> LLMResponse:
        return LLMResponse(
            text=f"LLM: {prompt}",
            provider="deepseek",
            model=model or "deepseek-chat",
        )


def test_chat_success(
    client: TestClient,
    auth_headers: dict[str, str],
    monkeypatch,
) -> None:
    """
    验证聊天接口的成功路径：
    1. 请求可以被正确接收
    2. 返回值符合 ChatResponse
    3. 默认 session_id 和 created_at 都存在
    """
    monkeypatch.setattr(chat_router_module, "LLMGateway", FakeGateway)

    response = client.post(
        "/chat",
        headers=auth_headers,
        json={
            "message": "你好，介绍一下你自己",
            "model": "default",
            "temperature": 0.7,
            "stream": False,
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["session_id"] == "session_user_demo_user"
    assert data["model"] == "deepseek-chat"
    assert data["answer"].startswith("LLM: 你好，介绍一下你自己")
    assert "created_at" in data


def test_chat_requires_token(client: TestClient) -> None:
    response = client.post(
        "/chat",
        json={
            "message": "你好",
            "temperature": 0.7,
        },
    )

    assert response.status_code == 401


def test_chat_rejects_invalid_temperature(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    """
    验证 temperature 超范围时返回 422。
    """
    response = client.post(
        "/chat",
        headers=auth_headers,
        json={
            "message": "帮我总结一下今天的工作",
            "temperature": 3,
        },
    )

    assert response.status_code == 422
