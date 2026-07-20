"""One-way coupled finite-memory knots with paired scalar controls."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from ._continuation import path_gradient, path_observables
from .core import SimulationConfig, validate_simulation_config
from .kernels import effective_double_gaussian_parameters
from .state import FiniteMemoryState, memory_centroid, place_finite_memory_state

try:
    from numba import njit
except ImportError:  # pragma: no cover

    def njit(*args, **kwargs):
        def wrapper(func):
            return func

        return wrapper


TARGET_CONDITIONS = (
    "dynamic_source",
    "frozen_source",
    "free",
    "eta_zero_dynamic",
)


@dataclass(frozen=True)
class RelativeOrbitalObservables:
    """Finite-difference relational motion between two memory centres."""

    relative_centers: np.ndarray
    relative_velocities: np.ndarray
    radial_velocities: np.ndarray
    tangential_speeds: np.ndarray
    angular_momentum_tensors: np.ndarray
    angular_momentum_norms: np.ndarray


@dataclass(frozen=True)
class OneWayCoupledResponse:
    """One dynamic source and four paired target-control paths."""

    sample_steps: np.ndarray
    target_conditions: tuple[str, ...]
    source_positions: np.ndarray
    source_memory_centers: np.ndarray
    source_shape_tensors: np.ndarray
    source_radius_ratios: np.ndarray
    target_positions: np.ndarray
    target_memory_centers: np.ndarray
    target_shape_tensors: np.ndarray
    target_radius_ratios: np.ndarray
    source_center_offset: np.ndarray
    cross_eta: float


@njit(cache=True)
def _copy_ring(values: np.ndarray, n_paths: int) -> np.ndarray:
    result = np.empty((n_paths, values.shape[0], values.shape[1]), np.float64)
    for path in range(n_paths):
        result[path] = values
    return result


@njit(cache=True)
def _one_way_batch(
    target_x_initial: np.ndarray,
    target_memory_initial: np.ndarray,
    target_weights: np.ndarray,
    source_x_initial: np.ndarray,
    source_memory_initial: np.ndarray,
    source_weights: np.ndarray,
    target_noise: np.ndarray,
    source_noise: np.ndarray,
    sample_steps: np.ndarray,
    source_drive: np.ndarray,
    target_epsilon: float,
    target_eta: float,
    source_epsilon: float,
    source_eta: float,
    target_sigma_rep2: float,
    target_sigma_att2: float,
    target_amplitude_rep: float,
    target_amplitude_att: float,
    source_sigma_rep2: float,
    source_sigma_att2: float,
    source_amplitude_rep: float,
    source_amplitude_att: float,
    cross_eta: float,
):
    n_paths = 4
    dynamic_path = 0
    frozen_path = 1
    free_path = 2
    eta_zero_path = 3
    dim = target_x_initial.shape[0]
    n_samples = sample_steps.shape[0]

    target_x = np.empty((n_paths, dim), np.float64)
    for path in range(n_paths):
        target_x[path] = target_x_initial
    target_history = _copy_ring(target_memory_initial, n_paths)
    target_heads = np.zeros(n_paths, np.int64)

    source_x = source_x_initial.copy()
    source_history = source_memory_initial.copy()
    source_head = 0

    source_positions = np.empty((n_samples, dim), np.float64)
    source_centers = np.empty((n_samples, dim), np.float64)
    source_tensors = np.empty((n_samples, dim, dim), np.float64)
    source_radii = np.empty(n_samples, np.float64)
    target_positions = np.empty((n_samples, n_paths, dim), np.float64)
    target_centers = np.empty((n_samples, n_paths, dim), np.float64)
    target_tensors = np.empty((n_samples, n_paths, dim, dim), np.float64)
    target_radii = np.empty((n_samples, n_paths), np.float64)

    target_mass = np.sum(target_weights)
    source_mass = np.sum(source_weights)
    sample_index = 0
    n_steps = int(sample_steps[-1])

    for step in range(n_steps + 1):
        if step > 0:
            source_self_gradient = path_gradient(
                source_x,
                source_history,
                source_head,
                source_weights,
                source_eta,
                source_sigma_rep2,
                source_sigma_att2,
                source_amplitude_rep,
                source_amplitude_att,
            )
            target_self_gradients = np.empty((n_paths, dim), np.float64)
            target_cross_gradients = np.zeros((n_paths, dim), np.float64)
            for path in range(n_paths):
                self_eta = 0.0 if path == eta_zero_path else target_eta
                target_self_gradients[path] = path_gradient(
                    target_x[path],
                    target_history[path],
                    target_heads[path],
                    target_weights,
                    self_eta,
                    target_sigma_rep2,
                    target_sigma_att2,
                    target_amplitude_rep,
                    target_amplitude_att,
                )
                if path == dynamic_path or path == eta_zero_path:
                    target_cross_gradients[path] = path_gradient(
                        target_x[path],
                        source_history,
                        source_head,
                        source_weights,
                        1.0,
                        source_sigma_rep2,
                        source_sigma_att2,
                        source_amplitude_rep,
                        source_amplitude_att,
                    )
                elif path == frozen_path:
                    target_cross_gradients[path] = path_gradient(
                        target_x[path],
                        source_memory_initial,
                        0,
                        source_weights,
                        1.0,
                        source_sigma_rep2,
                        source_sigma_att2,
                        source_amplitude_rep,
                        source_amplitude_att,
                    )

            for path in range(n_paths):
                self_eta = 0.0 if path == eta_zero_path else target_eta
                path_cross_eta = 0.0 if path == free_path else cross_eta
                for coord in range(dim):
                    target_x[path, coord] = (
                        target_x[path, coord]
                        + target_epsilon * target_noise[step - 1, coord]
                        - self_eta * target_self_gradients[path, coord]
                        - path_cross_eta * target_cross_gradients[path, coord]
                    )
                target_heads[path] = (
                    target_heads[path] - 1
                ) % target_memory_initial.shape[0]
                target_history[path, target_heads[path]] = target_x[path]

            for coord in range(dim):
                source_x[coord] = (
                    source_x[coord]
                    + source_epsilon * source_noise[step - 1, coord]
                    - source_eta * source_self_gradient[coord]
                    + source_drive[step - 1, coord]
                )
            source_head = (source_head - 1) % source_memory_initial.shape[0]
            source_history[source_head] = source_x

        while sample_index < n_samples and sample_steps[sample_index] == step:
            source_position, source_center, source_tensor, source_radius = (
                path_observables(
                    source_x,
                    source_history,
                    source_head,
                    source_weights,
                    source_mass,
                )
            )
            source_positions[sample_index] = source_position
            source_centers[sample_index] = source_center
            source_radii[sample_index] = source_radius
            source_tensors[sample_index] = source_tensor
            for path in range(n_paths):
                position, center, tensor, radius = path_observables(
                    target_x[path],
                    target_history[path],
                    target_heads[path],
                    target_weights,
                    target_mass,
                )
                target_positions[sample_index, path] = position
                target_centers[sample_index, path] = center
                target_tensors[sample_index, path] = tensor
                target_radii[sample_index, path] = radius
            sample_index += 1

    return (
        source_positions,
        source_centers,
        source_tensors,
        source_radii,
        target_positions,
        target_centers,
        target_tensors,
        target_radii,
    )


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


def one_way_coupled_response(
    target_state: FiniteMemoryState,
    source_state: FiniteMemoryState,
    target_config: SimulationConfig,
    *,
    source_center_offset: Iterable[float],
    target_noise: Iterable[Iterable[float]],
    source_noise: Iterable[Iterable[float]],
    source_drive: Iterable[Iterable[float]] | None = None,
    sample_steps: Iterable[int],
    cross_eta: float,
    source_config: SimulationConfig | None = None,
    source_rotation: Iterable[Iterable[float]] | None = None,
) -> OneWayCoupledResponse:
    """Evolve a source autonomously while paired target paths read its field."""

    validate_simulation_config(target_config)
    source_cfg = target_config if source_config is None else source_config
    validate_simulation_config(source_cfg)
    if target_state.dim != source_state.dim or target_state.dim != target_config.dim:
        raise ValueError("target, source, and target_config must share one dimension")
    if source_cfg.dim != target_state.dim:
        raise ValueError("source_config dimension must match the states")
    if not np.isfinite(cross_eta) or cross_eta < 0.0:
        raise ValueError("cross_eta must be non-negative and finite")

    offset = np.asarray(source_center_offset, dtype=float)
    if offset.shape != (target_state.dim,) or not np.isfinite(offset).all():
        raise ValueError(
            "source_center_offset must be a finite dimension-matched vector"
        )
    if float(np.linalg.norm(offset)) <= 0.0:
        raise ValueError("source_center_offset must be non-zero")
    placed_source = place_finite_memory_state(
        source_state,
        memory_centroid(target_state) + offset,
        rotation=source_rotation,
    )
    steps = _validated_steps(sample_steps)
    n_steps = int(steps[-1])
    if source_drive is None:
        source_drive_values = np.zeros((n_steps, target_state.dim), dtype=float)
    else:
        source_drive_values = _validated_noise(
            source_drive,
            n_steps=n_steps,
            dim=target_state.dim,
            name="source_drive",
        )
    target_noise_values = _validated_noise(
        target_noise,
        n_steps=n_steps,
        dim=target_state.dim,
        name="target_noise",
    )
    source_noise_values = _validated_noise(
        source_noise,
        n_steps=n_steps,
        dim=target_state.dim,
        name="source_noise",
    )
    target_effective = effective_double_gaussian_parameters(
        dim=target_config.dim,
        sigma_rep=target_config.sigma_rep,
        sigma_att=target_config.sigma_att,
        amplitude_rep=target_config.amplitude_rep,
        amplitude_att=target_config.amplitude_att,
        deposition_kernel=target_config.deposition_kernel,
        deposition_sigma=target_config.deposition_sigma,
    )
    source_effective = effective_double_gaussian_parameters(
        dim=source_cfg.dim,
        sigma_rep=source_cfg.sigma_rep,
        sigma_att=source_cfg.sigma_att,
        amplitude_rep=source_cfg.amplitude_rep,
        amplitude_att=source_cfg.amplitude_att,
        deposition_kernel=source_cfg.deposition_kernel,
        deposition_sigma=source_cfg.deposition_sigma,
    )
    (
        source_positions,
        source_centers,
        source_tensors,
        source_radii,
        target_positions,
        target_centers,
        target_tensors,
        target_radii,
    ) = _one_way_batch(
        target_state.x,
        target_state.memory,
        target_state.weights,
        placed_source.x,
        placed_source.memory,
        placed_source.weights,
        target_noise_values,
        source_noise_values,
        steps,
        source_drive_values,
        float(target_config.epsilon),
        float(target_config.eta),
        float(source_cfg.epsilon),
        float(source_cfg.eta),
        float(target_effective["sigma_rep"]) ** 2,
        float(target_effective["sigma_att"]) ** 2,
        float(target_effective["amplitude_rep"]),
        float(target_effective["amplitude_att"]),
        float(source_effective["sigma_rep"]) ** 2,
        float(source_effective["sigma_att"]) ** 2,
        float(source_effective["amplitude_rep"]),
        float(source_effective["amplitude_att"]),
        float(cross_eta),
    )
    target_initial_radius = float(target_radii[0, 0])
    source_initial_radius = float(source_radii[0])
    if target_initial_radius <= 0.0 or source_initial_radius <= 0.0:
        raise ValueError("target and source memory radii must be positive")
    return OneWayCoupledResponse(
        sample_steps=steps,
        target_conditions=TARGET_CONDITIONS,
        source_positions=source_positions,
        source_memory_centers=source_centers,
        source_shape_tensors=source_tensors,
        source_radius_ratios=source_radii / source_initial_radius,
        target_positions=target_positions,
        target_memory_centers=target_centers,
        target_shape_tensors=target_tensors,
        target_radius_ratios=target_radii / target_initial_radius,
        source_center_offset=offset,
        cross_eta=float(cross_eta),
    )


def relative_orbital_observables(
    target_memory_centers: np.ndarray,
    source_memory_centers: np.ndarray,
    sample_steps: Iterable[int],
) -> RelativeOrbitalObservables:
    """Compute radial, tangential, and antisymmetric relational motion."""

    target = np.asarray(target_memory_centers, dtype=float)
    source = np.asarray(source_memory_centers, dtype=float)
    steps = np.asarray(list(sample_steps), dtype=float)
    if (
        target.ndim != 2
        or target.shape != source.shape
        or target.shape[0] != steps.size
        or target.shape[0] < 2
        or not np.isfinite(target).all()
        or not np.isfinite(source).all()
        or not np.isfinite(steps).all()
        or np.any(np.diff(steps) <= 0.0)
    ):
        raise ValueError("centres and sample_steps must be finite and compatible")

    relative = target - source
    velocities = np.diff(relative, axis=0) / np.diff(steps)[:, None]
    midpoint = 0.5 * (relative[1:] + relative[:-1])
    radii = np.linalg.norm(midpoint, axis=1)
    unit = np.divide(
        midpoint,
        radii[:, None],
        out=np.zeros_like(midpoint),
        where=radii[:, None] > 0.0,
    )
    radial = np.sum(velocities * unit, axis=1)
    tangential_vectors = velocities - radial[:, None] * unit
    tangential = np.linalg.norm(tangential_vectors, axis=1)

    dim = target.shape[1]
    tensors = np.empty((len(velocities), dim, dim), dtype=float)
    for index, (position, velocity) in enumerate(
        zip(midpoint, velocities, strict=True)
    ):
        tensors[index] = np.outer(position, velocity) - np.outer(velocity, position)
    norms = np.linalg.norm(tensors, axis=(1, 2)) / np.sqrt(2.0)
    return RelativeOrbitalObservables(
        relative_centers=relative,
        relative_velocities=velocities,
        radial_velocities=radial,
        tangential_speeds=tangential,
        angular_momentum_tensors=tensors,
        angular_momentum_norms=norms,
    )
