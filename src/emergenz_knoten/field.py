"""Minimal scalar-field bridge for kernel-mediated memory dynamics.

The current Gaussian kernel can be represented exactly as a heat-flow
propagator in an auxiliary diffusion coordinate. A local relaxation-diffusion
mediator has a different stationary Green function. This module keeps those
two statements explicit instead of identifying them implicitly.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def _positive(name: str, value: float) -> float:
    number = float(value)
    if not np.isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be positive")
    return number


def _finite(name: str, value: float) -> float:
    number = float(value)
    if not np.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _non_negative(name: str, value: float) -> float:
    number = _finite(name, value)
    if number < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return number


@dataclass(frozen=True)
class RelaxationDiffusionField:
    """Parameters of ``tau*d_t phi=D*Delta phi-mu*phi+g*source``."""

    diffusivity: float
    decay_rate: float
    coupling: float = 1.0
    relaxation_time: float = 1.0

    def __post_init__(self) -> None:
        _positive("diffusivity", self.diffusivity)
        _positive("decay_rate", self.decay_rate)
        _positive("relaxation_time", self.relaxation_time)
        if not np.isfinite(self.coupling):
            raise ValueError("coupling must be finite")

    @property
    def correlation_length(self) -> float:
        """Return the stationary field length ``sqrt(D/mu)``."""

        return float(np.sqrt(self.diffusivity / self.decay_rate))

    @property
    def zero_mode_gain(self) -> float:
        """Return the stationary response at wave number zero."""

        return float(self.coupling / self.decay_rate)


@dataclass(frozen=True)
class FieldLinearStability:
    """Linear stability classification of a local scalar field expansion."""

    stable: bool
    high_wavenumber_stable: bool
    finite_wavenumber_preference: bool
    preferred_wavenumber: float
    minimum_denominator: float
    classification: str


@dataclass(frozen=True)
class LocalScalarFieldExpansion:
    r"""Lowest even-derivative local scalar field family used by the project.

    The deterministic field law is

    ``tau*d_t phi = -c0*phi + c2*Delta phi - c4*Delta^2 phi``
    ``              - v*phi^2 - u*phi^3 + s0*rho - s2*Delta rho``.

    Its linear stationary transfer is

    ``(s0+s2*k^2)/(c0+c2*k^2+c4*k^4)``.

    Spatial parity does not forbid the quadratic local term. Setting it to zero
    is an additional internal sign-symmetry choice, not an inherited model
    assumption. Neither local nonlinear term alters the linear transfer or
    stability margin around ``phi=0``.
    """

    mass_coefficient: float
    gradient_coefficient: float
    biharmonic_coefficient: float = 0.0
    source_coefficient: float = 1.0
    source_laplacian_coefficient: float = 0.0
    quadratic_nonlinearity: float = 0.0
    cubic_saturation: float = 0.0
    relaxation_time: float = 1.0

    def __post_init__(self) -> None:
        _finite("mass_coefficient", self.mass_coefficient)
        _finite("gradient_coefficient", self.gradient_coefficient)
        _non_negative("biharmonic_coefficient", self.biharmonic_coefficient)
        _finite("source_coefficient", self.source_coefficient)
        _finite(
            "source_laplacian_coefficient",
            self.source_laplacian_coefficient,
        )
        _finite("quadratic_nonlinearity", self.quadratic_nonlinearity)
        _non_negative("cubic_saturation", self.cubic_saturation)
        _positive("relaxation_time", self.relaxation_time)

    @property
    def zero_mode_gain(self) -> float:
        if self.mass_coefficient == 0.0:
            raise ValueError("zero-mode gain is singular for zero mass coefficient")
        return float(self.source_coefficient / self.mass_coefficient)

    @property
    def zero_mean_linear_response(self) -> bool:
        """Whether the regular stationary response vanishes at ``k=0``."""

        return self.mass_coefficient != 0.0 and self.source_coefficient == 0.0

    def linear_stability(self) -> FieldLinearStability:
        """Classify ``c0+c2*k^2+c4*k^4`` over real wave numbers."""

        c0 = float(self.mass_coefficient)
        c2 = float(self.gradient_coefficient)
        c4 = float(self.biharmonic_coefficient)
        if c4 == 0.0 and c2 < 0.0:
            return FieldLinearStability(
                stable=False,
                high_wavenumber_stable=False,
                finite_wavenumber_preference=False,
                preferred_wavenumber=float("inf"),
                minimum_denominator=float("-inf"),
                classification="ultraviolet_unstable",
            )

        if c4 > 0.0 and c2 < 0.0:
            preferred_squared = -c2 / (2.0 * c4)
            preferred = float(np.sqrt(preferred_squared))
            minimum = float(c0 - c2 * c2 / (4.0 * c4))
            finite_preference = True
        else:
            preferred = 0.0
            minimum = c0
            finite_preference = False

        scale = max(1.0, abs(c0), abs(minimum))
        tolerance = float(32.0 * np.finfo(float).eps * scale)
        stable = bool(minimum > tolerance)
        critical = bool(abs(minimum) <= tolerance)
        if stable and finite_preference:
            classification = "stable_finite_wavenumber_minimum"
        elif stable:
            classification = "stable_monotone"
        elif critical and finite_preference:
            classification = "critical_finite_wavenumber"
        elif critical:
            classification = "critical_zero_mode"
        elif finite_preference:
            classification = "finite_wavenumber_instability"
        else:
            classification = "zero_mode_instability"
        return FieldLinearStability(
            stable=stable,
            high_wavenumber_stable=(c4 > 0.0 or c2 > 0.0 or c0 > 0.0),
            finite_wavenumber_preference=finite_preference,
            preferred_wavenumber=preferred,
            minimum_denominator=float(minimum),
            classification=classification,
        )


def local_scalar_operator_denominator(
    wavenumber: np.ndarray | float,
    field: LocalScalarFieldExpansion,
) -> np.ndarray:
    """Return ``c0+c2*k^2+c4*k^4`` for a local scalar expansion."""

    k = np.asarray(wavenumber, dtype=float)
    if not np.isfinite(k).all():
        raise ValueError("wavenumber must be finite")
    k2 = np.square(k)
    return np.asarray(
        field.mass_coefficient
        + field.gradient_coefficient * k2
        + field.biharmonic_coefficient * np.square(k2),
        dtype=float,
    )


def local_scalar_source_multiplier(
    wavenumber: np.ndarray | float,
    field: LocalScalarFieldExpansion,
) -> np.ndarray:
    """Return ``s0+s2*k^2`` for the local source expansion."""

    k = np.asarray(wavenumber, dtype=float)
    if not np.isfinite(k).all():
        raise ValueError("wavenumber must be finite")
    return np.asarray(
        field.source_coefficient
        + field.source_laplacian_coefficient * np.square(k),
        dtype=float,
    )


def local_scalar_stationary_transfer(
    wavenumber: np.ndarray | float,
    field: LocalScalarFieldExpansion,
    *,
    normalize_zero_mode: bool = False,
) -> np.ndarray:
    """Return the stationary transfer of the local scalar operator family."""

    denominator = local_scalar_operator_denominator(wavenumber, field)
    if np.any(denominator == 0.0):
        raise ValueError("stationary transfer is singular at the requested mode")
    response = local_scalar_source_multiplier(wavenumber, field) / denominator
    if normalize_zero_mode:
        gain = field.zero_mode_gain
        if gain == 0.0:
            raise ValueError("cannot normalize a zero-mean response at k=0")
        response = response / gain
    return np.asarray(response, dtype=float)


def local_scalar_frequency_response(
    wavenumber: np.ndarray | float,
    angular_frequency: np.ndarray | float,
    field: LocalScalarFieldExpansion,
) -> np.ndarray:
    """Return the linear ``(k, omega)`` response of the local scalar law."""

    k, omega = np.broadcast_arrays(
        np.asarray(wavenumber, dtype=float),
        np.asarray(angular_frequency, dtype=float),
    )
    if not np.isfinite(k).all() or not np.isfinite(omega).all():
        raise ValueError("wavenumber and angular_frequency must be finite")
    denominator = local_scalar_operator_denominator(k, field) - 1j * (
        field.relaxation_time * omega
    )
    if np.any(np.abs(denominator) == 0.0):
        raise ValueError("frequency response is singular at the requested mode")
    numerator = local_scalar_source_multiplier(k, field)
    return np.asarray(numerator / denominator, dtype=np.complex128)


def gaussian_matched_local_expansion(
    *,
    gaussian_length: float,
    mass_coefficient: float = 1.0,
    source_coefficient: float = 1.0,
    relaxation_time: float = 1.0,
) -> LocalScalarFieldExpansion:
    """Match a normalized Gaussian transfer through order ``k^4``.

    ``1/(1+a*k^2+b*k^4)`` matches ``exp(-L^2*k^2/2)`` through ``k^4`` for
    ``a=L^2/2`` and ``b=L^4/8``.
    """

    length = _positive("gaussian_length", gaussian_length)
    mass = _positive("mass_coefficient", mass_coefficient)
    return LocalScalarFieldExpansion(
        mass_coefficient=mass,
        gradient_coefficient=mass * length**2 / 2.0,
        biharmonic_coefficient=mass * length**4 / 8.0,
        source_coefficient=_finite("source_coefficient", source_coefficient),
        relaxation_time=relaxation_time,
    )


def relaxation_diffusion_local_expansion(
    field: RelaxationDiffusionField,
) -> LocalScalarFieldExpansion:
    """Embed the existing relaxation-diffusion field in the operator family."""

    return LocalScalarFieldExpansion(
        mass_coefficient=field.decay_rate,
        gradient_coefficient=field.diffusivity,
        source_coefficient=field.coupling,
        relaxation_time=field.relaxation_time,
    )


def isotropic_ambient_transfer_matrix(
    response: np.ndarray | complex | float,
    *,
    dimension: int,
) -> np.ndarray:
    """Return ``H I_d`` for independent identical ambient field components."""

    if isinstance(dimension, bool) or not isinstance(dimension, (int, np.integer)):
        raise ValueError("dimension must be an integer")
    if dimension < 1:
        raise ValueError("dimension must be positive")
    value = np.asarray(response, dtype=np.complex128)
    if not np.isfinite(value).all():
        raise ValueError("response must be finite")
    return value[..., None, None] * np.eye(int(dimension), dtype=np.complex128)


def propagate_isotropic_ambient_covariance(
    source_covariance: np.ndarray,
    response: complex | float,
) -> np.ndarray:
    """Propagate covariance through ``H I_d``; nonzero ``H`` preserves rank."""

    covariance = np.asarray(source_covariance, dtype=np.complex128)
    if covariance.ndim != 2 or covariance.shape[0] != covariance.shape[1]:
        raise ValueError("source_covariance must be a square matrix")
    if not np.isfinite(covariance).all():
        raise ValueError("source_covariance must be finite")
    value = complex(response)
    if not np.isfinite(value):
        raise ValueError("response must be finite")
    return np.asarray(abs(value) ** 2 * covariance, dtype=np.complex128)


def gaussian_transfer(wavenumber: np.ndarray, *, length: float) -> np.ndarray:
    """Return the zero-mode-normalized Gaussian Fourier multiplier."""

    scale = _positive("length", length)
    k = np.asarray(wavenumber, dtype=float)
    if not np.isfinite(k).all():
        raise ValueError("wavenumber must be finite")
    return np.exp(-0.5 * np.square(scale * k))


def heat_transfer(
    wavenumber: np.ndarray,
    *,
    diffusivity: float,
    diffusion_time: float,
) -> np.ndarray:
    """Return the Fourier multiplier generated by a heat equation."""

    diffusivity = _positive("diffusivity", diffusivity)
    diffusion_time = _positive("diffusion_time", diffusion_time)
    k = np.asarray(wavenumber, dtype=float)
    if not np.isfinite(k).all():
        raise ValueError("wavenumber must be finite")
    return np.exp(-diffusivity * diffusion_time * np.square(k))


def gaussian_heat_time(*, length: float, diffusivity: float = 1.0) -> float:
    """Return the heat time whose propagator has Gaussian width ``length``."""

    length = _positive("length", length)
    diffusivity = _positive("diffusivity", diffusivity)
    return float(length * length / (2.0 * diffusivity))


def stationary_field_transfer(
    wavenumber: np.ndarray,
    field: RelaxationDiffusionField,
    *,
    normalize_zero_mode: bool = False,
) -> np.ndarray:
    """Return the stationary Green multiplier ``g/(mu+D*k^2)``."""

    k = np.asarray(wavenumber, dtype=float)
    if not np.isfinite(k).all():
        raise ValueError("wavenumber must be finite")
    response = field.coupling / (field.decay_rate + field.diffusivity * np.square(k))
    if normalize_zero_mode:
        if field.zero_mode_gain == 0.0:
            raise ValueError("cannot normalize a field with zero coupling")
        response = response / field.zero_mode_gain
    return np.asarray(response, dtype=float)


def low_wavenumber_matched_field(
    *,
    gaussian_length: float,
    decay_rate: float = 1.0,
    coupling: float = 1.0,
    relaxation_time: float = 1.0,
) -> RelaxationDiffusionField:
    """Match the Gaussian and stationary field through order ``k^2``.

    ``exp(-L^2 k^2/2)`` and ``1/(1+L_phi^2 k^2)`` have equal quadratic
    terms for ``L_phi=L/sqrt(2)``.
    """

    gaussian_length = _positive("gaussian_length", gaussian_length)
    decay_rate = _positive("decay_rate", decay_rate)
    return RelaxationDiffusionField(
        diffusivity=decay_rate * gaussian_length**2 / 2.0,
        decay_rate=decay_rate,
        coupling=coupling,
        relaxation_time=relaxation_time,
    )
