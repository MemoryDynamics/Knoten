"""Finite-window readouts at a fixed reference separation, not a dynamics.

No stationarity, independence, significance or physical force is inferred.
The empirical product uses all pairs of observations in the chosen window.
"""

from __future__ import annotations

from dataclasses import asdict
from numbers import Integral

import numpy as np

from .kernels import (
    ScalarReadoutKernel,
    two_scale_local_curvature,
    validate_scalar_readout_kernel,
)


def gaussian_gradient_remainder(
    displacement: np.ndarray, kernel: ScalarReadoutKernel
) -> np.ndarray:
    """Evaluate grad K(z) - kappa*z using expm1, including at tiny z."""
    validate_scalar_readout_kernel(kernel)
    z = np.asarray(displacement, dtype=float)
    if z.ndim < 1 or z.shape[-1] < 1 or not np.isfinite(z).all():
        raise ValueError("displacement must contain finite vectors")
    norm2 = np.sum(z * z, axis=-1)
    factor = (
        -kernel.amplitude_rep
        / kernel.sigma_rep**2
        * np.expm1(-norm2 / (2 * kernel.sigma_rep**2))
    )
    factor += (
        kernel.amplitude_att
        / kernel.sigma_att**2
        * np.expm1(-norm2 / (2 * kernel.sigma_att**2))
    )
    result = z * factor[..., None]
    if not np.isfinite(result).all():
        raise ValueError("non-finite kernel remainder")
    return result


def _probabilities(weights):
    values = np.asarray(weights, dtype=float)
    if (
        values.ndim != 1
        or len(values) < 1
        or not np.isfinite(values).all()
        or np.any(values < 0)
        or not np.isfinite(values.sum())
        or values.sum() <= 0
    ):
        raise ValueError("weights must be finite, non-negative and have positive sum")
    return values / values.sum()


def _lag_terms(target, source, separation, weights, start, stop, kernel):
    source_mean = np.zeros(target.shape[1])
    nonlinear = np.zeros(target.shape[1])
    third_moment = 0.0
    for lag, weight in enumerate(weights):
        past = source[start - lag : stop - lag]
        z = separation + target[start:stop] - past
        source_mean += weight * np.mean(past, axis=0)
        nonlinear += weight * np.mean(gaussian_gradient_remainder(z, kernel), axis=0)
        third_moment += weight * np.mean(np.linalg.norm(z, axis=1) ** 3)
    return source_mean, nonlinear, third_moment


def _product_terms(
    target, source, source_probabilities, separation, kernel, block_size
):
    remainder = np.zeros(target.shape[1])
    third_moment = 0.0
    for left in range(0, len(target), block_size):
        block = target[left : left + block_size]
        z = separation + block[:, None, :] - source[None, :, :]
        values = gaussian_gradient_remainder(z, kernel)
        remainder += np.sum(values * source_probabilities[None, :, None], axis=(0, 1))
        third_moment += float(
            np.sum(np.linalg.norm(z, axis=2) ** 3 * source_probabilities)
        )
    return remainder / len(target), third_moment / len(target)


def analyze_frozen_pair_window(
    first_inner,
    second_inner,
    separation,
    first_weights,
    second_weights,
    *,
    start: int,
    stop: int,
    kernel: ScalarReadoutKernel,
    product_block_size: int = 256,
) -> dict:
    """Separate linear endpoints from nonlinear empirical-product differences.

    Input rows must be consecutive, synchronized updates. ``separation`` is
    C_A-C_B, fixed for this evaluation. Moving-center errors are NOT included.
    ``kernel`` must already include any effective write/read convolution.
    This costs O(T*(H_A+H_B)+T**2); blocking bounds memory, not operation count.
    """
    first = np.asarray(first_inner, dtype=float)
    second = np.asarray(second_inner, dtype=float)
    if (
        first.ndim != 2
        or second.shape != first.shape
        or min(first.shape) < 1
        or not np.isfinite(first).all()
        or not np.isfinite(second).all()
    ):
        raise ValueError(
            "inner paths must be finite arrays of the same (updates, dim) shape"
        )
    r = np.asarray(separation, dtype=float)
    if r.shape != (first.shape[1],) or not np.isfinite(r).all():
        raise ValueError("separation must be a finite vector matching dim")
    pa, pb = _probabilities(first_weights), _probabilities(second_weights)
    if any(
        isinstance(value, bool) or not isinstance(value, Integral)
        for value in (start, stop, product_block_size)
    ):
        raise ValueError("window and block size must be integers")
    if not max(len(pa), len(pb)) - 1 <= start < stop <= len(first):
        raise ValueError("window must include complete past lag support")
    if product_block_size < 1:
        raise ValueError("product_block_size must be positive")
    curvature = two_scale_local_curvature(**asdict(kernel))
    coefficient = (
        abs(kernel.amplitude_rep) / kernel.sigma_rep**4
        + abs(kernel.amplitude_att) / kernel.sigma_att**4
    ) / 2
    if not np.isfinite([curvature, coefficient]).all():
        raise ValueError("kernel coefficients must be finite")

    mean_a, mean_b = (
        np.mean(first[start:stop], axis=0),
        np.mean(second[start:stop], axis=0),
    )
    lag_b, rem_a, third_a = _lag_terms(first, second, r, pb, start, stop, kernel)
    lag_a, rem_b, third_b = _lag_terms(second, first, -r, pa, start, stop, kernel)
    count = stop - start
    uniform = np.ones(count) / count
    product_remainder, product_third_moment = _product_terms(
        first[start:stop],
        second[start:stop],
        uniform,
        r,
        kernel,
        product_block_size,
    )
    # Each past source observation has its exact window/age multiplicity.
    qa, qb = np.convolve(uniform, pa[::-1]), np.convolve(uniform, pb[::-1])
    past_product_a, past_third_a = _product_terms(
        first[start:stop],
        second[start - len(pb) + 1 : stop],
        qb,
        r,
        kernel,
        product_block_size,
    )
    past_product_b, past_third_b = _product_terms(
        second[start:stop],
        first[start - len(pa) + 1 : stop],
        qa,
        -r,
        kernel,
        product_block_size,
    )

    linear_means = curvature * np.stack((r + mean_a - lag_b, -r + mean_b - lag_a))
    linear_product = curvature * (r + mean_a - mean_b)
    linear_excess = curvature * np.stack((mean_b - lag_b, mean_a - lag_a))
    nonlinear_excess = np.stack((rem_a - product_remainder, rem_b + product_remainder))
    result = {
        "window": [int(start), int(stop)],
        "curvature": curvature,
        "cubic_coefficient": coefficient,
        "mean_gradients": linear_means + np.stack((rem_a, rem_b)),
        "product_gradient": linear_product + product_remainder,
        "linear_means": linear_means,
        "linear_product": linear_product,
        "linear_excess": linear_excess,
        "nonlinear_excess": nonlinear_excess,
        "nonlinear_excess_bound": coefficient
        * (np.array([third_a, third_b]) + product_third_moment),
        "lag_matched_product_gradients": linear_means
        + np.stack((past_product_a, past_product_b)),
        "nonlinear_marginal_shift": np.stack(
            (
                past_product_a - product_remainder,
                past_product_b + product_remainder,
            )
        ),
        "lag_product_contrast": np.stack(
            (rem_a - past_product_a, rem_b - past_product_b)
        ),
        "lag_product_contrast_bound": coefficient
        * np.array(
            (
                third_a + past_third_a,
                third_b + past_third_b,
            )
        ),
    }
    if any(not np.isfinite(value).all() for value in map(np.asarray, result.values())):
        raise ValueError("non-finite diagnostic; no interpretable result")
    return result
