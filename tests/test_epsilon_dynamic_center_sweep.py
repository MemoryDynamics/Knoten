from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "current"
    / "dynamics"
    / "epsilon_dynamic_center_sweep.py"
)
SPEC = importlib.util.spec_from_file_location("epsilon_dynamic_center_sweep", SCRIPT_PATH)
assert SPEC is not None
epsilon_dynamic_center_sweep = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(epsilon_dynamic_center_sweep)


def test_default_epsilon_grid_includes_zero_and_24_log_points() -> None:
    values = epsilon_dynamic_center_sweep.DEFAULT_EPSILONS

    assert values[0] == 0.0
    assert len(values) == 25
    assert values[1] == pytest.approx(1.0e-12)
    assert values[-1] == pytest.approx(1.0e1)


def test_epsilon_token_is_path_safe_and_distinguishes_zero() -> None:
    assert epsilon_dynamic_center_sweep._epsilon_token(0.0) == "0"
    assert epsilon_dynamic_center_sweep._epsilon_token(1.0e-12) == "1em12"
    assert epsilon_dynamic_center_sweep._epsilon_token(1.5e1) == "1p5ep01"


def test_epsilon_positions_place_zero_before_log_axis() -> None:
    positions, ticks, labels = epsilon_dynamic_center_sweep._epsilon_positions(
        [0.0, 1.0e-3, 1.0e1]
    )

    assert positions[0.0] < positions[1.0e-3]
    assert positions[1.0e-3] == pytest.approx(-3.0)
    assert positions[1.0e1] == pytest.approx(1.0)
    assert labels[0] == "0"
    assert ticks[0] == pytest.approx(-4.0)


def test_nearest_epsilons_keeps_order_and_deduplicates() -> None:
    selected = epsilon_dynamic_center_sweep._nearest_epsilons(
        [0.0, 1.0e-12, 1.0e-6, 1.0e-3],
        [0.0, 2.0e-12, 9.0e-7, 1.1e-6],
    )

    assert selected == [0.0, 1.0e-12, 1.0e-6]

