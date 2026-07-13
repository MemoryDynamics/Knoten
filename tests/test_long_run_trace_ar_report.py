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
    / "long_run_trace_ar_report.py"
)
SPEC = importlib.util.spec_from_file_location("long_run_trace_ar_report", SCRIPT_PATH)
assert SPEC is not None
long_run_trace_ar_report = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = long_run_trace_ar_report
SPEC.loader.exec_module(long_run_trace_ar_report)


def _case() -> object:
    steps = np.arange(0, 101, dtype=int)
    theta = 0.1 * steps
    centers = np.column_stack((0.01 * steps, np.zeros_like(theta), np.zeros_like(theta)))
    orbit = np.column_stack((np.cos(theta), np.sin(theta), np.zeros_like(theta)))
    positions = centers + orbit
    payload = {
        "condition": "baseline",
        "seed": 1,
        "config": {
            "alpha": 0.1,
            "amplitude_att": 35.0,
        },
        "diagnostics": {
            "dynamic_center_trace": {
                "trace": {
                    "steps": steps.tolist(),
                    "centers": centers.tolist(),
                    "positions": positions.tolist(),
                    "rms_radii": np.ones_like(theta).tolist(),
                    "x_distances": np.ones_like(theta).tolist(),
                },
                "spin_proxy": {
                    "sample_count": len(steps),
                },
            }
        },
    }
    return long_run_trace_ar_report.CaseRecord(
        a_att=35.0,
        condition="baseline",
        seed=1,
        path=Path("case.json"),
        payload=payload,
    )


def test_trace_block_features_use_uniform_tail_and_are_finite() -> None:
    features = long_run_trace_ar_report.trace_block_features(
        _case(),
        block_memory_time=1.0,
    )

    assert features.shape[0] == 10
    assert features.shape[1] == 11
    assert np.all(np.isfinite(features))
    assert np.max(np.abs(features[:, 0])) <= 1.0


def test_build_report_summarizes_classification_counts() -> None:
    payload = {
        "created_utc": "2026-07-13T00:00:00Z",
        "git_revision": "abc",
        "git_status": "",
        "case_count": 1,
        "parameters": {
            "conditions": ["baseline"],
            "a_att": [35.0],
            "block_memory_times": [1.0],
            "lags": [1],
            "pca_components": 2,
            "ridge": 1e-6,
            "slow_abs_min": 0.2,
        },
        "results": [
            {
                "a_att": 35.0,
                "condition": "baseline",
                "block_memory_time": 1.0,
                "feature_dim_raw": 10,
                "feature_dim_projected": 2,
                "pca_explained_ratio": [0.8, 0.2],
                "seed_block_counts": {"1": 10},
                "rows": [
                    {
                        "lag": 1,
                        "lag_updates": 10,
                        "lag_memory_times": 1.0,
                        "classification": "real",
                        "leading_real": 0.9,
                        "leading_imag": 0.0,
                        "leading_abs": 0.9,
                        "residual_rms": 0.1,
                        "n_pairs": 9,
                        "top_eigenvalues": ["0.9000"],
                    }
                ],
            }
        ],
    }

    report = long_run_trace_ar_report.build_report(payload)

    assert "# Long-Run Trace AR Mode Probe" in report
    assert "`active` / `real`: `1`" in report
    assert "Paper-I implication" in report
