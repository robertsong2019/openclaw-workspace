"""Stub agent_registry — referenced by orchestrator but removed from codebase."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Agent:
    name: str = "default"
    capabilities: List[str] = field(default_factory=list)


class AgentRegistry:
    def __init__(self):
        self.agents: List[Agent] = []

    def select_agent(self, story: Any) -> Agent:
        return Agent()
