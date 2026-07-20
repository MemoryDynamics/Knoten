from __future__ import annotations

import math

import numpy as np
import pytest

from emergenz_knoten.markov.closure import (
    analytic_field_mode_multiplier,
    fit_ar_spectrum,
    leave_one_series_out_closure,
    mode_subspace_overlap,
)


def _scalar_ar_series(coefficient: float, seed: int, length: int = 4000) -> np.ndarray:
    rng = np.random.default_rng(seed)
    values = np.empty(length, dtype=float)
    values[0] = rng.normal()
    for index in range(1, length):
        values[index] = coefficient * values[index - 1] + rng.normal(scale=0.3)
    return values[:, None]


def test_closure_beats_persistence_and_shuffled_future() -> None:
    series = [_scalar_ar_series(0.45, seed) for seed in range(5)]
    scores = leave_one_series_out_closure(
        series,
        lag=1,
        shuffle_repeats=2,
        random_seed=9,
    )

    assert scores.ar_r2_median > 0.15
    assert scores.ar_minus_persistence > 0.3
    assert scores.ar_minus_shuffled > 0.15
    assert scores.closure_lift > 0.15


def test_lag_normalized_scalar_rate_is_stable() -> None:
    coefficient = 0.82
    series = [_scalar_ar_series(coefficient, seed) for seed in range(5)]
    lag_one = fit_ar_spectrum(series, lag=1, lag_updates=1)
    lag_two = fit_ar_spectrum(series, lag=2, lag_updates=2)
    expected = -math.log(coefficient)

    assert math.isclose(lag_one.rates_per_update[0], expected, rel_tol=0.04)
    assert math.isclose(lag_two.rates_per_update[0], expected, rel_tol=0.08)


def test_complex_rotation_frequency_is_recovered() -> None:
    radius = 0.98
    angle = 0.17
    matrix = radius * np.asarray(
        [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]
    )
    series: list[np.ndarray] = []
    for seed in range(5):
        rng = np.random.default_rng(seed)
        values = np.empty((5000, 2), dtype=float)
        values[0] = rng.normal(size=2)
        for index in range(1, values.shape[0]):
            values[index] = matrix @ values[index - 1] + rng.normal(
                scale=0.03,
                size=2,
            )
        series.append(values)

    spectrum = fit_ar_spectrum(series, lag=1, lag_updates=1)

    assert np.iscomplex(spectrum.eigenvalues[0])
    assert math.isclose(
        abs(spectrum.angular_frequencies_per_update[0]),
        angle,
        rel_tol=0.03,
    )
    assert math.isclose(spectrum.rates_per_update[0], -math.log(radius), rel_tol=0.1)


def test_feature_eigenvectors_are_physical_and_phase_normalized() -> None:
    series = [_scalar_ar_series(0.7, seed) for seed in range(3)]
    spectrum = fit_ar_spectrum(series, lag=1, lag_updates=1)

    assert spectrum.feature_eigenvectors.shape == (1, 1)
    assert spectrum.feature_eigenvectors[0, 0].real == pytest.approx(1.0)
    assert spectrum.feature_eigenvectors[0, 0].imag == pytest.approx(0.0)


def test_feature_eigenvectors_follow_physical_nonnormal_dynamics() -> None:
    dynamics = np.array([[0.82, 0.35], [0.0, 0.47]])
    rng = np.random.default_rng(44)
    values = np.empty((30_000, 2), dtype=float)
    values[0] = rng.normal(size=2)
    for index in range(1, len(values)):
        values[index] = dynamics @ values[index - 1] + rng.normal(
            scale=[0.03, 0.4],
            size=2,
        )

    spectrum = fit_ar_spectrum([values], lag=1, lag_updates=1, ridge=0.0)

    for eigenvalue, vector in zip(
        spectrum.eigenvalues,
        spectrum.feature_eigenvectors.T,
        strict=True,
    ):
        residual = np.linalg.norm(dynamics @ vector - eigenvalue * vector)
        assert residual < 0.02


def test_mode_subspace_overlap_handles_sign_phase_and_complex_pairs() -> None:
    real = np.array([1.0, 2.0, 0.0])
    assert mode_subspace_overlap(real, -real) == pytest.approx(1.0)

    complex_mode = np.array([1.0, 1j, 0.0])
    phase_rotated = np.exp(0.7j) * complex_mode
    conjugate = np.conjugate(complex_mode)
    assert mode_subspace_overlap(complex_mode, phase_rotated) == pytest.approx(1.0)
    assert mode_subspace_overlap(complex_mode, conjugate) == pytest.approx(1.0)
    assert mode_subspace_overlap(complex_mode, np.array([0.0, 0.0, 1.0])) == 0.0


def test_analytic_field_multiplier_combines_forgetting_and_diffusion() -> None:
    actual = analytic_field_mode_multiplier(0.01, 0.02, 0.5, 20)
    expected = ((1.0 - 0.01) * math.exp(-0.02 * 0.5**2)) ** 20

    assert math.isclose(actual, expected, rel_tol=1e-15)


def test_zero_ridge_uses_least_squares_for_singular_features() -> None:
    values = _scalar_ar_series(0.5, seed=3)
    duplicated = [np.column_stack((values, values))]

    spectrum = fit_ar_spectrum(
        duplicated,
        lag=1,
        lag_updates=1,
        ridge=0.0,
    )

    assert np.isfinite(spectrum.matrix).all()


def test_analytic_field_multiplier_rejects_nonfinite_diffusion() -> None:
    with pytest.raises(ValueError, match="invalid field-mode"):
        analytic_field_mode_multiplier(0.01, math.nan, 0.5, 20)


def test_closure_rejects_nonfinite_ridge() -> None:
    series = [_scalar_ar_series(0.5, seed) for seed in range(2)]

    with pytest.raises(ValueError, match="ridge"):
        leave_one_series_out_closure(series, lag=1, ridge=math.nan)
