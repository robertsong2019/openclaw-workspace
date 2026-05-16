"""Tests for RalphOrchestrator.story_digest()."""

import pytest
from unittest.mock import MagicMock, patch
from core.orchestrator import RalphOrchestrator
from core.prd_manager import UserStory


def _make_story(sid, title, priority=1, passes=False, notes=""):
    return UserStory(
        id=sid, title=title, description=f"Desc for {sid}",
        acceptance_criteria=["AC1"], priority=priority,
        passes=passes, notes=notes,
    )


def _orch_with_stories(stories):
    """Create an orchestrator pre-loaded with given stories."""
    orch = RalphOrchestrator.__new__(RalphOrchestrator)
    orch.config = MagicMock()
    orch.logger = MagicMock()
    orch.monitor = MagicMock()
    orch.prd_manager = MagicMock()
    orch.prd_manager.get_all_stories.return_value = stories
    orch.memory_manager = MagicMock()
    orch.agent_registry = MagicMock()
    orch.version_control = MagicMock()
    orch.current_session_id = None
    orch.iteration_count = 0
    from core.orchestrator import SessionStats
    orch.session_stats = SessionStats(
        total_iterations=0, successful_iterations=0,
        failed_iterations=0, total_duration=0.0,
    )
    return orch


class TestStoryDigest:

    def test_empty_prd(self):
        orch = _orch_with_stories([])
        d = orch.story_digest()
        assert d["total"] == 0
        assert d["completed"] == 0
        assert d["pending"] == 0
        assert d["skipped"] == 0
        assert d["completion_pct"] == 0.0
        assert d["is_complete"] is True
        assert d["top_pending"] == []

    def test_all_completed(self):
        stories = [
            _make_story("s1", "Alpha", passes=True),
            _make_story("s2", "Beta", passes=True),
        ]
        orch = _orch_with_stories(stories)
        d = orch.story_digest()
        assert d["completed"] == 2
        assert d["pending"] == 0
        assert d["is_complete"] is True
        assert d["completion_pct"] == 100.0

    def test_mixed_states(self):
        stories = [
            _make_story("s1", "Done", passes=True),
            _make_story("s2", "Skip", passes=True, notes="[SKIPPED] too hard"),
            _make_story("s3", "Pending", passes=False, priority=2),
            _make_story("s4", "Urgent", passes=False, priority=1),
        ]
        orch = _orch_with_stories(stories)
        d = orch.story_digest()
        assert d["total"] == 4
        assert d["completed"] == 1
        assert d["skipped"] == 1
        assert d["pending"] == 2
        assert d["completion_pct"] == 25.0
        assert d["is_complete"] is False

    def test_top_pending_sorted_by_priority(self):
        stories = [
            _make_story(f"s{i}", f"Story {i}", passes=False, priority=i)
            for i in [5, 2, 8, 1, 3, 7]
        ]
        orch = _orch_with_stories(stories)
        d = orch.story_digest()
        ids = [p["id"] for p in d["top_pending"]]
        assert ids == ["s1", "s2", "s3", "s5", "s7"]  # top 5 by priority

    def test_top_pending_capped_at_five(self):
        stories = [
            _make_story(f"s{i}", f"S{i}", passes=False, priority=i)
            for i in range(10)
        ]
        orch = _orch_with_stories(stories)
        d = orch.story_digest()
        assert len(d["top_pending"]) == 5

    def test_session_info_absent_when_no_session(self):
        orch = _orch_with_stories([_make_story("s1", "A")])
        d = orch.story_digest()
        assert "session" not in d

    def test_session_info_present_when_active(self):
        orch = _orch_with_stories([_make_story("s1", "A")])
        orch.current_session_id = "sess-123"
        orch.session_stats.total_iterations = 5
        orch.session_stats.successful_iterations = 4
        orch.session_stats.failed_iterations = 1
        d = orch.story_digest()
        assert d["session"]["session_id"] == "sess-123"
        assert d["session"]["iterations"] == 5
        assert d["session"]["successes"] == 4
        assert d["session"]["failures"] == 1

    def test_completion_pct_rounding(self):
        stories = [_make_story("s1", "A", passes=True)] + [
            _make_story(f"s{i}", f"S{i}", passes=False) for i in range(2, 4)
        ]  # 1/3 = 33.333...%
        orch = _orch_with_stories(stories)
        d = orch.story_digest()
        assert d["completion_pct"] == 33.3
