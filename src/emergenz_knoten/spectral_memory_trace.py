"""Fast, controlled traces for scalar spectral-memory diagnostics.

The Fourier coefficients remain a representation of the scalar memory field.
Recent positions are retained only when a direct real-space history check is
requested; they are not part of the simulated Markov state.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

from numba import njit
import numpy as np

from .spectral_memory_field import SpectralMemoryConfig, kernel_transfer, wavenumbers


@dataclass(frozen=True)
class SpectralMemoryTrace:
    """Sampled translation-invariant observables and final field state."""

    values: np.ndarray
    feature_names: tuple[str, ...]
    final_x: float
    final_rho_coefficients: np.ndarray
    recent_positions_newest_first: np.ndarray
    update_count: int


def low_mode_feature_names(
    n_low_modes: int,
    real_offsets: Sequence[float],
) -> tuple[str, ...]:
    """Names for kinematics, phase-aligned modes, and real-space samples."""

    if n_low_modes < 1:
        raise ValueError("n_low_modes must be positive")
    names = ["relative_x", "force"]
    for mode in range(1, n_low_modes + 1):
        names.extend((f"mode_{mode}_real", f"mode_{mode}_imag"))
    for index, _ in enumerate(real_offsets):
        names.extend((f"rho_even_{index}", f"rho_odd_{index}"))
    return tuple(names)


def low_mode_feature_groups(
    n_low_modes: int,
    real_offsets: Sequence[float],
) -> dict[str, list[int]]:
    """Return comparable feature groups for closure and representation checks."""

    names = low_mode_feature_names(n_low_modes, real_offsets)
    mode_end = 2 + 2 * n_low_modes
    return {
        "kinematic": [0, 1],
        "low_modes": list(range(mode_end)),
        "real_space": [0, 1, *range(mode_end, len(names))],
        "combined": list(range(len(names))),
    }


@njit(cache=True)
def _periodic_displacement_numba(x: float, origin: float, length: float) -> float:
    return (x - origin + 0.5 * length) % length - 0.5 * length


@njit(cache=True)
def _gradient_numba(
    rho: np.ndarray,
    k: np.ndarray,
    transfer: np.ndarray,
    x: float,
) -> float:
    total = 0.0
    for mode in range(1, rho.size):
        phase = np.exp(1j * k[mode] * x)
        total += 2.0 * (1j * k[mode] * transfer[mode] * rho[mode] * phase).real
    return total


@njit(cache=True)
def _simulate_trace_numba(
    noise: np.ndarray,
    box_length: float,
    lambda_value: float,
    memory_mass: float,
    epsilon: float,
    eta: float,
    burn_in: int,
    sample_every: int,
    n_low_modes: int,
    real_offsets: np.ndarray,
    k: np.ndarray,
    transfer: np.ndarray,
    smoothing: np.ndarray,
    heat_transfer: np.ndarray,
    history_length: int,
) -> tuple[np.ndarray, float, np.ndarray, np.ndarray]:
    steps = noise.size
    n_samples = steps // sample_every - burn_in // sample_every
    n_features = 2 + 2 * n_low_modes + 2 * real_offsets.size
    trace = np.empty((n_samples, n_features), dtype=np.float64)
    history_capacity = min(history_length, steps)
    history_ring = np.empty(history_capacity, dtype=np.float64)

    x = 0.5 * box_length
    base = memory_mass / box_length
    rho = np.empty(k.size, dtype=np.complex128)
    for mode in range(k.size):
        rho[mode] = base * smoothing[mode] * np.exp(-1j * k[mode] * x)
    rho[0] = base + 0.0j

    sample_index = 0
    q = 1.0 - lambda_value
    for update_index in range(1, steps + 1):
        gradient = _gradient_numba(rho, k, transfer, x)
        x = (x + epsilon * noise[update_index - 1] - eta * gradient) % box_length
        for mode in range(k.size):
            deposited = base * smoothing[mode] * np.exp(-1j * k[mode] * x)
            rho[mode] = heat_transfer[mode] * (
                q * rho[mode] + lambda_value * deposited
            )
        rho[0] = base + 0.0j
        if history_capacity > 0:
            history_ring[(update_index - 1) % history_capacity] = x

        if update_index > burn_in and update_index % sample_every == 0:
            center = (-np.angle(rho[1]) / k[1]) % box_length
            trace[sample_index, 0] = _periodic_displacement_numba(
                x, center, box_length
            )
            trace[sample_index, 1] = _gradient_numba(rho, k, transfer, x)
            column = 2
            for mode in range(1, n_low_modes + 1):
                aligned = rho[mode] * np.exp(1j * k[mode] * center) / base
                trace[sample_index, column] = aligned.real
                trace[sample_index, column + 1] = aligned.imag
                column += 2
            for offset in real_offsets:
                plus = rho[0].real
                minus = rho[0].real
                for mode in range(1, rho.size):
                    plus += 2.0 * (
                        rho[mode]
                        * np.exp(1j * k[mode] * ((center + offset) % box_length))
                    ).real
                    minus += 2.0 * (
                        rho[mode]
                        * np.exp(1j * k[mode] * ((center - offset) % box_length))
                    ).real
                trace[sample_index, column] = 0.5 * (plus + minus) / base
                trace[sample_index, column + 1] = 0.5 * (plus - minus) / base
                column += 2
            sample_index += 1

    history_count = min(history_capacity, steps)
    recent = np.empty(history_count, dtype=np.float64)
    for age in range(history_count):
        recent[age] = history_ring[(steps - 1 - age) % history_capacity]
    return trace, x, rho, recent


def simulate_spectral_memory_trace(
    config: SpectralMemoryConfig,
    *,
    noise: np.ndarray,
    diffusion_per_update: float,
    epsilon: float,
    eta: float,
    burn_in: int,
    sample_every: int,
    n_low_modes: int = 3,
    real_offsets: Sequence[float] = (0.0, 1.5, 3.0, 6.0),
    history_length: int = 0,
) -> SpectralMemoryTrace:
    """Simulate paired-noise low-mode and reconstructed-real-space traces."""

    noise_values = np.asarray(noise, dtype=np.float64)
    if noise_values.ndim != 1 or noise_values.size < 1:
        raise ValueError("noise must be a non-empty one-dimensional array")
    if not np.isfinite(noise_values).all():
        raise ValueError("noise must be finite")
    if config.memory_mass <= 0.0:
        raise ValueError(
            "positive memory_mass is required for normalized low-mode features"
        )
    if not math.isfinite(diffusion_per_update) or diffusion_per_update < 0.0:
        raise ValueError("diffusion_per_update must be non-negative and finite")
    for name, value in (("epsilon", epsilon), ("eta", eta)):
        if not math.isfinite(value) or value < 0.0:
            raise ValueError(f"{name} must be non-negative and finite")
    if burn_in < 0 or burn_in >= noise_values.size:
        raise ValueError("burn_in must satisfy 0 <= burn_in < number of updates")
    if sample_every < 1:
        raise ValueError("sample_every must be positive")
    if n_low_modes < 1 or n_low_modes > config.n_modes:
        raise ValueError("n_low_modes must lie between one and config.n_modes")
    offsets = np.asarray(tuple(real_offsets), dtype=np.float64)
    if offsets.ndim != 1 or not np.isfinite(offsets).all():
        raise ValueError("real_offsets must be a finite one-dimensional sequence")
    if np.any(offsets < 0.0) or np.any(offsets > 0.5 * config.box_length):
        raise ValueError("real_offsets must lie in [0, box_length/2]")
    if history_length < 0:
        raise ValueError("history_length must be non-negative")

    k = wavenumbers(config)
    smoothing = np.exp(-0.5 * config.deposition_sigma**2 * k**2)
    heat = np.exp(-float(diffusion_per_update) * k**2)
    values, final_x, final_rho, recent = _simulate_trace_numba(
        noise_values,
        float(config.box_length),
        float(config.lambda_value),
        float(config.memory_mass),
        float(epsilon),
        float(eta),
        int(burn_in),
        int(sample_every),
        int(n_low_modes),
        offsets,
        k,
        kernel_transfer(config),
        smoothing,
        heat,
        int(history_length),
    )
    return SpectralMemoryTrace(
        values=values,
        feature_names=low_mode_feature_names(n_low_modes, offsets),
        final_x=float(final_x),
        final_rho_coefficients=np.asarray(final_rho, dtype=np.complex128),
        recent_positions_newest_first=np.asarray(recent, dtype=float),
        update_count=int(noise_values.size),
    )


def direct_history_potential_gradient(
    config: SpectralMemoryConfig,
    *,
    evaluation_x: float,
    initial_x: float,
    recent_positions_newest_first: Sequence[float],
    total_updates: int,
    diffusion_per_update: float,
    periodic_images: int = 3,
) -> float:
    """Approximate the final gradient directly from retained real-space history.

    The omitted deposition weight is bounded by the geometric tail.
    Gaussian deposition and heat diffusion are folded into each kernel width.
    """

    if total_updates < 0 or periodic_images < 0:
        raise ValueError("total_updates and periodic_images must be non-negative")
    if not math.isfinite(diffusion_per_update) or diffusion_per_update < 0.0:
        raise ValueError("diffusion_per_update must be non-negative and finite")
    positions = np.asarray(recent_positions_newest_first, dtype=float)
    if positions.ndim != 1 or not np.isfinite(positions).all():
        raise ValueError("recent positions must be a finite one-dimensional array")
    if positions.size > total_updates:
        raise ValueError("recent positions cannot exceed total_updates")
    q = 1.0 - config.lambda_value

    def source_gradient(source_x: float, weight: float, heat_steps: int) -> float:
        total = 0.0
        for term in config.kernel:
            variance = (
                term.sigma**2
                + config.deposition_sigma**2
                + 2.0 * diffusion_per_update * heat_steps
            )
            sigma_effective = math.sqrt(variance)
            amplitude_effective = term.amplitude * term.sigma / sigma_effective
            for image in range(-periodic_images, periodic_images + 1):
                displacement = evaluation_x - source_x + image * config.box_length
                total += (
                    -weight
                    * amplitude_effective
                    * displacement
                    / variance
                    * math.exp(-0.5 * displacement**2 / variance)
                )
        return total

    gradient = source_gradient(
        float(initial_x),
        config.memory_mass * q**total_updates,
        total_updates,
    )
    for age, position in enumerate(positions):
        gradient += source_gradient(
            float(position),
            config.memory_mass * config.lambda_value * q**age,
            age + 1,
        )
    return float(gradient)


def omitted_history_weight(lambda_value: float, history_length: int) -> float:
    """Return the stationary exponential weight older than the retained history."""

    if not 0.0 < lambda_value <= 1.0 or history_length < 0:
        raise ValueError("invalid lambda_value or history_length")
    return float((1.0 - lambda_value) ** history_length)
