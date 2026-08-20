"""Evaluate the preregistered full-FIFO rotating-wave source-stability gate."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import math
from pathlib import Path
import subprocess
from typing import Any

import numpy as np
from scipy.sparse.linalg import ArpackNoConvergence, eigs

from emergenz_knoten.rotating_wave_stability import (
    circular_history,
    co_rotating_fifo_jacobian,
    co_rotating_fifo_step,
    rotation_matrix,
    rotation_translation_quotient_distance,
    symmetry_tangent_vectors,
    translation_reduced_norm,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_stability_protocol_2026-08-20.md"
)
P0_AUDIT = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_p0_audit_2026-08-20.json"
)
D0_CONTRACT = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_d0_contract_2026-08-20.md"
)
DEFAULT_REPORT = Path(
    "reports/dynamics/rotation/scalar_memory_rotating_wave_stability_2026-08-20.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/scalar_memory_rotating_wave_stability_2026-08-20.json"
)

CANDIDATE_ID = "k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1"
RADIUS = 0.946517504804225
THETA = 0.015770381717135
ALPHA = 0.01
HORIZON = 1200
MEMORY_MASS = 1.0
ETA = 0.15
SIGMA_REP = 1.0
SIGMA_ATT = 3.0
AMPLITUDE_REP = 1.0
AMPLITUDE_ATT = 3.5

EIGEN_PANELS = (
    {
        "name": "primary",
        "requested": 24,
        "ncv": 96,
        "tolerance": 1.0e-10,
        "max_iterations": 20_000,
    },
    {
        "name": "convergence",
        "requested": 36,
        "ncv": 144,
        "tolerance": 1.0e-12,
        "max_iterations": 40_000,
    },
)
EIGEN_RESIDUAL_TOLERANCE = 1.0e-8
SYMMETRY_OVERLAP_MINIMUM = 0.99
SYMMETRY_EIGENVALUE_TOLERANCE = 1.0e-7
LEADING_EIGENVALUE_AGREEMENT = 1.0e-5
LEADING_MODULUS_AGREEMENT = 1.0e-6
UNSTABLE_MODULUS_THRESHOLD = 1.0 + 1.0e-6
STABLE_MODULUS_THRESHOLD = 1.0 - 1.0e-4

PERTURBATION_SCALE = 1.0e-7 * RADIUS
CONTINUATION_STEPS = 5000
SAMPLE_EVERY = 10
STOPPING_RADIUS_FRACTION = 0.25
GROWTH_FACTOR_MINIMUM = 100.0
CONTRACTION_FACTOR_MAXIMUM = 0.1
EXACT_CONTROL_DISTANCE_MAXIMUM = 1.0e-10


def _git_output(arguments: list[str]) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return result.stdout.strip()


def _step_parameters() -> dict[str, float]:
    return {
        "alpha": ALPHA,
        "memory_mass": MEMORY_MASS,
        "eta": ETA,
        "sigma_rep": SIGMA_REP,
        "sigma_att": SIGMA_ATT,
        "amplitude_rep": AMPLITUDE_REP,
        "amplitude_att": AMPLITUDE_ATT,
    }


def _symmetry_basis(history: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    tangents = symmetry_tangent_vectors(history)
    translation = np.column_stack(
        (tangents["translation_x"], tangents["translation_y"])
    )
    translation_basis, _ = np.linalg.qr(translation)
    rotation = tangents["rotation"].copy()
    rotation -= translation_basis @ (translation_basis.T @ rotation)
    rotation /= np.linalg.norm(rotation)
    return translation_basis, rotation


def _analytic_symmetry_checks(jacobian, history: np.ndarray) -> dict[str, float | bool]:
    tangents = symmetry_tangent_vectors(history)
    rotate_back = rotation_matrix(-THETA)
    expected_x = np.tile(rotate_back @ np.asarray([1.0, 0.0]), (HORIZON, 1)).ravel()
    expected_y = np.tile(rotate_back @ np.asarray([0.0, 1.0]), (HORIZON, 1)).ravel()
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
            rotation_residual <= 1.0e-10
            and translation_x_residual <= 1.0e-10
            and translation_y_residual <= 1.0e-10
        ),
    }


def _deterministic_arnoldi_start(dimension: int) -> np.ndarray:
    indices = np.arange(dimension, dtype=float)
    values = np.sin(math.sqrt(2.0) * (indices + 1.0))
    values += np.cos(math.sqrt(3.0) * (indices + 0.5))
    return values / np.linalg.norm(values)


def _classify_eigenpairs(
    jacobian,
    eigenvalues: np.ndarray,
    eigenvectors: np.ndarray,
    history: np.ndarray,
) -> list[dict[str, Any]]:
    translation_basis, rotation_basis = _symmetry_basis(history)
    rows = []
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
        if translation_overlap >= SYMMETRY_OVERLAP_MINIMUM:
            label = "translation"
        elif rotation_overlap >= SYMMETRY_OVERLAP_MINIMUM:
            label = "rotation"
        else:
            label = "transverse"
        rows.append(
            {
                "real": float(eigenvalue.real),
                "imag": float(eigenvalue.imag),
                "modulus": float(abs(eigenvalue)),
                "normalized_residual": residual,
                "translation_overlap": translation_overlap,
                "rotation_overlap": rotation_overlap,
                "classification": label,
            }
        )
    rows.sort(key=lambda row: row["modulus"], reverse=True)
    return rows


def _symmetry_eigenvalue_pass(rows: list[dict[str, Any]]) -> bool:
    translations = [row for row in rows if row["classification"] == "translation"]
    rotations = [row for row in rows if row["classification"] == "rotation"]
    expected_translations = [np.exp(1j * THETA), np.exp(-1j * THETA)]
    translation_pass = len(translations) >= 2 and all(
        min(abs(complex(row["real"], row["imag"]) - expected) for row in translations)
        <= SYMMETRY_EIGENVALUE_TOLERANCE
        for expected in expected_translations
    )
    rotation_pass = any(
        abs(complex(row["real"], row["imag"]) - 1.0) <= SYMMETRY_EIGENVALUE_TOLERANCE
        for row in rotations
    )
    return bool(translation_pass and rotation_pass)


def _run_eigen_panel(
    jacobian,
    history: np.ndarray,
    registration: dict[str, Any],
) -> dict[str, Any]:
    exception = None
    try:
        values, vectors = eigs(
            jacobian,
            k=registration["requested"],
            which="LM",
            ncv=registration["ncv"],
            tol=registration["tolerance"],
            maxiter=registration["max_iterations"],
            v0=_deterministic_arnoldi_start(jacobian.shape[0]),
        )
        arpack_converged = True
    except ArpackNoConvergence as error:
        values = np.asarray(error.eigenvalues)
        vectors = np.asarray(error.eigenvectors)
        exception = str(error)
        arpack_converged = False
    rows = _classify_eigenpairs(jacobian, values, vectors, history)
    residual_pass = bool(
        len(rows) == registration["requested"]
        and all(row["normalized_residual"] <= EIGEN_RESIDUAL_TOLERANCE for row in rows)
    )
    symmetry_pass = _symmetry_eigenvalue_pass(rows)
    transverse = [row for row in rows if row["classification"] == "transverse"]
    leading = transverse[0] if transverse else None
    return {
        "registration": registration,
        "arpack_converged": arpack_converged,
        "exception": exception,
        "returned_eigenpairs": len(rows),
        "residual_pass": residual_pass,
        "symmetry_eigenvalue_pass": symmetry_pass,
        "panel_pass": bool(arpack_converged and residual_pass and symmetry_pass),
        "leading_transverse": leading,
        "eigenpairs": rows,
    }


def _panel_agreement(panels: list[dict[str, Any]]) -> dict[str, Any]:
    first = panels[0]["leading_transverse"]
    second_rows = [
        row for row in panels[1]["eigenpairs"] if row["classification"] == "transverse"
    ]
    if first is None or not second_rows:
        return {
            "pass": False,
            "complex_difference": None,
            "modulus_difference": None,
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
            complex_difference <= LEADING_EIGENVALUE_AGREEMENT
            and modulus_difference <= LEADING_MODULUS_AGREEMENT
        ),
        "complex_difference": complex_difference,
        "modulus_difference": modulus_difference,
        "primary": first,
        "matched_convergence": second,
    }


def _perturbations(history: np.ndarray) -> dict[str, np.ndarray]:
    radial = np.zeros_like(history)
    radial[0, 0] = PERTURBATION_SCALE
    tangential = np.zeros_like(history)
    tangential[0, 1] = PERTURBATION_SCALE

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
    symmetry_basis, _ = np.linalg.qr(symmetry)
    full -= symmetry_basis @ (symmetry_basis.T @ full)
    full *= PERTURBATION_SCALE / np.linalg.norm(full)
    return {
        "exact": np.zeros_like(history),
        "visible_radial": radial,
        "visible_tangential": tangential,
        "full_history_transverse": full.reshape(history.shape),
    }


def _run_continuation(
    name: str,
    perturbation: np.ndarray,
    history: np.ndarray,
    reference_norm: float,
) -> dict[str, Any]:
    state = history + perturbation
    distance, phase = rotation_translation_quotient_distance(
        state,
        history,
        alpha=ALPHA,
        memory_mass=MEMORY_MASS,
    )
    initial_distance = distance
    maximum_distance = distance
    trace = [{"step": 0, "distance": distance, "alignment_phase": phase}]
    stop_radius = STOPPING_RADIUS_FRACTION * reference_norm
    stopped = False
    stop_reason = "completed"
    final_step = 0
    for step in range(1, CONTINUATION_STEPS + 1):
        state = co_rotating_fifo_step(
            state,
            theta=THETA,
            **_step_parameters(),
        )
        distance, phase = rotation_translation_quotient_distance(
            state,
            history,
            alpha=ALPHA,
            memory_mass=MEMORY_MASS,
        )
        maximum_distance = max(maximum_distance, distance)
        final_step = step
        if step % SAMPLE_EVERY == 0:
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


def run_gate() -> dict[str, Any]:
    start_status = _git_output(["status", "--short"])
    if start_status:
        raise RuntimeError("stability gate requires a clean prospective revision")
    revision = _git_output(["rev-parse", "HEAD"])
    p0 = json.loads((ROOT / P0_AUDIT).read_text(encoding="utf-8"))
    if p0["decision"] != "pass" or p0["issue_count"] != 0:
        raise RuntimeError("rotating-wave P0 must pass before stability")

    history = circular_history(
        radius=RADIUS,
        theta=THETA,
        horizon=HORIZON,
    )
    fixed_update = co_rotating_fifo_step(
        history,
        theta=THETA,
        **_step_parameters(),
    )
    fixed_error = float(np.max(np.abs(fixed_update - history)))
    jacobian = co_rotating_fifo_jacobian(
        history,
        theta=THETA,
        **_step_parameters(),
    )
    symmetry_checks = _analytic_symmetry_checks(jacobian, history)
    panels = [
        _run_eigen_panel(jacobian, history, registration)
        for registration in EIGEN_PANELS
    ]
    agreement = _panel_agreement(panels)

    reference_norm = translation_reduced_norm(
        history,
        alpha=ALPHA,
        memory_mass=MEMORY_MASS,
    )
    continuations = [
        _run_continuation(name, perturbation, history, reference_norm)
        for name, perturbation in _perturbations(history).items()
    ]

    spectral_controls = bool(
        fixed_error <= 4.0e-15
        and symmetry_checks["pass"]
        and all(panel["panel_pass"] for panel in panels)
        and agreement["pass"]
    )
    leading_moduli = [
        panel["leading_transverse"]["modulus"]
        for panel in panels
        if panel["leading_transverse"] is not None
    ]
    perturbation_rows = [row for row in continuations if row["name"] != "exact"]
    unstable_spectrum = bool(
        len(leading_moduli) == len(EIGEN_PANELS)
        and all(modulus > UNSTABLE_MODULUS_THRESHOLD for modulus in leading_moduli)
    )
    perturbation_growth = any(
        row["growth_factor"] is not None
        and row["growth_factor"] >= GROWTH_FACTOR_MINIMUM
        for row in perturbation_rows
    )
    stable_spectrum = bool(
        len(leading_moduli) == len(EIGEN_PANELS)
        and all(modulus < STABLE_MODULUS_THRESHOLD for modulus in leading_moduli)
    )
    perturbation_contraction = all(
        not row["stopped"]
        and row["final_ratio"] is not None
        and row["final_ratio"] <= CONTRACTION_FACTOR_MAXIMUM
        for row in perturbation_rows
    )
    exact_row = next(row for row in continuations if row["name"] == "exact")
    exact_control_pass = bool(
        exact_row["maximum_distance"] <= EXACT_CONTROL_DISTANCE_MAXIMUM
    )

    if spectral_controls and unstable_spectrum and perturbation_growth:
        decision = "unstable-source-fail"
    elif (
        spectral_controls
        and stable_spectrum
        and perturbation_contraction
        and exact_control_pass
    ):
        decision = "numerically-stable-source-pass"
    else:
        decision = "source-stability-inconclusive"

    return {
        "schema": "emergenz-knoten.scalar-memory-rotating-wave-stability",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "execution_revision": revision,
        "git_status_at_start": start_status,
        "candidate_id": CANDIDATE_ID,
        "protocol": PROTOCOL.as_posix(),
        "p0_audit": P0_AUDIT.as_posix(),
        "d0_contract": D0_CONTRACT.as_posix(),
        "candidate": {
            "radius": RADIUS,
            "theta": THETA,
            "alpha": ALPHA,
            "horizon": HORIZON,
            "memory_mass": MEMORY_MASS,
            "eta": ETA,
            "sigma_rep": SIGMA_REP,
            "sigma_att": SIGMA_ATT,
            "amplitude_rep": AMPLITUDE_REP,
            "amplitude_att": AMPLITUDE_ATT,
            "epsilon": 0.0,
        },
        "registration": {
            "eigen_panels": EIGEN_PANELS,
            "perturbation_scale": PERTURBATION_SCALE,
            "continuation_steps": CONTINUATION_STEPS,
            "sample_every": SAMPLE_EVERY,
            "stopping_radius_fraction": STOPPING_RADIUS_FRACTION,
            "sealed_amplitude_holdout": 7.0,
            "topology_opened": False,
            "noise_opened": False,
        },
        "fixed_point_max_component_error": fixed_error,
        "jacobian_shape": list(jacobian.shape),
        "jacobian_nonzero_entries": int(jacobian.nnz),
        "analytic_symmetry_checks": symmetry_checks,
        "spectral_panels": panels,
        "panel_agreement": agreement,
        "reference_d0_norm": reference_norm,
        "continuations": continuations,
        "gates": {
            "spectral_controls": spectral_controls,
            "unstable_spectrum": unstable_spectrum,
            "registered_perturbation_growth": perturbation_growth,
            "stable_spectrum": stable_spectrum,
            "registered_perturbation_contraction": perturbation_contraction,
            "exact_control_pass": exact_control_pass,
        },
        "decision": decision,
        "claim_boundary": {
            "established_if_unstable": (
                "the prepared residual root is transversely unstable under "
                "the registered full-FIFO numerical tests"
            ),
            "established_if_stable": (
                "numerical transverse stability in the registered spectral "
                "and perturbation panels, pending a complete spectral enclosure"
            ),
            "not_established": (
                "internal S1 after SO(2) quotient, stochastic robustness, "
                "external phase coupling, physical work, or mass"
            ),
        },
    }


def _fmt(value: Any) -> str:
    if value is None:
        return "--"
    return f"{float(value):.9g}"


def render_report(payload: dict[str, Any]) -> str:
    lines = [
        "# Scalar-memory rotating-wave source stability",
        "",
        f"Generated: {payload['generated_utc']}.",
        "",
        f"Decision: **{payload['decision']}**.",
        "",
        "The candidate was evaluated from clean revision",
        f"{payload['execution_revision']} after a zero-defect P0 and frozen D0",
        "contract. No topology, noise or parameter holdout was opened.",
        "",
        "## Full-map controls",
        "",
        f"- Jacobian shape: {payload['jacobian_shape']}",
        f"- Sparse nonzeros: {payload['jacobian_nonzero_entries']}",
        f"- Fixed-point max error: {_fmt(payload['fixed_point_max_component_error'])}",
        f"- Analytic symmetry pass: {payload['analytic_symmetry_checks']['pass']}",
        "",
        "## Leading transverse multipliers",
        "",
        "| panel | lambda | modulus | residual | panel pass |",
        "| --- | ---: | ---: | ---: | :---: |",
    ]
    for panel in payload["spectral_panels"]:
        leading = panel["leading_transverse"]
        value = (
            f"{_fmt(leading['real'])} {leading['imag']:+.9g}i"
            if leading is not None
            else "--"
        )
        lines.append(
            "| "
            f"{panel['registration']['name']} | {value} | "
            f"{_fmt(leading['modulus'] if leading else None)} | "
            f"{_fmt(leading['normalized_residual'] if leading else None)} | "
            f"{panel['panel_pass']} |"
        )
    lines.extend(
        [
            "",
            "## Registered perturbations",
            "",
            "| perturbation | initial distance | max distance | final distance | growth | final/initial | stop |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in payload["continuations"]:
        lines.append(
            "| "
            f"{row['name']} | {_fmt(row['initial_distance'])} | "
            f"{_fmt(row['maximum_distance'])} | "
            f"{_fmt(row['final_distance'])} | "
            f"{_fmt(row['growth_factor'])} | "
            f"{_fmt(row['final_ratio'])} | {row['stop_reason']} |"
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This gate concerns only transverse stability of a prepared spatial",
            "rotating relative equilibrium. It does not establish an internal",
            "phase after quotienting ambient rotation, topology from data,",
            "noise robustness, physical work or mass.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = run_gate()
    report_path = ROOT / args.report
    summary_path = ROOT / args.summary
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(payload), encoding="utf-8")
    summary_path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Decision: {payload['decision']}")
    print(f"Report: {report_path.relative_to(ROOT)}")
    print(f"Summary: {summary_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
