"""Tests for MemoryManager clear_iterations, get_unique_story_ids, get_error_rate."""
import pytest
import tempfile
from pathlib import Path

from core.memory_manager import MemoryManager, IterationContext


def _make_mgr():
    return MemoryManager(memory_dir=Path(tempfile.mkdtemp()))


def _iter(sid, title="t", errors=None):
    return IterationContext(
        story_id=sid, story_title=title, timestamp="2026-01-01T00:00:00",
        errors=errors or [],
    )


class TestClearIterations:
    def test_clears_and_returns_count(self):
        m = _make_mgr()
        m.iterations = [_iter("a"), _iter("b"), _iter("c")]
        count = m.clear_iterations()
        assert count == 3
        assert m.iterations == []

    def test_clear_empty(self):
        m = _make_mgr()
        assert m.clear_iterations() == 0


class TestGetUniqueStoryIds:
    def test_empty(self):
        m = _make_mgr()
        assert m.get_unique_story_ids() == []

    def test_dedup_and_sort(self):
        m = _make_mgr()
        m.iterations = [_iter("c"), _iter("a"), _iter("b"), _iter("a")]
        assert m.get_unique_story_ids() == ["a", "b", "c"]


class TestGetErrorRate:
    def test_empty(self):
        m = _make_mgr()
        assert m.get_error_rate() == 0.0

    def test_no_errors(self):
        m = _make_mgr()
        m.iterations = [_iter("a"), _iter("b")]
        assert m.get_error_rate() == 0.0

    def test_all_errors(self):
        m = _make_mgr()
        m.iterations = [_iter("a", errors=["e1"]), _iter("b", errors=["e2"])]
        assert m.get_error_rate() == 1.0

    def test_mixed(self):
        m = _make_mgr()
        m.iterations = [_iter("a", errors=["e1"]), _iter("b"), _iter("c"), _iter("d", errors=["e2"])]
        assert m.get_error_rate() == 0.5
