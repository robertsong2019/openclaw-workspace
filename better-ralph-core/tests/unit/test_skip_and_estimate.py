"""Tests for RalphOrchestrator.skip_story() and estimate_remaining()."""
import pytest
from unittest.mock import patch
from core.orchestrator import RalphOrchestrator
from core.prd_manager import UserStory


def _story(sid, passes=False, priority=1):
    return UserStory(
        id=sid, title=f"Story {sid}", description="d",
        acceptance_criteria=["ac1"], priority=priority, passes=passes,
    )


class TestSkipStory:
    def test_skip_pending_story(self):
        orch = RalphOrchestrator()
        orch.prd_manager.stories = [_story("s1"), _story("s2")]
        result = orch.skip_story("blocked by external dependency")
        assert result is True
        # s1 should now be marked complete (passed)
        assert orch.prd_manager.get_story_by_id("s1").passes is True
        notes = orch.prd_manager.get_story_by_id("s1").notes
        assert "[SKIPPED]" in notes
        assert "blocked" in notes

    def test_skip_without_reason(self):
        orch = RalphOrchestrator()
        orch.prd_manager.stories = [_story("s1")]
        result = orch.skip_story()
        assert result is True
        assert orch.prd_manager.get_story_by_id("s1").notes == "[SKIPPED]"

    def test_skip_no_stories(self):
        orch = RalphOrchestrator()
        orch.prd_manager.stories = []
        result = orch.skip_story("nothing to skip")
        assert result is False

    def test_skip_all_complete(self):
        orch = RalphOrchestrator()
        orch.prd_manager.stories = [_story("s1", passes=True)]
        result = orch.skip_story()
        assert result is False


class TestEstimateRemaining:
    def test_no_stories(self):
        orch = RalphOrchestrator()
        est = orch.estimate_remaining()
        assert est["remaining_stories"] == 0
        assert est["completed_stories"] == 0
        assert est["estimated_iterations"] == 0.0

    def test_all_remaining(self):
        orch = RalphOrchestrator()
        orch.prd_manager.stories = [_story("s1"), _story("s2"), _story("s3")]
        est = orch.estimate_remaining()
        assert est["remaining_stories"] == 3
        assert est["completed_stories"] == 0

    def test_partial_completion(self):
        orch = RalphOrchestrator()
        orch.prd_manager.stories = [
            _story("s1", passes=True),
            _story("s2", passes=True),
            _story("s3"),
        ]
        est = orch.estimate_remaining()
        assert est["remaining_stories"] == 1
        assert est["completed_stories"] == 2

    def test_all_complete(self):
        orch = RalphOrchestrator()
        orch.prd_manager.stories = [_story("s1", passes=True)]
        est = orch.estimate_remaining()
        assert est["remaining_stories"] == 0
        assert est["estimated_iterations"] == 0.0
