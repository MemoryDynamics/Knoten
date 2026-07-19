from __future__ import annotations

import math

import numpy as np
import pytest

from emergenz_knoten.markov.closure import (
    analytic_field_mode_multiplier,
    fit_ar_spectrum,
    leave_one_series_out_closure,
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
