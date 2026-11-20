"""Existence and one sufficient instability test for antipodal FIFO pairs.

Identical kernels/weights, synchronous additive readout, zero noise. This
module does not certify stability, select target parameters or launch runs.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

from mpmath import iv, libmp, mp

from .rotating_wave_interval import (
    IntervalRotatingWaveParameters,
    _balance_and_jacobian,
    _contains_zero,
    _interval_record,
    _inverse_jacobian_strings,
    _strict_subset,
    _strictly_negative,
    _strictly_positive,
    krawczyk_image,
)


def _decimal(value: str, name: str) -> Decimal:
    if type(value) is not str:
        raise TypeError(f"{name} must be a decimal string")
    try:
        result = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} must be a decimal string") from error
    if not result.is_finite():
        raise ValueError(f"{name} must be finite")
    return result


@dataclass(frozen=True)
class AntipodalPairParameters:
    """Existing self parameters plus an explicit nonnegative cross gain."""

    self_parameters: IntervalRotatingWaveParameters
    cross_eta: str

    def __post_init__(self) -> None:
        if not isinstance(self.self_parameters, IntervalRotatingWaveParameters):
            raise TypeError("self_parameters must be IntervalRotatingWaveParameters")
        for name, value in asdict(self.self_parameters).items():
            if name != "horizon":
                _decimal(value, name)
        if _decimal(self.cross_eta, "cross_eta") < 0:
            raise ValueError("cross_eta must be nonnegative")


def _validate_point(radius: str, theta: str, precision_dps: int) -> None:
    if type(precision_dps) is not int or precision_dps < 50:
        raise ValueError("precision_dps must be an integer of at least 50")
    _decimal(radius, "radius")
    _decimal(theta, "theta")
    with mp.workdps(precision_dps):
        if not (mp.mpf(radius) > 0 and 0 < mp.mpf(theta) < mp.pi):
            raise ValueError("require radius > 0 and 0 < theta < pi")


def _pair_balance_and_jacobian(context, radius, theta, parameters):
    p = parameters.self_parameters
    balance, jacobian, _ = _balance_and_jacobian(context, radius, theta, p)
    chi = context.mpf(parameters.cross_eta)
    eta = context.mpf(p.eta)
    alpha = context.mpf(p.alpha)
    weight = alpha * context.mpf(p.memory_mass)
    q = 1 - alpha
    sr2 = context.mpf(p.sigma_rep) ** 2
    sa2 = context.mpf(p.sigma_att) ** 2
    ar = context.mpf(p.amplitude_rep)
    aa = context.mpf(p.amplitude_att)
    r2 = radius * radius
    radial, tangent, radial_r, radial_t, tangent_r, tangent_t = (
        context.mpf(0) for _ in range(6)
    )
    slope = context.mpf(1)
    # Cross age zero is not a self displacement and must not be dropped.
    for age in range(p.horizon):
        cosine = context.cos(age * theta)
        sine = context.sin(age * theta)
        chord = 1 + cosine
        rep = context.exp(-r2 * chord / sr2)
        att = context.exp(-r2 * chord / sa2)
        factor = -ar * rep / sr2 + aa * att / sa2
        core = ar * rep / sr2**2 - aa * att / sa2**2
        factor_r = 2 * radius * chord * core
        factor_t = -r2 * age * sine * core
        radial += weight * factor * chord
        tangent += weight * factor * sine
        radial_r += weight * factor_r * chord
        radial_t += weight * (factor_t * chord - factor * age * sine)
        tangent_r += weight * factor_r * sine
        tangent_t += weight * (factor_t * sine + factor * age * cosine)
        if age:
            self_factor = (
                -ar * context.exp(-r2 * (1 - cosine) / sr2) / sr2
                + aa * context.exp(-r2 * (1 - cosine) / sa2) / sa2
            )
            slope += age * weight * (eta * self_factor + chi * factor)
        weight *= q
    # F = (-F_R, F_T), matching the existing single-orbit convention.
    return (
        (balance[0] - chi * radial, balance[1] - chi * tangent),
        (
            (jacobian[0][0] - chi * radial_r, jacobian[0][1] - chi * radial_t),
            (jacobian[1][0] - chi * tangent_r, jacobian[1][1] - chi * tangent_t),
        ),
        slope,
    )


def point_pair_balance_and_jacobian(
    *,
    radius: str,
    theta: str,
    parameters: AntipodalPairParameters,
    precision_dps: int,
) -> dict[str, Any]:
    """Point diagnostics only; small residuals are not certificates."""
    _validate_point(radius, theta, precision_dps)
    with mp.workdps(precision_dps):
        balance, jacobian, slope = _pair_balance_and_jacobian(
            mp, mp.mpf(radius), mp.mpf(theta), parameters
        )
        digits = precision_dps - 8
        return {
            "parameters": asdict(parameters),
            "precision_dps": precision_dps,
            "balance": [mp.nstr(value, digits) for value in balance],
            "jacobian": [[mp.nstr(value, digits) for value in row] for row in jacobian],
            "common_normal_slope": mp.nstr(slope, digits),
        }


def refine_antipodal_pair_root(
    *,
    radius: str,
    theta: str,
    parameters: AntipodalPairParameters,
    precision_dps: int,
    iterations: int,
) -> dict[str, Any]:
    """Fixed Newton budget, no damping, restarts, parameter changes or proof.

    A caller running a target must separately enforce its approved wall-time
    and process limits. Invalid input raises; numerical exits are recorded.
    """
    _validate_point(radius, theta, precision_dps)
    if type(iterations) is not int or iterations < 1:
        raise ValueError("iterations must be a positive integer")
    with mp.workdps(precision_dps):
        current = (mp.mpf(radius), mp.mpf(theta))
        digits = precision_dps - 8

        def record(values):
            return {
                "radius": mp.nstr(values[0], digits),
                "theta": mp.nstr(values[1], digits),
            }

        iterates = [record(current)]
        corrections = []
        status = "iteration_budget_completed"
        rejected_candidate = None
        for _ in range(iterations):
            balance, jacobian, _ = _pair_balance_and_jacobian(mp, *current, parameters)
            determinant = (
                jacobian[0][0] * jacobian[1][1] - jacobian[0][1] * jacobian[1][0]
            )
            if not all(mp.isfinite(value) for value in (*balance, determinant)):
                status = "nonfinite_evaluation"
                break
            if determinant == 0:
                status = "singular_point_jacobian"
                break
            correction = (
                (jacobian[1][1] * balance[0] - jacobian[0][1] * balance[1])
                / determinant,
                (-jacobian[1][0] * balance[0] + jacobian[0][0] * balance[1])
                / determinant,
            )
            corrections.append(record(correction))
            candidate = (current[0] - correction[0], current[1] - correction[1])
            if not all(mp.isfinite(value) for value in candidate):
                status = "nonfinite_step"
                rejected_candidate = record(candidate)
                break
            if not (candidate[0] > 0 and 0 < candidate[1] < mp.pi):
                status = "left_physical_domain"
                rejected_candidate = record(candidate)
                break
            current = candidate
            iterates.append(record(current))
        return {
            "parameters": asdict(parameters),
            "precision_dps": precision_dps,
            "requested_iterations": iterations,
            "status": status,
            **record(current),
            "iterates": iterates,
            "corrections": corrections,
            "rejected_candidate": rejected_candidate,
            "root_certified": False,
        }


def certify_antipodal_pair_box(
    *,
    radius: str,
    theta: str,
    radius_half_width: str,
    theta_half_width: str,
    parameters: AntipodalPairParameters,
    precision_dps: int,
) -> dict[str, Any]:
    """One fixed Krawczyk box; failure is inconclusive, never nonexistence.

    A strictly negative common-normal slope proves instability only when
    the same box certifies the orbit. Other slopes leave stability open.
    Binary interval endpoints, not formatted decimals, determine all gates.
    """
    _validate_point(radius, theta, precision_dps)
    for name, value in (
        ("radius_half_width", radius_half_width),
        ("theta_half_width", theta_half_width),
    ):
        if _decimal(value, name) <= 0:
            raise ValueError(f"{name} must be positive")
    previous_dps = iv.dps
    iv.dps = precision_dps
    try:
        center = (iv.mpf(radius), iv.mpf(theta))
        box = (
            center[0] + iv.mpf([-1, 1]) * iv.mpf(radius_half_width),
            center[1] + iv.mpf([-1, 1]) * iv.mpf(theta_half_width),
        )
        values, jacobian, slope = _pair_balance_and_jacobian(iv, *box, parameters)
        center_values, _, _ = _pair_balance_and_jacobian(iv, *center, parameters)
        determinant = jacobian[0][0] * jacobian[1][1] - jacobian[0][1] * jacobian[1][0]
        gates = {
            "physical_box": (
                _strictly_positive(box[0])
                and _strictly_positive(box[1])
                and bool(libmp.mpf_lt(box[1]._mpi_[1], iv.pi._mpi_[0]))
            ),
            "balance_contains_zero": all(_contains_zero(value) for value in values),
            "jacobian_nonsingular": not _contains_zero(determinant),
            "preconditioner_nonsingular": False,
            "krawczyk_strict_interior": False,
        }
        inverse_strings = None
        image = None
        with mp.workdps(precision_dps):
            _, point_jacobian, _ = _pair_balance_and_jacobian(
                mp, mp.mpf(radius), mp.mpf(theta), parameters
            )
            try:
                inverse_strings = _inverse_jacobian_strings(
                    point_jacobian,
                    precision_dps=precision_dps,
                    singular_message="pair point Jacobian is singular",
                )
            except ArithmeticError:
                pass
        if inverse_strings is not None:
            inverse = tuple(
                tuple(iv.mpf(value) for value in row) for row in inverse_strings
            )
            inverse_det = inverse[0][0] * inverse[1][1] - inverse[0][1] * inverse[1][0]
            gates["preconditioner_nonsingular"] = not _contains_zero(inverse_det)
            image = krawczyk_image(
                center=center,
                box=box,
                function_at_center=center_values,
                jacobian_box=jacobian,
                inverse_point_jacobian=inverse,
            )
            gates["krawczyk_strict_interior"] = all(
                _strict_subset(inner, outer)
                for inner, outer in zip(image, box, strict=True)
            )
        root_certified = all(gates.values())
        slope_negative = _strictly_negative(slope)
        digits = precision_dps + 8
        return {
            "parameters": asdict(parameters),
            "precision_dps": precision_dps,
            "requested_center": [radius, theta],
            "requested_half_widths": [radius_half_width, theta_half_width],
            "root_certified": root_certified,
            "classification": (
                "certified_orbit_common_normal_unstable"
                if root_certified and slope_negative
                else "certified_orbit_stability_unresolved"
                if root_certified
                else "orbit_inconclusive"
            ),
            "gates": gates,
            "box": [_interval_record(value, digits) for value in box],
            "function_box": [_interval_record(value, digits) for value in values],
            "jacobian_box": [
                [_interval_record(value, digits) for value in row] for row in jacobian
            ],
            "jacobian_determinant": _interval_record(determinant, digits),
            "inverse_point_jacobian": inverse_strings,
            "krawczyk_image": None
            if image is None
            else [_interval_record(value, digits) for value in image],
            "common_normal_slope": _interval_record(slope, digits),
            "common_normal_slope_strictly_negative": slope_negative,
            "stability_certified": False,
        }
    finally:
        iv.dps = previous_dps
