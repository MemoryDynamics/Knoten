from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "current" / "kernels"))
sys.path.insert(0, str(ROOT / "experiments" / "current" / "dynamics"))
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import linear_memory_relative_rms_radius  # noqa: E402
import fixed_g_nonlinearity_slice as gate  # noqa: E402


def test_retained_memory_mass_matches_truncated_geometric_sum() -> None:
    mass = gate.retained_memory_mass(
        lambda_value=0.01,
        memory_mass=1.0,
        horizon=600,
    )

    assert mass == pytest.approx(1.0 - 0.99**600)


def test_epsilon_inverts_linear_radius_ratio() -> None:
    target = 0.1
    length = 3.0
    epsilon = gate.epsilon_for_target_radius_ratio(
        target_radius_ratio=target,
        length_scale=length,
        lambda_value=0.01,
        restoring_per_update=0.432,
        dim=3,
    )
    radius = linear_memory_relative_rms_radius(
        epsilon=epsilon,
        lambda_value=0.01,
        restoring_per_update=0.432,
        dim=3,
    )

    assert radius / length == pytest.approx(target)


def _endpoint_rows(departures: list[float], *, shape_shift: float) -> list[dict]:
    return [
        {
            "active_normalized_radius_departure": departure,
            "knot_score_change": 0.0,
            "memory_dimension_change": shape_shift,
            "memory_roundness_change": 0.0,
            "residence_log2_ratio": 0.0,
        }
        for departure in departures
    ]


def test_gate_requires_radius_and_independent_support_for_nonlinear_candidate() -> None:
    decision = gate.classify_nonlinearity_gate(
        _endpoint_rows([0.24, 0.25, 0.22, 0.27, -0.01], shape_shift=0.30)
    )

    assert decision["classification"] == "nonlinear_candidate"
    assert decision["same_sign_seed_count"] == 4
    assert decision["supporting_metric_flags"]["memory_dimension"] is True


def test_gate_accepts_seed_stable_linear_scaling() -> None:
    decision = gate.classify_nonlinearity_gate(
        _endpoint_rows([0.02, -0.03, 0.01, 0.04, -0.02], shape_shift=0.02)
    )

    assert decision["classification"] == "linear_compatible"
    assert decision["within_twenty_percent_seed_count"] == 5
