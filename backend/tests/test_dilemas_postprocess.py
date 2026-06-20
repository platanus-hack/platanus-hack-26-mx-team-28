"""Tests deterministas del post-procesador del Agente 2 — el guardrail de integridad (sin API key).

Usa borradores hechos a mano (sin LLM) sobre el fixture story_dino.json (checkpoints en págs 2 y 5).
"""

from pathlib import Path

from dilemas_postprocess import enrich_and_validate
from schemas import AnswerOption, ChildProfile, DilemmaDraft, DilemmaDraftSet, Story

FIXTURE = Path(__file__).resolve().parents[1] / "eval" / "fixtures" / "story_dino.json"


def _story() -> Story:
    return Story.model_validate_json(FIXTURE.read_text(encoding="utf-8"))


def _opt(i, text, pole):
    return AnswerOption(id=i, text=text, pole=pole)


def _empatia_page2():
    return DilemmaDraft(
        page=2, narrative_context="Mateo ve a la niña sola.", prompt="¿Qué hace Mateo?",
        primary_dimension="empatia", subaxis="reaccion_al_conflicto",
        options=[
            _opt("A", "Se acerca y la invita a jugar", "prosocial_asertivo"),
            _opt("B", "Sigue jugando solo sin acercarse", "pasivo_evitativo"),
            _opt("C", "Le grita que ese es su lugar", "reactivo_agresivo"),
        ],
    )


def _apego_page5():
    return DilemmaDraft(
        page=5, narrative_context="El dibujo de Sofía vuela al charco.", prompt="¿Qué hace Mateo?",
        primary_dimension="confianza_apego", subaxis="pedir_ayuda_vs_resolver_solo",
        options=[
            _opt("A", "Corre a ayudar a Sofía a rescatarlo", "busca_vinculo"),
            _opt("B", "Se queda quieto sin saber qué hacer", "evita_desconfia"),
        ],
    )


def test_valid_drafts_enrich_clean():
    profile = ChildProfile(name="Mateo", age=7.0)
    dilemmas, errors = enrich_and_validate(
        DilemmaDraftSet(items=[_empatia_page2(), _apego_page5()]), _story(), profile
    )
    assert errors == []
    assert len(dilemmas) == 2
    d = dilemmas[0]
    assert d.developmental_stage == "ma_stage_2"          # edad 7
    assert d.age_at_presentation == 7.0
    assert d.framework_refs.get("casel") == "social_awareness"  # rellenado por código
    assert d.dilemma_id and d.created_at


def test_invalid_dimension_is_rejected():
    profile = ChildProfile(name="X", age=7.0)
    bad = _empatia_page2().model_copy(update={"primary_dimension": "inventada"})
    dilemmas, errors = enrich_and_validate(DilemmaDraftSet(items=[bad]), _story(), profile)
    assert dilemmas == [] and any("dimensión inválida" in e for e in errors)


def test_invalid_pole_is_rejected():
    profile = ChildProfile(name="X", age=7.0)
    bad = _apego_page5()
    bad.options[0].pole = "autonomo"  # polo de otra dimensión
    dilemmas, errors = enrich_and_validate(DilemmaDraftSet(items=[bad]), _story(), profile)
    assert dilemmas == [] and any("polo" in e for e in errors)


def test_duplicate_poles_rejected():
    profile = ChildProfile(name="X", age=7.0)
    bad = _apego_page5()
    bad.options[1].pole = "busca_vinculo"  # ambas opciones al mismo polo
    dilemmas, errors = enrich_and_validate(DilemmaDraftSet(items=[bad]), _story(), profile)
    assert dilemmas == [] and any("MISMO polo" in e for e in errors)


def test_non_checkpoint_page_rejected():
    profile = ChildProfile(name="X", age=7.0)
    bad = _empatia_page2().model_copy(update={"page": 3})  # pág 3 no es checkpoint
    dilemmas, errors = enrich_and_validate(DilemmaDraftSet(items=[bad]), _story(), profile)
    assert dilemmas == [] and any("checkpoint" in e for e in errors)


def test_exclusion_leak_rejected():
    profile = ChildProfile(name="X", age=7.0, recent_events=["Se murió nuestro perro"])
    leaky = _empatia_page2().model_copy(update={
        "narrative_context": "El perrito de Mateo murió y él está triste.",
    })
    dilemmas, errors = enrich_and_validate(DilemmaDraftSet(items=[leaky]), _story(), profile)
    assert dilemmas == [] and any("FUGA de exclusión" in e for e in errors)
