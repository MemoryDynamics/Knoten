"""Execute the preregistered matched rotating-wave refinement ladder."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path
import subprocess
from typing import Any

from mpmath import mp
import numpy as np

from emergenz_knoten.rotating_wave_interval import (
    IntervalRotatingWaveParameters,
    certify_rotating_wave_box,
    refine_rotating_wave_root,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_refinement_ladder_protocol_2026-08-21.md"
)
ANCHOR_CERTIFICATE = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_interval_certificate_2026-08-21.json"
)
DEFAULT_REPORT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_refinement_ladder_2026-08-21.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_refinement_ladder_2026-08-21.json"
)

CELLS = (
    {"cell": "L0", "alpha": "0.04", "horizon": 300, "eta": "0.60"},
    {"cell": "L1", "alpha": "0.02", "horizon": 600, "eta": "0.30"},
    {"cell": "L2", "alpha": "0.01", "horizon": 1200, "eta": "0.15"},
    {"cell": "L3", "alpha": "0.005", "horizon": 2400, "eta": "0.075"},
    {"cell": "L4", "alpha": "0.0025", "horizon": 4800, "eta": "0.0375"},
)
PRECISION_PANELS = (80, 120)
NEWTON_ITERATIONS = 8
RADIUS_START = (
    "0.946517504804223960990626662735384935160072399313332184824852"
)
OMEGA_START = (
    "1.577038171713499190126896414134132313163211409800625077659236"
)
RADIUS_CORRIDOR = "0.15"
OMEGA_CORRIDOR = "0.15"
OUTER_RADIUS_HALF_WIDTH = "1e-6"
OUTER_OMEGA_HALF_WIDTH = "1e-6"
INNER_RADIUS_HALF_WIDTH = "1e-35"
INNER_OMEGA_HALF_WIDTH = "1e-35"
CROSS_PRECISION_TOLERANCE = "1e-55"
INNER_RADIUS_IMAGE_WIDTH_MAXIMUM = "1e-33"
INNER_OMEGA_IMAGE_WIDTH_MAXIMUM = "1e-33"
CONTINUUM_RADIUS_GUIDE = "0.9430108292781663"
CONTINUUM_OMEGA_GUIDE = "1.5868166272376472"
SLOPE_MINIMUM = 0.8
SLOPE_MAXIMUM = 1.2
FINE_TO_ANCHOR_ERROR_MAXIMUM = 0.35
RICHARDSON_RELATIVE_ERROR_MAXIMUM = 0.1


def _git_output(arguments: list[str]) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return result.stdout.strip()


def _parameters(cell: dict[str, Any]) -> IntervalRotatingWaveParameters:
    return IntervalRotatingWaveParameters(
        alpha=cell["alpha"],
        horizon=cell["horizon"],
        memory_mass="1.0",
        eta=cell["eta"],
        sigma_rep="1.0",
        sigma_att="3.0",
        amplitude_rep="1.0",
        amplitude_att="3.5",
    )


def _scaled(value: str, alpha: str, precision: int = 180) -> str:
    with mp.workdps(precision):
        return mp.nstr(mp.mpf(value) * mp.mpf(alpha), precision - 20)


def _record_endpoints(record: dict[str, Any]) -> tuple[mp.mpf, mp.mpf]:
    lower = tuple(int(value) for value in record["lower_binary"])
    upper = tuple(int(value) for value in record["upper_binary"])
    return mp.make_mpf(lower), mp.make_mpf(upper)


def _records_overlap(first: dict[str, Any], second: dict[str, Any]) -> bool:
    with mp.workdps(180):
        first_lower, first_upper = _record_endpoints(first)
        second_lower, second_upper = _record_endpoints(second)
        return bool(max(first_lower, second_lower) <= min(first_upper, second_upper))


def _record_width_in_omega_below(
    record: dict[str, Any], *, alpha: str, threshold: str
) -> bool:
    with mp.workdps(180):
        lower, upper = _record_endpoints(record)
        return bool((upper - lower) / mp.mpf(alpha) < mp.mpf(threshold))


def _record_width_below(record: dict[str, Any], threshold: str) -> bool:
    with mp.workdps(180):
        lower, upper = _record_endpoints(record)
        return bool(upper - lower < mp.mpf(threshold))


def _corridor_pass(iterates: list[dict[str, str]], *, alpha: str) -> bool:
    with mp.workdps(180):
        alpha_value = mp.mpf(alpha)
        return all(
            abs(mp.mpf(row["radius"]) - mp.mpf(RADIUS_START))
            < mp.mpf(RADIUS_CORRIDOR)
            and abs(mp.mpf(row["theta"]) / alpha_value - mp.mpf(OMEGA_START))
            < mp.mpf(OMEGA_CORRIDOR)
            for row in iterates
        )


def _panel(cell: dict[str, Any], precision_dps: int) -> dict[str, Any]:
    parameters = _parameters(cell)
    initial_theta = _scaled(OMEGA_START, cell["alpha"])
    refined = refine_rotating_wave_root(
        radius=RADIUS_START,
        theta=initial_theta,
        parameters=parameters,
        precision_dps=precision_dps,
        iterations=NEWTON_ITERATIONS,
    )
    outer = certify_rotating_wave_box(
        radius=refined["radius"],
        theta=refined["theta"],
        radius_half_width=OUTER_RADIUS_HALF_WIDTH,
        theta_half_width=_scaled(OUTER_OMEGA_HALF_WIDTH, cell["alpha"]),
        parameters=parameters,
        precision_dps=precision_dps,
    )
    inner = certify_rotating_wave_box(
        radius=refined["radius"],
        theta=refined["theta"],
        radius_half_width=INNER_RADIUS_HALF_WIDTH,
        theta_half_width=_scaled(INNER_OMEGA_HALF_WIDTH, cell["alpha"]),
        parameters=parameters,
        precision_dps=precision_dps,
    )
    with mp.workdps(180):
        omega = mp.mpf(refined["theta"]) / mp.mpf(cell["alpha"])
        point_residual_maximum = max(
            abs(mp.mpf(value)) for value in refined["balance"]
        )
        residual_threshold = mp.mpf(10) ** (-(precision_dps - 20))
    gates = {
        "newton_corridor": _corridor_pass(
            refined["iterates"], alpha=cell["alpha"]
        ),
        "outer_certificate": bool(outer["pass"]),
        "inner_certificate": bool(inner["pass"]),
        "point_residual": bool(point_residual_maximum <= residual_threshold),
        "inner_radius_image_width": _record_width_below(
            inner["krawczyk_image"][0], INNER_RADIUS_IMAGE_WIDTH_MAXIMUM
        ),
        "inner_omega_image_width": _record_width_in_omega_below(
            inner["krawczyk_image"][1],
            alpha=cell["alpha"],
            threshold=INNER_OMEGA_IMAGE_WIDTH_MAXIMUM,
        ),
    }
    return {
        "precision_dps": precision_dps,
        "initial": {"radius": RADIUS_START, "theta": initial_theta},
        "refined": refined,
        "omega": mp.nstr(omega, precision_dps - 12),
        "point_residual_maximum": mp.nstr(point_residual_maximum, 20),
        "point_residual_threshold": mp.nstr(residual_threshold, 20),
        "outer": outer,
        "inner": inner,
        "gates": gates,
        "pass": all(gates.values()),
    }


def _cell_cross_precision(panels: list[dict[str, Any]]) -> dict[str, Any]:
    with mp.workdps(180):
        radius_difference = abs(
            mp.mpf(panels[0]["refined"]["radius"])
            - mp.mpf(panels[1]["refined"]["radius"])
        )
        omega_difference = abs(
            mp.mpf(panels[0]["omega"]) - mp.mpf(panels[1]["omega"])
        )
        center_agreement = bool(
            radius_difference <= mp.mpf(CROSS_PRECISION_TOLERANCE)
            and omega_difference <= mp.mpf(CROSS_PRECISION_TOLERANCE)
        )
    enclosure_overlap = all(
        _records_overlap(
            panels[0]["inner"]["krawczyk_image"][index],
            panels[1]["inner"]["krawczyk_image"][index],
        )
        for index in range(2)
    )
    return {
        "radius_difference": mp.nstr(radius_difference, 20),
        "omega_difference": mp.nstr(omega_difference, 20),
        "center_agreement": center_agreement,
        "inner_enclosure_overlap": enclosure_overlap,
        "pass": bool(center_agreement and enclosure_overlap),
    }


def _run_cell(cell: dict[str, Any]) -> dict[str, Any]:
    panels = [_panel(cell, precision) for precision in PRECISION_PANELS]
    cross_precision = _cell_cross_precision(panels)
    return {
        **cell,
        "tail_extent": float(cell["alpha"]) * cell["horizon"],
        "eta_per_alpha": float(cell["eta"]) / float(cell["alpha"]),
        "panels": panels,
        "cross_precision": cross_precision,
        "pass": bool(all(panel["pass"] for panel in panels) and cross_precision["pass"]),
    }


def _anchor_overlap(
    cells: list[dict[str, Any]], anchor_certificate: dict[str, Any]
) -> bool:
    anchor = next(cell for cell in cells if cell["cell"] == "L2")
    prior_by_precision = {
        panel["precision_dps"]: panel for panel in anchor_certificate["panels"]
    }
    return all(
        all(
            _records_overlap(
                panel["inner"]["krawczyk_image"][index],
                prior_by_precision[panel["precision_dps"]]["inner"][
                    "krawczyk_image"
                ][index],
            )
            for index in range(2)
        )
        for panel in anchor["panels"]
    )


def scaling_diagnostics(rows: list[dict[str, float]]) -> dict[str, Any]:
    """Return the frozen continuum-guide scaling diagnostics."""

    ordered = sorted(rows, key=lambda row: row["alpha"], reverse=True)
    alphas = np.asarray([row["alpha"] for row in ordered], dtype=float)
    radius_errors = np.abs(
        np.asarray([row["radius"] for row in ordered])
        - float(CONTINUUM_RADIUS_GUIDE)
    )
    omega_errors = np.abs(
        np.asarray([row["omega"] for row in ordered])
        - float(CONTINUUM_OMEGA_GUIDE)
    )
    monotone_radius = bool(np.all(np.diff(radius_errors) < 0.0))
    monotone_omega = bool(np.all(np.diff(omega_errors) < 0.0))
    fine = alphas <= 0.02
    radius_slope = float(np.polyfit(np.log(alphas[fine]), np.log(radius_errors[fine]), 1)[0])
    omega_slope = float(np.polyfit(np.log(alphas[fine]), np.log(omega_errors[fine]), 1)[0])
    anchor_index = next(index for index, row in enumerate(ordered) if row["alpha"] == 0.01)
    radius_fine_ratio = float(radius_errors[-1] / radius_errors[anchor_index])
    omega_fine_ratio = float(omega_errors[-1] / omega_errors[anchor_index])
    radius_richardson = 2.0 * ordered[-1]["radius"] - ordered[-2]["radius"]
    omega_richardson = 2.0 * ordered[-1]["omega"] - ordered[-2]["omega"]
    radius_richardson_relative = float(
        abs(radius_richardson - float(CONTINUUM_RADIUS_GUIDE))
        / radius_errors[-1]
    )
    omega_richardson_relative = float(
        abs(omega_richardson - float(CONTINUUM_OMEGA_GUIDE))
        / omega_errors[-1]
    )
    gates = {
        "radius_error_monotone": monotone_radius,
        "omega_error_monotone": monotone_omega,
        "radius_slope": SLOPE_MINIMUM <= radius_slope <= SLOPE_MAXIMUM,
        "omega_slope": SLOPE_MINIMUM <= omega_slope <= SLOPE_MAXIMUM,
        "radius_fine_to_anchor": radius_fine_ratio <= FINE_TO_ANCHOR_ERROR_MAXIMUM,
        "omega_fine_to_anchor": omega_fine_ratio <= FINE_TO_ANCHOR_ERROR_MAXIMUM,
        "radius_richardson": radius_richardson_relative
        <= RICHARDSON_RELATIVE_ERROR_MAXIMUM,
        "omega_richardson": omega_richardson_relative
        <= RICHARDSON_RELATIVE_ERROR_MAXIMUM,
    }
    return {
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
        "gates": gates,
        "pass": all(gates.values()),
    }


def _scaling_rows(cells: list[dict[str, Any]]) -> list[dict[str, float]]:
    return [
        {
            "alpha": float(cell["alpha"]),
            "radius": float(cell["panels"][1]["refined"]["radius"]),
            "omega": float(cell["panels"][1]["omega"]),
        }
        for cell in cells
    ]


def run_gate() -> dict[str, Any]:
    start_status = _git_output(["status", "--short"])
    if start_status:
        raise RuntimeError("refinement ladder requires a clean prospective revision")
    revision = _git_output(["rev-parse", "HEAD"])
    anchor_certificate = json.loads(
        (ROOT / ANCHOR_CERTIFICATE).read_text(encoding="utf-8")
    )
    if anchor_certificate["decision"] != "interval-certified-unique-root-pass":
        raise RuntimeError("anchor interval certificate must pass before the ladder")

    try:
        cells = [_run_cell(cell) for cell in CELLS]
        anchor_overlap = _anchor_overlap(cells, anchor_certificate)
        scaling = scaling_diagnostics(_scaling_rows(cells))
        all_cells_certified = bool(all(cell["pass"] for cell in cells))
        if all_cells_certified and anchor_overlap and scaling["pass"]:
            decision = "matched-refinement-pass"
        elif all_cells_certified and anchor_overlap:
            decision = "certified-roots-nonconvergent"
        else:
            decision = "matched-refinement-inconclusive"
        exception = None
    except Exception as error:  # pragma: no cover - result-path safeguard
        cells = []
        anchor_overlap = False
        scaling = None
        all_cells_certified = False
        decision = "matched-refinement-inconclusive"
        exception = f"{type(error).__name__}: {error}"

    return {
        "schema": "emergenz-knoten.scalar-memory-rotating-wave-refinement-ladder",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "execution_revision": revision,
        "git_status_at_start": start_status,
        "protocol": PROTOCOL.as_posix(),
        "anchor_certificate": ANCHOR_CERTIFICATE.as_posix(),
        "registration": {
            "cells": CELLS,
            "precision_panels_dps": list(PRECISION_PANELS),
            "newton_iterations": NEWTON_ITERATIONS,
            "radius_start": RADIUS_START,
            "omega_start": OMEGA_START,
            "radius_corridor": RADIUS_CORRIDOR,
            "omega_corridor": OMEGA_CORRIDOR,
            "outer_radius_half_width": OUTER_RADIUS_HALF_WIDTH,
            "outer_omega_half_width": OUTER_OMEGA_HALF_WIDTH,
            "inner_radius_half_width": INNER_RADIUS_HALF_WIDTH,
            "inner_omega_half_width": INNER_OMEGA_HALF_WIDTH,
            "sealed_amplitude_holdout": 7.0,
        },
        "continuum_guide": {
            "radius": CONTINUUM_RADIUS_GUIDE,
            "omega": CONTINUUM_OMEGA_GUIDE,
            "tail_extent": 12.0,
            "status": "pre-existing high-order quadrature guide, not interval certified",
        },
        "cells": cells,
        "all_cells_certified": all_cells_certified,
        "anchor_overlap": anchor_overlap,
        "scaling": scaling,
        "decision": decision,
        "exception": exception,
        "claim_boundary": {
            "established_if_pass": (
                "a five-cell locally unique finite-H root ladder with numerical "
                "first-order approach to the pre-existing continuum guide"
            ),
            "not_established": (
                "an all-alpha convergence theorem, non-anchor stability, "
                "formation, noise robustness, internal S1, work, or mass"
            ),
        },
    }


def _fmt(value: Any) -> str:
    if value is None:
        return "--"
    try:
        return f"{float(value):.9g}"
    except (TypeError, ValueError):
        return str(value)


def render_report(payload: dict[str, Any]) -> str:
    lines = [
        "# Scalar-memory rotating-wave matched-refinement ladder",
        "",
        f"Generated: {payload['generated_utc']}.",
        "",
        f"Decision: **{payload['decision']}**.",
        "",
        "The ladder was evaluated from clean prospective revision",
        f"{payload['execution_revision']}.",
        "",
    ]
    if payload["exception"] is not None:
        lines.extend(["Execution exception:", "", payload["exception"], ""])
        return "\n".join(lines)

    scaling_by_alpha = {
        row["alpha"]: row for row in payload["scaling"]["rows"]
    }
    lines.extend(
        [
            "## Certified cells",
            "",
            "| cell | alpha | H | eta | R | Omega | R error | Omega error | certified |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |",
        ]
    )
    for cell in payload["cells"]:
        panel = cell["panels"][1]
        scaling = scaling_by_alpha[float(cell["alpha"])]
        lines.append(
            "| "
            f"{cell['cell']} | {cell['alpha']} | {cell['horizon']} | {cell['eta']} | "
            f"{_fmt(panel['refined']['radius'])} | {_fmt(panel['omega'])} | "
            f"{_fmt(scaling['radius_error'])} | {_fmt(scaling['omega_error'])} | "
            f"{cell['pass']} |"
        )
    lines.extend(
        [
            "",
            "## Scaling diagnostics",
            "",
            f"- anchor enclosure overlap: {payload['anchor_overlap']}",
            f"- radius log-log slope: {_fmt(payload['scaling']['radius_slope'])}",
            f"- Omega log-log slope: {_fmt(payload['scaling']['omega_slope'])}",
            "- radius finest/anchor error: "
            f"{_fmt(payload['scaling']['radius_fine_to_anchor_error_ratio'])}",
            "- Omega finest/anchor error: "
            f"{_fmt(payload['scaling']['omega_fine_to_anchor_error_ratio'])}",
            "- radius Richardson relative error: "
            f"{_fmt(payload['scaling']['radius_richardson_relative_error'])}",
            "- Omega Richardson relative error: "
            f"{_fmt(payload['scaling']['omega_richardson_relative_error'])}",
            "",
            "## Claim boundary",
            "",
            "A pass establishes five locally unique exact finite-H roots and",
            "numerical first-order approach to the pre-existing continuum guide.",
            "It is not an all-alpha convergence theorem and does not establish",
            "non-anchor stability, formation, noise robustness, internal phase,",
            "physical work or mass.",
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
