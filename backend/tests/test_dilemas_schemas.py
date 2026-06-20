"""Tests deterministas de los schemas del Contrato A (sin API key)."""

import pytest
from pydantic import ValidationError

from schemas import AnswerOption, DilemmaDraft, DilemmaDraftSet


def _opt(i, pole):
    return AnswerOption(id=i, text=f"opción {i}", pole=pole)


def test_dilemmadraft_validates():
    d = DilemmaDraft(
        page=2, narrative_context="ctx", prompt="¿qué hace?",
        primary_dimension="empatia", subaxis="reaccion_al_conflicto",
        options=[_opt("A", "prosocial_asertivo"), _opt("B", "pasivo_evitativo")],
    )
    assert d.page == 2 and len(d.options) == 2


def test_draftset_wraps_items():
    ds = DilemmaDraftSet(items=[])
    assert ds.items == []


def test_dilemmadraft_requires_fields():
    with pytest.raises(ValidationError):
        DilemmaDraft(page=2, prompt="x")  # faltan campos
