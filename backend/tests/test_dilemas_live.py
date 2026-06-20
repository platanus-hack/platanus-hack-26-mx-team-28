"""Tests EN VIVO del Agente 2 (requieren GOOGLE_API_KEY; se saltan si no está).

Sobre el fixture story_dino.json valida los criterios deterministas:
- un dilema por cada página de checkpoint (2);
- cero errores del post-procesador (mapeo válido, polos distintos, sin fugas) — el GATE del Paso 2;
- cada dilema tiene prompt y narrative_context no vacíos.
"""

import os
from pathlib import Path

import pytest

from schemas import ChildProfile, Story

pytestmark = pytest.mark.skipif(
    not os.environ.get("GOOGLE_API_KEY"),
    reason="sin GOOGLE_API_KEY: test en vivo omitido (corre cuando pongas la key en backend/.env)",
)

FIXTURE = Path(__file__).resolve().parents[1] / "eval" / "fixtures" / "story_dino.json"


def _story() -> Story:
    return Story.model_validate_json(FIXTURE.read_text(encoding="utf-8"))


def test_one_valid_dilemma_per_checkpoint():
    from dilemas_runner import generate_dilemmas

    story = _story()
    profile = ChildProfile(name="Mateo", age=7.0, likes=["dinosaurios"])
    checkpoints = [p.page for p in story.pages if p.is_checkpoint]

    dilemmas, errors = generate_dilemmas(story, profile)

    assert errors == [], f"el post-procesador reportó errores (gate): {errors}"
    assert len(dilemmas) == len(checkpoints), "debe haber un dilema por checkpoint"
    assert {d.page for d in dilemmas} == set(checkpoints)
    for d in dilemmas:
        assert d.prompt.strip() and d.narrative_context.strip()
        assert len(d.options) >= 2
        assert len({o.pole for o in d.options}) == len(d.options)  # polos distintos
