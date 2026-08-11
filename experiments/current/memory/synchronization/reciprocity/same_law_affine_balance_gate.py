"""P3.7b: test affine force balance at same-law complex-Jacobian geometries."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import subprocess
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from emergenz_knoten import (
    FiniteMemoryState,
    compact_two_scale_same_law_compatibility,
    double_gaussian_gradient,
    load_finite_memory_checkpoint,
    memory_centroid,
    memory_shape_tensor,
    place_finite_memory_state,
)
from emergenz_knoten.kernels import effective_double_gaussian_parameters


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
DEFAULT_AUDIT = Path(
    "reports/response/reciprocal/"
    "same_law_reciprocal_jacobian_audit_2026-08-11.json"
)
DEFAULT_SCALE = Path(
    "reports/response/reciprocal/"
    "same_law_common_scale_followup_2026-08-11.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-json", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument("--scale-json", type=Path, default=DEFAULT_SCALE)
    parser.add_argument("--memory-time-radius-limit", type=float, default=0.01)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/response/reciprocal/"
            "same_law_affine_balance_gate_2026-08-11.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/reciprocal/"
            "same_law_affine_balance_gate_2026-08-11.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/"
            "same_law_affine_balance_gate_2026-08-11.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _relative_from(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _git(arguments: list[str]) -> str:
    try:
        return subprocess.run(
            ["git", *arguments],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return _jsonable(value.tolist())
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, (float, np.floating)):
        number = float(value)
        return number if np.isfinite(number) else None
    if isinstance(value, Path):
        return _relative(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _centered_clone(state: FiniteMemoryState) -> FiniteMemoryState:
    center = memory_centroid(state)
    return FiniteMemoryState(
        x=state.x - center,
        memory=state.memory - center[None, :],
        weights=state.weights,
    )


def _cross_gradient(point: np.ndarray, state: FiniteMemoryState, config: Any) -> np.ndarray:
    return double_gaussian_gradient(
        point,
        state.memory,
        state.weights,
        sigma_rep=config.sigma_rep,
        sigma_att=config.sigma_att,
        amplitude_rep=config.amplitude_rep,
        amplitude_att=config.amplitude_att,
        deposition_kernel=config.deposition_kernel,
        deposition_sigma=config.deposition_sigma,
    )


def analyse(
    audit: dict[str, Any],
    scale: dict[str, Any],
    *,
    memory_time_radius_limit: float,
) -> dict[str, Any]:
    if not math.isfinite(memory_time_radius_limit) or memory_time_radius_limit <= 0.0:
        raise ValueError("memory_time_radius_limit must be positive and finite")
    eligible_scale = {
        str(row["distance_label"]): row
        for row in scale["distances"]
        if bool(row["all_full_modes_pass"])
    }
    rows: list[dict[str, Any]] = []
    point_force_crossings: list[dict[str, Any]] = []

    for case in audit["cases"]:
        checkpoint = load_finite_memory_checkpoint(_resolve(Path(case["checkpoint"])))
        state = _centered_clone(checkpoint.state)
        config = checkpoint.config
        memory_radius = float(np.sqrt(np.trace(memory_shape_tensor(state))))
        effective = effective_double_gaussian_parameters(
            dim=config.dim,
            sigma_rep=config.sigma_rep,
            sigma_att=config.sigma_att,
            amplitude_rep=config.amplitude_rep,
            amplitude_att=config.amplitude_att,
            deposition_kernel=config.deposition_kernel,
            deposition_sigma=config.deposition_sigma,
        )
        compatibility = compact_two_scale_same_law_compatibility(
            amplitude_rep=float(effective["amplitude_rep"]),
            length_rep=float(effective["sigma_rep"]),
            amplitude_att=float(effective["amplitude_att"]),
            length_att=float(effective["sigma_att"]),
        )
        point_force_crossings.append(
            {
                "dim": config.dim,
                "seed": checkpoint.formation_seed,
                "repulsive_curvature_scale": compatibility.repulsive_curvature_scale,
                "attractive_curvature_scale": compatibility.attractive_curvature_scale,
                "self_restoring_curvature": compatibility.self_restoring_curvature,
                "self_restoring": compatibility.self_restoring,
                "radius": compatibility.force_crossing_radius,
                "finite_pair_balance": compatibility.finite_pair_balance,
                "jointly_compatible": compatibility.jointly_compatible,
            }
        )

        for audit_row in case["rows"]:
            label = str(audit_row["distance_label"])
            if label not in eligible_scale:
                continue
            eta = float(eligible_scale[label]["midpoint_eta"])
            separation = float(audit_row["distance"]) * np.asarray(
                audit_row["direction"], dtype=float
            )
            first = place_finite_memory_state(state, -0.5 * separation)
            second = place_finite_memory_state(state, 0.5 * separation)
            first_gradient = _cross_gradient(first.x, second, config)
            second_gradient = _cross_gradient(second.x, first, config)
            relative_drift = -0.5 * eta * (first_gradient - second_gradient)
            drift_norm = float(np.linalg.norm(relative_drift))
            distance = float(np.linalg.norm(separation))
            per_distance = drift_norm / distance
            per_memory_time_radius = drift_norm / (config.alpha * memory_radius)
            rows.append(
                {
                    "distance_label": label,
                    "dim": config.dim,
                    "seed": checkpoint.formation_seed,
                    "axis": int(audit_row["axis"]),
                    "eta": eta,
                    "distance": distance,
                    "memory_radius": memory_radius,
                    "first_cross_gradient": first_gradient,
                    "second_cross_gradient": second_gradient,
                    "relative_affine_drift": relative_drift,
                    "drift_norm": drift_norm,
                    "drift_over_distance_per_update": per_distance,
                    "frozen_memory_time_drift_over_radius": per_memory_time_radius,
                    "passes_balance": per_memory_time_radius <= memory_time_radius_limit,
                }
            )

    labels = list(eligible_scale)
    distance_results: list[dict[str, Any]] = []
    for label in labels:
        selected = [row for row in rows if row["distance_label"] == label]
        distance_results.append(
            {
                "distance_label": label,
                "row_count": len(selected),
                "pass_count": sum(bool(row["passes_balance"]) for row in selected),
                "all_pass": bool(selected)
                and all(bool(row["passes_balance"]) for row in selected),
                "minimum_memory_time_drift_over_radius": min(
                    float(row["frozen_memory_time_drift_over_radius"])
                    for row in selected
                ),
                "median_memory_time_drift_over_radius": float(
                    np.median(
                        [
                            row["frozen_memory_time_drift_over_radius"]
                            for row in selected
                        ]
                    )
                ),
                "maximum_memory_time_drift_over_radius": max(
                    float(row["frozen_memory_time_drift_over_radius"])
                    for row in selected
                ),
            }
        )

    if any(bool(row["all_pass"]) for row in distance_results):
        decision = "affine-balance-eligible"
    elif all(not bool(row["jointly_compatible"]) for row in point_force_crossings):
        decision = "affine-balance-negative"
    else:
        decision = "inconclusive"
    return {
        "decision": decision,
        "memory_time_radius_limit": memory_time_radius_limit,
        "distance_results": distance_results,
        "rows": rows,
        "point_force_crossings": point_force_crossings,
    }


def _plot(payload: dict[str, Any], output: Path) -> None:
    labels = [row["distance_label"] for row in payload["distance_results"]]
    fig, axis = plt.subplots(figsize=(8.8, 4.8))
    for index, label in enumerate(labels):
        values = np.asarray(
            [
                row["frozen_memory_time_drift_over_radius"]
                for row in payload["rows"]
                if row["distance_label"] == label
            ],
            dtype=float,
        )
        jitter = np.linspace(-0.16, 0.16, values.size)
        axis.scatter(
            np.full(values.size, index) + jitter,
            values,
            color="#D55E00",
            alpha=0.75,
            s=26,
        )
        axis.plot(
            [index - 0.2, index + 0.2],
            [float(np.median(values)), float(np.median(values))],
            color="black",
            linewidth=1.8,
        )
    axis.axhline(
        payload["memory_time_radius_limit"],
        color="#0072B2",
        linestyle="--",
        label="balance gate",
    )
    axis.set_yscale("log")
    axis.set_xticks(range(len(labels)), labels, rotation=25, ha="right")
    axis.set_ylabel(r"frozen drift per memory time / $R_{mem}$")
    axis.set_title("Affine drift at same-law complex-Jacobian geometries")
    axis.grid(alpha=0.2, which="both")
    axis.legend()
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    lines = [
        "# Same-law affine-balance gate",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        f"**Decision: `{payload['decision']}`.**",
        "",
        "This registered post-Jacobian gate tests the affine residual omitted by",
        "a curvature-only mode classification.",
        "",
        f"![Affine-balance gate]({_relative_from(report, figure)})",
        "",
        "## Results",
        "",
        "| distance | fixed eta | frozen drift / R_mem per memory time min..median..max | balance pass |",
        "|---|---:|---:|---:|",
    ]
    for distance in payload["distance_results"]:
        selected = [
            row
            for row in payload["rows"]
            if row["distance_label"] == distance["distance_label"]
        ]
        eta = float(selected[0]["eta"])
        lines.append(
            f"| `{distance['distance_label']}` | {eta:.8g} | "
            f"{distance['minimum_memory_time_drift_over_radius']:.6g}.."
            f"{distance['median_memory_time_drift_over_radius']:.6g}.."
            f"{distance['maximum_memory_time_drift_over_radius']:.6g} | "
            f"{distance['pass_count']}/{distance['row_count']} |"
        )
    crossing_text = ", ".join(
        f"d={row['dim']}: {row['radius'] if row['radius'] is not None else 'none'}"
        for row in payload["point_force_crossings"]
    )
    lines.extend(
        [
            "",
            f"Point-deposit positive force-zero radius: {crossing_text}.",
            "",
            "For the compact point limit, self-confinement requires",
            "`A_att/L_att^2 > A_rep/L_rep^2`, whereas a positive two-scale",
            "force-zero radius requires the strict opposite inequality. The",
            "same scalar two-Gaussian law cannot satisfy both conditions.",
            "",
            "## Interpretation",
            "",
            "The previously identified complex Jacobian windows are not stationary",
            "normal modes under the unchanged same-law kernel. Their expansion",
            "points carry a finite relative drift, and the point-deposit kernel has",
            "no non-zero force-balance radius. A nonlinear low-g oscillation pilot",
            "is therefore blocked.",
            "",
            "This does not rule out transient curved response or a balance supplied",
            "by a distinct charge/sign channel, screening, retardation, more nodes or",
            "another dynamical field. Such a term would be a new mechanism and must",
            "be specified before its parameters are estimated.",
            "",
            "## Reproducibility",
            "",
            f"- Jacobian input: `{payload['audit_json']}`;",
            f"- common-scale input: `{payload['scale_json']}`;",
            f"- revision: `{payload['git_revision']}`;",
            f"- worktree at execution: `{payload['git_status'] or 'clean'}`;",
            f"- JSON: `{_relative(payload['summary_json'])}`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    audit_path = _resolve(args.audit_json)
    scale_path = _resolve(args.scale_json)
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    scale = json.loads(scale_path.read_text(encoding="utf-8"))
    result = analyse(
        audit,
        scale,
        memory_time_radius_limit=args.memory_time_radius_limit,
    )
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    payload = {
        "schema": "emergenz-knoten.same-law-affine-balance-gate.v1",
        "created_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_revision": _git(["rev-parse", "HEAD"]),
        "git_status": _git(["status", "--porcelain"]),
        "audit_json": _relative(audit_path),
        "scale_json": _relative(scale_path),
        "summary_json": summary,
        **result,
    }
    _plot(payload, figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(_report(payload, report, figure), encoding="utf-8")
    summary.write_text(
        json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"decision": payload["decision"], "distances": payload["distance_results"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
