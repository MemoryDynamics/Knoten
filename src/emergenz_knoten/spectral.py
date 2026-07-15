"""Scale-resolved spectral-dimension diagnostics for point clouds."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class SpectralDimensionResult:
    """Heat-trace profile and its selected intermediate-scale plateau."""

    dimension: float
    times: np.ndarray
    heat_trace: np.ndarray
    local_dimensions: np.ndarray
    laplacian_eigenvalues: np.ndarray
    bandwidth: float
    neighbor_count: int
    start_index: int
    stop_index: int
    log_width: float
    valid_scaling: bool


def _empty_result(
    *,
    bandwidth: float = float("nan"),
    neighbor_count: int = 0,
) -> SpectralDimensionResult:
    empty = np.array([], dtype=float)
    return SpectralDimensionResult(
        dimension=float("nan"),
        times=empty,
        heat_trace=empty,
        local_dimensions=empty,
        laplacian_eigenvalues=empty,
        bandwidth=float(bandwidth),
        neighbor_count=int(neighbor_count),
        start_index=-1,
        stop_index=-1,
        log_width=0.0,
        valid_scaling=False,
    )


def _as_points(points: Iterable[Iterable[float]]) -> np.ndarray:
    array = np.asarray(points, dtype=float)
    if array.ndim != 2:
        raise ValueError("points must be a 2D array with shape (n_points, dim)")
    if array.shape[0] < 2:
        raise ValueError("at least two points are required")
    if not np.isfinite(array).all():
        raise ValueError("points must be finite")
    return array


def heat_trace_spectral_dimension(
    points: Iterable[Iterable[float]],
    *,
    bandwidth_factor: float = 1.0,
    eigen_count: int = 50,
    neighbor_count: int = 8,
    time_points: int = 256,
    stability_tolerance: float = 0.25,
    min_log_width: float = float(np.log(2.0)),
) -> SpectralDimensionResult:
    """Estimate dimension from a stable heat-trace scaling window.

    A density-corrected diffusion kernel is built at a local
    k-nearest-neighbor scale. For normalized-Laplacian eigenvalues mu_i, the
    heat trace is Z(t) = sum_i exp(-t * mu_i), and the scale-dependent spectral
    dimension is -2 d log Z / d log t. A scalar estimate is accepted only when
    that derivative has a sufficiently wide, stable intermediate-scale
    plateau. Otherwise dimension is NaN and valid_scaling is false.

    Finite clouds have short-scale discretization artifacts and long-scale
    saturation. The window selection excludes both regimes.
    """

    pts = _as_points(points)
    if not np.isfinite(bandwidth_factor) or bandwidth_factor <= 0.0:
        raise ValueError("bandwidth_factor must be positive and finite")
    if eigen_count <= 1:
        raise ValueError("eigen_count must be greater than one")
    if neighbor_count < 2:
        raise ValueError("neighbor_count must be at least two")
    if time_points < 32:
        raise ValueError("time_points must be at least 32")
    if not np.isfinite(stability_tolerance) or stability_tolerance <= 0.0:
        raise ValueError("stability_tolerance must be positive and finite")
    if not np.isfinite(min_log_width) or min_log_width <= 0.0:
        raise ValueError("min_log_width must be positive and finite")
    if len(pts) < 100:
        return _empty_result(
            neighbor_count=min(int(neighbor_count), len(pts) - 1)
        )

    d2 = ((pts[:, None, :] - pts[None, :, :]) ** 2).sum(-1)
    k_neighbors = min(int(neighbor_count), len(pts) - 1)
    neighbor_d2 = d2.copy()
    np.fill_diagonal(neighbor_d2, np.inf)
    local_scale = np.partition(
        neighbor_d2, k_neighbors - 1, axis=1
    )[:, k_neighbors - 1]
    local_scale = local_scale[np.isfinite(local_scale) & (local_scale > 1e-14)]
    if local_scale.size == 0:
        return _empty_result(neighbor_count=k_neighbors)
    bandwidth = float(np.median(local_scale)) * float(bandwidth_factor)
    if not np.isfinite(bandwidth) or bandwidth <= 0.0:
        return _empty_result(
            bandwidth=bandwidth, neighbor_count=k_neighbors
        )

    kernel = np.exp(-d2 / bandwidth)
    density = kernel.sum(axis=1)
    density_corrected = kernel / (
        np.outer(density, density) + np.finfo(float).tiny
    )
    degree = density_corrected.sum(axis=1)
    symmetric_transition = density_corrected / np.sqrt(
        np.outer(degree, degree) + np.finfo(float).tiny
    )

    transition_eigenvalues = np.linalg.eigvalsh(symmetric_transition)
    laplacian_eigenvalues = np.maximum(1.0 - transition_eigenvalues, 0.0)
    laplacian_eigenvalues.sort()
    zero_modes = laplacian_eigenvalues[laplacian_eigenvalues <= 1e-10]
    positive_modes = laplacian_eigenvalues[laplacian_eigenvalues > 1e-10]
    if positive_modes.size < 2:
        return _empty_result(
            bandwidth=bandwidth, neighbor_count=k_neighbors
        )

    positive_modes = positive_modes[: min(int(eigen_count), positive_modes.size)]
    selected_modes = np.concatenate((zero_modes, positive_modes))
    times = np.geomspace(
        0.1 / float(positive_modes[-1]),
        10.0 / float(positive_modes[0]),
        int(time_points),
    )
    heat_trace = np.exp(-np.outer(times, selected_modes)).sum(axis=1)
    log_times = np.log(times)
    local_dimensions = -2.0 * np.gradient(
        np.log(heat_trace), log_times, edge_order=2
    )
    local_change = np.gradient(local_dimensions, log_times, edge_order=2)

    min_trace = max(float(zero_modes.size) + 1.0, 2.5)
    eligible = (
        np.isfinite(local_dimensions)
        & np.isfinite(local_change)
        & (heat_trace > min_trace)
        & (heat_trace < 0.5 * float(selected_modes.size))
        & (local_dimensions >= 0.25)
        & (local_dimensions <= 20.0)
        & (np.abs(local_change) <= float(stability_tolerance))
    )

    windows: list[tuple[float, int, int]] = []
    start: int | None = None
    for index, is_eligible in enumerate(eligible):
        if bool(is_eligible) and start is None:
            start = index
        if start is not None and (
            not bool(is_eligible) or index == len(eligible) - 1
        ):
            stop = index if bool(is_eligible) else index - 1
            width = float(log_times[stop] - log_times[start])
            if width >= float(min_log_width):
                windows.append((width, start, stop))
            start = None

    if not windows:
        return SpectralDimensionResult(
            dimension=float("nan"),
            times=times,
            heat_trace=heat_trace,
            local_dimensions=local_dimensions,
            laplacian_eigenvalues=selected_modes,
            bandwidth=bandwidth,
            neighbor_count=k_neighbors,
            start_index=-1,
            stop_index=-1,
            log_width=0.0,
            valid_scaling=False,
        )

    log_width, start_index, stop_index = max(windows, key=lambda item: item[0])
    dimension = float(
        np.median(local_dimensions[start_index : stop_index + 1])
    )
    valid = bool(np.isfinite(dimension) and 0.25 <= dimension <= 20.0)
    return SpectralDimensionResult(
        dimension=dimension if valid else float("nan"),
        times=times,
        heat_trace=heat_trace,
        local_dimensions=local_dimensions,
        laplacian_eigenvalues=selected_modes,
        bandwidth=bandwidth,
        neighbor_count=k_neighbors,
        start_index=start_index if valid else -1,
        stop_index=stop_index if valid else -1,
        log_width=log_width if valid else 0.0,
        valid_scaling=valid,
    )
