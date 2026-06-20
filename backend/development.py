"""Mapeo edad → estadio de desarrollo (determinista), anclado a `psicologia.md §2`.

Lo usa el post-procesador del Agente 2 para rellenar `developmental_stage` sin dejarlo al criterio
del LLM, y el system prompt para calibrar la dificultad moral del dilema.

Ma (2013), modelo moral integrado:
- Estadio 1 (≈3–6): supervivencia, egocentrismo, obediencia. El egoísmo es NORMAL aquí.
- Estadio 2 (≈6–9): afecto, altruismo recíproco.
- Estadio 3 (≈9–12): pertenencia, altruismo de grupo primario.
"""

from __future__ import annotations


def ma_stage(age: float) -> str:
    """Devuelve 'ma_stage_1' | 'ma_stage_2' | 'ma_stage_3' según la edad exacta."""
    if age < 6:
        return "ma_stage_1"
    if age < 9:
        return "ma_stage_2"
    return "ma_stage_3"


def erikson_stage(age: float) -> str:
    """Estadio psicosocial de Erikson relevante para 3–12 años."""
    if age < 6:
        return "initiative_vs_guilt"
    return "industry_vs_inferiority"


def stage_guidance(age: float) -> str:
    """Frase de calibración para inyectar en el prompt del Agente 2."""
    stage = ma_stage(age)
    return {
        "ma_stage_1": "Estadio Ma 1 (3-6): el egocentrismo es normal; dilemas simples y concretos, "
        "sin exigir razonamiento moral complejo.",
        "ma_stage_2": "Estadio Ma 2 (6-9): nociones de reciprocidad y amistad; dilemas con un poco "
        "más de matiz social.",
        "ma_stage_3": "Estadio Ma 3 (9-12): pertenencia a un grupo; dilemas con más matices y "
        "consecuencias sociales.",
    }[stage]
