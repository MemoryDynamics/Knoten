from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "memory"
    / "oriented_fourier_closure_audit.py"
)
SPEC = importlib.util.spec_from_file_location(
    "oriented_fourier_closure_audit",
    SCRIPT,
)
assert SPEC is not None and SPEC.loader is not None
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def test_mode_directions_include_axes_and_normalized_diagonal() -> None:
    directions = audit.mode_directions(3)

    assert directions.shape == (4, 3)
    np.testing.assert_array_equal(directions[:3], np.eye(3))
    assert np.isclose(np.linalg.norm(directions[-1]), 1.0)


def test_summary_recovers_constant_forgetting_without_spatial_terms() -> None:
    q = 0.9
    statistics = np.zeros((2, 2, 4, 3))
    statistics[..., 0] = 10.0
    statistics[..., 1] = q * 10.0
    statistics[..., 2] = q * q * 10.0

    summary = audit.summarize_statistics(
        statistics,
        np.array([0.5, 1.0, 2.0, 4.0]),
        q,
    )

    assert summary["max_abs_q_error"] < 1e-14
    assert summary["max_normalized_residual"] < 1e-14
    assert summary["max_abs_spatial_coefficient"] < 1e-14