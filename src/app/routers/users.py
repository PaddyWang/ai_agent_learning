from fastapi import APIRouter, BackgroundTasks, Depends, Request

from ..deps import get_current_user
from ..schemas import UserResponse
from ..services.logging_service import format_access_log, write_access_log

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_me(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
) -> UserResponse:
    """
    受保护接口示例。

    这里同时演示两件事：
    1. 通过 Depends 拿当前用户
    2. 通过 request.state 读取中间件写入的 request_id
    """
    _request_id = request.state.request_id

    log_line = format_access_log(
        path=str(request.url.path),
        method=request.method,
        user_id=current_user["user_id"],
        request_id=getattr(request.state, "request_id", None),
    )
    background_tasks.add_task(write_access_log, log_line)

    return UserResponse(**current_user)
