"""
Integration tests for full session lifecycle:
initialize_session → get_iteration_context → add_iteration_result → context updates.

Tests the end-to-end flow that agents actually use, not individual methods in isolation.
"""

import json
import pytest
from pathlib import Path
from core.memory_manager import MemoryManager


@pytest.fixture
def mm(tmp_path):
    """MemoryManager with isolated memory_dir and a project with real files."""
    memory_dir = tmp_path / "memory"
    project_root = tmp_path / "my_project"
    project_root.mkdir()
    return memory_dir, project_root, MemoryManager(memory_dir=memory_dir)


def _make_story(story_id="s1", title="Test Story", description="desc", criteria=None):
    """Minimal story-like object for get_iteration_context."""
    class Story:
        pass
    s = Story()
    s.id = story_id
    s.title = title
    s.description = description
    s.acceptance_criteria = criteria or ["ac1"]
    return s


class TestFullSessionLifecycle:
    """Test the complete agent session flow from init to context retrieval."""

    def test_initialize_session_populates_project_context(self, mm):
        """initialize_session should detect project name and scan patterns."""
        memory_dir, project_root, manager = mm

        # Create a realistic project structure
        (project_root / "package.json").write_text('{"name": "my-app"}')
        (project_root / "src").mkdir()
        (project_root / "src" / "index.ts").write_text("")
        (project_root / "src" / "utils.ts").write_text("")
        (project_root / "tests").mkdir()
        (project_root / "tests" / "test.ts").write_text("")
        (project_root / "Makefile").write_text("build:\n\techo ok\n")

        manager.initialize_session(project_root)

        # Verify project context
        assert manager.project_context is not None
        # _detect_project_name strips extensions from config filename
        assert manager.project_context.project_name == "package"
        assert manager.project_context.project_root == project_root
        assert ".ts" in manager.project_context.file_types
        assert manager.project_context.file_types[".ts"] >= 3

        # Verify conventions detected
        assert "src" in manager.project_context.conventions
        assert "tests" in manager.project_context.conventions
        assert "Makefile" in manager.project_context.conventions

        # Verify persistence
        ctx_file = memory_dir / "project_context.json"
        assert ctx_file.exists()
        saved = json.loads(ctx_file.read_text())
        assert saved["project_name"] == "package"

    def test_iteration_context_reflects_session_state(self, mm):
        """get_iteration_context should include project + memory + pattern context."""
        _, project_root, manager = mm
        (project_root / "pyproject.toml").write_text("[project]\nname='demo'\n")
        (project_root / "hello.py").write_text("print('hi')")

        manager.initialize_session(project_root)
        story = _make_story()
        ctx = manager.get_iteration_context(story)

        # Story context
        assert ctx["story"]["id"] == "s1"
        assert ctx["story"]["title"] == "Test Story"

        # Project context propagated
        assert ctx["project"]["project_name"] == "pyproject"
        assert ".py" in ctx["project"]["file_types"]

        # Memory context (empty initially)
        assert ctx["memory"]["total_iterations"] == 0
        assert ctx["memory"]["recent_iterations"] == 0

        # Patterns context (empty initially)
        assert ctx["patterns"]["code_patterns"] == []

    def test_add_iteration_updates_memory_context(self, mm):
        """After add_iteration_result, memory context should reflect new data."""
        _, project_root, manager = mm
        (project_root / "setup.py").write_text("pass")

        manager.initialize_session(project_root)

        # Add iteration
        manager.add_iteration_result(
            story_id="s1",
            story_title="Feature A",
            artifacts=["feature_a.py", "test_a.py"],
            learnings=["Use dataclasses for DTOs", "Prefer pathlib over os.path"],
            patterns=["DTO pattern"],
            errors=[],
            metrics={"duration": 12.3}
        )

        # Add second iteration
        manager.add_iteration_result(
            story_id="s2",
            story_title="Feature B",
            artifacts=["feature_b.py"],
            learnings=["Always add type hints"],
            patterns=["Service layer pattern"],
            errors=["ImportError on missing dep"],
            metrics={"duration": 8.1}
        )

        # Check memory context via get_iteration_context
        story = _make_story(story_id="s3")
        ctx = manager.get_iteration_context(story)

        assert ctx["memory"]["total_iterations"] == 2
        assert ctx["memory"]["recent_iterations"] == 2

        # Learnings should include both iterations
        learnings = ctx["memory"]["common_learnings"]
        assert any("dataclasses" in l for l in learnings)
        assert any("type hints" in l for l in learnings)

        # Recent artifacts
        artifacts = ctx["memory"]["recent_artifacts"]
        assert "feature_a.py" in artifacts
        assert "feature_b.py" in artifacts

    def test_patterns_accumulate_across_iterations(self, mm):
        """Patterns should accumulate and be available in subsequent contexts."""
        _, project_root, manager = mm
        (project_root / "Cargo.toml").write_text("[package]\nname=\"rust-app\"\n")

        manager.initialize_session(project_root)

        manager.add_iteration_result(
            story_id="s1", story_title="A",
            artifacts=[], learnings=["learning-A"],
            patterns=["pattern-A"], errors=[], metrics={}
        )

        manager.add_iteration_result(
            story_id="s2", story_title="B",
            artifacts=[], learnings=["learning-B"],
            patterns=["pattern-B"], errors=[], metrics={}
        )

        ctx = manager.get_iteration_context(_make_story())
        assert "pattern-A" in ctx["patterns"]["code_patterns"]
        assert "pattern-B" in ctx["patterns"]["code_patterns"]
        assert "learning-A" in ctx["patterns"]["common_patterns"]
        assert "learning-B" in ctx["patterns"]["common_patterns"]

    def test_session_persistence_across_manager_instances(self, mm):
        """Data should persist when creating a new MemoryManager for same dir."""
        memory_dir, project_root, manager = mm
        (project_root / "go.mod").write_text("module example.com/app\n")

        manager.initialize_session(project_root)
        manager.add_iteration_result(
            story_id="s1", story_title="Persist Test",
            artifacts=["main.go"],
            learnings=["Go modules are simple"],
            patterns=["Go project layout"],
            errors=[],
            metrics={"duration": 5.0}
        )

        # Create new manager pointing to same memory dir — loads persisted data
        manager2 = MemoryManager(memory_dir=memory_dir)

        # Iterations should be loaded
        assert len(manager2.iterations) == 1
        assert manager2.iterations[0].story_id == "s1"
        assert manager2.iterations[0].artifacts == ["main.go"]

    def test_iteration_context_limits_learnings(self, mm):
        """get_iteration_context should limit common_learnings to 10."""
        _, project_root, manager = mm
        (project_root / "package.json").write_text("{}")
        manager.initialize_session(project_root)

        # Add 12 iterations, each with a unique learning
        for i in range(12):
            manager.add_iteration_result(
                story_id=f"s{i}", story_title=f"T{i}",
                artifacts=[],
                learnings=[f"learning-{i:02d}"],
                patterns=[], errors=[], metrics={}
            )

        ctx = manager.get_iteration_context(_make_story())
        assert ctx["memory"]["total_iterations"] == 12
        assert ctx["memory"]["recent_iterations"] == 5  # last 5
        assert len(ctx["memory"]["common_learnings"]) <= 10  # capped at 10
