# Agent Framework Integration for OpenClaw

> Integrating CrewAI and LangGraph multi-agent frameworks with OpenClaw

**Status**: 🚧 Prototype Phase
**Author**: Catalyst 🧪
**Date**: 2026-04-13

---

## Overview

This package provides adapters that bridge **CrewAI** and **LangGraph** multi-agent frameworks with **OpenClaw's** agent orchestration capabilities. It enables building complex, stateful workflows with multiple AI agents while leveraging OpenClaw's process management and tooling.

### What This Provides

✅ **CrewAI Adapter** - Role-based agent orchestration
✅ **LangGraph Adapter** - Stateful graph-based workflows
✅ **OpenClaw Integration** - Seamless connection to OpenClaw's agent spawning
✅ **Examples** - Working demonstrations of both frameworks
✅ **Documentation** - Complete reference and comparison guide

---

## Quick Start

### 1. Install Dependencies

```bash
cd ~/.openclaw/workspace/agent-framework-integration
pip install -r requirements.txt  # If exists
```

### 2. Run Examples

**CrewAI Example** (Content Creation Pipeline):
```bash
python examples/content_pipeline_crewai.py
```

**LangGraph Example** (Customer Support Triage):
```bash
python examples/customer_support_langgraph.py
```

### 3. Use in Your Code

```python
# CrewAI-style
from crewai.adapter import OpenClawCrew, OpenClawAgentConfig

crew = OpenClawCrew(name="My Team")
crew.add_task("task1", "Do research", researcher_agent)
result = await crew.kickoff()
```

```python
# LangGraph-style
from langgraph.adapter import StateGraph, create_openclaw_node

graph = StateGraph()
graph.add_node("process", create_openclaw_node(
    name="process",
    prompt_template="Process: {task}",
    agent_type="codex"
))
compiled = graph.compile()
result = await compiled.invoke({"messages": ["Hello"]})
```

---

## Directory Structure

```
agent-framework-integration/
├── README.md                 # This file
├── FRAMEWORK_COMPARISON.md  # Detailed comparison of CrewAI vs LangGraph
├── docs/
│   └── RESEARCH.md          # Research findings and analysis
├── crewai/
│   └── adapter.py           # CrewAI to OpenClaw adapter
├── langgraph/
│   └── adapter.py           # LangGraph to OpenClaw adapter
└── examples/
    ├── content_pipeline_crewai.py      # CrewAI example
    └── customer_support_langgraph.py   # LangGraph example
```

---

## Framework Comparison

| Feature | CrewAI | LangGraph |
|---------|--------|-----------|
| **Philosophy** | Role-playing teams | Stateful graphs |
| **Learning Curve** | ⭐⭐ Easy | ⭐⭐⭐⭐ Moderate |
| **Best For** | Role-based workflows | Complex stateful workflows |
| **State Management** | Implicit | Explicit |
| **Conditional Routing** | Limited | Powerful |
| **Boilerplate** | Low | Moderate |

**Quick Rule:**
- Use **CrewAI** for team-like collaboration (researcher → writer → editor)
- Use **LangGraph** for process flows (classify → route → resolve → notify)

See [FRAMEWORK_COMPARISON.md](FRAMEWORK_COMPARISON.md) for detailed analysis.

---

## CrewAI Adapter

### Key Components

- **OpenClawCrew** - Orchestrator for multiple agents
- **OpenClawAgentConfig** - Configuration for agent sessions
- **OpenClawTask** - Task definition with dependencies

### Example

```python
from crewai.adapter import OpenClawCrew, OpenClawAgentConfig

# Create agents
researcher = OpenClawAgentConfig(name="Researcher", agent_type="codex", pty=True)
writer = OpenClawAgentConfig(name="Writer", agent_type="claude")

# Build crew
crew = OpenClawCrew(name="Content Team", verbose=True)

# Add tasks with dependencies
crew.add_task("research", "Research AI trends", researcher,
              output_file="output/research.json")
crew.add_task("write", "Write article", writer,
              depends_on=["research"],
              output_file="output/article.md")

# Execute
result = await crew.kickoff(process="sequential")
```

### Capabilities

✅ Sequential and parallel execution
✅ Task dependency management
✅ Output file persistence
✅ Rate limiting
✅ Error handling
✅ Progress logging

---

## LangGraph Adapter

### Key Components

- **StateGraph** - Graph builder
- **Node** - Work unit (function or agent)
- **Edge** - Connection between nodes
- **OpenClawAgentNode** - Node that runs OpenClaw agent

### Example

```python
from langgraph.adapter import StateGraph, create_openclaw_node, START, END

# Build graph
graph = StateGraph()

# Add nodes
graph.add_node("classify", classify_function)
graph.add_node("technical", create_openclaw_node(
    name="technical", prompt_template="Help: {task}", agent_type="codex"
))
graph.add_node("billing", create_openclaw_node(
    name="billing", prompt_template="Billing: {task}", agent_type="claude"
))

# Connect with conditional routing
graph.add_edge(START, "classify")
graph.add_conditional_edges("classify", route_function, {
    "technical": "technical",
    "billing": "billing"
})
graph.add_edge("technical", END)
graph.add_edge("billing", END)

# Execute
compiled = graph.compile()
result = await compiled.invoke({"messages": ["I have a billing question"]})
```

### Capabilities

✅ Explicit state management
✅ Conditional routing
✅ Parallel execution
✅ Cycles and loops
✅ Checkpointing (for resume)
✅ Streaming execution

---

## OpenClaw Integration

### Current Status (Prototype)

The adapters currently **simulate** OpenClaw integration. In production, they will:

1. Use `exec` tool to spawn agent processes
2. Use `process` tool to monitor sessions
3. Use `subagents` tool for management

### Integration Points

```python
# Simulated (current)
result = await self._simulate_execution(command, config)

# Production (planned)
session_id = await exec_tool.spawn_agent(
    agent_type=config.agent_type,
    prompt=prompt,
    pty=config.pty
)
result = await process_tool.wait(session_id)
```

---

## Examples

### 1. Content Creation Pipeline (CrewAI)

**File:** `examples/content_pipeline_crewai.py`

**Workflow:**
1. Researcher finds trending topics
2. Writer creates article outline
3. Writer writes full draft
4. Editor reviews and provides feedback
5. Writer incorporates feedback and finalizes

**Run:**
```bash
python examples/content_pipeline_crewai.py
```

### 2. Customer Support Triage (LangGraph)

**File:** `examples/customer_support_langgraph.py`

**Workflow:**
1. Classify issue type (technical/billing/feature)
2. Route to appropriate specialist
3. Resolve issue
4. Check if escalation needed
5. Send follow-up to customer

**Run:**
```bash
python examples/customer_support_langgraph.py
```

---

## Documentation

- **[Research Document](docs/RESEARCH.md)** - In-depth research on CrewAI and LangGraph
- **[Comparison Guide](FRAMEWORK_COMPARISON.md)** - Detailed comparison and use case analysis
- **[Agent Orchestrator Skill](../skills/agent-orchestrator/SKILL.md)** - User-facing skill documentation

---

## Architecture

```
┌─────────────────────────────────────────┐
│         User / Application              │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     Agent Orchestrator Skill            │
│     (High-level API)                    │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴───────┐
       │               │
┌──────▼──────┐  ┌─────▼──────┐
│  CrewAI     │  │  LangGraph │
│  Adapter    │  │  Adapter   │
└──────┬──────┘  └─────┬──────┘
       │               │
       └───────┬───────┘
               │
┌──────────────▼──────────────────────────┐
│         OpenClaw Core                   │
│  (exec, process, subagents tools)       │
└─────────────────────────────────────────┘
```

---

## Use Cases

### When to Use CrewAI

✅ **Role-based workflows** - Clear specialist roles
✅ **Simple to moderate complexity** - Sequential flows
✅ **Quick prototyping** - Get started fast
✅ **Tool-heavy tasks** - Need rich tool ecosystem

**Examples:**
- Research team (researcher → writer → editor)
- Content pipeline (idea → outline → draft → publish)
- Data analysis (extract → analyze → report)

### When to Use LangGraph

✅ **Complex stateful workflows** - Multi-step with branching
✅ **Explicit state management** - Need to track data flow
✅ **Cyclic workflows** - Loops, retries, conditional paths
✅ **Production systems** - Robust error handling

**Examples:**
- Customer support triage (classify → route → resolve → follow up)
- Approval workflow (submit → review → approve/reject → notify)
- Data pipeline (extract → validate → transform → load → monitor)

### When to Use OpenClaw Native

✅ **Simple one-off tasks** - No framework overhead
✅ **Channel integration** - Discord bots, Feishu workflows
✅ **CLI agents** - Codex, Claude Code, Pi integration

**Examples:**
- "Review this PR"
- "Fix this bug"
- "Generate documentation"

---

## Current Limitations

⚠️ **Prototype Status**

1. **Simulated Execution**: Adapters simulate agent execution; production needs real OpenClaw tool calls
2. **Python-Only**: Currently only Python workflows supported
3. **In-Memory State**: State not persisted; requires external store for production
4. **Limited Observability**: Basic logging; needs integration with OpenClaw telemetry
5. **No Web UI**: Workflow visualization not yet implemented

---

## Future Roadmap

### Phase 1: Production Integration (Week 1-2)
- [ ] Real OpenClaw tool integration (exec, process, subagents)
- [ ] State persistence with Redis
- [ ] Enhanced error handling and recovery
- [ ] Integration testing

### Phase 2: Advanced Features (Week 3-4)
- [ ] Workflow templates library
- [ ] Real-time monitoring dashboard
- [ ] Web UI for workflow visualization
- [ ] Integration with OpenClaw channels (Feishu, Discord)

### Phase 3: Ecosystem (Week 5-6)
- [ ] Community workflow library
- [ ] Workflow versioning and rollback
- [ ] A/B testing framework
- [ ] Performance analytics

---

## Development

### Running Tests

```bash
# Run all examples
cd ~/.openclaw/workspace/agent-framework-integration
python examples/content_pipeline_crewai.py
python examples/customer_support_langgraph.py
```

### Adding New Examples

1. Create new file in `examples/` directory
2. Follow existing example structure
3. Use adapters from `crewai/` or `langgraph/`
4. Add comments explaining the workflow
5. Update this README with example description

### Extending Adapters

**CrewAI Adapter:**
- Edit `crewai/adapter.py`
- Add new methods to `OpenClawCrew` class
- Update `OpenClawAgentConfig` if needed

**LangGraph Adapter:**
- Edit `langgraph/adapter.py`
- Extend `StateGraph` or `CompiledGraph` classes
- Add new node types or edge types

---

## Contributing

Contributions welcome! Areas to help:

1. **Real OpenClaw Integration** - Replace simulated execution with actual tool calls
2. **More Examples** - Add workflow examples for different use cases
3. **Documentation** - Improve guides and API docs
4. **Testing** - Add unit and integration tests
5. **Performance** - Optimize for large workflows

---

## Related Work

- **OpenClaw Coding Agent Skill**: `~/.openclaw/workspace/skills/coding-agent/SKILL.md`
- **Agent Task Orchestrator**: `~/.openclaw/workspace/tools/agent-task-orchestrator/`
- **Agent Framework Manager**: `~/.openclaw/workspace/tools/agent-framework-manager/`
- **Voice-Driven Agent Orchestration**: `~/.openclaw/workspace/catalyst-research/exploration-notes/2026-04-02-voice-driven-agent-orchestration.md`

---

## References

- **CrewAI**: https://docs.crewai.com
- **LangGraph**: https://langchain-ai.github.io/langgraph
- **OpenClaw**: https://docs.openclaw.ai

---

## License

Part of OpenClaw workspace. See main repository for license details.

---

**Built with 🧪 by Catalyst**

For questions or issues, check the documentation or create an issue in the main repository.
