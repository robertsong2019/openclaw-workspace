"""Tests for PRDManager reorder_story and duplicate_story."""
import pytest
import json
import tempfile
from pathlib import Path

from core.prd_manager import PRDManager, UserStory


def _make_manager(*stories):
    m = PRDManager()
    m.stories = list(stories)
    return m


def _story(sid, title="t", priority=1):
    return UserStory(id=sid, title=title, description="d", acceptance_criteria=["ac"], priority=priority)


class TestReorderStory:
    def test_basic_move(self):
        m = _make_manager(_story("a"), _story("b"), _story("c"))
        m.reorder_story("a", 2)
        assert [s.id for s in m.stories] == ["b", "c", "a"]

    def test_move_to_front(self):
        m = _make_manager(_story("a"), _story("b"), _story("c"))
        m.reorder_story("c", 0)
        assert [s.id for s in m.stories] == ["c", "a", "b"]

    def test_same_position(self):
        m = _make_manager(_story("a"), _story("b"))
        assert m.reorder_story("a", 0) is True
        assert [s.id for s in m.stories] == ["a", "b"]

    def test_not_found(self):
        m = _make_manager(_story("a"))
        assert m.reorder_story("z", 0) is False

    def test_clamp_negative(self):
        m = _make_manager(_story("a"), _story("b"))
        m.reorder_story("b", -5)
        assert m.stories[0].id == "b"

    def test_clamp_overflow(self):
        m = _make_manager(_story("a"), _story("b"))
        m.reorder_story("a", 100)
        assert m.stories[-1].id == "a"

    def test_single_story(self):
        m = _make_manager(_story("only"))
        assert m.reorder_story("only", 0) is True
        assert len(m.stories) == 1


class TestDuplicateStory:
    def test_basic(self):
        s = _story("a", "My Story", 3)
        s.notes = "keep"
        s.dependencies = ["dep1"]
        s.estimated_hours = 2.5
        m = _make_manager(s)
        dup = m.duplicate_story("a", "a-copy")
        assert dup is not None
        assert dup.id == "a-copy"
        assert dup.title == "My Story"
        assert dup.passes is False
        assert dup.notes == "keep"
        assert dup.dependencies == ["dep1"]
        assert len(m.stories) == 2

    def test_independent_copy(self):
        s = _story("a")
        s.acceptance_criteria = ["ac1", "ac2"]
        m = _make_manager(s)
        dup = m.duplicate_story("a", "b")
        dup.acceptance_criteria.append("ac3")
        assert len(s.acceptance_criteria) == 2

    def test_not_found(self):
        m = _make_manager(_story("a"))
        assert m.duplicate_story("z", "z2") is None

    def test_duplicate_resets_passes(self):
        s = _story("a")
        s.passes = True
        m = _make_manager(s)
        dup = m.duplicate_story("a", "b")
        assert dup.passes is False
