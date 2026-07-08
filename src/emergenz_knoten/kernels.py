"""Kernel gradients for finite-memory trajectory simulations.

The canonical simulation backend stores point deposits in the retained history.
This corresponds to a delta deposition kernel; the Gaussian lengths below are
therefore interaction/effective-kernel lengths, not a separate smoothing width.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np


def exponential_memory_weights(
    lambda_value: float,
    horizon: int,
    *,
    memory_mass: float = 1.0,
) -> np.ndarray:
    """Return finite exponential weights for mass ``memory_mass``.

    The general memory update is
    ``rho[n+1] = (1-lambda) rho[n] + lambda*M0*G_sigma``.
    For a normalized deposition kernel this has stationary mass ``M0`` and
    path weights ``lambda*M0*(1-lambda)^k``.
    """

    if not 0.0 < lambda_value <= 1.0:
        raise ValueError("lambda_value must satisfy 0 < value <= 1")
    if horizon < 1:
        raise ValueError("horizon must be positive")
    if not np.isfinite(memory_mass) or memory_mass < 0.0:
        raise ValueError("memory_mass must be non-negative")
    k = np.arange(horizon, dtype=float)
    return memory_mass * lambda_value * np.power(1.0 - lambda_value, k)


def exponential_weights(alpha: float, horizon: int) -> np.ndarray:
    """Return normalized finite exponential memory weights.

    This backward-compatible wrapper is the paper's normalized convention
    ``lambda_m=beta=alpha``, equivalent to ``memory_mass=1``.
    """

    return exponential_memory_weights(alpha, horizon, memory_mass=1.0)


def gaussian_gradient(
    x: Iterable[float],
    memory: Iterable[Iterable[float]],
    weights: Iterable[float],
    *,
    sigma: float,
    amplitude: float = 1.0,
) -> np.ndarray:
    """Weighted gradient contribution of a single Gaussian kernel."""

    x_arr = np.asarray(x, dtype=float)
    mem = np.asarray(memory, dtype=float)
    w = np.asarray(weights, dtype=float)
    if mem.size == 0:
        return np.zeros_like(x_arr)
    if mem.ndim != 2:
        raise ValueError("memory must have shape (n_memory, dim)")
    if mem.shape[0] != w.shape[0]:
        raise ValueError("weights must match memory length")
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    dx = x_arr[None, :] - mem
    r2 = np.einsum("ij,ij->i", dx, dx)
    fac = amplitude * np.exp(-0.5 * r2 / (sigma * sigma)) / (sigma * sigma)
    return np.sum((w * fac)[:, None] * dx, axis=0)


def repulsive_gaussian_gradient(
    x: Iterable[float],
    memory: Iterable[Iterable[float]],
    weights: Iterable[float],
    *,
    sigma: float,
    amplitude: float = 1.0,
) -> np.ndarray:
    """Return the outward Gaussian memory gradient for repulsive drift tests.

    The returned vector points away from the memory cloud. A simulation becomes
    repulsive only when this vector is added to the update; the canonical
    overdamped confinement update uses the opposite sign.
    """

    return gaussian_gradient(
        x,
        memory,
        weights,
        sigma=sigma,
        amplitude=amplitude,
    )


def double_gaussian_gradient(
    x: Iterable[float],
    memory: Iterable[Iterable[float]],
    weights: Iterable[float],
    *,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float = 1.0,
    amplitude_att: float = 0.35,
) -> np.ndarray:
    """Repulsive-attractive two-scale gradient used in later scans."""

    rep = gaussian_gradient(
        x,
        memory,
        weights,
        sigma=sigma_rep,
        amplitude=amplitude_rep,
    )
    att = gaussian_gradient(
        x,
        memory,
        weights,
        sigma=sigma_att,
        amplitude=amplitude_att,
    )
    return rep - att
