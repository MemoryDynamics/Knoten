from __future__ import annotations

import math

import numpy as np

from emergenz_knoten.spectral_memory_field import (
    SpectralMemoryConfig,
    SpectralMemoryState,
    advance_state,
    deposition_coefficients,
    explicit_history_coefficients,
    initialize_state,
    kernel_integral_coefficient,
    kernel_transfer,
    potential_gradient,
    update_rho,
    zero_mean_attractive_kernel,
)


def test_zero_mean_kernel_has_no_fourier_zero_mode() -> None:
    config = SpectralMemoryConfig(
        kernel=zero_mean_attractive_kernel(
            amplitude_att=26.0,
            sigma_att=3.0,
            sigma_comp=10.0,
        )
    )

    assert kernel_integral_coefficient(config) == 0.0
    assert abs(kernel_transfer(config)[0]) < 1e-14


def test_constant_potential_offset_does_not_change_force() -> None:
    config = SpectralMemoryConfig()
    state = initialize_state(config, x=17.0)

    baseline = potential_gradient(config, state.rho_coefficients, x=19.0)
    shifted = potential_gradient(
        config,
        state.rho_coefficients,
        x=19.0,
        zero_mode_offset=1e9,
    )

    assert shifted == baseline


def test_affine_update_matches_explicit_exponential_history() -> None:
    config = SpectralMemoryConfig(n_modes=12, lambda_value=0.17)
    initial = deposition_coefficients(config, 3.0)
    positions = [4.5, 9.0, 12.25, 39.5]
    iterative = initial
    for position in positions:
        iterative = update_rho(config, iterative, deposited_at=position)

    explicit = explicit_history_coefficients(
        config,
        positions,
        initial_coefficients=initial,
    )

    np.testing.assert_allclose(iterative, explicit, rtol=2e-15, atol=2e-15)


def test_memory_fibre_contracts_for_common_visible_path() -> None:
    config = SpectralMemoryConfig(n_modes=10, lambda_value=0.2)
    rho_a = deposition_coefficients(config, 2.0)
    rho_b = deposition_coefficients(config, 21.0)
    initial_distance = np.linalg.norm(rho_a - rho_b)

    for position in (8.0, 9.0, 14.0, 25.0):
        rho_a = update_rho(config, rho_a, deposited_at=position)
        rho_b = update_rho(config, rho_b, deposited_at=position)

    assert math.isclose(
        np.linalg.norm(rho_a - rho_b),
        (1.0 - config.lambda_value) ** 4 * initial_distance,
        rel_tol=2e-15,
        abs_tol=2e-15,
    )


def test_zero_mode_preserves_configured_memory_mass() -> None:
    config = SpectralMemoryConfig(
        box_length=50.0,
        n_modes=8,
        lambda_value=0.13,
        memory_mass=2.75,
    )
    rho = deposition_coefficients(config, 1.0)
    for position in (3.0, 7.0, 19.0, 31.0):
        rho = update_rho(config, rho, deposited_at=position)

    assert rho[0].imag == 0.0
    assert math.isclose(
        config.box_length * rho[0].real,
        config.memory_mass,
        rel_tol=0.0,
        abs_tol=5e-15,
    )


def test_eta_zero_is_exact_periodic_random_walk_update() -> None:
    config = SpectralMemoryConfig(box_length=80.0, n_modes=8)
    state = initialize_state(config, x=79.9)

    advanced = advance_state(
        state,
        config,
        epsilon=0.2,
        eta=0.0,
        noise=1.0,
    )

    assert math.isclose(advanced.x, 0.1, rel_tol=0.0, abs_tol=1e-14)
    assert advanced.update_index == 1


def test_spectral_force_matches_direct_gaussian_history_sum() -> None:
    config = SpectralMemoryConfig(
        box_length=200.0,
        n_modes=256,
        lambda_value=0.2,
        memory_mass=1.0,
        kernel=zero_mean_attractive_kernel(
            amplitude_att=5.0,
            sigma_att=3.0,
            sigma_comp=12.0,
        ),
    )
    positions = [91.0, 96.0, 103.0]
    weights = [0.2 * 0.8**2, 0.2 * 0.8, 0.2]
    initial = np.zeros(config.n_modes + 1, dtype=np.complex128)
    rho = explicit_history_coefficients(
        config,
        positions,
        initial_coefficients=initial,
    )
    x = 100.0

    direct = 0.0
    for position, weight in zip(positions, weights, strict=True):
        displacement = x - position
        for term in config.kernel:
            direct += (
                weight
                * config.memory_mass
                * term.amplitude
                * (-displacement / term.sigma**2)
                * math.exp(-0.5 * (displacement / term.sigma) ** 2)
            )

    spectral = potential_gradient(config, rho, x=x)
    assert math.isclose(spectral, direct, rel_tol=2e-8, abs_tol=2e-8)


def test_state_owns_immutable_coefficient_copy() -> None:
    coefficients = np.ones(5, dtype=np.complex128)
    state = SpectralMemoryState(x=0.0, rho_coefficients=coefficients)
    coefficients[0] = 12.0

    assert state.rho_coefficients[0] == 1.0
    assert not state.rho_coefficients.flags.writeable
