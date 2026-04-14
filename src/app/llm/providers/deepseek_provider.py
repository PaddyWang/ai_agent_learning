from __future__ import annotations

import inspect
import json
import os
from collections.abc import AsyncIterator
from typing import Any

from openai import AsyncOpenAI

from ..types import LLMRequest, LLMResponse, ToolSpec


class DeepSeekProvider:
    """
    基于 DeepSeek OpenAI-compatible API 的 provider。

    DeepSeek 当前主流接入方式是：
    1. 使用 OpenAI Python SDK
    2. 把 base_url 指到 https://api.deepseek.com
    3. 走 chat.completions 接口完成文本生成、工具调用和流式输出
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise RuntimeError("DEEPSEEK_API_KEY is not set")

        self.model = model or os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        self.base_url = base_url or os.getenv(
            "DEEPSEEK_BASE_URL", "https://api.deepseek.com"
        )

        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def _resolve_model(self, request: LLMRequest) -> str:
        return request.model or self.model

    def _build_messages(
        self,
        prompt: str,
        instructions: str | None = None,
    ) -> list[dict[str, Any]]:
        messages: list[dict[str, Any]] = []

        if instructions:
            messages.append(
                {
                    "role": "system",
                    "content": instructions,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        return messages

    def _collect_tool_calls(self, message: Any) -> list[dict[str, Any]]:
        tool_calls: list[dict[str, Any]] = []

        for item in getattr(message, "tool_calls", []) or []:
            tool_calls.append(
                {
                    "name": item.function.name,
                    "call_id": item.id,
                    "arguments": json.loads(item.function.arguments),
                }
            )

        return tool_calls

    async def _run_tool(self, tool: ToolSpec, args: dict[str, Any]) -> str:
        result = tool.handler(args)
        if inspect.isawaitable(result):
            result = await result

        if isinstance(result, str):
            return result

        return json.dumps(result, ensure_ascii=False)

    async def generate(self, request: LLMRequest) -> LLMResponse:
        model = self._resolve_model(request)
        response = await self.client.chat.completions.create(
            model=model,
            messages=self._build_messages(request.prompt, request.instructions),
        )

        message = response.choices[0].message
        return LLMResponse(
            text=message.content or "",
            provider="deepseek",
            model=model,
            tool_calls=self._collect_tool_calls(message),
            raw_output=[message.model_dump(exclude_none=True)],
        )

    async def generate_with_tools(
        self,
        request: LLMRequest,
        tools: list[ToolSpec],
    ) -> LLMResponse:
        model = self._resolve_model(request)
        tool_map = {tool.name: tool for tool in tools}
        tool_defs = [tool.to_chat_completions_tool() for tool in tools]
        messages = self._build_messages(request.prompt, request.instructions)
        collected_tool_calls: list[dict[str, Any]] = []
        last_message: Any | None = None

        for _ in range(request.max_tool_rounds):
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tool_defs,
                tool_choice="auto",
            )
            message = response.choices[0].message
            last_message = message
            current_tool_calls = self._collect_tool_calls(message)
            collected_tool_calls.extend(current_tool_calls)

            if not current_tool_calls:
                return LLMResponse(
                    text=message.content or "",
                    provider="deepseek",
                    model=model,
                    tool_calls=collected_tool_calls,
                    raw_output=[message.model_dump(exclude_none=True)],
                )

            messages.append(message.model_dump(exclude_none=True))

            for item in message.tool_calls or []:
                tool = tool_map.get(item.function.name)
                if tool is None:
                    raise ValueError(
                        f"unknown tool requested by model: {item.function.name}"
                    )

                args = json.loads(item.function.arguments)
                result = await self._run_tool(tool, args)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": item.id,
                        "content": result,
                    }
                )

        return LLMResponse(
            text=last_message.content
            if last_message is not None and last_message.content
            else "",
            provider="deepseek",
            model=model,
            tool_calls=collected_tool_calls,
            raw_output=(
                [last_message.model_dump(exclude_none=True)]
                if last_message is not None
                else []
            ),
        )

    async def stream(self, request: LLMRequest) -> AsyncIterator[str]:
        model = self._resolve_model(request)
        stream = await self.client.chat.completions.create(
            model=model,
            messages=self._build_messages(request.prompt, request.instructions),
            stream=True,
        )

        async for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
