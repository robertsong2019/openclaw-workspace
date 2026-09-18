#!/usr/bin/env python3
"""
Self-Evolving Agent 状态持久化（RED-first）

缺口：agent 的全部演化产物（工具代码/generation/hash）只活在内存里——
进程退出即丢失，"code as identity" 名不副实。补 export_state/import_state：

1. round-trip：evolve N 个 → export → 新 agent import → use() 可用、
   generation/hash 保真
2. 损坏条目：state 里混入非法 Python → 该条被跳过并报告，其余照常导入
   （compile() 先行验证 —— 绝不 exec 未编译验证的生成代码）
3. import 报告：返回 {"imported": [...], "skipped": {name: reason}} 结构
4. 边界：空 state / 空 agent / state 非 dict → 明确错误不崩溃
5. import 后再演化：generation 从导入值继续递增（不重置为 0/1）
"""

import pytest

from self_evolving_agent import SelfEvolvingAgent


def build_agent() -> SelfEvolvingAgent:
    agent = SelfEvolvingAgent(name="TestAgent")
    agent.evolve("fibonacci")
    agent.evolve("prime_check")
    agent.evolve("password_gen")
    agent.evolve("password_gen")  # gen 1
    return agent


def test_export_state_contains_code_and_generation():
    agent = build_agent()
    state = agent.export_state()
    assert set(state["tools"].keys()) == {"fibonacci", "prime_check", "password_gen"}
    assert state["tools"]["password_gen"]["generation"] == 1
    assert "def password_gen" in state["tools"]["password_gen"]["code"]


def test_import_roundtrip_preserves_behavior_and_identity(tmp_path):
    agent = build_agent()
    state = agent.export_state()

    revived = SelfEvolvingAgent(name="Revived")
    report = revived.import_state(state)
    assert report["imported"] == ["fibonacci", "prime_check", "password_gen"]
    assert report["skipped"] == {}

    # 行为保真
    assert "Fibonacci(10)" in revived.use("fibonacci", n=10)
    # 身份保真：hash 与原 agent 一致（同 code → md5 重算同值）
    for name in state["tools"]:
        assert revived.tools[name].hash == agent.tools[name].hash
        assert revived.tools[name].generation == agent.tools[name].generation


def test_import_skips_corrupted_entry_and_reports():
    agent = build_agent()
    state = agent.export_state()
    state["tools"]["broken_tool"] = {
        "code": "def broken_tool(:\n    syntax error here",
        "description": "corrupt", "generation": 0,
    }

    revived = SelfEvolvingAgent()
    report = revived.import_state(state)
    assert "broken_tool" in report["skipped"]
    assert "fibonacci" in report["imported"]
    assert "broken_tool" not in revived.tools


def test_import_nonexistent_entry_format():
    state = {"tools": {"no_code_tool": {"description": "missing code field"}}}
    report = SelfEvolvingAgent().import_state(state)
    assert "no_code_tool" in report["skipped"]
    assert report["imported"] == []


def test_import_state_rejects_non_dict():
    with pytest.raises(TypeError):
        SelfEvolvingAgent().import_state(["not", "a", "dict"])
    with pytest.raises(TypeError):
        SelfEvolvingAgent().import_state("fibonacci")


def test_empty_roundtrip():
    agent = SelfEvolvingAgent()
    assert agent.export_state() == {"tools": {}}
    report = SelfEvolvingAgent().import_state({"tools": {}})
    assert report == {"imported": [], "skipped": {}}


def test_generation_continues_after_import():
    agent = build_agent()
    state = agent.export_state()  # password_gen gen 1

    revived = SelfEvolvingAgent()
    revived.import_state(state)
    result = revived.evolve("password_gen")
    assert "gen 2" in result, f"导入后应从 gen 1 续增，得到: {result}"
