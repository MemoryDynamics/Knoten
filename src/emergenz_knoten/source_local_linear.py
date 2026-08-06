"""Linear source-local emission and reciprocal-channel diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from scipy import linalg

from .local_mediator import LocalMediatorGrid, TelegraphMediator


@dataclass(frozen=True)
class LinearChannel:
    """Discrete scalar channel realization ``h' = F h + B s, y = C h``."""

    transition: np.ndarray
    source: np.ndarray
    readout: np.ndarray

    @property
    def order(self) -> int:
        return int(self.transition.shape[0])


@dataclass(frozen=True)
class PoleDiagnostic:
    """Best observable complex pole of one reciprocal linearization."""

    stable: bool
    eigenvector_condition: float
    multiplier: complex | None
    damping_per_memory_time: float | None
    frequency_per_memory_time: float | None
    normalized_knot_residue: float
    nearest_one_way_generator_distance_ratio: float | None
    passes: bool


def _interpolating_readout(
    grid: LocalMediatorGrid,
    readout_position: float,
) -> np.ndarray:
    coordinates = grid.coordinates
    position = float(readout_position)
    if not math.isfinite(position) or not coordinates[0] < position < coordinates[-1]:
        raise ValueError("readout_position must lie strictly inside the grid")
    floating = position / grid.spacing + grid.source_index
    left = int(math.floor(floating))
    fraction = floating - left
    if left < 1 or left + 1 >= grid.n_points - 1:
        raise ValueError("readout_position must use two interior grid points")
    result = np.zeros(2 * (grid.n_points - 2), dtype=float)
    result[left - 1] = 1.0 - fraction
    result[left] = fraction
    return result


def telegraph_channel_realization(
    grid: LocalMediatorGrid,
    mediator: TelegraphMediator,
    *,
    readout_position: float,
) -> LinearChannel:
    """Build the exact finite-grid update and normalize its DC readout to one."""

    interior = grid.n_points - 2
    laplacian = np.zeros((interior, interior), dtype=float)
    np.fill_diagonal(laplacian, -2.0)
    np.fill_diagonal(laplacian[1:], 1.0)
    np.fill_diagonal(laplacian[:, 1:], 1.0)
    generator = (
        mediator.wave_speed**2 / grid.spacing**2 * laplacian
        - mediator.natural_frequency**2 * np.eye(interior)
    )
    dt = grid.time_step
    momentum_from_field = dt * generator
    momentum_from_momentum = (
        1.0 - 2.0 * mediator.damping_rate * dt
    ) * np.eye(interior)
    transition = np.block(
        [
            [
                np.eye(interior) + dt * momentum_from_field,
                dt * momentum_from_momentum,
            ],
            [momentum_from_field, momentum_from_momentum],
        ]
    )
    point_source = np.zeros(interior, dtype=float)
    point_source[grid.source_index - 1] = 1.0 / grid.spacing
    raw_source = np.concatenate((dt * dt * point_source, dt * point_source))
    readout = _interpolating_readout(grid, readout_position)
    static_state = linalg.solve(
        np.eye(2 * interior) - transition,
        raw_source,
        assume_a="gen",
    )
    dc_gain = float(readout @ static_state)
    if not math.isfinite(dc_gain) or dc_gain <= 0.0:
        raise ValueError("channel DC gain must be positive and finite")
    source = raw_source / dc_gain
    return LinearChannel(transition=transition, source=source, readout=readout)



def reciprocal_source_local_matrix(
    channel: LinearChannel,
    *,
    lambda_value: float,
    self_gain: float,
    cross_gain: float,
    emission: str = "offset",
    coupling_sign: float = 1.0,
) -> np.ndarray:
    """Return the translation-free reciprocal relative-state matrix."""

    if not 0.0 < lambda_value < 1.0:
        raise ValueError("lambda_value must lie in (0, 1)")
    for name, value in (
        ("self_gain", self_gain),
        ("cross_gain", cross_gain),
        ("coupling_sign", coupling_sign),
    ):
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
    q = 1.0 - lambda_value
    local_multiplier = q * (1.0 - self_gain)
    feedback = coupling_sign * q * cross_gain
    transition = channel.transition
    source = channel.source
    readout = channel.readout

    if emission == "offset":
        matrix = np.zeros((1 + channel.order, 1 + channel.order), dtype=float)
        matrix[0, 0] = local_multiplier + feedback * float(readout @ source)
        matrix[0, 1:] = feedback * (readout @ transition)
        matrix[1:, 0] = source
        matrix[1:, 1:] = transition
        return matrix
    if emission == "current":
        matrix = np.zeros((2 + channel.order, 2 + channel.order), dtype=float)
        source_now = source / q
        source_previous = -source
        matrix[0, 0] = local_multiplier + feedback * float(readout @ source_now)
        matrix[0, 1] = feedback * float(readout @ source_previous)
        matrix[0, 2:] = feedback * (readout @ transition)
        matrix[1, 0] = 1.0
        matrix[2:, 0] = source_now
        matrix[2:, 1] = source_previous
        matrix[2:, 2:] = transition
        return matrix
    if emission == "mass":
        return np.asarray([[local_multiplier]], dtype=float)
    raise ValueError("emission must be 'mass', 'offset', or 'current'")


def _generators(values: np.ndarray, lambda_value: float) -> np.ndarray:
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.log(np.asarray(values, dtype=np.complex128)) / lambda_value


def diagnose_reciprocal_poles(
    matrix: np.ndarray,
    one_way_channel: LinearChannel,
    *,
    lambda_value: float,
    frequency_min: float = 0.05,
    residue_min: float = 0.1,
    shift_ratio_min: float = 0.1,
    condition_max: float = 1.0e8,
) -> PoleDiagnostic:
    """Evaluate stability, knot residue, and separation from channel poles."""

    eigenvalues, eigenvectors = linalg.eig(matrix)
    condition = float(np.linalg.cond(eigenvectors))
    stable = bool(np.max(np.abs(eigenvalues)) < 1.0)
    if not math.isfinite(condition) or condition > condition_max:
        return PoleDiagnostic(
            stable=stable,
            eigenvector_condition=condition,
            multiplier=None,
            damping_per_memory_time=None,
            frequency_per_memory_time=None,
            normalized_knot_residue=0.0,
            nearest_one_way_generator_distance_ratio=None,
            passes=False,
        )

    inverse = linalg.inv(eigenvectors)
    residues = eigenvectors[0, :] * inverse[:, 0]
    denominator = float(np.sum(np.abs(residues)))
    channel_values = linalg.eigvals(one_way_channel.transition)
    channel_generators = _generators(channel_values, lambda_value)
    best: tuple[float, complex, float, float, float] | None = None
    generators = _generators(eigenvalues, lambda_value)
    for index, (value, generator) in enumerate(zip(eigenvalues, generators, strict=True)):
        if value.imag <= 1.0e-10 or abs(value) >= 1.0:
            continue
        frequency = float(abs(generator.imag))
        if frequency < frequency_min:
            continue
        pair_residue = 0.0 if denominator == 0.0 else 2.0 * abs(residues[index]) / denominator
        nearest = float(np.min(np.abs(channel_generators - generator)))
        scale = max(float(abs(generator)), frequency_min)
        shift_ratio = nearest / scale
        score = pair_residue * shift_ratio
        candidate = (score, complex(value), pair_residue, shift_ratio, frequency)
        if best is None or candidate[0] > best[0]:
            best = candidate
    if best is None:
        return PoleDiagnostic(
            stable=stable,
            eigenvector_condition=condition,
            multiplier=None,
            damping_per_memory_time=None,
            frequency_per_memory_time=None,
            normalized_knot_residue=0.0,
            nearest_one_way_generator_distance_ratio=None,
            passes=False,
        )
    _, multiplier, residue, shift_ratio, frequency = best
    damping = float(-math.log(abs(multiplier)) / lambda_value)
    passes = bool(
        stable
        and residue >= residue_min
        and shift_ratio >= shift_ratio_min
        and frequency >= frequency_min
    )
    return PoleDiagnostic(
        stable=stable,
        eigenvector_condition=condition,
        multiplier=multiplier,
        damping_per_memory_time=damping,
        frequency_per_memory_time=frequency,
        normalized_knot_residue=float(residue),
        nearest_one_way_generator_distance_ratio=float(shift_ratio),
        passes=passes,
    )

