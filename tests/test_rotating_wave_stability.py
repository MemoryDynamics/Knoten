import numpy as np

from emergenz_knoten.kernels import (
    double_gaussian_gradient,
    exponential_memory_weights,
)
from emergenz_knoten.rotating_wave_stability import (
    circular_history,
    co_rotating_fifo_jacobian,
    co_rotating_fifo_step,
    native_fifo_step,
    rotation_matrix,
    rotation_translation_quotient_distance,
    symmetry_tangent_vectors,
)


CANDIDATE = {
    "radius": 0.946517504804225,
    "theta": 0.015770381717135,
    "alpha": 0.01,
    "memory_mass": 1.0,
    "eta": 0.15,
    "sigma_rep": 1.0,
    "sigma_att": 3.0,
    "amplitude_rep": 1.0,
    "amplitude_att": 3.5,
}


def _step_parameters():
    return {
        name: CANDIDATE[name]
        for name in (
            "alpha",
            "memory_mass",
            "eta",
            "sigma_rep",
            "sigma_att",
            "amplitude_rep",
            "amplitude_att",
        )
    }


def test_frozen_candidate_is_fixed_in_co_rotating_full_fifo_map():
    history = circular_history(
        radius=CANDIDATE["radius"],
        theta=CANDIDATE["theta"],
        horizon=1200,
    )

    advanced = co_rotating_fifo_step(
        history,
        theta=CANDIDATE["theta"],
        **_step_parameters(),
    )

    np.testing.assert_allclose(advanced, history, rtol=0.0, atol=4.0e-15)


def test_sparse_fifo_jacobian_matches_centered_finite_difference():
    horizon = 17
    history = circular_history(radius=1.1, theta=0.13, horizon=horizon)
    parameters = {
        "alpha": 0.07,
        "memory_mass": 1.2,
        "eta": 0.18,
        "sigma_rep": 1.0,
        "sigma_att": 3.0,
        "amplitude_rep": 1.0,
        "amplitude_att": 4.5,
    }
    jacobian = co_rotating_fifo_jacobian(
        history,
        theta=0.13,
        **parameters,
    )
    direction = np.random.default_rng(20260820).normal(size=history.shape)
    direction /= np.linalg.norm(direction)
    step = 2.0e-6
    upper = co_rotating_fifo_step(
        history + step * direction,
        theta=0.13,
        **parameters,
    )
    lower = co_rotating_fifo_step(
        history - step * direction,
        theta=0.13,
        **parameters,
    )
    finite_difference = ((upper - lower) / (2.0 * step)).ravel()
    analytic = jacobian @ direction.ravel()

    np.testing.assert_allclose(analytic, finite_difference, rtol=2.0e-9, atol=2.0e-10)


def test_native_fifo_step_matches_production_kernel_and_shift():
    history = np.random.default_rng(20260820).normal(size=(29, 2))
    parameters = {
        "alpha": 0.04,
        "memory_mass": 1.3,
        "eta": 0.17,
        "sigma_rep": 1.0,
        "sigma_att": 3.0,
        "amplitude_rep": 1.0,
        "amplitude_att": 3.5,
    }
    weights = exponential_memory_weights(
        parameters["alpha"],
        history.shape[0],
        memory_mass=parameters["memory_mass"],
    )
    gradient = double_gaussian_gradient(
        history[0],
        history,
        weights,
        sigma_rep=parameters["sigma_rep"],
        sigma_att=parameters["sigma_att"],
        amplitude_rep=parameters["amplitude_rep"],
        amplitude_att=parameters["amplitude_att"],
        deposition_kernel="delta",
        deposition_sigma=0.0,
    )
    expected = np.empty_like(history)
    expected[0] = history[0] - parameters["eta"] * gradient
    expected[1:] = history[:-1]

    actual = native_fifo_step(history, **parameters)

    np.testing.assert_allclose(actual, expected, rtol=2.0e-15, atol=2.0e-15)


def test_candidate_jacobian_reproduces_rotation_and_translation_symmetries():
    history = circular_history(
        radius=CANDIDATE["radius"],
        theta=CANDIDATE["theta"],
        horizon=1200,
    )
    jacobian = co_rotating_fifo_jacobian(
        history,
        theta=CANDIDATE["theta"],
        **_step_parameters(),
    )
    tangents = symmetry_tangent_vectors(history)
    rotate_back = rotation_matrix(-CANDIDATE["theta"])

    rotation_error = jacobian @ tangents["rotation"] - tangents["rotation"]
    expected_x = np.tile(
        rotate_back @ np.asarray([1.0, 0.0]),
        (history.shape[0], 1),
    ).ravel()
    expected_y = np.tile(
        rotate_back @ np.asarray([0.0, 1.0]),
        (history.shape[0], 1),
    ).ravel()

    assert (
        np.linalg.norm(rotation_error) / np.linalg.norm(tangents["rotation"]) < 2.0e-14
    )
    np.testing.assert_allclose(
        jacobian @ tangents["translation_x"],
        expected_x,
        rtol=0.0,
        atol=2.0e-15,
    )
    np.testing.assert_allclose(
        jacobian @ tangents["translation_y"],
        expected_y,
        rtol=0.0,
        atol=2.0e-15,
    )


def test_d0_distance_quotients_common_translation_and_rotation():
    reference = circular_history(radius=1.4, theta=0.09, horizon=80)
    transform = rotation_matrix(0.73)
    moved = reference @ transform.T + np.asarray([4.0, -2.0])

    distance, alignment = rotation_translation_quotient_distance(
        moved,
        reference,
        alpha=0.04,
        memory_mass=1.0,
    )

    assert distance < 4.0e-15
    assert abs(alignment + 0.73) < 2.0e-15
