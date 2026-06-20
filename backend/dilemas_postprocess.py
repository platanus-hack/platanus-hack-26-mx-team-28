"""Post-procesador determinista del Agente 2: valida el borrador del LLM y lo enriquece.

Es el guardrail de integridad: el LLM solo propone (dimensión, sub-eje, opciones→polo); aquí se
verifica contra `taxonomy.py` y se rellenan los metadatos sensibles (anclaje teórico, estadio por
edad, edad exacta, temas excluidos, ids) que NO deben quedar a criterio del modelo.

`enrich_and_validate` devuelve (dilemas_válidos, errores). Un borrador con cualquier error se descarta
y su motivo queda en la lista de errores.
"""

from __future__ import annotations

import unicodedata
import uuid
from datetime import datetime, timezone

import taxonomy as tax
from development import ma_stage
from profile import derive_exclusion_list
from schemas import ChildProfile, Dilemma, DilemmaDraft, DilemmaDraftSet, Story


# Palabras que delatan una fuga de un tema vetado dentro del texto del dilema.
_LEAK_INDICATORS: dict[str, tuple[str, ...]] = {
    "duelo_muerte": ("murio", "muerte", "morir", "fallecio", "se fue al cielo", "tumba"),
    "perdida_mascota": ("murio", "perdio a su mascota", "su mascota ya no"),
    "mudanza": ("se mudaron", "mudanza", "dejar su casa para siempre"),
    "nuevo_bebe": ("nacio un bebe", "hermanito nuevo", "celos del bebe"),
    "divorcio_separacion_padres": ("se separaron", "divorcio", "papas ya no viven juntos"),
    "enfermedad_grave": ("cancer", "hospital", "muy enfermo"),
}


def _norm(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def _find_leaks(text: str, topics: list[str]) -> list[str]:
    blob = _norm(text)
    hits: list[str] = []
    for topic in topics:
        for word in _LEAK_INDICATORS.get(topic, ()):  # noqa: B007
            if word in blob:
                hits.append(f"{topic}:{word}")
    return hits


def _validate_draft(d: DilemmaDraft, checkpoint_pages: set[int], excluded: list[str]) -> list[str]:
    errs: list[str] = []
    prefix = f"pág {d.page}"

    if not tax.is_valid(d.primary_dimension):
        errs.append(f"{prefix}: dimensión inválida '{d.primary_dimension}'")
        return errs  # sin dimensión válida no podemos validar polos
    if not tax.is_valid(d.primary_dimension, d.subaxis):
        errs.append(f"{prefix}: sub-eje '{d.subaxis}' no pertenece a '{d.primary_dimension}'")

    if d.page not in checkpoint_pages:
        errs.append(f"{prefix}: no corresponde a una página de checkpoint del cuento")

    if len(d.options) < 2:
        errs.append(f"{prefix}: se requieren al menos 2 opciones")

    poles_seen: list[str] = []
    for opt in d.options:
        if not tax.is_valid(d.primary_dimension, pole=opt.pole):
            errs.append(f"{prefix} opción {opt.id}: polo '{opt.pole}' no es de '{d.primary_dimension}'")
        poles_seen.append(opt.pole)
    if len(set(poles_seen)) != len(poles_seen):
        errs.append(f"{prefix}: hay opciones que mapean al MISMO polo (deben ser distintos)")

    leaks = _find_leaks(f"{d.narrative_context} {d.prompt} " + " ".join(o.text for o in d.options), excluded)
    if leaks:
        errs.append(f"{prefix}: FUGA de exclusión {leaks}")

    return errs


def enrich_and_validate(
    draft_set: DilemmaDraftSet, story: Story, profile: ChildProfile
) -> tuple[list[Dilemma], list[str]]:
    checkpoint_pages = {p.page for p in story.pages if p.is_checkpoint}
    excluded = derive_exclusion_list(profile.recent_events)
    stage = ma_stage(profile.age)

    dilemmas: list[Dilemma] = []
    errors: list[str] = []

    for d in draft_set.items:
        draft_errors = _validate_draft(d, checkpoint_pages, excluded)
        if draft_errors:
            errors.extend(draft_errors)
            continue
        dilemmas.append(Dilemma(
            dilemma_id=uuid.uuid4().hex,
            page=d.page,
            narrative_context=d.narrative_context,
            prompt=d.prompt,
            primary_dimension=d.primary_dimension,
            subaxis=d.subaxis,
            framework_refs=dict(tax.DIMENSIONS[d.primary_dimension].framework_refs),
            options=d.options,
            age_at_presentation=profile.age,
            developmental_stage=stage,
            excluded_topics_respected=excluded,
            created_at=datetime.now(timezone.utc),
        ))

    return dilemmas, errors
