import math

import numpy as np
import pytest

from emergenz_knoten.kernels import (
    double_gaussian_gradient,
    exponential_memory_weights,
)
from emergenz_knoten.rotating_wave import (
    continuum_rotating_wave_components,
    double_gaussian_force_crossing_radius,
    double_gaussian_gradient_factor,
    finite_h_rotating_wave_balance,
    finite_h_rotating_wave_components,
    finite_h_rotating_wave_residual,
)


def _rotation(angle):
    return np.array(
        [
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)],
        ]
    )


def test_finite_h_residual_matches_native_two_dimensional_update():
    radius = 1.3
    theta = 0.17
    alpha = 0.08
    horizon = 37
    memory_mass = 1.4
    eta = 0.21
    x = np.array([radius, 0.0])
    history = np.asarray([_rotation(-j * theta) @ x for j in range(horizon)])
    weights = exponential_memory_weights(alpha, horizon, memory_mass=memory_mass)

    gradient = double_gaussian_gradient(
        x,
        history,
        weights,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=8.0,
    )
    x_next = x - eta * gradient
    target = _rotation(theta) @ x
    native_error = complex(*(x_next - target)) / radius
    analytic_residual = finite_h_rotating_wave_residual(
        radius=radius,
        theta=theta,
        alpha=alpha,
        horizon=horizon,
        memory_mass=memory_mass,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=8.0,
        eta=eta,
    )

    assert native_error == pytest.approx(-analytic_residual, abs=2.0e-15)


def test_force_crossing_separates_recent_repulsion_from_outer_attraction():
    crossing = double_gaussian_force_crossing_radius(
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=8.0,
    )

    assert crossing is not None
    assert (
        double_gaussian_gradient_factor(
            0.5 * crossing,
            sigma_rep=1.0,
            sigma_att=3.0,
            amplitude_rep=1.0,
            amplitude_att=8.0,
        )
        < 0.0
    )
    assert (
        double_gaussian_gradient_factor(
            1.5 * crossing,
            sigma_rep=1.0,
            sigma_att=3.0,
            amplitude_rep=1.0,
            amplitude_att=8.0,
        )
        > 0.0
    )


def test_current_attractive_reference_has_no_force_crossing():
    radii = np.linspace(0.0, 20.0, 2001)
    factors = double_gaussian_gradient_factor(
        radii,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=35.0,
    )

    assert (
        double_gaussian_force_crossing_radius(
            sigma_rep=1.0,
            sigma_att=3.0,
            amplitude_rep=1.0,
            amplitude_att=35.0,
        )
        is None
    )
    assert np.all(factors > 0.0)


@pytest.mark.parametrize("period", [3, 4, 7, 12, 31])
def test_positive_kernel_complete_period_history_has_backward_tangential_sum(
    period,
):
    alpha = 0.03
    complete_periods = 4
    balance = finite_h_rotating_wave_balance(
        radius=1.2,
        theta=2.0 * math.pi / period,
        alpha=alpha,
        horizon=complete_periods * period + 1,
        memory_mass=1.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=35.0,
    )

    assert balance.components.radial > 0.0
    assert balance.components.tangential > 0.0
    assert not balance.admissible_positive_eta


def test_finite_sums_converge_to_registered_continuum_integrals():
    radius = 1.1
    omega = 0.8
    extent = 6.0
    continuum = continuum_rotating_wave_components(
        radius=radius,
        angular_frequency=omega,
        tail_extent=extent,
        memory_mass=1.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=8.0,
        quadrature_order=512,
    )
    alpha = 0.001
    horizon = math.ceil(extent / alpha)
    finite = finite_h_rotating_wave_components(
        radius=radius,
        theta=alpha * omega,
        alpha=alpha,
        horizon=horizon,
        memory_mass=1.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=8.0,
    )

    assert finite.radial == pytest.approx(continuum.radial, rel=4.0e-3)
    assert finite.tangential == pytest.approx(continuum.tangential, rel=4.0e-3)


def test_eta_compatibility_is_exact_elimination_of_two_residual_components():
    parameters = {
        "radius": 1.0,
        "theta": 0.11,
        "alpha": 0.02,
        "horizon": 300,
        "memory_mass": 1.0,
        "sigma_rep": 1.0,
        "sigma_att": 3.0,
        "amplitude_rep": 1.0,
        "amplitude_att": 7.5,
    }
    balance = finite_h_rotating_wave_balance(**parameters)
    radial_residual = finite_h_rotating_wave_residual(
        eta=balance.radial_eta, **parameters
    )

    assert radial_residual.real == pytest.approx(0.0, abs=2.0e-15)
    assert (
        math.sin(parameters["theta"])
        + balance.tangential_eta * balance.components.tangential
    ) == pytest.approx(0.0, abs=2.0e-15)
    expected = (
        balance.components.radial * math.sin(parameters["theta"])
        + (1.0 - math.cos(parameters["theta"])) * balance.components.tangential
    )
    assert balance.compatibility_residual == pytest.approx(expected, abs=0.0)
