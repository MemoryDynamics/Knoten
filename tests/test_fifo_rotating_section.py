"""Rational exclusion of a rotating section in the fixed equal-mass case."""

from fractions import Fraction as F
from math import factorial

import numpy as np

from experiments.current.reference.fifo_carrier_clock_cycle import MobileMemoryClock
from experiments.current.reference.fifo_reversible_carrier import carrier_map


def _certify_trig_centers():
    pi = F("3.14159265359")
    root = F("1.41421356237")

    def atan_series(n):
        return sum(F((-1) ** j, (2 * j + 1) * n ** (2 * j + 1)) for j in range(10))

    # Machin's formula and the alternating arctangent remainders.
    pi_error = F(16, 21 * 5**21) + F(4, 21 * 239**21)
    assert abs(16 * atan_series(5) - 4 * atan_series(239) - pi) + pi_error < F(
        1, 10**11
    )
    radius = F(1, 10**11)
    assert (root - radius) ** 2 < 2 < (root + radius) ** 2
    theta = pi * root
    theta_radius = (pi + root + radius) * radius
    assert theta + theta_radius < F(9, 2)

    cosine = sum(F((-1) ** j, factorial(2 * j)) * theta ** (2 * j) for j in range(17))
    sine = sum(
        F((-1) ** j, factorial(2 * j + 1)) * theta ** (2 * j + 1) for j in range(17)
    )
    cos_radius = theta_radius + F(9, 2) ** 33 / factorial(33)
    sin_radius = theta_radius + F(9, 2) ** 34 / factorial(34)
    assert abs(sine) <= 1 + sin_radius
    scaled_sin_radius = sin_radius / (root - radius) + (
        abs(sine) * radius / (root * (root - radius))
    )
    centers = F("3.141593"), F("-0.266255"), F("-0.681582")
    assert abs(pi - centers[0]) + radius < F(1, 10**6)
    assert abs(cosine - centers[1]) + cos_radius < F(1, 10**6)
    assert abs(sine / root - centers[2]) + scaled_sin_radius < F(1, 10**6)
    return centers


def _reference_matrix():
    time, cosine, scaled_sine = _certify_trig_centers()
    eye = np.eye(5, dtype=int).astype(object)
    relative = np.array([1, 0, 0, 0, -1], dtype=object)
    balance = np.array([1, -1, -1, 0, 1], dtype=object)
    pd = F(1, 2) * np.outer(relative, relative)
    ps = F(1, 4) * np.outer(balance, balance)
    a = eye - 2 * pd + (cosine - 1) * ps
    b = time * (eye - pd - ps) + scaled_sine * ps
    c = -2 * scaled_sine * ps
    cq = np.array(
        [
            [1, 0, 0, 0, 0],
            [1, 0, 0, -1, 1],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
        ],
        dtype=object,
    )
    cp = np.array(
        [
            [1, 0, 0, 0, -1],
            [0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 1],
        ],
        dtype=object,
    )
    np.testing.assert_array_equal(cq.T @ cp, eye)
    return np.block([[a @ cq, b @ cp], [c @ cq, a @ cp]])


def test_certified_reciprocal_cubic_has_no_root_in_the_rotation_band():
    j0 = _reference_matrix()
    # Induced infinity norm: errors in the three flow blocks are bounded by
    # 1, 4 and 2 micro-units; the write blocks have row sums at most 3 and 2.
    delta = F(11, 10**6)
    bound = 16
    assert max(np.abs(j0).sum(axis=1)) + delta < bound
    e1, e2, e3 = [10 * k * bound ** (k - 1) * delta for k in (1, 2, 3)]
    t1, t2, t3 = [np.trace(power) for power in (j0, j0 @ j0, j0 @ j0 @ j0)]
    a = -t1
    b = (t1**2 - t2) / 2 - 1
    c = -(t1**3 - 3 * t1 * t2 + 2 * t3) / 6
    eb = (e1 * (2 * abs(t1) + e1) + e2) / 2
    ec = (
        e1 * (3 * t1**2 + 3 * abs(t1) * e1 + e1**2)
        + 3 * (e1 * (abs(t2) + e2) + abs(t1) * e2)
        + 2 * e3
    ) / 6
    assert F("1.3") < a - e1
    assert 0 < b - eb < b + eb < F("0.3")
    assert 5 < c - ec
    # For u in [-2, 0], u^2(u+a) + b*u + c > -2.8 - 0.6 + 5.
    # For u in [0, 2], every term is nonnegative and c is positive.
    assert 5 - 4 * (2 - F("1.3")) - 2 * F("0.3") > 0


def test_rational_matrix_matches_the_implemented_fixed_flight():
    j0 = _reference_matrix()
    model = MobileMemoryClock(spring=0.5)
    columns = []
    for e in np.eye(10):
        q, p = carrier_map(*e.reshape(2, 5, 1))
        columns.append(np.r_[model.flight(q, p, np.pi)].ravel())
    matrix = np.array(columns).T
    assert np.linalg.norm(matrix - j0.astype(float), ord=np.inf) < 11e-6
