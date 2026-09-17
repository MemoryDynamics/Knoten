"""Reusable numerical gate machinery for prepared rotating-wave stability."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Any

import numpy as np
from scipy.sparse.linalg import ArpackNoConvergence, eigs

from .rotating_wave_stability import (
    co_rotating_fifo_step,
    rotation_matrix,
    rotation_translation_quotient_distance,
    symmetry_tangent_vectors,
)


@dataclass(frozen=True)
class RotatingWaveCandidate:
    """Frozen native finite-memory rotating-wave candidate."""

    candidate_id: str
    radius: float
    theta: float
    alpha: float
    horizon: int
    memory_mass: float
    eta: float
    sigma_rep: float
    sigma_att: float
    amplitude_rep: float
    amplitude_att: float

    def step_parameters(self) -> dict[str, float]:
        """Return keyword arguments for the native FIFO update."""

        return {
            "alpha": self.alpha,
            "memory_mass": self.memory_mass,
            "eta": self.eta,
            "sigma_rep": self.sigma_rep,
            "sigma_att": self.sigma_att,
            "amplitude_rep": self.amplitude_rep,
            "amplitude_att": self.amplitude_att,
        }


@dataclass(frozen=True)
class ArnoldiPanel:
    """One preregistered ARPACK configuration."""

    name: str
    requested: int
    ncv: int
    tolerance: float
    max_iterations: int
    start_id: str


@dataclass(frozen=True)
class StabilityThresholds:
    """Frozen numerical thresholds for a local stability decision."""

    eigen_residual: float
    symmetry_overlap: float
    symmetry_eigenvalue: float
    leading_complex_agreement: float
    leading_modulus_agreement: float
    unstable_modulus: float
    stable_modulus: float
    perturbation_scale_fraction: float
    continuation_steps: int
    sample_every: int
    stopping_radius_fraction: float
    unstable_growth_minimum: float
    stable_transient_growth_maximum: float
    stable_final_ratio_maximum: float
    exact_control_distance_maximum: float


def deterministic_arnoldi_start(dimension: int, start_id: str) -> np.ndarray:
    """Return one of the two frozen deterministic Arnoldi starts."""

    if isinstance(dimension, bool) or not isinstance(dimension, int) or dimension < 1:
        raise ValueError("dimension must be a positive integer")
    indices = np.arange(dimension, dtype=float)
    if start_id == "S1":
        values = np.sin(math.sqrt(2.0) * (indices + 1.0))
        values += np.cos(math.sqrt(3.0) * (indices + 0.5))
    elif start_id == "S2":
        values = np.sin(math.sqrt(5.0) * (indices + 0.25))
        values -= np.cos(math.sqrt(7.0) * (indices + 0.75))
    else:
        raise ValueError(f"unknown Arnoldi start: {start_id}")
    return values / np.linalg.norm(values)


def symmetry_basis(history: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return orthonormal translation and rotation bases."""

    tangents = symmetry_tangent_vectors(history)
    translation = np.column_stack(
        (tangents["translation_x"], tangents["translation_y"])
    )
    translation_basis, _ = np.linalg.qr(translation)
    rotation = tangents["rotation"].copy()
    rotation -= translation_basis @ (translation_basis.T @ rotation)
    rotation /= np.linalg.norm(rotation)
    return translation_basis, rotation


def analytic_symmetry_checks(
    jacobian: Any,
    history: np.ndarray,
    candidate: RotatingWaveCandidate,
    *,
    residual_maximum: float,
) -> dict[str, float | bool]:
    """Check the exact analytic group tangents before Arnoldi execution."""

    tangents = symmetry_tangent_vectors(history)
    rotate_back = rotation_matrix(-candidate.theta)
    expected_x = np.tile(
        rotate_back @ np.asarray([1.0, 0.0]),
        (candidate.horizon, 1),
    ).ravel()
    expected_y = np.tile(
        rotate_back @ np.asarray([0.0, 1.0]),
        (candidate.horizon, 1),
    ).ravel()
    rotation_residual = float(
        np.linalg.norm(jacobian @ tangents["rotation"] - tangents["rotation"])
        / np.linalg.norm(tangents["rotation"])
    )
    translation_x_residual = float(
        np.linalg.norm(jacobian @ tangents["translation_x"] - expected_x)
        / np.linalg.norm(expected_x)
    )
    translation_y_residual = float(
        np.linalg.norm(jacobian @ tangents["translation_y"] - expected_y)
        / np.linalg.norm(expected_y)
    )
    return {
        "rotation_relative_residual": rotation_residual,
        "translation_x_relative_residual": translation_x_residual,
        "translation_y_relative_residual": translation_y_residual,
        "pass": bool(
            rotation_residual <= residual_maximum
            and translation_x_residual <= residual_maximum
            and translation_y_residual <= residual_maximum
        ),
    }


def classify_eigenpairs(
    jacobian: Any,
    eigenvalues: np.ndarray,
    eigenvectors: np.ndarray,
    history: np.ndarray,
    *,
    symmetry_overlap_minimum: float,
) -> list[dict[str, Any]]:
    """Classify returned Ritz pairs against the analytic symmetry subspace."""

    translation_basis, rotation_basis = symmetry_basis(history)
    rows: list[dict[str, Any]] = []
    for index, eigenvalue in enumerate(eigenvalues):
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
            }
        )
    rows.sort(key=lambda row: row["modulus"], reverse=True)
    return rows


def symmetry_eigenvalue_pass(
    rows: list[dict[str, Any]],
    *,
    theta: float,
    tolerance: float,
) -> bool:
    """Return whether all three analytic symmetry multipliers were recovered."""

    translations = [row for row in rows if row["classification"] == "translation"]
    rotations = [row for row in rows if row["classification"] == "rotation"]
    expected_translations = [np.exp(1j * theta), np.exp(-1j * theta)]
    translation_pass = len(translations) >= 2 and all(
        min(
            abs(complex(row["real"], row["imag"]) - expected)
            for row in translations
        )
        <= tolerance
        for expected in expected_translations
    )
    rotation_pass = any(
        abs(complex(row["real"], row["imag"]) - 1.0) <= tolerance
        for row in rotations
    )
    return bool(translation_pass and rotation_pass)


def run_eigen_panel(
    jacobian: Any,
    history: np.ndarray,
    candidate: RotatingWaveCandidate,
    panel: ArnoldiPanel,
    thresholds: StabilityThresholds,
) -> dict[str, Any]:
    """Run one frozen largest-modulus ARPACK panel."""

    exception = None
    try:
        values, vectors = eigs(
            jacobian,
            k=panel.requested,
            which="LM",
            ncv=panel.ncv,
            tol=panel.tolerance,
            maxiter=panel.max_iterations,
            v0=deterministic_arnoldi_start(jacobian.shape[0], panel.start_id),
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
    rows = classify_eigenpairs(
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
    leading = transverse[0] if transverse else None
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
        "leading_transverse": leading,
        "eigenpairs": rows,
    }


def panel_agreement(
    panels: list[dict[str, Any]],
    thresholds: StabilityThresholds,
) -> dict[str, Any]:
    """Match the primary leading transverse value in the convergence panel."""

    if len(panels) != 2:
        raise ValueError("exactly two panels are required")
    first = panels[0]["leading_transverse"]
    second_rows = [
        row for row in panels[1]["eigenpairs"] if row["classification"] == "transverse"
    ]
    if first is None or not second_rows:
        return {
            "pass": False,
            "complex_difference": None,
            "modulus_difference": None,
            "primary": first,
            "matched_convergence": None,
        }
    first_value = complex(first["real"], first["imag"])
    second = min(
        second_rows,
        key=lambda row: abs(complex(row["real"], row["imag"]) - first_value),
    )
    second_value = complex(second["real"], second["imag"])
    complex_difference = float(abs(first_value - second_value))
    modulus_difference = float(abs(first["modulus"] - second["modulus"]))
    return {
        "pass": bool(
            complex_difference <= thresholds.leading_complex_agreement
            and modulus_difference <= thresholds.leading_modulus_agreement
        ),
        "complex_difference": complex_difference,
        "modulus_difference": modulus_difference,
        "primary": first,
        "matched_convergence": second,
    }


def registered_perturbations(
    history: np.ndarray,
    *,
    scale: float,
) -> dict[str, np.ndarray]:
    """Return the exact and six mirrored preregistered perturbations."""

    if not math.isfinite(scale) or scale <= 0.0:
        raise ValueError("scale must be positive and finite")
    radial = np.zeros_like(history)
    radial[0, 0] = scale
    tangential = np.zeros_like(history)
    tangential[0, 1] = scale

    dimension = history.size
    indices = np.arange(dimension, dtype=float)
    full = np.sin(0.37 * indices) + np.cos(0.11 * indices)
    tangents = symmetry_tangent_vectors(history)
    symmetry = np.column_stack(
        (
            tangents["translation_x"],
            tangents["translation_y"],
            tangents["rotation"],
        )
    )
    symmetry_orthonormal, _ = np.linalg.qr(symmetry)
    full -= symmetry_orthonormal @ (symmetry_orthonormal.T @ full)
    full *= scale / np.linalg.norm(full)
    full = full.reshape(history.shape)
    return {
        "exact": np.zeros_like(history),
        "visible_radial_plus": radial,
        "visible_radial_minus": -radial,
        "visible_tangential_plus": tangential,
        "visible_tangential_minus": -tangential,
        "full_history_transverse_plus": full,
        "full_history_transverse_minus": -full,
    }


def run_continuation(
    name: str,
    perturbation: np.ndarray,
    history: np.ndarray,
    reference_norm: float,
    candidate: RotatingWaveCandidate,
    thresholds: StabilityThresholds,
) -> dict[str, Any]:
    """Run one frozen co-rotating perturbation continuation."""

    state = history + perturbation
    distance, phase = rotation_translation_quotient_distance(
        state,
        history,
        alpha=candidate.alpha,
        memory_mass=candidate.memory_mass,
    )
    initial_distance = distance
    maximum_distance = distance
    trace = [{"step": 0, "distance": distance, "alignment_phase": phase}]
    stop_radius = thresholds.stopping_radius_fraction * reference_norm
    stopped = False
    stop_reason = "completed"
    final_step = 0
    for step in range(1, thresholds.continuation_steps + 1):
        state = co_rotating_fifo_step(
            state,
            theta=candidate.theta,
            **candidate.step_parameters(),
        )
        distance, phase = rotation_translation_quotient_distance(
            state,
            history,
            alpha=candidate.alpha,
            memory_mass=candidate.memory_mass,
        )
        maximum_distance = max(maximum_distance, distance)
        final_step = step
        if step % thresholds.sample_every == 0:
            trace.append(
                {
                    "step": step,
                    "distance": distance,
                    "alignment_phase": phase,
                }
            )
        if not math.isfinite(distance):
            stopped = True
            stop_reason = "nonfinite-distance"
            break
        if name != "exact" and distance > stop_radius:
            stopped = True
            stop_reason = "registered-stopping-radius"
            break
    if trace[-1]["step"] != final_step:
        trace.append(
            {
                "step": final_step,
                "distance": distance,
                "alignment_phase": phase,
            }
        )
    growth_factor = (
        maximum_distance / initial_distance if initial_distance > 0.0 else None
    )
    final_ratio = distance / initial_distance if initial_distance > 0.0 else None
    return {
        "name": name,
        "initial_distance": initial_distance,
        "maximum_distance": maximum_distance,
        "final_distance": distance,
        "growth_factor": growth_factor,
        "final_ratio": final_ratio,
        "stopped": stopped,
        "stop_reason": stop_reason,
        "final_step": final_step,
        "trace": trace,
    }


def evaluate_decision(
    *,
    full_map_controls: bool,
    panels: list[dict[str, Any]],
    agreement: dict[str, Any],
    continuations: list[dict[str, Any]],
    thresholds: StabilityThresholds,
) -> tuple[str, dict[str, bool]]:
    """Apply the frozen pass, fail and inconclusive semantics."""

    expected_continuations = {
        "exact",
        "visible_radial_plus",
        "visible_radial_minus",
        "visible_tangential_plus",
        "visible_tangential_minus",
        "full_history_transverse_plus",
        "full_history_transverse_minus",
    }
    continuation_names = [row["name"] for row in continuations]
    continuation_registration_complete = bool(
        len(continuation_names) == len(expected_continuations)
        and set(continuation_names) == expected_continuations
    )
    spectral_controls = bool(
        len(panels) == 2
        and full_map_controls
        and all(panel["panel_pass"] for panel in panels)
        and agreement["pass"]
    )
    transverse_rows = [
        row
        for panel in panels
        for row in panel["eigenpairs"]
        if row["classification"] == "transverse"
    ]
    nonzero_rows = [row for row in continuations if row["name"] != "exact"]
    matched_rows = (
        agreement.get("primary"),
        agreement.get("matched_convergence"),
    )
    unstable_spectrum = bool(
        all(row is not None for row in matched_rows)
        and all(
            row["modulus"] > thresholds.unstable_modulus
            for row in matched_rows
            if row is not None
        )
    )
    perturbation_growth = any(
        row["growth_factor"] is not None
        and row["growth_factor"] >= thresholds.unstable_growth_minimum
        for row in nonzero_rows
    )
    stable_spectrum = bool(
        transverse_rows
        and all(
            row["modulus"] < thresholds.stable_modulus for row in transverse_rows
        )
    )
    perturbation_contraction = bool(
        nonzero_rows
        and all(
            not row["stopped"]
            and row["growth_factor"] is not None
            and row["growth_factor"]
            <= thresholds.stable_transient_growth_maximum
            and row["final_ratio"] is not None
            and row["final_ratio"] <= thresholds.stable_final_ratio_maximum
            for row in nonzero_rows
        )
    )
    exact_rows = [row for row in continuations if row["name"] == "exact"]
    exact_control_pass = bool(
        continuation_registration_complete
        and len(exact_rows) == 1
        and not exact_rows[0]["stopped"]
        and exact_rows[0]["final_step"] == thresholds.continuation_steps
        and math.isfinite(exact_rows[0]["maximum_distance"])
        and exact_rows[0]["maximum_distance"]
        <= thresholds.exact_control_distance_maximum
    )
    if (
        spectral_controls
        and continuation_registration_complete
        and unstable_spectrum
        and perturbation_growth
    ):
        decision = "unstable-source-fail"
    elif (
        spectral_controls
        and continuation_registration_complete
        and stable_spectrum
        and perturbation_contraction
        and exact_control_pass
    ):
        decision = "numerically-stable-source-pass"
    else:
        decision = "source-stability-inconclusive"
    return decision, {
        "spectral_controls": spectral_controls,
        "continuation_registration_complete": continuation_registration_complete,
        "unstable_spectrum": unstable_spectrum,
        "registered_perturbation_growth": perturbation_growth,
        "stable_spectrum": stable_spectrum,
        "registered_perturbation_contraction": perturbation_contraction,
        "exact_control_pass": exact_control_pass,
    }


def spectral_diagnostics(
    panels: list[dict[str, Any]],
    *,
    alpha: float,
    anchor_modulus: float,
    anchor_alpha: float,
) -> dict[str, Any]:
    """Return preregistered non-decision spectral diagnostics."""

    rows = []
    for panel in panels:
        leading = panel["leading_transverse"]
        if leading is None:
            rows.append(
                {
                    "panel": panel["registration"]["name"],
                    "decay_rate_per_memory_time": None,
                    "conjugacy_error": None,
                }
            )
            continue
        value = complex(leading["real"], leading["imag"])
        conjugate_error = min(
            abs(complex(row["real"], row["imag"]) - value.conjugate())
            for row in panel["eigenpairs"]
        )
        rows.append(
            {
                "panel": panel["registration"]["name"],
                "decay_rate_per_memory_time": float(
                    -math.log(leading["modulus"]) / alpha
                ),
                "conjugacy_error": float(conjugate_error),
            }
        )
    return {
        "panels": rows,
        "anchor_modulus": anchor_modulus,
        "anchor_alpha": anchor_alpha,
        "anchor_decay_rate_per_memory_time": float(
            -math.log(anchor_modulus) / anchor_alpha
        ),
    }


def mirrored_diagnostics(
    continuations: list[dict[str, Any]],
) -> list[dict[str, float | str]]:
    """Compare the three preregistered mirrored perturbation pairs."""

    by_name = {row["name"]: row for row in continuations}
    pairs = (
        ("visible_radial", "visible_radial_plus", "visible_radial_minus"),
        (
            "visible_tangential",
            "visible_tangential_plus",
            "visible_tangential_minus",
        ),
        (
            "full_history_transverse",
            "full_history_transverse_plus",
            "full_history_transverse_minus",
        ),
    )
    result: list[dict[str, float | str]] = []
    for label, plus_name, minus_name in pairs:
        plus = by_name[plus_name]
        minus = by_name[minus_name]
        maximum_scale = max(
            plus["maximum_distance"],
            minus["maximum_distance"],
            np.finfo(float).tiny,
        )
        final_scale = max(
            plus["final_distance"],
            minus["final_distance"],
            np.finfo(float).tiny,
        )
        result.append(
            {
                "pair": label,
                "initial_absolute_difference": float(
                    abs(plus["initial_distance"] - minus["initial_distance"])
                ),
                "maximum_relative_difference": float(
                    abs(plus["maximum_distance"] - minus["maximum_distance"])
                    / maximum_scale
                ),
                "final_relative_difference": float(
                    abs(plus["final_distance"] - minus["final_distance"])
                    / final_scale
                ),
            }
        )
    return result
