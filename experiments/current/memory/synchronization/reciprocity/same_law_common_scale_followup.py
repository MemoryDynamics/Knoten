"""P3.7a follow-up: test one common same-law gain scale across mature states."""

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
    common_gain_scale_interval,
    reciprocal_relative_mode_operator,
)


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-json", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/response/reciprocal/"
            "same_law_common_scale_followup_2026-08-11.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/reciprocal/"
            "same_law_common_scale_followup_2026-08-11.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/"
            "same_law_common_scale_followup_2026-08-11.png"
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


def analyse(audit: dict[str, Any]) -> dict[str, Any]:
    labels = list(
        dict.fromkeys(
            str(row["distance_label"])
            for case in audit["cases"]
            for row in case["rows"]
        )
    )
    eta_values = {float(case["eta"]) for case in audit["cases"]}
    if len(eta_values) != 1:
        raise ValueError("all audit cases must share one base eta")
    base_eta = eta_values.pop()
    distance_results: list[dict[str, Any]] = []

    for label in labels:
        row_results: list[dict[str, Any]] = []
        for case in audit["cases"]:
            self_gain = np.asarray(case["self_gain_matrix"], dtype=float)
            for row in case["rows"]:
                if row["distance_label"] != label:
                    continue
                interval = common_gain_scale_interval(
                    float(case["lambda"]),
                    float(row["g_directional"]),
                    float(row["c_directional"]),
                )
                row_results.append(
                    {
                        "dim": int(case["dim"]),
                        "seed": int(case["formation_seed"]),
                        "axis": int(row["axis"]),
                        "lambda": float(case["lambda"]),
                        "self_gain_matrix": self_gain,
                        "cross_gain_matrix": np.asarray(
                            row["cross_gain_matrix"], dtype=float
                        ),
                        "scale_lower": interval.lower,
                        "scale_upper": interval.upper,
                        "interval_exists": interval.exists,
                    }
                )

        all_intervals_exist = bool(row_results) and all(
            bool(row["interval_exists"]) for row in row_results
        )
        common_lower = (
            max(float(row["scale_lower"]) for row in row_results)
            if all_intervals_exist
            else math.nan
        )
        common_upper = (
            min(float(row["scale_upper"]) for row in row_results)
            if all_intervals_exist
            else math.nan
        )
        common_exists = bool(
            all_intervals_exist
            and math.isfinite(common_lower)
            and math.isfinite(common_upper)
            and 0.0 < common_lower < common_upper
        )
        scale = math.sqrt(common_lower * common_upper) if common_exists else math.nan

        full_results: list[dict[str, Any]] = []
        if common_exists:
            for row in row_results:
                mode = reciprocal_relative_mode_operator(
                    float(row["lambda"]),
                    scale * np.asarray(row["self_gain_matrix"], dtype=float),
                    scale * np.asarray(row["cross_gain_matrix"], dtype=float),
                )
                full_results.append(
                    {
                        "dim": row["dim"],
                        "seed": row["seed"],
                        "axis": row["axis"],
                        "is_stable": mode.is_stable,
                        "has_complex_pair": mode.has_complex_pair,
                        "spectral_radius": float(np.max(np.abs(mode.eigenvalues))),
                        "max_imaginary_part": float(
                            np.max(np.abs(mode.eigenvalues.imag))
                        ),
                        "eigenvalues": mode.eigenvalues,
                    }
                )
        all_full_pass = bool(full_results) and all(
            bool(row["is_stable"] and row["has_complex_pair"])
            for row in full_results
        )
        public_intervals = [
            {
                key: value
                for key, value in row.items()
                if key not in {"self_gain_matrix", "cross_gain_matrix"}
            }
            for row in row_results
        ]
        distance_results.append(
            {
                "distance_label": label,
                "row_count": len(row_results),
                "common_scale_lower": common_lower,
                "common_scale_upper": common_upper,
                "common_scale_exists": common_exists,
                "common_eta_lower": base_eta * common_lower,
                "common_eta_upper": base_eta * common_upper,
                "midpoint_scale": scale,
                "midpoint_eta": base_eta * scale,
                "all_full_modes_pass": all_full_pass,
                "full_pass_count": sum(
                    bool(row["is_stable"] and row["has_complex_pair"])
                    for row in full_results
                ),
                "full_results": full_results,
                "directional_intervals": public_intervals,
            }
        )

    if any(bool(row["all_full_modes_pass"]) for row in distance_results):
        decision = "common-scale-eligible"
    elif any(bool(row["common_scale_exists"]) for row in distance_results):
        decision = "matrix-inconclusive"
    else:
        decision = "common-scale-negative"
    return {
        "decision": decision,
        "base_eta": base_eta,
        "distances": distance_results,
    }


def _plot(payload: dict[str, Any], output: Path) -> None:
    rows = payload["distances"]
    fig, axis = plt.subplots(figsize=(9.2, 4.8))
    for index, row in enumerate(rows):
        if not row["common_scale_exists"]:
            axis.scatter(index, payload["base_eta"], marker="x", color="#999999")
            continue
        lower = float(row["common_eta_lower"])
        upper = float(row["common_eta_upper"])
        midpoint = float(row["midpoint_eta"])
        color = "#0072B2" if row["all_full_modes_pass"] else "#D55E00"
        axis.vlines(index, lower, upper, color=color, linewidth=4.0)
        axis.scatter(index, midpoint, color=color, s=38, zorder=3)
    axis.axhline(
        float(payload["base_eta"]),
        color="black",
        linestyle="--",
        linewidth=1.0,
        label=r"checkpoint $\eta_0$",
    )
    axis.set_yscale("log")
    axis.set_xticks(range(len(rows)), [row["distance_label"] for row in rows])
    axis.tick_params(axis="x", rotation=25)
    axis.set_ylabel(r"common coupling $\eta$")
    axis.set_title("Same-law stable-complex intervals shared by d=3 and d=10")
    axis.grid(alpha=0.2, which="both")
    axis.legend()
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _fmt_interval(lower: float, upper: float) -> str:
    if not (math.isfinite(lower) and math.isfinite(upper) and lower < upper):
        return "none"
    return f"{lower:.8g}..{upper:.8g}"


def _report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    lines = [
        "# Same-law common-scale follow-up",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        f"**Decision: `{payload['decision']}`.**",
        "",
        "This is a registered post-audit follow-up to the inconclusive fixed-gain",
        "Jacobian audit. Self and cross gains are scaled together; no separate",
        "cross normalization and no trajectory-frequency fit are used.",
        "",
        f"![Common same-law gain intervals]({_relative_from(report, figure)})",
        "",
        "## Shared intervals",
        "",
        "| distance | all directional scale intervals | shared eta interval | fixed midpoint eta | full matrix pass |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in payload["distances"]:
        directional = row["directional_intervals"]
        existing = sum(bool(item["interval_exists"]) for item in directional)
        eta_interval = _fmt_interval(
            float(row["common_eta_lower"]), float(row["common_eta_upper"])
        )
        midpoint = (
            f"{float(row['midpoint_eta']):.8g}"
            if row["common_scale_exists"]
            else "n/a"
        )
        lines.append(
            f"| `{row['distance_label']}` | {existing}/{row['row_count']} | "
            f"{eta_interval} | {midpoint} | "
            f"{row['full_pass_count']}/{row['row_count']} |"
        )

    eligible = [row for row in payload["distances"] if row["all_full_modes_pass"]]
    lines.extend(
        [
            "",
            "## Result boundary",
            "",
        ]
    )
    if eligible:
        labels = ", ".join(f"`{row['distance_label']}`" for row in eligible)
        lines.extend(
            [
                f"The shared full-matrix gate passes at {labels}.",
                "This reduces the local pilot choice to one common coupling and a",
                "pre-existing normalized separation. It does not show that the",
                "microscopic dynamics selects either quantity, nor that nonlinear",
                "trajectories sustain an oscillation.",
            ]
        )
    else:
        lines.extend(
            [
                "No preregistered separation passes the shared full-matrix gate.",
                "A same-law low-g reciprocal pilot is therefore not authorized by",
                "this analysis.",
            ]
        )
    lines.extend(
        [
            "",
            "Only one mature formation seed is available in each of d=3 and d=10.",
            "The result is a local structural eligibility test, not seed-robust",
            "evidence, a persistent orbit, a quantum state or dimension selection.",
            "",
            "## Reproducibility",
            "",
            f"- input audit: `{payload['audit_json']}`;",
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
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    result = analyse(audit)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    payload = {
        "schema": "emergenz-knoten.same-law-common-scale-followup.v1",
        "created_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_revision": _git(["rev-parse", "HEAD"]),
        "git_status": _git(["status", "--porcelain"]),
        "audit_json": _relative(audit_path),
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
    print(json.dumps({"decision": payload["decision"], "distances": payload["distances"]}, default=_jsonable))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
