"""Polynomial prototypes for the normal FIFO quotient, not a target-run gate."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any, Sequence

from mpmath import iv, libmp

from .rotating_wave_interval import _interval_record


def rotation_symmetry_division(
    coefficients: Sequence[Any], cosine: Any
) -> tuple[list[Any], list[Any]]:
    """Divide a monic descending polynomial by (z-1)(z^2-2*cosine*z+1).

    Operands may be exact rationals or interval numbers. The remainder is
    returned, never silently discarded. An interval remainder containing zero
    does not prove that the input polynomial has the symmetry factor.
    """
    if len(coefficients) < 4 or coefficients[0] != 1:
        raise ValueError("expected a monic polynomial of degree at least three")
    factor = [1, -(1 + 2 * cosine), 1 + 2 * cosine, -1]
    remainder = list(coefficients)
    quotient = []
    for index in range(len(coefficients) - 3):
        value = remainder[index]
        quotient.append(value)
        for offset in range(1, 4):
            remainder[index + offset] -= value * factor[offset]
        # Exact cancellation of the same expression, also for interval operands.
        remainder[index] = 0
    return quotient, remainder[-3:]


def interval_schur_test(
    coefficients: Sequence[tuple[str, str]], *, precision_dps: int
) -> dict[str, Any]:
    """Enclose the real monic Schur recursion for descending coefficients.

    The result concerns the supplied coefficient box, not a physical root or
    a nonlinear orbit. Ambiguous interval comparisons are inconclusive.
    Uses the repository's mpmath.iv trust basis and restores its global precision;
    like the existing interval helpers, this is not a concurrent-context API.
    """
    if type(precision_dps) is not int or precision_dps < 50:
        raise ValueError("precision_dps must be an integer of at least 50")
    if len(coefficients) < 1:
        raise ValueError("coefficients must not be empty")
    validated = []
    for bounds in coefficients:
        if (
            type(bounds) is not tuple
            or len(bounds) != 2
            or any(type(endpoint) is not str for endpoint in bounds)
        ):
            raise TypeError("each coefficient must be a pair of decimal strings")
        try:
            lower, upper = map(Decimal, bounds)
        except InvalidOperation as error:
            raise ValueError("invalid decimal coefficient") from error
        if not (lower.is_finite() and upper.is_finite() and lower <= upper):
            raise ValueError("coefficient endpoints must be finite and ordered")
        validated.append((lower, upper))
    if validated[0] != (Decimal(1), Decimal(1)):
        raise ValueError("leading coefficient must be exactly one")

    previous_precision = iv.dps
    iv.dps = precision_dps
    try:
        current = [iv.mpf(list(bounds)) for bounds in coefficients]
        reflections = []
        decision = "strictly-schur"
        while len(current) > 1:
            reflection = current[-1]
            magnitude = abs(reflection)
            reflections.append(
                {
                    "degree": len(current) - 1,
                    "coefficient": _interval_record(reflection, precision_dps + 8),
                    "magnitude": _interval_record(magnitude, precision_dps + 8),
                }
            )
            if libmp.mpf_ge(magnitude._mpi_[0], libmp.fone):
                decision = "not-strictly-schur"
                break
            if not libmp.mpf_lt(magnitude._mpi_[1], libmp.fone):
                decision = "inconclusive"
                break
            denominator = 1 - reflection**2
            degree = len(current) - 1
            current = [iv.mpf(1)] + [
                (current[index] - reflection * current[degree - index]) / denominator
                for index in range(1, degree)
            ]
        return {
            "schema": "normal-fifo-schur-prototype-v1",
            "scope": "supplied-real-monic-polynomial-box-only",
            "trust_basis": "mpmath.iv",
            "precision_dps": precision_dps,
            "degree": len(coefficients) - 1,
            "input_coefficients": [list(bounds) for bounds in coefficients],
            "decision": decision,
            "reflections": reflections,
        }
    finally:
        iv.dps = previous_precision
