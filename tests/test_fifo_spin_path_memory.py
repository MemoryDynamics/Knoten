"""Prescribed geometry controls; no candidate or controlled dynamics is evaluated."""

import math

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from emergenz_knoten.vector_memory import vector_gaussian_field


STEPS = 32
REFERENCE = np.array([[1, 0, 1], [0, 1, -1], [-1, 0, 1], [0, -1, -1]])


def _angles(times, turns):
    return math.tau * turns * np.clip(times / STEPS, 0, 1)


def _points(times, angles, height):
    points = REFERENCE[times % 4] * np.array([1, 1, height])
    angle = angles % math.tau
    c, s = np.cos(angle), np.sin(angle)
    x, y, z = np.moveaxis(points, -1, 0)
    return np.stack([c * x - s * y, s * x + c * y, z], axis=-1)


def _windows(times, turns, height, morph=1):
    stamps = times[:, None] - np.arange(5)
    angles = (1 - morph) * _angles(times[:, None], turns) + morph * _angles(
        stamps, turns
    )
    return _points(stamps, angles, height)


def _unit(vectors):
    return vectors / np.linalg.norm(vectors, axis=-1, keepdims=True)


def _frames(windows):
    head, middle, tail = np.moveaxis(windows[:, :3], 1, 0)
    first = _unit(head - tail)
    second = middle - (head + tail) / 2
    second = _unit(second - np.sum(first * second, axis=-1, keepdims=True) * first)
    return np.stack([first, second, np.cross(first, second)], axis=-1)


@pytest.mark.parametrize("turns", [0, 1, 2])
@pytest.mark.parametrize("height", [0.11, 0.42])
def test_phase_matched_frame_paths_lift_with_the_same_parity(turns, height):
    times = np.arange(STEPS + 5)
    reference = _frames(_windows(times, 0, height))
    ideal = Rotation.from_rotvec(_angles(times, turns)[:, None] * [0, 0, 1])
    delta = math.tau * turns / STEPS
    for morph in [0, 0.5, 1]:
        frames = _frames(_windows(times, turns, height, morph))
        relative = Rotation.from_matrix(frames @ reference.transpose(0, 2, 1))
        assert np.max((relative * ideal.inv()).magnitude()) < delta + math.log(2) / 2
        arcs = (relative[1:] * relative[:-1].inv()).magnitude()
        assert arcs.max() < 3 * delta + math.log(2)
        np.testing.assert_allclose(relative[[0, -1]].magnitude(), 0, atol=2e-15)
        lift = relative.as_quat()
        if lift[0, 3] < 0:
            lift[0] *= -1
        for i in range(1, len(lift)):
            if lift[i - 1] @ lift[i] < 0:
                lift[i] *= -1
        np.testing.assert_allclose(lift[-1], [0, 0, 0, (-1) ** turns], atol=2e-15)


@pytest.mark.parametrize("turns", [1, 2])
def test_shift_flushes_the_full_history_and_native_vector_readout(turns):
    times = np.arange(STEPS + 5)
    turned = _windows(times, turns, 0.17)
    baseline = _windows(times, 0, 0.17)
    np.testing.assert_array_equal(turned[1:, 1:], turned[:-1, :-1])
    assert not np.array_equal(turned[-2], baseline[-2])
    np.testing.assert_array_equal(turned[-1], baseline[-1])
    deposit_dirs = _unit(turned[:, :-1] - turned[:, 1:])
    unchanged_dirs = _unit(baseline[:, :-1] - baseline[:, 1:])
    np.testing.assert_array_equal(deposit_dirs[-1], unchanged_dirs[-1])
    weights = 0.4 * 0.6 ** np.arange(4)
    at = np.array([0.21, -0.31, 0.12])
    np.testing.assert_array_equal(
        vector_gaussian_field(at, turned[-1, :4], deposit_dirs[-1], weights, sigma=0.9),
        vector_gaussian_field(
            at, baseline[-1, :4], unchanged_dirs[-1], weights, sigma=0.9
        ),
    )


def _fading_distance(hold, turns, retention):
    # Earlier entries agree, so all nonzero terms of the infinite sum are here.
    times = np.arange(STEPS + hold, -2, -1)
    turned = _points(times, _angles(times, turns), 0.17)
    reference = _points(times, np.zeros_like(times), 0.17)
    delta = np.linalg.norm(turned[:-1] - reference[:-1], axis=1)
    delta += np.linalg.norm(
        _unit(turned[:-1] - turned[1:]) - _unit(reference[:-1] - reference[1:]), axis=1
    )
    return (1 - retention) * np.dot(retention ** np.arange(len(delta)), delta)


@pytest.mark.parametrize(("turns", "retention"), [(1, 0.45), (2, 0.87)])
def test_infinite_weighted_difference_decreases_exactly_by_the_age_factor(
    turns, retention
):
    initial = _fading_distance(0, turns, retention)
    assert initial > 0.01
    for hold in [1, 4, 12]:
        assert _fading_distance(hold, turns, retention) == pytest.approx(
            retention**hold * initial, rel=2e-14, abs=0
        )
