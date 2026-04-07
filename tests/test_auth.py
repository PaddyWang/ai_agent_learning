from fastapi.testclient import TestClient


def test_login_success(client: TestClient) -> None:
    response = client.post(
        "/login",
        json={
            "username": "demo_user",
            "password": "demo12345",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"].startswith("token-for:")


def test_login_rejects_invalid_credentials(client: TestClient) -> None:
    response = client.post(
        "/login",
        json={
            "username": "wrong_user",
            "password": "wrong12345",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "invalid username or password"
