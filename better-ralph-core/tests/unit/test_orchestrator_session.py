"""Tests for orchestrator session lifecycle: start_session, get_session_summary edge cases, is_complete edge cases."""
import sys
import types
import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from pathlib import Path

# Create stub modules
agent_registry_mod = types.ModuleType("core.agent_registry")
agent_registry_mod.AgentRegistry = MagicMock
agent_registry_mod.Agent = MagicMock
sys.modules["core.agent_registry"] = agent_registry_mod

sys.modules["plugins"] = types.ModuleType("plugins")
version_control_sub = types.ModuleType("plugins.version_control")
version_control_sub.VersionControl = MagicMock
sys.modules["plugins.version_control"] = version_control_sub

from core.orchestrator import RalphOrchestrator, SessionStats


def _make_orchestrator():
    orch = RalphOrchestrator.__new__(RalphOrchestrator)
    orch.config = MagicMock()
    orch.logger = MagicMock()
    orch.monitor = MagicMock()
    orch.prd_manager = MagicMock()
    orch.memory_manager = MagicMock()
    orch.agent_registry = MagicMock()
    orch.version_control = MagicMock()
    orch.current_session_id = None
    orch.iteration_count = 0
    orch.session_stats = SessionStats(
        total_iterations=0, successful_iterations=0,
        failed_iterations=0, total_duration=0.0, average_iteration_time=0.0
    )
    return orch


class TestStartSession:
    def test_returns_session_id(self):
        orch = _make_orchestrator()
        orch.prd_manager.prd_data = {"branchName": "feature-x"}
        with patch("core.orchestrator.time") as mock_time:
            mock_time.time.return_value = 1000
            sid = orch.start_session(Path("/tmp/test_prd.json"), Path("/tmp/project"))
        assert sid == "session-1000"
        assert orch.current_session_id == sid

    def test_loads_prd(self):
        orch = _make_orchestrator()
        orch.prd_manager.prd_data = {}
        prd_path = Path("/tmp/test_prd.json")
        orch.start_session(prd_path, Path("/tmp/project"))
        orch.prd_manager.load_prd.assert_called_once_with(prd_path)

    def test_initializes_memory(self):
        orch = _make_orchestrator()
        orch.prd_manager.prd_data = {}
        project_root = Path("/tmp/project")
        orch.start_session(Path("/tmp/prd.json"), project_root)
        orch.memory_manager.initialize_session.assert_called_once_with(project_root)

    def test_ensures_branch_when_set(self):
        orch = _make_orchestrator()
        orch.prd_manager.prd_data = {"branchName": "feature-auth"}
        orch.start_session(Path("/tmp/prd.json"), Path("/tmp/project"))
        orch.version_control.ensure_branch.assert_called_once_with("feature-auth")

    def test_no_branch_when_empty(self):
        orch = _make_orchestrator()
        orch.prd_manager.prd_data = {}
        orch.start_session(Path("/tmp/prd.json"), Path("/tmp/project"))
        orch.version_control.ensure_branch.assert_not_called()


class TestGetSessionSummaryEdgeCases:
    def test_summary_with_remaining_stories(self):
        orch = _make_orchestrator()
        orch.current_session_id = "session-1"
        orch.session_stats = SessionStats(
            total_iterations=3, successful_iterations=2,
            failed_iterations=1, total_duration=6.0, average_iteration_time=2.0
        )
        s1 = MagicMock(); s1.passes = True
        s2 = MagicMock(); s2.passes = False
        s3 = MagicMock(); s3.passes = False
        orch.prd_manager.get_all_stories.return_value = [s1, s2, s3]

        result = orch.get_session_summary()
        assert result["remaining_stories"] == 2
        assert result["success_rate"] == pytest.approx(2/3)

    def test_summary_duration_calculation(self):
        orch = _make_orchestrator()
        orch.current_session_id = "session-2"
        orch.session_stats = SessionStats(
            total_iterations=5, successful_iterations=5,
            failed_iterations=0, total_duration=15.0, average_iteration_time=3.0
        )
        orch.prd_manager.get_all_stories.return_value = []

        result = orch.get_session_summary()
        assert result["average_iteration_time"] == 3.0

    def test_no_iterations_returns_status_only(self):
        orch = _make_orchestrator()
        orch.current_session_id = "session-3"
        orch.session_stats = SessionStats(
            total_iterations=0, successful_iterations=0,
            failed_iterations=0, total_duration=0.0, average_iteration_time=0.0
        )
        result = orch.get_session_summary()
        assert result == {"status": "no_iterations"}


class TestIsCompleteEdgeCases:
    def test_empty_stories(self):
        orch = _make_orchestrator()
        orch.prd_manager.get_all_stories.return_value = []
        assert orch.is_complete() is True  # vacuous truth

    def test_single_incomplete(self):
        orch = _make_orchestrator()
        s = MagicMock(); s.passes = False
        orch.prd_manager.get_all_stories.return_value = [s]
        assert orch.is_complete() is False

    def test_mixed_completion(self):
        orch = _make_orchestrator()
        stories = [MagicMock(passes=True), MagicMock(passes=False), MagicMock(passes=True)]
        orch.prd_manager.get_all_stories.return_value = stories
        assert orch.is_complete() is False
