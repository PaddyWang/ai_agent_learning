FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app/src

# 先复制依赖文件，利用 Docker layer cache
COPY pyproject.toml ./
COPY README.md ./

# 安装项目依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    fastapi[standard] \
    sqlalchemy[asyncio] \
    asyncpg \
    redis \
    alembic \
    aiosqlite \
    email-validator \
    uvicorn

# 再复制项目代码
COPY src ./src
COPY main.py ./main.py
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic

# FastAPI 容器内必须监听 0.0.0.0
EXPOSE 8082
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8082"]
