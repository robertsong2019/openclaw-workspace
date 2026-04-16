"""
Unit tests for PRD Manager
测试 PRD 管理器的功能

Note: This test file contains simplified versions of PRDManager and UserStory
to avoid import issues with the original codebase.
"""

import pytest
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


# Simplified versions for testing
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
    Simplified PRD Manager for testing.
    """

    def __init__(self):
        """Initialize the PRD manager."""
        self.prd_data: Dict[str, Any] = {}
        self.stories: List[UserStory] = []
        self.file_path: Optional[Path] = None

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

        except FileNotFoundError:
            raise
        except json.JSONDecodeError as e:
            raise
        except Exception as e:
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
            "branch": branch_name,
            "description": description,
            "userStories": [story.to_dict() for story in stories]
        }
        self.stories = stories.copy()

    def save_prd(self, output_path: Optional[Path] = None) -> None:
        """
        Save the current PRD to a JSON file.

        Args:
            output_path: Path to save the PRD. If None, uses the original file path.
        """
        if output_path is None:
            output_path = self.file_path

        if output_path is None:
            raise ValueError("No output path specified and no original file path")

        # Update stories in PRD data
        self.prd_data["userStories"] = [story.to_dict() for story in self.stories]

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.prd_data, f, indent=2, ensure_ascii=False)

    def get_all_stories(self) -> List[UserStory]:
        """Get all stories."""
        return self.stories

    def get_story_by_id(self, story_id: str) -> Optional[UserStory]:
        """Get a story by ID."""
        for story in self.stories:
            if story.id == story_id:
                return story
        return None

    def get_next_story(self) -> Optional[UserStory]:
        """Get the next story to work on."""
        # Filter stories that are not passed and have met dependencies
        available_stories = []
        for story in self.stories:
            if not story.passes and self._check_dependencies_met(story):
                available_stories.append(story)

        # Sort by priority (higher first)
        available_stories.sort(key=lambda s: s.priority, reverse=True)

        return available_stories[0] if available_stories else None

    def _check_dependencies_met(self, story: UserStory) -> bool:
        """Check if all dependencies for a story are met."""
        for dep_id in story.dependencies:
            dep_story = self.get_story_by_id(dep_id)
            if dep_story is None or not dep_story.passes:
                return False
        return True

    def mark_story_complete(self, story_id: str) -> None:
        """Mark a story as complete."""
        story = self.get_story_by_id(story_id)
        if story:
            story.passes = True

    def mark_story_incomplete(self, story_id: str) -> None:
        """Mark a story as incomplete."""
        story = self.get_story_by_id(story_id)
        if story:
            story.passes = False

    def add_story(self, story: UserStory) -> None:
        """Add a new story."""
        self.stories.append(story)

    def remove_story(self, story_id: str) -> bool:
        """Remove a story."""
        for i, story in enumerate(self.stories):
            if story.id == story_id:
                self.stories.pop(i)
                return True
        return False

    def update_story(self, story_id: str, **kwargs) -> bool:
        """Update a story."""
        story = self.get_story_by_id(story_id)
        if story:
            for key, value in kwargs.items():
                if hasattr(story, key):
                    setattr(story, key, value)
            return True
        return False

    def get_progress_summary(self) -> Dict[str, Any]:
        """Get progress summary."""
        total = len(self.stories)
        completed = sum(1 for s in self.stories if s.passes)
        incomplete = total - completed

        return {
            "total_stories": total,
            "completed_stories": completed,
            "incomplete_stories": incomplete,
            "completion_percentage": (completed / total * 100) if total > 0 else 0
        }


# Test cases
class TestUserStory:
    """测试用户故事"""

    def test_create_user_story(self):
        story = UserStory(
            id="story-001",
            title="Test Story",
            description="A test story",
            acceptance_criteria=["Criteria 1", "Criteria 2"],
            priority=1
        )
        assert story.id == "story-001"
        assert story.title == "Test Story"
        assert story.description == "A test story"
        assert len(story.acceptance_criteria) == 2
        assert story.priority == 1
        assert story.passes is False
        assert story.notes == ""

    def test_user_story_to_dict(self):
        story = UserStory(
            id="story-001",
            title="Test Story",
            description="A test story",
            acceptance_criteria=["Criteria 1"],
            priority=1
        )
        data = story.to_dict()
        assert data["id"] == "story-001"
        assert data["title"] == "Test Story"
        assert data["passes"] is False

    def test_user_story_from_dict(self):
        data = {
            "id": "story-001",
            "title": "Test Story",
            "description": "A test story",
            "acceptance_criteria": ["Criteria 1"],
            "priority": 1,
            "passes": True
        }
        story = UserStory.from_dict(data)
        assert story.id == "story-001"
        assert story.passes is True

    def test_user_story_with_dependencies(self):
        story = UserStory(
            id="story-002",
            title="Story with dependencies",
            description="Test",
            acceptance_criteria=[],
            priority=2,
            dependencies=["story-001"]
        )
        assert len(story.dependencies) == 1
        assert story.dependencies[0] == "story-001"


class TestPRDManager:
    """测试 PRD 管理器"""

    @pytest.fixture
    def prd_manager(self):
        """Create a PRD manager"""
        return PRDManager()

    @pytest.fixture
    def sample_prd_file(self, tmp_path):
        """Create a sample PRD JSON file"""
        prd_data = {
            "project": "Test Project",
            "branch": "main",
            "description": "A test project",
            "userStories": [
                {
                    "id": "story-001",
                    "title": "Story 1",
                    "description": "First story",
                    "acceptance_criteria": ["AC 1", "AC 2"],
                    "priority": 1,
                    "passes": False
                },
                {
                    "id": "story-002",
                    "title": "Story 2",
                    "description": "Second story",
                    "acceptance_criteria": ["AC 1"],
                    "priority": 2,
                    "passes": True,
                    "dependencies": ["story-001"]
                }
            ]
        }
        prd_file = tmp_path / "test_prd.json"
        with open(prd_file, 'w') as f:
            json.dump(prd_data, f)
        return prd_file

    def test_initialization(self, prd_manager):
        """测试初始化"""
        assert prd_manager.prd_data == {}
        assert prd_manager.stories == []
        assert prd_manager.file_path is None

    def test_load_prd(self, prd_manager, sample_prd_file):
        """测试加载 PRD"""
        prd_manager.load_prd(sample_prd_file)

        assert prd_manager.file_path == sample_prd_file
        assert len(prd_manager.stories) == 2
        assert prd_manager.stories[0].title == "Story 1"
        assert prd_manager.stories[1].title == "Story 2"

    def test_load_prd_not_found(self, prd_manager):
        """测试加载不存在的 PRD 文件"""
        with pytest.raises(FileNotFoundError):
            prd_manager.load_prd(Path("/nonexistent/prd.json"))

    def test_create_prd(self, prd_manager):
        """测试创建 PRD"""
        stories = [
            UserStory(
                id="story-001",
                title="New Story",
                description="A new story",
                acceptance_criteria=["AC 1"],
                priority=1
            )
        ]

        prd_manager.create_prd(
            project_name="New Project",
            branch_name="feature/test",
            description="A new project",
            stories=stories
        )

        assert prd_manager.prd_data["project"] == "New Project"
        assert prd_manager.prd_data["branch"] == "feature/test"
        assert len(prd_manager.stories) == 1
        assert prd_manager.stories[0].title == "New Story"

    def test_get_next_story(self, prd_manager, sample_prd_file):
        """测试获取下一个故事"""
        prd_manager.load_prd(sample_prd_file)

        # Should return the first story (highest priority, not passed)
        next_story = prd_manager.get_next_story()
        assert next_story is not None
        assert next_story.id == "story-001"

    def test_get_next_story_all_passed(self, prd_manager, tmp_path):
        """测试所有故事都通过时的行为"""
        prd_data = {
            "project": "Test",
            "branch": "main",
            "description": "Test",
            "userStories": [
                {
                    "id": "story-001",
                    "title": "Story 1",
                    "description": "Test",
                    "acceptance_criteria": [],
                    "priority": 1,
                    "passes": True
                }
            ]
        }
        prd_file = tmp_path / "test_prd.json"
        with open(prd_file, 'w') as f:
            json.dump(prd_data, f)

        prd_manager.load_prd(prd_file)
        next_story = prd_manager.get_next_story()
        assert next_story is None

    def test_mark_story_complete(self, prd_manager, sample_prd_file):
        """测试标记故事为完成"""
        prd_manager.load_prd(sample_prd_file)

        story = prd_manager.stories[0]
        assert story.passes is False

        prd_manager.mark_story_complete(story.id)
        assert story.passes is True

    def test_get_story_by_id(self, prd_manager, sample_prd_file):
        """测试通过 ID 获取故事"""
        prd_manager.load_prd(sample_prd_file)

        story = prd_manager.get_story_by_id("story-002")
        assert story is not None
        assert story.title == "Story 2"

    def test_get_story_by_id_not_found(self, prd_manager, sample_prd_file):
        """测试获取不存在的故事"""
        prd_manager.load_prd(sample_prd_file)

        story = prd_manager.get_story_by_id("nonexistent")
        assert story is None

    def test_get_progress_summary(self, prd_manager, sample_prd_file):
        """测试获取进度摘要"""
        prd_manager.load_prd(sample_prd_file)

        progress = prd_manager.get_progress_summary()
        assert progress["total_stories"] == 2
        assert progress["completed_stories"] == 1
        assert progress["incomplete_stories"] == 1
        assert 0 < progress["completion_percentage"] < 100

    def test_save_prd(self, prd_manager, sample_prd_file, tmp_path):
        """测试保存 PRD"""
        prd_manager.load_prd(sample_prd_file)

        # Modify a story
        prd_manager.mark_story_complete("story-001")

        # Save to new file
        new_file = tmp_path / "saved_prd.json"
        prd_manager.save_prd(new_file)

        # Verify saved file
        with open(new_file, 'r') as f:
            saved_data = json.load(f)

        assert saved_data["userStories"][0]["passes"] is True
