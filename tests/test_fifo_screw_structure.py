"""Small synthetic geometry/balance controls; no target loads or root searches."""

from fractions import Fraction as F

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from emergenz_knoten.fifo_normal_stability import normal_translation_slope
from emergenz_knoten.kernels import double_gaussian_gradient
from emergenz_knoten.rotating_wave import double_gaussian_gradient_factor
from emergenz_knoten.rotating_wave_stability import (
    circular_history,
    finite_memory_weights,
)


KERNEL = {
    "sigma_rep": 0.9,
    "sigma_att": 2.1,
    "amplitude_rep": 1.3,
    "amplitude_att": 2.4,
}
MEMORY = {"alpha": 0.17, "memory_mass": 1.2}
ETA = 0.23


def history(radius, theta, speed, horizon=9):
    ages = np.arange(horizon)
    return np.column_stack(
        (radius * np.cos(ages * theta), -radius * np.sin(ages * theta), -ages * speed)
    )


def native_step(state, *, eta=ETA, kernel=KERNEL, memory=MEMORY):
    weights = finite_memory_weights(horizon=len(state), **memory)
    gradient = double_gaussian_gradient(state[0], state, weights, **kernel)
    return np.vstack((state[0] - eta * gradient, state[:-1]))


def balances(radius, theta, speed, *, horizon=9, eta=ETA, kernel=KERNEL, memory=MEMORY):
    ages = np.arange(1, horizon)
    distances = np.sqrt(2 * radius**2 * (1 - np.cos(ages * theta)) + ages**2 * speed**2)
    weights = finite_memory_weights(horizon=horizon, **memory)[1:]
    couplings = eta * weights * double_gaussian_gradient_factor(distances, **kernel)
    return np.array(
        [
            np.cos(theta) - 1 + np.sum(couplings * (1 - np.cos(ages * theta))),
            np.sin(theta) + np.sum(couplings * np.sin(ages * theta)),
            1 + np.sum(ages * couplings),
        ]
    ), couplings


@pytest.mark.parametrize(
    "radius,theta,speed",
    [(1.2, 0.37, 0.0), (1.2, 0.37, 0.21), (1.2, -0.37, -0.21), (0.0, 0.37, 0.21)],
)
def test_three_balances_match_native_kernel_and_age_shift(radius, theta, speed):
    state = history(radius, theta, speed)
    expected = state @ Rotation.from_rotvec([0, 0, theta]).as_matrix().T + [0, 0, speed]
    observed = native_step(state)
    residual, _ = balances(radius, theta, speed)
    np.testing.assert_allclose(
        observed[0] - expected[0],
        -np.array([radius, radius, speed]) * residual,
        atol=2e-15,
    )
    np.testing.assert_allclose(observed[1:], expected[1:], atol=2e-15)


def test_zero_pitch_reduces_to_existing_circle_without_requiring_z_zero():
    state = history(1.2, 0.37, 0)
    np.testing.assert_allclose(
        state[:, :2], circular_history(radius=1.2, theta=0.37, horizon=9), atol=1e-15
    )
    residual, couplings = balances(1.2, 0.37, 0)
    assert residual[2] == pytest.approx(normal_translation_slope(couplings), abs=1e-15)
    assert abs(residual[2]) > 0.1
    assert native_step(state)[0, 2] == 0


def test_pitch_and_rotation_parities():
    positive, _ = balances(1.2, 0.37, 0.21)
    pitch_flip, _ = balances(1.2, 0.37, -0.21)
    rotation_flip, _ = balances(1.2, -0.37, 0.21)
    np.testing.assert_array_equal(positive, pitch_flip)
    np.testing.assert_allclose(rotation_flip, positive * [1, -1, 1], atol=2e-15)


@pytest.mark.parametrize(
    "theta,speed", [(0.37, 0.21), (-0.37, 0.21), (0.37, -0.21), (0.37, 0.0)]
)
def test_oriented_history_volume_is_geometric_chirality_not_protection(theta, speed):
    radius = 1.2
    state = history(radius, theta, speed)
    volume = np.linalg.det(state[1:4] - state[0])
    expected = 4 * radius**2 * speed * np.sin(theta) * (1 - np.cos(theta)) ** 2
    assert volume == pytest.approx(expected, abs=2e-16)
    rotation = Rotation.from_rotvec([0.4, -0.7, 0.2]).as_matrix()
    rotated = state @ rotation.T + [0.3, -0.8, 0.2]
    assert np.linalg.det(rotated[1:4] - rotated[0]) == pytest.approx(volume, abs=5e-16)
    reflected = state * [1, 1, -1]
    assert np.linalg.det(reflected[1:4] - reflected[0]) == pytest.approx(
        -volume, abs=2e-16
    )


def test_slope_is_native_axial_defect_derivative():
    residual, _ = balances(1.2, 0.37, 0)
    errors = []
    for speed in (1e-3, 5e-4):
        observed = native_step(history(1.2, 0.37, speed))[0, 2]
        errors.append(abs((speed - observed) / speed - residual[2]))
    assert errors[0] > 0
    assert 0.24 < errors[1] / errors[0] < 0.26


@pytest.mark.parametrize(
    "couplings",
    [
        [F(-1)],
        [F(1, 4), F(-1, 8), F(-1, 3)],
        [F(-1, 8), F(-3, 4)],
        [F(1, 4), F(1, 8), F(-1, 4)],
    ],
)
def test_exact_drift_jordan_identity(couplings):
    size = len(couplings) + 1
    block = np.zeros((size, size), dtype=object)
    block[0] = [1 - sum(couplings), *couplings]
    block[1:, :-1] = np.eye(size - 1, dtype=int)
    operator = block - np.eye(size, dtype=int)
    ones = np.ones(size, dtype=object)
    ages = -np.arange(size, dtype=object)
    slope = normal_translation_slope(couplings)
    expected = ones.copy()
    expected[0] -= slope
    np.testing.assert_array_equal(operator @ ones, np.zeros(size, dtype=object))
    np.testing.assert_array_equal(operator @ ages, expected)
    if slope == 0:
        np.testing.assert_array_equal(
            operator @ operator @ ages, np.zeros(size, dtype=object)
        )
        assert any(value != 0 for value in operator @ ages)


@pytest.mark.parametrize("dimension", [1, 2, 3])
def test_affine_hull_cannot_grow_under_native_step(dimension):
    rng = np.random.default_rng(20261026)
    basis = np.linalg.qr(rng.normal(size=(5, dimension)))[0]
    origin = np.array([0.4, -1.2, 0.8, 0.1, 0.7])
    state = origin + rng.normal(size=(9, dimension)) @ basis.T
    result = native_step(state)
    orthogonal = np.eye(5) - basis @ basis.T
    np.testing.assert_allclose((result - origin) @ orthogonal, 0, atol=3e-15)


def test_collapsed_history_is_a_fixed_point_but_extended_static_history_is_not():
    collapsed = np.tile([0.4, -1.2, 0.8], (9, 1))
    np.testing.assert_array_equal(native_step(collapsed), collapsed)
    extended = history(1.2, 0.37, 0.21)
    assert not np.allclose(native_step(extended)[1:], extended[1:])


def test_constructed_h2_translator_is_exact_without_root_search():
    sigma, kappa, eta = 0.8, 2.0, 0.7
    memory = {"alpha": 0.2, "memory_mass": 1.1}
    weight = finite_memory_weights(horizon=2, **memory)[1]
    kernel = {
        "sigma_rep": sigma,
        "sigma_att": 2.0,
        "amplitude_rep": kappa * sigma**2 / (eta * weight),
        "amplitude_att": 0.0,
    }
    speed = sigma * np.sqrt(2 * np.log(kappa))
    for sign in (-1, 1):
        state = history(0, 0, sign * speed, horizon=2)
        expected = state + [0, 0, sign * speed]
        np.testing.assert_allclose(
            native_step(state, eta=eta, kernel=kernel, memory=memory),
            expected,
            atol=2e-15,
        )


def test_axial_self_consistency_does_not_imply_helical_solution():
    radius, theta, speed, sigma, eta = 1.0, 0.6, 0.2, 0.8, 0.7
    memory = {"alpha": 0.2, "memory_mass": 1.1}
    weight = finite_memory_weights(horizon=2, **memory)[1]
    chi = radius**2 * (1 - np.cos(theta)) + speed**2 / 2
    kernel = {
        "sigma_rep": sigma,
        "sigma_att": 2.0,
        "amplitude_rep": sigma**2 * np.exp(chi / sigma**2) / (eta * weight),
        "amplitude_att": 0.0,
    }
    residual, couplings = balances(
        radius, theta, speed, horizon=2, eta=eta, kernel=kernel, memory=memory
    )
    np.testing.assert_allclose(couplings, [-1], atol=2e-15)
    np.testing.assert_allclose(residual[1:], 0, atol=2e-15)
    assert residual[0] == pytest.approx(2 * (np.cos(theta) - 1), abs=2e-15)
    assert abs(residual[0]) > 0.1


@pytest.mark.parametrize(
    "radius,theta,speed",
    [(1.2, 0.37, 0.21), (1.2, 0.37, 0.0), (0.0, 0.37, 0.21), (0.0, 0.0, 0.0)],
)
def test_fixed_rigid_motion_has_screw_or_degenerate_orbit(radius, theta, speed):
    basis = Rotation.from_rotvec([0.4, -0.7, 0.2]).as_matrix()
    axis = basis[:, 2]
    rotation = basis @ Rotation.from_rotvec([0, 0, theta]).as_matrix() @ basis.T
    center = np.array([0.3, -0.8, 0.2])
    translation = (np.eye(3) - rotation) @ center + speed * axis
    point = center + radius * basis[:, 0]
    for index in range(9):
        expected = center + basis @ np.array(
            [
                radius * np.cos(index * theta),
                radius * np.sin(index * theta),
                index * speed,
            ]
        )
        np.testing.assert_allclose(point, expected, atol=4e-15)
        point = rotation @ point + translation


def test_four_dimensional_double_rotation_exceeds_three_dimensional_class():
    radii = np.array([0.9, 1.3])
    angles = np.array([0.37, 0.61])
    ages = np.arange(11)
    state = np.column_stack(
        [
            coordinate
            for radius, theta in zip(radii, angles, strict=True)
            for coordinate in (
                radius * np.cos(ages * theta),
                -radius * np.sin(ages * theta),
            )
        ]
    )
    rotation = np.zeros((4, 4))
    for index, theta in enumerate(angles):
        rotation[2 * index : 2 * index + 2, 2 * index : 2 * index + 2] = [
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)],
        ]
    expected = state @ rotation.T
    assert np.linalg.matrix_rank(state - state[0], tol=1e-10) == 4
    for index, radius in enumerate(radii):
        np.testing.assert_allclose(
            np.linalg.norm(expected[:, 2 * index : 2 * index + 2], axis=1),
            radius,
            atol=1e-15,
        )
    distances_squared = sum(
        2 * radius**2 * (1 - np.cos(ages * theta))
        for radius, theta in zip(radii, angles, strict=True)
    )
    weights = finite_memory_weights(horizon=len(state), **MEMORY)
    couplings = (
        ETA
        * weights
        * double_gaussian_gradient_factor(np.sqrt(distances_squared), **KERNEL)
    )
    first_defect = []
    for radius, theta in zip(radii, angles, strict=True):
        first_defect.extend(
            [
                -radius
                * (np.cos(theta) - 1 + np.sum(couplings * (1 - np.cos(ages * theta)))),
                -radius * (np.sin(theta) + np.sum(couplings * np.sin(ages * theta))),
            ]
        )
    actual = native_step(state)
    np.testing.assert_allclose(actual[0] - expected[0], first_defect, atol=3e-15)
    np.testing.assert_allclose(actual[1:], expected[1:], atol=3e-15)


@pytest.mark.parametrize("surface", ["sphere", "torus"])
def test_nonrigid_three_dimensional_surface_paths_are_not_excluded(surface):
    # Kinematic examples only: not native solutions or evidence of uniform coverage.
    index = np.arange(19)
    first, second = 0.37 * index, 0.61 * index
    if surface == "sphere":
        state = 1.3 * np.column_stack(
            (
                np.sin(second) * np.cos(first),
                np.sin(second) * np.sin(first),
                np.cos(second),
            )
        )
        np.testing.assert_allclose(np.linalg.norm(state, axis=1), 1.3, atol=2e-15)
    else:
        major, minor = 1.4, 0.4
        radial = major + minor * np.cos(second)
        state = np.column_stack(
            (radial * np.cos(first), radial * np.sin(first), minor * np.sin(second))
        )
        np.testing.assert_allclose(
            (np.linalg.norm(state[:, :2], axis=1) - major) ** 2 + state[:, 2] ** 2,
            minor**2,
            atol=2e-15,
        )
    # A single repeated isometry preserves consecutive step lengths; these vary.
    step_lengths = np.linalg.norm(np.diff(state, axis=0), axis=1)
    assert np.ptp(step_lengths) > 0.01
