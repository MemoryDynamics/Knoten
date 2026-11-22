"""Fixed scalar-field controls, not native FIFO trajectories."""

from math import pi

import numpy as np
import pytest
from scipy.integrate import quad

from experiments.current.reference.retarded_scalar_interferometer import (
    integrated_source_kernel,
    vacuum_dephasing,
)


def test_compact_balls_have_a_causal_start_and_exact_late_integral():
    radius, distance = 0.4, 2.2
    assert integrated_source_kernel(distance, radius, distance - 2 * radius) == 0
    intermediate = integrated_source_kernel(distance, radius, distance)
    assert 0 < intermediate < 0.01
    for duration in (3.1, 6.0):
        actual = integrated_source_kernel(distance, radius, duration)
        assert actual == pytest.approx((duration / distance - 1) / (4 * pi), abs=1e-16)


def test_retarded_delays_cancel_in_the_two_arm_phase_after_both_fronts():
    a, b, radius = 2.0, 3.0, 0.45
    for duration in (4.1, 7.5):
        difference = integrated_source_kernel(
            a, radius, duration
        ) - integrated_source_kernel(b, radius, duration)
        assert difference == pytest.approx(duration * (1 / a - 1 / b) / (4 * pi))


def test_phase_slope_and_stationary_force_share_the_same_scalar_potential():
    radius, distance, duration = 0.35, 2.7, 6.0
    gain = 1.4 * 0.6  # source and probe charges in this reference
    step = 1e-4

    def phase_slope(r):
        larger = integrated_source_kernel(r, radius, duration + step)
        smaller = integrated_source_kernel(r, radius, duration - step)
        return gain * (larger - smaller) / (2 * step)

    assert phase_slope(distance) == pytest.approx(gain / (4 * pi * distance), rel=1e-10)
    inward_force = (phase_slope(distance + step) - phase_slope(distance - step)) / (
        2 * step
    )
    assert inward_force == pytest.approx(-gain / (4 * pi * distance**2), rel=1e-6)


def test_vacuum_exponent_matches_direct_positive_spectral_quadrature():
    radius, separation, charge, duration = 0.6, 1.1, 0.8, 2.4

    def integrand(k):
        x = k * radius
        form = 3 * (np.sin(x) - x * np.cos(x)) / x**3
        return (
            form**2
            * (1 - np.sinc(k * separation / pi))
            * (1 - np.cos(k * duration))
            / k
        )

    direct = quad(integrand, 0, 100 / radius, epsabs=1e-10, limit=250)[0]
    direct *= charge**2 / (2 * pi**2)
    assert vacuum_dephasing(radius, separation, charge, duration) == pytest.approx(
        direct, abs=2e-8
    )


def test_long_hold_retains_nonzero_visibility_and_same_arm_has_no_dephasing():
    radius, separation, charge = 0.5, 0.9, 1.2
    asymptotic = vacuum_dephasing(radius, separation, charge)
    assert 0 < asymptotic < 1
    for duration in (1.0, 2.0, 16.0, 64.0):
        value = vacuum_dephasing(radius, separation, charge, duration)
        assert 0 < value < 2 * asymptotic
    late = vacuum_dephasing(radius, separation, charge, 64)
    assert late == pytest.approx(asymptotic, rel=2e-4)
    assert vacuum_dephasing(radius, 0, charge, 64) == 0


def test_short_hold_exponent_is_positive_and_quadratic():
    first = vacuum_dephasing(0.5, 0.9, 1.0, 0.003)
    second = vacuum_dephasing(0.5, 0.9, 1.0, 0.006)
    assert first > 0
    assert second / first == pytest.approx(4, rel=1e-3)
