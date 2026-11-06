"""Exact Gaussian readout expectations for the declared R=t=0 comparison.

Deterministic moment/propagator algebra only, not a native FIFO simulator or an
assertion that the nonlinear pair is Gaussian. Evaluations use binary64.
"""

from numbers import Integral

import numpy as np
from scipy.linalg import solve_discrete_lyapunov

from .pair_lag_diagnostics import _probabilities
from .pair_path_diagnostics import _constants


def isotropic_gaussian_contrast(mean, joint_variance, product_variance, kernel):
    """E grad K(N(mean,v_joint I)) minus E grad K(N(mean,v_product I)).

    Variances are PER COORDINATE, not radii or traces. The last mean axis is
    spatial. Leading cubic term and a global fifth-order remainder bound are
    returned alongside an expm1 evaluation of the full Gaussian integral.
    """
    mean = np.asarray(mean, float)
    joint, product = (
        np.asarray(joint_variance, float),
        np.asarray(product_variance, float),
    )
    if mean.ndim < 1 or mean.shape[-1] < 1 or not np.isfinite(mean).all():
        raise ValueError("finite mean vectors required")
    joint, product = np.broadcast_arrays(joint, product, np.zeros(mean.shape[:-1]))[:2]
    if (
        not np.isfinite(joint).all()
        or not np.isfinite(product).all()
        or np.any(joint < 0)
        or np.any(product < 0)
    ):
        raise ValueError("nonnegative finite coordinate variances required")
    amplitudes = np.array([kernel.amplitude_rep, -kernel.amplitude_att], float)
    widths = np.array([kernel.sigma_rep, kernel.sigma_att], float)
    if (
        not np.isfinite(amplitudes).all()
        or not np.isfinite(widths).all()
        or np.any(widths <= 0)
    ):
        raise ValueError("finite kernel with positive widths required")
    dim, radius2 = mean.shape[-1], np.sum(mean**2, axis=-1)
    delta = joint - product
    coefficient = np.zeros_like(radius2)
    for amplitude, sigma in zip(amplitudes, widths, strict=True):
        scale2 = sigma**2
        joint_scale, product_scale = scale2 + joint, scale2 + product
        log_product = -(dim / 2 + 1) * np.log1p(product / scale2) - radius2 / (
            2 * product_scale
        )
        log_joint = -(dim / 2 + 1) * np.log1p(joint / scale2) - radius2 / (
            2 * joint_scale
        )
        log_ratio = -(dim / 2 + 1) * np.log1p(
            delta / product_scale
        ) + radius2 * delta / (2 * joint_scale * product_scale)
        # Use the larger exponent as base; expm1 always receives a nonpositive
        # argument, avoiding both cancellation and exp(large)*exp(-large).
        difference = np.where(
            log_ratio >= 0,
            -np.exp(log_joint) * np.expm1(-np.maximum(log_ratio, 0)),
            np.exp(log_product) * np.expm1(np.minimum(log_ratio, 0)),
        )
        coefficient -= amplitude / scale2 * difference
    cubic = np.sum(amplitudes / widths**4) / 2
    c5 = np.sum(np.abs(amplitudes) / widths**6) / 8

    def fifth_moment_bound(variance):
        sixth = (
            radius2**3
            + 3 * (dim + 4) * variance * radius2**2
            + 3 * (dim + 2) * (dim + 4) * variance**2 * radius2
            + dim * (dim + 2) * (dim + 4) * variance**3
        )
        return sixth ** (5 / 6)

    result = dict(
        exact=coefficient[..., None] * mean,
        cubic=(cubic * (dim + 2) * delta)[..., None] * mean,
        cubic_error_bound=c5
        * (fifth_moment_bound(joint) + fifth_moment_bound(product)),
    )
    if not all(np.isfinite(v).all() for v in result.values()):
        raise ValueError("non-finite Gaussian expectation")
    return result


def linear_gaussian_moments(
    *, alpha, self_gain, cross_gain, epsilon, points, centers, length
):
    """Finite-start Gaussian moments of the 3-state stable inner comparison.

    No random generator, trajectory update, or fitted parameters. The common
    absolute position is deliberately absent because it has a neutral mode.
    """
    if (
        not isinstance(length, Integral)
        or isinstance(length, bool)
        or length < 1
        or not np.isfinite([alpha, self_gain, cross_gain, epsilon]).all()
        or not 0 < alpha <= 1
        or not 0 < cross_gain <= self_gain
        or self_gain + cross_gain > 1
        or epsilon < 0
    ):
        raise ValueError("stable nonnegative comparison parameters required")
    points, centers = np.asarray(points, float), np.asarray(centers, float)
    if (
        points.ndim != 2
        or points.shape[0] != 2
        or points.shape[1] < 1
        or centers.shape != points.shape
        or not np.isfinite(points).all()
        or not np.isfinite(centers).all()
    ):
        raise ValueError("finite points and centers (2,d) required")
    q, s = 1 - alpha, 1 - self_gain - cross_gain
    lam = q * s
    matrix = np.array(
        [[s, self_gain - cross_gain], [alpha * s, q + alpha * (self_gain - cross_gain)]]
    )
    v, e = np.array([1.0, alpha]), np.array([1.0, -1.0])
    stationary = solve_discrete_lyapunov(matrix, 2 * epsilon**2 * np.outer(v, v))
    powers = np.empty((length, 2, 2))
    powers[0] = np.eye(2)
    for n in range(1, length):
        powers[n] = matrix @ powers[n - 1]
    lam_powers = lam ** np.arange(length)
    covariance = stationary - powers @ stationary @ powers.transpose(0, 2, 1)
    covariance[0] = 0
    variance_common_stationary = epsilon**2 * q**2 / (2 * (1 - lam**2))
    variance_common = variance_common_stationary * (1 - lam_powers**2)
    relative_mean = powers @ np.array([points[0] - points[1], centers[0] - centers[1]])
    common_mean = lam_powers[:, None] * (points.mean(axis=0) - centers.mean(axis=0))
    relative_inner = (relative_mean[:, 0] - relative_mean[:, 1]) / 2
    inner_means = np.stack(
        [common_mean + relative_inner, common_mean - relative_inner], axis=1
    )
    inner_variance = variance_common + np.einsum("i,nij,j->n", e, covariance, e) / 4
    if np.any(inner_variance < 0):
        raise ValueError("negative numerical variance")
    return dict(
        matrix=matrix,
        powers=powers,
        relative_covariance=covariance,
        common_variance=variance_common,
        common_powers=lam_powers,
        stationary_relative_covariance=stationary,
        stationary_common_variance=variance_common_stationary,
        inner_means=inner_means,
        inner_variance=inner_variance,
    )


def linear_gaussian_pair_readout(
    *,
    alpha,
    self_gain,
    cross_gain,
    epsilon,
    points,
    centers,
    separation,
    weights,
    start,
    stop,
    kernel,
):
    """Full fixed-window expectation, retaining every time and source age.

    This evaluates the nonlinear READOUT on linear Gaussian comparison states,
    not the nonlinear state law. No inference of native signal size or power.
    """
    p = _probabilities(weights)
    if (
        any(not isinstance(n, Integral) or isinstance(n, bool) for n in (start, stop))
        or not len(p) <= start < stop
    ):
        raise ValueError("integer window after initial history replacement required")
    moments = linear_gaussian_moments(
        alpha=alpha,
        self_gain=self_gain,
        cross_gain=cross_gain,
        epsilon=epsilon,
        points=points,
        centers=centers,
        length=stop,
    )
    r = np.asarray(separation, float)
    if r.shape != (np.shape(points)[1],) or not np.isfinite(r).all():
        raise ValueError("finite fixed reference separation required")
    e = np.array([1.0, -1.0])
    exact, cubic = np.zeros((2, len(r))), np.zeros((2, len(r)))
    error = np.zeros(2)
    cross_mean, cross_abs_mean = 0.0, 0.0
    stationary_cross = []
    for lag, weight in enumerate(p):
        past = slice(start - lag, stop - lag)
        now = slice(start, stop)
        cross = (
            moments["common_powers"][lag] * moments["common_variance"][past]
            - np.einsum(
                "i,ij,njk,k->n",
                e,
                moments["powers"][lag],
                moments["relative_covariance"][past],
                e,
            )
            / 4
        )
        cross_mean += weight * float(np.mean(cross))
        cross_abs_mean += weight * float(np.mean(np.abs(cross)))
        stationary_cross.append(
            moments["common_powers"][lag] * moments["stationary_common_variance"]
            - e
            @ moments["powers"][lag]
            @ moments["stationary_relative_covariance"]
            @ e
            / 4
        )
        product = moments["inner_variance"][now] + moments["inner_variance"][past]
        joint = product - 2 * cross
        for target, source, sign in ((0, 1, 1), (1, 0, -1)):
            mean = (
                sign * r
                + moments["inner_means"][now, target]
                - moments["inner_means"][past, source]
            )
            readout = isotropic_gaussian_contrast(mean, joint, product, kernel)
            exact[target] += weight * readout["exact"].mean(axis=0)
            cubic[target] += weight * readout["cubic"].mean(axis=0)
            error[target] += weight * readout["cubic_error_bound"].mean()
    kappa, _, _, _ = _constants(kernel)
    return dict(
        claim_class="finite_window_linear_Gaussian_comparison_only_not_native_prediction",
        start=int(start),
        stop=int(stop),
        source_ages=len(p),
        exact_gradient_contrast=exact.tolist(),
        cubic_gradient_contrast=cubic.tolist(),
        cubic_error_bound=error.tolist(),
        mean_cross_covariance_per_coordinate=cross_mean,
        mean_absolute_cross_covariance_per_coordinate=cross_abs_mean,
        stationary_weighted_cross_covariance_per_coordinate=float(p @ stationary_cross),
        stationary_lag_zero_cross_covariance=float(stationary_cross[0]),
        stationary_inner_variance_per_coordinate=float(
            moments["stationary_common_variance"]
            + e @ moments["stationary_relative_covariance"] @ e / 4
        ),
        linear_reference_gradient_norm=float(abs(kappa) * np.linalg.norm(r)),
        ideal_readout_zero_at_zero_mean=True,
        target_trajectories_generated=0,
    )
