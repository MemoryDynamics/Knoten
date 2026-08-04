"""Linear mode test for reciprocal scalar-memory coupling."""

from __future__ import annotations

from dataclasses import dataclass
import cmath
import math


@dataclass(frozen=True)
class ReciprocalScalarModeResult:
    """Common and relative multipliers of the local two-node reduction."""

    lambda_value: float
    self_gain: float
    cross_gain: float
    common_multipliers: tuple[complex, complex]
    relative_multipliers: tuple[complex, complex]
    relative_trace: float
    relative_determinant: float
    relative_discriminant: float

    @property
    def relative_is_complex(self) -> bool:
        return self.relative_discriminant < 0.0

    @property
    def relative_is_stable(self) -> bool:
        return max(abs(value) for value in self.relative_multipliers) < 1.0

    @property
    def relative_angular_frequency(self) -> float:
        """Return the positive phase advance per update, or zero for real modes."""

        if not self.relative_is_complex:
            return 0.0
        return float(abs(cmath.phase(self.relative_multipliers[0])))

    @property
    def relative_damping_rate(self) -> float:
        """Return ``-log(max |mu|)``; negative values denote growth."""

        radius = max(abs(value) for value in self.relative_multipliers)
        if radius == 0.0:
            return math.inf
        return float(-math.log(radius))


def reciprocal_scalar_memory_modes(
    lambda_value: float,
    *,
    self_gain: float,
    cross_gain: float,
) -> ReciprocalScalarModeResult:
    r"""Return modes of two synchronously and reciprocally coupled memories.

    The local deterministic model is

    .. math::

       x_i' = x_i-g(x_i-m_i)-c(x_i-m_j),\qquad
       m_i'=(1-\lambda)m_i+\lambda x_i',\quad j\ne i.

    Here ``g`` and ``c`` are dimensionless self and cross gains per update.
    The common channel has multipliers ``1`` and ``q(1-g-c)``. The relative
    channel has trace

    ``T=2-lambda-(1-lambda)g-(1+lambda)c``

    and determinant ``D=(1-lambda)(1-g-c)``. A damped oscillatory relative
    mode requires ``T**2 < 4*D`` and ``0 < D < 1``.
    """

    if not math.isfinite(lambda_value) or not 0.0 < lambda_value <= 1.0:
        raise ValueError("lambda_value must lie in (0, 1]")
    if not math.isfinite(self_gain):
        raise ValueError("self_gain must be finite")
    if not math.isfinite(cross_gain):
        raise ValueError("cross_gain must be finite")

    q = 1.0 - lambda_value
    common_relative = q * (1.0 - self_gain - cross_gain)
    trace = 2.0 - lambda_value - q * self_gain - (1.0 + lambda_value) * cross_gain
    determinant = common_relative
    discriminant = trace * trace - 4.0 * determinant
    root = cmath.sqrt(discriminant)
    relative = (0.5 * (trace + root), 0.5 * (trace - root))
    return ReciprocalScalarModeResult(
        lambda_value=float(lambda_value),
        self_gain=float(self_gain),
        cross_gain=float(cross_gain),
        common_multipliers=(1.0 + 0.0j, complex(common_relative)),
        relative_multipliers=relative,
        relative_trace=float(trace),
        relative_determinant=float(determinant),
        relative_discriminant=float(discriminant),
    )


def reciprocal_complex_window_exists(
    lambda_value: float,
    *,
    self_gain: float,
) -> bool:
    r"""Return whether some positive cross gain can yield a complex pair.

    Minimizing the relative discriminant over the cross gain gives the exact
    condition ``g < lambda/(1+lambda)`` for ``0 < lambda < 1``. At
    ``lambda=1`` the determinant vanishes and the minimum discriminant is
    zero, so no non-real pair exists. This only establishes that a complex
    window exists; stability must still be checked at the selected cross gain.
    """

    if not math.isfinite(lambda_value) or not 0.0 < lambda_value <= 1.0:
        raise ValueError("lambda_value must lie in (0, 1]")
    if not math.isfinite(self_gain):
        raise ValueError("self_gain must be finite")
    return bool(lambda_value < 1.0 and self_gain < lambda_value / (1.0 + lambda_value))
