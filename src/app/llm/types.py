from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

ToolHandler = Callable[
    [dict[str, Any]], str | dict[str, Any] | Awaitable[str | dict[str, Any]]
]


@dataclass(slots=True)
class ToolSpec:
    """
    统一描述一个可供模型调用的函数工具。
    """

    name: str
    description: str
    parameters: dict[str, Any]
    handler: ToolHandler
    strict: bool = True

    def to_openai_tool(self) -> dict[str, Any]:
        """
        转成 OpenAI Responses API 所需的 tool 定义。
        Responses API 下 function tool 的常用形态是：
        {
            "type": "function",
            "name": "...",
            "description": "...",
            "parameters": {...},
            "strict": true
        }
        """
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "strict": self.strict,
        }

    def to_chat_completions_tool(self) -> dict[str, Any]:
        """
        转成兼容 OpenAI / DeepSeek chat.completions 的 tool 定义。

        这类接口要求把函数信息包在 `function` 字段下。
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
                "strict": self.strict,
            },
        }


@dataclass(slots=True)
class LLMRequest:
    """
    统一的模型请求对象。
    """

    prompt: str
    instructions: str | None = None
    model: str | None = None
    max_tool_rounds: int = 5


@dataclass(slots=True)
class LLMResponse:
    """
    统一的模型响应对象。
    """

    text: str
    provider: str
    model: str
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    raw_output: list[Any] = field(default_factory=list)
