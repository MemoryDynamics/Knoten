"""Finite transition matrices for sampled augmented-state features."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .validation import implied_relaxation_rates


def voxel_labels(points: Iterable[Iterable[float]], *, voxel_size: float) -> np.ndarray:
    """Assign each point to an integer voxel label."""

    pts = np.asarray(points, dtype=float)
    if pts.ndim != 2:
        raise ValueError("points must be a 2D array")
    if voxel_size <= 0.0:
        raise ValueError("voxel_size must be positive")

    boxes = np.floor(pts / voxel_size).astype(np.int64)
    label_by_box: dict[tuple[int, ...], int] = {}
    labels = np.empty(pts.shape[0], dtype=np.int64)
    for i, box in enumerate(boxes):
        key = tuple(int(v) for v in box)
        labels[i] = label_by_box.setdefault(key, len(label_by_box))
    return labels


def transition_count_matrix(
    labels: Iterable[int],
    *,
    sample_lag: int = 1,
    lag: int | None = None,
    n_states: int | None = None,
) -> np.ndarray:
    """Count sample-lagged transitions between integer state labels."""

    if lag is not None:
        sample_lag = lag
    arr = np.asarray(labels, dtype=np.int64)
    if arr.ndim != 1:
        raise ValueError("labels must be a 1D array")
    if sample_lag < 1:
        raise ValueError("sample_lag must be positive")
    if arr.size <= sample_lag:
        raise ValueError("need more labels than sample_lag")
    if np.any(arr < 0):
        raise ValueError("labels must be non-negative")
    if n_states is None:
        n_states = int(arr.max()) + 1
    if n_states < 1:
        raise ValueError("n_states must be positive")
    if n_states <= int(arr.max()):
        raise ValueError("n_states must exceed the maximum label")

    counts = np.zeros((n_states, n_states), dtype=float)
    for i in range(arr.size - sample_lag):
        counts[arr[i], arr[i + sample_lag]] += 1.0
    return counts


def row_stochastic_matrix(
    counts: Iterable[Iterable[float]],
    *,
    empty_row: str = "self",
) -> np.ndarray:
    """Normalize transition counts row-wise.

    Finite trajectories can produce states that are observed only as terminal
    targets for the chosen lag and therefore have no outgoing transition
    counts. By default these rows are made absorbing. Use ``empty_row="zero"``
    to keep a substochastic matrix with explicit zero rows.
    """

    mat = np.asarray(counts, dtype=float)
    if mat.ndim != 2 or mat.shape[0] != mat.shape[1]:
        raise ValueError("counts must be a square matrix")
    if empty_row not in {"self", "zero"}:
        raise ValueError("empty_row must be 'self' or 'zero'")
    row_sum = mat.sum(axis=1, keepdims=True)
    out = np.zeros_like(mat, dtype=float)
    np.divide(mat, row_sum, out=out, where=row_sum > 0.0)
    if empty_row == "self":
        empty = np.flatnonzero(row_sum[:, 0] == 0.0)
        out[empty, empty] = 1.0
    return out


@dataclass(frozen=True)
class TransferOperatorEstimate:
    labels: np.ndarray
    counts: np.ndarray
    transition_matrix: np.ndarray
    eigenvalues: np.ndarray
    relaxation_rates: np.ndarray
    empty_rows: np.ndarray
    sample_lag: int
    lag_updates: int | None


def estimate_transfer_operator(
    features: Iterable[Iterable[float]],
    *,
    voxel_size: float,
    sample_lag: int = 1,
    lag: int | None = None,
    sample_steps: Iterable[int] | None = None,
    lag_updates: int | None = None,
    lag_time: float | None = None,
    empty_row: str = "self",
) -> TransferOperatorEstimate:
    """Estimate a finite-state transfer operator from augmented features.

    ``sample_lag`` counts rows in the sampled feature array. The legacy
    keyword ``lag`` is accepted as an alias. ``lag_updates`` stores the
    corresponding update-index lag when known. ``lag_time`` is only a numeric
    denominator for rates and does not imply physical time.
    """

    if lag is not None:
        sample_lag = lag
    labels = voxel_labels(features, voxel_size=voxel_size)
    counts = transition_count_matrix(labels, sample_lag=sample_lag)
    empty_rows = np.flatnonzero(counts.sum(axis=1) == 0.0)
    transition = row_stochastic_matrix(counts, empty_row=empty_row)

    inferred_lag_updates = lag_updates
    if sample_steps is not None:
        steps = np.asarray(sample_steps, dtype=int)
        if steps.ndim != 1:
            raise ValueError("sample_steps must be a 1D array")
        if steps.shape[0] != labels.shape[0]:
            raise ValueError("sample_steps length must match features")
        update_lags = steps[sample_lag:] - steps[:-sample_lag]
        if update_lags.size and np.all(update_lags == update_lags[0]):
            inferred_lag_updates = int(update_lags[0])

    rate_denominator = float(
        lag_time
        if lag_time is not None
        else inferred_lag_updates
        if inferred_lag_updates is not None
        else sample_lag
    )
    eigenvalues, rates = implied_relaxation_rates(
        transition,
        lag_time=rate_denominator,
        drop_stationary=True,
    )
    return TransferOperatorEstimate(
        labels=labels,
        counts=counts,
        transition_matrix=transition,
        eigenvalues=eigenvalues,
        relaxation_rates=rates,
        empty_rows=empty_rows,
        sample_lag=int(sample_lag),
        lag_updates=inferred_lag_updates,
    )
