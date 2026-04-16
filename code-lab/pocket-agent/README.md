# 🧪 Pocket Agent

A minimal AI Agent framework in ~130 lines of Python. Demonstrates the core ReAct loop (Observe → Think → Act) with a pluggable tool system.

## Features

- **ReAct Loop**: Think → Act → Observe, complete cycle
- **Tool Registry**: Decorator-based, hot-pluggable tools
- **3 Built-in Tools**: Calculator, File Reader, Shell Executor
- **Dual Mode**: Demo mode (zero deps) or real LLM via OpenAI-compatible API
- **Interactive & One-shot**: Use as REPL or CLI

## Quick Start

```bash
# Demo mode (no API key needed)
python3 pocket_agent.py "who are you"
python3 pocket_agent.py "what is 42*17+3"
python3 pocket_agent.py "list files"
python3 pocket_agent.py "几点了"

# Interactive mode
python3 pocket_agent.py

# With real LLM
OPENAI_API_KEY=sk-xxx python3 pocket_agent.py "explain quantum computing"
```

## Adding Tools

```python
@tool("my_tool", "Description of what it does. Input: expected input")
def my_tool(input: str) -> str:
    # Your implementation
    return "result"
```

That's it. The agent automatically discovers new tools.

## Architecture

```
User Input → Agent.think()
                ↓
            Call LLM / Demo Brain
                ↓
         Parse JSON response
           ↙          ↘
     Has "action"    Has "answer"
         ↓               ↓
    Execute tool      Return result
         ↓
    Add observation
         ↓
    Loop back to LLM
```

## Extending

- Swap `_call_llm()` for any LLM provider
- Add tools for web search, database, API calls
- Add memory/persistence across sessions
- Multi-agent orchestration

---

*Created in Code Lab Evening Session — 2026-03-31*
