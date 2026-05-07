"""
PRD Manager - Product Requirements Document management.

Handles loading, parsing, and managing PRD stories and their state.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field, asdict

from utils.logger import Logger


@dataclass
class UserStory:
    """Represents a single user story in the PRD."""
    id: str
    title: str
    description: str
    acceptance_criteria: List[str]
    priority: int
    passes: bool = False
    notes: str = ""
    estimated_hours: Optional[float] = None
    dependencies: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserStory':
        """Create from dictionary."""
        return cls(**data)


class PRDManager:
    """
    Manages Product Requirements Document (PRD) stories and their state.
    
    Handles loading PRD files, managing story states, and providing methods
    to track progress and manage stories.
    """
    
    def __init__(self):
        """Initialize the PRD manager."""
        self.logger = Logger.get_logger("prd_manager")
        self.prd_data: Dict[str, Any] = {}
        self.stories: List[UserStory] = []
        self.file_path: Optional[Path] = None
        
        self.logger.info("PRD Manager initialized")
    
    def load_prd(self, prd_path: Path) -> None:
        """
        Load PRD from a JSON file.
        
        Args:
            prd_path: Path to the PRD JSON file
        """
        self.file_path = prd_path
        
        try:
            with open(prd_path, 'r', encoding='utf-8') as f:
                self.prd_data = json.load(f)
            
            # Parse stories
            self.stories = []
            for story_data in self.prd_data.get("userStories", []):
                story = UserStory.from_dict(story_data)
                self.stories.append(story)
            
            self.logger.info(f"Loaded PRD from {prd_path}: {len(self.stories)} stories")
            
        except FileNotFoundError:
            self.logger.error(f"PRD file not found: {prd_path}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in PRD file: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading PRD: {e}")
            raise
    
    def create_prd(self, project_name: str, branch_name: str, description: str, 
                  stories: List[UserStory]) -> None:
        """
        Create a new PRD with the given stories.
        
        Args:
            project_name: Name of the project
            branch_name: Git branch name
            description: Short project description
            stories: List of user stories
        """
        self.prd_data = {
            "project": project_name,
            "branchName": branch_name,
            "description": description,
            "userStories": [story.to_dict() for story in stories],
            "createdAt": datetime.now().isoformat()
        }
        
        self.stories = stories
        self.logger.info(f"Created new PRD with {len(stories)} stories")
    
    def save_prd(self, output_path: Optional[Path] = None) -> None:
        """
        Save the current PRD to a file.
        
        Args:
            output_path: Optional output path. If None, uses original path.
        """
        save_path = output_path or self.file_path
        
        if not save_path:
            raise ValueError("No output path specified")
        
        try:
            # Update story data in prd_data
            self.prd_data["userStories"] = [story.to_dict() for story in self.stories]
            self.prd_data["updatedAt"] = datetime.now().isoformat()
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self.prd_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved PRD to {save_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving PRD: {e}")
            raise
    
    def get_all_stories(self) -> List[UserStory]:
        """Get all user stories."""
        return self.stories
    
    def get_story_by_id(self, story_id: str) -> Optional[UserStory]:
        """Get a specific user story by ID."""
        for story in self.stories:
            if story.id == story_id:
                return story
        return None
    
    def get_next_story(self) -> Optional[UserStory]:
        """
        Get the next highest priority incomplete story.
        
        Returns:
            The next story to work on, or None if all stories are complete
        """
        # Filter incomplete stories
        incomplete_stories = [s for s in self.stories if not s.passes]
        
        if not incomplete_stories:
            return None
        
        # Sort by priority (lower number = higher priority)
        incomplete_stories.sort(key=lambda s: s.priority)
        
        # Check dependencies
        next_story = incomplete_stories[0]
        
        # Check if this story's dependencies are met
        if not self._check_dependencies_met(next_story):
            # Find next story without dependencies or with met dependencies
            for story in incomplete_stories[1:]:
                if self._check_dependencies_met(story):
                    next_story = story
                    break
        
        return next_story
    
    def _check_dependencies_met(self, story: UserStory) -> bool:
        """Check if all dependencies for a story are met."""
        if not story.dependencies:
            return True
        
        for dep_id in story.dependencies:
            dep_story = self.get_story_by_id(dep_id)
            if not dep_story or not dep_story.passes:
                return False
        
        return True
    
    def mark_story_complete(self, story_id: str) -> None:
        """
        Mark a story as complete.
        
        Args:
            story_id: ID of the story to mark complete
        """
        story = self.get_story_by_id(story_id)
        if story:
            story.passes = True
            self.logger.info(f"Marked story {story_id} as complete")
        else:
            self.logger.warning(f"Story {story_id} not found for marking complete")
    
    def mark_story_incomplete(self, story_id: str) -> None:
        """
        Mark a story as incomplete.
        
        Args:
            story_id: ID of the story to mark incomplete
        """
        story = self.get_story_by_id(story_id)
        if story:
            story.passes = False
            self.logger.info(f"Marked story {story_id} as incomplete")
        else:
            self.logger.warning(f"Story {story_id} not found for marking incomplete")
    
    def add_story(self, story: UserStory) -> None:
        """
        Add a new story to the PRD.
        
        Args:
            story: User story to add
        """
        self.stories.append(story)
        self.logger.info(f"Added story {story.id} to PRD")
    
    def remove_story(self, story_id: str) -> bool:
        """
        Remove a story from the PRD.
        
        Args:
            story_id: ID of the story to remove
            
        Returns:
            True if story was removed, False if not found
        """
        for i, story in enumerate(self.stories):
            if story.id == story_id:
                del self.stories[i]
                self.logger.info(f"Removed story {story_id} from PRD")
                return True
        
        self.logger.warning(f"Story {story_id} not found for removal")
        return False
    
    def update_story(self, story_id: str, **kwargs) -> bool:
        """
        Update a story with new values.
        
        Args:
            story_id: ID of the story to update
            **kwargs: Fields to update
            
        Returns:
            True if story was updated, False if not found
        """
        story = self.get_story_by_id(story_id)
        if story:
            for key, value in kwargs.items():
                if hasattr(story, key):
                    setattr(story, key, value)
            
            self.logger.info(f"Updated story {story_id}")
            return True
        
        self.logger.warning(f"Story {story_id} not found for update")
        return False
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a summary of PRD progress."""
        total_stories = len(self.stories)
        completed_stories = sum(1 for s in self.stories if s.passes)
        
        # Calculate priority distribution
        priority_stats = {}
        for story in self.stories:
            priority = story.priority
            if priority not in priority_stats:
                priority_stats[priority] = {"total": 0, "completed": 0}
            
            priority_stats[priority]["total"] += 1
            if story.passes:
                priority_stats[priority]["completed"] += 1
        
        return {
            "total_stories": total_stories,
            "completed_stories": completed_stories,
            "progress_percentage": (completed_stories / total_stories) * 100 if total_stories > 0 else 0,
            "priority_distribution": priority_stats,
            "completed_stories_list": [s.id for s in self.stories if s.passes],
            "remaining_stories": [s.id for s in self.stories if not s.passes]
        }
    
    def split_large_story(self, story_id: str, max_criteria: int = 3) -> List[UserStory]:
        """
        Split a large story into smaller stories based on acceptance criteria.
        
        Args:
            story_id: ID of the story to split
            max_criteria: Maximum criteria per story
            
        Returns:
            List of new stories created
        """
        original_story = self.get_story_by_id(story_id)
        if not original_story:
            self.logger.warning(f"Story {story_id} not found for splitting")
            return []
        
        # Remove original story
        self.remove_story(story_id)
        
        # Create new stories
        new_stories = []
        criteria_chunks = self._chunk_list(original_story.acceptance_criteria, max_criteria)
        
        for i, criteria_chunk in enumerate(criteria_chunks):
            new_story = UserStory(
                id=f"{story_id}-{i+1}",
                title=f"{original_story.title} (Part {i+1})",
                description=original_story.description,
                acceptance_criteria=criteria_chunk,
                priority=original_story.priority,
                passes=False,
                notes=original_story.notes,
                estimated_hours=original_story.estimated_hours / len(criteria_chunks) if original_story.estimated_hours else None,
                dependencies=original_story.dependencies
            )
            new_stories.append(new_story)
            self.add_story(new_story)
        
        self.logger.info(f"Split story {story_id} into {len(new_stories)} smaller stories")
        return new_stories

    def reorder_story(self, story_id: str, new_index: int) -> bool:
        """
        Move a story to a new position in the list.

        Args:
            story_id: ID of the story to move
            new_index: Target index (clamped to valid range)

        Returns:
            True if reordered, False if story not found
        """
        idx = None
        for i, s in enumerate(self.stories):
            if s.id == story_id:
                idx = i
                break
        if idx is None:
            self.logger.warning(f"Story {story_id} not found for reorder")
            return False

        clamped = max(0, min(new_index, len(self.stories) - 1))
        story = self.stories.pop(idx)
        self.stories.insert(clamped, story)
        self.logger.info(f"Reordered story {story_id} from {idx} to {clamped}")
        return True

    def duplicate_story(self, story_id: str, new_id: str) -> Optional[UserStory]:
        """
        Create a deep copy of a story with a new ID.

        Args:
            story_id: ID of the story to duplicate
            new_id: ID for the duplicate

        Returns:
            The new story, or None if source not found
        """
        source = self.get_story_by_id(story_id)
        if not source:
            self.logger.warning(f"Story {story_id} not found for duplication")
            return None

        dup = UserStory(
            id=new_id,
            title=source.title,
            description=source.description,
            acceptance_criteria=source.acceptance_criteria.copy(),
            priority=source.priority,
            passes=False,
            notes=source.notes,
            estimated_hours=source.estimated_hours,
            dependencies=source.dependencies.copy(),
        )
        self.stories.append(dup)
        self.logger.info(f"Duplicated story {story_id} as {new_id}")
        return dup
    
    def _chunk_list(self, lst: List[str], size: int) -> List[List[str]]:
        """Split a list into chunks of specified size."""
        return [lst[i:i + size] for i in range(0, len(lst), size)]
    
    def auto_adjust_priorities(self) -> None:
        """
        Automatically adjust story priorities based on dependencies and completion status.
        """
        # Build dependency graph
        dependency_graph = {}
        for story in self.stories:
            dependency_graph[story.id] = story.dependencies
        
        # Calculate dependency depth for each story
        dependency_depths = {}
        for story_id in dependency_graph:
            depth = self._calculate_dependency_depth(story_id, dependency_graph)
            dependency_depths[story_id] = depth
        
        # Adjust priorities based on dependency depth
        for story in self.stories:
            if not story.passes:
                # Increase priority (lower number) for stories with deeper dependencies
                base_priority = 1
                depth_bonus = min(dependency_depths.get(story.id, 0), 5)
                new_priority = base_priority + depth_bonus
                
                if new_priority != story.priority:
                    story.priority = new_priority
                    self.logger.info(f"Adjusted priority for story {story.id}: {story.priority}")
    
    def _calculate_dependency_depth(self, story_id: str, dependency_graph: Dict[str, List[str]], 
                                   visited: Optional[Set[str]] = None) -> int:
        """Calculate the maximum depth of dependencies for a story."""
        if visited is None:
            visited = set()
        
        if story_id in visited:
            return 0  # Circular dependency
        
        visited.add(story_id)
        
        if story_id not in dependency_graph or not dependency_graph[story_id]:
            return 0
        
        max_depth = 0
        for dep_id in dependency_graph[story_id]:
            depth = self._calculate_dependency_depth(dep_id, dependency_graph, visited.copy())
            max_depth = max(max_depth, depth + 1)
        
        return max_depth
    
    def validate_dependencies(self) -> Dict[str, Any]:
        """
        Validate all story dependencies: detect cycles and missing references.
        
        Returns:
            Dict with 'valid' (bool), 'errors' (list), and 'warnings' (list).
        """
        story_ids = {s.id for s in self.stories}
        errors = []
        warnings = []
        
        # Check for missing dependency references
        for story in self.stories:
            for dep_id in story.dependencies:
                if dep_id not in story_ids:
                    errors.append(f"Story '{story.id}' depends on '{dep_id}' which does not exist")
        
        # Check for circular dependencies using DFS
        def has_cycle(node: str, visited: Set[str], rec_stack: Set[str]) -> Optional[List[str]]:
            visited.add(node)
            rec_stack.add(node)
            story = self.get_story_by_id(node)
            if story:
                for dep_id in story.dependencies:
                    if dep_id not in story_ids:
                        continue
                    if dep_id not in visited:
                        result = has_cycle(dep_id, visited, rec_stack)
                        if result is not None:
                            return [node] + result
                    elif dep_id in rec_stack:
                        return [node, dep_id]
            rec_stack.discard(node)
            return None
        
        visited: Set[str] = set()
        for story in self.stories:
            if story.id not in visited:
                cycle = has_cycle(story.id, visited, set())
                if cycle is not None:
                    cycle_str = ' -> '.join(cycle)
                    errors.append(f"Circular dependency detected: {cycle_str}")
        
        # Check for self-dependencies
        for story in self.stories:
            if story.id in story.dependencies:
                errors.append(f"Story '{story.id}' has a self-dependency")
        
        # Warn about stories with many dependencies (maintenance risk)
        for story in self.stories:
            if len(story.dependencies) > 3:
                warnings.append(
                    f"Story '{story.id}' has {len(story.dependencies)} dependencies "
                    f"(consider splitting)"
                )
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

    def merge_prd(self, other: 'PRDManager', conflict_strategy: str = 'skip') -> Dict[str, int]:
        """
        Merge stories from another PRD into this one.

        Args:
            other: Another PRDManager to merge from
            conflict_strategy: How to handle duplicate IDs - 'skip', 'overwrite', or 'rename'

        Returns:
            Dict with counts: added, skipped, renamed
        """
        existing_ids = {s.id for s in self.stories}
        added = skipped = renamed = 0

        for story in other.stories:
            if story.id not in existing_ids:
                self.stories.append(story)
                existing_ids.add(story.id)
                added += 1
            elif conflict_strategy == 'overwrite':
                for i, s in enumerate(self.stories):
                    if s.id == story.id:
                        self.stories[i] = story
                        break
                skipped += 1  # overwritten count
            elif conflict_strategy == 'rename':
                new_id = f"{story.id}-merged"
                counter = 1
                while new_id in existing_ids:
                    new_id = f"{story.id}-merged-{counter}"
                    counter += 1
                merged_story = UserStory(
                    id=new_id,
                    title=story.title,
                    description=story.description,
                    acceptance_criteria=story.acceptance_criteria.copy(),
                    priority=story.priority,
                    passes=story.passes,
                    notes=story.notes,
                    estimated_hours=story.estimated_hours,
                    dependencies=story.dependencies.copy()
                )
                self.stories.append(merged_story)
                existing_ids.add(new_id)
                renamed += 1
            else:  # skip
                skipped += 1

        self.logger.info(f"Merged PRD: {added} added, {skipped} skipped, {renamed} renamed")
        return {"added": added, "skipped": skipped, "renamed": renamed}

    def export_markdown(self) -> str:
        """
        Export the PRD as a Markdown document.

        Returns:
            Markdown string representation of the PRD
        """
        lines = []
        project = self.prd_data.get('project', 'Untitled Project')
        description = self.prd_data.get('description', '')

        lines.append(f"# {project}")
        lines.append('')
        if description:
            lines.append(description)
            lines.append('')

        summary = self.get_progress_summary()
        total = summary['total_stories'] if isinstance(summary.get('total_stories'), int) else len(self.stories)
        completed = summary['completed_stories'] if isinstance(summary.get('completed_stories'), int) else sum(1 for s in self.stories if s.passes)
        pct = (completed / total * 100) if total > 0 else 0
        lines.append(f"## Progress: {completed}/{total} ({pct:.0f}%)")
        lines.append('')

        for story in self.stories:
            status = '✅' if story.passes else '⬜'
            lines.append(f"### {status} {story.id}: {story.title}")
            lines.append('')
            lines.append(story.description)
            lines.append('')
            if story.acceptance_criteria:
                lines.append('**Acceptance Criteria:**')
                for ac in story.acceptance_criteria:
                    lines.append(f"- {ac}")
                lines.append('')
            if story.dependencies:
                lines.append(f"**Dependencies:** {', '.join(story.dependencies)}")
                lines.append('')
            if story.estimated_hours:
                lines.append(f"**Estimated:** {story.estimated_hours}h")
                lines.append('')
            if story.notes:
                lines.append(f"**Notes:** {story.notes}")
                lines.append('')

        return '\n'.join(lines)

    def find_critical_path(self) -> List[str]:
        """
        Find the longest dependency chain (critical path).

        Returns:
            List of story IDs forming the critical path, or empty list if no dependencies.
        """
        story_ids = {s.id for s in self.stories}
        dependents: Dict[str, List[str]] = {s.id: [] for s in self.stories}
        has_deps = False

        for story in self.stories:
            for dep_id in story.dependencies:
                if dep_id in dependents:
                    dependents[dep_id].append(story.id)
                    has_deps = True

        if not has_deps:
            return []

        def dfs(node: str, visited: Set[str]) -> List[str]:
            best_path = [node]
            for child in dependents.get(node, []):
                if child not in visited:
                    child_path = dfs(child, visited | {child})
                    if len(child_path) + 1 > len(best_path):
                        best_path = [node] + child_path
            return best_path

        longest: List[str] = []
        # Start from stories with no dependencies (roots)
        roots = [s.id for s in self.stories if not s.dependencies]
        if not roots:
            # All stories have dependencies; pick any as root
            roots = list(story_ids)

        for root in roots:
            path = dfs(root, {root})
            if len(path) > len(longest):
                longest = path

        return longest