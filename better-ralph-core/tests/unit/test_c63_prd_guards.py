"""C63 RED-first: PRDManager silent-corruption guards.

Family: silent destruction / silent no-op.
1. duplicate_story() with an already-existing new_id silently appended a second
   story with the same ID — every ID-keyed lookup then silently hits the first.
2. split_large_story(max_criteria < 1) removed the original story, produced zero
   replacements (negative chunk step → empty chunks) → silent data loss.
3. merge_prd(conflict_strategy=<typo>) silently fell through to 'skip'.
"""
import pytest

from core.prd_manager import PRDManager, UserStory


def _story(sid, title="t", priority=1):
    return UserStory(id=sid, title=title, description="d",
                     acceptance_criteria=["ac1", "ac2", "ac3", "ac4"], priority=priority)


def _make_manager(*stories):
    m = PRDManager()
    m.stories = list(stories)
    return m


class TestDuplicateStoryCollision:
    def test_duplicate_with_existing_id_raises(self):
        m = _make_manager(_story("a"), _story("b"))
        with pytest.raises(ValueError):
            m.duplicate_story("a", "b")

    def test_duplicate_onto_source_id_raises(self):
        m = _make_manager(_story("a"))
        with pytest.raises(ValueError):
            m.duplicate_story("a", "a")

    def test_state_unchanged_after_rejected_duplicate(self):
        m = _make_manager(_story("a"), _story("b"))
        with pytest.raises(ValueError):
            m.duplicate_story("a", "b")
        assert [s.id for s in m.stories] == ["a", "b"]

    def test_valid_duplicate_still_works(self):
        m = _make_manager(_story("a"))
        dup = m.duplicate_story("a", "a-copy")
        assert dup is not None and dup.id == "a-copy"
        assert [s.id for s in m.stories] == ["a", "a-copy"]


class TestSplitLargeStoryGuard:
    def test_max_criteria_zero_raises_and_keeps_story(self):
        m = _make_manager(_story("big"))
        with pytest.raises(ValueError):
            m.split_large_story("big", max_criteria=0)
        assert m.get_story_by_id("big") is not None, "story silently destroyed!"

    def test_max_criteria_negative_raises_and_keeps_story(self):
        m = _make_manager(_story("big"))
        with pytest.raises(ValueError):
            m.split_large_story("big", max_criteria=-1)
        assert m.get_story_by_id("big") is not None

    def test_valid_split_still_works(self):
        m = _make_manager(_story("big"))
        parts = m.split_large_story("big", max_criteria=2)
        assert m.get_story_by_id("big") is None
        assert len(parts) == 2


class TestMergeStrategyValidation:
    def test_invalid_strategy_raises(self):
        m1 = _make_manager(_story("a"))
        m2 = _make_manager(_story("b"))
        with pytest.raises(ValueError):
            m1.merge_prd(m2, conflict_strategy="replce")  # typo

    def test_invalid_strategy_mutates_nothing(self):
        m1 = _make_manager(_story("a"))
        m2 = _make_manager(_story("b"))
        with pytest.raises(ValueError):
            m1.merge_prd(m2, conflict_strategy="")
        assert [s.id for s in m1.stories] == ["a"]

    def test_valid_strategies_still_work(self):
        m1 = _make_manager(_story("a"))
        m2 = _make_manager(_story("b"))
        assert m1.merge_prd(m2)["added"] == 1
