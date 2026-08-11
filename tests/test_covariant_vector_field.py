from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten import (
    InertialVectorFieldDynamics,
    LocalVectorFieldExpansion,
    inertial_mode_energy_rate,
    inertial_vector_dimensionless_groups,
    inertial_vector_fourier_operator,
    inertial_vector_frequency_response,
    inertial_vector_mode,
    inertial_vector_mode_operator,
    isotropic_vector_energy_hessian,
    isotropic_vector_fourier_operator,
    reactive_pair_operator,
    vector_channel_denominator,
    vector_field_dimensionless_groups,
    vector_gradient_flow_rates,
)


def _field(**overrides: float) -> LocalVectorFieldExpansion:
    values = {
        "mass_coefficient": 1.0,
        "longitudinal_gradient_coefficient": 0.5,
        "transverse_gradient_coefficient": 1.5,
        "biharmonic_coefficient": 0.25,
        "cubic_saturation": 2.0,
        "mobility": 0.4,
    }
    values.update(overrides)
    return LocalVectorFieldExpansion(**values)


def test_fourier_operator_has_expected_helmholtz_rates() -> None:
    field = _field()
    wavevector = np.array([2.0, 0.0, 0.0])
    operator = isotropic_vector_fourier_operator(wavevector, field)
    longitudinal, transverse = vector_gradient_flow_rates(2.0, field)

    np.testing.assert_allclose(
        np.diag(operator),
        [longitudinal, transverse, transverse],
    )
    np.testing.assert_allclose(operator, operator.T)
    assert np.all(np.isreal(np.linalg.eigvalsh(operator)))


def test_fourier_operator_is_orthogonally_covariant() -> None:
    field = _field()
    wavevector = np.array([0.5, -1.2, 0.7])
    q, _ = np.linalg.qr(
        np.array(
            [
                [1.0, 2.0, 0.5],
                [-0.3, 0.7, 1.4],
                [0.8, -0.2, 0.9],
            ]
        )
    )

    original = isotropic_vector_fourier_operator(wavevector, field)
    transformed = isotropic_vector_fourier_operator(q @ wavevector, field)

    np.testing.assert_allclose(transformed, q @ original @ q.T, atol=1e-14)


def test_finite_wavenumber_threshold_is_dimensionless_ratio_minus_two() -> None:
    critical = _field(
        longitudinal_gradient_coefficient=-2.0,
        transverse_gradient_coefficient=0.5,
        biharmonic_coefficient=1.0,
    )
    unstable = _field(
        longitudinal_gradient_coefficient=-2.2,
        transverse_gradient_coefficient=0.5,
        biharmonic_coefficient=1.0,
    )

    critical_stability = critical.channel_stability("longitudinal")
    unstable_stability = unstable.channel_stability("longitudinal")
    groups = vector_field_dimensionless_groups(critical)

    assert groups.longitudinal_gradient_ratio == pytest.approx(-2.0)
    assert critical_stability.classification == "critical_finite_wavenumber"
    assert critical_stability.preferred_wavenumber == pytest.approx(1.0)
    assert unstable_stability.classification == "finite_wavenumber_instability"


def test_negative_gradient_without_biharmonic_term_is_uv_unstable() -> None:
    field = _field(
        longitudinal_gradient_coefficient=-0.1,
        biharmonic_coefficient=0.0,
    )

    stability = field.channel_stability("longitudinal")

    assert stability.classification == "ultraviolet_unstable"
    assert not stability.high_wavenumber_stable


def test_energy_rescaling_preserves_dimensionless_shape_groups() -> None:
    original = _field()
    factor = 7.0
    scaled = LocalVectorFieldExpansion(
        mass_coefficient=factor * original.mass_coefficient,
        longitudinal_gradient_coefficient=(
            factor * original.longitudinal_gradient_coefficient
        ),
        transverse_gradient_coefficient=(
            factor * original.transverse_gradient_coefficient
        ),
        biharmonic_coefficient=factor * original.biharmonic_coefficient,
        cubic_saturation=factor * original.cubic_saturation,
        mobility=original.mobility / factor,
    )

    left = vector_field_dimensionless_groups(original)
    right = vector_field_dimensionless_groups(scaled)

    assert right == left


def test_reactive_pair_is_an_explicit_second_state_with_complex_modes() -> None:
    operator = reactive_pair_operator(damping_rate=0.2, angular_frequency=0.7)
    eigenvalues = np.linalg.eigvals(operator)

    np.testing.assert_allclose(np.real(eigenvalues), -0.2)
    np.testing.assert_allclose(np.sort(np.abs(np.imag(eigenvalues))), [0.7, 0.7])


def test_inertial_mode_matches_exact_quadratic_roots() -> None:
    dynamics = InertialVectorFieldDynamics(energy=_field(), inertia=2.0, damping=0.4)
    operator = inertial_vector_mode_operator(0.0, dynamics, channel="longitudinal")
    mode = inertial_vector_mode(0.0, dynamics, channel="longitudinal")

    np.testing.assert_allclose(
        np.sort_complex(np.linalg.eigvals(operator)),
        np.sort_complex(np.asarray(mode.eigenvalues)),
    )
    assert mode.classification == "damped_oscillation"
    assert mode.asymptotically_stable
    assert mode.oscillatory


def test_reversible_limit_is_skew_in_the_energy_metric() -> None:
    dynamics = InertialVectorFieldDynamics(energy=_field(), inertia=2.0, damping=0.0)
    wavevector = np.array([0.7, -0.2, 0.4])
    operator = inertial_vector_fourier_operator(wavevector, dynamics)
    dim = wavevector.size
    hessian = isotropic_vector_energy_hessian(wavevector, dynamics.energy)
    energy_metric = np.block(
        [
            [hessian, np.zeros((dim, dim))],
            [np.zeros((dim, dim)), np.eye(dim) / dynamics.inertia],
        ]
    )

    np.testing.assert_allclose(
        operator.T @ energy_metric + energy_metric @ operator,
        0.0,
        atol=1e-14,
    )
    mode = inertial_vector_mode(0.0, dynamics, channel="transverse")
    assert mode.classification == "conservative_oscillation"
    assert mode.bounded
    assert not mode.asymptotically_stable


def test_inertial_fourier_operator_is_orthogonally_covariant() -> None:
    dynamics = InertialVectorFieldDynamics(energy=_field(), inertia=1.3, damping=0.2)
    wavevector = np.array([0.5, -1.2, 0.7])
    rotation, _ = np.linalg.qr(
        np.array([[1.0, 2.0, 0.5], [-0.3, 0.7, 1.4], [0.8, -0.2, 0.9]])
    )
    transform = np.block(
        [
            [rotation, np.zeros_like(rotation)],
            [np.zeros_like(rotation), rotation],
        ]
    )
    original = inertial_vector_fourier_operator(wavevector, dynamics)
    transformed = inertial_vector_fourier_operator(rotation @ wavevector, dynamics)
    np.testing.assert_allclose(
        transformed, transform @ original @ transform.T, atol=1e-14
    )


def test_reversible_coupling_does_not_stabilize_negative_energy_curvature() -> None:
    dynamics = InertialVectorFieldDynamics(
        energy=_field(mass_coefficient=-0.2), inertia=1.0, damping=2.0
    )
    mode = inertial_vector_mode(0.0, dynamics, channel="longitudinal")

    assert mode.classification == "restoring_instability"
    assert not mode.asymptotically_stable
    assert max(value.real for value in mode.eigenvalues) > 0.0


def test_frequency_response_and_energy_rate_follow_exact_equations() -> None:
    dynamics = InertialVectorFieldDynamics(energy=_field(), inertia=2.0, damping=0.5)
    response = inertial_vector_frequency_response(
        np.array([0.0, 1.0]), 0.0, dynamics, channel="transverse"
    )
    np.testing.assert_allclose(response[0], 1.0)
    np.testing.assert_allclose(response[1], 1.0 / (-1.0 - 0.5j))
    np.testing.assert_allclose(
        inertial_mode_energy_rate(np.array([0.0, 2.0]), dynamics),
        [0.0, -0.5],
    )


def test_inertial_dimensionless_groups_remove_common_energy_scale() -> None:
    original = InertialVectorFieldDynamics(energy=_field(), inertia=3.0, damping=0.7)
    factor = 5.0
    scaled = InertialVectorFieldDynamics(
        energy=LocalVectorFieldExpansion(
            mass_coefficient=factor * original.energy.mass_coefficient,
            longitudinal_gradient_coefficient=(
                factor * original.energy.longitudinal_gradient_coefficient
            ),
            transverse_gradient_coefficient=(
                factor * original.energy.transverse_gradient_coefficient
            ),
            biharmonic_coefficient=factor * original.energy.biharmonic_coefficient,
            cubic_saturation=factor * original.energy.cubic_saturation,
            mobility=original.energy.mobility,
        ),
        inertia=factor * original.inertia,
        damping=factor * original.damping,
    )
    left = inertial_vector_dimensionless_groups(original)
    right = inertial_vector_dimensionless_groups(scaled)
    np.testing.assert_allclose(
        [
            left.length_scale,
            left.amplitude_scale,
            left.inertial_time,
            left.damping_ratio,
            left.longitudinal_gradient_ratio,
            left.transverse_gradient_ratio,
        ],
        [
            right.length_scale,
            right.amplitude_scale,
            right.inertial_time,
            right.damping_ratio,
            right.longitudinal_gradient_ratio,
            right.transverse_gradient_ratio,
        ],
    )


@pytest.mark.parametrize(
    ("inertia", "damping"),
    [(-1.0, 0.1), (1.0, -0.1)],
)
def test_inertial_dynamics_rejects_nonphysical_kinetic_coefficients(
    inertia: float, damping: float
) -> None:
    with pytest.raises(ValueError):
        InertialVectorFieldDynamics(energy=_field(), inertia=inertia, damping=damping)


def test_inertial_mode_apis_reject_negative_wavenumber() -> None:
    dynamics = InertialVectorFieldDynamics(energy=_field(), inertia=1.0, damping=0.2)
    with pytest.raises(ValueError, match="wavenumber"):
        inertial_vector_mode_operator(-1.0, dynamics, channel="longitudinal")
    with pytest.raises(ValueError, match="wavenumber"):
        inertial_vector_frequency_response(1.0, -1.0, dynamics, channel="longitudinal")


def test_channel_denominator_validates_channel_and_wavenumber() -> None:
    field = _field()

    with pytest.raises(ValueError, match="channel"):
        vector_channel_denominator(1.0, field, channel="invalid")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="finite"):
        vector_channel_denominator(np.nan, field, channel="longitudinal")
