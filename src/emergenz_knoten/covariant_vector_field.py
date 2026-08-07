"""O(d)-covariant local vector-field feedback and its linear limits."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np


VectorChannel = Literal["longitudinal", "transverse"]


def _finite(name: str, value: float) -> float:
    number = float(value)
    if not np.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _positive(name: str, value: float) -> float:
    number = _finite(name, value)
    if number <= 0.0:
        raise ValueError(f"{name} must be positive")
    return number


def _non_negative(name: str, value: float) -> float:
    number = _finite(name, value)
    if number < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return number


@dataclass(frozen=True)
class VectorChannelStability:
    """Linear stability of one longitudinal or transverse vector channel."""

    channel: VectorChannel
    stable: bool
    high_wavenumber_stable: bool
    finite_wavenumber_preference: bool
    preferred_wavenumber: float
    minimum_denominator: float
    classification: str


@dataclass(frozen=True)
class VectorFieldDimensionlessGroups:
    """Natural scales and irreducible ratios of the local vector family."""

    length_scale: float
    amplitude_scale: float
    relaxation_time: float
    longitudinal_gradient_ratio: float
    transverse_gradient_ratio: float


@dataclass(frozen=True)
class LocalVectorFieldExpansion:
    r"""Parity-even isotropic local vector-field energy through fourth order.

    The quadratic and saturating energy density contains mass, longitudinal
    and transverse gradients, a biharmonic regularizer, cubic saturation and
    a directed source. Its purely dissipative dynamics is gradient flow. This
    class deliberately excludes chirality and reactive dynamics.
    """

    mass_coefficient: float
    longitudinal_gradient_coefficient: float
    transverse_gradient_coefficient: float
    biharmonic_coefficient: float
    cubic_saturation: float
    mobility: float = 1.0

    def __post_init__(self) -> None:
        _finite("mass_coefficient", self.mass_coefficient)
        _finite(
            "longitudinal_gradient_coefficient",
            self.longitudinal_gradient_coefficient,
        )
        _finite(
            "transverse_gradient_coefficient",
            self.transverse_gradient_coefficient,
        )
        _non_negative("biharmonic_coefficient", self.biharmonic_coefficient)
        _non_negative("cubic_saturation", self.cubic_saturation)
        _positive("mobility", self.mobility)

    def gradient_coefficient(self, channel: VectorChannel) -> float:
        """Return the quadratic-gradient coefficient of one Helmholtz channel."""

        if channel == "longitudinal":
            return float(self.longitudinal_gradient_coefficient)
        if channel == "transverse":
            return float(self.transverse_gradient_coefficient)
        raise ValueError("channel must be longitudinal or transverse")

    def channel_stability(self, channel: VectorChannel) -> VectorChannelStability:
        """Classify a+b_channel*k^2+c*k^4 over real wave numbers."""

        a = float(self.mass_coefficient)
        b = self.gradient_coefficient(channel)
        c = float(self.biharmonic_coefficient)
        if c == 0.0 and b < 0.0:
            return VectorChannelStability(
                channel=channel,
                stable=False,
                high_wavenumber_stable=False,
                finite_wavenumber_preference=False,
                preferred_wavenumber=float("inf"),
                minimum_denominator=float("-inf"),
                classification="ultraviolet_unstable",
            )

        if c > 0.0 and b < 0.0:
            preferred = float(np.sqrt(-b / (2.0 * c)))
            minimum = float(a - b * b / (4.0 * c))
            finite_preference = True
        else:
            preferred = 0.0
            minimum = a
            finite_preference = False

        scale = max(1.0, abs(a), abs(minimum))
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
        return VectorChannelStability(
            channel=channel,
            stable=stable,
            high_wavenumber_stable=(c > 0.0 or b > 0.0 or a > 0.0),
            finite_wavenumber_preference=finite_preference,
            preferred_wavenumber=preferred,
            minimum_denominator=minimum,
            classification=classification,
        )

    @property
    def linearly_stable(self) -> bool:
        """Whether both Helmholtz channels are linearly stable."""

        return bool(
            self.channel_stability("longitudinal").stable
            and self.channel_stability("transverse").stable
        )


def vector_channel_denominator(
    wavenumber: np.ndarray | float,
    field: LocalVectorFieldExpansion,
    *,
    channel: VectorChannel,
) -> np.ndarray:
    """Return a+b_channel*k^2+c*k^4."""

    k = np.asarray(wavenumber, dtype=float)
    if not np.isfinite(k).all():
        raise ValueError("wavenumber must be finite")
    k2 = np.square(k)
    return np.asarray(
        field.mass_coefficient
        + field.gradient_coefficient(channel) * k2
        + field.biharmonic_coefficient * np.square(k2),
        dtype=float,
    )


def vector_gradient_flow_rates(
    wavenumber: np.ndarray | float,
    field: LocalVectorFieldExpansion,
) -> tuple[np.ndarray, np.ndarray]:
    """Return real longitudinal and transverse growth rates."""

    longitudinal = -field.mobility * vector_channel_denominator(
        wavenumber,
        field,
        channel="longitudinal",
    )
    transverse = -field.mobility * vector_channel_denominator(
        wavenumber,
        field,
        channel="transverse",
    )
    return np.asarray(longitudinal), np.asarray(transverse)


def isotropic_vector_fourier_operator(
    wavevector: np.ndarray,
    field: LocalVectorFieldExpansion,
) -> np.ndarray:
    """Return the real symmetric gradient-flow operator for one wavevector."""

    k = np.asarray(wavevector, dtype=float)
    if k.ndim != 1 or k.size < 1 or not np.isfinite(k).all():
        raise ValueError("wavevector must be a finite non-empty vector")
    k2 = float(np.dot(k, k))
    identity = np.eye(k.size)
    if k2 == 0.0:
        longitudinal_projector = np.zeros_like(identity)
    else:
        longitudinal_projector = np.outer(k, k) / k2
    transverse_projector = identity - longitudinal_projector
    common = field.mass_coefficient + field.biharmonic_coefficient * k2 * k2
    denominator = (
        common * identity
        + field.longitudinal_gradient_coefficient
        * k2
        * longitudinal_projector
        + field.transverse_gradient_coefficient
        * k2
        * transverse_projector
    )
    return np.asarray(-field.mobility * denominator, dtype=float)


def vector_field_dimensionless_groups(
    field: LocalVectorFieldExpansion,
) -> VectorFieldDimensionlessGroups:
    """Reduce positive a,c,u,Gamma to natural units and two ratios."""

    a = _positive("mass_coefficient", field.mass_coefficient)
    c = _positive("biharmonic_coefficient", field.biharmonic_coefficient)
    u = _positive("cubic_saturation", field.cubic_saturation)
    scale = float(np.sqrt(a * c))
    return VectorFieldDimensionlessGroups(
        length_scale=float((c / a) ** 0.25),
        amplitude_scale=float(np.sqrt(a / u)),
        relaxation_time=float(1.0 / (field.mobility * a)),
        longitudinal_gradient_ratio=float(
            field.longitudinal_gradient_coefficient / scale
        ),
        transverse_gradient_ratio=float(
            field.transverse_gradient_coefficient / scale
        ),
    )


def reactive_pair_operator(
    damping_rate: float,
    angular_frequency: float,
) -> np.ndarray:
    """Return the minimal two-state damped rotation operator.

    This operator is O(d)-covariant when applied identically to every spatial
    component, but it introduces a second internal state and an antisymmetric
    coupling. It is not generated by a one-field gradient flow.
    """

    damping = _non_negative("damping_rate", damping_rate)
    frequency = _finite("angular_frequency", angular_frequency)
    return np.array(
        [
            [-damping, -frequency],
            [frequency, -damping],
        ],
        dtype=float,
    )