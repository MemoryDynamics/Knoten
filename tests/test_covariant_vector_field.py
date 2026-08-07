from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten import (
    LocalVectorFieldExpansion,
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


def test_channel_denominator_validates_channel_and_wavenumber() -> None:
    field = _field()

    with pytest.raises(ValueError, match="channel"):
        vector_channel_denominator(1.0, field, channel="invalid")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="finite"):
        vector_channel_denominator(np.nan, field, channel="longitudinal")