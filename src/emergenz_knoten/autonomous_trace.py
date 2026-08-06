"""Autonomous finite-memory knot continuations with shape observables."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from ._continuation import path_gradient, path_observables
from .core import SimulationConfig, validate_simulation_config
from .kernels import effective_double_gaussian_parameters
from .state import FiniteMemoryState

try:
    from numba import njit
except ImportError:  # pragma: no cover

    def njit(*args, **kwargs):
        def wrapper(func):
            return func

        return wrapper


@dataclass(frozen=True)
class AutonomousKnotTrace:
    """Sampled continuation of one scalar knot from a complete Markov state."""

    sample_steps: np.ndarray
    positions: np.ndarray
    memory_centers: np.ndarray
    shape_tensors: np.ndarray
    radius_ratios: np.ndarray


@njit(cache=True)
def _autonomous_knot_batch(
    x_initial: np.ndarray,
    memory_initial: np.ndarray,
    weights: np.ndarray,
    noise: np.ndarray,
    sample_steps: np.ndarray,
    epsilon: float,
    eta: float,
    sigma_rep2: float,
    sigma_att2: float,
    amplitude_rep: float,
    amplitude_att: float,
):
    dim = x_initial.shape[0]
    n_samples = sample_steps.shape[0]
    x = x_initial.copy()
    history = memory_initial.copy()
    head = 0
    mass = np.sum(weights)
    positions = np.empty((n_samples, dim), np.float64)
    centers = np.empty((n_samples, dim), np.float64)
    tensors = np.empty((n_samples, dim, dim), np.float64)
    radii = np.empty(n_samples, np.float64)
    sample_index = 0
    n_steps = int(sample_steps[-1])

    for step in range(n_steps + 1):
        if step > 0:
            gradient = path_gradient(
                x,
                history,
                head,
                weights,
                eta,
                sigma_rep2,
                sigma_att2,
                amplitude_rep,
                amplitude_att,
            )
            for coord in range(dim):
                x[coord] = (
                    x[coord]
                    + epsilon * noise[step - 1, coord]
                    - eta * gradient[coord]
                )
            head = (head - 1) % memory_initial.shape[0]
            history[head] = x

        while sample_index < n_samples and sample_steps[sample_index] == step:
            position, center, tensor, radius = path_observables(
                x,
                history,
                head,
                weights,
                mass,
            )
            positions[sample_index] = position
            centers[sample_index] = center
            tensors[sample_index] = tensor
            radii[sample_index] = radius
            sample_index += 1

    return positions, centers, tensors, radii


def _validated_steps(sample_steps: Iterable[int]) -> np.ndarray:
    steps = np.asarray(list(sample_steps), dtype=int)
    if steps.ndim != 1 or steps.size < 2 or steps[0] != 0:
        raise ValueError("sample_steps must start at zero and contain two points")
    if np.any(steps < 0) or not np.array_equal(steps, np.unique(steps)):
        raise ValueError("sample_steps must be strictly increasing")
    return steps


def autonomous_knot_trace(
    state: FiniteMemoryState,
    config: SimulationConfig,
    *,
    noise: Iterable[Iterable[float]],
    sample_steps: Iterable[int],
) -> AutonomousKnotTrace:
    """Continue a scalar knot while retaining its complete sampled shape tensor."""

    validate_simulation_config(config)
    if state.dim != config.dim:
        raise ValueError("state and config dimensions must match")
    steps = _validated_steps(sample_steps)
    noise_values = np.asarray(noise, dtype=float)
    expected_shape = (int(steps[-1]), config.dim)
    if noise_values.shape != expected_shape or not np.isfinite(noise_values).all():
        raise ValueError(f"noise must have shape {expected_shape} and be finite")
    effective = effective_double_gaussian_parameters(
        dim=config.dim,
        sigma_rep=config.sigma_rep,
        sigma_att=config.sigma_att,
        amplitude_rep=config.amplitude_rep,
        amplitude_att=config.amplitude_att,
        deposition_kernel=config.deposition_kernel,
        deposition_sigma=config.deposition_sigma,
    )
    positions, centers, tensors, radii = _autonomous_knot_batch(
        state.x,
        state.memory,
        state.weights,
        noise_values,
        steps,
        float(config.epsilon),
        float(config.eta),
        float(effective["sigma_rep"]) ** 2,
        float(effective["sigma_att"]) ** 2,
        float(effective["amplitude_rep"]),
        float(effective["amplitude_att"]),
    )
    initial_radius = float(radii[0])
    if initial_radius <= 0.0:
        raise ValueError("initial memory radius must be positive")
    return AutonomousKnotTrace(
        sample_steps=steps,
        positions=positions,
        memory_centers=centers,
        shape_tensors=tensors,
        radius_ratios=radii / initial_radius,
    )
