from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten.balanced_memory import (
    balanced_hankel_spectrum,
    gaussian_memory_readout_rows,
    minimum_principal_cosine,
    observation_block_weights,
    passive_delay_observability,
    passive_delay_reachability,
    randomized_holdout_error,
    select_balanced_rank,
)


def _delay_matrix(n_memory: int, decay: float) -> np.ndarray:
    matrix = np.zeros((n_memory, n_memory))
    matrix[0, 0] = decay
    if n_memory > 1:
        matrix[1:, :-1] = np.eye(n_memory - 1)
    return matrix


def test_passive_delay_reachability_matches_dense_powers() -> None:
    n_memory = 5
    horizon = 7
    decay = 0.8
    gain = 0.2
    matrix = _delay_matrix(n_memory, decay)
    vector = gain * np.eye(n_memory)[:, 0]
    expected = np.column_stack(
        [np.linalg.matrix_power(matrix, step) @ vector for step in range(horizon)]
    )
    actual = passive_delay_reachability(
        n_memory, horizon, carrier_decay=decay, deposition_gain=gain
    )
    np.testing.assert_allclose(actual, expected)


def test_passive_delay_observability_matches_dense_propagation() -> None:
    decay = 0.7
    steps = np.array([0, 2, 5, 8])
    rows = np.arange(1.0, 21.0).reshape(4, 5)
    matrix = _delay_matrix(5, decay)
    expected = np.vstack(
        [row @ np.linalg.matrix_power(matrix, step) for row, step in zip(rows, steps)]
    )
    actual = passive_delay_observability(
        rows, steps, carrier_decay=decay, block_weighted=False
    )
    np.testing.assert_allclose(actual, expected)


def test_observation_block_weights_and_gaussian_rows() -> None:
    np.testing.assert_allclose(
        observation_block_weights(np.array([0, 2, 5])), [1.0, 2.0, 3.0]
    )
    probes = np.array([[0.0, 0.0], [1.0, 0.0]])
    memories = np.array(
        [
            [[0.0, 0.0], [1.0, 0.0]],
            [[0.0, 0.0], [1.0, 0.0]],
        ]
    )
    rows = gaussian_memory_readout_rows(
        probes, memories, np.array([0.6, 0.4]), kernel_sigma=1.0
    )
    np.testing.assert_allclose(rows[0], [0.6, 0.4 * np.exp(-0.5)])
    np.testing.assert_allclose(rows[1], [0.6 * np.exp(-0.5), 0.4])


def test_balanced_spectrum_uses_full_energy_and_selects_rank_one() -> None:
    observable = np.diag([3.0, 1.0, 0.1])
    reachable = np.eye(3)
    spectrum = balanced_hankel_spectrum(observable, reachable, max_modes=1)
    assert spectrum.singular_values[0] == pytest.approx(3.0)
    assert spectrum.total_hankel_energy == pytest.approx(10.01)
    assert spectrum.energy_fractions[0] == pytest.approx(9.0 / 10.01)
    assert spectrum.tail_energy_relative_se == 0.0
    assert (
        select_balanced_rank(spectrum, max_rank=1, minimum_gap=2.5, minimum_energy=0.89)
        == 1
    )


def test_principal_cosine_and_holdout_distinguish_correct_subspace() -> None:
    first = np.eye(3)[:, :2]
    same = first @ np.array([[0.0, 1.0], [1.0, 0.0]])
    tilted = np.eye(3)[:, 1:]
    assert minimum_principal_cosine(first, same) == pytest.approx(1.0)
    assert minimum_principal_cosine(first, tilted) == pytest.approx(0.0)

    observable = np.array([[2.0, 0.0], [0.0, 0.0]])
    reachable = np.eye(2)
    correct = np.array([[1.0], [0.0]])
    wrong = np.array([[0.0], [1.0]])
    assert randomized_holdout_error(observable, reachable, correct) < 1e-12
    assert randomized_holdout_error(observable, reachable, wrong) == pytest.approx(1.0)
