# 🧪 Pocket Agent

A minimal (~150 lines) AI agent framework in Python that demonstrates:
- **Tool use** - register and call tools with JSON schema validation
- **ReAct loop** - Reason → Act → Observe cycle
- **Memory** - short-term conversation + long-term vector-like retrieval
- **Streaming thoughts** - see the agent think in real-time

No external LLM API needed — includes a **mock LLM backend** for demonstration.
Swap in `openai.ChatCompletion` or any API with one function change.

## Quick Start

```bash
python pocket_agent.py
```

## Concepts Demonstrated

1. **Tool Registry** - Functions auto-registered with type hints → JSON Schema
2. **ReAct Loop** - Agent reasons, picks tools, observes results, repeats
3. **Episodic Memory** - Stores important observations for later retrieval
4. **Guard Rails** - Max iterations, tool timeout, output validation

## Extend It

- Replace `MockLLM` with real API calls
- Add your own tools with `@agent.tool`
- Connect to MCP servers
- Add persistence (sqlite/jsonl)
