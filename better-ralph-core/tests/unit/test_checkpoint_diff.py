"""Tests for RalphOrchestrator.checkpoint_diff()."""

import pytest
from core.orchestrator import RalphOrchestrator


def _cp(iterations=0, duration=0.0, stories=None, commits=None,
         successful=0, failed=0, session_id="s1"):
    return {
        "session_id": session_id,
        "iteration_count": iterations,
        "total_iterations": iterations,
        "total_duration": duration,
        "stories_completed": stories or [],
        "commits_made": commits or [],
        "successful_iterations": successful,
        "failed_iterations": failed,
    }


def test_diff_identical_checkpoints():
    cp = _cp(iterations=5, duration=10.0, stories=["a"], commits=["c1"])
    diff = RalphOrchestrator.checkpoint_diff(cp, cp)
    assert diff["stories_added"] == []
    assert diff["stories_removed"] == []
    assert diff["commits_added"] == []
    assert diff["numeric_changes"] == {}
    assert diff["elapsed_iterations"] == 0
    assert diff["elapsed_duration"] == 0.0


def test_diff_added_stories():
    a = _cp(stories=["s1", "s2"])
    b = _cp(stories=["s1", "s2", "s3", "s4"])
    diff = RalphOrchestrator.checkpoint_diff(a, b)
    assert diff["stories_added"] == ["s3", "s4"]
    assert diff["stories_removed"] == []


def test_diff_removed_stories():
    a = _cp(stories=["s1", "s2", "s3"])
    b = _cp(stories=["s1"])
    diff = RalphOrchestrator.checkpoint_diff(a, b)
    assert diff["stories_added"] == []
    assert diff["stories_removed"] == ["s2", "s3"]


def test_diff_added_commits():
    a = _cp(commits=["abc"])
    b = _cp(commits=["abc", "def", "ghi"])
    diff = RalphOrchestrator.checkpoint_diff(a, b)
    assert diff["commits_added"] == ["def", "ghi"]
    assert diff["commits_removed"] == []


def test_diff_numeric_changes():
    a = _cp(iterations=5, duration=10.0, successful=3, failed=2)
    b = _cp(iterations=10, duration=25.5, successful=8, failed=2)
    diff = RalphOrchestrator.checkpoint_diff(a, b)
    assert diff["numeric_changes"]["iteration_count"] == {"from": 5, "to": 10}
    assert diff["numeric_changes"]["total_duration"] == {"from": 10.0, "to": 25.5}
    assert diff["numeric_changes"]["successful_iterations"] == {"from": 3, "to": 8}
    assert "failed_iterations" not in diff["numeric_changes"]


def test_diff_elapsed():
    a = _cp(iterations=5, duration=10.0)
    b = _cp(iterations=12, duration=28.3)
    diff = RalphOrchestrator.checkpoint_diff(a, b)
    assert diff["elapsed_iterations"] == 7
    assert diff["elapsed_duration"] == 18.3


def test_diff_empty_checkpoints():
    diff = RalphOrchestrator.checkpoint_diff({}, {})
    assert diff["stories_added"] == []
    assert diff["numeric_changes"] == {}
    assert diff["elapsed_iterations"] == 0
