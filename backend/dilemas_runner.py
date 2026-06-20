"""Runner reutilizable del Agente 2 (Dilemas) en aislamiento.

Pasa el cuento (JSON) en el mensaje del usuario y la calibración por `state`, ejecuta el agente con
`InMemoryRunner`, y devuelve los `Dilemma` ya validados/enriquecidos por el post-procesador.
"""

from __future__ import annotations

import asyncio

from google.adk.runners import InMemoryRunner
from google.genai import types

from agents.dilemas import root_agent
from development import stage_guidance
from dilemas_postprocess import enrich_and_validate
from profile import derive_exclusion_list
from schemas import ChildProfile, Dilemma, DilemmaDraftSet, Story

APP_NAME = "dilemas"


def build_state(story: Story, profile: ChildProfile) -> dict[str, str]:
    checkpoint_pages = [p.page for p in story.pages if p.is_checkpoint]
    return {
        "child_age": f"{profile.age:g}",
        "stage_guidance": stage_guidance(profile.age),
        "exclusion_list": ", ".join(derive_exclusion_list(profile.recent_events)),
        "checkpoint_pages": ", ".join(str(p) for p in checkpoint_pages),
    }


async def agenerate_dilemmas(story: Story, profile: ChildProfile) -> tuple[list[Dilemma], list[str]]:
    runner = InMemoryRunner(agent=root_agent, app_name=APP_NAME)
    session = await runner.session_service.create_session(
        app_name=APP_NAME, user_id="tester", state=build_state(story, profile)
    )
    message = "Aquí está el cuento. Inserta los dilemas en los checkpoints.\n\n" + story.model_dump_json()
    final_text: str | None = None
    async for event in runner.run_async(
        user_id="tester",
        session_id=session.id,
        new_message=types.Content(role="user", parts=[types.Part(text=message)]),
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = event.content.parts[0].text
    if final_text is None:
        raise RuntimeError("El agente Dilemas no devolvió respuesta final.")
    draft_set = DilemmaDraftSet.model_validate_json(final_text)
    return enrich_and_validate(draft_set, story, profile)


def generate_dilemmas(story: Story, profile: ChildProfile) -> tuple[list[Dilemma], list[str]]:
    """Versión síncrona. Devuelve (dilemas_válidos, errores)."""
    return asyncio.run(agenerate_dilemmas(story, profile))
