"""
高级测试 — 边界条件和 Bug 验证
"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nano_agent import Agent, tool, Memory, LLM
from nano_agent.tools import clear_tools, list_tools, get_tool


def setup_module():
    """每个测试模块前清空工具注册表"""
    clear_tools()


def test_memory_max_entries():
    """测试记忆上限"""
    memory = Memory(max_entries=3)
    for i in range(5):
        memory.add(f"消息 {i}")
    assert len(memory.get_all()) == 3
    assert memory.get_all()[0].content == "消息 2"
    print("✅ 记忆上限测试通过")


def test_memory_search():
    """测试记忆搜索"""
    memory = Memory()
    memory.add("Python is great")
    memory.add("Rust is fast")
    memory.add("JavaScript is dynamic")

    results = memory.search("rust")
    assert len(results) == 1
    assert "Rust" in results[0].content
    print("✅ 记忆搜索测试通过")


def test_memory_search_no_match():
    """测试搜索无匹配"""
    memory = Memory()
    memory.add("hello world")
    results = memory.search("nonexistent")
    assert len(results) == 0
    print("✅ 搜索无匹配测试通过")


def test_memory_clear():
    """测试记忆清除"""
    memory = Memory()
    memory.add("test")
    memory.clear()
    assert len(memory.get_all()) == 0
    print("✅ 记忆清除测试通过")


def test_memory_to_context_empty():
    """测试空记忆转上下文"""
    memory = Memory()
    ctx = memory.to_context()
    assert ctx == ""
    print("✅ 空记忆上下文测试通过")


def test_memory_to_context_with_entries():
    """测试有内容的记忆转上下文"""
    memory = Memory()
    memory.add("test entry")
    ctx = memory.to_context()
    assert "test entry" in ctx
    print("✅ 记忆上下文转换测试通过")


def test_memory_persistence():
    """测试记忆持久化"""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        path = f.name

    try:
        m1 = Memory(persistence_path=path)
        m1.add("persistent data")
        del m1

        m2 = Memory(persistence_path=path)
        assert len(m2.get_all()) == 1
        assert m2.get_all()[0].content == "persistent data"
        print("✅ 记忆持久化测试通过")
    finally:
        os.unlink(path)


def test_tool_decorator_with_options():
    """测试带选项的工具装饰器"""
    @tool(name="custom_search", description="自定义搜索")
    def my_search(q: str) -> str:
        return f"搜索: {q}"

    t = get_tool("custom_search")
    assert t is not None
    assert t.name == "custom_search"
    assert t.description == "自定义搜索"
    assert t.execute(q="test") == "搜索: test"
    print("✅ 带选项工具装饰器测试通过")


def test_tool_default_description():
    """测试工具默认描述来自 docstring"""
    @tool
    def documented_func(x: int) -> int:
        """这是一个有文档的函数"""
        return x + 1

    t = get_tool("documented_func")
    assert t.description == "这是一个有文档的函数"
    print("✅ 工具默认描述测试通过")


def test_tool_no_docstring():
    """测试无文档字符串的工具"""
    @tool
    def no_doc_func(x: int) -> int:
        return x

    t = get_tool("no_doc_func")
    assert t.description == "工具: no_doc_func"
    print("✅ 无文档工具测试通过")


def test_tool_with_default_params():
    """测试带默认参数的工具"""
    @tool
    def flexible_func(x: int, y: int = 10) -> int:
        """灵活函数"""
        return x + y

    t = get_tool("flexible_func")
    assert "default" in t.parameters["y"]
    assert t.parameters["y"]["default"] == 10
    assert t.execute(x=5) == 15
    assert t.execute(x=5, y=20) == 25
    print("✅ 默认参数工具测试通过")


def test_tool_to_dict():
    """测试工具序列化"""
    @tool
    def serializable(query: str) -> str:
        """可序列化"""
        return query

    t = get_tool("serializable")
    d = t.to_dict()
    assert "name" in d
    assert "description" in d
    assert "parameters" in d
    assert d["name"] == "serializable"
    print("✅ 工具序列化测试通过")


def test_list_tools():
    """测试列出所有工具"""
    clear_tools()
    @tool
    def tool_a() -> str:
        """工具A"""
        return "a"

    @tool
    def tool_b() -> str:
        """工具B"""
        return "b"

    tools = list_tools()
    assert len(tools) == 2
    print("✅ 列出工具测试通过")


def test_agent_with_tools():
    """测试带工具的 Agent"""
    clear_tools()

    @tool
    def calculator(a: int, b: int) -> int:
        """计算器"""
        return a + b

    agent = Agent(
        name="计算代理",
        instructions="你是一个计算助手",
        llm=LLM.mock(),
        tools=[get_tool("calculator")]
    )
    assert len(agent.tools) == 1
    assert agent.tools[0].name == "calculator"
    print("✅ 带工具 Agent 测试通过")


def test_agent_reset():
    """测试 Agent 重置"""
    agent = Agent(name="测试", instructions="测试", llm=LLM.mock())
    agent._conversation_history.append({"role": "user", "content": "test"})
    agent.reset()
    assert len(agent._conversation_history) == 0
    print("✅ Agent 重置测试通过")


def test_agent_max_iterations():
    """测试 Agent 最大迭代次数"""
    agent = Agent(
        name="测试",
        instructions="测试",
        llm=LLM.mock(),
        max_iterations=1
    )
    assert agent.max_iterations == 1
    print("✅ Agent 最大迭代测试通过")


def test_agent_execute_tool_error():
    """测试 Agent 工具执行错误处理"""
    agent = Agent(
        name="测试",
        instructions="测试",
        llm=LLM.mock()
    )
    # 调用不存在的工具
    result = agent._execute_tool({"name": "nonexistent", "arguments": "{}"})
    assert "错误" in result
    print("✅ 工具执行错误处理测试通过")


def test_agent_execute_tool_exception():
    """测试工具抛异常时的处理"""
    clear_tools()

    @tool
    def broken_tool() -> str:
        """会出错的工具"""
        raise ValueError("故意出错")

    agent = Agent(
        name="测试",
        instructions="测试",
        llm=LLM.mock(),
        tools=[get_tool("broken_tool")]
    )
    result = agent._execute_tool({"name": "broken_tool", "arguments": "{}"})
    assert "错误" in result
    assert "故意出错" in result
    print("✅ 工具异常处理测试通过")


def test_memory_entry_to_dict():
    """测试 MemoryEntry 序列化"""
    memory = Memory()
    memory.add("test content", metadata={"key": "value"})
    entries = memory.get_all()
    d = entries[0].to_dict()
    assert "content" in d
    assert "timestamp" in d
    assert "metadata" in d
    assert d["content"] == "test content"
    assert d["metadata"]["key"] == "value"
    print("✅ MemoryEntry 序列化测试通过")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Nano-Agent 高级测试")
    print("=" * 60)
    print()

    # Run all test functions
    tests = [obj for name, obj in sorted(globals().items())
             if name.startswith('test_') and callable(obj)]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1

    print()
    print("=" * 60)
    print(f"✅ {passed} 通过, ❌ {failed} 失败")
    print("=" * 60)
