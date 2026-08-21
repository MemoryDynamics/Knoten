import math

import numpy as np
import pytest

from emergenz_knoten.kernels import (
    double_gaussian_gradient,
    exponential_memory_weights,
)
from emergenz_knoten.rotating_wave import (
    continuum_rotating_wave_balance,
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


def test_fixed_gain_continuum_balance_matches_component_definition():
    parameters = {
        "radius": 0.87,
        "angular_frequency": 1.31,
        "eta_per_alpha": 13.0,
        "tail_extent": 7.0,
        "memory_mass": 1.2,
        "sigma_rep": 1.0,
        "sigma_att": 3.0,
        "amplitude_rep": 1.0,
        "amplitude_att": 3.5,
        "quadrature_order": 256,
        "quadrature_backend": "numpy",
    }
    balance = continuum_rotating_wave_balance(**parameters)
    component_parameters = dict(parameters)
    eta_rate = component_parameters.pop("eta_per_alpha")
    components = continuum_rotating_wave_components(**component_parameters)

    assert balance.components.radial == pytest.approx(components.radial, abs=3.0e-16)
    assert balance.components.tangential == pytest.approx(
        components.tangential,
        abs=3.0e-16,
    )
    assert balance.residual[0] == pytest.approx(components.radial, abs=3.0e-16)
    assert balance.residual[1] == pytest.approx(
        parameters["angular_frequency"] + eta_rate * components.tangential,
        abs=0.0,
    )
    assert balance.required_eta_per_alpha == pytest.approx(
        -parameters["angular_frequency"] / components.tangential,
        abs=0.0,
    )


def test_fixed_gain_continuum_analytic_jacobian_matches_centered_difference():
    parameters = {
        "radius": 0.91,
        "angular_frequency": 1.43,
        "eta_per_alpha": 15.0,
        "tail_extent": 8.0,
        "memory_mass": 1.0,
        "sigma_rep": 1.0,
        "sigma_att": 3.0,
        "amplitude_rep": 1.0,
        "amplitude_att": 3.5,
        "quadrature_order": 256,
        "quadrature_backend": "numpy",
    }
    analytic = np.asarray(
        continuum_rotating_wave_balance(**parameters).jacobian,
        dtype=float,
    )
    centered = np.empty((2, 2), dtype=float)
    for column, name in enumerate(("radius", "angular_frequency")):
        step = 2.0e-6
        lower = dict(parameters)
        upper = dict(parameters)
        lower[name] -= step
        upper[name] += step
        lower_residual = np.asarray(
            continuum_rotating_wave_balance(**lower).residual,
            dtype=float,
        )
        upper_residual = np.asarray(
            continuum_rotating_wave_balance(**upper).residual,
            dtype=float,
        )
        centered[:, column] = (upper_residual - lower_residual) / (2.0 * step)

    assert analytic == pytest.approx(centered, rel=3.0e-9, abs=3.0e-10)


def test_independent_continuum_quadrature_backends_agree():
    parameters = {
        "radius": 1.07,
        "angular_frequency": 0.93,
        "eta_per_alpha": 11.0,
        "tail_extent": 6.0,
        "memory_mass": 1.0,
        "sigma_rep": 1.0,
        "sigma_att": 3.0,
        "amplitude_rep": 1.0,
        "amplitude_att": 4.0,
        "quadrature_order": 256,
    }
    numpy_balance = continuum_rotating_wave_balance(
        **parameters,
        quadrature_backend="numpy",
    )
    scipy_balance = continuum_rotating_wave_balance(
        **parameters,
        quadrature_backend="scipy",
    )

    assert numpy_balance.residual == pytest.approx(
        scipy_balance.residual,
        abs=4.0e-14,
    )
    assert np.asarray(numpy_balance.jacobian) == pytest.approx(
        np.asarray(scipy_balance.jacobian),
        abs=3.0e-13,
    )


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
