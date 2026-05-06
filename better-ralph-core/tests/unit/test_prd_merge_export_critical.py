"""
Tests for PRD merge, export_markdown, and find_critical_path.
"""

import pytest
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Set


@dataclass
class UserStory:
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
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserStory':
        return cls(**data)


class PRDManager:
    def __init__(self):
        self.prd_data: Dict[str, Any] = {}
        self.stories: List[UserStory] = []
        self.file_path: Optional[Path] = None

    def create_prd(self, project_name: str, branch_name: str, description: str,
                  stories: List[UserStory]) -> None:
        self.prd_data = {
            "project": project_name,
            "branch": branch_name,
            "description": description,
            "userStories": [s.to_dict() for s in stories]
        }
        self.stories = list(stories)

    def get_progress_summary(self) -> Dict[str, Any]:
        total = len(self.stories)
        completed = sum(1 for s in self.stories if s.passes)
        return {
            "total_stories": total,
            "completed_stories": completed,
            "completion_percentage": (completed / total * 100) if total > 0 else 0
        }

    def merge_prd(self, other: 'PRDManager', conflict_strategy: str = 'skip') -> Dict[str, int]:
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
                skipped += 1
            elif conflict_strategy == 'rename':
                new_id = f"{story.id}-merged"
                counter = 1
                while new_id in existing_ids:
                    new_id = f"{story.id}-merged-{counter}"
                    counter += 1
                merged_story = UserStory(
                    id=new_id, title=story.title, description=story.description,
                    acceptance_criteria=story.acceptance_criteria.copy(),
                    priority=story.priority, passes=story.passes, notes=story.notes,
                    estimated_hours=story.estimated_hours,
                    dependencies=story.dependencies.copy()
                )
                self.stories.append(merged_story)
                existing_ids.add(new_id)
                renamed += 1
            else:
                skipped += 1

        return {"added": added, "skipped": skipped, "renamed": renamed}

    def export_markdown(self) -> str:
        lines = []
        project = self.prd_data.get('project', 'Untitled Project')
        description = self.prd_data.get('description', '')

        lines.append(f"# {project}")
        lines.append('')
        if description:
            lines.append(description)
            lines.append('')

        total = len(self.stories)
        completed = sum(1 for s in self.stories if s.passes)
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
        roots = [s.id for s in self.stories if not s.dependencies]
        if not roots:
            roots = list(story_ids)

        for root in roots:
            path = dfs(root, {root})
            if len(path) > len(longest):
                longest = path

        return longest


class TestMergePRD:
    def test_merge_no_conflicts(self):
        mgr1 = PRDManager()
        mgr1.create_prd("P1", "main", "", [
            UserStory(id="s1", title="A", description="d", acceptance_criteria=[], priority=1)
        ])
        mgr2 = PRDManager()
        mgr2.create_prd("P2", "main", "", [
            UserStory(id="s2", title="B", description="d", acceptance_criteria=[], priority=2)
        ])
        result = mgr1.merge_prd(mgr2)
        assert result == {"added": 1, "skipped": 0, "renamed": 0}
        assert len(mgr1.stories) == 2

    def test_merge_skip_conflicts(self):
        mgr1 = PRDManager()
        mgr1.create_prd("P1", "main", "", [
            UserStory(id="s1", title="Original", description="d", acceptance_criteria=[], priority=1)
        ])
        mgr2 = PRDManager()
        mgr2.create_prd("P2", "main", "", [
            UserStory(id="s1", title="Updated", description="d", acceptance_criteria=[], priority=2)
        ])
        result = mgr1.merge_prd(mgr2, conflict_strategy='skip')
        assert result == {"added": 0, "skipped": 1, "renamed": 0}
        assert mgr1.stories[0].title == "Original"

    def test_merge_overwrite_conflicts(self):
        mgr1 = PRDManager()
        mgr1.create_prd("P1", "main", "", [
            UserStory(id="s1", title="Original", description="d", acceptance_criteria=[], priority=1)
        ])
        mgr2 = PRDManager()
        mgr2.create_prd("P2", "main", "", [
            UserStory(id="s1", title="Updated", description="d", acceptance_criteria=[], priority=2)
        ])
        result = mgr1.merge_prd(mgr2, conflict_strategy='overwrite')
        assert result == {"added": 0, "skipped": 1, "renamed": 0}
        assert mgr1.stories[0].title == "Updated"

    def test_merge_rename_conflicts(self):
        mgr1 = PRDManager()
        mgr1.create_prd("P1", "main", "", [
            UserStory(id="s1", title="Original", description="d", acceptance_criteria=[], priority=1)
        ])
        mgr2 = PRDManager()
        mgr2.create_prd("P2", "main", "", [
            UserStory(id="s1", title="Updated", description="d", acceptance_criteria=[], priority=2)
        ])
        result = mgr1.merge_prd(mgr2, conflict_strategy='rename')
        assert result == {"added": 0, "skipped": 0, "renamed": 1}
        assert len(mgr1.stories) == 2
        assert mgr1.stories[1].id == "s1-merged"

    def test_merge_empty_other(self):
        mgr1 = PRDManager()
        mgr1.create_prd("P1", "main", "", [
            UserStory(id="s1", title="A", description="d", acceptance_criteria=[], priority=1)
        ])
        mgr2 = PRDManager()
        result = mgr1.merge_prd(mgr2)
        assert result == {"added": 0, "skipped": 0, "renamed": 0}
        assert len(mgr1.stories) == 1


class TestExportMarkdown:
    def test_basic_export(self):
        mgr = PRDManager()
        mgr.create_prd("My Project", "main", "A test project", [
            UserStory(id="s1", title="Login", description="User login feature",
                     acceptance_criteria=["User can log in"], priority=1)
        ])
        md = mgr.export_markdown()
        assert "# My Project" in md
        assert "A test project" in md
        assert "⬜ s1: Login" in md
        assert "- User can log in" in md

    def test_completed_story_shows_checkmark(self):
        mgr = PRDManager()
        mgr.create_prd("P", "main", "", [
            UserStory(id="s1", title="Done", description="d",
                     acceptance_criteria=[], priority=1, passes=True)
        ])
        md = mgr.export_markdown()
        assert "✅ s1: Done" in md

    def test_export_with_metadata(self):
        mgr = PRDManager()
        mgr.create_prd("P", "main", "", [
            UserStory(id="s1", title="T", description="d",
                     acceptance_criteria=["AC1"],
                     priority=1, notes="Important",
                     estimated_hours=4.0,
                     dependencies=["s0"])
        ])
        md = mgr.export_markdown()
        assert "**Dependencies:** s0" in md
        assert "**Estimated:** 4.0h" in md
        assert "**Notes:** Important" in md

    def test_export_empty_prd(self):
        mgr = PRDManager()
        mgr.create_prd("Empty", "main", "", [])
        md = mgr.export_markdown()
        assert "# Empty" in md
        assert "Progress: 0/0 (0%)" in md

    def test_progress_calculation(self):
        mgr = PRDManager()
        mgr.create_prd("P", "main", "", [
            UserStory(id="s1", title="A", description="d", acceptance_criteria=[], priority=1, passes=True),
            UserStory(id="s2", title="B", description="d", acceptance_criteria=[], priority=2, passes=False),
            UserStory(id="s3", title="C", description="d", acceptance_criteria=[], priority=3, passes=True),
        ])
        md = mgr.export_markdown()
        assert "Progress: 2/3 (67%)" in md


class TestFindCriticalPath:
    def test_no_dependencies(self):
        mgr = PRDManager()
        mgr.create_prd("P", "main", "", [
            UserStory(id="s1", title="A", description="d", acceptance_criteria=[], priority=1),
            UserStory(id="s2", title="B", description="d", acceptance_criteria=[], priority=2),
        ])
        assert mgr.find_critical_path() == []

    def test_linear_chain(self):
        mgr = PRDManager()
        mgr.create_prd("P", "main", "", [
            UserStory(id="s1", title="A", description="d", acceptance_criteria=[], priority=1),
            UserStory(id="s2", title="B", description="d", acceptance_criteria=[], priority=2, dependencies=["s1"]),
            UserStory(id="s3", title="C", description="d", acceptance_criteria=[], priority=3, dependencies=["s2"]),
        ])
        path = mgr.find_critical_path()
        assert path == ["s1", "s2", "s3"]

    def test_diamond_shape(self):
        mgr = PRDManager()
        mgr.create_prd("P", "main", "", [
            UserStory(id="s1", title="Root", description="d", acceptance_criteria=[], priority=1),
            UserStory(id="s2a", title="Left", description="d", acceptance_criteria=[], priority=2, dependencies=["s1"]),
            UserStory(id="s2b", title="Right", description="d", acceptance_criteria=[], priority=2, dependencies=["s1"]),
            UserStory(id="s3", title="Merge", description="d", acceptance_criteria=[], priority=3, dependencies=["s2a", "s2b"]),
        ])
        path = mgr.find_critical_path()
        assert len(path) == 3  # s1 -> s2a/s2b -> s3
        assert path[0] == "s1"
        assert path[-1] == "s3"

    def test_longer_branch_wins(self):
        mgr = PRDManager()
        mgr.create_prd("P", "main", "", [
            UserStory(id="root", title="R", description="d", acceptance_criteria=[], priority=1),
            # Short branch: root -> s2 -> s4
            UserStory(id="s2", title="B2", description="d", acceptance_criteria=[], priority=2, dependencies=["root"]),
            UserStory(id="s4", title="B4", description="d", acceptance_criteria=[], priority=4, dependencies=["s2"]),
            # Long branch: root -> s3 -> s5 -> s6
            UserStory(id="s3", title="B3", description="d", acceptance_criteria=[], priority=3, dependencies=["root"]),
            UserStory(id="s5", title="B5", description="d", acceptance_criteria=[], priority=5, dependencies=["s3"]),
            UserStory(id="s6", title="B6", description="d", acceptance_criteria=[], priority=6, dependencies=["s5"]),
        ])
        path = mgr.find_critical_path()
        assert len(path) == 4  # root -> s3 -> s5 -> s6
        assert path == ["root", "s3", "s5", "s6"]

    def test_single_story(self):
        mgr = PRDManager()
        mgr.create_prd("P", "main", "", [
            UserStory(id="s1", title="A", description="d", acceptance_criteria=[], priority=1),
        ])
        assert mgr.find_critical_path() == []
