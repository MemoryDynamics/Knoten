"""P3.7a: audit self/cross Jacobians before any reciprocal gain retuning."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
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
    finite_memory_gain_matrix,
    load_finite_memory_checkpoint,
    memory_centroid,
    memory_shape_tensor,
    reciprocal_relative_mode_operator,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
DEFAULT_CHECKPOINTS = (
    Path(
        "data/processed/reference_states/"
        "scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16/"
        "scalar_Aatt35_d3_seed1_N100000000.npz"
    ),
    Path(
        "data/processed/reference_states/"
        "scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16/"
        "scalar_Aatt35_d10_seed1_N100000000.npz"
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkpoints",
        default=",".join(path.as_posix() for path in DEFAULT_CHECKPOINTS),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/response/reciprocal/"
            "same_law_reciprocal_jacobian_audit_2026-08-11.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/reciprocal/"
            "same_law_reciprocal_jacobian_audit_2026-08-11.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/"
            "same_law_reciprocal_jacobian_audit_2026-08-11.png"
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
    if isinstance(value, np.complexfloating):
        value = complex(value)
    if isinstance(value, complex):
        return {"real": float(value.real), "imag": float(value.imag)}
    if isinstance(value, Path):
        return _relative(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _centered_clone(state: FiniteMemoryState) -> tuple[FiniteMemoryState, np.ndarray]:
    center = memory_centroid(state)
    offset = state.x - center
    return (
        FiniteMemoryState(
            x=offset,
            memory=state.memory - center[None, :],
            weights=state.weights,
        ),
        offset,
    )


def _distance_rows(radius: float, sigma_rep: float, sigma_att: float) -> list[tuple[str, float]]:
    return [
        ("2.5_Rmem", 2.5 * radius),
        ("10_Rmem", 10.0 * radius),
        ("0.1_sigma_rep", 0.1 * sigma_rep),
        ("1_sigma_rep", sigma_rep),
        ("1_sigma_att", sigma_att),
    ]


def audit_checkpoint(path: Path) -> dict[str, Any]:
    checkpoint = load_finite_memory_checkpoint(path)
    state, visible_offset = _centered_clone(checkpoint.state)
    config = checkpoint.config
    radius = float(np.sqrt(np.trace(memory_shape_tensor(state))))
    self_gain = finite_memory_gain_matrix(state.x, state, config)
    self_gain = 0.5 * (self_gain + self_gain.T)
    self_values, self_vectors = np.linalg.eigh(self_gain)
    rows: list[dict[str, Any]] = []

    for distance_label, distance in _distance_rows(
        radius,
        config.sigma_rep,
        config.sigma_att,
    ):
        for axis in range(config.dim):
            direction = self_vectors[:, axis]
            target_point = visible_offset + distance * direction
            cross_gain = finite_memory_gain_matrix(target_point, state, config)
            cross_gain = 0.5 * (cross_gain + cross_gain.T)
            mode = reciprocal_relative_mode_operator(
                config.alpha,
                self_gain,
                cross_gain,
            )
            g_direction = float(direction @ self_gain @ direction)
            c_direction = float(direction @ cross_gain @ direction)
            ordering_excess = float(np.max(np.linalg.eigvalsh(cross_gain - self_gain)))
            tolerance = 1.0e-8 * max(
                1.0,
                float(np.linalg.norm(self_gain, ord=2)),
                float(np.linalg.norm(cross_gain, ord=2)),
            )
            rows.append(
                {
                    "distance_label": distance_label,
                    "distance": distance,
                    "distance_over_memory_radius": distance / radius,
                    "distance_over_sigma_rep": distance / config.sigma_rep,
                    "axis": axis,
                    "direction": direction,
                    "g_directional": g_direction,
                    "c_directional": c_direction,
                    "cross_gain_matrix": cross_gain,
                    "c_over_g": (
                        c_direction / g_direction
                        if abs(g_direction) > np.finfo(float).tiny
                        else np.nan
                    ),
                    "cross_minus_self_max_eigenvalue": ordering_excess,
                    "ordering_tolerance": tolerance,
                    "cross_leq_self": ordering_excess <= tolerance,
                    "spectral_radius": float(np.max(np.abs(mode.eigenvalues))),
                    "max_imaginary_part": float(np.max(np.abs(mode.eigenvalues.imag))),
                    "is_stable": mode.is_stable,
                    "has_complex_pair": mode.has_complex_pair,
                    "stable_complex": mode.is_stable and mode.has_complex_pair,
                    "eigenvalues": mode.eigenvalues,
                }
            )

    no_complex = not any(bool(row["stable_complex"]) for row in rows)
    ordered = all(bool(row["cross_leq_self"]) for row in rows)
    decision = (
        "same-law-eligible"
        if not no_complex
        else "same-law-negative"
        if ordered
        else "inconclusive"
    )
    return {
        "checkpoint": _relative(path),
        "dim": config.dim,
        "lambda": config.alpha,
        "eta": config.eta,
        "formation_seed": checkpoint.formation_seed,
        "update_index": checkpoint.update_index,
        "memory_radius": radius,
        "visible_offset_from_memory_center": visible_offset,
        "self_gain_matrix": self_gain,
        "self_gain_eigenvalues": self_values,
        "complex_window_self_gain_threshold": config.alpha / (1.0 + config.alpha),
        "rows": rows,
        "all_cross_leq_self": ordered,
        "stable_complex_row_count": sum(bool(row["stable_complex"]) for row in rows),
        "decision": decision,
    }


def _plot(payload: dict[str, Any], output: Path) -> None:
    cases = payload["cases"]
    fig, axes = plt.subplots(1, len(cases), figsize=(6.4 * len(cases), 4.8), squeeze=False)
    for axis_plot, case in zip(axes[0], cases, strict=True):
        grouped: dict[str, list[dict[str, Any]]] = {}
        for row in case["rows"]:
            grouped.setdefault(str(row["distance_label"]), []).append(row)
        positions = np.arange(len(grouped), dtype=float)
        for index, (label, rows) in enumerate(grouped.items()):
            ratios = np.asarray([row["c_over_g"] for row in rows], dtype=float)
            jitter = np.linspace(-0.14, 0.14, ratios.size)
            axis_plot.scatter(
                np.full(ratios.size, positions[index]) + jitter,
                ratios,
                s=24,
                alpha=0.75,
                color="#0072B2",
            )
            axis_plot.plot(
                [positions[index] - 0.18, positions[index] + 0.18],
                [float(np.median(ratios)), float(np.median(ratios))],
                color="#D55E00",
                linewidth=2.0,
            )
        axis_plot.axhline(1.0, color="black", linestyle="--", linewidth=1.0)
        axis_plot.set_xticks(positions, list(grouped), rotation=25, ha="right")
        axis_plot.set_ylabel("directional same-law c/g")
        axis_plot.set_title(
            f"d={case['dim']}, seed={case['formation_seed']}\n{case['decision']}"
        )
        axis_plot.grid(alpha=0.2)
    fig.suptitle("Same-law reciprocal Jacobian audit (no gain fit)")
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    lines = [
        "# Same-law reciprocal Jacobian audit",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        f"**Decision: `{payload['decision']}`.**",
        "",
        "This audit computes self and cross Hessians from complete stored memory states.",
        "It does not fit a trajectory frequency or retune the cross gain.",
        "",
        f"![Same-law Jacobian audit]({_relative_from(report, figure)})",
        "",
        "## Model boundary",
        "",
        "The reduced state is $Y_-=(x_-,\\bar x_-^\\rho)$. The matrices",
        "$G=\\eta\\nabla^2\\Phi_{self}$ and $C(R)=\\eta\\nabla^2\\Phi_{cross}$",
        "are evaluated under the same kernel and coupling. The full",
        "$A_-(G,C,\\lambda)$ spectrum is derived from them. None of $Y_-$,",
        "$A_-$ or its poles is an additional microscopic parameter.",
        "",
        "## Results",
        "",
        "| d | seed | N | R_mem | eig(G) min..max | g threshold | max c/g | max eig(C-G) | complex rows | decision |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for case in payload["cases"]:
        ratios = [float(row["c_over_g"]) for row in case["rows"]]
        excess = [float(row["cross_minus_self_max_eigenvalue"]) for row in case["rows"]]
        self_values = np.asarray(case["self_gain_eigenvalues"], dtype=float)
        lines.append(
            f"| {case['dim']} | {case['formation_seed']} | {case['update_index']} | "
            f"{case['memory_radius']:.6g} | {self_values.min():.6g}..{self_values.max():.6g} | "
            f"{case['complex_window_self_gain_threshold']:.6g} | {max(ratios):.9g} | "
            f"{max(excess):.6g} | {case['stable_complex_row_count']} | `{case['decision']}` |"
        )
    lines.extend(
        [
            "",
            "Directional values by preregistered distance:",
            "",
            "| d | distance | c/g min..median..max | max eig(C-G) | stable complex |",
            "|---:|---|---:|---:|---:|",
        ]
    )
    for case in payload["cases"]:
        labels = list(dict.fromkeys(str(row["distance_label"]) for row in case["rows"]))
        for label in labels:
            rows = [row for row in case["rows"] if row["distance_label"] == label]
            ratios = np.asarray([row["c_over_g"] for row in rows], dtype=float)
            excess = max(float(row["cross_minus_self_max_eigenvalue"]) for row in rows)
            complex_count = sum(bool(row["stable_complex"]) for row in rows)
            lines.append(
                f"| {case['dim']} | `{label}` | {ratios.min():.9g}.."
                f"{np.median(ratios):.9g}..{ratios.max():.9g} | "
                f"{excess:.6g} | {complex_count}/{len(rows)} |"
            )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "A stable complex local pole would be a damped relative mode, not a",
            "persistent orbit, quantum state, particle or dimension-selection result.",
            "The available repository state coverage is one formation seed in each",
            "of d=3 and d=10; this is a structural case study, not seed-robust evidence.",
            "",
            "## Reproducibility",
            "",
            f"- revision: `{payload['git_revision']}`;",
            f"- worktree at execution: `{payload['git_status'] or 'clean'}`;",
            "- same-law means identical self/cross kernel, deposition and eta;",
            f"- JSON: `{_relative(payload['summary_json'])}`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    checkpoint_paths = [
        _resolve(Path(part.strip()))
        for part in args.checkpoints.split(",")
        if part.strip()
    ]
    if not checkpoint_paths:
        raise SystemExit("at least one checkpoint is required")
    cases = [audit_checkpoint(path) for path in checkpoint_paths]
    decisions = {str(case["decision"]) for case in cases}
    decision = decisions.pop() if len(decisions) == 1 else "mixed-inconclusive"
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    payload = {
        "schema": "emergenz-knoten.same-law-reciprocal-jacobian-audit.v1",
        "created_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_revision": _git(["rev-parse", "HEAD"]),
        "git_status": _git(["status", "--porcelain"]),
        "decision": decision,
        "cases": cases,
        "summary_json": summary,
    }
    _plot(payload, figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(_report(payload, report, figure), encoding="utf-8")
    summary.write_text(
        json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"decision": decision, "cases": cases}, default=_jsonable))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
