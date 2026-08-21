"""Exact rotating-wave balances for the native scalar finite-memory map."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import math

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import roots_legendre


@dataclass(frozen=True)
class RotatingWaveComponents:
    """Radial and tangential history sums in the co-rotating frame."""

    radial: float
    tangential: float


@dataclass(frozen=True)
class FiniteRotatingWaveBalance:
    """Gain compatibility of one finite-memory circle geometry."""

    components: RotatingWaveComponents
    radial_eta: float
    tangential_eta: float
    compatibility_residual: float
    admissible_positive_eta: bool


@dataclass(frozen=True)
class ContinuumRotatingWaveBalance:
    """Fixed-gain continuum balance and its analytic two-variable Jacobian."""

    components: RotatingWaveComponents
    residual: tuple[float, float]
    jacobian: tuple[tuple[float, float], tuple[float, float]]
    required_eta_per_alpha: float


def _positive_finite(name: str, value: float) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be positive and finite")
    return number


def _nonnegative_finite(name: str, value: float) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be non-negative and finite")
    return number


def _kernel_parameters(
    *,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float,
    amplitude_att: float,
) -> tuple[float, float, float, float]:
    rep_sigma = _positive_finite("sigma_rep", sigma_rep)
    att_sigma = _positive_finite("sigma_att", sigma_att)
    rep_amplitude = _nonnegative_finite("amplitude_rep", amplitude_rep)
    att_amplitude = _nonnegative_finite("amplitude_att", amplitude_att)
    return rep_sigma, att_sigma, rep_amplitude, att_amplitude


def double_gaussian_gradient_factor(
    radius: float | np.ndarray,
    *,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float = 1.0,
    amplitude_att: float = 0.35,
) -> float | np.ndarray:
    r"""Return phi(r) for grad K(d)=phi(norm(d)) d.

    The kernel convention is
    K=A_rep exp(-r^2/(2 sigma_rep^2))
      -A_att exp(-r^2/(2 sigma_att^2)).
    Negative phi gives outward drift under the native update x <- x-eta grad K.
    """

    rep_sigma, att_sigma, rep_amplitude, att_amplitude = _kernel_parameters(
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
    )
    radii = np.asarray(radius, dtype=float)
    if np.any(~np.isfinite(radii)) or np.any(radii < 0.0):
        raise ValueError("radius must be finite and non-negative")
    rep = (
        -rep_amplitude / rep_sigma**2 * np.exp(-(radii * radii) / (2.0 * rep_sigma**2))
    )
    att = att_amplitude / att_sigma**2 * np.exp(-(radii * radii) / (2.0 * att_sigma**2))
    result = rep + att
    return float(result) if result.ndim == 0 else result


def double_gaussian_force_crossing_radius(
    *,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float = 1.0,
    amplitude_att: float,
) -> float | None:
    """Return the positive radius at which the radial force changes sign."""

    rep_sigma, att_sigma, rep_amplitude, att_amplitude = _kernel_parameters(
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
    )
    if att_sigma <= rep_sigma or rep_amplitude == 0.0 or att_amplitude == 0.0:
        return None
    numerator = 2.0 * math.log(
        (rep_amplitude * att_sigma**2) / (att_amplitude * rep_sigma**2)
    )
    denominator = 1.0 / rep_sigma**2 - 1.0 / att_sigma**2
    radius_squared = numerator / denominator
    if radius_squared <= 0.0 or not math.isfinite(radius_squared):
        return None
    return float(math.sqrt(radius_squared))


def finite_h_rotating_wave_components(
    *,
    radius: float,
    theta: float,
    alpha: float,
    horizon: int,
    memory_mass: float,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float = 1.0,
    amplitude_att: float,
) -> RotatingWaveComponents:
    """Return exact finite-H radial and tangential history sums."""

    orbit_radius = _positive_finite("radius", radius)
    angle = _positive_finite("theta", theta)
    if angle >= math.pi:
        raise ValueError("theta must lie strictly between zero and pi")
    forgetting = _positive_finite("alpha", alpha)
    if forgetting >= 1.0:
        raise ValueError("alpha must be smaller than one")
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 1:
        raise ValueError("horizon must be a positive integer")
    mass = _positive_finite("memory_mass", memory_mass)
    _kernel_parameters(
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
    )

    if horizon == 1:
        return RotatingWaveComponents(radial=0.0, tangential=0.0)
    ages = np.arange(1, horizon, dtype=float)
    phases = angle * ages
    chord_radii = 2.0 * orbit_radius * np.abs(np.sin(0.5 * phases))
    gradient_factor = np.asarray(
        double_gaussian_gradient_factor(
            chord_radii,
            sigma_rep=sigma_rep,
            sigma_att=sigma_att,
            amplitude_rep=amplitude_rep,
            amplitude_att=amplitude_att,
        )
    )
    weights = forgetting * mass * np.power(1.0 - forgetting, ages)
    radial = np.sum(weights * gradient_factor * (1.0 - np.cos(phases)))
    tangential = np.sum(weights * gradient_factor * np.sin(phases))
    return RotatingWaveComponents(
        radial=float(radial),
        tangential=float(tangential),
    )


def finite_h_rotating_wave_balance(
    *,
    radius: float,
    theta: float,
    alpha: float,
    horizon: int,
    memory_mass: float,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float = 1.0,
    amplitude_att: float,
) -> FiniteRotatingWaveBalance:
    """Return the two independently required eta values and compatibility."""

    components = finite_h_rotating_wave_components(
        radius=radius,
        theta=theta,
        alpha=alpha,
        horizon=horizon,
        memory_mass=memory_mass,
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
    )
    angle = float(theta)
    radial_eta = (
        (1.0 - math.cos(angle)) / components.radial
        if components.radial != 0.0
        else math.inf
    )
    tangential_eta = (
        -math.sin(angle) / components.tangential
        if components.tangential != 0.0
        else math.inf
    )
    compatibility = (
        components.radial * math.sin(angle)
        + (1.0 - math.cos(angle)) * components.tangential
    )
    return FiniteRotatingWaveBalance(
        components=components,
        radial_eta=float(radial_eta),
        tangential_eta=float(tangential_eta),
        compatibility_residual=float(compatibility),
        admissible_positive_eta=bool(
            components.radial > 0.0
            and components.tangential < 0.0
            and radial_eta > 0.0
            and tangential_eta > 0.0
        ),
    )


def finite_h_rotating_wave_residual(
    *,
    eta: float,
    **parameters: float | int,
) -> complex:
    """Return the exact complex one-update residual of a circular history."""

    gain = _positive_finite("eta", eta)
    components = finite_h_rotating_wave_components(**parameters)
    angle = float(parameters["theta"])
    return complex(
        math.cos(angle) - 1.0 + gain * components.radial,
        math.sin(angle) + gain * components.tangential,
    )


@lru_cache(maxsize=None)
def _legendre_rule(
    order: int,
    backend: str = "numpy",
) -> tuple[np.ndarray, np.ndarray]:
    if isinstance(order, bool) or not isinstance(order, int) or order < 16:
        raise ValueError("quadrature_order must be an integer of at least 16")
    if backend == "numpy":
        nodes, weights = leggauss(order)
    elif backend == "scipy":
        nodes, weights = roots_legendre(order)
    else:
        raise ValueError("quadrature_backend must be 'numpy' or 'scipy'")
    nodes = np.asarray(nodes, dtype=float)
    weights = np.asarray(weights, dtype=float)
    nodes.setflags(write=False)
    weights.setflags(write=False)
    return nodes, weights


def continuum_rotating_wave_components(
    *,
    radius: float,
    angular_frequency: float,
    tail_extent: float,
    memory_mass: float,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float = 1.0,
    amplitude_att: float,
    quadrature_order: int = 512,
    quadrature_backend: str = "numpy",
) -> RotatingWaveComponents:
    """Return the matched small-step continuum radial and tangential integrals."""

    orbit_radius = _positive_finite("radius", radius)
    omega = _positive_finite("angular_frequency", angular_frequency)
    extent = _positive_finite("tail_extent", tail_extent)
    mass = _positive_finite("memory_mass", memory_mass)
    _kernel_parameters(
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
    )
    nodes, weights = _legendre_rule(quadrature_order, quadrature_backend)
    times = 0.5 * extent * (nodes + 1.0)
    integration_weights = 0.5 * extent * weights
    phases = omega * times
    chord_radii = 2.0 * orbit_radius * np.abs(np.sin(0.5 * phases))
    gradient_factor = np.asarray(
        double_gaussian_gradient_factor(
            chord_radii,
            sigma_rep=sigma_rep,
            sigma_att=sigma_att,
            amplitude_rep=amplitude_rep,
            amplitude_att=amplitude_att,
        )
    )
    memory_weights = mass * np.exp(-times) * integration_weights
    radial = np.sum(memory_weights * gradient_factor * (1.0 - np.cos(phases)))
    tangential = np.sum(memory_weights * gradient_factor * np.sin(phases))
    return RotatingWaveComponents(
        radial=float(radial),
        tangential=float(tangential),
    )


def continuum_rotating_wave_balance(
    *,
    radius: float,
    angular_frequency: float,
    eta_per_alpha: float,
    tail_extent: float,
    memory_mass: float,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float = 1.0,
    amplitude_att: float,
    quadrature_order: int = 512,
    quadrature_backend: str = "numpy",
) -> ContinuumRotatingWaveBalance:
    r"""Return the fixed-gain continuum equations and analytic Jacobian.

    With ``u(t)=1-cos(Omega*t)`` and ``q(t)=R**2*u(t)``, the chord obeys
    ``r(t)**2=2*q(t)``.  This avoids the removable absolute-value cusp in
    ``2*R*abs(sin(Omega*t/2))``.  The two equations are

    ``F_R = I_R`` and ``F_T = Omega + eta_hat*I_T``.

    They are the leading small-step limits of the two native finite-memory
    update components; no oscillator or inertial term is introduced.
    """

    orbit_radius = _positive_finite("radius", radius)
    omega = _positive_finite("angular_frequency", angular_frequency)
    gain_rate = _positive_finite("eta_per_alpha", eta_per_alpha)
    extent = _positive_finite("tail_extent", tail_extent)
    mass = _positive_finite("memory_mass", memory_mass)
    rep_sigma, att_sigma, rep_amplitude, att_amplitude = _kernel_parameters(
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
    )
    nodes, weights = _legendre_rule(quadrature_order, quadrature_backend)
    times = 0.5 * extent * (nodes + 1.0)
    integration_weights = 0.5 * extent * weights
    phases = omega * times
    phase_sine = np.sin(phases)
    phase_cosine = np.cos(phases)
    radial_chord_factor = 1.0 - phase_cosine
    q = orbit_radius**2 * radial_chord_factor

    rep_exponential = np.exp(-q / rep_sigma**2)
    att_exponential = np.exp(-q / att_sigma**2)
    gradient_factor = (
        -rep_amplitude / rep_sigma**2 * rep_exponential
        + att_amplitude / att_sigma**2 * att_exponential
    )
    gradient_factor_q = (
        rep_amplitude / rep_sigma**4 * rep_exponential
        - att_amplitude / att_sigma**4 * att_exponential
    )
    gradient_factor_radius = (
        gradient_factor_q * 2.0 * orbit_radius * radial_chord_factor
    )
    gradient_factor_omega = (
        gradient_factor_q * orbit_radius**2 * times * phase_sine
    )
    memory_weights = mass * np.exp(-times) * integration_weights

    radial = np.sum(memory_weights * gradient_factor * radial_chord_factor)
    tangential = np.sum(memory_weights * gradient_factor * phase_sine)
    radial_radius = np.sum(
        memory_weights * gradient_factor_radius * radial_chord_factor
    )
    radial_omega = np.sum(
        memory_weights
        * (
            gradient_factor_omega * radial_chord_factor
            + gradient_factor * times * phase_sine
        )
    )
    tangential_radius = np.sum(
        memory_weights * gradient_factor_radius * phase_sine
    )
    tangential_omega = np.sum(
        memory_weights
        * (
            gradient_factor_omega * phase_sine
            + gradient_factor * times * phase_cosine
        )
    )
    required_gain_rate = -omega / tangential if tangential != 0.0 else math.inf
    return ContinuumRotatingWaveBalance(
        components=RotatingWaveComponents(
            radial=float(radial),
            tangential=float(tangential),
        ),
        residual=(
            float(radial),
            float(omega + gain_rate * tangential),
        ),
        jacobian=(
            (float(radial_radius), float(radial_omega)),
            (
                float(gain_rate * tangential_radius),
                float(1.0 + gain_rate * tangential_omega),
            ),
        ),
        required_eta_per_alpha=float(required_gain_rate),
    )


def continuum_required_eta_per_alpha(
    *,
    radius: float,
    angular_frequency: float,
    tail_extent: float,
    memory_mass: float,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float = 1.0,
    amplitude_att: float,
    quadrature_order: int = 512,
    quadrature_backend: str = "numpy",
) -> float:
    """Return eta/alpha required by tangential balance in the continuum limit."""

    components = continuum_rotating_wave_components(
        radius=radius,
        angular_frequency=angular_frequency,
        tail_extent=tail_extent,
        memory_mass=memory_mass,
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
        quadrature_order=quadrature_order,
        quadrature_backend=quadrature_backend,
    )
    if components.tangential >= 0.0:
        return math.nan
    return float(-angular_frequency / components.tangential)
