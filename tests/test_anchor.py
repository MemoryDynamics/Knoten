from __future__ import annotations

import numpy as np

from emergenz_knoten import SimulationConfig
from emergenz_knoten.anchor import (
    estimate_transfer_operator,
    memory_summary_features,
    memory_weight_in_ball,
    simulate_augmented_features,
    transition_count_matrix,
    vector_autocorrelation,
    voxel_labels,
)


def test_memory_summary_features_shape_and_values() -> None:
    x = np.array([1.0, 0.0])
    memory = np.array([[0.0, 0.0], [2.0, 0.0]])
    weights = np.array([0.25, 0.75])

    features = memory_summary_features(x, memory, weights)

    assert features.shape == (2 * 3 + 3,)
    assert np.allclose(features[:2], x)
    assert np.allclose(features[2:4], [1.5, 0.0])
    assert np.allclose(features[4:6], [-0.5, 0.0])
    assert features[-1] == 1.0


def test_memory_weight_in_ball_counts_weighted_deposits() -> None:
    memory = np.array([[0.0, 0.0], [0.4, 0.0], [2.0, 0.0]])
    weights = np.array([0.2, 0.3, 0.5])

    value = memory_weight_in_ball(memory, weights, [0.0, 0.0], radius=0.5)

    assert abs(value - 0.5) < 1e-12


def test_vector_autocorrelation_normalizes_lag_zero() -> None:
    values = np.array([[1.0], [0.0], [1.0], [0.0]])
    ac = vector_autocorrelation(values, max_lag=2)

    assert ac[0] == 1.0
    assert np.isfinite(ac[1])


def test_simulate_augmented_features_is_reproducible() -> None:
    cfg = SimulationConfig(steps=80, dim=2, alpha=0.1, sample_every=10, max_memory=20)

    first = simulate_augmented_features(cfg, seed=11)
    second = simulate_augmented_features(cfg, seed=11)

    assert first["samples"].shape == (8, 2)
    assert first["augmented_features"].shape == (8, 9)
    assert np.allclose(first["augmented_features"], second["augmented_features"])


def test_voxel_labels_and_transition_counts() -> None:
    points = np.array([[0.1], [0.2], [1.1], [1.2], [0.3]])
    labels = voxel_labels(points, voxel_size=1.0)
    counts = transition_count_matrix(labels, lag=1)

    assert labels.tolist() == [0, 0, 1, 1, 0]
    assert counts.shape == (2, 2)
    assert counts[0, 0] == 1.0
    assert counts[0, 1] == 1.0
    assert counts[1, 1] == 1.0
    assert counts[1, 0] == 1.0


def test_estimate_transfer_operator_returns_rates() -> None:
    features = np.array(
        [
            [0.0, 0.0],
            [0.1, 0.0],
            [1.0, 0.0],
            [1.1, 0.0],
            [1.2, 0.0],
            [0.2, 0.0],
            [0.3, 0.0],
        ]
    )

    estimate = estimate_transfer_operator(features, voxel_size=0.5, lag=1)

    assert estimate.transition_matrix.shape[0] >= 2
    assert estimate.eigenvalues.size == estimate.transition_matrix.shape[0]
    assert estimate.relaxation_rates.ndim == 1
