"""Fixed occupation and lag-index controls, not an interacting trajectory test."""

import math

import numpy as np
import pytest
from scipy.integrate import quad


@pytest.mark.parametrize("core", [0.7, 2.3])
def test_regularized_inverse_square_has_a_bounded_core_and_integrable_square(core):
    strength = 1.3

    def force(radius):
        return strength * radius / (radius**2 + core**2) ** 1.5

    integral = quad(
        lambda r: 4 * math.pi * r * r * force(r) ** 2, 0, math.inf, epsabs=2e-12
    )[0]
    assert force(0) == 0
    assert integral == pytest.approx(
        3 * math.pi**2 * strength**2 / (4 * core), rel=2e-13
    )
    for radius in [0, core / 2, core, 5 * core, 80 * core]:
        assert force(radius) <= 2 * strength / (radius + core) ** 2
    far = 1000 * core
    assert far**2 * force(far) == pytest.approx(strength, rel=2e-6)


@pytest.mark.parametrize(("dimension", "power"), [(3, 1.25), (4, 2), (3, 2)])
def test_density_cutoff_and_far_tail_bound_the_power_occupation(dimension, power):
    cycles, length = 48, 0.85
    radius = length * math.sqrt(cycles)
    area = 2 * math.pi ** (dimension / 2) / math.gamma(dimension / 2)
    peak = (math.tau * cycles) ** (-dimension / 2)

    def weighted_shell(r):
        return area * r ** (dimension - 1) * (1 + r / length) ** (-2 * power)

    occupation = (
        peak
        * quad(
            lambda r: weighted_shell(r) * math.exp(-(r**2) / (2 * cycles)),
            0,
            math.inf,
        )[0]
    )
    density_budget = peak * quad(weighted_shell, 0, radius)[0]
    tail_budget = (1 + radius / length) ** (-2 * power)
    assert 0 < occupation <= density_budget + tail_budget
    assert tail_budget <= cycles ** (-power)


def test_delayed_source_distance_requires_only_the_current_and_previous_cycle_marks():
    # These fixed dyadic offsets check indexing, not a prescribed solver path.
    starts = [0, 4, 12, 16]
    increments = (np.arange(96).reshape(2, 16, 3) % 17 - 8) / 16
    start_points = np.array([[75, -2, 3], [-45, 5, 12]])
    displacements = np.concatenate(
        [np.zeros((2, 1, 3)), np.cumsum(increments, axis=1)], axis=1
    )
    points = start_points[:, None, :] + displacements
    for m in [1, 2]:
        origin = starts[m - 1]
        for clock in range(starts[m], starts[m + 1]):
            for lag in range(5):
                delayed = clock - lag
                assert origin <= delayed <= clock
                for receiver, sender in [(0, 1), (1, 0)]:
                    shift = increments[receiver, origin:clock].sum(axis=0)
                    shift -= increments[sender, origin:delayed].sum(axis=0)
                    base = points[receiver, origin] - points[sender, origin]
                    np.testing.assert_array_equal(
                        points[receiver, clock] - points[sender, delayed], base + shift
                    )
