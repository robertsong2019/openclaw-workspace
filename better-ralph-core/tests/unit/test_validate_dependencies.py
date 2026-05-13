"""Tests for validate_dependencies() — circular, missing, and self-dep detection."""
import pytest
from core.orchestrator import RalphOrchestrator
from core.prd_manager import PRDManager, UserStory


def _make_orchestrator_with_stories(stories):
    """Helper: create orchestrator with given stories and an active session."""
    orch = RalphOrchestrator()
    prd = PRDManager()
    for s in stories:
        prd.add_story(s)
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as td:
        prd_path = Path(td) / "prd.json"
        prd.save_prd(prd_path)
        orch.start_session(prd_path, Path(td))
        # Re-inject stories since start_session reloads from file
        orch.prd_manager.stories = stories
    return orch


class TestValidateDependencies:
    def test_valid_no_deps(self):
        orch = _make_orchestrator_with_stories([
            UserStory(id="S1", title="A", description="", acceptance_criteria=[], priority=1),
            UserStory(id="S2", title="B", description="", acceptance_criteria=[], priority=2),
        ])
        result = orch.validate_dependencies()
        assert result["valid"] is True
        assert result["circular_deps"] == []
        assert result["missing_deps"] == []
        assert result["self_deps"] == []
        assert result["total_stories_checked"] == 2

    def test_valid_with_deps(self):
        orch = _make_orchestrator_with_stories([
            UserStory(id="S1", title="A", description="", acceptance_criteria=[], priority=1, dependencies=[]),
            UserStory(id="S2", title="B", description="", acceptance_criteria=[], priority=2, dependencies=["S1"]),
        ])
        result = orch.validate_dependencies()
        assert result["valid"] is True

    def test_missing_dependency(self):
        orch = _make_orchestrator_with_stories([
            UserStory(id="S1", title="A", description="", acceptance_criteria=[], priority=1, dependencies=["S_MISSING"]),
        ])
        result = orch.validate_dependencies()
        assert result["valid"] is False
        assert len(result["missing_deps"]) == 1
        assert result["missing_deps"][0]["story_id"] == "S1"
        assert result["missing_deps"][0]["dependency"] == "S_MISSING"

    def test_self_dependency(self):
        orch = _make_orchestrator_with_stories([
            UserStory(id="S1", title="A", description="", acceptance_criteria=[], priority=1, dependencies=["S1"]),
        ])
        result = orch.validate_dependencies()
        assert result["valid"] is False
        assert len(result["self_deps"]) == 1
        assert result["self_deps"][0]["story_id"] == "S1"

    def test_circular_dependency(self):
        orch = _make_orchestrator_with_stories([
            UserStory(id="S1", title="A", description="", acceptance_criteria=[], priority=1, dependencies=["S2"]),
            UserStory(id="S2", title="B", description="", acceptance_criteria=[], priority=2, dependencies=["S1"]),
        ])
        result = orch.validate_dependencies()
        assert result["valid"] is False
        assert len(result["circular_deps"]) >= 1

    def test_three_node_cycle(self):
        orch = _make_orchestrator_with_stories([
            UserStory(id="S1", title="A", description="", acceptance_criteria=[], priority=1, dependencies=["S3"]),
            UserStory(id="S2", title="B", description="", acceptance_criteria=[], priority=2, dependencies=["S1"]),
            UserStory(id="S3", title="C", description="", acceptance_criteria=[], priority=3, dependencies=["S2"]),
        ])
        result = orch.validate_dependencies()
        assert result["valid"] is False
        assert len(result["circular_deps"]) >= 1

    def test_mixed_issues(self):
        orch = _make_orchestrator_with_stories([
            UserStory(id="S1", title="A", description="", acceptance_criteria=[], priority=1, dependencies=["S_GONE"]),
            UserStory(id="S2", title="B", description="", acceptance_criteria=[], priority=2, dependencies=["S2"]),
        ])
        result = orch.validate_dependencies()
        assert result["valid"] is False
        assert len(result["missing_deps"]) == 1
        assert len(result["self_deps"]) == 1
