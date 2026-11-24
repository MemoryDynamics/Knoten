"""Fixed closed histories for the six-phase bound and 4D sign witnesses."""

import numpy as np
import pytest

from emergenz_knoten.kernels import exponential_memory_weights, gaussian_gradient
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


def _two_shell_geometry(sign):
    basis, _ = np.linalg.qr(np.eye(5)[:, :4] - np.eye(5)[:, -1:])
    inner = np.sqrt(5 / 4) * basis
    orientation = np.eye(4) + (sign - 1) * np.outer(inner[0], inner[0])
    points = np.empty((10, 4))
    points[::2] = inner
    points[1::2] = inner - 6 * (inner @ orientation.T)
    return points, inner, orientation


@pytest.mark.parametrize("phase", range(10))
@pytest.mark.parametrize("sign", [1, -1])
def test_4d_signed_core_at_every_prepared_phase(sign, phase):
    points, inner, orientation = _two_shell_geometry(sign)
    steps = points - np.roll(points, -1, axis=0)
    directions = steps / np.linalg.norm(steps, axis=1, keepdims=True)
    weights = exponential_memory_weights(0.001, 10)
    expected = 1.25 * np.exp(-0.5) * orientation

    np.testing.assert_allclose(directions[::2], inner @ orientation.T, atol=3e-16)
    assert np.min(np.linalg.norm(points[1::2], axis=1)) >= 5 - 3e-15
    points = np.roll(points, -phase, axis=0)
    directions = np.roll(directions, -phase, axis=0)

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


def test_single_affine_eight_phase_recurrence_reduces_to_positive_moments():
    theta = 2 * np.pi * np.arange(8) / 8
    circle = np.column_stack(
        (np.cos(theta), np.sin(theta), np.cos(3 * theta), np.sin(3 * theta))
    )
    embedding = np.array(
        [[1, 0.4, 0, 0], [0, 0.7, 0, 0], [0.1, 0, 1.2, 0], [0, 0, 0, 0.8]]
    )
    points = circle @ embedding.T
    tail = np.roll(points, -1, axis=0)
    affine = np.linalg.lstsq(points, tail, rcond=None)[0].T
    steps = points - tail
    linear = np.eye(4) - affine
    np.testing.assert_allclose(steps, points @ linear.T, atol=2e-15)
    lengths = np.linalg.norm(steps, axis=1)
    directions = steps / lengths[:, None]
    desired_root = np.array([0.2, -0.1, 0.4, -0.3])
    weights = lengths * np.exp(np.sum((points - desired_root) ** 2, axis=1) / 2)
    field = vector_gaussian_field(desired_root, points, directions, weights, sigma=1.0)
    np.testing.assert_allclose(field, 0, atol=2e-15)
    jac = _jacobian(desired_root, points, directions, weights)
    np.testing.assert_allclose(jac, linear @ (points.T @ points), atol=9e-15)
    assert np.linalg.slogdet(jac)[0] == 1


def test_negative_witness_far_phase_vector_has_nonmonotone_tangent_coefficients():
    points, inner, _ = _two_shell_geometry(-1)
    axis = inner[0]
    tangent = np.eye(4) - np.outer(axis, axis) / (axis @ axis)
    w = inner[1:] @ tangent
    q = 0.999
    t = q**2
    k = np.exp(-107 / 4) / q
    b = np.exp(-50) / np.sqrt(47 / 2)
    b_last = np.exp(-50) / np.sqrt(31)
    coefficients = [
        (k - 5 * b) * t - 1 / np.sqrt(107 / 2),
        (k - 5 * b) * t**2 - b * t,
        (k - 5 * b) * t**3 - b * t**2,
        (k - 5 * b_last) * t**4 - b * t**3,
    ]
    assert coefficients[0] < 0 < coefficients[2] < coefficients[1]

    history = np.roll(points, -1, axis=0)
    steps = history - np.roll(history, -1, axis=0)
    directions = steps / np.linalg.norm(steps, axis=1, keepdims=True)
    weights = exponential_memory_weights(1 - q, 10)
    raw = vector_gaussian_field(history[0], history, directions, weights, sigma=1.0)
    np.testing.assert_allclose(tangent @ raw / weights[0], coefficients @ w, atol=2e-16)


@pytest.mark.parametrize("phase", [0, 1])
@pytest.mark.parametrize("scalar_retention", [0.3, 0.97])
def test_scalar_tangent_is_one_geometrical_direction_at_both_special_phases(
    phase, scalar_retention
):
    points, inner, _ = _two_shell_geometry(-1)
    axis = inner[0]
    tangent = np.eye(4) - np.outer(axis, axis) / (axis @ axis)
    w = inner[1:] @ tangent
    s = scalar_retention
    direction = s ** (2 * np.arange(1, 5)) @ w
    direction /= np.linalg.norm(direction)
    history = np.roll(points, -phase, axis=0)
    wanted = tangent @ (history[-1] - history[0])
    scalar = tangent @ gaussian_gradient(
        history[0], history, exponential_memory_weights(1 - s, 10), sigma=3.0
    )
    np.testing.assert_allclose(scalar, (direction @ scalar) * direction, atol=2e-16)
    if phase == 0:
        assert np.linalg.norm(wanted - (wanted @ direction) * direction) > 0.1
    else:
        np.testing.assert_allclose(wanted, 0, atol=2e-15)
