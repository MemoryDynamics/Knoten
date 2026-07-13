from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import numpy as np


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "current"
    / "markov"
    / "feature_closure_report.py"
)
SPEC = importlib.util.spec_from_file_location("feature_closure_report", SCRIPT_PATH)
assert SPEC is not None
feature_closure_report = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = feature_closure_report
SPEC.loader.exec_module(feature_closure_report)


def test_feature_groups_match_trace_feature_layout() -> None:
    groups = feature_closure_report.feature_groups(11)

    assert groups["geometry"] == [0, 1, 2, 6, 7]
    assert groups["kinematics"] == [0, 1, 2, 3, 4, 5, 9]
    assert groups["shape_scalars"] == [6, 7]
    assert groups["drift_scalars"] == [8, 9]
    assert groups["spin_scalar"] == [10]
    assert groups["all"] == list(range(11))


def test_closure_scores_beat_shuffled_control_on_ar_process() -> None:
    rng = np.random.default_rng(123)
    transition = np.array([[0.8, 0.1], [-0.05, 0.7]], dtype=float)
    series = []
    for seed in range(4):
        local = np.random.default_rng(seed)
        values = [local.normal(size=2)]
        for _ in range(200):
            values.append(values[-1] @ transition + 0.05 * local.normal(size=2))
        series.append(np.asarray(values, dtype=float))

    scores = feature_closure_report._closure_scores(
        series,
        lag=1,
        ridge=1e-8,
        shuffle_repeats=3,
        rng=rng,
    )

    assert scores is not None
    assert scores["n_series"] == 4
    assert scores["ar_r2_median"] > 0.6
    assert scores["ar_minus_shuffle"] > 0.4


def test_build_report_contains_scalar_boundary() -> None:
    payload = {
        "created_utc": "2026-07-13T00:00:00Z",
        "git_revision": "abc",
        "git_status": "",
        "case_count": 2,
        "parameters": {
            "conditions": ["baseline", "eta_zero"],
            "a_att": [35.0],
            "block_memory_times": [1.0],
            "lags": [1],
            "ridge": 1e-6,
            "shuffle_repeats": 3,
            "random_seed": 1,
        },
        "results": [
            {
                "a_att": 35.0,
                "condition": "baseline",
                "feature_group": "geometry",
                "block_memory_time": 1.0,
                "lag": 1,
                "lag_memory_time": 1.0,
                "ar_r2_median": 0.5,
                "shuffle_r2_median": 0.0,
                "persistence_r2_median": 0.45,
                "ar_minus_shuffle": 0.5,
                "ar_minus_persistence": 0.05,
                "closure_lift": 0.05,
                "n_pairs": 100,
            }
        ],
    }

    report = feature_closure_report.build_report(payload)

    assert "# Feature-Closure Probe" in report
    assert "Paper-I implication" in report
    assert "future vector, tensor or internal-memory" in report
