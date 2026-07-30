from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from emergenz_knoten.active_scalar_field import (
    ActiveScalarFieldConfig,
    scalar_field_linear_rate,
    scalar_field_preferred_wavenumber,
    simulate_active_scalar_delta_field,
    spectral_delta_coefficients,
)


def test_configuration_rejects_under_dealiased_cubic_grid() -> None:
    with pytest.raises(ValueError, match="dealias_fraction"):
        ActiveScalarFieldConfig(dealias_fraction=0.4)


def test_periodic_delta_has_unit_integral() -> None:
    config = ActiveScalarFieldConfig(grid_points=64, steps=1)
    coefficients = spectral_delta_coefficients(0.37, config)
    field = np.fft.ifft(coefficients).real
    dx = config.domain_length / config.grid_points

    assert np.sum(field) * dx == pytest.approx(1.0)


def test_source_off_zero_initial_field_remains_exactly_zero() -> None:
    config = ActiveScalarFieldConfig(
        grid_points=64,
        steps=20,
        sample_every=2,
        source_enabled=False,
        epsilon=0.0,
    )
    trace = simulate_active_scalar_delta_field(config)

    np.testing.assert_array_equal(trace.field_rms, 0.0)
    np.testing.assert_array_equal(trace.final_coefficients, 0.0)
    assert trace.stop_reason == "completed"


def test_linear_etd_step_matches_constant_source_solution() -> None:
    config = ActiveScalarFieldConfig(
        grid_points=64,
        time_step=0.2,
        steps=1,
        sample_every=1,
        gradient_coefficient=0.5,
        biharmonic_coefficient=0.125,
        cubic_saturation=0.0,
        source_strength=0.1,
        eta=0.0,
        epsilon=0.0,
    )
    position = 0.31 * config.domain_length
    trace = simulate_active_scalar_delta_field(
        config,
        initial_position=position,
    )
    source = config.source_strength * spectral_delta_coefficients(position, config)
    rate = scalar_field_linear_rate(config)
    expected = source * np.expm1(config.time_step * rate) / rate
    mode_number = np.fft.fftfreq(config.grid_points) * config.grid_points
    expected[np.abs(mode_number) >= config.grid_points / 4] = 0.0
    expected[config.grid_points // 2] = 0.0

    np.testing.assert_allclose(trace.final_coefficients, expected, atol=1.0e-13)


def test_active_cubic_saturation_bounds_linear_instability() -> None:
    base = ActiveScalarFieldConfig(
        grid_points=64,
        domain_length=8.0 * np.pi,
        time_step=0.05,
        steps=2400,
        sample_every=20,
        gradient_coefficient=-2.2,
        biharmonic_coefficient=1.0,
        source_strength=0.02,
        eta=0.0,
        epsilon=0.0,
        amplitude_stop=1.0e3,
    )
    saturated = simulate_active_scalar_delta_field(base)
    unsaturated = simulate_active_scalar_delta_field(
        replace(base, cubic_saturation=0.0)
    )

    assert saturated.stop_reason == "completed"
    assert np.max(saturated.field_max_abs[-10:]) < 5.0
    assert unsaturated.field_max_abs[-1] > 10.0 * saturated.field_max_abs[-1]
    assert scalar_field_preferred_wavenumber(base) == pytest.approx(np.sqrt(1.1))
    np.testing.assert_allclose(
        saturated.final_coefficients[1 : base.grid_points // 2],
        np.conj(saturated.final_coefficients[-1 : base.grid_points // 2 : -1]),
        atol=1.0e-12,
    )
