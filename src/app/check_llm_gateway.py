from __future__ import annotations

import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from .llm.types import ToolSpec
from .services.llm_gateway import LLMGateway


def get_current_time(args: dict) -> dict:
    """
    一个最小本地工具。

    这里故意不接外部 API，
    这样你可以专注验证 function calling 流程本身。
    """
    timezone = args.get("timezone", "Asia/Shanghai")
    now = datetime.now(ZoneInfo(timezone))

    return {
        "timezone": timezone,
        "iso_time": now.isoformat(),
        "readable_time": now.strftime("%Y-%m-%d %H:%M:%S"),
    }


async def main() -> None:
    gateway = LLMGateway()

    print("=== 1. DeepSeek 普通文本生成 ===")
    text_response = await gateway.generate(
        prompt="请用一句话介绍 DeepSeek Function Calling 的作用。",
        instructions="你是一名简洁、专业的 Python AI 工程助手。",
    )
    print(text_response.text)
    print()

    print("=== 2. Function Calling ===")
    tools = [
        ToolSpec(
            name="get_current_time",
            description="获取指定时区的当前时间。",
            parameters={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "IANA 时区名称，例如 Asia/Shanghai",
                    },
                },
                "required": ["timezone"],
                "additionalProperties": False,
            },
            handler=get_current_time,
            strict=True,
        )
    ]

    tool_response = await gateway.generate_with_tools(
        prompt="请调用工具获取北京时间，并用中文告诉我现在几点了。",
        instructions="你是一个会优先使用工具获取准确信息的助手。",
        tools=tools,
    )
    print(tool_response.text)
    print()

    print("=== 3. DeepSeek 流式输出 ===")
    async for chunk in gateway.stream(
        prompt="请用三句话解释什么是 Function Calling。",
        instructions="你是一名简洁的技术讲师。",
    ):
        print(chunk, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(main())
