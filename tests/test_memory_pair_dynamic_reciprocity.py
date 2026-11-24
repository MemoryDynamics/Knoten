"""Finite-history transfer identities with fixed synthetic controls."""

from fractions import Fraction as F

import numpy as np
import pytest

from emergenz_knoten.kernels import double_gaussian_gradient


def _weights(q):
    powers = [q**age for age in range(3)]
    return [power / sum(powers) for power in powers]


def _history_matrix(p, g, h, mu):
    count = len(p[0])
    matrix = np.zeros((2 * count, 2 * count), dtype=object)
    drive = np.zeros((2 * count, 2), dtype=object)
    points = np.zeros((2, 2 * count), dtype=object)
    centers = points.copy()
    for i in range(2):
        j = 1 - i
        head, other = i * count, j * count
        own_slice = slice(head, head + count)
        other_slice = slice(other, other + count)
        matrix[head, own_slice] = [g[i] * weight for weight in p[i]]
        matrix[head, head] += 1 - g[i] - h[i]
        matrix[head, other_slice] = [h[i] * weight for weight in p[j]]
        matrix[head + 1 : head + count, head : head + count - 1] = np.eye(
            count - 1, dtype=int
        )
        drive[head, i] = mu[i]
        points[i, head] = 1
        centers[i, own_slice] = p[i]
    return matrix, drive, points, centers


@pytest.mark.parametrize("z", [1.4, np.exp(0.61j), -0.5 + 0.8j])
@pytest.mark.parametrize("q_b", [F(1, 2), F(1, 3)])
def test_full_history_resolvent_agrees_with_both_reduced_transfers(z, q_b):
    p = [_weights(F(1, 2)), _weights(q_b)]
    g, h, mu = [F(1, 5), F(2, 7)], [F(1, 4), F(1, 6)], [F(3), F(2)]
    matrix, drive, points, centers = _history_matrix(p, g, h, mu)
    state = np.linalg.solve(z * np.eye(6) - matrix.astype(float), drive.astype(float))
    filters = np.array([sum(p_i[age] * z**-age for age in range(3)) for p_i in p])
    g, h, mu = (np.asarray(coeffs, dtype=float) for coeffs in (g, h, mu))
    diagonal = z - (1 - g - h) - g * filters
    reduced = np.array(
        [[diagonal[0], -h[0] * filters[1]], [-h[1] * filters[0], diagonal[1]]]
    )
    expected = np.linalg.solve(reduced, np.diag(mu))
    point_transfer = points.astype(float) @ state
    center_transfer = centers.astype(float) @ state
    np.testing.assert_allclose(point_transfer, expected, atol=2e-15)
    np.testing.assert_allclose(center_transfer, filters[:, None] * expected, atol=2e-15)
    np.testing.assert_allclose(center_transfer, center_transfer.T, atol=2e-15)
    if q_b == F(1, 2):
        np.testing.assert_allclose(point_transfer, point_transfer.T, atol=2e-15)
    else:
        assert abs(point_transfer[0, 1] - point_transfer[1, 0]) > 1e-3


def test_same_impulses_give_exact_center_symmetry_and_point_asymmetry():
    p = [_weights(F(1, 2)), _weights(F(1, 3))]
    g, h, mu = [F(1, 5), F(2, 7)], [F(1, 4), F(1, 6)], [F(3), F(2)]
    matrix, drive, points, centers = _history_matrix(p, g, h, mu)
    response_after_two = points @ matrix @ drive
    assert response_after_two[0, 1] - response_after_two[1, 0] == h[0] * mu[1] * (
        p[1][0] - p[0][0]
    )
    for lag in range(1, 9):
        response = centers @ np.linalg.matrix_power(matrix, lag - 1) @ drive
        np.testing.assert_array_equal(response, response.T)


def test_matching_first_point_response_cannot_match_next_age_coefficient():
    p = [_weights(F(1, 2)), _weights(F(1, 3))]
    g, h = [F(1, 5), F(2, 7)], [F(1, 4), F(1, 6)]
    mu = [h[0] * p[1][0], h[1] * p[0][0]]
    matrix, drive, points, _ = _history_matrix(p, g, h, mu)
    first = points @ matrix @ drive
    second = points @ matrix @ matrix @ drive
    assert first[0, 1] == first[1, 0] != 0
    assert second[0, 1] - second[1, 0] == first[0, 1] * (F(1, 3) - F(1, 2))


def test_native_gradient_linearization_at_a_prescribed_separated_stationary_pair():
    # A completely specified kernel control, not a selected dynamical orbit.
    axis = np.array([0.6, 0.8])
    base = np.array([axis, np.zeros(2)])
    p = np.asarray([_weights(0.5), _weights(1 / 3)])
    weights = np.array([2.0, 3.0])[:, None] * p
    eta, chi = [0.19, 0.11], 0.2
    self_kernel = dict(sigma_rep=1, sigma_att=1, amplitude_rep=0, amplitude_att=1)
    cross_kernel = dict(
        sigma_rep=1, sigma_att=2, amplitude_rep=1, amplitude_att=4 * np.exp(-3 / 8)
    )
    history = np.repeat(base[:, None, :], 3, axis=1)
    tangent = np.array(
        [[[0.2, 0.3], [-0.1, 0.2], [0.1, 0.04]], [[0.04, 0.1], [0.3, -0.2], [0.5, 0.1]]]
    )

    def heads(y):
        return np.array(
            [
                y[i, 0]
                - eta[i]
                * double_gaussian_gradient(y[i, 0], y[i], weights[i], **self_kernel)
                - chi
                * double_gaussian_gradient(
                    y[i, 0], y[1 - i], weights[1 - i], **cross_kernel
                )
                for i in range(2)
            ]
        )

    np.testing.assert_allclose(heads(history), base, atol=1e-16)
    centers = np.einsum("ij,ijk->ik", p, tangent)
    cross_hessian = 0.75 * np.exp(-0.5) * np.outer(axis, axis)
    expected = np.array(
        [
            tangent[i, 0]
            - eta[i] * weights[i].sum() * (tangent[i, 0] - centers[i])
            - chi
            * weights[1 - i].sum()
            * (cross_hessian @ (tangent[i, 0] - centers[1 - i]))
            for i in range(2)
        ]
    )
    step = 1e-6
    derivative = (heads(history + step * tangent) - heads(history - step * tangent)) / (
        2 * step
    )
    np.testing.assert_allclose(derivative, expected, atol=2e-10)
