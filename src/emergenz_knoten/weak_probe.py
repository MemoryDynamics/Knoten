"""Paired weak-probe dynamics for equilibrated finite-memory states."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .core import SimulationConfig, validate_simulation_config
from .kernels import effective_double_gaussian_parameters
from .state import FiniteMemoryState, memory_shape_tensor

try:
    from numba import njit
except ImportError:  # pragma: no cover
    def njit(*args, **kwargs):
        def wrapper(func):
            return func

        return wrapper


@dataclass(frozen=True)
class PairedProbeResponse:
    """Central-difference response matrices for one initial memory state."""

    sample_steps: np.ndarray
    directions: np.ndarray
    per_step_strength: float
    pulse_steps: int
    position_matrices: np.ndarray
    memory_center_matrices: np.ndarray
    shape_matrices: np.ndarray
    radius_ratios: np.ndarray
    control_positions: np.ndarray
    control_memory_centers: np.ndarray
    control_shape_vectors: np.ndarray
    control_radius_ratios: np.ndarray


@njit(cache=True)
def _path_gradient(
    x: np.ndarray,
    history: np.ndarray,
    head: int,
    weights: np.ndarray,
    eta: float,
    sigma_rep2: float,
    sigma_att2: float,
    amplitude_rep: float,
    amplitude_att: float,
) -> np.ndarray:
    dim = x.shape[0]
    n_memory = history.shape[0]
    gradient = np.zeros(dim, np.float64)
    if eta == 0.0:
        return gradient
    for age in range(n_memory):
        memory_index = (head + age) % n_memory
        r2 = 0.0
        for coord in range(dim):
            delta = x[coord] - history[memory_index, coord]
            r2 += delta * delta
        rep_factor = -amplitude_rep * np.exp(-0.5 * r2 / sigma_rep2) / sigma_rep2
        att_factor = -amplitude_att * np.exp(-0.5 * r2 / sigma_att2) / sigma_att2
        factor = weights[age] * (rep_factor - att_factor)
        for coord in range(dim):
            gradient[coord] += factor * (x[coord] - history[memory_index, coord])
    return gradient


@njit(cache=True)
def _path_observables(
    x: np.ndarray,
    history: np.ndarray,
    head: int,
    weights: np.ndarray,
    weight_mass: float,
):
    dim = x.shape[0]
    n_memory = history.shape[0]
    center = np.zeros(dim, np.float64)
    tensor = np.zeros((dim, dim), np.float64)
    for age in range(n_memory):
        memory_index = (head + age) % n_memory
        for coord in range(dim):
            center[coord] += weights[age] * history[memory_index, coord]
    center /= weight_mass

    radius2 = 0.0
    for row in range(dim):
        for col in range(dim):
            value = 0.0
            for age in range(n_memory):
                memory_index = (head + age) % n_memory
                delta_row = history[memory_index, row] - center[row]
                delta_col = history[memory_index, col] - center[col]
                value += weights[age] * delta_row * delta_col
            value /= weight_mass
            tensor[row, col] = value
            if row == col:
                radius2 += value
    return x.copy(), center, tensor, np.sqrt(max(radius2, 0.0))


@njit(cache=True)
def _uniform_probe_batch(
    initial_x: np.ndarray,
    initial_memory: np.ndarray,
    weights: np.ndarray,
    directions: np.ndarray,
    noise: np.ndarray,
    sample_steps: np.ndarray,
    epsilon: float,
    eta: float,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float,
    amplitude_att: float,
    per_step_strength: float,
    pulse_steps: int,
):
    n_probes = directions.shape[0]
    control_path = 2 * n_probes
    n_paths = control_path + 1
    n_memory = initial_memory.shape[0]
    dim = initial_x.shape[0]
    n_samples = sample_steps.shape[0]

    positions = np.empty((n_samples, n_probes, 2, dim), np.float64)
    centers = np.empty((n_samples, n_probes, 2, dim), np.float64)
    tensors = np.empty((n_samples, n_probes, 2, dim, dim), np.float64)
    radii = np.empty((n_samples, n_probes, 2), np.float64)
    control_positions = np.empty((n_samples, dim), np.float64)
    control_centers = np.empty((n_samples, dim), np.float64)
    control_tensors = np.empty((n_samples, dim, dim), np.float64)
    control_radii = np.empty(n_samples, np.float64)

    xs = np.empty((n_paths, dim), np.float64)
    histories = np.empty((n_paths, n_memory, dim), np.float64)
    heads = np.zeros(n_paths, np.int64)
    for path in range(n_paths):
        for coord in range(dim):
            xs[path, coord] = initial_x[coord]
        for age in range(n_memory):
            for coord in range(dim):
                histories[path, age, coord] = initial_memory[age, coord]

    weight_mass = np.sum(weights)
    sample_index = 0
    n_steps = int(sample_steps[-1])
    rep_sigma2 = sigma_rep * sigma_rep
    att_sigma2 = sigma_att * sigma_att

    for step in range(n_steps + 1):
        if step > 0:
            for path in range(n_paths):
                gradient = _path_gradient(
                    xs[path],
                    histories[path],
                    heads[path],
                    weights,
                    eta,
                    rep_sigma2,
                    att_sigma2,
                    amplitude_rep,
                    amplitude_att,
                )
                for coord in range(dim):
                    applied = 0.0
                    if path < control_path and step <= pulse_steps:
                        probe = path // 2
                        sign = 1.0 if path % 2 == 0 else -1.0
                        applied = sign * per_step_strength * directions[probe, coord]
                    xs[path, coord] = (
                        xs[path, coord]
                        + epsilon * noise[step - 1, coord]
                        - eta * gradient[coord]
                        + applied
                    )

                heads[path] = (heads[path] - 1) % n_memory
                for coord in range(dim):
                    histories[path, heads[path], coord] = xs[path, coord]

        while sample_index < n_samples and sample_steps[sample_index] == step:
            for path in range(n_paths):
                position, center, tensor, radius = _path_observables(
                    xs[path], histories[path], heads[path], weights, weight_mass
                )
                if path == control_path:
                    control_positions[sample_index] = position
                    control_centers[sample_index] = center
                    control_tensors[sample_index] = tensor
                    control_radii[sample_index] = radius
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
        control_positions,
        control_centers,
        control_tensors,
        control_radii,
    )


def _symmetric_vector(tensor: np.ndarray) -> np.ndarray:
    dim = tensor.shape[0]
    values = []
    for row in range(dim):
        for col in range(row, dim):
            scale = 1.0 if row == col else np.sqrt(2.0)
            values.append(scale * float(tensor[row, col]))
    return np.asarray(values, dtype=float)


def paired_uniform_probe_response(
    state: FiniteMemoryState,
    config: SimulationConfig,
    *,
    directions: Iterable[Iterable[float]],
    noise: Iterable[Iterable[float]],
    sample_steps: Iterable[int],
    per_step_strength: float,
    pulse_steps: int,
) -> PairedProbeResponse:
    """Apply ``+/-`` uniform drift pulses with one shared future-noise path.

    The uniform pulse is a calibration probe. Its direct position response has
    the rank of the supplied input basis by construction; only delayed or
    control-subtracted responses may be interpreted as memory-mediated.
    """

    validate_simulation_config(config)
    if state.dim != config.dim:
        raise ValueError("state dimension must match simulation config")
    if not np.isfinite(per_step_strength) or per_step_strength <= 0.0:
        raise ValueError("per_step_strength must be positive and finite")
    if isinstance(pulse_steps, bool) or not isinstance(pulse_steps, (int, np.integer)):
        raise ValueError("pulse_steps must be an integer")
    if pulse_steps < 1:
        raise ValueError("pulse_steps must be positive")

    basis = np.asarray(directions, dtype=float)
    if basis.ndim != 2 or basis.shape[1] != state.dim or basis.shape[0] < 1:
        raise ValueError("directions must have shape (n_probes, dim)")
    if not np.isfinite(basis).all():
        raise ValueError("directions contain non-finite values")
    norms = np.linalg.norm(basis, axis=1)
    if np.any(norms <= 0.0):
        raise ValueError("probe directions must be non-zero")
    basis = basis / norms[:, None]

    steps = np.asarray(list(sample_steps), dtype=int)
    if steps.ndim != 1 or steps.size < 1 or np.any(steps < 0):
        raise ValueError("sample_steps must be a non-empty non-negative sequence")
    if not np.array_equal(steps, np.unique(steps)):
        raise ValueError("sample_steps must be strictly increasing")
    if pulse_steps > int(steps[-1]):
        raise ValueError("last sample step must not precede the pulse end")

    future_noise = np.asarray(noise, dtype=float)
    if future_noise.shape != (int(steps[-1]), state.dim):
        raise ValueError("noise must have shape (max(sample_steps), dim)")
    if not np.isfinite(future_noise).all():
        raise ValueError("noise contains non-finite values")

    effective = effective_double_gaussian_parameters(
        dim=config.dim,
        sigma_rep=config.sigma_rep,
        sigma_att=config.sigma_att,
        amplitude_rep=config.amplitude_rep,
        amplitude_att=config.amplitude_att,
        deposition_kernel=config.deposition_kernel,
        deposition_sigma=config.deposition_sigma,
    )
    (
        positions,
        centers,
        tensors,
        radii,
        control_positions,
        control_centers,
        control_tensors,
        control_radii,
    ) = _uniform_probe_batch(
        state.x,
        state.memory,
        state.weights,
        basis,
        future_noise,
        steps,
        float(config.epsilon),
        float(config.eta),
        float(effective["sigma_rep"]),
        float(effective["sigma_att"]),
        float(effective["amplitude_rep"]),
        float(effective["amplitude_att"]),
        float(per_step_strength),
        int(pulse_steps),
    )

    scale = 2.0 * float(per_step_strength)
    position_matrices = np.transpose(
        (positions[:, :, 0, :] - positions[:, :, 1, :]) / scale,
        (0, 2, 1),
    )
    memory_center_matrices = np.transpose(
        (centers[:, :, 0, :] - centers[:, :, 1, :]) / scale,
        (0, 2, 1),
    )

    n_shape = state.dim * (state.dim + 1) // 2
    shape_matrices = np.empty((len(steps), n_shape, len(basis)), dtype=float)
    control_shape_vectors = np.empty((len(steps), n_shape), dtype=float)
    for sample_index in range(len(steps)):
        control_shape_vectors[sample_index] = _symmetric_vector(control_tensors[sample_index])
        for probe_index in range(len(basis)):
            difference = (
                tensors[sample_index, probe_index, 0]
                - tensors[sample_index, probe_index, 1]
            ) / scale
            shape_matrices[sample_index, :, probe_index] = _symmetric_vector(difference)

    initial_radius = float(np.sqrt(max(np.trace(memory_shape_tensor(state)), 0.0)))
    if initial_radius <= 0.0:
        raise ValueError("initial memory radius must be positive")

    return PairedProbeResponse(
        sample_steps=steps,
        directions=basis,
        per_step_strength=float(per_step_strength),
        pulse_steps=int(pulse_steps),
        position_matrices=position_matrices,
        memory_center_matrices=memory_center_matrices,
        shape_matrices=shape_matrices,
        radius_ratios=radii / initial_radius,
        control_positions=control_positions,
        control_memory_centers=control_centers,
        control_shape_vectors=control_shape_vectors,
        control_radius_ratios=control_radii / initial_radius,
    )
