import inspect
import json
import os
from collections.abc import AsyncIterator
from typing import Any

from openai import AsyncOpenAI

from ..types import LLMRequest, LLMResponse, ToolSpec


class OpenAIProvider:
    """
    基于 OpenAI Responses API 的 provider。

    这里做三件事：
    1. 普通文本生成
    2. function calling
    3. 流式输出
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")

        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def _resolve_model(self, request: LLMRequest) -> str:
        return request.model or self.model

    def _build_input(self, prompt: str) -> list[dict[str, str]]:
        """
        统一把 prompt 包装成 Responses API input。
        """
        return [
            {
                "role": "user",
                "content": prompt,
            }
        ]

    def _collect_tool_calls(self, output: list[Any]) -> list[dict[str, Any]]:
        tool_calls: list[dict[str, Any]] = []

        for item in output:
            if getattr(item, "type", None) != "function_call":
                continue

            tool_calls.append(
                {
                    "name": item.name,
                    "call_id": item.call_id,
                    "arguments": json.loads(item.arguments),
                }
            )

        return tool_calls

    async def _run_tool(self, tool: ToolSpec, args: dict[str, Any]) -> str:
        """
        支持同步函数和异步函数两种 handler。
        """
        result = tool.handler(args)
        if inspect.isawaitable(result):
            result = await result

        if isinstance(result, str):
            return result

        return json.dumps(result, ensure_ascii=False)

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """
        普通文本生成。
        """
        payload: dict[str, Any] = {
            "model": self._resolve_model(request),
            "input": self._build_input(request.prompt),
        }

        if request.instructions:
            payload["instructions"] = request.instructions

        response = await self.client.responses.create(**payload)

        return LLMResponse(
            text=response.output_text,
            provider="openai",
            model=payload["model"],
            tool_calls=self._collect_tool_calls(response.output),
            raw_output=list(response.output),
        )

    async def generate_with_tools(
        self,
        request: LLMRequest,
        tools: list[ToolSpec],
    ) -> LLMResponse:
        """
        跑完整的 function calling 循环。

        官方文档的推荐流程是：
        1. 带 tools 发起请求
        2. 检查 response.output 里的 function_call
        3. 执行本地函数
        4. 把 function_call_output 回传给模型
        5. 再拿最终回答
        """
        model = self._resolve_model(request)
        tool_map = {tool.name: tool for tool in tools}
        input_items: list[Any] = self._build_input(request.prompt)

        payload: dict[str, Any] = {
            "model": model,
            "tools": [tool.to_openai_tool() for tool in tools],
        }

        if request.instructions:
            payload["instructions"] = request.instructions

        last_response = None

        for _ in range(request.max_tool_rounds):
            response = await self.client.responses.create(
                **payload,
                input=input_items,
            )
            last_response = response

            # 按官方示例，把模型本轮 output 保留到下一轮 input 中
            input_items += list(response.output)

            function_calls = [
                item
                for item in response.output
                if getattr(item, "type", None) == "function_call"
            ]

            # 没有 tool call，说明可以直接结束
            if not function_calls:
                return LLMResponse(
                    text=response.output_text,
                    provider="openai",
                    model=model,
                    tool_calls=self._collect_tool_calls(response.output),
                    raw_output=list(response.output),
                )

            for item in function_calls:
                tool = tool_map.get(item.name)
                if tool is None:
                    raise ValueError(f"unknown tool requested by model: {item.name}")

                args = json.loads(item.arguments)
                result = await self._run_tool(tool, args)

                input_items.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": result,
                    }
                )

        # 到这里说明超过 max_tool_rounds 了
        return LLMResponse(
            text=(
                last_response.output_text
                if last_response is not None
                else "tool calling stopped before final text was produced"
            ),
            provider="openai",
            model=model,
            tool_calls=(
                self._collect_tool_calls(last_response.output)
                if last_response is not None
                else []
            ),
            raw_output=(
                list(last_response.output) if last_response is not None else []
            ),
        )

    async def stream(self, request: LLMRequest) -> AsyncIterator[str]:
        """
        预留给 Day 16+ 的流式文本输出。
        """
        payload: dict[str, Any] = {
            "model": self._resolve_model(request),
            "input": self._build_input(request.prompt),
            "stream": True,
        }
        if request.instructions:
            payload["instructions"] = request.instructions

        stream = await self.client.responses.create(**payload)

        async for event in stream:
            if getattr(event, "type", None) == "response.output_text.delta":
                yield event.delta
