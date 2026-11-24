"""Full linear certification at the fixed radius and masses of the center-free orbit."""

from dataclasses import replace
from fractions import Fraction

import numpy as np
import pytest
from mpmath import iv

from experiments.current.reference.fifo_carrier_clock_cycle import clock_return
from experiments.current.reference.fifo_center_free_hexagon import (
    planar_tangent,
    prepared_center_free_hexagon,
)
from experiments.current.reference.fifo_reversible_carrier import carrier_map


def test_center_free_hexagon_closes_the_true_history():
    model, start = prepared_center_free_hexagon()
    state = start
    phase = np.exp(1j * np.pi / 3)
    radius = start.position[0, 0]
    for n in range(6):
        stored = radius * phase ** (n - np.arange(1, 4))
        np.testing.assert_allclose(
            state.position[1:-1], np.c_[stored.real, stored.imag], atol=3e-11, rtol=0
        )
        np.testing.assert_allclose(state.position[-1], state.position[-2], atol=3e-11)
        state, event, duration = clock_return(state, model)
        assert event.crossed
        assert event.energy_gap == pytest.approx(0, abs=3e-11)
        assert duration == pytest.approx(np.pi / 3, abs=3e-11)
    np.testing.assert_allclose(state.position, start.position, atol=3e-11, rtol=0)
    np.testing.assert_allclose(state.momentum, start.momentum, atol=3e-11, rtol=0)
    assert state.clock_momentum == pytest.approx(start.clock_momentum, abs=3e-11)


def test_planar_clock_derivative_matches_the_fixed_energy_return():
    model, base = prepared_center_free_hexagon()
    energy = (
        model.internal_energy(base.position, base.momentum) + base.clock_momentum**2 / 2
    )
    rotation = np.array([[0.5, -np.sqrt(3) / 2], [np.sqrt(3) / 2, 0.5]])

    def observed(probe):
        q, p = np.split(
            np.vstack((base.position, base.momentum)) + probe.reshape(10, 2), 2
        )
        clock = np.sqrt(2 * (energy - model.internal_energy(q, p)))
        result, _, _ = clock_return(
            replace(base, position=q, momentum=p, clock_momentum=clock), model
        )
        return (np.vstack((result.position, result.momentum)) @ rotation).ravel()

    step = 1e-7
    difference = np.column_stack(
        [(observed(step * v) - observed(-step * v)) / (2 * step) for v in np.eye(20)]
    )
    np.testing.assert_allclose(
        difference, planar_tangent(model, base), atol=4e-9, rtol=0
    )


def test_finite_impulse_probe_keeps_invariants_but_changes_the_next_copy():
    model, base = prepared_center_free_hexagon()
    q = np.c_[base.position, np.zeros(5)]
    p0 = np.c_[base.momentum, np.zeros(5)]
    amplitude = 1e-4
    p = p0.copy()
    p[-1, 2] += amplitude
    p[-2, 2] -= amplitude
    clock = np.sqrt(base.clock_momentum**2 - 2 * amplitude**2)
    initial = replace(base, position=q, momentum=p, clock_momentum=clock)
    np.testing.assert_array_equal(q[-1], q[-2])
    np.testing.assert_allclose(p.sum(axis=0), p0.sum(axis=0), atol=3e-17, rtol=0)
    np.testing.assert_allclose(
        np.cross(q, p).sum(axis=0), np.cross(q, p0).sum(axis=0), atol=3e-17, rtol=0
    )
    assert model.internal_energy(q, p) + clock**2 / 2 == pytest.approx(
        model.internal_energy(q, p0) + base.clock_momentum**2 / 2, abs=2e-16
    )
    arrived, event, _ = clock_return(initial, model)
    assert event.crossed
    np.testing.assert_allclose(event.state.position[1], q[0], atol=2e-17, rtol=0)
    error = (arrived.position[-1, 2] - arrived.position[-2, 2]) / amplitude
    newest_drift = arrived.position[1, 2] / amplitude
    assert -0.0162 < error < -0.0159
    assert 0.1208 < newest_drift < 0.1212


def _as_interval(rational):
    return iv.mpf(rational.numerator) / rational.denominator


def _enclose_frequency(target, bounds):
    def residual(ratio):
        phase = _as_interval(ratio) * iv.pi / 6
        return _as_interval(ratio) * iv.sin(phase) / iv.cos(phase) - target

    left, right = map(Fraction, bounds)
    assert residual(left).b < 0 < residual(right).a
    for _ in range(56):
        center = (left + right) / 2
        error = residual(center)
        if error.b < 0:
            left = center
        else:
            assert error.a > 0
            right = center
    return iv.mpf([_as_interval(left).a, _as_interval(right).b])


def _exact_modes_and_orbit():
    phase = iv.mpc(iv.mpf(1) / 2, iv.sqrt(3) / 2)
    a = -(1 + iv.sqrt(5)) / 2
    tail = -1 - a
    shift = a - phase + phase**2 * tail
    relative = iv.mpc(0, 2)
    sigma = -(1 + phase) * relative / (phase * shift)
    carrier = sigma * shift / 2
    newest = (-carrier + sigma * a) / phase
    second = (-newest + sigma) / phase
    q = [1, 1 / phase, 1 / phase**2, -1, -1]
    p = [relative + carrier, newest, second, -carrier, carrier]
    inverse = [iv.mpf(1) / 2, 1, 1, 1]
    basis = [
        [1, -iv.mpf(1) / 3, -iv.mpf(1) / 3, -iv.mpf(1) / 3],
        [0, 1 - tail, tail - a, a - 1],
    ]
    basis = [
        [
            x / iv.sqrt(sum(k * y**2 for k, y in zip(inverse, row, strict=True)))
            for x in row
        ]
        for row in basis
    ]
    coords = [
        sum(w * z for w, z in zip(row, [0, *q[:3]], strict=True)) for row in basis
    ]
    impulse = [
        sum(
            w * k * z
            for w, k, z in zip(
                row, inverse, [relative, carrier, newest, second], strict=True
            )
        )
        for row in basis
    ]
    z0, z1 = coords
    denom = z0.real * z1.imag - z0.imag * z1.real
    assert denom.a > 0 or denom.b < 0
    inverse_coords = iv.matrix([[z1.imag, -z0.imag], [-z1.real, z0.real]]) / denom
    robin = iv.matrix([[z.real, z.imag] for z in impulse]) * inverse_coords
    # Symmetry follows from the exact rotation and angular-momentum balance.
    skew = robin[0, 1] - robin[1, 0]
    assert skew.a <= 0 <= skew.b
    robin = (robin + robin.T) / 2
    gap = iv.sqrt((robin[0, 0] - robin[1, 1]) ** 2 + 4 * robin[0, 1] ** 2)
    trace = robin[0, 0] + robin[1, 1]
    minus, plus = (trace - gap) / 2, (trace + gap) / 2
    assert minus.b < 0 < plus.a
    lift = iv.matrix([[row[0] / 2, *row[1:], row[0] / 2] for row in basis]).T
    return (
        q + p,
        (
            (
                minus,
                lift * (plus * iv.eye(2) - robin) * lift.T / gap,
                ("5.43992841570", "5.43992841571"),
            ),
            (
                plus,
                lift * (robin - minus * iv.eye(2)) * lift.T / gap,
                ("1.92362290553", "1.92362290554"),
            ),
        ),
        iv.matrix([0, a, 1, tail, 0]),
    )


def _certified_maps():
    orbit, detuned, preserved = _exact_modes_and_orbit()
    e = iv.matrix([1, 0, 0, 0, -1])
    relative = e * e.T / 2
    stiffness = relative + 36 * preserved * preserved.T / sum(
        preserved[i] ** 2 for i in range(5)
    )
    qq = iv.eye(5) - relative / 2
    qp = iv.sqrt(3) * relative / 2
    pq = -qp
    pp = qq.T
    for eta, projector, box in detuned:
        omega2 = _enclose_frequency(eta, box) ** 2
        total = omega2 + eta**2
        qq -= (2 * eta**2 / total) * projector
        pp -= (2 * eta**2 / total) * projector
        qp += (2 * eta / total) * projector
        pq -= (2 * eta * omega2 / total) * projector
        stiffness += omega2 * projector
    c, g = [
        iv.matrix(x.astype(int).tolist()) for x in carrier_map(np.eye(5), np.eye(5))
    ]

    def block(left, right, lower_left, lower_right):
        return iv.matrix(
            [
                [*[left[i, j] for j in range(5)], *[right[i, j] for j in range(5)]]
                for i in range(5)
            ]
            + [
                [
                    *[lower_left[i, j] for j in range(5)],
                    *[lower_right[i, j] for j in range(5)],
                ]
                for i in range(5)
            ]
        )

    # The omitted translation drift feeds only the factored symmetry block.
    normal = block(qq * c, qp * g, pq * c, pp * g)
    phase = iv.matrix([[iv.mpf(z.real) / 25, iv.mpf(z.imag) / 25] for z in orbit])
    hessian = block(stiffness, iv.zeros(5), iv.zeros(5), iv.eye(5))
    generator = block(iv.zeros(5), iv.eye(5), -stiffness, iv.zeros(5))
    gate = block(c, iv.zeros(5), iv.zeros(5), g)
    velocity = generator * phase
    gradient = gate.T * hessian * gate * phase
    rot = iv.matrix([[iv.mpf(1) / 2, iv.sqrt(3) / 2], [-iv.sqrt(3) / 2, iv.mpf(1) / 2]])
    planar = iv.matrix(
        [
            [
                normal[i // 2, j // 2] * rot[i % 2, j % 2]
                + (iv.pi / 3) ** 3 * velocity[i // 2, i % 2] * gradient[j // 2, j % 2]
                for j in range(20)
            ]
            for i in range(20)
        ]
    )
    return normal, planar


def _reduced_coefficients(matrix, symmetry_roots):
    size = matrix.rows
    degree = size // 2
    power = iv.eye(size)
    coefficients, traces = [iv.mpf(1)], [iv.mpf(0)]
    for k in range(1, degree + 1):
        power = power * matrix
        traces.append(sum(power[i, i] for i in range(size)))
        coefficients.append(
            -sum(c * traces[k - j] for j, c in enumerate(coefficients)) / k
        )
    # Ascending coefficients of z**k + z**(-k) in u = z + 1/z.
    previous, current = [2], [0, 1]
    poly = [coefficients[degree]] + [iv.mpf(0)] * degree
    for k in range(1, degree + 1):
        for j, val in enumerate(current):
            poly[j] += coefficients[degree - k] * val
        following = [0, *current]
        for j, val in enumerate(previous):
            following[j] -= val
        previous, current = current, following
    poly.reverse()
    for root in symmetry_roots:
        quotient = [poly[0]]
        for value in poly[1:-1]:
            quotient.append(value + root * quotient[-1])
        remainder = poly[-1] + root * quotient[-1]
        assert remainder.a <= 0 <= remainder.b
        poly = quotient
    return poly


def _sign(interval):
    if interval.a > 0:
        return 1
    assert interval.b < 0
    return -1


def _isolate_roots(poly, boxes):
    assert len(boxes) == len(poly) - 1

    def evaluate(rational):
        x = _as_interval(rational)
        result = iv.mpf(0)
        for coefficient in poly:
            result = result * x + coefficient
        return result

    roots = []
    for lo, hi in boxes:
        left, right = map(Fraction, (lo, hi))
        sign_left = _sign(evaluate(left))
        assert sign_left != _sign(evaluate(right))
        for _ in range(28):
            center = (left + right) / 2
            if _sign(evaluate(center)) == sign_left:
                left = center
            else:
                right = center
        roots.append(iv.mpf([_as_interval(left).a, _as_interval(right).b]))
    return roots


def _frequency_sums(angles, start, remaining, total, order=0):
    # A fixed positive first coefficient removes the duplicate negated vector.
    for j in range(start, len(angles)):
        for multiplicity in range(1, remaining + 1):
            for sign in (1,) if order == 0 else (-1, 1):
                combined = total + (sign * multiplicity) * angles[j]
                new_order = order + multiplicity
                yield combined, new_order
                yield from _frequency_sums(
                    angles, j + 1, remaining - multiplicity, combined, new_order
                )


def test_stable_reduced_blocks_have_no_nontrivial_resonance_through_degree_five():
    saved = iv.dps
    iv.dps = 75
    try:
        normal, planar = _certified_maps()
        cases = (
            (normal, [2, 1], [("-1.83", "-1.80"), (".41", ".43"), ("1.02", "1.05")]),
            (
                planar,
                [1, 1, 2],
                [
                    ("-1.70", "-1.66"),
                    ("-1.61", "-1.57"),
                    ("-1.06", "-1.02"),
                    ("-.70", "-.66"),
                    (".39", ".43"),
                    ("1.005", "1.017"),
                    ("1.98", "1.995"),
                ],
            ),
        )
        roots = [
            u / 2
            for matrix, symmetry_roots, boxes in cases
            for u in _isolate_roots(
                _reduced_coefficients(matrix, symmetry_roots), boxes
            )
        ]
        angles = [iv.atan2(iv.sqrt(1 - x**2), x) for x in roots]
        margins = [iv.mpf(string) for string in ("0.0058", "0.001", "0.000024")]
        turns = [2 * j * iv.pi for j in range(-2, 3)]
        for total, order in _frequency_sums(angles, 0, 5, iv.mpf(0)):
            margin = margins[max(0, order - 3)]
            for turn in turns:
                excess = total - turn
                assert excess.a > margin or excess.b < -margin

        probe = iv.matrix([0, 0, 0, 0, 0, 0, 0, 0, -1, 1])
        tangent = normal * probe
        error = tangent[4] - tangent[3]
        assert iv.mpf("-0.0162") < error.a <= error.b < iv.mpf("-0.0159")
        assert iv.mpf("0.1208") < tangent[1].a <= tangent[1].b < iv.mpf("0.1212")
        orbit, _, _ = _exact_modes_and_orbit()
        angular = (
            sum(
                orbit[i].real * orbit[i + 5].imag - orbit[i].imag * orbit[i + 5].real
                for i in range(5)
            )
            / 25**2
        )
        assert angular.a > iv.mpf("0.0028")
    finally:
        iv.dps = saved
