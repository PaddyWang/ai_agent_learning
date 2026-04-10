from pathlib import Path

import pytest
from app.main import app
from fastapi.testclient import TestClient


class FakePipeline:
    def __init__(self, redis_client: "FakeRedis") -> None:
        self.redis_client = redis_client
        self.commands: list[tuple[str, tuple, dict]] = []

    def incr(self, key: str) -> "FakePipeline":
        self.commands.append(("incr", (key,), {}))
        return self

    def ttl(self, key: str) -> "FakePipeline":
        self.commands.append(("ttl", (key,), {}))
        return self

    def execute(self) -> list[object]:
        results: list[object] = []
        for name, args, kwargs in self.commands:
            results.append(getattr(self.redis_client, name)(*args, **kwargs))
        self.commands.clear()
        return results


class FakeRedis:
    """
    一个足够覆盖当前测试场景的内存版 Redis。

    目标：
    1. 不依赖本机 Redis 服务
    2. 支持当前项目已经用到的 get/set/delete/incr/ttl/expire/pipeline
    """

    def __init__(self) -> None:
        self.store: dict[str, str] = {}
        self.expiry: dict[str, int] = {}

    def from_json(self, value: str) -> str:
        return value

    def set(self, key: str, value: str, ex: int | None = None) -> bool:
        self.store[key] = value
        if ex is not None:
            self.expiry[key] = ex
        elif key in self.expiry:
            del self.expiry[key]
        return True

    def get(self, key: str) -> str | None:
        return self.store.get(key)

    def delete(self, key: str) -> int:
        deleted = 0
        if key in self.store:
            del self.store[key]
            deleted += 1
        self.expiry.pop(key, None)
        return deleted

    def incr(self, key: str) -> int:
        current = int(self.store.get(key, "0"))
        current += 1
        self.store[key] = str(current)
        return current

    def ttl(self, key: str) -> int:
        if key not in self.store:
            return -2
        return self.expiry.get(key, -1)

    def expire(self, key: str, seconds: int) -> bool:
        if key not in self.store:
            return False
        self.expiry[key] = seconds
        return True

    def ping(self) -> bool:
        return True

    def pipeline(self) -> FakePipeline:
        return FakePipeline(self)


@pytest.fixture
def fake_redis() -> FakeRedis:
    return FakeRedis()


@pytest.fixture(autouse=True)
def patch_redis_and_logs(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    fake_redis: FakeRedis,
) -> None:
    """
    自动把测试环境里的外部依赖替换掉：
    1. 用内存版 FakeRedis 替代真实 Redis
    2. 把日志文件写到 pytest 的临时目录，避免权限问题
    """
    import app.core.redis_client as redis_client_module
    import app.routers.users as users_router_module
    import app.services.cache_service as cache_service_module
    import app.services.rate_limit_service as rate_limit_service_module
    import app.services.session_store_service as session_store_service_module
    from app.services import logging_service as logging_service_module

    monkeypatch.setattr(redis_client_module, "redis_client", fake_redis)
    monkeypatch.setattr(cache_service_module, "redis_client", fake_redis)
    monkeypatch.setattr(session_store_service_module, "redis_client", fake_redis)
    monkeypatch.setattr(rate_limit_service_module, "redis_client", fake_redis)
    monkeypatch.setattr(users_router_module, "redis_client", fake_redis)

    monkeypatch.setattr(logging_service_module, "LOG_FILE", tmp_path / "app.log")


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
