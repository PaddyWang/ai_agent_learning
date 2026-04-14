from __future__ import annotations

from collections.abc import AsyncIterator

from ..llm.providers.deepseek_provider import DeepSeekProvider
from ..llm.types import LLMRequest, LLMResponse, ToolSpec


class LLMGateway:
    """
    统一网关层。

    现在默认接 DeepSeek provider。
    后面如果你要扩展 OpenAI / Qwen / OpenAI-compatible 供应商，
    只需要在这一层切 provider，不需要改业务层。
    """

    def __init__(self, provider: DeepSeekProvider | None = None) -> None:
        self.provider: DeepSeekProvider = provider or DeepSeekProvider()

    async def generate(
        self,
        *,
        prompt: str,
        instructions: str | None = None,
        model: str | None = None,
    ) -> LLMResponse:
        request = LLMRequest(
            prompt=prompt,
            instructions=instructions,
            model=model,
        )

        return await self.provider.generate(request)

    async def generate_with_tools(
        self,
        *,
        prompt: str,
        tools: list[ToolSpec],
        instructions: str | None = None,
        model: str | None = None,
        max_tool_rounds: int = 5,
    ) -> LLMResponse:
        request = LLMRequest(
            prompt=prompt,
            instructions=instructions,
            model=model,
            max_tool_rounds=max_tool_rounds,
        )

        return await self.provider.generate_with_tools(request, tools)

    async def stream(
        self,
        *,
        prompt: str,
        instructions: str | None = None,
        model: str | None = None,
    ) -> AsyncIterator[str]:
        request = LLMRequest(
            prompt=prompt,
            instructions=instructions,
            model=model,
        )
        async for chunk in self.provider.stream(request):
            yield chunk
