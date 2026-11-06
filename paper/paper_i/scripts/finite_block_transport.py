"""Finite-block variance bounds for the leading paired transport coefficient.

No target trajectories, Gaussian approximation to the block statistic,
or independence of adjacent blocks/coordinate products is used. These
floating-point bounds do NOT cover the finite-noise nonlinear remainder.
"""

from __future__ import annotations

import json

import numpy as np

from paired_transport import (
    _positive_integer,
    cubic_force_covariances,
    exponential_cubic_tail_bound,
    exponential_two_length_bias_bounds,
)
from weak_nonlinearity import (
    covariance_response,
    exponential_weights,
    lag_matrix,
    stationary_msd_response,
    transport_response,
)


def filtered_block_variance_bounds(
    forcing_covariances, impulse, length, omitted_impulse_l1, forcing_absolute_sum_bound
):
    """Bound a scalar block variance after truncating a stable signed filter.

    Covariances must cover the entire finite convolution. Their absolute
    infinite sum and the filter's omitted l1 norm are explicit inputs;
    neither missing tail is silently set to zero.
    """
    _positive_integer(length, "length")
    forcing = np.asarray(forcing_covariances, dtype=float)
    impulse = np.asarray(impulse, dtype=float)
    if (
        forcing.ndim != 1
        or impulse.ndim != 1
        or len(impulse) < 1
        or len(forcing) < length + len(impulse) - 1
        or not np.all(np.isfinite(forcing))
        or not np.all(np.isfinite(impulse))
        or not np.isfinite(omitted_impulse_l1)
        or omitted_impulse_l1 < 0
        or not np.isfinite(forcing_absolute_sum_bound)
        or forcing_absolute_sum_bound < 0
    ):
        raise ValueError(
            "require finite coefficients, enough covariances, and explicit nonnegative tail bounds"
        )
    if forcing_absolute_sum_bound < forcing[0] + 2 * np.abs(forcing[1:]).sum() - 1e-12:
        raise ValueError(
            "absolute covariance bound is smaller than the supplied partial sum"
        )
    block_filter = np.convolve(np.ones(length), impulse)
    products = np.correlate(block_filter, block_filter, mode="full")[
        len(block_filter) - 1 :
    ]
    variance = forcing[0] * products[0] + 2 * (
        forcing[1 : len(products)] @ products[1:]
    )
    if not np.isfinite(variance) or variance < 0:
        raise ValueError("filtered variance is negative or unresolved")
    remainder = omitted_impulse_l1 * np.sqrt(length * forcing_absolute_sum_bound)
    return {
        "truncated_variance": float(variance),
        "standard_deviation_error_bound": float(remainder),
        "variance_lower": float(max(0.0, np.sqrt(variance) - remainder) ** 2),
        "variance_upper": float((np.sqrt(variance) + remainder) ** 2),
    }


def stationary_average_variance_bound(
    second_moment_bound, mean, remote_coupling_sum, near_lags, blocks, seeds
):
    """Covariance bound for a stationary superblock average, including overlap.

    remote_coupling_sum bounds sum_{k>near_lags} ||Q_k-Q_k^*||_2,
    where Q_k^* has an independently replaced past through the end of Q_0.
    No normal approximation or coordinate-independence factor is used.
    """
    for name, value in (("near_lags", near_lags), ("blocks", blocks), ("seeds", seeds)):
        _positive_integer(value, name)
    if (
        not np.all(np.isfinite([second_moment_bound, mean, remote_coupling_sum]))
        or second_moment_bound < mean**2
        or remote_coupling_sum < 0
    ):
        raise ValueError("invalid second moment, mean, or coupling bound")
    variance = second_moment_bound - mean**2
    count = min(near_lags, blocks - 1)
    inflation = 1 + 2 * count - count * (count + 1) / blocks
    remote = (
        0.0 if blocks <= near_lags + 1 else 2 * np.sqrt(variance) * remote_coupling_sum
    )
    return float((inflation * variance + remote) / (seeds * blocks))


def finite_block_reference_bound(
    alpha,
    horizon,
    untruncated_gain,
    dimension,
    length,
    filter_cutoff,
    superblocks,
    seeds,
):
    """Canonical stationary reference, at specified finite L and sample counts."""
    weights = exponential_weights(alpha, horizon)
    for name, value in (
        ("dimension", dimension),
        ("length", length),
        ("filter_cutoff", filter_cutoff),
        ("superblocks", superblocks),
        ("seeds", seeds),
    ):
        _positive_integer(value, name)
    if not np.isfinite(untruncated_gain) or untruncated_gain < 0:
        raise ValueError("untruncated gain must be finite and nonnegative")
    q = 1 - alpha
    b = q * untruncated_gain
    root = q + b
    if not 0 < root < 1:
        raise ValueError("absolute impulse envelope must be summable")
    maximum_lag = filter_cutoff + length - 1
    k = horizon - 1
    if maximum_lag < k:
        raise ValueError("covariance cutoff must reach H-1")
    mass = -np.expm1(horizon * np.log1p(-alpha))
    gain = mass * untruncated_gain
    covariance, _, perturbation = covariance_response(weights, gain, dimension)
    first, third = cubic_force_covariances(
        weights, gain, covariance, dimension, maximum_lag
    )
    ages = np.arange(1, horizon)
    tail_weights = weights[1:]
    variances = np.diag(covariance)
    age_sum = -np.expm1(ages * np.log(root)) / (1 - root)
    envelope = b * (1 - q * root) / (1 - root**2)
    linear_force = (dimension + 2) * tail_weights * variances
    first_tail = (
        2
        * envelope
        * root ** (maximum_lag + 1 - k)
        / (1 - root)
        * (linear_force @ (age_sum * root ** (k - ages)))
        * (linear_force @ age_sum)
    )
    third_tail = exponential_cubic_tail_bound(
        alpha, untruncated_gain, horizon, dimension, maximum_lag
    )
    absolute_sums = [
        first[0] + 2 * np.abs(first[1:]).sum() + first_tail,
        third[0] + 2 * np.abs(third[1:]).sum() + third_tail,
    ]
    matrix = lag_matrix(weights, gain)
    state = np.ones(k)
    impulse = np.empty(filter_cutoff + 1)
    for time in range(filter_cutoff + 1):
        impulse[time] = state[0]
        following = np.full(k, matrix[0] @ state)
        following[1:] += state[:-1]
        state = following
    impulse_tail = b * root**filter_cutoff / (1 - root)
    first_block, third_block = [
        filtered_block_variance_bounds(series, impulse, length, impulse_tail, total)
        for series, total in zip((first, third), absolute_sums, strict=True)
    ]
    msd, response = stationary_msd_response(
        weights, gain, np.array([length, 2 * length]), dimension
    )
    mean = (response[1] - response[0]) / (2 * dimension * length)
    _, long_time_mean = transport_response(weights, gain, perturbation)
    if long_time_mean == 0:
        raise ValueError("relative precision requires a nonzero long-time coefficient")
    gaussian_fourth_norm = (dimension * (dimension + 2)) ** 0.25
    w4 = gaussian_fourth_norm * np.sqrt(msd[0] / dimension)
    z4 = gaussian_fourth_norm * np.sqrt(first_block["variance_upper"]) + np.sqrt(
        dimension
    ) * 3**1.5 * np.sqrt(third_block["variance_upper"])
    second_moment_bound = (3 * w4 * z4 / (dimension * length)) ** 2

    # Independently replace all innovations through the end of Q_0.
    # Nearby superblocks need no decay estimate: Cauchy--Schwarz covers them.
    near_lags = (k + 2 * length - 1) // (2 * length)
    initial_age = 2 * length * near_lags - k
    power = root**length
    step = power**2
    block_age_sum = -np.expm1(length * np.log(root)) / (1 - root)
    weighted_block_age_sum = np.arange(length) @ root ** np.arange(length)
    innovation_difference = b * np.sqrt(2 / (1 - root**2))
    w_coupling_sum = (
        gaussian_fourth_norm
        * innovation_difference
        * block_age_sum
        * (1 + power)
        * root ** (2 * length * near_lags)
        / (1 - step)
    )
    gaussian_twelfth_norm_cubed = np.prod(dimension + 2.0 * np.arange(6)) ** 0.25
    old_force = 2 * gaussian_twelfth_norm_cubed * (tail_weights @ variances**1.5)
    decaying_force = (
        3
        * gaussian_twelfth_norm_cubed
        * innovation_difference
        * (tail_weights @ (variances * age_sum * root ** (k - ages)))
    )
    c0 = decaying_force + b * old_force / (1 - root)
    c1 = b * decaying_force / root
    u = (1 + power) * (c0 * block_age_sum + c1 * weighted_block_age_sum)
    u += power * c1 * length * block_age_sum
    v = (1 + power) * c1 * block_age_sum
    z_coupling_sum = root**initial_age * (
        (u + v * initial_age) / (1 - step) + 2 * length * v * step / (1 - step) ** 2
    )
    remote_q_sum = (
        3 * (z4 * w_coupling_sum + w4 * z_coupling_sum) / (2 * dimension * length)
    )
    variance_bound = stationary_average_variance_bound(
        second_moment_bound, mean, remote_q_sum, near_lags, superblocks, seeds
    )
    relative_sd = np.sqrt(variance_bound) / abs(long_time_mean)
    return {
        "scope": "finite stationary sample bound for the leading Gaussian-polynomial coefficient only; not finite-noise nonlinear power",
        "alpha": alpha,
        "horizon": horizon,
        "dimension": dimension,
        "untruncated_gain": untruncated_gain,
        "elementary_block_length": length,
        "superblocks_per_seed": superblocks,
        "seeds": seeds,
        "implied_steps_per_seed": 2 * length * superblocks,
        "filter_cutoff": filter_cutoff,
        "forcing_covariance_maximum_lag": maximum_lag,
        "first_chaos_forcing_absolute_tail_bound": float(first_tail),
        "third_chaos_forcing_absolute_tail_bound": float(third_tail),
        "omitted_filter_l1_bound": float(impulse_tail),
        "first_chaos_block_variance": first_block,
        "third_chaos_block_variance": third_block,
        "linear_block_variance": float(msd[0] / dimension),
        "finite_two_length_mean_per_beta": float(mean),
        "long_time_mean_per_beta": float(long_time_mean),
        "superblock_second_moment_bound": float(second_moment_bound),
        "nearby_covariances_bounded_without_decay": near_lags,
        "remote_superblock_coupling_sum_bound": float(remote_q_sum),
        "sample_mean_variance_bound": variance_bound,
        "relative_sampling_sd_bound_against_long_time_coefficient": float(relative_sd),
        "relative_chebyshev_95_radius_about_finite_mean": float(
            relative_sd / np.sqrt(0.05)
        ),
        "coefficient_bias_bounds": exponential_two_length_bias_bounds(
            alpha, untruncated_gain, horizon, dimension, length, covariance
        ),
        "finite_noise_remainder_and_burn_in": "not included; no panel authorization",
    }


def audit_finite_block_reference():
    alpha, horizon, dimension = 0.01, 600, 3
    eta = 0.5 * alpha / ((1 - alpha) * (1 + 35 / 9))
    return finite_block_reference_bound(
        alpha, horizon, eta * 26 / 9, dimension, 1000, 2400, 200_000, 5
    )


if __name__ == "__main__":
    print(json.dumps(audit_finite_block_reference(), indent=2))
