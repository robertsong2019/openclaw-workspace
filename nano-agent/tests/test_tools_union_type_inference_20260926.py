"""tools.py 类型推断：Union/Optional 解包（RED-first 2026-09-26）

装饰器类型推断只认 `__origin__`（list/dict 等），Union 类型（typing.Optional
与 PEP 604 `X | None`）无映射 → 落回 "string"。工具 schema 对 LLM 谎报类型：
def f(x: Optional[int] = None) 会让 LLM 传字符串 "42" 而非 42。
修复：Union（含 NoneType）解包取第一个非 None 类型，再走原有映射。
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from typing import Optional, List, Union

from nano_agent.tools import tool, clear_tools, get_tool


class TestUnionTypeInference(unittest.TestCase):
    def setUp(self):
        clear_tools()

    def tearDown(self):
        clear_tools()

    def _param_type(self, tool_name, param_name):
        t = get_tool(tool_name)
        self.assertIsNotNone(t)
        return t.parameters[param_name]["type"]

    def test_typing_optional_int_is_integer(self):
        @tool
        def f1(x: Optional[int] = None):
            return x

        self.assertEqual(self._param_type("f1", "x"), "integer")

    def test_pep604_int_or_none_is_integer(self):
        @tool
        def f2(y: int | None = None):
            return y

        self.assertEqual(self._param_type("f2", "y"), "integer")

    def test_pep604_str_or_none_is_string(self):
        @tool
        def f3(s: str | None = None):
            return s

        self.assertEqual(self._param_type("f3", "s"), "string")

    def test_optional_list_is_array(self):
        @tool
        def f4(items: Optional[List[str]] = None):
            return items

        self.assertEqual(self._param_type("f4", "items"), "array")

    def test_plain_union_takes_first_non_none(self):
        @tool
        def f5(v: Union[int, str, None] = None):
            return v

        self.assertEqual(self._param_type("f5", "v"), "integer")

    def test_non_union_behavior_unchanged(self):
        @tool
        def f6(a: str, b: List[int], c: bool = True, d=None):
            return a

        t = get_tool("f6")
        self.assertEqual(t.parameters["a"]["type"], "string")
        self.assertEqual(t.parameters["b"]["type"], "array")
        self.assertEqual(t.parameters["c"]["type"], "boolean")
        # 未注解仍回落 string（既有契约）
        self.assertEqual(t.parameters["d"]["type"], "string")


if __name__ == "__main__":
    unittest.main()
