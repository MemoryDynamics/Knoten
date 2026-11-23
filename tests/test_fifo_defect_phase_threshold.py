"""Fixed closed histories for the six-phase bound and 4D sign witnesses."""

import numpy as np
import pytest

from emergenz_knoten.kernels import exponential_memory_weights
from emergenz_knoten.vector_memory import vector_gaussian_field


def _jacobian(z, points, directions, weights, sigma=1.0):
    offset = points - z
    coeff = weights * np.exp(-np.sum(offset**2, axis=1) / (2 * sigma**2))
    return (directions.T * coeff) @ offset / sigma**2


def _six_phase_fixture():
    e1, e2, e3, e4 = np.eye(4)
    points = np.stack((np.zeros(4), e1, e2, e3, e4, e2 + e3))
    v = np.array([1, 1, 0, -1, -1, 0])
    return points, v


def _six_phase_exact_root(points, v, weights, sigma):
    steps = points - np.roll(points, -1, axis=0)
    lengths = np.linalg.norm(steps, axis=1)
    circuit = v - np.roll(v, 1)
    np.testing.assert_array_equal(circuit @ points, 0)
    np.testing.assert_array_equal(v @ steps, 0)
    log_amp = np.log(weights / lengths) - np.sum(points**2, axis=1) / (2 * sigma**2)
    # This fixture's master function is log((1+s)/(1-s)).
    s = np.tanh((circuit @ log_amp) / 2)
    r = 1 + s * v
    design = np.column_stack((points / sigma**2, np.ones(6)))
    root = np.linalg.lstsq(design, np.log(r) - log_amp, rcond=None)[0][:4]
    directions = steps / lengths[:, None]
    np.testing.assert_allclose(
        vector_gaussian_field(root, points, directions, weights, sigma=sigma),
        0,
        atol=2e-15,
    )
    assert (
        np.linalg.slogdet(_jacobian(root, points, directions, weights, sigma))[0] == 1
    )
    return root, directions


@pytest.mark.parametrize("sigma", [0.8, 1.6])
def test_closed_six_deposits_with_unrestricted_positive_weights(sigma):
    points, v = _six_phase_fixture()
    _six_phase_exact_root(points, v, np.array([1.1, 0.3, 0.8, 0.9, 1.4, 0.5]), sigma)


@pytest.mark.parametrize("horizon", [6, 7, 13])
def test_longer_fifo_on_the_same_six_phases_only_changes_positive_weights(horizon):
    points, v = _six_phase_fixture()
    ages = np.arange(horizon) % 6
    weights = exponential_memory_weights(0.15, horizon)
    folded = np.bincount(ages, weights)
    sigma = 1.2
    root, directions = _six_phase_exact_root(points, v, folded, sigma)
    np.testing.assert_allclose(
        vector_gaussian_field(
            root, points[ages], directions[ages], weights, sigma=sigma
        ),
        0,
        atol=2e-15,
    )
    assert (
        np.linalg.slogdet(
            _jacobian(root, points[ages], directions[ages], weights, sigma)
        )[0]
        == 1
    )


@pytest.mark.parametrize("sign", [1, -1])
def test_4d_signed_core_with_native_weights_and_bahn_consistent_directions(sign):
    basis, _ = np.linalg.qr(np.eye(5)[:, :4] - np.eye(5)[:, -1:])
    inner = np.sqrt(5 / 4) * basis
    orientation = np.eye(4) + (sign - 1) * np.outer(inner[0], inner[0])
    points = np.empty((10, 4))
    points[::2] = inner
    points[1::2] = inner - 6 * (inner @ orientation.T)
    steps = points - np.roll(points, -1, axis=0)
    directions = steps / np.linalg.norm(steps, axis=1, keepdims=True)
    weights = exponential_memory_weights(0.001, 10)
    expected = 1.25 * np.exp(-0.5) * orientation

    np.testing.assert_allclose(directions[::2], inner @ orientation.T, atol=3e-16)
    assert np.min(np.linalg.norm(points[1::2], axis=1)) >= 5 - 3e-15

    # Fixed iterations of the analytically certified local contraction.
    z = np.zeros(4)
    for _ in range(64):
        value = vector_gaussian_field(z, points, directions, weights, sigma=1.0)
        z -= np.linalg.solve(expected, value / weights[0])
        assert np.linalg.norm(z) < 1 / 8
    np.testing.assert_allclose(
        vector_gaussian_field(z, points, directions, weights, sigma=1.0),
        0,
        atol=1e-15,
    )
    jac = _jacobian(z, points, directions, weights) / weights[0]
    assert np.linalg.norm(jac - expected, ord=2) < 1 / 2
    assert np.linalg.slogdet(jac)[0] == sign
    assert np.all((1 + 4 * inner @ z) / 5 > 0)
