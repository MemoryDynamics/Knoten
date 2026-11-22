"""Fixed linear homogeneous-block controls, not a native many-node run."""

import numpy as np
import pytest
from scipy.optimize import brentq
from scipy.special import roots_legendre


EPSILON = 0.8
SIGMA = 0.7
SCALAR_WIDTH = 0.4
CHI = 2 * np.sqrt(2 / np.pi) / (3 * EPSILON)
VECTOR_AGES = np.array([2 / 3, 1 / 3])


def _moments(k):
    mu, mu_weights = roots_legendre(32)
    radial_nodes, radial_weights = roots_legendre(64)
    r = 5 * (radial_nodes + 1)
    weights = 5 * radial_weights * np.sqrt(2 / np.pi) * r**2 * np.exp(-(r**2) / 2)
    phase = k * EPSILON * r[:, None] * mu
    odd = np.sum(weights * (np.sin(phase) @ (mu_weights * mu))) / 2
    response = np.sum(weights * r * (np.cos(phase) @ (mu_weights * mu**2)))
    return odd, response / (2 * EPSILON)


def _mode(k, scalar_gain, alignment=1.0):
    p = np.exp(-(EPSILON**2) * k**2 / 2)
    gain = alignment * np.exp(-(SIGMA**2) * k**2 / 2) / CHI
    b = scalar_gain * np.exp(-SCALAR_WIDTH * k**2)
    odd, response = _moments(k)
    matrix = np.zeros((3, 3), dtype=complex)
    matrix[0, 0] = p * (1 - k**2 * b)
    matrix[0, 1:] = -1j * p * k * gain * VECTOR_AGES
    matrix[1, 0] = -1j * (odd + k * response * b)
    matrix[1, 1:] = response * gain * VECTOR_AGES
    matrix[2, 1] = 1
    source = np.array([-p * k**2 * b, -1j * k * response * b, 0])
    return matrix, source


def test_gaussian_endpoint_write_supplies_the_zero_mode_susceptibility():
    odd0, response0 = _moments(0)
    assert odd0 == 0
    assert response0 == pytest.approx(CHI, rel=3e-15)
    k = 0.004
    odd, response = _moments(k)
    assert odd / k == pytest.approx(EPSILON**2 * CHI, rel=1e-5)
    assert (1 - response / CHI) / k**2 == pytest.approx(6 / 5 * EPSILON**2, rel=1e-5)


@pytest.mark.parametrize(("strength", "conclusion"), [(0.8, -1), (1.0, 0), (1.2, 1)])
def test_uniform_direction_is_critical_only_at_unit_loop_gain(strength, conclusion):
    block, _ = _mode(0, -(EPSILON**2) / 2, alignment=strength)
    roots = np.linalg.eigvals(block[1:, 1:])
    dominant = roots.real.max()
    if conclusion == 0:
        assert dominant == pytest.approx(1, abs=1e-14)
    else:
        assert (dominant - 1) * conclusion > 0


def test_two_age_current_gives_damped_longitudinal_waves_at_vector_threshold():
    k = 0.014
    block, _ = _mode(k, -(EPSILON**2) / 2)
    roots = np.linalg.eigvals(block)
    waves = roots[np.argsort(np.abs(roots - 1))[:2]]
    assert np.all(np.abs(waves) < 1)
    logs = np.log(waves)
    np.testing.assert_allclose(
        np.sort(logs.imag) / k, EPSILON * np.sqrt(3 / 8) * np.array([-1, 1]), rtol=4e-4
    )
    vector_width = SIGMA**2 / 2 + 6 / 5 * EPSILON**2
    damping = (13 / 24 * EPSILON**2 - vector_width) / (8 / 3)
    np.testing.assert_allclose(logs.real / k**2, damping, rtol=8e-4)


def test_at_old_scalar_criticality_static_pole_disappears_when_current_is_critical():
    b = -(EPSILON**2) / 2
    errors = []
    for k in (0.02, 0.01):
        gains = []
        for alignment in (0, 1):
            block, source = _mode(k, b, alignment)
            state = np.linalg.solve(np.eye(3) - block, source)
            gains.append(state[0].real)
        scalar, coupled = gains
        assert scalar > 1000
        assert coupled == pytest.approx(1, rel=4e-4)
        errors.append(1 - coupled)
    assert errors[0] / errors[1] == pytest.approx(4, rel=1e-3)


def test_cancelling_the_static_denominator_removes_nonzero_sound_speed():
    k = 0.012
    block, source = _mode(k, -(EPSILON**2))
    state = np.linalg.solve(np.eye(3) - block, source)
    assert abs(state[0]) > 1000  # static response restored in this fixed case
    roots = np.linalg.eigvals(block)
    close = roots[np.argsort(np.abs(roots - 1))[:2]]
    assert max(abs(close - 1)) / k < 0.03


@pytest.mark.parametrize("frequency_scale", [0, 0.3, 0.25 + 0.4j])
def test_reconstructed_potential_has_both_static_pole_and_acoustic_resolvent(
    frequency_scale,
):
    b = -(EPSILON**2) / 2
    coefficient = -b / (4 / 3 * frequency_scale**2 + EPSILON**2 + b)
    for k in (0.012, 0.006):
        matrix, source = _mode(k, b)
        z = np.exp(k * frequency_scale)
        density = np.linalg.solve(z * np.eye(3) - matrix, source)[0]
        reconstructed = density / k**2
        assert reconstructed * k**2 == pytest.approx(coefficient, rel=0.015)
        assert abs(density) < 3


def test_integrating_exact_linear_transport_recovers_longitudinal_potential_gradient():
    k = 0.17
    p = np.exp(-(EPSILON**2) * k**2 / 2)
    gain = np.exp(-(SIGMA**2) * k**2 / 2) / CHI
    b = -(EPSILON**2) / 2 * np.exp(-SCALAR_WIDTH * k**2)
    block, drive = _mode(k, -(EPSILON**2) / 2)
    state = np.zeros(3, dtype=complex)
    accumulated = 0j
    for tick in range(18):
        source = 0.3 * np.cos(tick / 3)
        step = gain * (VECTOR_AGES @ state[1:]) - 1j * k * b * (state[0] + source)
        flux = p * step - 1j * (1 - p) * state[0] / k
        accumulated += flux
        state = block @ state + source * drive
        assert accumulated == pytest.approx(1j * state[0] / k, abs=2e-15)


def test_compact_directional_source_can_supply_dipole_but_not_monopole_pole():
    b = -(EPSILON**2) / 2
    previous = None
    for k in (0.02, 0.01):
        p = np.exp(-(EPSILON**2) * k**2 / 2)
        gain = np.exp(-(SIGMA**2) * k**2 / 2) / CHI
        _, response = _moments(k)
        block, _ = _mode(k, b)
        source = gain * np.array([-1j * k * p, response, 0])
        density = np.linalg.solve(np.eye(3) - block, source)[0]
        assert k * density == pytest.approx(-1j / (CHI * (EPSILON**2 + b)), rel=4e-4)
        centered_source_density = np.linalg.solve(np.eye(3) - block, 1j * k * source)[0]
        assert centered_source_density == pytest.approx(
            1 / (CHI * (EPSILON**2 + b)), rel=4e-4
        )
        if previous is not None:
            assert density / previous == pytest.approx(2, rel=4e-4)
        previous = density


def test_stationary_native_step_is_quadratically_suppressed_against_reconstructed_field():
    k = 0.025
    b = -(EPSILON**2) / 2
    block, source = _mode(k, b)
    state = np.linalg.solve(np.eye(3) - block, source)
    gain = np.exp(-(SIGMA**2) * k**2 / 2) / CHI
    native = gain * (VECTOR_AGES @ state[1:]) - 1j * k * b * np.exp(
        -SCALAR_WIDTH * k**2
    ) * (1 + state[0])
    field = 1j * state[0] / k
    suppression = np.expm1(EPSILON**2 * k**2 / 2)
    assert abs(field) > 30
    assert abs(native) < 0.01
    assert native / field == pytest.approx(suppression, abs=1e-15)


def _field_feedback_matrix(k, gain):
    matrix, _ = _mode(k, -(EPSILON**2) / 2)
    p = np.exp(-(EPSILON**2) * k**2 / 2)
    _, response = _moments(k)
    matrix[:, 0] += (1j * gain / k) * np.array([-1j * k * p, response, 0])
    return matrix


@pytest.mark.parametrize("z", [1, 1.12, 1.02 + 0.14j])
def test_self_feedback_determinant_has_exact_signed_shift(z):
    k, gain = 0.06, 0.015
    reference, _ = _mode(k, -(EPSILON**2) / 2)
    closed = _field_feedback_matrix(k, gain)
    p = np.exp(-(EPSILON**2) * k**2 / 2)
    difference = np.linalg.det(z * np.eye(3) - closed) - np.linalg.det(
        z * np.eye(3) - reference
    )
    # The full 3x3 determinant carries one extra shift-state factor z.
    assert difference == pytest.approx(-gain * p * z**2, abs=2e-16)


def test_attractive_feedback_has_nonvanishing_growth_as_wavenumber_decreases():
    gain = 0.016

    def limiting_equation(z):
        ages = VECTOR_AGES @ np.array([1, 1 / z])
        return (z - 1) * (1 - ages / z) - gain

    predicted = brentq(limiting_equation, 1, 2)
    for k in (0.016, 0.008):
        roots = np.linalg.eigvals(_field_feedback_matrix(k, gain))
        growing = roots[np.argmax(roots.real)]
        assert growing.real > 1.1
        assert growing == pytest.approx(predicted, abs=4e-4)


def test_delayed_attraction_still_has_a_real_growing_root():
    k, gain, lag = 0.025, 0.009, 4

    def determinant(z):
        matrix = _field_feedback_matrix(k, gain * z**-lag)
        return np.linalg.det(z * np.eye(3) - matrix).real

    assert determinant(1) < 0 < determinant(2)
    assert brentq(determinant, 1, 2) > 1.05


def test_leading_jeans_threshold_changes_growth_to_oscillation():
    k = 0.013
    c = EPSILON**2 / 2
    for scaled_gain in (1.5 * c, 0.5 * c):
        roots = np.linalg.eigvals(_field_feedback_matrix(k, scaled_gain * k**2))
        close = roots[np.argsort(np.abs(roots - 1))[:2]]
        squared_speed = (scaled_gain - c) / (4 / 3)
        np.testing.assert_allclose(((close - 1) / k) ** 2, squared_speed, rtol=0.06)


def test_formal_static_response_is_not_a_stable_screened_limit():
    k, gain = 0.018, 0.02
    scalar = -(EPSILON**2) / 2
    matrix = _field_feedback_matrix(k, gain)
    _, source = _mode(k, scalar)
    potential = np.linalg.solve(np.eye(3) - matrix, source)[0] / k**2
    assert potential == pytest.approx(scalar / gain, rel=0.01)
    assert max(np.linalg.eigvals(matrix).real) > 1


def _material_medium_block(k, retention, mobility, sourcing, transport):
    matrix, source = _mode(k, -(EPSILON**2) / 2)
    coupled = np.zeros((4, 4), dtype=complex)
    coupled[:3, :3] = matrix
    coupled[:3, 3] = sourcing * source
    coupled[3, 0] = mobility * transport
    coupled[3, 3] = retention
    return coupled, np.r_[source, 0]


def test_separate_mobile_material_still_grows_at_fractional_wavenumber_rate():
    mobility, sourcing = 0.2, 0.2
    coefficient = (mobility * sourcing * (EPSILON**2 / 2) / (4 / 3)) ** (1 / 3)
    errors = []
    for k in (0.008, 0.004):
        p_m = np.exp(-0.27 * k**2)
        coupled, _ = _material_medium_block(k, p_m, mobility, sourcing, p_m)
        roots = np.linalg.eigvals(coupled)
        growing = roots[np.argmax(roots.real)]
        scaled = (growing - 1) / k ** (2 / 3)
        assert growing.real > 1
        assert scaled == pytest.approx(coefficient, rel=0.14)
        errors.append(abs(scaled - coefficient))
    assert errors[1] < errors[0]


def test_anchored_material_keeps_a_static_pole_and_damped_longitudinal_waves():
    k, retention, mobility, sourcing = 0.012, 0.48, 0.2, 0.2
    matrix, drive = _material_medium_block(k, retention, mobility, sourcing, 1)
    c = EPSILON**2 / 2
    coupling = c * sourcing * mobility
    restored = c - coupling / (1 - retention)
    stationary = np.linalg.solve(np.eye(4) - matrix, drive)
    assert stationary[0] == pytest.approx(c / restored, rel=4e-4)
    roots = np.linalg.eigvals(matrix)
    assert np.all(np.abs(roots) < 1)
    waves = roots[np.argsort(np.abs(roots - 1))[:2]]
    logs = np.log(waves)
    speed_squared = restored / (4 / 3)
    np.testing.assert_allclose(np.abs(logs.imag / k), np.sqrt(speed_squared), rtol=5e-4)
    vector_width = SIGMA**2 / 2 + 6 / 5 * EPSILON**2
    damping = (
        speed_squared
        - vector_width
        + EPSILON**2 / 6
        - coupling * retention / (1 - retention) ** 2
    ) / (8 / 3)
    np.testing.assert_allclose(logs.real / k**2, damping, rtol=8e-4)


def test_internal_shape_change_does_not_polarize_a_mass_proportional_monopole():
    masses = np.array([1, 3])

    def contrast(k, charges):
        offsets = np.array([-0.75, 0.25])
        return abs(charges @ (np.exp(-1j * k * offsets) - np.exp(-2j * k * offsets)))

    for charges, exponent in ((masses, 2), (np.ones(2), 1)):
        assert contrast(0.02, charges) / contrast(0.01, charges) == pytest.approx(
            2**exponent, rel=3e-4
        )


def _paired_material_block(k, charges, spring):
    mobility = np.array([0.7, 1.3])
    translation = 1 / np.sqrt(mobility)
    internal = np.sqrt(mobility) * np.array([1, -1])
    response = np.eye(2) - spring * np.outer(internal, internal)
    coupling = np.sqrt(mobility) * charges
    p_m = np.exp(-0.27 * k**2)
    field, source = _mode(k, -(EPSILON**2) / 2)
    matrix = np.zeros((5, 5), dtype=complex)
    matrix[:3, :3] = field
    matrix[:3, 3:] = np.outer(source, coupling)
    matrix[3:, 0] = p_m * coupling
    matrix[3:, 3:] = p_m * response
    return matrix, np.r_[source, 0, 0], translation, coupling


def test_bound_pair_center_and_internal_response_have_nonnegative_residues():
    k, z, spring = 0.09, 1.08 + 0.05j, 0.24
    charges = np.array([0.2, -0.15])
    matrix, _, translation, coupling = _paired_material_block(k, charges, spring)
    p_m = np.exp(-0.27 * k**2)
    monopole = charges.sum() ** 2 / (translation @ translation)
    polarization = coupling @ coupling - monopole
    assert monopole > 0 and polarization > 0
    expected = p_m * (monopole / (z - p_m) + polarization / (z - 0.52 * p_m))
    actual = coupling @ np.linalg.solve(z * np.eye(2) - matrix[3:, 3:], matrix[3:, 0])
    assert actual == pytest.approx(expected, rel=1e-14)


def test_neutral_bound_pair_retains_damped_sound_and_pole_without_fixed_anchors():
    k, spring = 0.012, 0.24
    charges = np.array([0.15, -0.15])
    matrix, source, translation, coupling = _paired_material_block(k, charges, spring)
    assert coupling @ translation == pytest.approx(0, abs=1e-16)
    c = EPSILON**2 / 2
    restored = c * (1 - (coupling @ coupling) / (1 - 0.52))
    static = np.linalg.solve(np.eye(5) - matrix, source)
    assert static[0] == pytest.approx(c / restored, rel=4e-4)

    roots = np.linalg.eigvals(matrix)
    assert np.all(np.abs(roots) < 1)
    p_m = np.exp(-0.27 * k**2)
    assert min(abs(roots - p_m)) < 1e-14
    waves = roots[np.abs(roots.imag) > 1e-3]
    assert len(waves) == 2
    np.testing.assert_allclose(
        np.abs(np.log(waves).imag / k), np.sqrt(restored / (4 / 3)), rtol=6e-4
    )

    disconnected, *_ = _paired_material_block(k, charges, 0)
    assert max(np.linalg.eigvals(disconnected).real) > 1


def test_nonzero_monopole_restores_growth_in_spite_of_internal_binding():
    charges = np.array([0.15, 0.15])
    for k in (0.006, 0.003):
        matrix, _, translation, _ = _paired_material_block(k, charges, 0.24)
        monopole = charges.sum() ** 2 / (translation @ translation)
        expected = ((EPSILON**2 / 2) * monopole / (4 / 3)) ** (1 / 3)
        largest = max(np.linalg.eigvals(matrix).real)
        assert largest > 1
        assert (largest - 1) / k ** (2 / 3) == pytest.approx(expected, rel=0.13)
