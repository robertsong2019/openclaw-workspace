"""Tests for PRDManager.validate_dependencies()."""
import pytest
from core.prd_manager import PRDManager, UserStory


@pytest.fixture
def manager():
    return PRDManager()


def _make_stories(story_defs):
    """Helper: create list of UserStory from (id, deps) tuples."""
    return [
        UserStory(
            id=sid,
            title=f"Story {sid}",
            description="desc",
            acceptance_criteria=["ac1"],
            priority=1,
            dependencies=list(deps),
        )
        for sid, deps in story_defs
    ]


class TestValidateDependencies:
    def test_valid_no_deps(self, manager):
        manager.stories = _make_stories([("s1", []), ("s2", [])])
        result = manager.validate_dependencies()
        assert result["valid"] is True
        assert result["errors"] == []

    def test_valid_with_deps(self, manager):
        manager.stories = _make_stories([("s1", []), ("s2", ["s1"])])
        result = manager.validate_dependencies()
        assert result["valid"] is True

    def test_missing_dependency(self, manager):
        manager.stories = _make_stories([("s1", ["nonexistent"])])
        result = manager.validate_dependencies()
        assert result["valid"] is False
        assert any("nonexistent" in e for e in result["errors"])

    def test_self_dependency(self, manager):
        manager.stories = _make_stories([("s1", ["s1"])])
        result = manager.validate_dependencies()
        assert result["valid"] is False
        assert any("self-dependency" in e for e in result["errors"])

    def test_circular_dependency(self, manager):
        manager.stories = _make_stories([("s1", ["s2"]), ("s2", ["s1"])])
        result = manager.validate_dependencies()
        assert result["valid"] is False
        assert any("Circular" in e for e in result["errors"])

    def test_three_node_cycle(self, manager):
        manager.stories = _make_stories([
            ("s1", ["s2"]), ("s2", ["s3"]), ("s3", ["s1"])
        ])
        result = manager.validate_dependencies()
        assert result["valid"] is False

    def test_many_deps_warning(self, manager):
        manager.stories = _make_stories([
            ("s1", []), ("s2", []), ("s3", []), ("s4", []),
            ("s5", ["s1", "s2", "s3", "s4"]),
        ])
        result = manager.validate_dependencies()
        assert result["valid"] is True
        assert len(result["warnings"]) == 1
        assert "s5" in result["warnings"][0]

    def test_empty_stories(self, manager):
        result = manager.validate_dependencies()
        assert result["valid"] is True

    def test_chain_valid(self, manager):
        manager.stories = _make_stories([
            ("s1", []), ("s2", ["s1"]), ("s3", ["s2"]), ("s4", ["s3"])
        ])
        result = manager.validate_dependencies()
        assert result["valid"] is True
        assert result["errors"] == []
