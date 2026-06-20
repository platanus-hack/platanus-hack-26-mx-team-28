"""Tests deterministas del mapeo edad → estadio (sin API key)."""

from development import erikson_stage, ma_stage


def test_ma_stage_boundaries():
    assert ma_stage(3.0) == "ma_stage_1"
    assert ma_stage(5.9) == "ma_stage_1"
    assert ma_stage(6.0) == "ma_stage_2"
    assert ma_stage(8.9) == "ma_stage_2"
    assert ma_stage(9.0) == "ma_stage_3"
    assert ma_stage(12.0) == "ma_stage_3"


def test_erikson_stage():
    assert erikson_stage(5.0) == "initiative_vs_guilt"
    assert erikson_stage(7.0) == "industry_vs_inferiority"
