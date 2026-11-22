"""Fixed kernel and covariance checks, not a pair or candidate trajectory."""

import numpy as np
import pytest

from emergenz_knoten.kernels import double_gaussian_gradient


@pytest.mark.parametrize("scale", [0.5, 0.125, 0.03125])
def test_broadened_native_cross_kernel_has_quadratic_age_remainder(scale):
    receiver = np.array([0.44, -0.24, 0.18])
    sender = np.array([-0.31, 0.15, 0.23])
    offsets = np.array(
        [[0, 0, 0], [-0.22, 0.11, 0.14], [-0.41, -0.02, 0.17], [0.08, 0.13, -0.18]]
    )
    weights = np.array([0.4, 0.16, 0.064, 0.0256])
    rep, att = 0.6, 1.2
    rep_width, att_width = 0.77, 1.31
    microscopic = double_gaussian_gradient(
        receiver / scale,
        sender / scale + offsets,
        weights,
        amplitude_rep=rep,
        amplitude_att=att,
        sigma_rep=rep_width / scale,
        sigma_att=att_width / scale,
    )
    macro = {
        "amplitude_rep": rep,
        "amplitude_att": att,
        "sigma_rep": rep_width,
        "sigma_att": att_width,
    }
    resolved = scale * double_gaussian_gradient(
        receiver, sender + scale * offsets, weights, **macro
    )
    collapsed = scale * double_gaussian_gradient(
        receiver, sender[None, :], np.array([weights.sum()]), **macro
    )
    np.testing.assert_allclose(microscopic, resolved, atol=2e-16, rtol=2e-15)
    hessian_bound = rep / rep_width**2 + att / att_width**2
    budget = scale**2 * hessian_bound * (weights @ np.linalg.norm(offsets, axis=1))
    assert 0 < np.linalg.norm(microscopic - collapsed) <= budget


@pytest.mark.parametrize("diffusion", [(0.3, 0.9), (0.4, 0.6)])
def test_drift_free_center_and_relative_noise_have_distinct_conditions(diffusion):
    c1, c2 = 0.4, 1.2
    # A single coordinate; independent copies give the spatial identity tensor.
    change = np.array([[c2 / (c1 + c2), c1 / (c1 + c2)], [1, -1]])
    interaction = np.array([-c1, c2])
    np.testing.assert_allclose(change @ interaction, [0, -(c1 + c2)], atol=2e-16)
    assert np.mean(interaction) != 0
    covariance = change @ np.diag(diffusion) @ change.T
    a1, a2 = diffusion
    assert covariance[1, 1] == pytest.approx(a1 + a2)
    assert covariance[0, 1] == pytest.approx((c2 * a1 - c1 * a2) / (c1 + c2))
    if a1 / c1 == pytest.approx(a2 / c2):
        assert covariance[0, 1] == pytest.approx(0, abs=1e-16)
    else:
        assert abs(covariance[0, 1]) > 0.1
