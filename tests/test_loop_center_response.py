import numpy as np

from emergenz_knoten.loop_center_response import (
    co_rotating_fifo_forced_step,
    finite_h_center_recurrence,
    laboratory_center_displacement,
    laboratory_force_in_next_corotating_frame,
    memory_center,
    native_fifo_forced_step,
    normalized_memory_weights,
    registered_zero_sum_waveforms,
    tangent_fifo_forced_step,
    weighted_state_norm,
)
from emergenz_knoten.rotating_wave_stability import (
    circular_history,
    co_rotating_fifo_jacobian,
    native_fifo_step,
    rotation_matrix,
)


PARAMETERS = {
    "alpha": 0.07,
    "memory_mass": 1.2,
    "eta": 0.18,
    "sigma_rep": 1.0,
    "sigma_att": 3.0,
    "amplitude_rep": 1.0,
    "amplitude_att": 4.5,
}


def test_normalized_center_matches_geometric_circular_filter() -> None:
    radius = 1.3
    theta = 0.11
    horizon = 31
    history = circular_history(radius=radius, theta=theta, horizon=horizon)
    center = memory_center(history, alpha=0.04, memory_mass=2.7)
    q = 0.96
    z = np.exp(1j * theta)
    transfer = 0.04 / (1.0 - q**horizon) * np.sum(
        np.power(q / z, np.arange(horizon))
    )
    expected = radius * np.asarray([transfer.real, transfer.imag])

    np.testing.assert_allclose(center, expected, rtol=2.0e-15, atol=2.0e-15)


def test_finite_h_center_recurrence_keeps_retiring_sample() -> None:
    rng = np.random.default_rng(20260825)
    history = rng.normal(size=(23, 2))
    advanced = rng.normal(size=2)
    shifted = np.vstack((advanced, history[:-1]))
    center = memory_center(history, alpha=0.06, memory_mass=1.4)

    recurrent = finite_h_center_recurrence(
        center,
        new_visible=advanced,
        retiring_visible=history[-1],
        alpha=0.06,
        horizon=history.shape[0],
    )

    np.testing.assert_allclose(
        recurrent,
        memory_center(shifted, alpha=0.06, memory_mass=1.4),
        rtol=2.0e-15,
        atol=2.0e-15,
    )


def test_forced_corotating_step_matches_force_then_rotation() -> None:
    theta = 0.13
    step_index = 7
    history = circular_history(radius=1.1, theta=theta, horizon=17)
    force_lab = np.asarray([0.3, -0.2])
    expected = native_fifo_step(history, **PARAMETERS)
    force_current = rotation_matrix(-step_index * theta) @ force_lab
    expected[0] += PARAMETERS["alpha"] * force_current
    expected = expected @ rotation_matrix(-theta).T

    actual = co_rotating_fifo_forced_step(
        history,
        force_lab=force_lab,
        step_index=step_index,
        theta=theta,
        **PARAMETERS,
    )

    np.testing.assert_allclose(actual, expected, rtol=0.0, atol=3.0e-16)


def test_tangent_forced_step_matches_joint_centered_difference() -> None:
    theta = 0.13
    step_index = 9
    history = circular_history(radius=1.1, theta=theta, horizon=17)
    jacobian = co_rotating_fifo_jacobian(history, theta=theta, **PARAMETERS)
    rng = np.random.default_rng(20260826)
    direction = rng.normal(size=history.shape)
    direction /= np.linalg.norm(direction)
    force_direction = np.asarray([0.17, -0.31])
    step = 2.0e-6
    upper = co_rotating_fifo_forced_step(
        history + step * direction,
        force_lab=step * force_direction,
        step_index=step_index,
        theta=theta,
        **PARAMETERS,
    )
    lower = co_rotating_fifo_forced_step(
        history - step * direction,
        force_lab=-step * force_direction,
        step_index=step_index,
        theta=theta,
        **PARAMETERS,
    )
    finite_difference = (upper - lower) / (2.0 * step)

    tangent = tangent_fifo_forced_step(
        direction,
        jacobian=jacobian,
        force_lab=force_direction,
        step_index=step_index,
        theta=theta,
        alpha=PARAMETERS["alpha"],
    )

    np.testing.assert_allclose(tangent, finite_difference, rtol=2.0e-9, atol=2.0e-10)


def test_native_forced_step_is_rotation_covariant() -> None:
    history = circular_history(radius=1.1, theta=0.13, horizon=17)
    force = np.asarray([0.2, -0.4])
    base = native_fifo_forced_step(history, force=force, **PARAMETERS)
    for phase in (0.0, np.pi / 2.0, np.pi, 3.0 * np.pi / 2.0):
        rotation = rotation_matrix(phase)
        transformed = native_fifo_forced_step(
            history @ rotation.T,
            force=rotation @ force,
            **PARAMETERS,
        )
        np.testing.assert_allclose(
            transformed,
            base @ rotation.T,
            rtol=0.0,
            atol=6.0e-16,
        )


def test_laboratory_center_displacement_undoes_corotating_frame() -> None:
    rng = np.random.default_rng(20260827)
    delta = rng.normal(size=(19, 2))
    center = memory_center(delta, alpha=0.05, memory_mass=1.8)
    expected = rotation_matrix(0.4 + 12 * 0.08) @ center

    actual = laboratory_center_displacement(
        delta,
        alpha=0.05,
        memory_mass=1.8,
        theta=0.08,
        step=12,
        initial_phase=0.4,
    )

    np.testing.assert_allclose(actual, expected, rtol=0.0, atol=2.0e-15)


def test_weighted_state_norm_and_registered_waveforms() -> None:
    weights = normalized_memory_weights(alpha=0.08, horizon=21)
    delta = np.tile([3.0, 4.0], (21, 1))
    assert abs(weighted_state_norm(delta, weights=weights) - 5.0) < 2.0e-15

    waveforms = registered_zero_sum_waveforms()
    assert set(waveforms) == {"sine_cycle", "hann_doublet"}
    for values in waveforms.values():
        assert values.shape == (400,)
        assert abs(float(np.sum(values))) < 1.0e-13


def test_next_frame_force_has_registered_one_step_phase() -> None:
    force = np.asarray([1.0, 0.0])
    transformed = laboratory_force_in_next_corotating_frame(
        force,
        theta=0.2,
        step_index=3,
    )
    np.testing.assert_allclose(
        transformed,
        rotation_matrix(-0.8) @ force,
        rtol=0.0,
        atol=2.0e-15,
    )
