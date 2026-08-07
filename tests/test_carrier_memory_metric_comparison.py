from __future__ import annotations

import numpy as np

from emergenz_knoten import FiniteMemoryState, OrientedMemoryState
from experiments.current.memory.carrier_memory_metric_comparison import (
    _classification,
    perturb_carrier,
    summarize_metric,
)


def _state() -> OrientedMemoryState:
    scalar = FiniteMemoryState(
        x=np.array([0.0, 0.0]),
        memory=np.array([[0.0, 0.0], [-1.0, 0.0]]),
        weights=np.array([0.6, 0.3]),
    )
    return OrientedMemoryState(
        scalar_state=scalar,
        orientations=np.zeros((2, 2)),
        weights=np.array([0.2, 0.1]),
        carrier_orientation=np.array([0.3, -0.4]),
        orientation_relaxation=0.1,
    )


def test_perturb_carrier_leaves_deposited_history_unchanged() -> None:
    state = _state()
    perturbed = perturb_carrier(state, np.array([0.1, 0.2]))
    np.testing.assert_allclose(perturbed.carrier_orientation, [0.4, -0.2])
    np.testing.assert_array_equal(perturbed.orientations, state.orientations)
    assert perturbed.scalar_state is state.scalar_state


def test_classification_covers_exact_mode_order() -> None:
    q = 0.99
    lower = (1.0 - np.sqrt(q)) ** 2
    upper = (1.0 + np.sqrt(q)) ** 2
    assert _classification(0.0, q) == "null"
    assert _classification(0.5 * lower, q) == "overdamped"
    assert _classification(np.sqrt(lower * upper), q) == "complex"
    assert _classification(0.5 * (upper + 2.0 * (1.0 + q)), q) == "alternating"
    assert _classification(5.0, q) == "unstable"


def test_metric_summary_preserves_forward_null_mode() -> None:
    metric = np.diag([2.0, 3.0, 4.0])
    forward = np.diag([1.0, 1.0, 0.0])
    summary = summarize_metric(metric, forward, gain=0.1, q=0.9)
    np.testing.assert_allclose(summary["pullback_eigenvalues"][0], 0.0)
    assert summary["classifications"][0] == "null"
