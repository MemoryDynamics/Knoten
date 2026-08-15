"""Canonical zero-net trajectory write port for scalar finite memory."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from ._continuation import path_gradient, path_observables
from .core import SimulationConfig, validate_simulation_config
from .finite_k_response import _centered_scalar_modes
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
class PairedCanonicalWriteResponse:
    """Mirrored response to a two-update, zero-net visible kick sequence."""

    sample_steps: np.ndarray
    direction: np.ndarray
    kr_values: np.ndarray
    wavevectors: np.ndarray
    memory_radius: float
    perturbation_fraction: float
    perturbation_amplitude: float
    plus_kicks: np.ndarray
    branch_positions: np.ndarray
    branch_memory_centers: np.ndarray
    branch_centered_modes: np.ndarray
    branch_self_drifts: np.ndarray
    branch_radius_ratios: np.ndarray
    control_positions: np.ndarray
    control_memory_centers: np.ndarray
    control_centered_modes: np.ndarray
    control_self_drifts: np.ndarray
    control_radius_ratios: np.ndarray
    position_response: np.ndarray
    memory_center_response: np.ndarray
    centered_mode_response: np.ndarray
    self_drift_response: np.ndarray
    position_even_leakage: np.ndarray
    memory_center_even_leakage: np.ndarray
    centered_mode_even_leakage: np.ndarray


@njit(cache=True)
def _canonical_write_response_batch(
    initial_x: np.ndarray,
    initial_memory: np.ndarray,
    weights: np.ndarray,
    axis: np.ndarray,
    amplitude: float,
    wavevectors: np.ndarray,
    noise: np.ndarray,
    sample_steps: np.ndarray,
    epsilon: float,
    eta: float,
    sigma_rep2: float,
    sigma_att2: float,
    amplitude_rep: float,
    amplitude_att: float,
):
    n_paths = 3
    control_path = 2
    n_memory = initial_memory.shape[0]
    dim = initial_x.shape[0]
    n_samples = sample_steps.shape[0]
    n_modes = wavevectors.shape[0]

    xs = np.empty((n_paths, dim), np.float64)
    histories = np.empty((n_paths, n_memory, dim), np.float64)
    heads = np.zeros(n_paths, np.int64)
    for path in range(n_paths):
        xs[path] = initial_x
        histories[path] = initial_memory

    positions = np.empty((n_samples, n_paths, dim), np.float64)
    centers = np.empty((n_samples, n_paths, dim), np.float64)
    mode_real = np.empty((n_samples, n_paths, n_modes), np.float64)
    mode_imag = np.empty((n_samples, n_paths, n_modes), np.float64)
    self_drifts = np.empty((n_samples, n_paths, dim), np.float64)
    radii = np.empty((n_samples, n_paths), np.float64)

    weight_mass = np.sum(weights)
    sample_index = 0
    n_steps = int(sample_steps[-1])
    for step in range(n_steps + 1):
        if step > 0:
            for path in range(n_paths):
                gradient = path_gradient(
                    xs[path],
                    histories[path],
                    heads[path],
                    weights,
                    eta,
                    sigma_rep2,
                    sigma_att2,
                    amplitude_rep,
                    amplitude_att,
                )
                branch_sign = 0.0
                if path != control_path:
                    branch_sign = 1.0 if path == 0 else -1.0
                    if step == 2:
                        branch_sign = -branch_sign
                    elif step != 1:
                        branch_sign = 0.0
                for coord in range(dim):
                    xs[path, coord] = (
                        xs[path, coord]
                        + epsilon * noise[step - 1, coord]
                        - eta * gradient[coord]
                        + branch_sign * amplitude * axis[coord]
                    )
                heads[path] = (heads[path] - 1) % n_memory
                histories[path, heads[path]] = xs[path]

        while sample_index < n_samples and sample_steps[sample_index] == step:
            for path in range(n_paths):
                position, center, _, radius = path_observables(
                    xs[path], histories[path], heads[path], weights, weight_mass
                )
                real, imag = _centered_scalar_modes(
                    histories[path],
                    heads[path],
                    weights,
                    weight_mass,
                    center,
                    wavevectors,
                )
                gradient = path_gradient(
                    xs[path],
                    histories[path],
                    heads[path],
                    weights,
                    eta,
                    sigma_rep2,
                    sigma_att2,
                    amplitude_rep,
                    amplitude_att,
                )
                positions[sample_index, path] = position
                centers[sample_index, path] = center
                mode_real[sample_index, path] = real
                mode_imag[sample_index, path] = imag
                for coord in range(dim):
                    self_drifts[sample_index, path, coord] = -eta * gradient[coord]
                radii[sample_index, path] = radius
            sample_index += 1

    return positions, centers, mode_real, mode_imag, self_drifts, radii


def paired_canonical_write_response(
    state: FiniteMemoryState,
    config: SimulationConfig,
    *,
    direction: Iterable[float],
    kr_values: Iterable[float],
    perturbation_fraction: float,
    noise: Iterable[Iterable[float]],
    sample_steps: Iterable[int],
) -> PairedCanonicalWriteResponse:
    """Write a mirrored dipole through the canonical visible update.

    The plus arm receives ``(+delta, -delta)`` and the minus arm receives its
    sign reversal. Both arms therefore have zero direct net kick after update
    two. Every kicked visible state is deposited through the unmodified scalar
    memory rule. Central differences isolate the odd response, while the
    paired average relative to the common control measures even leakage.
    """

    validate_simulation_config(config)
    if state.dim != config.dim:
        raise ValueError("state dimension must match simulation config")
    axis = np.asarray(direction, dtype=float)
    if axis.shape != (state.dim,) or not np.isfinite(axis).all():
        raise ValueError("direction must be a finite vector matching state dimension")
    norm = float(np.linalg.norm(axis))
    if norm <= 0.0:
        raise ValueError("direction must be non-zero")
    axis = axis / norm

    values = np.asarray(list(kr_values), dtype=float)
    if (
        values.ndim != 1
        or values.size < 1
        or not np.isfinite(values).all()
        or np.any(values <= 0.0)
        or not np.array_equal(values, np.unique(values))
    ):
        raise ValueError("kr_values must be unique increasing positive values")
    fraction = float(perturbation_fraction)
    if not np.isfinite(fraction) or fraction <= 0.0:
        raise ValueError("perturbation_fraction must be positive and finite")
    radius = float(np.sqrt(max(np.trace(memory_shape_tensor(state)), 0.0)))
    if radius <= 0.0:
        raise ValueError("state memory radius must be positive")
    amplitude = fraction * radius
    wavevectors = (values / radius)[:, None] * axis[None, :]

    steps = np.asarray(list(sample_steps), dtype=int)
    if (
        steps.ndim != 1
        or steps.size < 3
        or steps[0] != 0
        or steps[-1] < 2
        or np.any(steps < 0)
        or not np.array_equal(steps, np.unique(steps))
    ):
        raise ValueError("sample_steps must be unique, increase from zero, and reach two")
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
    positions, centers, mode_real, mode_imag, self_drifts, radii = (
        _canonical_write_response_batch(
            state.x,
            state.memory,
            state.weights,
            axis,
            amplitude,
            wavevectors,
            future_noise,
            steps,
            float(config.epsilon),
            float(config.eta),
            float(effective["sigma_rep"]) ** 2,
            float(effective["sigma_att"]) ** 2,
            float(effective["amplitude_rep"]),
            float(effective["amplitude_att"]),
        )
    )
    modes = mode_real + 1j * mode_imag
    scale = 2.0 * amplitude
    plus_kicks = np.stack((amplitude * axis, -amplitude * axis))
    return PairedCanonicalWriteResponse(
        sample_steps=steps,
        direction=axis,
        kr_values=values,
        wavevectors=wavevectors,
        memory_radius=radius,
        perturbation_fraction=fraction,
        perturbation_amplitude=amplitude,
        plus_kicks=plus_kicks,
        branch_positions=positions[:, :2],
        branch_memory_centers=centers[:, :2],
        branch_centered_modes=modes[:, :2],
        branch_self_drifts=self_drifts[:, :2],
        branch_radius_ratios=radii[:, :2] / radius,
        control_positions=positions[:, 2],
        control_memory_centers=centers[:, 2],
        control_centered_modes=modes[:, 2],
        control_self_drifts=self_drifts[:, 2],
        control_radius_ratios=radii[:, 2] / radius,
        position_response=(positions[:, 0] - positions[:, 1]) / scale,
        memory_center_response=(centers[:, 0] - centers[:, 1]) / scale,
        centered_mode_response=(modes[:, 0] - modes[:, 1]) / scale,
        self_drift_response=(self_drifts[:, 0] - self_drifts[:, 1]) / scale,
        position_even_leakage=(positions[:, 0] + positions[:, 1] - 2.0 * positions[:, 2])
        / scale,
        memory_center_even_leakage=(
            centers[:, 0] + centers[:, 1] - 2.0 * centers[:, 2]
        )
        / scale,
        centered_mode_even_leakage=(modes[:, 0] + modes[:, 1] - 2.0 * modes[:, 2])
        / scale,
    )
