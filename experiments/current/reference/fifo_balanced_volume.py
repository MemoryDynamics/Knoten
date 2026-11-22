"""Finite constrained write for the oriented-volume FIFO reference."""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

from emergenz_knoten.kernels import gaussian_gradient

from .fifo_4d_delayed_spin import delayed_step


def _head_cofactor(retained):
    singular = np.linalg.svd(retained, compute_uv=False)
    if singular[-1] <= 4 * np.finfo(float).eps * singular[0]:
        return np.zeros(4)
    return np.array(
        [(-1) ** i * np.linalg.det(np.delete(retained, i, axis=1)) for i in range(4)]
    )


def _closest_heads(targets, free_heads, normals):
    lengths = np.linalg.norm(normals, axis=1)
    active = lengths > 0
    if not active.any():
        return targets

    scale = lengths.max()
    normals = normals / scale
    lengths = lengths / scale
    total = np.sum(free_heads * normals)
    if np.sum(targets * normals) == total:
        return targets

    lengths = lengths[active]
    axes = normals[active] / lengths[:, None]
    fraction = np.clip(total / lengths.sum(), -1, 1)
    result = targets.copy()
    if abs(fraction) == 1:
        result[active] = fraction * axes
        return result

    parallel = np.sum(targets[active] * axes, axis=1)
    perpendicular = targets[active] - parallel[:, None] * axes
    transverse = np.linalg.norm(perpendicular, axis=1)
    if np.any(transverse <= 16 * np.finfo(float).eps):
        raise ValueError("axial targets outside the regular projection chart")

    def offsets(multiplier):
        axial = parallel - multiplier * lengths
        return axial, np.hypot(axial, transverse)

    def residual(multiplier):
        axial, norms = offsets(multiplier)
        return lengths @ (axial / norms) - total

    # At the individual bounds each active head supplies the same volume fraction.
    bounds = (parallel - transverse * fraction / np.sqrt(1 - fraction**2)) / lengths
    lower, upper = bounds.min(), bounds.max()
    if residual(lower) <= 0:
        multiplier = lower
    elif residual(upper) >= 0:
        multiplier = upper
    else:
        multiplier = brentq(residual, lower, upper, xtol=2e-15)
    axial, norms = offsets(multiplier)
    result[active] = (axial[:, None] * axes + perpendicular) / norms[:, None]
    return result


def balanced_gaussian_write(first, second, weights, *, coupling, sigma=1.0):
    """Apply one simultaneous write to two windows of four unit 4-vectors.

    The normalized Gaussian proposals are projected to the nearest heads
    with fixed total determinant. The regular chart excludes nontrivial
    axial targets, where nearest heads need not be unique. Cofactors
    below numerical rank resolution are treated as zero.
    """
    advanced = np.stack((delayed_step(first), delayed_step(second)))
    if not np.allclose(np.linalg.norm(advanced, axis=2), 1, atol=2e-15, rtol=2e-15):
        raise ValueError("balanced reference requires unit slots")

    free = advanced[:, 0]
    corrections = np.stack(
        [
            gaussian_gradient(head, other, weights, sigma=sigma, amplitude=coupling)
            for head, other in zip(free, (second, first), strict=True)
        ]
    )
    raw = free - corrections
    norms = np.linalg.norm(raw, axis=1)
    if not np.isfinite(norms).all() or np.any(norms == 0):
        raise ValueError("nonfinite or zero raw head")

    targets = raw / norms[:, None]
    normals = np.stack([_head_cofactor(window[1:]) for window in advanced])
    advanced[:, 0] = _closest_heads(targets, free, normals)
    return advanced
