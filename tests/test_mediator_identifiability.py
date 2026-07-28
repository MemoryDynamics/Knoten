from __future__ import annotations

import numpy as np

from emergenz_knoten import (
    transfer_identifiability_metrics,
    vector_segment_power,
)


def test_vector_segment_power_removes_dc_and_finds_vector_sinusoid() -> None:
    samples = 64
    index = np.arange(samples)
    segments = np.zeros((2, samples, 2))
    segments[:, :, 0] = np.sin(2.0 * np.pi * 5.0 * index / samples)
    segments[:, :, 1] = 3.0

    angular_frequency, power = vector_segment_power(segments, time_step=0.5)

    assert angular_frequency.shape == (samples // 2 + 1,)
    np.testing.assert_array_equal(power[:, 0], 0.0)
    assert np.argmax(power[0]) == 5
    np.testing.assert_allclose(power[0], power[1])


def test_identical_transfer_functions_have_zero_identifiability() -> None:
    power = np.ones((2, 9))
    power[:, 0] = 0.0
    response = np.linspace(1.0, 0.1, 9).astype(complex)

    metrics = transfer_identifiability_metrics(
        power,
        response,
        response,
        minimum_frequency_contrast=0.25,
    )

    np.testing.assert_array_equal(metrics["weighted_contrast"], 0.0)
    np.testing.assert_array_equal(
        metrics["distinguishable_power_fraction"], 0.0
    )
    assert metrics["pooled_weighted_contrast"] == 0.0


def test_power_in_a_separated_bin_is_counted_as_distinguishable() -> None:
    power = np.zeros((2, 5))
    power[:, 2] = 1.0
    first = np.ones(5, dtype=complex)
    second = np.ones(5, dtype=complex)
    second[2] = -1.0

    metrics = transfer_identifiability_metrics(
        power,
        first,
        second,
        minimum_frequency_contrast=0.25,
    )

    np.testing.assert_allclose(metrics["distinguishable_power_fraction"], 1.0)
    np.testing.assert_allclose(metrics["transmitted_power_fraction"], 1.0)
    assert metrics["pooled_weighted_contrast"] == 2.0
