"""Analytic gates for a continuity-constrained memory density and flux.

The density-flux state in this module is a proposed extension of the canonical
``(x, rho)`` model.  It is not used by the finite-memory simulator.  Unlike a
freely assigned vector-memory channel, the longitudinal flux is constrained by
a local balance law.  Its constitutive relaxation and stiffness remain new
model assumptions.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


def _finite(name: str, value: float) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _non_negative(name: str, value: float) -> float:
    number = _finite(name, value)
    if number < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return number


@dataclass(frozen=True)
class MemoryInnovationMoments:
    """Zeroth and first moments of one ideal scalar-memory innovation."""

    monopole: float
    first_moment: np.ndarray


@dataclass(frozen=True)
class ContinuityMemoryMode:
    """Linear longitudinal mode of a relaxing memory density and flux."""

    wavenumber: float
    eigenvalues: tuple[complex, complex]
    asymptotically_stable: bool
    oscillatory: bool
    trace_damping_rate: float
    angular_frequency: float
    classification: str


def memory_innovation_moments(
    *,
    memory_relaxation: float,
    target_mass: float,
    current_mass: float,
    current_centroid: np.ndarray,
    deposited_position: np.ndarray,
) -> MemoryInnovationMoments:
    r"""Return moments of ``lambda*(M0*G_x-rho)`` for normalized ``G``.

    The monopole vanishes when the current memory mass equals ``M0``.  In that
    case the first moment is ``lambda*M0*(x-centroid)``.  A finite-history
    truncation can leave a small, explicitly measurable monopole residual.
    """

    relaxation = _non_negative("memory_relaxation", memory_relaxation)
    if relaxation > 1.0:
        raise ValueError("memory_relaxation must not exceed one")
    target = _non_negative("target_mass", target_mass)
    current = _non_negative("current_mass", current_mass)
    centroid = np.asarray(current_centroid, dtype=float)
    position = np.asarray(deposited_position, dtype=float)
    if centroid.ndim != 1 or position.shape != centroid.shape or centroid.size < 1:
        raise ValueError("centroid and deposited_position must share a non-empty shape")
    if not np.isfinite(centroid).all() or not np.isfinite(position).all():
        raise ValueError("centroid and deposited_position must be finite")
    return MemoryInnovationMoments(
        monopole=float(relaxation * (target - current)),
        first_moment=np.asarray(
            relaxation * (target * position - current * centroid), dtype=float
        ),
    )


def continuity_memory_mode_operator(
    wavenumber: float,
    *,
    memory_relaxation: float,
    flux_relaxation: float,
    stiffness: float,
) -> np.ndarray:
    r"""Return the Fourier operator for one longitudinal ``(rho, j)`` mode.

    The homogeneous proposal is

    ``rho_dot = -lambda*rho - div(j)`` and
    ``j_dot = -gamma*j - stiffness*grad(rho)``.

    For a Fourier mode of magnitude ``k`` its characteristic polynomial is
    ``(s+lambda)(s+gamma)+stiffness*k**2``.
    """

    k = _non_negative("wavenumber", wavenumber)
    relaxation = _non_negative("memory_relaxation", memory_relaxation)
    flux_decay = _non_negative("flux_relaxation", flux_relaxation)
    restoring = _finite("stiffness", stiffness)
    return np.asarray(
        [
            [-relaxation, -1j * k],
            [-1j * restoring * k, -flux_decay],
        ],
        dtype=np.complex128,
    )


def continuity_memory_mode(
    wavenumber: float,
    *,
    memory_relaxation: float,
    flux_relaxation: float,
    stiffness: float,
) -> ContinuityMemoryMode:
    """Classify one exact longitudinal density-flux mode."""

    operator = continuity_memory_mode_operator(
        wavenumber,
        memory_relaxation=memory_relaxation,
        flux_relaxation=flux_relaxation,
        stiffness=stiffness,
    )
    eigenvalues = np.linalg.eigvals(operator)
    order = np.lexsort((eigenvalues.imag, eigenvalues.real))
    roots = eigenvalues[order]
    tolerance = 64.0 * np.finfo(float).eps * max(1.0, float(np.max(np.abs(roots))))
    stable = bool(np.max(roots.real) < -tolerance)
    spectral_abscissa = float(np.max(roots.real))
    marginal = bool(abs(spectral_abscissa) <= tolerance)
    oscillatory = bool(np.max(np.abs(roots.imag)) > tolerance)
    if stable and oscillatory:
        classification = "stable_oscillatory"
    elif stable:
        classification = "stable_real"
    elif marginal and oscillatory:
        classification = "marginal_oscillatory"
    elif marginal:
        classification = "marginal_real"
    else:
        classification = "unstable"
    return ContinuityMemoryMode(
        wavenumber=float(wavenumber),
        eigenvalues=(complex(roots[0]), complex(roots[1])),
        asymptotically_stable=stable,
        oscillatory=oscillatory,
        trace_damping_rate=float(-np.mean(roots.real)),
        angular_frequency=float(np.max(np.abs(roots.imag))),
        classification=classification,
    )


def continuity_oscillation_threshold(
    *, memory_relaxation: float, flux_relaxation: float, stiffness: float
) -> float:
    r"""Return the strict oscillation threshold in ``k``.

    For positive stiffness, modes are complex when
    ``2*sqrt(stiffness)*k > abs(lambda-gamma)``.  Zero stiffness has no finite
    threshold and is represented by infinity.
    """

    relaxation = _non_negative("memory_relaxation", memory_relaxation)
    flux_decay = _non_negative("flux_relaxation", flux_relaxation)
    restoring = _non_negative("stiffness", stiffness)
    if restoring == 0.0:
        return float("inf")
    return float(abs(relaxation - flux_decay) / (2.0 * math.sqrt(restoring)))
