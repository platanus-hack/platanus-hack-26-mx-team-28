"""Tests deterministas de la taxonomía (corren sin API key)."""

import taxonomy as tax


def test_six_dimensions_present():
    assert set(tax.dimension_keys()) == {
        "regulacion_emocional", "confianza_apego", "honestidad",
        "empatia", "autonomia", "riesgo_cautela",
    }


def test_poles_unique_per_dimension():
    for key in tax.dimension_keys():
        poles = tax.poles_for(key)
        assert len(poles) == len(set(poles)), f"polos duplicados en {key}"
        assert len(poles) >= 2


def test_empatia_has_three_poles():
    assert set(tax.poles_for("empatia")) == {
        "prosocial_asertivo", "pasivo_evitativo", "reactivo_agresivo",
    }


def test_riesgo_cautela_is_secondary():
    assert tax.is_secondary("riesgo_cautela") is True
    # las demás NO son secundarias
    for key in tax.dimension_keys():
        if key != "riesgo_cautela":
            assert tax.is_secondary(key) is False


def test_every_dimension_has_framework_ref():
    for key in tax.dimension_keys():
        assert tax.DIMENSIONS[key].framework_refs, f"{key} sin anclaje teórico"
        assert tax.subaxes_for(key), f"{key} sin sub-ejes"


def test_is_valid_accepts_real_triple():
    assert tax.is_valid("empatia", "reaccion_al_conflicto", "prosocial_asertivo")
    assert tax.is_valid("autonomia", pole="autonomo")
    assert tax.is_valid("honestidad")  # solo dimensión


def test_is_valid_rejects_bad_values():
    assert not tax.is_valid("inventada")
    assert not tax.is_valid("empatia", "subaxis_falso")
    assert not tax.is_valid("empatia", "reaccion_al_conflicto", "polo_falso")
    # un polo válido pero de OTRA dimensión debe fallar
    assert not tax.is_valid("autonomia", pole="prosocial_asertivo")
