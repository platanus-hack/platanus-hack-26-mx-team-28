"""Agente 1 — Narrador. Genera un cuento personalizado y seguro (salida estructurada `Story`).

Aislado por diseño: no usa tools ni sub-agentes. El contexto del niño se inyecta vía el `state` de
la sesión ADK (templating `{...}` en la instrucción). Ver `prompts.py`.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from google.adk.agents import LlmAgent

# Permite importar `schemas` (en backend/) tanto vía `adk` como en pytest.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from schemas import Story  # noqa: E402

from .prompts import NARRADOR_INSTRUCTION  # noqa: E402

MODEL = os.environ.get("NARRADOR_MODEL", "gemini-2.5-flash")

root_agent = LlmAgent(
    name="narrador",
    model=MODEL,
    description="Genera un cuento infantil personalizado al perfil del niño, respetando la lista de "
    "exclusión, con checkpoints abiertos para que el Agente 2 inserte dilemas.",
    instruction=NARRADOR_INSTRUCTION,
    output_schema=Story,
    # La salida estructurada se guarda en state['story'] para inspección/encadenado.
    output_key="story",
)
