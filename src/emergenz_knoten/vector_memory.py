"""Minimal oriented-memory extension for finite-memory simulations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import numpy as np

from .core import (
    SimulationConfig,
    memory_horizon,
    validate_simulation_config,
)
from .kernels import double_gaussian_gradient, exponential_memory_weights
from .markov.features import augmented_feature_names, memory_summary_features
from .state import FiniteMemoryState


VectorForceMode = Literal["alignment", "transverse_2d"]
HistoryCurrentMode = Literal["displacement", "unit"]


@dataclass(frozen=True)
class VectorMemoryConfig:
    """Configuration for a scalar-memory simulation with an oriented memory channel.

    ``scalar`` is intentionally kept as an embedded ``SimulationConfig`` so that
    ``eta_vector=0`` can be tested against the canonical scalar simulator.
    """

    scalar: SimulationConfig = field(default_factory=SimulationConfig)
    lambda_vector: float | None = None
    vector_mass: float = 1.0
    eta_vector: float = 0.0
    sigma_vector: float = 1.0
    vector_memory_factor: float | None = None
    max_vector_memory: int | None = None
    force_mode: VectorForceMode = "alignment"


def _validate_vector_config(config: VectorMemoryConfig) -> None:
    validate_simulation_config(config.scalar)
    lambda_vector = _lambda_vector(config)
    if not np.isfinite(lambda_vector) or not 0.0 < lambda_vector <= 1.0:
        raise ValueError("lambda_vector must satisfy 0 < value <= 1")
    if not np.isfinite(config.vector_mass) or config.vector_mass < 0.0:
        raise ValueError("vector_mass must be non-negative")
    if not np.isfinite(config.eta_vector):
        raise ValueError("eta_vector must be finite")
    if not np.isfinite(config.sigma_vector) or config.sigma_vector <= 0.0:
        raise ValueError("sigma_vector must be positive")
    if config.vector_memory_factor is not None and (
        not np.isfinite(config.vector_memory_factor)
        or config.vector_memory_factor <= 0.0
    ):
        raise ValueError("vector_memory_factor must be positive")
    if config.max_vector_memory is not None and config.max_vector_memory < 1:
        raise ValueError("max_vector_memory must be positive")
    if config.force_mode not in ("alignment", "transverse_2d"):
        raise ValueError("unknown force_mode")
    if config.force_mode == "transverse_2d" and config.scalar.dim != 2:
        raise ValueError("transverse_2d force_mode requires dim=2")


def _lambda_vector(config: VectorMemoryConfig) -> float:
    return (
        config.scalar.alpha
        if config.lambda_vector is None
        else float(config.lambda_vector)
    )


def _vector_horizon(config: VectorMemoryConfig) -> int:
    lambda_value = _lambda_vector(config)
    factor = config.scalar.memory_factor
    if config.vector_memory_factor is not None:
        factor = config.vector_memory_factor
    max_memory = config.scalar.max_memory
    if config.max_vector_memory is not None:
        max_memory = config.max_vector_memory
    return min(max_memory, max(1, int(factor / lambda_value)))


def normalize_orientation(displacement: np.ndarray) -> np.ndarray:
    """Return a unit orientation, or zeros for a zero displacement."""

    disp = np.asarray(displacement, dtype=float)
    norm = float(np.linalg.norm(disp))
    if norm == 0.0:
        return np.zeros_like(disp)
    return disp / norm


def oriented_history_from_state(
    state: FiniteMemoryState,
    *,
    mode: HistoryCurrentMode = "displacement",
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Derive ordered current deposits from a retained scalar history."""

    if state.n_memory < 2:
        raise ValueError("oriented history requires at least two memory points")
    if mode not in ("displacement", "unit"):
        raise ValueError("unknown history current mode")
    positions = state.memory[:-1].copy()
    currents = (state.memory[:-1] - state.memory[1:]).copy()
    if mode == "unit":
        norms = np.linalg.norm(currents, axis=1)
        nonzero = norms > 0.0
        currents[nonzero] /= norms[nonzero, None]
        currents[~nonzero] = 0.0
    return positions, currents, state.weights[:-1].copy()


def update_vector_history(
    positions: np.ndarray,
    orientations: np.ndarray,
    x: np.ndarray,
    orientation: np.ndarray,
    filled: int,
) -> tuple[np.ndarray, np.ndarray, int]:
    """Push a new oriented deposit into finite vector memory."""

    if positions.shape != orientations.shape:
        raise ValueError("positions and orientations must have the same shape")
    if filled < positions.shape[0]:
        if filled > 0:
            positions[1 : filled + 1] = positions[:filled]
            orientations[1 : filled + 1] = orientations[:filled]
        filled += 1
    else:
        positions[1:] = positions[:-1]
        orientations[1:] = orientations[:-1]
    positions[0] = x
    orientations[0] = orientation
    return positions, orientations, filled


def vector_gaussian_field(
    x: np.ndarray,
    positions: np.ndarray,
    orientations: np.ndarray,
    weights: np.ndarray,
    *,
    sigma: float,
) -> np.ndarray:
    """Evaluate the local oriented memory field at ``x``."""

    x_arr = np.asarray(x, dtype=float)
    pos = np.asarray(positions, dtype=float)
    orient = np.asarray(orientations, dtype=float)
    w = np.asarray(weights, dtype=float)
    if pos.size == 0:
        return np.zeros_like(x_arr)
    if pos.ndim != 2:
        raise ValueError("positions must have shape (n_memory, dim)")
    if orient.shape != pos.shape:
        raise ValueError("orientations must match positions")
    if w.shape[0] != pos.shape[0]:
        raise ValueError("weights must match positions length")
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")

    dx = x_arr[None, :] - pos
    r2 = np.einsum("ij,ij->i", dx, dx)
    kernel = np.exp(-0.5 * r2 / (sigma * sigma))
    return np.sum((w * kernel)[:, None] * orient, axis=0)


def antisymmetric_current_tensor(
    positions: np.ndarray,
    currents: np.ndarray,
    weights: np.ndarray,
    *,
    origin: np.ndarray,
) -> np.ndarray:
    """Return the weighted bivector current about a supplied origin."""

    pos = np.asarray(positions, dtype=float)
    current = np.asarray(currents, dtype=float)
    w = np.asarray(weights, dtype=float)
    center = np.asarray(origin, dtype=float)
    if pos.ndim != 2 or current.shape != pos.shape:
        raise ValueError("positions and currents must have shape (n_memory, dim)")
    if w.shape != (pos.shape[0],):
        raise ValueError("weights must match positions length")
    if center.shape != (pos.shape[1],):
        raise ValueError("origin must match current dimension")
    radial = pos - center[None, :]
    wedges = (
        radial[:, :, None] * current[:, None, :]
        - current[:, :, None] * radial[:, None, :]
    )
    return np.sum(w[:, None, None] * wedges, axis=0)


def antisymmetric_current_coherence(
    positions: np.ndarray,
    currents: np.ndarray,
    weights: np.ndarray,
    *,
    origin: np.ndarray,
) -> float:
    """Return coherent bivector norm divided by absolute bivector current."""

    pos = np.asarray(positions, dtype=float)
    current = np.asarray(currents, dtype=float)
    w = np.asarray(weights, dtype=float)
    radial = pos - np.asarray(origin, dtype=float)[None, :]
    wedges = (
        radial[:, :, None] * current[:, None, :]
        - current[:, :, None] * radial[:, None, :]
    )
    absolute = float(np.sum(w * np.linalg.norm(wedges, axis=(1, 2))))
    if absolute == 0.0:
        return 0.0
    tensor = antisymmetric_current_tensor(pos, current, w, origin=origin)
    return float(np.linalg.norm(tensor) / absolute)


def vector_field_coherence(
    x: np.ndarray,
    positions: np.ndarray,
    currents: np.ndarray,
    weights: np.ndarray,
    *,
    sigma: float,
) -> float:
    """Return local directed current divided by local absolute current."""

    field = vector_gaussian_field(
        x,
        positions,
        currents,
        weights,
        sigma=sigma,
    )
    dx = np.asarray(x, dtype=float)[None, :] - np.asarray(positions, dtype=float)
    kernel = np.exp(-0.5 * np.einsum("ij,ij->i", dx, dx) / (sigma * sigma))
    absolute_current = float(
        np.sum(
            np.asarray(weights, dtype=float) * kernel * np.linalg.norm(currents, axis=1)
        )
    )
    if absolute_current == 0.0:
        return 0.0
    return float(np.linalg.norm(field) / absolute_current)


def vector_memory_feature_names(dim: int) -> list[str]:
    """Return feature names for the reduced vector-memory summary."""

    if dim < 1:
        raise ValueError("dim must be positive")
    return (
        [f"vector_field_{i}" for i in range(dim)]
        + [f"mean_orientation_{i}" for i in range(dim)]
        + ["vector_field_norm", "mean_orientation_norm", "vector_memory_mass"]
    )


def vector_memory_summary_features(
    x: np.ndarray,
    positions: np.ndarray,
    orientations: np.ndarray,
    weights: np.ndarray,
    *,
    sigma: float,
) -> np.ndarray:
    """Compress oriented finite memory into diagnostic features."""

    x_arr = np.asarray(x, dtype=float)
    pos = np.asarray(positions, dtype=float)
    orient = np.asarray(orientations, dtype=float)
    w = np.asarray(weights, dtype=float)
    if pos.size == 0 or w.size == 0:
        field = np.zeros_like(x_arr)
        mean_orientation = np.zeros_like(x_arr)
        tail = np.array([0.0, 0.0, 0.0], dtype=float)
        return np.concatenate([field, mean_orientation, tail])
    if orient.shape != pos.shape:
        raise ValueError("orientations must match positions")
    if pos.shape[0] != w.shape[0]:
        raise ValueError("weights must match positions length")
    mass = float(w.sum())
    if mass <= 0.0:
        field = np.zeros_like(x_arr)
        mean_orientation = np.zeros_like(x_arr)
        tail = np.array([0.0, 0.0, 0.0], dtype=float)
        return np.concatenate([field, mean_orientation, tail])

    field = vector_gaussian_field(
        x_arr,
        pos,
        orient,
        w,
        sigma=sigma,
    )
    mean_orientation = np.sum((w / mass)[:, None] * orient, axis=0)
    tail = np.array(
        [
            float(np.linalg.norm(field)),
            float(np.linalg.norm(mean_orientation)),
            mass,
        ],
        dtype=float,
    )
    return np.concatenate([field, mean_orientation, tail])


def vector_memory_force(
    x: np.ndarray,
    positions: np.ndarray,
    orientations: np.ndarray,
    weights: np.ndarray,
    *,
    sigma: float,
    mode: VectorForceMode = "alignment",
) -> np.ndarray:
    """Return the switchable vector-memory force contribution."""

    field = vector_gaussian_field(
        x,
        positions,
        orientations,
        weights,
        sigma=sigma,
    )
    if mode == "alignment":
        return field
    if mode == "transverse_2d":
        if field.shape[0] != 2:
            raise ValueError("transverse_2d force_mode requires dim=2")
        return np.array([-field[1], field[0]], dtype=float)
    raise ValueError("unknown force_mode")


def simulate_vector_memory(
    config: VectorMemoryConfig, *, seed: int = 0
) -> dict[str, np.ndarray]:
    """Run the scalar finite-memory model with an optional vector-memory channel."""

    _validate_vector_config(config)
    scalar = config.scalar
    rng = np.random.default_rng(seed)

    scalar_horizon = memory_horizon(scalar)
    scalar_weights = exponential_memory_weights(
        scalar.alpha,
        scalar_horizon,
        memory_mass=scalar.memory_mass,
    )
    scalar_history = np.zeros((scalar_horizon, scalar.dim), dtype=float)
    scalar_filled = 0

    vector_horizon = _vector_horizon(config)
    vector_weights = exponential_memory_weights(
        _lambda_vector(config),
        vector_horizon,
        memory_mass=config.vector_mass,
    )
    vector_positions = np.zeros((vector_horizon, scalar.dim), dtype=float)
    vector_orientations = np.zeros((vector_horizon, scalar.dim), dtype=float)
    vector_filled = 0

    x = np.zeros(scalar.dim, dtype=float)
    samples: list[np.ndarray] = []
    sample_steps: list[int] = []
    features: list[np.ndarray] = []

    for step in range(1, scalar.steps + 1):
        if scalar_filled and scalar.eta != 0.0 and scalar.memory_mass != 0.0:
            scalar_grad = double_gaussian_gradient(
                x,
                scalar_history[:scalar_filled],
                scalar_weights[:scalar_filled],
                sigma_rep=scalar.sigma_rep,
                sigma_att=scalar.sigma_att,
                amplitude_rep=scalar.amplitude_rep,
                amplitude_att=scalar.amplitude_att,
                deposition_kernel=scalar.deposition_kernel,
                deposition_sigma=scalar.deposition_sigma,
            )
        else:
            scalar_grad = np.zeros(scalar.dim, dtype=float)

        if vector_filled and config.eta_vector != 0.0 and config.vector_mass != 0.0:
            vector_force = vector_memory_force(
                x,
                vector_positions[:vector_filled],
                vector_orientations[:vector_filled],
                vector_weights[:vector_filled],
                sigma=config.sigma_vector,
                mode=config.force_mode,
            )
        else:
            vector_force = np.zeros(scalar.dim, dtype=float)

        noise = rng.normal(size=scalar.dim)
        x_next = x + scalar.epsilon * noise - scalar.eta * scalar_grad
        x_next = x_next + config.eta_vector * vector_force
        orientation = normalize_orientation(x_next - x)
        x = x_next

        if scalar_filled < scalar_horizon:
            if scalar_filled > 0:
                scalar_history[1 : scalar_filled + 1] = scalar_history[:scalar_filled]
            scalar_filled += 1
        else:
            scalar_history[1:] = scalar_history[:-1]
        scalar_history[0] = x

        vector_positions, vector_orientations, vector_filled = update_vector_history(
            vector_positions,
            vector_orientations,
            x,
            orientation,
            vector_filled,
        )

        if step >= scalar.burn_in and step % scalar.sample_every == 0:
            current_memory = scalar_history[:scalar_filled].copy()
            current_weights = scalar_weights[:scalar_filled].copy()
            current_vector_positions = vector_positions[:vector_filled].copy()
            current_vector_orientations = vector_orientations[:vector_filled].copy()
            current_vector_weights = vector_weights[:vector_filled].copy()
            samples.append(x.copy())
            sample_steps.append(step)
            features.append(
                np.concatenate(
                    [
                        memory_summary_features(x, current_memory, current_weights),
                        vector_memory_summary_features(
                            x,
                            current_vector_positions,
                            current_vector_orientations,
                            current_vector_weights,
                            sigma=config.sigma_vector,
                        ),
                    ]
                )
            )

    return {
        "samples": np.asarray(samples, dtype=float),
        "sample_steps": np.asarray(sample_steps, dtype=int),
        "augmented_features": np.asarray(features, dtype=float),
        "feature_names": np.asarray(
            [
                *augmented_feature_names(scalar.dim),
                *vector_memory_feature_names(scalar.dim),
            ],
            dtype=str,
        ),
        "final_x": x.copy(),
        "memory": scalar_history[:scalar_filled].copy(),
        "weights": scalar_weights[:scalar_filled].copy(),
        "vector_positions": vector_positions[:vector_filled].copy(),
        "vector_orientations": vector_orientations[:vector_filled].copy(),
        "vector_weights": vector_weights[:vector_filled].copy(),
    }
