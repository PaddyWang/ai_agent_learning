from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .middleware import RequestContextMiddleware
from .routers import auth, chat, users

app = FastAPI(title="AI Agent Learning Project")

# 注册中间件
app.add_middleware(RequestContextMiddleware)

# 再加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    # allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    """
    最小健康检查接口。
    """
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(users.router)
