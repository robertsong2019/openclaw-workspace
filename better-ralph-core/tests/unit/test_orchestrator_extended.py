"""Extended tests for RalphOrchestrator - covering _run_quality_checks, _commit_story, _update_memory_progress."""
import sys
import types
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

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
    """Create a minimally initialized orchestrator for testing internal methods."""
    orch = RalphOrchestrator.__new__(RalphOrchestrator)
    orch.config = MagicMock()
    orch.logger = MagicMock()
    orch.version_control = MagicMock()
    orch.memory_manager = MagicMock()
    orch.session_stats = SessionStats(
        total_iterations=0, successful_iterations=0,
        failed_iterations=0, total_duration=0.0, average_iteration_time=0.0
    )
    return orch


class TestRunQualityChecks:
    def test_no_commands_passes(self):
        orch = _make_orchestrator()
        orch.config.get_quality_commands.return_value = []
        assert orch._run_quality_checks() is True

    def test_all_commands_succeed(self):
        orch = _make_orchestrator()
        orch.config.get_quality_commands.return_value = ["lint", "test"]
        orch.version_control.run_command.side_effect = [
            {"exit_code": 0}, {"exit_code": 0}
        ]
        assert orch._run_quality_checks() is True

    def test_command_failure_returns_false(self):
        orch = _make_orchestrator()
        orch.config.get_quality_commands.return_value = ["lint"]
        orch.version_control.run_command.return_value = {"exit_code": 1}
        assert orch._run_quality_checks() is False

    def test_exception_returns_false(self):
        orch = _make_orchestrator()
        orch.config.get_quality_commands.side_effect = RuntimeError("boom")
        assert orch._run_quality_checks() is False

    def test_second_command_failure_stops_early(self):
        orch = _make_orchestrator()
        orch.config.get_quality_commands.return_value = ["lint", "test", "typecheck"]
        orch.version_control.run_command.side_effect = [
            {"exit_code": 0}, {"exit_code": 1}
        ]
        assert orch._run_quality_checks() is False
        # Should not call third command
        assert orch.version_control.run_command.call_count == 2


class TestCommitStory:
    def test_successful_commit(self):
        orch = _make_orchestrator()
        story = MagicMock()
        story.id = "S01"
        story.title = "Login feature"
        orch.version_control.commit.return_value = "abc123"

        result = orch._commit_story(story)
        assert result == "abc123"
        assert "abc123" in orch.session_stats.commits_made

    def test_commit_returns_none_on_no_hash(self):
        orch = _make_orchestrator()
        story = MagicMock()
        story.id = "S01"
        story.title = "Test"
        orch.version_control.commit.return_value = None

        result = orch._commit_story(story)
        assert result is None

    def test_commit_exception_returns_none(self):
        orch = _make_orchestrator()
        story = MagicMock()
        story.id = "S01"
        story.title = "Test"
        orch.version_control.stage_all.side_effect = Exception("git error")

        result = orch._commit_story(story)
        assert result is None

    def test_commit_message_format(self):
        orch = _make_orchestrator()
        story = MagicMock()
        story.id = "S05"
        story.title = "Add auth"
        orch.version_control.commit.return_value = "def456"

        orch._commit_story(story)
        orch.version_control.commit.assert_called_once_with("feat: S05 - Add auth")


class TestUpdateMemoryProgress:
    def test_happy_path(self):
        orch = _make_orchestrator()
        story = MagicMock()
        story.id = "S01"
        story.title = "Feature"
        progress = MagicMock()
        orch.memory_manager.get_progress.return_value = progress

        orch._update_memory_progress(story, {
            "artifacts": ["main.py"],
            "learnings": ["learned X"]
        })

        progress.add_story_completion.assert_called_once()
        orch.memory_manager.save_progress.assert_called_once()

    def test_exception_does_not_raise(self):
        orch = _make_orchestrator()
        story = MagicMock()
        story.id = "S01"
        story.title = "Feature"
        orch.memory_manager.get_progress.side_effect = Exception("db error")

        # Should not raise
        orch._update_memory_progress(story, {})

    def test_result_missing_keys_uses_defaults(self):
        orch = _make_orchestrator()
        story = MagicMock()
        story.id = "S01"
        story.title = "Feature"
        progress = MagicMock()
        orch.memory_manager.get_progress.return_value = progress

        orch._update_memory_progress(story, {})
        call_kwargs = progress.add_story_completion.call_args[0][1]
        assert call_kwargs["artifacts"] == []
        assert call_kwargs["learnings"] == []
