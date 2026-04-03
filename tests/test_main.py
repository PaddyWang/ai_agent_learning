import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from health_api.main import app

# 创建测试客户端
client = TestClient(app)


def test_health_endpoint():
    """测试 /health 端点"""
    response = client.get("/health")

    # 验证状态码
    assert response.status_code == 200

    # 验证响应结构
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "version" in data
    assert "python_version" in data

    # 验证数据内容
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"
    assert isinstance(data["timestamp"], str)


def test_root_endpoint():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "/health" in response.json()["health_endpoint"]


def test_health_response_format():
    """测试响应格式是否正确"""
    response = client.get("/health")
    data = response.json()

    # 验证时间戳格式（ISO格式）
    from datetime import datetime

    try:
        datetime.fromisoformat(data["timestamp"])
        timestamp_valid = True
    except ValueError:
        timestamp_valid = False
    assert timestamp_valid


# 参数化测试示例
@pytest.mark.parametrize(
    "endpoint,expected_status",
    [
        ("/health", 200),
        ("/", 200),
        ("/nonexistent", 404),
    ],
)
def test_multiple_endpoints(endpoint, expected_status):
    """测试多个端点的状态码"""
    response = client.get(endpoint)
    assert response.status_code == expected_status


def test_health_method_not_allowed():
    """测试 /health 不支持 POST 方法"""
    response = client.post("/health")
    assert response.status_code == 405  # Method Not Allowed
