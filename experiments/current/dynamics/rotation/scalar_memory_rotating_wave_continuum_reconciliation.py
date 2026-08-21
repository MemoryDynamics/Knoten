"""Reconcile the rotating-wave ladder with the exact fixed-gain continuum root."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from datetime import UTC, datetime
import json
from pathlib import Path
import subprocess
from typing import Any

import numpy as np

from emergenz_knoten.rotating_wave import (
    ContinuumRotatingWaveBalance,
    continuum_rotating_wave_balance,
    continuum_rotating_wave_components,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_continuum_reconciliation_protocol_2026-08-21.md"
)
DISCOVERY_RESULT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_discovery_2026-08-20.json"
)
LADDER_RESULT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_refinement_ladder_2026-08-21.json"
)
DEFAULT_REPORT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_continuum_reconciliation_2026-08-21.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_continuum_reconciliation_2026-08-21.json"
)

TAIL_EXTENT = 12.0
ETA_PER_ALPHA = 15.0
MEMORY_MASS = 1.0
SIGMA_REP = 1.0
SIGMA_ATT = 3.0
AMPLITUDE_REP = 1.0
AMPLITUDE_ATT = 3.5
OLD_GUIDE_RADIUS = 0.9430108292781663
OLD_GUIDE_OMEGA = 1.5868166272376472
OLD_GUIDE_REQUIRED_ETA_PER_ALPHA = 15.016345187237246
NEWTON_ITERATIONS = 8
RADIUS_CORRIDOR = 0.05
OMEGA_CORRIDOR = 0.05
PANELS = (
    {"name": "numpy-256", "quadrature_backend": "numpy", "quadrature_order": 256},
    {"name": "numpy-512", "quadrature_backend": "numpy", "quadrature_order": 512},
    {"name": "scipy-1024", "quadrature_backend": "scipy", "quadrature_order": 1024},
)
RESIDUAL_MAXIMUM = 1.0e-12
COMPONENT_CROSSCHECK_MAXIMUM = 5.0e-14
REQUIRED_GAIN_ERROR_MAXIMUM = 1.0e-10
CONDITION_NUMBER_MAXIMUM = 1.0e8
PANEL_RANGE_MAXIMUM = 5.0e-11
SOURCE_VALUE_TOLERANCE = 2.0e-15
SOURCE_GAIN_MISMATCH_MINIMUM = 1.0e-3
SLOPE_MINIMUM = 0.8
SLOPE_MAXIMUM = 1.2
FINE_TO_ANCHOR_ERROR_MAXIMUM = 0.35
RICHARDSON_RELATIVE_ERROR_MAXIMUM = 0.1
EXPECTED_LADDER_EXECUTION_REVISION = (
    "b03ff433776ced084f8bf3d56b54b8fe7b1e5ef2"
)
EXPECTED_LADDER_CELLS = (
    ("L0", 0.04, 300, 0.60),
    ("L1", 0.02, 600, 0.30),
    ("L2", 0.01, 1200, 0.15),
    ("L3", 0.005, 2400, 0.075),
    ("L4", 0.0025, 4800, 0.0375),
)


def _git_output(arguments: list[str]) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return result.stdout.strip()


def _balance(
    radius: float,
    omega: float,
    *,
    quadrature_order: int,
    quadrature_backend: str,
) -> ContinuumRotatingWaveBalance:
    return continuum_rotating_wave_balance(
        radius=radius,
        angular_frequency=omega,
        eta_per_alpha=ETA_PER_ALPHA,
        tail_extent=TAIL_EXTENT,
        memory_mass=MEMORY_MASS,
        sigma_rep=SIGMA_REP,
        sigma_att=SIGMA_ATT,
        amplitude_rep=AMPLITUDE_REP,
        amplitude_att=AMPLITUDE_ATT,
        quadrature_order=quadrature_order,
        quadrature_backend=quadrature_backend,
    )


def fixed_newton(
    function: Callable[[float, float], ContinuumRotatingWaveBalance],
    *,
    radius_start: float,
    omega_start: float,
    iterations: int,
) -> dict[str, Any]:
    """Apply a fixed number of undamped analytic Newton steps."""

    if iterations < 1:
        raise ValueError("iterations must be positive")
    point = np.asarray([radius_start, omega_start], dtype=float)
    records = []
    for index in range(iterations + 1):
        balance = function(float(point[0]), float(point[1]))
        residual = np.asarray(balance.residual, dtype=float)
        jacobian = np.asarray(balance.jacobian, dtype=float)
        determinant = float(np.linalg.det(jacobian))
        condition_number = float(np.linalg.cond(jacobian))
        record = {
            "iteration": index,
            "radius": float(point[0]),
            "omega": float(point[1]),
            "residual": [float(value) for value in residual],
            "residual_maximum": float(np.max(np.abs(residual))),
            "jacobian": [[float(value) for value in row] for row in jacobian],
            "jacobian_determinant": determinant,
            "jacobian_condition_number": condition_number,
        }
        if index < iterations:
            step = np.linalg.solve(jacobian, residual)
            record["newton_step"] = [float(value) for value in step]
            point = point - step
        records.append(record)
    return {
        "radius": float(point[0]),
        "omega": float(point[1]),
        "iterations": records,
        "balance": function(float(point[0]), float(point[1])),
    }


def _solve_panel(panel: dict[str, Any]) -> dict[str, Any]:
    order = int(panel["quadrature_order"])
    backend = str(panel["quadrature_backend"])
    result = fixed_newton(
        lambda radius, omega: _balance(
            radius,
            omega,
            quadrature_order=order,
            quadrature_backend=backend,
        ),
        radius_start=OLD_GUIDE_RADIUS,
        omega_start=OLD_GUIDE_OMEGA,
        iterations=NEWTON_ITERATIONS,
    )
    balance = result.pop("balance")
    radius = float(result["radius"])
    omega = float(result["omega"])
    components = continuum_rotating_wave_components(
        radius=radius,
        angular_frequency=omega,
        tail_extent=TAIL_EXTENT,
        memory_mass=MEMORY_MASS,
        sigma_rep=SIGMA_REP,
        sigma_att=SIGMA_ATT,
        amplitude_rep=AMPLITUDE_REP,
        amplitude_att=AMPLITUDE_ATT,
        quadrature_order=order,
        quadrature_backend=backend,
    )
    component_discrepancy = max(
        abs(balance.components.radial - components.radial),
        abs(balance.components.tangential - components.tangential),
    )
    residual_maximum = max(abs(value) for value in balance.residual)
    maximum_condition_number = max(
        row["jacobian_condition_number"] for row in result["iterations"]
    )
    corridor = all(
        abs(row["radius"] - OLD_GUIDE_RADIUS) < RADIUS_CORRIDOR
        and abs(row["omega"] - OLD_GUIDE_OMEGA) < OMEGA_CORRIDOR
        for row in result["iterations"]
    )
    gates = {
        "all_values_finite": bool(
            np.all(
                np.isfinite(
                    [
                        radius,
                        omega,
                        *balance.residual,
                        *balance.jacobian[0],
                        *balance.jacobian[1],
                        balance.required_eta_per_alpha,
                        component_discrepancy,
                        maximum_condition_number,
                    ]
                )
            )
        ),
        "branch_corridor": corridor,
        "positive_geometry": radius > 0.0 and omega > 0.0,
        "residual": residual_maximum <= RESIDUAL_MAXIMUM,
        "negative_tangential_integral": balance.components.tangential < 0.0,
        "required_gain": (
            abs(balance.required_eta_per_alpha - ETA_PER_ALPHA)
            <= REQUIRED_GAIN_ERROR_MAXIMUM
        ),
        "component_crosscheck": (
            component_discrepancy <= COMPONENT_CROSSCHECK_MAXIMUM
        ),
        "jacobian_condition": (
            maximum_condition_number <= CONDITION_NUMBER_MAXIMUM
        ),
    }
    return {
        "name": panel["name"],
        "quadrature_backend": backend,
        "quadrature_order": order,
        **result,
        "components": {
            "radial": balance.components.radial,
            "tangential": balance.components.tangential,
        },
        "residual": list(balance.residual),
        "jacobian": [list(row) for row in balance.jacobian],
        "required_eta_per_alpha": balance.required_eta_per_alpha,
        "residual_maximum": residual_maximum,
        "component_crosscheck_maximum": component_discrepancy,
        "maximum_jacobian_condition_number": maximum_condition_number,
        "gates": gates,
        "pass": all(gates.values()),
    }


def panel_agreement(panels: list[dict[str, Any]]) -> dict[str, Any]:
    radius_range = max(row["radius"] for row in panels) - min(
        row["radius"] for row in panels
    )
    omega_range = max(row["omega"] for row in panels) - min(
        row["omega"] for row in panels
    )
    gates = {
        "radius_range": radius_range <= PANEL_RANGE_MAXIMUM,
        "omega_range": omega_range <= PANEL_RANGE_MAXIMUM,
    }
    return {
        "radius_range": radius_range,
        "omega_range": omega_range,
        "gates": gates,
        "pass": all(gates.values()),
    }


def _source_audit(discovery: dict[str, Any]) -> dict[str, Any]:
    initializer = discovery["selected_candidate"]["initializer"]
    observed = {
        "radius": float(initializer["radius_over_sigma_rep"]),
        "omega": float(initializer["angular_frequency_per_memory_time"]),
        "required_eta_per_alpha": float(initializer["required_eta_per_alpha"]),
    }
    gates = {
        "registered_radius_reproduced": (
            abs(observed["radius"] - OLD_GUIDE_RADIUS) <= SOURCE_VALUE_TOLERANCE
        ),
        "registered_omega_reproduced": (
            abs(observed["omega"] - OLD_GUIDE_OMEGA) <= SOURCE_VALUE_TOLERANCE
        ),
        "registered_gain_reproduced": (
            abs(
                observed["required_eta_per_alpha"]
                - OLD_GUIDE_REQUIRED_ETA_PER_ALPHA
            )
            <= SOURCE_VALUE_TOLERANCE
        ),
        "gain_mismatch_is_material": (
            abs(observed["required_eta_per_alpha"] - ETA_PER_ALPHA)
            >= SOURCE_GAIN_MISMATCH_MINIMUM
        ),
    }
    return {"observed": observed, "gates": gates, "pass": all(gates.values())}


def _ladder_rows_and_integrity(
    ladder: dict[str, Any],
) -> tuple[list[dict[str, float]], dict[str, Any]]:
    observed_cells = []
    rows = []
    all_cell_flags = True
    for cell in ladder["cells"]:
        observed_cells.append(
            (
                str(cell["cell"]),
                float(cell["alpha"]),
                int(cell["horizon"]),
                float(cell["eta"]),
            )
        )
        panel = max(cell["panels"], key=lambda row: int(row["precision_dps"]))
        rows.append(
            {
                "alpha": float(cell["alpha"]),
                "radius": float(panel["refined"]["radius"]),
                "omega": float(panel["omega"]),
            }
        )
        all_cell_flags = all_cell_flags and bool(cell["pass"])
    gates = {
        "historical_decision_preserved": (
            ladder["decision"] == "certified-roots-nonconvergent"
        ),
        "execution_revision_preserved": (
            ladder["execution_revision"] == EXPECTED_LADDER_EXECUTION_REVISION
        ),
        "registered_cells_preserved": tuple(observed_cells) == EXPECTED_LADDER_CELLS,
        "all_cells_certified": bool(ladder["all_cells_certified"]),
        "anchor_overlap": bool(ladder["anchor_overlap"]),
        "all_cell_flags": all_cell_flags,
    }
    rows.sort(key=lambda row: row["alpha"], reverse=True)
    return rows, {"gates": gates, "pass": all(gates.values())}


def scaling_diagnostics(
    rows: list[dict[str, float]],
    *,
    target_radius: float,
    target_omega: float,
) -> dict[str, Any]:
    """Apply the original ladder thresholds to an explicitly supplied target."""

    ordered = sorted(rows, key=lambda row: row["alpha"], reverse=True)
    alphas = np.asarray([row["alpha"] for row in ordered], dtype=float)
    radius_errors = np.abs(
        np.asarray([row["radius"] for row in ordered], dtype=float) - target_radius
    )
    omega_errors = np.abs(
        np.asarray([row["omega"] for row in ordered], dtype=float) - target_omega
    )
    positive_errors = bool(np.all(radius_errors > 0.0) and np.all(omega_errors > 0.0))
    fine = alphas <= 0.02
    if positive_errors:
        radius_slope = float(
            np.polyfit(np.log(alphas[fine]), np.log(radius_errors[fine]), 1)[0]
        )
        omega_slope = float(
            np.polyfit(np.log(alphas[fine]), np.log(omega_errors[fine]), 1)[0]
        )
    else:
        radius_slope = None
        omega_slope = None
    anchor_index = int(np.flatnonzero(np.isclose(alphas, 0.01, rtol=0.0, atol=1e-15))[0])
    radius_fine_ratio = (
        float(radius_errors[-1] / radius_errors[anchor_index])
        if radius_errors[anchor_index] > 0.0
        else None
    )
    omega_fine_ratio = (
        float(omega_errors[-1] / omega_errors[anchor_index])
        if omega_errors[anchor_index] > 0.0
        else None
    )
    radius_richardson = 2.0 * ordered[-1]["radius"] - ordered[-2]["radius"]
    omega_richardson = 2.0 * ordered[-1]["omega"] - ordered[-2]["omega"]
    radius_richardson_relative = (
        float(abs(radius_richardson - target_radius) / radius_errors[-1])
        if radius_errors[-1] > 0.0
        else None
    )
    omega_richardson_relative = (
        float(abs(omega_richardson - target_omega) / omega_errors[-1])
        if omega_errors[-1] > 0.0
        else None
    )
    gates = {
        "positive_errors": positive_errors,
        "radius_error_monotone": bool(np.all(np.diff(radius_errors) < 0.0)),
        "omega_error_monotone": bool(np.all(np.diff(omega_errors) < 0.0)),
        "radius_slope": (
            radius_slope is not None
            and SLOPE_MINIMUM <= radius_slope <= SLOPE_MAXIMUM
        ),
        "omega_slope": (
            omega_slope is not None
            and SLOPE_MINIMUM <= omega_slope <= SLOPE_MAXIMUM
        ),
        "radius_fine_to_anchor": (
            radius_fine_ratio is not None
            and radius_fine_ratio <= FINE_TO_ANCHOR_ERROR_MAXIMUM
        ),
        "omega_fine_to_anchor": (
            omega_fine_ratio is not None
            and omega_fine_ratio <= FINE_TO_ANCHOR_ERROR_MAXIMUM
        ),
        "radius_richardson": (
            radius_richardson_relative is not None
            and radius_richardson_relative <= RICHARDSON_RELATIVE_ERROR_MAXIMUM
        ),
        "omega_richardson": (
            omega_richardson_relative is not None
            and omega_richardson_relative <= RICHARDSON_RELATIVE_ERROR_MAXIMUM
        ),
    }
    successive_radius_differences = np.abs(np.diff([row["radius"] for row in ordered]))
    successive_omega_differences = np.abs(np.diff([row["omega"] for row in ordered]))
    return {
        "target_radius": target_radius,
        "target_omega": target_omega,
        "rows": [
            {
                **row,
                "radius_error": float(radius_errors[index]),
                "omega_error": float(omega_errors[index]),
            }
            for index, row in enumerate(ordered)
        ],
        "radius_slope": radius_slope,
        "omega_slope": omega_slope,
        "radius_fine_to_anchor_error_ratio": radius_fine_ratio,
        "omega_fine_to_anchor_error_ratio": omega_fine_ratio,
        "radius_richardson": radius_richardson,
        "omega_richardson": omega_richardson,
        "radius_richardson_relative_error": radius_richardson_relative,
        "omega_richardson_relative_error": omega_richardson_relative,
        "radius_successive_difference_ratios": [
            (
                float(successive_radius_differences[index + 1] / value)
                if value > 0.0
                else None
            )
            for index, value in enumerate(successive_radius_differences[:-1])
        ],
        "omega_successive_difference_ratios": [
            (
                float(successive_omega_differences[index + 1] / value)
                if value > 0.0
                else None
            )
            for index, value in enumerate(successive_omega_differences[:-1])
        ],
        "gates": gates,
        "pass": all(gates.values()),
    }


def run_gate() -> dict[str, Any]:
    start_status = _git_output(["status", "--short"])
    if start_status:
        raise RuntimeError("continuum reconciliation requires a clean revision")
    revision = _git_output(["rev-parse", "HEAD"])
    try:
        # Target construction is deliberately completed before the ladder is loaded.
        panels = [_solve_panel(panel) for panel in PANELS]
        agreement = panel_agreement(panels)
        primary = panels[-1]
        all_panels_pass = all(panel["pass"] for panel in panels)

        discovery = json.loads((ROOT / DISCOVERY_RESULT).read_text(encoding="utf-8"))
        source_audit = _source_audit(discovery)
        ladder = json.loads((ROOT / LADDER_RESULT).read_text(encoding="utf-8"))
        ladder_rows, ladder_integrity = _ladder_rows_and_integrity(ladder)
        scaling = scaling_diagnostics(
            ladder_rows,
            target_radius=primary["radius"],
            target_omega=primary["omega"],
        )
        continuum_pass = all_panels_pass and agreement["pass"]
        inputs_pass = source_audit["pass"] and ladder_integrity["pass"]
        if continuum_pass and inputs_pass and scaling["pass"]:
            decision = "fixed-gain-continuum-reconciliation-pass"
        elif continuum_pass and inputs_pass:
            decision = "fixed-gain-target-ladder-mismatch"
        else:
            decision = "fixed-gain-continuum-inconclusive"
        exception = None
    except Exception as error:  # pragma: no cover - result-path safeguard
        panels = []
        agreement = None
        source_audit = None
        ladder_integrity = None
        scaling = None
        all_panels_pass = False
        continuum_pass = False
        inputs_pass = False
        decision = "fixed-gain-continuum-inconclusive"
        exception = f"{type(error).__name__}: {error}"

    return {
        "schema": "emergenz-knoten.scalar-memory-rotating-wave-continuum-reconciliation",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "execution_revision": revision,
        "git_status_at_start": start_status,
        "protocol": PROTOCOL.as_posix(),
        "sources": {
            "discovery": DISCOVERY_RESULT.as_posix(),
            "ladder": LADDER_RESULT.as_posix(),
        },
        "registration": {
            "tail_extent": TAIL_EXTENT,
            "eta_per_alpha": ETA_PER_ALPHA,
            "memory_mass": MEMORY_MASS,
            "sigma_rep": SIGMA_REP,
            "sigma_att": SIGMA_ATT,
            "amplitude_rep": AMPLITUDE_REP,
            "amplitude_att": AMPLITUDE_ATT,
            "old_guide_radius_start": OLD_GUIDE_RADIUS,
            "old_guide_omega_start": OLD_GUIDE_OMEGA,
            "newton_iterations": NEWTON_ITERATIONS,
            "radius_corridor": RADIUS_CORRIDOR,
            "omega_corridor": OMEGA_CORRIDOR,
            "panels": PANELS,
            "residual_maximum": RESIDUAL_MAXIMUM,
            "panel_range_maximum": PANEL_RANGE_MAXIMUM,
            "sealed_amplitude_holdout": 7.0,
        },
        "panels": panels,
        "all_panels_pass": all_panels_pass,
        "panel_agreement": agreement,
        "continuum_pass": continuum_pass,
        "source_audit": source_audit,
        "ladder_integrity": ladder_integrity,
        "inputs_pass": inputs_pass,
        "scaling": scaling,
        "historical_ladder_decision": "certified-roots-nonconvergent",
        "decision": decision,
        "exception": exception,
        "claim_boundary": {
            "established_if_pass": (
                "a numerically quadrature-converged fixed-gain continuum root and "
                "consistency of the frozen five-cell ladder with the original "
                "first-order scaling gates against that corrected target"
            ),
            "not_established": (
                "an interval theorem for the continuum integral, an all-alpha "
                "convergence theorem, non-anchor stability, formation, noise "
                "robustness, internal S1, work, inertia, or mass"
            ),
        },
    }


def _fmt(value: Any) -> str:
    if value is None:
        return "--"
    try:
        return f"{float(value):.12g}"
    except (TypeError, ValueError):
        return str(value)


def render_report(payload: dict[str, Any]) -> str:
    lines = [
        "# Fixed-gain continuum reconciliation for the rotating-wave ladder",
        "",
        f"Generated: {payload['generated_utc']}.",
        "",
        f"Decision: **{payload['decision']}**.",
        "",
        "The historical ladder verdict remains "
        f"**{payload['historical_ladder_decision']}**; this result does not relabel it.",
        "",
    ]
    if payload["exception"] is not None:
        lines.extend(["Execution exception:", "", payload["exception"], ""])
        return "\n".join(lines)

    lines.extend(
        [
            "## Fixed equations",
            "",
            "The target solves `I_R(R, Omega) = 0` and "
            "`Omega + 15 I_T(R, Omega) = 0` at `C = 12`, using the unchanged "
            "native two-Gaussian kernel. No ladder value or extrapolation seeds "
            "the solve.",
            "",
            "## Independent quadrature panels",
            "",
            "| panel | order | R | Omega | max residual | required gain | pass |",
            "| --- | ---: | ---: | ---: | ---: | ---: | :---: |",
        ]
    )
    for panel in payload["panels"]:
        lines.append(
            f"| {panel['name']} | {panel['quadrature_order']} | "
            f"{_fmt(panel['radius'])} | {_fmt(panel['omega'])} | "
            f"{_fmt(panel['residual_maximum'])} | "
            f"{_fmt(panel['required_eta_per_alpha'])} | {panel['pass']} |"
        )
    agreement = payload["panel_agreement"]
    primary = payload["panels"][-1]
    source = payload["source_audit"]["observed"]
    scaling = payload["scaling"]
    lines.extend(
        [
            "",
            f"Panel ranges: R = {_fmt(agreement['radius_range'])}, "
            f"Omega = {_fmt(agreement['omega_range'])}.",
            "",
            "The registered target is the highest-order panel:",
            "",
            f"- R = {_fmt(primary['radius'])}",
            f"- Omega = {_fmt(primary['omega'])}",
            f"- required eta/alpha = {_fmt(primary['required_eta_per_alpha'])}",
            "",
            "## Audited source mismatch",
            "",
            "The old discovery initializer is reproduced directly from its JSON:",
            "",
            f"- old R = {_fmt(source['radius'])}",
            f"- old Omega = {_fmt(source['omega'])}",
            f"- old required eta/alpha = {_fmt(source['required_eta_per_alpha'])}",
            "",
            "It therefore belongs to a different gain than the ladder's exact "
            "eta/alpha = 15.",
            "",
            "## Original scaling gates against the corrected target",
            "",
            f"- radius slope: {_fmt(scaling['radius_slope'])}",
            f"- Omega slope: {_fmt(scaling['omega_slope'])}",
            "- radius finest/anchor error ratio: "
            f"{_fmt(scaling['radius_fine_to_anchor_error_ratio'])}",
            "- Omega finest/anchor error ratio: "
            f"{_fmt(scaling['omega_fine_to_anchor_error_ratio'])}",
            "- radius Richardson relative error: "
            f"{_fmt(scaling['radius_richardson_relative_error'])}",
            "- Omega Richardson relative error: "
            f"{_fmt(scaling['omega_richardson_relative_error'])}",
            f"- all original scaling gates: {scaling['pass']}",
            "",
            "## Claim boundary",
            "",
            payload["claim_boundary"]["established_if_pass"] + ".",
            "",
            "This does not establish "
            + payload["claim_boundary"]["not_established"]
            + ".",
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
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(f"Decision: {payload['decision']}")
    print(f"Report: {report_path.relative_to(ROOT)}")
    print(f"Summary: {summary_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
