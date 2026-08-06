"""Structure-preserving modal reductions for source-local Telegraph gates."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np
from scipy import linalg

from .local_mediator import LocalMediatorGrid, TelegraphMediator
from .source_local_linear import LinearChannel


def _interior_readout(
    grid: LocalMediatorGrid,
    readout_position: float,
) -> np.ndarray:
    coordinates = grid.coordinates
    position = float(readout_position)
    if not math.isfinite(position) or not coordinates[0] < position < coordinates[-1]:
        raise ValueError("readout_position must lie strictly inside the grid")
    floating = position / grid.spacing + grid.source_index
    left = int(math.floor(floating))
    fraction = floating - left
    if left < 1 or left + 1 >= grid.n_points - 1:
        raise ValueError("readout_position must use two interior grid points")
    result = np.zeros(grid.n_points - 2, dtype=float)
    result[left - 1] = 1.0 - fraction
    result[left] = fraction
    return result


def telegraph_spatial_mode_reductions(
    grid: LocalMediatorGrid,
    mediator: TelegraphMediator,
    *,
    readout_position: float,
    orders: Iterable[int],
) -> dict[int, LinearChannel]:
    """Return stable reductions ranked by source-to-readout DC contribution.

    Each Dirichlet spatial eigenmode retains its complete real ``(u, p)``
    Telegraph block. Consequently truncation cannot split conjugate temporal
    modes or manufacture an unstable block.
    """

    requested = tuple(sorted(set(int(value) for value in orders)))
    interior = grid.n_points - 2
    if not requested or any(value < 2 or value % 2 for value in requested):
        raise ValueError("orders must be non-empty positive even integers")
    if requested[-1] > 2 * interior:
        raise ValueError("order exceeds the exact channel order")

    laplacian = np.zeros((interior, interior), dtype=float)
    np.fill_diagonal(laplacian, -2.0)
    np.fill_diagonal(laplacian[1:], 1.0)
    np.fill_diagonal(laplacian[:, 1:], 1.0)
    laplace_values, spatial_modes = linalg.eigh(laplacian)
    field_rates = (
        mediator.wave_speed**2 / grid.spacing**2 * laplace_values
        - mediator.natural_frequency**2
    )
    point_source = np.zeros(interior, dtype=float)
    point_source[grid.source_index - 1] = 1.0 / grid.spacing
    readout = _interior_readout(grid, readout_position)
    source_modes = spatial_modes.T @ point_source
    readout_modes = readout @ spatial_modes
    dc_contributions = -readout_modes * source_modes / field_rates
    full_dc_gain = float(np.sum(dc_contributions))
    if not math.isfinite(full_dc_gain) or full_dc_gain <= 0.0:
        raise ValueError("full modal DC gain must be positive and finite")
    ranking = np.argsort(-np.abs(dc_contributions), kind="stable")

    dt = grid.time_step
    momentum_retention = 1.0 - 2.0 * mediator.damping_rate * dt
    reductions: dict[int, LinearChannel] = {}
    for order in requested:
        selected = ranking[: order // 2]
        transition = np.zeros((order, order), dtype=float)
        source_vector = np.zeros(order, dtype=float)
        readout_vector = np.zeros(order, dtype=float)
        for block, mode_index in enumerate(selected):
            rate = float(field_rates[mode_index])
            start = 2 * block
            transition[start : start + 2, start : start + 2] = (
                (1.0 + dt * dt * rate, dt * momentum_retention),
                (dt * rate, momentum_retention),
            )
            normalized_source = float(source_modes[mode_index] / full_dc_gain)
            source_vector[start : start + 2] = (
                dt * dt * normalized_source,
                dt * normalized_source,
            )
            readout_vector[start] = float(readout_modes[mode_index])
        reductions[order] = LinearChannel(
            transition=transition,
            source=source_vector,
            readout=readout_vector,
        )
    return reductions
