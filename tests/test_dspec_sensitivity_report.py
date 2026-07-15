from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np

SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "current"
    / "dynamics"
    / "dspec_sensitivity_report.py"
)
SPEC = importlib.util.spec_from_file_location("dspec_sensitivity_report", SCRIPT_PATH)
assert SPEC is not None
dspec_sensitivity_report = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = dspec_sensitivity_report
SPEC.loader.exec_module(dspec_sensitivity_report)


def test_covariance_surrogate_preserves_effective_rank_order() -> None:
    points = dspec_sensitivity_report.covariance_surrogate(
        [4.0, 1.0, 0.25],
        n_points=400,
        seed=123,
    )

    assert points.shape == (400, 3)
    cov_dim = dspec_sensitivity_report.covariance_dimension(points)
    assert 1.4 <= cov_dim <= 2.2


def test_heat_and_knn_spectral_sensitivity_return_finite_values() -> None:
    rng = np.random.default_rng(456)
    points = rng.normal(size=(220, 3))
    d2 = dspec_sensitivity_report._pairwise_squared(points)

    heat = dspec_sensitivity_report.heat_spectral_from_d2(
        d2,
        bandwidth_factor=1.0,
        normalization="symmetric",
    )
    knn = dspec_sensitivity_report.knn_spectral_from_d2(d2, k=16)

    assert heat is not None
    assert knn is not None
    assert np.isfinite(heat)
    assert np.isfinite(knn)


def test_synthetic_rank_controls_include_rank_three() -> None:
    rows = dspec_sensitivity_report.synthetic_rank_controls(n_points=180, ambient_dim=10)
    by_rank = {row["rank"]: row for row in rows}

    assert 3 in by_rank
    assert by_rank[3]["covariance_dimension"] > by_rank[1]["covariance_dimension"]
    assert by_rank[3]["heat_sym_1"] is not None