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
    decay_rate: float
    angular_frequency: float
    classification: str


@dataclass(frozen=True)
class ContinuityKernelDimensionlessGroups:
    """Natural scales and irreducible ratios of the local density-flux law."""

    length_scale: float
    denominator_scale: float
    flux_relaxation_ratio: float
    spectral_shape: float
    memory_loading: float


@dataclass(frozen=True)
class ContinuityKernelSelection:
    """Selected response scale and stability of a reciprocal gradient channel."""

    selected_scaled_wavenumber: float
    selected_scaled_wavelength: float
    peak_dimensionless_transfer: float
    constitutive_energy_positive: bool
    statically_stable: bool
    selected_mode_oscillatory: bool
    minimum_dimensionless_denominator: float
    classification: str


@dataclass(frozen=True)
class ContinuityKernelInference:
    """Shape groups inferred from a gain-independent local spectral peak."""

    spectral_shape: float
    memory_loading: float


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
    marginal = bool(np.max(np.abs(roots.real)) <= tolerance)
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
        decay_rate=float(-np.mean(roots.real)),
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


def continuity_kernel_dimensionless_groups(
    *,
    memory_relaxation: float,
    flux_relaxation: float,
    local_stiffness: float,
    gradient_stiffness: float,
    biharmonic_stiffness: float,
) -> ContinuityKernelDimensionlessGroups:
    r"""Reduce the local density-flux kernel to scales and three ratios.

    With ``D(k)=a+b*k**2+c*k**4``, use
    ``ell=(c/a)**(1/4)`` and ``S=a**(3/2)/sqrt(c)``.  The dimensionless static
    denominator is ``mu+u**2+delta*u**4+u**6`` for ``u=k*ell``.
    """

    relaxation = _finite("memory_relaxation", memory_relaxation)
    flux_decay = _finite("flux_relaxation", flux_relaxation)
    local = _finite("local_stiffness", local_stiffness)
    gradient = _finite("gradient_stiffness", gradient_stiffness)
    biharmonic = _finite("biharmonic_stiffness", biharmonic_stiffness)
    if relaxation <= 0.0 or flux_decay <= 0.0:
        raise ValueError("memory and flux relaxation must be positive")
    if local <= 0.0 or biharmonic <= 0.0:
        raise ValueError("local and biharmonic stiffness must be positive")
    root_ac = math.sqrt(local * biharmonic)
    denominator_scale = local ** 1.5 / math.sqrt(biharmonic)
    return ContinuityKernelDimensionlessGroups(
        length_scale=float((biharmonic / local) ** 0.25),
        denominator_scale=float(denominator_scale),
        flux_relaxation_ratio=float(flux_decay / relaxation),
        spectral_shape=float(gradient / root_ac),
        memory_loading=float(relaxation * flux_decay / denominator_scale),
    )


def dimensionless_continuity_kernel_denominator(
    scaled_wavenumber: np.ndarray | float,
    *,
    spectral_shape: float,
    memory_loading: float,
) -> np.ndarray:
    """Return ``mu+u**2+delta*u**4+u**6``."""

    u = np.asarray(scaled_wavenumber, dtype=float)
    if not np.isfinite(u).all() or np.any(u < 0.0):
        raise ValueError("scaled_wavenumber must be finite and non-negative")
    delta = _finite("spectral_shape", spectral_shape)
    loading = _non_negative("memory_loading", memory_loading)
    u2 = np.square(u)
    return np.asarray(loading + u2 + delta * np.square(u2) + u2**3, dtype=float)


def reciprocal_continuity_kernel_transfer(
    wavenumber: np.ndarray | float,
    *,
    memory_relaxation: float,
    flux_relaxation: float,
    local_stiffness: float,
    gradient_stiffness: float,
    biharmonic_stiffness: float,
    coupling: float = 1.0,
    gradient_coupling: bool = True,
) -> np.ndarray:
    r"""Return the static common-energy effective kernel in Fourier space.

    A single interaction coefficient enters quadratically because write and
    readout are adjoints.  Gradient coupling contributes ``k**2`` and hence an
    exact zero mode; direct scalar coupling contributes one.  The function
    raises when the requested Fourier grid contains a non-positive static
    denominator.
    """

    k = np.asarray(wavenumber, dtype=float)
    if not np.isfinite(k).all():
        raise ValueError("wavenumber must be finite")
    groups = continuity_kernel_dimensionless_groups(
        memory_relaxation=memory_relaxation,
        flux_relaxation=flux_relaxation,
        local_stiffness=local_stiffness,
        gradient_stiffness=gradient_stiffness,
        biharmonic_stiffness=biharmonic_stiffness,
    )
    k2 = np.square(k)
    denominator = (
        memory_relaxation * flux_relaxation
        + local_stiffness * k2
        + gradient_stiffness * np.square(k2)
        + biharmonic_stiffness * k2**3
    )
    if np.any(denominator <= 0.0):
        raise ValueError("static density-flux kernel is not positive")
    gain = _finite("coupling", coupling)
    numerator = k2 if gradient_coupling else np.ones_like(k2)
    response = gain * gain * numerator / denominator
    if groups.denominator_scale <= 0.0:  # pragma: no cover - construction guard
        raise RuntimeError("invalid denominator scale")
    return np.asarray(response, dtype=float)


def continuity_kernel_selection(
    *,
    spectral_shape: float,
    memory_loading: float,
    flux_relaxation_ratio: float,
) -> ContinuityKernelSelection:
    r"""Select the peak of the reciprocal gradient-coupled susceptibility.

    For ``H(u)=u**2/(mu+u**2+delta*u**4+u**6)``, the positive peak solves
    ``2*y**3+delta*y**2-mu=0`` with ``y=u**2``.  No target wavelength is
    supplied.  The constitutive stiffness ``1+delta*u**2+u**4`` is positive
    for every mode exactly when ``delta>-2``.
    """

    delta = _finite("spectral_shape", spectral_shape)
    loading = _finite("memory_loading", memory_loading)
    ratio = _finite("flux_relaxation_ratio", flux_relaxation_ratio)
    if loading <= 0.0 or ratio <= 0.0:
        raise ValueError("memory loading and flux relaxation ratio must be positive")

    roots = np.roots([2.0, delta, 0.0, -loading])
    positive = [float(root.real) for root in roots if abs(root.imag) < 1.0e-10 and root.real > 0.0]
    if len(positive) != 1:
        raise RuntimeError("gradient-coupled response must have one positive peak")
    y_peak = positive[0]
    u_peak = float(math.sqrt(y_peak))
    denominator_at_peak = float(
        dimensionless_continuity_kernel_denominator(
            u_peak,
            spectral_shape=delta,
            memory_loading=loading,
        )
    )
    peak_transfer = float(y_peak / denominator_at_peak)

    derivative_roots = np.roots([3.0, 2.0 * delta, 1.0])
    candidates = [0.0]
    candidates.extend(
        float(root.real)
        for root in derivative_roots
        if abs(root.imag) < 1.0e-10 and root.real > 0.0
    )
    minimum = min(
        float(loading + y + delta * y * y + y**3) for y in candidates
    )
    tolerance = 64.0 * np.finfo(float).eps * max(1.0, loading, abs(minimum))
    stable = bool(minimum > tolerance)
    constitutive_positive = bool(delta > -2.0 + tolerance)
    stiffness_at_peak = float(y_peak * (1.0 + delta * y_peak + y_peak**2))
    mismatch = float((1.0 - ratio) ** 2 / ratio)
    oscillatory = bool(stiffness_at_peak > 0.0 and 4.0 * stiffness_at_peak / loading > mismatch)

    if not stable:
        classification = "static_instability"
    elif not constitutive_positive:
        classification = "stable_response_with_indefinite_constitutive_energy"
    elif oscillatory:
        classification = "stable_selected_oscillatory_mode"
    else:
        classification = "stable_selected_real_mode"
    return ContinuityKernelSelection(
        selected_scaled_wavenumber=u_peak,
        selected_scaled_wavelength=float(2.0 * math.pi / u_peak),
        peak_dimensionless_transfer=peak_transfer,
        constitutive_energy_positive=constitutive_positive,
        statically_stable=stable,
        selected_mode_oscillatory=oscillatory,
        minimum_dimensionless_denominator=minimum,
        classification=classification,
    )


def infer_continuity_kernel_groups_from_peak(
    *,
    selected_scaled_wavenumber: float,
    log_transfer_curvature_y: float,
) -> ContinuityKernelInference:
    r"""Infer ``delta`` and ``mu`` from peak position and log curvature.

    The curvature is the second derivative of ``log H`` with respect to
    ``y=u**2`` at the maximum of
    ``H(y)=y/(mu+y+delta*y**2+y**3)``.  It is independent of an unknown
    multiplicative response gain.  This is an effective-parameter estimator,
    not a microscopic law that generates the coefficients.
    """

    u_peak = _finite("selected_scaled_wavenumber", selected_scaled_wavenumber)
    curvature = _finite("log_transfer_curvature_y", log_transfer_curvature_y)
    if u_peak <= 0.0:
        raise ValueError("selected_scaled_wavenumber must be positive")
    if curvature >= 0.0:
        raise ValueError("log_transfer_curvature_y must be negative at a peak")
    y_peak = u_peak * u_peak
    sharpness = -curvature
    denominator = 2.0 * (sharpness * y_peak * y_peak - 1.0)
    tolerance = 64.0 * np.finfo(float).eps * max(1.0, abs(denominator))
    if abs(denominator) <= tolerance:
        raise ValueError("peak position and curvature do not identify spectral shape")
    delta = y_peak * (
        6.0 - sharpness * (1.0 + 3.0 * y_peak * y_peak)
    ) / denominator
    loading = 2.0 * y_peak**3 + delta * y_peak**2
    if loading <= 0.0:
        raise ValueError("inferred memory loading is not positive")
    return ContinuityKernelInference(
        spectral_shape=float(delta),
        memory_loading=float(loading),
    )
