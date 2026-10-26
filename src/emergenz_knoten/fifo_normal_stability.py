"""Polynomial prototypes for the normal FIFO quotient, not a target-run gate."""

from __future__ import annotations

from dataclasses import asdict
from decimal import Decimal, InvalidOperation
from typing import Any, Sequence

from mpmath import iv, libmp

from .rotating_wave_interval import (
    IntervalRotatingWaveParameters,
    _interval_record,
    certify_rotating_wave_box,
)


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


def normal_translation_slope(couplings: Sequence[Any]) -> Any:
    """Return p'(1)=1+sum(j*c_j) for the translation-preserving normal block.

    A rigorously negative upper bound suffices for a real eigenvalue >1.
    Nonnegative or unresolved values do not imply stability. This arithmetic
    helper does not bind coefficients to a certified physical circle.
    """
    if len(couplings) < 1:
        raise ValueError("at least one lag coupling is required")
    return 1 + sum(age * coupling for age, coupling in enumerate(couplings, start=1))


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
        decision, reflections = _schur_recursion(current, precision_dps + 8)
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


def _schur_recursion(coefficients: Sequence[Any], digits: int) -> tuple[str, list]:
    current = list(coefficients)
    reflections = []
    while len(current) > 1:
        reflection = current[-1]
        magnitude = abs(reflection)
        reflections.append(
            {
                "degree": len(current) - 1,
                "coefficient": _interval_record(reflection, digits),
                "magnitude": _interval_record(magnitude, digits),
            }
        )
        if libmp.mpf_ge(magnitude._mpi_[0], libmp.fone):
            return "not-strictly-schur", reflections
        if not libmp.mpf_lt(magnitude._mpi_[1], libmp.fone):
            return "inconclusive", reflections
        denominator = 1 - reflection**2
        degree = len(current) - 1
        current = [iv.mpf(1)] + [
            (current[index] - reflection * current[degree - index]) / denominator
            for index in range(1, degree)
        ]
    return "strictly-schur", reflections


def _normal_characteristic_polynomial(
    radius: Any, theta: Any, parameters: IntervalRotatingWaveParameters
) -> list[Any]:
    one = iv.mpf(1)
    alpha = iv.mpf(parameters.alpha)
    decay = one - alpha
    weight = alpha * iv.mpf(parameters.memory_mass) * decay
    eta = iv.mpf(parameters.eta)
    rep_variance = iv.mpf(parameters.sigma_rep) ** 2
    att_variance = iv.mpf(parameters.sigma_att) ** 2
    rep_scale = iv.mpf(parameters.amplitude_rep) / rep_variance
    att_scale = iv.mpf(parameters.amplitude_att) / att_variance
    couplings = []
    for age in range(1, parameters.horizon):
        half_chord_squared = radius**2 * (one - iv.cos(age * theta))
        gradient = -rep_scale * iv.exp(-half_chord_squared / rep_variance)
        gradient += att_scale * iv.exp(-half_chord_squared / att_variance)
        couplings.append(eta * weight * gradient)
        weight *= decay
    return [one, sum(couplings, iv.mpf(0)) - one] + [-value for value in couplings]


def certify_normal_fifo_box(
    *,
    radius: str,
    theta: str,
    radius_half_width: str,
    theta_half_width: str,
    parameters: IntervalRotatingWaveParameters,
    precision_dps: int,
) -> dict[str, Any]:
    """Recertify a supplied finite circle box, then test its normal form block.

    No archived pass flag is accepted. The full root-box binary endpoints are
    passed directly to interval arithmetic; displayed decimals are never reused.
    This has no target loader, search, precision escalation or run authorization.
    The result concerns local linear normal stability, not the planar block.
    """
    if type(precision_dps) is not int or precision_dps < 50:
        raise ValueError("precision_dps must be an integer of at least 50")
    if parameters.horizon < 3:
        raise ValueError("normal symmetry quotient requires horizon >= 3")
    root_inputs = {
        "radius": radius,
        "theta": theta,
        "radius_half_width": radius_half_width,
        "theta_half_width": theta_half_width,
    }
    parameter_values = asdict(parameters)
    decimal_inputs = {
        key: value for key, value in parameter_values.items() if key != "horizon"
    }
    for name, value in (root_inputs | decimal_inputs).items():
        if type(value) is not str:
            raise TypeError(f"{name} must be a decimal string")
        try:
            number = Decimal(value)
        except InvalidOperation as error:
            raise ValueError(f"{name} must be a finite decimal") from error
        if not number.is_finite():
            raise ValueError(f"{name} must be finite")
        if name not in ("radius", "theta") and number <= 0:
            raise ValueError(f"{name} must be positive")
        if name == "alpha" and number >= 1:
            raise ValueError("alpha must lie strictly between zero and one")

    root = certify_rotating_wave_box(
        **root_inputs, parameters=parameters, precision_dps=precision_dps
    )
    result = {
        "schema": "normal-fifo-root-box-prototype-v1",
        "scope": "finite-H-local-linear-normal-form-only",
        "trust_basis": "mpmath.iv",
        "precision_dps": precision_dps,
        "parameters": parameter_values,
        "root_inputs": root_inputs,
        "root_certificate": root,
        "decision": "root-not-certified",
        "normal_polynomial": None,
        "cosine": None,
        "quotient": None,
        "remainder": None,
        "schur": None,
    }
    if not root["pass"]:
        return result

    previous_precision = iv.dps
    iv.dps = precision_dps
    try:
        radius_box, theta_box = [
            iv.make_mpf((tuple(record["lower_binary"]), tuple(record["upper_binary"])))
            for record in root["box"]
        ]
        polynomial = _normal_characteristic_polynomial(
            radius_box, theta_box, parameters
        )
        cosine = iv.cos(theta_box)
        quotient, remainder = rotation_symmetry_division(polynomial, cosine)
        digits = precision_dps + 8
        result.update(
            normal_polynomial=[_interval_record(value, digits) for value in polynomial],
            cosine=_interval_record(cosine, digits),
            quotient=[_interval_record(value, digits) for value in quotient],
            remainder=[_interval_record(value, digits) for value in remainder],
        )
        if not all(record["contains_zero"] for record in result["remainder"]):
            result["decision"] = "inconsistent-symmetry-factor"
            return result
        decision, reflections = _schur_recursion(quotient, digits)
        result["decision"] = decision
        result["schur"] = {
            "degree": len(quotient) - 1,
            "decision": decision,
            "reflections": reflections,
        }
        return result
    finally:
        iv.dps = previous_precision
