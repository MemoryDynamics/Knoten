from __future__ import annotations

import math

import numpy as np
import pytest

from emergenz_knoten.relaxation_diffusion_memory import (
    RelaxationDiffusionMemoryOperators,
)
from emergenz_knoten.spectral_memory_field import (
    SpectralMemoryConfig,
    circular_center,
    periodic_displacement,
)
from emergenz_knoten.spectral_memory_trace import (
    direct_history_potential_gradient,
    low_mode_feature_groups,
    omitted_history_weight,
    simulate_spectral_memory_trace,
)


def test_fast_trace_matches_stepwise_runtime() -> None:
    config = SpectralMemoryConfig(n_modes=16, lambda_value=0.03)
    nu = 0.004
    epsilon = 2e-4
    eta = 0.12
    noise = np.random.default_rng(7).normal(size=300)
    trace = simulate_spectral_memory_trace(
        config,
        noise=noise,
        diffusion_per_update=nu,
        epsilon=epsilon,
        eta=eta,
        burn_in=100,
        sample_every=10,
        n_low_modes=3,
        history_length=300,
    )

    operators = RelaxationDiffusionMemoryOperators(
        config,
        diffusion_per_update=nu,
    )
    x = 0.5 * config.box_length
    rho = operators.deposition(x)
    expected_rows: list[list[float]] = []
    offsets = (0.0, 1.5, 3.0, 6.0)
    base = config.memory_mass / config.box_length
    for update_index, noise_value in enumerate(noise, start=1):
        gradient = operators.gradient(rho, x=x)
        x = (x + epsilon * noise_value - eta * gradient) % config.box_length
        rho = operators.update_rho(rho, deposited_at=x)
        if update_index > 100 and update_index % 10 == 0:
            center = circular_center(config, rho)
            assert center is not None
            row = [
                periodic_displacement(x, center, config.box_length),
                operators.gradient(rho, x=x),
            ]
            for mode in range(1, 4):
                aligned = (
                    rho[mode]
                    * np.exp(1j * operators.k[mode] * center)
                    / base
                )
                row.extend((aligned.real, aligned.imag))
            for offset in offsets:
                plus = base + 2.0 * np.real(
                    np.sum(
                        rho[1:]
                        * np.exp(
                            1j
                            * operators.k[1:]
                            * ((center + offset) % config.box_length)
                        )
                    )
                )
                minus = base + 2.0 * np.real(
                    np.sum(
                        rho[1:]
                        * np.exp(
                            1j
                            * operators.k[1:]
                            * ((center - offset) % config.box_length)
                        )
                    )
                )
                row.extend(
                    (0.5 * (plus + minus) / base, 0.5 * (plus - minus) / base)
                )
            expected_rows.append(row)

    np.testing.assert_allclose(trace.values, expected_rows, rtol=2e-12, atol=2e-12)
    np.testing.assert_allclose(
        trace.final_rho_coefficients,
        rho,
        rtol=2e-12,
        atol=2e-12,
    )
    assert math.isclose(trace.final_x, x, rel_tol=0.0, abs_tol=2e-12)


def test_recent_history_is_newest_first() -> None:
    config = SpectralMemoryConfig(n_modes=8)
    noise = np.arange(1.0, 11.0)
    trace = simulate_spectral_memory_trace(
        config,
        noise=noise,
        diffusion_per_update=0.0,
        epsilon=1e-3,
        eta=0.0,
        burn_in=1,
        sample_every=1,
        history_length=4,
    )
    positions = 0.5 * config.box_length + np.cumsum(1e-3 * noise)
    np.testing.assert_allclose(
        trace.recent_positions_newest_first,
        positions[-4:][::-1],
        rtol=0.0,
        atol=1e-13,
    )


def test_direct_real_history_recovers_spectral_gradient() -> None:
    config = SpectralMemoryConfig(n_modes=128, lambda_value=0.04)
    nu = 0.008
    noise = np.random.default_rng(11).normal(size=800)
    trace = simulate_spectral_memory_trace(
        config,
        noise=noise,
        diffusion_per_update=nu,
        epsilon=1e-4,
        eta=0.15,
        burn_in=100,
        sample_every=10,
        history_length=800,
    )
    operators = RelaxationDiffusionMemoryOperators(
        config,
        diffusion_per_update=nu,
    )
    spectral = operators.gradient(
        trace.final_rho_coefficients,
        x=trace.final_x + 1.25,
    )
    direct = direct_history_potential_gradient(
        config,
        evaluation_x=trace.final_x + 1.25,
        initial_x=0.5 * config.box_length,
        recent_positions_newest_first=trace.recent_positions_newest_first,
        total_updates=trace.update_count,
        diffusion_per_update=nu,
        periodic_images=3,
    )
    assert math.isclose(direct, spectral, rel_tol=2e-10, abs_tol=2e-10)


def test_groups_separate_modes_from_real_space_representation() -> None:
    groups = low_mode_feature_groups(3, (0.0, 1.0))

    assert groups["kinematic"] == [0, 1]
    assert groups["low_modes"] == list(range(8))
    assert groups["real_space"] == [0, 1, 8, 9, 10, 11]
    assert groups["combined"] == list(range(12))


def test_omitted_history_weight_is_exact_stationary_tail() -> None:
    assert math.isclose(omitted_history_weight(0.01, 2000), 0.99**2000)


def test_normalized_trace_rejects_zero_memory_mass() -> None:
    config = SpectralMemoryConfig(memory_mass=0.0)

    with pytest.raises(ValueError, match="positive memory_mass"):
        simulate_spectral_memory_trace(
            config,
            noise=np.ones(20),
            diffusion_per_update=0.0,
            epsilon=1e-4,
            eta=0.0,
            burn_in=1,
            sample_every=1,
        )


def test_direct_history_includes_initial_field_at_zero_updates() -> None:
    config = SpectralMemoryConfig(n_modes=128, lambda_value=0.04)
    operators = RelaxationDiffusionMemoryOperators(
        config,
        diffusion_per_update=0.0,
    )
    initial_x = 0.5 * config.box_length
    spectral = operators.gradient(
        operators.deposition(initial_x),
        x=initial_x + 1.25,
    )
    direct = direct_history_potential_gradient(
        config,
        evaluation_x=initial_x + 1.25,
        initial_x=initial_x,
        recent_positions_newest_first=(),
        total_updates=0,
        diffusion_per_update=0.0,
    )

    assert math.isclose(direct, spectral, rel_tol=2e-10, abs_tol=2e-10)
