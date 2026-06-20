"""Tests deterministas de la derivación de la lista de exclusión (el guardrail C1, sin API key).

Casos tomados de `pruebas-agente1.md §3.2`.
"""

from profile import derive_exclusion_list


def test_E1_duelo_perro():
    out = derive_exclusion_list(["Se murió nuestro perro hace 3 días"])
    assert "duelo_muerte" in out or "perdida_mascota" in out


def test_E2_mudanza():
    assert "mudanza" in derive_exclusion_list(["Nos mudamos de ciudad la semana pasada"])


def test_E3_nuevo_bebe():
    assert "nuevo_bebe" in derive_exclusion_list(["Nació su hermanito"])


def test_E4_divorcio():
    assert "divorcio_separacion_padres" in derive_exclusion_list(
        ["Sus papás se están divorciando"]
    )


def test_E5_pelea_escuela_NO_se_excluye():
    # una pelea menor NO es tema vetado: puede inspirar un dilema suave de empatía
    assert derive_exclusion_list(["Hoy se peleó en la escuela por un juguete"]) == []


def test_X1_sin_eventos():
    assert derive_exclusion_list([]) == []


def test_X2_multiples_eventos():
    out = derive_exclusion_list(["Nos mudamos de casa", "y nació su hermanita"])
    assert "mudanza" in out and "nuevo_bebe" in out


def test_matching_es_robusto_a_tildes_y_mayusculas():
    assert "duelo_muerte" in derive_exclusion_list(["ABUELO FALLECIÓ"])
