"""Paired scalar-knot continuation under a prescribed additive field."""

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


EXTERNAL_FIELD_CONDITIONS = ("active", "sign_flip", "channel_off")


@dataclass(frozen=True)
class PairedExternalFieldResponse:
    """Active, sign-reversed, and channel-off target continuations."""

    sample_steps: np.ndarray
    target_conditions: tuple[str, ...]
    applied_displacements: np.ndarray
    target_positions: np.ndarray
    target_memory_centers: np.ndarray
    target_shape_tensors: np.ndarray
    target_radius_ratios: np.ndarray


@njit(cache=True)
def _external_field_batch(
    initial_x: np.ndarray,
    initial_memory: np.ndarray,
    weights: np.ndarray,
    noise: np.ndarray,
    applied_displacements: np.ndarray,
    sample_steps: np.ndarray,
    epsilon: float,
    eta: float,
    sigma_rep2: float,
    sigma_att2: float,
    amplitude_rep: float,
    amplitude_att: float,
):
    n_paths = 3
    n_steps = applied_displacements.shape[0]
    n_memory = initial_memory.shape[0]
    dim = initial_x.shape[0]
    n_samples = sample_steps.shape[0]
    xs = np.empty((n_paths, dim), np.float64)
    histories = np.empty((n_paths, n_memory, dim), np.float64)
    heads = np.zeros(n_paths, np.int64)
    for path in range(n_paths):
        xs[path] = initial_x
        histories[path] = initial_memory

    positions = np.empty((n_samples, n_paths, dim), np.float64)
    centers = np.empty((n_samples, n_paths, dim), np.float64)
    tensors = np.empty((n_samples, n_paths, dim, dim), np.float64)
    radii = np.empty((n_samples, n_paths), np.float64)
    weight_mass = np.sum(weights)
    sample_index = 0
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
                sign = 0.0
                if path == 0:
                    sign = 1.0
                elif path == 1:
                    sign = -1.0
                for coord in range(dim):
                    xs[path, coord] = (
                        xs[path, coord]
                        + epsilon * noise[step - 1, coord]
                        - eta * gradient[coord]
                        + sign * applied_displacements[step - 1, coord]
                    )
                heads[path] = (heads[path] - 1) % n_memory
                histories[path, heads[path]] = xs[path]

        while sample_index < n_samples and sample_steps[sample_index] == step:
            for path in range(n_paths):
                position, center, tensor, radius = path_observables(
                    xs[path],
                    histories[path],
                    heads[path],
                    weights,
                    weight_mass,
                )
                positions[sample_index, path] = position
                centers[sample_index, path] = center
                tensors[sample_index, path] = tensor
                radii[sample_index, path] = radius
            sample_index += 1

    return positions, centers, tensors, radii


def paired_external_field_response(
    state: FiniteMemoryState,
    config: SimulationConfig,
    *,
    applied_displacements: Iterable[Iterable[float]],
    noise: Iterable[Iterable[float]],
    sample_steps: Iterable[int],
) -> PairedExternalFieldResponse:
    """Continue a target under a field, its sign flip, and an exact off arm.

    ``applied_displacements[n]`` is the additive displacement during target
    update ``n+1``. The three branches share the same future-noise path.
    """

    validate_simulation_config(config)
    if state.dim != config.dim:
        raise ValueError("state dimension must match simulation config")
    forcing = np.asarray(applied_displacements, dtype=float)
    if (
        forcing.ndim != 2
        or forcing.shape[1] != state.dim
        or forcing.shape[0] < 1
        or not np.isfinite(forcing).all()
    ):
        raise ValueError(
            "applied_displacements must have shape (n_steps, state dimension)"
        )
    future_noise = np.asarray(noise, dtype=float)
    if future_noise.shape != forcing.shape or not np.isfinite(future_noise).all():
        raise ValueError("noise must match applied_displacements")
    steps = np.asarray(list(sample_steps), dtype=int)
    if (
        steps.ndim != 1
        or steps.size < 2
        or steps[0] != 0
        or steps[-1] != forcing.shape[0]
        or np.any(steps < 0)
        or not np.array_equal(steps, np.unique(steps))
    ):
        raise ValueError(
            "sample_steps must increase from zero through the forcing horizon"
        )

    effective = effective_double_gaussian_parameters(
        dim=config.dim,
        sigma_rep=config.sigma_rep,
        sigma_att=config.sigma_att,
        amplitude_rep=config.amplitude_rep,
        amplitude_att=config.amplitude_att,
        deposition_kernel=config.deposition_kernel,
        deposition_sigma=config.deposition_sigma,
    )
    positions, centers, tensors, radii = _external_field_batch(
        state.x,
        state.memory,
        state.weights,
        future_noise,
        forcing,
        steps,
        float(config.epsilon),
        float(config.eta),
        float(effective["sigma_rep"]) ** 2,
        float(effective["sigma_att"]) ** 2,
        float(effective["amplitude_rep"]),
        float(effective["amplitude_att"]),
    )
    initial_radius = float(radii[0, 0])
    if initial_radius <= 0.0:
        raise ValueError("initial target memory radius must be positive")
    return PairedExternalFieldResponse(
        sample_steps=steps,
        target_conditions=EXTERNAL_FIELD_CONDITIONS,
        applied_displacements=forcing,
        target_positions=positions,
        target_memory_centers=centers,
        target_shape_tensors=tensors,
        target_radius_ratios=radii / initial_radius,
    )


def external_field_response_metrics(
    response: PairedExternalFieldResponse,
    *,
    radius: float,
) -> dict[str, np.ndarray | float]:
    """Measure odd response, flip consistency, and paired shape disturbance."""

    if not np.isfinite(radius) or radius <= 0.0:
        raise ValueError("radius must be positive")
    centers = np.asarray(response.target_memory_centers, dtype=float)
    active_delta = centers[:, 0] - centers[:, 2]
    flip_delta = centers[:, 1] - centers[:, 2]
    active_norm = np.linalg.norm(active_delta, axis=1)
    final_active = active_delta[-1]
    final_flip = flip_delta[-1]
    active_final_norm = float(np.linalg.norm(final_active))
    flip_final_norm = float(np.linalg.norm(final_flip))
    tiny = np.finfo(float).tiny
    flip_cosine = float(
        np.dot(final_active, final_flip)
        / max(active_final_norm * flip_final_norm, tiny)
    )

    active_radius = response.target_radius_ratios[:, 0]
    off_radius = response.target_radius_ratios[:, 2]
    radius_ratio = np.divide(
        active_radius,
        off_radius,
        out=np.ones_like(active_radius),
        where=np.abs(off_radius) > tiny,
    )
    active_tensors = response.target_shape_tensors[:, 0]
    off_tensors = response.target_shape_tensors[:, 2]
    tensor_scale = np.maximum(np.trace(off_tensors, axis1=1, axis2=2), tiny)
    return {
        "active_response_r": active_final_norm / radius,
        "active_response_vector_r": final_active / radius,
        "odd_response_vector_r": 0.5 * (final_active - final_flip) / radius,
        "flip_cosine": flip_cosine,
        "flip_magnitude_ratio": flip_final_norm / max(active_final_norm, tiny),
        "target_radius_max_change": float(np.max(np.abs(radius_ratio - 1.0))),
        "target_shape_max_change": float(
            np.max(
                np.linalg.norm(active_tensors - off_tensors, axis=(1, 2))
                / tensor_scale
            )
        ),
        "trace_active_response_r": active_norm / radius,
    }
