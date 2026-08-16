"""Matched generalized-force and work diagnostics for scalar memory."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

import numpy as np

from .continuum_limit import (
    ScalarContinuumCase,
    _form_state,
    _path_gradient,
    _positive_finite,
    _weighted_center_and_radius,
)

try:
    from numba import njit
except ImportError:  # pragma: no cover

    def njit(*args, **kwargs):
        def wrapper(func):
            return func

        return wrapper


@dataclass(frozen=True)
class PairedForceWorkResponse:
    """Common-noise mirrored response to a prescribed generalized force."""

    sample_times: np.ndarray
    impulse_fractions: np.ndarray
    impulse_amplitudes: np.ndarray
    normalized_force_profile: np.ndarray
    integrated_impulses: np.ndarray
    position_responses: np.ndarray
    center_responses: np.ndarray
    relative_responses: np.ndarray
    position_even_leakage: np.ndarray
    relative_even_leakage: np.ndarray
    memory_radii: np.ndarray
    branch_cumulative_work: np.ndarray
    paired_even_cumulative_work: np.ndarray
    branch_center_cumulative_work: np.ndarray
    paired_even_center_cumulative_work: np.ndarray
    control_positions: np.ndarray
    control_centers: np.ndarray
    control_relative: np.ndarray
    force_off_maximum_residual: float


@dataclass(frozen=True)
class StationaryVisibleMSD:
    """Monte Carlo and reference MSDs for the stationary local scalar mode."""

    sample_times: np.ndarray
    simulated_msd: np.ndarray
    exact_discrete_msd: np.ndarray
    continuum_msd: np.ndarray
    n_paths: int
    seed: int


@dataclass(frozen=True)
class StationaryCenterMSD:
    """Monte Carlo and reference MSDs for the local scalar-memory center."""

    sample_times: np.ndarray
    simulated_msd: np.ndarray
    exact_discrete_msd: np.ndarray
    continuum_msd: np.ndarray
    n_paths: int
    seed: int


@njit(cache=True)
def _paired_force_work_batch(
    initial_x: np.ndarray,
    initial_history: np.ndarray,
    initial_head: int,
    weights: np.ndarray,
    noise: np.ndarray,
    impulse_amplitudes: np.ndarray,
    force_profile: np.ndarray,
    axis: np.ndarray,
    alpha: float,
    epsilon: float,
    eta: float,
    sigma_rep2: float,
    sigma_att2: float,
    amplitude_rep: float,
    amplitude_att: float,
):
    n_impulses = impulse_amplitudes.shape[0]
    n_paths = 2 + 2 * n_impulses
    n_steps = noise.shape[0]
    dim = initial_x.shape[0]
    horizon = weights.shape[0]
    mass = np.sum(weights)
    q = 1.0 - alpha
    tail = q**horizon
    deposition_fraction = alpha / (1.0 - tail)

    xs = np.empty((n_paths, dim), np.float64)
    histories = np.empty((n_paths, horizon, dim), np.float64)
    heads = np.empty(n_paths, np.int64)
    centers = np.empty((n_paths, dim), np.float64)
    base_center, initial_radius = _weighted_center_and_radius(
        initial_history, initial_head, weights, mass
    )
    base_second_moment = initial_radius * initial_radius
    for coord in range(dim):
        base_second_moment += base_center[coord] * base_center[coord]
    second_moments = np.empty(n_paths, np.float64)
    cumulative_work = np.zeros(n_paths, np.float64)
    cumulative_center_work = np.zeros(n_paths, np.float64)
    for path in range(n_paths):
        xs[path] = initial_x
        histories[path] = initial_history
        heads[path] = initial_head
        centers[path] = base_center
        second_moments[path] = base_second_moment

    positions = np.empty((n_steps + 1, n_paths, dim), np.float64)
    center_trace = np.empty((n_steps + 1, n_paths, dim), np.float64)
    relative = np.empty((n_steps + 1, n_paths, dim), np.float64)
    radii = np.empty((n_steps + 1, n_paths), np.float64)
    work_trace = np.empty((n_steps + 1, n_paths), np.float64)
    center_work_trace = np.empty((n_steps + 1, n_paths), np.float64)
    for path in range(n_paths):
        radii[0, path] = initial_radius
        work_trace[0, path] = 0.0
        center_work_trace[0, path] = 0.0
        for coord in range(dim):
            positions[0, path, coord] = xs[path, coord]
            center_trace[0, path, coord] = centers[path, coord]
            relative[0, path, coord] = xs[path, coord] - centers[path, coord]

    for step in range(n_steps):
        for path in range(n_paths):
            gradient = _path_gradient(
                xs[path],
                histories[path],
                heads[path],
                horizon,
                weights,
                sigma_rep2,
                sigma_att2,
                amplitude_rep,
                amplitude_att,
            )
            force_scalar = 0.0
            if path >= 2:
                impulse_index = (path - 2) // 2
                sign = 1.0 if (path - 2) % 2 == 0 else -1.0
                force_scalar = (
                    sign
                    * impulse_amplitudes[impulse_index]
                    * force_profile[step]
                )

            oldest_index = (heads[path] + horizon - 1) % horizon
            oldest = histories[path, oldest_index].copy()
            oldest_norm2 = 0.0
            work_increment = 0.0
            for coord in range(dim):
                oldest_norm2 += oldest[coord] * oldest[coord]
                old_value = xs[path, coord]
                xs[path, coord] += (
                    epsilon * noise[step, coord]
                    - eta * gradient[coord]
                    + alpha * force_scalar * axis[coord]
                )
                work_increment += (
                    force_scalar * axis[coord] * (xs[path, coord] - old_value)
                )
            cumulative_work[path] += work_increment

            x_norm2 = 0.0
            center_work_increment = 0.0
            for coord in range(dim):
                x_norm2 += xs[path, coord] * xs[path, coord]
                old_center_value = centers[path, coord]
                new_center_value = (
                    q * old_center_value
                    + deposition_fraction * xs[path, coord]
                    - deposition_fraction * tail * oldest[coord]
                )
                centers[path, coord] = new_center_value
                center_work_increment += (
                    force_scalar
                    * axis[coord]
                    * (new_center_value - old_center_value)
                )
            cumulative_center_work[path] += center_work_increment
            second_moments[path] = (
                q * second_moments[path]
                + deposition_fraction * x_norm2
                - deposition_fraction * tail * oldest_norm2
            )
            center_norm2 = 0.0
            for coord in range(dim):
                center_norm2 += centers[path, coord] * centers[path, coord]
            radius2 = second_moments[path] - center_norm2
            radii[step + 1, path] = np.sqrt(max(radius2, 0.0))

            heads[path] = (heads[path] - 1) % horizon
            histories[path, heads[path]] = xs[path]
            work_trace[step + 1, path] = cumulative_work[path]
            center_work_trace[step + 1, path] = cumulative_center_work[path]
            for coord in range(dim):
                positions[step + 1, path, coord] = xs[path, coord]
                center_trace[step + 1, path, coord] = centers[path, coord]
                relative[step + 1, path, coord] = (
                    xs[path, coord] - centers[path, coord]
                )

    return (
        positions,
        center_trace,
        relative,
        radii,
        work_trace,
        center_work_trace,
    )


def simulate_matched_force_work_response(
    case: ScalarContinuumCase,
    *,
    formation_noise: Iterable[Iterable[float]],
    response_noise: Iterable[Iterable[float]],
    impulse_fractions: Iterable[float],
    normalized_force_profile: Iterable[float],
    axis: Iterable[float],
    memory_mass: float = 1.0,
    sigma_rep: float = 1.0,
    sigma_att: float = 3.0,
    amplitude_rep: float = 1.0,
    amplitude_att: float = 35.0,
) -> PairedForceWorkResponse:
    """Apply mirrored generalized forces with update displacement ``alpha*f``."""

    formation = np.asarray(formation_noise, dtype=float)
    response = np.asarray(response_noise, dtype=float)
    profile = np.asarray(list(normalized_force_profile), dtype=float)
    if (
        formation.ndim != 2
        or response.ndim != 2
        or formation.shape[1] != response.shape[1]
        or formation.shape[0] < case.horizon
        or response.shape[0] < 1
        or profile.shape != (response.shape[0],)
        or not np.isfinite(formation).all()
        or not np.isfinite(response).all()
        or not np.isfinite(profile).all()
    ):
        raise ValueError("formation, response and force profile must be compatible")
    if not np.any(profile != 0.0):
        raise ValueError("normalized_force_profile must contain a non-zero input")

    direction = np.asarray(axis, dtype=float)
    if direction.shape != (formation.shape[1],) or not np.isfinite(direction).all():
        raise ValueError("axis must match the noise dimension")
    direction_norm = float(np.linalg.norm(direction))
    if direction_norm <= 0.0:
        raise ValueError("axis must be non-zero")
    direction = direction / direction_norm

    fractions = np.asarray(list(impulse_fractions), dtype=float)
    if (
        fractions.ndim != 1
        or fractions.size < 1
        or not np.isfinite(fractions).all()
        or np.any(fractions <= 0.0)
        or not np.array_equal(fractions, np.unique(fractions))
    ):
        raise ValueError("impulse_fractions must be unique increasing positive values")
    mass = _positive_finite("memory_mass", memory_mass)
    impulses = fractions * case.continuum_rms_radius
    ages = np.arange(case.horizon, dtype=float)
    weights = mass * case.alpha * np.power(case.q, ages)
    initial_x, initial_history, initial_head, filled = _form_state(
        formation,
        weights,
        case.epsilon,
        case.eta,
        float(sigma_rep) ** 2,
        float(sigma_att) ** 2,
        float(amplitude_rep),
        float(amplitude_att),
    )
    if filled != case.horizon:
        raise RuntimeError("formation did not fill the finite memory horizon")

    (
        positions,
        centers,
        relative,
        radii,
        work,
        center_work,
    ) = _paired_force_work_batch(
        initial_x,
        initial_history,
        initial_head,
        weights,
        response,
        impulses,
        profile,
        direction,
        case.alpha,
        case.epsilon,
        case.eta,
        float(sigma_rep) ** 2,
        float(sigma_att) ** 2,
        float(amplitude_rep),
        float(amplitude_att),
    )

    n_steps = response.shape[0]
    dim = response.shape[1]
    position_response = np.empty((fractions.size, n_steps + 1, dim), dtype=float)
    center_response = np.empty_like(position_response)
    relative_response = np.empty_like(position_response)
    position_even = np.empty_like(position_response)
    relative_even = np.empty_like(position_response)
    branch_work = np.empty((fractions.size, 2, n_steps + 1), dtype=float)
    paired_work = np.empty((fractions.size, n_steps + 1), dtype=float)
    branch_center_work = np.empty(
        (fractions.size, 2, n_steps + 1), dtype=float
    )
    paired_center_work = np.empty((fractions.size, n_steps + 1), dtype=float)
    for impulse_index, impulse in enumerate(impulses):
        plus = 2 + 2 * impulse_index
        minus = plus + 1
        scale = 2.0 * impulse
        position_response[impulse_index] = (
            positions[:, plus] - positions[:, minus]
        ) / scale
        center_response[impulse_index] = (
            centers[:, plus] - centers[:, minus]
        ) / scale
        relative_response[impulse_index] = (
            relative[:, plus] - relative[:, minus]
        ) / scale
        position_even[impulse_index] = (
            positions[:, plus] + positions[:, minus] - 2.0 * positions[:, 0]
        ) / scale
        relative_even[impulse_index] = (
            relative[:, plus] + relative[:, minus] - 2.0 * relative[:, 0]
        ) / scale
        branch_work[impulse_index, 0] = work[:, plus]
        branch_work[impulse_index, 1] = work[:, minus]
        paired_work[impulse_index] = 0.5 * (work[:, plus] + work[:, minus])
        branch_center_work[impulse_index, 0] = center_work[:, plus]
        branch_center_work[impulse_index, 1] = center_work[:, minus]
        paired_center_work[impulse_index] = 0.5 * (
            center_work[:, plus] + center_work[:, minus]
        )

    off_residual = max(
        float(np.max(np.abs(positions[:, 0] - positions[:, 1]))),
        float(np.max(np.abs(centers[:, 0] - centers[:, 1]))),
        float(np.max(np.abs(relative[:, 0] - relative[:, 1]))),
        float(np.max(np.abs(radii[:, 0] - radii[:, 1]))),
        float(np.max(np.abs(work[:, :2]))),
        float(np.max(np.abs(center_work[:, :2]))),
    )
    return PairedForceWorkResponse(
        sample_times=case.alpha * np.arange(n_steps + 1, dtype=float),
        impulse_fractions=fractions,
        impulse_amplitudes=impulses,
        normalized_force_profile=profile,
        integrated_impulses=case.alpha * float(np.sum(profile)) * impulses,
        position_responses=position_response,
        center_responses=center_response,
        relative_responses=relative_response,
        position_even_leakage=position_even,
        relative_even_leakage=relative_even,
        memory_radii=radii,
        branch_cumulative_work=branch_work,
        paired_even_cumulative_work=paired_work,
        branch_center_cumulative_work=branch_center_work,
        paired_even_center_cumulative_work=paired_center_work,
        control_positions=positions[:, 0],
        control_centers=centers[:, 0],
        control_relative=relative[:, 0],
        force_off_maximum_residual=off_residual,
    )


def finite_h_force_work_response(
    case: ScalarContinuumCase,
    *,
    normalized_force_profile: Iterable[float],
) -> dict[str, np.ndarray | float]:
    """Return the exact finite-``H`` linear response and native work ledger."""

    force = np.asarray(list(normalized_force_profile), dtype=float)
    if force.ndim != 1 or force.size < 2 or not np.isfinite(force).all():
        raise ValueError("normalized_force_profile must be a finite vector")
    n_steps = int(force.size)
    history = np.zeros(case.horizon, dtype=float)
    head = 0
    x = 0.0
    center = 0.0
    positions = np.empty(n_steps + 1, dtype=float)
    centers = np.empty(n_steps + 1, dtype=float)
    relative = np.empty(n_steps + 1, dtype=float)
    cumulative_work = np.empty(n_steps + 1, dtype=float)
    cumulative_x_dissipation = np.empty(n_steps + 1, dtype=float)
    cumulative_center_dissipation = np.empty(n_steps + 1, dtype=float)
    storage = np.empty(n_steps + 1, dtype=float)
    center_port_cumulative_work = np.empty(n_steps + 1, dtype=float)
    center_port_cumulative_dissipation = np.empty(n_steps + 1, dtype=float)
    center_port_kinetic_storage = np.empty(n_steps + 1, dtype=float)
    positions[0] = x
    centers[0] = center
    relative[0] = x - center
    cumulative_work[0] = 0.0
    cumulative_x_dissipation[0] = 0.0
    cumulative_center_dissipation[0] = 0.0
    storage[0] = 0.0
    center_port_cumulative_work[0] = 0.0
    center_port_cumulative_dissipation[0] = 0.0
    center_port_kinetic_storage[0] = 0.0

    for step in range(n_steps):
        relative_old = x - center
        displacement = case.alpha * force[step]
        x_next = (1.0 - case.restoring_per_update) * x
        x_next += case.restoring_per_update * center + displacement
        oldest = history[(head + case.horizon - 1) % case.horizon]
        center_next = case.q * center
        center_next += case.centroid_deposition_fraction * x_next
        center_next -= (
            case.centroid_deposition_fraction
            * case.tail_mass_fraction
            * oldest
        )
        delta_x = x_next - x
        delta_center = center_next - center
        head = (head - 1) % case.horizon
        history[head] = x_next
        x = x_next
        center = center_next
        positions[step + 1] = x
        centers[step + 1] = center
        relative[step + 1] = x - center
        relative_new = relative[step + 1]
        cumulative_work[step + 1] = (
            cumulative_work[step] + force[step] * delta_x
        )
        cumulative_x_dissipation[step + 1] = (
            cumulative_x_dissipation[step]
            + delta_x * delta_x / case.alpha
        )
        cumulative_center_dissipation[step + 1] = (
            cumulative_center_dissipation[step]
            + case.restoring_per_memory_time
            * delta_center
            * delta_center
            / case.alpha
        )
        storage[step + 1] = (
            0.5
            * case.restoring_per_memory_time
            * relative_new
            * relative_new
        )
        center_port_cumulative_work[step + 1] = (
            center_port_cumulative_work[step] + force[step] * delta_center
        )
        center_port_cumulative_dissipation[step + 1] = (
            center_port_cumulative_dissipation[step]
            + case.continuum_relative_rate
            * case.alpha
            * 0.5
            * (relative_old * relative_old + relative_new * relative_new)
        )
        center_port_kinetic_storage[step + 1] = 0.5 * relative_new * relative_new

    trace = (
        1.0
        - case.restoring_per_update
        + case.q
        + case.restoring_per_update * case.centroid_deposition_fraction
    )
    determinant = case.q * (1.0 - case.restoring_per_update)
    tail_coefficient = (
        case.restoring_per_update
        * case.centroid_deposition_fraction
        * case.tail_mass_fraction
    )
    applied_displacement = case.alpha * force
    recurrence_residual: list[float] = []
    for n in range(1, n_steps):
        delayed = positions[n - case.horizon] if n > case.horizon else 0.0
        value = positions[n + 1] - trace * positions[n]
        value += determinant * positions[n - 1] + tail_coefficient * delayed
        value -= applied_displacement[n] - case.q * applied_displacement[n - 1]
        recurrence_residual.append(value)
    maximum_residual = max((abs(value) for value in recurrence_residual), default=0.0)
    ledger_residual = (
        storage
        - storage[0]
        - cumulative_work
        + cumulative_x_dissipation
        + cumulative_center_dissipation
    )
    center_port_ledger_residual = (
        center_port_kinetic_storage
        - center_port_kinetic_storage[0]
        - center_port_cumulative_work
        + center_port_cumulative_dissipation
    )
    return {
        "sample_times": case.alpha * np.arange(n_steps + 1, dtype=float),
        "positions": positions,
        "centers": centers,
        "relative": relative,
        "cumulative_work": cumulative_work,
        "cumulative_x_dissipation": cumulative_x_dissipation,
        "cumulative_center_dissipation": cumulative_center_dissipation,
        "storage": storage,
        "ledger_residual": ledger_residual,
        "center_port_cumulative_work": center_port_cumulative_work,
        "center_port_cumulative_dissipation": center_port_cumulative_dissipation,
        "center_port_kinetic_storage": center_port_kinetic_storage,
        "center_port_ledger_residual": center_port_ledger_residual,
        "maximum_recurrence_residual": float(maximum_residual),
    }


def continuum_unit_impulse_response(
    case: ScalarContinuumCase,
    *,
    sample_times: Iterable[float],
) -> dict[str, np.ndarray]:
    """Return the registered continuum response to one native-step impulse."""

    times = np.asarray(list(sample_times), dtype=float)
    if (
        times.ndim != 1
        or times.size < 2
        or not np.isfinite(times).all()
        or np.any(times < 0.0)
        or not np.all(np.diff(times) > 0.0)
    ):
        raise ValueError("sample_times must be finite and strictly increasing")
    position = np.zeros_like(times)
    center = np.zeros_like(times)
    relative = np.zeros_like(times)
    mask = times >= case.alpha - 1.0e-14
    shifted = np.maximum(times[mask] - case.alpha, 0.0)
    decay = np.exp(-case.continuum_relative_rate * shifted)
    rate = case.continuum_relative_rate
    chi = case.restoring_per_memory_time
    position[mask] = (1.0 + chi * decay) / rate
    center[mask] = (1.0 - decay) / rate
    relative[mask] = decay
    return {"positions": position, "centers": center, "relative": relative}


def continuum_rectangular_force_response(
    case: ScalarContinuumCase,
    *,
    sample_times: Iterable[float],
    pulse_width: float,
) -> dict[str, np.ndarray]:
    """Return the local continuum response to a unit-area rectangular force."""

    times = np.asarray(list(sample_times), dtype=float)
    width = _positive_finite("pulse_width", pulse_width)
    if (
        times.ndim != 1
        or times.size < 2
        or not np.isfinite(times).all()
        or np.any(times < 0.0)
        or not np.all(np.diff(times) > 0.0)
    ):
        raise ValueError("sample_times must be finite and strictly increasing")

    gamma = case.continuum_relative_rate
    relative = np.empty_like(times)
    center = np.empty_like(times)
    inside = times <= width + 1.0e-14
    inside_times = np.minimum(times[inside], width)
    inside_decay = np.exp(-gamma * inside_times)
    relative[inside] = (1.0 - inside_decay) / (gamma * width)
    center[inside] = (
        inside_times / gamma
        - (1.0 - inside_decay) / gamma**2
    ) / width

    z = gamma * width
    end_relative = (1.0 - math.exp(-z)) / z
    end_center = width * (z - 1.0 + math.exp(-z)) / z**2
    after = ~inside
    shifted = times[after] - width
    after_decay = np.exp(-gamma * shifted)
    relative[after] = end_relative * after_decay
    center[after] = (
        end_center + end_relative * (1.0 - after_decay) / gamma
    )

    center_work = np.empty_like(times)
    center_work[inside] = center[inside] / width
    center_work[after] = end_center / width
    kinetic = 0.5 * relative * relative
    dissipation = center_work - kinetic
    return {
        "positions": center + relative,
        "centers": center,
        "relative": relative,
        "center_cumulative_work": center_work,
        "center_kinetic_storage": kinetic,
        "center_cumulative_dissipation": dissipation,
    }


def stationary_center_msd(
    case: ScalarContinuumCase,
    *,
    dim: int,
    n_paths: int,
    n_steps: int,
    seed: int,
) -> StationaryCenterMSD:
    """Simulate stationary local center increments and exact references."""

    if isinstance(dim, bool) or not isinstance(dim, (int, np.integer)) or dim < 1:
        raise ValueError("dim must be a positive integer")
    if (
        isinstance(n_paths, bool)
        or not isinstance(n_paths, (int, np.integer))
        or n_paths < 1
    ):
        raise ValueError("n_paths must be a positive integer")
    if (
        isinstance(n_steps, bool)
        or not isinstance(n_steps, (int, np.integer))
        or n_steps < 2
    ):
        raise ValueError("n_steps must be an integer at least two")
    if case.q <= 0.0:
        raise ValueError("stationary center MSD requires alpha below one")

    rng = np.random.default_rng(int(seed))
    relative_variance = (
        (case.q * case.epsilon) ** 2
        / (1.0 - case.untruncated_relative_root**2)
    )
    relative = rng.standard_normal((int(n_paths), int(dim))) * math.sqrt(
        relative_variance
    )
    center = np.zeros_like(relative)
    simulated = np.zeros(int(n_steps) + 1, dtype=float)
    for step in range(int(n_steps)):
        noise = rng.standard_normal(relative.shape)
        relative = (
            case.untruncated_relative_root * relative
            + case.q * case.epsilon * noise
        )
        center += case.alpha * relative / case.q
        simulated[step + 1] = float(np.mean(np.sum(center * center, axis=1)))

    covariance = np.array(
        [[0.0, 0.0], [0.0, relative_variance]], dtype=float
    )
    transition = np.array(
        [
            [
                1.0,
                case.alpha * case.untruncated_relative_root / case.q,
            ],
            [0.0, case.untruncated_relative_root],
        ],
        dtype=float,
    )
    noise_vector = np.array(
        [case.alpha * case.epsilon, case.q * case.epsilon], dtype=float
    )
    exact_discrete = np.zeros(int(n_steps) + 1, dtype=float)
    for step in range(int(n_steps)):
        covariance = (
            transition @ covariance @ transition.T
            + np.outer(noise_vector, noise_vector)
        )
        exact_discrete[step + 1] = int(dim) * covariance[0, 0]

    times = case.alpha * np.arange(int(n_steps) + 1, dtype=float)
    gamma = case.continuum_relative_rate
    continuum_per_dim = (
        2.0
        * case.diffusion_per_memory_time
        / gamma**3
        * (gamma * times - 1.0 + np.exp(-gamma * times))
    )
    return StationaryCenterMSD(
        sample_times=times,
        simulated_msd=simulated,
        exact_discrete_msd=exact_discrete,
        continuum_msd=int(dim) * continuum_per_dim,
        n_paths=int(n_paths),
        seed=int(seed),
    )


def stationary_visible_msd(
    case: ScalarContinuumCase,
    *,
    dim: int,
    n_paths: int,
    n_steps: int,
    seed: int,
) -> StationaryVisibleMSD:
    """Simulate stationary local visible increments and return exact references."""

    if isinstance(dim, bool) or not isinstance(dim, (int, np.integer)) or dim < 1:
        raise ValueError("dim must be a positive integer")
    if (
        isinstance(n_paths, bool)
        or not isinstance(n_paths, (int, np.integer))
        or n_paths < 1
    ):
        raise ValueError("n_paths must be a positive integer")
    if (
        isinstance(n_steps, bool)
        or not isinstance(n_steps, (int, np.integer))
        or n_steps < 2
    ):
        raise ValueError("n_steps must be an integer at least two")

    rng = np.random.default_rng(int(seed))
    relative_variance = (
        (case.q * case.epsilon) ** 2
        / (1.0 - case.untruncated_relative_root**2)
    )
    relative = rng.standard_normal((int(n_paths), int(dim))) * math.sqrt(
        relative_variance
    )
    position = np.zeros_like(relative)
    simulated = np.zeros(int(n_steps) + 1, dtype=float)
    for step in range(int(n_steps)):
        noise = rng.standard_normal(relative.shape)
        position += -case.restoring_per_update * relative + case.epsilon * noise
        relative = (
            case.untruncated_relative_root * relative
            + case.q * case.epsilon * noise
        )
        simulated[step + 1] = float(np.mean(np.sum(position * position, axis=1)))

    covariance = np.array(
        [[0.0, 0.0], [0.0, relative_variance]], dtype=float
    )
    transition = np.array(
        [
            [1.0, -case.restoring_per_update],
            [0.0, case.untruncated_relative_root],
        ],
        dtype=float,
    )
    noise_vector = np.array([case.epsilon, case.q * case.epsilon], dtype=float)
    exact_discrete = np.zeros(int(n_steps) + 1, dtype=float)
    for step in range(int(n_steps)):
        covariance = (
            transition @ covariance @ transition.T
            + np.outer(noise_vector, noise_vector)
        )
        exact_discrete[step + 1] = int(dim) * covariance[0, 0]

    times = case.alpha * np.arange(int(n_steps) + 1, dtype=float)
    gamma = case.continuum_relative_rate
    chi = case.restoring_per_memory_time
    decay = 1.0 - np.exp(-gamma * times)
    continuum_per_dim = (
        case.diffusion_per_memory_time * chi * chi / gamma**3 * decay * decay
    )
    continuum_per_dim += 2.0 * case.diffusion_per_memory_time / gamma**2 * (
        times
        + 2.0 * chi / gamma * decay
        + chi * chi / (2.0 * gamma) * (1.0 - np.exp(-2.0 * gamma * times))
    )
    return StationaryVisibleMSD(
        sample_times=times,
        simulated_msd=simulated,
        exact_discrete_msd=exact_discrete,
        continuum_msd=int(dim) * continuum_per_dim,
        n_paths=int(n_paths),
        seed=int(seed),
    )
