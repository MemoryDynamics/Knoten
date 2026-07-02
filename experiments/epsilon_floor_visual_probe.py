from __future__ import annotations

import argparse
from dataclasses import asdict, replace
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))

from emergenz_knoten import SimulationConfig  # noqa: E402
from kernel_shape_probe import (  # noqa: E402
    _entry_from_samples,
    _fmt_metric,
    _plot_trajectories_svg,
    simulate_probe_numpy,
)


def _parse_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one float")
    return values


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


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def build_report(payload: dict[str, Any]) -> str:
    lines = [
        "# Epsilon Floor Visual Probe",
        "",
        f"Date: {payload['finished_utc']}.",
        "",
        "## Scope",
        "",
        "This visual probe renders the epsilon-floor cases with panel-specific",
        "scales. It is for shape inspection only; absolute sizes are reported in",
        "the table and in the axis-unit annotations.",
        "",
        "## Figure",
        "",
        f"![Epsilon floor flexible trajectories]({payload['figure_path']})",
        "",
        "## Results",
        "",
        "| epsilon | mean radius | median step | turn mean | span xyz |",
        "| ---: | ---: | ---: | ---: | --- |",
    ]
    for case in payload["cases"]:
        metrics = case["metrics"]
        spans = ", ".join(_fmt_metric(value) for value in metrics["plot_span"])
        lines.append(
            f"| `{case['epsilon']:.5g}` | `{_fmt_metric(metrics['mean_centered_radius'])}` | "
            f"`{_fmt_metric(metrics['median_sample_step'])}` | `{_fmt_metric(metrics['turn_cosine_mean'])}` | `{spans}` |"
        )
    lines.extend(
        [
            "",
            "## Reading",
            "",
            "- `epsilon=0` is a fixed-point control for the zero-start baseline and",
            "  therefore collapses to a point.",
            "- Positive epsilon cases look shape-similar under flexible scaling because",
            "  this slice is scale-equivalent: lowering epsilon shrinks the trajectory",
            "  without smoothing its directional statistics.",
            "- Use this figure only together with the numeric epsilon-floor report; panel",
            "  scaling deliberately hides absolute size differences.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render flexible-scale epsilon-floor trajectory panels.")
    parser.add_argument("--steps", type=int, default=80_000)
    parser.add_argument("--burn-in", type=int, default=8_000)
    parser.add_argument("--sample-every", type=int, default=10)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--epsilons", type=_parse_float_list, default=_parse_float_list("0,1e-5,1e-10,1e-20,1e-34"))
    parser.add_argument("--dim", type=int, default=3)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--memory-factor", type=float, default=6.0)
    parser.add_argument("--max-memory", type=int, default=800)
    parser.add_argument("--rolling", type=int, default=25)
    parser.add_argument("--figure", type=Path, default=Path("figures/draft/epsilon_floor_trajectories_flexible_2026-07-02.svg"))
    parser.add_argument("--report", type=Path, default=Path("reports/epsilon_floor_visual_probe_2026-07-02.md"))
    parser.add_argument("--output-json", type=Path, default=Path("data/processed/epsilon_floor_visual_probe/2026-07-02_seed1/summary.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base = SimulationConfig(
        steps=args.steps,
        dim=args.dim,
        epsilon=0.0,
        eta=args.eta,
        alpha=args.alpha,
        memory_factor=args.memory_factor,
        max_memory=args.max_memory,
        burn_in=args.burn_in,
        sample_every=args.sample_every,
    )
    started = _utc_now()
    start = time.perf_counter()
    cases = []
    for epsilon in args.epsilons:
        config = replace(base, epsilon=epsilon)
        print(f"running epsilon={epsilon:g}", flush=True)
        samples = simulate_probe_numpy(config, seed=args.seed)
        entry = _entry_from_samples(f"epsilon={epsilon:.0e}" if epsilon else "epsilon=0", config, samples)
        entry["epsilon"] = float(epsilon)
        cases.append(entry)

    figure = args.figure if args.figure.is_absolute() else ROOT / args.figure
    report = args.report if args.report.is_absolute() else ROOT / args.report
    output_json = args.output_json if args.output_json.is_absolute() else ROOT / args.output_json
    _plot_trajectories_svg(
        cases,
        figure,
        title="Epsilon Floor: flexible-scale isometric 3D trajectory projections",
        rolling=args.rolling,
        scale_mode="per-panel",
    )
    payload = {
        "description": "Flexible-scale epsilon floor trajectory visual probe.",
        "started_utc": started,
        "finished_utc": _utc_now(),
        "elapsed_seconds": float(time.perf_counter() - start),
        "git_revision": _git_output(["rev-parse", "--short", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "seed": int(args.seed),
        "base_config": asdict(base),
        "epsilons": [float(value) for value in args.epsilons],
        "figure_path": Path(os.path.relpath(figure, report.parent)).as_posix(),
        "cases": cases,
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    report.write_text(build_report(payload), encoding="utf-8")
    print(f"wrote {figure}", flush=True)
    print(f"wrote {report}", flush=True)
    print(f"wrote {output_json}", flush=True)


if __name__ == "__main__":
    main()