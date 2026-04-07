from fastapi import APIRouter, HTTPException, status

from ..core.security import fake_encode_token
from ..schemas import TokenResponse, UserLogin

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin) -> TokenResponse:
    """
    学习版登录接口。

    这里先不用数据库校验用户，
    只要用户名和密码满足一个最小条件，就返回演示 token。
    """
    if payload.username != "demo_user" or payload.password != "demo12345":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )

    token = fake_encode_token(payload.username)
    return TokenResponse(access_token=token)
