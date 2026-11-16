"""Fixed two-phase force identities and kernel bounds, without orbit search."""

from fractions import Fraction

import numpy as np
import pytest

from emergenz_knoten.kernels import (
    double_gaussian_gradient,
    effective_double_gaussian_parameters,
    exponential_memory_weights,
)
from emergenz_knoten.vector_memory import normalize_orientation, vector_gaussian_field


def _rotation(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def _geometry():
    return np.array([0.8, 0.1, -0.4]), np.array([-0.2, 1.1, 0.6])


def _history(a, b, matrix, phase, count):
    points = []
    for age in range(count):
        power, seed = divmod(phase - age, 2)
        points.append(np.linalg.matrix_power(matrix, power) @ (a if seed == 0 else b))
    return np.array(points)


def _phase_table(a, b, matrix, phase, count):
    p_a = normalize_orientation(a - matrix.T @ b)
    p_b = normalize_orientation(b - a)
    positions, directions = [], []
    for age in range(count):
        lag, odd = divmod(age, 2)
        if phase == 0:
            rotation = np.linalg.matrix_power(matrix.T, lag + odd)
            position, direction = (b, p_b) if odd else (a, p_a)
        else:
            rotation = np.linalg.matrix_power(matrix.T, lag)
            position, direction = (a, p_a) if odd else (b, p_b)
        positions.append(rotation @ position)
        directions.append(rotation @ direction)
    return np.array(positions), np.array(directions)


def _gaussian(delta, ell):
    return np.exp(-np.sum(np.asarray(delta) ** 2, axis=-1) / (2 * ell**2))


def _coefficients(a, b, matrix, q, horizon, ell):
    even, odd = [], []
    for phase, receiver in enumerate((a, b)):
        positions, _ = _phase_table(a, b, matrix, phase, horizon)
        values = q ** np.arange(horizon) * _gaussian(receiver - positions, ell)
        even.append(values[::2].sum())
        odd.append(values[1::2].sum())
    even, odd = np.array(even), np.array(odd)
    lengths = np.array([np.linalg.norm(a - matrix.T @ b), np.linalg.norm(b - a)])
    axial = even / lengths - odd / lengths[::-1]
    determinant = np.prod(even) - np.prod(odd)
    multipliers = (even + odd)[::-1]
    return even, odd, axial, determinant, multipliers, lengths


def _cross_sums(a, b, matrix, q, pairs, ell):
    powers = np.array([np.linalg.matrix_power(matrix.T, j) for j in range(pairs + 1)])
    weights = (q**2) ** np.arange(pairs)
    k = _gaussian(a - powers @ b, ell)
    c = weights @ k[:-1]
    d = weights @ _gaussian(b - powers[:-1] @ a, ell)
    return c, d, k[0], k[-1]


@pytest.mark.parametrize("deposition", ["delta", "gaussian", "matched_gaussian"])
@pytest.mark.parametrize("hs,hv", [(4, 4), (5, 6), (7, 5)])
def test_both_phase_force_tables_match_native_history_and_axial_balances(
    deposition, hs, hv
):
    a, b = _geometry()
    matrix, q, s, ell = _rotation(0.73), 0.6, 0.7, 1.2
    vector_weights = exponential_memory_weights(1 - q, hv, memory_mass=0.8)
    scalar_weights = exponential_memory_weights(1 - s, hs, memory_mass=1.1)
    kernel = dict(
        sigma_rep=0.7,
        sigma_att=1.4,
        amplitude_rep=0.8,
        amplitude_att=1.2,
        deposition_kernel=deposition,
        deposition_sigma=0.3 if deposition == "gaussian" else 0.0,
    )
    effective = effective_double_gaussian_parameters(dim=3, **kernel)
    even, odd, axial, determinant, multipliers, lengths = _coefficients(
        a, b, matrix, q, hv, ell
    )
    np.testing.assert_allclose(
        multipliers @ axial, determinant * np.sum(1 / lengths), atol=2e-15
    )
    difference = b[2] - a[2]
    for phase, receiver in enumerate((a, b)):
        history = _history(a, b, matrix, phase, max(hs, hv + 1))
        currents = np.array(
            [normalize_orientation(x) for x in history[:hv] - history[1 : hv + 1]]
        )
        table_points, table_currents = _phase_table(a, b, matrix, phase, hv)
        np.testing.assert_allclose(table_points, history[:hv], atol=1e-15)
        np.testing.assert_allclose(table_currents, currents, atol=1e-15)
        field = vector_gaussian_field(
            receiver, history[:hv], currents, vector_weights, sigma=ell
        )
        table_field = np.sum(
            (vector_weights * _gaussian(receiver - table_points, ell))[:, None]
            * table_currents,
            axis=0,
        )
        np.testing.assert_allclose(field, table_field, atol=3e-16)
        gradient = double_gaussian_gradient(
            receiver, history[:hs], scalar_weights, **kernel
        )
        radii = np.sum((receiver - history[:hs]) ** 2, axis=1)
        radial = (
            -effective["amplitude_rep"]
            / effective["sigma_rep"] ** 2
            * np.exp(-radii / (2 * effective["sigma_rep"] ** 2))
        )
        radial += (
            effective["amplitude_att"]
            / effective["sigma_att"] ** 2
            * np.exp(-radii / (2 * effective["sigma_att"] ** 2))
        )
        table_gradient = np.sum(
            (scalar_weights * radial)[:, None] * (receiver - history[:hs]), axis=0
        )
        np.testing.assert_allclose(gradient, table_gradient, atol=3e-16)
        restoring = np.sum((scalar_weights * radial)[1::2])
        sign = 1 if phase == 0 else -1
        assert gradient[2] == pytest.approx(-sign * difference * restoring, abs=3e-16)
        assert field[2] == pytest.approx(
            -sign * difference * vector_weights[0] * axial[phase], abs=3e-16
        )
        assert (
            restoring
            <= effective["amplitude_att"]
            / effective["sigma_att"] ** 2
            * scalar_weights[1::2].sum()
        )
    expected_odd_mass = (1 - s) * 1.1 * s * (1 - s ** (2 * (hs // 2))) / (1 - s**2)
    assert scalar_weights[1::2].sum() == pytest.approx(expected_odd_mass, rel=2e-15)


@pytest.mark.parametrize("order", [2, 3, 4])
@pytest.mark.parametrize("q", [0.3, 0.85])
def test_full_period_gaussian_determinant_has_the_proved_positive_margin(order, q):
    a, b = _geometry()
    matrix, ell, pairs = _rotation(2 * np.pi / order), 1.2, 2 * order
    even, odd, axial, determinant, multipliers, lengths = _coefficients(
        a, b, matrix, q, 2 * pairs, ell
    )
    c, d, k0, k_end = _cross_sums(a, b, matrix, q, pairs, ell)
    assert k_end == pytest.approx(k0, abs=1e-15)
    t = q**2
    assert odd[0] == pytest.approx((c - (1 - t**pairs) * k0) / q, abs=8e-16)
    assert odd[1] == pytest.approx(q * d, abs=8e-16)
    gram = np.array([[even[0], (c + d) / 2], [(c + d) / 2, even[1]]])
    assert np.linalg.eigvalsh(gram).min() > 0
    margin = (c - d) ** 2 / 4 + (1 - t**pairs) * k0 * d
    assert margin > 0 and determinant >= margin - 2e-15
    assert np.max(axial) > 0
    assert multipliers @ axial == pytest.approx(
        determinant * np.sum(1 / lengths), abs=2e-15
    )
    odd_horizon = _coefficients(a, b, matrix, q, 2 * pairs + 1, ell)
    np.testing.assert_allclose(odd_horizon[1], odd, atol=2e-16)
    assert odd_horizon[3] > determinant
    # For a periodic geometry, the infinite sums are exact geometric extensions.
    infinite_even, infinite_odd = even / (1 - t**pairs), odd / (1 - t**pairs)
    infinite_c, infinite_d = c / (1 - t**pairs), d / (1 - t**pairs)
    assert infinite_odd[0] == pytest.approx((infinite_c - k0) / q, abs=8e-16)
    infinite_margin = (infinite_c - infinite_d) ** 2 / 4 + k0 * infinite_d
    assert np.prod(infinite_even) - np.prod(infinite_odd) >= infinite_margin - 3e-15


@pytest.mark.parametrize("angle", [0.73, 1.1])
def test_nonperiodic_cutoff_keeps_its_tail_and_can_pass_sufficient_bound(angle):
    a, b = _geometry()
    matrix, q, pairs, ell = _rotation(angle), 0.4, 3, 1.2
    even, odd, _, determinant, _, _ = _coefficients(a, b, matrix, q, 2 * pairs, ell)
    c, d, k0, k_end = _cross_sums(a, b, matrix, q, pairs, ell)
    t = q**2
    assert abs(k_end - k0) > 0.01
    assert odd[0] == pytest.approx((c - k0 + t**pairs * k_end) / q, abs=5e-16)
    assert 1 / (1 + t) - t**pairs / (1 - t) > 0
    assert k0 > t**pairs * k_end
    margin = (c - d) ** 2 / 4 + (k0 - t**pairs * k_end) * d
    assert determinant >= margin - 2e-15 and margin > 0
    assert np.prod(even) >= ((c + d) / 2) ** 2


def test_cutoff_operator_is_not_automatically_positive_by_exact_arithmetic():
    t, cosine = Fraction(99, 100), Fraction(-1, 4)
    symmetric_part = 1 + t * cosine + t**2 * (2 * cosine**2 - 1)
    assert symmetric_part == Fraction(-8407, 80000) < 0


@pytest.mark.parametrize("q", [0.3, 0.85])
def test_unitary_resolvent_symmetric_part_identity(q):
    t, unitary = q**2, _rotation(0.73)
    resolvent = np.linalg.inv(np.eye(3) - t * unitary)
    expected = np.eye(3) / 2 + (1 - t**2) / 2 * resolvent.T @ resolvent
    np.testing.assert_allclose((resolvent + resolvent.T) / 2, expected, atol=1e-15)
    assert np.linalg.eigvalsh(expected).min() >= 1 / (1 + t) - 1e-15


def test_known_negative_gain_cycle_satisfies_both_axial_balances_without_attraction():
    a = np.array([1.0, 1.0, 1.0]) / 2
    improper = np.array([[0, 0, -1], [0, -1, 0], [1, 0, 0]])
    b, matrix = improper @ a, improper @ improper
    ell, q, s = 1 / np.sqrt(np.log(2)), 0.5, 1 / 6
    _, _, axial, determinant, multipliers, lengths = _coefficients(
        a, b, matrix, q, 4, ell
    )
    eta_scalar = 108 / ((5 / 6) * 0.5 * np.exp(-0.5))
    eta_vector = -48 * np.sqrt(2)
    scalar_weights = exponential_memory_weights(1 - s, 4)
    vector_weights = exponential_memory_weights(1 - q, 4)
    restoring = []
    for phase, receiver in enumerate((a, b)):
        history = _history(a, b, matrix, phase, 5)
        directions = np.array(
            [normalize_orientation(x) for x in history[:4] - history[1:]]
        )
        gradient = double_gaussian_gradient(
            receiver,
            history[:4],
            scalar_weights,
            sigma_rep=np.sqrt(2),
            sigma_att=2,
            amplitude_rep=1,
            amplitude_att=0,
        )
        field = vector_gaussian_field(
            receiver, history[:4], directions, vector_weights, sigma=ell
        )
        expected_point = b if phase == 0 else matrix @ a
        np.testing.assert_allclose(
            receiver - eta_scalar * gradient + eta_vector * field,
            expected_point,
            atol=2e-14,
        )
        radial = -0.5 * np.exp(-np.sum((receiver - history[:4]) ** 2, axis=1) / 4)
        restoring.append(np.sum((scalar_weights * radial)[1::2]))
        assert eta_scalar * restoring[-1] == pytest.approx(-37 / 2, abs=1e-14)
        assert eta_vector * vector_weights[0] * axial[phase] == pytest.approx(
            -39 / 2, abs=1e-14
        )
    assert determinant > 0
    assert eta_scalar * (multipliers @ restoring) == pytest.approx(
        multipliers.sum()
        + eta_vector * vector_weights[0] * determinant * np.sum(1 / lengths),
        abs=4e-14,
    )
