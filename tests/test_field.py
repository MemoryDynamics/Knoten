from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten import (
    RelaxationDiffusionField,
    gaussian_heat_time,
    gaussian_transfer,
    heat_transfer,
    low_wavenumber_matched_field,
    stationary_field_transfer,
)


def test_heat_flow_exactly_represents_gaussian_transfer() -> None:
    wavenumber = np.linspace(0.0, 4.0, 101)
    length = 3.0
    diffusivity = 0.7
    diffusion_time = gaussian_heat_time(
        length=length,
        diffusivity=diffusivity,
    )

    np.testing.assert_allclose(
        heat_transfer(
            wavenumber,
            diffusivity=diffusivity,
            diffusion_time=diffusion_time,
        ),
        gaussian_transfer(wavenumber, length=length),
        rtol=2e-14,
        atol=0.0,
    )


def test_relaxation_diffusion_field_matches_gaussian_at_low_wavenumber() -> None:
    length = 3.0
    field = low_wavenumber_matched_field(
        gaussian_length=length,
        decay_rate=2.0,
        coupling=4.0,
    )
    assert np.isclose(field.correlation_length, length / np.sqrt(2.0))
    assert np.isclose(field.zero_mode_gain, 2.0)

    step = 1.0e-5
    wavenumber = np.array([0.0, step])
    gaussian = gaussian_transfer(wavenumber, length=length)
    stationary = stationary_field_transfer(
        wavenumber,
        field,
        normalize_zero_mode=True,
    )
    gaussian_quadratic = (gaussian[1] - gaussian[0]) / step**2
    stationary_quadratic = (stationary[1] - stationary[0]) / step**2
    assert np.isclose(gaussian_quadratic, stationary_quadratic, rtol=1e-5)


def test_zero_coupling_field_cannot_be_zero_mode_normalized() -> None:
    field = RelaxationDiffusionField(
        diffusivity=1.0,
        decay_rate=1.0,
        coupling=0.0,
    )

    with pytest.raises(ValueError, match="zero coupling"):
        stationary_field_transfer(np.array([0.0, 1.0]), field, normalize_zero_mode=True)


def test_stationary_field_is_not_globally_a_gaussian_kernel() -> None:
    wavenumber = np.array([0.0, 1.0, 2.0])
    field = low_wavenumber_matched_field(gaussian_length=1.0)

    gaussian = gaussian_transfer(wavenumber, length=1.0)
    stationary = stationary_field_transfer(
        wavenumber,
        field,
        normalize_zero_mode=True,
    )

    assert stationary[0] == gaussian[0] == 1.0
    assert not np.allclose(stationary[1:], gaussian[1:])
