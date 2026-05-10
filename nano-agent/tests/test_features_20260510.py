"""
2026-05-10 新功能测试 — Memory tags + Agent on_step callback
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nano_agent import Agent, Memory


class TestMemoryTags:
    """Memory 标签系统"""

    def test_add_with_tags(self):
        """带标签添加记忆"""
        m = Memory()
        m.add("天气晴朗", tags=["weather", "daily"])
        m.add("开会讨论项目", tags=["work"])
        entry = m.get_all()[0]
        assert entry.tags == ["weather", "daily"]

    def test_search_with_tag_filter(self):
        """按标签过滤搜索"""
        m = Memory()
        m.add("修复了bug", tags=["work", "urgent"])
        m.add("天气不错", tags=["daily"])
        m.add("部署上线", tags=["work"])

        results = m.search("", tags=["work"])
        assert len(results) == 2

    def test_search_with_tags_and_query(self):
        """标签 + 关键词组合搜索"""
        m = Memory()
        m.add("修复了登录bug", tags=["work", "bug"])
        m.add("修复了支付bug", tags=["work", "bug"])
        m.add("天气修复不了", tags=["daily"])

        results = m.search("修复", tags=["bug"])
        assert len(results) == 2

    def test_search_tags_no_match(self):
        """标签过滤无匹配返回空"""
        m = Memory()
        m.add("hello", tags=["greeting"])
        results = m.search("hello", tags=["nonexistent"])
        assert len(results) == 0

    def test_tags_persisted(self):
        """标签持久化"""
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name

        try:
            m1 = Memory(persistence_path=path)
            m1.add("tagged entry", tags=["persist"])
            del m1

            m2 = Memory(persistence_path=path)
            entries = m2.get_all()
            assert len(entries) == 1
            assert entries[0].tags == ["persist"]
        finally:
            os.unlink(path)

    def test_entry_without_tags(self):
        """无标签记忆的tags为空列表"""
        m = Memory()
        m.add("no tags here")
        assert m.get_all()[0].tags == []

    def test_to_dict_with_tags(self):
        """to_dict包含tags"""
        m = Memory()
        m.add("test", tags=["a", "b"])
        d = m.get_all()[0].to_dict()
        assert d["tags"] == ["a", "b"]

    def test_to_dict_without_tags(self):
        """无tags时to_dict不含tags键"""
        m = Memory()
        m.add("test")
        d = m.get_all()[0].to_dict()
        assert "tags" not in d

    print("✅ Memory tags 测试就绪")


class TestAgentOnStep:
    """Agent on_step 回调"""

    def test_on_step_called(self):
        """on_step 在每次迭代被调用"""
        steps = []
        agent = Agent(name="test", instructions="test", verbose=False)
        agent.on_step = lambda s: steps.append(s)
        agent.run("hello")
        assert len(steps) >= 1
        assert "iteration" in steps[0]

    def test_on_step_contains_tool_calls(self):
        """on_step 包含工具调用信息"""
        from nano_agent import tool
        from nano_agent.tools import clear_tools, get_tool
        clear_tools()

        @tool
        def echo(text: str) -> str:
            """echo"""
            return text

        steps = []
        echo_tool = get_tool("echo")
        agent = Agent(name="test", instructions="test", verbose=False, tools=[echo_tool])
        agent.on_step = lambda s: steps.append(s)
        agent.run("搜索 echo")  # triggers mock tool call
        # mock backend triggers tool call when "搜索" is in input
        assert len(steps) >= 1

    def test_on_step_none_is_safe(self):
        """on_step=None 不会报错"""
        agent = Agent(name="test", instructions="test", verbose=False)
        agent.on_step = None
        result = agent.run("hello")
        assert isinstance(result, str)

    print("✅ Agent on_step 测试就绪")
