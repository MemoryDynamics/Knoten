"""Exact controls for the exclusion algebra; no native orbit is evaluated."""

from fractions import Fraction as F

import numpy as np
import pytest


@pytest.mark.parametrize(
    ("f", "g", "q"),
    [(F(2, 5), F(4, 5), F(3, 4)), (F(3, 4), F(1, 2), F(2, 3))],
)
def test_normal_threshold_factorizes_on_off_family_coefficients(f, g, q):
    assert f <= g * g or g <= f  # Neither triple defines the positive family.
    s = q * g * (g - f * q) / (f * (1 - g * q))
    delta = s**2 * (1 - g * q) - q**2 * (f - g * q)
    numerator = f**3 * (1 - g * q) - g**2 * (g - f * q) ** 2
    assert g * q**3 - delta == f * q**2 - s**2 * (1 - g * q)
    assert g * q**3 - delta == q**2 * numerator / (f**2 * (1 - g * q))


def test_synthetic_threshold_ratio_has_the_predicted_sense():
    # Formal exponents A=2, b=1, c=1 cannot occur together in the family.
    def formal_ratio(x):
        return x * (1 - 1 / x) ** 2 / (1 - 1 / x**2)

    assert formal_ratio(F(2)) == F(2, 3) < 1
    assert formal_ratio(F(3)) == F(3, 2) > 1


def test_trace_cutoffs_follow_from_exact_rational_bounds():
    radial_cutoff = F(8, 267)
    assert -F(2, 3) + F(25, 4) * radial_cutoff == -16 * radial_cutoff
    height_cutoff = F(5, 4)
    assert F(11, 6) - 4 * height_cutoff < 0
    assert F(11, 6) - 8 * height_cutoff == -F(49, 6) < -8


def test_aspect_cutoff_couples_two_exclusions_without_a_trial_orbit():
    aspect_floor = F(999, 4000)
    max_scaled_radius = F(5, 4) / aspect_floor
    max_b = 1 - 2 * aspect_floor + F(1, 4)
    max_c = 2 - 8 * aspect_floor
    assert max_b * max_scaled_radius < 4
    assert max_c * max_scaled_radius == F(10, 999) < F(1, 81)


def test_formal_normal_collision_leaves_only_linear_translation_drift():
    normal = np.vstack([[1, 0, 0, 1, -1], np.eye(5, dtype=int)[:4]])
    full = np.linalg.matrix_power(normal, 4)
    residual = np.array([1, 0, 0, 0, -1])
    translation = np.ones(5, dtype=int)
    np.testing.assert_array_equal(
        full - np.eye(5, dtype=int), np.outer(translation, residual)
    )
    np.testing.assert_array_equal(residual @ full, residual)
    np.testing.assert_array_equal(full @ translation, translation)
