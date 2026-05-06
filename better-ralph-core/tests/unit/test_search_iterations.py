"""Tests for MemoryManager.search_iterations()."""
import pytest
from pathlib import Path
from core.memory_manager import MemoryManager, IterationContext


@pytest.fixture
def mm(tmp_path):
    return MemoryManager(memory_dir=tmp_path)


def _iter(story_id="s1", title="Test", errors=None, learnings=None, notes=""):
    return IterationContext(
        story_id=story_id,
        story_title=title,
        timestamp="2026-05-06T19:00:00",
        errors=errors or [],
        learnings=learnings or [],
        notes=notes,
    )


class TestSearchIterations:
    def test_empty(self, mm):
        assert mm.search_iterations() == []

    def test_filter_by_story_id(self, mm):
        mm.iterations = [_iter("s1"), _iter("s2"), _iter("s1")]
        results = mm.search_iterations(story_id="s1")
        assert len(results) == 2

    def test_filter_has_errors(self, mm):
        mm.iterations = [_iter(errors=["fail"]), _iter(), _iter(errors=["err"])]
        results = mm.search_iterations(has_errors=True)
        assert len(results) == 2

    def test_filter_no_errors(self, mm):
        mm.iterations = [_iter(errors=["fail"]), _iter()]
        results = mm.search_iterations(has_errors=False)
        assert len(results) == 1

    def test_keyword_in_title(self, mm):
        mm.iterations = [_iter(title="Auth module"), _iter(title="Logging")]
        results = mm.search_iterations(query="auth")
        assert len(results) == 1

    def test_keyword_in_learnings(self, mm):
        mm.iterations = [_iter(learnings=["use caching"]), _iter(learnings=["avoid loops"])]
        results = mm.search_iterations(query="caching")
        assert len(results) == 1

    def test_keyword_in_notes(self, mm):
        mm.iterations = [_iter(notes="performance issue"), _iter(notes="clean code")]
        results = mm.search_iterations(query="performance")
        assert len(results) == 1

    def test_combined_filters(self, mm):
        mm.iterations = [
            _iter(story_id="s1", errors=["fail"], notes="auth bug"),
            _iter(story_id="s1", notes="auth works"),
            _iter(story_id="s2", errors=["err"]),
        ]
        results = mm.search_iterations(story_id="s1", has_errors=True, query="auth")
        assert len(results) == 1
        assert results[0].story_id == "s1"
