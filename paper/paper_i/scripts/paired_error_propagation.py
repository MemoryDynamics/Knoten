"""Conditional split-state error propagation and a bounded pairwise mean.

State bounds REQUIRE supplied per-step defects and lag bounds. They do
not certify exprel, weights, a PRNG, or the existing production runner.
Only the scalar reducer includes outward-rounded arithmetic bounds,
under normal-or-zero IEEE binary64 round-to-nearest without reassociation.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math

import numpy as np

from paired_residual_precision import _checked_epsilon, _checked_kernel
from paired_transport import _positive_integer


def _nonnegative_vector(values, name):
    values = np.asarray(values, dtype=float)
    if (
        values.ndim != 1
        or len(values) < 1
        or not np.all(np.isfinite(values))
        or np.any(values < 0)
    ):
        raise ValueError(f"{name} must be a finite nonnegative vector")
    return values


def _lag_parameters(alpha, eta, kernel, count):
    if (
        not np.isfinite(alpha)
        or not 0 < alpha < 1
        or not 0 < 1 - alpha < 1
        or not np.isfinite(eta)
    ):
        raise ValueError("require resolved 0<alpha<1 and finite eta")
    ar, aa, sr, sa = _checked_kernel(kernel)
    gamma = alpha * (1 - alpha) ** np.arange(1, count + 1)
    linear = abs(eta * (aa / sa**2 - ar / sr**2))
    full = abs(eta) * (abs(ar) / sr**2 + abs(aa) / sa**2)
    cubic = abs(eta) * (abs(ar) / (2 * sr**4) + abs(aa) / (2 * sa**4))
    if not np.all(np.isfinite([linear, full, cubic])):
        raise ValueError("kernel bounds overflow")
    return gamma, linear, full, cubic


def propagate_split_error(
    linear_error,
    residual_error,
    normalized_lag_norms,
    linear_defects,
    residual_defects,
    alpha,
    eta,
    kernel,
):
    """One real-arithmetic error-envelope step, evaluated in floating point.

    Error/defect entries are Euclidean norm bounds per lag, not signed
    component errors. normalized_lag_norms bounds |Wtilde_j+eps^2 Rtilde_j|.
    Defects compare the computed update with the EXACT split update at
    its computed inputs. Norms/coefficients of this helper are not intervals.
    """
    ew, er, norms, dw, dr = [
        _nonnegative_vector(values, name)
        for values, name in (
            (linear_error, "linear error"),
            (residual_error, "residual error"),
            (normalized_lag_norms, "lag norms"),
            (linear_defects, "linear defects"),
            (residual_defects, "residual defects"),
        )
    ]
    if any(a.shape != ew.shape for a in (er, norms, dw, dr)):
        raise ValueError("all lag arrays must have the same shape")
    gamma, linear, full, cubic = _lag_parameters(alpha, eta, kernel, len(ew))
    cross = 3 * cubic * (gamma @ ((norms + ew) ** 2 * ew))
    next_w = np.r_[0.0, ew[:-1]] + linear * (gamma @ ew) + dw
    next_r = np.r_[0.0, er[:-1]] + full * (gamma @ er) + cross + dr
    if not np.all(np.isfinite(next_w)) or not np.all(np.isfinite(next_r)):
        raise ValueError("error propagation overflows")
    return next_w, next_r


def constant_defect_envelope(weights, gain, defects):
    """Exact positive-lag resolvent formula for a constant defect envelope.

    If initial errors lie below the returned vector and each subsequent
    defect is <= defects, this vector bounds ALL times when gain*sum(j*w)<1.
    This numerical evaluation is not outward-rounded certification.
    """
    weights, defects = (
        _nonnegative_vector(weights, "weights"),
        _nonnegative_vector(defects, "defects"),
    )
    if weights.shape != defects.shape or not np.isfinite(gain) or gain < 0:
        raise ValueError("require matching arrays and finite gain>=0")
    ages = np.arange(1, len(weights) + 1)
    theta = gain * (weights @ ages)
    if not np.isfinite(theta) or theta >= 1:
        raise ValueError("constant envelope needs strict finite-history contraction")
    cumulative = np.cumsum(defects)
    force = gain * (weights @ cumulative) / (1 - theta)
    result = cumulative + ages * force
    if not np.all(np.isfinite(result)):
        raise ValueError("constant envelope overflows")
    return result


def uniform_split_envelope(
    linear_defects, residual_defects, normalized_lag_caps, alpha, eta, kernel
):
    """Time-uniform bound conditional on LOCAL defects and GLOBAL lag caps.

    Caps bound the computed normalized lag vectors for every retained step;
    neither they nor the local defects are inferred from short tests.
    """
    dw, dr, caps = [
        _nonnegative_vector(values, name)
        for values, name in (
            (linear_defects, "linear defects"),
            (residual_defects, "residual defects"),
            (normalized_lag_caps, "lag caps"),
        )
    ]
    if dw.shape != dr.shape or dw.shape != caps.shape:
        raise ValueError("all lag arrays must have the same shape")
    gamma, linear, full, cubic = _lag_parameters(alpha, eta, kernel, len(dw))
    ew = constant_defect_envelope(gamma, linear, dw)
    cross = 3 * cubic * (gamma @ ((caps + ew) ** 2 * ew))
    er = constant_defect_envelope(gamma, full, dr + cross)
    return ew, er


def paired_block_input_error(
    linear_block, residual_blocks, linear_error, residual_errors, epsilon, length
):
    """Bound only input perturbation of the exact normalized paired raw block.

    Block errors must INCLUDE accumulation of increments. Evaluation of
    this block expression and the two-length/seed reductions need their
    own defect bounds. This helper does not supply them by default.
    """
    _positive_integer(length, "length")
    _checked_epsilon(epsilon)
    w, r = (
        np.asarray(linear_block, dtype=float),
        np.asarray(residual_blocks, dtype=float),
    )
    errors = _nonnegative_vector(residual_errors, "residual block errors")
    if (
        w.ndim != 1
        or len(w) < 1
        or r.shape != (2, len(w))
        or errors.shape != (2,)
        or not np.all(np.isfinite(w))
        or not np.all(np.isfinite(r))
        or not np.isfinite(linear_error)
        or linear_error < 0
    ):
        raise ValueError("require finite two-kernel blocks, errors and eps>=0")
    ea, eb = errors
    linear = linear_error * np.linalg.norm(r[1] - r[0]) + (
        np.linalg.norm(w) + linear_error
    ) * (ea + eb)
    quadratic = (
        2 * np.linalg.norm(r[0]) * ea + ea**2 + 2 * np.linalg.norm(r[1]) * eb + eb**2
    )
    result = (2 * linear + epsilon**2 * quadratic) / (2 * len(w) * length)
    if not np.isfinite(result):
        raise ValueError("block error bound overflows")
    return float(result)


def _normal_or_zero(value):
    a = np.asarray(value, dtype=float)
    return bool(
        np.all(np.isfinite(a))
        and np.all((a == 0) | (np.abs(a) >= np.finfo(float).tiny))
    )


def _up(value):
    if value == 0:
        # Do not turn an unresolved underflow into a spurious zero bound.
        raise ValueError("positive error-bound arithmetic underflowed")
    result = math.nextafter(float(value), math.inf)
    if not _normal_or_zero(result):
        raise ValueError("error-bound arithmetic left the normal finite domain")
    return result


def _gamma_upper(depth):
    if depth == 0:
        return 0.0
    if depth < 0 or depth >= 2**52:
        raise ValueError("unresolved rounding depth")
    return _up(float(Fraction(depth, 2**53 - depth)))


def _pairwise_sum(values):
    level = values.copy()
    while len(level) > 1:
        paired = len(level) // 2 * 2
        with np.errstate(over="ignore", under="ignore", invalid="ignore"):
            following = level[:paired:2] + level[1:paired:2]
        if len(level) % 2:
            following = np.r_[following, level[-1]]
        if not _normal_or_zero(following):
            raise ValueError("pairwise addition left the normal-or-zero finite domain")
        level = following
    return float(level[0])


def bounded_pairwise_mean(values):
    """Sum/mean and outward bounds relative to EXACT supplied binary64 values.

    Requires IEEE binary64 round-to-nearest, no fast-math/reassociation,
    normal-or-zero checked intermediates and exact count conversion.
    Does NOT cover error already present in individual input values.
    """
    values = np.asarray(values, dtype=float)
    if (
        values.ndim != 1
        or len(values) < 1
        or len(values) > 2**53
        or not _normal_or_zero(values)
    ):
        raise ValueError("require nonempty finite normal-or-zero binary64 input values")
    count = len(values)
    depth = (count - 1).bit_length()
    gamma = _gamma_upper(depth)
    total, magnitude = _pairwise_sum(values), _pairwise_sum(np.abs(values))
    mean = total / count
    if not _normal_or_zero(mean):
        raise ValueError("mean division left the normal-or-zero domain")
    if total != 0 and mean == 0:
        raise ValueError("mean division underflowed")
    if gamma == 0 or magnitude == 0:
        sum_error, mean_error = 0.0, 0.0
        magnitude_upper = magnitude
    else:
        denominator_lower = math.nextafter(1.0 - gamma, -math.inf)
        if denominator_lower <= 0:
            raise ValueError("unresolved positive sum envelope")
        magnitude_upper = _up(magnitude / denominator_lower)
        sum_error = _up(gamma * magnitude_upper)
        mean_error = _up(sum_error / count)
        if mean != 0:
            division_error = _up(_gamma_upper(1) * abs(mean))
            mean_error = _up(mean_error + division_error)
    return {
        "sum": total,
        "mean": mean,
        "count": count,
        "depth": depth,
        "gamma_upper": gamma,
        "absolute_input_sum_upper": magnitude_upper,
        "sum_error_bound": sum_error,
        "mean_error_bound": mean_error,
    }


def audit_accumulation_contract():
    """Unit-defect gains and a declared synthetic reducer stress case only."""
    alpha, horizon = 0.01, 600
    eta = 0.5 * alpha / ((1 - alpha) * (1 + 35 / 9))
    ages = np.arange(1, horizon)
    gamma, linear, full, _ = _lag_parameters(alpha, eta, (1, 35, 1, 3), horizon - 1)
    ew = constant_defect_envelope(gamma, linear, np.ones(horizon - 1))
    er = constant_defect_envelope(gamma, full, np.ones(horizon - 1))
    values = np.tile(np.array([1e16, 1.0, -1e16, 2.0, -0.5]), 200)
    summary = bounded_pairwise_mean(values)
    exact = sum((Fraction.from_float(float(x)) for x in values), Fraction())
    return {
        "scope": "conditional defect amplification, not validated local defects or a whole-simulator certificate",
        "horizon": horizon,
        "finite_linear_feedback_mass": float(linear * (gamma @ ages)),
        "finite_full_feedback_mass": float(full * (gamma @ ages)),
        "linear_uniform_unit_defect_increment_gain": float(ew[0]),
        "residual_uniform_unit_defect_increment_gain_excluding_linear_cross_error": float(
            er[0]
        ),
        "linear_largest_lag_gain": float(ew[-1]),
        "residual_largest_lag_gain_excluding_linear_cross_error": float(er[-1]),
        "synthetic_cancellation_reducer": summary,
        "synthetic_exact_sum": float(exact),
        "synthetic_actual_sum_error": float(
            abs(Fraction.from_float(summary["sum"]) - exact)
        ),
        "one_million_values_tree_depth": (1_000_000 - 1).bit_length(),
        "one_million_values_gamma_upper": _gamma_upper((1_000_000 - 1).bit_length()),
    }


if __name__ == "__main__":
    print(json.dumps(audit_accumulation_contract(), indent=2))
