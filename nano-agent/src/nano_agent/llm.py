"""
LLM 接口 - 统一的大语言模型接口
"""

import json
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod


class LLMBackend(ABC):
    """LLM 后端抽象类"""

    @abstractmethod
    def complete(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        完成对话

        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]
            tools: 可用的工具列表
            **kwargs: 其他参数

        Returns:
            {"content": "...", "tool_calls": [...], "usage": {...}}
        """
        pass


class OpenAIBackend(LLMBackend):
    """OpenAI 后端"""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.openai.com/v1",
        model: str = "gpt-3.5-turbo"
    ):
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        except ImportError:
            raise ImportError("请安装 openai: pip install openai")
        self.model = model

    def complete(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        # 构建 OpenAI 工具格式
        openai_tools = None
        if tools:
            openai_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool["description"],
                        "parameters": {
                            "type": "object",
                            "properties": {
                                k: {"type": v.get("type", "string")}
                                for k, v in tool["parameters"].items()
                            },
                            "required": []
                        }
                    }
                }
                for tool in tools
            ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=openai_tools,
            **kwargs
        )

        message = response.choices[0].message
        tool_calls = []

        # 解析工具调用
        if message.tool_calls:
            for call in message.tool_calls:
                tool_calls.append({
                    "id": call.id,
                    "name": call.function.name,
                    "arguments": call.function.arguments
                })

        return {
            "content": message.content or "",
            "tool_calls": tool_calls,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }


class MockBackend(LLMBackend):
    """Mock 后端 - 用于测试和演示"""

    def complete(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        last_message = messages[-1]["content"] if messages else ""

        # 模拟工具调用
        if tools and "搜索" in last_message:
            tool_name = tools[0]["name"]
            return {
                "content": "",
                "tool_calls": [{
                    "id": "mock_1",
                    "name": tool_name,
                    "arguments": json.dumps({"query": last_message})
                }],
                "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
            }

        return {
            "content": f"这是对 '{last_message}' 的模拟回复",
            "tool_calls": [],
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
        }


class LLM:
    """LLM 接口"""

    def __init__(self, backend: LLMBackend):
        self.backend = backend

    @classmethod
    def openai(cls, api_key: str, **kwargs):
        """创建 OpenAI LLM"""
        return cls(OpenAIBackend(api_key=api_key, **kwargs))

    @classmethod
    def mock(cls):
        """创建 Mock LLM"""
        return cls(MockBackend())

    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """发送聊天请求"""
        return self.backend.complete(messages, tools, **kwargs)
