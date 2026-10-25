"""Synthetic FIFO geometry controls; no target roots or stability measurements."""

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from emergenz_knoten.kernels import double_gaussian_gradient
from emergenz_knoten.rotating_wave import (
    double_gaussian_gradient_factor,
    finite_h_rotating_wave_components,
)
from emergenz_knoten.rotating_wave_stability import (
    circular_history,
    finite_memory_weights,
    native_fifo_step,
)


KERNEL = {
    "sigma_rep": 1.0,
    "sigma_att": 2.7,
    "amplitude_rep": 1.0,
    "amplitude_att": 3.9,
}
MEMORY = {"alpha": 0.13, "memory_mass": 1.2}
ETA = 0.21
THETA = 0.31


def _history(horizon=17):
    planar = circular_history(radius=1.1, theta=THETA, horizon=horizon)
    return np.column_stack((planar, np.zeros(horizon)))


def _frame(history):
    u, v = history[1] - history[0], history[2] - history[0]
    u_norm = np.linalg.norm(u)
    v_norm = np.linalg.norm(v)
    if min(u_norm, v_norm) == 0.0:
        raise ValueError("degenerate ordered triple")
    first = u / u_norm
    transverse = v - np.dot(v, first) * first
    transverse_norm = np.linalg.norm(transverse)
    if transverse_norm <= 1e-12 * v_norm:
        raise ValueError("degenerate ordered triple")
    second = transverse / transverse_norm
    return np.column_stack((first, second, np.cross(first, second)))


def _kernel_step(history):
    weights = finite_memory_weights(horizon=len(history), **MEMORY)
    gradient = double_gaussian_gradient(history[0], history, weights, **KERNEL)
    return np.vstack((history[0] - ETA * gradient, history[:-1]))


def _normal_block(history):
    weights = finite_memory_weights(horizon=len(history), **MEMORY)
    radii = np.linalg.norm(history[0] - history, axis=1)
    coefficients = (
        ETA * weights[1:] * double_gaussian_gradient_factor(radii[1:], **KERNEL)
    )
    block = np.zeros((len(history), len(history)))
    block[0, 0] = 1.0 - np.sum(coefficients)
    block[0, 1:] = coefficients
    block[1:, :-1] = np.eye(len(history) - 1)
    return block


@pytest.mark.parametrize("rotvec", [[0.2, -0.6, 0.8], [np.pi, 0, 0], [0, 0, 1.2]])
def test_ordered_frame_is_covariant_under_proper_rotation(rotvec):
    history = _history()
    rotation = Rotation.from_rotvec(rotvec).as_matrix()
    frame = _frame(history)
    transformed = 2.3 * history @ rotation.T + [1.3, -0.7, 0.4]
    np.testing.assert_allclose(_frame(transformed), rotation @ frame, atol=2e-14)
    np.testing.assert_allclose(frame.T @ frame, np.eye(3), atol=2e-14)
    assert np.linalg.det(frame) == pytest.approx(1.0)


def test_ordered_triple_has_explicit_frame_coordinate_inverse():
    history = _history()
    frame = _frame(history)
    u, v = history[1] - history[0], history[2] - history[0]
    a = np.dot(u, frame[:, 0])
    b = np.dot(v, frame[:, 0])
    c = np.dot(v, frame[:, 1])
    assert a > 0.0 and c > 0.0
    np.testing.assert_allclose(history[0] + a * frame[:, 0], history[1], atol=2e-15)
    np.testing.assert_allclose(
        history[0] + b * frame[:, 0] + c * frame[:, 1], history[2], atol=2e-15
    )


def test_opposite_planar_traversals_are_one_proper_rotation_orbit_in_3d():
    history = _history()
    ages = np.arange(len(history))
    opposite = np.column_stack(
        (1.1 * np.cos(THETA * ages), 1.1 * np.sin(THETA * ages), np.zeros(len(ages)))
    )
    rotation = np.diag([1.0, -1.0, -1.0])
    assert np.linalg.det(rotation) == 1.0
    np.testing.assert_allclose(history @ rotation.T, opposite, atol=2e-15)
    np.testing.assert_allclose(_frame(opposite), rotation @ _frame(history), atol=2e-14)


@pytest.mark.parametrize("triple", [np.zeros((3, 3)), np.diag([1.0, 0.0, 0.0])])
def test_frame_rejects_collapsed_or_collinear_triple(triple):
    with pytest.raises(ValueError, match="degenerate"):
        _frame(triple)


@pytest.mark.parametrize("fraction", [0.0, 0.25, 0.5, 0.75, 1.0])
def test_rotation_loop_contracts_in_full_fifo_space_with_fixed_endpoints(fraction):
    history = _history()
    angles = np.linspace(0.0, 2.0 * np.pi, 17)
    rotations = Rotation.from_rotvec(angles[:, None] * [0, 0, 1]).as_matrix()
    rotated = np.einsum("tij,hj->thi", rotations, history)
    contracted = fraction * history + (1.0 - fraction) * rotated
    np.testing.assert_allclose(contracted[0], history, atol=2e-15)
    np.testing.assert_allclose(contracted[-1], history, atol=2e-15)
    assert np.isfinite(contracted).all()
    if fraction == 1.0:
        np.testing.assert_allclose(
            contracted, np.broadcast_to(history, contracted.shape)
        )
    if fraction == 0.5:
        np.testing.assert_allclose(contracted[8], 0.0, atol=2e-15)
        # Use the exact collapsed point, not a roundoff-scale artificial frame.
        with pytest.raises(ValueError, match="degenerate"):
            _frame(np.zeros_like(history))


def test_collapsed_history_is_a_regular_native_fixed_point():
    planar = np.tile([0.3, -0.4], (7, 1))
    advanced = native_fifo_step(planar, eta=ETA, **MEMORY, **KERNEL)
    np.testing.assert_array_equal(advanced, planar)
    spatial = np.column_stack((planar, np.full(len(planar), 0.8)))
    np.testing.assert_array_equal(_kernel_step(spatial), spatial)


@pytest.mark.parametrize("turns", [1, 2])
def test_quaternion_lift_sign_is_not_a_changed_fifo_state(turns):
    angles = np.linspace(0.0, turns * 2.0 * np.pi, 33)
    rotations = Rotation.from_rotvec(angles[:, None] * [0, 0, 1])
    lift = rotations.as_quat(canonical=False)
    assert np.all(np.sum(lift[:-1] * lift[1:], axis=1) > 0.0)
    np.testing.assert_allclose(lift[-1], (-1.0) ** turns * lift[0], atol=1e-15)
    np.testing.assert_allclose(rotations[-1].as_matrix(), np.eye(3), atol=2e-15)
    np.testing.assert_allclose(rotations[-1].apply(_history()), _history(), atol=3e-15)


@pytest.mark.parametrize("tilt", [0.0, 0.4, np.pi / 2.0])
def test_four_dimensional_frame_loop_contracts_without_shape_collapse(tilt):
    angles = np.linspace(0.0, 2.0 * np.pi, 33)
    first = np.column_stack(
        (
            np.cos(tilt) * np.cos(angles),
            np.cos(tilt) * np.sin(angles),
            np.full(len(angles), np.sin(tilt)),
            np.zeros(len(angles)),
        )
    )
    second = first[:, [1, 0, 3, 2]] * [-1, 1, 1, -1]
    frames = np.stack((first, second), axis=2)
    grams = np.einsum("tdi,tdj->tij", frames, frames)
    np.testing.assert_allclose(
        grams, np.broadcast_to(np.eye(2), grams.shape), atol=1e-15
    )
    np.testing.assert_allclose(frames[0], frames[-1], atol=1e-15)
    planar = _history()[:, :2]
    histories = np.einsum("tdi,hi->thd", frames, planar)
    chords = histories - histories[:, :1]
    np.testing.assert_allclose(
        np.linalg.norm(chords, axis=2),
        np.broadcast_to(np.linalg.norm(planar - planar[0], axis=1), chords.shape[:2]),
        atol=2e-15,
    )
    if tilt == np.pi / 2.0:
        np.testing.assert_allclose(
            histories, np.broadcast_to(histories[0], histories.shape), atol=1e-15
        )


@pytest.mark.parametrize("rotvec", [[0.3, 0.7, -0.4], [np.pi, 0, 0]])
def test_native_planar_step_embeds_covariantly_in_3d(rotvec):
    history = _history()
    planar_next = native_fifo_step(history[:, :2], eta=ETA, **MEMORY, **KERNEL)
    spatial_next = _kernel_step(history)
    np.testing.assert_allclose(spatial_next[:, :2], planar_next, atol=2e-15)
    np.testing.assert_array_equal(spatial_next[:, 2], 0.0)
    rotation = Rotation.from_rotvec(rotvec).as_matrix()
    offset = np.asarray([0.8, -0.2, 1.7])
    np.testing.assert_allclose(
        _kernel_step(history @ rotation.T + offset),
        spatial_next @ rotation.T + offset,
        atol=3e-15,
    )


@pytest.mark.parametrize("horizon", [3, 7, 17])
def test_normal_block_matches_full_production_kernel_derivative(horizon):
    history = _history(horizon)
    block = _normal_block(history)
    step = 1e-6
    measured = np.zeros_like(block)
    for column in range(horizon):
        direction = np.zeros_like(history)
        direction[column, 2] = 1.0
        derivative = (
            _kernel_step(history + step * direction)
            - _kernel_step(history - step * direction)
        ) / (2.0 * step)
        measured[:, column] = derivative[:, 2]
        np.testing.assert_allclose(derivative[:, :2], 0.0, atol=1e-12)
    np.testing.assert_allclose(measured, block, rtol=1e-11, atol=1e-13)


@pytest.mark.parametrize("horizon", [3, 9, 17])
def test_normal_symmetry_defect_equals_unforced_circle_balance(horizon):
    history = _history(horizon)
    block = _normal_block(history)
    np.testing.assert_allclose(block @ np.ones(horizon), 1.0, atol=2e-15)
    components = finite_h_rotating_wave_components(
        radius=1.1, theta=THETA, horizon=horizon, **MEMORY, **KERNEL
    )
    residual = (
        np.cos(THETA)
        - 1.0
        + ETA * components.radial
        + 1j * (np.sin(THETA) + ETA * components.tangential)
    )
    assert abs(residual) > 0.01  # Deliberately not a root or a target evaluation.
    mode = np.exp(-1j * THETA * np.arange(horizon))
    defect = block @ mode - np.exp(1j * THETA) * mode
    expected = np.zeros(horizon, dtype=complex)
    expected[0] = -residual
    np.testing.assert_allclose(defect, expected, atol=2e-15)
