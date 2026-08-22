"""Evaluate the frozen P1 L3 non-Anchor rotating-wave stability gate."""

from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime
import json
from pathlib import Path
import platform
import subprocess
import time
from typing import Any

import numpy as np
import scipy

from emergenz_knoten.kernels import (
    double_gaussian_gradient,
    exponential_memory_weights,
)
from emergenz_knoten.rotating_wave_stability import (
    circular_history,
    co_rotating_fifo_jacobian,
    co_rotating_fifo_step,
    native_fifo_step,
    rotation_matrix,
    rotation_translation_quotient_distance,
    translation_reduced_norm,
)
from emergenz_knoten.rotating_wave_stability_gate import (
    ArnoldiPanel,
    RotatingWaveCandidate,
    StabilityThresholds,
    analytic_symmetry_checks,
    evaluate_decision,
    mirrored_diagnostics,
    panel_agreement,
    registered_perturbations,
    run_continuation,
    run_eigen_panel,
    spectral_diagnostics,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_l3_stability_protocol_2026-08-22.md"
)
LADDER = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_refinement_ladder_2026-08-21.json"
)
FOUNDATION = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_foundation_audit_2026-08-21.json"
)
ANCHOR_STABILITY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_stability_2026-08-20.json"
)
DEFAULT_REPORT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_l3_stability_2026-08-22.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_l3_stability_2026-08-22.json"
)

FREEZE_REVISION = "d10d5321754a67a0672f6fdda78f5b55a2527d44"
PROTOCOL_BLOB = "548ff395b21e16c894bc11e536023f19c0cc64cd"
EXPECTED_BLOBS = {
    LADDER.as_posix(): "66e8681c2b2e9aa7309a48acba15bb8dc33143f5",
    FOUNDATION.as_posix(): "622c06c3d9c2ad24819e39daf5c9bd86f90c515a",
    ANCHOR_STABILITY.as_posix(): "1c9d5746c9553d9cb8031b58258e6d613f1633d9",
    "src/emergenz_knoten/rotating_wave_stability.py": (
        "9defb5a6876371202e1ba57cea030c997b9c6edd"
    ),
    "src/emergenz_knoten/rotating_wave.py": (
        "3b70f408ab8bb24e7cc6df4b9c61f54f17a65a4d"
    ),
}

CANDIDATE_ID = "k0h-rw-l3-aatt3p5-alpha0p005-h2400-eta0p075-v1"
RADIUS_DECIMAL = (
    "0.944805811705743656419366118422595657454474452804188781825799206245348"
    "464567689511866917417017911971955244464"
)
THETA_DECIMAL = (
    "0.007906661462435523749384967030309742461978034595274092598156965831417"
    "08245813094145986593003659167675765833059"
)

CANDIDATE = RotatingWaveCandidate(
    candidate_id=CANDIDATE_ID,
    radius=float(RADIUS_DECIMAL),
    theta=float(THETA_DECIMAL),
    alpha=0.005,
    horizon=2400,
    memory_mass=1.0,
    eta=0.075,
    sigma_rep=1.0,
    sigma_att=3.0,
    amplitude_rep=1.0,
    amplitude_att=3.5,
)

PANELS = (
    ArnoldiPanel(
        name="primary",
        requested=32,
        ncv=128,
        tolerance=1.0e-10,
        max_iterations=40_000,
        start_id="S1",
    ),
    ArnoldiPanel(
        name="convergence",
        requested=48,
        ncv=192,
        tolerance=1.0e-12,
        max_iterations=80_000,
        start_id="S2",
    ),
)

THRESHOLDS = StabilityThresholds(
    eigen_residual=1.0e-8,
    symmetry_overlap=0.99,
    symmetry_eigenvalue=1.0e-7,
    leading_complex_agreement=1.0e-5,
    leading_modulus_agreement=1.0e-6,
    unstable_modulus=1.0 + 1.0e-6,
    stable_modulus=1.0 - 1.0e-4,
    perturbation_scale_fraction=1.0e-7,
    continuation_steps=10_000,
    sample_every=20,
    stopping_radius_fraction=0.25,
    unstable_growth_minimum=100.0,
    stable_transient_growth_maximum=10.0,
    stable_final_ratio_maximum=0.1,
    exact_control_distance_maximum=1.0e-10,
)

FIXED_POINT_ERROR_MAXIMUM = 1.0e-14
SYMMETRY_RESIDUAL_MAXIMUM = 1.0e-10
EXPECTED_JACOBIAN_SHAPE = (4800, 4800)
EXPECTED_JACOBIAN_NONZEROS = 19_196


def _git_output(arguments: list[str]) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return result.stdout.strip()


def _git_blob(path: str) -> str:
    return _git_output(["rev-parse", f"HEAD:{path}"])


def _verify_provenance() -> dict[str, Any]:
    status = _git_output(["status", "--short"])
    if status:
        raise RuntimeError("L3 stability gate requires a clean prospective revision")
    revision = _git_output(["rev-parse", "HEAD"])
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", FREEZE_REVISION, revision],
        cwd=ROOT,
        check=False,
    ).returncode == 0
    if not ancestor:
        raise RuntimeError("protocol freeze revision is not an ancestor")
    protocol_addition = _git_output(
        ["log", "-1", "--format=%H", "--diff-filter=A", "--", PROTOCOL.as_posix()]
    )
    current_protocol_blob = _git_blob(PROTOCOL.as_posix())
    blob_rows = {}
    for path, expected in EXPECTED_BLOBS.items():
        observed = _git_blob(path)
        blob_rows[path] = {
            "expected": expected,
            "observed": observed,
            "pass": observed == expected,
        }
    protocol_pass = bool(
        protocol_addition == FREEZE_REVISION
        and current_protocol_blob == PROTOCOL_BLOB
    )
    if not protocol_pass or not all(row["pass"] for row in blob_rows.values()):
        raise RuntimeError("frozen protocol or dependency blob mismatch")
    return {
        "execution_revision": revision,
        "git_status_at_start": status,
        "freeze_revision": FREEZE_REVISION,
        "freeze_is_ancestor": ancestor,
        "protocol_addition_revision": protocol_addition,
        "protocol_blob": {
            "expected": PROTOCOL_BLOB,
            "observed": current_protocol_blob,
            "pass": protocol_pass,
        },
        "dependency_blobs": blob_rows,
        "pass": True,
    }


def _load_frozen_inputs() -> tuple[dict[str, Any], float, float]:
    ladder = json.loads((ROOT / LADDER).read_text(encoding="utf-8"))
    cells = [cell for cell in ladder["cells"] if cell["cell"] == "L3"]
    if len(cells) != 1:
        raise RuntimeError("refinement ladder must contain exactly one L3 cell")
    cell = cells[0]
    panels = sorted(cell["panels"], key=lambda row: int(row["precision_dps"]))
    if (
        not cell["pass"]
        or [int(row["precision_dps"]) for row in panels] != [80, 120]
        or not all(row["pass"] for row in panels)
        or cell["alpha"] != "0.005"
        or int(cell["horizon"]) != 2400
        or cell["eta"] != "0.075"
    ):
        raise RuntimeError("frozen L3 interval dependency does not pass")
    certified = panels[-1]["refined"]
    if (
        certified["radius"] != RADIUS_DECIMAL
        or certified["theta"] != THETA_DECIMAL
    ):
        raise RuntimeError("frozen L3 root does not match the registered center")

    foundation = json.loads((ROOT / FOUNDATION).read_text(encoding="utf-8"))
    replay_rows = [
        row for row in foundation["finite_ladder_replay"]["rows"] if row["cell"] == "L3"
    ]
    if (
        len(replay_rows) != 1
        or not replay_rows[0]["pass"]
        or not foundation["finite_ladder_replay"]["pass"]
        or not all(foundation["gates"].values())
        or not foundation["decision"].endswith("-pass-scoped")
    ):
        raise RuntimeError("foundation replay does not validate L3")

    anchor = json.loads((ROOT / ANCHOR_STABILITY).read_text(encoding="utf-8"))
    if anchor["decision"] != "numerically-stable-source-pass":
        raise RuntimeError("frozen Anchor stability dependency does not pass")
    anchor_modulus = float(
        anchor["spectral_panels"][0]["leading_transverse"]["modulus"]
    )
    anchor_alpha = float(anchor["candidate"]["alpha"])
    return {
        "ladder_decision": ladder["decision"],
        "l3_interval_panels": [
            {
                "precision_dps": int(row["precision_dps"]),
                "pass": bool(row["pass"]),
                "point_residual_maximum": row["point_residual_maximum"],
            }
            for row in panels
        ],
        "l3_foundation_replay": replay_rows[0],
        "foundation_decision": foundation["decision"],
        "anchor_decision": anchor["decision"],
    }, anchor_modulus, anchor_alpha


def _finite_difference_control() -> dict[str, float | bool]:
    horizon = 17
    history = circular_history(radius=1.1, theta=0.13, horizon=horizon)
    parameters = {
        "alpha": 0.07,
        "memory_mass": 1.2,
        "eta": 0.18,
        "sigma_rep": 1.0,
        "sigma_att": 3.0,
        "amplitude_rep": 1.0,
        "amplitude_att": 4.5,
    }
    jacobian = co_rotating_fifo_jacobian(
        history,
        theta=0.13,
        **parameters,
    )
    direction = np.random.default_rng(20260820).normal(size=history.shape)
    direction /= np.linalg.norm(direction)
    step = 2.0e-6
    upper = co_rotating_fifo_step(
        history + step * direction,
        theta=0.13,
        **parameters,
    )
    lower = co_rotating_fifo_step(
        history - step * direction,
        theta=0.13,
        **parameters,
    )
    finite_difference = ((upper - lower) / (2.0 * step)).ravel()
    analytic = jacobian @ direction.ravel()
    difference = analytic - finite_difference
    relative_error = float(
        np.linalg.norm(difference) / np.linalg.norm(finite_difference)
    )
    maximum_absolute_error = float(np.max(np.abs(difference)))
    return {
        "relative_error": relative_error,
        "maximum_absolute_error": maximum_absolute_error,
        "pass": bool(relative_error <= 2.0e-9),
    }


def _production_kernel_control() -> dict[str, float | bool]:
    history = np.random.default_rng(20260820).normal(size=(29, 2))
    parameters = {
        "alpha": 0.04,
        "memory_mass": 1.3,
        "eta": 0.17,
        "sigma_rep": 1.0,
        "sigma_att": 3.0,
        "amplitude_rep": 1.0,
        "amplitude_att": 3.5,
    }
    weights = exponential_memory_weights(
        parameters["alpha"],
        history.shape[0],
        memory_mass=parameters["memory_mass"],
    )
    gradient = double_gaussian_gradient(
        history[0],
        history,
        weights,
        sigma_rep=parameters["sigma_rep"],
        sigma_att=parameters["sigma_att"],
        amplitude_rep=parameters["amplitude_rep"],
        amplitude_att=parameters["amplitude_att"],
        deposition_kernel="delta",
        deposition_sigma=0.0,
    )
    expected = np.empty_like(history)
    expected[0] = history[0] - parameters["eta"] * gradient
    expected[1:] = history[:-1]
    actual = native_fifo_step(history, **parameters)
    difference = actual - expected
    maximum_absolute_error = float(np.max(np.abs(difference)))
    relative_error = float(
        np.linalg.norm(difference) / max(np.linalg.norm(expected), np.finfo(float).tiny)
    )
    return {
        "maximum_absolute_error": maximum_absolute_error,
        "relative_error": relative_error,
        "pass": bool(
            np.allclose(actual, expected, rtol=2.0e-15, atol=2.0e-15)
        ),
    }


def _d0_control() -> dict[str, float | bool]:
    reference = circular_history(radius=1.4, theta=0.09, horizon=80)
    moved = reference @ rotation_matrix(0.73).T + np.asarray([4.0, -2.0])
    distance, alignment = rotation_translation_quotient_distance(
        moved,
        reference,
        alpha=0.04,
        memory_mass=1.0,
    )
    return {
        "distance": distance,
        "alignment_error": float(abs(alignment + 0.73)),
        "pass": bool(distance < 4.0e-15 and abs(alignment + 0.73) < 2.0e-15),
    }


def _implementation_controls() -> dict[str, Any]:
    finite_difference = _finite_difference_control()
    production_kernel = _production_kernel_control()
    d0 = _d0_control()
    return {
        "finite_difference": finite_difference,
        "production_kernel": production_kernel,
        "d0_quotient": d0,
        "pass": bool(
            finite_difference["pass"]
            and production_kernel["pass"]
            and d0["pass"]
        ),
    }


def _base_payload(
    *,
    provenance: dict[str, Any],
    input_checks: dict[str, Any],
    implementation_controls: dict[str, Any],
    started: float,
) -> dict[str, Any]:
    return {
        "schema": "emergenz-knoten.scalar-memory-rotating-wave-l3-stability",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": float(time.monotonic() - started),
        "candidate_id": CANDIDATE_ID,
        "protocol": PROTOCOL.as_posix(),
        "provenance": provenance,
        "input_checks": input_checks,
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "candidate": {
            **asdict(CANDIDATE),
            "radius_decimal": RADIUS_DECIMAL,
            "theta_decimal": THETA_DECIMAL,
            "epsilon": 0.0,
            "deposition_kernel": "delta",
        },
        "registration": {
            "arnoldi_panels": [asdict(panel) for panel in PANELS],
            "thresholds": asdict(THRESHOLDS),
            "fixed_point_error_maximum": FIXED_POINT_ERROR_MAXIMUM,
            "symmetry_residual_maximum": SYMMETRY_RESIDUAL_MAXIMUM,
            "expected_jacobian_shape": list(EXPECTED_JACOBIAN_SHAPE),
            "expected_jacobian_nonzero_entries": EXPECTED_JACOBIAN_NONZEROS,
            "sealed_amplitude_holdout": 7.0,
            "topology_opened": False,
            "noise_opened": False,
            "loop_center_gate_opened": False,
        },
        "implementation_controls": implementation_controls,
    }


def run_gate() -> dict[str, Any]:
    """Execute the frozen controls, spectrum and nonlinear continuations."""

    started = time.monotonic()
    provenance = _verify_provenance()
    input_checks, anchor_modulus, anchor_alpha = _load_frozen_inputs()
    implementation_controls = _implementation_controls()
    history = circular_history(
        radius=CANDIDATE.radius,
        theta=CANDIDATE.theta,
        horizon=CANDIDATE.horizon,
    )
    fixed_update = co_rotating_fifo_step(
        history,
        theta=CANDIDATE.theta,
        **CANDIDATE.step_parameters(),
    )
    fixed_error = float(np.max(np.abs(fixed_update - history)))
    jacobian = co_rotating_fifo_jacobian(
        history,
        theta=CANDIDATE.theta,
        **CANDIDATE.step_parameters(),
    )
    symmetry_checks = analytic_symmetry_checks(
        jacobian,
        history,
        CANDIDATE,
        residual_maximum=SYMMETRY_RESIDUAL_MAXIMUM,
    )
    full_map_controls = bool(
        implementation_controls["pass"]
        and fixed_error <= FIXED_POINT_ERROR_MAXIMUM
        and jacobian.shape == EXPECTED_JACOBIAN_SHAPE
        and jacobian.nnz == EXPECTED_JACOBIAN_NONZEROS
        and symmetry_checks["pass"]
    )
    payload = _base_payload(
        provenance=provenance,
        input_checks=input_checks,
        implementation_controls=implementation_controls,
        started=started,
    )
    payload.update(
        {
            "fixed_point_max_component_error": fixed_error,
            "jacobian_shape": list(jacobian.shape),
            "jacobian_nonzero_entries": int(jacobian.nnz),
            "analytic_symmetry_checks": symmetry_checks,
            "full_map_controls": full_map_controls,
        }
    )
    if not full_map_controls:
        payload.update(
            {
                "spectral_panels": [],
                "panel_agreement": None,
                "continuations": [],
                "spectral_diagnostics": None,
                "mirrored_diagnostics": [],
                "gates": {
                    "spectral_controls": False,
                    "continuation_registration_complete": False,
                    "unstable_spectrum": False,
                    "registered_perturbation_growth": False,
                    "stable_spectrum": False,
                    "registered_perturbation_contraction": False,
                    "exact_control_pass": False,
                },
                "decision": "execution-blocked",
            }
        )
    else:
        panels = [
            run_eigen_panel(jacobian, history, CANDIDATE, panel, THRESHOLDS)
            for panel in PANELS
        ]
        agreement = panel_agreement(panels, THRESHOLDS)
        reference_norm = translation_reduced_norm(
            history,
            alpha=CANDIDATE.alpha,
            memory_mass=CANDIDATE.memory_mass,
        )
        perturbation_scale = THRESHOLDS.perturbation_scale_fraction * CANDIDATE.radius
        continuations = [
            run_continuation(
                name,
                perturbation,
                history,
                reference_norm,
                CANDIDATE,
                THRESHOLDS,
            )
            for name, perturbation in registered_perturbations(
                history,
                scale=perturbation_scale,
            ).items()
        ]
        decision, gates = evaluate_decision(
            full_map_controls=full_map_controls,
            panels=panels,
            agreement=agreement,
            continuations=continuations,
            thresholds=THRESHOLDS,
        )
        payload.update(
            {
                "reference_d0_norm": reference_norm,
                "perturbation_scale": perturbation_scale,
                "spectral_panels": panels,
                "panel_agreement": agreement,
                "continuations": continuations,
                "spectral_diagnostics": spectral_diagnostics(
                    panels,
                    alpha=CANDIDATE.alpha,
                    anchor_modulus=anchor_modulus,
                    anchor_alpha=anchor_alpha,
                ),
                "mirrored_diagnostics": mirrored_diagnostics(continuations),
                "gates": gates,
                "decision": decision,
            }
        )
    payload["duration_seconds"] = float(time.monotonic() - started)
    payload["claim_boundary"] = {
        "established_if_unstable": (
            "the certified prepared L3 balance root is transversely unstable "
            "under the registered full-FIFO numerical tests"
        ),
        "established_if_stable": (
            "local numerical transverse stability of the prepared L3 relative "
            "equilibrium in the registered panels; together with the Anchor, "
            "two tested scales but not a stable family"
        ),
        "not_established": (
            "complete spectral enclosure, L0-L5 stability, formation, noise "
            "robustness, internal S1, Loop-Center compatibility, work, mass, "
            "or interactions"
        ),
    }
    return payload


def _fmt(value: Any) -> str:
    if value is None:
        return "--"
    return f"{float(value):.9g}"


def render_report(payload: dict[str, Any]) -> str:
    """Render the compact human-readable result report."""

    lines = [
        "# P1 L3 non-Anchor rotating-wave stability",
        "",
        f"Generated: {payload['generated_utc']}.",
        "",
        f"Decision: **{payload['decision']}**.",
        "",
        "The run used the unchanged protocol frozen at",
        f"{payload['provenance']['freeze_revision']} and clean execution",
        f"revision {payload['provenance']['execution_revision']}.",
        "",
        "## Prospective and full-map controls",
        "",
        f"- Frozen provenance pass: {payload['provenance']['pass']}",
        f"- Input replay pass: {payload['input_checks']['l3_foundation_replay']['pass']}",
        f"- Implementation controls: {payload['implementation_controls']['pass']}",
        f"- Fixed-point max error: {_fmt(payload['fixed_point_max_component_error'])}",
        f"- Jacobian shape: {payload['jacobian_shape']}",
        f"- Sparse nonzeros: {payload['jacobian_nonzero_entries']}",
        f"- Analytic symmetry pass: {payload['analytic_symmetry_checks']['pass']}",
        f"- Full-map controls: {payload['full_map_controls']}",
        f"- Runtime: {_fmt(payload['duration_seconds'])} s",
        "",
    ]
    if payload["spectral_panels"]:
        lines.extend(
            [
                "## Leading transverse multipliers",
                "",
                "| panel | lambda | modulus | residual | decay rate | panel pass |",
                "| --- | ---: | ---: | ---: | ---: | :---: |",
            ]
        )
        diagnostic_by_panel = {
            row["panel"]: row for row in payload["spectral_diagnostics"]["panels"]
        }
        for panel in payload["spectral_panels"]:
            leading = panel["leading_transverse"]
            value = (
                f"{_fmt(leading['real'])} {leading['imag']:+.9g}i"
                if leading is not None
                else "--"
            )
            decay = diagnostic_by_panel[panel["registration"]["name"]][
                "decay_rate_per_memory_time"
            ]
            lines.append(
                "| "
                f"{panel['registration']['name']} | {value} | "
                f"{_fmt(leading['modulus'] if leading else None)} | "
                f"{_fmt(leading['normalized_residual'] if leading else None)} | "
                f"{_fmt(decay)} | {panel['panel_pass']} |"
            )
        lines.extend(
            [
                "",
                f"- Panel agreement: {payload['panel_agreement']['pass']}",
                "- Complex difference: "
                f"{_fmt(payload['panel_agreement']['complex_difference'])}",
                "- Modulus difference: "
                f"{_fmt(payload['panel_agreement']['modulus_difference'])}",
                "- Anchor decay rate per memory time: "
                f"{_fmt(payload['spectral_diagnostics']['anchor_decay_rate_per_memory_time'])}",
                "",
                "## Registered perturbations",
                "",
                "| perturbation | initial | maximum | final | max/initial | final/initial | stop |",
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
            "A pass concerns one prepared L3 spatial relative equilibrium in",
            "the registered numerical panels. It is not a complete spectral",
            "enclosure, stable-family, formation, topology, Loop--Center, work,",
            "mass or interaction result. The critical review is mandatory before",
            "P2 or any Paper claim is opened.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    payload = run_gate()
    report_path = ROOT / DEFAULT_REPORT
    summary_path = ROOT / DEFAULT_SUMMARY
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
