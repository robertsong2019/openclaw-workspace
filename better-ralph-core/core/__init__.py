"""
Better Ralph - Core Module

Advanced autonomous agent loop for automated development tasks.
"""

__version__ = "1.0.0"
__author__ = "Better Ralph Team"

from .orchestrator import RalphOrchestrator
from .prd_manager import PRDManager
from .memory_manager import MemoryManager
# AgentRegistry removed

__all__ = [
    "RalphOrchestrator",
    "PRDManager", 
    "MemoryManager",
# removed
]