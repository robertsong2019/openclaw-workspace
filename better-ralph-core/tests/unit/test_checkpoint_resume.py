"""Tests for save_checkpoint(), load_checkpoint(), and resume_batch() on RalphOrchestrator."""

import pytest
from unittest.mock import MagicMock, patch
from core.orchestrator import RalphOrchestrator, IterationResult


def _make_orchestrator_with_session():
    """Create an orchestrator with an active session and PRD loaded."""
    orch = RalphOrchestrator.__new__(RalphOrchestrator)
    orch.config = MagicMock()
    orch.logger = MagicMock()
    orch.monitor = MagicMock()
    orch.prd_manager = MagicMock()
    orch.memory_manager = MagicMock()
    orch.agent_registry = MagicMock()
    orch.version_control = MagicMock()
    orch.current_session_id = "session-test"
    orch.iteration_count = 0
    from core.orchestrator import SessionStats
    orch.session_stats = SessionStats(
        total_iterations=0,
        successful_iterations=0,
        failed_iterations=0,
        total_duration=0.0,
    )
    return orch


def _success_result(story_id="s1"):
    return IterationResult(
        story_id=story_id, story_title=f"Story {story_id}",
        success=True, duration=0.1,
    )


def _fail_result(story_id="s1"):
    return IterationResult(
        story_id=story_id, story_title=f"Story {story_id}",
        success=False, duration=0.1, error_message="fail",
    )


class TestSaveCheckpoint:
    def test_captures_session_state(self):
        orch = _make_orchestrator_with_session()
        orch.iteration_count = 5
        orch.session_stats.successful_iterations = 4
        orch.session_stats.failed_iterations = 1
        orch.session_stats.total_iterations = 5
        orch.session_stats.stories_completed = ["s1", "s2"]
        orch.session_stats.commits_made = ["abc123"]
        orch.session_stats.total_duration = 12.5

        cp = orch.save_checkpoint()
        assert cp["session_id"] == "session-test"
        assert cp["iteration_count"] == 5
        assert cp["stories_completed"] == ["s1", "s2"]
        assert cp["commits_made"] == ["abc123"]
        assert cp["successful_iterations"] == 4
        assert cp["failed_iterations"] == 1
        assert cp["total_iterations"] == 5
        assert cp["total_duration"] == 12.5
        assert "timestamp" in cp

    def test_checkpoint_is_serializable(self):
        import json
        orch = _make_orchestrator_with_session()
        cp = orch.save_checkpoint()
        serialized = json.dumps(cp)
        assert json.loads(serialized) == cp


class TestLoadCheckpoint:
    def test_restores_state(self):
        orch = _make_orchestrator_with_session()
        cp = {
            "session_id": "session-42",
            "iteration_count": 10,
            "stories_completed": ["s1", "s2", "s3"],
            "commits_made": ["a1", "b2"],
            "successful_iterations": 8,
            "failed_iterations": 2,
            "total_iterations": 10,
            "total_duration": 50.0,
        }
        orch.load_checkpoint(cp)
        assert orch.current_session_id == "session-42"
        assert orch.iteration_count == 10
        assert orch.session_stats.stories_completed == ["s1", "s2", "s3"]
        assert orch.session_stats.commits_made == ["a1", "b2"]
        assert orch.session_stats.successful_iterations == 8

    def test_load_preserves_lists_independently(self):
        orch = _make_orchestrator_with_session()
        cp = {"session_id": "x", "stories_completed": ["a"]}
        orch.load_checkpoint(cp)
        # Mutating checkpoint shouldn't affect orchestrator
        cp["stories_completed"].append("b")
        assert orch.session_stats.stories_completed == ["a"]


class TestResumeBatch:
    def test_resumes_with_remaining_budget(self):
        orch = _make_orchestrator_with_session()
        story1 = MagicMock(id="s1", passes=False)
        story2 = MagicMock(id="s2", passes=False)
        call_count = [0]

        def mock_get_next():
            call_count[0] += 1
            if call_count[0] == 1:
                return story1
            if call_count[0] == 2:
                return story2
            return None

        orch.prd_manager.get_next_story.side_effect = mock_get_next
        orch.prd_manager.get_all_stories.return_value = [story1, story2]
        orch.is_complete = MagicMock(side_effect=[False, False, True])
        orch.agent_registry.select_agent.return_value = MagicMock(
            execute_story=MagicMock(return_value=MagicMock(success=True, get=MagicMock(return_value=[])))
        )
        orch._run_quality_checks = MagicMock(return_value=True)
        orch._commit_story = MagicMock(return_value="abc")
        orch._update_memory_progress = MagicMock()

        cp = {
            "session_id": "session-test",
            "iteration_count": 8,
            "stories_completed": [],
            "commits_made": [],
            "successful_iterations": 8,
            "failed_iterations": 0,
            "total_iterations": 8,
            "total_duration": 10.0,
        }
        results = orch.resume_batch(cp, max_iterations=10)
        # Budget was 10, 8 already done → 2 remaining, 2 stories → 2 results
        assert len(results) == 2

    def test_no_iterations_if_budget_exhausted(self):
        orch = _make_orchestrator_with_session()
        cp = {
            "session_id": "session-test",
            "iteration_count": 10,
            "stories_completed": [],
            "commits_made": [],
            "successful_iterations": 10,
            "failed_iterations": 0,
            "total_iterations": 10,
            "total_duration": 10.0,
        }
        results = orch.resume_batch(cp, max_iterations=10)
        assert results == []

    def test_raises_if_no_session_in_checkpoint(self):
        orch = _make_orchestrator_with_session()
        cp = {"session_id": None, "iteration_count": 0, "stories_completed": [],
              "commits_made": [], "successful_iterations": 0, "failed_iterations": 0,
              "total_iterations": 0, "total_duration": 0.0}
        with pytest.raises(ValueError, match="no active session"):
            orch.resume_batch(cp)
