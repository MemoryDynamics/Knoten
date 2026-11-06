"""Synthetic checks for the R0 assumptions audit, not new physics evidence."""

from itertools import product

import numpy as np
import pytest

from emergenz_knoten.analytic import local_scalar_memory_modes
from emergenz_knoten.kernels import (
    double_gaussian_gradient,
    double_gaussian_hessian,
    exponential_memory_weights,
)
from emergenz_knoten.rotating_wave_stability import (
    circular_history,
    rotation_matrix,
    rotation_translation_quotient_distance,
)


KERNEL = {
    "sigma_rep": 1.0,
    "sigma_att": 3.0,
    "amplitude_rep": 1.0,
    "amplitude_att": 4.0,
    "deposition_kernel": "delta",
    "deposition_sigma": 0.0,
}


@pytest.mark.parametrize("phase", [-1.2, 0.3, 2.0])
def test_single_circle_phase_is_a_spatial_rotation(phase):
    reference = circular_history(radius=1.2, theta=0.23, horizon=17)
    moved = reference @ rotation_matrix(phase).T + [1.0, -2.0]
    kwargs = {"alpha": 0.13, "memory_mass": 1.0}
    distance, _ = rotation_translation_quotient_distance(moved, reference, **kwargs)
    assert distance < 2e-15

    # A shape change must not disappear with the common rotation.
    changed = 1.1 * reference @ rotation_matrix(phase).T + [1.0, -2.0]
    distance, _ = rotation_translation_quotient_distance(changed, reference, **kwargs)
    assert distance > 0.05


def test_relative_orientation_survives_one_common_rotation():
    first = circular_history(radius=1.2, theta=0.23, horizon=17)
    second = first @ rotation_matrix(0.61).T + [3.0, -1.0]

    def relative_orientation(left, right):
        u = left[0] - left[1]
        v = right[0] - right[1]
        return np.asarray([np.dot(u, v), u[0] * v[1] - u[1] * v[0]]) / (
            np.linalg.norm(u) * np.linalg.norm(v)
        )

    expected = relative_orientation(first, second)
    common = rotation_matrix(0.8)
    actual = relative_orientation(
        first @ common.T + [4.0, 2.0], second @ common.T + [4.0, 2.0]
    )
    np.testing.assert_allclose(actual, expected, rtol=0.0, atol=4e-15)
    assert np.linalg.norm(expected - relative_orientation(first, first)) > 0.5


@pytest.mark.parametrize("distance", [4.0, 9.0, 18.0])
def test_mass_preserving_remote_source_shift_has_one_step_response(distance):
    target = np.zeros(2)
    source = np.asarray([[distance, 0.0]])
    mass = np.asarray([0.7])
    direction = np.asarray([0.0, 1.0])
    gain = 0.15
    step = 1e-5
    upper = double_gaussian_gradient(target, source + step * direction, mass, **KERNEL)
    lower = double_gaussian_gradient(target, source - step * direction, mass, **KERNEL)
    measured = -gain * (upper - lower) / (2.0 * step)
    analytic = gain * double_gaussian_hessian(target, source, mass, **KERNEL) @ direction

    np.testing.assert_allclose(measured, analytic, rtol=1e-9, atol=0.0)
    assert analytic[1] > 0.0


@pytest.mark.parametrize("dimension", [3, 8])
def test_radial_drift_preserves_prepared_affine_plane_but_normal_noise_does_not(dimension):
    basis = np.eye(dimension)[:, :2]
    origin = np.arange(dimension, dtype=float) / 7.0
    coordinates = np.asarray([[0.2, -0.4], [0.0, 1.0], [1.0, 0.0], [-0.7, -0.2]])
    memory = origin + coordinates @ basis.T
    target = memory[0]
    weights = exponential_memory_weights(0.2, len(memory), memory_mass=1.0)
    advanced = target - 0.15 * double_gaussian_gradient(target, memory, weights, **KERNEL)
    normal_projector = np.eye(dimension) - basis @ basis.T

    np.testing.assert_allclose(normal_projector @ (advanced - origin), 0.0, atol=1e-15)
    normal_innovation = np.eye(dimension)[2]
    noisy = advanced + 0.01 * normal_innovation
    np.testing.assert_allclose(
        normal_projector @ (noisy - origin), 0.01 * normal_innovation, atol=1e-15
    )


def test_real_two_state_modes_do_not_rule_out_finite_history_complex_transients():
    alpha, gain = 0.2, 0.8
    two_state = np.asarray(
        [[1.0 - gain, gain], [alpha * (1.0 - gain), 1.0 - alpha + alpha * gain]]
    )
    np.testing.assert_allclose(
        np.sort(np.linalg.eigvals(two_state)),
        np.sort(local_scalar_memory_modes(alpha, gain)),
        rtol=0.0,
        atol=5e-16,
    )

    weights = exponential_memory_weights(alpha, 3, memory_mass=1.0)
    weights /= weights.sum()
    companion = np.zeros((3, 3))
    companion[0] = gain * weights
    companion[0, 0] += 1.0 - gain
    companion[1:, :-1] = np.eye(2)
    spectrum = np.linalg.eigvals(companion)
    transverse = spectrum[np.abs(spectrum - 1.0) > 1e-12]
    assert len(transverse) == 2
    assert np.all(np.abs(transverse.imag) > 0.1)
    assert np.all(np.abs(transverse) < 1.0)


def test_all_local_binary_strategies_obey_chsh_and_three_quarter_win_bound():
    chsh_values, wins = set(), set()
    for a0, a1, b0, b1 in product((-1, 1), repeat=4):
        correlations = np.outer([a0, a1], [b0, b1])
        chsh_values.add(
            int(correlations[0, 0] + correlations[0, 1]
                + correlations[1, 0] - correlations[1, 1])
        )
        wins.add(int(np.sum(correlations == np.asarray([[1, 1], [1, -1]]))))
    assert chsh_values == {-2, 2}
    assert wins == {1, 3}


def test_non_signalling_alone_does_not_identify_quantum_correlations():
    signs = np.asarray([[1.0, 1.0], [1.0, -1.0]])
    products = np.outer([-1.0, 1.0], [-1.0, 1.0])
    scores = []
    for strength in (1.0 / np.sqrt(2.0), 1.0):
        correlations = strength * signs
        probabilities = 0.25 * (
            1.0 + correlations[:, :, None, None] * products[None, None, :, :]
        )
        assert np.all(probabilities >= 0.0)
        np.testing.assert_allclose(probabilities.sum(axis=(2, 3)), 1.0)
        np.testing.assert_allclose(probabilities.sum(axis=3), 0.5)
        np.testing.assert_allclose(probabilities.sum(axis=2), 0.5)
        reconstructed = np.sum(probabilities * products, axis=(2, 3))
        scores.append(float(np.sum(signs * reconstructed)))
    np.testing.assert_allclose(scores, [2.0 * np.sqrt(2.0), 4.0])
