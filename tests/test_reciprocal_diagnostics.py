from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten.reciprocal_diagnostics import (
    fit_isotropic_relative_mode,
    relative_mode_phase_coherence,
)


def _trace(matrix: np.ndarray, *, samples: int = 300) -> tuple[np.ndarray, np.ndarray]:
    state = np.empty((samples, 4, 2), dtype=float)
    state[0] = np.array(
        [
            [1.0, 0.2],
            [-0.3, 0.8],
            [0.4, -0.7],
            [0.9, 0.5],
        ]
    )
    for index in range(1, samples):
        state[index] = state[index - 1] @ matrix.T
    return state[:, :, 0], state[:, :, 1]


def test_fit_recovers_stable_complex_transition() -> None:
    matrix = np.array([[0.96, -0.12], [0.12, 0.96]])
    positions, centers = _trace(matrix)

    fitted = fit_isotropic_relative_mode(positions, centers)

    np.testing.assert_allclose(fitted.transition, matrix, atol=1e-12)
    assert fitted.is_complex
    assert fitted.is_stable
    assert fitted.angular_frequency == pytest.approx(np.arctan2(0.12, 0.96))
    assert fitted.damping_rate > 0.0
    assert fitted.residual_ratio < 1e-12
    assert relative_mode_phase_coherence(positions, centers, fitted) == pytest.approx(
        1.0
    )


def test_fit_recovers_complex_transition_around_coordinate_specific_equilibria() -> (
    None
):
    matrix = np.array([[0.96, -0.12], [0.12, 0.96]])
    samples = 500
    equilibria = np.array(
        [
            [5.0, 5.0],
            [0.0, 0.0],
            [-2.0, -2.0],
        ]
    )
    state = np.empty((samples, 3, 2), dtype=float)
    state[0] = equilibria + np.array(
        [
            [0.2, -0.1],
            [0.3, 0.4],
            [-0.4, 0.2],
        ]
    )
    for index in range(1, samples):
        state[index] = equilibria + (state[index - 1] - equilibria) @ matrix.T

    fitted = fit_isotropic_relative_mode(state[:, :, 0], state[:, :, 1])

    np.testing.assert_allclose(fitted.transition, matrix, atol=1e-12)
    np.testing.assert_allclose(
        fitted.intercept,
        equilibria - equilibria @ matrix.T,
        atol=1e-12,
    )
    assert fitted.is_complex
    assert fitted.residual_ratio < 1e-12
    assert relative_mode_phase_coherence(
        state[:, :, 0], state[:, :, 1], fitted
    ) == pytest.approx(1.0)


def test_fit_recovers_real_transition_and_lag_power() -> None:
    matrix = np.array([[0.8, 0.1], [0.0, 0.95]])
    positions, centers = _trace(matrix)

    fitted = fit_isotropic_relative_mode(positions, centers, lag=2)

    np.testing.assert_allclose(fitted.transition, matrix @ matrix, atol=1e-12)
    assert not fitted.is_complex
    assert fitted.is_stable


def test_fit_rejects_incompatible_traces() -> None:
    with pytest.raises(ValueError, match="shape"):
        fit_isotropic_relative_mode(np.zeros((10, 2)), np.zeros((10, 3)))
