"""Target-free weak-noise coefficients for exponential-memory dynamics.

Stationary nonlinear validity requires the separately proved global
condition, not merely a stable linear reference. No trajectory simulation
or existence proof is performed here. Production evidence remains frozen.
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import solve_discrete_lyapunov


def exponential_contraction_diagnostic(alpha: float, global_hessian_gain: float):
    """Return (theta, history_decay, contraction_rate) or (theta, None, None).

    global_hessian_gain bounds |eta|*sup_x ||Hess K(x)|| for unit memory mass;
    it is NOT the local curvature gain. The sufficient condition theta<1
    covers all truncations and the untruncated exponential history.
    This floating-point diagnostic is not an interval certificate or a
    simulation authorization. Unresolved near-boundary rates return None.
    """
    if not np.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("require finite 0<alpha<1")
    q = 1 - alpha
    if not 0 < q < 1:
        raise ValueError("memory decay must be resolvable in floating point")
    if not np.isfinite(global_hessian_gain) or global_hessian_gain < 0:
        raise ValueError("global Hessian gain must be finite and nonnegative")
    theta = global_hessian_gain * q / alpha
    if not np.isfinite(theta):
        raise ValueError("contraction diagnostic overflows")
    if theta >= 1:
        return theta, None, None
    threshold = max(q ** (1 / 5), q / (1 - global_hessian_gain * q))
    history_decay = (1 + threshold) / 2
    if not q < history_decay**5 < 1:
        return theta, None, None
    rate = max(
        history_decay,
        global_hessian_gain * q / (1 - q / history_decay),
    )
    if not np.isfinite(rate) or rate >= 1:
        return theta, None, None
    return theta, history_decay, rate


def exponential_weights(alpha: float, horizon: int) -> np.ndarray:
    if not np.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("require finite 0<alpha<1")
    if isinstance(horizon, bool) or not isinstance(horizon, (int, np.integer)):
        raise ValueError("horizon must be an integer")
    if horizon < 2:
        raise ValueError("require H>=2 for lag coordinates")
    weights = (1 - alpha) ** np.arange(horizon, dtype=float)
    return weights / weights.sum()


def finite_averaging_diagnostic(
    alpha: float, horizon: int, radial_feedback_bound: float
):
    """Return (chi, self_weight, log10_moment_factor), or (chi, None, None).

    Assumes grad K(u)=c(|u|)*u with 0<=eta*c<=radial_feedback_bound.
    The caller must check that sign condition separately. Canonical unit
    memory mass is assumed. chi<1 controls fixed-H stationary moments,
    NOT pairwise contraction, nonlinear transport, or an infinite horizon.
    The logarithmic factor avoids forming a block rate rounded to one.
    This floating-point diagnostic is not an interval certificate.
    """
    if not np.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("require finite 0<alpha<1")
    q = 1 - alpha
    if not 0 < q < 1:
        raise ValueError("memory decay must be resolvable in floating point")
    if isinstance(horizon, bool) or not isinstance(horizon, (int, np.integer)):
        raise ValueError("horizon must be an integer")
    if horizon < 2:
        raise ValueError("require H>=2")
    if not np.isfinite(radial_feedback_bound) or radial_feedback_bound < 0:
        raise ValueError("radial feedback bound must be finite and nonnegative")
    k = horizon - 1
    tail_mass = q * -np.expm1(k * np.log1p(-alpha))
    chi = radial_feedback_bound * tail_mass
    if chi >= 1:
        return float(chi), None, None
    log_factor = np.log10(float(k)) - k * np.log1p(-chi) / np.log(10)
    if not np.isfinite(log_factor):
        raise ValueError("moment-factor diagnostic overflows")
    return float(chi), float(1 - chi), float(log_factor)


def lag_matrix(weights, gain: float) -> np.ndarray:
    """Advance L_j=x_n-x_(n-j), j=1,...,H-1, in the linear map."""
    weights = np.asarray(weights, dtype=float)
    if (
        weights.ndim != 1
        or weights.size < 2
        or not np.all(np.isfinite(weights))
        or np.any(weights < 0)
        or not np.isclose(weights.sum(), 1.0, rtol=0, atol=1e-13)
    ):
        raise ValueError("weights must be a finite normalized nonnegative vector")
    if not np.isfinite(gain) or not 0 <= gain < 1:
        raise ValueError("require finite 0<=g<1")
    size = len(weights) - 1
    matrix = -gain * np.outer(np.ones(size), weights[1:])
    matrix[1:, :-1] += np.eye(size - 1)
    return matrix


def covariance_response(weights, gain: float, dimension: int):
    """Return unit-noise covariance C and its derivative at t=beta*eps^2=0.

    grad K(u)=kappa*u+lambda*|u|^2*u+O(|u|^5), beta=eta*M*lambda.
    Wick contraction yields the exact first-order moment forcing *if* the
    local stationary expansion exists. It is not a finite-noise closure.
    """
    if (
        isinstance(dimension, bool)
        or not isinstance(dimension, (int, np.integer))
        or dimension < 1
    ):
        raise ValueError("dimension must be a positive integer")
    matrix = lag_matrix(weights, gain)
    weights = np.asarray(weights, dtype=float)
    source = np.ones(matrix.shape[0])
    if np.max(np.abs(np.linalg.eigvals(matrix))) >= 1:
        raise ValueError("relative linear state is not stable")
    covariance = solve_discrete_lyapunov(matrix, np.outer(source, source))
    derivative_matrix = -(dimension + 2) * np.outer(
        source, weights[1:] * np.diag(covariance)
    )
    forcing = derivative_matrix @ covariance @ matrix.T
    derivative = solve_discrete_lyapunov(matrix, forcing + forcing.T)
    return covariance, derivative, derivative_matrix


def radius_energies(weights, covariance, dimension: int) -> np.ndarray:
    """Position and cloud second moments; also applies to their derivatives."""
    tail = np.asarray(weights, dtype=float)[1:]
    relative = tail @ covariance @ tail
    cloud = tail @ np.diag(covariance) - relative
    return dimension * np.array([relative, cloud])


def transport_response(weights, gain: float, derivative_matrix=None):
    """Per-coordinate D/eps^2 and its formal derivative with respect to t."""
    matrix = lag_matrix(weights, gain)
    inverse_response = np.linalg.solve(
        np.eye(len(matrix)) - matrix, np.ones(len(matrix))
    )
    transfer = inverse_response[0]
    if derivative_matrix is None:
        return 0.5 * transfer**2, 0.0
    transfer_derivative = np.linalg.solve(
        np.eye(len(matrix)) - matrix, derivative_matrix @ inverse_response
    )[0]
    return 0.5 * transfer**2, transfer * transfer_derivative


def untruncated_transport_response(
    alpha: float, gain: float, cubic_gain: float, dimension: int
):
    """Return D2, D4 in per-coordinate D=eps^2*D2+eps^4*D4+O(eps^6).

    Canonical unit-mass exponential memory: gain=eta*kappa and
    cubic_gain=eta*lambda. Linear stability is checked here; it does not
    certify the nonlinear expansion's global contraction hypothesis.
    """
    if not np.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("require finite 0<alpha<1")
    q = 1 - alpha
    if not 0 < q < 1:
        raise ValueError("memory decay must be resolvable in floating point")
    if not np.isfinite(gain) or not np.isfinite(cubic_gain):
        raise ValueError("curvature and cubic gains must be finite")
    if (
        isinstance(dimension, bool)
        or not isinstance(dimension, (int, np.integer))
        or dimension < 1
    ):
        raise ValueError("dimension must be a positive integer")
    root = q * (1 - gain)
    if not np.isfinite(root) or abs(root) >= 1:
        raise ValueError("untruncated linear increment process is not stable")
    # Stable gaps avoid subtracting two nearly equal numbers at small alpha.
    gap = alpha + q * gain
    memory_gap = alpha * (1 + q) + q**2 * gain
    numerator = alpha * (1 + 4 * q + q**2) + q * (q**2 + 2 * q - 1) * gap
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        age_covariance = np.divide(q * numerator, alpha * gap * (1 + root) * memory_gap)
        transfer = np.divide(alpha, gap)
        diffusion = 0.5 * transfer**2
        correction = -(dimension + 2) * cubic_gain * age_covariance * transfer**3
    if not np.all(np.isfinite([diffusion, correction, age_covariance])):
        raise ValueError("transport coefficients overflow")
    if age_covariance <= 0 or diffusion <= 0:
        raise ValueError("transport coefficients are unresolved in floating point")
    return float(diffusion), float(correction)


def stationary_msd(weights, gain: float, lags, dimension: int = 1):
    """Exact linear displacement variance/eps^2 from stationary increments."""
    lags = np.asarray(lags)
    if lags.ndim != 1 or not np.issubdtype(lags.dtype, np.integer) or np.any(lags < 0):
        raise ValueError("lags must be a vector of nonnegative integers")
    matrix = lag_matrix(weights, gain)
    covariance, _, _ = covariance_response(weights, gain, dimension)
    maximum = int(lags.max(initial=0))
    msd = np.zeros(maximum + 1)
    covariance_column = covariance[:, 0].copy()
    gamma_zero = covariance_column[0]
    correlation_sum = weighted_sum = 0.0
    for lag in range(1, maximum + 1):
        msd[lag] = lag * gamma_zero + 2 * (lag * correlation_sum - weighted_sum)
        covariance_column = matrix @ covariance_column
        correlation_sum += covariance_column[0]
        weighted_sum += lag * covariance_column[0]
    return dimension * msd[lags]
