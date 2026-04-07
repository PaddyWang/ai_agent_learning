import pytest
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """
    共享的 FastAPI 测试客户端。

    为什么要做成 fixture：
    1. 避免每个测试文件都重复创建 TestClient
    2. 后面如果 app 初始化方式变化，只需要改一处
    3. 测试代码会更短、更稳定
    """
    return TestClient(app)


@pytest.fixture
def login_payload() -> dict[str, str]:
    """
    学习版登录账号。
    """
    return {
        "username": "demo_user",
        "password": "demo12345",
    }


@pytest.fixture
def auth_token(client: TestClient, login_payload: dict[str, str]) -> dict[str, str]:
    """
    先调用 /login，再把 token 提出来。

    这样其他测试不需要自己关心登录细节。
    """
    response = client.post("/login", json=login_payload)
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token: str) -> dict[str, str]:
    """
    生成标准 Bearer Token 请求头。
    """
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def request_headers(auth_headers: dict[str, str]) -> dict[str, str]:
    """
    在登录头的基础上，再补一个 request id。

    为什么拆成两个 fixture：
    1. auth_headers 只表达“身份”
    2. request_headers 表达“完整请求上下文”
    3. 这样复用粒度更灵活
    """
    return {
        **auth_headers,
        "x-request-id": "req_test_001",
    }
