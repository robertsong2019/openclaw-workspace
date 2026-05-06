"""Tests for RalphOrchestrator.get_status()."""
import pytest
from pathlib import Path
from unittest.mock import patch
from core.orchestrator import RalphOrchestrator
from core.prd_manager import UserStory


def _story(sid, passes=False, priority=1):
    return UserStory(
        id=sid, title=f"Story {sid}", description="d",
        acceptance_criteria=["ac1"], priority=priority, passes=passes,
    )


class TestGetStatus:
    def test_no_session(self):
        orch = RalphOrchestrator()
        status = orch.get_status()
        assert status["active"] is False
        assert status["session_id"] is None
        # empty stories => is_complete = True
        assert status["is_complete"] is True

    def test_with_session(self, tmp_path):
        orch = RalphOrchestrator()
        prd = tmp_path / "prd.json"
        prd.write_text('{"project":"test","userStories":[{"id":"s1","title":"T","description":"d","acceptance_criteria":["ac"],"priority":1,"passes":false,"notes":"","estimated_hours":null,"dependencies":[]}]}')
        with patch.object(orch, '_run_quality_checks', return_value=True), \
             patch.object(orch, '_commit_story', return_value="abc"), \
             patch.object(orch, '_update_memory_progress'):
            orch.start_session(prd, tmp_path)
        status = orch.get_status()
        assert status["active"] is True
        assert status["total_stories"] == 1
        assert status["completed_stories"] == 0
        assert status["current_story"] == "s1"
        assert status["is_complete"] is False

    def test_completed(self):
        orch = RalphOrchestrator()
        orch.prd_manager.stories = [_story("s1", passes=True)]
        status = orch.get_status()
        assert status["is_complete"] is True
        assert status["current_story"] is None

    def test_partial_progress(self):
        orch = RalphOrchestrator()
        orch.prd_manager.stories = [
            _story("s1", passes=True),
            _story("s2", passes=False, priority=2),
            _story("s3", passes=False, priority=3),
        ]
        status = orch.get_status()
        assert status["total_stories"] == 3
        assert status["completed_stories"] == 1
        assert round(status["progress_percentage"], 1) == 33.3
        assert status["current_story"] == "s2"
