"""Paired finite-wavenumber responses of canonical scalar memory states."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from ._continuation import path_gradient, path_observables
from .core import SimulationConfig, validate_simulation_config
from .kernels import effective_double_gaussian_parameters
from .state import FiniteMemoryState, memory_centroid, memory_shape_tensor

try:
    from numba import njit
except ImportError:  # pragma: no cover

    def njit(*args, **kwargs):
        def wrapper(func):
            return func

        return wrapper


@dataclass(frozen=True)
class PairedFiniteKResponse:
    """Central-difference response to zero-centroid memory deformations.

    A single spatial direction is fixed for the complete response. Every
    input channel deforms the retained path at one dimensionless wavenumber
    ``k R_mem``. Every output channel is the centered scalar-memory Fourier
    coefficient at one of the same registered wavenumbers.
    """

    sample_steps: np.ndarray
    direction: np.ndarray
    kr_values: np.ndarray
    wavevectors: np.ndarray
    memory_radius: float
    perturbation_fraction: float
    perturbation_amplitude: float
    input_profiles: np.ndarray
    position_matrices: np.ndarray
    memory_center_matrices: np.ndarray
    centered_mode_matrices: np.ndarray
    radius_ratios: np.ndarray
    control_positions: np.ndarray
    control_memory_centers: np.ndarray
    control_centered_modes: np.ndarray
    control_radius_ratios: np.ndarray


def scalar_memory_fourier_modes(
    state: FiniteMemoryState,
    wavevectors: Iterable[Iterable[float]],
    *,
    centered: bool = True,
) -> np.ndarray:
    """Evaluate the retained scalar memory measure in Fourier space."""

    vectors = np.asarray(wavevectors, dtype=float)
    if (
        vectors.ndim != 2
        or vectors.shape[0] < 1
        or vectors.shape[1] != state.dim
        or not np.isfinite(vectors).all()
    ):
        raise ValueError("wavevectors must be finite with shape (n_modes, dim)")
    origin = memory_centroid(state) if centered else np.zeros(state.dim)
    phases = np.exp(-1j * (vectors @ (state.memory - origin).T))
    return np.asarray(
        phases @ state.weights / np.sum(state.weights),
        dtype=np.complex128,
    )


def longitudinal_memory_mode_profiles(
    state: FiniteMemoryState,
    *,
    direction: Iterable[float],
    kr_values: Iterable[float],
) -> tuple[np.ndarray, np.ndarray, float]:
    r"""Return registered zero-centroid path-deformation profiles.

    For each non-zero ``k R_mem`` the raw profile is

    ``sin(k e . (r_j - x))``.

    A correction on ages ``j>0`` enforces zero weighted displacement while
    preserving the youngest point exactly. Consequently the perturbed states
    retain both ``x=memory[0]`` and the original memory centroid. Profiles are
    normalized to unit weighted RMS before the physical amplitude is applied.
    """

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

    radius = float(np.sqrt(max(np.trace(memory_shape_tensor(state)), 0.0)))
    if radius <= 0.0:
        raise ValueError("state memory radius must be positive")
    mass = float(np.sum(state.weights))
    tail_mass = mass - float(state.weights[0])
    if tail_mass <= 0.0:
        raise ValueError("finite-k deformation requires at least two weighted ages")

    coordinate = (state.memory - state.x[None, :]) @ axis
    profiles = np.empty((values.size, state.n_memory), dtype=float)
    for index, kr in enumerate(values):
        raw = np.sin((kr / radius) * coordinate)
        raw[0] = 0.0
        correction = float(np.dot(state.weights, raw)) / tail_mass
        profile = raw.copy()
        profile[1:] -= correction
        profile[0] = 0.0
        rms = float(np.sqrt(np.dot(state.weights, profile * profile) / mass))
        if rms <= np.finfo(float).eps:
            raise ValueError("finite-k profile is numerically unresolved")
        profiles[index] = profile / rms

    wavevectors = (values / radius)[:, None] * axis[None, :]
    return profiles, wavevectors, radius


@njit(cache=True)
def _centered_scalar_modes(
    history: np.ndarray,
    head: int,
    weights: np.ndarray,
    weight_mass: float,
    center: np.ndarray,
    wavevectors: np.ndarray,
):
    n_modes = wavevectors.shape[0]
    n_memory = history.shape[0]
    dim = history.shape[1]
    real = np.zeros(n_modes, np.float64)
    imag = np.zeros(n_modes, np.float64)
    for mode in range(n_modes):
        for age in range(n_memory):
            memory_index = (head + age) % n_memory
            phase = 0.0
            for coord in range(dim):
                phase += wavevectors[mode, coord] * (
                    history[memory_index, coord] - center[coord]
                )
            real[mode] += weights[age] * np.cos(phase)
            imag[mode] -= weights[age] * np.sin(phase)
        real[mode] /= weight_mass
        imag[mode] /= weight_mass
    return real, imag


@njit(cache=True)
def _finite_k_response_batch(
    initial_x: np.ndarray,
    branch_memories: np.ndarray,
    control_memory: np.ndarray,
    weights: np.ndarray,
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
    n_inputs = branch_memories.shape[0]
    n_paths = 2 * n_inputs + 1
    control_path = n_paths - 1
    n_memory = control_memory.shape[0]
    dim = initial_x.shape[0]
    n_samples = sample_steps.shape[0]
    n_modes = wavevectors.shape[0]

    xs = np.empty((n_paths, dim), np.float64)
    histories = np.empty((n_paths, n_memory, dim), np.float64)
    heads = np.zeros(n_paths, np.int64)
    for path in range(n_paths):
        xs[path] = initial_x
        if path == control_path:
            histories[path] = control_memory
        else:
            histories[path] = branch_memories[path // 2, path % 2]

    positions = np.empty((n_samples, n_inputs, 2, dim), np.float64)
    centers = np.empty((n_samples, n_inputs, 2, dim), np.float64)
    mode_real = np.empty((n_samples, n_inputs, 2, n_modes), np.float64)
    mode_imag = np.empty((n_samples, n_inputs, 2, n_modes), np.float64)
    radii = np.empty((n_samples, n_inputs, 2), np.float64)
    control_positions = np.empty((n_samples, dim), np.float64)
    control_centers = np.empty((n_samples, dim), np.float64)
    control_mode_real = np.empty((n_samples, n_modes), np.float64)
    control_mode_imag = np.empty((n_samples, n_modes), np.float64)
    control_radii = np.empty(n_samples, np.float64)

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
                for coord in range(dim):
                    xs[path, coord] = (
                        xs[path, coord]
                        + epsilon * noise[step - 1, coord]
                        - eta * gradient[coord]
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
                if path == control_path:
                    control_positions[sample_index] = position
                    control_centers[sample_index] = center
                    control_mode_real[sample_index] = real
                    control_mode_imag[sample_index] = imag
                    control_radii[sample_index] = radius
                else:
                    input_index = path // 2
                    branch = path % 2
                    positions[sample_index, input_index, branch] = position
                    centers[sample_index, input_index, branch] = center
                    mode_real[sample_index, input_index, branch] = real
                    mode_imag[sample_index, input_index, branch] = imag
                    radii[sample_index, input_index, branch] = radius
            sample_index += 1

    return (
        positions,
        centers,
        mode_real,
        mode_imag,
        radii,
        control_positions,
        control_centers,
        control_mode_real,
        control_mode_imag,
        control_radii,
    )


def paired_finite_k_memory_response(
    state: FiniteMemoryState,
    config: SimulationConfig,
    *,
    direction: Iterable[float],
    kr_values: Iterable[float],
    perturbation_fraction: float,
    noise: Iterable[Iterable[float]],
    sample_steps: Iterable[int],
) -> PairedFiniteKResponse:
    """Continue paired finite-``k`` memory deformations with common noise.

    The intervention changes only the already retained memory path. It does
    not add a field equation, target pole, inertia, or cross-node channel.
    The youngest point and visible state are unchanged, and the perturbation
    has exactly zero weighted centroid to first order and in finite precision.
    """

    validate_simulation_config(config)
    if state.dim != config.dim:
        raise ValueError("state dimension must match simulation config")
    fraction = float(perturbation_fraction)
    if not np.isfinite(fraction) or fraction <= 0.0:
        raise ValueError("perturbation_fraction must be positive and finite")
    registered_kr = np.asarray(list(kr_values), dtype=float)
    profiles, wavevectors, radius = longitudinal_memory_mode_profiles(
        state,
        direction=direction,
        kr_values=registered_kr,
    )
    axis = wavevectors[0] / np.linalg.norm(wavevectors[0])
    amplitude = fraction * radius
    displacement = amplitude * profiles[:, :, None] * axis[None, None, :]
    branch_memories = np.stack(
        (state.memory[None, :, :] + displacement, state.memory[None, :, :] - displacement),
        axis=1,
    )
    if not np.allclose(branch_memories[:, :, 0], state.x, rtol=0.0, atol=1e-14):
        raise RuntimeError("finite-k perturbation changed the youngest memory point")
    branch_centers = np.einsum("ibnd,n->ibd", branch_memories, state.weights)
    branch_centers /= np.sum(state.weights)
    if not np.allclose(
        branch_centers,
        memory_centroid(state)[None, None, :],
        rtol=0.0,
        atol=1e-13 * max(1.0, radius),
    ):
        raise RuntimeError("finite-k perturbation changed the memory centroid")

    steps = np.asarray(list(sample_steps), dtype=int)
    if (
        steps.ndim != 1
        or steps.size < 2
        or steps[0] != 0
        or np.any(steps < 0)
        or not np.array_equal(steps, np.unique(steps))
    ):
        raise ValueError("sample_steps must be unique and increase from zero")
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
    raw = _finite_k_response_batch(
        state.x,
        branch_memories,
        state.memory,
        state.weights,
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
    (
        positions,
        centers,
        mode_real,
        mode_imag,
        radii,
        control_positions,
        control_centers,
        control_mode_real,
        control_mode_imag,
        control_radii,
    ) = raw
    scale = 2.0 * amplitude
    position_matrices = np.transpose(
        (positions[:, :, 0] - positions[:, :, 1]) / scale,
        (0, 2, 1),
    )
    center_matrices = np.transpose(
        (centers[:, :, 0] - centers[:, :, 1]) / scale,
        (0, 2, 1),
    )
    mode_difference = (
        (mode_real[:, :, 0] - mode_real[:, :, 1])
        + 1j * (mode_imag[:, :, 0] - mode_imag[:, :, 1])
    ) / scale
    centered_mode_matrices = np.transpose(mode_difference, (0, 2, 1))
    control_modes = control_mode_real + 1j * control_mode_imag
    return PairedFiniteKResponse(
        sample_steps=steps,
        direction=np.asarray(axis, dtype=float),
        kr_values=registered_kr,
        wavevectors=np.asarray(wavevectors, dtype=float),
        memory_radius=radius,
        perturbation_fraction=fraction,
        perturbation_amplitude=amplitude,
        input_profiles=np.asarray(profiles, dtype=float),
        position_matrices=np.asarray(position_matrices, dtype=float),
        memory_center_matrices=np.asarray(center_matrices, dtype=float),
        centered_mode_matrices=np.asarray(centered_mode_matrices, dtype=np.complex128),
        radius_ratios=np.asarray(radii / radius, dtype=float),
        control_positions=np.asarray(control_positions, dtype=float),
        control_memory_centers=np.asarray(control_centers, dtype=float),
        control_centered_modes=np.asarray(control_modes, dtype=np.complex128),
        control_radius_ratios=np.asarray(control_radii / radius, dtype=float),
    )
