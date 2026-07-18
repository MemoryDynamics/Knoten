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


def two_scale_integral_coefficient(
    *,
    dim: int,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float = 1.0,
    amplitude_att: float = 0.35,
) -> float:
    """Return the Gaussian-integral coefficient of ``A_rep G_rep-A_att G_att``.

    The common positive factor ``(2*pi)**(dim/2)`` is omitted. Therefore a
    zero return value is equivalent to a zero spatial integral for the
    unnormalized Gaussian convention used by the canonical kernel.
    """

    if dim < 1:
        raise ValueError("dim must be positive")
    for name, value in (("sigma_rep", sigma_rep), ("sigma_att", sigma_att)):
        if value <= 0.0 or not np.isfinite(value):
            raise ValueError(f"{name} must be positive")
    for name, value in (
        ("amplitude_rep", amplitude_rep),
        ("amplitude_att", amplitude_att),
    ):
        if not np.isfinite(value):
            raise ValueError(f"{name} must be finite")
    return float(amplitude_rep * sigma_rep**dim - amplitude_att * sigma_att**dim)


def two_scale_local_curvature(
    *,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float = 1.0,
    amplitude_att: float = 0.35,
) -> float:
    """Return the restoring curvature at the origin for the two-scale kernel.

    For ``K=A_rep G_rep-A_att G_att`` and update ``x <- x-eta*grad K``, a
    positive value means locally inward linear drift around a point deposit.
    """

    for name, value in (("sigma_rep", sigma_rep), ("sigma_att", sigma_att)):
        if value <= 0.0 or not np.isfinite(value):
            raise ValueError(f"{name} must be positive")
    for name, value in (
        ("amplitude_rep", amplitude_rep),
        ("amplitude_att", amplitude_att),
    ):
        if not np.isfinite(value):
            raise ValueError(f"{name} must be finite")
    return float(amplitude_att / sigma_att**2 - amplitude_rep / sigma_rep**2)


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


def zero_mean_compensator_amplitude(
    *,
    dim: int,
    sigma_rep: float,
    sigma_att: float,
    sigma_comp: float,
    amplitude_rep: float = 1.0,
    amplitude_att: float = 0.35,
) -> float:
    """Return ``A_comp`` for ``A_rep G_rep-A_att G_att+A_comp G_comp``.

    The returned amplitude is signed. It is positive when the original
    two-scale kernel has a negative integral, as in the current compact-knot
    candidates. A sufficiently broad compensator can cancel the monopole
    integral while perturbing the local curvature only weakly.
    """

    if sigma_comp <= 0.0 or not np.isfinite(sigma_comp):
        raise ValueError("sigma_comp must be positive")
    residual = two_scale_integral_coefficient(
        dim=dim,
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
    )
    return float(-residual / sigma_comp**dim)


def zero_mean_curvature_matched_amplitudes(
    *,
    dim: int,
    sigma_rep: float,
    sigma_att: float,
    sigma_comp: float,
    target_curvature: float,
    amplitude_rep: float = 1.0,
) -> tuple[float, float]:
    """Return ``(A_att, A_comp)`` matching zero integral and local curvature.

    The result parameterizes
    ``K=A_rep G_rep-A_att G_att+A_comp G_comp`` in the unnormalized
    Gaussian convention. ``sigma_comp`` must differ from ``sigma_att``;
    the intended use is a compensator broader than both original scales.
    """

    if dim < 1:
        raise ValueError("dim must be positive")
    for name, value in (
        ("sigma_rep", sigma_rep),
        ("sigma_att", sigma_att),
        ("sigma_comp", sigma_comp),
    ):
        if value <= 0.0 or not np.isfinite(value):
            raise ValueError(f"{name} must be positive")
    if not np.isfinite(target_curvature):
        raise ValueError("target_curvature must be finite")
    if not np.isfinite(amplitude_rep):
        raise ValueError("amplitude_rep must be finite")

    inverse_comp_power = sigma_comp ** (-(dim + 2))
    denominator = sigma_att**-2 - sigma_att**dim * inverse_comp_power
    if np.isclose(denominator, 0.0, rtol=1e-12, atol=0.0):
        raise ValueError("sigma_comp and sigma_att produce a singular constraint")
    numerator = (
        target_curvature
        + amplitude_rep / sigma_rep**2
        - amplitude_rep * sigma_rep**dim * inverse_comp_power
    )
    amplitude_att = numerator / denominator
    amplitude_comp = zero_mean_compensator_amplitude(
        dim=dim,
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        sigma_comp=sigma_comp,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
    )
    return float(amplitude_att), float(amplitude_comp)


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
            raise ValueError(
                "deposition_sigma must be zero for matched_gaussian deposition"
            )
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


def gaussian_potential(
    x: Iterable[float],
    memory: Iterable[Iterable[float]],
    weights: Iterable[float],
    *,
    sigma: float,
    amplitude: float = 1.0,
) -> float:
    """Weighted ``amplitude * exp(-r^2/(2 sigma^2))`` potential."""

    x_arr = np.asarray(x, dtype=float)
    mem = np.asarray(memory, dtype=float)
    w = np.asarray(weights, dtype=float)
    if mem.size == 0:
        return 0.0
    if x_arr.ndim != 1:
        raise ValueError("x must be one-dimensional")
    if mem.ndim != 2 or mem.shape[1] != x_arr.size:
        raise ValueError("memory must have shape (n_memory, dim)")
    if w.ndim != 1 or mem.shape[0] != w.shape[0]:
        raise ValueError("weights must match memory length")
    if sigma <= 0.0 or not np.isfinite(sigma):
        raise ValueError("sigma must be positive and finite")
    if not np.isfinite(amplitude):
        raise ValueError("amplitude must be finite")
    if not np.isfinite(x_arr).all() or not np.isfinite(mem).all():
        raise ValueError("field coordinates must be finite")
    if not np.isfinite(w).all():
        raise ValueError("weights must be finite")
    dx = x_arr[None, :] - mem
    r2 = np.einsum("ij,ij->i", dx, dx)
    return float(np.sum(w * amplitude * np.exp(-0.5 * r2 / (sigma * sigma))))


def double_gaussian_potential(
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
) -> float:
    """Potential ``A_rep G_rep - A_att G_att`` after write convolution."""

    x_arr = np.asarray(x, dtype=float)
    if x_arr.ndim != 1:
        raise ValueError("x must be one-dimensional")
    params = effective_double_gaussian_parameters(
        dim=x_arr.size,
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
        deposition_kernel=deposition_kernel,
        deposition_sigma=deposition_sigma,
    )
    rep = gaussian_potential(
        x_arr,
        memory,
        weights,
        sigma=params["sigma_rep"],
        amplitude=params["amplitude_rep"],
    )
    att = gaussian_potential(
        x_arr,
        memory,
        weights,
        sigma=params["sigma_att"],
        amplitude=params["amplitude_att"],
    )
    return rep - att


def three_scale_gaussian_potential(
    x: Iterable[float],
    memory: Iterable[Iterable[float]],
    weights: Iterable[float],
    *,
    sigma_rep: float,
    sigma_att: float,
    sigma_comp: float,
    amplitude_rep: float = 1.0,
    amplitude_att: float = 0.35,
    amplitude_comp: float = 0.0,
    deposition_kernel: str = "delta",
    deposition_sigma: float = 0.0,
) -> float:
    """Potential ``A_rep G_rep-A_att G_att+A_comp G_comp`` after convolution."""

    x_arr = np.asarray(x, dtype=float)
    if x_arr.ndim != 1:
        raise ValueError("x must be one-dimensional")
    base = double_gaussian_potential(
        x_arr,
        memory,
        weights,
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
        deposition_kernel=deposition_kernel,
        deposition_sigma=deposition_sigma,
    )
    effective_sigma, effective_amplitude = effective_gaussian_parameters(
        sigma=sigma_comp,
        amplitude=amplitude_comp,
        dim=x_arr.size,
        deposition_kernel=deposition_kernel,
        deposition_sigma=deposition_sigma,
    )
    return base + gaussian_potential(
        x_arr,
        memory,
        weights,
        sigma=effective_sigma,
        amplitude=effective_amplitude,
    )


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


def three_scale_gaussian_gradient(
    x: Iterable[float],
    memory: Iterable[Iterable[float]],
    weights: Iterable[float],
    *,
    sigma_rep: float,
    sigma_att: float,
    sigma_comp: float,
    amplitude_rep: float = 1.0,
    amplitude_att: float = 0.35,
    amplitude_comp: float = 0.0,
    deposition_kernel: str = "delta",
    deposition_sigma: float = 0.0,
) -> np.ndarray:
    """Gradient of ``A_rep G_rep-A_att G_att+A_comp G_comp`` after convolution."""

    x_arr = np.asarray(x, dtype=float)
    base = double_gaussian_gradient(
        x_arr,
        memory,
        weights,
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
        deposition_kernel=deposition_kernel,
        deposition_sigma=deposition_sigma,
    )
    effective_sigma, effective_amplitude = effective_gaussian_parameters(
        sigma=sigma_comp,
        amplitude=amplitude_comp,
        dim=x_arr.size,
        deposition_kernel=deposition_kernel,
        deposition_sigma=deposition_sigma,
    )
    return base + gaussian_gradient(
        x_arr,
        memory,
        weights,
        sigma=effective_sigma,
        amplitude=effective_amplitude,
    )
