"""Scalar action readouts on prescribed separated arms, not a target trajectory."""

import numpy as np
import pytest

from emergenz_knoten.kernels import gaussian_potential


def _arm_readout(hold):
    sigma, height, step = 1.3, 0.75, 0.25
    weights = np.array([0.5, 0.25, 0.125, 0.0625])
    ages = np.arange(len(weights))
    times = np.arange(hold + ages[-1])

    def path(n, arm_height):
        return np.stack(
            (n * 0.125, np.zeros_like(n), arm_height * ((0 <= n) & (n < hold))),
            axis=-1,
        )

    def signal(n, arm_height):
        points = path(n - ages, arm_height)
        return gaussian_potential(points[0], points, weights, sigma=sigma)

    readouts = np.array([signal(n, height) - signal(n, 0) for n in times])
    lipschitz = np.exp(-0.5) / sigma
    bound = 2 * height * step * lipschitz * (ages @ weights)
    assert abs(step * readouts.sum()) <= bound
    np.testing.assert_array_equal(readouts[ages[-1] : hold], 0)
    heights = path(times, height)[:, 2]
    # Normalized known-law control: m*g/hbar=1, with any common potential offset.
    external_action = -step * np.sum((2 + heights) - 2)
    return step * readouts.sum(), external_action, -step * height * hold


@pytest.mark.parametrize("hold", [8, 64, 128])
def test_self_action_saturates_but_shared_affine_potential_phase_grows(hold):
    self_action, external_action, expected = _arm_readout(hold)
    short_self, _, _ = _arm_readout(4)
    assert self_action < 0
    assert self_action == pytest.approx(short_self, abs=1e-15)
    assert external_action == pytest.approx(expected, abs=1e-15)
