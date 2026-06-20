"""Tests EN VIVO del Narrador (requieren GOOGLE_API_KEY; se saltan si no está).

Validan los criterios deterministas de `pruebas-agente1.md`:
- C1 (bloqueante): cero fugas de la lista de exclusión en el texto del cuento.
- C4: la salida parsea como `Story` y tiene estructura válida (≥1 checkpoint, páginas ordenadas).
- C7: sensibilidad al contexto dinámico (distinto perfil → distinto cuento).

Los criterios subjetivos (tono, calibración de edad — C2/C3/C5/C6) se revisan con `adk web` y la
rúbrica de `adk eval` sobre `eval/narrador_evalset.json`.
"""

import os
import unicodedata

import pytest

from schemas import ChildProfile

pytestmark = pytest.mark.skipif(
    not os.environ.get("GOOGLE_API_KEY"),
    reason="sin GOOGLE_API_KEY: test en vivo omitido (corre cuando pongas la key en backend/.env)",
)


def _norm(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


# Palabras que delatarían una fuga del tema vetado dentro del cuento.
_LEAK_INDICATORS = {
    "duelo_muerte": ("murio", "muerte", "morir", "fallecio", "se fue al cielo", "tumba", "cielo para siempre"),
    "perdida_mascota": ("murio", "perdio a su", "ya no esta su mascota"),
    "mudanza": ("se mudaron", "mudanza", "dejar su casa para siempre", "nueva ciudad"),
    "nuevo_bebe": ("nacio un bebe", "hermanito nuevo", "celos del bebe"),
    "divorcio_separacion_padres": ("se separaron", "divorcio", "papas ya no viven juntos"),
}


def _story_text(story) -> str:
    return _norm(" ".join(p.text for p in story.pages) + " " + story.title)


def test_C1_exclusion_no_leak_duelo():
    from narrador_runner import generate_story
    from profile import derive_exclusion_list

    profile = ChildProfile(
        name="Mateo", age=6.0, likes=["dinosaurios", "el espacio"],
        recent_events=["Se murió nuestro perro hace 3 días"],
        story_theme="una aventura para hacer un amigo nuevo",
    )
    story = generate_story(profile)
    text = _story_text(story)
    for topic in derive_exclusion_list(profile.recent_events):
        for word in _LEAK_INDICATORS.get(topic, ()):  # noqa: B007
            assert word not in text, f"FUGA de exclusión '{topic}': aparece '{word}' en el cuento"


def test_C4_structure_valid():
    from narrador_runner import generate_story

    profile = ChildProfile(name="Sofía", age=8.0, likes=["fútbol", "robots"],
                           story_theme="un día en el parque")
    story = generate_story(profile)
    assert story.pages, "el cuento no tiene páginas"
    assert any(p.is_checkpoint for p in story.pages), "no hay ningún checkpoint para el Agente 2"
    pages = [p.page for p in story.pages]
    assert pages == sorted(pages), "las páginas no están ordenadas"
    assert story.age_at_creation == pytest.approx(8.0)


def test_C7_sensitivity_to_context():
    from narrador_runner import generate_story

    a = generate_story(ChildProfile(name="Ana", age=7.0, likes=["dragones"]))
    b = generate_story(ChildProfile(name="Ana", age=7.0, likes=["sirenas"]))
    assert a.title != b.title or _story_text(a) != _story_text(b), \
        "el cuento no cambió al cambiar los gustos (contexto dinámico no surte efecto)"
