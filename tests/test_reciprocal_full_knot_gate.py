from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments" / "current" / "memory" / "synchronization" / "reciprocity" / "reciprocal_full_knot_gate.py"
)
SPEC = importlib.util.spec_from_file_location("reciprocal_full_knot_gate", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _trace(matrix: np.ndarray, *, samples: int = 600) -> tuple[np.ndarray, np.ndarray]:
    state = np.empty((samples, 3, 2), dtype=float)
    state[0] = np.array([[1.0, 0.2], [-0.4, 0.7], [0.3, -0.8]])
    for index in range(1, samples):
        state[index] = state[index - 1] @ matrix.T
    return state[:, :, 0], state[:, :, 1]


def _thresholds() -> dict[str, float]:
    return {
        "min_complex_segments": 3,
        "frequency_min_per_memory_time": 0.05,
        "mode_relative_range_max": 0.25,
        "phase_coherence_min": 0.5,
        "fit_residual_ratio_max": 0.8,
        "fit_condition_max": 1e8,
    }


def test_mode_row_accepts_clean_complex_mode_and_rejects_real_mode() -> None:
    complex_matrix = np.array([[0.995, -0.02], [0.02, 0.995]])
    real_matrix = np.array([[0.96, 0.02], [0.0, 0.99]])
    complex_positions, complex_centers = _trace(complex_matrix)
    real_positions, real_centers = _trace(real_matrix)

    complex_row = MODULE._mode_row(
        complex_positions,
        complex_centers,
        alpha=0.01,
        sample_every=1,
        thresholds=_thresholds(),
    )
    real_row = MODULE._mode_row(
        real_positions,
        real_centers,
        alpha=0.01,
        sample_every=1,
        thresholds=_thresholds(),
    )

    assert complex_row["meaningful_complex"]
    assert complex_row["phase_coherence"] > 0.99
    assert not real_row["meaningful_complex"]


def test_segment_gate_requires_identity_across_registered_segments() -> None:
    matrix = np.array([[0.995, -0.02], [0.02, 0.995]])
    positions, centers = _trace(matrix, samples=1200)

    rows, summary = MODULE._segment_modes(
        positions,
        centers,
        start_index=0,
        segments=4,
        alpha=0.01,
        sample_every=1,
        thresholds=_thresholds(),
    )

    assert len(rows) == 4
    assert summary["meaningful_complex_segments"] == 4
    assert summary["segment_identity_pass"]


def test_cyclic_rotation_is_proper_and_orthogonal() -> None:
    rotation = MODULE._proper_cyclic_rotation(3)

    np.testing.assert_allclose(rotation.T @ rotation, np.eye(3))
    assert np.linalg.det(rotation) > 0.0
