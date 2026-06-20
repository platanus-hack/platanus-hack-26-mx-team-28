"""Agente 'cuentista' — Narrador interactivo por tramos (output_schema=StorySegment)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from google.adk.agents import LlmAgent

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from schemas import StorySegment  # noqa: E402

from .prompts import CUENTISTA_INSTRUCTION  # noqa: E402

MODEL = os.environ.get("NARRADOR_MODEL", "gemini-2.5-flash")

root_agent = LlmAgent(
    name="cuentista",
    model=MODEL,
    description="Genera el cuento por tramos, ramificando según las decisiones del niño.",
    instruction=CUENTISTA_INSTRUCTION,
    output_schema=StorySegment,
    output_key="segment",
)
