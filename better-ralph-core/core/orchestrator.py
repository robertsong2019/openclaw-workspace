"""
Ralph Orchestrator - Main orchestration logic for the Better Ralph system.

Coordinates agents, manages PRD stories, and orchestrates the development workflow.
"""

import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from pathlib import Path

from .prd_manager import PRDManager, UserStory
from .memory_manager import MemoryManager
from .agent_registry import AgentRegistry, Agent
from utils.config import Config
from utils.logger import Logger
from utils.monitor import PerformanceMonitor
from plugins.version_control import VersionControl


@dataclass
class IterationResult:
    """Result of a single iteration."""
    story_id: str
    story_title: str
    success: bool
    duration: float
    commit_hash: Optional[str] = None
    error_message: Optional[str] = None
    artifacts: List[str] = field(default_factory=list)


@dataclass
class SessionStats:
    """Statistics for a complete session."""
    total_iterations: int
    successful_iterations: int
    failed_iterations: int
    total_duration: float
    average_iteration_time: float
    stories_completed: List[str] = field(default_factory=list)
    commits_made: List[str] = field(default_factory=list)


class RalphOrchestrator:
    """
    Main orchestrator for the Better Ralph autonomous agent system.
    
    Coordinates all components to automate development tasks based on PRD stories.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the orchestrator with configuration."""
        self.config = config or Config()
        self.logger = Logger.get_logger("orchestrator")
        self.monitor = PerformanceMonitor()
        
        # Core components
        self.prd_manager = PRDManager()
        self.memory_manager = MemoryManager()
        self.agent_registry = AgentRegistry()
        self.version_control = VersionControl()
        
        # State tracking
        self.current_session_id: Optional[str] = None
        self.iteration_count = 0
        self.session_stats = SessionStats(
            total_iterations=0,
            successful_iterations=0,
            failed_iterations=0,
            total_duration=0.0
        )
        
        self.logger.info("Ralph Orchestrator initialized")
    
    def start_session(self, prd_path: Path, project_root: Path) -> str:
        """Start a new development session."""
        session_id = f"session-{int(time.time())}"
        self.current_session_id = session_id
        
        # Initialize components
        self.prd_manager.load_prd(prd_path)
        self.memory_manager.initialize_session(project_root)
        
        # Set up git branch
        if self.prd_manager.prd_data.get("branchName"):
            self.version_control.ensure_branch(self.prd_manager.prd_data["branchName"])
        
        self.logger.info(f"Session started: {session_id}")
        return session_id
    
    def execute_iteration(self) -> IterationResult:
        """Execute a single iteration of the development workflow."""
        if not self.current_session_id:
            raise ValueError("No active session")
        
        start_time = time.time()
        self.iteration_count += 1
        
        # Get next story to work on
        next_story = self.prd_manager.get_next_story()
        if not next_story:
            # All stories completed
            return IterationResult(
                story_id="complete",
                story_title="All stories completed",
                success=True,
                duration=time.time() - start_time
            )
        
        self.logger.info(f"Starting iteration {self.iteration_count}: {next_story.title}")
        
        # Select best agent for this story
        agent = self.agent_registry.select_agent(next_story)
        if not agent:
            return IterationResult(
                story_id=next_story.id,
                story_title=next_story.title,
                success=False,
                duration=time.time() - start_time,
                error_message="No suitable agent available"
            )
        
        # Load context for this iteration
        context = self.memory_manager.get_iteration_context(next_story)
        
        try:
            # Execute the story
            result = agent.execute_story(next_story, context)
            
            # Run quality checks
            quality_passed = self._run_quality_checks()
            
            if quality_passed and result.success:
                # Commit changes
                commit_hash = self._commit_story(next_story)
                
                # Update PRD to mark story as complete
                self.prd_manager.mark_story_complete(next_story.id)
                
                # Update memory and progress
                self._update_memory_progress(next_story, result)
                
                # Update statistics
                self.session_stats.successful_iterations += 1
                self.session_stats.stories_completed.append(next_story.id)
                
                return IterationResult(
                    story_id=next_story.id,
                    story_title=next_story.title,
                    success=True,
                    duration=time.time() - start_time,
                    commit_hash=commit_hash,
                    artifacts=result.get("artifacts", [])
                )
            else:
                # Quality checks failed or story execution failed
                self.session_stats.failed_iterations += 1
                
                return IterationResult(
                    story_id=next_story.id,
                    story_title=next_story.title,
                    success=False,
                    duration=time.time() - start_time,
                    error_message=result.get("error") or "Quality checks failed"
                )
                
        except Exception as e:
            self.logger.error(f"Error executing story {next_story.id}: {str(e)}")
            self.session_stats.failed_iterations += 1
            
            return IterationResult(
                story_id=next_story.id,
                story_title=next_story.title,
                success=False,
                duration=time.time() - start_time,
                error_message=str(e)
            )
        finally:
            # Update session statistics
            self.session_stats.total_iterations += 1
            self.session_stats.total_duration += time.time() - start_time
    
    def _run_quality_checks(self) -> bool:
        """Run project quality checks."""
        try:
            # Get quality commands from config
            quality_commands = self.config.get_quality_commands()
            
            for cmd in quality_commands:
                result = self.version_control.run_command(cmd)
                if result["exit_code"] != 0:
                    self.logger.warning(f"Quality check failed: {cmd}")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error running quality checks: {str(e)}")
            return False
    
    def _commit_story(self, story: UserStory) -> Optional[str]:
        """Commit changes for a completed story."""
        try:
            # Get appropriate commit message
            commit_message = f"feat: {story.id} - {story.title}"
            
            # Stage changes and commit
            self.version_control.stage_all()
            commit_hash = self.version_control.commit(commit_message)
            
            if commit_hash:
                self.session_stats.commits_made.append(commit_hash)
                self.logger.info(f"Committed story {story.id}: {commit_hash}")
                return commit_hash
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error committing story {story.id}: {str(e)}")
            return None
    
    def _update_memory_progress(self, story: UserStory, result: Dict[str, Any]):
        """Update memory and progress tracking."""
        try:
            # Get current progress
            progress = self.memory_manager.get_progress()
            
            # Add story completion
            progress.add_story_completion(story.id, {
                "timestamp": datetime.now().isoformat(),
                "story_title": story.title,
                "artifacts": result.get("artifacts", []),
                "learnings": result.get("learnings", [])
            })
            
            # Save updated progress
            self.memory_manager.save_progress()
            
            self.logger.info(f"Updated memory progress for story {story.id}")
            
        except Exception as e:
            self.logger.error(f"Error updating memory progress: {str(e)}")
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of the current session."""
        if self.session_stats.total_iterations == 0:
            return {"status": "no_iterations"}
        
        return {
            "session_id": self.current_session_id,
            "total_iterations": self.session_stats.total_iterations,
            "successful_iterations": self.session_stats.successful_iterations,
            "failed_iterations": self.session_stats.failed_iterations,
            "success_rate": self.session_stats.successful_iterations / max(self.session_stats.total_iterations, 1),
            "total_duration": self.session_stats.total_duration,
            "average_iteration_time": self.session_stats.total_duration / max(self.session_stats.total_iterations, 1),
            "stories_completed": self.session_stats.stories_completed,
            "commits_made": self.session_stats.commits_made,
            "remaining_stories": len([s for s in self.prd_manager.get_all_stories() if not s.passes])
        }
    
    def end_session(self):
        """End the current session."""
        if self.current_session_id:
            self.logger.info(f"Ending session: {self.current_session_id}")
            self.current_session_id = None
            self.iteration_count = 0
            
            # Save final progress
            self.memory_manager.save_session_summary(self.get_session_summary())
    
    def is_complete(self) -> bool:
        """Check if all stories are complete."""
        return all(story.passes for story in self.prd_manager.get_all_stories())