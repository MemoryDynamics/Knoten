"""Finite necessary-force certificate, not a kernel fit or target trajectory."""

from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt

import numpy as np
import pytest

from emergenz_knoten.kernels import exponential_memory_weights
from emergenz_knoten.state import FiniteMemoryState
from emergenz_knoten.vector_memory import (
    oriented_history_from_state,
    vector_memory_force,
)


SCALE = 10**40


@dataclass(frozen=True)
class _Interval:
    lo: F
    hi: F

    def __post_init__(self):
        if not isinstance(self.lo, F) or not isinstance(self.hi, F):
            raise TypeError("rational endpoints required")
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    @staticmethod
    def point(value):
        if not isinstance(value, (int, F)):
            raise TypeError("only exact scalar inputs")
        return _Interval(F(value), F(value))

    @staticmethod
    def rounded(lo, hi):
        lower = (lo * SCALE).__floor__()
        upper = (hi * SCALE).__ceil__()
        return _Interval(F(lower, SCALE), F(upper, SCALE))

    @staticmethod
    def convert(value):
        return value if isinstance(value, _Interval) else _Interval.point(value)

    def __add__(self, other):
        other = self.convert(other)
        return self.rounded(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return _Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -self.convert(other)

    def __rsub__(self, other):
        return self.convert(other) + -self

    def __mul__(self, other):
        other = self.convert(other)
        products = [a * b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return self.rounded(min(products), max(products))

    __rmul__ = __mul__

    def reciprocal(self):
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError("interval contains zero")
        return self.rounded(1 / self.hi, 1 / self.lo)

    def __truediv__(self, other):
        return self * self.convert(other).reciprocal()

    def __rtruediv__(self, other):
        return self.convert(other) * self.reciprocal()

    def __pow__(self, exponent):
        if type(exponent) is not int or exponent < 0:
            raise ValueError("nonnegative integer power required")
        result = self.point(1)
        for _ in range(exponent):
            result = result * self
        return result

    def sqrt(self):
        if self.lo < 0:
            raise ValueError("negative square-root argument")
        lower = isqrt(self.lo.numerator * SCALE**2 // self.lo.denominator)
        upper = isqrt(self.hi.numerator * SCALE**2 // self.hi.denominator) + 1
        return _Interval(F(lower, SCALE), F(upper, SCALE))


def _exp_minus(x):
    """Bound exp(-x) by a positive Taylor sum and geometric remainder."""
    x = F(x)
    order = 160
    if not 0 <= x < order + 2:
        raise ValueError("outside fixed Taylor remainder contract")
    total, term = F(1), F(1)
    for k in range(1, order + 1):
        term *= x / k
        total += term
    tail = term * x / (order + 1) / (1 - x / (order + 2))
    return _Interval.rounded(1 / (total + tail), 1 / total)


@pytest.fixture(scope="module")
def necessary():
    q = _Interval.point(F(99, 100))
    t = q * q
    ell = _Interval.point(F(88, 3)).sqrt()
    g_n, g_r, g_x, g_f = map(_exp_minus, [F(4, 3), 8, F(44, 3), F(100, 3)])
    beta_n, beta_f = q * (g_r - g_x) / ell, (1 - g_f) / ell
    a_n = -g_n + q * g_x * (5 - 1 / t) / ell
    a_f = g_f * (5 - 1 / t) / ell - g_x / q
    rho_n = -1 + q * (5 * g_r - q**6 * g_x) / ell
    rho_f = (5 - q**6 * g_f) / ell - q**7 * g_r
    magnitude = -a_f
    u = magnitude * t**2 * (1 - t) / (beta_f + magnitude * t * (1 - t))
    s = u.sqrt()
    delta = a_n - beta_n * a_f / beta_f
    c = -5 * (beta_f + magnitude * t * (1 - t)) / (beta_f * delta * t**2 * (1 - t))
    k_near = 5 * magnitude * (beta_n - a_n * t * (1 - t))
    k_near /= beta_f * delta * u**2 * (1 - u)
    j = (beta_f + magnitude * t * (1 - t)) / (u * (1 - u))
    k_far = -c * j
    w_s, w_q = u + u**2 + u**3, t + t**2 + t**3
    radial_n = rho_n - a_n * w_q / 3 + beta_n / 3
    radial_f = rho_f - a_f * w_q / 3 + beta_f / 3
    l_value = (F(4, 3) * k_near * w_s + c * radial_n + F(8, 3)) / (4 * s)
    m_value = (-4 - F(4, 3) * k_far * w_s - c * radial_f) / 4
    force_x = (m_value - s**7 * l_value) / (w_s / s - s**7 * w_s)
    force_r = l_value - w_s * force_x
    force_n = k_near - 5 * s * force_x
    force_f = (k_far - force_x / s) / 5
    return {
        "s": s,
        "C": c,
        "delta": delta,
        "A": magnitude,
        "beta_f": beta_f,
        "N": force_n,
        "R": force_r,
        "X": force_x,
        "F": force_f,
    }


@pytest.mark.parametrize("bounds", [(-3, -2, 4, 5), (-2, 3, -5, -4), (1, 2, 3, 4)])
def test_rational_arithmetic_encloses_exact_endpoint_operations(bounds):
    a, b, c, d = map(F, bounds)
    left, right = _Interval(a, b), _Interval(c, d)
    for x in (a, (a + b) / 2, b):
        for y in (c, (c + d) / 2, d):
            for result, exact in (
                (left + right, x + y),
                (left - right, x - y),
                (left * right, x * y),
                (left / right, x / y),
            ):
                assert result.lo <= exact <= result.hi


def test_interval_guards_and_outward_rounding():
    value = F(-2, 3)
    rounded = _Interval.rounded(value, value)
    assert rounded.lo <= value <= rounded.hi
    assert rounded.hi - rounded.lo <= F(1, SCALE)
    with pytest.raises(ZeroDivisionError):
        _Interval(F(-1), F(1)).reciprocal()
    with pytest.raises(ValueError):
        _Interval.point(-1).sqrt()
    with pytest.raises(TypeError):
        _Interval.point(0.1)
    with pytest.raises(ValueError):
        _exp_minus(F(162))


def test_square_root_and_taylor_constants_have_exact_endpoint_checks():
    for value in (F(0), F(1, 3), F(88, 3)):
        result = _Interval.point(value).sqrt()
        assert result.lo**2 <= value <= result.hi**2
    result = _exp_minus(F(1, 2))
    assert F(3, 5) < result.lo < result.hi < F(2, 3)


def test_required_values_are_in_strict_rational_boxes(necessary):
    bounds = {
        "s": (F(211, 1000000), F(212, 1000000)),
        "C": (992, 993),
        "N": (-116000000, -115000000),
        "R": (-882000, -881000),
        "X": (-872000, -871000),
        "F": (4130000, 4140000),
    }
    for name, (lower, upper) in bounds.items():
        assert lower < necessary[name].lo <= necessary[name].hi < upper
    assert necessary["delta"].hi < 0
    assert necessary["A"].lo > 0
    assert necessary["beta_f"].lo > 0
    assert necessary["R"].hi < necessary["X"].lo


def test_force_table_contradicts_every_real_two_exponential_kernel(necessary):
    assert F(16) - F(8, 3) == F(88, 3) - F(16) == F(40, 3)
    # The coarse rational boxes alone already give a strictly negative determinant.
    assert 882000**2 - 115000000 * 871000 < 0
    determinant = necessary["R"] ** 2 - necessary["N"] * necessary["X"]
    assert determinant.hi < 0
    assert necessary["N"].hi < 0 < necessary["F"].lo


@pytest.mark.parametrize("amplitudes", [(2, 3), (-2, -3), (2, -3), (-2, 3), (0, 3)])
def test_two_exponential_midpoint_identity_is_exact(amplitudes):
    a, b = map(F, amplitudes)
    r, s = F(1, 2), F(1, 3)
    first, middle, last = a + b, a * r + b * s, a * r**2 + b * s**2
    assert middle**2 - first * last == -a * b * (r - s) ** 2


@pytest.mark.parametrize("phase", range(8))
def test_formal_necessary_table_satisfies_full_vector_balance_not_a_native_kernel(
    necessary, phase
):
    values = {
        name: float((bound.lo + bound.hi) / 2) for name, bound in necessary.items()
    }
    q = 0.99
    vertices = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / np.sqrt(3)
    base = np.empty((8, 3))
    base[::2], base[1::2] = vertices, 5 * vertices
    base = np.roll(base, -phase, axis=0)
    history = np.vstack([base, base[0]])
    state = FiniteMemoryState(
        x=history[0],
        memory=history,
        weights=exponential_memory_weights(1 - q, len(history), memory_mass=1),
    )
    positions, directions, weights = oriented_history_from_state(state, mode="unit")
    vector = vector_memory_force(history[0], positions, directions, weights, sigma=1)
    displacements = history[0] - positions
    distances = np.sum(displacements**2, axis=1)
    scalar = np.zeros(3)
    categories = np.array([8 / 3, 16, 88 / 3, 200 / 3])
    force_values = [values[name] for name in ("N", "R", "X", "F")]
    for age in range(1, 8):
        category = np.argmin(abs(categories - distances[age]))
        assert abs(categories[category] - distances[age]) < 1e-12
        scalar += values["s"] ** age * force_values[category] * displacements[age]
    # Independent native readout check; this four-value table is NOT installed.
    residual = scalar + values["C"] * vector / weights[0] - (base[-1] - base[0])
    assert np.linalg.norm(residual) < 5e-11
