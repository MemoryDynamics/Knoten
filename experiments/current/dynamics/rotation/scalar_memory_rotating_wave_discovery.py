"""Run the prospectively frozen scalar-memory rotating-wave discovery."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import math
from pathlib import Path
import subprocess
from typing import Any

import numpy as np
from scipy.optimize import brentq, least_squares

from emergenz_knoten.rotating_wave import (
    continuum_required_eta_per_alpha,
    continuum_rotating_wave_components,
    double_gaussian_force_crossing_radius,
    finite_h_rotating_wave_balance,
    finite_h_rotating_wave_residual,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_discovery_protocol_2026-08-20.md"
)
DEFAULT_REPORT = Path(
    "reports/dynamics/rotation/scalar_memory_rotating_wave_discovery_2026-08-20.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/scalar_memory_rotating_wave_discovery_2026-08-20.json"
)

MECHANISM_AMPLITUDES = (3.5, 5.5, 6.5, 7.5, 8.0, 8.5)
CONTROL_AMPLITUDES = (0.0, 9.0, 35.0)
ALL_AMPLITUDES = (*MECHANISM_AMPLITUDES, *CONTROL_AMPLITUDES)
TAIL_EXTENT = 12.0
SENSITIVITY_TAIL_EXTENT = 6.0
OMEGA_VALUES = np.geomspace(0.05, 8.0, 161)
RADIUS_VALUES = np.geomspace(0.05, 6.0, 241)
QUADRATURE_ORDER = 512
CONVERGENCE_QUADRATURE_ORDER = 256
RADIAL_ROOT_TOLERANCE = 1.0e-12
RADIAL_ACCEPTANCE_TOLERANCE = 1.0e-10
QUADRATURE_DISCREPANCY_TOLERANCE = 1.0e-8
FINITE_ALPHA = 0.01
FINITE_HORIZON = 1200
FINITE_ETA = 0.15
FINITE_RESIDUAL_TOLERANCE = 1.0e-11
MAX_FINITE_INITIALIZERS = 20
MEMORY_MASS = 1.0
SIGMA_REP = 1.0
SIGMA_ATT = 3.0
AMPLITUDE_REP = 1.0


def _git_output(arguments: list[str]) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return result.stdout.strip()


def _components(
    radius: float,
    omega: float,
    amplitude_att: float,
    *,
    extent: float = TAIL_EXTENT,
    order: int = QUADRATURE_ORDER,
):
    return continuum_rotating_wave_components(
        radius=radius,
        angular_frequency=omega,
        tail_extent=extent,
        memory_mass=MEMORY_MASS,
        sigma_rep=SIGMA_REP,
        sigma_att=SIGMA_ATT,
        amplitude_rep=AMPLITUDE_REP,
        amplitude_att=amplitude_att,
        quadrature_order=order,
    )


def _continuum_row(
    *,
    amplitude_att: float,
    omega: float,
    radius: float,
    lower_radius: float,
    upper_radius: float,
) -> dict[str, Any]:
    primary = _components(radius, omega, amplitude_att)
    convergence = _components(
        radius,
        omega,
        amplitude_att,
        order=CONVERGENCE_QUADRATURE_ORDER,
    )
    discrepancy = max(
        abs(primary.radial - convergence.radial),
        abs(primary.tangential - convergence.tangential),
    )
    eta_rate = continuum_required_eta_per_alpha(
        radius=radius,
        angular_frequency=omega,
        tail_extent=TAIL_EXTENT,
        memory_mass=MEMORY_MASS,
        sigma_rep=SIGMA_REP,
        sigma_att=SIGMA_ATT,
        amplitude_rep=AMPLITUDE_REP,
        amplitude_att=amplitude_att,
        quadrature_order=QUADRATURE_ORDER,
    )
    serialized_eta_rate = float(eta_rate) if math.isfinite(eta_rate) else None
    crossing = double_gaussian_force_crossing_radius(
        sigma_rep=SIGMA_REP,
        sigma_att=SIGMA_ATT,
        amplitude_rep=AMPLITUDE_REP,
        amplitude_att=amplitude_att,
    )
    admissible = bool(
        abs(primary.radial) <= RADIAL_ACCEPTANCE_TOLERANCE
        and primary.tangential < 0.0
        and math.isfinite(eta_rate)
        and eta_rate > 0.0
        and discrepancy <= QUADRATURE_DISCREPANCY_TOLERANCE
    )
    return {
        "amplitude_att": float(amplitude_att),
        "angular_frequency_per_memory_time": float(omega),
        "radius_over_sigma_rep": float(radius),
        "radial_integral": primary.radial,
        "tangential_integral": primary.tangential,
        "required_eta_per_alpha": serialized_eta_rate,
        "force_crossing_radius": crossing,
        "radial_bracket": [float(lower_radius), float(upper_radius)],
        "quadrature_discrepancy_256_vs_512": float(discrepancy),
        "admissible": admissible,
    }


def scan_continuum_roots() -> list[dict[str, Any]]:
    """Return every registered sign-changing radial root."""

    rows: list[dict[str, Any]] = []
    for amplitude_att in ALL_AMPLITUDES:
        for omega in OMEGA_VALUES:
            values = np.asarray(
                [
                    _components(float(radius), float(omega), amplitude_att).radial
                    for radius in RADIUS_VALUES
                ]
            )
            roots_for_frequency: list[float] = []
            for index in range(RADIUS_VALUES.size - 1):
                lower = float(RADIUS_VALUES[index])
                upper = float(RADIUS_VALUES[index + 1])
                lower_value = float(values[index])
                upper_value = float(values[index + 1])
                if lower_value == 0.0:
                    root_radius = lower
                elif lower_value * upper_value < 0.0:
                    root_radius = float(
                        brentq(
                            lambda radius: (
                                _components(radius, float(omega), amplitude_att).radial
                            ),
                            lower,
                            upper,
                            xtol=RADIAL_ROOT_TOLERANCE,
                            rtol=4.0 * np.finfo(float).eps,
                        )
                    )
                else:
                    continue
                if any(
                    abs(root_radius - previous) <= 10.0 * RADIAL_ROOT_TOLERANCE
                    for previous in roots_for_frequency
                ):
                    continue
                roots_for_frequency.append(root_radius)
                rows.append(
                    _continuum_row(
                        amplitude_att=amplitude_att,
                        omega=float(omega),
                        radius=root_radius,
                        lower_radius=lower,
                        upper_radius=upper,
                    )
                )
    return rows


def _finite_refinement(
    continuum_row: dict[str, Any],
) -> dict[str, Any]:
    amplitude_att = float(continuum_row["amplitude_att"])
    initial_radius = float(continuum_row["radius_over_sigma_rep"])
    initial_omega = float(continuum_row["angular_frequency_per_memory_time"])

    def residual(log_variables: np.ndarray) -> np.ndarray:
        radius, omega = np.exp(log_variables)
        theta = FINITE_ALPHA * omega
        value = finite_h_rotating_wave_residual(
            radius=float(radius),
            theta=float(theta),
            alpha=FINITE_ALPHA,
            horizon=FINITE_HORIZON,
            memory_mass=MEMORY_MASS,
            sigma_rep=SIGMA_REP,
            sigma_att=SIGMA_ATT,
            amplitude_rep=AMPLITUDE_REP,
            amplitude_att=amplitude_att,
            eta=FINITE_ETA,
        )
        return np.asarray([value.real, value.imag])

    result = least_squares(
        residual,
        x0=np.log([initial_radius, initial_omega]),
        bounds=(
            np.log([float(RADIUS_VALUES[0]), float(OMEGA_VALUES[0])]),
            np.log([float(RADIUS_VALUES[-1]), float(OMEGA_VALUES[-1])]),
        ),
        xtol=1.0e-13,
        ftol=1.0e-13,
        gtol=1.0e-13,
        max_nfev=2000,
    )
    radius, omega = np.exp(result.x)
    theta = FINITE_ALPHA * omega
    exact_residual = residual(result.x)
    residual_norm = float(np.linalg.norm(exact_residual))
    balance = finite_h_rotating_wave_balance(
        radius=float(radius),
        theta=float(theta),
        alpha=FINITE_ALPHA,
        horizon=FINITE_HORIZON,
        memory_mass=MEMORY_MASS,
        sigma_rep=SIGMA_REP,
        sigma_att=SIGMA_ATT,
        amplitude_rep=AMPLITUDE_REP,
        amplitude_att=amplitude_att,
    )
    in_box = bool(
        RADIUS_VALUES[0] <= radius <= RADIUS_VALUES[-1]
        and OMEGA_VALUES[0] <= omega <= OMEGA_VALUES[-1]
    )
    accepted = bool(
        result.success
        and in_box
        and residual_norm <= FINITE_RESIDUAL_TOLERANCE
        and balance.admissible_positive_eta
    )
    return {
        "initializer": continuum_row,
        "solver_success": bool(result.success),
        "solver_message": str(result.message),
        "function_evaluations": int(result.nfev),
        "amplitude_att": amplitude_att,
        "radius": float(radius),
        "angular_frequency_per_memory_time": float(omega),
        "theta_per_update": float(theta),
        "alpha": FINITE_ALPHA,
        "horizon": FINITE_HORIZON,
        "eta": FINITE_ETA,
        "memory_mass": MEMORY_MASS,
        "sigma_rep": SIGMA_REP,
        "sigma_att": SIGMA_ATT,
        "amplitude_rep": AMPLITUDE_REP,
        "epsilon": 0.0,
        "dimension": 2,
        "deposition_kernel": "delta",
        "residual_real": float(exact_residual[0]),
        "residual_imag": float(exact_residual[1]),
        "residual_norm": residual_norm,
        "radial_history_sum": balance.components.radial,
        "tangential_history_sum": balance.components.tangential,
        "radial_eta": balance.radial_eta,
        "tangential_eta": balance.tangential_eta,
        "compatibility_residual": balance.compatibility_residual,
        "accepted": accepted,
    }


def select_and_refine_candidate(
    continuum_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    admissible = [
        row
        for row in continuum_rows
        if row["admissible"] and row["amplitude_att"] in MECHANISM_AMPLITUDES
    ]
    admissible.sort(
        key=lambda row: (
            abs(math.log(row["required_eta_per_alpha"] / 15.0)),
            row["amplitude_att"],
            row["angular_frequency_per_memory_time"],
            row["radius_over_sigma_rep"],
        )
    )
    attempts: list[dict[str, Any]] = []
    selected = None
    for row in admissible[:MAX_FINITE_INITIALIZERS]:
        attempt = _finite_refinement(row)
        attempts.append(attempt)
        if attempt["accepted"]:
            selected = attempt
            break
    return attempts, selected


def _amplitude_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary = []
    for amplitude in ALL_AMPLITUDES:
        selected = [row for row in rows if row["amplitude_att"] == amplitude]
        admissible = [row for row in selected if row["admissible"]]
        eta_rates = [row["required_eta_per_alpha"] for row in admissible]
        summary.append(
            {
                "amplitude_att": amplitude,
                "force_sign_change": amplitude in MECHANISM_AMPLITUDES,
                "radial_root_count": len(selected),
                "admissible_root_count": len(admissible),
                "minimum_required_eta_per_alpha": (
                    min(eta_rates) if eta_rates else None
                ),
                "maximum_required_eta_per_alpha": (
                    max(eta_rates) if eta_rates else None
                ),
            }
        )
    return summary


def run_discovery() -> dict[str, Any]:
    start_status = _git_output(["status", "--short"])
    if start_status:
        raise RuntimeError(
            "rotating-wave discovery requires a clean prospective revision"
        )
    revision = _git_output(["rev-parse", "HEAD"])
    rows = scan_continuum_roots()
    attempts, candidate = select_and_refine_candidate(rows)
    sensitivity = None
    if candidate is not None:
        components = _components(
            candidate["radius"],
            candidate["angular_frequency_per_memory_time"],
            candidate["amplitude_att"],
            extent=SENSITIVITY_TAIL_EXTENT,
        )
        eta_rate = continuum_required_eta_per_alpha(
            radius=candidate["radius"],
            angular_frequency=candidate["angular_frequency_per_memory_time"],
            tail_extent=SENSITIVITY_TAIL_EXTENT,
            memory_mass=MEMORY_MASS,
            sigma_rep=SIGMA_REP,
            sigma_att=SIGMA_ATT,
            amplitude_rep=AMPLITUDE_REP,
            amplitude_att=candidate["amplitude_att"],
            quadrature_order=QUADRATURE_ORDER,
        )
        sensitivity = {
            "tail_extent": SENSITIVITY_TAIL_EXTENT,
            "radial_integral": components.radial,
            "tangential_integral": components.tangential,
            "required_eta_per_alpha": (
                float(eta_rate) if math.isfinite(eta_rate) else None
            ),
            "used_for_selection": False,
        }
    return {
        "schema": "emergenz-knoten.scalar-memory-rotating-wave-discovery",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "simulation_revision": revision,
        "git_status_at_start": start_status,
        "protocol": PROTOCOL.as_posix(),
        "registration": {
            "mechanism_amplitudes": MECHANISM_AMPLITUDES,
            "control_amplitudes": CONTROL_AMPLITUDES,
            "sealed_amplitude_holdout": 7.0,
            "tail_extent": TAIL_EXTENT,
            "sensitivity_tail_extent_nonselecting": SENSITIVITY_TAIL_EXTENT,
            "omega_grid": {
                "minimum": float(OMEGA_VALUES[0]),
                "maximum": float(OMEGA_VALUES[-1]),
                "count": int(OMEGA_VALUES.size),
                "spacing": "geometric",
            },
            "radius_grid": {
                "minimum": float(RADIUS_VALUES[0]),
                "maximum": float(RADIUS_VALUES[-1]),
                "count": int(RADIUS_VALUES.size),
                "spacing": "geometric",
            },
            "quadrature_orders": [
                CONVERGENCE_QUADRATURE_ORDER,
                QUADRATURE_ORDER,
            ],
            "finite_refinement": {
                "alpha": FINITE_ALPHA,
                "horizon": FINITE_HORIZON,
                "eta": FINITE_ETA,
                "maximum_initializers": MAX_FINITE_INITIALIZERS,
            },
            "target_topology_opened": False,
            "stochastic_trajectory_opened": False,
        },
        "amplitude_summary": _amplitude_summary(rows),
        "continuum_roots": rows,
        "finite_refinement_attempts": attempts,
        "selected_candidate": candidate,
        "tail_extent_sensitivity": sensitivity,
        "decision": (
            "finite-h-rotating-wave-candidate-found"
            if candidate is not None
            else "no-finite-h-rotating-wave-candidate"
        ),
        "claim_boundary": {
            "established_if_candidate_found": (
                "one exact native finite-H rotating-wave residual root to "
                "floating-point tolerance"
            ),
            "not_established": (
                "interval-certified existence, stability, basin formation, "
                "internal S1 topology, physical work, or mass"
            ),
            "next_gate": (
                "commit candidate discovery artifacts and pass a new P0-S "
                "before candidate-targeted stability work"
            ),
        },
    }


def _fmt(value: Any) -> str:
    if value is None:
        return "--"
    return f"{float(value):.8g}"


def render_report(payload: dict[str, Any]) -> str:
    lines = [
        "# Scalar-memory rotating-wave discovery",
        "",
        f"Generated: {payload['generated_utc']}.",
        "",
        f"Decision: **{payload['decision']}**.",
        "",
        "This deterministic discovery was executed from clean revision",
        f"{payload['simulation_revision']}. No stochastic trajectory,",
        "topology statistic or sealed amplitude holdout was opened.",
        "",
        "## Continuum root inventory",
        "",
        "| A_att | force crossing | radial roots | admissible roots | min eta/alpha | max eta/alpha |",
        "| ---: | :---: | ---: | ---: | ---: | ---: |",
    ]
    for row in payload["amplitude_summary"]:
        lines.append(
            "| "
            f"{_fmt(row['amplitude_att'])} | "
            f"{'yes' if row['force_sign_change'] else 'no'} | "
            f"{row['radial_root_count']} | "
            f"{row['admissible_root_count']} | "
            f"{_fmt(row['minimum_required_eta_per_alpha'])} | "
            f"{_fmt(row['maximum_required_eta_per_alpha'])} |"
        )
    lines.extend(["", "## Finite-H selection", ""])
    candidate = payload["selected_candidate"]
    if candidate is None:
        lines.extend(
            [
                "No registered continuum initializer produced an accepted",
                "finite-H root at alpha=0.01, H=1200 and eta=0.15.",
            ]
        )
    else:
        lines.extend(
            [
                "| quantity | value |",
                "| --- | ---: |",
                f"| A_att | {_fmt(candidate['amplitude_att'])} |",
                f"| radius R | {_fmt(candidate['radius'])} |",
                f"| Omega=theta/alpha | {_fmt(candidate['angular_frequency_per_memory_time'])} |",
                f"| theta | {_fmt(candidate['theta_per_update'])} |",
                f"| alpha | {_fmt(candidate['alpha'])} |",
                f"| H | {candidate['horizon']} |",
                f"| eta | {_fmt(candidate['eta'])} |",
                f"| radial residual | {_fmt(candidate['residual_real'])} |",
                f"| tangential residual | {_fmt(candidate['residual_imag'])} |",
                f"| residual norm | {_fmt(candidate['residual_norm'])} |",
                f"| radial eta | {_fmt(candidate['radial_eta'])} |",
                f"| tangential eta | {_fmt(candidate['tangential_eta'])} |",
                "",
                "The C=6 calculation was performed only after this selection",
                "and did not enter the ordering.",
            ]
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "A candidate is only a floating-point residual root of the native",
            "finite-memory map. Stability, spontaneous formation, a genuine",
            "internal S1 phase, physical work and mass remain untested. The",
            "A_att=7.0 parameter holdout remains sealed.",
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
    payload = run_discovery()
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
