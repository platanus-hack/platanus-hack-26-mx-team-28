"""Runner reutilizable del Agente 1 (Narrador) en aislamiento.

Construye el `state` de la sesión a partir de un `ChildProfile` (incluida la lista de exclusión
derivada) y ejecuta el agente con `InMemoryRunner`, devolviendo un `Story` validado. Lo usan tanto
el arnés de pruebas como, más adelante, la orquestación.
"""

from __future__ import annotations

import asyncio

from google.adk.runners import InMemoryRunner
from google.genai import types

from agents.narrador import root_agent
from profile import derive_exclusion_list
from schemas import ChildProfile, Story

APP_NAME = "narrador"


def ensure_checkpoints(story: Story) -> Story:
    """Garantiza ≥1 checkpoint de forma determinista (el LLM a veces marca 0).

    Solo interviene si el modelo NO marcó ninguno: respeta su elección cuando sí marcó. Política:
    marca la página 2 (o la 1ª si solo hay una) y, en cuentos de ≥5 páginas, también una intermedia.
    """
    if not story.pages or any(p.is_checkpoint for p in story.pages):
        return story
    n = len(story.pages)
    idx = 1 if n >= 2 else 0
    story.pages[idx].is_checkpoint = True
    if n >= 5:
        mid = n // 2
        if mid != idx:
            story.pages[mid].is_checkpoint = True
    return story


def build_state(profile: ChildProfile) -> dict[str, str]:
    """Aplana el perfil al state que el system prompt consume vía templating `{...}`."""
    return {
        "child_name": profile.name,
        "child_age": f"{profile.age:g}",
        "child_sex": profile.sex,
        "child_likes": ", ".join(profile.likes),
        "child_temperament": profile.temperament,
        "story_theme": profile.story_theme,
        "recent_events": "\n".join(profile.recent_events),
        "exclusion_list": ", ".join(derive_exclusion_list(profile.recent_events)),
        "main_character": profile.main_character,
        "secondary_characters": ", ".join(profile.secondary_characters),
    }


async def agenerate_story(profile: ChildProfile) -> Story:
    runner = InMemoryRunner(agent=root_agent, app_name=APP_NAME)
    session = await runner.session_service.create_session(
        app_name=APP_NAME, user_id="tester", state=build_state(profile)
    )
    final_text: str | None = None
    async for event in runner.run_async(
        user_id="tester",
        session_id=session.id,
        new_message=types.Content(role="user", parts=[types.Part(text="Crea el cuento ahora.")]),
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = event.content.parts[0].text
    if final_text is None:
        raise RuntimeError("El Narrador no devolvió respuesta final.")
    return ensure_checkpoints(Story.model_validate_json(final_text))


def generate_story(profile: ChildProfile) -> Story:
    """Versión síncrona para tests y scripts."""
    return asyncio.run(agenerate_story(profile))
