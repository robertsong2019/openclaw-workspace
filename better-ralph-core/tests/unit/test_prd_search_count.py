"""Tests for PRDManager.story_count_by_status and search_stories."""
import pytest
from pathlib import Path
from core.prd_manager import PRDManager, UserStory


@pytest.fixture
def pm():
    m = PRDManager()
    m.create_prd("test", "main", "desc", [
        UserStory(id="s1", title="Login page", description="Build login UI", priority=1, acceptance_criteria=["ac1"], passes=True),
        UserStory(id="s2", title="Auth API", description="Build auth endpoints", priority=2, acceptance_criteria=["ac2"]),
        UserStory(id="s3", title="Dashboard", description="Build dashboard page", priority=3, acceptance_criteria=["ac3"]),
        UserStory(id="s4", title="User profile", description="User profile page", priority=4, acceptance_criteria=["ac4"], passes=True),
    ])
    return m


def test_story_count_by_status(pm):
    counts = pm.story_count_by_status()
    assert counts == {"completed": 2, "pending": 2}


def test_story_count_empty():
    m = PRDManager()
    m.create_prd("empty", "main", "desc", [])
    assert m.story_count_by_status() == {}


def test_search_stories_title(pm):
    results = pm.search_stories("login")
    assert len(results) == 1
    assert results[0].id == "s1"


def test_search_stories_description(pm):
    results = pm.search_stories("endpoints")
    assert len(results) == 1
    assert results[0].id == "s2"


def test_search_stories_multi(pm):
    results = pm.search_stories("page")
    assert len(results) == 3  # login page, dashboard page, user profile page


def test_search_stories_case_insensitive(pm):
    results = pm.search_stories("LOGIN")
    assert len(results) == 1


def test_search_stories_no_match(pm):
    assert pm.search_stories("nonexistent") == []
