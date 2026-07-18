"""Signed scalar coupling to a frozen finite-memory source.

The source and target labels affect only the cross-channel. The target's
non-negative scalar memory and self-interaction remain unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from ._continuation import (
    path_gradient,
    path_observables,
    path_three_scale_gradient,
    symmetric_tensor_vector,
)
from .core import SimulationConfig, validate_simulation_config
from .kernels import (
    effective_double_gaussian_parameters,
    effective_gaussian_parameters,
    three_scale_gaussian_gradient,
)
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


_ALLOWED_LABELS = {-1, 0, 1}


@dataclass(frozen=True)
class SignedCrossCalibration:
    """Cross-coupling scale derived from the initial frozen-source field."""

    response_fraction: float
    pulse_steps: int
    source_center_offset: np.ndarray
    target_radius: float
    initial_gradient: np.ndarray
    canonical_directional_drift: float
    cross_eta: float


@dataclass(frozen=True)
class SignedCrossResponse:
    """Common-noise continuations for signed source-target label pairs."""

    sample_steps: np.ndarray
    label_pairs: np.ndarray
    label_products: np.ndarray
    source_center_offset: np.ndarray
    source_center: np.ndarray
    cross_eta: float
    pulse_steps: int
    target_radius: float
    initial_source_gradient: np.ndarray
    positions: np.ndarray
    memory_centers: np.ndarray
    shape_vectors: np.ndarray
    radius_ratios: np.ndarray
    position_displacements: np.ndarray
    memory_center_displacements: np.ndarray
    shape_displacements: np.ndarray
    radius_displacements: np.ndarray
    free_positions: np.ndarray
    free_memory_centers: np.ndarray
    free_shape_vectors: np.ndarray
    free_radius_ratios: np.ndarray


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


def _label_pairs(label_pairs: Iterable[Iterable[int]]) -> np.ndarray:
    labels = np.asarray(list(label_pairs))
    if labels.ndim != 2 or labels.shape[1] != 2 or labels.shape[0] < 1:
        raise ValueError("label_pairs must have shape (n_pairs, 2)")
    if not np.issubdtype(labels.dtype, np.number):
        raise ValueError("labels must be numeric")
    labels_float = labels.astype(float)
    if not np.isfinite(labels_float).all():
        raise ValueError("labels must be finite")
    labels_int = labels_float.astype(np.int8)
    if not np.array_equal(labels_float, labels_int.astype(float)):
        raise ValueError("labels must be integers")
    if any(int(value) not in _ALLOWED_LABELS for value in labels_int.ravel()):
        raise ValueError("labels must belong to {-1, 0, +1}")
    return labels_int


def _validate_common(
    target_state: FiniteMemoryState,
    source_state: FiniteMemoryState,
    target_config: SimulationConfig,
    source_config: SimulationConfig | None,
    *,
    sigma_comp: float | None,
    amplitude_comp: float,
) -> tuple[SimulationConfig, float, float]:
    validate_simulation_config(target_config)
    source_cfg = target_config if source_config is None else source_config
    validate_simulation_config(source_cfg)
    if target_state.dim != target_config.dim or source_state.dim != target_state.dim:
        raise ValueError("target, source, and configs must share one dimension")
    if source_cfg.dim != target_state.dim:
        raise ValueError("source_config dimension must match the states")
    if not np.isfinite(amplitude_comp):
        raise ValueError("amplitude_comp must be finite")
    if sigma_comp is None:
        if amplitude_comp != 0.0:
            raise ValueError("sigma_comp is required when amplitude_comp is non-zero")
        sigma_comp_value = source_cfg.sigma_rep
    else:
        if not np.isfinite(sigma_comp) or sigma_comp <= 0.0:
            raise ValueError("sigma_comp must be positive and finite")
        sigma_comp_value = float(sigma_comp)
    return source_cfg, sigma_comp_value, float(amplitude_comp)


def _place_source(
    target_state: FiniteMemoryState,
    source_state: FiniteMemoryState,
    offset: np.ndarray,
    source_rotation: Iterable[Iterable[float]] | None,
) -> tuple[np.ndarray, FiniteMemoryState]:
    center = memory_centroid(target_state) + offset
    placed = place_finite_memory_state(
        source_state,
        center,
        rotation=source_rotation,
    )
    return center, placed


def _source_gradient(
    target_state: FiniteMemoryState,
    placed_source: FiniteMemoryState,
    source_config: SimulationConfig,
    *,
    sigma_comp: float,
    amplitude_comp: float,
) -> np.ndarray:
    return three_scale_gaussian_gradient(
        target_state.x,
        placed_source.memory,
        placed_source.weights,
        sigma_rep=source_config.sigma_rep,
        sigma_att=source_config.sigma_att,
        sigma_comp=sigma_comp,
        amplitude_rep=source_config.amplitude_rep,
        amplitude_att=source_config.amplitude_att,
        amplitude_comp=amplitude_comp,
        deposition_kernel=source_config.deposition_kernel,
        deposition_sigma=source_config.deposition_sigma,
    )


def calibrate_signed_cross_eta(
    target_state: FiniteMemoryState,
    source_state: FiniteMemoryState,
    target_config: SimulationConfig,
    *,
    source_center_offset: Iterable[float],
    response_fraction: float,
    pulse_steps: int,
    source_config: SimulationConfig | None = None,
    source_rotation: Iterable[Iterable[float]] | None = None,
    sigma_comp: float | None = None,
    amplitude_comp: float = 0.0,
) -> SignedCrossCalibration:
    """Calibrate cross_eta from the magnitude of the initial cross drift.

    For label product +1 the update uses the canonical sign
    -cross_eta*grad(Phi_cross). Product -1 reverses that drift. Labels never
    enter the target's self-memory update.
    """

    source_cfg, sigma_comp_value, amplitude_comp_value = _validate_common(
        target_state,
        source_state,
        target_config,
        source_config,
        sigma_comp=sigma_comp,
        amplitude_comp=amplitude_comp,
    )
    if not np.isfinite(response_fraction) or response_fraction <= 0.0:
        raise ValueError("response_fraction must be positive and finite")
    if isinstance(pulse_steps, bool) or not isinstance(pulse_steps, (int, np.integer)):
        raise ValueError("pulse_steps must be an integer")
    if pulse_steps < 1:
        raise ValueError("pulse_steps must be positive")

    offset = _source_offset(source_center_offset, dim=target_state.dim)
    _, placed_source = _place_source(
        target_state,
        source_state,
        offset,
        source_rotation,
    )
    gradient = _source_gradient(
        target_state,
        placed_source,
        source_cfg,
        sigma_comp=sigma_comp_value,
        amplitude_comp=amplitude_comp_value,
    )
    direction = offset / np.linalg.norm(offset)
    canonical_drift = float(np.dot(-gradient, direction))
    if abs(canonical_drift) <= np.finfo(float).eps:
        raise ValueError("initial signed cross drift is too small to calibrate")
    target_radius = float(
        np.sqrt(max(np.trace(memory_shape_tensor(target_state)), 0.0))
    )
    if target_radius <= 0.0:
        raise ValueError("target memory radius must be positive")
    cross_eta = (
        float(response_fraction)
        * target_radius
        / (float(pulse_steps) * abs(canonical_drift))
    )
    return SignedCrossCalibration(
        response_fraction=float(response_fraction),
        pulse_steps=int(pulse_steps),
        source_center_offset=offset,
        target_radius=target_radius,
        initial_gradient=gradient,
        canonical_directional_drift=canonical_drift,
        cross_eta=float(cross_eta),
    )


@njit(cache=True)
def _signed_cross_batch(
    initial_x: np.ndarray,
    initial_memory: np.ndarray,
    target_weights: np.ndarray,
    source_memory: np.ndarray,
    source_weights: np.ndarray,
    label_products: np.ndarray,
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
    source_sigma_comp: float,
    source_amplitude_rep: float,
    source_amplitude_att: float,
    source_amplitude_comp: float,
    cross_eta: float,
    pulse_steps: int,
):
    n_label_paths = label_products.shape[0]
    free_path = n_label_paths
    n_paths = n_label_paths + 1
    n_memory = initial_memory.shape[0]
    dim = initial_x.shape[0]
    n_samples = sample_steps.shape[0]

    positions = np.empty((n_samples, n_label_paths, dim), np.float64)
    centers = np.empty((n_samples, n_label_paths, dim), np.float64)
    tensors = np.empty((n_samples, n_label_paths, dim, dim), np.float64)
    radii = np.empty((n_samples, n_label_paths), np.float64)
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
    source_sigma_comp2 = source_sigma_comp * source_sigma_comp
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
                cross_gradient = np.zeros(dim, np.float64)
                product = 0
                if path != free_path:
                    product = int(label_products[path])
                if product != 0 and step <= pulse_steps and cross_eta != 0.0:
                    cross_gradient = path_three_scale_gradient(
                        xs[path],
                        source_memory,
                        0,
                        source_weights,
                        1.0,
                        source_sigma_rep2,
                        source_sigma_att2,
                        source_sigma_comp2,
                        source_amplitude_rep,
                        source_amplitude_att,
                        source_amplitude_comp,
                    )
                for coord in range(dim):
                    xs[path, coord] = (
                        xs[path, coord]
                        + epsilon * noise[step - 1, coord]
                        - eta * self_gradient[coord]
                        - cross_eta * product * cross_gradient[coord]
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
                else:
                    positions[sample_index, path] = position
                    centers[sample_index, path] = center
                    tensors[sample_index, path] = tensor
                    radii[sample_index, path] = radius
            sample_index += 1

    return (
        positions,
        centers,
        tensors,
        radii,
        free_positions,
        free_centers,
        free_tensors,
        free_radii,
    )


def paired_signed_cross_response(
    target_state: FiniteMemoryState,
    source_state: FiniteMemoryState,
    target_config: SimulationConfig,
    *,
    label_pairs: Iterable[Iterable[int]],
    source_center_offset: Iterable[float],
    noise: Iterable[Iterable[float]],
    sample_steps: Iterable[int],
    cross_eta: float,
    pulse_steps: int,
    source_config: SimulationConfig | None = None,
    source_rotation: Iterable[Iterable[float]] | None = None,
    sigma_comp: float | None = None,
    amplitude_comp: float = 0.0,
) -> SignedCrossResponse:
    """Continue signed label pairs and an exact no-cross path under common noise."""

    source_cfg, sigma_comp_value, amplitude_comp_value = _validate_common(
        target_state,
        source_state,
        target_config,
        source_config,
        sigma_comp=sigma_comp,
        amplitude_comp=amplitude_comp,
    )
    labels = _label_pairs(label_pairs)
    products = np.prod(labels, axis=1, dtype=np.int8)
    offset = _source_offset(source_center_offset, dim=target_state.dim)
    if not np.isfinite(cross_eta) or cross_eta < 0.0:
        raise ValueError("cross_eta must be non-negative and finite")
    if isinstance(pulse_steps, bool) or not isinstance(pulse_steps, (int, np.integer)):
        raise ValueError("pulse_steps must be an integer")
    if pulse_steps < 1:
        raise ValueError("pulse_steps must be positive")

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

    source_center, placed_source = _place_source(
        target_state,
        source_state,
        offset,
        source_rotation,
    )
    initial_gradient = _source_gradient(
        target_state,
        placed_source,
        source_cfg,
        sigma_comp=sigma_comp_value,
        amplitude_comp=amplitude_comp_value,
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
    source_sigma_comp, source_amplitude_comp = effective_gaussian_parameters(
        sigma=sigma_comp_value,
        amplitude=amplitude_comp_value,
        dim=source_cfg.dim,
        deposition_kernel=source_cfg.deposition_kernel,
        deposition_sigma=source_cfg.deposition_sigma,
    )
    (
        positions,
        centers,
        tensors,
        radii,
        free_positions,
        free_centers,
        free_tensors,
        free_radii,
    ) = _signed_cross_batch(
        target_state.x,
        target_state.memory,
        target_state.weights,
        placed_source.memory,
        placed_source.weights,
        products,
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
        float(source_sigma_comp),
        float(source_effective["amplitude_rep"]),
        float(source_effective["amplitude_att"]),
        float(source_amplitude_comp),
        float(cross_eta),
        int(pulse_steps),
    )

    n_shape = target_state.dim * (target_state.dim + 1) // 2
    shape_vectors = np.empty((len(steps), len(labels), n_shape), dtype=float)
    free_shape_vectors = np.empty((len(steps), n_shape), dtype=float)
    for sample_index in range(len(steps)):
        free_shape_vectors[sample_index] = symmetric_tensor_vector(
            free_tensors[sample_index]
        )
        for path in range(len(labels)):
            shape_vectors[sample_index, path] = symmetric_tensor_vector(
                tensors[sample_index, path]
            )

    target_radius = float(
        np.sqrt(max(np.trace(memory_shape_tensor(target_state)), 0.0))
    )
    if target_radius <= 0.0:
        raise ValueError("target memory radius must be positive")
    radius_ratios = radii / target_radius
    free_radius_ratios = free_radii / target_radius

    return SignedCrossResponse(
        sample_steps=steps,
        label_pairs=labels,
        label_products=products,
        source_center_offset=offset,
        source_center=source_center,
        cross_eta=float(cross_eta),
        pulse_steps=int(pulse_steps),
        target_radius=target_radius,
        initial_source_gradient=initial_gradient,
        positions=positions,
        memory_centers=centers,
        shape_vectors=shape_vectors,
        radius_ratios=radius_ratios,
        position_displacements=positions - free_positions[:, None, :],
        memory_center_displacements=centers - free_centers[:, None, :],
        shape_displacements=shape_vectors - free_shape_vectors[:, None, :],
        radius_displacements=radius_ratios - free_radius_ratios[:, None],
        free_positions=free_positions,
        free_memory_centers=free_centers,
        free_shape_vectors=free_shape_vectors,
        free_radius_ratios=free_radius_ratios,
    )
