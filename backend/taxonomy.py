"""Taxonomía psicológica — FUENTE ÚNICA DE VERDAD del feature.

Implementa la tabla de `esquema-datos.md §1` (dimensión → subaxis → polos), anclada al marco
CASEL + Ma (2013) + Erikson de `psicologia.md §2`. El Agente 2 (Dilemas) y el Dashboard solo
pueden usar valores definidos aquí; cualquier dimensión/subaxis/polo fuera de esta lista es inválido.

Diseño en Python puro (sin dependencias) a propósito: se importa y se testea sin instalar nada.

Nota: esto SUPERSEDE el snippet binario simplificado de `plan-desarrollo.md §2`. Los polos son
descriptivos del comportamiento, NO juicios clínicos: la alerta emerge solo del patrón agregado +
umbrales (ver `psicologia.md §3`), nunca de una opción suelta.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Dimension:
    """Una dimensión psicológica con sus sub-ejes y polos conductuales permitidos."""

    key: str
    subaxes: tuple[str, ...]
    poles: tuple[str, ...]
    framework_refs: dict[str, object]
    secondary: bool = False  # si True, no puede elevar alertas por sí sola (riesgo_cautela)
    description: str = ""


# --- Las 6 dimensiones (esquema-datos.md §1) ---------------------------------

DIMENSIONS: dict[str, Dimension] = {
    "regulacion_emocional": Dimension(
        key="regulacion_emocional",
        subaxes=("frustracion", "miedo_a_lo_desconocido"),
        poles=("regulado", "desregulado"),
        framework_refs={"casel": "self_management", "erikson": "trust_autonomy"},
        description="Manejo de frustración, miedo y calma ante lo desconocido.",
    ),
    "confianza_apego": Dimension(
        key="confianza_apego",
        subaxes=("apego", "pedir_ayuda_vs_resolver_solo"),
        poles=("busca_vinculo", "evita_desconfia"),
        framework_refs={"casel": "relationship_skills", "bowlby": "attachment"},
        description="Acercarse/pedir ayuda vs. desconfiar/resolver solo.",
    ),
    "honestidad": Dimension(
        key="honestidad",
        subaxes=("decir_verdad_incomoda", "asumir_error"),
        poles=("asume_transparente", "evade_oculta"),
        framework_refs={"casel": "responsible_decision_making", "ma": "justice_reasoning"},
        description="Decir la verdad incómoda y asumir errores.",
    ),
    "empatia": Dimension(
        key="empatia",
        subaxes=("reaccion_al_conflicto", "dano_a_otro"),
        poles=("prosocial_asertivo", "pasivo_evitativo", "reactivo_agresivo"),
        framework_refs={"casel": "social_awareness", "ma": "altruism"},
        description="Cómo trata a otro en conflicto; reacción ante el daño a otro.",
    ),
    "autonomia": Dimension(
        key="autonomia",
        subaxes=("decidir_solo_vs_guia",),
        poles=("autonomo", "dependiente"),
        framework_refs={"erikson": "autonomy_initiative", "casel": "self_management"},
        description="Decidir solo vs. buscar la guía de una figura adulta.",
    ),
    "riesgo_cautela": Dimension(
        key="riesgo_cautela",
        subaxes=("explorar_vs_quedarse_seguro",),
        poles=("explorador", "cauto"),
        framework_refs={"erikson": "initiative_vs_guilt"},
        secondary=True,  # secundaria: NO escala alertas sola (psicologia.md §2)
        description="Explorar lo desconocido vs. quedarse en lo seguro. Eje exploratorio.",
    ),
}


# --- Helpers de validación ----------------------------------------------------

def dimension_keys() -> list[str]:
    return list(DIMENSIONS.keys())


def poles_for(dimension: str) -> tuple[str, ...]:
    """Polos permitidos para una dimensión. KeyError si la dimensión no existe."""
    return DIMENSIONS[dimension].poles


def subaxes_for(dimension: str) -> tuple[str, ...]:
    return DIMENSIONS[dimension].subaxes


def is_secondary(dimension: str) -> bool:
    return DIMENSIONS[dimension].secondary


def is_valid(dimension: str, subaxis: str | None = None, pole: str | None = None) -> bool:
    """Valida una tripleta (dimensión, subaxis, polo) contra la taxonomía.

    `subaxis` y `pole` son opcionales: si se omiten, solo se valida lo provisto.
    """
    dim = DIMENSIONS.get(dimension)
    if dim is None:
        return False
    if subaxis is not None and subaxis not in dim.subaxes:
        return False
    if pole is not None and pole not in dim.poles:
        return False
    return True
