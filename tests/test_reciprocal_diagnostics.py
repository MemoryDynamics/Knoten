from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten.reciprocal_diagnostics import (
    correlated_pair_noise,
    fit_isotropic_relative_mode,
    fit_panel_delay_mode,
    fit_panel_hankel_audit,
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


def test_correlated_pair_noise_preserves_marginals_and_controls_relative_noise() -> (
    None
):
    rng = np.random.default_rng(20260804)
    common = rng.standard_normal((100_000, 3))
    relative = rng.standard_normal((100_000, 3))

    for rho in (0.0, 0.9, 0.99):
        first, second = correlated_pair_noise(common, relative, rho)

        np.testing.assert_allclose(
            0.5 * (first - second),
            np.sqrt(0.5 * (1.0 - rho)) * relative,
            atol=1e-14,
        )
        assert np.var(first) == pytest.approx(1.0, abs=0.015)
        assert np.var(second) == pytest.approx(1.0, abs=0.015)
        assert np.corrcoef(first.ravel(), second.ravel())[0, 1] == pytest.approx(
            rho, abs=0.015
        )


def test_delay_fit_recovers_hidden_scalar_oscillator_at_depth_two() -> None:
    radius = 0.985
    angle = 0.2
    first_coefficient = 2.0 * radius * np.cos(angle)
    second_coefficient = -(radius**2)
    values = np.empty((800, 4, 1), dtype=float)
    values[0, :, 0] = [1.0, -0.4, 0.7, -1.2]
    values[1, :, 0] = [0.2, 0.8, -0.6, -0.3]
    for index in range(2, values.shape[0]):
        values[index] = (
            first_coefficient * values[index - 1]
            + second_coefficient * values[index - 2]
        )

    depth_one = fit_panel_delay_mode(values, delay_depth=1)
    depth_two = fit_panel_delay_mode(values, delay_depth=2)

    assert not np.any(np.abs(depth_one.eigenvalues.imag) > 1e-8)
    expected = radius * np.exp(1j * np.array([-angle, angle]))
    np.testing.assert_allclose(
        np.sort_complex(depth_two.eigenvalues),
        np.sort_complex(expected),
        atol=1e-10,
    )
    assert depth_one.test_transitions == depth_two.test_transitions
    assert depth_two.test_residual_ratio < 1e-8


def test_full_ambient_fit_detects_rotation_hidden_by_isotropic_panels() -> None:
    radius = 0.98
    angle = 0.15
    matrix = radius * np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )
    state = np.empty((500, 2), dtype=float)
    state[0] = [1.0, 0.2]
    for index in range(1, state.shape[0]):
        state[index] = matrix @ state[index - 1]

    isotropic_panels = fit_panel_delay_mode(state[:, :, None], delay_depth=1)
    ambient = fit_panel_delay_mode(state[:, None, :], delay_depth=1)

    assert not np.any(np.abs(isotropic_panels.eigenvalues.imag) > 1e-8)
    np.testing.assert_allclose(
        np.sort_complex(ambient.eigenvalues),
        np.sort_complex(np.linalg.eigvals(matrix)),
        atol=1e-10,
    )
    assert ambient.stable_complex_eigenvalues.size == 2
    assert ambient.test_residual_ratio < 1e-8


def test_hankel_audit_uses_common_target_windows_and_recovers_ar2_mode() -> None:
    radius = 0.985
    angle = 0.2
    values = np.empty((900, 4, 1), dtype=float)
    values[0, :, 0] = [1.0, -0.4, 0.7, -1.2]
    values[1, :, 0] = [0.2, 0.8, -0.6, -0.3]
    for index in range(2, values.shape[0]):
        values[index] = (
            2.0 * radius * np.cos(angle) * values[index - 1]
            - radius**2 * values[index - 2]
        )

    shallow = fit_panel_hankel_audit(
        values,
        delay_depth=2,
        common_max_depth=40,
        retained_ranks=(2,),
    )
    deep = fit_panel_hankel_audit(
        values,
        delay_depth=40,
        common_max_depth=40,
        retained_ranks=(2,),
    )

    assert shallow.train_transitions == deep.train_transitions
    assert shallow.test_transitions == deep.test_transitions
    expected = radius * np.exp(1j * np.array([-angle, angle]))
    for audit in (shallow, deep):
        np.testing.assert_allclose(
            np.sort_complex(audit.rank_fits[0].eigenvalues),
            np.sort_complex(expected),
            atol=1e-9,
        )
        assert audit.rank_fits[0].test_residual_ratio < 1e-8


def test_hankel_audit_rejects_rank_beyond_data_support() -> None:
    rng = np.random.default_rng(8)
    values = rng.standard_normal((80, 2, 1))

    with pytest.raises(ValueError, match="exceeds numerical rank"):
        fit_panel_hankel_audit(
            values,
            delay_depth=10,
            common_max_depth=40,
            retained_ranks=(16,),
        )


def test_hankel_audit_standardized_scores_are_scale_invariant() -> None:
    rng = np.random.default_rng(20260804)
    values = rng.standard_normal((500, 3, 2))

    reference = fit_panel_hankel_audit(
        values,
        delay_depth=20,
        common_max_depth=40,
        retained_ranks=(2, 4, 8),
    )
    rescaled = fit_panel_hankel_audit(
        0.1 * values,
        delay_depth=20,
        common_max_depth=40,
        retained_ranks=(2, 4, 8),
    )

    np.testing.assert_allclose(reference.singular_values, rescaled.singular_values)
    assert reference.stable_rank == pytest.approx(rescaled.stable_rank)
    assert reference.entropy_rank == pytest.approx(rescaled.entropy_rank)
    for expected, actual in zip(reference.rank_fits, rescaled.rank_fits):
        assert expected.test_score_rmse == pytest.approx(actual.test_score_rmse)
        assert expected.test_persistence_rmse == pytest.approx(
            actual.test_persistence_rmse
        )
        assert expected.test_residual_ratio == pytest.approx(actual.test_residual_ratio)
        np.testing.assert_allclose(
            np.sort_complex(expected.eigenvalues),
            np.sort_complex(actual.eigenvalues),
        )


def test_fit_rejects_incompatible_traces() -> None:
    with pytest.raises(ValueError, match="shape"):
        fit_isotropic_relative_mode(np.zeros((10, 2)), np.zeros((10, 3)))
