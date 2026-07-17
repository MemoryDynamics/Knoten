"""Paired continuation under a locally perturbed frozen memory source."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from ._continuation import (
    path_gradient,
    path_observables,
    symmetric_tensor_vector,
)
from .core import SimulationConfig, validate_simulation_config
from .kernels import double_gaussian_gradient, effective_double_gaussian_parameters
from .state import (
    FiniteMemoryState,
    memory_centroid,
    memory_shape_tensor,
    place_finite_memory_state,
)

try:
    from numba import njit
except ImportError:  # pragma: no cover

    def njit(*args, **kwargs):
        def wrapper(func):
            return func

        return wrapper


@dataclass(frozen=True)
class FrozenSourceCalibration:
    """Cross-coupling calibrated from the unperturbed source field."""

    response_fraction: float
    pulse_steps: int
    source_center_offset: np.ndarray
    target_radius: float
    baseline_gradient_norm: float
    baseline_directional_drift: float
    cross_eta: float


@dataclass(frozen=True)
class PairedFrozenSourceResponse:
    """Local source-translation Jacobians and paired control observables."""

    sample_steps: np.ndarray
    directions: np.ndarray
    source_center_offset: np.ndarray
    perturbation: float
    cross_eta: float
    pulse_steps: int
    baseline_source_center: np.ndarray
    source_centers: np.ndarray
    baseline_initial_gradient_norm: float
    initial_source_gradient_norms: np.ndarray
    position_jacobians: np.ndarray
    memory_center_jacobians: np.ndarray
    shape_jacobians: np.ndarray
    position_even_offsets: np.ndarray
    memory_center_even_offsets: np.ndarray
    shape_even_vectors: np.ndarray
    radius_ratios: np.ndarray
    radius_even_offsets: np.ndarray
    baseline_positions: np.ndarray
    baseline_memory_centers: np.ndarray
    baseline_shape_vectors: np.ndarray
    baseline_radius_ratios: np.ndarray
    free_positions: np.ndarray
    free_memory_centers: np.ndarray
    free_shape_vectors: np.ndarray
    free_radius_ratios: np.ndarray


def _normalized_directions(
    directions: Iterable[Iterable[float]],
    *,
    dim: int,
) -> np.ndarray:
    basis = np.asarray(directions, dtype=float)
    if basis.ndim != 2 or basis.shape[1] != dim or basis.shape[0] < 1:
        raise ValueError("directions must have shape (n_probes, dim)")
    if not np.isfinite(basis).all():
        raise ValueError("directions contain non-finite values")
    norms = np.linalg.norm(basis, axis=1)
    if np.any(norms <= 0.0):
        raise ValueError("source directions must be non-zero")
    return basis / norms[:, None]


def _source_offset(
    source_center_offset: Iterable[float],
    *,
    dim: int,
) -> np.ndarray:
    offset = np.asarray(source_center_offset, dtype=float)
    if offset.shape != (dim,) or not np.isfinite(offset).all():
        raise ValueError(
            "source_center_offset must be a finite vector matching dimension"
        )
    if float(np.linalg.norm(offset)) <= 0.0:
        raise ValueError("source_center_offset must be non-zero")
    return offset


def _source_placements(
    target_state: FiniteMemoryState,
    source_state: FiniteMemoryState,
    directions: np.ndarray,
    source_center_offset: np.ndarray,
    perturbation: float,
    source_rotation: Iterable[Iterable[float]] | None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    target_center = memory_centroid(target_state)
    baseline_center = target_center + source_center_offset
    baseline_state = place_finite_memory_state(
        source_state,
        baseline_center,
        rotation=source_rotation,
    )
    source_centers = np.empty((len(directions), 2, target_state.dim), dtype=float)
    source_memories = np.empty(
        (len(directions), 2, source_state.n_memory, target_state.dim),
        dtype=float,
    )
    for probe_index, direction in enumerate(directions):
        for branch, sign in enumerate((1.0, -1.0)):
            center = baseline_center + sign * perturbation * direction
            placed = place_finite_memory_state(
                source_state,
                center,
                rotation=source_rotation,
            )
            source_centers[probe_index, branch] = center
            source_memories[probe_index, branch] = placed.memory
    return (
        baseline_center,
        baseline_state.memory,
        source_centers,
        source_memories,
    )


def _source_gradient(
    target_state: FiniteMemoryState,
    source_memory: np.ndarray,
    source_state: FiniteMemoryState,
    source_config: SimulationConfig,
) -> np.ndarray:
    return double_gaussian_gradient(
        target_state.x,
        source_memory,
        source_state.weights,
        sigma_rep=source_config.sigma_rep,
        sigma_att=source_config.sigma_att,
        amplitude_rep=source_config.amplitude_rep,
        amplitude_att=source_config.amplitude_att,
        deposition_kernel=source_config.deposition_kernel,
        deposition_sigma=source_config.deposition_sigma,
    )


def _source_gradient_norm(
    target_state: FiniteMemoryState,
    source_memory: np.ndarray,
    source_state: FiniteMemoryState,
    source_config: SimulationConfig,
) -> float:
    return float(
        np.linalg.norm(
            _source_gradient(
                target_state,
                source_memory,
                source_state,
                source_config,
            )
        )
    )


def _initial_gradient_norms(
    target_state: FiniteMemoryState,
    source_state: FiniteMemoryState,
    baseline_source_memory: np.ndarray,
    source_memories: np.ndarray,
    source_config: SimulationConfig,
) -> tuple[float, np.ndarray]:
    baseline_norm = _source_gradient_norm(
        target_state,
        baseline_source_memory,
        source_state,
        source_config,
    )
    norms = np.empty(source_memories.shape[:2], dtype=float)
    for probe_index in range(source_memories.shape[0]):
        for branch in range(2):
            norms[probe_index, branch] = _source_gradient_norm(
                target_state,
                source_memories[probe_index, branch],
                source_state,
                source_config,
            )
    return baseline_norm, norms


def calibrate_frozen_source_cross_eta(
    target_state: FiniteMemoryState,
    source_state: FiniteMemoryState,
    target_config: SimulationConfig,
    *,
    source_center_offset: Iterable[float],
    response_fraction: float,
    pulse_steps: int,
    source_config: SimulationConfig | None = None,
    source_rotation: Iterable[Iterable[float]] | None = None,
) -> FrozenSourceCalibration:
    """Calibrate cross-coupling from the unperturbed initial source force.

    The calibration solves
    ``eta_cross * dot(-grad Phi_source, source_direction) * pulse_steps
    = response_fraction * target_radius``. It fixes a transparent weak-
    interaction scale; it does not impose the nonlinear displacement after
    a complete pulse.
    """

    validate_simulation_config(target_config)
    source_cfg = target_config if source_config is None else source_config
    validate_simulation_config(source_cfg)
    if target_state.dim != target_config.dim or source_state.dim != target_state.dim:
        raise ValueError("target, source, and configs must share one dimension")
    if source_cfg.dim != target_state.dim:
        raise ValueError("source_config dimension must match the states")
    if not np.isfinite(response_fraction) or response_fraction <= 0.0:
        raise ValueError("response_fraction must be positive and finite")
    if isinstance(pulse_steps, bool) or not isinstance(pulse_steps, (int, np.integer)):
        raise ValueError("pulse_steps must be an integer")
    if pulse_steps < 1:
        raise ValueError("pulse_steps must be positive")

    offset = _source_offset(source_center_offset, dim=target_state.dim)
    baseline_center = memory_centroid(target_state) + offset
    baseline_source = place_finite_memory_state(
        source_state,
        baseline_center,
        rotation=source_rotation,
    )
    gradient = _source_gradient(
        target_state,
        baseline_source.memory,
        source_state,
        source_cfg,
    )
    gradient_norm = float(np.linalg.norm(gradient))
    if gradient_norm <= np.finfo(float).eps:
        raise ValueError("initial frozen-source gradient is too small to calibrate")
    source_direction = offset / np.linalg.norm(offset)
    directional_drift = float(np.dot(-gradient, source_direction))
    if directional_drift <= np.finfo(float).eps:
        raise ValueError(
            "initial frozen-source drift does not point toward the source centre"
        )
    target_radius = float(
        np.sqrt(max(np.trace(memory_shape_tensor(target_state)), 0.0))
    )
    if target_radius <= 0.0:
        raise ValueError("target memory radius must be positive")
    cross_eta = (
        float(response_fraction)
        * target_radius
        / (float(pulse_steps) * directional_drift)
    )
    return FrozenSourceCalibration(
        response_fraction=float(response_fraction),
        pulse_steps=int(pulse_steps),
        source_center_offset=offset,
        target_radius=target_radius,
        baseline_gradient_norm=gradient_norm,
        baseline_directional_drift=directional_drift,
        cross_eta=float(cross_eta),
    )


@njit(cache=True)
def _frozen_source_batch(
    initial_x: np.ndarray,
    initial_memory: np.ndarray,
    target_weights: np.ndarray,
    baseline_source_memory: np.ndarray,
    source_memories: np.ndarray,
    source_weights: np.ndarray,
    noise: np.ndarray,
    sample_steps: np.ndarray,
    epsilon: float,
    eta: float,
    target_sigma_rep: float,
    target_sigma_att: float,
    target_amplitude_rep: float,
    target_amplitude_att: float,
    source_sigma_rep: float,
    source_sigma_att: float,
    source_amplitude_rep: float,
    source_amplitude_att: float,
    cross_eta: float,
    pulse_steps: int,
):
    n_probes = source_memories.shape[0]
    baseline_path = 2 * n_probes
    free_path = baseline_path + 1
    n_paths = free_path + 1
    n_memory = initial_memory.shape[0]
    dim = initial_x.shape[0]
    n_samples = sample_steps.shape[0]

    positions = np.empty((n_samples, n_probes, 2, dim), np.float64)
    centers = np.empty((n_samples, n_probes, 2, dim), np.float64)
    tensors = np.empty((n_samples, n_probes, 2, dim, dim), np.float64)
    radii = np.empty((n_samples, n_probes, 2), np.float64)
    baseline_positions = np.empty((n_samples, dim), np.float64)
    baseline_centers = np.empty((n_samples, dim), np.float64)
    baseline_tensors = np.empty((n_samples, dim, dim), np.float64)
    baseline_radii = np.empty(n_samples, np.float64)
    free_positions = np.empty((n_samples, dim), np.float64)
    free_centers = np.empty((n_samples, dim), np.float64)
    free_tensors = np.empty((n_samples, dim, dim), np.float64)
    free_radii = np.empty(n_samples, np.float64)

    xs = np.empty((n_paths, dim), np.float64)
    histories = np.empty((n_paths, n_memory, dim), np.float64)
    heads = np.zeros(n_paths, np.int64)
    for path in range(n_paths):
        for coord in range(dim):
            xs[path, coord] = initial_x[coord]
        for age in range(n_memory):
            for coord in range(dim):
                histories[path, age, coord] = initial_memory[age, coord]

    target_weight_mass = np.sum(target_weights)
    target_sigma_rep2 = target_sigma_rep * target_sigma_rep
    target_sigma_att2 = target_sigma_att * target_sigma_att
    source_sigma_rep2 = source_sigma_rep * source_sigma_rep
    source_sigma_att2 = source_sigma_att * source_sigma_att
    sample_index = 0
    n_steps = int(sample_steps[-1])

    for step in range(n_steps + 1):
        if step > 0:
            for path in range(n_paths):
                self_gradient = path_gradient(
                    xs[path],
                    histories[path],
                    heads[path],
                    target_weights,
                    eta,
                    target_sigma_rep2,
                    target_sigma_att2,
                    target_amplitude_rep,
                    target_amplitude_att,
                )
                source_gradient = np.zeros(dim, np.float64)
                if path != free_path and step <= pulse_steps and cross_eta != 0.0:
                    if path == baseline_path:
                        field_memory = baseline_source_memory
                    else:
                        probe = path // 2
                        branch = path % 2
                        field_memory = source_memories[probe, branch]
                    source_gradient = path_gradient(
                        xs[path],
                        field_memory,
                        0,
                        source_weights,
                        1.0,
                        source_sigma_rep2,
                        source_sigma_att2,
                        source_amplitude_rep,
                        source_amplitude_att,
                    )
                for coord in range(dim):
                    xs[path, coord] = (
                        xs[path, coord]
                        + epsilon * noise[step - 1, coord]
                        - eta * self_gradient[coord]
                        - cross_eta * source_gradient[coord]
                    )

                heads[path] = (heads[path] - 1) % n_memory
                for coord in range(dim):
                    histories[path, heads[path], coord] = xs[path, coord]

        while sample_index < n_samples and sample_steps[sample_index] == step:
            for path in range(n_paths):
                position, center, tensor, radius = path_observables(
                    xs[path],
                    histories[path],
                    heads[path],
                    target_weights,
                    target_weight_mass,
                )
                if path == free_path:
                    free_positions[sample_index] = position
                    free_centers[sample_index] = center
                    free_tensors[sample_index] = tensor
                    free_radii[sample_index] = radius
                elif path == baseline_path:
                    baseline_positions[sample_index] = position
                    baseline_centers[sample_index] = center
                    baseline_tensors[sample_index] = tensor
                    baseline_radii[sample_index] = radius
                else:
                    probe = path // 2
                    branch = path % 2
                    positions[sample_index, probe, branch] = position
                    centers[sample_index, probe, branch] = center
                    tensors[sample_index, probe, branch] = tensor
                    radii[sample_index, probe, branch] = radius
            sample_index += 1

    return (
        positions,
        centers,
        tensors,
        radii,
        baseline_positions,
        baseline_centers,
        baseline_tensors,
        baseline_radii,
        free_positions,
        free_centers,
        free_tensors,
        free_radii,
    )


def paired_frozen_source_response(
    target_state: FiniteMemoryState,
    source_state: FiniteMemoryState,
    target_config: SimulationConfig,
    *,
    directions: Iterable[Iterable[float]],
    source_center_offset: Iterable[float],
    perturbation: float,
    noise: Iterable[Iterable[float]],
    sample_steps: Iterable[int],
    cross_eta: float,
    pulse_steps: int,
    source_config: SimulationConfig | None = None,
    source_rotation: Iterable[Iterable[float]] | None = None,
) -> PairedFrozenSourceResponse:
    """Differentiate target response under local translations of one source.

    A complete source state is placed at one non-zero center offset. For every
    input direction, two additional source states are placed at plus/minus
    perturbation around that same baseline. The baseline-source path and a
    no-source free path are evolved alongside all pairs with common noise.
    """

    validate_simulation_config(target_config)
    source_cfg = target_config if source_config is None else source_config
    validate_simulation_config(source_cfg)
    if target_state.dim != target_config.dim or source_state.dim != target_state.dim:
        raise ValueError("target, source, and configs must share one dimension")
    if source_cfg.dim != target_state.dim:
        raise ValueError("source_config dimension must match the states")
    if not np.isfinite(perturbation) or perturbation <= 0.0:
        raise ValueError("perturbation must be positive and finite")
    if not np.isfinite(cross_eta) or cross_eta < 0.0:
        raise ValueError("cross_eta must be non-negative and finite")
    if isinstance(pulse_steps, bool) or not isinstance(pulse_steps, (int, np.integer)):
        raise ValueError("pulse_steps must be an integer")
    if pulse_steps < 1:
        raise ValueError("pulse_steps must be positive")

    basis = _normalized_directions(directions, dim=target_state.dim)
    offset = _source_offset(source_center_offset, dim=target_state.dim)
    steps = np.asarray(list(sample_steps), dtype=int)
    if steps.ndim != 1 or steps.size < 1 or np.any(steps < 0):
        raise ValueError("sample_steps must be a non-empty non-negative sequence")
    if not np.array_equal(steps, np.unique(steps)):
        raise ValueError("sample_steps must be strictly increasing")
    if pulse_steps > int(steps[-1]):
        raise ValueError("last sample step must not precede the pulse end")

    future_noise = np.asarray(noise, dtype=float)
    if future_noise.shape != (int(steps[-1]), target_state.dim):
        raise ValueError("noise must have shape (max(sample_steps), dim)")
    if not np.isfinite(future_noise).all():
        raise ValueError("noise contains non-finite values")

    (
        baseline_source_center,
        baseline_source_memory,
        source_centers,
        source_memories,
    ) = _source_placements(
        target_state,
        source_state,
        basis,
        offset,
        float(perturbation),
        source_rotation,
    )
    baseline_gradient_norm, initial_gradient_norms = _initial_gradient_norms(
        target_state,
        source_state,
        baseline_source_memory,
        source_memories,
        source_cfg,
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
        positions,
        centers,
        tensors,
        radii,
        baseline_positions,
        baseline_centers,
        baseline_tensors,
        baseline_radii,
        free_positions,
        free_centers,
        free_tensors,
        free_radii,
    ) = _frozen_source_batch(
        target_state.x,
        target_state.memory,
        target_state.weights,
        baseline_source_memory,
        source_memories,
        source_state.weights,
        future_noise,
        steps,
        float(target_config.epsilon),
        float(target_config.eta),
        float(target_effective["sigma_rep"]),
        float(target_effective["sigma_att"]),
        float(target_effective["amplitude_rep"]),
        float(target_effective["amplitude_att"]),
        float(source_effective["sigma_rep"]),
        float(source_effective["sigma_att"]),
        float(source_effective["amplitude_rep"]),
        float(source_effective["amplitude_att"]),
        float(cross_eta),
        int(pulse_steps),
    )

    derivative_scale = 2.0 * float(perturbation)
    position_jacobians = np.transpose(
        (positions[:, :, 0, :] - positions[:, :, 1, :]) / derivative_scale,
        (0, 2, 1),
    )
    center_jacobians = np.transpose(
        (centers[:, :, 0, :] - centers[:, :, 1, :]) / derivative_scale,
        (0, 2, 1),
    )
    position_even = np.mean(positions, axis=2) - baseline_positions[:, None, :]
    center_even = np.mean(centers, axis=2) - baseline_centers[:, None, :]

    n_shape = target_state.dim * (target_state.dim + 1) // 2
    shape_jacobians = np.empty((len(steps), n_shape, len(basis)), dtype=float)
    shape_even = np.empty((len(steps), len(basis), n_shape), dtype=float)
    baseline_shape_vectors = np.empty((len(steps), n_shape), dtype=float)
    free_shape_vectors = np.empty((len(steps), n_shape), dtype=float)
    for sample_index in range(len(steps)):
        baseline_shape = symmetric_tensor_vector(baseline_tensors[sample_index])
        baseline_shape_vectors[sample_index] = baseline_shape
        free_shape_vectors[sample_index] = symmetric_tensor_vector(
            free_tensors[sample_index]
        )
        for probe_index in range(len(basis)):
            derivative_tensor = (
                tensors[sample_index, probe_index, 0]
                - tensors[sample_index, probe_index, 1]
            ) / derivative_scale
            even_tensor = 0.5 * (
                tensors[sample_index, probe_index, 0]
                + tensors[sample_index, probe_index, 1]
            )
            shape_jacobians[sample_index, :, probe_index] = symmetric_tensor_vector(
                derivative_tensor
            )
            shape_even[sample_index, probe_index] = (
                symmetric_tensor_vector(even_tensor) - baseline_shape
            )

    initial_radius = float(
        np.sqrt(max(np.trace(memory_shape_tensor(target_state)), 0.0))
    )
    if initial_radius <= 0.0:
        raise ValueError("target memory radius must be positive")
    radius_ratios = radii / initial_radius
    baseline_radius_ratios = baseline_radii / initial_radius
    free_radius_ratios = free_radii / initial_radius
    radius_even = np.mean(radius_ratios, axis=2) - baseline_radius_ratios[:, None]

    return PairedFrozenSourceResponse(
        sample_steps=steps,
        directions=basis,
        source_center_offset=offset,
        perturbation=float(perturbation),
        cross_eta=float(cross_eta),
        pulse_steps=int(pulse_steps),
        baseline_source_center=baseline_source_center,
        source_centers=source_centers,
        baseline_initial_gradient_norm=baseline_gradient_norm,
        initial_source_gradient_norms=initial_gradient_norms,
        position_jacobians=position_jacobians,
        memory_center_jacobians=center_jacobians,
        shape_jacobians=shape_jacobians,
        position_even_offsets=position_even,
        memory_center_even_offsets=center_even,
        shape_even_vectors=shape_even,
        radius_ratios=radius_ratios,
        radius_even_offsets=radius_even,
        baseline_positions=baseline_positions,
        baseline_memory_centers=baseline_centers,
        baseline_shape_vectors=baseline_shape_vectors,
        baseline_radius_ratios=baseline_radius_ratios,
        free_positions=free_positions,
        free_memory_centers=free_centers,
        free_shape_vectors=free_shape_vectors,
        free_radius_ratios=free_radius_ratios,
    )
