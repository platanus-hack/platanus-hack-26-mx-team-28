"""Agente 2 — Dilemas. Inserta dilemas pre-registrados en los checkpoints del cuento.

Aislado: no usa tools. Recibe el cuento en el mensaje y la calibración por `state`. Su salida es un
borrador (`DilemmaDraftSet`); el post-procesador determinista lo valida y enriquece.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from google.adk.agents import LlmAgent

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from schemas import DilemmaDraftSet  # noqa: E402

from .prompts import DILEMAS_INSTRUCTION  # noqa: E402

MODEL = os.environ.get("DILEMAS_MODEL", "gemini-2.5-flash")

root_agent = LlmAgent(
    name="dilemas",
    model=MODEL,
    description="Lee el cuento del Narrador e inserta, en cada checkpoint, un dilema con el mapeo "
    "pre-registrado de cada opción a un polo conductual de la taxonomía.",
    instruction=DILEMAS_INSTRUCTION,
    output_schema=DilemmaDraftSet,
    output_key="dilemmas",
)
