"""
基础测试
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nano_agent import Agent, tool, Memory, LLM


def test_tool_registration():
    """测试工具注册"""
    @tool
    def test_func(x: int) -> int:
        """测试函数"""
        return x * 2

    from nano_agent.tools import get_tool
    tool_obj = get_tool("test_func")
    assert tool_obj is not None
    assert tool_obj.name == "test_func"
    assert tool_obj.execute(x=5) == 10
    print("✅ 工具注册测试通过")


def test_memory():
    """测试记忆系统"""
    memory = Memory()
    memory.add("测试消息 1")
    memory.add("测试消息 2")

    recent = memory.get_recent(2)
    assert len(recent) == 2
    assert recent[-1].content == "测试消息 2"
    print("✅ 记忆系统测试通过")


def test_mock_llm():
    """测试 Mock LLM"""
    llm = LLM.mock()
    response = llm.chat([{"role": "user", "content": "测试"}])
    assert "content" in response
    assert isinstance(response["content"], str)
    print("✅ Mock LLM 测试通过")


def test_agent_creation():
    """测试 Agent 创建"""
    agent = Agent(
        name="测试代理",
        instructions="你是一个测试代理",
        llm=LLM.mock()
    )
    assert agent.name == "测试代理"
    assert len(agent.tools) == 0
    print("✅ Agent 创建测试通过")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Nano-Agent 基础测试")
    print("=" * 60)
    print()

    test_tool_registration()
    test_memory()
    test_mock_llm()
    test_agent_creation()

    print()
    print("=" * 60)
    print("✅ 所有测试通过!")
    print("=" * 60)
