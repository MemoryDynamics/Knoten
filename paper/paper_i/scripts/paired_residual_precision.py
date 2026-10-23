"""Exact scaled-residual algebra and small deterministic precision controls.

No stochastic target simulation, long-run error certificate or production
runner. Kernel tuples are (A_rep, A_att, s_rep, s_att). Histories are FULL
canonical memories, including a zero-force age-zero point.
"""

from __future__ import annotations

import json
import math
import platform
import timeit

import mpmath as mp
import numpy as np
import scipy
from scipy.special import exprel

from paired_transport import _positive_integer


KERNEL_PAIR = ((0, 26, 1, 3), (1, 35, 1, 3))


def _checked_kernel(kernel):
    kernel = np.asarray(kernel, dtype=float)
    if (
        kernel.shape != (4,)
        or not np.all(np.isfinite(kernel))
        or np.any(kernel[2:] <= 0)
    ):
        raise ValueError(
            "require (A_rep,A_att,s_rep,s_att), finite with positive scales"
        )
    return kernel


def _checked_epsilon(epsilon):
    if (
        not np.isfinite(epsilon)
        or epsilon < 0
        or epsilon > np.sqrt(np.finfo(float).max)
    ):
        raise ValueError("require finite eps>=0 with representable square")
    if epsilon > 0 and epsilon**2 == 0:
        raise ValueError("eps squared underflows")


def scaled_force_remainder(normalized_lags, epsilon, kernel):
    """[grad K(eps*u)-eps*kappa*u]/eps**3 without subtracting linear terms.

    At eps=0 return the continuous cubic limit. At eps>0 this is the FULL
    Gaussian force remainder, not a truncation. Arrays end in spatial d.
    """
    _checked_epsilon(epsilon)
    ar, aa, sr, sa = _checked_kernel(kernel)
    u = np.asarray(normalized_lags, dtype=float)
    if u.ndim < 1 or u.shape[-1] < 1 or not np.all(np.isfinite(u)):
        raise ValueError("require finite vectors with a nonempty spatial axis")
    r2 = np.sum(u * u, axis=-1)
    factor = ar / (2 * sr**4) * exprel(-(epsilon**2) * r2 / (2 * sr**2))
    factor -= aa / (2 * sa**4) * exprel(-(epsilon**2) * r2 / (2 * sa**2))
    result = (r2 * factor)[..., None] * u
    if not np.all(np.isfinite(result)):
        raise ValueError("scaled force overflows")
    return result


def split_step(linear_lags, residual_lags, innovation, alpha, eta, epsilon, kernels):
    """Advance full lag states v=eps*W+eps**3*R on one shared innovation.

    W has shape (H-1,d), R has shape (kernels,H-1,d). Coefficients are
    rebuilt as alpha*(1-alpha)**j, not normalized retained-memory weights.
    Kernel curvatures must match; equality in float is a domain check, not
    a symbolic certificate for arbitrary user-supplied kernel parameters.
    Inputs are not mutated. No contraction/rounding guarantee is implied.
    """
    _checked_epsilon(epsilon)
    if (
        not np.isfinite(alpha)
        or not 0 < alpha < 1
        or not 0 < 1 - alpha < 1
        or not np.isfinite(eta)
    ):
        raise ValueError("require resolved 0<alpha<1 and finite eta")
    w = np.asarray(linear_lags, dtype=float)
    r = np.asarray(residual_lags, dtype=float)
    innovation = np.asarray(innovation, dtype=float)
    kernels = np.asarray([_checked_kernel(kernel) for kernel in kernels])
    if (
        w.ndim != 2
        or min(w.shape) < 1
        or kernels.ndim != 2
        or r.shape != (len(kernels), *w.shape)
        or innovation.shape != (w.shape[1],)
        or not all(np.all(np.isfinite(a)) for a in (w, r, innovation))
    ):
        raise ValueError("require compatible finite full lag states and one innovation")
    curvatures = kernels[:, 1] / kernels[:, 3] ** 2 - kernels[:, 0] / kernels[:, 2] ** 2
    if not np.all(curvatures == curvatures[0]):
        raise ValueError("kernel curvatures must match")
    kappa = curvatures[0]
    gamma = alpha * (1 - alpha) ** np.arange(1, len(w) + 1)
    w_increment = innovation - eta * kappa * (gamma @ w)
    r_increment = np.empty((len(kernels), w.shape[1]))
    for k, kernel in enumerate(kernels):
        force = scaled_force_remainder(w + epsilon**2 * r[k], epsilon, kernel)
        r_increment[k] = -eta * (kappa * (gamma @ r[k]) + gamma @ force)
    next_w = np.broadcast_to(w_increment, w.shape).copy()
    next_w[1:] += w[:-1]
    next_r = np.broadcast_to(r_increment[:, None, :], r.shape).copy()
    next_r[:, 1:] += r[:, :-1]
    if not np.all(np.isfinite(next_w)) or not np.all(np.isfinite(next_r)):
        raise ValueError("split update overflows")
    return next_w, next_r


def paired_two_length_values(linear_blocks, residual_blocks, epsilon, length):
    """Per-superblock (Dhat_T,second-Dhat_T,first)/eps**4 without that division.

    Inputs are vector SUMS of W and R increments in successive length-L
    blocks. This is the exact finite-noise statistic; eps=0 gives its
    response limit. No variance or independence claim is made here.
    """
    _checked_epsilon(epsilon)
    _positive_integer(length, "length")
    w = np.asarray(linear_blocks, dtype=float)
    r = np.asarray(residual_blocks, dtype=float)
    if (
        w.ndim != 2
        or min(w.shape) < 1
        or len(w) % 2
        or r.shape != (2, *w.shape)
        or not np.all(np.isfinite(w))
        or not np.all(np.isfinite(r))
    ):
        raise ValueError(
            "require an even number of finite blocks and exactly two kernels"
        )
    dimension = w.shape[1]

    def raw(wb, rb, block_length):
        difference, total = rb[1] - rb[0], rb[1] + rb[0]
        return (
            2 * np.sum(wb * difference, axis=-1)
            + epsilon**2 * np.sum(difference * total, axis=-1)
        ) / (2 * dimension * block_length)

    short = raw(w, r, length).reshape(-1, 2).mean(axis=1)
    long = raw(
        w.reshape(-1, 2, dimension).sum(axis=1),
        r.reshape(2, -1, 2, dimension).sum(axis=2),
        2 * length,
    )
    result = 2 * long - short
    if not np.all(np.isfinite(result)):
        raise ValueError("paired statistic overflows")
    return result


def _direct_position_reference(
    innovations, alpha, eta, epsilon, horizon, kernels, digits
):
    """Independent high-precision ABSOLUTE-position recursion, full exponentials.

    Not the split recurrence: small remainders are obtained by subtracting
    only after the entire calculation at the requested decimal precision.
    This bounded fixture is not a general stochastic production simulator.
    """
    with mp.workdps(digits):
        alpha, eta, eps = map(mp.mpf, (alpha, eta, epsilon))
        kernels = [tuple(map(mp.mpf, kernel)) for kernel in kernels]
        dimension = len(innovations[0])
        kappa = kernels[0][1] / kernels[0][3] ** 2 - kernels[0][0] / kernels[0][2] ** 2
        weights = [alpha * (1 - alpha) ** j for j in range(horizon)]
        histories = [
            [[mp.mpf(0)] * dimension for _ in range(horizon)]
            for _ in range(len(kernels) + 1)
        ]
        increments = [[] for _ in histories]
        for innovation in innovations:
            xi = list(map(mp.mpf, innovation))
            for index, history in enumerate(histories):
                x = history[0]
                force = [mp.mpf(0)] * dimension
                for weight, past in zip(weights, history, strict=True):
                    delta = [a - b for a, b in zip(x, past, strict=True)]
                    if index == len(kernels):
                        factor = kappa
                    else:
                        ar, aa, sr, sa = kernels[index]
                        r2 = mp.fsum(a * a for a in delta)
                        factor = aa / sa**2 * mp.exp(
                            -r2 / (2 * sa**2)
                        ) - ar / sr**2 * mp.exp(-r2 / (2 * sr**2))
                    for coordinate in range(dimension):
                        force[coordinate] += weight * factor * delta[coordinate]
                noise_scale = 1 if index == len(kernels) else eps
                v = [noise_scale * xi[c] - eta * force[c] for c in range(dimension)]
                increments[index].append(v)
                new_x = [x[c] + v[c] for c in range(dimension)]
                histories[index] = [new_x] + history[:-1]
        w = increments[-1]
        residual = [
            [
                [(v[c] - eps * w[n][c]) / eps**3 for c in range(dimension)]
                for n, v in enumerate(series)
            ]
            for series in increments[:-1]
        ]
        return increments[:-1], w, residual


def _direct_two_length_values(increments, epsilon, length, digits):
    """Direct high-precision difference of squared physical displacements."""
    with mp.workdps(digits):
        eps = mp.mpf(epsilon)
        dimension = len(increments[0][0])
        result = []
        for start in range(0, len(increments[0]), 2 * length):
            kernel_values = []
            for series in increments:
                first = [
                    mp.fsum(series[n][c] for n in range(start, start + length))
                    for c in range(dimension)
                ]
                second = [
                    mp.fsum(
                        series[n][c] for n in range(start + length, start + 2 * length)
                    )
                    for c in range(dimension)
                ]
                long = mp.fsum(
                    (a + b) ** 2 for a, b in zip(first, second, strict=True)
                ) / (4 * dimension * length)
                short = mp.fsum(
                    a * a + b * b for a, b in zip(first, second, strict=True)
                ) / (4 * dimension * length)
                kernel_values.append(2 * long - short)
            result.append((kernel_values[1] - kernel_values[0]) / eps**4)
        return result


def _relative_max_error(computed, reference):
    computed = np.asarray(computed, dtype=float)
    reference = np.asarray(reference, dtype=float)
    scale = np.max(np.abs(reference))
    if scale == 0:
        return float(np.max(np.abs(computed - reference)))
    return float(np.max(np.abs(computed - reference)) / scale)


def _reference_precision_difference(computed, reference):
    with mp.workdps(110):
        computed = np.asarray(computed, dtype=object).ravel()
        reference = np.asarray(reference, dtype=object).ravel()
        error = max(abs(a - b) for a, b in zip(computed, reference, strict=True))
        scale = max(abs(a) for a in reference)
        return float(error / scale if scale else error)


def audit_split_precision():
    """48 fixed dyadic innovation vectors, H=5; not sampled from a noise law."""
    horizon, dimension, steps, length = 5, 3, 48, 4
    alpha, eta = 0.25, 0.02
    kernels = KERNEL_PAIR
    innovations = (
        np.array(
            [
                [(17 * n + 5 * c) % 13 - 6 for c in range(dimension)]
                for n in range(steps)
            ],
            dtype=float,
        )
        / 8
    )
    cells = []
    for epsilon in (1e-12, 4.4e-6, 0.007, 0.2):
        w, r = np.zeros((horizon - 1, dimension)), np.zeros((2, horizon - 1, dimension))
        wi, ri = [], []
        for xi in innovations:
            w, r = split_step(w, r, xi, alpha, eta, epsilon, kernels)
            wi.append(w[0].copy())
            ri.append(r[:, 0].copy())
        wi, ri = np.asarray(wi), np.asarray(ri).transpose(1, 0, 2)
        wb = wi.reshape(-1, length, dimension).sum(axis=1)
        rb = ri.reshape(2, -1, length, dimension).sum(axis=2)
        paired = paired_two_length_values(wb, rb, epsilon, length)
        reference80, w80, r80 = _direct_position_reference(
            innovations, alpha, eta, epsilon, horizon, kernels, 80
        )
        reference110, w110, r110 = _direct_position_reference(
            innovations, alpha, eta, epsilon, horizon, kernels, 110
        )
        paired80 = _direct_two_length_values(reference80, epsilon, length, 80)
        paired110 = _direct_two_length_values(reference110, epsilon, length, 110)
        # Deliberately round physical paths first: expose subtraction loss.
        physical = (
            np.asarray(reference110, dtype=float)
            .reshape(2, -1, length, dimension)
            .sum(axis=2)
        )
        short = np.sum(physical**2, axis=-1).reshape(2, -1, 2).mean(axis=2) / (
            2 * dimension * length
        )
        long = np.sum(
            physical.reshape(2, -1, 2, dimension).sum(axis=2) ** 2, axis=-1
        ) / (4 * dimension * length)
        rounded = ((2 * long - short)[1] - (2 * long - short)[0]) / epsilon**4
        cells.append(
            {
                "epsilon": epsilon,
                "linear_increment_relative_max_error": _relative_max_error(wi, w110),
                "residual_increment_relative_max_error": _relative_max_error(ri, r110),
                "paired_statistic_relative_max_error": _relative_max_error(
                    paired, paired110
                ),
                "rounded_physical_subtraction_relative_max_error": _relative_max_error(
                    rounded, paired110
                ),
                "reference_80_110_residual_relative_max_difference": _reference_precision_difference(
                    r80, r110
                ),
                "reference_80_110_statistic_relative_max_difference": _reference_precision_difference(
                    paired80, paired110
                ),
                "paired_normalized_mean": math.fsum(paired) / len(paired),
            }
        )
    return {
        "scope": "small deterministic algebra/precision fixture, not transport data, full-run rounding certification or a production authorization",
        "alpha": alpha,
        "eta": eta,
        "horizon": horizon,
        "dimension": dimension,
        "steps": steps,
        "elementary_block_length": length,
        "initialization": "full canonical memory of coincident points",
        "innovation_rule": "xi[n,c]=((17*n+5*c)%13-6)/8; deterministic, not Gaussian",
        "cells": cells,
    }


def _full_history_fixture():
    horizon, dimension = 600, 3
    j = np.arange(1, horizon, dtype=float)[:, None]
    c = np.arange(dimension)[None, :]
    w = np.sqrt(j) * ((j * (c + 1) + 2 * c) % 17 - 8) / 8
    r = np.stack((j * w / 64, -j * w / 32))
    xi = np.array([0.5, -0.25, 0.125])
    alpha = 0.01
    eta = 0.5 * alpha / ((1 - alpha) * (1 + 35 / 9))
    return w, r, xi, alpha, eta, KERNEL_PAIR


def audit_full_history_step():
    """One arbitrary full H=600 state, not a stationary/production trajectory."""
    w, r, xi, alpha, eta, kernels = _full_history_fixture()

    def reference(epsilon, digits):
        with mp.workdps(digits):
            a, e, eps = map(mp.mpf, (alpha, eta, epsilon))
            kappa = mp.mpf(26) / 9
            gamma = [a * (1 - a) ** j for j in range(1, len(w) + 1)]
            wv = [
                mp.mpf(xi[c])
                - e * kappa * mp.fsum(gamma[j] * mp.mpf(w[j, c]) for j in range(len(w)))
                for c in range(3)
            ]
            rv = []
            for k, kernel in enumerate(kernels):
                ar, aa, sr, sa = map(mp.mpf, kernel)
                terms = [[] for _ in range(3)]
                for j in range(len(w)):
                    lag = [
                        eps * mp.mpf(w[j, c]) + eps**3 * mp.mpf(r[k, j, c])
                        for c in range(3)
                    ]
                    r2 = mp.fsum(x * x for x in lag)
                    factor = aa / sa**2 * mp.exp(
                        -r2 / (2 * sa**2)
                    ) - ar / sr**2 * mp.exp(-r2 / (2 * sr**2))
                    for c in range(3):
                        terms[c].append(gamma[j] * factor * lag[c])
                physical = [
                    eps * mp.mpf(xi[c]) - e * mp.fsum(terms[c]) for c in range(3)
                ]
                rv.append([(physical[c] - eps * wv[c]) / eps**3 for c in range(3)])
            return wv, rv

    results = []
    for epsilon in (1e-12, 4.4e-6, 0.007):
        nw, nr = split_step(w, r, xi, alpha, eta, epsilon, kernels)
        _, r80 = reference(epsilon, 80)
        w110, r110 = reference(epsilon, 110)
        results.append(
            {
                "epsilon": epsilon,
                "linear_increment_relative_max_error": _relative_max_error(nw[0], w110),
                "residual_increment_relative_max_error": _relative_max_error(
                    nr[:, 0], r110
                ),
                "reference_80_110_residual_relative_max_difference": _reference_precision_difference(
                    r80, r110
                ),
            }
        )
    return {
        "scope": "one arbitrary H=600 lag state; no time evolution, sampling or stationary-law claim",
        "cells": results,
    }


def benchmark_split_step(repetitions=500, repeats=5):
    """Microbenchmark repeated evaluations of ONE unchanged state, not a path.

    Includes validation/allocations and excludes RNG, sampling, accumulation
    and output. Extrapolation is neither a production forecast nor a bound.
    """
    _positive_integer(repetitions, "repetitions")
    _positive_integer(repeats, "repeats")
    w, r, xi, alpha, eta, kernels = _full_history_fixture()

    def call():
        return split_step(w, r, xi, alpha, eta, 4.4e-6, kernels)

    call()
    seconds = (
        np.array(timeit.repeat(call, number=repetitions, repeat=repeats)) / repetitions
    )
    paired_steps = 5 * 2 * 1000 * 200_000
    return {
        "scope": "unoptimized fixed-state Python/SciPy microbenchmark; not target execution or a production runtime guarantee",
        "python": platform.python_version(),
        "platform": platform.system(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "horizon": 600,
        "dimension": 3,
        "kernels": 2,
        "repetitions_per_repeat": repetitions,
        "repeats": repeats,
        "seconds_per_paired_step": seconds.tolist(),
        "median_seconds_per_paired_step": float(np.median(seconds)),
        "previously_discussed_paired_step_count": paired_steps,
        "naive_serial_extrapolation_hours_excluding_rng_statistics_io": float(
            np.median(seconds) * paired_steps / 3600
        ),
    }


if __name__ == "__main__":
    print(
        json.dumps(
            {
                "short_history": audit_split_precision(),
                "full_history_step": audit_full_history_step(),
            },
            indent=2,
        )
    )
