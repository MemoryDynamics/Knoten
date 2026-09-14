"""Horizon-specific Arnoldi adapter with an explicit portable start vector.

The historical stability gate module is hash-frozen by several completed
experiments.  This module extends the reusable numerical boundary without
changing those historical source bytes.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

import numpy as np
from scipy.sparse.linalg import ArpackNoConvergence, eigs

from .rotating_wave_stability_gate import (
    ArnoldiPanel,
    RotatingWaveCandidate,
    StabilityThresholds,
    symmetry_basis,
    symmetry_eigenvalue_pass,
)


def _explicit_start(values: np.ndarray, *, dimension: int) -> np.ndarray:
    raw = np.asarray(values)
    if np.iscomplexobj(raw):
        raise ValueError("explicit Arnoldi start must be real")
    start = np.asarray(raw, dtype=np.float64)
    if start.shape != (dimension,):
        raise ValueError("explicit Arnoldi start has the wrong dimension")
    if not np.isfinite(start).all():
        raise ValueError("explicit Arnoldi start must be finite")
    if not np.any(start):
        raise ValueError("explicit Arnoldi start must be nonzero")
    return start


def _classify_with_vectors(
    jacobian: Any,
    eigenvalues: np.ndarray,
    eigenvectors: np.ndarray,
    history: np.ndarray,
    *,
    symmetry_overlap_minimum: float,
) -> list[dict[str, Any]]:
    translation_basis, rotation_basis = symmetry_basis(history)
    rows: list[dict[str, Any]] = []
    available = min(len(eigenvalues), eigenvectors.shape[1])
    for index in range(available):
        eigenvalue = eigenvalues[index]
        vector = eigenvectors[:, index]
        vector_norm = np.linalg.norm(vector)
        residual = float(
            np.linalg.norm(jacobian @ vector - eigenvalue * vector) / vector_norm
        )
        translation_overlap = float(
            np.linalg.norm(translation_basis.conj().T @ vector) / vector_norm
        )
        rotation_overlap = float(abs(np.vdot(rotation_basis, vector)) / vector_norm)
        if translation_overlap >= symmetry_overlap_minimum:
            classification = "translation"
        elif rotation_overlap >= symmetry_overlap_minimum:
            classification = "rotation"
        else:
            classification = "transverse"
        rows.append(
            {
                "real": float(eigenvalue.real),
                "imag": float(eigenvalue.imag),
                "modulus": float(abs(eigenvalue)),
                "normalized_residual": residual,
                "translation_overlap": translation_overlap,
                "rotation_overlap": rotation_overlap,
                "classification": classification,
                "vector": [
                    [float(value.real), float(value.imag)] for value in vector
                ],
            }
        )
    rows.sort(key=lambda row: row["modulus"], reverse=True)
    return rows


def run_lcg_eigen_panel(
    jacobian: Any,
    history: np.ndarray,
    candidate: RotatingWaveCandidate,
    panel: ArnoldiPanel,
    thresholds: StabilityThresholds,
    *,
    explicit_start: np.ndarray,
) -> dict[str, Any]:
    """Run one largest-modulus panel with the supplied vector passed to ARPACK."""

    start = _explicit_start(explicit_start, dimension=jacobian.shape[0])
    exception = None
    try:
        values, vectors = eigs(
            jacobian,
            k=panel.requested,
            which="LM",
            ncv=panel.ncv,
            tol=panel.tolerance,
            maxiter=panel.max_iterations,
            v0=start,
        )
        arpack_converged = True
    except ArpackNoConvergence as error:
        values = (
            np.asarray(error.eigenvalues)
            if error.eigenvalues is not None
            else np.empty(0, dtype=complex)
        )
        vectors = (
            np.asarray(error.eigenvectors)
            if error.eigenvectors is not None
            else np.empty((jacobian.shape[0], 0), dtype=complex)
        )
        exception = str(error)
        arpack_converged = False
    rows = _classify_with_vectors(
        jacobian,
        values,
        vectors,
        history,
        symmetry_overlap_minimum=thresholds.symmetry_overlap,
    )
    residual_pass = bool(
        len(rows) == panel.requested
        and all(
            row["normalized_residual"] <= thresholds.eigen_residual for row in rows
        )
    )
    recovered_symmetries = symmetry_eigenvalue_pass(
        rows,
        theta=candidate.theta,
        tolerance=thresholds.symmetry_eigenvalue,
    )
    transverse = [row for row in rows if row["classification"] == "transverse"]
    return {
        "registration": asdict(panel),
        "arpack_converged": arpack_converged,
        "exception": exception,
        "returned_eigenpairs": len(rows),
        "residual_pass": residual_pass,
        "symmetry_eigenvalue_pass": recovered_symmetries,
        "panel_pass": bool(
            arpack_converged and residual_pass and recovered_symmetries
        ),
        "leading_transverse": transverse[0] if transverse else None,
        "eigenpairs": rows,
    }
