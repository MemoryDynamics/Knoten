"""Horizon-specific Arnoldi adapter with an explicit portable start vector.

The historical stability gate module is hash-frozen by several completed
experiments.  This module extends the reusable numerical boundary without
changing those historical source bytes.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from typing import Any

import numpy as np
from scipy.sparse.linalg import ArpackNoConvergence, eigs

from .rotating_wave_stability import (
    circular_history,
    co_rotating_fifo_jacobian,
    co_rotating_fifo_step,
    finite_memory_weights,
    native_fifo_step,
    rotation_matrix,
)
from .rotating_wave_stability_gate import (
    ArnoldiPanel,
    RotatingWaveCandidate,
    StabilityThresholds,
    analytic_symmetry_checks,
    symmetry_basis,
    symmetry_eigenvalue_pass,
)


PREFLIGHT_SCHEMA = "scalar-memory-rotating-wave-g5-preflight-v1"
EQUATION_ID = "deterministic-native-k0h-full-fifo-v1"


@dataclass(frozen=True)
class HorizonStabilityPreflight:
    """Validated full-FIFO state plus its persistable scalar record."""

    history: np.ndarray
    jacobian: Any
    record: dict[str, Any]


def _float64_sha256(values: np.ndarray) -> str:
    portable = np.ascontiguousarray(np.asarray(values, dtype="<f8"))
    return hashlib.sha256(portable.tobytes()).hexdigest()


def _csr_sha256(jacobian: Any) -> str:
    canonical = jacobian.copy().tocsr()
    canonical.sort_indices()
    digest = hashlib.sha256()
    for values, dtype in (
        (canonical.indptr, "<i8"),
        (canonical.indices, "<i8"),
        (canonical.data, "<f8"),
    ):
        block = np.ascontiguousarray(np.asarray(values, dtype=dtype)).tobytes()
        digest.update(len(block).to_bytes(8, byteorder="little", signed=False))
        digest.update(block)
    return digest.hexdigest()


def preflight_sha256(record: dict[str, Any]) -> str:
    """Return the canonical JSON hash used to bind a persisted preflight."""

    content = json.dumps(
        record,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def build_full_fifo_preflight(
    candidate: RotatingWaveCandidate,
    *,
    fixed_point_maximum: float,
    symmetry_residual_maximum: float,
) -> HorizonStabilityPreflight:
    """Build and validate the direct-equation state used by the G5 solvers."""

    if not math.isfinite(fixed_point_maximum) or fixed_point_maximum < 0.0:
        raise ValueError("fixed-point threshold must be finite and nonnegative")
    if (
        not math.isfinite(symmetry_residual_maximum)
        or symmetry_residual_maximum < 0.0
    ):
        raise ValueError("symmetry threshold must be finite and nonnegative")

    parameters = candidate.step_parameters()
    history = circular_history(
        radius=candidate.radius,
        theta=candidate.theta,
        horizon=candidate.horizon,
    )
    native_update = native_fifo_step(history, **parameters)
    expected_native = history @ rotation_matrix(candidate.theta).T
    native_covariance_error = float(
        np.max(np.abs(native_update - expected_native))
    )
    co_rotating_update = co_rotating_fifo_step(
        history,
        theta=candidate.theta,
        **parameters,
    )
    fixed_point_error = float(np.max(np.abs(co_rotating_update - history)))
    weights = finite_memory_weights(
        alpha=candidate.alpha,
        horizon=candidate.horizon,
        memory_mass=candidate.memory_mass,
    )
    retained_weight_sum = float(math.fsum(float(value) for value in weights))
    q = 1.0 - candidate.alpha
    retained_weight_closed_form = candidate.memory_mass * (
        1.0 - q**candidate.horizon
    )
    weight_identity_error = abs(
        retained_weight_sum - retained_weight_closed_form
    )

    jacobian = co_rotating_fifo_jacobian(
        history,
        theta=candidate.theta,
        **parameters,
    )
    expected_dimension = 2 * candidate.horizon
    expected_nnz = 8 * candidate.horizon - 4
    symmetry = analytic_symmetry_checks(
        jacobian,
        history,
        candidate,
        residual_maximum=symmetry_residual_maximum,
    )
    finite_scalars = all(
        math.isfinite(value)
        for value in (
            native_covariance_error,
            fixed_point_error,
            retained_weight_sum,
            retained_weight_closed_form,
            weight_identity_error,
            symmetry["rotation_relative_residual"],
            symmetry["translation_x_relative_residual"],
            symmetry["translation_y_relative_residual"],
        )
    )
    gates = {
        "finite": finite_scalars,
        "fixed_point": fixed_point_error <= fixed_point_maximum,
        "jacobian_structure": bool(
            jacobian.shape == (expected_dimension, expected_dimension)
            and jacobian.nnz == expected_nnz
        ),
        "native_circle_covariance": (
            native_covariance_error <= fixed_point_maximum
        ),
        "symmetries": symmetry["pass"] is True,
        "weight_identity": weight_identity_error <= 8.0 * math.ulp(
            max(1.0, abs(retained_weight_closed_form))
        ),
    }
    gates["pass"] = all(gates.values())
    record = {
        "candidate": {
            "candidate_id": candidate.candidate_id,
            "horizon": candidate.horizon,
            "radius": candidate.radius,
            "theta": candidate.theta,
        },
        "equation": {
            "alpha": candidate.alpha,
            "amplitude_att": candidate.amplitude_att,
            "amplitude_rep": candidate.amplitude_rep,
            "deposition_weight": candidate.alpha * candidate.memory_mass,
            "equation_id": EQUATION_ID,
            "eta": candidate.eta,
            "memory_mass": candidate.memory_mass,
            "noise_amplitude": 0.0,
            "q": q,
            "sigma_att": candidate.sigma_att,
            "sigma_rep": candidate.sigma_rep,
        },
        "gates": gates,
        "jacobian": {
            "dimension": expected_dimension,
            "nnz": jacobian.nnz,
            "sha256": _csr_sha256(jacobian),
            "shape": list(jacobian.shape),
        },
        "memory": {
            "closed_form_retained_weight": retained_weight_closed_form,
            "direct_retained_weight": retained_weight_sum,
            "identity_absolute_error": weight_identity_error,
        },
        "orbit": {
            "co_rotating_fixed_point_max_abs_error": fixed_point_error,
            "history_sha256": _float64_sha256(history),
            "native_circle_covariance_max_abs_error": native_covariance_error,
        },
        "portability": "same-platform-binary64-transcendentals",
        "schema": PREFLIGHT_SCHEMA,
        "symmetry": {
            "residual_maximum": symmetry_residual_maximum,
            **symmetry,
        },
        "thresholds": {
            "fixed_point_maximum": fixed_point_maximum,
            "symmetry_residual_maximum": symmetry_residual_maximum,
        },
    }
    if gates["pass"] is not True:
        failed = sorted(name for name, value in gates.items() if not value)
        raise ArithmeticError(f"G5 full-FIFO preflight failed: {failed}")
    return HorizonStabilityPreflight(
        history=history,
        jacobian=jacobian,
        record=record,
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


def _canonical_projection_overlap(value: float, *, dimension: int) -> float:
    """Map roundoff-sized projection-bound drift back to ``[0, 1]``.

    A normalized orthogonal projection is mathematically bounded by one.
    Binary64 dot products, QR, and norms can cross that bound by a few ulp.
    The error budget is a conservative multiple of the standard accumulated
    roundoff bound for ``dimension`` terms; larger violations fail closed.
    """

    overlap = float(value)
    accumulated = dimension * np.finfo(np.float64).eps
    if dimension < 1 or accumulated >= 1.0:
        raise ValueError("projection dimension is outside the binary64 error model")
    tolerance = 8.0 * accumulated / (1.0 - accumulated)
    if not math.isfinite(overlap) or not -tolerance <= overlap <= 1.0 + tolerance:
        raise ArithmeticError("symmetry overlap violates the projection bound")
    return min(1.0, max(0.0, overlap))


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
        translation_overlap = _canonical_projection_overlap(
            np.linalg.norm(translation_basis.conj().T @ vector) / vector_norm,
            dimension=vector.size,
        )
        rotation_overlap = _canonical_projection_overlap(
            abs(np.vdot(rotation_basis, vector)) / vector_norm,
            dimension=vector.size,
        )
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
