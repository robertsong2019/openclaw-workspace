"""
LangGraph to OpenClaw Adapter

This adapter maps LangGraph concepts (State, Node, Edge, Graph) to OpenClaw's
subagent and process management capabilities, providing stateful workflow
orchestration.

Author: Catalyst
Date: 2026-04-13
"""

import asyncio
import json
import time
from typing import Any, Callable, Dict, List, Optional, TypedDict, Union
from dataclasses import dataclass, field
from enum import Enum


# LangGraph-like State Types
class State(TypedDict, total=False):
    """Base state type - extend for your workflows"""
    messages: List[str]
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    error: Optional[str]
    done: bool
    step: int


# Special nodes
START = "__start__"
END = "__end__"


class EdgeType(Enum):
    """Types of edges in the graph"""
    NORMAL = "normal"
    CONDITIONAL = "conditional"


@dataclass
class Edge:
    """Represents a connection between nodes"""
    from_node: str
    to_node: Union[str, Callable]
    edge_type: EdgeType = EdgeType.NORMAL
    condition_map: Optional[Dict[str, str]] = None  # For conditional edges


@dataclass
class Node:
    """Represents a node in the graph"""
    name: str
    func: Callable
    metadata: Dict[str, Any] = field(default_factory=dict)

    async def __call__(self, state: State) -> Dict[str, Any]:
        """Execute the node's function"""
        try:
            # If function is async, await it
            if asyncio.iscoroutinefunction(self.func):
                result = await self.func(state)
            else:
                result = self.func(state)

            # Ensure result is a dict
            if not isinstance(result, dict):
                result = {"output": result}

            return result
        except Exception as e:
            return {
                "error": str(e),
                "error_node": self.name
            }


class OpenClawAgentNode:
    """
    A LangGraph node that executes an OpenClaw agent

    This bridges LangGraph's node concept with OpenClaw's agent execution.
    """

    def __init__(
        self,
        name: str,
        agent_type: str = "codex",
        prompt_template: str = "{task}",
        timeout: Optional[int] = None,
        **agent_config
    ):
        self.name = name
        self.agent_type = agent_type
        self.prompt_template = prompt_template
        self.timeout = timeout
        self.agent_config = agent_config

    def format_prompt(self, state: State) -> str:
        """Format the prompt using state and template"""
        try:
            # Simple template substitution
            prompt = self.prompt_template

            # Replace common placeholders
            if "{task}" in prompt:
                task = state.get("messages", [""])[-1] if state.get("messages") else ""
                prompt = prompt.replace("{task}", task)

            if "{data}" in prompt:
                prompt = prompt.replace("{data}", json.dumps(state.get("data", {})))

            if "{step}" in prompt:
                prompt = prompt.replace("{step}", str(state.get("step", 0)))

            return prompt
        except Exception as e:
            # Fallback to simple task
            return state.get("messages", [""])[-1] if state.get("messages") else "Execute task"

    async def __call__(self, state: State) -> Dict[str, Any]:
        """Execute the OpenClaw agent"""
        prompt = self.format_prompt(state)

        # In a real implementation, this would spawn an OpenClaw agent
        # For now, we simulate execution
        result = await self._execute_agent(prompt)

        # Update state
        updates: Dict[str, Any] = {}

        if "messages" in state:
            updates["messages"] = state["messages"] + [result]
        else:
            updates["messages"] = [result]

        if "step" in state:
            updates["step"] = state["step"] + 1
        else:
            updates["step"] = 1

        return updates

    async def _execute_agent(self, prompt: str) -> str:
        """Execute the OpenClaw agent (simulated)"""
        # This is a placeholder - in production, use OpenClaw's exec/process tools

        # Simulate execution time
        await asyncio.sleep(1.5)

        # Simulate different responses based on agent type and prompt
        if "research" in prompt.lower() or "find" in prompt.lower():
            return json.dumps({
                "type": "research_result",
                "findings": [
                    "AI agents are becoming mainstream",
                    "Edge AI deployment is growing",
                    "Multimodal models are the next frontier"
                ],
                "confidence": 0.87
            }, indent=2)

        elif "write" in prompt.lower() or "create" in prompt.lower():
            return """# AI Agent Research Summary

## Key Findings

### 1. Mainstream Adoption
AI agents are moving from experimental to production use across industries.

### 2. Edge Deployment
Running AI agents on edge devices is becoming more common.

### 3. Multimodal Capabilities
Agents that can process text, images, and audio are emerging.

## Conclusion
The agent ecosystem is maturing rapidly with strong adoption trends.
"""

        elif "analyze" in prompt.lower() or "evaluate" in prompt.lower():
            return json.dumps({
                "type": "analysis",
                "quality_score": 8.5,
                "completeness": 0.9,
                "recommendations": [
                    "Add more citations",
                    "Include case studies",
                    "Expand conclusion"
                ]
            }, indent=2)

        else:
            return f"Executed {self.agent_type} agent with prompt: {prompt[:100]}..."


class StateGraph:
    """
    LangGraph-like StateGraph implementation using OpenClaw

    Manages stateful workflows with nodes, edges, and conditional routing.
    """

    def __init__(self, state_type: type = State):
        self.state_type = state_type
        self.nodes: Dict[str, Union[Node, Callable]] = {}
        self.edges: List[Edge] = []
        self.entry_point: Optional[str] = None
        self.finish_point: Optional[str] = None
        self.compiled = False

    def add_node(
        self,
        name: str,
        func: Union[Callable, OpenClawAgentNode],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Add a node to the graph"""
        if metadata:
            if isinstance(func, OpenClawAgentNode):
                func.metadata.update(metadata)
            else:
                func = Node(name=name, func=func, metadata=metadata)

        self.nodes[name] = func
        return self

    def add_edge(self, from_node: str, to_node: str):
        """Add a normal edge between nodes"""
        self.edges.append(Edge(
            from_node=from_node,
            to_node=to_node,
            edge_type=EdgeType.NORMAL
        ))
        return self

    def add_conditional_edges(
        self,
        from_node: str,
        condition: Callable,
        condition_map: Dict[str, str]
    ):
        """Add conditional edges based on state"""
        self.edges.append(Edge(
            from_node=from_node,
            to_node=condition,
            edge_type=EdgeType.CONDITIONAL,
            condition_map=condition_map
        ))
        return self

    def set_entry_point(self, node_name: str):
        """Set the starting node"""
        self.entry_point = node_name
        return self

    def set_finish_point(self, node_name: str):
        """Set the ending node"""
        self.finish_point = node_name
        return self

    def add_sequence(self, functions: List[Union[Callable, str]]):
        """Add a sequence of nodes and connect them"""
        for i, func in enumerate(functions):
            if isinstance(func, str):
                # Already a node name
                node_name = func
            else:
                # Function - create node
                node_name = f"node_{i}"
                self.add_node(node_name, func)

            if i == 0:
                self.set_entry_point(node_name)
            else:
                prev_name = functions[i-1] if isinstance(functions[i-1], str) else f"node_{i-1}"
                self.add_edge(prev_name, node_name)

        if self.finish_point is None and functions:
            last_name = functions[-1] if isinstance(functions[-1], str) else f"node_{len(functions)-1}"
            self.set_finish_point(last_name)

        return self

    def compile(self):
        """Compile the graph for execution"""
        if not self.entry_point:
            raise ValueError("No entry point set")

        self.compiled = True
        return CompiledGraph(self)


class CompiledGraph:
    """
    A compiled graph ready for execution
    """

    def __init__(self, graph: StateGraph):
        self.graph = graph
        self.nodes = graph.nodes
        self.edges = graph.edges
        self.entry_point = graph.entry_point
        self.finish_point = graph.finish_point

    async def invoke(
        self,
        initial_state: Optional[State] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> State:
        """
        Execute the graph

        Args:
            initial_state: Starting state
            config: Execution configuration (thread_id, etc.)

        Returns:
            Final state after execution
        """
        if not initial_state:
            initial_state = State()

        state = initial_state.copy()
        current_node = self.entry_point
        execution_path = []

        print(f"\n{'='*60}")
        print(f"Starting Graph Execution")
        print(f"Entry Point: {self.entry_point}")
        print(f"{'='*60}\n")

        step = 0
        while current_node and current_node != END:
            step += 1
            print(f"[Step {step}] Executing node: {current_node}")

            try:
                # Get the node
                node_func = self.nodes.get(current_node)
                if not node_func:
                    raise ValueError(f"Node not found: {current_node}")

                # Execute the node
                if isinstance(node_func, (Node, OpenClawAgentNode)):
                    updates = await node_func(state)
                else:
                    # Plain function
                    if asyncio.iscoroutinefunction(node_func):
                        updates = await node_func(state)
                    else:
                        updates = node_func(state)

                    # Ensure dict
                    if not isinstance(updates, dict):
                        updates = {"output": updates}

                # Update state
                state.update(updates)
                execution_path.append(current_node)

                print(f"  → Completed. State updated: {list(updates.keys())}")

                # Find next node
                current_node = self._get_next_node(current_node, state)

                if current_node == END:
                    print(f"\n[Step {step+1}] Reached END node")
                    break

            except Exception as e:
                print(f"  → ERROR: {str(e)}")
                state["error"] = str(e)
                state["error_node"] = current_node
                break

        print(f"\n{'='*60}")
        print(f"Graph Execution Complete")
        print(f"Path: {' → '.join(execution_path)}")
        print(f"Final State Keys: {list(state.keys())}")
        print(f"{'='*60}\n")

        return state

    def _get_next_node(self, current_node: str, state: State) -> str:
        """Determine the next node to execute"""
        # Find edges from current node
        outgoing_edges = [
            edge for edge in self.edges
            if edge.from_node == current_node
        ]

        if not outgoing_edges:
            # No outgoing edges - check if this is finish point
            if current_node == self.finish_point:
                return END
            # Otherwise, end the graph
            return END

        # Handle edges
        for edge in outgoing_edges:
            if edge.edge_type == EdgeType.NORMAL:
                # Normal edge - return the target
                if edge.to_node == START:
                    continue  # Skip START references
                return str(edge.to_node)

            elif edge.edge_type == EdgeType.CONDITIONAL:
                # Conditional edge - call the condition function
                condition_result = edge.to_node(state)

                # Map condition result to next node
                if edge.condition_map and condition_result in edge.condition_map:
                    return edge.condition_map[condition_result]
                elif isinstance(edge.to_node, str):
                    return edge.to_node
                else:
                    # Condition returned a string, use it directly
                    return str(condition_result)

        # No matching edge found
        return END

    async def astream(
        self,
        initial_state: Optional[State] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Async stream execution - yields state after each node

        Args:
            initial_state: Starting state
            config: Execution configuration

        Yields:
            State after each node execution
        """
        if not initial_state:
            initial_state = State()

        state = initial_state.copy()
        current_node = self.entry_point

        while current_node and current_node != END:
            # Execute node
            node_func = self.nodes.get(current_node)
            if not node_func:
                raise ValueError(f"Node not found: {current_node}")

            if isinstance(node_func, (Node, OpenClawAgentNode)):
                updates = await node_func(state)
            else:
                if asyncio.iscoroutinefunction(node_func):
                    updates = await node_func(state)
                else:
                    updates = node_func(state)

                if not isinstance(updates, dict):
                    updates = {"output": updates}

            state.update(updates)
            yield state

            # Get next node
            current_node = self._get_next_node(current_node, state)

            if current_node == END:
                yield state
                break


# Helper functions

def create_openclaw_node(
    name: str,
    prompt_template: str,
    agent_type: str = "codex",
    **config
) -> OpenClawAgentNode:
    """Convenience function to create an OpenClaw agent node"""
    return OpenClawAgentNode(
        name=name,
        agent_type=agent_type,
        prompt_template=prompt_template,
        **config
    )


# Example workflows

async def example_simple_graph():
    """Simple linear graph: research → write → review"""

    # Define state
    class ResearchState(State):
        topic: str
        research: str
        article: str
        review: str

    # Build graph
    graph = StateGraph(ResearchState)

    # Add nodes
    research_node = create_openclaw_node(
        name="research",
        prompt_template="Research this topic: {task}",
        agent_type="codex"
    )

    write_node = create_openclaw_node(
        name="write",
        prompt_template="Write an article based on this research: {data}",
        agent_type="claude"
    )

    review_node = create_openclaw_node(
        name="review",
        prompt_template="Review this article: {data}",
        agent_type="pi"
    )

    graph.add_node("research", research_node)
    graph.add_node("write", write_node)
    graph.add_node("review", review_node)

    # Connect nodes
    graph.add_edge(START, "research")
    graph.add_edge("research", "write")
    graph.add_edge("write", "review")
    graph.add_edge("review", END)

    # Compile and execute
    compiled = graph.compile()

    initial_state: ResearchState = {
        "messages": ["AI agent trends for 2024"],
        "topic": "AI agent trends",
        "step": 0
    }

    result = await compiled.invoke(initial_state)
    print("\nFinal State:")
    print(json.dumps(result, indent=2))

    return result


async def example_conditional_graph():
    """Graph with conditional routing"""

    class WorkflowState(State):
        task_type: str
        research: str
        article: str
        code: str
        done: bool

    # Build graph
    graph = StateGraph(WorkflowState)

    # Define nodes
    def classify_task(state: WorkflowState) -> dict:
        """Classify the task type"""
        task = state.get("messages", [""])[-1].lower()
        if "code" in task or "implement" in task:
            task_type = "coding"
        elif "write" in task or "article" in task:
            task_type = "writing"
        else:
            task_type = "research"

        return {"task_type": task_type}

    research_node = create_openclaw_node(
        name="research",
        prompt_template="Research: {task}"
    )

    write_node = create_openclaw_node(
        name="write",
        prompt_template="Write: {task}"
    )

    code_node = create_openclaw_node(
        name="code",
        prompt_template="Code: {task}",
        agent_type="codex"
    )

    # Add nodes
    graph.add_node("classify", classify_task)
    graph.add_node("research", research_node)
    graph.add_node("write", write_node)
    graph.add_node("code", code_node)

    # Add edges
    graph.add_edge(START, "classify")

    # Conditional routing based on task type
    def route_based_on_type(state: WorkflowState) -> str:
        return state.get("task_type", "research")

    graph.add_conditional_edges(
        "classify",
        route_based_on_type,
        {
            "research": "research",
            "writing": "write",
            "coding": "code"
        }
    )

    # All paths converge to END
    graph.add_edge("research", END)
    graph.add_edge("write", END)
    graph.add_edge("code", END)

    # Compile and execute
    compiled = graph.compile()

    # Test with different tasks
    tasks = [
        "Write an article about AI agents",
        "Implement a REST API for user management",
        "Research the latest LLM developments"
    ]

    for task in tasks:
        print(f"\n{'='*60}")
        print(f"Testing task: {task}")
        print(f"{'='*60}")

        result = await compiled.invoke({
            "messages": [task],
            "step": 0
        })

        print(f"Task type: {result.get('task_type')}")
        print(f"Execution path inferred from result keys")


async def example_loop_graph():
    """Graph with loop/retry logic"""

    class IterationState(State):
        iterations: int
        quality: float
        done: bool
        final_result: str

    graph = StateGraph(IterationState)

    def generate_draft(state: IterationState) -> dict:
        """Generate a draft"""
        iteration = state.get("iterations", 0) + 1
        return {
            "iterations": iteration,
            "final_result": f"Draft {iteration}: Initial content"
        }

    def evaluate_quality(state: IterationState) -> dict:
        """Evaluate the draft quality"""
        iteration = state.get("iterations", 1)
        # Simulate improving quality with iterations
        quality = min(0.5 + (iteration * 0.2), 0.95)
        return {"quality": quality}

    def improve_draft(state: IterationState) -> dict:
        """Improve the draft"""
        iteration = state.get("iterations", 1) + 1
        return {
            "iterations": iteration,
            "final_result": f"Draft {iteration}: Improved content based on feedback"
        }

    # Add nodes
    graph.add_node("generate", generate_draft)
    graph.add_node("evaluate", evaluate_quality)
    graph.add_node("improve", improve_draft)

    # Build loop structure
    graph.add_edge(START, "generate")
    graph.add_edge("generate", "evaluate")

    # Conditional: if quality >= 0.9, finish; else improve
    def should_continue(state: IterationState) -> str:
        quality = state.get("quality", 0)
        return "done" if quality >= 0.9 else "improve"

    graph.add_conditional_edges(
        "evaluate",
        should_continue,
        {"done": END, "improve": "improve"}
    )

    # Loop back: improve → evaluate
    graph.add_edge("improve", "evaluate")

    # Compile and execute
    compiled = graph.compile()

    result = await compiled.invoke({
        "iterations": 0,
        "quality": 0.0,
        "done": False
    })

    print(f"\nLoop completed after {result.get('iterations')} iterations")
    print(f"Final quality: {result.get('quality')}")
    print(f"Final result: {result.get('final_result')}")


if __name__ == "__main__":
    print("="*60)
    print("Example 1: Simple Linear Graph")
    print("="*60)
    asyncio.run(example_simple_graph())

    print("\n" + "="*60)
    print("Example 2: Conditional Routing Graph")
    print("="*60)
    asyncio.run(example_conditional_graph())

    print("\n" + "="*60)
    print("Example 3: Loop/Retry Graph")
    print("="*60)
    asyncio.run(example_loop_graph())
