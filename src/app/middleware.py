import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    一个学习版中间件，负责做两件事：
    1. 给每个请求补 request id
    2. 统计接口耗时

    这类逻辑适合放中间件，
    因为它和具体业务无关，但所有请求都会用到。
    """

    async def dispatch(self, request: Request, call_next):
        request_id = (
            request.headers.get("x-request-id") or f"req-{uuid.uuid4().hex[:8]}"
        )
        request.state.request_id = request_id

        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        response.headers["x-request-id"] = request_id
        response.headers["x-process-time-ms"] = str(duration_ms)
        return response
