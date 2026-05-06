"""
Memory Manager - Context persistence and memory management.

Handles loading, storing, and retrieving context information between iterations.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field, asdict

from utils.logger import Logger


@dataclass
class IterationContext:
    """Context information for a specific iteration."""
    story_id: str
    story_title: str
    timestamp: str
    artifacts: List[str] = field(default_factory=list)
    learnings: List[str] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "story_id": self.story_id,
            "story_title": self.story_title,
            "timestamp": self.timestamp,
            "artifacts": self.artifacts,
            "learnings": self.learnings,
            "patterns": self.patterns,
            "errors": self.errors,
            "metrics": self.metrics,
            "notes": self.notes,
        }


@dataclass
class ProjectContext:
    """Overall project context and patterns."""
    project_name: str
    project_root: Path
    code_patterns: List[str] = field(default_factory=list)
    common_gotchas: List[str] = field(default_factory=list)
    file_types: Dict[str, str] = field(default_factory=dict)
    conventions: Dict[str, str] = field(default_factory=dict)
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())


class MemoryManager:
    """
    Manages context persistence and memory across iterations.
    
    Handles loading and storing project context, tracking patterns,
    and maintaining memory of previous iterations.
    """
    
    def __init__(self, memory_dir: Optional[Path] = None):
        """
        Initialize the memory manager.
        
        Args:
            memory_dir: Directory to store memory files
        """
        self.logger = Logger.get_logger("memory_manager")
        self.memory_dir = memory_dir or Path.home() / ".better-ralph" / "memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Memory files
        self.project_context_file = self.memory_dir / "project_context.json"
        self.progress_file = self.memory_dir / "progress.txt"
        self.iterations_file = self.memory_dir / "iterations.json"
        self.patterns_file = self.memory_dir / "patterns.json"
        
        # In-memory data
        self.project_context: Optional[ProjectContext] = None
        self.iterations: List[IterationContext] = []
        self.patterns: Dict[str, Any] = {}
        
        # Load existing data
        self._load_memory()
        
        self.logger.info("Memory Manager initialized")
    
    def initialize_session(self, project_root: Path) -> None:
        """
        Initialize a new session with project context.
        
        Args:
            project_root: Root directory of the project
        """
        # Create or update project context
        self.project_context = ProjectContext(
            project_name=self._detect_project_name(project_root),
            project_root=project_root,
            last_updated=datetime.now().isoformat()
        )
        
        # Scan project for patterns
        self._scan_project_patterns(project_root)
        
        # Save initial context
        self._save_project_context()
        
        self.logger.info(f"Initialized session for project: {self.project_context.project_name}")
    
    def get_iteration_context(self, story) -> Dict[str, Any]:
        """
        Get context for a specific iteration.
        
        Args:
            story: Current story being worked on
            
        Returns:
            Context dictionary for the iteration
        """
        context = {
            "story": {
                "id": story.id,
                "title": story.title,
                "description": story.description,
                "acceptance_criteria": story.acceptance_criteria
            },
            "project": self._get_project_context(),
            "memory": self._get_memory_context(),
            "patterns": self._get_patterns_context()
        }
        
        return context
    
    def add_iteration_result(self, story_id: str, story_title: str, 
                           artifacts: List[str], learnings: List[str],
                           patterns: List[str], errors: List[str],
                           metrics: Dict[str, Any]) -> None:
        """
        Add the result of an iteration to memory.
        
        Args:
            story_id: ID of the story that was worked on
            story_title: Title of the story
            artifacts: List of files created/modified
            learnings: List of learnings from this iteration
            patterns: Patterns discovered during this iteration
            errors: Errors encountered during this iteration
            metrics: Performance metrics
        """
        iteration = IterationContext(
            story_id=story_id,
            story_title=story_title,
            timestamp=datetime.now().isoformat(),
            artifacts=artifacts,
            learnings=learnings,
            patterns=patterns,
            errors=errors,
            metrics=metrics
        )
        
        self.iterations.append(iteration)
        self._update_patterns(patterns, learnings)
        self._save_iterations()
        self._save_patterns()
        
        self.logger.info(f"Added iteration result for story {story_id}")
    
    def add_story_completion(self, story_id: str, completion_data: Dict[str, Any]) -> None:
        """
        Add completion data for a story.
        
        Args:
            story_id: ID of the completed story
            completion_data: Data about the completion
        """
        # Find the last iteration for this story
        story_iterations = [i for i in self.iterations if i.story_id == story_id]
        if story_iterations:
            last_iteration = story_iterations[-1]
            for key, value in completion_data.items():
                if hasattr(last_iteration, key):
                    setattr(last_iteration, key, value)
            
            self._save_iterations()
            self.logger.info(f"Added completion data for story {story_id}")
        else:
            self.logger.warning(f"No iterations found for story {story_id}")
    
    def get_progress(self) -> Dict[str, Any]:
        """
        Get overall progress information.
        
        Returns:
            Progress summary dictionary
        """
        total_iterations = len(self.iterations)
        successful_iterations = len([i for i in self.iterations if not i.errors])
        failed_iterations = total_iterations - successful_iterations
        
        # Calculate average metrics
        avg_metrics = {}
        if total_iterations > 0:
            metric_keys = self.iterations[0].metrics.keys()
            for key in metric_keys:
                values = [i.metrics.get(key, 0) for i in self.iterations if key in i.metrics]
                if values:
                    avg_metrics[key] = sum(values) / len(values)
        
        return {
            "total_iterations": total_iterations,
            "successful_iterations": successful_iterations,
            "failed_iterations": failed_iterations,
            "success_rate": successful_iterations / max(total_iterations, 1),
            "average_metrics": avg_metrics,
            "recent_iterations": [i.to_dict() for i in self.iterations[-5:]],
            "total_artifacts": len(set().union(*[i.artifacts for i in self.iterations])),
            "unique_stories": len(set(i.story_id for i in self.iterations))
        }
    
    def save_session_summary(self, summary: Dict[str, Any]) -> None:
        """Save a session summary to memory."""
        session_file = self.memory_dir / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved session summary to {session_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving session summary: {e}")
    
    def _load_memory(self) -> None:
        """Load existing memory data from files."""
        try:
            # Load project context
            if self.project_context_file.exists():
                with open(self.project_context_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'project_root' in data:
                        data['project_root'] = Path(data['project_root'])
                    self.project_context = ProjectContext(**data)
            
            # Load iterations
            if self.iterations_file.exists():
                with open(self.iterations_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.iterations = [IterationContext(**item) for item in data]
            
            # Load patterns
            if self.patterns_file.exists():
                with open(self.patterns_file, 'r', encoding='utf-8') as f:
                    self.patterns = json.load(f)
            
            self.logger.info(f"Loaded memory: {len(self.iterations)} iterations, {len(self.patterns)} patterns")
            
        except Exception as e:
            self.logger.error(f"Error loading memory: {e}")
    
    def _save_project_context(self) -> None:
        """Save project context to file."""
        try:
            if self.project_context:
                data = asdict(self.project_context)
                data['project_root'] = str(data['project_root'])
                with open(self.project_context_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving project context: {e}")
    
    def _save_iterations(self) -> None:
        """Save iterations to file."""
        try:
            with open(self.iterations_file, 'w', encoding='utf-8') as f:
                json.dump([asdict(i) for i in self.iterations], f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving iterations: {e}")
    
    def _save_patterns(self) -> None:
        """Save patterns to file."""
        try:
            with open(self.patterns_file, 'w', encoding='utf-8') as f:
                json.dump(self.patterns, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving patterns: {e}")
    
    def _detect_project_name(self, project_root: Path) -> str:
        """Detect project name from directory."""
        # Try common project files
        common_files = ["package.json", "pyproject.toml", "setup.py", "Cargo.toml", "go.mod"]
        
        for file in common_files:
            if (project_root / file).exists():
                return file.replace(".json", "").replace(".toml", "").replace(".py", "").replace(".mod", "")
        
        # Fall back to directory name
        return project_root.name
    
    def _scan_project_patterns(self, project_root: Path) -> None:
        """Scan project for patterns and conventions."""
        try:
            # Scan common file types
            file_extensions = []
            for file in project_root.rglob("*"):
                if file.is_file() and not file.name.startswith('.'):
                    ext = file.suffix.lower()
                    if ext and ext not in ['.pyc', '.class', '.gitignore']:
                        file_extensions.append(ext)
            
            # Deduplicate and count
            file_counts = {}
            for ext in file_extensions:
                file_counts[ext] = file_counts.get(ext, 0) + 1
            
            self.project_context.file_types = file_counts
            
            # Look for common patterns
            self._detect_conventions(project_root)
            
            self.logger.info(f"Scanned project patterns: {len(file_counts)} file types")
            
        except Exception as e:
            self.logger.error(f"Error scanning project patterns: {e}")
    
    def _detect_conventions(self, project_root: Path) -> None:
        """Detect project conventions."""
        conventions = {}
        
        # Check for common directories
        common_dirs = ["src", "lib", "components", "utils", "tests", "docs"]
        for dir_name in common_dirs:
            if (project_root / dir_name).exists():
                conventions[dir_name] = "common"
        
        # Check for build files
        build_files = ["Makefile", "build.gradle", "pom.xml", "requirements.txt", "package.json"]
        for build_file in build_files:
            if (project_root / build_file).exists():
                conventions[build_file] = "build"
        
        self.project_context.conventions = conventions
    
    def _get_project_context(self) -> Dict[str, Any]:
        """Get project context for iterations."""
        if not self.project_context:
            return {}
        
        return {
            "project_name": self.project_context.project_name,
            "project_root": str(self.project_context.project_root),
            "file_types": self.project_context.file_types,
            "conventions": self.project_context.conventions
        }
    
    def _get_memory_context(self) -> Dict[str, Any]:
        """Get memory context for iterations."""
        recent_iterations = self.iterations[-5:] if len(self.iterations) > 0 else []
        
        # Extract common learnings
        common_learnings = []
        for iteration in recent_iterations:
            common_learnings.extend(iteration.learnings)
        
        # Get unique learnings
        unique_learnings = list(set(common_learnings))
        
        return {
            "recent_iterations": len(recent_iterations),
            "total_iterations": len(self.iterations),
            "common_learnings": unique_learnings[:10],  # Limit to 10
            "recent_artifacts": [item for sublist in [i.artifacts for i in recent_iterations] for item in sublist][-10:]
        }
    
    def _get_patterns_context(self) -> Dict[str, Any]:
        """Get patterns context for iterations."""
        return {
            "code_patterns": self.patterns.get("code_patterns", []),
            "common_patterns": self.patterns.get("common_patterns", []),
            "avoid_patterns": self.patterns.get("avoid_patterns", [])
        }
    
    def _update_patterns(self, patterns: List[str], learnings: List[str]) -> None:
        """Update patterns based on iteration results."""
        # Update code patterns
        if "code_patterns" not in self.patterns:
            self.patterns["code_patterns"] = []
        
        for pattern in patterns:
            if pattern not in self.patterns["code_patterns"]:
                self.patterns["code_patterns"].append(pattern)
        
        # Update common patterns
        if "common_patterns" not in self.patterns:
            self.patterns["common_patterns"] = []
        
        for learning in learnings:
            if learning not in self.patterns["common_patterns"]:
                self.patterns["common_patterns"].append(learning)
        
        # Limit patterns to prevent memory growth
        max_patterns = 100
        if len(self.patterns["code_patterns"]) > max_patterns:
            self.patterns["code_patterns"] = self.patterns["code_patterns"][-max_patterns:]
        
        if len(self.patterns["common_patterns"]) > max_patterns:
            self.patterns["common_patterns"] = self.patterns["common_patterns"][-max_patterns:]
    
    def search_iterations(self, query: str = "", story_id: Optional[str] = None,
                          has_errors: Optional[bool] = None) -> List[IterationContext]:
        """
        Search past iterations by keyword, story_id, or error status.
        
        Args:
            query: Keyword to search in title, learnings, patterns, notes
            story_id: Filter by specific story ID
            has_errors: If True, only iterations with errors; if False, only without
            
        Returns:
            List of matching IterationContext objects
        """
        results = self.iterations
        
        if story_id is not None:
            results = [i for i in results if i.story_id == story_id]
        
        if has_errors is not None:
            if has_errors:
                results = [i for i in results if i.errors]
            else:
                results = [i for i in results if not i.errors]
        
        if query:
            q = query.lower()
            matched = []
            for i in results:
                searchable = " ".join([
                    i.story_title, i.notes,
                    *i.learnings, *i.patterns, *i.errors
                ]).lower()
                if q in searchable:
                    matched.append(i)
            results = matched
        
        return results
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of all memory data."""
        return {
            "project_context": {
                "project_name": self.project_context.project_name if self.project_context else None,
                "file_types": self.project_context.file_types if self.project_context else {},
                "conventions": self.project_context.conventions if self.project_context else {}
            },
            "iterations_count": len(self.iterations),
            "iterations_summary": [i.to_dict() for i in self.iterations],
            "patterns_count": len(self.patterns),
            "memory_directory": str(self.memory_dir)
        }