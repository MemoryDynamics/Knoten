"""Constructed one-write balances and H=3 controllability, no target runs."""

import numpy as np
import pytest
from scipy.integrate import quad_vec

from emergenz_knoten.core import SimulationConfig, finite_memory_step, update_history
from emergenz_knoten.kernels import double_gaussian_gradient, exponential_memory_weights
from emergenz_knoten.memory_current import (
    fifo_current_fourier,
    fifo_replacement_coefficients,
    path_current_fourier,
)


@pytest.mark.parametrize("horizon,alpha", [(1, 0.2), (4, 0.2), (4, 1.0)])
def test_geometric_fifo_removal_includes_oldest_tail(horizon, alpha):
    weights = exponential_memory_weights(alpha, horizon, memory_mass=1.3)
    coefficients = fifo_replacement_coefficients(weights)
    expected = alpha * weights
    expected[-1] += (1 - alpha) * weights[-1]
    np.testing.assert_allclose(coefficients, expected, atol=3e-17, rtol=2e-15)
    assert coefficients.sum() == pytest.approx(weights[0])
    assert np.all(coefficients >= 0)


@pytest.mark.parametrize("dim,sigma", [(1, 0), (2, 0.3), (4, 0.2)])
def test_fifo_fourier_continuity_matches_actual_history_update(dim, sigma):
    history = 0.2 * np.sin(np.arange(4 * dim).reshape(4, dim))
    point = 0.1 * np.cos(np.arange(dim))
    weights = exponential_memory_weights(0.2, 4, memory_mass=1.3)
    k = np.vstack(
        [np.zeros(dim), np.full(dim, 1e-10), np.cos(np.arange(5 * dim).reshape(5, dim))]
    )
    result = fifo_current_fourier(history, point, weights, k, sigma=sigma)
    new_history, _ = update_history(history.copy(), point, 4)
    smoothing = np.exp(-sigma * sigma * np.sum(k * k, axis=1) / 2)
    direct = smoothing * (
        (np.exp(-1j * k @ new_history.T) - np.exp(-1j * k @ history.T)) @ weights
    )
    np.testing.assert_allclose(result["increment"], direct, atol=2e-16)
    divergence = 1j * np.einsum("nd,nd->n", k, result["current"])
    np.testing.assert_allclose(divergence, -result["increment"], atol=1e-16, rtol=1e-13)
    np.testing.assert_allclose(
        result["current"][0], weights @ new_history - weights @ history, atol=4e-17
    )
    assert result["increment"][0] == 0


def test_omitting_fifo_tail_produces_spurious_monopole():
    alpha, horizon, mass = 0.2, 4, 1.3
    weights = exponential_memory_weights(alpha, horizon, memory_mass=mass)
    false_monopole = alpha * (mass - weights.sum())
    assert false_monopole == pytest.approx(mass * alpha * (1 - alpha) ** horizon)
    assert false_monopole > 0
    assert weights[0] - fifo_replacement_coefficients(weights).sum() == pytest.approx(
        0, abs=1e-16
    )


def test_nonmonotone_weights_give_signed_flux_but_same_exact_identity():
    coefficients = fifo_replacement_coefficients([0.2, 0.5, 0.3])
    assert coefficients[0] < 0
    assert coefficients.sum() == pytest.approx(0.2)


def test_different_routes_have_same_divergence_and_nonzero_solenoidal_difference():
    direct = np.array([[0.0, 0.0], [1.0, 0.0]])
    bent = np.array([[0.0, 0.0], [0.4, 0.8], [1.0, 0.0]])
    k = np.array([[0.0, 0.0], [0.2, 0.7], [1.2, -0.3], [-0.4, 1.1]])
    difference = path_current_fourier(bent, k, sigma=0.2) - path_current_fourier(
        direct, k, sigma=0.2
    )
    np.testing.assert_allclose(np.einsum("nd,nd->n", k, difference), 0, atol=3e-16)
    assert np.linalg.norm(difference[1:]) > 0.1
    np.testing.assert_allclose(difference[0], 0, atol=1e-16)


def test_closed_path_current_changes_no_density():
    path = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [0.0, 0.0]])
    k = np.array([[0.0, 0.0], [0.4, 0.7], [1.2, -0.3]])
    current = path_current_fourier(path, k)
    np.testing.assert_allclose(np.einsum("nd,nd->n", k, current), 0, atol=3e-16)
    assert np.linalg.norm(current[1:]) > 0.1


def test_translation_changes_only_fourier_phase():
    path = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    k, shift = np.array([[0.0, 0.0], [0.4, 0.7]]), np.array([0.3, -0.2])
    np.testing.assert_allclose(
        path_current_fourier(path + shift, k),
        np.exp(-1j * k @ shift)[:, None] * path_current_fourier(path, k),
        atol=2e-16,
    )


def test_full_current_matches_independent_segment_quadrature():
    history = np.array([[0.1, -0.2], [0.7, 0.3], [-0.4, 0.6]])
    point = np.array([0.2, 0.4])
    weights = np.array([0.2, 0.5, 0.3])
    k = np.array([[0.0, 0.0], [0.4, 0.7], [1.2, -0.3]])
    sigma = 0.25
    result = fifo_current_fourier(history, point, weights, k, sigma=sigma)
    expected = np.zeros((len(k), 2), complex)
    for j, start in enumerate(history):
        coefficient = weights[j] - (weights[j + 1] if j + 1 < len(weights) else 0)
        displacement = point - start
        integral, error = quad_vec(
            lambda s: (
                np.exp(-1j * (k @ (start + s * displacement)))[:, None] * displacement
            ),
            0,
            1,
            epsabs=1e-12,
        )
        assert error < 1e-12
        expected += coefficient * integral
    expected *= np.exp(-(sigma**2) * np.sum(k * k, axis=1) / 2)[:, None]
    np.testing.assert_allclose(result["current"], expected, atol=2e-16)


def test_initial_filling_has_mass_growth_unlike_full_fifo():
    horizon, alpha, mass = 4, 0.2, 1.3
    weights = exponential_memory_weights(alpha, horizon, memory_mass=mass)
    history, filled = np.zeros((horizon, 1)), 0
    for n in range(horizon + 1):
        old_mass = weights[:filled].sum()
        history, filled = update_history(history, np.array([0.1 * n]), filled)
        increment = weights[:filled].sum() - old_mass
        expected = mass * alpha * (1 - alpha) ** n if n < horizon else 0
        assert increment == pytest.approx(expected, abs=2e-16)


class _PrescribedInnovation:
    def __init__(self, value):
        self.value = value

    def normal(self, *, size):
        assert self.value.shape == (size,)
        return self.value.copy()


@pytest.mark.parametrize("offset", [0.0, 0.7])
def test_three_writes_reach_same_arbitrary_fifo_from_different_initial_states(offset):
    config = SimulationConfig(
        steps=3,
        dim=2,
        epsilon=0.3,
        eta=0.07,
        alpha=0.2,
        memory_mass=1,
        sigma_rep=1,
        sigma_att=2,
        amplitude_rep=1,
        amplitude_att=8,
        burn_in=0,
        sample_every=1,
    )
    weights = exponential_memory_weights(config.alpha, 3, memory_mass=1)
    history = np.array([[0.1, 0.2], [-0.3, 0.1], [0.2, -0.4]]) + offset
    x = np.array([-0.2, 0.1]) + offset
    target = np.array([[0.2, -0.1], [-0.3, -0.2], [0.1, 0.3]])
    log_density = 0.0
    for next_point in target[::-1]:
        gradient = double_gaussian_gradient(
            x,
            history,
            weights,
            sigma_rep=1,
            sigma_att=2,
            amplitude_rep=1,
            amplitude_att=8,
        )
        innovation = (next_point - x + config.eta * gradient) / config.epsilon
        x = finite_memory_step(
            x, history, weights, config, rng=_PrescribedInnovation(innovation)
        )
        history, _ = update_history(history, x, 3)
        log_density += -0.5 * innovation @ innovation - config.dim * np.log(
            config.epsilon * np.sqrt(2 * np.pi)
        )
    np.testing.assert_allclose(history, target, atol=2e-16)
    np.testing.assert_allclose(x, target[0], atol=2e-16)
    assert np.isfinite(log_density)
    assert np.exp(log_density) > 0  # density, NOT probability of a single point


@pytest.mark.parametrize("weights", [[], [0, 0], [-1, 2], [np.nan]])
def test_invalid_weights_rejected(weights):
    with pytest.raises(ValueError):
        fifo_replacement_coefficients(weights)
