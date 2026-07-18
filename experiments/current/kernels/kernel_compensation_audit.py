from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (  # noqa: E402
    two_scale_integral_coefficient,
    two_scale_local_curvature,
    zero_mean_compensator_amplitude,
)


def _parse_int_list(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(item < 1 for item in values):
        raise argparse.ArgumentTypeError("expected positive comma-separated integers")
    return values


def _parse_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(not math.isfinite(item) for item in values):
        raise argparse.ArgumentTypeError("expected finite comma-separated numbers")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the zero-integral/local-curvature constraint and derive a "
            "broad third-scale compensator for the canonical Gaussian kernel."
        )
    )
    parser.add_argument("--dims", type=_parse_int_list, default=_parse_int_list("3,10"))
    parser.add_argument("--q-min", type=float, default=1.05)
    parser.add_argument("--q-max", type=float, default=6.0)
    parser.add_argument("--q-points", type=int, default=320)
    parser.add_argument("--reference-q", type=float, default=3.0)
    parser.add_argument(
        "--reference-a-att",
        type=_parse_float_list,
        default=_parse_float_list("20,35"),
    )
    parser.add_argument(
        "--compensator-scales",
        type=_parse_float_list,
        default=_parse_float_list("5,10,30,100"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/kernels/compensation/"
            "kernel_compensation_constraint_audit_2026-07-18.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/kernels/compensation/"
            "kernel_compensation_constraint_audit_2026-07-18.json"
        ),
    )
    parser.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("figures/draft/kernels/compensation_2026-07-18"),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel_from(source_file: Path, target: Path) -> str:
    return Path(
        os.path.relpath(target.resolve(), source_file.resolve().parent)
    ).as_posix()


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


def _fmt(value: float, digits: int = 5) -> str:
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3 or abs(value) >= 1e4:
        return f"{value:.{digits}e}"
    return f"{value:.{digits}f}"


def fixed_curvature_amplitude(
    *, q: float, chi: float, amplitude_rep: float = 1.0
) -> float:
    if q <= 0.0 or not math.isfinite(q):
        raise ValueError("q must be positive")
    if not math.isfinite(chi) or not math.isfinite(amplitude_rep):
        raise ValueError("chi and amplitude_rep must be finite")
    return float(amplitude_rep * chi * q**2)


def reference_record(
    *, dim: int, q: float, amplitude_att: float
) -> dict[str, float | int]:
    sigma_rep = 1.0
    sigma_att = q
    integral = two_scale_integral_coefficient(
        dim=dim,
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=1.0,
        amplitude_att=amplitude_att,
    )
    curvature = two_scale_local_curvature(
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=1.0,
        amplitude_att=amplitude_att,
    )
    return {
        "dim": dim,
        "q": q,
        "amplitude_att": amplitude_att,
        "chi": amplitude_att / q**2,
        "restoring_curvature": curvature,
        "integral_coefficient": integral,
        "integrated_attraction_to_repulsion": amplitude_att * q**dim,
        "zero_mean_amplitude_att": q ** (-dim),
        "zero_mean_chi": q ** (-(dim + 2)),
    }


def compensation_record(
    *,
    dim: int,
    q: float,
    amplitude_att: float,
    sigma_comp: float,
) -> dict[str, float | int]:
    amplitude_comp = zero_mean_compensator_amplitude(
        dim=dim,
        sigma_rep=1.0,
        sigma_att=q,
        sigma_comp=sigma_comp,
        amplitude_rep=1.0,
        amplitude_att=amplitude_att,
    )
    original_curvature = two_scale_local_curvature(
        sigma_rep=1.0,
        sigma_att=q,
        amplitude_rep=1.0,
        amplitude_att=amplitude_att,
    )
    compensated_curvature = original_curvature - amplitude_comp / sigma_comp**2
    residual = (
        two_scale_integral_coefficient(
            dim=dim,
            sigma_rep=1.0,
            sigma_att=q,
            amplitude_rep=1.0,
            amplitude_att=amplitude_att,
        )
        + amplitude_comp * sigma_comp**dim
    )
    retention = (
        compensated_curvature / original_curvature
        if original_curvature != 0.0
        else float("nan")
    )
    return {
        "dim": dim,
        "q": q,
        "amplitude_att": amplitude_att,
        "sigma_comp": sigma_comp,
        "amplitude_comp": amplitude_comp,
        "original_curvature": original_curvature,
        "compensated_curvature": compensated_curvature,
        "curvature_retention": retention,
        "integral_residual": residual,
    }


def radial_profile(
    radius: np.ndarray,
    *,
    q: float,
    amplitude_att: float,
    sigma_comp: float | None = None,
    amplitude_comp: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    rep = np.exp(-0.5 * radius**2)
    att = amplitude_att * np.exp(-0.5 * radius**2 / q**2)
    potential = rep - att
    radial_drift = radius * (rep - att / q**2)
    if sigma_comp is not None:
        comp = amplitude_comp * np.exp(-0.5 * radius**2 / sigma_comp**2)
        potential = potential + comp
        radial_drift = radial_drift + radius * comp / sigma_comp**2
    return potential, radial_drift


def _plot_constraint_map(
    *,
    dims: list[int],
    q_values: np.ndarray,
    reference_q: float,
    reference_amplitudes: list[float],
    output: Path,
) -> None:
    fig, axes = plt.subplots(
        1, len(dims), figsize=(6.0 * len(dims), 4.8), squeeze=False
    )
    colors = ["#c23b22", "#147d64"]
    for axis, dim in zip(axes[0], dims, strict=True):
        zero_mean = q_values ** (-dim)
        local_balance = q_values**2
        axis.fill_between(
            q_values,
            local_balance,
            1e4,
            color="#d8eee5",
            alpha=0.55,
            label="locally restoring (chi > 1)",
        )
        axis.plot(
            q_values, local_balance, color="#202020", linewidth=2.0, label="chi = 1"
        )
        axis.plot(
            q_values,
            zero_mean,
            color="#7a4eab",
            linewidth=2.2,
            label="zero integral",
        )
        for color, amplitude in zip(colors, reference_amplitudes, strict=False):
            chi = amplitude / reference_q**2
            axis.plot(
                q_values,
                chi * q_values**2,
                color=color,
                linestyle="--",
                linewidth=1.7,
                label=f"fixed chi={chi:.2f}",
            )
            axis.scatter([reference_q], [amplitude], color=color, s=42, zorder=4)
        axis.set_yscale("log")
        axis.set_ylim(1e-9 if dim >= 10 else 1e-4, 1e3)
        axis.set_xlabel("q = sigma_att / sigma_rep")
        axis.set_ylabel("a = A_att / A_rep")
        axis.set_title(f"ambient dimension d={dim}")
        axis.grid(True, which="both", alpha=0.22)
        axis.legend(frameon=False, fontsize=8)
    fig.suptitle("Two-scale kernel constraints", fontsize=13)
    fig.tight_layout()
    fig.savefig(output, dpi=190)
    plt.close(fig)


def _plot_compensation(
    records: list[dict[str, float | int]],
    *,
    output: Path,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5))
    palette = {
        (3, 20.0): "#147d64",
        (3, 35.0): "#c23b22",
        (10, 20.0): "#377eb8",
        (10, 35.0): "#7a4eab",
    }
    for (dim, amplitude), color in palette.items():
        rows = [
            row
            for row in records
            if int(row["dim"]) == dim and float(row["amplitude_att"]) == amplitude
        ]
        if not rows:
            continue
        rows.sort(key=lambda row: float(row["sigma_comp"]))
        x = [float(row["sigma_comp"]) for row in rows]
        y_amp = [float(row["amplitude_comp"]) for row in rows]
        y_ret = [float(row["curvature_retention"]) for row in rows]
        label = f"d={dim}, A_att={amplitude:g}"
        axes[0].plot(x, y_amp, marker="o", color=color, label=label)
        axes[1].plot(x, y_ret, marker="o", color=color, label=label)
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    axes[0].set_xlabel("sigma_comp / sigma_rep")
    axes[0].set_ylabel("A_comp / A_rep")
    axes[0].set_title("exact zero-integral amplitude")
    axes[1].set_xscale("log")
    axes[1].axhline(1.0, color="#202020", linewidth=1.0)
    axes[1].set_xlabel("sigma_comp / sigma_rep")
    axes[1].set_ylabel("retained local curvature")
    axes[1].set_title("local effect of broad compensation")
    for axis in axes:
        axis.grid(True, which="both", alpha=0.22)
        axis.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(output, dpi=190)
    plt.close(fig)


def _plot_point_field(
    *,
    dim: int,
    q: float,
    amplitude_att: float,
    compensator_scales: list[float],
    output: Path,
) -> None:
    selected = compensator_scales[:2]
    radius = np.linspace(0.0, max(12.0, 1.3 * max(selected)), 1200)
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.5))
    profiles: list[tuple[str, np.ndarray, np.ndarray, str]] = []
    potential, drift = radial_profile(radius, q=q, amplitude_att=amplitude_att)
    profiles.append(("two-scale", potential, drift, "#202020"))
    for sigma_comp, color in zip(selected, ["#147d64", "#c23b22"], strict=False):
        amplitude_comp = zero_mean_compensator_amplitude(
            dim=dim,
            sigma_rep=1.0,
            sigma_att=q,
            sigma_comp=sigma_comp,
            amplitude_rep=1.0,
            amplitude_att=amplitude_att,
        )
        potential, drift = radial_profile(
            radius,
            q=q,
            amplitude_att=amplitude_att,
            sigma_comp=sigma_comp,
            amplitude_comp=amplitude_comp,
        )
        profiles.append(
            (f"zero integral, sigma_comp={sigma_comp:g}", potential, drift, color)
        )
    near_limit = min(10.0, float(radius[-1]))
    for label, potential, drift, color in profiles:
        axes[0, 0].plot(radius, potential, color=color, label=label)
        axes[1, 0].plot(radius, drift, color=color, label=label)
        near = radius <= near_limit
        axes[0, 1].plot(radius[near], potential[near], color=color, label=label)
        axes[1, 1].plot(radius[near], drift[near], color=color, label=label)
    axes[0, 0].set_title("potential: full plotted range")
    axes[1, 0].set_title("radial drift: full plotted range")
    axes[0, 1].set_title("potential: knot-scale window")
    axes[1, 1].set_title("radial drift: knot-scale window")
    for axis in axes.flat:
        axis.axhline(0.0, color="#777777", linewidth=0.8)
        axis.set_xlabel("r / sigma_rep")
        axis.grid(True, alpha=0.22)
    axes[0, 0].set_ylabel("K(r)")
    axes[0, 1].set_ylabel("K(r)")
    axes[1, 0].set_ylabel("-dK/dr (outward positive)")
    axes[1, 1].set_ylabel("-dK/dr (outward positive)")
    axes[0, 0].legend(frameon=False, fontsize=8)
    fig.suptitle(f"Point-deposit field, d={dim}, q={q:g}, A_att={amplitude_att:g}")
    fig.tight_layout()
    fig.savefig(output, dpi=190)
    plt.close(fig)


def write_report(
    *,
    report_path: Path,
    summary_path: Path,
    figure_paths: list[Path],
    payload: dict[str, Any],
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )

    refs = payload["reference_records"]
    comps = payload["compensation_records"]
    fixed = payload["fixed_curvature_pilot"]
    lines = [
        "# Kernel Compensation Constraint Audit",
        "",
        f"Date: {payload['generated_utc']}.",
        "",
        "## Question",
        "",
        "Can the compact two-scale knot candidates (`A_att=20..35`, `q=3`)",
        "also satisfy `integral K = 0`, and can a sigma variation reconcile the",
        "two requirements without a broad parameter scan?",
        "",
        "## Exact Two-Scale Constraint",
        "",
        "Write `q=sigma_att/sigma_rep>1` and `a=A_att/A_rep`. For the",
        "unnormalized Gaussian convention in the code, zero integral requires",
        "",
        "```text",
        "a_zero = q^(-d).",
        "```",
        "",
        "Local inward linear drift around a point deposit requires",
        "",
        "```text",
        "chi = a/q^2 > 1, equivalently a > q^2.",
        "```",
        "",
        "For every `q>1` and `d>=1`, `q^(-d)<1<q^2`. The two conditions are",
        "therefore disjoint in this two-scale ordering. This is a structural",
        "result, not a failure that can be repaired by a generic sigma sweep.",
        "It is also only a local point-deposit test, not a full knot-existence theorem.",
        "",
        "## Existing Reference Points",
        "",
        "| d | q | A_att | chi | local curvature | attraction/repulsion integral | zero-mean A_att |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in refs:
        lines.append(
            "| "
            f"{int(row['dim'])} | {_fmt(float(row['q']))} | "
            f"{_fmt(float(row['amplitude_att']))} | {_fmt(float(row['chi']))} | "
            f"{_fmt(float(row['restoring_curvature']))} | "
            f"{_fmt(float(row['integrated_attraction_to_repulsion']))} | "
            f"{_fmt(float(row['zero_mean_amplitude_att']))} |"
        )
    lines.extend(
        [
            "",
            "The q=3 candidates are locally restoring, but their unnormalized",
            "integrals are attraction dominated by factors from hundreds (d=3)",
            "to millions (d=10). Thus they do not approximate a neutral kernel.",
            "",
            "## Figures",
            "",
        ]
    )
    lines.extend(
        f"- [{path.stem}]({_rel_from(report_path, path)})" for path in figure_paths
    )
    lines.extend(
        [
            "",
            "## Controlled Sigma Test",
            "",
            "The next simulation varies one scale ratio only while preserving",
            f"`chi={fixed['chi']:.8g}`, the q=3, A_att=35 local stiffness ratio.",
            "This separates scale geometry from the already known curvature effect.",
            "",
            "| q | A_att at fixed chi | local curvature |",
            "| ---: | ---: | ---: |",
        ]
    )
    for row in fixed["rows"]:
        lines.append(
            f"| {_fmt(float(row['q']))} | {_fmt(float(row['amplitude_att']))} | "
            f"{_fmt(float(row['local_curvature']))} |"
        )
    lines.extend(
        [
            "",
            "Planned fixed parameters: `d=3`, `N=1M`, seeds `1..5`,",
            "`epsilon=1e-4`, `eta=0.15`, `lambda=0.01`, `M0=1`, delta",
            "deposition, `sigma_rep=1`, with seed-matched `eta_zero` controls.",
            "This is a mechanism pilot, not a long-run knot claim.",
            "",
            "## Broad Third-Scale Compensation",
            "",
            "A minimal neutral extension is",
            "",
            "```text",
            "K3 = A_rep G(sigma_rep) - A_att G(sigma_att) + A_comp G(sigma_comp),",
            "A_comp = (A_att sigma_att^d - A_rep sigma_rep^d) / sigma_comp^d.",
            "```",
            "",
            "The final broad positive term cancels the integral. Its reduction of",
            "the local restoring curvature is `A_comp/sigma_comp^2`, which decays",
            "rapidly with a broad compensator.",
            "",
            "| d | A_att | sigma_comp | A_comp | curvature retained | residual integral coefficient |",
            "| ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in comps:
        lines.append(
            "| "
            f"{int(row['dim'])} | {_fmt(float(row['amplitude_att']))} | "
            f"{_fmt(float(row['sigma_comp']))} | {_fmt(float(row['amplitude_comp']))} | "
            f"{_fmt(float(row['curvature_retention']))} | "
            f"{_fmt(float(row['integral_residual']))} |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "1. Do not reinterpret `A_att=20..35` as approximately zero mean.",
            "2. Do not launch an unconstrained sigma sweep.",
            "3. Run the fixed-chi q slice first to test whether compactness is",
            "   controlled mainly by local curvature or also by scale separation.",
            "4. If the compact branch survives that slice, implement one broad",
            "   compensated third-scale pilot with exact integral cancellation.",
            "5. Keep kernel neutrality as a cross-knot/far-field hypothesis, not",
            "   as an axiom of the self-confining scalar memory channel.",
            "",
            "## Provenance",
            "",
            f"- Git revision: `{payload['git_revision']}`",
            f"- Git status at generation: `{payload['git_status'] or 'clean'}`",
            "- Script: `experiments/current/kernels/kernel_compensation_audit.py`",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    if not 1.0 < args.q_min < args.q_max:
        raise SystemExit("require 1 < q_min < q_max")
    if args.q_points < 10:
        raise SystemExit("--q-points must be at least 10")
    if args.reference_q <= 1.0 or not math.isfinite(args.reference_q):
        raise SystemExit("--reference-q must be finite and greater than one")
    if any(value <= 0.0 for value in args.reference_a_att):
        raise SystemExit("--reference-a-att values must be positive")
    if any(value <= args.reference_q for value in args.compensator_scales):
        raise SystemExit("compensator scales must be broader than reference q")

    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_dir = _resolve(args.figure_dir)
    figure_dir.mkdir(parents=True, exist_ok=True)

    q_values = np.geomspace(args.q_min, args.q_max, args.q_points)
    refs = [
        reference_record(dim=dim, q=args.reference_q, amplitude_att=amplitude)
        for dim in args.dims
        for amplitude in args.reference_a_att
    ]
    comps = [
        compensation_record(
            dim=dim,
            q=args.reference_q,
            amplitude_att=amplitude,
            sigma_comp=sigma_comp,
        )
        for dim in args.dims
        for amplitude in args.reference_a_att
        for sigma_comp in args.compensator_scales
    ]
    chi = max(args.reference_a_att) / args.reference_q**2
    fixed_rows = []
    for q in (2.0, 3.0, 4.0):
        amplitude = fixed_curvature_amplitude(q=q, chi=chi)
        fixed_rows.append(
            {
                "q": q,
                "amplitude_att": amplitude,
                "local_curvature": two_scale_local_curvature(
                    sigma_rep=1.0,
                    sigma_att=q,
                    amplitude_rep=1.0,
                    amplitude_att=amplitude,
                ),
            }
        )

    constraint_figure = figure_dir / "two_scale_constraint_map.png"
    compensation_figure = figure_dir / "three_scale_compensation.png"
    field_figure = figure_dir / "compensated_point_field.png"
    _plot_constraint_map(
        dims=args.dims,
        q_values=q_values,
        reference_q=args.reference_q,
        reference_amplitudes=args.reference_a_att,
        output=constraint_figure,
    )
    _plot_compensation(comps, output=compensation_figure)
    _plot_point_field(
        dim=args.dims[0],
        q=args.reference_q,
        amplitude_att=max(args.reference_a_att),
        compensator_scales=args.compensator_scales,
        output=field_figure,
    )

    payload: dict[str, Any] = {
        "description": "Two-scale neutrality/local-curvature constraint and broad compensator audit.",
        "generated_utc": _utc_now(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "parameters": {
            "dims": args.dims,
            "q_min": args.q_min,
            "q_max": args.q_max,
            "q_points": args.q_points,
            "reference_q": args.reference_q,
            "reference_a_att": args.reference_a_att,
            "compensator_scales": args.compensator_scales,
        },
        "reference_records": refs,
        "compensation_records": comps,
        "fixed_curvature_pilot": {"chi": chi, "rows": fixed_rows},
        "figures": [
            constraint_figure.relative_to(ROOT).as_posix(),
            compensation_figure.relative_to(ROOT).as_posix(),
            field_figure.relative_to(ROOT).as_posix(),
        ],
    }
    write_report(
        report_path=report_path,
        summary_path=summary_path,
        figure_paths=[constraint_figure, compensation_figure, field_figure],
        payload=payload,
    )
    print(f"wrote {report_path}")
    print(f"wrote {summary_path}")
    for path in (constraint_figure, compensation_figure, field_figure):
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
