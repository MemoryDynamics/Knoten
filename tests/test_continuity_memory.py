from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten.continuity_memory import (
    continuity_kernel_dimensionless_groups,
    continuity_kernel_selection,
    continuity_memory_mode,
    continuity_memory_mode_operator,
    continuity_oscillation_threshold,
    dimensionless_continuity_kernel_denominator,
    infer_continuity_kernel_groups_from_peak,
    memory_innovation_moments,
    reciprocal_continuity_kernel_transfer,
)


def test_stationary_memory_innovation_has_zero_monopole_and_canonical_dipole() -> None:
    result = memory_innovation_moments(
        memory_relaxation=0.1,
        target_mass=2.0,
        current_mass=2.0,
        current_centroid=np.array([1.0, -2.0]),
        deposited_position=np.array([4.0, 3.0]),
    )
    assert result.monopole == pytest.approx(0.0)
    np.testing.assert_allclose(result.first_moment, [0.6, 1.0])


def test_truncated_mass_residual_is_explicit_not_silently_normalized() -> None:
    result = memory_innovation_moments(
        memory_relaxation=0.01,
        target_mass=1.0,
        current_mass=0.997,
        current_centroid=np.zeros(1),
        deposited_position=np.ones(1),
    )
    assert result.monopole == pytest.approx(3.0e-5)


@pytest.mark.parametrize("wavenumber", [0.0, 0.2, 1.0, 3.0])
def test_mode_formula_matches_numerical_operator(wavenumber: float) -> None:
    kwargs = {
        "memory_relaxation": 0.1,
        "flux_relaxation": 0.3,
        "stiffness": 2.0,
    }
    mode = continuity_memory_mode(wavenumber, **kwargs)
    numerical = np.sort_complex(
        np.linalg.eigvals(continuity_memory_mode_operator(wavenumber, **kwargs))
    )
    np.testing.assert_allclose(np.sort_complex(mode.eigenvalues), numerical)


def test_continuity_mode_crosses_exact_oscillation_threshold() -> None:
    kwargs = {
        "memory_relaxation": 0.1,
        "flux_relaxation": 0.5,
        "stiffness": 4.0,
    }
    threshold = continuity_oscillation_threshold(**kwargs)
    assert threshold == pytest.approx(0.1)
    assert not continuity_memory_mode(0.99 * threshold, **kwargs).oscillatory
    above = continuity_memory_mode(1.01 * threshold, **kwargs)
    assert above.oscillatory
    assert above.asymptotically_stable


def test_zero_stiffness_is_first_order_negative_control() -> None:
    kwargs = {
        "memory_relaxation": 0.1,
        "flux_relaxation": 0.5,
        "stiffness": 0.0,
    }
    assert np.isinf(continuity_oscillation_threshold(**kwargs))
    mode = continuity_memory_mode(10.0, **kwargs)
    assert mode.classification == "stable_real"
    np.testing.assert_allclose(np.sort_complex(mode.eigenvalues), [-0.5, -0.1])


def test_negative_stiffness_exposes_instability() -> None:
    mode = continuity_memory_mode(
        1.0,
        memory_relaxation=0.1,
        flux_relaxation=0.2,
        stiffness=-1.0,
    )
    assert mode.classification == "unstable"


@pytest.mark.parametrize(
    ("argument", "value"),
    [("memory_relaxation", -0.1), ("flux_relaxation", -0.1)],
)
def test_invalid_relaxation_is_rejected(argument: str, value: float) -> None:
    kwargs = {
        "memory_relaxation": 0.1,
        "flux_relaxation": 0.2,
        "stiffness": 1.0,
    }
    kwargs[argument] = value
    with pytest.raises(ValueError):
        continuity_memory_mode(1.0, **kwargs)


def test_dynamic_kernel_reduces_to_three_dimensionless_shape_groups() -> None:
    groups = continuity_kernel_dimensionless_groups(
        memory_relaxation=np.sqrt(0.3),
        flux_relaxation=np.sqrt(0.3),
        local_stiffness=1.0,
        gradient_stiffness=-1.9,
        biharmonic_stiffness=1.0,
    )
    assert groups.length_scale == pytest.approx(1.0)
    assert groups.denominator_scale == pytest.approx(1.0)
    assert groups.flux_relaxation_ratio == pytest.approx(1.0)
    assert groups.spectral_shape == pytest.approx(-1.9)
    assert groups.memory_loading == pytest.approx(0.3)


def test_dimensionless_denominator_collapses_rescaled_coefficients() -> None:
    parameters = {
        "memory_relaxation": 0.2,
        "flux_relaxation": 0.5,
        "local_stiffness": 4.0,
        "gradient_stiffness": -3.8,
        "biharmonic_stiffness": 0.25,
    }
    groups = continuity_kernel_dimensionless_groups(**parameters)
    u = np.linspace(0.0, 3.0, 31)
    k = u / groups.length_scale
    k2 = np.square(k)
    dimensional = (
        parameters["memory_relaxation"] * parameters["flux_relaxation"]
        + parameters["local_stiffness"] * k2
        + parameters["gradient_stiffness"] * k2**2
        + parameters["biharmonic_stiffness"] * k2**3
    )
    collapsed = dimensionless_continuity_kernel_denominator(
        u,
        spectral_shape=groups.spectral_shape,
        memory_loading=groups.memory_loading,
    )
    np.testing.assert_allclose(dimensional / groups.denominator_scale, collapsed)


def test_gradient_channel_selects_scale_without_target_wavenumber() -> None:
    selection = continuity_kernel_selection(
        spectral_shape=-1.9,
        memory_loading=0.3,
        flux_relaxation_ratio=1.0,
    )
    assert selection.classification == "stable_selected_oscillatory_mode"
    assert selection.constitutive_energy_positive
    assert selection.statically_stable
    u = np.linspace(0.0, 3.0, 20001)
    transfer = np.square(u) / dimensionless_continuity_kernel_denominator(
        u,
        spectral_shape=-1.9,
        memory_loading=0.3,
    )
    numerical_peak = float(u[int(np.argmax(transfer))])
    assert selection.selected_scaled_wavenumber == pytest.approx(
        numerical_peak, abs=2.0e-4
    )


def test_common_energy_uses_squared_coupling_and_gradient_zero_mode() -> None:
    parameters = {
        "memory_relaxation": np.sqrt(0.3),
        "flux_relaxation": np.sqrt(0.3),
        "local_stiffness": 1.0,
        "gradient_stiffness": -1.9,
        "biharmonic_stiffness": 1.0,
    }
    k = np.array([0.0, 0.5, 1.0])
    positive = reciprocal_continuity_kernel_transfer(k, coupling=2.0, **parameters)
    negative = reciprocal_continuity_kernel_transfer(k, coupling=-2.0, **parameters)
    np.testing.assert_allclose(positive, negative)
    assert positive[0] == pytest.approx(0.0)
    direct = reciprocal_continuity_kernel_transfer(
        k, coupling=2.0, gradient_coupling=False, **parameters
    )
    assert direct[0] > 0.0


def test_indefinite_constitutive_branch_is_not_misreported_as_emergent_energy() -> None:
    selection = continuity_kernel_selection(
        spectral_shape=-2.2,
        memory_loading=0.4,
        flux_relaxation_ratio=1.0,
    )
    assert selection.statically_stable
    assert not selection.constitutive_energy_positive
    assert selection.classification == "stable_response_with_indefinite_constitutive_energy"


def test_peak_position_and_gain_free_curvature_recover_shape_groups() -> None:
    selection = continuity_kernel_selection(
        spectral_shape=-1.9,
        memory_loading=0.3,
        flux_relaxation_ratio=1.0,
    )
    y_peak = selection.selected_scaled_wavenumber**2
    denominator = 0.3 + y_peak - 1.9 * y_peak**2 + y_peak**3
    curvature = -(-3.8 + 6.0 * y_peak) / denominator
    inferred = infer_continuity_kernel_groups_from_peak(
        selected_scaled_wavenumber=selection.selected_scaled_wavenumber,
        log_transfer_curvature_y=curvature,
    )
    assert inferred.spectral_shape == pytest.approx(-1.9)
    assert inferred.memory_loading == pytest.approx(0.3)


def test_peak_inference_rejects_non_peak_curvature() -> None:
    with pytest.raises(ValueError):
        infer_continuity_kernel_groups_from_peak(
            selected_scaled_wavenumber=1.0,
            log_transfer_curvature_y=0.1,
        )
