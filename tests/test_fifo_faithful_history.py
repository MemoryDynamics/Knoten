"""Algebraic controls for exact historical samples in the mobile model."""

import numpy as np
import pytest

from experiments.current.reference.fifo_carrier_clock_cycle import MobileMemoryClock
from experiments.current.reference.fifo_reversible_carrier import carrier_map


def test_orthogonal_memory_drift_measures_momentum_outside_the_force_direction():
    model = MobileMemoryClock(weights=(0.2, 0, 0.8), record_mass=0.7)
    q = np.array([[0.5, 0.625], [0.2, -0.3], [0.7, 0], [0.25, 0.375], [0.25, 0.375]])
    p = np.array([[0.07, 0.03], [0.05, -0.02], [0.1, 0.4], [0.5, 0], [0, -0.4]])
    time = 0.7
    post_write_q, post_write_p = carrier_map(q, p)
    arrived_q, arrived_p = model.flight(post_write_q, post_write_p, time)
    np.testing.assert_array_equal(post_write_q[1], q[0])

    weights = np.array(model.weights)
    projector = np.eye(3) - np.outer(weights, weights) / (weights @ weights)
    drift = arrived_q[1:-1] - post_write_q[1:-1]
    impulse_defect = (model.record_mass / time) * (projector @ drift)
    assert np.linalg.norm(impulse_defect) > 0.1
    np.testing.assert_allclose(
        impulse_defect, projector @ post_write_p[1:-1], atol=2e-16
    )
    np.testing.assert_allclose(impulse_defect, projector @ arrived_p[1:-1], atol=2e-16)


@pytest.mark.parametrize(
    ("weights", "before", "after"),
    [
        ((4 / 7, 2 / 7, 1 / 7), 1, 2),
        ((1, 0, 0), 0, 1),
        ((0, 0, 1), 1, 0),
    ],
)
def test_exceptional_weights_raise_relative_energy_unless_impulses_are_zero(
    weights, before, after
):
    direction = np.array([0.3, -0.5])
    weights = np.array(weights)
    memory = before * weights[:, None] * direction
    carrier = after * weights[0] * direction
    head = -carrier - memory.sum(axis=0)
    momentum = np.vstack([head, memory, carrier])
    position = np.array([[0.4, 0.6], [0.2, -0.3], [0.7, 0], [0.2, 0.3], [0.2, 0.3]])
    written_q, written_p = carrier_map(position, momentum)
    np.testing.assert_array_equal(written_q[[0, -1]], position[[0, -1]])
    np.testing.assert_allclose(written_p[1:-1], after * weights[:, None] * direction)
    np.testing.assert_allclose(written_p.sum(axis=0), 0, atol=2e-16)

    relative_before = before + 2 * after * weights[0]
    relative_after = before + 3 * after * weights[0] + before * weights[-1]
    actual_jump = (
        np.square(written_p[0] - written_p[-1]).sum()
        - np.square(momentum[0] - momentum[-1]).sum()
    ) / 4
    expected = (relative_after**2 - relative_before**2) * (direction @ direction) / 4
    assert actual_jump == pytest.approx(expected)
    assert expected > 0
