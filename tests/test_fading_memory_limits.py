"""Constructed measure identities, not stochastic or physical target runs."""

from fractions import Fraction
import math

import numpy as np
import pytest

from emergenz_knoten.kernels import double_gaussian_gradient, exponential_memory_weights


def _write(measure, point, q):
    result = {x: q * weight for x, weight in measure.items()}
    result[point] = result.get(point, Fraction(0)) + 1 - q
    return result


@pytest.mark.parametrize(
    "q,n,p", [(Fraction(1, 5), 1, 1), (Fraction(4, 5), 4, 2), (Fraction(4, 5), 7, 1)]
)
def test_constant_writes_contract_dirac_transport_cost_exactly(q, n, p):
    initial = {-2: Fraction(1, 3), 3: Fraction(2, 3)}
    measure, target = initial.copy(), 1
    for _ in range(n):
        measure = _write(measure, target, q)
    assert sum(measure.values()) == 1
    assert measure[target] == 1 - q**n
    for x in initial:
        assert measure[x] == q**n * initial[x]
    # The only coupling to a Dirac measure moves every source point to target.
    cost = sum(weight * abs(x - target) ** p for x, weight in measure.items())
    initial_cost = sum(weight * abs(x - target) ** p for x, weight in initial.items())
    assert cost == q**n * initial_cost


def test_common_prefix_contracts_signed_measure_exactly_not_actual_trajectories():
    q = Fraction(4, 5)
    initial_a = {-2: Fraction(1, 3), 3: Fraction(2, 3)}
    initial_b = {-1: Fraction(2, 5), 4: Fraction(3, 5)}
    a, b, prefix = initial_a.copy(), initial_b.copy(), [1, -3, 4]
    for point in prefix:
        a, b = _write(a, point, q), _write(b, point, q)
    for x in a.keys() | b.keys():
        assert a.get(x, 0) - b.get(x, 0) == q ** len(prefix) * (
            initial_a.get(x, 0) - initial_b.get(x, 0)
        )


def test_native_gaussian_force_remembers_common_prefix_tail_with_same_factor():
    alpha, n = 0.2, 3
    q = 1 - alpha
    a = np.array([[-0.2, 0.4], [0.6, -0.1]])
    b = np.array([[0.3, -0.2], [-0.1, 0.5]])
    weights = np.array([0.4, 0.6])
    prefix = np.array([[0.1, 0.0], [0.2, 0.1], [-0.2, -0.1]])
    updated_weights = np.r_[exponential_memory_weights(alpha, n), q**n * weights]
    kwargs = dict(sigma_rep=1.0, sigma_att=3.0, amplitude_rep=1, amplitude_att=35)
    for probe in (np.array([0.3, 0.2]), np.array([-0.4, 0.1])):
        before = double_gaussian_gradient(probe, a, weights, **kwargs)
        before -= double_gaussian_gradient(probe, b, weights, **kwargs)
        after = double_gaussian_gradient(
            probe, np.vstack([prefix[::-1], a]), updated_weights, **kwargs
        )
        after -= double_gaussian_gradient(
            probe, np.vstack([prefix[::-1], b]), updated_weights, **kwargs
        )
        np.testing.assert_allclose(after, q**n * before, atol=2e-16, rtol=2e-14)


@pytest.mark.parametrize("horizon", [1, 4, 17])
def test_fixed_finite_horizon_loses_mass_as_alpha_vanishes(horizon):
    alpha = Fraction(1, 1000)
    exact_mass = 1 - (1 - alpha) ** horizon
    assert 0 < exact_mass <= horizon * alpha
    numerical_mass = exponential_memory_weights(float(alpha), horizon).sum()
    assert numerical_mass == pytest.approx(float(exact_mass), rel=2e-14)


def test_horizon_inversely_proportional_to_alpha_retains_nonzero_tail():
    alpha, horizon, c = 1 / 1000, 3000, 3
    tail = math.exp(horizon * math.log1p(-alpha))
    assert abs(tail - math.exp(-c)) < 8e-5
    mass = exponential_memory_weights(alpha, horizon).sum()
    assert mass == pytest.approx(1 - tail, abs=2e-15)
    assert tail > 0.04


def test_exact_tail_is_not_zero_when_binary64_underflows():
    exact_tail = Fraction(1, 2) ** 1100
    assert exact_tail > 0
    assert float(exact_tail) == 0.0
