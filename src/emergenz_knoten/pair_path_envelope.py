"""Analytical finite-horizon envelope for an identical, reciprocal Gaussian pair.

No trajectories or random numbers are generated. Returned numerical evaluations
are binary64 estimates of the documented inequalities, NOT interval certificates.
"""

from numbers import Integral

import numpy as np
from scipy.linalg import solve_discrete_lyapunov

from .kernels import ScalarReadoutKernel
from .pair_path_diagnostics import _constants


def _positive_integer(value):
    return isinstance(value, Integral) and not isinstance(value, bool) and value > 0


def pair_path_envelope(
    points,
    histories,
    *,
    alpha,
    eta,
    cross_eta,
    epsilon,
    memory_mass,
    kernel: ScalarReadoutKernel,
    updates,
    diameter,
    gaussian_threshold,
):
    """Evaluate a fixed proposed diameter, without searching for one.

    Inputs: points (2,d), newest-first histories (2,H,d). Exact geometric
    weights M*alpha*(1-alpha)**age and iid standard Gaussian node innovations
    are assumptions of the theorem, not inferred from a saved trajectory.
    ``closes_numerically`` is a prerequisite, not a simulator certification.
    """
    points, histories = np.asarray(points, float), np.asarray(histories, float)
    if (
        points.ndim != 2
        or points.shape[0] != 2
        or points.shape[1] < 1
        or histories.ndim != 3
        or histories.shape[0] != 2
        or histories.shape[1] < 1
        or histories.shape[2] != points.shape[1]
        or not np.isfinite(points).all()
        or not np.isfinite(histories).all()
    ):
        raise ValueError("finite points (2,d) and histories (2,H,d) required")
    parameters = [
        alpha,
        eta,
        cross_eta,
        epsilon,
        memory_mass,
        diameter,
        gaussian_threshold,
    ]
    if (
        not np.isfinite(parameters).all()
        or not 0 < alpha <= 1
        or not 0 < cross_eta <= eta
        or epsilon < 0
        or min(memory_mass, diameter, gaussian_threshold) <= 0
        or not _positive_integer(updates)
    ):
        raise ValueError("invalid envelope parameters")
    if (
        not np.isfinite(list(vars(kernel).values())).all()
        or not 0 < kernel.sigma_rep <= kernel.sigma_att
        or not 0 <= kernel.amplitude_rep
        or not 0 < kernel.amplitude_att
    ):
        raise ValueError("ordered positive widths and nonnegative amplitudes required")
    kappa, c3, _, gradient_bound = _constants(kernel)
    if kappa <= 0:
        raise ValueError("globally attractive radial coefficient required")
    horizon, dim = histories.shape[1:]
    q = 1 - alpha
    mass = memory_mass * (1 - q**horizon)
    p = alpha * q ** np.arange(horizon) / (1 - q**horizon)
    centers = np.einsum("h,ihd->id", p, histories)
    g, h = eta * kappa * mass, cross_eta * kappa * mass
    s = 1 - g - h
    convex_gain = (eta + cross_eta) * mass * kernel.amplitude_att / kernel.sigma_att**2
    if convex_gain > 1 or s < 0:
        raise ValueError("convex-update and nonnegative comparison matrix required")
    lam = q * s
    matrix = np.array([[s, g - h], [alpha * s, q + alpha * (g - h)]])
    drive = np.array([1.0, alpha])
    covariance = solve_discrete_lyapunov(
        matrix, 2 * epsilon**2 * np.outer(drive, drive)
    )
    covariance = (covariance + covariance.T) / 2
    e = np.array([1.0, -1.0])
    variance_v = epsilon**2 * q**2 / (2 * (1 - lam**2))
    variance_inner = variance_v + float(e @ covariance @ e) / 4
    a0, a1 = alpha / (1 - lam), q * (g + h) / (1 - lam)
    variance_lag = (
        epsilon**2
        / 2
        * (
            a0**2 * horizon
            + 2 * a0 * a1 * (1 - lam**horizon) / (1 - lam)
            + 2 * a1**2 * (1 - lam**horizon) / (1 - lam**2)
        )
    )
    if (
        not np.isfinite(covariance).all()
        or np.linalg.eigvalsh(covariance)[0] < 0
        or min(variance_inner, variance_lag) < 0
    ):
        raise ValueError("invalid numerical covariance")

    mean_x, mean_c = points.mean(axis=0), centers.mean(axis=0)
    v0 = float(np.linalg.norm(mean_x - mean_c))
    initial_common = float(
        np.max(np.linalg.norm(histories.mean(axis=0) - mean_x, axis=1))
    )
    initial_relative = max(
        float(np.linalg.norm(points[0] - points[1])),
        float(np.linalg.norm(centers[0] - centers[1])),
        float(np.max(np.linalg.norm(histories[0] - histories[1], axis=1))),
    )
    zdim = gaussian_threshold * np.sqrt(dim)
    innovation_bound = epsilon * zdim
    reference_diameter = (
        initial_relative
        + 2 * initial_common
        + (g + h) / (1 - lam) * v0
        + zdim * (np.sqrt(covariance[0, 0]) + np.sqrt(variance_lag))
    )
    nonlinear_bound = (eta + cross_eta) * mass * c3 * diameter**3
    tail_coefficient = alpha * q**horizon / (1 - q**horizon)
    tail_bound = tail_coefficient * (diameter + innovation_bound)
    relative_perturbation = nonlinear_bound / h + (g - h) / (alpha * h) * tail_bound
    common_lag_perturbation = (horizon * alpha + 2 * q) / (
        1 - lam
    ) * nonlinear_bound + (
        horizon * (1 + alpha * s / (1 - lam)) + 2 / (1 - lam)
    ) * tail_bound
    closure_rhs = reference_diameter + relative_perturbation + common_lag_perturbation
    inner_bound = (
        v0
        + initial_relative
        + zdim * np.sqrt(variance_inner)
        + (q / (1 - lam) + 1 / h) * nonlinear_bound
        + (1 / (1 - lam) + g / (alpha * h)) * tail_bound
    )
    # N*H common increments, N relative, 2N inner, 2N node innovations,
    # each in d coordinates. All times may be dependent; this is a union bound.
    scalar_count = int(updates) * dim * (horizon + 5)
    failure = min(1.0, float(2 * scalar_count * np.exp(-(gaussian_threshold**2) / 2)))
    result = dict(
        claim_class="exact_model_inequality_binary64_evaluation_not_interval_certificate",
        updates=int(updates),
        horizon=horizon,
        dimension=dim,
        proposed_diameter=diameter,
        gaussian_threshold=gaussian_threshold,
        convex_gain=convex_gain,
        self_gain=g,
        cross_gain=h,
        common_multiplier=lam,
        relative_matrix=matrix.tolist(),
        relative_covariance=covariance.tolist(),
        common_lag_variance_bound=variance_lag,
        inner_variance_bound=variance_inner,
        initial_relative_bound=initial_relative,
        initial_common_offset=initial_common,
        initial_common_inner=v0,
        innovation_bound=innovation_bound,
        reference_diameter_bound=reference_diameter,
        nonlinear_update_bound=nonlinear_bound,
        tail_update_bound=tail_bound,
        relative_perturbation_bound=relative_perturbation,
        common_lag_perturbation_bound=common_lag_perturbation,
        closure_rhs=closure_rhs,
        closure_margin=diameter - closure_rhs,
        closes_numerically=bool(closure_rhs < diameter),
        inner_bound=inner_bound,
        scalar_gaussian_count=scalar_count,
        failure_probability_bound=failure,
        cubic_coefficient=c3,
        global_gradient_bound=gradient_bound,
    )
    if not np.isfinite(
        [v for v in result.values() if isinstance(v, (int, float))]
    ).all():
        raise ValueError("non-finite envelope result")
    return result


def truncated_contrast_budget(
    envelope, separation_norm, *, independent_pairs, family_size, alpha=0.05
):
    """Budget for zero-on-failure whole-replica pairs; never discard failed pairs.

    Applies to the same-time/lag contrast with fixed R and windows starting
    after initial FIFO replacement. No data, power calculation, or run approval.
    """
    if not envelope["closes_numerically"]:
        raise ValueError("a closing envelope is required")
    if (
        not _positive_integer(independent_pairs)
        or not _positive_integer(family_size)
        or not np.isfinite([separation_norm, alpha]).all()
        or separation_norm < 0
        or not 0 < alpha < 1
    ):
        raise ValueError("invalid contrast budget parameters")
    bound = min(
        2
        * envelope["cubic_coefficient"]
        * (separation_norm + 2 * envelope["inner_bound"]) ** 3,
        2 * envelope["global_gradient_bound"],
    )
    half_width = (
        2 * bound * np.sqrt(np.log(2 * family_size / alpha) / (2 * independent_pairs))
    )
    bias = (
        2
        * envelope["global_gradient_bound"]
        * min(1, 2 * envelope["failure_probability_bound"])
    )
    return dict(
        local_contrast_norm_bound=bound,
        hoeffding_half_width=float(half_width),
        unconditional_truncation_bias_bound=bias,
        total_half_width=float(half_width + bias),
        includes_numerical_error=False,
    )
