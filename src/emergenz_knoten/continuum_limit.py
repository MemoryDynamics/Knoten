"""Matched small-step diagnostics for the scalar finite-memory model."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

import numpy as np

try:
    from numba import njit
except ImportError:  # pragma: no cover

    def njit(*args, **kwargs):
        def wrapper(func):
            return func

        return wrapper


@dataclass(frozen=True)
class ScalarContinuumCase:
    """One finite-step member of a matched scalar-memory continuum family."""

    alpha: float
    tail_extent: float
    horizon: int
    q: float
    tail_mass_fraction: float
    stored_memory_mass: float
    local_curvature: float
    restoring_per_memory_time: float
    diffusion_per_memory_time: float
    restoring_per_update: float
    eta: float
    epsilon: float
    centroid_deposition_fraction: float
    finite_relative_root: float
    finite_relative_rate: float
    untruncated_relative_root: float
    untruncated_relative_rate: float
    continuum_relative_rate: float
    continuum_rms_radius: float
    untruncated_discrete_rms_radius: float


@dataclass(frozen=True)
class PairedContinuumResponse:
    """Common-noise mirrored response from a complete finite-memory state."""

    sample_times: np.ndarray
    offset_fractions: np.ndarray
    offset_amplitudes: np.ndarray
    relative_responses: np.ndarray
    drift_responses: np.ndarray
    relative_even_leakage: np.ndarray
    initial_control_radius: float
    final_control_radius: float


def _positive_finite(name: str, value: float) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be positive and finite")
    return number


def matched_scalar_continuum_case(
    *,
    alpha: float,
    tail_extent: float,
    restoring_per_memory_time: float,
    diffusion_per_memory_time: float,
    dim: int,
    memory_mass: float = 1.0,
    sigma_rep: float = 1.0,
    sigma_att: float = 3.0,
    amplitude_rep: float = 1.0,
    amplitude_att: float = 35.0,
) -> ScalarContinuumCase:
    """Return a finite-step case with fixed ``chi``, ``D``, and tail extent.

    The horizon is ``ceil(C/alpha)``.  ``eta`` and ``epsilon`` are then chosen
    so that ``g_H/alpha=chi`` and ``epsilon**2/(2*alpha)=D`` exactly for the
    retained finite memory mass.
    """

    alpha_value = _positive_finite("alpha", alpha)
    if alpha_value >= 1.0:
        raise ValueError("alpha must be smaller than one")
    extent = _positive_finite("tail_extent", tail_extent)
    chi = _positive_finite(
        "restoring_per_memory_time", restoring_per_memory_time
    )
    diffusion = _positive_finite(
        "diffusion_per_memory_time", diffusion_per_memory_time
    )
    mass = _positive_finite("memory_mass", memory_mass)
    rep_sigma = _positive_finite("sigma_rep", sigma_rep)
    att_sigma = _positive_finite("sigma_att", sigma_att)
    if isinstance(dim, bool) or not isinstance(dim, (int, np.integer)) or dim < 1:
        raise ValueError("dim must be a positive integer")
    for name, value in (
        ("amplitude_rep", amplitude_rep),
        ("amplitude_att", amplitude_att),
    ):
        if not math.isfinite(float(value)):
            raise ValueError(f"{name} must be finite")

    horizon = max(1, int(math.ceil(extent / alpha_value - 1.0e-12)))
    q = 1.0 - alpha_value
    tail = q**horizon
    stored_mass = mass * (1.0 - tail)
    curvature = float(amplitude_att) / att_sigma**2 - float(
        amplitude_rep
    ) / rep_sigma**2
    if curvature <= 0.0:
        raise ValueError("the matched continuum case requires positive curvature")

    g = chi * alpha_value
    eta = g / (stored_mass * curvature)
    epsilon = math.sqrt(2.0 * diffusion * alpha_value)
    untruncated_root = q * (1.0 - g)
    if not 0.0 < untruncated_root < 1.0:
        raise ValueError("the registered relative root must lie strictly in (0, 1)")

    centroid_fraction = alpha_value / (1.0 - tail)
    trace = 1.0 - g + q + g * centroid_fraction
    determinant = q * (1.0 - g)
    discriminant = trace * trace - 4.0 * determinant
    if discriminant < 0.0:
        raise ValueError("finite-horizon response roots must be real")
    root_minus = 0.5 * (trace - math.sqrt(discriminant))
    root_plus = 0.5 * (trace + math.sqrt(discriminant))
    finite_root = min(
        (root_minus, root_plus), key=lambda root: abs(root - untruncated_root)
    )
    if not 0.0 < finite_root < 1.0:
        raise ValueError("finite relative response root must lie strictly in (0, 1)")

    continuum_rate = 1.0 + chi
    continuum_radius = math.sqrt(dim * diffusion / continuum_rate)
    discrete_radius = (
        math.sqrt(dim)
        * q
        * epsilon
        / math.sqrt(1.0 - untruncated_root * untruncated_root)
    )
    return ScalarContinuumCase(
        alpha=alpha_value,
        tail_extent=extent,
        horizon=horizon,
        q=q,
        tail_mass_fraction=tail,
        stored_memory_mass=stored_mass,
        local_curvature=curvature,
        restoring_per_memory_time=chi,
        diffusion_per_memory_time=diffusion,
        restoring_per_update=g,
        eta=eta,
        epsilon=epsilon,
        centroid_deposition_fraction=centroid_fraction,
        finite_relative_root=float(finite_root),
        finite_relative_rate=float(-math.log(finite_root) / alpha_value),
        untruncated_relative_root=float(untruncated_root),
        untruncated_relative_rate=float(
            -math.log(untruncated_root) / alpha_value
        ),
        continuum_relative_rate=float(continuum_rate),
        continuum_rms_radius=float(continuum_radius),
        untruncated_discrete_rms_radius=float(discrete_radius),
    )


def aggregate_standard_normal_increments(
    fine_noise: Iterable[Iterable[float]], ratio: int
) -> np.ndarray:
    """Aggregate standard normals into exact coarser Brownian increments."""

    values = np.asarray(fine_noise, dtype=float)
    if values.ndim != 2 or values.shape[0] < 1 or not np.isfinite(values).all():
        raise ValueError("fine_noise must be a non-empty finite matrix")
    if isinstance(ratio, bool) or not isinstance(ratio, (int, np.integer)):
        raise ValueError("ratio must be an integer")
    ratio_value = int(ratio)
    if ratio_value < 1 or values.shape[0] % ratio_value != 0:
        raise ValueError("ratio must divide the fine-noise length")
    reshaped = values.reshape(values.shape[0] // ratio_value, ratio_value, -1)
    return np.sum(reshaped, axis=1) / math.sqrt(ratio_value)


def finite_h_linear_response(
    case: ScalarContinuumCase, *, response_steps: int
) -> dict[str, np.ndarray | float]:
    """Return the exact finite-``H`` response to ``x_0-c_0=1``.

    The retained pre-intervention history has zero response.  This is the
    linear reference for a visible-coordinate displacement that leaves memory
    untouched.
    """

    if (
        isinstance(response_steps, bool)
        or not isinstance(response_steps, (int, np.integer))
        or response_steps < 1
    ):
        raise ValueError("response_steps must be a positive integer")
    n_steps = int(response_steps)
    history = np.zeros(case.horizon, dtype=float)
    head = 0
    x = 1.0
    center = 0.0
    positions = np.empty(n_steps + 1, dtype=float)
    centers = np.empty(n_steps + 1, dtype=float)
    relative = np.empty(n_steps + 1, dtype=float)
    positions[0] = x
    centers[0] = center
    relative[0] = x - center

    for step in range(n_steps):
        x_next = (1.0 - case.restoring_per_update) * x
        x_next += case.restoring_per_update * center
        oldest = history[(head + case.horizon - 1) % case.horizon]
        center_next = case.q * center
        center_next += case.centroid_deposition_fraction * x_next
        center_next -= (
            case.centroid_deposition_fraction
            * case.tail_mass_fraction
            * oldest
        )
        head = (head - 1) % case.horizon
        history[head] = x_next
        x = x_next
        center = center_next
        positions[step + 1] = x
        centers[step + 1] = center
        relative[step + 1] = x - center

    coefficient = np.empty(n_steps, dtype=float)
    coefficient[:] = np.nan
    nonzero = np.abs(relative[:-1]) > 0.0
    coefficient[nonzero] = relative[1:][nonzero] / relative[:-1][nonzero]

    recurrence_residual = []
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
    for n in range(1, n_steps):
        # The visible displacement at response time zero is not deposited into
        # the pre-intervention memory.  The first non-zero dropped response is
        # therefore x_1 when n=H+1, not x_0 when n=H.
        delayed = positions[n - case.horizon] if n > case.horizon else 0.0
        value = positions[n + 1] - trace * positions[n]
        value += determinant * positions[n - 1] + tail_coefficient * delayed
        recurrence_residual.append(value)
    maximum_residual = max((abs(value) for value in recurrence_residual), default=0.0)
    return {
        "positions": positions,
        "centers": centers,
        "relative": relative,
        "step_coefficients": coefficient,
        "maximum_recurrence_residual": float(maximum_residual),
    }


@njit(cache=True)
def _path_gradient(
    x: np.ndarray,
    history: np.ndarray,
    head: int,
    filled: int,
    weights: np.ndarray,
    sigma_rep2: float,
    sigma_att2: float,
    amplitude_rep: float,
    amplitude_att: float,
) -> np.ndarray:
    dim = x.shape[0]
    horizon = history.shape[0]
    gradient = np.zeros(dim, np.float64)
    for age in range(filled):
        index = (head + age) % horizon
        radius2 = 0.0
        for coord in range(dim):
            delta = x[coord] - history[index, coord]
            radius2 += delta * delta
        rep = -amplitude_rep * np.exp(-0.5 * radius2 / sigma_rep2) / sigma_rep2
        att = -amplitude_att * np.exp(-0.5 * radius2 / sigma_att2) / sigma_att2
        factor = weights[age] * (rep - att)
        for coord in range(dim):
            gradient[coord] += factor * (x[coord] - history[index, coord])
    return gradient


@njit(cache=True)
def _weighted_center_and_radius(
    history: np.ndarray,
    head: int,
    weights: np.ndarray,
    mass: float,
):
    dim = history.shape[1]
    horizon = history.shape[0]
    center = np.zeros(dim, np.float64)
    for age in range(horizon):
        index = (head + age) % horizon
        for coord in range(dim):
            center[coord] += weights[age] * history[index, coord]
    center /= mass
    radius2 = 0.0
    for age in range(horizon):
        index = (head + age) % horizon
        for coord in range(dim):
            delta = history[index, coord] - center[coord]
            radius2 += weights[age] * delta * delta / mass
    return center, np.sqrt(max(radius2, 0.0))


@njit(cache=True)
def _form_state(
    noise: np.ndarray,
    weights: np.ndarray,
    epsilon: float,
    eta: float,
    sigma_rep2: float,
    sigma_att2: float,
    amplitude_rep: float,
    amplitude_att: float,
):
    dim = noise.shape[1]
    horizon = weights.shape[0]
    x = np.zeros(dim, np.float64)
    history = np.zeros((horizon, dim), np.float64)
    head = 0
    filled = 0
    for step in range(noise.shape[0]):
        gradient = _path_gradient(
            x,
            history,
            head,
            filled,
            weights,
            sigma_rep2,
            sigma_att2,
            amplitude_rep,
            amplitude_att,
        )
        for coord in range(dim):
            x[coord] += epsilon * noise[step, coord] - eta * gradient[coord]
        if filled == 0:
            head = 0
        else:
            head = (head - 1) % horizon
        history[head] = x
        if filled < horizon:
            filled += 1
    return x, history, head, filled


@njit(cache=True)
def _paired_response(
    initial_x: np.ndarray,
    initial_history: np.ndarray,
    initial_head: int,
    weights: np.ndarray,
    noise: np.ndarray,
    offset_amplitudes: np.ndarray,
    axis: np.ndarray,
    alpha: float,
    epsilon: float,
    eta: float,
    sigma_rep2: float,
    sigma_att2: float,
    amplitude_rep: float,
    amplitude_att: float,
):
    n_offsets = offset_amplitudes.shape[0]
    n_paths = 1 + 2 * n_offsets
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
    for path in range(n_paths):
        xs[path] = initial_x
        histories[path] = initial_history
        heads[path] = initial_head
        centers[path] = base_center
    for offset in range(n_offsets):
        plus = 1 + 2 * offset
        minus = plus + 1
        for coord in range(dim):
            displacement = offset_amplitudes[offset] * axis[coord]
            xs[plus, coord] += displacement
            xs[minus, coord] -= displacement

    relative = np.empty((n_steps + 1, n_paths, dim), np.float64)
    drifts = np.empty((n_steps, n_paths, dim), np.float64)
    for path in range(n_paths):
        for coord in range(dim):
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
            oldest_index = (heads[path] + horizon - 1) % horizon
            oldest = histories[path, oldest_index].copy()
            for coord in range(dim):
                drift = -eta * gradient[coord]
                drifts[step, path, coord] = drift
                xs[path, coord] += epsilon * noise[step, coord] + drift
            for coord in range(dim):
                centers[path, coord] = (
                    q * centers[path, coord]
                    + deposition_fraction * xs[path, coord]
                    - deposition_fraction * tail * oldest[coord]
                )
            heads[path] = (heads[path] - 1) % horizon
            histories[path, heads[path]] = xs[path]
            for coord in range(dim):
                relative[step + 1, path, coord] = (
                    xs[path, coord] - centers[path, coord]
                )

    _, final_radius = _weighted_center_and_radius(
        histories[0], heads[0], weights, mass
    )
    return relative, drifts, initial_radius, final_radius


def simulate_matched_continuum_response(
    case: ScalarContinuumCase,
    *,
    formation_noise: Iterable[Iterable[float]],
    response_noise: Iterable[Iterable[float]],
    offset_fractions: Iterable[float],
    axis: Iterable[float],
    memory_mass: float = 1.0,
    sigma_rep: float = 1.0,
    sigma_att: float = 3.0,
    amplitude_rep: float = 1.0,
    amplitude_att: float = 35.0,
) -> PairedContinuumResponse:
    """Form one state and apply mirrored visible-coordinate displacements."""

    formation = np.asarray(formation_noise, dtype=float)
    response = np.asarray(response_noise, dtype=float)
    if (
        formation.ndim != 2
        or response.ndim != 2
        or formation.shape[1] != response.shape[1]
        or formation.shape[0] < case.horizon
        or response.shape[0] < 1
        or not np.isfinite(formation).all()
        or not np.isfinite(response).all()
    ):
        raise ValueError("formation and response noise must be compatible finite matrices")
    direction = np.asarray(axis, dtype=float)
    if direction.shape != (formation.shape[1],) or not np.isfinite(direction).all():
        raise ValueError("axis must match the noise dimension")
    direction_norm = float(np.linalg.norm(direction))
    if direction_norm <= 0.0:
        raise ValueError("axis must be non-zero")
    direction = direction / direction_norm
    fractions = np.asarray(list(offset_fractions), dtype=float)
    if (
        fractions.ndim != 1
        or fractions.size < 1
        or not np.isfinite(fractions).all()
        or np.any(fractions <= 0.0)
        or not np.array_equal(fractions, np.unique(fractions))
    ):
        raise ValueError("offset_fractions must be unique increasing positive values")
    mass = _positive_finite("memory_mass", memory_mass)
    amplitudes = fractions * case.continuum_rms_radius
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
    relative, drifts, initial_radius, final_radius = _paired_response(
        initial_x,
        initial_history,
        initial_head,
        weights,
        response,
        amplitudes,
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
    response_values = np.empty(
        (fractions.size, n_steps + 1, formation.shape[1]), dtype=float
    )
    drift_values = np.empty(
        (fractions.size, n_steps, formation.shape[1]), dtype=float
    )
    even_values = np.empty_like(response_values)
    for offset, amplitude in enumerate(amplitudes):
        plus = 1 + 2 * offset
        minus = plus + 1
        scale = 2.0 * amplitude
        response_values[offset] = (relative[:, plus] - relative[:, minus]) / scale
        drift_values[offset] = (drifts[:, plus] - drifts[:, minus]) / scale
        even_values[offset] = (
            relative[:, plus] + relative[:, minus] - 2.0 * relative[:, 0]
        ) / scale

    times = case.alpha * np.arange(n_steps + 1, dtype=float)
    return PairedContinuumResponse(
        sample_times=times,
        offset_fractions=fractions,
        offset_amplitudes=amplitudes,
        relative_responses=response_values,
        drift_responses=drift_values,
        relative_even_leakage=even_values,
        initial_control_radius=float(initial_radius),
        final_control_radius=float(final_radius),
    )
