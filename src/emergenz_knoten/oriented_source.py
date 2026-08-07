"""One-way response to an independently relaxing oriented memory state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from ._continuation import path_gradient, path_observables
from .core import SimulationConfig, validate_simulation_config
from .kernels import (
    double_gaussian_gradient,
    effective_double_gaussian_parameters,
    exponential_memory_weights,
)
from .state import FiniteMemoryState, memory_centroid, place_finite_memory_state

try:
    from numba import njit
except ImportError:  # pragma: no cover

    def njit(*args, **kwargs):
        def wrapper(func):
            return func

        return wrapper


ORIENTED_TARGET_CONDITIONS = ("active", "sign_flip", "channel_off")


@dataclass(frozen=True)
class OrientedMemoryState:
    """Scalar carrier state plus a separately weighted vector memory fibre."""

    scalar_state: FiniteMemoryState
    orientations: np.ndarray
    weights: np.ndarray
    carrier_orientation: np.ndarray
    orientation_relaxation: float

    def __post_init__(self) -> None:
        orientations = np.asarray(self.orientations, dtype=float)
        weights = np.asarray(self.weights, dtype=float)
        carrier = np.asarray(self.carrier_orientation, dtype=float)
        shape = self.scalar_state.memory.shape
        if orientations.shape != shape or not np.isfinite(orientations).all():
            raise ValueError("orientations must be finite and match scalar memory")
        if weights.shape != (shape[0],) or not np.isfinite(weights).all():
            raise ValueError("vector weights must match scalar memory length")
        if np.any(weights < 0.0):
            raise ValueError("vector weights must be non-negative")
        if carrier.shape != (self.scalar_state.dim,) or not np.isfinite(carrier).all():
            raise ValueError("carrier_orientation must match scalar dimension")
        if not np.isfinite(self.orientation_relaxation) or not (
            0.0 < self.orientation_relaxation <= 1.0
        ):
            raise ValueError("orientation_relaxation must lie in (0, 1]")
        orientations = orientations.copy()
        weights = weights.copy()
        carrier = carrier.copy()
        orientations.setflags(write=False)
        weights.setflags(write=False)
        carrier.setflags(write=False)
        object.__setattr__(self, "orientations", orientations)
        object.__setattr__(self, "weights", weights)
        object.__setattr__(self, "carrier_orientation", carrier)

    @property
    def dim(self) -> int:
        return self.scalar_state.dim


@dataclass(frozen=True)
class OrientedOneWayResponse:
    """Autonomous scalar source and paired vector-readout target paths."""

    sample_steps: np.ndarray
    target_conditions: tuple[str, ...]
    source_positions: np.ndarray
    source_memory_centers: np.ndarray
    source_shape_tensors: np.ndarray
    source_radius_ratios: np.ndarray
    source_carrier_orientations: np.ndarray
    target_positions: np.ndarray
    target_memory_centers: np.ndarray
    target_shape_tensors: np.ndarray
    target_radius_ratios: np.ndarray
    source_center_offset: np.ndarray
    vector_eta: float
    vector_sigma: float
    randomization_count: int


@dataclass(frozen=True)
class OrientedSourceTrace:
    """Autonomous scalar source and its persistent carrier orientation."""

    sample_steps: np.ndarray
    positions: np.ndarray
    memory_centers: np.ndarray
    shape_tensors: np.ndarray
    radius_ratios: np.ndarray
    carrier_orientations: np.ndarray


def update_persistent_orientation(
    previous: np.ndarray,
    displacement: np.ndarray,
    *,
    relaxation: float,
) -> np.ndarray:
    """Low-pass a unit step direction without fixing the output magnitude."""

    old = np.asarray(previous, dtype=float)
    step = np.asarray(displacement, dtype=float)
    if old.shape != step.shape or old.ndim != 1:
        raise ValueError("previous and displacement must be matching vectors")
    if not np.isfinite(old).all() or not np.isfinite(step).all():
        raise ValueError("orientation inputs must be finite")
    if not np.isfinite(relaxation) or not 0.0 < relaxation <= 1.0:
        raise ValueError("relaxation must lie in (0, 1]")
    norm = float(np.linalg.norm(step))
    drive = np.zeros_like(step) if norm == 0.0 else step / norm
    return (1.0 - relaxation) * old + relaxation * drive


def advance_oriented_memory_state(
    state: OrientedMemoryState,
    config: SimulationConfig,
    *,
    noise_increment: Iterable[float],
) -> OrientedMemoryState:
    """Advance the passive oriented-memory source by one exact discrete update.

    The scalar memory drives the visible update. The oriented fibre records the
    persistent carrier at the new position but does not yet exert a self-force.
    Keeping this boundary explicit prevents a phenomenological target readout
    from silently becoming a new source equation.
    """

    validate_simulation_config(config)
    if state.dim != config.dim:
        raise ValueError("state and config dimensions must match")
    noise = np.asarray(noise_increment, dtype=float)
    if noise.shape != (state.dim,) or not np.isfinite(noise).all():
        raise ValueError("noise_increment must be finite and match state dimension")

    scalar = state.scalar_state
    gradient = double_gaussian_gradient(
        scalar.x,
        scalar.memory,
        scalar.weights,
        sigma_rep=config.sigma_rep,
        sigma_att=config.sigma_att,
        amplitude_rep=config.amplitude_rep,
        amplitude_att=config.amplitude_att,
        deposition_kernel=config.deposition_kernel,
        deposition_sigma=config.deposition_sigma,
    )
    x_next = scalar.x + config.epsilon * noise - config.eta * gradient
    carrier = update_persistent_orientation(
        state.carrier_orientation,
        x_next - scalar.x,
        relaxation=state.orientation_relaxation,
    )

    memory = np.empty_like(scalar.memory)
    memory[0] = x_next
    memory[1:] = scalar.memory[:-1]
    orientations = np.empty_like(state.orientations)
    orientations[0] = carrier
    orientations[1:] = state.orientations[:-1]
    return OrientedMemoryState(
        scalar_state=FiniteMemoryState(
            x=x_next,
            memory=memory,
            weights=scalar.weights,
        ),
        orientations=orientations,
        weights=state.weights,
        carrier_orientation=carrier,
        orientation_relaxation=state.orientation_relaxation,
    )


def initialize_oriented_memory_state(
    state: FiniteMemoryState,
    *,
    lambda_vector: float,
    vector_mass: float = 1.0,
    orientation_relaxation: float | None = None,
) -> OrientedMemoryState:
    """Reconstruct a persistent vector fibre from an age-ordered scalar state."""

    if state.n_memory < 2:
        raise ValueError("oriented memory requires at least two retained points")
    if not np.isfinite(lambda_vector) or not 0.0 < lambda_vector <= 1.0:
        raise ValueError("lambda_vector must lie in (0, 1]")
    relaxation = (
        float(lambda_vector)
        if orientation_relaxation is None
        else float(orientation_relaxation)
    )
    if not np.isfinite(relaxation) or not 0.0 < relaxation <= 1.0:
        raise ValueError("orientation_relaxation must lie in (0, 1]")
    steps = state.memory[:-1] - state.memory[1:]
    norms = np.linalg.norm(steps, axis=1)
    directions = np.divide(
        steps,
        norms[:, None],
        out=np.zeros_like(steps),
        where=norms[:, None] > 0.0,
    )
    orientations = np.zeros_like(state.memory)
    carrier = np.zeros(state.dim, dtype=float)
    for index in range(state.n_memory - 2, -1, -1):
        carrier = (1.0 - relaxation) * carrier + relaxation * directions[index]
        orientations[index] = carrier
    weights = exponential_memory_weights(
        lambda_vector,
        state.n_memory,
        memory_mass=vector_mass,
    )
    return OrientedMemoryState(
        scalar_state=state,
        orientations=orientations,
        weights=weights,
        carrier_orientation=carrier,
        orientation_relaxation=relaxation,
    )


def place_oriented_memory_state(
    state: OrientedMemoryState,
    target_center: Iterable[float],
    *,
    rotation: Iterable[Iterable[float]] | None = None,
) -> OrientedMemoryState:
    """Rigidly place scalar positions and vector orientations together."""

    placed_scalar = place_finite_memory_state(
        state.scalar_state,
        target_center,
        rotation=rotation,
    )
    if rotation is None:
        orientations = state.orientations
        carrier = state.carrier_orientation
    else:
        transform = np.asarray(rotation, dtype=float)
        orientations = state.orientations @ transform.T
        carrier = transform @ state.carrier_orientation
    return OrientedMemoryState(
        scalar_state=placed_scalar,
        orientations=orientations,
        weights=state.weights,
        carrier_orientation=carrier,
        orientation_relaxation=state.orientation_relaxation,
    )


@njit(cache=True)
def _oriented_field(
    x: np.ndarray,
    history: np.ndarray,
    orientations: np.ndarray,
    head: int,
    weights: np.ndarray,
    sigma2: float,
) -> np.ndarray:
    dim = x.shape[0]
    field = np.zeros(dim, np.float64)
    for age in range(history.shape[0]):
        index = (head + age) % history.shape[0]
        radius2 = 0.0
        for coord in range(dim):
            delta = x[coord] - history[index, coord]
            radius2 += delta * delta
        factor = weights[age] * np.exp(-0.5 * radius2 / sigma2)
        for coord in range(dim):
            field[coord] += factor * orientations[index, coord]
    return field


@njit(cache=True)
def _copy_ring(values: np.ndarray, n_paths: int) -> np.ndarray:
    result = np.empty((n_paths, values.shape[0], values.shape[1]), np.float64)
    for path in range(n_paths):
        result[path] = values
    return result


@njit(cache=True)
def _autonomous_oriented_source_batch(
    source_x_initial: np.ndarray,
    source_memory_initial: np.ndarray,
    source_weights: np.ndarray,
    carrier_orientation_initial: np.ndarray,
    source_noise: np.ndarray,
    sample_steps: np.ndarray,
    source_epsilon: float,
    source_eta: float,
    source_sigma_rep2: float,
    source_sigma_att2: float,
    source_amplitude_rep: float,
    source_amplitude_att: float,
    orientation_relaxation: float,
):
    dim = source_x_initial.shape[0]
    n_memory = source_memory_initial.shape[0]
    n_samples = sample_steps.shape[0]
    source_x = source_x_initial.copy()
    source_history = source_memory_initial.copy()
    carrier = carrier_orientation_initial.copy()
    source_head = 0
    source_mass = np.sum(source_weights)
    positions = np.empty((n_samples, dim), np.float64)
    centers = np.empty((n_samples, dim), np.float64)
    tensors = np.empty((n_samples, dim, dim), np.float64)
    radii = np.empty(n_samples, np.float64)
    carriers = np.empty((n_samples, dim), np.float64)
    sample_index = 0
    n_steps = int(sample_steps[-1])
    for step in range(n_steps + 1):
        if step > 0:
            source_gradient = path_gradient(
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
            previous_source = source_x.copy()
            for coord in range(dim):
                source_x[coord] = (
                    source_x[coord]
                    + source_epsilon * source_noise[step - 1, coord]
                    - source_eta * source_gradient[coord]
                )
            displacement_norm = 0.0
            for coord in range(dim):
                delta = source_x[coord] - previous_source[coord]
                displacement_norm += delta * delta
            displacement_norm = np.sqrt(displacement_norm)
            for coord in range(dim):
                drive = 0.0
                if displacement_norm > 0.0:
                    drive = (
                        source_x[coord] - previous_source[coord]
                    ) / displacement_norm
                carrier[coord] = (1.0 - orientation_relaxation) * carrier[
                    coord
                ] + orientation_relaxation * drive
            source_head = (source_head - 1) % n_memory
            source_history[source_head] = source_x

        while sample_index < n_samples and sample_steps[sample_index] == step:
            position, center, tensor, radius = path_observables(
                source_x,
                source_history,
                source_head,
                source_weights,
                source_mass,
            )
            positions[sample_index] = position
            centers[sample_index] = center
            tensors[sample_index] = tensor
            radii[sample_index] = radius
            carriers[sample_index] = carrier
            sample_index += 1

    return positions, centers, tensors, radii, carriers


@njit(cache=True)
def _one_way_oriented_batch(
    target_x_initial: np.ndarray,
    target_memory_initial: np.ndarray,
    target_weights: np.ndarray,
    source_x_initial: np.ndarray,
    source_memory_initial: np.ndarray,
    source_weights: np.ndarray,
    source_orientations_initial: np.ndarray,
    vector_weights: np.ndarray,
    carrier_orientation_initial: np.ndarray,
    target_noise: np.ndarray,
    source_noise: np.ndarray,
    initial_random_signs: np.ndarray,
    future_random_signs: np.ndarray,
    sample_steps: np.ndarray,
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
    vector_sigma2: float,
    vector_eta: float,
    orientation_relaxation: float,
):
    n_random = initial_random_signs.shape[0]
    n_paths = 3 + n_random
    dim = target_x_initial.shape[0]
    n_memory = source_memory_initial.shape[0]
    n_samples = sample_steps.shape[0]

    target_x = np.empty((n_paths, dim), np.float64)
    for path in range(n_paths):
        target_x[path] = target_x_initial
    target_history = _copy_ring(target_memory_initial, n_paths)
    target_heads = np.zeros(n_paths, np.int64)

    source_x = source_x_initial.copy()
    source_history = source_memory_initial.copy()
    source_orientations = source_orientations_initial.copy()
    random_orientations = np.empty((n_random, n_memory, dim), np.float64)
    for random_index in range(n_random):
        for age in range(n_memory):
            for coord in range(dim):
                random_orientations[random_index, age, coord] = (
                    initial_random_signs[random_index, age]
                    * source_orientations_initial[age, coord]
                )
    carrier = carrier_orientation_initial.copy()
    source_head = 0

    source_positions = np.empty((n_samples, dim), np.float64)
    source_centers = np.empty((n_samples, dim), np.float64)
    source_tensors = np.empty((n_samples, dim, dim), np.float64)
    source_radii = np.empty(n_samples, np.float64)
    source_carriers = np.empty((n_samples, dim), np.float64)
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
            source_gradient = path_gradient(
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
            for path in range(n_paths):
                target_gradient = path_gradient(
                    target_x[path],
                    target_history[path],
                    target_heads[path],
                    target_weights,
                    target_eta,
                    target_sigma_rep2,
                    target_sigma_att2,
                    target_amplitude_rep,
                    target_amplitude_att,
                )
                vector_field = np.zeros(dim, np.float64)
                if path == 0 or path == 1:
                    vector_field = _oriented_field(
                        target_x[path],
                        source_history,
                        source_orientations,
                        source_head,
                        vector_weights,
                        vector_sigma2,
                    )
                    if path == 1:
                        vector_field *= -1.0
                elif path >= 3:
                    vector_field = _oriented_field(
                        target_x[path],
                        source_history,
                        random_orientations[path - 3],
                        source_head,
                        vector_weights,
                        vector_sigma2,
                    )
                for coord in range(dim):
                    target_x[path, coord] = (
                        target_x[path, coord]
                        + target_epsilon * target_noise[step - 1, coord]
                        - target_eta * target_gradient[coord]
                        + vector_eta * vector_field[coord]
                    )
                target_heads[path] = (
                    target_heads[path] - 1
                ) % target_memory_initial.shape[0]
                target_history[path, target_heads[path]] = target_x[path]

            previous_source = source_x.copy()
            for coord in range(dim):
                source_x[coord] = (
                    source_x[coord]
                    + source_epsilon * source_noise[step - 1, coord]
                    - source_eta * source_gradient[coord]
                )
            displacement_norm = 0.0
            for coord in range(dim):
                delta = source_x[coord] - previous_source[coord]
                displacement_norm += delta * delta
            displacement_norm = np.sqrt(displacement_norm)
            for coord in range(dim):
                drive = 0.0
                if displacement_norm > 0.0:
                    drive = (
                        source_x[coord] - previous_source[coord]
                    ) / displacement_norm
                carrier[coord] = (1.0 - orientation_relaxation) * carrier[
                    coord
                ] + orientation_relaxation * drive
            source_head = (source_head - 1) % n_memory
            source_history[source_head] = source_x
            source_orientations[source_head] = carrier
            for random_index in range(n_random):
                sign = future_random_signs[random_index, step - 1]
                for coord in range(dim):
                    random_orientations[random_index, source_head, coord] = (
                        sign * carrier[coord]
                    )

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
            source_tensors[sample_index] = source_tensor
            source_radii[sample_index] = source_radius
            source_carriers[sample_index] = carrier
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
        source_carriers,
        target_positions,
        target_centers,
        target_tensors,
        target_radii,
    )


def _validated_steps(sample_steps: Iterable[int]) -> np.ndarray:
    steps = np.asarray(list(sample_steps), dtype=int)
    if steps.ndim != 1 or steps.size < 2 or steps[0] != 0:
        raise ValueError("sample_steps must start at zero and contain two points")
    if np.any(steps < 0) or not np.array_equal(steps, np.unique(steps)):
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
        raise ValueError(f"{name} must have shape (max(sample_steps), dim)")
    return values


def autonomous_oriented_source_trace(
    source_state: OrientedMemoryState,
    config: SimulationConfig,
    *,
    source_noise: Iterable[Iterable[float]],
    sample_steps: Iterable[int],
) -> OrientedSourceTrace:
    """Evolve only the autonomous source represented in a one-way response."""

    validate_simulation_config(config)
    if source_state.dim != config.dim:
        raise ValueError("source state and config dimensions must match")
    steps = _validated_steps(sample_steps)
    noise = _validated_noise(
        source_noise,
        n_steps=int(steps[-1]),
        dim=config.dim,
        name="source_noise",
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
    result = _autonomous_oriented_source_batch(
        source_state.scalar_state.x,
        source_state.scalar_state.memory,
        source_state.scalar_state.weights,
        source_state.carrier_orientation,
        noise,
        steps,
        float(config.epsilon),
        float(config.eta),
        float(effective["sigma_rep"]) ** 2,
        float(effective["sigma_att"]) ** 2,
        float(effective["amplitude_rep"]),
        float(effective["amplitude_att"]),
        float(source_state.orientation_relaxation),
    )
    initial_radius = float(result[3][0])
    if initial_radius <= 0.0:
        raise ValueError("source memory radius must be positive")
    return OrientedSourceTrace(
        sample_steps=steps,
        positions=result[0],
        memory_centers=result[1],
        shape_tensors=result[2],
        radius_ratios=result[3] / initial_radius,
        carrier_orientations=result[4],
    )


def one_way_oriented_response(
    target_state: FiniteMemoryState,
    source_state: OrientedMemoryState,
    config: SimulationConfig,
    *,
    source_center_offset: Iterable[float],
    target_noise: Iterable[Iterable[float]],
    source_noise: Iterable[Iterable[float]],
    sample_steps: Iterable[int],
    vector_eta: float,
    vector_sigma: float,
    randomization_count: int = 16,
    random_seed: int = 0,
    source_rotation: Iterable[Iterable[float]] | None = None,
) -> OrientedOneWayResponse:
    """Evolve an autonomous source with paired oriented-readout controls."""

    validate_simulation_config(config)
    if target_state.dim != source_state.dim or target_state.dim != config.dim:
        raise ValueError("target, source, and config dimensions must match")
    if not np.isfinite(vector_eta) or vector_eta < 0.0:
        raise ValueError("vector_eta must be finite and non-negative")
    if not np.isfinite(vector_sigma) or vector_sigma <= 0.0:
        raise ValueError("vector_sigma must be positive")
    if randomization_count < 1:
        raise ValueError("randomization_count must be positive")
    offset = np.asarray(source_center_offset, dtype=float)
    if offset.shape != (config.dim,) or not np.isfinite(offset).all():
        raise ValueError("source_center_offset must match the state dimension")
    if float(np.linalg.norm(offset)) <= 0.0:
        raise ValueError("source_center_offset must be non-zero")
    placed = place_oriented_memory_state(
        source_state,
        memory_centroid(target_state) + offset,
        rotation=source_rotation,
    )
    steps = _validated_steps(sample_steps)
    n_steps = int(steps[-1])
    target_noise_values = _validated_noise(
        target_noise,
        n_steps=n_steps,
        dim=config.dim,
        name="target_noise",
    )
    source_noise_values = _validated_noise(
        source_noise,
        n_steps=n_steps,
        dim=config.dim,
        name="source_noise",
    )
    rng = np.random.default_rng(random_seed)
    initial_signs = (
        2.0
        * rng.integers(
            0,
            2,
            size=(randomization_count, placed.scalar_state.n_memory),
        )
        - 1.0
    )
    future_signs = (
        2.0
        * rng.integers(
            0,
            2,
            size=(randomization_count, n_steps),
        )
        - 1.0
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
    result = _one_way_oriented_batch(
        target_state.x,
        target_state.memory,
        target_state.weights,
        placed.scalar_state.x,
        placed.scalar_state.memory,
        placed.scalar_state.weights,
        placed.orientations,
        placed.weights,
        placed.carrier_orientation,
        target_noise_values,
        source_noise_values,
        initial_signs,
        future_signs,
        steps,
        float(config.epsilon),
        float(config.eta),
        float(config.epsilon),
        float(config.eta),
        float(effective["sigma_rep"]) ** 2,
        float(effective["sigma_att"]) ** 2,
        float(effective["amplitude_rep"]),
        float(effective["amplitude_att"]),
        float(effective["sigma_rep"]) ** 2,
        float(effective["sigma_att"]) ** 2,
        float(effective["amplitude_rep"]),
        float(effective["amplitude_att"]),
        float(vector_sigma) ** 2,
        float(vector_eta),
        float(placed.orientation_relaxation),
    )
    source_radius = float(result[3][0])
    target_radius = float(result[8][0, 0])
    if source_radius <= 0.0 or target_radius <= 0.0:
        raise ValueError("source and target memory radii must be positive")
    conditions = ORIENTED_TARGET_CONDITIONS + tuple(
        f"random_sign_{index}" for index in range(randomization_count)
    )
    return OrientedOneWayResponse(
        sample_steps=steps,
        target_conditions=conditions,
        source_positions=result[0],
        source_memory_centers=result[1],
        source_shape_tensors=result[2],
        source_radius_ratios=result[3] / source_radius,
        source_carrier_orientations=result[4],
        target_positions=result[5],
        target_memory_centers=result[6],
        target_shape_tensors=result[7],
        target_radius_ratios=result[8] / target_radius,
        source_center_offset=offset,
        vector_eta=float(vector_eta),
        vector_sigma=float(vector_sigma),
        randomization_count=randomization_count,
    )
