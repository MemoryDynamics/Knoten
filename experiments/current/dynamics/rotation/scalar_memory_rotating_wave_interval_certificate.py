"""Execute the preregistered interval certificate for the rotating wave."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path
import subprocess
from typing import Any

import mpmath
from mpmath import mp

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
    "scalar_memory_rotating_wave_interval_certificate_protocol_2026-08-21.md"
)
P0_AUDIT = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_p0_audit_2026-08-20.json"
)
STABILITY_RESULT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_stability_2026-08-20.json"
)
DEFAULT_REPORT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_interval_certificate_2026-08-21.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_interval_certificate_2026-08-21.json"
)

CANDIDATE_ID = "k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1"
PUBLISHED_RADIUS = "0.946517504804225"
PUBLISHED_THETA = "0.015770381717135"
OUTER_HALF_WIDTH = "1e-10"
INNER_HALF_WIDTH = "1e-40"
PRECISION_PANELS = (80, 120)
NEWTON_ITERATIONS = 8
CENTER_AGREEMENT_TOLERANCE = "1e-60"
INNER_IMAGE_WIDTH_MAXIMUM = "1e-38"

PARAMETERS = IntervalRotatingWaveParameters(
    alpha="0.01",
    horizon=1200,
    memory_mass="1.0",
    eta="0.15",
    sigma_rep="1.0",
    sigma_att="3.0",
    amplitude_rep="1.0",
    amplitude_att="3.5",
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


def _absolute_max(values: list[str], precision: int = 180) -> mp.mpf:
    with mp.workdps(precision):
        return max(abs(mp.mpf(value)) for value in values)


def _record_endpoints(record: dict[str, Any]) -> tuple[mp.mpf, mp.mpf]:
    lower = tuple(int(value) for value in record["lower_binary"])
    upper = tuple(int(value) for value in record["upper_binary"])
    return mp.make_mpf(lower), mp.make_mpf(upper)


def _records_overlap(first: dict[str, Any], second: dict[str, Any]) -> bool:
    with mp.workdps(180):
        first_lower, first_upper = _record_endpoints(first)
        second_lower, second_upper = _record_endpoints(second)
        return bool(max(first_lower, second_lower) <= min(first_upper, second_upper))


def _record_width_below(record: dict[str, Any], threshold: str) -> bool:
    with mp.workdps(180):
        lower, upper = _record_endpoints(record)
        return bool(upper - lower < mp.mpf(threshold))


def _inner_subset_outer(refined: dict[str, Any]) -> bool:
    with mp.workdps(180):
        radius_offset = abs(mp.mpf(refined["radius"]) - mp.mpf(PUBLISHED_RADIUS))
        theta_offset = abs(mp.mpf(refined["theta"]) - mp.mpf(PUBLISHED_THETA))
        return bool(
            radius_offset + mp.mpf(INNER_HALF_WIDTH) < mp.mpf(OUTER_HALF_WIDTH)
            and theta_offset + mp.mpf(INNER_HALF_WIDTH) < mp.mpf(OUTER_HALF_WIDTH)
        )


def _panel(precision_dps: int) -> dict[str, Any]:
    refined = refine_rotating_wave_root(
        radius=PUBLISHED_RADIUS,
        theta=PUBLISHED_THETA,
        parameters=PARAMETERS,
        precision_dps=precision_dps,
        iterations=NEWTON_ITERATIONS,
    )
    outer = certify_rotating_wave_box(
        radius=PUBLISHED_RADIUS,
        theta=PUBLISHED_THETA,
        radius_half_width=OUTER_HALF_WIDTH,
        theta_half_width=OUTER_HALF_WIDTH,
        parameters=PARAMETERS,
        precision_dps=precision_dps,
    )
    inner = certify_rotating_wave_box(
        radius=refined["radius"],
        theta=refined["theta"],
        radius_half_width=INNER_HALF_WIDTH,
        theta_half_width=INNER_HALF_WIDTH,
        parameters=PARAMETERS,
        precision_dps=precision_dps,
    )
    point_residual_threshold = mp.mpf(10) ** (-(precision_dps - 20))
    point_residual_maximum = _absolute_max(refined["balance"])
    gates = {
        "outer_certificate": bool(outer["pass"]),
        "inner_certificate": bool(inner["pass"]),
        "inner_subset_outer": _inner_subset_outer(refined),
        "point_residual": bool(point_residual_maximum <= point_residual_threshold),
        "inner_image_width": all(
            _record_width_below(record, INNER_IMAGE_WIDTH_MAXIMUM)
            for record in inner["krawczyk_image"]
        ),
    }
    return {
        "precision_dps": precision_dps,
        "refined": refined,
        "outer": outer,
        "inner": inner,
        "point_residual_maximum": mp.nstr(point_residual_maximum, 20),
        "point_residual_threshold": mp.nstr(point_residual_threshold, 20),
        "gates": gates,
        "pass": all(gates.values()),
    }


def _cross_panel(panels: list[dict[str, Any]]) -> dict[str, Any]:
    with mp.workdps(180):
        radius_difference = abs(
            mp.mpf(panels[0]["refined"]["radius"])
            - mp.mpf(panels[1]["refined"]["radius"])
        )
        theta_difference = abs(
            mp.mpf(panels[0]["refined"]["theta"])
            - mp.mpf(panels[1]["refined"]["theta"])
        )
        center_agreement = bool(
            radius_difference <= mp.mpf(CENTER_AGREEMENT_TOLERANCE)
            and theta_difference <= mp.mpf(CENTER_AGREEMENT_TOLERANCE)
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
        "theta_difference": mp.nstr(theta_difference, 20),
        "center_agreement": center_agreement,
        "inner_enclosure_overlap": enclosure_overlap,
        "pass": bool(center_agreement and enclosure_overlap),
    }


def _intersection_enclosure(panels: list[dict[str, Any]]) -> dict[str, Any]:
    labels = ("radius", "theta")
    result = {}
    with mp.workdps(180):
        for index, label in enumerate(labels):
            endpoints = [
                _record_endpoints(panel["inner"]["krawczyk_image"][index])
                for panel in panels
            ]
            lower = max(value[0] for value in endpoints)
            upper = min(value[1] for value in endpoints)
            result[label] = {
                "lower": mp.nstr(lower, 90),
                "upper": mp.nstr(upper, 90),
                "width": mp.nstr(upper - lower, 20),
            }
    return result


def run_gate() -> dict[str, Any]:
    start_status = _git_output(["status", "--short"])
    if start_status:
        raise RuntimeError("interval gate requires a clean prospective revision")
    revision = _git_output(["rev-parse", "HEAD"])
    p0 = json.loads((ROOT / P0_AUDIT).read_text(encoding="utf-8"))
    stability = json.loads((ROOT / STABILITY_RESULT).read_text(encoding="utf-8"))
    if p0["decision"] != "pass" or p0["issue_count"] != 0:
        raise RuntimeError("rotating-wave P0 must pass before certification")
    if stability["candidate_id"] != CANDIDATE_ID:
        raise RuntimeError("stability result and certificate candidate differ")

    try:
        panels = [_panel(precision) for precision in PRECISION_PANELS]
        cross_panel = _cross_panel(panels)
        all_controls = bool(all(panel["pass"] for panel in panels) and cross_panel["pass"])
        decision = (
            "interval-certified-unique-root-pass"
            if all_controls
            else "interval-certificate-inconclusive"
        )
        exception = None
        intersection = _intersection_enclosure(panels) if all_controls else None
    except Exception as error:  # pragma: no cover - result-path safeguard
        panels = []
        cross_panel = None
        all_controls = False
        decision = "interval-certificate-execution-fail"
        exception = f"{type(error).__name__}: {error}"
        intersection = None

    return {
        "schema": "emergenz-knoten.scalar-memory-rotating-wave-interval-certificate",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "execution_revision": revision,
        "git_status_at_start": start_status,
        "protocol": PROTOCOL.as_posix(),
        "candidate_id": CANDIDATE_ID,
        "dependency": {"mpmath": mpmath.__version__},
        "parameters": {
            "radius_center": PUBLISHED_RADIUS,
            "theta_center": PUBLISHED_THETA,
            "alpha": PARAMETERS.alpha,
            "horizon": PARAMETERS.horizon,
            "memory_mass": PARAMETERS.memory_mass,
            "eta": PARAMETERS.eta,
            "sigma_rep": PARAMETERS.sigma_rep,
            "sigma_att": PARAMETERS.sigma_att,
            "amplitude_rep": PARAMETERS.amplitude_rep,
            "amplitude_att": PARAMETERS.amplitude_att,
        },
        "registration": {
            "precision_panels_dps": list(PRECISION_PANELS),
            "newton_iterations": NEWTON_ITERATIONS,
            "outer_half_width": OUTER_HALF_WIDTH,
            "inner_half_width": INNER_HALF_WIDTH,
            "center_agreement_tolerance": CENTER_AGREEMENT_TOLERANCE,
            "inner_image_width_maximum": INNER_IMAGE_WIDTH_MAXIMUM,
            "sealed_amplitude_holdout": 7.0,
        },
        "panels": panels,
        "cross_panel": cross_panel,
        "certified_intersection": intersection,
        "all_controls": all_controls,
        "decision": decision,
        "exception": exception,
        "claim_boundary": {
            "established_if_pass": (
                "existence and uniqueness of one exact finite-H rotating-wave "
                "root inside the registered interval boxes"
            ),
            "not_established": (
                "complete spectral stability, formation, noise or horizon "
                "robustness, internal S1, work, or mass"
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
        "# Scalar-memory rotating-wave interval certificate",
        "",
        f"Generated: {payload['generated_utc']}.",
        "",
        f"Decision: **{payload['decision']}**.",
        "",
        "The candidate was evaluated from clean prospective revision",
        f"{payload['execution_revision']} with mpmath {payload['dependency']['mpmath']}.",
        "",
    ]
    if payload["exception"] is not None:
        lines.extend(["Execution exception:", "", payload["exception"], ""])
        return "\n".join(lines)

    lines.extend(
        [
            "## Precision panels",
            "",
            "| dps | outer | inner | point residual | inner K width pass | panel |",
            "| ---: | :---: | :---: | ---: | :---: | :---: |",
        ]
    )
    for panel in payload["panels"]:
        lines.append(
            "| "
            f"{panel['precision_dps']} | {panel['gates']['outer_certificate']} | "
            f"{panel['gates']['inner_certificate']} | "
            f"{_fmt(panel['point_residual_maximum'])} | "
            f"{panel['gates']['inner_image_width']} | {panel['pass']} |"
        )
    lines.extend(
        [
            "",
            "## Certified root enclosure",
            "",
        ]
    )
    if payload["certified_intersection"] is not None:
        for coordinate in ("radius", "theta"):
            record = payload["certified_intersection"][coordinate]
            lines.extend(
                [
                    f"- {coordinate}: [{record['lower']}, {record['upper']}]",
                    f"  (displayed width {_fmt(record['width'])})",
                ]
            )
    lines.extend(
        [
            "",
            "Cross-precision refined-center differences:",
            "",
            f"- radius: {_fmt(payload['cross_panel']['radius_difference'])}",
            f"- theta: {_fmt(payload['cross_panel']['theta_difference'])}",
            "",
            "Every machine-readable interval stores exact binary endpoint tuples;",
            "the decimal enclosure above is a readability rendering.",
            "",
            "## Claim boundary",
            "",
            "A pass certifies one unique exact zero of the two finite-H balance",
            "equations in the registered box. It does not certify the omitted",
            "full stability spectrum, formation, noise or horizon robustness,",
            "an internal phase, physical work or mass.",
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
