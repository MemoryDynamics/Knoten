from __future__ import annotations

import numpy as np

from emergenz_knoten import (
    critical_eta,
    frozen_hessian_stability,
    gaussian_kernel_curvature,
    local_scalar_memory_modes,
    scalar_dimensionless_groups,
    stationary_deposition_weight,
    stationary_memory_mass,
    two_scale_force_crossing_radius,
)


def test_stationary_memory_mass_parametrization() -> None:
    beta = stationary_deposition_weight(0.1, memory_mass=2.5)

    assert np.isclose(beta, 0.25)
    assert np.isclose(stationary_memory_mass(0.1, beta), 2.5)
    assert stationary_deposition_weight(0.1, memory_mass=0.0) == 0.0


def test_scalar_dimensionless_groups_use_memory_and_length_units() -> None:
    groups = scalar_dimensionless_groups(
        epsilon=1.0e-4,
        eta=0.15,
        lambda_value=0.01,
        memory_mass=1.0,
        local_curvature=26.0 / 9.0,
        length_scale=3.0,
    )

    assert groups.memory_time_updates == 100.0
    assert np.isclose(groups.restoring_per_update, 13.0 / 30.0)
    assert np.isclose(groups.restoring_per_memory_time, 130.0 / 3.0)
    assert np.isclose(groups.noise_per_update, 1.0e-4 / 3.0)
    assert np.isclose(
        groups.noise_diffusion_per_memory_time,
        1.0e-8 / (2.0 * 0.01 * 9.0),
    )


def test_critical_eta_uses_memory_mass_and_curvature() -> None:
    assert np.isclose(critical_eta(0.1), 0.11111111111111112)
    assert np.isclose(critical_eta(0.1, memory_mass=2.0), 0.05555555555555556)
    assert np.isclose(
        critical_eta(
            0.1, curvature=gaussian_kernel_curvature(amplitude=2.0, length=2.0)
        ),
        0.22222222222222224,
    )


def test_critical_eta_rejects_zero_memory_mass() -> None:
    try:
        critical_eta(0.1, memory_mass=0.0)
    except ValueError as exc:
        assert "memory_mass" in str(exc)
    else:
        raise AssertionError("expected critical_eta to reject M0=0")


def test_local_scalar_memory_modes_are_real() -> None:
    modes = local_scalar_memory_modes(0.1, g=1.2)

    assert modes[0] == 1.0
    assert np.isclose(modes[1], -0.18)
    assert all(isinstance(mode, float) for mode in modes)


def test_frozen_hessian_stability_classification() -> None:
    labels = frozen_hessian_stability(0.5, [-1.0, 1.0, 3.0, 5.0])

    assert labels == [
        "flat_or_anti_restoring",
        "monotone",
        "alternating",
        "unstable",
    ]


def test_two_scale_force_crossing_radius() -> None:
    radius = two_scale_force_crossing_radius(
        amplitude_rep=1.0,
        length_rep=1.0,
        amplitude_att=1.5,
        length_att=3.0,
    )

    assert radius is not None
    assert 1.8 <= radius <= 2.1
