"""Geometry and independent-replicate diagnostics on supplied paths only."""

from dataclasses import asdict
from numbers import Integral

import numpy as np

from .kernels import ScalarReadoutKernel, two_scale_local_curvature
from .pair_lag_diagnostics import _probabilities, gaussian_gradient_remainder


def _window(start, stop, minimum, length):
    if any(isinstance(v, bool) or not isinstance(v, Integral) for v in (start, stop)):
        raise ValueError("window endpoints must be integers")
    if not minimum <= start < stop <= length:
        raise ValueError("window lacks complete past support")


def _constants(kernel):
    curvature = two_scale_local_curvature(**asdict(kernel))
    amplitudes = np.abs([kernel.amplitude_rep, kernel.amplitude_att])
    scales = np.array([kernel.sigma_rep, kernel.sigma_att])
    values = (
        curvature,
        np.sum(amplitudes / scales**4) / 2,
        np.sum(amplitudes / scales**2),
        np.exp(-0.5) * np.sum(amplitudes / scales),
    )
    if not np.isfinite(values).all():
        raise ValueError("kernel constants must be finite")
    return values


def fifo_centers(initial_history, positions, weights):
    """Reconstruct weighted centers, including initial deposits, without a solver.

    positions[0] is the initial current point; only rows 1..N are new deposits.
    The initial history is newest first and need not start with positions[0].
    """
    initial, points = np.asarray(initial_history, float), np.asarray(positions, float)
    p = _probabilities(weights)
    if (
        initial.ndim != 2
        or points.ndim != 2
        or len(points) < 1
        or initial.shape != (len(p), points.shape[1])
        or points.shape[1] < 1
        or not np.isfinite(initial).all()
        or not np.isfinite(points).all()
    ):
        raise ValueError(
            "finite history and point arrays with matching dimension required"
        )
    centers = np.zeros_like(points)
    centers[0] = p @ initial
    if len(points) > 1:
        for axis in range(points.shape[1]):
            centers[1:, axis] = np.convolve(points[1:, axis], p)[: len(points) - 1]
        for step in range(1, min(len(points), len(p))):
            centers[step] += p[step:] @ initial[: len(p) - step]
    if not np.isfinite(centers).all():
        raise ValueError("non-finite reconstructed centers")
    return centers


def analyze_pair_geometry(
    positions,
    initial_histories,
    weights,
    separation,
    *,
    start,
    stop,
    kernel: ScalarReadoutKernel,
):
    """Exact native-minus-frozen readout and bounds; no stationarity assumption.

    Positions have shape (updates+1, 2, dim). Both histories must have been fully
    replaced before the measurement window, to use only recorded point lags.
    Kernel parameters must already include the write/read convolution.
    """
    points = np.asarray(positions, float)
    if (
        points.ndim != 3
        or points.shape[1] != 2
        or points.shape[2] < 1
        or not np.isfinite(points).all()
        or len(initial_histories) != 2
        or len(weights) != 2
    ):
        raise ValueError("two finite synchronized point paths and histories required")
    probabilities = [_probabilities(w) for w in weights]
    _window(start, stop, max(map(len, probabilities)), len(points))
    r = np.asarray(separation, float)
    if r.shape != (points.shape[2],) or not np.isfinite(r).all():
        raise ValueError("finite reference separation matching dim required")
    centers = np.stack(
        [
            fifo_centers(initial_histories[i], points[:, i], weights[i])
            for i in range(2)
        ],
        axis=1,
    )
    inner = points - centers
    curvature, c3, l2, _ = _constants(kernel)
    separation_error = centers[start:stop, 0] - centers[start:stop, 1] - r
    sep_budget = float(np.mean(np.linalg.norm(separation_error, axis=1)))
    rows = []
    for target, source, sign in ((0, 1, 1), (1, 0, -1)):
        linear = np.zeros(points.shape[2])
        nonlinear = np.zeros(points.shape[2])
        native_mean = np.zeros(points.shape[2])
        frozen_mean = np.zeros(points.shape[2])
        source_budget, nonlinear_bound = 0.0, 0.0
        for lag, p in enumerate(probabilities[source]):
            past = slice(start - lag, stop - lag)
            z = points[start:stop, target] - points[past, source]
            z0 = sign * r + inner[start:stop, target] - inner[past, source]
            motion = centers[start:stop, source] - centers[past, source]
            delta = sign * separation_error + motion
            rem, rem0 = (
                gaussian_gradient_remainder(z, kernel),
                gaussian_gradient_remainder(z0, kernel),
            )
            linear += p * curvature * np.mean(delta, axis=0)
            nonlinear += p * np.mean(rem - rem0, axis=0)
            native_mean += p * np.mean(curvature * z + rem, axis=0)
            frozen_mean += p * np.mean(curvature * z0 + rem0, axis=0)
            source_budget += p * np.mean(np.linalg.norm(motion, axis=1))
            radius = np.maximum(np.linalg.norm(z, axis=1), np.linalg.norm(z0, axis=1))
            nonlinear_bound += p * np.mean(
                3 * c3 * radius**2 * np.linalg.norm(delta, axis=1)
            )
        rows.append(
            dict(
                native_mean=native_mean,
                frozen_mean=frozen_mean,
                linear_correction=linear,
                nonlinear_correction=nonlinear,
                geometry_correction=linear + nonlinear,
                separation_motion_budget=sep_budget,
                source_motion_budget=float(source_budget),
                full_gradient_bound=l2 * (sep_budget + source_budget),
                nonlinear_bound=nonlinear_bound,
            )
        )
    if any(
        not np.isfinite(value).all()
        for row in rows
        for value in map(np.asarray, row.values())
    ):
        raise ValueError("non-finite geometry result")
    return {"centers": centers, "inner": inner, "directions": rows}


def paired_replica_contrast(
    first_inner,
    second_inner,
    separation,
    weights,
    *,
    start,
    stop,
    kernel: ScalarReadoutKernel,
):
    """Two whole replicas, matched versus crossed at the same time and lag.

    Each input has shape (2, updates, dim). Independence of the two replicas is
    a required external design assumption, never inferred by this function.
    """
    first, second = np.asarray(first_inner, float), np.asarray(second_inner, float)
    if (
        first.ndim != 3
        or first.shape[0] != 2
        or first.shape[2] < 1
        or second.shape != first.shape
        or not np.isfinite(first).all()
        or not np.isfinite(second).all()
        or len(weights) != 2
    ):
        raise ValueError("two finite replicas of each inner path required")
    p = [_probabilities(w) for w in weights]
    _window(start, stop, max(map(len, p)) - 1, first.shape[1])
    r = np.asarray(separation, float)
    if r.shape != (first.shape[2],) or not np.isfinite(r).all():
        raise ValueError("fixed finite reference separation matching dim required")
    _, _, _, gradient_bound = _constants(kernel)
    matrix = np.zeros((2, 2, 2, first.shape[2]))
    for direction, target, source, sign, ages in (
        (0, first, second, 1, p[1]),
        (1, second, first, -1, p[0]),
    ):
        for i in range(2):
            for j in range(2):
                for lag, weight in enumerate(ages):
                    z = (
                        sign * r
                        + target[i, start:stop]
                        - source[j, start - lag : stop - lag]
                    )
                    matrix[direction, i, j] += weight * np.mean(
                        gaussian_gradient_remainder(z, kernel), axis=0
                    )
    contrast = (
        matrix[:, 0, 0] + matrix[:, 1, 1] - matrix[:, 0, 1] - matrix[:, 1, 0]
    ) / 2
    if not np.isfinite(contrast).all():
        raise ValueError("non-finite replica contrast")
    return {"contrast": contrast, "global_norm_bound_per_direction": 2 * gradient_bound}


def replica_hoeffding_half_width(independent_pairs, kernel, *, family_size, alpha=0.05):
    """Two-sided simultaneous Hoeffding bound, excluding numerical error.

    Counts disjoint pairs of independent whole replicas, NEVER time points or
    overlapping pairings. Kernel bounds apply globally, not only to seen data.
    """
    if any(
        isinstance(v, bool) or not isinstance(v, Integral) or v < 1
        for v in (independent_pairs, family_size)
    ):
        raise ValueError("positive integer independent-pair and family counts required")
    if not np.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("alpha must be between zero and one")
    _, _, _, gradient_bound = _constants(kernel)
    return float(
        4
        * gradient_bound
        * np.sqrt(
            (np.log(2.0) + np.log(family_size) - np.log(alpha))
            / (2 * independent_pairs)
        )
    )
