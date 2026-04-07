from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class UserResponse(BaseSchema):
    user_id: str
    username: str


class UserCreate(BaseSchema):
    username: str = Field(min_length=3, max_length=20, description="用户名")
    email: EmailStr
    password: str = Field(min_length=8, max_length=64, description="登录密码")

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        # allowed = value.replace("_", "").replace("-", "")
        if value.isalnum():
            raise ValueError("username can only contain letters, numbers, '_' and '-'")
        return value.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if value.isalpha() or value.isdigit():
            raise ValueError("password must contain both letters and numbers")
        return value


class UserLogin(BaseSchema):
    """
    登录请求模型。

    学习阶段先用 username + password，
    不接数据库，直接做一个 mock 登录。
    """

    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=64)


class TokenResponse(BaseSchema):
    """
    登录成功后返回给前端的 token 结构。
    """

    access_token: str
    token_type: str = "bearer"


class ChatRequest(BaseSchema):
    message: str = Field(min_length=1, max_length=4000, description="用户输入")
    session_id: str | None = Field(default=None, max_length=64, description="会话ID")
    model: str = Field(
        default="default", min_length=1, max_length=50, description="模型名称"
    )
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    stream: bool = False

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("message cannot be empty")
        return value

    @field_validator("session_id")
    @classmethod
    def normalize_session_id(cls, value: str) -> str:
        if value == "":
            return None
        return value


class ChatResponse(BaseSchema):
    session_id: str
    answer: str = Field(min_length=1, description="模型回复")
    model: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("answer")
    @classmethod
    def validate_answer(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("answer cannot be empty")
        return value


class ChatStreamChunk(BaseSchema):
    """
    流式输出中的单个分片事件。

    先把结构定下来，后面前端解析就更稳定。
    """

    type: str
    index: int | None = None
    session_id: str
    model: str
    content: str | None = None
