#!/usr/bin/env python3
"""
🧪 Pocket Agent — A minimal AI Agent framework in ~120 lines.

Demonstrates the core Agent loop: Observe → Think → Act
with a pluggable tool system. Zero external dependencies for the framework itself.

Usage:
  python pocket_agent.py                    # Interactive mode
  python pocket_agent.py "list files in ."  # One-shot mode

Set OPENAI_API_KEY (or compatible) to use real LLM.
Without it, runs in DEMO mode with a mock brain.
"""

import json, os, sys, subprocess, traceback
from datetime import datetime

# ── Tool Registry ────────────────────────────────────────────────

TOOLS = {}

def tool(name, description):
    """Decorator to register a tool."""
    def decorator(fn):
        TOOLS[name] = {"fn": fn, "description": description, "name": name}
        return fn
    return decorator

# ── Built-in Tools ───────────────────────────────────────────────

@tool("calculator", "Evaluate a math expression. Input: expression string")
def calc(expr: str) -> str:
    try:
        result = eval(expr, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"

@tool("read_file", "Read file contents. Input: file path")
def read_file(path: str) -> str:
    try:
        with open(path, 'r') as f:
            return f.read()[:2000]
    except Exception as e:
        return f"Error: {e}"

@tool("run_shell", "Run a shell command and return output. Input: command string")
def run_shell(cmd: str) -> str:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        output = r.stdout[:1500]
        if r.stderr:
            output += f"\nSTDERR: {r.stderr[:500]}"
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: command timed out (10s)"
    except Exception as e:
        return f"Error: {e}"

# ── Agent Brain ──────────────────────────────────────────────────

class PocketAgent:
    """The core agent: maintains conversation + routes tool calls."""

    def __init__(self, system_prompt: str = None):
        self.tools = TOOLS
        self.history = []
        self.system = system_prompt or (
            "You are Pocket Agent, a helpful AI assistant. "
            "Use tools when needed. Reply in JSON with 'thought' and either 'action' "
            "(with 'tool' and 'input') or 'answer' (final response to user).\n\n"
            "Available tools:\n"
            + "\n".join(f"- {t['name']}: {t['description']}" for t in TOOLS.values())
        )

    def think(self, user_input: str, max_steps: int = 5) -> str:
        """Run the agent loop: think → act → observe until answer."""
        self.history.append({"role": "user", "content": user_input})
        prompt = self._build_prompt()

        for step in range(max_steps):
            print(f"\n  🤔 Step {step + 1}...", flush=True)
            response = self._call_llm(prompt)

            try:
                parsed = json.loads(response)
            except json.JSONDecodeError:
                return response  # Plain text response

            thought = parsed.get("thought", "")
            print(f"  💭 {thought}", flush=True)

            if "answer" in parsed:
                self.history.append({"role": "assistant", "content": parsed["answer"]})
                return parsed["answer"]

            if "action" in parsed:
                action = parsed["action"]
                tool_name = action.get("tool")
                tool_input = action.get("input", "")

                if tool_name not in self.tools:
                    observation = f"Error: unknown tool '{tool_name}'"
                else:
                    print(f"  🔧 {tool_name}({tool_input})", flush=True)
                    observation = self.tools[tool_name]["fn"](tool_input)

                print(f"  👁️  {observation[:200]}", flush=True)
                self.history.append({"role": "observation", "content": observation})
                prompt += '\nObservation: ' + observation + '\n\nNow respond with a final answer in JSON: {"thought": "...", "answer": "..."}\n'

        return "(max steps reached)"

    def _build_prompt(self) -> str:
        lines = [self.system, ""]
        for msg in self.history[-6:]:  # Keep last 6 messages
            role = "User" if msg["role"] == "user" else "Assistant"
            lines.append(f"{role}: {msg['content']}")
        lines.append("\nRespond in JSON: {\"thought\": \"...\", \"action\": {\"tool\": \"...\", \"input\": \"...\"}} or {\"thought\": \"...\", \"answer\": \"...\"}\n")
        return "\n".join(lines)

    def _call_llm(self, prompt: str) -> str:
        """Call LLM API or fall back to demo mode."""
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return self._demo_brain(prompt)

        import urllib.request
        url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1") + "/chat/completions"
        body = json.dumps({
            "model": os.environ.get("MODEL", "gpt-4o-mini"),
            "messages": [{"role": "system", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 500,
        }).encode()

        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f'{{"thought": "API error, falling back", "answer": "API call failed: {e}. Running in demo mode."}}'

    def _demo_brain(self, prompt: str) -> str:
        """Offline demo brain — pattern matches user input to demonstrate tool use."""
        last_user = ""
        for msg in reversed(self.history):
            if msg["role"] == "user":
                last_user = msg["content"].lower()
                break

        # Check if we just got an observation — answer from it
        if "Observation:" in prompt.split("User:")[-1] or (self.history and self.history[-1]["role"] == "observation"):
            # We already acted, now answer
            obs = self.history[-1]["content"] if self.history[-1]["role"] == "observation" else ""
            return json.dumps({"thought": "Got observation, answering now", "answer": f"Here's what I found:\n{obs}"})

        if any(w in last_user for w in ["calc", "compute", "math", "what is", "计算"]):
            import re
            # Extract from original (not lowered) to preserve format
            original = self.history[-1]["content"]
            expr_match = re.search(r'[\d][\d+\-*/ ().]+[\d)]', original)
            expr = expr_match.group(0).strip() if expr_match else "2+2"
            return json.dumps({"thought": "User wants math, using calculator", "action": {"tool": "calculator", "input": expr}})

        if any(w in last_user for w in ["file", "read", "文件", "cat"]):
            return json.dumps({"thought": "Listing files first", "action": {"tool": "run_shell", "input": "ls -la"}})

        if any(w in last_user for w in ["list", "ls", "dir", "show", "列出"]):
            return json.dumps({"thought": "Listing files", "action": {"tool": "run_shell", "input": "ls -la"}})

        if any(w in last_user for w in ["time", "date", "时间", "几点"]):
            return json.dumps({"thought": "Checking current time", "answer": f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 🕐"})

        if any(w in last_user for w in ["who", "what are you", "你是"]):
            return json.dumps({"thought": "Introducing myself", "answer": "I'm Pocket Agent 🧪 — a minimal AI agent in ~120 lines of Python. I can use tools (calculator, file reader, shell) to help you!"})

        return json.dumps({"thought": "General response", "answer": f"Hi! I'm Pocket Agent 🧪\nI heard: \"{self.history[-1]['content']}\"\n\nTry asking me to: calculate something, list files, read a file, or check the time!\n(With OPENAI_API_KEY set, I get much smarter 😄)"})


# ── CLI ──────────────────────────────────────────────────────────

def main():
    agent = PocketAgent()

    print("╔══════════════════════════════════════╗")
    print("║  🧪 Pocket Agent v0.1                ║")
    print("║  Minimal AI Agent Framework          ║")
    print("╚══════════════════════════════════════╝")

    has_api = bool(os.environ.get("OPENAI_API_KEY"))
    print(f"  Brain: {'LLM API ✅' if has_api else 'Demo Mode (set OPENAI_API_KEY for real AI)'}")
    print(f"  Tools: {', '.join(TOOLS.keys())}")
    print()

    if len(sys.argv) > 1:
        # One-shot mode
        query = " ".join(sys.argv[1:])
        print(f"  📨 {query}")
        result = agent.think(query)
        print(f"\n  ✅ {result}")
        return

    # Interactive mode
    print("  Type 'quit' to exit, 'tools' to list tools.\n")
    while True:
        try:
            query = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Bye! 👋")
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            print("  Bye! 👋")
            break
        if query.lower() == "tools":
            for t in TOOLS.values():
                print(f"  - {t['name']}: {t['description']}")
            continue

        result = agent.think(query)
        print(f"\n  ✅ {result}\n")


if __name__ == "__main__":
    main()
