"""Target-free, formal weak-noise response of the finite-history model.

This computes local perturbative coefficients, not a stationary nonlinear
simulation or an existence proof. Production evidence remains frozen.
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import solve_discrete_lyapunov


def exponential_weights(alpha: float, horizon: int) -> np.ndarray:
    if not np.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("require finite 0<alpha<1")
    if isinstance(horizon, bool) or not isinstance(horizon, (int, np.integer)):
        raise ValueError("horizon must be an integer")
    if horizon < 2:
        raise ValueError("require H>=2 for lag coordinates")
    weights = (1 - alpha) ** np.arange(horizon, dtype=float)
    return weights / weights.sum()


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
