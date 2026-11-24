"""Deterministic audit of PR8 review 5606957081; no target trajectories.

The reviewed cell is reproduced, not selected here. Gaussian-reference
precision is not a nonlinear, paired-kernel power calculation. All numbers
are floating-point diagnostics, not interval certificates.
"""

from __future__ import annotations

import json

import numpy as np

from weak_nonlinearity import (
    covariance_response,
    exponential_weights,
    stationary_msd_response,
    transport_response,
    untruncated_transport_response,
)


def gaussian_block_floor(
    msd_at_block_multiples,
    blocks_per_seed: int,
    seeds: int,
    dimension: int,
    omitted_covariance_squares: float | None = None,
):
    """Relative SE bounds for the mean squared stationary Gaussian block.

    Input is per-coordinate MSD at lags 0,L,...,(K+1)L. The supplied tail
    bounds sum_{m>K} Cov(Y_0,Y_m)^2, not squared correlations. No independence
    of adjacent blocks is assumed. Seeds and Gaussian coordinates are
    independent. Paired differences between kernels are not covered.
    """
    for value in (blocks_per_seed, seeds, dimension):
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, np.integer))
            or value < 1
        ):
            raise ValueError(
                "block, seed and dimension counts must be positive integers"
            )
    msd = np.asarray(msd_at_block_multiples, dtype=float)
    if (
        msd.ndim != 1
        or len(msd) < 3
        or not np.all(np.isfinite(msd))
        or msd[0] != 0
        or msd[1] <= 0
    ):
        raise ValueError("require finite MSD at 0,L,... with positive block variance")
    if omitted_covariance_squares is None:
        if len(msd) - 2 < blocks_per_seed - 1:
            raise ValueError(
                "incomplete block covariance requires an explicit tail bound"
            )
        omitted_covariance_squares = 0.0
    if not np.isfinite(omitted_covariance_squares) or omitted_covariance_squares < 0:
        raise ValueError("tail bound must be finite and nonnegative")
    covariances = 0.5 * (msd[2:] + msd[:-2] - 2 * msd[1:-1])
    count = min(len(covariances), blocks_per_seed - 1)
    ages = np.arange(1, count + 1)
    inflation = 1 + 2 * np.sum(
        (1 - ages / blocks_per_seed) * (covariances[:count] / msd[1]) ** 2
    )
    upper = inflation
    if len(covariances) < blocks_per_seed - 1:
        upper += 2 * omitted_covariance_squares / msd[1] ** 2
    base_variance = 2 / (dimension * seeds * blocks_per_seed)
    return {
        "variance_inflation_lower": float(inflation),
        "variance_inflation_upper": float(upper),
        "relative_se_lower": float(np.sqrt(base_variance * inflation)),
        "relative_se_upper": float(np.sqrt(base_variance * upper)),
        "first_block_correlation": float(covariances[0] / msd[1]),
    }


def audit_review_cell():
    alpha, horizon, dimension, epsilon = 0.01, 600, 3, 0.007
    block_length, steps, seeds, covariance_blocks = 100, 400_000_000, 5, 50
    q = 1 - alpha
    eta = 0.5 * alpha / (q * (1 + 35 / 9))
    mass = 1 - q**horizon
    weights = exponential_weights(alpha, horizon)
    curvature = 26 / 9
    gain = eta * mass * curvature
    covariance, _, perturbation = covariance_response(weights, gain, dimension)
    diffusion, derivative = transport_response(weights, gain, perturbation)
    lags = block_length * np.arange(covariance_blocks + 2)
    msd, response = stationary_msd_response(weights, gain, lags, dimension)
    msd /= dimension
    response /= dimension
    block_diffusion = msd[1] / (2 * block_length)

    # Absolute linear impulse envelope bounds the omitted block-covariance tail.
    b = q * abs(eta * curvature)
    root = q + b
    if not 0 < root < 1:
        raise ValueError("linear absolute impulse envelope is not summable")
    covariance_envelope = b * (1 - q * root) / (1 - root**2)
    block_envelope = covariance_envelope * ((1 - root**block_length) / (1 - root)) ** 2
    tail = block_envelope**2 * root ** (2 * covariance_blocks * block_length)
    tail /= 1 - root ** (2 * block_length)
    floor = gaussian_block_floor(msd, steps // block_length, seeds, dimension, tail)

    kernels = []
    for repulsive, attractive in ((0.0, 26.0), (1.0, 35.0)):
        cubic = repulsive / 2 - attractive / 162
        fifth_bound = repulsive / 8 + attractive / (8 * 3**6)
        beta = eta * mass * cubic
        infinite = untruncated_transport_response(
            alpha, eta * curvature, eta * cubic, dimension
        )
        finite_correction = beta * derivative
        block_correction = beta * response[1] / (2 * block_length)
        variances = np.diag(covariance)
        force_norm_ratio = (
            epsilon**2
            * (dimension + 3)
            * fifth_bound
            / abs(cubic)
            * np.dot(weights[1:], variances**2.5)
            / np.dot(weights[1:], variances**1.5)
        )
        kernels.append(
            {
                "amplitude_rep": repulsive,
                "amplitude_att": attractive,
                "theta": eta * (repulsive + attractive / 9) * q / alpha,
                "infinite_D2": infinite[0],
                "infinite_D4": infinite[1],
                "infinite_relative_correction": epsilon**2 * infinite[1] / infinite[0],
                "finite_D4": finite_correction,
                "finite_relative_correction": epsilon**2
                * finite_correction
                / diffusion,
                "block_D4": block_correction,
                "block_relative_correction": epsilon**2
                * block_correction
                / block_diffusion,
                "gaussian_weighted_force_norm_ratio_not_transport_error": float(
                    force_norm_ratio
                ),
            }
        )
    contrast = kernels[1]["block_D4"] - kernels[0]["block_D4"]
    relative_contrast = epsilon**2 * contrast / block_diffusion
    return {
        "review_url": "https://github.com/MemoryDynamics/Knoten/pull/8#pullrequestreview-5606957081",
        "scope": "fixed reviewed cell; stationary linear Gaussian reference and formal quartic response; no trajectories",
        "alpha": alpha,
        "horizon": horizon,
        "eta": eta,
        "epsilon": epsilon,
        "dimension": dimension,
        "block_length": block_length,
        "steps_per_seed": steps,
        "seeds": seeds,
        "finite_mean_age": float(mass * np.dot(np.arange(horizon), weights)),
        "finite_D2": diffusion,
        "block_D2": block_diffusion,
        "relative_linear_block_bias": block_diffusion / diffusion - 1,
        "block_to_long_time_quartic_ratio": response[1]
        / (2 * block_length * derivative),
        "gaussian_reference_floor": floor,
        "omitted_block_covariance_squares_bound": tail,
        "block_contrast_relative_to_linear_block_mean": relative_contrast,
        "independent_kernel_gaussian_sizing_z": abs(relative_contrast)
        / (np.sqrt(2) * floor["relative_se_upper"]),
        "paired_kernel_precision": "not calculated; do not substitute the independent-kernel floor",
        "kernels": kernels,
    }


if __name__ == "__main__":
    print(json.dumps(audit_review_cell(), indent=2))
