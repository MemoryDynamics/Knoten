"""Kinematic FIFO mass redistribution, not an electromagnetic current law.

The Fourier current uses explicitly chosen straight segments. Other paths with
the same endpoints differ by a divergence-free current. No dynamics is changed.
"""

import numpy as np


def fifo_replacement_coefficients(weights):
    """Return a_j=w_j-w_{j+1}, with w_H=0, for a filled fixed-weight FIFO.

    sum(a)=w_0. For decreasing weights a>=0; arbitrary nonnegative weights
    remain algebraically valid but can give signed redistribution coefficients.
    """
    weights = np.asarray(weights, float)
    if (
        weights.ndim != 1
        or len(weights) < 1
        or not np.isfinite(weights).all()
        or np.any(weights < 0)
        or weights.sum() <= 0
    ):
        raise ValueError(
            "finite nonnegative nonempty weights with positive mass required"
        )
    return weights - np.r_[weights[1:], 0.0]


def _geometry(points, wavevectors, sigma):
    points, wavevectors = np.asarray(points, float), np.asarray(wavevectors, float)
    if (
        points.ndim != 2
        or points.shape[0] < 1
        or points.shape[1] < 1
        or wavevectors.ndim != 2
        or wavevectors.shape[1] != points.shape[1]
        or not np.isfinite(points).all()
        or not np.isfinite(wavevectors).all()
        or not np.isfinite(sigma)
        or sigma < 0
    ):
        raise ValueError(
            "finite matching spatial arrays and nonnegative sigma required"
        )
    return points, wavevectors, np.exp(-0.5 * sigma**2 * np.sum(wavevectors**2, axis=1))


def path_current_fourier(path, wavevectors, *, sigma=0.0):
    """Unit-mass current along a declared polygonal path, per update.

    Fourier convention exp(-i*k.x); sigma=0 represents delta deposits, and
    sigma>0 a normalized Gaussian of covariance sigma^2 I. No grid quadrature.
    """
    path, k, smoothing = _geometry(path, wavevectors, sigma)
    if len(path) < 2:
        raise ValueError("path needs at least two endpoints")
    displacement = np.diff(path, axis=0)
    midpoint = (path[1:] + path[:-1]) / 2
    phase = k @ displacement.T
    factors = np.exp(-1j * (k @ midpoint.T)) * np.sinc(phase / (2 * np.pi))
    result = smoothing[:, None] * (factors @ displacement)
    if not np.isfinite(result).all():
        raise ValueError("non-finite current")
    return result


def fifo_current_fourier(history, new_point, weights, wavevectors, *, sigma=0.0):
    """Exact Fourier mass increment and straight-segment current of one write.

    History is full and newest first. The old current point is deliberately
    absent: it need not equal history[0] and is not a second density deposit.
    """
    history, k, smoothing = _geometry(history, wavevectors, sigma)
    new_point = np.asarray(new_point, float)
    coefficients = fifo_replacement_coefficients(weights)
    if (
        new_point.shape != (history.shape[1],)
        or not np.isfinite(new_point).all()
        or len(coefficients) != len(history)
    ):
        raise ValueError("matching new point and FIFO weights required")
    displacement = new_point - history
    phase = k @ displacement.T
    old_phase = np.exp(-1j * (k @ history.T))
    increment = smoothing * ((old_phase * np.expm1(-1j * phase)) @ coefficients)
    factors = np.exp(-1j * (k @ ((history + new_point) / 2).T)) * np.sinc(
        phase / (2 * np.pi)
    )
    current = smoothing[:, None] * ((factors * coefficients) @ displacement)
    if not np.isfinite(increment).all() or not np.isfinite(current).all():
        raise ValueError("non-finite FIFO Fourier balance")
    return dict(
        increment=increment, current=current, replacement_coefficients=coefficients
    )
