"""Kernel gradients for finite-memory trajectory simulations."""

from __future__ import annotations

from typing import Iterable

import numpy as np


def exponential_weights(alpha: float, horizon: int) -> np.ndarray:
    """Return finite exponential memory weights alpha * (1-alpha)^k."""

    if not 0.0 < alpha <= 1.0:
        raise ValueError("alpha must satisfy 0 < alpha <= 1")
    if horizon < 1:
        raise ValueError("horizon must be positive")
    k = np.arange(horizon, dtype=float)
    return alpha * np.power(1.0 - alpha, k)


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
