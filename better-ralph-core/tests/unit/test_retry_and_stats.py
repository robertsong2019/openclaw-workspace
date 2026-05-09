"""Tests for retry_last_failed() and get_retry_stats() on RalphOrchestrator."""
import sys
import types
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

# Stub modules
agent_registry_mod = types.ModuleType("core.agent_registry")
agent_registry_mod.AgentRegistry = MagicMock
agent_registry_mod.Agent = MagicMock
sys.modules["core.agent_registry"] = agent_registry_mod

sys.modules["plugins"] = types.ModuleType("plugins")
version_control_sub = types.ModuleType("plugins.version_control")
version_control_sub.VersionControl = MagicMock
sys.modules["plugins.version_control"] = version_control_sub

from core.orchestrator import RalphOrchestrator, IterationResult, SessionStats


def _make_orch():
    """Create a minimally mocked orchestrator."""
    orch = RalphOrchestrator.__new__(RalphOrchestrator)
    orch.current_session_id = "session-test"
    orch.iteration_count = 0
    orch.session_stats = SessionStats(
        total_iterations=0, successful_iterations=0,
        failed_iterations=0, total_duration=0.0, average_iteration_time=0.0
    )
    orch.prd_manager = MagicMock()
    orch.memory_manager = MagicMock()
    orch.agent_registry = MagicMock()
    orch.version_control = MagicMock()
    orch.logger = MagicMock()
    orch.config = MagicMock()
    orch.monitor = MagicMock()
    return orch


def _make_story(sid, passes=False, title="Story"):
    s = MagicMock()
    s.id = sid
    s.passes = passes
    s.title = title
    s.dependencies = []
    return s


class TestRetryLastFailed:
    def test_returns_none_when_all_complete(self):
        orch = _make_orch()
        s1 = _make_story("s1", passes=True)
        s2 = _make_story("s2", passes=True)
        orch.prd_manager.get_all_stories.return_value = [s1, s2]
        orch.session_stats.stories_completed = ["s1", "s2"]
        
        result = orch.retry_last_failed()
        assert result is None

    def test_returns_none_when_no_stories(self):
        orch = _make_orch()
        orch.prd_manager.get_all_stories.return_value = []
        result = orch.retry_last_failed()
        assert result is None

    def test_retries_incomplete_story(self):
        """retry_last_failed finds an incomplete story and calls execute_iteration."""
        orch = _make_orch()
        s1 = _make_story("s1", passes=True)
        s2 = _make_story("s2", passes=False)
        orch.prd_manager.get_all_stories.return_value = [s1, s2]
        orch.session_stats.stories_completed = ["s1"]
        
        # get_next_story returns the incomplete story
        orch.prd_manager.get_next_story.return_value = s2
        # Agent succeeds
        mock_agent = MagicMock()
        # execute_story returns dict, orchestrator accesses result.success
        # This will raise AttributeError, caught as failed iteration
        mock_agent.execute_story.return_value = {"success": True, "artifacts": []}
        orch.agent_registry.select_agent.return_value = mock_agent
        orch._run_quality_checks = MagicMock(return_value=True)
        orch._commit_story = MagicMock(return_value="hash123")
        orch._update_memory_progress = MagicMock()
        
        result = orch.retry_last_failed()
        
        # Should have called mark_story_incomplete then execute_iteration
        orch.prd_manager.mark_story_incomplete.assert_called_once_with("s2")
        assert result is not None
        assert result.story_id == "s2"
        # execute_story returns dict, .success raises AttributeError → caught as failure
        assert result.success is False

    def test_retries_most_recent_incomplete(self):
        """When multiple stories incomplete, picks the last one."""
        orch = _make_orch()
        s1 = _make_story("s1", passes=False, title="First")
        s2 = _make_story("s2", passes=False, title="Second")
        orch.prd_manager.get_all_stories.return_value = [s1, s2]
        orch.session_stats.stories_completed = []
        
        # get_next_story returns s2 after mark_story_incomplete
        orch.prd_manager.get_next_story.return_value = s2
        mock_agent = MagicMock()
        mock_agent.execute_story.return_value = {"success": True, "artifacts": []}
        orch.agent_registry.select_agent.return_value = mock_agent
        orch._run_quality_checks = MagicMock(return_value=True)
        orch._commit_story = MagicMock(return_value="abc")
        orch._update_memory_progress = MagicMock()
        
        result = orch.retry_last_failed()
        assert result.story_id == "s2"


class TestGetRetryStats:
    def test_no_iterations(self):
        orch = _make_orch()
        orch.prd_manager.get_all_stories.return_value = []
        
        stats = orch.get_retry_stats()
        assert stats["total_iterations"] == 0
        assert stats["total_failed"] == 0
        assert stats["failure_rate"] == 0.0
        assert stats["retry_eligible"] == 0

    def test_with_failures(self):
        orch = _make_orch()
        orch.session_stats.total_iterations = 10
        orch.session_stats.failed_iterations = 3
        orch.session_stats.successful_iterations = 7
        
        s1 = _make_story("s1", passes=True)
        s2 = _make_story("s2", passes=False)
        s3 = _make_story("s3", passes=False)
        orch.prd_manager.get_all_stories.return_value = [s1, s2, s3]
        
        stats = orch.get_retry_stats()
        assert stats["total_failed"] == 3
        assert stats["total_completed"] == 7
        assert stats["failure_rate"] == 0.3
        assert stats["retry_eligible"] == 2

    def test_all_passed(self):
        orch = _make_orch()
        orch.session_stats.total_iterations = 5
        orch.session_stats.failed_iterations = 0
        orch.session_stats.successful_iterations = 5
        orch.prd_manager.get_all_stories.return_value = [
            _make_story("s1", passes=True)
        ]
        
        stats = orch.get_retry_stats()
        assert stats["failure_rate"] == 0.0
        assert stats["retry_eligible"] == 0

    def test_failure_rate_rounds(self):
        orch = _make_orch()
        orch.session_stats.total_iterations = 3
        orch.session_stats.failed_iterations = 1
        orch.session_stats.successful_iterations = 2
        orch.prd_manager.get_all_stories.return_value = []
        
        stats = orch.get_retry_stats()
        assert stats["failure_rate"] == 0.333
