"""Fixed probes of supplied 4D reference histories, not native pair runs."""

import numpy as np
from scipy.special import ive

from emergenz_knoten.kernels import (
    double_gaussian_gradient,
    double_gaussian_potential,
    gaussian_gradient,
    gaussian_potential,
)
from experiments.current.reference.fifo_4d_delayed_spin import (
    AXIS,
    coherent_history,
    delayed_step,
    frame_readout,
)
from experiments.current.reference.fifo_4d_spin_projection import (
    GENERATORS,
    INITIAL,
    direction_readout,
    real_rotation,
)


WEIGHTS = np.array([1.0, 0.5, 0.25, 0.125])


def _readout(probe, history):
    settings = {"sigma": 1.0}
    return np.r_[
        gaussian_potential(probe, history, WEIGHTS, **settings),
        gaussian_gradient(probe, history, WEIGHTS, **settings),
    ]


def test_equal_frames_have_unequal_4d_potential_and_opposite_tangential_force():
    history = coherent_history()
    for entry in history:
        np.testing.assert_array_equal(frame_readout(entry), frame_readout(-entry))

    plus, minus = (_readout(INITIAL, sign * history) for sign in (1, -1))
    expected = (
        2
        * np.exp(-1)
        * (
            WEIGHTS[0] * np.sinh(1)
            + (WEIGHTS[1] - WEIGHTS[3]) * np.sinh(1 / np.sqrt(2))
        )
    )
    np.testing.assert_allclose(plus[0] - minus[0], expected, rtol=1e-15)
    tangent = np.einsum("i,ijk,k->j", AXIS, GENERATORS, INITIAL)
    assert (-plus[1:]) @ tangent > 0 > (-minus[1:]) @ tangent


def test_antipodal_weight_pairs_hide_sign_even_in_full_gradient_off_the_orbit():
    history = coherent_history()
    points = np.concatenate((history, -history))
    weights = np.tile(WEIGHTS, 2)
    probe = np.array([0.3, 0.6, -0.4, -0.9])
    settings = dict(sigma_rep=0.8, sigma_att=1.2, amplitude_rep=0.7, amplitude_att=0.5)
    for kernel in (double_gaussian_potential, double_gaussian_gradient):
        np.testing.assert_allclose(
            kernel(probe, points, weights, **settings),
            kernel(probe, -points, weights, **settings),
            atol=2e-16,
        )


def test_two_scales_can_cancel_first_but_not_third_harmonic():
    rep, att = 2.0, 0.5
    amplitude = ive(1, rep) / ive(1, att)
    settings = dict(
        sigma_rep=rep**-0.5,
        sigma_att=att**-0.5,
        amplitude_att=amplitude,
    )
    history = coherent_history()
    angles = np.linspace(0, 2 * np.pi, 64, endpoint=False)
    values = np.array(
        [
            double_gaussian_potential(
                real_rotation(AXIS, 2 * alpha) @ INITIAL, history, WEIGHTS, **settings
            )
            for alpha in angles
        ]
    )
    coeff = np.fft.fft(values) / len(values)
    np.testing.assert_allclose(coeff[1], 0, atol=4e-16)
    expected = (ive(3, rep) - amplitude * ive(3, att)) * np.sum(
        WEIGHTS * np.exp(3j * np.pi / 4 * np.arange(4))
    )
    assert abs(expected) > 0.01
    np.testing.assert_allclose(coeff[3], expected, atol=4e-16)


def test_cycle_average_erases_fixed_probe_contrast_but_not_comoving_contrast():
    history = coherent_history()
    fixed_contrasts, comoving_contrasts = [], []
    for _ in range(8):
        fixed_contrasts.append(_readout(INITIAL, history) - _readout(INITIAL, -history))
        probe = history[0]
        comoving_contrasts.append(
            _readout(probe, history)[0] - _readout(probe, -history)[0]
        )
        history = delayed_step(history)

    assert np.linalg.norm(fixed_contrasts[0]) > 0.1
    np.testing.assert_allclose(np.mean(fixed_contrasts, axis=0), 0, atol=1e-16)
    assert comoving_contrasts[0] > 0.1
    np.testing.assert_allclose(comoving_contrasts, comoving_contrasts[0], atol=1e-15)


def test_antiparallel_directions_allow_either_sign_of_the_cross_drift():
    axis = [0, 0, 1]
    history_a = coherent_history(axis)
    history_b = history_a @ real_rotation(axis, np.pi).T
    head_a, head_b = history_a[0], history_b[0]
    direction_a, direction_b = direction_readout([head_a, head_b])
    np.testing.assert_allclose(direction_b, -direction_a, atol=2e-16)
    np.testing.assert_allclose(direction_readout(-head_a), direction_a, atol=2e-16)

    def cross_drift(amplitude):
        a = -gaussian_gradient(head_a, history_b, WEIGHTS, sigma=1, amplitude=amplitude)
        b = -gaussian_gradient(head_b, history_a, WEIGHTS, sigma=1, amplitude=amplitude)
        return np.stack((a, b))

    repelling, attracting = cross_drift(1), cross_drift(-1)
    np.testing.assert_array_equal(attracting, -repelling)
    drift_a, drift_b = repelling
    separation_rate = (head_a - head_b) @ (drift_a - drift_b)
    age = np.arange(4) * np.pi / 4
    distances = 1 + np.stack((-np.sin(age), np.sin(age)))
    expected = np.sum(WEIGHTS * np.exp(-distances) * (distances + np.cos(age)))
    np.testing.assert_allclose(separation_rate, expected, rtol=2e-15)
    assert separation_rate > 0


def _coupled_reference_step(a, b, amplitude):
    next_a, next_b = delayed_step(a), delayed_step(b)
    for advanced, other in ((next_a, b), (next_b, a)):
        head = advanced[0]
        head -= gaussian_gradient(head, other, WEIGHTS, sigma=1.0, amplitude=amplitude)
        head /= np.linalg.norm(head)
    return next_a, next_b


def _coupled_reference_cycle(a, b, amplitude):
    for _ in range(8):
        a, b = _coupled_reference_step(a, b, amplitude)
    return a, b


def test_antiparallel_reference_cycle_separates_signs_in_4d_but_not_by_3d_alignment():
    axis = [0, 0, 1]
    a = coherent_history(axis)
    b = a @ real_rotation(axis, np.pi).T
    tangent = GENERATORS[2] @ INITIAL

    def relative_phase(first, second):
        def phases(history):
            return np.arctan2(history @ tangent, history @ INITIAL)

        return (phases(second) - phases(first)) % (2 * np.pi)

    neutral = _coupled_reference_cycle(a, b, 0.0)
    np.testing.assert_allclose(neutral, (a, b), atol=3e-16)
    np.testing.assert_allclose(relative_phase(*neutral), np.pi / 2, atol=3e-16)
    weight = (WEIGHTS[0] - WEIGHTS[2]) * np.cosh(1 / np.sqrt(2)) / np.sqrt(2)
    predicted_slope = 4 / np.e * (weight - WEIGHTS[3])
    assert predicted_slope > 0
    amplitude = 1e-5

    for sign in (1, -1):
        first, second = _coupled_reference_cycle(a, b, sign * amplitude)
        slip = relative_phase(first, second) - np.pi / 2
        # Each original slot has been rewritten twice.
        np.testing.assert_allclose(
            slip / (sign * amplitude), predicted_slope, rtol=5e-5
        )
        distance = np.linalg.norm(first - second, axis=1)
        assert np.all(sign * (distance - np.sqrt(2)) > 0)
        first_dir, second_dir = direction_readout([first[0], second[0]])
        angle_loss = np.arctan2(
            np.linalg.norm(np.cross(first_dir, second_dir)), -(first_dir @ second_dir)
        )
        np.testing.assert_allclose(angle_loss, 2 * abs(slip[0]), atol=5e-16)


def test_oriented_volume_is_conserved_but_hidden_from_the_full_frame_history():
    a = np.eye(4)
    b = a.copy()
    b[3] *= -1

    for _ in range(8):
        assert np.linalg.det(a) == 1
        assert np.linalg.det(b) == -1
        for first, second in zip(a, b, strict=True):
            np.testing.assert_array_equal(frame_readout(first), frame_readout(second))
        a, b = delayed_step(a), delayed_step(b)

    np.testing.assert_array_equal(a, np.eye(4))
    np.testing.assert_allclose(np.linalg.det(coherent_history()), 0, atol=1e-16)


def test_relative_orientation_is_recoverable_from_gaussian_slot_comparisons():
    a = np.eye(4)
    b = a.copy()
    b[3] *= -1
    reflection = np.diag([-1, 1, 1, 1])
    sigma = 0.8

    def gauss_gram(first, second):
        values = [
            [gaussian_potential(x, [y], [1.0], sigma=sigma) for y in second]
            for x in first
        ]
        return 1 + sigma**2 * np.log(values)

    for first, second, expected in (
        (a, a, 1),
        (a, b, -1),
        (a @ reflection, b @ reflection, -1),
        (a, coherent_history(), 0),
    ):
        gram = gauss_gram(first, second)
        np.testing.assert_allclose(gram, first @ second.T, atol=4e-16)
        np.testing.assert_allclose(np.linalg.det(gram), expected, atol=1e-15)


def test_symmetric_gaussian_cross_write_creates_unbalanced_oriented_volume():
    e1, e2, e3, e4 = np.eye(4)
    a = np.stack((e1, e2, e3, e1))
    t = 0.25
    beta = np.sqrt(1 - t**2)
    b = np.tile(t * e1 + beta * e4, (4, 1))
    assert np.linalg.det(a) == np.linalg.det(b) == 0

    for amplitude in (0.0, 0.01, -0.01):
        next_a, next_b = _coupled_reference_step(a, b, amplitude)
        strength = amplitude * WEIGHTS.sum() * np.exp(-(1 + t))
        head_norm = np.hypot(1 + strength * (1 + t), strength * beta)
        expected = strength * beta / head_norm
        np.testing.assert_allclose(np.linalg.det(next_a), expected, atol=1e-17)
        assert np.linalg.det(next_b) == 0

    a[3] = np.sqrt(1 - 1e-8) * e1 + 1e-4 * e4
    after, _ = _coupled_reference_step(a, b, -0.01)
    assert np.linalg.det(a) > 0 > np.linalg.det(after)
