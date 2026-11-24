"""Conditional thermal spectral controls; no native trajectory or fit."""

import numpy as np
import pytest
from scipy.integrate import quad


THERMAL_STEP = 0.8
GAIN = 0.7


def _resolved_noise(theta):
    if theta == 0:
        return 2 * GAIN / THERMAL_STEP
    return GAIN * np.sin(theta) / np.tanh(THERMAL_STEP * theta / 2)


def test_resolved_one_lag_requires_thermal_colored_noise():
    theta = np.linspace(0.04, np.pi - 0.04, 80)
    spectrum = np.array([_resolved_noise(angle) for angle in theta])
    odd = GAIN * np.sin(theta)
    np.testing.assert_allclose(
        spectrum - odd,
        np.exp(-THERMAL_STEP * theta) * (spectrum + odd),
        atol=4e-16,
    )
    assert _resolved_noise(0) > 1
    assert abs(_resolved_noise(np.pi)) < 3e-16


@pytest.mark.parametrize("index", [40, 81])
def test_one_response_lag_does_not_make_the_thermal_noise_finite_lag(index):
    integral, _ = quad(
        _resolved_noise, 0, np.pi, weight="cos", wvar=index, epsabs=1e-12
    )
    predicted = -GAIN * (-1) ** index / (np.pi * np.tanh(THERMAL_STEP * np.pi / 2))
    assert integral / np.pi * index**2 == pytest.approx(predicted, rel=0.004)


def _aliased_correlation(times, band_index):
    theta = np.pi * (np.arange(128) + 0.5) / 128
    white = 1.35
    odd = np.sin(theta) - 0.3 * np.sin(2 * theta)
    high = 2 * np.pi * band_index + theta
    higher = 2 * np.pi * (band_index + 1) - theta
    q_high, q_higher = np.exp(-THERMAL_STEP * np.stack((high, higher)))
    scale = 1 - q_high * q_higher
    positive = (white + odd - q_higher * (white - odd)) / scale
    negative = (white - odd - q_high * (white + odd)) / scale
    assert min(positive.min(), negative.min()) > 0
    np.testing.assert_allclose(positive + q_higher * negative, white + odd)
    np.testing.assert_allclose(negative + q_high * positive, white - odd)

    def contributions(energy, weight, ratio):
        phase = np.exp(1j * np.asarray(times)[:, None] * energy)
        return weight * (phase + ratio * phase.conj())

    return (
        np.mean(
            contributions(high, positive, q_high)
            + contributions(higher, negative, q_higher),
            axis=1,
        )
        / 2
    )


def test_different_equilibrium_bands_have_same_fifo_data_but_different_intersample_data():
    times = np.arange(6)
    expected = np.array([1.35, 0.5j, -0.15j, 0, 0, 0])
    for band in (1, 2):
        np.testing.assert_allclose(
            _aliased_correlation(times, band), expected, rtol=0, atol=4e-15
        )
    first, second = (_aliased_correlation([0.5], band)[0] for band in (1, 2))
    assert abs(first - second) > 0.5


def test_positive_discrete_spectrum_can_still_violate_finite_thermal_cutoff():
    gain = 1.0
    white = 1 + 2**-8
    maximum_resolved_energy = 2 * np.pi
    ratio_at_peak = (white - gain) / (white + gain)
    assert ratio_at_peak > 0
    assert ratio_at_peak < np.exp(-THERMAL_STEP * maximum_resolved_energy)
