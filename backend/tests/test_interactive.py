"""Tests deterministas del cuento interactivo (sin API key)."""

from interactive_runner import ensure_segment_checkpoint
from schemas import StorySegment, StoryPage


def _seg(n, ending=False, checkpoints=frozenset()):
    return StorySegment(
        is_ending=ending,
        pages=[StoryPage(page=i + 1, text=f"p{i+1}", image_prompt="img",
                         is_checkpoint=(i + 1) in checkpoints) for i in range(n)],
    )


def test_segment_schema():
    s = _seg(2)
    assert len(s.pages) == 2 and s.is_ending is False


def test_marks_last_page_when_no_checkpoint():
    s = ensure_segment_checkpoint(_seg(2))
    assert s.pages[-1].is_checkpoint is True
    assert s.pages[0].is_checkpoint is False


def test_respects_existing_checkpoint():
    s = ensure_segment_checkpoint(_seg(3, checkpoints={2}))
    assert [p.page for p in s.pages if p.is_checkpoint] == [2]


def test_ending_segment_gets_no_checkpoint():
    s = ensure_segment_checkpoint(_seg(2, ending=True))
    assert not any(p.is_checkpoint for p in s.pages)
