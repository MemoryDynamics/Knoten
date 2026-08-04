import numpy as np
import pytest

from emergenz_knoten.reciprocal_modes import (
    reciprocal_complex_window_exists,
    reciprocal_scalar_memory_modes,
)


def test_zero_cross_gain_recovers_two_independent_scalar_modes() -> None:
    result = reciprocal_scalar_memory_modes(
        0.1,
        self_gain=0.4,
        cross_gain=0.0,
    )
    expected = sorted((1.0, 0.9 * 0.6))
    observed = sorted(value.real for value in result.relative_multipliers)
    assert np.allclose(observed, expected)
    assert not result.relative_is_complex


def test_weak_self_gain_allows_a_stable_complex_relative_mode() -> None:
    result = reciprocal_scalar_memory_modes(
        0.01,
        self_gain=0.0,
        cross_gain=0.02,
    )
    assert result.relative_is_complex
    assert result.relative_is_stable
    assert result.relative_angular_frequency > 0.0
    assert result.relative_damping_rate > 0.0
    assert np.isclose(
        np.prod(result.relative_multipliers).real,
        result.relative_determinant,
    )


def test_current_compact_node_gain_has_no_complex_cross_window() -> None:
    current_gain = 0.15 * (35.0 / 9.0 - 1.0)
    assert current_gain > 0.4
    assert not reciprocal_complex_window_exists(
        0.01,
        self_gain=current_gain,
    )


@pytest.mark.parametrize("lambda_value", [0.01, 0.1, 0.5])
def test_exact_window_threshold(lambda_value: float) -> None:
    threshold = lambda_value / (1.0 + lambda_value)
    assert reciprocal_complex_window_exists(
        lambda_value,
        self_gain=np.nextafter(threshold, -np.inf),
    )
    assert not reciprocal_complex_window_exists(
        lambda_value,
        self_gain=threshold,
    )


def test_lambda_one_has_no_nonreal_window() -> None:
    assert not reciprocal_complex_window_exists(1.0, self_gain=0.0)
    result = reciprocal_scalar_memory_modes(
        1.0,
        self_gain=0.0,
        cross_gain=0.5,
    )
    assert result.relative_discriminant == pytest.approx(0.0)
    assert not result.relative_is_complex


@pytest.mark.parametrize(
    ("lambda_value", "self_gain", "cross_gain"),
    [(0.0, 0.0, 0.0), (1.1, 0.0, 0.0), (0.1, np.nan, 0.0), (0.1, 0.0, np.inf)],
)
def test_invalid_parameters_are_rejected(
    lambda_value: float,
    self_gain: float,
    cross_gain: float,
) -> None:
    with pytest.raises(ValueError):
        reciprocal_scalar_memory_modes(
            lambda_value,
            self_gain=self_gain,
            cross_gain=cross_gain,
        )
