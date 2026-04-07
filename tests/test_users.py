from fastapi.testclient import TestClient


def test_get_me_success(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    """
    验证：
    1. 带上 x-user-id 后，接口可以正常返回
    2. 返回结构符合 UserResponse
    """
    response = client.get("/users/me", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user_demo_user"
    assert data["username"] == "demo_user"


def test_get_me_requires_headers(client: TestClient) -> None:
    """
    验证：
    缺少 x-user-id 时，依赖函数会主动拦截并返回 401。
    """
    response = client.get("/users/me")
    assert response.status_code == 401


def test_get_me_accepts_request_id_header(
    client: TestClient,
    request_headers: dict[str, str],
) -> None:
    """
    验证：
    1. 带 request id 不会影响接口正常执行
    2. 这为后面做日志追踪和链路追踪打基础
    """
    response = client.get("/users/me", headers=request_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user_demo_user"
    assert data["username"] == "demo_user"
