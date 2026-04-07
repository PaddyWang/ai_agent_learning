from fastapi import HTTPException, status

# TODO
# 这里先用“假 token”方案做学习版认证。
# 后面你学到 JWT 时，再把这里替换成真正的签名和解码逻辑。


def fake_encode_token(username: str) -> str:
    """
    根据用户名生成一个最小可用的演示 token。

    这里故意不做真正加密，只是为了先跑通：
    登录 -> 拿 token -> 带 token 访问受保护接口
    """
    return f"token-for:{username}"


def fake_decode_token(token: str) -> dict:
    """
    解析演示 token。

    预期格式：
    token-for:username
    """
    prefix = "token-for:"
    if not token.startswith(prefix):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        )

    username = token.removeprefix(prefix).strip()
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        )

    return {
        "user_id": f"user_{username}",
        "username": username,
    }
