"""Data-derived metrics for reduced memory features."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class MetricEstimate:
    """A positive-semidefinite metric with explicit numerical support."""

    metric: np.ndarray
    eigenvalues: np.ndarray
    rank: int
    cutoff: float


def _feature_matrix(values: np.ndarray, *, name: str) -> np.ndarray:
    matrix = np.asarray(values, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] < 2 or matrix.shape[1] < 1:
        raise ValueError(f"{name} must have shape (samples, features)")
    if not np.isfinite(matrix).all():
        raise ValueError(f"{name} must be finite")
    return matrix


def _symmetric(values: np.ndarray, *, name: str) -> np.ndarray:
    matrix = np.asarray(values, dtype=float)
    if (
        matrix.ndim != 2
        or matrix.shape[0] != matrix.shape[1]
        or matrix.shape[0] < 1
        or not np.isfinite(matrix).all()
    ):
        raise ValueError(f"{name} must be a finite square matrix")
    return 0.5 * (matrix + matrix.T)


def covariance_precision_metric(
    samples: np.ndarray,
    *,
    relative_cutoff: float = 1e-6,
) -> MetricEstimate:
    """Return a truncated covariance pseudoinverse without lifting null modes."""

    values = _feature_matrix(samples, name="samples")
    cutoff_ratio = float(relative_cutoff)
    if not np.isfinite(cutoff_ratio) or not 0.0 <= cutoff_ratio < 1.0:
        raise ValueError("relative_cutoff must lie in [0, 1)")
    covariance = np.cov(values, rowvar=False, bias=False)
    covariance = np.atleast_2d(covariance)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    maximum = float(max(0.0, eigenvalues[-1]))
    cutoff = float(cutoff_ratio * maximum)
    supported = eigenvalues > cutoff
    inverse_values = np.zeros_like(eigenvalues)
    inverse_values[supported] = np.reciprocal(eigenvalues[supported])
    metric = (eigenvectors * inverse_values) @ eigenvectors.T
    return MetricEstimate(
        metric=np.asarray(metric, dtype=float),
        eigenvalues=np.asarray(eigenvalues, dtype=float),
        rank=int(np.count_nonzero(supported)),
        cutoff=cutoff,
    )


def exponential_block_weights(
    sample_steps: np.ndarray,
    *,
    forgetting_factor: float,
) -> np.ndarray:
    """Assign each sampled endpoint the exact forgotten mass of its time block."""

    steps = np.asarray(sample_steps, dtype=int)
    if (
        steps.ndim != 1
        or steps.size < 2
        or steps[0] != 0
        or np.any(np.diff(steps) <= 0)
    ):
        raise ValueError("sample_steps must start at zero and increase strictly")
    q = float(forgetting_factor)
    if not np.isfinite(q) or not 0.0 <= q < 1.0:
        raise ValueError("forgetting_factor must lie in [0, 1)")
    previous = steps[:-1]
    following = steps[1:]
    return np.asarray(np.power(q, previous) - np.power(q, following), dtype=float)


def observability_gramian(
    response_jacobians: np.ndarray,
    sample_steps: np.ndarray,
    *,
    forgetting_factor: float,
    output_scale: float = 1.0,
) -> np.ndarray:
    """Return a weighted finite-horizon observability Gramian.

    Jacobians have shape ``(samples, output, memory)`` and include the zero-time
    sample. Exact exponential block masses make different sampling cadences
    comparable without normalizing every finite horizon to unit mass.
    """

    jacobians = np.asarray(response_jacobians, dtype=float)
    steps = np.asarray(sample_steps, dtype=int)
    if (
        jacobians.ndim != 3
        or jacobians.shape[0] != steps.size
        or jacobians.shape[1] < 1
        or jacobians.shape[2] < 1
        or not np.isfinite(jacobians).all()
    ):
        raise ValueError("response_jacobians must match sample_steps")
    scale = float(output_scale)
    if not np.isfinite(scale) or scale <= 0.0:
        raise ValueError("output_scale must be positive")
    weights = exponential_block_weights(steps, forgetting_factor=forgetting_factor)
    normalized = jacobians[1:] / scale
    gramian = np.einsum("t,tom,ton->mn", weights, normalized, normalized)
    return np.asarray(0.5 * (gramian + gramian.T), dtype=float)


def gaussian_rkhs_emission_norms(
    positions: np.ndarray,
    *,
    deposition_weight: float,
    carrier_decay: float,
    memory_decay: float,
    kernel_sigma: float,
) -> np.ndarray:
    """Track the RKHS norm of the field emitted by one carrier perturbation.

    ``positions[0]`` is the initial source position. At update ``t`` the
    carrier perturbation has amplitude ``carrier_decay**t`` and deposits a
    normalized Gaussian representer. The returned scalar norm applies to each
    ambient carrier component independently.
    """

    points = _feature_matrix(positions, name="positions")
    beta = float(deposition_weight)
    carrier = float(carrier_decay)
    memory = float(memory_decay)
    sigma = float(kernel_sigma)
    if not np.isfinite(beta) or beta < 0.0:
        raise ValueError("deposition_weight must be finite and non-negative")
    if not np.isfinite(carrier) or not 0.0 <= carrier <= 1.0:
        raise ValueError("carrier_decay must lie in [0, 1]")
    if not np.isfinite(memory) or not 0.0 <= memory <= 1.0:
        raise ValueError("memory_decay must lie in [0, 1]")
    if not np.isfinite(sigma) or sigma <= 0.0:
        raise ValueError("kernel_sigma must be positive")

    norms = np.zeros(points.shape[0], dtype=float)
    coefficients = np.empty(points.shape[0] - 1, dtype=float)
    active_points = np.empty((points.shape[0] - 1, points.shape[1]), dtype=float)
    count = 0
    for update in range(1, points.shape[0]):
        coefficients[:count] *= memory
        coefficient = beta * carrier**update
        if count:
            differences = active_points[:count] - points[update]
            kernel_values = np.exp(
                -0.5 * np.einsum("nd,nd->n", differences, differences) / sigma**2
            )
            cross = float(np.dot(coefficients[:count], kernel_values))
        else:
            cross = 0.0
        norms[update] = (
            memory * memory * norms[update - 1]
            + 2.0 * coefficient * cross
            + coefficient * coefficient
        )
        coefficients[count] = coefficient
        active_points[count] = points[update]
        count += 1
    return norms


def isotropic_rkhs_observability_metric(
    emission_norms: np.ndarray,
    sample_steps: np.ndarray,
    *,
    forgetting_factor: float,
    feature_dimension: int,
) -> np.ndarray:
    """Integrate scalar RKHS field norms into a carrier-space metric."""

    norms = np.asarray(emission_norms, dtype=float)
    steps = np.asarray(sample_steps, dtype=int)
    if norms.shape != steps.shape or not np.isfinite(norms).all() or np.any(norms < 0):
        raise ValueError("emission_norms must be non-negative and match sample_steps")
    if feature_dimension < 1:
        raise ValueError("feature_dimension must be positive")
    weights = exponential_block_weights(steps, forgetting_factor=forgetting_factor)
    value = float(np.dot(weights, norms[1:]))
    return value * np.eye(feature_dimension)


def metric_pullback(forward_operator: np.ndarray, metric: np.ndarray) -> np.ndarray:
    """Pull a positive-semidefinite memory metric back to visible features."""

    forward = np.asarray(forward_operator, dtype=float)
    memory_metric = _symmetric(metric, name="metric")
    if (
        forward.ndim != 2
        or forward.shape[0] != memory_metric.shape[0]
        or not np.isfinite(forward).all()
    ):
        raise ValueError("forward_operator and metric dimensions must match")
    result = forward.T @ memory_metric @ forward
    return np.asarray(0.5 * (result + result.T), dtype=float)


def trace_normalized_distance(left: np.ndarray, right: np.ndarray) -> float:
    """Compare metric shape after explicitly discarding overall scale."""

    a = _symmetric(left, name="left")
    b = _symmetric(right, name="right")
    if a.shape != b.shape:
        raise ValueError("metrics must have matching shapes")
    trace_a = float(np.trace(a))
    trace_b = float(np.trace(b))
    if trace_a <= 0.0 or trace_b <= 0.0:
        raise ValueError("metrics must have positive trace")
    return float(np.linalg.norm(a / trace_a - b / trace_b, ord="fro"))


def supported_subspace_overlap(
    left: np.ndarray,
    right: np.ndarray,
    *,
    relative_cutoff: float = 1e-8,
) -> float:
    """Return normalized projector overlap of supported metric subspaces."""

    a = _symmetric(left, name="left")
    b = _symmetric(right, name="right")
    if a.shape != b.shape:
        raise ValueError("metrics must have matching shapes")
    if not 0.0 <= relative_cutoff < 1.0:
        raise ValueError("relative_cutoff must lie in [0, 1)")

    def projector(matrix: np.ndarray) -> tuple[np.ndarray, int]:
        values, vectors = np.linalg.eigh(matrix)
        keep = values > relative_cutoff * max(0.0, float(values[-1]))
        basis = vectors[:, keep]
        return basis @ basis.T, int(np.count_nonzero(keep))

    projector_a, rank_a = projector(a)
    projector_b, rank_b = projector(b)
    if rank_a == 0 or rank_b == 0:
        return 0.0
    return float(np.trace(projector_a @ projector_b) / min(rank_a, rank_b))
