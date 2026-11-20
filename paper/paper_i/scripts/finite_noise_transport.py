"""Conservative finite-noise error budget, without target trajectories.

Real-arithmetic inequalities are evaluated in floating point, not interval
arithmetic. The initialization contract is a FULL canonical memory at one
point, not empty-memory startup. No numerical panel is authorized here.
"""

from __future__ import annotations

import json

import numpy as np
from scipy.special import gammaln

from finite_block_transport import audit_finite_block_reference
from paired_transport import _checked_covariance, _positive_integer
from weak_nonlinearity import covariance_response, exponential_weights


def gaussian_norm(dimension, order):
    """Lp norm of the Euclidean norm of a standard d-vector."""
    _positive_integer(dimension, "dimension")
    if not np.isfinite(order) or order < 1:
        raise ValueError("require finite order >= 1")
    return float(
        np.exp(
            0.5 * np.log(2)
            + (gammaln((dimension + order) / 2) - gammaln(dimension / 2)) / order
        )
    )


def remainder_constants(
    alpha,
    horizon,
    eta,
    repulsion,
    attraction,
    repulsive_scale,
    attractive_scale,
    dimension,
    covariance=None,
):
    """Bounds for v=eps*W+eps**3*Z+E, with Z INCLUDING eta*lambda.

    Moment constants bound vector Lp norms. Dependence constants bound
    sums of vector Lp one-innovation differences, except dW2 which is a
    scalar-coordinate bound. Canonical gamma_j are NOT renormalized.
    """
    weights = exponential_weights(alpha, horizon)
    _positive_integer(dimension, "dimension")
    if (
        not np.all(
            np.isfinite([eta, repulsion, attraction, repulsive_scale, attractive_scale])
        )
        or min(repulsive_scale, attractive_scale) <= 0
    ):
        raise ValueError("require finite kernel parameters and positive scales")
    q = 1 - alpha
    kappa = attraction / attractive_scale**2 - repulsion / repulsive_scale**2
    cubic = repulsion / (2 * repulsive_scale**4) - attraction / (
        2 * attractive_scale**4
    )
    hessian = (
        abs(repulsion) / repulsive_scale**2 + abs(attraction) / attractive_scale**2
    )
    a3 = abs(eta) * (
        abs(repulsion) / (2 * repulsive_scale**4)
        + abs(attraction) / (2 * attractive_scale**4)
    )
    a5 = abs(eta) * (
        abs(repulsion) / (8 * repulsive_scale**6)
        + abs(attraction) / (8 * attractive_scale**6)
    )
    alambda = abs(eta * cubic)
    theta = abs(eta) * hessian * q / alpha
    theta_linear = abs(eta * kappa) * q / alpha
    root = q + abs(eta) * hessian * q
    if (
        not np.all(np.isfinite([theta, theta_linear, a3, a5, alambda]))
        or not 0 <= theta < 1
        or not 0 < root < 1
    ):
        raise ValueError("require resolved strict global contraction")
    mass = -np.expm1(horizon * np.log1p(-alpha))
    gain = eta * kappa * mass
    if covariance is None:
        covariance, _, _ = covariance_response(weights, gain, dimension)
    else:
        _, covariance = _checked_covariance(weights, gain, covariance)
    tf, tl = 1 / (1 - theta), 1 / (1 - theta_linear)
    ages = np.arange(1, horizon, dtype=float)
    gamma = alpha * q**ages
    nonlinear_lag = tf * np.minimum(ages, np.pi / 2 * np.sqrt(ages))
    linear_lag = np.sqrt(np.diag(covariance))
    r, s, j = nonlinear_lag, linear_lag, ages
    mixed = gamma @ (j * (r**2 + r * s + s**2))

    def u(p):
        return tl * a3 * gaussian_norm(dimension, 3 * p) ** 3 * (gamma @ r**3)

    def z(p):
        return tl * alambda * gaussian_norm(dimension, 3 * p) ** 3 * (gamma @ s**3)

    def e(p):
        return tl * (
            alambda * u(3 * p) * gaussian_norm(dimension, 3 * p) ** 2 * mixed
            + a5 * gaussian_norm(dimension, 5 * p) ** 5 * (gamma @ r**5)
        )

    def du(p):
        return (
            3
            * np.sqrt(2)
            * a3
            * tl
            * tf
            * gaussian_norm(dimension, 3 * p) ** 3
            * (gamma @ (j * r**2))
        )

    def dz(p):
        return (
            3
            * np.sqrt(2)
            * alambda
            * tl**2
            * gaussian_norm(dimension, 3 * p) ** 3
            * (gamma @ (j * s**2))
        )

    def de(p):
        return tl * (
            alambda
            * gaussian_norm(dimension, 3 * p) ** 2
            * (
                du(3 * p) * mixed
                + np.sqrt(2)
                * u(3 * p)
                * (gamma @ (j**2 * ((2 * r + s) * tf + (r + 2 * s) * tl)))
            )
            + 5
            * np.sqrt(2)
            * a5
            * tf
            * gaussian_norm(dimension, 5 * p) ** 5
            * (gamma @ (j * r**4))
        )

    values = {
        "u4": u(4),
        "z4": z(4),
        "e4": e(4),
        "dU2": du(2),
        "dZ2": dz(2),
        "dE2": de(2),
        "dW2": np.sqrt(2) * tl,
    }
    if not np.all(np.isfinite(list(values.values()))):
        raise ValueError("remainder constants overflow")
    mu = gamma @ j
    diffusion2 = 0.5 / (1 + eta * kappa * mu) ** 2
    diffusion4 = (
        -eta
        * cubic
        * (dimension + 2)
        * (gamma @ (j * s**2))
        / (1 + eta * kappa * mu) ** 3
    )
    return {
        "theta": float(theta),
        "theta_linear": float(theta_linear),
        "positive_root": float(root),
        "nonlinear_filter_l1": float(tf),
        "linear_filter_l1": float(tl),
        "dimension": dimension,
        "D2": float(diffusion2),
        "D4": float(diffusion4),
        **{key: float(value) for key, value in values.items()},
    }


def transport_error_coefficients(constants):
    """A,B,C for |D-eps^2 D2-eps^4 D4| <= eps^6(A+B eps^2+C eps^4)."""
    w, z, e = (constants[key] for key in ("dW2", "dZ2", "dE2"))
    return np.array([0.5 * z**2 + w * e, z * e, 0.5 * e**2])


def estimator_error_coefficients(constants, length):
    """L2 remainder of 2*Dhat_(2L)-Dhat_L, for any number of blocks/seeds.

    No independence or averaging improvement for the remainder is assumed.
    Returns coefficients multiplying eps^6, eps^8, eps^10.
    """
    _positive_integer(length, "length")
    d = constants["dimension"]
    z, e = constants["z4"], constants["e4"]

    def raw(m):
        w = gaussian_norm(d, 4) * constants["linear_filter_l1"] * np.sqrt(m)
        return np.array(
            [w * e / d + m * z**2 / (2 * d), m * z * e / d, m * e**2 / (2 * d)]
        )

    return 2 * raw(2 * length) + raw(length)


def flat_start_error_coefficient(alpha, theta, dimension, length, superblocks, burn_in):
    """L2 difference from stationary two-length estimator <= eps^2 * result.

    All increments at n<=0 are zero; memory is FULL with canonical weights.
    Discard updates 1,...,burn_in, then retain 2*L*superblocks increments.
    """
    _positive_integer(dimension, "dimension")
    _positive_integer(length, "length")
    _positive_integer(superblocks, "superblocks")
    if (
        isinstance(burn_in, bool)
        or not isinstance(burn_in, (int, np.integer))
        or burn_in < 0
    ):
        raise ValueError("burn_in must be a nonnegative integer")
    if (
        not np.isfinite(alpha)
        or not 0 < alpha < 1
        or not np.isfinite(theta)
        or not 0 <= theta < 1
    ):
        raise ValueError("require 0<alpha<1 and 0<=theta<1")
    root = 1 - alpha * (1 - theta)
    if not 0 < root < 1:
        raise ValueError("initialization decay must be resolved")
    if theta == 0:
        return 0.0
    log_root = np.log(root)
    t = gaussian_norm(dimension, 4) / (1 - theta)

    def average_decay(m, count):
        return -np.expm1(count * m * log_root) / (count * -np.expm1(m * log_root))

    def raw(m, count):
        initial = (
            t
            * theta
            * np.exp(burn_in * log_root)
            * -np.expm1(m * log_root)
            / (1 - root)
        )
        stationary = t * min(m, np.pi / 2 * np.sqrt(m))
        return (
            2 * stationary * initial * average_decay(m, count)
            + initial**2 * average_decay(2 * m, count)
        ) / (2 * dimension * m)

    return float(2 * raw(2 * length, superblocks) + raw(length, 2 * superblocks))


def sufficient_noise_interval(coefficients, initial, allowance):
    """Sufficient eps interval for a*t+b*t^2+c*t^3+initial/t <= allowance.

    t=eps^2. Split the allowance equally; no parameter search or fitted
    noise selection. A failed sufficient interval is NOT a no-go theorem.
    """
    coefficients = np.asarray(coefficients, dtype=float)
    if (
        coefficients.shape != (3,)
        or not np.all(np.isfinite(coefficients))
        or np.any(coefficients < 0)
        or coefficients[0] <= 0
    ):
        raise ValueError("require finite nonnegative polynomial with a>0")
    if (
        not np.isfinite(initial)
        or initial < 0
        or not np.isfinite(allowance)
        or allowance <= 0
    ):
        raise ValueError("require initial>=0 and allowance>0")
    a, b, c = coefficients
    lower = 2 * initial / allowance
    trial = allowance / (2 * a)
    upper = (allowance / 2) / (a + b * trial + c * trial**2)
    return {
        "nonempty": bool(lower <= upper),
        "epsilon_lower": float(np.sqrt(lower)),
        "epsilon_upper": float(np.sqrt(upper)),
        "zero_endpoint_excluded": True,
    }


def relative_error_budget(
    epsilon,
    coefficient_bias,
    sampling_sd,
    estimator,
    transport,
    initial,
    failure_probability,
):
    """Triangle/Markov radius relative to |eps^4 * Delta D4|, not to D2."""
    estimator, transport = (
        np.asarray(estimator, dtype=float),
        np.asarray(transport, dtype=float),
    )
    if (
        not np.isfinite(epsilon)
        or epsilon <= 0
        or not np.isfinite(failure_probability)
        or not 0 < failure_probability < 1
    ):
        raise ValueError("require eps>0 and 0<failure probability<1")
    if (
        any(
            a.shape != (3,) or not np.all(np.isfinite(a)) or np.any(a < 0)
            for a in (estimator, transport)
        )
        or not np.all(np.isfinite([coefficient_bias, sampling_sd, initial]))
        or min(coefficient_bias, sampling_sd, initial) < 0
    ):
        raise ValueError("error inputs must be finite and nonnegative")
    t = epsilon**2
    powers = np.array([t, t**2, t**3])
    estimator_rest = float(estimator @ powers)
    transport_rest = float(transport @ powers)
    initialization = float(initial / t)
    stochastic_radius = (sampling_sd + estimator_rest + initialization) / np.sqrt(
        failure_probability
    )
    return {
        "coefficient_bias": float(coefficient_bias),
        "sampling_l2": float(sampling_sd),
        "estimator_remainder_l2": estimator_rest,
        "initialization_l2": initialization,
        "transport_remainder": transport_rest,
        "radius_about_leading_prediction": float(coefficient_bias + stochastic_radius),
        "radius_about_finite_noise_transport": float(
            coefficient_bias + stochastic_radius + transport_rest
        ),
    }


def audit_finite_noise_budget():
    """Fixed pre-existing comparison and count, not an approved experiment."""
    alpha, horizon, dimension = 0.01, 600, 3
    eta = 0.5 * alpha / ((1 - alpha) * (1 + 35 / 9))
    length, superblocks, burn_in = 1000, 200_000, 10_000
    covariance, _, _ = covariance_response(
        exponential_weights(alpha, horizon),
        eta * 26 / 9 * (1 - (1 - alpha) ** horizon),
        dimension,
    )
    models = [
        remainder_constants(alpha, horizon, eta, ar, aa, 1, 3, dimension, covariance)
        for ar, aa in ((0, 26), (1, 35))
    ]
    contrast = models[1]["D4"] - models[0]["D4"]
    estimator = sum((estimator_error_coefficients(m, length) for m in models)) / abs(
        contrast
    )
    transport = sum((transport_error_coefficients(m) for m in models)) / abs(contrast)
    initial = sum(
        flat_start_error_coefficient(
            alpha, m["theta"], dimension, length, superblocks, burn_in
        )
        for m in models
    ) / abs(contrast)
    reference = audit_finite_block_reference()
    bias = reference["coefficient_bias_bounds"][
        "quartic_per_beta_absolute_bias_bound"
    ] / abs(reference["long_time_mean_per_beta"])
    sd = reference["relative_sampling_sd_bound_against_long_time_coefficient"]
    failure, margin = 0.05, 0.10
    base = bias + sd / np.sqrt(failure)
    interval = sufficient_noise_interval(
        transport + estimator / np.sqrt(failure),
        initial / np.sqrt(failure),
        margin - base,
    )

    def budget(eps):
        return relative_error_budget(
            eps, bias, sd, estimator, transport, initial, failure
        )

    return {
        "scope": "conditional real-arithmetic full nonlinear bound; floating-point evaluation, not interval/roundoff certification or panel authorization",
        "initialization": "H coincident points with FULL canonical weights; not empty-memory startup",
        "alpha": alpha,
        "horizon": horizon,
        "eta": eta,
        "dimension": dimension,
        "elementary_block_length": length,
        "superblocks_per_seed": superblocks,
        "seeds": reference["seeds"],
        "burn_in": burn_in,
        "models": models,
        "Delta_D4": float(contrast),
        "relative_estimator_coefficients": estimator.tolist(),
        "relative_transport_coefficients": transport.tolist(),
        "relative_initialization_coefficient": float(initial),
        "reference_radius": float(base),
        "diagnostic_margin_not_protocol": margin,
        "sufficient_noise_interval": interval,
        "lower_endpoint_budget": budget(interval["epsilon_lower"]),
        "upper_endpoint_budget": budget(interval["epsilon_upper"]),
        "previously_proposed_noise_budget": budget(0.007),
        "upper_endpoint_leading_contrast_relative_to_linear_diffusion": float(
            interval["epsilon_upper"] ** 2 * abs(contrast) / models[0]["D2"]
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit_finite_noise_budget(), indent=2))
