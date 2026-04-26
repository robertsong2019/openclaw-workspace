"""
Unit tests for Memory Manager
测试内存管理器的功能
"""

import pytest
import json
import sys
from pathlib import Path
from datetime import datetime

# Direct import to avoid package-level imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import directly from the module file
import importlib.util
spec = importlib.util.spec_from_file_location(
    "memory_manager",
    Path(__file__).parent.parent.parent / "core" / "memory_manager.py"
)
memory_manager_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory_manager_module)

MemoryManager = memory_manager_module.MemoryManager
IterationContext = memory_manager_module.IterationContext
ProjectContext = memory_manager_module.ProjectContext


class TestIterationContext:
    """测试迭代上下文"""

    def test_create_iteration_context(self):
        context = IterationContext(
            story_id="story-001",
            story_title="Test Story",
            timestamp=datetime.now().isoformat()
        )
        assert context.story_id == "story-001"
        assert context.story_title == "Test Story"
        assert context.artifacts == []
        assert context.learnings == []
        assert context.patterns == []
        assert context.errors == []

    def test_iteration_context_with_artifacts(self):
        context = IterationContext(
            story_id="story-001",
            story_title="Test Story",
            timestamp=datetime.now().isoformat(),
            artifacts=["file1.py", "file2.py"],
            learnings=["Learning 1"],
            errors=["Error 1"]
        )
        assert len(context.artifacts) == 2
        assert len(context.learnings) == 1
        assert len(context.errors) == 1


class TestProjectContext:
    """测试项目上下文"""

    def test_create_project_context(self):
        context = ProjectContext(
            project_name="test-project",
            project_root=Path("/tmp/test")
        )
        assert context.project_name == "test-project"
        assert context.project_root == Path("/tmp/test")
        assert context.code_patterns == []
        assert context.common_gotchas == []

    def test_project_context_with_patterns(self):
        context = ProjectContext(
            project_name="test-project",
            project_root=Path("/tmp/test"),
            code_patterns=["pattern1", "pattern2"],
            conventions={"style": "pep8"}
        )
        assert len(context.code_patterns) == 2
        assert context.conventions["style"] == "pep8"


class TestMemoryManager:
    """测试内存管理器"""

    @pytest.fixture
    def memory_manager(self, tmp_path):
        """Create a memory manager with a temporary directory"""
        manager = MemoryManager(memory_dir=tmp_path)
        return manager

    def test_initialization(self, memory_manager):
        """测试初始化"""
        assert memory_manager.memory_dir.exists()
        assert memory_manager.project_context_file.parent == memory_manager.memory_dir
        assert memory_manager.iterations == []

    def test_initialize_session(self, memory_manager, tmp_path):
        """测试初始化会话"""
        project_root = tmp_path / "test_project"
        project_root.mkdir()

        memory_manager.initialize_session(project_root)

        assert memory_manager.project_context is not None
        assert memory_manager.project_context.project_name == "test_project"
        assert memory_manager.project_context.project_root == project_root

    def test_add_iteration_result(self, memory_manager):
        """测试添加迭代结果"""
        memory_manager.add_iteration_result(
            story_id="story-001",
            story_title="Test Story",
            artifacts=["test.py", "test2.py"],
            learnings=["Learning 1", "Learning 2"],
            patterns=["Pattern 1"],
            errors=[],
            metrics={"duration": 10.5}
        )

        assert len(memory_manager.iterations) == 1
        assert memory_manager.iterations[0].story_id == "story-001"
        assert len(memory_manager.iterations[0].artifacts) == 2
        assert len(memory_manager.iterations[0].learnings) == 2
        assert memory_manager.iterations[0].metrics["duration"] == 10.5

    def test_add_story_completion(self, memory_manager):
        """测试添加故事完成数据"""
        # First add an iteration
        memory_manager.add_iteration_result(
            story_id="story-001",
            story_title="Test Story",
            artifacts=[],
            learnings=[],
            patterns=[],
            errors=[],
            metrics={}
        )

        # Add completion data
        memory_manager.add_story_completion(
            "story-001",
            {"notes": "Story completed successfully"}
        )

        # Verify completion data was added
        assert memory_manager.iterations[0].notes == "Story completed successfully"

    def test_get_progress(self, memory_manager):
        """测试获取进度"""
        memory_manager.add_iteration_result(
            story_id="story-001",
            story_title="Story 1",
            artifacts=[],
            learnings=[],
            patterns=[],
            errors=[],
            metrics={"duration": 10}
        )

        memory_manager.add_iteration_result(
            story_id="story-002",
            story_title="Story 2",
            artifacts=[],
            learnings=[],
            patterns=[],
            errors=["Error occurred"],
            metrics={"duration": 15}
        )

        progress = memory_manager.get_progress()
        assert progress["total_iterations"] == 2
        assert progress["successful_iterations"] == 1
        assert progress["failed_iterations"] == 1

    def test_get_memory_summary(self, memory_manager, tmp_path):
        """测试获取内存摘要"""
        project_root = tmp_path / "test_project"
        project_root.mkdir()
        memory_manager.initialize_session(project_root)

        memory_manager.add_iteration_result(
            story_id="story-001",
            story_title="Test Story",
            artifacts=["file1.py"],
            learnings=["Learning"],
            patterns=["Pattern"],
            errors=[],
            metrics={}
        )

        summary = memory_manager.get_memory_summary()
        assert "project_context" in summary
        assert "iterations_summary" in summary
        assert summary["project_context"]["project_name"] == "test_project"

    def test_iteration_context_to_dict(self):
        """测试 IterationContext.to_dict 方法"""
        context = IterationContext(
            story_id="story-123",
            story_title="Test to_dict",
            timestamp="2026-04-27T00:00:00",
            artifacts=["a.py", "b.py"],
            learnings=["l1"],
            patterns=["p1"],
            errors=["e1"],
            metrics={"duration": 5.0},
            notes="some notes"
        )
        d = context.to_dict()
        assert d["story_id"] == "story-123"
        assert d["story_title"] == "Test to_dict"
        assert d["artifacts"] == ["a.py", "b.py"]
        assert d["learnings"] == ["l1"]
        assert d["patterns"] == ["p1"]
        assert d["errors"] == ["e1"]
        assert d["metrics"] == {"duration": 5.0}
        assert d["notes"] == "some notes"

    def test_save_session_summary(self, memory_manager, tmp_path):
        """测试保存会话摘要"""
        summary = {
            "total_stories": 5,
            "completed": 3,
            "failed": 1,
            "skipped": 1
        }
        memory_manager.save_session_summary(summary)

        # Find the session file
        session_files = list(tmp_path.glob("session_*.json"))
        assert len(session_files) == 1

        with open(session_files[0]) as f:
            saved = json.load(f)
        assert saved["total_stories"] == 5
        assert saved["completed"] == 3

    def test_progress_with_zero_iterations(self, memory_manager):
        """测试无迭代时的进度"""
        progress = memory_manager.get_progress()
        assert progress["total_iterations"] == 0
        assert progress["successful_iterations"] == 0
        assert progress["failed_iterations"] == 0
        assert progress["success_rate"] == 0.0
        assert progress["average_metrics"] == {}

    def test_progress_success_rate(self, memory_manager):
        """测试成功率计算"""
        for i in range(3):
            memory_manager.add_iteration_result(
                story_id=f"story-{i}",
                story_title=f"Story {i}",
                artifacts=[],
                learnings=[],
                patterns=[],
                errors=[] if i < 2 else ["error"],
                metrics={"duration": float(i + 1)}
            )
        progress = memory_manager.get_progress()
        assert progress["success_rate"] == pytest.approx(2.0 / 3.0)
        assert progress["average_metrics"]["duration"] == pytest.approx(2.0)

    def test_persistence_roundtrip(self, memory_manager, tmp_path):
        """测试数据持久化和加载"""
        memory_manager.add_iteration_result(
            story_id="story-persist",
            story_title="Persistence Test",
            artifacts=["main.py"],
            learnings=["learned"],
            patterns=["pat"],
            errors=[],
            metrics={"t": 1}
        )

        # Create a new manager loading from same dir
        manager2 = MemoryManager(memory_dir=tmp_path)
        assert len(manager2.iterations) == 1
        assert manager2.iterations[0].story_id == "story-persist"
        assert manager2.iterations[0].artifacts == ["main.py"]

    def test_add_story_completion_no_existing_iteration(self, memory_manager):
        """测试对不存在的 story 添加完成数据"""
        # Should not raise, just log warning
        memory_manager.add_story_completion("nonexistent", {"notes": "test"})
        assert len(memory_manager.iterations) == 0

    def test_progress_unique_artifacts_and_stories(self, memory_manager):
        """测试唯一 artifacts 和 stories 统计"""
        memory_manager.add_iteration_result(
            "s1", "S1", ["a.py", "b.py"], [], [], [], {}
        )
        memory_manager.add_iteration_result(
            "s2", "S2", ["b.py", "c.py"], [], [], [], {}
        )
        memory_manager.add_iteration_result(
            "s1", "S1 again", ["d.py"], [], [], [], {}
        )
        progress = memory_manager.get_progress()
        assert progress["total_artifacts"] == 4  # a, b, c, d
        assert progress["unique_stories"] == 2  # s1, s2
