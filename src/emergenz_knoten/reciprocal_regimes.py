"""Regime boundaries for the local reciprocal scalar-memory reduction."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Literal

from .reciprocal_modes import reciprocal_scalar_memory_modes


ReciprocalModeRegime = Literal[
    "real_stable",
    "complex_stable",
    "real_unstable",
    "complex_unstable",
]


@dataclass(frozen=True)
class CrossGainInterval:
    """Open positive cross-gain interval for stable complex relative modes."""

    lower: float
    upper: float

    def __post_init__(self) -> None:
        if not (0.0 <= self.lower < self.upper):
            raise ValueError("cross-gain interval must satisfy 0 <= lower < upper")


def classify_reciprocal_mode_regime(
    lambda_value: float,
    *,
    self_gain: float,
    cross_gain: float,
) -> ReciprocalModeRegime:
    """Classify the local relative mode by reality and discrete stability."""

    result = reciprocal_scalar_memory_modes(
        lambda_value,
        self_gain=self_gain,
        cross_gain=cross_gain,
    )
    if result.relative_is_complex:
        return "complex_stable" if result.relative_is_stable else "complex_unstable"
    return "real_stable" if result.relative_is_stable else "real_unstable"


def stable_complex_cross_gain_interval(
    lambda_value: float,
    *,
    self_gain: float,
) -> CrossGainInterval | None:
    r"""Return the positive cross-gain interval satisfying the oscillator gate.

    The relative discriminant is a quadratic in the cross gain ``c``. This
    function intersects its negative interval with ``c>0`` and
    ``0 < (1-lambda)(1-g-c) < 1``. Endpoints are excluded because they are
    repeated-real or marginal boundaries.
    """

    if not math.isfinite(lambda_value) or not 0.0 < lambda_value <= 1.0:
        raise ValueError("lambda_value must lie in (0, 1]")
    if not math.isfinite(self_gain):
        raise ValueError("self_gain must be finite")

    q = 1.0 - lambda_value
    if q == 0.0:
        return None
    slope = 1.0 + lambda_value
    trace_at_zero = 2.0 - lambda_value - q * self_gain
    determinant_at_zero = q * (1.0 - self_gain)

    quadratic = slope * slope
    linear = -2.0 * slope * trace_at_zero + 4.0 * q
    constant = trace_at_zero * trace_at_zero - 4.0 * determinant_at_zero
    root_discriminant = linear * linear - 4.0 * quadratic * constant
    tolerance = 64.0 * math.ulp(max(abs(linear * linear), 1.0))
    if root_discriminant <= tolerance:
        return None

    root = math.sqrt(root_discriminant)
    first = (-linear - root) / (2.0 * quadratic)
    second = (-linear + root) / (2.0 * quadratic)
    discriminant_lower = min(first, second)
    discriminant_upper = max(first, second)

    determinant_lower = 1.0 - self_gain - 1.0 / q
    determinant_upper = 1.0 - self_gain
    lower = max(0.0, discriminant_lower, determinant_lower)
    upper = min(discriminant_upper, determinant_upper)
    if not lower < upper:
        return None
    return CrossGainInterval(lower=float(lower), upper=float(upper))
