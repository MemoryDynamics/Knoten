"""Resource-bounded dynamics for a local active scalar delta-source field."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


def _finite(name: str, value: float) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _positive(name: str, value: float) -> float:
    number = _finite(name, value)
    if number <= 0.0:
        raise ValueError(f"{name} must be positive")
    return number


def _non_negative(name: str, value: float) -> float:
    number = _finite(name, value)
    if number < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return number


@dataclass(frozen=True)
class ActiveScalarFieldConfig:
    r"""Configuration of a one-dimensional periodic scalar field.

    The dimensionless equation is

    ``d_t phi = -P(-i*d_x) phi - u*phi^3 + s*delta_L(x-X_t)``,

    with ``P(k)=1+a2*k^2+a4*k^4``. The visible source follows

    ``dX_t=-eta*d_x phi(X_t)dt+epsilon*dW_t``.

    The delta source is represented by all retained Fourier modes. The
    ``dealias_fraction=0.25`` default is the cubic 1/2 rule.
    """

    grid_points: int = 256
    domain_length: float = 16.0 * math.pi
    time_step: float = 0.05
    steps: int = 4000
    sample_every: int = 10
    gradient_coefficient: float = -2.2
    biharmonic_coefficient: float = 1.0
    cubic_saturation: float = 1.0
    source_strength: float = 0.05
    source_enabled: bool = True
    eta: float = 0.2
    epsilon: float = 0.001
    seed: int = 1
    dealias_fraction: float = 0.25
    amplitude_stop: float = 1.0e6

    def __post_init__(self) -> None:
        if self.grid_points < 32 or self.grid_points % 2:
            raise ValueError("grid_points must be an even integer of at least 32")
        _positive("domain_length", self.domain_length)
        _positive("time_step", self.time_step)
        if self.steps < 1:
            raise ValueError("steps must be positive")
        if self.sample_every < 1:
            raise ValueError("sample_every must be positive")
        _finite("gradient_coefficient", self.gradient_coefficient)
        _positive("biharmonic_coefficient", self.biharmonic_coefficient)
        _non_negative("cubic_saturation", self.cubic_saturation)
        _finite("source_strength", self.source_strength)
        _non_negative("eta", self.eta)
        _non_negative("epsilon", self.epsilon)
        fraction = _positive("dealias_fraction", self.dealias_fraction)
        if fraction > 0.25:
            raise ValueError(
                "dealias_fraction must not exceed 0.25 for the cubic 1/2 rule"
            )
        _positive("amplitude_stop", self.amplitude_stop)


@dataclass(frozen=True)
class ActiveScalarFieldTrace:
    """Sampled trajectory and field observables from one scalar-field run."""

    times: np.ndarray
    positions: np.ndarray
    field_rms: np.ndarray
    field_max_abs: np.ndarray
    dominant_wavenumber: np.ndarray
    dominant_mode_amplitude: np.ndarray
    source_field_phase: np.ndarray
    final_coefficients: np.ndarray
    wavenumbers: np.ndarray
    completed_steps: int
    stop_reason: str


def scalar_field_wavenumbers(config: ActiveScalarFieldConfig) -> np.ndarray:
    """Return FFT-ordered angular wavenumbers."""

    dx = config.domain_length / config.grid_points
    return 2.0 * np.pi * np.fft.fftfreq(config.grid_points, d=dx)


def scalar_field_linear_rate(
    config: ActiveScalarFieldConfig,
    wavenumbers: np.ndarray | None = None,
) -> np.ndarray:
    """Return the linear growth rate ``-[1+a2*k^2+a4*k^4]``."""

    k = (
        scalar_field_wavenumbers(config)
        if wavenumbers is None
        else np.asarray(wavenumbers, dtype=float)
    )
    k2 = np.square(k)
    return -(
        1.0
        + config.gradient_coefficient * k2
        + config.biharmonic_coefficient * np.square(k2)
    )


def scalar_field_preferred_wavenumber(
    config: ActiveScalarFieldConfig,
) -> float:
    """Return the linear finite-wavenumber minimum, or zero."""

    if config.gradient_coefficient >= 0.0:
        return 0.0
    return float(
        np.sqrt(-config.gradient_coefficient / (2.0 * config.biharmonic_coefficient))
    )


def spectral_delta_coefficients(
    position: float,
    config: ActiveScalarFieldConfig,
    wavenumbers: np.ndarray | None = None,
) -> np.ndarray:
    """Return NumPy-FFT coefficients of the retained periodic delta."""

    k = (
        scalar_field_wavenumbers(config)
        if wavenumbers is None
        else np.asarray(wavenumbers, dtype=float)
    )
    coefficients = (
        config.grid_points / config.domain_length * np.exp(-1j * k * float(position))
    )
    return np.asarray(coefficients, dtype=np.complex128)


def _dealias_mask(config: ActiveScalarFieldConfig) -> np.ndarray:
    mode_number = np.fft.fftfreq(config.grid_points) * config.grid_points
    return np.abs(mode_number) < (
        config.dealias_fraction * config.grid_points - 1.0e-12
    )


def _project_real_spectrum(coefficients: np.ndarray) -> None:
    """Project FFT coefficients onto the Hermitian subspace in place."""

    n = coefficients.size
    positive = np.arange(1, n // 2)
    average = 0.5 * (coefficients[positive] + np.conj(coefficients[-positive]))
    coefficients[positive] = average
    coefficients[-positive] = np.conj(average)
    coefficients[0] = complex(coefficients[0].real, 0.0)
    coefficients[n // 2] = complex(coefficients[n // 2].real, 0.0)


def _etd_coefficients(
    linear_rate: np.ndarray,
    time_step: float,
) -> tuple[np.ndarray, np.ndarray]:
    argument = time_step * linear_rate
    propagator = np.exp(argument)
    forcing = np.empty_like(linear_rate)
    small = np.abs(argument) < 1.0e-7
    forcing[small] = time_step * (
        1.0 + argument[small] / 2.0 + np.square(argument[small]) / 6.0
    )
    forcing[~small] = np.expm1(argument[~small]) / linear_rate[~small]
    return propagator, forcing


def _field_gradient_at(
    coefficients: np.ndarray,
    wavenumbers: np.ndarray,
    position: float,
) -> float:
    series = coefficients / coefficients.size
    gradient = np.sum(1j * wavenumbers * series * np.exp(1j * wavenumbers * position))
    return float(np.real(gradient))


def _sample_observables(
    *,
    coefficients: np.ndarray,
    wavenumbers: np.ndarray,
    position: float,
    source_enabled: bool,
    source_strength: float,
) -> tuple[float, float, float, float, float]:
    field = np.fft.ifft(coefficients).real
    rms = float(np.sqrt(np.mean(np.square(field))))
    maximum = float(np.max(np.abs(field)))
    positive = wavenumbers > 0.0
    amplitudes = np.abs(coefficients[positive]) / coefficients.size
    if amplitudes.size == 0 or float(np.max(amplitudes)) == 0.0:
        return rms, maximum, 0.0, 0.0, float("nan")
    positive_k = wavenumbers[positive]
    index = int(np.argmax(amplitudes))
    dominant_k = float(positive_k[index])
    dominant_amplitude = float(amplitudes[index])
    phase = float("nan")
    if source_enabled and source_strength != 0.0:
        field_coefficient = coefficients[positive][index]
        source_phase = np.exp(-1j * dominant_k * position)
        if abs(field_coefficient) > 0.0:
            phase = float(np.angle(field_coefficient * np.conj(source_phase)))
    return rms, maximum, dominant_k, dominant_amplitude, phase


def simulate_active_scalar_delta_field(
    config: ActiveScalarFieldConfig,
    *,
    initial_position: float | None = None,
    initial_coefficients: np.ndarray | None = None,
) -> ActiveScalarFieldTrace:
    """Simulate the local scalar field with an ETD1 pseudo-spectral step."""

    n = config.grid_points
    length = config.domain_length
    position = (
        0.5 * length if initial_position is None else float(initial_position) % length
    )
    k = scalar_field_wavenumbers(config)
    linear_rate = scalar_field_linear_rate(config, k)
    propagator, forcing = _etd_coefficients(linear_rate, config.time_step)
    mask = _dealias_mask(config)
    if initial_coefficients is None:
        coefficients = np.zeros(n, dtype=np.complex128)
    else:
        coefficients = np.asarray(initial_coefficients, dtype=np.complex128).copy()
        if coefficients.shape != (n,):
            raise ValueError("initial_coefficients must have shape (grid_points,)")
        if not np.isfinite(coefficients).all():
            raise ValueError("initial_coefficients must be finite")
    coefficients[~mask] = 0.0
    _project_real_spectrum(coefficients)
    rng = np.random.default_rng(config.seed)

    sample_steps = np.unique(
        np.concatenate(
            (
                np.array([0], dtype=int),
                np.arange(
                    config.sample_every,
                    config.steps + 1,
                    config.sample_every,
                    dtype=int,
                ),
                np.array([config.steps], dtype=int),
            )
        )
    )
    sampled_times: list[float] = []
    sampled_positions: list[float] = []
    sampled_rms: list[float] = []
    sampled_maximum: list[float] = []
    sampled_k: list[float] = []
    sampled_amplitude: list[float] = []
    sampled_phase: list[float] = []

    def append_sample(step: int) -> None:
        rms, maximum, dominant_k, amplitude, phase = _sample_observables(
            coefficients=coefficients,
            wavenumbers=k,
            position=position,
            source_enabled=config.source_enabled,
            source_strength=config.source_strength,
        )
        sampled_times.append(step * config.time_step)
        sampled_positions.append(position)
        sampled_rms.append(rms)
        sampled_maximum.append(maximum)
        sampled_k.append(dominant_k)
        sampled_amplitude.append(amplitude)
        sampled_phase.append(phase)

    append_sample(0)
    next_sample_index = 1
    stop_reason = "completed"
    completed_steps = 0
    for step in range(1, config.steps + 1):
        field = np.fft.ifft(coefficients).real
        nonlinear = -config.cubic_saturation * np.power(field, 3)
        nonlinear_coefficients = np.fft.fft(nonlinear)
        nonlinear_coefficients[~mask] = 0.0
        if config.source_enabled and config.source_strength != 0.0:
            source = config.source_strength * spectral_delta_coefficients(
                position,
                config,
                k,
            )
            source[~mask] = 0.0
        else:
            source = 0.0
        coefficients = propagator * coefficients + forcing * (
            nonlinear_coefficients + source
        )
        coefficients[~mask] = 0.0
        _project_real_spectrum(coefficients)
        coefficients[n // 2] = 0.0

        gradient = _field_gradient_at(coefficients, k, position)
        noise = config.epsilon * math.sqrt(config.time_step) * float(rng.normal())
        position = (
            position - config.eta * gradient * config.time_step + noise
        ) % length
        completed_steps = step

        if not np.isfinite(coefficients).all():
            stop_reason = "non_finite_amplitude"
        elif float(np.max(np.abs(coefficients)) / n) > config.amplitude_stop:
            stop_reason = "amplitude_stop"
        if stop_reason != "completed":
            append_sample(step)
            break
        if next_sample_index < sample_steps.size and step == int(
            sample_steps[next_sample_index]
        ):
            append_sample(step)
            next_sample_index += 1

    return ActiveScalarFieldTrace(
        times=np.asarray(sampled_times, dtype=float),
        positions=np.asarray(sampled_positions, dtype=float),
        field_rms=np.asarray(sampled_rms, dtype=float),
        field_max_abs=np.asarray(sampled_maximum, dtype=float),
        dominant_wavenumber=np.asarray(sampled_k, dtype=float),
        dominant_mode_amplitude=np.asarray(sampled_amplitude, dtype=float),
        source_field_phase=np.asarray(sampled_phase, dtype=float),
        final_coefficients=coefficients.copy(),
        wavenumbers=k,
        completed_steps=int(completed_steps),
        stop_reason=stop_reason,
    )
