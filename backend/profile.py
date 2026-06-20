"""Derivación de la lista de exclusión a partir de los 'recuerdos' de los padres.

`idea.md §3` y `pruebas-agente1.md §3.2`: los eventos recientes en texto libre derivan una lista de
**temas vetados** que el Narrador no debe usar como eje del cuento (no activar duelos/traumas).

Implementación heurística y auditable (keyword → tema) a propósito: es transparente y testeable sin
LLM. Se documenta que podría convertirse en un paso LLM separado si se necesita más matiz.

Importante: NO todo evento se excluye. Una pelea menor en la escuela (E5) NO se veta — puede inspirar
un dilema suave de empatía; solo se vetan temas sensibles/potencialmente traumáticos.
"""

from __future__ import annotations

import unicodedata

# tema_vetado -> palabras clave que lo disparan (en minúsculas, sin tildes)
_TOPIC_KEYWORDS: dict[str, tuple[str, ...]] = {
    "duelo_muerte": (
        "murio", "muerte", "fallecio", "falleci", "se fue al cielo", "perdimos a",
        "enterramos", "velorio", "luto",
    ),
    "mudanza": ("mudamos", "mudanza", "nos cambiamos de casa", "nueva ciudad", "nuevo hogar"),
    "nuevo_bebe": ("nacio", "hermanito", "hermanita", "embaraz", "recien nacido", "llego el bebe"),
    "divorcio_separacion_padres": (
        "divorci", "se separaron", "nos separamos", "papas se separan", "ya no viven juntos",
    ),
    "perdida_mascota": ("se murio el perro", "se murio el gato", "perdimos a la mascota", "mascota murio"),
    "enfermedad_grave": ("cancer", "hospital", "enfermedad grave", "esta muy enfermo", "internado"),
}


def _normalize(text: str) -> str:
    """minúsculas y sin tildes, para matching robusto."""
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def derive_exclusion_list(recent_events: list[str]) -> list[str]:
    """Devuelve los temas vetados detectados en los recuerdos (sin duplicados, orden estable)."""
    found: list[str] = []
    blob = _normalize(" ".join(recent_events))
    for topic, keywords in _TOPIC_KEYWORDS.items():
        if any(kw in blob for kw in keywords):
            found.append(topic)
    return found
