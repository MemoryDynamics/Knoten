from __future__ import annotations

import numpy as np

from emergenz_knoten import SimulationConfig
from emergenz_knoten.markov import (
    chapman_kolmogorov_error,
    estimate_transfer_operator,
    implied_timescales,
    lagged_pairs,
    leading_nontrivial_eigenvalues,
    simulate_augmented_features,
    spectral_gap,
)


def test_lagged_pairs_use_sample_and_update_indices() -> None:
    features = np.arange(20, dtype=float).reshape(5, 4)
    sample_steps = np.array([10, 20, 30, 40, 50])

    dataset = lagged_pairs(features, sample_lag=2, sample_steps=sample_steps)

    assert dataset.current.shape == (3, 4)
    assert dataset.future.shape == (3, 4)
    assert dataset.sample_lag == 2
    assert dataset.lag_updates == 20
    assert np.all(dataset.current_sample_steps == [10, 20, 30])
    assert np.all(dataset.future_sample_steps == [30, 40, 50])


def test_simulate_augmented_features_can_return_dataclass() -> None:
    cfg = SimulationConfig(steps=50, dim=2, alpha=0.1, sample_every=10, max_memory=20)

    trajectory = simulate_augmented_features(cfg, seed=3, as_dataclass=True)

    assert trajectory.samples.shape == (5, 2)
    assert trajectory.augmented_features.shape == (5, 9)
    assert trajectory.as_dict()["sample_steps"].tolist() == [10, 20, 30, 40, 50]


def test_transfer_operator_reports_sample_and_update_lags() -> None:
    features = np.array(
        [
            [0.0],
            [0.2],
            [1.0],
            [1.2],
            [0.1],
            [0.3],
        ]
    )
    sample_steps = np.array([5, 10, 15, 20, 25, 30])

    estimate = estimate_transfer_operator(
        features,
        voxel_size=0.5,
        sample_lag=2,
        sample_steps=sample_steps,
    )

    assert estimate.sample_lag == 2
    assert estimate.lag_updates == 10
    assert estimate.transition_matrix.shape[0] == 2


def test_validation_helpers_on_simple_chain() -> None:
    p = np.array([[0.9, 0.1], [0.2, 0.8]])
    eigenvalues = np.linalg.eigvals(p)

    timescales = implied_timescales(eigenvalues, lag_time=2.0)
    gap = spectral_gap(eigenvalues)
    slow = leading_nontrivial_eigenvalues(eigenvalues, count=1)
    ck_error = chapman_kolmogorov_error(p, np.linalg.matrix_power(p, 2), steps=2)

    assert timescales.shape == (1,)
    assert np.allclose(abs(slow[0]), 0.7)
    assert np.allclose(gap, 0.3)
    assert ck_error == 0.0
