"""Fixed formal FIFO derivatives, not native orbit or stability evaluations."""

import numpy as np
import pytest


S = np.array([[0, -1, 0], [1, 0, 0], [0, 0, -1]])
SPACE = np.eye(3)
EZ = SPACE[:, 2]
IDENTITY = np.eye(15)
S_ALL = np.kron(np.eye(5), S)
E = IDENTITY[:, 2]
T = np.tile(EZ, 5)


def _cross(vector):
    return np.cross(vector, SPACE).T


def _control(delayed_difference):
    # Derivative of a synthetic rigid-pose fit, not a Memory force.
    seed = np.array([1.0, 0.0, 0.3])
    sites = np.array([np.linalg.matrix_power(S, -age) @ seed for age in range(4)])
    inertia = np.sum(sites**2) * SPACE - sites.T @ sites
    blocks = np.zeros((5, 3, 3))
    for age, site in enumerate(sites):
        blocks[age] = SPACE / 4 - _cross(S @ seed) @ np.linalg.solve(
            inertia, _cross(site)
        )
    # The first and fifth sites coincide on the formal reference history.
    blocks[0] += delayed_difference * SPACE
    blocks[4] -= delayed_difference * SPACE
    full = np.vstack([np.hstack(blocks), IDENTITY[:12]])
    return np.vstack([sites, seed]), blocks, full


def _head_reduction(blocks):
    age_rotations = np.array([np.linalg.matrix_power(-S, -age) for age in range(5)])
    m = -S - np.einsum("aij,ajk->ik", blocks, age_rotations)
    v = EZ + np.einsum("a,aij,j->i", np.arange(5), blocks, EZ)
    return m, v, age_rotations


@pytest.mark.parametrize(("delayed_difference", "sign"), [(0, 1), (1, -1)])
def test_axial_derivative_agrees_across_bordered_map_projector_and_head_system(
    delayed_difference, sign
):
    positions, blocks, jac = _control(delayed_difference)
    w = np.cross(EZ, positions).ravel()
    linear = S_ALL.T @ jac
    two_step = linear @ linear - IDENTITY
    np.testing.assert_allclose(linear @ T, -T, atol=9e-16)
    np.testing.assert_allclose(linear @ w, w, atol=9e-16)
    assert np.linalg.matrix_rank(two_step, tol=1e-10) == 13

    first_kick = (S_ALL @ jac @ S_ALL.T) @ E
    two_step_kick = S_ALL.T @ S_ALL.T @ (first_kick + E)
    np.testing.assert_allclose(two_step_kick, (IDENTITY - linear) @ E, atol=9e-16)
    slice_basis = np.linalg.qr(np.column_stack([T, w]), mode="complete")[0][:, 2:]
    bordered = np.column_stack([two_step @ slice_basis, -w, -2 * T])
    tangent = np.linalg.solve(bordered, -two_step_kick)
    assert tangent[-2] == pytest.approx(0, abs=2e-15)

    left = np.linalg.lstsq(
        np.vstack([linear.T + IDENTITY, T]), np.r_[np.zeros(15), 1], rcond=None
    )[0]
    np.testing.assert_allclose(left @ linear, -left, atol=2e-15)
    assert left @ T == pytest.approx(1, abs=2e-15)
    chi = left @ E
    assert np.sign(chi) == sign
    assert tangent[-1] == pytest.approx(chi, rel=2e-14)

    m, v, age_rotations = _head_reduction(blocks)
    np.testing.assert_allclose(m @ EZ, 0, atol=7e-16)
    square = np.column_stack([m[:, :2], v])
    u_x, u_y, drift = np.linalg.solve(square, EZ)
    ratio = np.linalg.det(np.column_stack([m[:, :2], EZ])) / np.linalg.det(square)
    assert drift == pytest.approx(chi, rel=2e-14)
    assert ratio == pytest.approx(chi, rel=2e-14)

    ramp = (-np.arange(5)[:, None] * EZ).ravel()
    rotated = (age_rotations @ np.array([u_x, u_y, 0])).ravel()
    head_tangent = rotated + drift * ramp
    np.testing.assert_allclose(
        (linear + IDENTITY) @ head_tangent, E - drift * T, atol=2e-15
    )
    np.testing.assert_allclose(slice_basis.T @ head_tangent, tangent[:-2], atol=5e-15)


def test_geometrically_simple_translation_can_have_a_zero_response_denominator():
    _, blocks, _ = _control(0)
    _, uncompensated_v, _ = _head_reduction(blocks)
    _, singular_blocks, jac = _control(uncompensated_v[2] / 4)
    m, v, _ = _head_reduction(singular_blocks)
    shifted = S_ALL.T @ jac + IDENTITY
    square = np.column_stack([m[:, :2], v])
    assert np.linalg.matrix_rank(shifted, tol=1e-10) == 14
    assert np.linalg.matrix_rank(shifted @ shifted, tol=1e-10) <= 13
    assert np.linalg.matrix_rank(square, tol=1e-10) == 2
    assert abs(np.linalg.det(np.column_stack([m[:, :2], EZ]))) > 0.9
