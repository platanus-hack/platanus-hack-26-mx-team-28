"""Tests deterministas de los schemas Pydantic (corren sin API key)."""

import pytest
from pydantic import ValidationError

from schemas import ChildProfile, Story, StoryPage


def test_story_validates_good_payload():
    story = Story(
        title="La aventura de Tomás",
        age_at_creation=7.0,
        pages=[
            StoryPage(page=1, text="Había una vez...", image_prompt="a watercolor meadow"),
            StoryPage(page=2, text="Tomás vio algo...", image_prompt="a curious boy",
                      is_checkpoint=True),
        ],
    )
    assert story.pages[1].is_checkpoint is True
    assert story.pages[0].is_checkpoint is False  # default


def test_story_rejects_missing_title():
    with pytest.raises(ValidationError):
        Story(age_at_creation=7.0, pages=[])


def test_storypage_rejects_page_below_one():
    with pytest.raises(ValidationError):
        StoryPage(page=0, text="x", image_prompt="y")


def test_childprofile_age_bounds():
    ChildProfile(name="Ana", age=2.0)   # límite inferior ok
    ChildProfile(name="Ana", age=12.0)  # límite superior ok
    with pytest.raises(ValidationError):
        ChildProfile(name="Ana", age=1.0)
    with pytest.raises(ValidationError):
        ChildProfile(name="Ana", age=13.0)


def test_childprofile_defaults():
    p = ChildProfile(name="Leo", age=5.0)
    assert p.likes == [] and p.recent_events == []
    assert p.sex == "" and p.story_theme == ""
