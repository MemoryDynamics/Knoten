"""Fixed controls for the delayed reference; no native trajectory."""

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from experiments.current.reference.fifo_4d_delayed_spin import (
    AXIS,
    BASIS,
    STEP,
    coherent_history,
    delayed_step,
    frame_readout,
)


def test_signed_replay_shifts_every_age_and_returns_at_eight_not_four():
    initial = np.arange(16.0).reshape(4, 4)
    history = initial
    for step in range(1, 9):
        updated = delayed_step(history)
        np.testing.assert_array_equal(updated[1:], history[:-1])
        np.testing.assert_array_equal(updated[0], -history[-1])
        assert np.sum(updated**2) == np.sum(initial**2)
        if step == 4:
            np.testing.assert_array_equal(updated, -initial)
        if step < 8:
            assert not np.array_equal(updated, initial)
        history = updated
    np.testing.assert_array_equal(history, initial)


@pytest.mark.parametrize("axis", [AXIS, [0, 1, 0], [2, -1, 4]])
def test_coherent_replay_rotates_the_whole_readout_frame_about_an_oblique_axis(axis):
    np.testing.assert_array_equal(BASIS.T @ BASIS, np.eye(4))
    axis = np.asarray(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)
    initial = coherent_history(axis)
    history = initial
    for step in range(9):
        spatial_rotation = Rotation.from_rotvec(step * STEP * axis).as_matrix()
        for item, reference in zip(history, initial, strict=True):
            np.testing.assert_allclose(
                frame_readout(item),
                spatial_rotation @ frame_readout(reference),
                rtol=0,
                atol=3e-15,
            )
        if step == 4:
            np.testing.assert_array_equal(history, -initial)
        if step == 8:
            np.testing.assert_array_equal(history, initial)
        history = delayed_step(history)


def test_antiperiodicity_alone_does_not_imply_a_rotating_3d_frame():
    initial = np.tile(BASIS[:, 0], (4, 1))
    history = initial
    for _ in range(8):
        history = delayed_step(history)
        np.testing.assert_array_equal(frame_readout(history[0]), np.eye(3))


def test_frame_ignores_global_sign_but_reference_overlap_does_not():
    head = coherent_history()[2]
    np.testing.assert_array_equal(frame_readout(-head), frame_readout(head))
    assert (-head) @ head == pytest.approx(-1)
    assert head @ head == pytest.approx(1)
    with pytest.raises(ValueError, match="zero"):
        frame_readout(np.zeros(4))
