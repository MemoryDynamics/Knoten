"""Kernel gradients for finite-memory trajectory simulations.

The canonical backend stores point deposits in the retained history. With
``deposition_kernel="delta"`` the Gaussian lengths are interaction-kernel
lengths. Finite Gaussian deposition is represented through the exact effective
convolution of Gaussian write/read kernels.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np


DEPOSITION_KERNELS = {"delta", "gaussian", "matched_gaussian"}


def zero_mean_attractive_amplitude(
    *,
    dim: int,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float = 1.0,
) -> float:
    """Return ``A_att`` such that the unnormalized two-Gaussian kernel has zero integral."""

    if dim < 1:
        raise ValueError("dim must be positive")
    if sigma_rep <= 0.0 or not np.isfinite(sigma_rep):
        raise ValueError("sigma_rep must be positive")
    if sigma_att <= 0.0 or not np.isfinite(sigma_att):
        raise ValueError("sigma_att must be positive")
    if not np.isfinite(amplitude_rep):
        raise ValueError("amplitude_rep must be finite")
    return float(amplitude_rep) * float((sigma_rep / sigma_att) ** dim)


def matched_local_stiffness_renormalization(dim: int) -> float:
    """Return the amplitude factor preserving local Gaussian stiffness after matching."""

    if dim < 1:
        raise ValueError("dim must be positive")
    return float(2.0 ** (0.5 * dim + 1.0))


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


def effective_gaussian_parameters(
    *,
    sigma: float,
    amplitude: float,
    dim: int,
    deposition_kernel: str = "delta",
    deposition_sigma: float = 0.0,
    matched_sigma: float | None = None,
) -> tuple[float, float]:
    """Return effective read-kernel parameters after Gaussian deposition.

    For a normalized Gaussian deposition kernel with width ``s``, convolution
    maps ``A exp(-r^2/(2 L^2))`` to
    ``A (L / sqrt(L^2+s^2))^dim exp(-r^2/(2(L^2+s^2)))``.
    ``matched_gaussian`` sets ``s`` to the read-kernel length unless an explicit
    ``matched_sigma`` is supplied.
    """

    if dim < 1:
        raise ValueError("dim must be positive")
    if sigma <= 0.0 or not np.isfinite(sigma):
        raise ValueError("sigma must be positive")
    if deposition_kernel not in DEPOSITION_KERNELS:
        raise ValueError(f"unknown deposition_kernel: {deposition_kernel}")
    if deposition_kernel == "delta":
        if deposition_sigma != 0.0:
            raise ValueError("deposition_sigma must be zero for delta deposition")
        return float(sigma), float(amplitude)
    if deposition_kernel == "gaussian":
        dep_sigma = deposition_sigma
    else:
        if deposition_sigma != 0.0:
            raise ValueError("deposition_sigma must be zero for matched_gaussian deposition")
        dep_sigma = sigma if matched_sigma is None else matched_sigma
    if dep_sigma <= 0.0 or not np.isfinite(dep_sigma):
        raise ValueError("deposition_sigma must be positive for finite deposition")
    effective_sigma = float(np.sqrt(sigma * sigma + dep_sigma * dep_sigma))
    effective_amplitude = float(amplitude) * float((sigma / effective_sigma) ** dim)
    return effective_sigma, effective_amplitude


def effective_double_gaussian_parameters(
    *,
    dim: int,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float = 1.0,
    amplitude_att: float = 0.35,
    deposition_kernel: str = "delta",
    deposition_sigma: float = 0.0,
) -> dict[str, float]:
    """Return effective two-scale parameters for the selected deposition mode."""

    rep_sigma, rep_amp = effective_gaussian_parameters(
        sigma=sigma_rep,
        amplitude=amplitude_rep,
        dim=dim,
        deposition_kernel=deposition_kernel,
        deposition_sigma=deposition_sigma,
    )
    att_sigma, att_amp = effective_gaussian_parameters(
        sigma=sigma_att,
        amplitude=amplitude_att,
        dim=dim,
        deposition_kernel=deposition_kernel,
        deposition_sigma=deposition_sigma,
    )
    return {
        "sigma_rep": rep_sigma,
        "sigma_att": att_sigma,
        "amplitude_rep": rep_amp,
        "amplitude_att": att_amp,
    }


def gaussian_gradient(
    x: Iterable[float],
    memory: Iterable[Iterable[float]],
    weights: Iterable[float],
    *,
    sigma: float,
    amplitude: float = 1.0,
) -> np.ndarray:
    """Weighted gradient of ``amplitude * exp(-r^2/(2 sigma^2))``.

    For positive amplitude this gradient points toward the memory point. The
    deterministic model update uses ``-eta * grad``; a positive one-scale
    Gaussian therefore produces outward, repulsive drift.
    """

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
    fac = -amplitude * np.exp(-0.5 * r2 / (sigma * sigma)) / (sigma * sigma)
    return np.sum((w * fac)[:, None] * dx, axis=0)


def repulsive_gaussian_gradient(
    x: Iterable[float],
    memory: Iterable[Iterable[float]],
    weights: Iterable[float],
    *,
    sigma: float,
    amplitude: float = 1.0,
) -> np.ndarray:
    """Return the outward vector generated by a positive Gaussian potential.

    This helper is a drift-direction convenience, not ``grad K`` itself. It is
    used by self-repulsion/ballistic probes that add an outward Gaussian term
    directly to the update.
    """

    return -gaussian_gradient(
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
    deposition_kernel: str = "delta",
    deposition_sigma: float = 0.0,
) -> np.ndarray:
    """Gradient of ``A_rep G_rep - A_att G_att`` after write-kernel convolution.

    With the canonical update ``x <- x - eta * grad``, the short positive
    ``A_rep`` term produces local repulsive drift, while the subtracted broad
    ``A_att`` term produces attractive drift at its active scale.
    """

    x_arr = np.asarray(x, dtype=float)
    params = effective_double_gaussian_parameters(
        dim=x_arr.size,
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
        deposition_kernel=deposition_kernel,
        deposition_sigma=deposition_sigma,
    )
    rep = gaussian_gradient(
        x_arr,
        memory,
        weights,
        sigma=params["sigma_rep"],
        amplitude=params["amplitude_rep"],
    )
    att = gaussian_gradient(
        x_arr,
        memory,
        weights,
        sigma=params["sigma_att"],
        amplitude=params["amplitude_att"],
    )
    return rep - att
