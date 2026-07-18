from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
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
    attractive_amplitude_for_curvature,
    scalar_dimensionless_groups,
    two_scale_local_curvature,
)


@dataclass(frozen=True)
class KernelSpec:
    label: str
    amplitude_rep: float
    sigma_rep: float
    amplitude_att: float
    sigma_att: float

    @property
    def curvature(self) -> float:
        return two_scale_local_curvature(
            sigma_rep=self.sigma_rep,
            sigma_att=self.sigma_att,
            amplitude_rep=self.amplitude_rep,
            amplitude_att=self.amplitude_att,
        )


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the current narrow repulsive Gaussian on the scales sampled "
            "by the compact scalar knot and compare a curvature-matched "
            "attractive-only kernel."
        )
    )
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--amplitude-rep", type=float, default=1.0)
    parser.add_argument("--amplitude-att", type=float, default=35.0)
    parser.add_argument("--epsilon", type=float, default=1.0e-4)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--lambda-value", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--memory-radius", type=float, default=1.94163e-4)
    parser.add_argument("--full-radius", type=float, default=12.0)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/kernels/core/kernel_core_audit_2026-07-18.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/kernels/core/kernel_core_audit_2026-07-18.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path("figures/draft/kernels/core_2026-07-18/kernel_core_audit.png"),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel_from(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _validate_args(args: argparse.Namespace) -> None:
    for name in ("sigma_rep", "sigma_att", "epsilon", "memory_radius", "full_radius"):
        value = float(getattr(args, name))
        if not math.isfinite(value) or value <= 0.0:
            raise SystemExit(f"--{name.replace('_', '-')} must be positive")
    if not 0.0 < args.lambda_value <= 1.0:
        raise SystemExit("--lambda-value must satisfy 0 < value <= 1")
    if args.memory_mass < 0.0 or not math.isfinite(args.memory_mass):
        raise SystemExit("--memory-mass must be non-negative")


def build_specs(args: argparse.Namespace) -> tuple[KernelSpec, KernelSpec]:
    current = KernelSpec(
        label="current two-scale (1, 35)",
        amplitude_rep=float(args.amplitude_rep),
        sigma_rep=float(args.sigma_rep),
        amplitude_att=float(args.amplitude_att),
        sigma_att=float(args.sigma_att),
    )
    matched_amplitude = attractive_amplitude_for_curvature(
        target_curvature=current.curvature,
        sigma_rep=current.sigma_rep,
        sigma_att=current.sigma_att,
        amplitude_rep=0.0,
    )
    attractive_only = KernelSpec(
        label=f"attractive only (0, {matched_amplitude:g})",
        amplitude_rep=0.0,
        sigma_rep=current.sigma_rep,
        amplitude_att=matched_amplitude,
        sigma_att=current.sigma_att,
    )
    return current, attractive_only


def radial_components(
    radius: np.ndarray,
    spec: KernelSpec,
) -> dict[str, np.ndarray]:
    radius = np.asarray(radius, dtype=float)
    rep_shape = np.exp(-0.5 * np.square(radius / spec.sigma_rep))
    att_shape = np.exp(-0.5 * np.square(radius / spec.sigma_att))
    potential_rep = spec.amplitude_rep * rep_shape
    potential_att = -spec.amplitude_att * att_shape
    force_over_radius_rep = spec.amplitude_rep / spec.sigma_rep**2 * rep_shape
    force_over_radius_att = -spec.amplitude_att / spec.sigma_att**2 * att_shape
    force_over_radius = force_over_radius_rep + force_over_radius_att
    return {
        "potential_rep": potential_rep,
        "potential_att": potential_att,
        "potential": potential_rep + potential_att,
        "force_over_radius_rep": force_over_radius_rep,
        "force_over_radius_att": force_over_radius_att,
        "force_over_radius": force_over_radius,
        "force": radius * force_over_radius,
        "restoring_stiffness": -force_over_radius,
    }


def _plot(
    *,
    args: argparse.Namespace,
    current: KernelSpec,
    attractive_only: KernelSpec,
    output: Path,
) -> None:
    full = np.linspace(0.0, args.full_radius, 1800)
    inner = np.geomspace(
        min(args.epsilon, args.memory_radius) / 20.0,
        args.full_radius,
        2200,
    )
    profiles_full = {
        spec.label: radial_components(full, spec) for spec in (current, attractive_only)
    }
    profiles_inner = {
        spec.label: radial_components(inner, spec)
        for spec in (current, attractive_only)
    }

    fig, axes = plt.subplots(2, 2, figsize=(12.5, 8.2))
    colors = {current.label: "#202020", attractive_only.label: "#147d64"}
    for spec in (current, attractive_only):
        profile = profiles_full[spec.label]
        axes[0, 0].plot(
            full,
            profile["potential"],
            color=colors[spec.label],
            linewidth=2.0,
            label=spec.label,
        )
        axes[0, 1].plot(
            full,
            profile["force"],
            color=colors[spec.label],
            linewidth=2.0,
            label=spec.label,
        )

    current_inner = profiles_inner[current.label]
    axes[1, 0].plot(
        inner,
        current_inner["force_over_radius_rep"],
        label="repulsive contribution",
        color="#c23b22",
        linewidth=1.8,
    )
    axes[1, 0].plot(
        inner,
        current_inner["force_over_radius_att"],
        label="attractive contribution",
        color="#377eb8",
        linewidth=1.8,
    )
    axes[1, 0].plot(
        inner,
        current_inner["force_over_radius"],
        label="total",
        color="#202020",
        linewidth=2.2,
    )
    for spec in (current, attractive_only):
        axes[1, 1].plot(
            inner,
            profiles_inner[spec.label]["restoring_stiffness"],
            color=colors[spec.label],
            linewidth=2.0,
            label=spec.label,
        )

    axes[0, 0].set_title("Point-deposit potential")
    axes[0, 0].set_xlabel("r / sigma_rep")
    axes[0, 0].set_ylabel("K(r)")
    axes[0, 1].set_title("Outward force; negative is inward")
    axes[0, 1].set_xlabel("r / sigma_rep")
    axes[0, 1].set_ylabel("F_out(r) = -dK/dr")
    axes[1, 0].set_title("Current force components on sampled scales")
    axes[1, 0].set_xlabel("r / sigma_rep")
    axes[1, 0].set_ylabel("F_out(r) / r")
    axes[1, 1].set_title("Local restoring stiffness")
    axes[1, 1].set_xlabel("r / sigma_rep")
    axes[1, 1].set_ylabel("-F_out(r) / r")

    for axis in axes.flat:
        axis.axhline(0.0, color="#777777", linewidth=0.8)
        axis.grid(True, alpha=0.22)
        axis.legend(frameon=False, fontsize=8)
    for axis in axes[1]:
        axis.set_xscale("log")
        markers = [
            (args.epsilon, "epsilon"),
            (args.memory_radius, "R_mem"),
            (args.sigma_rep, "sigma_rep"),
            (args.sigma_att, "sigma_att"),
        ]
        for value, label in markers:
            axis.axvline(value, color="#888888", linestyle=":", linewidth=0.9)
            axis.text(
                value,
                0.02,
                label,
                rotation=90,
                va="bottom",
                ha="right",
                fontsize=7,
                color="#666666",
                transform=axis.get_xaxis_transform(),
            )
    fig.suptitle("Kernel core audit: potential amplitude is not local force curvature")
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=190)
    plt.close(fig)


def _fmt(value: Any) -> str:
    number = float(value)
    if abs(number) < 1.0e-3 or abs(number) >= 1.0e4:
        return f"{number:.6e}"
    return f"{number:.6f}"


def write_outputs(args: argparse.Namespace) -> None:
    _validate_args(args)
    current, attractive_only = build_specs(args)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    source_git_revision = _git_output(["rev-parse", "HEAD"])
    source_git_status = _git_output(["status", "--short"])
    _plot(
        args=args,
        current=current,
        attractive_only=attractive_only,
        output=figure,
    )

    rep_curvature = current.amplitude_rep / current.sigma_rep**2
    att_curvature = current.amplitude_att / current.sigma_att**2
    groups = {
        spec.label: asdict(
            scalar_dimensionless_groups(
                epsilon=args.epsilon,
                eta=args.eta,
                lambda_value=args.lambda_value,
                memory_mass=args.memory_mass,
                local_curvature=spec.curvature,
                length_scale=args.sigma_att,
            )
        )
        for spec in (current, attractive_only)
    }
    payload = {
        "description": "Analytic narrow-core and curvature-matched attractive-only audit.",
        "generated_utc": datetime.now(UTC)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "git_revision": source_git_revision,
        "git_status": source_git_status,
        "inputs": vars(args)
        | {
            "report": str(args.report),
            "summary_json": str(args.summary_json),
            "figure": str(args.figure),
        },
        "kernels": [asdict(current), asdict(attractive_only)],
        "dimensionless_groups": groups,
        "diagnostics": {
            "repulsive_potential_fraction_at_origin": current.amplitude_rep
            / current.amplitude_att,
            "repulsive_to_attractive_curvature_ratio": rep_curvature / att_curvature,
            "current_has_repulsive_core": rep_curvature > att_curvature,
            "memory_radius_over_sigma_rep": args.memory_radius / args.sigma_rep,
            "matched_curvature_error": attractive_only.curvature - current.curvature,
        },
    }
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    lines = [
        "# Kernel Core Audit",
        "",
        f"Date: {payload['generated_utc']}.",
        "",
        "## Question",
        "",
        "Does the current `A_rep=1`, `A_att=35`, `sigma_rep=1`,",
        "`sigma_att=3` kernel implement the intended narrow self-avoidance core?",
        "The comparison removes the repulsive component while preserving the",
        "point-deposit restoring curvature exactly.",
        "",
        f"![Kernel core audit]({_rel_from(report, figure)})",
        "",
        "## Analytic comparison",
        "",
        "| kernel | A_rep | A_att | K(0) | restoring curvature | g/update | g/memory time |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for spec in (current, attractive_only):
        group = groups[spec.label]
        lines.append(
            f"| {spec.label} | {_fmt(spec.amplitude_rep)} | {_fmt(spec.amplitude_att)} | "
            f"{_fmt(spec.amplitude_rep - spec.amplitude_att)} | {_fmt(spec.curvature)} | "
            f"{_fmt(group['restoring_per_update'])} | {_fmt(group['restoring_per_memory_time'])} |"
        )
    lines.extend(
        [
            "",
            f"- `A_rep/A_att = {_fmt(current.amplitude_rep / current.amplitude_att)}` in potential amplitude.",
            f"- `(A_rep/sigma_rep^2)/(A_att/sigma_att^2) = {_fmt(rep_curvature / att_curvature)}` in local force curvature.",
            f"- Current near-origin force is repulsive: `{rep_curvature > att_curvature}`.",
            f"- The sampled memory radius is only `{_fmt(args.memory_radius / args.sigma_rep)} sigma_rep`.",
            f"- Curvature-matched attractive-only amplitude: `{_fmt(attractive_only.amplitude_att)}`.",
            "",
            "## Decision",
            "",
            "The narrow positive Gaussian is not an active repulsive core in the",
            "current compact branch. It subtracts about 26% of the attractive local",
            "curvature, while the trajectory samples only the common Taylor regime.",
            "`A_rep=0, A_att=26` is therefore the correct matched ablation. This",
            "analytic result does not yet establish dynamical equivalence; that is",
            "the purpose of the seed-matched regime scan.",
            "",
            "## Provenance",
            "",
            f"- Git revision: `{payload['git_revision']}`",
            f"- Git status: `{payload['git_status'] or 'clean'}`",
            "- Script: `experiments/current/kernels/kernel_core_audit.py`",
            "",
        ]
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_outputs(parse_args())


if __name__ == "__main__":
    main()
