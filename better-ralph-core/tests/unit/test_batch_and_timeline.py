"""Tests for run_batch() and get_story_timeline() on RalphOrchestrator."""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from core.orchestrator import RalphOrchestrator, IterationResult


def _make_result(story_id, success, title="Story"):
    return IterationResult(
        story_id=story_id,
        story_title=title,
        success=success,
        duration=0.1,
    )


def _orch_with_session():
    """Create an orchestrator with an active session and mocked components."""
    orch = RalphOrchestrator()
    orch.current_session_id = "session-test"
    # Mock execute_iteration so we control outcomes
    return orch


# --- run_batch tests ---

def test_run_batch_no_session_raises():
    orch = RalphOrchestrator()
    with pytest.raises(ValueError, match="No active session"):
        orch.run_batch()


def test_run_batch_completes_all():
    orch = _orch_with_session()
    results = [_make_result("s1", True), _make_result("complete", True)]
    call_count = 0
    def fake_execute():
        nonlocal call_count
        r = results[min(call_count, len(results)-1)]
        call_count += 1
        # Stop after returning "complete"
        if r.story_id == "complete":
            orch.prd_manager = MagicMock()
            orch.prd_manager.get_all_stories.return_value = []
        return r

    with patch.object(orch, 'is_complete', side_effect=[False, True]):
        orch.execute_iteration = fake_execute
        batch = orch.run_batch(max_iterations=5)
    assert len(batch) == 1
    assert batch[0].story_id == "s1"


def test_run_batch_stops_on_consecutive_failures():
    orch = _orch_with_session()
    outcomes = [_make_result("s1", False), _make_result("s2", False), _make_result("s3", False)]
    idx = 0
    def fake_execute():
        nonlocal idx
        r = outcomes[idx]
        idx += 1
        return r

    orch.execute_iteration = fake_execute
    with patch.object(orch, 'is_complete', return_value=False):
        batch = orch.run_batch(max_iterations=10, max_consecutive_failures=2)
    assert len(batch) == 2  # stopped after 2 consecutive failures


def test_run_batch_mixed_resets_failure_counter():
    orch = _orch_with_session()
    outcomes = [
        _make_result("s1", False),
        _make_result("s2", True),
        _make_result("s3", False),
        _make_result("s4", False),
    ]
    idx = 0
    def fake_execute():
        nonlocal idx
        r = outcomes[idx]
        idx += 1
        return r

    orch.execute_iteration = fake_execute
    with patch.object(orch, 'is_complete', return_value=False):
        batch = orch.run_batch(max_iterations=4, max_consecutive_failures=2)
    # s1(fail), s2(success resets), s3(fail), s4(fail) -> stops at 2 consecutive
    assert len(batch) == 4


# --- get_story_timeline tests ---

def test_timeline_no_memory_search():
    orch = _orch_with_session()
    # memory_manager without search_iterations
    orch.memory_manager = MagicMock(spec=[])
    assert orch.get_story_timeline() == []


def test_timeline_empty_iterations():
    orch = _orch_with_session()
    orch.memory_manager = MagicMock()
    orch.memory_manager.search_iterations.return_value = []
    assert orch.get_story_timeline() == []


def test_timeline_tracks_attempts():
    orch = _orch_with_session()
    orch.memory_manager = MagicMock()
    orch.memory_manager.search_iterations.return_value = [
        {"story_id": "s1", "story_title": "First", "success": False, "timestamp": "t1"},
        {"story_id": "s1", "story_title": "First", "success": True, "timestamp": "t2"},
        {"story_id": "s2", "story_title": "Second", "success": True, "timestamp": "t3"},
    ]
    timeline = orch.get_story_timeline()
    assert len(timeline) == 3
    assert timeline[0]["attempt"] == 1
    assert timeline[1]["attempt"] == 2
    assert timeline[2]["attempt"] == 1
    assert timeline[0]["success"] is False
    assert timeline[1]["success"] is True
