from __future__ import annotations

import numpy as np

from emergenz_knoten import SimulationConfig
from emergenz_knoten.markov import (
    chapman_kolmogorov_error,
    estimate_transfer_operator,
    implied_relaxation_rates,
    implied_timescales,
    lagged_pairs,
    leading_nontrivial_eigenvalues,
    simulate_augmented_features,
    spectral_gap,
    transition_count_matrix,
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


def test_augmented_simulation_reuses_canonical_config_validation() -> None:
    config = SimulationConfig(steps=10, burn_in=-1)

    try:
        simulate_augmented_features(config, seed=3)
    except ValueError as exc:
        assert "burn_in" in str(exc)
    else:
        raise AssertionError("expected canonical burn_in validation")


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
    assert estimate.relaxation_eigenvalues.shape == estimate.relaxation_rates.shape
    assert estimate.eigenvalues.size == estimate.relaxation_eigenvalues.size + 1
    assert estimate.transition_matrix.shape[0] == 2


def test_transition_count_matrix_rejects_too_few_states() -> None:
    labels = np.array([0, 2, 1, 2])

    try:
        transition_count_matrix(labels, n_states=2)
    except ValueError as exc:
        assert "maximum label" in str(exc)
    else:
        raise AssertionError("expected ValueError for too-small n_states")

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


def test_relaxation_eigenvalues_and_rates_are_aligned() -> None:
    transition = np.array([[0.9, 0.1], [0.2, 0.8]])

    eigenvalues, rates = implied_relaxation_rates(transition, lag_time=2.0)

    assert eigenvalues.shape == rates.shape == (1,)
    assert np.allclose(eigenvalues, [0.7])
    assert np.allclose(rates, [-np.log(0.7) / 2.0])


def test_periodic_mode_is_not_dropped_as_stationary() -> None:
    transition = np.array([[0.0, 1.0], [1.0, 0.0]])
    full_eigenvalues = np.linalg.eigvals(transition)

    eigenvalues, rates = implied_relaxation_rates(transition)
    timescales = implied_timescales(full_eigenvalues)

    assert eigenvalues.shape == rates.shape == (1,)
    assert np.allclose(eigenvalues, [-1.0])
    assert np.allclose(rates, [0.0])
    assert timescales.shape == (1,)
    assert np.isinf(timescales[0])
    assert np.allclose(leading_nontrivial_eigenvalues(full_eigenvalues, count=1), [-1.0])
    assert spectral_gap(full_eigenvalues) == 0.0


def test_reducible_chain_has_zero_spectral_gap() -> None:
    eigenvalues = np.linalg.eigvals(np.eye(2))

    assert np.allclose(leading_nontrivial_eigenvalues(eigenvalues, count=1), [1.0])
    assert spectral_gap(eigenvalues) == 0.0



def test_relaxation_helpers_reject_nonfinite_inputs() -> None:
    transition = np.array([[1.0, 0.0], [0.0, float("nan")]])

    for call, expected in [
        (lambda: implied_relaxation_rates(transition), "finite"),
        (
            lambda: implied_relaxation_rates(np.eye(2), lag_time=float("nan")),
            "lag_time",
        ),
    ]:
        try:
            call()
        except ValueError as exc:
            assert expected in str(exc)
        else:
            raise AssertionError(f"expected validation error for {expected}")
