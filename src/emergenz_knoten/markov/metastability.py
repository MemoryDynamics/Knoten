"""Small metastability helpers for finite transfer matrices."""

from __future__ import annotations

from typing import Iterable

import numpy as np


def leading_nontrivial_eigenvalues(
    eigenvalues: Iterable[complex],
    *,
    count: int = 3,
    unit_tol: float = 1e-8,
) -> np.ndarray:
    """Return leading non-unit eigenvalues by modulus."""

    if count < 1:
        raise ValueError("count must be positive")
    values = np.asarray(eigenvalues, dtype=complex)
    if values.ndim != 1:
        raise ValueError("eigenvalues must be a 1D array")
    nontrivial = values[~np.isclose(np.abs(values), 1.0, atol=unit_tol)]
    order = np.argsort(-np.abs(nontrivial))
    return nontrivial[order[:count]]


def spectral_gap(
    eigenvalues: Iterable[complex],
    *,
    unit_tol: float = 1e-8,
) -> float:
    """Return ``1 - |lambda_2|`` after removing unit-modulus eigenvalues."""

    slow = leading_nontrivial_eigenvalues(eigenvalues, count=1, unit_tol=unit_tol)
    if slow.size == 0:
        return float("nan")
    return float(1.0 - abs(slow[0]))
