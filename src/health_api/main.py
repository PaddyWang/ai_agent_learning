"""
健康检查 API 服务
"""

import sys
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Health Check API", version="1.0.0")


class HealthResponse(BaseModel):
    """健康检查响应模型"""

    status: str
    timestamp: str
    version: str
    python_version: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    健康检查端点
    返回服务状态、时间戳和版本信息
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}",
    )


@app.get("/")
async def root():
    """根路径重定向到健康检查"""
    return {"message": "Welcome to Health API", "health_endpoint": "/health"}


# 可选：直接运行此文件
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8090)
