"""Reciprocal full-knot continuations through a fixed Telegraph channel.

The mediator grid is a one-dimensional source-target reference axis carrying
independent ambient-vector components.  It is kept fixed during a continuation
to isolate temporal retardation from moving-grid geometry.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

import numpy as np

from ._continuation import path_gradient, path_observables
from .core import SimulationConfig, validate_simulation_config
from .kernels import (
    ScalarReadoutKernel,
    effective_double_gaussian_parameters,
    resolve_scalar_readout_kernel,
)
from .local_mediator import LocalMediatorGrid, TelegraphMediator
from .state import FiniteMemoryState, memory_centroid, place_finite_memory_state

try:
    from numba import njit
except ImportError:  # pragma: no cover

    def njit(*args, **kwargs):
        def wrapper(func):
            return func

        return wrapper


RETARDED_RECIPROCAL_CONDITIONS = (
    "channel_off",
    "instantaneous_reciprocal",
    "retarded_one_way",
    "retarded_reciprocal",
)


@dataclass(frozen=True)
class RetardedReciprocalPairResponse:
    """Common-noise pair continuations with direct and retarded controls."""

    sample_steps: np.ndarray
    conditions: tuple[str, ...]
    positions: np.ndarray
    memory_centers: np.ndarray
    shape_tensors: np.ndarray
    radius_ratios: np.ndarray
    mediator_readouts: np.ndarray
    mediator_inputs: np.ndarray
    initial_center_separation: np.ndarray
    cross_eta: float
    cross_readout: ScalarReadoutKernel
    mediator_grid: LocalMediatorGrid
    mediator: TelegraphMediator
    mediator_readout_position: float
    static_readout_gain: float
    source_normalization: float


def telegraph_static_readout_gain(
    grid: LocalMediatorGrid,
    mediator: TelegraphMediator,
    *,
    readout_position: float,
) -> float:
    """Return the finite-grid DC readout from a unit point source.

    This solves the discrete stationary equation with the same homogeneous
    Dirichlet boundaries as the time-domain Telegraph update.
    """

    position = float(readout_position)
    coordinates = grid.coordinates
    if not math.isfinite(position) or not coordinates[0] < position < coordinates[-1]:
        raise ValueError("readout_position must lie strictly inside the grid")
    floating_index = position / grid.spacing + grid.source_index
    left_index = int(math.floor(floating_index))
    fraction = floating_index - left_index

    interior_points = grid.n_points - 2
    laplacian_scale = mediator.wave_speed**2 / grid.spacing**2
    operator = np.zeros((interior_points, interior_points), dtype=float)
    np.fill_diagonal(
        operator,
        2.0 * laplacian_scale + mediator.natural_frequency**2,
    )
    np.fill_diagonal(operator[1:], -laplacian_scale)
    np.fill_diagonal(operator[:, 1:], -laplacian_scale)
    source = np.zeros(interior_points, dtype=float)
    source[grid.source_index - 1] = 1.0 / grid.spacing
    interior = np.linalg.solve(operator, source)
    field = np.zeros(grid.n_points, dtype=float)
    field[1:-1] = interior
    gain = float(
        field[left_index] + fraction * (field[left_index + 1] - field[left_index])
    )
    if not math.isfinite(gain) or gain <= 0.0:
        raise ValueError("static readout gain must be positive and finite")
    return gain


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
def _advance_channel(
    field: np.ndarray,
    momentum: np.ndarray,
    source: np.ndarray,
    source_index: int,
    source_normalization: float,
    spacing: float,
    time_step: float,
    wave_speed: float,
    damping_rate: float,
    natural_frequency: float,
) -> tuple[np.ndarray, np.ndarray]:
    updated_momentum = np.zeros_like(momentum)
    updated_field = np.zeros_like(field)
    wave_factor = wave_speed * wave_speed / (spacing * spacing)
    restoring = natural_frequency * natural_frequency
    for component in range(field.shape[0]):
        for index in range(1, field.shape[1] - 1):
            laplacian = (
                field[component, index - 1]
                - 2.0 * field[component, index]
                + field[component, index + 1]
            )
            acceleration = (
                wave_factor * laplacian
                - 2.0 * damping_rate * momentum[component, index]
                - restoring * field[component, index]
            )
            updated_momentum[component, index] = (
                momentum[component, index] + time_step * acceleration
            )
        updated_momentum[component, source_index] += (
            time_step * source_normalization * source[component] / spacing
        )
        for index in range(1, field.shape[1] - 1):
            updated_field[component, index] = (
                field[component, index] + time_step * updated_momentum[component, index]
            )
    return updated_field, updated_momentum


@njit(cache=True)
def _field_readout(
    field: np.ndarray,
    left_index: int,
    fraction: float,
) -> np.ndarray:
    return field[:, left_index] + fraction * (
        field[:, left_index + 1] - field[:, left_index]
    )


@njit(cache=True)
def _retarded_pair_batch(
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
    grid_points: int,
    source_index: int,
    target_left_index: int,
    target_fraction: float,
    source_normalization: float,
    spacing: float,
    time_step: float,
    wave_speed: float,
    damping_rate: float,
    natural_frequency: float,
):
    n_conditions = 4
    direct_condition = 1
    retarded_one_way_condition = 2
    retarded_reciprocal_condition = 3
    dim = first_x_initial.shape[0]
    n_samples = sample_steps.shape[0]

    positions_now = np.empty((n_conditions, 2, dim), np.float64)
    for condition in range(n_conditions):
        positions_now[condition, 0] = first_x_initial
        positions_now[condition, 1] = second_x_initial
    histories = _copy_pair_ring(
        first_memory_initial, second_memory_initial, n_conditions
    )
    heads = np.zeros((n_conditions, 2), np.int64)

    # Two directions: 0 -> 1 and 1 -> 0. Only retarded arms own fields.
    fields = np.zeros((2, 2, dim, grid_points), np.float64)
    momenta = np.zeros_like(fields)
    current_inputs = np.zeros((n_conditions, 2, dim), np.float64)
    current_readouts = np.zeros((n_conditions, 2, dim), np.float64)

    positions = np.empty((n_samples, n_conditions, 2, dim), np.float64)
    centers = np.empty((n_samples, n_conditions, 2, dim), np.float64)
    tensors = np.empty((n_samples, n_conditions, 2, dim, dim), np.float64)
    radii = np.empty((n_samples, n_conditions, 2), np.float64)
    readouts = np.empty((n_samples, n_conditions, 2, dim), np.float64)
    inputs = np.empty((n_samples, n_conditions, 2, dim), np.float64)
    masses = np.array((np.sum(first_weights), np.sum(second_weights)))
    sample_index = 0
    n_steps = int(sample_steps[-1])

    for step in range(n_steps + 1):
        if step > 0:
            self_gradients = np.empty((n_conditions, 2, dim), np.float64)
            current_inputs[:] = 0.0
            current_readouts[:] = 0.0
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

                if condition > 0:
                    current_inputs[condition, 0] = path_gradient(
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
                    if condition != retarded_one_way_condition:
                        current_inputs[condition, 1] = path_gradient(
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

            current_readouts[direct_condition] = current_inputs[direct_condition]
            for field_condition, condition in enumerate(
                (retarded_one_way_condition, retarded_reciprocal_condition)
            ):
                directions = 1 if condition == retarded_one_way_condition else 2
                for direction in range(directions):
                    updated_field, updated_momentum = _advance_channel(
                        fields[field_condition, direction],
                        momenta[field_condition, direction],
                        current_inputs[condition, direction],
                        source_index,
                        source_normalization,
                        spacing,
                        time_step,
                        wave_speed,
                        damping_rate,
                        natural_frequency,
                    )
                    fields[field_condition, direction] = updated_field
                    momenta[field_condition, direction] = updated_momentum
                    current_readouts[condition, direction] = _field_readout(
                        updated_field, target_left_index, target_fraction
                    )

            for condition in range(n_conditions):
                for coord in range(dim):
                    # Direction 1 is the 1 -> 0 channel; direction 0 is 0 -> 1.
                    positions_now[condition, 0, coord] = (
                        positions_now[condition, 0, coord]
                        + first_epsilon * first_noise[step - 1, coord]
                        - first_eta * self_gradients[condition, 0, coord]
                        - cross_eta * current_readouts[condition, 1, coord]
                    )
                    positions_now[condition, 1, coord] = (
                        positions_now[condition, 1, coord]
                        + second_epsilon * second_noise[step - 1, coord]
                        - second_eta * self_gradients[condition, 1, coord]
                        - cross_eta * current_readouts[condition, 0, coord]
                    )
                for node in range(2):
                    heads[condition, node] = (
                        heads[condition, node] - 1
                    ) % first_memory_initial.shape[0]
                    histories[condition, node, heads[condition, node]] = positions_now[
                        condition, node
                    ]

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
            readouts[sample_index] = current_readouts
            inputs[sample_index] = current_inputs
            sample_index += 1

    return positions, centers, tensors, radii, readouts, inputs


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
        raise ValueError(
            f"{name} must have shape (max(sample_steps), dim) and be finite"
        )
    return values


def retarded_reciprocal_pair_response(
    first_state: FiniteMemoryState,
    second_state: FiniteMemoryState,
    first_config: SimulationConfig,
    *,
    initial_center_separation: Iterable[float],
    first_noise: Iterable[Iterable[float]],
    second_noise: Iterable[Iterable[float]],
    sample_steps: Iterable[int],
    cross_eta: float,
    mediator_grid: LocalMediatorGrid,
    mediator: TelegraphMediator,
    mediator_readout_position: float,
    second_config: SimulationConfig | None = None,
    cross_readout: ScalarReadoutKernel | None = None,
    second_rotation: Iterable[Iterable[float]] | None = None,
) -> RetardedReciprocalPairResponse:
    """Run off, direct, retarded one-way, and retarded reciprocal arms."""

    validate_simulation_config(first_config)
    second_cfg = first_config if second_config is None else second_config
    validate_simulation_config(second_cfg)
    if first_state.dim != second_state.dim or first_state.dim != first_config.dim:
        raise ValueError("states and first_config must share one dimension")
    if second_cfg.dim != first_state.dim:
        raise ValueError("second_config dimension must match the states")
    if first_state.n_memory != second_state.n_memory:
        raise ValueError("paired states must use the same retained memory horizon")
    if not math.isfinite(cross_eta) or cross_eta < 0.0:
        raise ValueError("cross_eta must be non-negative and finite")
    if not math.isclose(
        mediator_grid.time_step, first_config.alpha, rel_tol=0.0, abs_tol=1e-15
    ):
        raise ValueError(
            "mediator time_step must equal the model memory-time update alpha"
        )
    courant = mediator.wave_speed * mediator_grid.time_step / mediator_grid.spacing
    if courant > 1.0:
        raise ValueError("telegraph update violates the 1D Courant bound")
    if 2.0 * mediator.damping_rate * mediator_grid.time_step > 1.0:
        raise ValueError("telegraph damping is too large for the explicit update")
    if mediator.natural_frequency * mediator_grid.time_step > 1.0:
        raise ValueError("telegraph natural frequency is under-resolved")

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
        first_noise, n_steps=n_steps, dim=first_state.dim, name="first_noise"
    )
    second_noise_values = _validated_noise(
        second_noise, n_steps=n_steps, dim=first_state.dim, name="second_noise"
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

    readout_position = float(mediator_readout_position)
    floating_index = (
        readout_position / mediator_grid.spacing + mediator_grid.source_index
    )
    left_index = int(math.floor(floating_index))
    if left_index < 1 or left_index + 1 >= mediator_grid.n_points - 1:
        raise ValueError("mediator readout must be inside the interior grid")
    target_fraction = floating_index - left_index
    static_gain = telegraph_static_readout_gain(
        mediator_grid,
        mediator,
        readout_position=readout_position,
    )
    source_normalization = 1.0 / static_gain

    positions, centers, tensors, radii, readouts, inputs = _retarded_pair_batch(
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
        mediator_grid.n_points,
        mediator_grid.source_index,
        left_index,
        target_fraction,
        source_normalization,
        float(mediator_grid.spacing),
        float(mediator_grid.time_step),
        float(mediator.wave_speed),
        float(mediator.damping_rate),
        float(mediator.natural_frequency),
    )
    initial_radii = radii[0]
    if np.any(initial_radii <= 0.0):
        raise ValueError("both initial memory radii must be positive")
    return RetardedReciprocalPairResponse(
        sample_steps=steps,
        conditions=RETARDED_RECIPROCAL_CONDITIONS,
        positions=positions,
        memory_centers=centers,
        shape_tensors=tensors,
        radius_ratios=radii / initial_radii[None, :, :],
        mediator_readouts=readouts,
        mediator_inputs=inputs,
        initial_center_separation=separation,
        cross_eta=float(cross_eta),
        cross_readout=cross_kernel,
        mediator_grid=mediator_grid,
        mediator=mediator,
        mediator_readout_position=readout_position,
        static_readout_gain=static_gain,
        source_normalization=source_normalization,
    )
