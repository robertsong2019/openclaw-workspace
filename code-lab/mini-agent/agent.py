#!/usr/bin/env python3
"""
Mini Agent Framework — A toy AI agent in ~200 lines.
Demonstrates: tool calling, memory, planning, reflection.

No external deps. Uses a mock LLM for demonstration.
"""

import json
import re
from datetime import datetime
from dataclasses import dataclass, field
from typing import Callable, Any


# ── Memory ─────────────────────────────────────────────────────

@dataclass
class Memory:
    short_term: list[dict] = field(default_factory=list)
    long_term: dict[str, str] = field(default_factory=dict)

    def add_message(self, role: str, content: str):
        self.short_term.append({"role": role, "content": content, "ts": datetime.now().isoformat()})

    def remember(self, key: str, value: str):
        self.long_term[key] = value

    def recall(self, key: str) -> str | None:
        if key in self.long_term:
            return self.long_term[key]
        # Fuzzy: substring match
        for k, v in self.long_term.items():
            if key in k or k in key:
                return v
        return None

    def recent(self, n: int = 5) -> list[dict]:
        return self.short_term[-n:]

    def summary(self) -> str:
        facts = "\n".join(f"  - {k}: {v}" for k, v in self.long_term.items())
        return f"Long-term memory:\n{facts}" if facts else "No long-term memories."


# ── Toolbox ────────────────────────────────────────────────────

@dataclass
class Toolbox:
    tools: dict[str, Callable] = field(default_factory=dict)
    schemas: dict[str, str] = field(default_factory=dict)

    def register(self, name: str, func: Callable, schema: str):
        self.tools[name] = func
        self.schemas[name] = schema

    def available(self) -> str:
        return "\n".join(f"  - {name}: {desc}" for name, desc in self.schemas.items())

    def invoke(self, name: str, **kwargs) -> str:
        if name not in self.tools:
            return f"Error: unknown tool '{name}'"
        try:
            return str(self.tools[name](**kwargs))
        except Exception as e:
            return f"Error: {e}"


# ── Planner ────────────────────────────────────────────────────

class Planner:
    """Decomposes a goal into sequential steps (mock)."""

    @staticmethod
    def decompose(goal: str) -> list[str]:
        """Simple rule-based planner — in real agent, LLM does this."""
        steps = []
        if any(w in goal.lower() for w in ["calculate", "math", "compute", "sum", "+"]):
            steps.append("Extract numbers from the query")
            steps.append("Use calculator tool to compute")
        if any(w in goal.lower() for w in ["time", "date", "when", "clock"]):
            steps.append("Check current time")
        if any(w in goal.lower() for w in ["remember", "save", "note", "store"]):
            steps.append("Store in long-term memory")
        if any(w in goal.lower() for w in ["recall", "what did", "what is my", "what's my"]):
            steps.append("Search long-term memory")
        if not steps:
            steps.append("Process the query directly")
        steps.append("Reflect on the answer before responding")
        return steps


# ── Brain (Mock LLM) ──────────────────────────────────────────

class MockBrain:
    """Simulates an LLM — pattern matches and generates responses."""

    def think(self, prompt: str, memory: Memory, toolbox: Toolbox) -> dict:
        """Returns {response: str, tool_calls: [{name, args}]}"""
        tool_calls = []
        response = ""

        lower = prompt.lower()

        # Math
        nums = [float(x) for x in re.findall(r"-?\d+\.?\d*", prompt)]
        if any(op in prompt for op in ["+", "-", "*", "/", "sum", "calculate", "compute", "total"]):
            if len(nums) >= 2:
                expr = " + ".join(str(n) for n in nums)
                tool_calls.append({"name": "calculator", "args": {"expression": expr}})

        # Time
        if any(w in lower for w in ["time", "date", "what day", "what time"]):
            tool_calls.append({"name": "clock", "args": {}})

        # Remember
        remember_match = re.search(r"remember (?:that )?(.+?)(?:\s+(?:is|=)\s+(.+))?$", lower)
        if remember_match:
            key = remember_match.group(1).strip()
            value = remember_match.group(2).strip() if remember_match.group(2) else "true"
            tool_calls.append({"name": "memorize", "args": {"key": key, "value": value}})

        # Recall
        recall_match = re.search(r"(?:what(?:'s| is) my|recall|remember)\s+(.+?)[\?]?$", lower)
        if recall_match and "remember that" not in lower:
            tool_calls.append({"name": "recall", "args": {"key": recall_match.group(1).strip()}})

        if not tool_calls and not response:
            response = f"I processed your message: '{prompt}'. As a mock brain, I can do math, tell time, and remember things for you."

        return {"response": response, "tool_calls": tool_calls}

    def reflect(self, answer: str) -> str:
        """Agent reflects on its answer to catch issues."""
        if "error" in answer.lower():
            return answer + "\n[⚠️ Reflection: Encountered an error, may need retry.]"
        if len(answer) < 5:
            return answer + "\n[💡 Reflection: Answer is very short, might need elaboration.]"
        return answer + "\n[✅ Reflection: Answer looks good.]"


# ── Agent ──────────────────────────────────────────────────────

class Agent:
    def __init__(self, name: str = "MiniAgent"):
        self.name = name
        self.memory = Memory()
        self.toolbox = Toolbox()
        self.brain = MockBrain()
        self.planner = Planner()
        self._register_default_tools()

    def _register_default_tools(self):
        self.toolbox.register(
            "calculator", self._tool_calculator,
            "Evaluate math expressions (e.g. '2 + 3 * 4')"
        )
        self.toolbox.register(
            "clock", self._tool_clock,
            "Get current date and time"
        )
        self.toolbox.register(
            "memorize", self._tool_memorize,
            "Store a key-value pair in long-term memory"
        )
        self.toolbox.register(
            "recall", self._tool_recall,
            "Retrieve a value from long-term memory"
        )

    # ── Tool implementations ──

    @staticmethod
    def _tool_calculator(expression: str = "") -> str:
        # Safe eval: only allow numbers and basic operators
        safe = re.sub(r"[^0-9+\-*/().%\s]", "", expression)
        if not safe.strip():
            return "Nothing to calculate."
        try:
            result = eval(safe)  # noqa: safe input
            return f"{safe} = {result}"
        except Exception as e:
            return f"Calculation error: {e}"

    @staticmethod
    def _tool_clock() -> str:
        now = datetime.now()
        return now.strftime("It's %A, %B %d, %Y at %I:%M %p")

    def _tool_memorize(self, key: str = "", value: str = "") -> str:
        if not key:
            return "Error: no key provided"
        self.memory.remember(key, value)
        return f"Remembered: {key} = {value}"

    def _tool_recall(self, key: str = "") -> str:
        if not key:
            return "Error: no key provided"
        val = self.memory.recall(key)
        return f"{key} = {val}" if val else f"I don't remember '{key}'"

    # ── Main loop ──

    def run(self, user_input: str) -> str:
        print(f"\n🧠 [{self.name}] Thinking...")
        self.memory.add_message("user", user_input)

        # 1. Plan
        steps = self.planner.decompose(user_input)
        print(f"📋 Plan: {steps}")

        # 2. Think (brain generates response + tool calls)
        thought = self.brain.think(user_input, self.memory, self.toolbox)

        # 3. Execute tool calls
        results = []
        for tc in thought["tool_calls"]:
            print(f"  🔧 Calling tool: {tc['name']}({tc['args']})")
            result = self.toolbox.invoke(tc["name"], **tc["args"])
            print(f"  📤 Result: {result}")
            results.append(result)

        # 4. Compose answer
        if results:
            answer = "\n".join(results)
        elif thought["response"]:
            answer = thought["response"]
        else:
            answer = "I'm not sure how to handle that."

        # 5. Reflect
        final = self.brain.reflect(answer)

        self.memory.add_message("assistant", final)
        return final


# ── REPL ───────────────────────────────────────────────────────

def main():
    agent = Agent(name="Catalyst")
    print(f"🧪 {agent.name} — Mini Agent Framework")
    print(f"Tools: {agent.toolbox.available()}")
    print(f"Type 'quit' to exit, 'memory' to see memories.\n")

    examples = [
        "What time is it?",
        "Calculate 42 + 58 + 100",
        "Remember that my favorite color is blue",
        "What is my favorite color?",
        "Remember that project deadline is April 15",
        "Recall project deadline",
    ]

    for msg in examples:
        print(f"\n👤 User: {msg}")
        reply = agent.run(msg)
        print(f"🤖 {agent.name}: {reply}")

    # Interactive loop
    print("\n" + "=" * 50)
    print("Now it's your turn! Or type 'quit'.")
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input:
            continue
        if user_input.lower() == "quit":
            break
        if user_input.lower() == "memory":
            print(agent.memory.summary())
            continue
        reply = agent.run(user_input)
        print(f"🤖 {agent.name}: {reply}")

    print(f"\n📋 Session memory:\n{agent.memory.summary()}")
    print("\n👋 Bye!")


if __name__ == "__main__":
    main()
