from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import math
from pathlib import Path
import subprocess
from typing import Any


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()


DEFAULT_SUMMARY = Path(
    "reports/long_runs/long_3e8/"
    "dynamic_center_spin_trace_q3_N30M_eps1em4_summary_2026-07-13.json"
)
DEFAULT_REPORT = Path(
    "reports/long_runs/long_3e8/"
    "paper_i_evidence_table_N30M_eps1em4_2026-07-13.md"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a conservative Paper-I evidence table from the N=30M "
            "dynamic-center summary. This script does not rerun simulations."
        )
    )
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--reference-a-att", type=float, default=35.0)
    return parser.parse_args()


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _git_output(args: list[str]) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return completed.stdout.strip()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _fmt(value: Any, digits: int = 3) -> str:
    if value is None:
        return "`n/a`"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return f"`{value}`"
    if not math.isfinite(number):
        return "`n/a`"
    if number == 0.0:
        text = "0"
    elif abs(number) < 1e-3 or abs(number) >= 1e4:
        text = f"{number:.{digits}e}"
    else:
        text = f"{number:.{digits}f}"
    return f"`{text}`"


def _fmt_plain(value: Any, digits: int = 3) -> str:
    wrapped = _fmt(value, digits)
    return wrapped[1:-1] if wrapped.startswith("`") and wrapped.endswith("`") else wrapped


def _metric(group: dict[str, Any], name: str) -> float | None:
    for key in (f"{name}_median", name):
        value = group.get(key)
        if value is None:
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        return number if math.isfinite(number) else None
    return None


def _group_map(summary: list[dict[str, Any]]) -> dict[tuple[float, str], dict[str, Any]]:
    return {
        (float(item["a_att"]), str(item["condition"])): item
        for item in summary
        if item.get("a_att") is not None and item.get("condition") is not None
    }


def _ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator == 0.0:
        return None
    return numerator / denominator


def _delta(active: float | None, control: float | None) -> float | None:
    if active is None or control is None:
        return None
    return active - control


def evidence_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    groups = _group_map(payload.get("summary", []))
    a_values = sorted({key[0] for key in groups})
    rows: list[dict[str, Any]] = []
    for a_att in a_values:
        active = groups.get((a_att, "baseline"))
        control = groups.get((a_att, "eta_zero"))
        if active is None or control is None:
            continue
        active_radius = _metric(active, "dynamic_rms_radius_median")
        control_radius = _metric(control, "dynamic_rms_radius_median")
        active_drift = _metric(active, "dynamic_center_drift_radius_fraction_per_memory_time")
        control_drift = _metric(control, "dynamic_center_drift_radius_fraction_per_memory_time")
        active_dim = _metric(active, "memory_shape_dimension")
        control_dim = _metric(control, "memory_shape_dimension")
        active_round = _metric(active, "memory_roundness")
        control_round = _metric(control, "memory_roundness")
        rows.append(
            {
                "a_att": a_att,
                "n": active.get("n"),
                "steps": active.get("steps"),
                "radius_active": active_radius,
                "radius_control": control_radius,
                "radius_control_over_active": _ratio(control_radius, active_radius),
                "drift_active": active_drift,
                "drift_control": control_drift,
                "drift_control_over_active": _ratio(control_drift, active_drift),
                "memory_dimension_active": active_dim,
                "memory_dimension_control": control_dim,
                "memory_dimension_delta": _delta(active_dim, control_dim),
                "roundness_active": active_round,
                "roundness_control": control_round,
                "roundness_delta": _delta(active_round, control_round),
                "voxel_residence_active": _metric(active, "best_residence_memory_times"),
                "voxel_residence_control": _metric(control, "best_residence_memory_times"),
                "center_residence_active": _metric(
                    active, "memory_center_residence_memory_times"
                ),
                "center_residence_control": _metric(
                    control, "memory_center_residence_memory_times"
                ),
                "spin_axis_active": _metric(active, "spin_axis_polarization"),
                "spin_axis_control": _metric(control, "spin_axis_polarization"),
                "spin_dephasing_active": _metric(
                    active, "spin_raw_spin_dephasing_memory_times"
                ),
                "spin_dephasing_control": _metric(
                    control, "spin_raw_spin_dephasing_memory_times"
                ),
                "spin_dephasing_active_is_upper": _metric(
                    active, "spin_raw_spin_dephasing_is_upper_bound"
                ),
            }
        )
    return rows


def build_report(payload: dict[str, Any], *, source_path: Path, reference_a_att: float) -> str:
    rows = evidence_rows(payload)
    reference = next((row for row in rows if row["a_att"] == reference_a_att), None)
    lines = [
        "# Paper I Evidence Table: N=30M Dynamic-Center Trace",
        "",
        f"Date: {_utc_now()}.",
        "",
        "## Scope",
        "",
        "This report condenses the corrected-sign scalar long-run evidence into a",
        "Paper-I-facing table. It is deliberately conservative: the accepted claim",
        "is a co-moving compact memory-cloud regime, not a fixed absolute center,",
        "not a spin/phase mode, and not a physical particle identification.",
        "",
        "## Provenance",
        "",
        f"- Source aggregate: `{_rel(source_path)}`",
        f"- Git revision while building this report: `{_git_output(['rev-parse', 'HEAD'])}`",
        f"- Git status while building this report: `{_git_output(['status', '--short']) or 'clean'}`",
        "",
        "## Main Evidence Rows",
        "",
        "| A_att | seeds | N | radius active | radius eta=0 | radius gain | drift/r active | drift/r eta=0 | drift separation | D_mem active | D_mem eta=0 | roundness active | roundness eta=0 |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['a_att']:.6g}` | `{row['n']}` | `{int(row['steps']):,}` | "
            f"{_fmt(row['radius_active'])} | {_fmt(row['radius_control'])} | "
            f"{_fmt(row['radius_control_over_active'])} | {_fmt(row['drift_active'])} | "
            f"{_fmt(row['drift_control'])} | {_fmt(row['drift_control_over_active'])} | "
            f"{_fmt(row['memory_dimension_active'])} | {_fmt(row['memory_dimension_control'])} | "
            f"{_fmt(row['roundness_active'])} | {_fmt(row['roundness_control'])} |"
        )

    lines.extend(
        [
            "",
            "## Residence And Spin Guardrails",
            "",
            "| A_att | voxel residence active | voxel residence eta=0 | final-center residence active | final-center residence eta=0 | spin axis active | raw L dephasing active |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in rows:
        upper = row.get("spin_dephasing_active_is_upper")
        dephasing = _fmt(row["spin_dephasing_active"])
        if upper is not None and upper >= 0.5 and row["spin_dephasing_active"] is not None:
            dephasing = f"`<= {_fmt_plain(row['spin_dephasing_active'])}`"
        lines.append(
            f"| `{row['a_att']:.6g}` | {_fmt(row['voxel_residence_active'])} | "
            f"{_fmt(row['voxel_residence_control'])} | {_fmt(row['center_residence_active'])} | "
            f"{_fmt(row['center_residence_control'])} | {_fmt(row['spin_axis_active'])} | "
            f"{dephasing} |"
        )

    lines.extend(["", "## Reading", ""])
    if reference is not None:
        lines.extend(
            [
                f"- Current scalar reference candidate: `A_att={reference_a_att:g}`, `epsilon=1e-4`.",
                "- The strongest Paper-I evidence is not raw voxel residence, because the",
                "  `eta_zero` control can also produce long residence in its own broad",
                "  voxelized path. The discriminating observables are co-moving radius,",
                "  radius-normalized center drift, memory-shape dimension, and roundness.",
                f"- For `A_att={reference_a_att:g}`, the active radius is about",
                f"  `{_fmt_plain(reference['radius_control_over_active'])}` times smaller",
                "  than the matched `eta_zero` control and the radius-normalized center",
                f"  drift is separated by about `{_fmt_plain(reference['drift_control_over_active'])}`.",
                "- The scalar spin proxy remains negative: axis polarization is near zero",
                "  and raw spin dephasing is only an upper bound at the first resolved lag.",
            ]
        )
    else:
        lines.append("- No configured reference row was found in the aggregate.")
    lines.extend(
        [
            "",
            "## Paper-I Claim Boundary",
            "",
            "Supported: the corrected scalar model has seed-robust co-moving compact",
            "memory-cloud candidates in this parameter slice, strongest at `A_att=35`.",
            "",
            "Not supported here: a fixed absolute spatial knot, a stable spin axis,",
            "an oscillatory/photon-like mode, a physical mass claim, or a claim that",
            "three external dimensions have been derived.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    source = _resolve(args.summary_json)
    payload = json.loads(source.read_text(encoding="utf-8"))
    report = _resolve(args.report)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        build_report(payload, source_path=source, reference_a_att=args.reference_a_att),
        encoding="utf-8",
    )
    print(f"wrote {report}")


if __name__ == "__main__":
    main()
