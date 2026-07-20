from __future__ import annotations

from argparse import Namespace
import importlib.util
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT / "experiments/current/memory/synchronization/one_way_interaction_age_audit.py"
)
SPEC = importlib.util.spec_from_file_location("one_way_interaction_age_audit", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = audit
SPEC.loader.exec_module(audit)


def _args() -> Namespace:
    return Namespace(
        evaluation_updates=[500_000, 1_000_000],
        min_seed_fraction=0.8,
        plateau_radius_log_limit=0.05,
        plateau_dimension_limit=0.05,
        plateau_spectrum_limit=0.02,
        modified_radius_log_min=0.10,
        modified_dimension_min=0.10,
        modified_spectrum_min=0.05,
    )


def _row(seed: int, *, plateau: bool = True, modified: bool = True) -> dict:
    previous_radius = 1.19 if plateau else 1.0
    final_radius = 1.20 if modified else 1.01
    return {
        "continuation_seed": seed,
        "source_stationarity": {"stationary_shape_pass": True},
        "checkpoints": [
            {
                "evaluation_update": 500_000,
                "dynamic_free_radius_ratio": previous_radius,
                "dynamic_shape_dimension": 2.8,
                "dynamic_free_shape_spectrum_median": 0.06,
            },
            {
                "evaluation_update": 1_000_000,
                "dynamic_free_radius_ratio": final_radius,
                "dynamic_shape_dimension": 2.81 if plateau else 3.0,
                "dynamic_minus_free_shape_dimension": 0.12 if modified else 0.01,
                "dynamic_free_shape_spectrum_median": 0.06 if modified else 0.01,
                "dynamic_minus_free_center_radii": 0.2,
            },
        ],
    }


def test_shape_features_are_rotation_invariant() -> None:
    base = np.diag([0.7, 0.2, 0.1])
    rotation = np.array(
        [
            [0.0, -1.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    tensors = np.asarray([base, rotation @ base @ rotation.T])

    dimension, roundness = audit._shape_features(tensors)

    np.testing.assert_allclose(dimension[0], dimension[1])
    np.testing.assert_allclose(roundness[0], roundness[1])


def test_gate_requires_seed_robust_plateau_and_modification() -> None:
    passing = [_row(seed) for seed in range(1, 6)]
    failing = [_row(seed, plateau=seed <= 3, modified=True) for seed in range(1, 6)]

    pass_gate = audit._gate(passing, _args())
    fail_gate = audit._gate(failing, _args())

    assert pass_gate["late_shape_plateau_pass"]
    assert pass_gate["interaction_modified_shape_pass"]
    assert pass_gate["stable_interaction_modified_shape_candidate"]
    assert not fail_gate["late_shape_plateau_pass"]
    assert not fail_gate["stable_interaction_modified_shape_candidate"]


def test_center_trend_recovers_linear_response() -> None:
    payload = {
        "aggregate": [
            {
                "evaluation_update": update,
                "dynamic_minus_free_center_radii": {
                    "median": 2.0e-5 * update + 0.25,
                    "q25": 0.0,
                    "q75": 0.0,
                },
            }
            for update in (20_000, 50_000, 100_000, 200_000)
        ],
        "parameters": {"separation_sigma_rep": 2.0},
        "calibration": {
            "source_center_offset": [4.0, 0.0, 0.0],
            "initial_target_radius": 0.5,
        },
    }

    trend = audit._center_trend(payload)

    np.testing.assert_allclose(trend["slope_radii_per_update"], 2.0e-5)
    np.testing.assert_allclose(trend["intercept_radii"], 0.25)
    np.testing.assert_allclose(trend["r_squared"], 1.0)
    np.testing.assert_allclose(trend["kernel_width_radii"], 4.0)
    np.testing.assert_allclose(trend["linear_updates_per_kernel_width"], 200_000)
