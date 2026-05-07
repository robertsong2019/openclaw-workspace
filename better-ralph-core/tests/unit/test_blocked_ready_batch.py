"""Tests for PRDManager get_blocked_stories, get_ready_stories, batch_update_priority."""
import pytest

from core.prd_manager import PRDManager, UserStory


def _story(sid, passes=False, deps=None, priority=1):
    return UserStory(
        id=sid, title=sid, description="d",
        acceptance_criteria=["ac"], priority=priority,
        passes=passes, dependencies=deps or [],
    )


class TestGetBlockedStories:
    def test_no_deps_no_block(self):
        m = PRDManager()
        m.stories = [_story("a"), _story("b")]
        assert m.get_blocked_stories() == []

    def test_blocked_by_incomplete(self):
        m = PRDManager()
        m.stories = [_story("a", passes=False), _story("b", deps=["a"])]
        blocked = m.get_blocked_stories()
        assert len(blocked) == 1
        assert blocked[0].id == "b"

    def test_unblocked_when_dep_complete(self):
        m = PRDManager()
        m.stories = [_story("a", passes=True), _story("b", deps=["a"])]
        assert m.get_blocked_stories() == []

    def test_chain_blocking(self):
        m = PRDManager()
        m.stories = [_story("a"), _story("b", deps=["a"]), _story("c", deps=["b"])]
        blocked = m.get_blocked_stories()
        ids = {s.id for s in blocked}
        assert ids == {"b", "c"}

    def test_completed_stories_never_blocked(self):
        m = PRDManager()
        m.stories = [_story("a", passes=False), _story("b", passes=True, deps=["a"])]
        assert m.get_blocked_stories() == []


class TestGetReadyStories:
    def test_all_ready(self):
        m = PRDManager()
        m.stories = [_story("c", priority=3), _story("a", priority=1), _story("b", priority=2)]
        ready = m.get_ready_stories()
        assert [s.id for s in ready] == ["a", "b", "c"]

    def test_only_ready_returned(self):
        m = PRDManager()
        m.stories = [_story("a", passes=False), _story("b", deps=["a"])]
        ready = m.get_ready_stories()
        assert len(ready) == 1
        assert ready[0].id == "a"

    def test_completed_excluded(self):
        m = PRDManager()
        m.stories = [_story("a", passes=True)]
        assert m.get_ready_stories() == []

    def test_empty(self):
        m = PRDManager()
        assert m.get_ready_stories() == []


class TestBatchUpdatePriority:
    def test_batch_update(self):
        m = PRDManager()
        m.stories = [_story("a"), _story("b"), _story("c")]
        results = m.batch_update_priority({"a": 5, "b": 1, "c": 3})
        assert results == {"a": True, "b": True, "c": True}
        assert m.get_story_by_id("a").priority == 5

    def test_missing_story(self):
        m = PRDManager()
        m.stories = [_story("a")]
        results = m.batch_update_priority({"a": 2, "z": 1})
        assert results == {"a": True, "z": False}

    def test_empty_batch(self):
        m = PRDManager()
        assert m.batch_update_priority({}) == {}
