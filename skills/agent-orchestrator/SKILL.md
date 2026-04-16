---
name: agent-orchestrator
description: Multi-agent orchestration for OpenClaw using CrewAI and LangGraph frameworks. Create complex workflows with multiple AI agents, manage state, and handle task dependencies. Use when you need to coordinate multiple agents for complex tasks like content creation, research pipelines, or customer support.
metadata:
  {
    "openclaw": { "emoji": "🤖", "requires": { "python": ">=3.8" } },
  }
---

# Agent Orchestrator

Orchestrate multiple AI agents using **CrewAI** or **LangGraph** frameworks. Build complex, stateful workflows with task dependencies, conditional routing, and parallel execution.

---

## Quick Start

### CrewAI-style (Role-Based Workflows)

Best for: Teams of specialists working together

```python
from agent_orchestrator.crewai import OpenClawCrew, OpenClawAgentConfig

# Create agents
researcher = OpenClawAgentConfig(
    name="Researcher",
    agent_type="codex"
)

writer = OpenClawAgentConfig(
    name="Writer",
    agent_type="claude"
)

# Build crew
crew = OpenClawCrew(name="Content Team", verbose=True)

crew.add_task(
    task_id="research",
    description="Research AI trends",
    agent_config=researcher,
    output_file="output/research.json"
)

crew.add_task(
    task_id="write",
    description="Write article based on research",
    agent_config=writer,
    depends_on=["research"],
    output_file="output/article.md"
)

# Execute
result = await crew.kickoff(process="sequential")
```

### LangGraph-style (Stateful Workflows)

Best for: Complex workflows with conditional routing

```python
from agent_orchestrator.langgraph import StateGraph, create_openclaw_node, START, END

# Define state
class WorkflowState(dict):
    messages: list
    analysis: dict
    done: bool

# Build graph
graph = StateGraph(WorkflowState)

# Add nodes
graph.add_node("research", create_openclaw_node(
    name="research",
    prompt_template="Research: {task}",
    agent_type="codex"
))

graph.add_node("analyze", create_openclaw_node(
    name="analyze",
    prompt_template="Analyze: {task}",
    agent_type="claude"
))

# Connect with conditional routing
def route_next(state):
    return "end" if state.get("done") else "analyze"

graph.add_edge(START, "research")
graph.add_conditional_edges("analyze", route_next, {
    "analyze": "research",  # Loop back
    "end": END
})

# Execute
compiled = graph.compile()
result = await compiled.invoke({"messages": ["Analyze AI trends"], "step": 0})
```

---

## When to Use This Skill

**Use Agent Orchestrator when:**

✅ You need to coordinate **multiple agents** for a complex task
✅ Tasks have **dependencies** (task B needs task A's output)
✅ You need **state management** between agents
✅ Workflow requires **conditional routing** (if X then A else B)
✅ Building **production systems** with complex logic

**Don't use when:**

❌ Simple one-off task (use `exec` with coding-agent skill instead)
❌ Single agent is sufficient
❌ Task is trivial and doesn't need coordination

---

## Framework Selection Guide

| Use Case | Recommended Framework | Why |
|----------|----------------------|-----|
| **Research team** (researcher → writer → editor) | CrewAI | Natural role-based metaphor |
| **Content pipeline** (outline → draft → review → polish) | CrewAI | Sequential dependencies |
| **Customer support triage** (classify → route → resolve) | LangGraph | Conditional routing needed |
| **Data pipeline** (extract → transform → load) | LangGraph | State management important |
| **Approval workflow** (submit → approve/reject → notify) | LangGraph | Cycles/retry support |
| **Quick prototype** | CrewAI | Less boilerplate |
| **Production system** | LangGraph | More robust error handling |

**Rule of thumb:**
- **CrewAI** = "Here's a team, give them a job"
- **LangGraph** = "Here's a process, run it"

---

## CrewAI API

### OpenClawCrew

Main orchestrator for CrewAI-style workflows.

```python
crew = OpenClawCrew(
    name="My Team",
    description="Team description",
    verbose=True,        # Print execution logs
    max_rpm=10          # Rate limit (requests per minute)
)
```

### add_task()

Add a task to the crew.

```python
crew.add_task(
    task_id="unique_id",              # Required: unique identifier
    description="What to do",          # Required: task description
    agent_config=agent,                # Required: agent configuration
    expected_output="Format hint",    # Optional: expected output format
    depends_on=["task1", "task2"],    # Optional: task dependencies
    output_file="path/to/file",       # Optional: save output to file
    async_execution=False              # Optional: run in parallel
)
```

### kickoff()

Execute the crew.

```python
result = await crew.kickoff(
    inputs={"key": "value"},     # Optional: initial inputs
    process="sequential",        # "sequential" or "parallel"
    max_concurrent=3            # For parallel execution
)
```

**Returns:**
```python
{
    "crew": "My Team",
    "status": "completed",       # or "failed"
    "total_time": 45.2,         # seconds
    "tasks": {
        "task1": {
            "status": "completed",
            "result": "...",
            "duration": 12.5
        },
        ...
    }
}
```

### OpenClawAgentConfig

Configure an OpenClaw agent.

```python
agent = OpenClawAgentConfig(
    name="Agent Name",           # Required: for logging
    agent_type="codex",          # Required: "codex", "claude", "pi"
    workdir="/path/to/project",  # Optional: working directory
    pty=True,                    # Optional: use PTY (for Codex/Pi)
    background=True,             # Optional: run in background
    timeout=None                 # Optional: timeout in seconds
)
```

**Supported Agent Types:**

| Type | Description | PTY Required |
|------|-------------|--------------|
| `codex` | Codex coding agent | ✅ Yes |
| `claude` | Claude Code | ❌ No |
| `pi` | Pi coding agent | ✅ Yes |

---

## LangGraph API

### StateGraph

Builder for stateful workflows.

```python
graph = StateGraph(state_type)
```

**state_type** can be:
- `dict` (default)
- `TypedDict` for type safety
- Any dict-like class

### add_node()

Add a node to the graph.

```python
# With OpenClaw agent
graph.add_node("node_name", create_openclaw_node(
    name="node_name",
    prompt_template="Process: {task}",
    agent_type="codex"
))

# With custom function
def my_node(state: dict) -> dict:
    # Process state
    return {"key": "updated_value"}

graph.add_node("node_name", my_node)
```

### add_edge()

Add a normal edge (always executes).

```python
graph.add_edge("node1", "node2")
graph.add_edge(START, "first_node")
graph.add_edge("last_node", END)
```

### add_conditional_edges()

Add conditional routing.

```python
def route_function(state: dict) -> str:
    # Return string indicating next node
    if state.get("condition"):
        return "path_a"
    return "path_b"

graph.add_conditional_edges(
    "decision_node",
    route_function,
    {
        "path_a": "node_a",
        "path_b": "node_b"
    }
)
```

### set_entry_point() / set_finish_point()

Set start and end nodes.

```python
graph.set_entry_point("first_node")
graph.set_finish_point("last_node")
```

### add_sequence()

Add a linear sequence of nodes.

```python
graph.add_sequence([
    step1_func,
    step2_func,
    step3_func
])
# Automatically creates edges: step1 → step2 → step3
```

### compile()

Compile the graph for execution.

```python
compiled = graph.compile()
```

### invoke()

Execute the graph synchronously.

```python
result = await compiled.invoke(
    initial_state={"messages": ["Start"]},
    config={"thread_id": "session-123"}  # Optional: for checkpointing
)
```

### astream()

Execute with streaming (yields state after each node).

```python
async for state in compiled.astream(initial_state):
    print("Current state:", state)
```

### create_openclaw_node()

Convenience function to create OpenClaw agent nodes.

```python
node = create_openclaw_node(
    name="research",
    prompt_template="Research: {task}",
    agent_type="codex",
    timeout=300
)
```

**Template Variables:**
- `{task}` - Last message in state
- `{data}` - Full state data (JSON)
- `{step}` - Current step number

---

## Patterns and Examples

### Pattern 1: Sequential Pipeline (CrewAI)

```python
# Content creation pipeline
crew = OpenClawCrew(name="Content Team")

crew.add_task("research", "Research topic", researcher)
crew.add_task("outline", "Create outline", writer, depends_on=["research"])
crew.add_task("draft", "Write draft", writer, depends_on=["outline"])
crew.add_task("review", "Review draft", editor, depends_on=["draft"])
crew.add_task("finalize", "Finalize article", writer, depends_on=["review"])

result = await crew.kickoff(process="sequential")
```

### Pattern 2: Parallel Execution (CrewAI)

```python
# Run independent tasks in parallel
crew = OpenClawCrew(name="Analysis Team")

crew.add_task("analyze_a", "Analyze dataset A", analyst1, async_execution=True)
crew.add_task("analyze_b", "Analyze dataset B", analyst2, async_execution=True)
crew.add_task("combine", "Combine results", synthesizer,
              depends_on=["analyze_a", "analyze_b"])

result = await crew.kickoff(process="parallel", max_concurrent=2)
```

### Pattern 3: Conditional Routing (LangGraph)

```python
# Customer support triage
graph = StateGraph()

def classify(state):
    issue = state["issue"].lower()
    if "bug" in issue:
        return "technical"
    elif "bill" in issue:
        return "billing"
    return "general"

graph.add_node("classify", classify)
graph.add_node("technical", tech_agent)
graph.add_node("billing", billing_agent)
graph.add_node("general", general_agent)

graph.add_conditional_edges("classify", classify, {
    "technical": "technical",
    "billing": "billing",
    "general": "general"
})
```

### Pattern 4: Loop/Retry (LangGraph)

```python
# Quality check loop
graph = StateGraph()

def should_retry(state):
    return state["quality"] < 0.9

graph.add_node("generate", generator)
graph.add_node("check", quality_checker)

graph.add_edge(START, "generate")
graph.add_edge("generate", "check")
graph.add_conditional_edges("check", should_retry, {
    True: "generate",   # Retry
    False: END         # Done
})
```

### Pattern 5: Parallel Processing (LangGraph)

```python
# Process multiple items in parallel
graph = StateGraph()

graph.add_edge(START, ["process1", "process2", "process3"])
graph.add_edge(["process1", "process2", "process3"], "merge")
graph.add_edge("merge", END)

# All three process nodes run in parallel
```

---

## Error Handling

### CrewAI Error Handling

```python
result = await crew.kickoff()

if result["status"] == "failed":
    print("Crew failed!")
    for task_id, task_result in result["tasks"].items():
        if task_result["status"] == "failed":
            print(f"  Failed task: {task_id}")
```

### LangGraph Error Handling

```python
# Node-level error handling
def safe_node(state):
    try:
        result = do_work()
        return {"result": result}
    except Exception as e:
        return {"error": str(e), "failed": True}

# Conditional routing based on error
def check_error(state):
    return "error_handler" if state.get("error") else "next_step"

graph.add_conditional_edges("node", check_error, {
    "error_handler": "error_handler",
    "next_step": "next_step"
})
```

---

## Advanced Features

### Task Output Persistence

Both frameworks support saving task outputs to files:

```python
# CrewAI
crew.add_task(
    task_id="research",
    description="Research topic",
    agent_config=agent,
    output_file="output/research.json"
)

# LangGraph (in node)
def save_output(state):
    with open("output/result.json", "w") as f:
        json.dump(state, f)
    return state
```

### Rate Limiting

CrewAI has built-in rate limiting:

```python
crew = OpenClawCrew(
    name="My Team",
    max_rpm=10  # 10 requests per minute
)
```

### State Persistence (LangGraph)

```python
# Use thread_id for checkpointing
result = await compiled.invoke(
    initial_state,
    config={"thread_id": "user-session-123"}
)

# Can resume from checkpoint
result2 = await compiled.invoke(
    new_input,
    config={"thread_id": "user-session-123"}
)
```

### Custom Node Metadata

```python
# LangGraph
graph.add_node(
    "expensive_task",
    my_node,
    metadata={
        "cost": "high",
        "timeout": 60,
        "priority": 1
    }
)
```

---

## Best Practices

### 1. Design Your Workflow First

Before coding, sketch the flow:

```
CrewAI:
Researcher → Writer → Editor

LangGraph:
[START] → Classify → [Technical/Billing/Feature] → Resolve → [END]
```

### 2. Use Descriptive Task IDs

```python
# ✅ Good
crew.add_task("market_research", "Research market...", researcher)

# ❌ Bad
crew.add_task("task1", "Research...", researcher)
```

### 3. Handle Errors Gracefully

```python
# Always check results
result = await crew.kickoff()
if result["status"] == "failed":
    # Handle failure
    pass
```

### 4. Use Output Files for Long Results

```python
# Don't return huge strings in state
crew.add_task(
    task_id="long_task",
    description="Generate 10k word article",
    agent_config=writer,
    output_file="output/article.md"  # Save to file
)
```

### 5. Test Individual Tasks First

Before building complex workflows, test each task/agent independently:

```python
# Test a single task
test_crew = OpenClawCrew(name="Test")
test_crew.add_task("test", "Your task", agent)
result = await test_crew.kickoff()
print(result)
```

### 6. Choose the Right Framework

- **Simple, role-based** → CrewAI
- **Complex, stateful** → LangGraph
- **Don't know** → Start with CrewAI, migrate to LangGraph if needed

---

## Troubleshooting

### CrewAI Tasks Not Executing

**Problem:** Tasks stay in "pending" state

**Solution:** Check for circular dependencies
```python
# ✅ Correct
task_b depends_on=["task_a"]

# ❌ Circular
task_a depends_on=["task_b"]
task_b depends_on=["task_a"]
```

### LangGraph Graph Not Compiling

**Problem:** `ValueError: No entry point set`

**Solution:** Always set entry point
```python
graph.set_entry_point("first_node")
```

### State Not Updating

**Problem:** Nodes don't seem to update state

**Solution:** Ensure nodes return dict
```python
# ✅ Correct
def my_node(state):
    return {"key": "value"}

# ❌ Wrong
def my_node(state):
    # Returns nothing
    pass
```

### Agent Not Responding

**Problem:** Agent hangs or times out

**Solution:** Check PTY setting
```python
# Codex and Pi need PTY
codex_agent = OpenClawAgentConfig(
    name="codex",
    agent_type="codex",
    pty=True  # Required!
)

# Claude Code does NOT need PTY
claude_agent = OpenClawAgentConfig(
    name="claude",
    agent_type="claude",
    pty=False
)
```

---

## Examples Location

Full working examples are available in:

```
~/.openclaw/workspace/agent-framework-integration/examples/
├── content_pipeline_crewai.py     # CrewAI content creation
└── customer_support_langgraph.py  # LangGraph support triage
```

Run them:

```bash
cd ~/.openclaw/workspace/agent-framework-integration
python examples/content_pipeline_crewai.py
python examples/customer_support_langgraph.py
```

---

## Reference Documentation

For more details, see:

- **Research**: `~/.openclaw/workspace/agent-framework-integration/docs/RESEARCH.md`
- **Comparison**: `~/.openclaw/workspace/agent-framework-integration/FRAMEWORK_COMPARISON.md`
- **CrewAI Adapter**: `~/.openclaw/workspace/agent-framework-integration/crewai/adapter.py`
- **LangGraph Adapter**: `~/.openclaw/workspace/agent-framework-integration/langgraph/adapter.py`

---

## Integration with OpenClaw

This skill uses OpenClaw's native capabilities:

- **subagents** tool: For managing agent sessions
- **exec** tool: For spawning agents
- **process** tool: For monitoring background processes

The adapters provide a high-level API while leveraging OpenClaw's robust process management.

---

## Limitations

- **Python-only**: Currently only supports Python-based workflows
- **Simulated execution**: Prototypes simulate OpenClaw integration; production requires actual OpenClaw tool calls
- **State storage**: State is in-memory; persistence requires external store (Redis, file system)

---

## Future Enhancements

Planned features:

- [ ] Real OpenClaw tool integration (currently simulated)
- [ ] State persistence with Redis
- [ ] Web UI for workflow visualization
- [ ] Workflow templates library
- [ ] Integration with OpenClaw channels (Feishu, Discord)
- [ ] Real-time monitoring dashboard
- [ ] Workflow versioning and rollback

---

## Contributing

To extend or improve this skill:

1. Add new patterns to SKILL.md
2. Create examples in `examples/` directory
3. Update adapters in `crewai/` or `langgraph/` directories
4. Document breaking changes

---

**Happy Orchestrating! 🤖**
