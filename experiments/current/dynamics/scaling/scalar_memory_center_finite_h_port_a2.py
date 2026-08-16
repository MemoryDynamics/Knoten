"""Certify the preregistered finite-H scalar-memory center port."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
import json
import math
from pathlib import Path
import subprocess
from typing import Any

import numpy as np


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
DEFAULT_REPORT = Path(
    "reports/dynamics/limits/scalar_memory_center_finite_h_port_a2_2026-08-16.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/limits/scalar_memory_center_finite_h_port_a2_2026-08-16.json"
)
PREREGISTRATION = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_center_finite_h_port_a2_protocol_2026-08-16.md"
)
P0_MANIFEST = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_center_mechanics_p0_manifest_2026-08-16.json"
)

ALPHA_VALUES = (0.04, 0.02, 0.01, 0.005, 0.0025)
TAIL_EXTENT = 12.0
CHI = 4.0
GRID_SIZE = 131_073
SAFETY_FACTOR_MINIMUM = 10.0
FLOAT_TOLERANCE = 5.0e-13


@dataclass(frozen=True)
class FiniteHCertificate:
    """One analytic and numerical finite-memory passivity certificate."""

    alpha: float
    horizon: int
    q: float
    tail_fraction: float
    restoring_per_update: float
    untruncated_relative_root: float
    truncated_mean_age_updates: float
    exact_dc_gain: float
    untruncated_real_part_lower_bound: float
    untruncated_magnitude_upper_bound: float
    multiplicative_tail_bound: float
    small_gain_loop_bound: float
    finite_h_transfer_error_bound: float
    certified_real_part_lower_bound: float
    certificate_safety_factor: float
    grid_minimum_real_part: float
    grid_minimum_frequency: float
    grid_maximum_transfer_error: float
    grid_maximum_loop_gain: float
    small_gain_stability_pass: bool
    strict_positive_real_pass: bool
    safety_factor_pass: bool
    grid_bound_sanity_pass: bool
    grid_positive_real_sanity_pass: bool
    decision: str


def _positive_finite(name: str, value: float) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be positive and finite")
    return number


def finite_h_parameters(
    *, alpha: float, tail_extent: float, chi: float
) -> tuple[float, int, float, float, float]:
    """Return ``q, H, q**H, g, a`` for one matched finite-memory case."""

    step = _positive_finite("alpha", alpha)
    if step >= 1.0:
        raise ValueError("alpha must be smaller than one")
    extent = _positive_finite("tail_extent", tail_extent)
    restoring = _positive_finite("chi", chi)
    q = 1.0 - step
    horizon = max(1, int(math.ceil(extent / step - 1.0e-12)))
    tail = q**horizon
    gain = restoring * step
    relative_root = q * (1.0 - gain)
    if not 0.0 < relative_root < 1.0:
        raise ValueError("the untruncated relative root must lie in (0, 1)")
    return q, horizon, tail, gain, relative_root


def truncated_geometric_mean_age(*, q: float, horizon: int) -> float:
    """Return the normalized mean age of a finite geometric memory."""

    if not 0.0 < q < 1.0:
        raise ValueError("q must lie in (0, 1)")
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 1:
        raise ValueError("horizon must be a positive integer")
    tail = q**horizon
    return q / (1.0 - q) - horizon * tail / (1.0 - tail)


def _finite_h_transfer_grid(
    *, alpha: float, horizon: int, q: float, tail: float, gain: float, root: float
) -> dict[str, float]:
    frequencies = np.linspace(0.0, math.pi, GRID_SIZE, dtype=float)
    z = np.exp(1j * frequencies)
    transfer = np.empty(GRID_SIZE, dtype=np.complex128)
    untruncated = alpha * z / (z - root)
    loop = np.empty_like(transfer)

    mean_age = truncated_geometric_mean_age(q=q, horizon=horizon)
    transfer[0] = 1.0 / (1.0 + gain * mean_age)
    untruncated_dc = alpha / (1.0 - root)
    loop[0] = gain * untruncated_dc * tail * horizon / (1.0 - tail)

    z_tail = z[1:] ** (-horizon)
    memory_filter = alpha / (1.0 - tail) * (1.0 - tail * z_tail) / (1.0 - q / z[1:])
    denominator = z[1:] - (1.0 - gain) - gain * memory_filter
    transfer[1:] = (z[1:] - 1.0) * memory_filter / denominator
    multiplicative_tail = tail * (1.0 - z_tail) / (1.0 - tail)
    loop[1:] = gain * untruncated[1:] * multiplicative_tail / (z[1:] - 1.0)

    real_parts = np.real(transfer)
    minimum_index = int(np.argmin(real_parts))
    return {
        "minimum_real_part": float(real_parts[minimum_index]),
        "minimum_frequency": float(frequencies[minimum_index]),
        "maximum_transfer_error": float(np.max(np.abs(transfer - untruncated))),
        "maximum_loop_gain": float(np.max(np.abs(loop))),
    }


def certify_case(
    *, alpha: float, tail_extent: float = TAIL_EXTENT, chi: float = CHI
) -> FiniteHCertificate:
    """Return the registered global finite-H positive-real certificate."""

    q, horizon, tail, gain, root = finite_h_parameters(
        alpha=alpha, tail_extent=tail_extent, chi=chi
    )
    mean_age = truncated_geometric_mean_age(q=q, horizon=horizon)
    dc_gain = 1.0 / (1.0 + gain * mean_age)

    untruncated_real_lower = alpha / (1.0 + root)
    untruncated_magnitude_upper = alpha / (1.0 - root)
    tail_bound = 2.0 * tail / (1.0 - tail)
    loop_bound = gain * untruncated_magnitude_upper * tail * horizon / (1.0 - tail)
    if loop_bound >= 1.0:
        transfer_error_bound = math.inf
    else:
        transfer_error_bound = (
            untruncated_magnitude_upper * (tail_bound + loop_bound) / (1.0 - loop_bound)
        )
    finite_real_lower = untruncated_real_lower - transfer_error_bound
    safety_factor = (
        untruncated_real_lower / transfer_error_bound
        if transfer_error_bound > 0.0
        else math.inf
    )
    grid = _finite_h_transfer_grid(
        alpha=alpha,
        horizon=horizon,
        q=q,
        tail=tail,
        gain=gain,
        root=root,
    )

    small_gain_pass = loop_bound < 1.0
    positive_real_pass = finite_real_lower > 0.0
    safety_pass = safety_factor >= SAFETY_FACTOR_MINIMUM
    grid_bound_pass = (
        grid["maximum_transfer_error"]
        <= transfer_error_bound * (1.0 + FLOAT_TOLERANCE) + FLOAT_TOLERANCE
        and grid["maximum_loop_gain"]
        <= loop_bound * (1.0 + FLOAT_TOLERANCE) + FLOAT_TOLERANCE
    )
    grid_positive_pass = grid["minimum_real_part"] > 0.0
    passed = all(
        (
            small_gain_pass,
            positive_real_pass,
            safety_pass,
            grid_bound_pass,
            grid_positive_pass,
        )
    )
    return FiniteHCertificate(
        alpha=alpha,
        horizon=horizon,
        q=q,
        tail_fraction=tail,
        restoring_per_update=gain,
        untruncated_relative_root=root,
        truncated_mean_age_updates=mean_age,
        exact_dc_gain=dc_gain,
        untruncated_real_part_lower_bound=untruncated_real_lower,
        untruncated_magnitude_upper_bound=untruncated_magnitude_upper,
        multiplicative_tail_bound=tail_bound,
        small_gain_loop_bound=loop_bound,
        finite_h_transfer_error_bound=transfer_error_bound,
        certified_real_part_lower_bound=finite_real_lower,
        certificate_safety_factor=safety_factor,
        grid_minimum_real_part=grid["minimum_real_part"],
        grid_minimum_frequency=grid["minimum_frequency"],
        grid_maximum_transfer_error=grid["maximum_transfer_error"],
        grid_maximum_loop_gain=grid["maximum_loop_gain"],
        small_gain_stability_pass=small_gain_pass,
        strict_positive_real_pass=positive_real_pass,
        safety_factor_pass=safety_pass,
        grid_bound_sanity_pass=grid_bound_pass,
        grid_positive_real_sanity_pass=grid_positive_pass,
        decision="pass" if passed else "fail",
    )


def _git_output(arguments: list[str]) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return completed.stdout.strip()


def run_gate() -> dict[str, Any]:
    """Run the deterministic registered family without opening holdout data."""

    cases = [asdict(certify_case(alpha=alpha)) for alpha in ALPHA_VALUES]
    passed = all(case["decision"] == "pass" for case in cases)
    return {
        "schema": "emergenz-knoten.scalar-memory-center-finite-h-port-a2",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "simulation_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "preregistration": PREREGISTRATION.as_posix(),
        "p0_manifest": P0_MANIFEST.as_posix(),
        "registration": {
            "alpha_values": ALPHA_VALUES,
            "tail_extent": TAIL_EXTENT,
            "chi": CHI,
            "frequency_grid_size_non_decisional": GRID_SIZE,
            "certificate_safety_factor_minimum": SAFETY_FACTOR_MINIMUM,
            "float_tolerance": FLOAT_TOLERANCE,
            "sealed_holdout_opened": False,
            "stochastic_target_data_opened": False,
        },
        "analytic_contract": {
            "finite_memory_filter": ("B_H(z)=alpha/(1-q^H)*(1-q^H*z^-H)/(1-q*z^-1)"),
            "center_velocity_transfer": ("G_H(z)=(z-1)*B_H(z)/[z-(1-g)-g*B_H(z)]"),
            "untruncated_transfer": "G_inf(z)=alpha*z/[z-q*(1-g)]",
            "supply": "u_n dot (c_{n+1}-c_n)",
            "reciprocal_interaction": (
                "discrete-gradient U_ext(c_H,Q) with equal-and-opposite "
                "center/external work"
            ),
        },
        "cases": cases,
        "gates": {
            "all_small_gain_stable": all(
                case["small_gain_stability_pass"] for case in cases
            ),
            "all_strict_positive_real": all(
                case["strict_positive_real_pass"] for case in cases
            ),
            "all_safety_factors": all(case["safety_factor_pass"] for case in cases),
            "all_grid_sanity_checks": all(
                case["grid_bound_sanity_pass"]
                and case["grid_positive_real_sanity_pass"]
                for case in cases
            ),
        },
        "decision": (
            "finite-h-effective-center-port-pass"
            if passed
            else "finite-h-effective-center-port-fail"
        ),
        "claim_boundary": {
            "established_if_pass": (
                "global finite-H passivity and a reciprocal effective port "
                "realization for the registered linear local plant"
            ),
            "not_established": (
                "material COM, microscopic actuator selection, SI mass, "
                "or additive two-node momentum"
            ),
            "downstream_if_pass": (
                "B-star filter scaling authorized; physical B remains blocked"
            ),
            "s1_branch": "sealed-no-s1-candidate",
        },
    }


def _fmt(value: float) -> str:
    return f"{value:.8g}"


def render_report(payload: dict[str, Any]) -> str:
    lines = [
        "# Finite-H center-port Gate A2",
        "",
        f"Generated: {payload['generated_utc']}.",
        "",
        f"Decision: **`{payload['decision']}`**.",
        "",
        "This deterministic certificate was run from the clean preregistered",
        f"revision `{payload['simulation_revision']}`. No stochastic target",
        "trace, new seed, or sealed transfer cell was opened.",
        "",
        "## Registered finite-memory certificate",
        "",
        "For the normalized finite geometric memory,",
        "",
        r"\[",
        r"B_H(z)={\alpha\over1-q^H}{1-q^Hz^{-H}\over1-qz^{-1}},",
        r"\qquad",
        r"G_H(z)={(z-1)B_H(z)\over z-(1-g)-gB_H(z)}.",
        r"\]",
        "",
        "The report uses a global analytic perturbation bound from",
        r"\(G_\infty(z)=\alpha z/[z-q(1-g)]\). The dense frequency grid is",
        "only a sanity check and cannot decide the gate.",
        "",
        "| alpha | H | q^H | small-gain bound | certified min Re G_H | safety | grid min Re G_H | decision |",
        "|---:|---:|---:|---:|---:|---:|---:|:---:|",
    ]
    for case in payload["cases"]:
        lines.append(
            "| "
            f"{_fmt(case['alpha'])} | {case['horizon']} | "
            f"{_fmt(case['tail_fraction'])} | "
            f"{_fmt(case['small_gain_loop_bound'])} | "
            f"{_fmt(case['certified_real_part_lower_bound'])} | "
            f"{_fmt(case['certificate_safety_factor'])} | "
            f"{_fmt(case['grid_minimum_real_part'])} | "
            f"{case['decision']} |"
        )
    lines.extend(
        [
            "",
            "## Decision boundary",
            "",
            "A pass establishes an exact passive finite-H input/output",
            "realization for the registered local linear plant and permits a",
            "reciprocal discrete-gradient wrapper. It does not identify the",
            "memory centroid as material mass or derive a microscopic natural",
            "actuator. Consequently only the separately labelled B-star filter",
            "scaling study is authorized; physical B remains blocked.",
            "",
            "The S1 branch remains sealed because this real-pole center plant is",
            "not an S1 candidate.",
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
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Decision: {payload['decision']}")
    print(f"Report: {report_path.relative_to(ROOT)}")
    print(f"Summary: {summary_path.relative_to(ROOT)}")
    raise SystemExit(0 if payload["decision"].endswith("-pass") else 1)


if __name__ == "__main__":
    main()
