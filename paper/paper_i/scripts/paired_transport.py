"""Target-free paired transport reference, not a finite-run power guarantee.

The cubic forcing's third Gaussian chaos contributes to paired variance
even though it is orthogonal to the linear process in the mean response.
All numerical evaluations are floating-point diagnostics, not certificates.
"""

from __future__ import annotations

import json

import numpy as np

from weak_nonlinearity import (
    covariance_response,
    exponential_weights,
    lag_matrix,
    stationary_msd_response,
    transport_response,
)


def _positive_integer(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _checked_covariance(weights, gain, covariance):
    matrix = lag_matrix(weights, gain)
    covariance = np.asarray(covariance, dtype=float)
    if (
        covariance.shape != matrix.shape
        or not np.all(np.isfinite(covariance))
        or not np.allclose(covariance, covariance.T, rtol=1e-11, atol=1e-12)
    ):
        raise ValueError("require a finite symmetric lag covariance")
    try:
        np.linalg.cholesky(covariance)
    except np.linalg.LinAlgError as error:
        raise ValueError("lag covariance must be positive definite") from error
    residual = covariance - matrix @ covariance @ matrix.T - 1
    if np.max(np.abs(residual)) > 1e-9 * max(1.0, np.max(np.abs(covariance))):
        raise ValueError("covariance does not solve the unit-noise Lyapunov equation")
    return matrix, covariance


def cubic_force_covariance_sum(weights, gain, covariance, dimension, maximum_lag):
    """Partial zero-frequency variance of the Wick-ordered cubic forcing.

    Returns 2(d+2) sum_{|t|<=T,j,k} w_j w_k C_jk(t)^3 per coordinate.
    Signed covariances are retained. A finite sum is NOT a lower bound;
    the caller must supply an absolute omitted-tail bound separately.
    """
    _positive_integer(dimension, "dimension")
    _positive_integer(maximum_lag, "maximum_lag")
    matrix, cross = _checked_covariance(weights, gain, covariance)
    tail = np.asarray(weights, dtype=float)[1:]
    pair_weights = np.outer(tail, tail)
    total = np.sum(pair_weights * cross * cross * cross)
    for _ in range(maximum_lag):
        # A is a common first row plus a shift, avoiding a dense matrix product.
        first_row = matrix[0] @ cross
        following = np.broadcast_to(first_row, cross.shape).copy()
        following[1:] += cross[:-1]
        cross = following
        total += 2 * np.sum(pair_weights * cross * cross * cross)
    return float(2 * (dimension + 2) * total)


def exponential_cubic_tail_bound(
    alpha, untruncated_gain, horizon, dimension, maximum_lag
):
    """Bound the omitted cubic covariance sum for canonical finite memory.

    Requires g_H=(1-q**H)*untruncated_gain and normalized exponential w.
    This bounds only the numerical covariance-series tail, NOT finite block
    length, finite noise, burn-in, or the finite-H to infinite-H difference.
    """
    weights = exponential_weights(alpha, horizon)
    _positive_integer(dimension, "dimension")
    _positive_integer(maximum_lag, "maximum_lag")
    if not np.isfinite(untruncated_gain) or untruncated_gain < 0:
        raise ValueError("untruncated gain must be finite and nonnegative")
    if maximum_lag < horizon - 1:
        raise ValueError("tail bound requires maximum_lag >= H-1")
    q = 1 - alpha
    b = q * untruncated_gain
    root = q + b
    if not 0 < root < 1:
        raise ValueError("absolute impulse envelope must be summable")
    if b == 0:
        return 0.0
    envelope = b * (1 - q * root) / (1 - root**2)
    ages = np.arange(1, horizon)
    age_sum = -np.expm1(ages * np.log(root)) / (1 - root)
    left = weights[1:] @ (age_sum**3 * root ** (3 * (horizon - 1 - ages)))
    right = weights[1:] @ age_sum**3
    result = (
        4
        * (dimension + 2)
        * envelope**3
        * root ** (3 * (maximum_lag + 1 - (horizon - 1)))
        * left
        * right
        / (1 - root**3)
    )
    if not np.isfinite(result):
        raise ValueError("cubic covariance tail bound overflows")
    return float(result)


def exponential_two_length_bias_bounds(
    alpha, untruncated_gain, horizon, dimension, length, covariance
):
    """Absolute finite-lag bias bounds for D2 and the D4/beta response.

    Uses a positive impulse envelope and its gain derivative. These are
    coefficient-level bounds, not an error bound at nonzero noise.
    """
    weights = exponential_weights(alpha, horizon)
    _positive_integer(dimension, "dimension")
    _positive_integer(length, "length")
    if not np.isfinite(untruncated_gain) or untruncated_gain < 0:
        raise ValueError("untruncated gain must be finite and nonnegative")
    q = 1 - alpha
    mass = -np.expm1(horizon * np.log1p(-alpha))
    _, covariance = _checked_covariance(weights, mass * untruncated_gain, covariance)
    b = q * untruncated_gain
    root = q + b
    if not 0 < root < 1:
        raise ValueError("absolute impulse envelope must be summable")
    envelope = b * (1 - q * root) / (1 - root**2)
    envelope_root_derivative = (1 - q * root - b * q) / (1 - root**2)
    envelope_root_derivative += 2 * root * b * (1 - q * root) / (1 - root**2) ** 2
    power = root**length
    one_minus_power = -np.expm1(length * np.log(root))
    tail_factor = power * one_minus_power / (length * (1 - root) ** 2)
    tail_factor_derivative = root ** (length - 1) * (1 - 2 * power) / (
        1 - root
    ) ** 2 + 2 * power * one_minus_power / (length * (1 - root) ** 3)
    response_scale = (dimension + 2) * np.max(np.diag(covariance)) / mass
    return {
        "linear_absolute_bias_bound": float(envelope * tail_factor),
        "quartic_per_beta_absolute_bias_bound": float(
            response_scale
            * q
            * (
                envelope_root_derivative * tail_factor
                + envelope * tail_factor_derivative
            )
        ),
    }


def paired_long_block_reference(weights, gain, covariance, dimension, cubic_spectrum):
    """Leading paired variance in the iterated weak-noise/long-block limit.

    Z is the response per unit beta=eta*M_H*lambda. Coordinates become
    independent in the joint Gaussian block limit, not at finite block
    length. Returned relative variance factors multiply 1/(d*S*M), where
    M is the number of elementary blocks; the two-length factor assumes
    nested adjacent blocks with even M. No finite-L accuracy is asserted.
    """
    _positive_integer(dimension, "dimension")
    _, covariance = _checked_covariance(weights, gain, covariance)
    if not np.isfinite(cubic_spectrum) or cubic_spectrum < 0:
        raise ValueError("cubic spectrum must be finite and nonnegative")
    tail = np.asarray(weights, dtype=float)[1:]
    ages = np.arange(1, len(weights))
    age_variance = float((ages * tail) @ np.diag(covariance))
    transfer = 1 / (1 + gain * (ages @ tail))
    linear_variance = transfer**2
    cross_variance = -(dimension + 2) * age_variance * transfer**3
    first_chaos_variance = (dimension + 2) ** 2 * age_variance**2 * transfer**4
    third_chaos_variance = transfer**2 * cubic_spectrum
    if cross_variance == 0:
        raise ValueError("relative paired precision requires a nonzero mean response")
    extra = linear_variance * third_chaos_variance / cross_variance**2
    return {
        "linear_zero_frequency_variance": float(linear_variance),
        "linear_cubic_zero_frequency_covariance": float(cross_variance),
        "cubic_first_chaos_zero_frequency_variance": float(first_chaos_variance),
        "cubic_third_chaos_zero_frequency_variance": float(third_chaos_variance),
        "extra_relative_variance_from_third_chaos": float(extra),
        "raw_relative_variance_times_d_S_M": float(2 + extra),
        "two_length_relative_variance_times_d_S_M": float(5 * (2 + extra)),
    }


def audit_paired_reference():
    """Fixed review cell, two declared lag diagnostics, no sampling or scan."""
    alpha, horizon, dimension = 0.01, 600, 3
    maximum_lag = 2400
    q = 1 - alpha
    eta = 0.5 * alpha / (q * (1 + 35 / 9))
    mass = 1 - q**horizon
    bare_gain = eta * 26 / 9
    gain = mass * bare_gain
    weights = exponential_weights(alpha, horizon)
    covariance, _, perturbation = covariance_response(weights, gain, dimension)
    diffusion, derivative = transport_response(weights, gain, perturbation)
    # L=100 is the reviewed design; L=1000 is a declared decade-longer
    # analytic diagnostic, not a selected production block length.
    lengths = np.array([100, 1000])
    msd, response = stationary_msd_response(
        weights, gain, np.concatenate((lengths, 2 * lengths)), dimension
    )
    rows = []
    for index, length in enumerate(lengths):
        raw_linear = msd[index] / (2 * dimension * length)
        raw_response = response[index] / (2 * dimension * length)
        corrected_linear = (msd[index + 2] - msd[index]) / (2 * dimension * length)
        corrected_response = (response[index + 2] - response[index]) / (
            2 * dimension * length
        )
        rows.append(
            {
                "elementary_block_length": int(length),
                "raw_linear_relative_bias": float(raw_linear / diffusion - 1),
                "raw_quartic_relative_bias": float(raw_response / derivative - 1),
                "two_length_linear_relative_bias": float(
                    corrected_linear / diffusion - 1
                ),
                "two_length_quartic_relative_bias": float(
                    corrected_response / derivative - 1
                ),
                "coefficient_bias_bounds": exponential_two_length_bias_bounds(
                    alpha, bare_gain, horizon, dimension, length, covariance
                ),
            }
        )
    spectrum = cubic_force_covariance_sum(
        weights, gain, covariance, dimension, maximum_lag
    )
    tail = exponential_cubic_tail_bound(
        alpha, bare_gain, horizon, dimension, maximum_lag
    )
    return {
        "scope": "stationary perturbative coefficients and long-block paired reference only; no finite-run power guarantee",
        "alpha": alpha,
        "horizon": horizon,
        "eta": eta,
        "dimension": dimension,
        "finite_D2": diffusion,
        "finite_D4_per_unit_beta": derivative,
        "lag_diagnostics": rows,
        "cubic_covariance_maximum_lag": maximum_lag,
        "cubic_force_spectrum_partial_sum": spectrum,
        "cubic_force_spectrum_omitted_absolute_bound": tail,
        "long_block_reference": paired_long_block_reference(
            weights, gain, covariance, dimension, spectrum
        ),
        "finite_block_paired_covariance": "not yet bounded; long-block variance must not be used as finite-L power",
        "finite_noise_transport_remainder": "not yet numerically bounded",
    }


if __name__ == "__main__":
    print(json.dumps(audit_paired_reference(), indent=2))
