# Multi-Agent Framework Research: CrewAI & LangGraph

> Research Date: 2026-04-13
> Focus: Integration with OpenClaw agent orchestration

## 1. CrewAI Framework

### 1.1 Core Concepts

**Architecture Philosophy**: Role-playing agents collaborating in structured workflows

**Key Components**:

1. **Agents**
   - `role`: Agent's position and responsibility
   - `goal`: What the agent aims to achieve
   - `backstory`: Context that influences behavior
   - `tools`: External capabilities (web search, APIs, etc.)
   - `llm`: Language model specification

```python
from crewai import Agent

researcher = Agent(
    role='Senior Researcher',
    goal='Uncover groundbreaking technologies',
    backstory='Driven by curiosity, exploring innovations',
    tools=[SerperDevTool()],
    llm=cerebras_llm
)
```

2. **Tasks**
   - `description`: What needs to be done
   - `expected_output`: Format of the result
   - `agent`: Which agent handles it
   - `output_file`: Where to save results
   - `async_execution`: Parallel execution support
   - `guardrail`: Output validation

```python
from crewai import Task

research_task = Task(
    description='Identify the next big trend',
    expected_output='A 3-paragraph report',
    agent=researcher,
    output_file='reports/trend_analysis.md'
)
```

3. **Crews**
   - Collection of agents working together
   - Defines execution strategy and workflow
   - Handles agent coordination

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # or Process.hierarchical
    max_rpm=3,
    cache=True
)
```

4. **Flows** (New in CrewAI 2.0)
   - Structured, event-driven workflows
   - Manage state and control execution
   - Trigger crews as needed
   - Production-ready scaffolding

### 1.2 Execution Models

**Sequential Process**:
- Tasks execute in order
- Each task receives previous task's output
- Simple, predictable flow

**Hierarchical Process**:
- Manager agent coordinates
- Delegates to specialist agents
- Dynamic task assignment

**Key Features**:
- Autonomous inter-agent delegation
- Modular tool integration
- Async execution support
- Built-in caching and rate limiting
- Guardrails for output validation

### 1.3 Advantages

✅ **Role-based design** - Easy to understand agent responsibilities
✅ **Tool integration** - Rich ecosystem of tools
✅ **Simple API** - Minimal boilerplate
✅ **Async support** - Efficient parallel execution
✅ **Production-ready** - Flows provide structure for real apps
✅ **Open source** - Full control and extensibility

### 1.4 Limitations

❌ **Python-only** - Limited to Python ecosystem
❌ **Learning curve** - CrewAI 2.0 flows add complexity
❌ **State management** - Less explicit than LangGraph
❌ **Tool dependencies** - Requires tool ecosystem buy-in

---

## 2. LangGraph Framework

### 2.1 Core Concepts

**Architecture Philosophy**: Stateful, message-passing graphs

**Key Components**:

1. **State**
   - Shared data structure between nodes
   - Represents application snapshot
   - Passed along edges
   - Can be any Python structure (TypedDict, Pydantic)

```python
from typing_extensions import TypedDict

class State(TypedDict):
    messages: list
    count: int
    analysis: dict
```

2. **Nodes**
   - Units of work (functions, agents, LLM calls)
   - Receive state, return state updates
   - Can be simple functions or complex agents

```python
from langgraph.graph import StateGraph

def research_node(state: State) -> dict:
    # Perform research
    return {"messages": [research_result]}

def analysis_node(state: State) -> dict:
    # Analyze results
    return {"analysis": analysis_data}
```

3. **Edges**
   - Communication channels between nodes
   - Define execution flow
   - Can be unconditional or conditional

```python
# Unconditional edge
graph.add_edge("research", "analysis")

# Conditional edge (routing)
def route_next(state: State) -> str:
    if state["count"] > 10:
        return "finish"
    return "continue"

graph.add_conditional_edges(
    "check",
    route_next,
    {"continue": "work", "finish": END}
)
```

4. **Graph**
   - StateGraph builder
   - Compiles to executable graph
   - Supports cycles, parallelism, branching

```python
from langgraph.graph import START, END

graph_builder = StateGraph(State)
graph_builder.add_node("research", research_node)
graph_builder.add_node("analysis", analysis_node)
graph_builder.add_edge(START, "research")
graph_builder.add_edge("research", "analysis")
graph_builder.add_edge("analysis", END)

graph = graph_builder.compile()
```

### 2.2 Execution Patterns

**Sequential Flow**:
```python
graph_builder.add_sequence([step1, step2, step3])
```

**Parallel Execution**:
```python
# Multiple nodes can run in parallel
graph_builder.add_edge(START, ["node1", "node2", "node3"])
graph_builder.add_edge(["node1", "node2", "node3"], "merge")
```

**Cycles and Loops**:
```python
# Condition-based loops
def should_continue(state: State) -> str:
    return "continue" if not state["done"] else "end"

graph.add_conditional_edges("work", should_continue)
```

**Node Metadata**:
```python
graph.add_node(
    "expensive_operation",
    my_node,
    metadata={
        "cost": "high",
        "timeout": 30,
        "version": "2.0"
    }
)
```

### 2.3 Advanced Features

**State Management**:
- Typed state with Pydantic
- Message history tracking
- Partial state updates
- State reducers (add_messages)

**Control Flow**:
- Conditional routing
- Parallel execution
- Cycles and loops
- Error handling

**Integration**:
- LangChain ecosystem
- Custom LLMs
- Tool calling
- Observability (tracing)

### 2.4 Advantages

✅ **Explicit state** - Clear data flow between nodes
✅ **Flexible control** - Complex workflows with branching/looping
✅ **Type safety** - Pydantic validation
✅ **LangChain integration** - Leverages existing ecosystem
✅ **Visual debugging** - Graph visualization
✅ **Async support** - Built-in async execution
✅ **Production-ready** - Robust error handling

### 2.5 Limitations

❌ **Steeper learning curve** - Graph concepts require understanding
❌ **Verbosity** - More boilerplate than CrewAI
❌ **Python-only** - Limited to Python
❌ **LangChain dependency** - Tied to LangChain ecosystem

---

## 3. OpenClaw Current Multi-Agent Capabilities

### 3.1 Built-in Tools

**subagents** tool:
- `list`: List running sub-agent sessions
- `kill`: Terminate a sub-agent
- `steer`: Send messages to guide sub-agents
- Push-based completion notification

**sessions_spawn** (via CLI):
- Spawn agents in background
- Different runtime modes (acp, etc.)
- Channel-based communication

**exec** with background mode:
- Spawn any CLI agent (Codex, Claude Code, Pi)
- PTY support for interactive agents
- Process management via `process` tool

### 3.2 Existing Tools in Workspace

**agent-task-orchestrator** (`/root/.openclaw/workspace/tools/agent-task-orchestrator/`):
- JSON-based task orchestration
- Dependency management
- Sequential/parallel execution
- Shell/agent/function task types
- CLI interface (`ato` command)

**agent-framework-manager** (`/root/.openclaw/workspace/tools/agent-framework-manager/`):
- Manages multiple agent frameworks
- Binaries and libraries for framework integration

### 3.3 Strengths

✅ **Native integration** - Built into OpenClaw core
✅ **Simple API** - subagents tool is easy to use
✅ **Background execution** - Long-running tasks supported
✅ **Channel integration** - Feishu, Discord, etc.
✅ **Multi-framework** - Supports various agents (Codex, Claude Code, Pi)

### 3.4 Gaps

❌ **No high-level orchestration** - Manual coordination required
❌ **No state management** - Each agent is isolated
❌ **No task dependencies** - Can't express complex workflows
❌ **No visual debugging** - Hard to understand agent interactions
❌ **No reusable patterns** - Each workflow built from scratch

---

## 4. Integration Opportunities

### 4.1 Why Integrate CrewAI/LangGraph?

1. **High-level orchestration** - Declarative workflows vs. imperative spawning
2. **State management** - Shared context between agents
3. **Reusable patterns** - Crew templates, graph blueprints
4. **Better observability** - Tracing, visualization
5. **Production readiness** - Battle-tested frameworks

### 4.2 Integration Approaches

**Approach 1: Wrapper Pattern**
- Use OpenClaw's `subagents` as backend
- CrewAI/LangGraph orchestrates via wrapper
- Agents communicate through OpenClaw

**Approach 2: Adapter Pattern**
- Map CrewAI agents → OpenClaw sessions
- Map LangGraph nodes → OpenClaw processes
- Leverage OpenClaw's tooling

**Approach 3: Hybrid Pattern**
- CrewAI/LangGraph for workflow definition
- OpenClaw for execution and channel integration
- Best of both worlds

### 4.3 Recommended Approach

**Hybrid Pattern** with these layers:

```
┌─────────────────────────────────────┐
│   User/Channel (Feishu, Discord)   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   OpenClaw Agent Orchestrator       │
│   (SKILL.md - High-level API)       │
└──────────────┬──────────────────────┘
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
┌──────────────▼──────────────────────┐
│   OpenClaw Core (subagents, exec)  │
│   Spawn processes, manage sessions │
└─────────────────────────────────────┘
```

---

## 5. Use Case Analysis

### 5.1 CrewAI Best For

- **Role-based workflows** - Clearly defined specialist roles
- **Simple to moderate complexity** - Sequential or simple hierarchical flows
- **Tool-heavy workflows** - Need rich tool ecosystem
- **Quick prototyping** - Minimal setup, fast iteration
- **Team collaboration** - Agents "working together" metaphor

**Example**: Research team (researcher → writer → reviewer)

### 5.2 LangGraph Best For

- **Complex stateful workflows** - Multi-step processes with branching
- **Explicit state management** - Need to track complex data flow
- **Cyclic workflows** - Loops, retries, conditional paths
- **Production systems** - Robust error handling, observability
- **LangChain ecosystem** - Already using LangChain tools

**Example**: Customer support triage (classify → route → resolve → follow up)

### 5.3 OpenClaw Native Best For

- **Simple one-off tasks** - Spawn agent, get result
- **Channel integration** - Discord bots, Feishu workflows
- **CLI agents** - Codex, Claude Code, Pi integration
- **Lightweight orchestration** - Don't need full framework overhead

**Example**: "Review this PR" → spawn Codex in background

---

## 6. Implementation Priorities

### Phase 1: Core Adapters (Week 1)
1. CrewAI adapter
   - Agent → OpenClaw session mapping
   - Task execution via subagents
   - Basic sequential crew support

2. LangGraph adapter
   - Node → OpenClaw session mapping
   - State management
   - Basic linear graph support

### Phase 2: Advanced Features (Week 2)
1. Parallel execution
2. Error handling and retries
3. State persistence
4. Caching and optimization

### Phase 3: Integration (Week 3)
1. OpenClaw skill wrapper
2. Examples and documentation
3. Testing and validation
4. Performance tuning

---

## 7. Technical Challenges

### 7.1 Communication
- **Challenge**: OpenClaw uses process I/O, frameworks expect function calls
- **Solution**: Adapter layer translates between protocols

### 7.2 State Synchronization
- **Challenge**: Distributed state across multiple processes
- **Solution**: Shared state store (Redis, file system, or OpenClaw context)

### 7.3 Error Handling
- **Challenge**: Process failures vs. framework exceptions
- **Solution**: Standardized error mapping and recovery

### 7.4 Observability
- **Challenge**: Tracing across process boundaries
- **Solution**: Structured logging + OpenClaw telemetry

---

## 8. Next Steps

1. ✅ Research complete
2. ⏭️ Design integration architecture
3. ⏭️ Implement CrewAI adapter prototype
4. ⏭️ Implement LangGraph adapter prototype
5. ⏭️ Create comparison document
6. ⏭️ Update agent-orchestrator skill
7. ⏭️ Write examples and documentation

---

## 9. References

- CrewAI Docs: https://docs.crewai.com
- LangGraph Docs: https://langchain-ai.github.io/langgraph
- OpenAI Agents SDK: https://github.com/openai/openai-agents
- DeerFlow 2.0: https://github.com/bytedance/deer-flow
