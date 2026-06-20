"""Tests deterministas de la garantía de checkpoints del Narrador (sin API key)."""

from narrador_runner import ensure_checkpoints
from schemas import Story, StoryPage


def _story(n_pages: int, checkpoints: set[int] = frozenset()) -> Story:
    return Story(
        title="t", age_at_creation=7.0,
        pages=[StoryPage(page=i + 1, text=f"p{i+1}", image_prompt="img",
                         is_checkpoint=(i + 1) in checkpoints) for i in range(n_pages)],
    )


def test_forces_checkpoint_when_zero():
    s = ensure_checkpoints(_story(6))
    cps = [p.page for p in s.pages if p.is_checkpoint]
    assert cps, "debe forzar al menos un checkpoint"
    assert 2 in cps  # la página 2 por política


def test_long_story_gets_two_checkpoints():
    s = ensure_checkpoints(_story(6))
    assert sum(p.is_checkpoint for p in s.pages) >= 2  # pág 2 + intermedia


def test_respects_existing_checkpoints():
    s = ensure_checkpoints(_story(6, checkpoints={3}))
    cps = [p.page for p in s.pages if p.is_checkpoint]
    assert cps == [3], "no debe tocar los checkpoints que el modelo ya marcó"


def test_single_page_story():
    s = ensure_checkpoints(_story(1))
    assert s.pages[0].is_checkpoint is True
