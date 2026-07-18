"""Analytic reference formulas for the finite-memory model."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import math

import numpy as np


@dataclass(frozen=True)
class DimensionlessScalarGroups:
    """Dimensionless controls for one scalar-memory parameter slice.

    ``restoring_per_update`` is the local linear drift multiplier. Dividing it
    by ``lambda_value`` expresses the same restoring strength per nominal
    memory time. ``noise_diffusion_per_memory_time`` is the continuum-scaled
    noise level in units of ``length_scale``.
    """

    length_scale: float
    memory_time_updates: float
    local_curvature: float
    restoring_per_update: float
    restoring_per_memory_time: float
    noise_per_update: float
    noise_diffusion_per_memory_time: float


def _validate_lambda(lambda_value: float, *, strict_upper: bool = False) -> None:
    upper_ok = lambda_value < 1.0 if strict_upper else lambda_value <= 1.0
    if not np.isfinite(lambda_value) or not (0.0 < lambda_value and upper_ok):
        bound = "< 1" if strict_upper else "<= 1"
        raise ValueError(f"lambda_value must satisfy 0 < value {bound}")


def _validate_positive(name: str, value: float) -> None:
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be positive")


def _validate_non_negative(name: str, value: float) -> None:
    if not np.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be non-negative")


def stationary_deposition_weight(
    lambda_value: float,
    *,
    memory_mass: float = 1.0,
) -> float:
    """Return beta for stationary memory mass ``M0``.

    For normalized ``G_sigma``, the update
    ``rho[n+1]=(1-lambda)rho[n]+beta*G_sigma`` has stationary mass
    ``M0=beta/lambda``. Hence the clean M0 parametrization uses
    ``beta=lambda*M0``.
    """

    _validate_lambda(lambda_value)
    _validate_non_negative("memory_mass", memory_mass)
    return float(lambda_value * memory_mass)


def stationary_memory_mass(lambda_value: float, deposition_weight: float) -> float:
    """Return stationary mass ``M0=beta/lambda`` for normalized deposition."""

    _validate_lambda(lambda_value)
    if not np.isfinite(deposition_weight) or deposition_weight < 0.0:
        raise ValueError("deposition_weight must be non-negative")
    return float(deposition_weight / lambda_value)


def scalar_dimensionless_groups(
    *,
    epsilon: float,
    eta: float,
    lambda_value: float,
    memory_mass: float,
    local_curvature: float,
    length_scale: float,
) -> DimensionlessScalarGroups:
    """Return dimensionless controls after choosing one reference length.

    The function does not assert that ``length_scale`` is a physical length.
    It only removes the coordinate unit. For the attractive-only pilot the
    natural convention is ``length_scale=sigma_att``.
    """

    _validate_lambda(lambda_value)
    _validate_positive("length_scale", length_scale)
    _validate_non_negative("epsilon", epsilon)
    _validate_non_negative("memory_mass", memory_mass)
    for name, value in (("eta", eta), ("local_curvature", local_curvature)):
        if not np.isfinite(value):
            raise ValueError(f"{name} must be finite")

    restoring_per_update = eta * memory_mass * local_curvature
    noise_per_update = epsilon / length_scale
    return DimensionlessScalarGroups(
        length_scale=float(length_scale),
        memory_time_updates=float(1.0 / lambda_value),
        local_curvature=float(local_curvature),
        restoring_per_update=float(restoring_per_update),
        restoring_per_memory_time=float(restoring_per_update / lambda_value),
        noise_per_update=float(noise_per_update),
        noise_diffusion_per_memory_time=float(
            noise_per_update * noise_per_update / (2.0 * lambda_value)
        ),
    )


def gaussian_kernel_curvature(
    *,
    amplitude: float = 1.0,
    length: float = 1.0,
) -> float:
    """Return ``a0=-w''(0)`` for ``w(r)=A exp(-r^2/(2L^2))``."""

    _validate_positive("amplitude", amplitude)
    _validate_positive("length", length)
    return float(amplitude / (length * length))


def critical_eta(
    lambda_value: float,
    *,
    memory_mass: float = 1.0,
    curvature: float = 1.0,
) -> float:
    """Return the local ballistic threshold eta_c.

    The formula is ``eta_c=lambda/((1-lambda)*M0*a0)`` with
    ``a0=-w''(0)>0`` for the effective kernel ``W=K*G``. It is undefined for
    ``M0=0`` and deliberately validates ``memory_mass`` as strictly positive.
    """

    _validate_lambda(lambda_value, strict_upper=True)
    _validate_positive("memory_mass", memory_mass)
    _validate_positive("curvature", curvature)
    return float(lambda_value / ((1.0 - lambda_value) * memory_mass * curvature))


def local_scalar_memory_modes(lambda_value: float, g: float) -> tuple[float, float]:
    """Return eigenvalues of the minimal scalar memory linearization.

    For ``x[n+1]=(1-g)x[n]+g m[n]`` and
    ``m[n+1]=(1-lambda)m[n]+lambda x[n+1]``, the eigenvalues are
    translation ``1`` and relative mode ``(1-lambda)(1-g)``. They are real.
    """

    _validate_lambda(lambda_value)
    if not np.isfinite(g):
        raise ValueError("g must be finite")
    return 1.0, float((1.0 - lambda_value) * (1.0 - g))


def frozen_hessian_stability(
    eta: float,
    hessian_eigenvalues: Iterable[float],
) -> list[str]:
    """Classify frozen-memory local stability from ``eta*h_i``.

    Labels are ``flat_or_anti_restoring``, ``monotone``, ``alternating``, and
    ``unstable``. The underlying discrete multiplier is ``1-eta*h_i``.
    """

    _validate_positive("eta", eta)
    values = np.asarray(list(hessian_eigenvalues), dtype=float)
    if values.ndim != 1:
        raise ValueError("hessian_eigenvalues must be one-dimensional")
    labels: list[str] = []
    for value in values:
        if not np.isfinite(value):
            raise ValueError("hessian_eigenvalues must be finite")
        product = eta * value
        if product <= 0.0:
            labels.append("flat_or_anti_restoring")
        elif product < 1.0:
            labels.append("monotone")
        elif product < 2.0:
            labels.append("alternating")
        else:
            labels.append("unstable")
    return labels


def two_scale_force_crossing_radius(
    *,
    amplitude_rep: float,
    length_rep: float,
    amplitude_att: float,
    length_att: float,
) -> float | None:
    """Return force sign-change radius for a two-Gaussian effective kernel.

    The formula applies to ``A_rep exp(-r^2/(2L_rep^2)) -
    A_att exp(-r^2/(2L_att^2))``. ``None`` means the supplied positive
    parameters do not produce a real positive crossing under this formula.
    """

    _validate_positive("amplitude_rep", amplitude_rep)
    _validate_positive("length_rep", length_rep)
    _validate_positive("amplitude_att", amplitude_att)
    _validate_positive("length_att", length_att)

    numerator = 2.0 * math.log(
        (amplitude_rep * length_att * length_att)
        / (amplitude_att * length_rep * length_rep)
    )
    denominator = 1.0 / (length_rep * length_rep) - 1.0 / (length_att * length_att)
    if denominator <= 0.0:
        return None
    radius_squared = numerator / denominator
    if radius_squared <= 0.0 or not math.isfinite(radius_squared):
        return None
    return float(math.sqrt(radius_squared))
