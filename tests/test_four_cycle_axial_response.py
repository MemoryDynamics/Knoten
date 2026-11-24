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


def _pose_tangents(positions):
    return np.vstack([np.column_stack([SPACE, -_cross(point)]) for point in positions])


def _project_period_response(positions, jac, phase_rotation=S):
    frame = np.kron(np.eye(5), phase_rotation)
    linear = frame.T @ jac
    period = np.linalg.matrix_power(linear, 4)
    head = IDENTITY[:, :3]
    port = sum(
        np.linalg.matrix_power(linear, k)
        @ head
        @ np.linalg.matrix_power(phase_rotation, k)
        for k in range(4)
    )
    pose = _pose_tangents(positions)
    complement = np.linalg.qr(pose, mode="complete")[0][:, 6:]
    bordered = np.column_stack([(period - IDENTITY) @ complement, 4 * pose])
    response = np.linalg.solve(bordered, port)[-6:]
    return period, port, response


@pytest.mark.parametrize("delayed_difference", [0, 1])
def test_general_response_has_two_distinct_transverse_channels(delayed_difference):
    positions, blocks, jac = _control(delayed_difference)
    _, port, response = _project_period_response(positions, jac)
    direct = np.zeros_like(port)
    for phase in range(4):
        rotation = np.linalg.matrix_power(S_ALL, phase)
        direct = (rotation @ jac @ rotation.T) @ direct + IDENTITY[:, :3]
    np.testing.assert_allclose(port, direct, atol=3e-15)
    translation, rotation = response[:3], response[3:]
    np.testing.assert_allclose(translation @ S, S @ translation, atol=2e-14)
    np.testing.assert_allclose(rotation @ S, -S @ rotation, atol=2e-14)
    np.testing.assert_allclose(rotation, rotation.T, atol=2e-14)
    assert abs(translation[1, 0]) > 0.01
    assert np.linalg.det(rotation[:2, :2]) < -0.0001

    m, v, _ = _head_reduction(blocks)
    axial = np.linalg.solve(np.column_stack([m[:, :2], v]), EZ)[-1]
    np.testing.assert_allclose(response[:, 2], np.r_[0, 0, axial, 0, 0, 0], atol=2e-14)


def test_phase_invariance_and_mirror_odd_translation():
    positions, _, jac = _control(0)
    _, _, original = _project_period_response(positions, jac)
    mirror = np.diag([1, -1, 1])
    for transform in [S, S @ S, S.T, mirror]:
        frame = np.kron(np.eye(5), transform)
        _, _, measured = _project_period_response(
            positions @ transform.T, frame @ jac @ frame.T, transform @ S @ transform.T
        )
        expected = np.vstack(
            [
                transform @ original[:3] @ transform.T,
                np.linalg.det(transform) * transform @ original[3:] @ transform.T,
            ]
        )
        np.testing.assert_allclose(measured, expected, atol=2e-15)
        factor = -1 if np.array_equal(transform, mirror) else 1
        assert measured[1, 0] == pytest.approx(factor * original[1, 0], abs=2e-15)
        if factor == 1:
            np.testing.assert_allclose(measured, original, atol=2e-15)


def test_phase_average_removes_rotational_motion_of_an_equivariant_landmark():
    positions, _, jac = _control(0)
    period, port, response = _project_period_response(positions, jac)
    pose = _pose_tangents(positions)
    complement = np.linalg.qr(pose, mode="complete")[0][:, 6:]
    assert np.max(np.abs(np.linalg.eigvals(complement.T @ period @ complement))) < 0.5
    kick = np.array([0.5, -0.3, 0.2])
    expected_translation, expected_rotation = (response @ kick).reshape(2, 3)
    # Difference of two formal linear responses one cycle apart.
    increment = np.linalg.matrix_power(period, 32) @ port @ kick / 4
    marker = np.array([0.21, -0.13, 0.08])
    marker_rates = []
    for phase in range(4):
        symmetry = np.linalg.matrix_power(S, phase)
        full = np.kron(np.eye(5), symmetry)
        phase_pose = _pose_tangents(positions @ symmetry.T)
        np.testing.assert_allclose(
            increment,
            phase_pose @ np.r_[expected_translation, expected_rotation],
            atol=4e-14,
        )
        center_rate = increment.reshape(5, 3)[:4].mean(axis=0)
        np.testing.assert_allclose(center_rate, expected_translation, atol=4e-14)
        decoupled = np.linalg.lstsq(phase_pose, increment, rcond=None)[0]
        marker_rates.append(decoupled[:3] + np.cross(decoupled[3:], symmetry @ marker))
        increment = (full @ jac @ full.T) @ increment
    assert np.linalg.norm(marker_rates[0] - expected_translation) > 0.001
    np.testing.assert_allclose(
        np.mean(marker_rates, axis=0), expected_translation, atol=4e-14
    )
