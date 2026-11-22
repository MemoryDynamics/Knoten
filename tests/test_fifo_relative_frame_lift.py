"""Fixed frame schedules and the exact signed-replay control, no native run."""

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from experiments.current.reference.fifo_4d_delayed_spin import (
    coherent_history,
    delayed_step,
    frame_readout,
)
from experiments.current.reference.fifo_4d_spin_projection import direction_readout
from experiments.current.reference.fifo_relative_frame_lift import relative_frame_sign


def _opposite_paths():
    arms = []
    for axis in ([1, 0, 0], [-1, 0, 0]):
        history = coherent_history(axis)
        for _ in range(2):
            history = delayed_step(history)
        arms.append(history[2::-1])
    return arms


def _frame_path(history):
    return np.stack([frame_readout(entry) for entry in history])


def _axial_path(degrees):
    return Rotation.from_euler("x", degrees, degrees=True).as_matrix()


def test_opposite_exact_fifo_half_turns_have_same_ends_and_direction_but_negative_lift():
    a, b = _opposite_paths()
    frames_a, frames_b = _frame_path(a), _frame_path(b)
    np.testing.assert_allclose(frames_a[[0, -1]], frames_b[[0, -1]], atol=1e-15)
    assert np.linalg.norm(frames_a[1] - frames_b[1]) > 2
    directions = np.tile([1, 0, 0], (3, 1))
    np.testing.assert_allclose(direction_readout(a), directions, atol=1e-15)
    np.testing.assert_allclose(direction_readout(b), directions, atol=1e-15)
    assert relative_frame_sign(frames_a, frames_b) == -1
    assert relative_frame_sign(frames_a, _frame_path(-a)) == 1


def test_independent_constant_lab_frames_do_not_set_a_relative_sign():
    a, b = map(_frame_path, _opposite_paths())
    lab_a, lab_b = Rotation.from_rotvec([[0.2, 0.3, 1.1], [-0.8, 1.0, 0.6]]).as_matrix()
    assert relative_frame_sign(lab_a @ a, lab_b @ b) == -1


@pytest.mark.parametrize("error_degrees", [12, 31, 44])
def test_short_join_sign_is_stable_under_fixed_sample_errors(error_degrees):
    a, b = map(_frame_path, _opposite_paths())
    directions_a = np.array([[1, 0, 0], [-1, 0, 0], [1, 0, 0]])
    directions_b = np.array([[0, -1, 0], [0, 0, 1], [0, 1, 0]])
    errors = np.deg2rad(error_degrees)
    noise_a, noise_b = [
        Rotation.from_rotvec(errors * directions).as_matrix()
        for directions in (directions_a, directions_b)
    ]
    assert relative_frame_sign(noise_a @ a, noise_b @ b) == -1


def test_rejects_ambiguous_internal_step_and_ambiguous_endpoint_join():
    with pytest.raises(ValueError, match="step is ambiguous"):
        relative_frame_sign(_axial_path([0, 180]), _axial_path([0, 90]))
    with pytest.raises(ValueError, match="join is ambiguous"):
        relative_frame_sign(_axial_path([0, 90, 180]), _axial_path([0, 0, 0]))
    improper = _axial_path([0, 90]) @ np.diag([1, 1, -1])
    with pytest.raises(ValueError, match="proper orthogonal"):
        relative_frame_sign(improper, _axial_path([0, 90]))


def test_discarding_old_samples_erases_the_path_comparison():
    a, b = map(_frame_path, _opposite_paths())
    common = np.repeat(a[-1:], 2, axis=0)
    last_a, last_b = [np.concatenate((arm, common))[-3:] for arm in (a, b)]
    np.testing.assert_allclose(last_a, last_b, atol=1e-15)
    assert relative_frame_sign(last_a, last_b) == 1


def test_unresolved_full_turn_aliases_to_a_rest_path():
    turned = _axial_path([0, 90, 180, 270, 360])
    resting = np.repeat(np.eye(3)[None, ...], len(turned), axis=0)
    assert relative_frame_sign(turned, resting) == -1
    assert relative_frame_sign(turned[[0, -1]], resting[[0, -1]]) == 1
