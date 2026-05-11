# Nano-Agent Architecture

> Design decisions and internal structure of the Nano-Agent framework.
> Core: 643 lines across 5 modules. Zero external dependencies for the core.

---

## Design Philosophy

**"Remove everything until it breaks, then add back only what's essential."**

Nano-Agent is built on three constraints:
1. **Core < 500 lines** — the entire framework fits in a single screen of file list
2. **Zero hard dependencies** — `pip install -r requirements.txt` is empty for core (openai optional)
3. **Readable in one sitting** — a developer should understand the whole system in <30 minutes

---

## Module Map

```
nano_agent/
├── __init__.py     (11 lines)   — Public API exports
├── agent.py        (179 lines)  — Agent orchestrator, loop, system prompt builder
├── tools.py        (131 lines)  — @tool decorator, Tool dataclass, global registry
├── memory.py       (160 lines)  — In-memory + file-backed Memory with keyword search
└── llm.py          (162 lines)  — LLMBackend ABC, OpenAIBackend, MockBackend, LLM facade
```

### Dependency Graph

```
agent.py ──→ tools.py    (Tool.to_dict for LLM function calling)
        ──→ memory.py   (Memory.add, .to_context for prompt enrichment)
        ──→ llm.py      (LLM.chat for inference)

tools.py   — standalone (no imports from other modules)
memory.py  — standalone (uses only stdlib: json, datetime, pathlib)
llm.py     — standalone (openai is optional import)
```

Each module is independently testable with no circular dependencies.

---

## Core Execution Loop

```python
Agent.run(user_input, context=None):
  1. Build messages: [system_prompt] + conversation_history[-10:] + [user_input]
  2. For each iteration (up to max_iterations):
     a. LLM.chat(messages, tools) → response
     b. If tool_calls in response:
        - Execute each tool → append tool result message
        - Continue loop
     c. If no tool_calls:
        - Final response found → break
  3. Save interaction to Memory
  4. Return final response text
```

**Key design choices:**
- **Tool calls = continue loop.** The agent keeps iterating until the LLM produces a response without tool calls (i.e., it's done reasoning).
- **max_iterations guard rail.** Prevents infinite loops. Default 10.
- **Conversation history is in-memory only.** `_conversation_history` accumulates per-session, recent 10 messages injected into each prompt. Call `agent.reset()` to clear.

---

## System Prompt Construction

The system prompt is built fresh each call via `_build_system_prompt()`:

```
1. Agent name + instructions
2. Tool list (name + description)
3. Optional context parameter
4. Recent memory entries (Memory.to_context, capped at max_tokens)
5. Workflow instructions (understand → analyze → tool call → synthesize)
```

This means memory is always fresh in the prompt — no stale cache issues.

---

## Tool System

### Registration Flow

```
@tool decorator on a function
  → inspect.signature() extracts parameter names, types, defaults
  → Tool dataclass created with name, description, parameters schema
  → Registered in global _tools dict
  → Tool object attached to function._nano_agent_tool
```

### Tool → LLM Schema

`Tool.to_dict()` produces the function calling schema passed to the LLM:

```python
{
    "name": "search",
    "description": "搜索网络获取信息",
    "parameters": {
        "query": {"type": "string"},
        "limit": {"type": "integer", "default": 5}
    }
}
```

In `agent.py`, this is wrapped in OpenAI's tool format before sending to the LLM backend.

### Execution

When the LLM returns a tool call, `_execute_tool()`:
1. Parses `arguments` JSON string
2. Looks up tool by name in `self.tools`
3. Calls `tool.execute(**arguments)`
4. Returns string result (or error message)

**No sandboxing** — tools run in the same process with full access. This is intentional for simplicity. For production use, wrap tool functions with appropriate guards.

---

## Memory System

### Storage Model

- **In-memory:** `List[MemoryEntry]` — append-only, FIFO eviction at `max_entries`
- **Optional persistence:** JSON file at `persistence_path`, auto-saved on every `add/remove/update/clear`

### Retrieval

- `search(query, limit, tags)` — case-insensitive keyword match + optional tag filter, returns most recent matches
- `get_recent(n)` — last N entries (for context injection)
- `to_context(max_tokens)` — formats recent entries for prompt injection, truncated by byte size

### Memory in the Loop

Memory is **read-only during a run** — it's injected into the system prompt at the start. New interactions are written to memory after the agent completes. This avoids self-referential loops.

---

## LLM Backend

### Architecture

```
LLM (facade)
  ├── .openai(api_key, base_url, model) → OpenAIBackend
  └── .mock()                           → MockBackend

LLMBackend (ABC)
  └── .complete(messages, tools) → {"content", "tool_calls", "usage"}
```

### Adding a Custom Backend

Subclass `LLMBackend` and implement `complete()`:

```python
from nano_agent.llm import LLMBackend, LLM

class MyBackend(LLMBackend):
    def complete(self, messages, tools=None, **kwargs):
        # Call your LLM API
        return {
            "content": "response text",
            "tool_calls": [{"id": "1", "name": "tool_name", "arguments": "{}"}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        }

agent = Agent(name="test", instructions="...", llm=LLM(MyBackend()))
```

The contract is minimal: return a dict with `content` (str), `tool_calls` (list), and `usage` (dict).

---

## Data Flow Diagram

```
User Input
    │
    ▼
┌─────────┐    system prompt     ┌─────────┐
│  Agent   │────────────────────→│   LLM   │
│          │←────────────────────│ Backend  │
│          │   {content, calls}  └─────────┘
│          │
│          │── if tool_calls ──→ Tool.execute()
│          │←── result ──────────
│          │
│          │── loop back to LLM with tool results
│          │
│          │── no tool_calls ──→ final response
│          │
└────┬─────┘
     │
     ▼
  Memory.add(interaction)
     │
     ▼
  Return response to user
```

---

## Extension Points

| Extension | How | Where |
|-----------|-----|-------|
| Custom LLM | Subclass `LLMBackend` | `llm.py` |
| Custom tool | `@tool` decorator or `Tool(...)` | `tools.py` |
| Custom memory | Subclass `Memory` or replace | `memory.py` |
| Step callback | `agent.on_step = callback` | `agent.py` |
| Pre/post hooks | Wrap `agent.run()` | User code |

---

## Limitations (By Design)

- **Single-agent only** — no multi-agent orchestration (use CrewAI/AutoGen for that)
- **No streaming** — `run()` blocks until complete
- **Keyword search only** — no vector/semantic search in memory
- **No rate limiting** — tools execute immediately
- **No sandboxing** — tools have full process access

These are intentional tradeoffs for keeping the core under 500 lines.

---

*Last updated: 2026-05-11*
*Source: src/nano_agent/ (643 lines total)*
