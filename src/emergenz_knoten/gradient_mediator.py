"""Energy-reciprocal gradient mediator proposed beyond canonical scalar memory.

This module does not alter the canonical ``z=(x, rho)`` process.  It describes
an independent longitudinal vector mediator ``m`` and conjugate velocity ``p``.
The interaction energy ``-g <m, grad(q)>`` for a scalar source ``q`` makes field
writing and source readout adjoints.  A point deposit uses ``q=G_x``; the
frozen-knot test uses the complete retained scalar memory as ``q=rho_H``.
Eliminating ``(m,p)`` therefore supplies a ``g**2*k**2`` pair response.  That
numerator does not follow from additive scalar occupancy deposition alone.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Literal

import numpy as np


CouplingGeometry = Literal["gradient_vector", "direct_scalar"]


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


@dataclass(frozen=True)
class GradientMediatorDimensionlessGroups:
    """Natural scales and irreducible ratios of the linear mediator."""

    length_scale: float
    denominator_scale: float
    decay_rate_ratio: float
    spectral_shape: float
    memory_loading: float


@dataclass(frozen=True)
class GradientMediatorSelection:
    """Selected response scale and stability of the gradient mediator."""

    selected_scaled_wavenumber: float
    selected_scaled_wavelength: float
    peak_dimensionless_transfer: float
    constitutive_operator_positive: bool
    statically_stable: bool
    selected_mode_oscillatory: bool
    minimum_dimensionless_denominator: float
    classification: str


@dataclass(frozen=True)
class GradientMediatorInference:
    """Shape groups inferred from a gain-independent local spectral peak."""

    spectral_shape: float
    memory_loading: float


def gradient_mediator_dimensionless_groups(
    *,
    memory_decay: float,
    conjugate_decay: float,
    local_stiffness: float,
    gradient_stiffness: float,
    biharmonic_stiffness: float,
) -> GradientMediatorDimensionlessGroups:
    r"""Reduce the proposed mediator to natural scales and three ratios.

    With ``D(k)=a+b*k**2+c*k**4``, the homogeneous field denominator is

    ``(-i*w+lambda)*(-i*w+gamma)+k**2*D(k)``.

    The natural variables ``ell=(c/a)**(1/4)`` and
    ``S=a**(3/2)/sqrt(c)`` give the static dimensionless denominator
    ``mu+u**2+delta*u**4+u**6`` for ``u=k*ell``.  Because the two decay rates
    enter only through their sum and product, the reported ratio is
    canonically ``max(lambda,gamma)/min(lambda,gamma) >= 1``.
    """

    relaxation = _positive("memory_decay", memory_decay)
    conjugate = _positive("conjugate_decay", conjugate_decay)
    local = _positive("local_stiffness", local_stiffness)
    gradient = _finite("gradient_stiffness", gradient_stiffness)
    biharmonic = _positive("biharmonic_stiffness", biharmonic_stiffness)
    root_ac = math.sqrt(local * biharmonic)
    denominator_scale = local**1.5 / math.sqrt(biharmonic)
    return GradientMediatorDimensionlessGroups(
        length_scale=float((biharmonic / local) ** 0.25),
        denominator_scale=float(denominator_scale),
        decay_rate_ratio=float(max(conjugate, relaxation) / min(conjugate, relaxation)),
        spectral_shape=float(gradient / root_ac),
        memory_loading=float(relaxation * conjugate / denominator_scale),
    )


def dimensionless_gradient_mediator_denominator(
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
    loading = _positive("memory_loading", memory_loading)
    u2 = np.square(u)
    return np.asarray(loading + u2 + delta * np.square(u2) + u2**3, dtype=float)


def gradient_mediator_mode_operator(
    wavenumber: float,
    *,
    memory_decay: float,
    conjugate_decay: float,
    local_stiffness: float,
    gradient_stiffness: float,
    biharmonic_stiffness: float,
) -> np.ndarray:
    r"""Return the homogeneous longitudinal ``(m, p)`` generator.

    The exact characteristic polynomial is
    ``(s+lambda)*(s+gamma)+k**2*D(k)``.  This second-order field has the same
    longitudinal pole polynomial as a density-current balance law, but it is a
    different state and source architecture from canonical occupancy memory.
    """

    k = _finite("wavenumber", wavenumber)
    if k < 0.0:
        raise ValueError("wavenumber must be non-negative")
    groups = gradient_mediator_dimensionless_groups(
        memory_decay=memory_decay,
        conjugate_decay=conjugate_decay,
        local_stiffness=local_stiffness,
        gradient_stiffness=gradient_stiffness,
        biharmonic_stiffness=biharmonic_stiffness,
    )
    del groups
    k2 = k * k
    restoring = (
        memory_decay * conjugate_decay
        + local_stiffness * k2
        + gradient_stiffness * k2**2
        + biharmonic_stiffness * k2**3
    )
    return np.asarray(
        [[0.0, 1.0], [-restoring, -(memory_decay + conjugate_decay)]],
        dtype=float,
    )


def gradient_mediator_source_readout_multipliers(
    wavevector: np.ndarray,
    *,
    coupling: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    r"""Return adjoint write/read multipliers for ``-g<m,grad(q)>``.

    The write multiplier is ``i*g*k`` and its Hilbert adjoint is ``-i*g*k``.
    Their contraction supplies ``g**2*k**2`` after field elimination.
    """

    k = np.asarray(wavevector, dtype=float)
    if k.ndim != 1 or k.size < 1 or not np.isfinite(k).all():
        raise ValueError("wavevector must be a finite non-empty vector")
    gain = _finite("coupling", coupling)
    write = 1j * gain * k
    return np.asarray(write, dtype=complex), np.asarray(write.conj(), dtype=complex)


def gradient_mediator_transfer(
    wavenumber: np.ndarray | float,
    *,
    memory_decay: float,
    conjugate_decay: float,
    local_stiffness: float,
    gradient_stiffness: float,
    biharmonic_stiffness: float,
    coupling: float = 1.0,
    angular_frequency: np.ndarray | float = 0.0,
    coupling_geometry: CouplingGeometry = "gradient_vector",
) -> np.ndarray:
    r"""Return the common-energy source-to-source frequency response.

    ``gradient_vector`` is generated by ``-g<m,grad G_x>`` and has numerator
    ``g**2*k**2``.  ``direct_scalar`` is the corresponding direct-source
    architecture control and has numerator ``g**2``.  They are distinct field
    geometries, not two gain choices within canonical scalar deposition.
    """

    k = np.asarray(wavenumber, dtype=float)
    omega = np.asarray(angular_frequency, dtype=float)
    if not np.isfinite(k).all() or not np.isfinite(omega).all():
        raise ValueError("wavenumber and angular_frequency must be finite")
    if np.any(k < 0.0):
        raise ValueError("wavenumber must be non-negative")
    gradient_mediator_dimensionless_groups(
        memory_decay=memory_decay,
        conjugate_decay=conjugate_decay,
        local_stiffness=local_stiffness,
        gradient_stiffness=gradient_stiffness,
        biharmonic_stiffness=biharmonic_stiffness,
    )
    k2 = np.square(k)
    denominator = (
        (-1j * omega + memory_decay) * (-1j * omega + conjugate_decay)
        + local_stiffness * k2
        + gradient_stiffness * np.square(k2)
        + biharmonic_stiffness * k2**3
    )
    scale = np.maximum(1.0, np.abs(denominator))
    if np.any(np.abs(denominator) <= 64.0 * np.finfo(float).eps * scale):
        raise ValueError("mediator response contains a pole on the requested grid")
    gain = _finite("coupling", coupling)
    if coupling_geometry == "gradient_vector":
        numerator = k2
    elif coupling_geometry == "direct_scalar":
        numerator = np.ones_like(k2)
    else:
        raise ValueError("coupling_geometry must be gradient_vector or direct_scalar")
    return np.asarray(gain * gain * numerator / denominator, dtype=complex)


def gradient_mediator_selection(
    *,
    spectral_shape: float,
    memory_loading: float,
    decay_rate_ratio: float,
) -> GradientMediatorSelection:
    r"""Select the peak of ``u**2/(mu+u**2+delta*u**4+u**6)``.

    No target wavelength is supplied.  The stronger constitutive condition
    ``1+delta*u**2+u**4>0`` for every mode holds exactly when ``delta>-2``.
    """

    delta = _finite("spectral_shape", spectral_shape)
    loading = _positive("memory_loading", memory_loading)
    ratio = _positive("decay_rate_ratio", decay_rate_ratio)
    if ratio < 1.0:
        raise ValueError("decay_rate_ratio must use the canonical ratio >= 1")
    roots = np.roots([2.0, delta, 0.0, -loading])
    positive = [
        float(root.real)
        for root in roots
        if abs(root.imag) < 1.0e-10 and root.real > 0.0
    ]
    if len(positive) != 1:
        raise RuntimeError("gradient response must have one positive peak")
    y_peak = positive[0]
    u_peak = float(math.sqrt(y_peak))
    denominator_at_peak = float(
        dimensionless_gradient_mediator_denominator(
            u_peak,
            spectral_shape=delta,
            memory_loading=loading,
        )
    )

    derivative_roots = np.roots([3.0, 2.0 * delta, 1.0])
    candidates = [0.0]
    candidates.extend(
        float(root.real)
        for root in derivative_roots
        if abs(root.imag) < 1.0e-10 and root.real > 0.0
    )
    minimum = min(loading + y + delta * y * y + y**3 for y in candidates)
    tolerance = 64.0 * np.finfo(float).eps * max(1.0, loading, abs(minimum))
    stable = bool(minimum > tolerance)
    constitutive_positive = bool(delta > -2.0 + tolerance)
    restoring_at_peak = float(y_peak * (1.0 + delta * y_peak + y_peak**2))
    mismatch = float((1.0 - ratio) ** 2 / ratio)
    oscillatory = bool(
        restoring_at_peak > 0.0
        and 4.0 * restoring_at_peak / loading > mismatch
    )
    if not stable:
        classification = "static_instability"
    elif not constitutive_positive:
        classification = "stable_total_operator_with_indefinite_constitutive_part"
    elif oscillatory:
        classification = "stable_selected_oscillatory_mode"
    else:
        classification = "stable_selected_real_mode"
    return GradientMediatorSelection(
        selected_scaled_wavenumber=u_peak,
        selected_scaled_wavelength=float(2.0 * math.pi / u_peak),
        peak_dimensionless_transfer=float(y_peak / denominator_at_peak),
        constitutive_operator_positive=constitutive_positive,
        statically_stable=stable,
        selected_mode_oscillatory=oscillatory,
        minimum_dimensionless_denominator=float(minimum),
        classification=classification,
    )


def infer_gradient_mediator_groups_from_peak(
    *,
    selected_scaled_wavenumber: float,
    log_transfer_curvature_y: float,
) -> GradientMediatorInference:
    r"""Infer ``delta`` and ``mu`` from gain-free peak position and curvature."""

    u_peak = _positive("selected_scaled_wavenumber", selected_scaled_wavenumber)
    curvature = _finite("log_transfer_curvature_y", log_transfer_curvature_y)
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
    return GradientMediatorInference(
        spectral_shape=float(delta),
        memory_loading=float(loading),
    )


def _green_residues(
    *,
    spectral_shape: float,
    memory_loading: float,
    coupling_geometry: CouplingGeometry,
) -> tuple[np.ndarray, np.ndarray]:
    """Return exact Yukawa coefficients and decay poles for the 3D inverse."""

    delta = _finite("spectral_shape", spectral_shape)
    loading = _positive("memory_loading", memory_loading)
    y_roots = np.roots([1.0, delta, 1.0, loading]).astype(complex)
    derivative = 3.0 * y_roots**2 + 2.0 * delta * y_roots + 1.0
    tolerance = 256.0 * np.finfo(float).eps * max(1.0, float(np.max(np.abs(derivative))))
    if np.any(np.abs(derivative) <= tolerance):
        raise ValueError("repeated spectral pole requires a separate Green formula")
    if coupling_geometry == "gradient_vector":
        numerator = y_roots
    elif coupling_geometry == "direct_scalar":
        numerator = np.ones_like(y_roots)
    else:
        raise ValueError("coupling_geometry must be gradient_vector or direct_scalar")
    residues = numerator / derivative
    decay_poles = np.sqrt(-y_roots + 0j)
    decay_poles = np.where(decay_poles.real < 0.0, -decay_poles, decay_poles)
    if np.any(decay_poles.real <= 0.0):
        raise ValueError("static Green function does not decay in real space")
    return residues, decay_poles


def radial_gradient_mediator_green_3d(
    radii: np.ndarray | float,
    *,
    spectral_shape: float,
    memory_loading: float,
    coupling_geometry: CouplingGeometry = "gradient_vector",
) -> np.ndarray:
    r"""Return the exact dimensionless isotropic 3D static Green function.

    The rational spectrum is decomposed into three Yukawa terms.  This avoids
    a finite Fourier cutoff.  The removable ``r=0`` singularity is evaluated
    analytically from cancellation of the residues.
    """

    radius = np.asarray(radii, dtype=float)
    if not np.isfinite(radius).all() or np.any(radius < 0.0):
        raise ValueError("radii must be finite and non-negative")
    residues, poles = _green_residues(
        spectral_shape=spectral_shape,
        memory_loading=memory_loading,
        coupling_geometry=coupling_geometry,
    )
    flat = radius.reshape(-1)
    result = np.empty_like(flat)
    zero = flat == 0.0
    result[zero] = float(np.real(-np.sum(residues * poles) / (4.0 * np.pi)))
    positive = ~zero
    if np.any(positive):
        r = flat[positive, None]
        values = np.sum(
            residues[None, :] * np.expm1(-r * poles[None, :]), axis=1
        )
        result[positive] = np.real(values / (4.0 * np.pi * flat[positive]))
    return np.asarray(result.reshape(radius.shape), dtype=float)


def radial_gradient_mediator_green_derivative_3d(
    radii: np.ndarray | float,
    *,
    spectral_shape: float,
    memory_loading: float,
    coupling_geometry: CouplingGeometry = "gradient_vector",
) -> np.ndarray:
    """Return the exact outward radial derivative ``dK/dr`` for ``r>0``."""

    radius = np.asarray(radii, dtype=float)
    if not np.isfinite(radius).all() or np.any(radius <= 0.0):
        raise ValueError("radii must be finite and strictly positive")
    residues, poles = _green_residues(
        spectral_shape=spectral_shape,
        memory_loading=memory_loading,
        coupling_geometry=coupling_geometry,
    )
    flat = radius.reshape(-1)
    r = flat[:, None]
    scaled = r * poles[None, :]
    values = np.sum(
        residues[None, :]
        * (-scaled * np.exp(-scaled) - np.expm1(-scaled)),
        axis=1,
    )
    return np.asarray(
        np.real(values / (4.0 * np.pi * np.square(flat))).reshape(radius.shape),
        dtype=float,
    )


def gradient_mediator_homogeneous_energy_rate(
    conjugate_velocity: np.ndarray | complex | float,
    *,
    memory_decay: float,
    conjugate_decay: float,
) -> np.ndarray:
    r"""Return ``-(lambda+gamma)*|p|**2`` for a fixed source."""

    velocity = np.asarray(conjugate_velocity, dtype=complex)
    if not np.isfinite(velocity).all():
        raise ValueError("conjugate_velocity must be finite")
    damping = _positive("memory_decay", memory_decay) + _positive(
        "conjugate_decay", conjugate_decay
    )
    return np.asarray(-damping * np.square(np.abs(velocity)), dtype=float)
