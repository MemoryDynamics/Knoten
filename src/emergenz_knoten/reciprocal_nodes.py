"""Paired full-knot continuations with synchronous reciprocal readout."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from ._continuation import path_gradient, path_observables
from .core import SimulationConfig, validate_simulation_config
from .kernels import (
    ScalarReadoutKernel,
    effective_double_gaussian_parameters,
    resolve_scalar_readout_kernel,
)
from .state import FiniteMemoryState, memory_centroid, place_finite_memory_state

try:
    from numba import njit
except ImportError:  # pragma: no cover

    def njit(*args, **kwargs):
        def wrapper(func):
            return func

        return wrapper


RECIPROCAL_CONDITIONS = ("channel_off", "one_way", "reciprocal")


@dataclass(frozen=True)
class ReciprocalPairResponse:
    """Common-noise continuations for off, one-way, and reciprocal channels."""

    sample_steps: np.ndarray
    conditions: tuple[str, ...]
    positions: np.ndarray
    memory_centers: np.ndarray
    shape_tensors: np.ndarray
    radius_ratios: np.ndarray
    initial_center_separation: np.ndarray
    cross_eta: float
    cross_readout: ScalarReadoutKernel


@njit(cache=True)
def _copy_pair_ring(
    first: np.ndarray,
    second: np.ndarray,
    n_conditions: int,
) -> np.ndarray:
    histories = np.empty(
        (n_conditions, 2, first.shape[0], first.shape[1]),
        np.float64,
    )
    for condition in range(n_conditions):
        histories[condition, 0] = first
        histories[condition, 1] = second
    return histories


@njit(cache=True)
def _reciprocal_pair_batch(
    first_x_initial: np.ndarray,
    first_memory_initial: np.ndarray,
    first_weights: np.ndarray,
    second_x_initial: np.ndarray,
    second_memory_initial: np.ndarray,
    second_weights: np.ndarray,
    first_noise: np.ndarray,
    second_noise: np.ndarray,
    sample_steps: np.ndarray,
    first_epsilon: float,
    first_eta: float,
    second_epsilon: float,
    second_eta: float,
    first_sigma_rep2: float,
    first_sigma_att2: float,
    first_amplitude_rep: float,
    first_amplitude_att: float,
    second_sigma_rep2: float,
    second_sigma_att2: float,
    second_amplitude_rep: float,
    second_amplitude_att: float,
    cross_sigma_rep2: float,
    cross_sigma_att2: float,
    cross_amplitude_rep: float,
    cross_amplitude_att: float,
    cross_eta: float,
):
    n_conditions = 3
    one_way_condition = 1
    reciprocal_condition = 2
    dim = first_x_initial.shape[0]
    n_samples = sample_steps.shape[0]

    positions_now = np.empty((n_conditions, 2, dim), np.float64)
    for condition in range(n_conditions):
        positions_now[condition, 0] = first_x_initial
        positions_now[condition, 1] = second_x_initial
    histories = _copy_pair_ring(
        first_memory_initial,
        second_memory_initial,
        n_conditions,
    )
    heads = np.zeros((n_conditions, 2), np.int64)

    positions = np.empty((n_samples, n_conditions, 2, dim), np.float64)
    centers = np.empty((n_samples, n_conditions, 2, dim), np.float64)
    tensors = np.empty((n_samples, n_conditions, 2, dim, dim), np.float64)
    radii = np.empty((n_samples, n_conditions, 2), np.float64)
    masses = np.array((np.sum(first_weights), np.sum(second_weights)))
    sample_index = 0
    n_steps = int(sample_steps[-1])

    for step in range(n_steps + 1):
        if step > 0:
            self_gradients = np.empty((n_conditions, 2, dim), np.float64)
            cross_gradients = np.zeros((n_conditions, 2, dim), np.float64)
            for condition in range(n_conditions):
                self_gradients[condition, 0] = path_gradient(
                    positions_now[condition, 0],
                    histories[condition, 0],
                    heads[condition, 0],
                    first_weights,
                    first_eta,
                    first_sigma_rep2,
                    first_sigma_att2,
                    first_amplitude_rep,
                    first_amplitude_att,
                )
                self_gradients[condition, 1] = path_gradient(
                    positions_now[condition, 1],
                    histories[condition, 1],
                    heads[condition, 1],
                    second_weights,
                    second_eta,
                    second_sigma_rep2,
                    second_sigma_att2,
                    second_amplitude_rep,
                    second_amplitude_att,
                )

                if condition == one_way_condition:
                    cross_gradients[condition, 1] = path_gradient(
                        positions_now[condition, 1],
                        histories[condition, 0],
                        heads[condition, 0],
                        first_weights,
                        1.0,
                        cross_sigma_rep2,
                        cross_sigma_att2,
                        cross_amplitude_rep,
                        cross_amplitude_att,
                    )
                elif condition == reciprocal_condition:
                    # Both gradients use z_n. Neither node sees the other's z_{n+1}.
                    cross_gradients[condition, 0] = path_gradient(
                        positions_now[condition, 0],
                        histories[condition, 1],
                        heads[condition, 1],
                        second_weights,
                        1.0,
                        cross_sigma_rep2,
                        cross_sigma_att2,
                        cross_amplitude_rep,
                        cross_amplitude_att,
                    )
                    cross_gradients[condition, 1] = path_gradient(
                        positions_now[condition, 1],
                        histories[condition, 0],
                        heads[condition, 0],
                        first_weights,
                        1.0,
                        cross_sigma_rep2,
                        cross_sigma_att2,
                        cross_amplitude_rep,
                        cross_amplitude_att,
                    )

            for condition in range(n_conditions):
                for coord in range(dim):
                    positions_now[condition, 0, coord] = (
                        positions_now[condition, 0, coord]
                        + first_epsilon * first_noise[step - 1, coord]
                        - first_eta * self_gradients[condition, 0, coord]
                        - cross_eta * cross_gradients[condition, 0, coord]
                    )
                    positions_now[condition, 1, coord] = (
                        positions_now[condition, 1, coord]
                        + second_epsilon * second_noise[step - 1, coord]
                        - second_eta * self_gradients[condition, 1, coord]
                        - cross_eta * cross_gradients[condition, 1, coord]
                    )
                for node in range(2):
                    heads[condition, node] = (
                        heads[condition, node] - 1
                    ) % first_memory_initial.shape[0]
                    histories[
                        condition,
                        node,
                        heads[condition, node],
                    ] = positions_now[condition, node]

        while sample_index < n_samples and sample_steps[sample_index] == step:
            for condition in range(n_conditions):
                for node in range(2):
                    weights = first_weights if node == 0 else second_weights
                    position, center, tensor, radius = path_observables(
                        positions_now[condition, node],
                        histories[condition, node],
                        heads[condition, node],
                        weights,
                        masses[node],
                    )
                    positions[sample_index, condition, node] = position
                    centers[sample_index, condition, node] = center
                    tensors[sample_index, condition, node] = tensor
                    radii[sample_index, condition, node] = radius
            sample_index += 1

    return positions, centers, tensors, radii


def _validated_steps(sample_steps: Iterable[int]) -> np.ndarray:
    steps = np.asarray(list(sample_steps), dtype=int)
    if steps.ndim != 1 or steps.size < 2 or np.any(steps < 0):
        raise ValueError("sample_steps must contain at least two non-negative values")
    if not np.array_equal(steps, np.unique(steps)):
        raise ValueError("sample_steps must be strictly increasing")
    return steps


def _validated_noise(
    noise: Iterable[Iterable[float]],
    *,
    n_steps: int,
    dim: int,
    name: str,
) -> np.ndarray:
    values = np.asarray(noise, dtype=float)
    if values.shape != (n_steps, dim) or not np.isfinite(values).all():
        raise ValueError(f"{name} must have shape (max(sample_steps), dim) and be finite")
    return values


def reciprocal_pair_response(
    first_state: FiniteMemoryState,
    second_state: FiniteMemoryState,
    first_config: SimulationConfig,
    *,
    initial_center_separation: Iterable[float],
    first_noise: Iterable[Iterable[float]],
    second_noise: Iterable[Iterable[float]],
    sample_steps: Iterable[int],
    cross_eta: float,
    second_config: SimulationConfig | None = None,
    cross_readout: ScalarReadoutKernel | None = None,
    second_rotation: Iterable[Iterable[float]] | None = None,
) -> ReciprocalPairResponse:
    """Run three paired two-knot arms with a synchronous reciprocal update.

    The one-way arm evolves node 0 autonomously while node 1 reads node 0.
    The reciprocal arm computes both cross-gradients from the pre-update state.
    Node-specific future noise is identical across all three conditions.
    """

    validate_simulation_config(first_config)
    second_cfg = first_config if second_config is None else second_config
    validate_simulation_config(second_cfg)
    if first_state.dim != second_state.dim or first_state.dim != first_config.dim:
        raise ValueError("states and first_config must share one dimension")
    if second_cfg.dim != first_state.dim:
        raise ValueError("second_config dimension must match the states")
    if first_state.n_memory != second_state.n_memory:
        raise ValueError("paired states must use the same retained memory horizon")
    if not np.isfinite(cross_eta) or cross_eta < 0.0:
        raise ValueError("cross_eta must be non-negative and finite")

    separation = np.asarray(initial_center_separation, dtype=float)
    if separation.shape != (first_state.dim,) or not np.isfinite(separation).all():
        raise ValueError("initial_center_separation must match state dimension")
    if float(np.linalg.norm(separation)) <= 0.0:
        raise ValueError("initial_center_separation must be non-zero")
    midpoint = 0.5 * (memory_centroid(first_state) + memory_centroid(second_state))
    placed_first = place_finite_memory_state(first_state, midpoint - 0.5 * separation)
    placed_second = place_finite_memory_state(
        second_state,
        midpoint + 0.5 * separation,
        rotation=second_rotation,
    )

    steps = _validated_steps(sample_steps)
    n_steps = int(steps[-1])
    first_noise_values = _validated_noise(
        first_noise,
        n_steps=n_steps,
        dim=first_state.dim,
        name="first_noise",
    )
    second_noise_values = _validated_noise(
        second_noise,
        n_steps=n_steps,
        dim=first_state.dim,
        name="second_noise",
    )
    cross_kernel = resolve_scalar_readout_kernel(
        cross_readout,
        sigma_rep=first_config.sigma_rep,
        sigma_att=first_config.sigma_att,
        amplitude_rep=first_config.amplitude_rep,
        amplitude_att=first_config.amplitude_att,
    )
    first_effective = effective_double_gaussian_parameters(
        dim=first_config.dim,
        sigma_rep=first_config.sigma_rep,
        sigma_att=first_config.sigma_att,
        amplitude_rep=first_config.amplitude_rep,
        amplitude_att=first_config.amplitude_att,
        deposition_kernel=first_config.deposition_kernel,
        deposition_sigma=first_config.deposition_sigma,
    )
    second_effective = effective_double_gaussian_parameters(
        dim=second_cfg.dim,
        sigma_rep=second_cfg.sigma_rep,
        sigma_att=second_cfg.sigma_att,
        amplitude_rep=second_cfg.amplitude_rep,
        amplitude_att=second_cfg.amplitude_att,
        deposition_kernel=second_cfg.deposition_kernel,
        deposition_sigma=second_cfg.deposition_sigma,
    )
    cross_effective = effective_double_gaussian_parameters(
        dim=first_config.dim,
        sigma_rep=cross_kernel.sigma_rep,
        sigma_att=cross_kernel.sigma_att,
        amplitude_rep=cross_kernel.amplitude_rep,
        amplitude_att=cross_kernel.amplitude_att,
        deposition_kernel=first_config.deposition_kernel,
        deposition_sigma=first_config.deposition_sigma,
    )
    positions, centers, tensors, radii = _reciprocal_pair_batch(
        placed_first.x,
        placed_first.memory,
        placed_first.weights,
        placed_second.x,
        placed_second.memory,
        placed_second.weights,
        first_noise_values,
        second_noise_values,
        steps,
        float(first_config.epsilon),
        float(first_config.eta),
        float(second_cfg.epsilon),
        float(second_cfg.eta),
        float(first_effective["sigma_rep"]) ** 2,
        float(first_effective["sigma_att"]) ** 2,
        float(first_effective["amplitude_rep"]),
        float(first_effective["amplitude_att"]),
        float(second_effective["sigma_rep"]) ** 2,
        float(second_effective["sigma_att"]) ** 2,
        float(second_effective["amplitude_rep"]),
        float(second_effective["amplitude_att"]),
        float(cross_effective["sigma_rep"]) ** 2,
        float(cross_effective["sigma_att"]) ** 2,
        float(cross_effective["amplitude_rep"]),
        float(cross_effective["amplitude_att"]),
        float(cross_eta),
    )
    initial_radii = radii[0]
    if np.any(initial_radii <= 0.0):
        raise ValueError("both initial memory radii must be positive")
    return ReciprocalPairResponse(
        sample_steps=steps,
        conditions=RECIPROCAL_CONDITIONS,
        positions=positions,
        memory_centers=centers,
        shape_tensors=tensors,
        radius_ratios=radii / initial_radii[None, :, :],
        initial_center_separation=separation,
        cross_eta=float(cross_eta),
        cross_readout=cross_kernel,
    )
