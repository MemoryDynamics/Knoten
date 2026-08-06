"""CLI and report writer for the stored-pole identity audit."""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path

from emergenz_knoten.hankel_pole_identity_report import analyze, plot_result


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("reports/response/long_horizon_hankel_gate_2026-08-04.json"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/hankel_pole_identity_audit_2026-08-06.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/response/hankel_pole_identity_audit_2026-08-06.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/hankel_pole_identity_audit_2026-08-06.png"
        ),
    )
    return parser


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative_from(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def render_report(result: dict, report: Path, figure: Path, summary: Path) -> str:
    lines = [
        "# P3.2 reduced DMD pole-identity audit",
        "",
        f"Date: {result['created_utc']}.",
        "",
        "## Registered result",
        "",
        f"Classification: **{result['classification']}**.",
        "",
        "The audit uses only stored visible-state fits. A complex pole must match",
        "at least 10/12 cells across ranks 8,16,32 and depths 100,150,200,250,",
        "remain seed-stable at every paired noise correlation, and be absent from",
        "the same cells in the retarded one-way control.",
        "",
        f"![Pole identity audit]({_relative_from(report, figure)})",
        "",
        "| seed | noise corr. | anchors | identity tracks | reciprocal cells | one-way cells | omega | Gamma |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in result["rows"]:
        best = row["best_track"]
        lines.append(
            f"| {row['future_seed']} | {row['noise_correlation']:.2g} | "
            f"{row['anchor_count']} | {row['identity_track_count']} | "
            f"{best['matching_cells'] if best else 0} | "
            f"{best['control_matching_cells'] if best else 0} | "
            f"{best['median_frequency'] if best else math.nan:.4g} | "
            f"{best['median_damping'] if best else math.nan:.4g} |"
        )
    lines.extend(
        [
            "",
            "## Cross-seed and control gate",
            "",
            f"Cross-correlation candidates: {result['cross_correlation_candidate_count']}.",
            "Control-separated survivors: "
            f"{result['control_separated_cross_correlation_candidate_count']}.",
            "",
            "The correlation ladder reuses the same innovations at different",
            "relative amplitudes. It is a robustness check, not three independent",
            "ensembles. Only future-noise seeds count as independent units.",
            "",
            "A pole recurring in the one-way arm is a delay/noise/mediator feature,",
            "not evidence for a reciprocal knot mode.",
            "",
            "## Decision",
            "",
            (
                "A fixed confirmation run of at least 500,000 updates is permitted."
                if result["pass"]
                else "P3.2 is closed without a new 500,000-update run. The next step is P3.2c: source-local emission/readout analysis before another mechanism simulation."
            ),
            "",
            "No physical oscillation, spin, photon, dimension, or particle claim",
            "follows from this prescreen.",
            "",
            "## Reproducibility",
            "",
            "- source: `reports/response/long_horizon_hankel_gate_2026-08-04.json`;",
            f"- source git revision: `{result['source_git_revision']}`;",
            "- no simulation was run;",
            f"- [machine-readable summary]({_relative_from(report, summary)}).",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = build_parser().parse_args()
    source = _resolve(args.input)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    result = analyze(json.loads(source.read_text(encoding="utf-8")))
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    plot_result(result, figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(render_report(result, report, figure, summary), encoding="utf-8")


if __name__ == "__main__":
    main()
