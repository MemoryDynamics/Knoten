"""Small metastability helpers for finite transfer matrices."""

from __future__ import annotations

from typing import Iterable

import numpy as np

from .validation import _drop_one_stationary_mode


def leading_nontrivial_eigenvalues(
    eigenvalues: Iterable[complex],
    *,
    count: int = 3,
    unit_tol: float = 1e-8,
) -> np.ndarray:
    """Return slow modes after removing exactly one stationary +1 mode."""

    if count < 1:
        raise ValueError("count must be positive")
    values = np.asarray(eigenvalues, dtype=complex)
    if values.ndim != 1:
        raise ValueError("eigenvalues must be a 1D array")
    order = np.argsort(-np.abs(values))
    nontrivial = _drop_one_stationary_mode(values[order], unit_tol=unit_tol)
    return nontrivial[:count]


def spectral_gap(
    eigenvalues: Iterable[complex],
    *,
    unit_tol: float = 1e-8,
) -> float:
    """Return ``1 - |lambda_2|`` after removing one stationary +1 mode.

    Periodic -1 modes and additional +1 modes therefore produce a zero gap.
    """

    slow = leading_nontrivial_eigenvalues(eigenvalues, count=1, unit_tol=unit_tol)
    if slow.size == 0:
        return float("nan")
    return float(1.0 - abs(slow[0]))
