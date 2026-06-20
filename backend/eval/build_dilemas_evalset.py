"""Genera el evalset NATIVO de ADK del Agente 2 (`dilemas_evalset.json`) desde `dilemas_cases.json`.

Cada caso: el cuento (fixture) va en el mensaje del usuario; la calibración (edad, estadio, exclusión,
checkpoints) en `session_input.state` (idéntico al runner real, vía build_state). Rúbrica D1-D6.

Construir el JSON NO requiere key. Evaluar sí:
    adk eval backend/agents/dilemas backend/eval/dilemas_evalset.json --print_detailed_results

Regenerar: backend/.venv/bin/python backend/eval/build_dilemas_evalset.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

from google.adk.evaluation.eval_case import EvalCase, Invocation, SessionInput  # noqa: E402
from google.adk.evaluation.eval_rubrics import Rubric, RubricContent  # noqa: E402
from google.adk.evaluation.eval_set import EvalSet  # noqa: E402
from google.genai import types  # noqa: E402

from dilemas_runner import build_state  # noqa: E402
from schemas import ChildProfile, Story  # noqa: E402

CASES_PATH = Path(__file__).resolve().parent / "dilemas_cases.json"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
OUT_PATH = Path(__file__).resolve().parent / "dilemas_evalset.json"


def _rubric(rid: str, text: str, desc: str) -> Rubric:
    return Rubric(rubric_id=rid, rubric_content=RubricContent(text_property=text), description=desc)


RUBRICS = [
    _rubric("D1_taxonomia",
            "Cada dilema usa primary_dimension, subaxis y polos EXCLUSIVAMENTE de la taxonomía.",
            "Mapeo dentro de la taxonomía"),
    _rubric("D2_polos_distintos",
            "Cada opción mapea a un polo DISTINTO de la dimensión (2 polos→2 opciones; empatia→3).",
            "Opciones a polos distintos"),
    _rubric("D3_coherencia",
            "El dilema corresponde a una página de checkpoint y calza con su situación abierta.",
            "Coherencia con el checkpoint"),
    _rubric("D4_edad",
            "La dificultad moral del dilema está calibrada al estadio de desarrollo del niño.",
            "Calibración por edad"),
    _rubric("D5_exclusion",
            "El dilema NO introduce ningún tema de la lista de exclusión del estado.",
            "Respeta exclusión"),
    _rubric("D6_no_evaluativo",
            "Tono de cuento: las opciones no premian ni castigan; sin lenguaje clínico ni de examen. "
            "El niño no debe sentir que lo evalúan.",
            "No se siente evaluación"),
]


def build() -> EvalSet:
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    cases: list[EvalCase] = []
    for case in data["cases"]:
        story = Story.model_validate_json((FIXTURES / case["story_fixture"]).read_text(encoding="utf-8"))
        profile = ChildProfile(**case["profile"])
        message = "Aquí está el cuento. Inserta los dilemas en los checkpoints.\n\n" + story.model_dump_json()
        inv = Invocation(
            invocation_id=f"{case['id']}-1",
            user_content=types.Content(role="user", parts=[types.Part(text=message)]),
            rubrics=list(RUBRICS),
        )
        cases.append(EvalCase(
            eval_id=f"{case['id']}_{case['focus']}",
            conversation=[inv],
            session_input=SessionInput(app_name="dilemas", user_id="tester",
                                       state=build_state(story, profile)),
        ))
    return EvalSet(
        eval_set_id="dilemas_v1",
        name="Dilemas (Agente 2) — rúbrica D1-D6",
        description="Inserta dilemas pre-registrados en los checkpoints; valida mapeo y exclusión.",
        eval_cases=cases,
    )


if __name__ == "__main__":
    es = build()
    OUT_PATH.write_text(es.model_dump_json(indent=2, exclude_none=True), encoding="utf-8")
    print(f"OK: {OUT_PATH} ({len(es.eval_cases)} casos)")
