"""Resource-bounded Fourier representation of exponential scalar memory.

The module rewrites the existing periodic one-dimensional memory measure as
Fourier coefficients. It is a coarse-grained representation of ``rho``, not
a new physical field equation and not a finite-propagation model.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class GaussianKernelMode:
    """One signed term ``amplitude*exp(-r^2/(2*sigma^2))``."""

    amplitude: float
    sigma: float

    def __post_init__(self) -> None:
        if not np.isfinite(self.amplitude):
            raise ValueError("amplitude must be finite")
        if not np.isfinite(self.sigma) or self.sigma <= 0.0:
            raise ValueError("sigma must be positive and finite")


@dataclass(frozen=True)
class SpectralMemoryConfig:
    """Configuration of a periodic one-dimensional spectral memory state."""

    box_length: float = 80.0
    n_modes: int = 64
    lambda_value: float = 0.01
    memory_mass: float = 1.0
    deposition_sigma: float = 0.0
    kernel: tuple[GaussianKernelMode, ...] = (
        GaussianKernelMode(amplitude=-26.0, sigma=3.0),
        GaussianKernelMode(amplitude=7.8, sigma=10.0),
    )

    def __post_init__(self) -> None:
        if not np.isfinite(self.box_length) or self.box_length <= 0.0:
            raise ValueError("box_length must be positive and finite")
        if self.n_modes < 1:
            raise ValueError("n_modes must be positive")
        if not 0.0 < self.lambda_value <= 1.0:
            raise ValueError("lambda_value must lie in (0,1]")
        if not np.isfinite(self.memory_mass) or self.memory_mass < 0.0:
            raise ValueError("memory_mass must be non-negative and finite")
        if not np.isfinite(self.deposition_sigma) or self.deposition_sigma < 0.0:
            raise ValueError("deposition_sigma must be non-negative and finite")
        if not self.kernel:
            raise ValueError("kernel must contain at least one mode")


@dataclass(frozen=True)
class SpectralMemoryState:
    """Immutable visible coordinate plus retained spectral memory field."""

    x: float
    rho_coefficients: np.ndarray
    update_index: int = 0

    def __post_init__(self) -> None:
        if not np.isfinite(self.x):
            raise ValueError("x must be finite")
        if self.update_index < 0:
            raise ValueError("update_index must be non-negative")
        coefficients = np.asarray(self.rho_coefficients, dtype=np.complex128).copy()
        if coefficients.ndim != 1 or coefficients.size < 2:
            raise ValueError("rho_coefficients must be a one-dimensional array")
        if not np.isfinite(coefficients).all():
            raise ValueError("rho_coefficients must be finite")
        coefficients.setflags(write=False)
        object.__setattr__(self, "rho_coefficients", coefficients)


def wavenumbers(config: SpectralMemoryConfig) -> np.ndarray:
    """Return non-negative retained periodic wavenumbers."""

    return 2.0 * np.pi * np.arange(config.n_modes + 1) / config.box_length


def wrap_periodic(x: float, box_length: float) -> float:
    if not np.isfinite(x) or not np.isfinite(box_length) or box_length <= 0.0:
        raise ValueError("x and positive box_length must be finite")
    return float(x % box_length)


def periodic_displacement(x: float, origin: float, box_length: float) -> float:
    """Return the signed shortest displacement from ``origin`` to ``x``."""

    length = float(box_length)
    if not np.isfinite(x) or not np.isfinite(origin) or length <= 0.0:
        raise ValueError("coordinates and positive box_length must be finite")
    return float((x - origin + 0.5 * length) % length - 0.5 * length)


def deposition_coefficients(
    config: SpectralMemoryConfig,
    x: float,
) -> np.ndarray:
    """Return normalized Fourier coefficients deposited at ``x``."""

    x = wrap_periodic(x, config.box_length)
    k = wavenumbers(config)
    smoothing = np.exp(-0.5 * config.deposition_sigma**2 * k**2)
    coefficients = (
        config.memory_mass
        / config.box_length
        * smoothing
        * np.exp(-1j * k * x)
    )
    coefficients[0] = complex(config.memory_mass / config.box_length, 0.0)
    return np.asarray(coefficients, dtype=np.complex128)


def kernel_integral_coefficient(config: SpectralMemoryConfig) -> float:
    """Return the 1D Gaussian integral apart from ``sqrt(2*pi)``."""

    return float(sum(term.amplitude * term.sigma for term in config.kernel))


def kernel_transfer(config: SpectralMemoryConfig) -> np.ndarray:
    """Return the periodic convolution multiplier for every retained mode."""

    k = wavenumbers(config)
    transfer = np.zeros_like(k)
    for term in config.kernel:
        transfer += (
            math.sqrt(2.0 * math.pi)
            * term.amplitude
            * term.sigma
            * np.exp(-0.5 * term.sigma**2 * k**2)
        )
    return transfer


def zero_mean_attractive_kernel(
    *,
    amplitude_att: float = 26.0,
    sigma_att: float = 3.0,
    sigma_comp: float = 10.0,
) -> tuple[GaussianKernelMode, GaussianKernelMode]:
    """Return ``-A_att G_att + A_comp G_comp`` with zero 1D integral."""

    for name, value in (
        ("amplitude_att", amplitude_att),
        ("sigma_att", sigma_att),
        ("sigma_comp", sigma_comp),
    ):
        if not np.isfinite(value) or value <= 0.0:
            raise ValueError(f"{name} must be positive and finite")
    amplitude_comp = amplitude_att * sigma_att / sigma_comp
    return (
        GaussianKernelMode(amplitude=-float(amplitude_att), sigma=float(sigma_att)),
        GaussianKernelMode(amplitude=float(amplitude_comp), sigma=float(sigma_comp)),
    )


def initialize_state(
    config: SpectralMemoryConfig,
    *,
    x: float = 0.0,
) -> SpectralMemoryState:
    x = wrap_periodic(x, config.box_length)
    return SpectralMemoryState(x=x, rho_coefficients=deposition_coefficients(config, x))


def update_rho(
    config: SpectralMemoryConfig,
    rho_coefficients: np.ndarray,
    *,
    deposited_at: float,
) -> np.ndarray:
    """Apply the exact affine exponential-memory update mode by mode."""

    rho = np.asarray(rho_coefficients, dtype=np.complex128)
    if rho.shape != (config.n_modes + 1,):
        raise ValueError("rho coefficient shape does not match config")
    return np.asarray(
        (1.0 - config.lambda_value) * rho
        + config.lambda_value * deposition_coefficients(config, deposited_at),
        dtype=np.complex128,
    )


def evaluate_real_series(
    coefficients: np.ndarray,
    *,
    x: float,
    box_length: float,
) -> float:
    values = np.asarray(coefficients, dtype=np.complex128)
    if values.ndim != 1 or values.size < 2 or not np.isfinite(values).all():
        raise ValueError("coefficients must be a finite one-dimensional array")
    k = 2.0 * np.pi * np.arange(values.size) / box_length
    phases = np.exp(1j * k[1:] * wrap_periodic(x, box_length))
    return float(values[0].real + 2.0 * np.real(np.sum(values[1:] * phases)))


def potential_coefficients(
    config: SpectralMemoryConfig,
    rho_coefficients: np.ndarray,
    *,
    zero_mode_offset: float = 0.0,
) -> np.ndarray:
    """Return ``Phi_hat=K_hat*rho_hat`` with optional constant-mode offset."""

    rho = np.asarray(rho_coefficients, dtype=np.complex128)
    if rho.shape != (config.n_modes + 1,):
        raise ValueError("rho coefficient shape does not match config")
    if not np.isfinite(zero_mode_offset):
        raise ValueError("zero_mode_offset must be finite")
    transfer = kernel_transfer(config).astype(np.complex128)
    transfer[0] += zero_mode_offset
    return transfer * rho


def potential_gradient(
    config: SpectralMemoryConfig,
    rho_coefficients: np.ndarray,
    *,
    x: float,
    zero_mode_offset: float = 0.0,
) -> float:
    """Evaluate ``d_x(K*rho)``; the zero mode cancels exactly."""

    phi = potential_coefficients(
        config,
        rho_coefficients,
        zero_mode_offset=zero_mode_offset,
    )
    k = wavenumbers(config)
    phases = np.exp(1j * k[1:] * wrap_periodic(x, config.box_length))
    return float(2.0 * np.real(np.sum(1j * k[1:] * phi[1:] * phases)))


def circular_center(
    config: SpectralMemoryConfig,
    rho_coefficients: np.ndarray,
) -> float | None:
    """Return the first-mode circular memory center."""

    rho = np.asarray(rho_coefficients, dtype=np.complex128)
    if rho.shape != (config.n_modes + 1,):
        raise ValueError("rho coefficient shape does not match config")
    if abs(rho[1]) <= np.finfo(float).eps:
        return None
    return wrap_periodic(-float(np.angle(rho[1])) / wavenumbers(config)[1], config.box_length)


def advance_state(
    state: SpectralMemoryState,
    config: SpectralMemoryConfig,
    *,
    epsilon: float,
    eta: float,
    noise: float,
) -> SpectralMemoryState:
    """Advance ``(x,rho_hat)`` by one Markov update."""

    if state.rho_coefficients.shape != (config.n_modes + 1,):
        raise ValueError("state coefficient shape does not match config")
    for name, value in (("epsilon", epsilon), ("eta", eta)):
        if not np.isfinite(value) or value < 0.0:
            raise ValueError(f"{name} must be non-negative and finite")
    if not np.isfinite(noise):
        raise ValueError("noise must be finite")
    gradient = potential_gradient(config, state.rho_coefficients, x=state.x)
    x_new = wrap_periodic(
        state.x + float(epsilon) * float(noise) - float(eta) * gradient,
        config.box_length,
    )
    rho_new = update_rho(config, state.rho_coefficients, deposited_at=x_new)
    return SpectralMemoryState(
        x=x_new,
        rho_coefficients=rho_new,
        update_index=state.update_index + 1,
    )


def explicit_history_coefficients(
    config: SpectralMemoryConfig,
    positions: Iterable[float],
    *,
    initial_coefficients: np.ndarray,
) -> np.ndarray:
    """Evaluate the rolled-out affine history for verification."""

    points = [float(value) for value in positions]
    initial = np.asarray(initial_coefficients, dtype=np.complex128)
    if initial.shape != (config.n_modes + 1,):
        raise ValueError("initial coefficient shape does not match config")
    q = 1.0 - config.lambda_value
    result = q ** len(points) * initial
    for age, point in enumerate(reversed(points)):
        result = result + config.lambda_value * q**age * deposition_coefficients(
            config, point
        )
    return np.asarray(result, dtype=np.complex128)
