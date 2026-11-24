"""Exact rank, fixed write, and field checks; no native target runs."""

from fractions import Fraction

import numpy as np
import pytest

from emergenz_knoten.vector_memory import vector_gaussian_field
from experiments.current.reference.fifo_inverse_radial_pair import (
    BASIS_COLUMNS,
    EDGES,
    NUMERATORS,
    PERIOD,
    S_WEIGHTS,
    SCALE,
    V_WEIGHTS,
    integer_force_matrix,
    inverse_reference,
    phase_history,
    reference_head,
)


def _det_mod(matrix, prime):
    matrix = matrix.copy() % prime
    determinant = 1
    for i in range(len(matrix)):
        row = next(j for j in range(i, len(matrix)) if matrix[j, i] != 0)
        if row != i:
            determinant = -determinant
            matrix[[i, row]] = matrix[[row, i]]
        pivot = int(matrix[i, i])
        determinant = determinant * pivot % prime
        factors = matrix[i + 1 :, i] * pow(pivot, -1, prime) % prime
        matrix[i + 1 :] = (matrix[i + 1 :] - factors[:, None] * matrix[i]) % prime
    return determinant


def _helmert_coefficient(i, k):
    return int(i < k) - k * int(i == k)


def test_force_ranks_distance_separation_and_small_perturbations_are_exact():
    margin = Fraction(1, 400)
    squared = []
    for sign, numerators, determinant in zip(
        (1, -1), NUMERATORS, (23994, 6152), strict=True
    ):
        integer_matrix = integer_force_matrix(numerators)
        assert _det_mod(integer_matrix[:, BASIS_COLUMNS], 65537) == determinant
        for i, j in EDGES:
            squared.append(sum(int(x) ** 2 for x in numerators[i] - numerators[j]))
        for i, point in enumerate(numerators):
            for k, value in enumerate(point, 1):
                v = _helmert_coefficient(i // 2, k)
                if i % 2:
                    v = -5 * v + (12 if i == 1 else -3) * int(sign < 0)
                coord = Fraction(int(value), SCALE)
                if v == 0:
                    assert abs(coord) < margin
                    continue
                coord *= 1 if v > 0 else -1
                expected_sq = Fraction(5 * v**2, 4 * k * (k + 1))
                assert 0 < (coord - margin) < (coord + margin)
                assert (coord - margin) ** 2 < expected_sq < (coord + margin) ** 2
    assert len(set(squared)) == 90
    ordered = sorted(squared)
    assert min(b - a for a, b in zip(ordered[:-1], ordered[1:])) == 234034976171


@pytest.fixture(scope="module")
def profiles():
    return inverse_reference(), inverse_reference(slope=1e8)


@pytest.mark.parametrize("shape", [0, 1])
@pytest.mark.parametrize("phase", range(PERIOD))
def test_one_radial_profile_reproduces_both_sign_orbits_at_each_phase(
    profiles, shape, phase
):
    points = NUMERATORS[shape] / SCALE
    history = phase_history(points, phase)
    for profile in profiles:
        np.testing.assert_allclose(
            reference_head(history, profile), points[phase - 1], atol=1e-9, rtol=0
        )

    direction = np.sqrt(5 / (4 * np.arange(1, 5) * np.arange(2, 6)))
    orientation = np.eye(4) - 2 * shape * np.outer(direction, direction)
    expected = (5 / 4) * np.exp(-0.5) * orientation
    steps = history[:-1] - history[1:]
    p = steps / np.linalg.norm(steps, axis=1, keepdims=True)

    def field(z):
        return vector_gaussian_field(z, history[:-1], p, V_WEIGHTS, sigma=1.0)

    z = np.zeros(4)
    for _ in range(64):
        z -= np.linalg.solve(expected, field(z) / V_WEIGHTS[0])
    assert np.linalg.norm(z) < 1 / 8
    np.testing.assert_allclose(field(z), 0, atol=2e-16)
    delta = history[:-1] - z
    coeff = V_WEIGHTS * np.exp(-0.5 * np.einsum("ij,ij->i", delta, delta))
    jac = (p.T * coeff) @ delta / V_WEIGHTS[0]
    assert np.linalg.norm(jac - expected, ord=2) < 0.55
    assert np.linalg.slogdet(jac)[0] == 1 - 2 * shape

    tangent = history[0] - history[:-1]
    np.linalg.cholesky(2 * (tangent.T * S_WEIGHTS) @ tangent)


def test_adding_force_slope_keeps_all_fitted_values_but_changes_the_local_response(
    profiles,
):
    flat, steep = profiles
    np.testing.assert_array_equal(flat(flat.distances_squared), flat.values)
    np.testing.assert_array_equal(steep(flat.distances_squared), flat.values)
    assert flat.half_width == pytest.approx(7.801165872e-6, rel=2e-8)
    shifted = flat.distances_squared + flat.half_width / 1024
    delta = shifted - flat.distances_squared
    q = (delta / flat.half_width) ** 2
    expected_change = steep.slope * delta * np.exp(-q / (1 - q))
    np.testing.assert_allclose(
        steep(shifted) - flat(shifted), expected_change, atol=2e-12
    )
