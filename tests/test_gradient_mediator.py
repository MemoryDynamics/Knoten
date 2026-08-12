from __future__ import annotations

import numpy as np
import pytest
from scipy.integrate import quad

from emergenz_knoten import (
    dimensionless_gradient_mediator_denominator,
    gradient_mediator_dimensionless_groups,
    gradient_mediator_homogeneous_energy_rate,
    gradient_mediator_mode_operator,
    gradient_mediator_selection,
    gradient_mediator_source_readout_multipliers,
    gradient_mediator_transfer,
    infer_gradient_mediator_groups_from_peak,
    radial_gradient_mediator_green_3d,
    radial_gradient_mediator_green_derivative_3d,
)


def _parameters() -> dict[str, float]:
    relaxation = float(np.sqrt(0.3))
    return {
        "memory_decay": relaxation,
        "conjugate_decay": relaxation,
        "local_stiffness": 1.0,
        "gradient_stiffness": -1.9,
        "biharmonic_stiffness": 1.0,
    }


def test_mode_operator_has_claimed_conjugate_field_polynomial() -> None:
    parameters = _parameters()
    k = 0.73
    operator = gradient_mediator_mode_operator(k, **parameters)
    eigenvalues = np.linalg.eigvals(operator)
    d_k = 1.0 - 1.9 * k**2 + k**4
    for root in eigenvalues:
        residual = (
            (root + parameters["memory_decay"])
            * (root + parameters["conjugate_decay"])
            + k * k * d_k
        )
        assert abs(residual) < 1.0e-13


def test_dimensionless_denominator_collapses_rescaled_coefficients() -> None:
    parameters = {
        "memory_decay": 0.2,
        "conjugate_decay": 0.5,
        "local_stiffness": 4.0,
        "gradient_stiffness": -3.8,
        "biharmonic_stiffness": 0.25,
    }
    groups = gradient_mediator_dimensionless_groups(**parameters)
    u = np.linspace(0.0, 3.0, 31)
    k = u / groups.length_scale
    k2 = np.square(k)
    dimensional = (
        parameters["memory_decay"] * parameters["conjugate_decay"]
        + parameters["local_stiffness"] * k2
        + parameters["gradient_stiffness"] * k2**2
        + parameters["biharmonic_stiffness"] * k2**3
    )
    collapsed = dimensionless_gradient_mediator_denominator(
        u, spectral_shape=groups.spectral_shape, memory_loading=groups.memory_loading
    )
    np.testing.assert_allclose(dimensional / groups.denominator_scale, collapsed)
    swapped = gradient_mediator_dimensionless_groups(
        memory_decay=parameters["conjugate_decay"],
        conjugate_decay=parameters["memory_decay"],
        local_stiffness=parameters["local_stiffness"],
        gradient_stiffness=parameters["gradient_stiffness"],
        biharmonic_stiffness=parameters["biharmonic_stiffness"],
    )
    assert swapped == groups


def test_common_interaction_geometry_generates_squared_gain_and_zero_mode() -> None:
    parameters = _parameters()
    k = np.array([0.0, 0.5, 1.0])
    positive = gradient_mediator_transfer(k, coupling=2.0, **parameters)
    negative = gradient_mediator_transfer(k, coupling=-2.0, **parameters)
    np.testing.assert_allclose(positive, negative)
    assert positive[0] == pytest.approx(0.0)
    direct = gradient_mediator_transfer(
        k, coupling=2.0, coupling_geometry="direct_scalar", **parameters
    )
    assert direct[0].real > 0.0

    write, read = gradient_mediator_source_readout_multipliers(
        np.array([0.2, -0.7, 0.1]), coupling=-2.0
    )
    np.testing.assert_allclose(write, -2.0j * np.array([0.2, -0.7, 0.1]))
    np.testing.assert_allclose(read, write.conj())


def test_homogeneous_quadratic_energy_rate_matches_finite_difference() -> None:
    parameters = _parameters()
    k = 0.8
    state = np.array([0.4 + 0.2j, -0.3 + 0.1j])
    operator = gradient_mediator_mode_operator(k, **parameters)
    derivative = operator @ state
    restoring = 0.3 + k**2 - 1.9 * k**4 + k**6
    analytic_from_state = float(
        np.real(
            restoring * np.conj(state[0]) * derivative[0]
            + np.conj(state[1]) * derivative[1]
        )
    )
    expected = float(
        gradient_mediator_homogeneous_energy_rate(
            state[1],
            memory_decay=parameters["memory_decay"],
            conjugate_decay=parameters["conjugate_decay"],
        )
    )
    assert analytic_from_state == pytest.approx(expected, abs=1.0e-14)


def test_gradient_channel_selects_scale_without_target_wavenumber() -> None:
    selection = gradient_mediator_selection(
        spectral_shape=-1.9,
        memory_loading=0.3,
        decay_rate_ratio=1.0,
    )
    assert selection.classification == "stable_selected_oscillatory_mode"
    assert selection.constitutive_operator_positive
    u = np.linspace(0.0, 3.0, 20001)
    transfer = np.square(u) / dimensionless_gradient_mediator_denominator(
        u, spectral_shape=-1.9, memory_loading=0.3
    )
    assert selection.selected_scaled_wavenumber == pytest.approx(
        float(u[int(np.argmax(transfer))]), abs=2.0e-4
    )


def test_indefinite_constitutive_branch_is_reported_explicitly() -> None:
    selection = gradient_mediator_selection(
        spectral_shape=-2.2,
        memory_loading=0.4,
        decay_rate_ratio=1.0,
    )
    assert selection.statically_stable
    assert not selection.constitutive_operator_positive
    assert (
        selection.classification
        == "stable_total_operator_with_indefinite_constitutive_part"
    )


def test_peak_position_and_gain_free_curvature_recover_shape_groups() -> None:
    selection = gradient_mediator_selection(
        spectral_shape=-1.9, memory_loading=0.3, decay_rate_ratio=1.0
    )
    y_peak = selection.selected_scaled_wavenumber**2
    denominator = 0.3 + y_peak - 1.9 * y_peak**2 + y_peak**3
    curvature = -(-3.8 + 6.0 * y_peak) / denominator
    inferred = infer_gradient_mediator_groups_from_peak(
        selected_scaled_wavenumber=selection.selected_scaled_wavenumber,
        log_transfer_curvature_y=curvature,
    )
    assert inferred.spectral_shape == pytest.approx(-1.9)
    assert inferred.memory_loading == pytest.approx(0.3)


@pytest.mark.parametrize("radius", [0.2, 1.0, 4.0, 7.0, 10.0])
def test_exact_green_residues_match_infinite_fourier_quadrature(radius: float) -> None:
    exact = float(
        radial_gradient_mediator_green_3d(
            radius, spectral_shape=-1.9, memory_loading=0.3
        )
    )

    def transfer(k: float) -> float:
        return k * k / (0.3 + k * k - 1.9 * k**4 + k**6)

    integral = quad(
        lambda k: k * transfer(k),
        0.0,
        np.inf,
        weight="sin",
        wvar=radius,
        epsabs=1.0e-11,
        epsrel=1.0e-11,
        limit=500,
        limlst=500,
    )[0]
    numerical = integral / (2.0 * np.pi**2 * radius)
    assert exact == pytest.approx(numerical, abs=2.0e-11)


def test_exact_green_derivative_matches_centered_finite_difference() -> None:
    radii = np.array([1.0, 3.9, 7.0, 10.0])
    step = 1.0e-5
    plus = radial_gradient_mediator_green_3d(
        radii + step, spectral_shape=-1.9, memory_loading=0.3
    )
    minus = radial_gradient_mediator_green_3d(
        radii - step, spectral_shape=-1.9, memory_loading=0.3
    )
    exact = radial_gradient_mediator_green_derivative_3d(
        radii, spectral_shape=-1.9, memory_loading=0.3
    )
    np.testing.assert_allclose(exact, (plus - minus) / (2.0 * step), atol=2.0e-10)


def test_peak_inference_rejects_non_peak_curvature() -> None:
    with pytest.raises(ValueError):
        infer_gradient_mediator_groups_from_peak(
            selected_scaled_wavenumber=1.0,
            log_transfer_curvature_y=0.1,
        )
