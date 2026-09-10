"""Interval certificates for finite-memory scalar rotating-wave roots."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Sequence

from mpmath import iv, libmp, mp


@dataclass(frozen=True)
class IntervalRotatingWaveParameters:
    """Decimal parameters of the exact finite-H rotating-wave balance."""

    alpha: str
    horizon: int
    memory_mass: str
    eta: str
    sigma_rep: str
    sigma_att: str
    amplitude_rep: str
    amplitude_att: str

    def __post_init__(self) -> None:
        if (
            isinstance(self.horizon, bool)
            or not isinstance(self.horizon, int)
            or self.horizon < 2
        ):
            raise ValueError("horizon must be an integer of at least two")
        for name in (
            "alpha",
            "memory_mass",
            "eta",
            "sigma_rep",
            "sigma_att",
            "amplitude_rep",
            "amplitude_att",
        ):
            try:
                value = float(getattr(self, name))
            except (TypeError, ValueError) as error:
                raise ValueError(f"{name} must be a decimal string") from error
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be positive and finite")
        if not 0.0 < float(self.alpha) < 1.0:
            raise ValueError("alpha must lie strictly between zero and one")


def _balance_and_jacobian(
    context: Any,
    radius: Any,
    theta: Any,
    parameters: IntervalRotatingWaveParameters,
) -> tuple[tuple[Any, Any], tuple[tuple[Any, Any], tuple[Any, Any]], tuple[Any, Any]]:
    """Evaluate the exact balance, analytic Jacobian and (A_H,S_H)."""

    one = context.mpf(1)
    alpha = context.mpf(parameters.alpha)
    memory_mass = context.mpf(parameters.memory_mass)
    eta = context.mpf(parameters.eta)
    sigma_rep = context.mpf(parameters.sigma_rep)
    sigma_att = context.mpf(parameters.sigma_att)
    amplitude_rep = context.mpf(parameters.amplitude_rep)
    amplitude_att = context.mpf(parameters.amplitude_att)
    sigma_rep2 = sigma_rep * sigma_rep
    sigma_att2 = sigma_att * sigma_att
    sigma_rep4 = sigma_rep2 * sigma_rep2
    sigma_att4 = sigma_att2 * sigma_att2
    radius2 = radius * radius
    q = one - alpha

    radial = context.mpf(0)
    tangential = context.mpf(0)
    radial_radius = context.mpf(0)
    radial_theta = context.mpf(0)
    tangential_radius = context.mpf(0)
    tangential_theta = context.mpf(0)
    weight = alpha * memory_mass * q

    for age in range(1, parameters.horizon):
        phase = age * theta
        cosine = context.cos(phase)
        sine = context.sin(phase)
        chord_factor = one - cosine
        rep_exp = context.exp(-radius2 * chord_factor / sigma_rep2)
        att_exp = context.exp(-radius2 * chord_factor / sigma_att2)
        gradient_factor = (
            -amplitude_rep * rep_exp / sigma_rep2
            + amplitude_att * att_exp / sigma_att2
        )
        derivative_core = (
            amplitude_rep * rep_exp / sigma_rep4
            - amplitude_att * att_exp / sigma_att4
        )
        gradient_radius = 2 * radius * chord_factor * derivative_core
        gradient_theta = radius2 * age * sine * derivative_core

        radial += weight * gradient_factor * chord_factor
        tangential += weight * gradient_factor * sine
        radial_radius += weight * gradient_radius * chord_factor
        radial_theta += weight * (
            gradient_theta * chord_factor + gradient_factor * age * sine
        )
        tangential_radius += weight * gradient_radius * sine
        tangential_theta += weight * (
            gradient_theta * sine + gradient_factor * age * cosine
        )
        weight *= q

    first = one - context.cos(theta) - eta * radial
    second = context.sin(theta) + eta * tangential
    jacobian = (
        (-eta * radial_radius, context.sin(theta) - eta * radial_theta),
        (eta * tangential_radius, context.cos(theta) + eta * tangential_theta),
    )
    return (first, second), jacobian, (radial, tangential)


def point_balance_and_jacobian(
    *,
    radius: str,
    theta: str,
    parameters: IntervalRotatingWaveParameters,
    precision_dps: int,
) -> dict[str, Any]:
    """Return a multiprecision point evaluation as decimal strings."""

    if precision_dps < 30:
        raise ValueError("precision_dps must be at least 30")
    with mp.workdps(precision_dps):
        values, jacobian, components = _balance_and_jacobian(
            mp,
            mp.mpf(radius),
            mp.mpf(theta),
            parameters,
        )
        digits = precision_dps - 5
        return {
            "balance": [mp.nstr(value, digits) for value in values],
            "jacobian": [
                [mp.nstr(value, digits) for value in row] for row in jacobian
            ],
            "components": [mp.nstr(value, digits) for value in components],
        }


def refine_rotating_wave_root(
    *,
    radius: str,
    theta: str,
    parameters: IntervalRotatingWaveParameters,
    precision_dps: int,
    iterations: int,
) -> dict[str, Any]:
    """Apply a fixed number of analytic multiprecision Newton iterations."""

    if precision_dps < 50:
        raise ValueError("precision_dps must be at least 50")
    if isinstance(iterations, bool) or iterations < 1:
        raise ValueError("iterations must be a positive integer")
    with mp.workdps(precision_dps):
        current_radius = mp.mpf(radius)
        current_theta = mp.mpf(theta)
        corrections: list[dict[str, str]] = []
        iterates = [
            {
                "radius": mp.nstr(current_radius, precision_dps - 8),
                "theta": mp.nstr(current_theta, precision_dps - 8),
            }
        ]
        for _ in range(iterations):
            values, jacobian, _ = _balance_and_jacobian(
                mp,
                current_radius,
                current_theta,
                parameters,
            )
            determinant = (
                jacobian[0][0] * jacobian[1][1]
                - jacobian[0][1] * jacobian[1][0]
            )
            if determinant == 0:
                raise ArithmeticError("point Jacobian is singular")
            radius_correction = (
                jacobian[1][1] * values[0] - jacobian[0][1] * values[1]
            ) / determinant
            theta_correction = (
                -jacobian[1][0] * values[0] + jacobian[0][0] * values[1]
            ) / determinant
            current_radius -= radius_correction
            current_theta -= theta_correction
            corrections.append(
                {
                    "radius": mp.nstr(radius_correction, precision_dps - 8),
                    "theta": mp.nstr(theta_correction, precision_dps - 8),
                }
            )
            iterates.append(
                {
                    "radius": mp.nstr(current_radius, precision_dps - 8),
                    "theta": mp.nstr(current_theta, precision_dps - 8),
                }
            )

        values, jacobian, components = _balance_and_jacobian(
            mp,
            current_radius,
            current_theta,
            parameters,
        )
        digits = precision_dps - 12
        return {
            "radius": mp.nstr(current_radius, digits),
            "theta": mp.nstr(current_theta, digits),
            "balance": [mp.nstr(value, digits) for value in values],
            "jacobian": [
                [mp.nstr(value, digits) for value in row] for row in jacobian
            ],
            "components": [mp.nstr(value, digits) for value in components],
            "corrections": corrections,
            "iterates": iterates,
        }


def krawczyk_image(
    *,
    center: Sequence[Any],
    box: Sequence[Any],
    function_at_center: Sequence[Any],
    jacobian_box: Sequence[Sequence[Any]],
    inverse_point_jacobian: Sequence[Sequence[Any]],
) -> tuple[Any, Any]:
    """Return the two-dimensional Krawczyk image using interval operands."""

    if not (
        len(center) == len(box) == len(function_at_center) == 2
        and len(jacobian_box) == len(inverse_point_jacobian) == 2
        and all(len(row) == 2 for row in jacobian_box)
        and all(len(row) == 2 for row in inverse_point_jacobian)
    ):
        raise ValueError("Krawczyk operands must all be two-dimensional")

    result = []
    for row in range(2):
        base = center[row]
        for column in range(2):
            base -= inverse_point_jacobian[row][column] * function_at_center[column]
        remainder = iv.mpf(0)
        for column in range(2):
            coefficient = iv.mpf(1 if row == column else 0)
            for inner in range(2):
                coefficient -= (
                    inverse_point_jacobian[row][inner]
                    * jacobian_box[inner][column]
                )
            remainder += coefficient * (box[column] - center[column])
        result.append(base + remainder)
    return result[0], result[1]


def _inverse_jacobian_strings(
    jacobian: Sequence[Sequence[Any]],
    *,
    precision_dps: int,
    singular_message: str,
) -> tuple[tuple[str, str], tuple[str, str]]:
    """Invert one 2x2 point Jacobian and preserve decimal transport."""

    determinant = (
        jacobian[0][0] * jacobian[1][1]
        - jacobian[0][1] * jacobian[1][0]
    )
    if determinant == 0:
        raise ArithmeticError(singular_message)
    digits = precision_dps - 8
    return (
        (
            mp.nstr(jacobian[1][1] / determinant, digits),
            mp.nstr(-jacobian[0][1] / determinant, digits),
        ),
        (
            mp.nstr(-jacobian[1][0] / determinant, digits),
            mp.nstr(jacobian[0][0] / determinant, digits),
        ),
    )


def _strict_subset(inner: Any, outer: Any) -> bool:
    return bool(
        libmp.mpf_gt(inner._mpi_[0], outer._mpi_[0])
        and libmp.mpf_lt(inner._mpi_[1], outer._mpi_[1])
    )


def _contains_zero(interval: Any) -> bool:
    return bool(
        libmp.mpf_le(interval._mpi_[0], libmp.fzero)
        and libmp.mpf_ge(interval._mpi_[1], libmp.fzero)
    )


def _strictly_positive(interval: Any) -> bool:
    return bool(libmp.mpf_gt(interval._mpi_[0], libmp.fzero))


def _strictly_negative(interval: Any) -> bool:
    return bool(libmp.mpf_lt(interval._mpi_[1], libmp.fzero))


def _contains_decimal(interval: Any, value: str) -> bool:
    point = iv.mpf(value)
    return bool(
        libmp.mpf_le(interval._mpi_[0], point._mpi_[0])
        and libmp.mpf_ge(interval._mpi_[1], point._mpi_[1])
    )


def _interval_record(value: Any, digits: int) -> dict[str, Any]:
    lower, upper = value._mpi_
    with mp.workdps(digits + 10):
        width = mp.make_mpf(upper) - mp.make_mpf(lower)
        midpoint = (mp.make_mpf(upper) + mp.make_mpf(lower)) / 2
        return {
            "lower": libmp.to_str(lower, digits),
            "upper": libmp.to_str(upper, digits),
            "lower_binary": list(lower),
            "upper_binary": list(upper),
            "width": mp.nstr(width, digits),
            "midpoint": mp.nstr(midpoint, digits),
            "contains_zero": _contains_zero(value),
        }


def _ordered_decimal_interval(
    values: tuple[str, str], *, name: str, precision_dps: int
) -> tuple[str, str]:
    if (
        type(values) is not tuple
        or len(values) != 2
        or any(type(value) is not str for value in values)
    ):
        raise TypeError(f"{name} must be a pair of decimal strings")
    with mp.workdps(precision_dps):
        lower, upper = (mp.mpf(value) for value in values)
        if not (mp.isfinite(lower) and mp.isfinite(upper) and lower <= upper):
            raise ValueError(f"{name} must be finite and ordered")
    return values


def interval_balance_and_jacobian_box(
    *,
    radius_interval: tuple[str, str],
    theta_interval: tuple[str, str],
    parameters: IntervalRotatingWaveParameters,
    precision_dps: int,
) -> dict[str, Any]:
    """Evaluate finite-H balance and Jacobian on one outward-rounded box."""

    if type(precision_dps) is not int or precision_dps < 50:
        raise ValueError("precision_dps must be an integer of at least 50")
    radius_interval = _ordered_decimal_interval(
        radius_interval, name="radius_interval", precision_dps=precision_dps
    )
    theta_interval = _ordered_decimal_interval(
        theta_interval, name="theta_interval", precision_dps=precision_dps
    )
    previous_iv_dps = iv.dps
    iv.dps = precision_dps
    try:
        radius = iv.mpf(list(radius_interval))
        theta = iv.mpf(list(theta_interval))
        balance, jacobian, components = _balance_and_jacobian(
            iv, radius, theta, parameters
        )
        digits = precision_dps + 8
        return {
            "box": [_interval_record(radius, digits), _interval_record(theta, digits)],
            "balance": [_interval_record(value, digits) for value in balance],
            "jacobian": [
                [_interval_record(value, digits) for value in row]
                for row in jacobian
            ],
            "components": [
                _interval_record(value, digits) for value in components
            ],
        }
    finally:
        iv.dps = previous_iv_dps


def _same_parameters_except_horizon(
    first: IntervalRotatingWaveParameters,
    second: IntervalRotatingWaveParameters,
) -> bool:
    names = (
        "alpha",
        "memory_mass",
        "eta",
        "sigma_rep",
        "sigma_att",
        "amplitude_rep",
        "amplitude_att",
    )
    return all(getattr(first, name) == getattr(second, name) for name in names)


def certify_rotating_wave_homotopy_box(
    *,
    radius: str,
    theta: str,
    radius_half_width: str,
    theta_half_width: str,
    s_interval: tuple[str, str],
    first_parameters: IntervalRotatingWaveParameters,
    second_parameters: IntervalRotatingWaveParameters,
    precision_dps: int,
) -> dict[str, Any]:
    """Apply Krawczyk to a fixed box across one closed horizon-homotopy slab."""

    if type(precision_dps) is not int or precision_dps < 50:
        raise ValueError("precision_dps must be an integer of at least 50")
    if not _same_parameters_except_horizon(first_parameters, second_parameters):
        raise ValueError("homotopy may change only the horizon")
    s_interval = _ordered_decimal_interval(
        s_interval, name="s_interval", precision_dps=precision_dps
    )
    with mp.workdps(precision_dps):
        s_lower, s_upper = (mp.mpf(value) for value in s_interval)
        if s_lower < 0 or s_upper > 1:
            raise ValueError("s_interval must lie in [0, 1]")
        for name, value in (("radius", radius), ("theta", theta)):
            if type(value) is not str:
                raise TypeError(f"{name} must be a decimal string")
            numeric = mp.mpf(value)
            if not mp.isfinite(numeric):
                raise ValueError(f"{name} must be finite")
        for name, value in (
            ("radius_half_width", radius_half_width),
            ("theta_half_width", theta_half_width),
        ):
            numeric = mp.mpf(value)
            if not mp.isfinite(numeric) or numeric <= 0:
                raise ValueError(f"{name} must be positive and finite")

    previous_iv_dps = iv.dps
    iv.dps = precision_dps
    try:
        center = (iv.mpf(radius), iv.mpf(theta))
        box = (
            center[0] + iv.mpf([f"-{radius_half_width}", radius_half_width]),
            center[1] + iv.mpf([f"-{theta_half_width}", theta_half_width]),
        )
        s_box = iv.mpf(list(s_interval))
        first_center, _, _ = _balance_and_jacobian(
            iv, center[0], center[1], first_parameters
        )
        second_center, _, _ = _balance_and_jacobian(
            iv, center[0], center[1], second_parameters
        )
        function_at_center = tuple(
            first_center[index]
            + s_box * (second_center[index] - first_center[index])
            for index in range(2)
        )
        first_box, first_jacobian, _ = _balance_and_jacobian(
            iv, box[0], box[1], first_parameters
        )
        second_box, second_jacobian, _ = _balance_and_jacobian(
            iv, box[0], box[1], second_parameters
        )
        function_box = tuple(
            first_box[index] + s_box * (second_box[index] - first_box[index])
            for index in range(2)
        )
        jacobian_box = tuple(
            tuple(
                first_jacobian[row][column]
                + s_box
                * (
                    second_jacobian[row][column]
                    - first_jacobian[row][column]
                )
                for column in range(2)
            )
            for row in range(2)
        )

        with mp.workdps(precision_dps):
            point_radius = mp.mpf(radius)
            point_theta = mp.mpf(theta)
            point_s = (mp.mpf(s_interval[0]) + mp.mpf(s_interval[1])) / 2
            _, first_point_jacobian, _ = _balance_and_jacobian(
                mp, point_radius, point_theta, first_parameters
            )
            _, second_point_jacobian, _ = _balance_and_jacobian(
                mp, point_radius, point_theta, second_parameters
            )
            point_jacobian = tuple(
                tuple(
                    first_point_jacobian[row][column]
                    + point_s
                    * (
                        second_point_jacobian[row][column]
                        - first_point_jacobian[row][column]
                    )
                    for column in range(2)
                )
                for row in range(2)
            )
            inverse_strings = _inverse_jacobian_strings(
                point_jacobian,
                precision_dps=precision_dps,
                singular_message="homotopy point Jacobian is singular",
            )
        inverse = tuple(
            tuple(iv.mpf(value) for value in row) for row in inverse_strings
        )
        image = krawczyk_image(
            center=center,
            box=box,
            function_at_center=function_at_center,
            jacobian_box=jacobian_box,
            inverse_point_jacobian=inverse,
        )
        strict_interior = all(
            _strict_subset(image[index], box[index]) for index in range(2)
        )
        digits = precision_dps + 8
        return {
            "precision_dps": precision_dps,
            "s_interval": list(s_interval),
            "center": {"radius": radius, "theta": theta},
            "half_width": {
                "radius": radius_half_width,
                "theta": theta_half_width,
            },
            "box": [_interval_record(value, digits) for value in box],
            "function_at_center": [
                _interval_record(value, digits) for value in function_at_center
            ],
            "function_box": [
                _interval_record(value, digits) for value in function_box
            ],
            "jacobian_box": [
                [_interval_record(value, digits) for value in row]
                for row in jacobian_box
            ],
            "inverse_point_jacobian": [list(row) for row in inverse_strings],
            "krawczyk_image": [_interval_record(value, digits) for value in image],
            "gates": {"krawczyk_strict_interior": strict_interior},
            "pass": strict_interior,
        }
    finally:
        iv.dps = previous_iv_dps


def certify_rotating_wave_box(
    *,
    radius: str,
    theta: str,
    radius_half_width: str,
    theta_half_width: str,
    parameters: IntervalRotatingWaveParameters,
    precision_dps: int,
) -> dict[str, Any]:
    """Apply a directed-rounding Krawczyk certificate to one fixed box."""

    if precision_dps < 50:
        raise ValueError("precision_dps must be at least 50")
    for name, value in (
        ("radius_half_width", radius_half_width),
        ("theta_half_width", theta_half_width),
    ):
        try:
            numeric = float(value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"{name} must be a decimal string") from error
        if not math.isfinite(numeric) or numeric <= 0.0:
            raise ValueError(f"{name} must be positive and finite")

    previous_iv_dps = iv.dps
    iv.dps = precision_dps
    try:
        center = (iv.mpf(radius), iv.mpf(theta))
        box = (
            center[0] + iv.mpf([f"-{radius_half_width}", radius_half_width]),
            center[1] + iv.mpf([f"-{theta_half_width}", theta_half_width]),
        )
        function_at_center, _, _ = _balance_and_jacobian(
            iv,
            center[0],
            center[1],
            parameters,
        )
        function_box, jacobian_box, components_box = _balance_and_jacobian(
            iv,
            box[0],
            box[1],
            parameters,
        )

        with mp.workdps(precision_dps):
            _, point_jacobian, _ = _balance_and_jacobian(
                mp,
                mp.mpf(radius),
                mp.mpf(theta),
                parameters,
            )
            inverse_strings = _inverse_jacobian_strings(
                point_jacobian,
                precision_dps=precision_dps,
                singular_message="point Jacobian is singular",
            )
        inverse = tuple(
            tuple(iv.mpf(value) for value in row) for row in inverse_strings
        )
        inverse_determinant = (
            inverse[0][0] * inverse[1][1] - inverse[0][1] * inverse[1][0]
        )
        image = krawczyk_image(
            center=center,
            box=box,
            function_at_center=function_at_center,
            jacobian_box=jacobian_box,
            inverse_point_jacobian=inverse,
        )
        radial_eta = (iv.mpf(1) - iv.cos(box[1])) / components_box[0]
        tangential_eta = -iv.sin(box[1]) / components_box[1]
        physical_domain = bool(
            _strictly_positive(box[0])
            and _strictly_positive(box[1])
            and libmp.mpf_lt(box[1]._mpi_[1], iv.pi._mpi_[0])
        )
        gates = {
            "physical_domain": physical_domain,
            "inverse_nonsingular": not _contains_zero(inverse_determinant),
            "function_box_contains_zero": all(
                _contains_zero(value) for value in function_box
            ),
            "radial_component_positive": _strictly_positive(components_box[0]),
            "tangential_component_negative": _strictly_negative(components_box[1]),
            "registered_eta_in_radial_eta_interval": _contains_decimal(
                radial_eta, parameters.eta
            ),
            "registered_eta_in_tangential_eta_interval": _contains_decimal(
                tangential_eta, parameters.eta
            ),
            "krawczyk_strict_interior": all(
                _strict_subset(image[index], box[index]) for index in range(2)
            ),
        }
        digits = precision_dps + 8
        return {
            "precision_dps": precision_dps,
            "center": {"radius": radius, "theta": theta},
            "half_width": {
                "radius": radius_half_width,
                "theta": theta_half_width,
            },
            "box": [_interval_record(value, digits) for value in box],
            "function_at_center": [
                _interval_record(value, digits) for value in function_at_center
            ],
            "function_box": [
                _interval_record(value, digits) for value in function_box
            ],
            "jacobian_box": [
                [_interval_record(value, digits) for value in row]
                for row in jacobian_box
            ],
            "components_box": [
                _interval_record(value, digits) for value in components_box
            ],
            "required_eta": {
                "radial": _interval_record(radial_eta, digits),
                "tangential": _interval_record(tangential_eta, digits),
            },
            "inverse_point_jacobian": [list(row) for row in inverse_strings],
            "inverse_determinant": _interval_record(inverse_determinant, digits),
            "krawczyk_image": [
                _interval_record(value, digits) for value in image
            ],
            "gates": gates,
            "pass": all(gates.values()),
        }
    finally:
        iv.dps = previous_iv_dps


def certify_rotating_wave_tail_box(
    *,
    radius: str,
    theta: str,
    radius_half_width: str,
    theta_half_width: str,
    parameters: IntervalRotatingWaveParameters,
    residual_tail_bound: str,
    jacobian_radius_tail_bound: str,
    jacobian_theta_tail_bound: str,
    precision_dps: int,
) -> dict[str, Any]:
    """Certify a root after outward-rounded infinite-tail augmentation.

    The supplied scalar bounds are Euclidean norm bounds for the omitted
    residual and the two omitted Jacobian columns.  Hence every component is
    enclosed by the corresponding symmetric interval.  The finite-H point
    Jacobian is used only as a numerical preconditioner; the Krawczyk
    Jacobian interval contains the full finite box plus the omitted tail.
    """

    if type(precision_dps) is not int or precision_dps < 50:
        raise ValueError("precision_dps must be an integer of at least 50")
    decimal_values = (
        ("radius", radius, False),
        ("theta", theta, False),
        ("radius_half_width", radius_half_width, True),
        ("theta_half_width", theta_half_width, True),
        ("residual_tail_bound", residual_tail_bound, False),
        ("jacobian_radius_tail_bound", jacobian_radius_tail_bound, False),
        ("jacobian_theta_tail_bound", jacobian_theta_tail_bound, False),
    )
    with mp.workdps(precision_dps):
        for name, value, strictly_positive in decimal_values:
            if type(value) is not str:
                raise TypeError(f"{name} must be a decimal string")
            numeric = mp.mpf(value)
            if not mp.isfinite(numeric) or numeric < 0:
                raise ValueError(f"{name} must be nonnegative and finite")
            if strictly_positive and numeric == 0:
                raise ValueError(f"{name} must be positive")

    previous_iv_dps = iv.dps
    iv.dps = precision_dps
    try:
        center = (iv.mpf(radius), iv.mpf(theta))
        box = (
            center[0] + iv.mpf([f"-{radius_half_width}", radius_half_width]),
            center[1] + iv.mpf([f"-{theta_half_width}", theta_half_width]),
        )
        finite_center, _, _ = _balance_and_jacobian(
            iv, center[0], center[1], parameters
        )
        finite_box, finite_jacobian_box, _ = _balance_and_jacobian(
            iv, box[0], box[1], parameters
        )
        residual_uncertainty = iv.mpf(
            [f"-{residual_tail_bound}", residual_tail_bound]
        )
        column_uncertainties = (
            iv.mpf(
                [f"-{jacobian_radius_tail_bound}", jacobian_radius_tail_bound]
            ),
            iv.mpf(
                [f"-{jacobian_theta_tail_bound}", jacobian_theta_tail_bound]
            ),
        )
        function_at_center = tuple(
            value + residual_uncertainty for value in finite_center
        )
        function_box = tuple(value + residual_uncertainty for value in finite_box)
        jacobian_box = tuple(
            tuple(
                finite_jacobian_box[row][column] + column_uncertainties[column]
                for column in range(2)
            )
            for row in range(2)
        )

        with mp.workdps(precision_dps):
            _, point_jacobian, _ = _balance_and_jacobian(
                mp, mp.mpf(radius), mp.mpf(theta), parameters
            )
            inverse_strings = _inverse_jacobian_strings(
                point_jacobian,
                precision_dps=precision_dps,
                singular_message="finite point Jacobian is singular",
            )
        inverse = tuple(
            tuple(iv.mpf(value) for value in row) for row in inverse_strings
        )
        inverse_determinant = (
            inverse[0][0] * inverse[1][1] - inverse[0][1] * inverse[1][0]
        )
        image = krawczyk_image(
            center=center,
            box=box,
            function_at_center=function_at_center,
            jacobian_box=jacobian_box,
            inverse_point_jacobian=inverse,
        )
        gates = {
            "physical_domain": bool(
                _strictly_positive(box[0])
                and _strictly_positive(box[1])
                and libmp.mpf_lt(box[1]._mpi_[1], iv.pi._mpi_[0])
            ),
            "inverse_nonsingular": not _contains_zero(inverse_determinant),
            "function_box_contains_zero": all(
                _contains_zero(value) for value in function_box
            ),
            "krawczyk_strict_interior": all(
                _strict_subset(image[index], box[index]) for index in range(2)
            ),
        }
        digits = precision_dps + 8
        return {
            "precision_dps": precision_dps,
            "center": {"radius": radius, "theta": theta},
            "half_width": {
                "radius": radius_half_width,
                "theta": theta_half_width,
            },
            "tail_bounds": {
                "residual": residual_tail_bound,
                "jacobian_radius": jacobian_radius_tail_bound,
                "jacobian_theta": jacobian_theta_tail_bound,
            },
            "box": [_interval_record(value, digits) for value in box],
            "finite_function_at_center": [
                _interval_record(value, digits) for value in finite_center
            ],
            "function_at_center": [
                _interval_record(value, digits) for value in function_at_center
            ],
            "function_box": [
                _interval_record(value, digits) for value in function_box
            ],
            "finite_jacobian_box": [
                [_interval_record(value, digits) for value in row]
                for row in finite_jacobian_box
            ],
            "jacobian_box": [
                [_interval_record(value, digits) for value in row]
                for row in jacobian_box
            ],
            "inverse_point_jacobian": [list(row) for row in inverse_strings],
            "inverse_determinant": _interval_record(inverse_determinant, digits),
            "krawczyk_image": [
                _interval_record(value, digits) for value in image
            ],
            "gates": gates,
            "pass": all(gates.values()),
        }
    finally:
        iv.dps = previous_iv_dps
