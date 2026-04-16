"""
CrewAI to OpenClaw Adapter

This adapter maps CrewAI concepts (Agent, Task, Crew) to OpenClaw's
subagent and process management capabilities.

Author: Catalyst
Date: 2026-04-13
"""

import asyncio
import json
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class OpenClawAgentConfig:
    """Configuration for an OpenClaw agent session"""
    name: str
    agent_type: str  # "codex", "claude", "pi", etc.
    workdir: Optional[str] = None
    pty: bool = False
    background: bool = True
    timeout: Optional[int] = None
    extra_args: List[str] = field(default_factory=list)

    def to_command(self, prompt: str) -> str:
        """Convert config to actual command string"""
        if self.agent_type == "codex":
            base = "codex exec"
            if self.pty:
                base = f"bash pty:true command:\"{base}\""
            return f"{base} {prompt}"
        elif self.agent_type == "claude":
            return f"claude --permission-mode bypassPermissions --print '{prompt}'"
        elif self.agent_type == "pi":
            base = "pi"
            if self.pty:
                base = f"bash pty:true command:\"{base}\""
            return f"{base} '{prompt}'"
        else:
            raise ValueError(f"Unknown agent type: {self.agent_type}")


@dataclass
class OpenClawTask:
    """Task to be executed by an agent"""
    id: str
    description: str
    agent_config: OpenClawAgentConfig
    expected_output: str = ""
    depends_on: List[str] = field(default_factory=list)
    output_file: Optional[str] = None
    async_execution: bool = False
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[str] = None
    session_id: Optional[str] = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None


class OpenClawCrew:
    """
    Crew-like orchestration using OpenClaw sessions

    Manages multiple tasks and their execution using OpenClaw's
    subagent and process management capabilities.
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        verbose: bool = True,
        max_rpm: int = 10
    ):
        self.name = name
        self.description = description
        self.verbose = verbose
        self.max_rpm = max_rpm
        self.tasks: Dict[str, OpenClawTask] = {}
        self.results: Dict[str, Any] = {}
        self._rate_limit_window = []
        self._lock = asyncio.Lock()

    def log(self, message: str, level: str = "info"):
        """Log messages if verbose mode is on"""
        if self.verbose:
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level.upper()}] {message}")

    async def _check_rate_limit(self):
        """Simple rate limiting implementation"""
        now = time.time()
        # Remove entries older than 1 minute
        self._rate_limit_window = [
            t for t in self._rate_limit_window if now - t < 60
        ]

        if len(self._rate_limit_window) >= self.max_rpm:
            # Wait until oldest request is 1 minute old
            sleep_time = 60 - (now - self._rate_limit_window[0])
            if sleep_time > 0:
                self.log(f"Rate limit reached, sleeping {sleep_time:.1f}s", "warn")
                await asyncio.sleep(sleep_time)

        self._rate_limit_window.append(now)

    def add_task(
        self,
        task_id: str,
        description: str,
        agent_config: OpenClawAgentConfig,
        expected_output: str = "",
        depends_on: List[str] = None,
        output_file: Optional[str] = None,
        async_execution: bool = False
    ) -> OpenClawTask:
        """Add a task to the crew"""
        if depends_on is None:
            depends_on = []

        task = OpenClawTask(
            id=task_id,
            description=description,
            agent_config=agent_config,
            expected_output=expected_output,
            depends_on=depends_on,
            output_file=output_file,
            async_execution=async_execution
        )

        self.tasks[task_id] = task
        self.log(f"Added task: {task_id}")
        return task

    def _get_ready_tasks(self) -> List[OpenClawTask]:
        """Get tasks that are ready to execute (dependencies met)"""
        ready = []
        for task in self.tasks.values():
            if task.status == "pending":
                # Check if all dependencies are completed
                deps_completed = all(
                    self.tasks[dep_id].status == "completed"
                    for dep_id in task.depends_on
                )
                if deps_completed:
                    ready.append(task)
        return ready

    async def _execute_task(self, task: OpenClawTask):
        """Execute a single task"""
        await self._check_rate_limit()

        task.status = "running"
        task.started_at = time.time()
        self.log(f"Starting task: {task.id}", "info")

        try:
            # In a real implementation, this would use OpenClaw's exec/process tools
            # For now, we simulate the execution
            command = task.agent_config.to_command(task.description)

            self.log(f"Task {task.id} command: {command[:100]}...", "debug")

            # Simulate execution (replace with actual OpenClaw integration)
            result = await self._simulate_execution(command, task.agent_config)

            task.result = result
            task.status = "completed"
            task.completed_at = time.time()

            self.log(f"Completed task: {task.id} in {task.completed_at - task.started_at:.2f}s", "success")

            # Save to file if specified
            if task.output_file:
                await self._save_output(task.output_file, result)

        except Exception as e:
            task.status = "failed"
            task.completed_at = time.time()
            self.log(f"Task {task.id} failed: {str(e)}", "error")
            raise

    async def _simulate_execution(
        self,
        command: str,
        config: OpenClawAgentConfig
    ) -> str:
        """Simulate agent execution (replace with actual OpenClaw integration)"""
        # This is a placeholder - in production, use OpenClaw's exec/process tools
        await asyncio.sleep(2)  # Simulate work

        # Simulate different results based on agent type
        if "research" in command.lower():
            return json.dumps({
                "findings": [
                    "Trend 1: AI agents becoming mainstream",
                    "Trend 2: Edge AI deployment",
                    "Trend 3: Multimodal models"
                ],
                "confidence": 0.85
            }, indent=2)
        elif "write" in command.lower():
            return """# AI Trends Report

## Introduction
AI is transforming industries at an unprecedented pace.

## Key Trends

### 1. AI Agents
Autonomous agents are becoming production-ready...

### 2. Edge AI
Running AI models on edge devices...

### 3. Multimodal Models
Models that understand text, images, and audio...

## Conclusion
The future of AI is agentic, edge-native, and multimodal.
"""
        else:
            return f"Task completed by {config.agent_type} agent"

    async def _save_output(self, filepath: str, content: str):
        """Save task output to file"""
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            self.log(f"Saved output to: {filepath}", "info")
        except Exception as e:
            self.log(f"Failed to save output: {str(e)}", "error")

    async def _execute_sequential(self):
        """Execute tasks sequentially (respecting dependencies)"""
        total_tasks = len(self.tasks)
        completed = 0

        while completed < total_tasks:
            ready_tasks = self._get_ready_tasks()

            if not ready_tasks:
                # No tasks ready but not all completed - circular dependency?
                self.log("No tasks ready to execute - possible circular dependency", "error")
                break

            # Execute one task at a time
            task = ready_tasks[0]
            await self._execute_task(task)
            completed += 1

    async def _execute_parallel(self, max_concurrent: int = 3):
        """Execute tasks in parallel (respecting dependencies)"""
        semaphore = asyncio.Semaphore(max_concurrent)

        async def execute_with_limit(task: OpenClawTask):
            async with semaphore:
                await self._execute_task(task)

        total_tasks = len(self.tasks)
        completed = 0

        while completed < total_tasks:
            ready_tasks = self._get_ready_tasks()

            if not ready_tasks:
                await asyncio.sleep(0.5)  # Wait for running tasks to complete
                continue

            # Execute all ready tasks up to concurrency limit
            running = [
                execute_with_limit(task)
                for task in ready_tasks[:max_concurrent]
            ]

            await asyncio.gather(*running, return_exceptions=True)

            # Update completed count
            completed = sum(
                1 for t in self.tasks.values() if t.status == "completed"
            )

    async def kickoff(
        self,
        inputs: Optional[Dict[str, Any]] = None,
        process: str = "sequential",
        max_concurrent: int = 3
    ) -> Dict[str, Any]:
        """
        Execute the crew's tasks

        Args:
            inputs: Initial inputs for the crew
            process: "sequential" or "parallel"
            max_concurrent: Maximum concurrent tasks for parallel execution

        Returns:
            Dictionary containing task results
        """
        self.log(f"Starting crew: {self.name}", "info")
        self.log(f"Process: {process}, Tasks: {len(self.tasks)}", "info")

        if inputs:
            self.results.update(inputs)

        start_time = time.time()

        try:
            if process == "sequential":
                await self._execute_sequential()
            elif process == "parallel":
                await self._execute_parallel(max_concurrent)
            else:
                raise ValueError(f"Unknown process type: {process}")

            total_time = time.time() - start_time

            # Collect results
            results = {
                "crew": self.name,
                "status": "completed",
                "total_time": total_time,
                "tasks": {
                    task_id: {
                        "status": task.status,
                        "result": task.result,
                        "duration": (task.completed_at or 0) - (task.started_at or 0)
                    }
                    for task_id, task in self.tasks.items()
                }
            }

            self.log(f"Crew completed in {total_time:.2f}s", "success")
            return results

        except Exception as e:
            total_time = time.time() - start_time
            self.log(f"Crew failed after {total_time:.2f}s: {str(e)}", "error")
            return {
                "crew": self.name,
                "status": "failed",
                "error": str(e),
                "total_time": total_time
            }


# Convenience functions for CrewAI-like API

def create_agent(
    role: str,
    goal: str,
    backstory: str = "",
    agent_type: str = "codex",
    tools: List = None,
    **kwargs
) -> OpenClawAgentConfig:
    """
    Create an agent configuration

    Args:
        role: Agent's role (used in prompt)
        goal: Agent's goal
        backstory: Agent's backstory (used in prompt)
        agent_type: Type of agent to spawn ("codex", "claude", "pi")
        tools: List of tools (for documentation, not used in this adapter)
        **kwargs: Additional configuration

    Returns:
        OpenClawAgentConfig
    """
    # Build prompt from role, goal, backstory
    prompt = f"You are a {role}.\n"
    if goal:
        prompt += f"Your goal: {goal}\n"
    if backstory:
        prompt += f"Backstory: {backstory}\n"
    prompt += "\nTask: {task_description}"

    return OpenClawAgentConfig(
        name=role,
        agent_type=agent_type,
        **kwargs
    )


def create_task(
    description: str,
    agent: OpenClawAgentConfig,
    expected_output: str = "",
    **kwargs
) -> tuple:
    """
    Create a task tuple (id, description, agent_config)

    This is a convenience function that returns a tuple suitable
    for add_task()

    Args:
        description: Task description
        agent: Agent configuration
        expected_output: Expected output format
        **kwargs: Additional task parameters

    Returns:
        Tuple (task_id, description, agent_config, kwargs)
    """
    task_id = f"task_{hash(description) % 10000}"
    return (task_id, description, agent, expected_output, kwargs)


async def run_crew_example():
    """Example usage of the OpenClawCrew"""

    # Create agents
    researcher = create_agent(
        role="Senior Researcher",
        goal="Find the latest AI trends",
        backstory="You are curious and thorough in your research",
        agent_type="codex"
    )

    writer = create_agent(
        role="Technical Writer",
        goal="Write engaging technical articles",
        backstory="You simplify complex topics for broad audiences",
        agent_type="claude"
    )

    # Create crew
    crew = OpenClawCrew(
        name="AI Research Team",
        description="Research and write about AI trends",
        verbose=True
    )

    # Add tasks
    crew.add_task(
        task_id="research",
        description="Research the latest AI trends for 2024",
        agent_config=researcher,
        expected_output="List of top 5 AI trends with brief descriptions",
        output_file="output/research.json"
    )

    crew.add_task(
        task_id="write_article",
        description="Write a comprehensive article based on the research findings",
        agent_config=writer,
        expected_output="1500-word article with introduction, body, and conclusion",
        depends_on=["research"],
        output_file="output/article.md"
    )

    # Execute crew
    result = await crew.kickoff(process="sequential")

    print("\n" + "="*50)
    print("CREW EXECUTION RESULTS")
    print("="*50)
    print(json.dumps(result, indent=2))

    return result


if __name__ == "__main__":
    # Run example
    asyncio.run(run_crew_example())
