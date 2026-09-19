#!/usr/bin/env python3
"""Demo main() integration tests + MockLLM intent-branch coverage.

Covers the previously-untested shipped surface:
- pocket_agent.main() / self_evolving_agent.main() (89 LOC, 0 coverage before)
- MockLLM time / remember / search intent branches (lines 111/113/115)
"""

import re

import pocket_agent as pa
import self_evolving_agent as sea


# ── MockLLM intent branches (via full agent.run loop) ──────────

def _agent_with_builtins():
    agent = pa.PocketAgent(name="t")

    @agent.tool(description="Get current weather for a city")
    def get_weather(city: str) -> str:
        return pa.json.dumps({"city": city, "temp": "22°C"})

    @agent.tool(description="Evaluate a math expression")
    def calculate(expression: str) -> str:
        try:
            return f"{expression} = {eval(expression, {'__builtins__': {}}, {})}"  # noqa: S307
        except Exception:
            return f"Could not evaluate: {expression}"

    @agent.tool(description="Get current date and time")
    def current_time() -> str:
        return pa.time.strftime("%Y-%m-%d %H:%M:%S %Z")

    @agent.tool(description="Search the web (simulated)")
    def web_search(query: str) -> str:
        return pa.json.dumps({"results": [f"Simulated result for '{query}'"], "source": "mock"})

    return agent


def test_time_intent_routes_to_current_time_tool(capsys):
    agent = _agent_with_builtins()
    result = agent.run("现在几点了？")
    assert "current_time 返回结果" in result
    tool_msgs = [m for m in agent.history if m.get("role") == "tool" and m.get("name") == "current_time"]
    assert len(tool_msgs) == 1
    assert re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", tool_msgs[0]["content"])
    assert "🔧 Calling current_time" in capsys.readouterr().out


def test_remember_intent_answers_directly_without_tools():
    agent = _agent_with_builtins()
    result = agent.run("请记住这件事")
    assert "💭 我的记忆中有" in result
    assert "tool_calls" not in str(agent.history)  # no tool was invoked
    # final answer stored in memory
    assert any("Final answer" in e for e in agent.memory.entries)


def test_search_intent_routes_to_web_search_with_query(capsys):
    agent = _agent_with_builtins()
    result = agent.run("搜索 Quantum Computing")
    assert "web_search 返回结果" in result
    tool_msgs = [m for m in agent.history if m.get("role") == "tool" and m.get("name") == "web_search"]
    assert len(tool_msgs) == 1
    assert "quantum" in tool_msgs[0]["content"].lower()  # MockLLM lowercases the query
    assert "Simulated result" in tool_msgs[0]["content"]


# ── pocket_agent.main() demo integration ──────────────────────

def test_pocket_agent_main_demo_full_loop(capsys):
    pa.main()
    out = capsys.readouterr().out
    # 5 demo inputs, all answered
    assert out.count("👤") == 5
    assert out.count("Final answer:") == 5
    # 4 of 5 intents emit tool calls (remember answers directly)
    assert out.count("🔧 Calling") == 4
    # real computed values from the registered tools
    assert "42 * 137 = 5754" in out
    assert '"temp": "22\\u00b0C"' in out  # json.dumps 默认 ensure_ascii 转义
    assert re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", out)
    assert "Simulated result" in out


# ── self_evolving_agent.main() demo integration ───────────────

def test_self_evolving_main_demo_full_loop(capsys):
    sea.main()
    out = capsys.readouterr().out
    # Phase 1: all 8 templates evolved
    assert out.count("🧬 Evolved tool") == 10  # 8 initial + 2 re-evolutions
    assert "Tools: 8" in out
    # Phase 2: real computed outputs
    assert "Fibonacci(42) = 267914296" in out
    assert "97 is prime" in out
    assert "100 is not prime (divisible by 2)" in out
    assert '"strength": "strong"' in out  # password length 20
    assert "hsl(210, 70%, 55%)" in out    # palette base_hue 210 first color
    assert "base64_encode" in out
    # Phase 4: re-evolution bumps generation, same code → same hash
    assert "Evolved tool 'password_gen' (gen 1" in out
    assert "Evolved tool 'password_gen' (gen 2" in out
    assert "Evolutions: 10" in out
