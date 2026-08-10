from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import subprocess

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


@dataclass(frozen=True)
class KernelAuditMetrics:
    dimension: int
    sigma_rep: float
    sigma_att: float
    amplitude_rep: float
    amplitude_att: float
    scale_ratio: float
    local_curvature: float
    effective_amplitude: float
    matched_attractive_amplitude: float
    log_polynomial_amplitude: float
    log_laplacian_amplitude: float
    log_central_depth: float
    sampled_radius_over_reference_scale: float
    volume_ratio: float
    raw_amplitude_if_effective_equals_volume_ratio: float
    two_scale_zero_mean_attractive_amplitude: float


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
            "Compare the current two-scale kernel, its curvature-matched "
            "attractive-only reduction, and a zero-mean Laplacian-of-Gaussian "
            "completion at fixed local curvature."
        )
    )
    parser.add_argument("--dimension", type=int, default=3)
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--amplitude-rep", type=float, default=1.0)
    parser.add_argument("--amplitude-att", type=float, default=35.0)
    parser.add_argument("--memory-radius", type=float, default=1.94163e-4)
    parser.add_argument("--max-radius-over-l", type=float, default=5.0)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/kernels/core/log_taylor_kernel_audit_2026-07-28.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/kernels/core/log_taylor_kernel_audit_2026-07-28.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/kernels/core_2026-07-28/log_taylor_kernel_audit.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative_link(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _validate_args(args: argparse.Namespace) -> None:
    if args.dimension < 1:
        raise SystemExit("--dimension must be at least one")
    for name in ("sigma_rep", "sigma_att", "memory_radius", "max_radius_over_l"):
        value = float(getattr(args, name))
        if not math.isfinite(value) or value <= 0.0:
            raise SystemExit(f"--{name.replace('_', '-')} must be positive and finite")
    for name in ("amplitude_rep", "amplitude_att"):
        value = float(getattr(args, name))
        if not math.isfinite(value) or value < 0.0:
            raise SystemExit(
                f"--{name.replace('_', '-')} must be non-negative and finite"
            )


def build_metrics(args: argparse.Namespace) -> KernelAuditMetrics:
    _validate_args(args)
    scale_ratio = float(args.sigma_att / args.sigma_rep)
    curvature = (
        args.amplitude_att / args.sigma_att**2
        - args.amplitude_rep / args.sigma_rep**2
    )
    if curvature <= 0.0:
        raise SystemExit("the reference kernel must have positive restoring curvature")

    effective_amplitude = curvature * args.sigma_att**2
    log_polynomial_amplitude = effective_amplitude / (args.dimension + 2.0)
    volume_ratio = scale_ratio**args.dimension
    return KernelAuditMetrics(
        dimension=int(args.dimension),
        sigma_rep=float(args.sigma_rep),
        sigma_att=float(args.sigma_att),
        amplitude_rep=float(args.amplitude_rep),
        amplitude_att=float(args.amplitude_att),
        scale_ratio=scale_ratio,
        local_curvature=float(curvature),
        effective_amplitude=float(effective_amplitude),
        matched_attractive_amplitude=float(effective_amplitude),
        log_polynomial_amplitude=float(log_polynomial_amplitude),
        log_laplacian_amplitude=float(
            log_polynomial_amplitude * args.sigma_att**2
        ),
        log_central_depth=float(args.dimension * log_polynomial_amplitude),
        sampled_radius_over_reference_scale=float(
            args.memory_radius / args.sigma_att
        ),
        volume_ratio=float(volume_ratio),
        raw_amplitude_if_effective_equals_volume_ratio=float(
            volume_ratio
            + args.amplitude_rep * args.sigma_att**2 / args.sigma_rep**2
        ),
        two_scale_zero_mean_attractive_amplitude=float(
            args.amplitude_rep / volume_ratio
        ),
    )


def kernel_profiles(
    radius_over_l: np.ndarray,
    metrics: KernelAuditMetrics,
) -> dict[str, dict[str, np.ndarray]]:
    u = np.asarray(radius_over_l, dtype=float)
    if np.any(u < 0.0) or not np.all(np.isfinite(u)):
        raise ValueError("radius_over_l must be finite and non-negative")

    length = metrics.sigma_att
    radius = length * u
    curvature_scale = metrics.local_curvature * length**2
    broad = np.exp(-0.5 * np.square(u))
    narrow = np.exp(-0.5 * np.square(radius / metrics.sigma_rep))

    current_potential = (
        metrics.amplitude_rep * narrow - metrics.amplitude_att * broad
    )
    current_gradient = radius * (
        -metrics.amplitude_rep / metrics.sigma_rep**2 * narrow
        + metrics.amplitude_att / length**2 * broad
    )

    matched_potential = -metrics.matched_attractive_amplitude * broad
    matched_gradient = (
        metrics.matched_attractive_amplitude / length * u * broad
    )

    log_potential = (
        metrics.log_polynomial_amplitude
        * (np.square(u) - metrics.dimension)
        * broad
    )
    log_gradient = (
        metrics.log_polynomial_amplitude
        / length
        * u
        * (metrics.dimension + 2.0 - np.square(u))
        * broad
    )

    raw = {
        "two_scale": (current_potential, current_gradient),
        "attractive_only": (matched_potential, matched_gradient),
        "log": (log_potential, log_gradient),
    }
    profiles: dict[str, dict[str, np.ndarray]] = {}
    for label, (potential, gradient) in raw.items():
        outward_force = -gradient
        restoring_ratio = np.ones_like(u)
        positive = u > 0.0
        restoring_ratio[positive] = (
            gradient[positive]
            / (metrics.local_curvature * radius[positive])
        )
        profiles[label] = {
            "potential": potential,
            "potential_rise": (potential - potential[0]) / curvature_scale,
            "outward_force": outward_force
            / (metrics.local_curvature * length),
            "restoring_ratio": restoring_ratio,
        }
    return profiles


def cumulative_radial_moment(
    radius_over_l: np.ndarray,
    normalized_potential: np.ndarray,
    *,
    dimension: int,
) -> np.ndarray:
    u = np.asarray(radius_over_l, dtype=float)
    values = np.asarray(normalized_potential, dtype=float)
    if u.ndim != 1 or values.shape != u.shape or u.size < 2:
        raise ValueError("radius and potential must be matching one-dimensional arrays")
    integrand = np.power(u, dimension - 1) * values
    increments = 0.5 * (integrand[1:] + integrand[:-1]) * np.diff(u)
    return np.concatenate(([0.0], np.cumsum(increments)))


def gaussian_radial_factor(dimension: int) -> float:
    return 2.0 ** (dimension / 2.0 - 1.0) * math.gamma(dimension / 2.0)


def analytic_radial_integrals(
    metrics: KernelAuditMetrics,
) -> dict[str, float]:
    factor = gaussian_radial_factor(metrics.dimension)
    curvature_scale = metrics.local_curvature * metrics.sigma_att**2
    narrow_scale = metrics.sigma_rep / metrics.sigma_att
    current = factor * (
        metrics.amplitude_rep / curvature_scale * narrow_scale**metrics.dimension
        - metrics.amplitude_att / curvature_scale
    )
    return {
        "two_scale": float(current),
        "attractive_only": float(-factor),
        "log": 0.0,
    }


def dimensionless_force_cubic_coefficients(
    metrics: KernelAuditMetrics,
) -> dict[str, float]:
    """Return c3 L^2/kappa for F_out=-kappa r+c3 r^3+O(r^5)."""

    current_cubic = (
        -metrics.amplitude_rep / (2.0 * metrics.sigma_rep**4)
        + metrics.amplitude_att / (2.0 * metrics.sigma_att**4)
    )
    return {
        "two_scale": float(
            current_cubic * metrics.sigma_att**2 / metrics.local_curvature
        ),
        "attractive_only": 0.5,
        "log": float((metrics.dimension + 4.0) / (2.0 * (metrics.dimension + 2.0))),
    }


def _plot(
    *,
    args: argparse.Namespace,
    metrics: KernelAuditMetrics,
    output: Path,
) -> None:
    u = np.linspace(0.0, args.max_radius_over_l, 2401)
    profiles = kernel_profiles(u, metrics)
    normalized_potentials = {
        label: profile["potential"]
        / (metrics.local_curvature * metrics.sigma_att**2)
        for label, profile in profiles.items()
    }
    cumulative = {
        label: cumulative_radial_moment(
            u,
            normalized_potentials[label],
            dimension=metrics.dimension,
        )
        for label in profiles
    }

    log_min = max(metrics.sampled_radius_over_reference_scale / 100.0, 1.0e-8)
    u_log = np.geomspace(log_min, args.max_radius_over_l, 2401)
    profiles_log = kernel_profiles(u_log, metrics)

    labels = {
        "two_scale": (
            f"two-scale ({metrics.amplitude_rep:g}, {metrics.amplitude_att:g})"
        ),
        "attractive_only": (
            f"matched one-scale (0, {metrics.matched_attractive_amplitude:g})"
        ),
        "log": f"zero-mean LoG (B={metrics.log_polynomial_amplitude:g})",
    }
    colors = {
        "two_scale": "#202020",
        "attractive_only": "#147d64",
        "log": "#d06b25",
    }
    linestyles = {"two_scale": "-", "attractive_only": "--", "log": "-."}

    fig, axes = plt.subplots(2, 2, figsize=(12.6, 8.4))
    for label in ("two_scale", "attractive_only", "log"):
        style = {
            "color": colors[label],
            "linestyle": linestyles[label],
            "linewidth": 2.0,
            "label": labels[label],
        }
        axes[0, 0].plot(u, profiles[label]["potential_rise"], **style)
        axes[0, 1].plot(u, profiles[label]["outward_force"], **style)
        axes[1, 0].plot(u_log, profiles_log[label]["restoring_ratio"], **style)
        axes[1, 1].plot(u, cumulative[label], **style)

    axes[0, 0].set_title("Potential rise from the common local minimum")
    axes[0, 0].set_ylabel("[K(r)-K(0)] / (kappa L^2)")
    axes[0, 1].set_title("Radial force")
    axes[0, 1].set_ylabel("F_out / (kappa L)")
    axes[1, 0].set_title("Local restoring factor")
    axes[1, 0].set_ylabel("-F_out / (kappa r)")
    axes[1, 0].set_xscale("log")
    axes[1, 1].set_title("Cumulative radial kernel moment")
    axes[1, 1].set_ylabel("integral_0^u s^(d-1) K(Ls)/(kappa L^2) ds")
    for axis in axes.flat:
        axis.set_xlabel("u = r / L")
        axis.axhline(0.0, color="#777777", linewidth=0.8)
        axis.grid(True, alpha=0.22)
        axis.legend(frameon=False, fontsize=8)

    axes[1, 0].axvline(
        metrics.sampled_radius_over_reference_scale,
        color="#6f6f6f",
        linestyle=":",
        linewidth=1.1,
    )
    axes[1, 0].text(
        metrics.sampled_radius_over_reference_scale,
        0.03,
        "sampled R_mem/L",
        rotation=90,
        va="bottom",
        ha="right",
        fontsize=7,
        color="#666666",
        transform=axes[1, 0].get_xaxis_transform(),
    )
    axes[0, 0].axvline(
        math.sqrt(metrics.dimension),
        color=colors["log"],
        linestyle=":",
        linewidth=1.0,
        alpha=0.75,
    )
    axes[0, 1].axvline(
        math.sqrt(metrics.dimension + 2.0),
        color=colors["log"],
        linestyle=":",
        linewidth=1.0,
        alpha=0.75,
    )
    fig.suptitle(
        "Curvature-matched kernel audit: local Taylor data versus global neutrality"
    )
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=190)
    plt.close(fig)


def _fmt(value: float) -> str:
    if value == 0.0:
        return "0"
    if abs(value) < 1.0e-3 or abs(value) >= 1.0e4:
        return f"{value:.6e}"
    return f"{value:.6f}"


def write_outputs(args: argparse.Namespace) -> None:
    metrics = build_metrics(args)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    git_revision = _git_output(["rev-parse", "HEAD"])
    git_status = _git_output(["status", "--short"])
    integrals = analytic_radial_integrals(metrics)
    cubic = dimensionless_force_cubic_coefficients(metrics)

    _plot(args=args, metrics=metrics, output=figure)
    payload = {
        "description": (
            "Analytic curvature-matched comparison of the current Gaussian "
            "families and a zero-mean Laplacian-of-Gaussian completion."
        ),
        "generated_utc": datetime.now(UTC)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "git_revision": git_revision,
        "git_status": git_status,
        "inputs": {
            key: str(value) if isinstance(value, Path) else value
            for key, value in vars(args).items()
        },
        "metrics": asdict(metrics),
        "dimensionless_force_cubic_coefficients": cubic,
        "dimensionless_total_radial_integrals": integrals,
        "claims": {
            "log_is_exactly_zero_mean": True,
            "current_and_matched_one_scale_share_local_curvature": True,
            "log_derives_current_amplitudes": False,
            "integer_36_requires_extra_effective_equals_volume_hypothesis": True,
        },
    }
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    rows = [
        (
            f"two-scale ({metrics.amplitude_rep:g}, {metrics.amplitude_att:g})",
            metrics.local_curvature,
            cubic["two_scale"],
            integrals["two_scale"],
        ),
        (
            f"matched one-scale (0, {metrics.matched_attractive_amplitude:g})",
            metrics.local_curvature,
            cubic["attractive_only"],
            integrals["attractive_only"],
        ),
        (
            f"zero-mean LoG (B={metrics.log_polynomial_amplitude:g})",
            metrics.local_curvature,
            cubic["log"],
            integrals["log"],
        ),
    ]
    lines = [
        "# LoG / Taylor Kernel Audit",
        "",
        f"Date: {payload['generated_utc']}.",
        "",
        "## Question",
        "",
        "Can a Laplacian-of-Gaussian (LoG) provide a minimal decaying,",
        "exactly zero-mean completion of the local Taylor data, and does that",
        "construction determine the previously used amplitudes?",
        "",
        "The comparison is analytic. It fixes the local restoring curvature of",
        f"the current `(A_rep,A_att)=({metrics.amplitude_rep:g},{metrics.amplitude_att:g})`,",
        f"`(sigma_rep,sigma_att)=({metrics.sigma_rep:g},{metrics.sigma_att:g})` kernel",
        "and uses `L=sigma_att`. No trajectory is fitted and no amplitude is swept.",
        "",
        f"![LoG and Taylor kernel audit]({_relative_link(report, figure)})",
        "",
        "## What LoG means here",
        "",
        "For `u=r/L`, the tested radial kernel is",
        "",
        "```text",
        "K_LoG(r) = B (u^2-d) exp(-u^2/2)",
        "B = kappa L^2/(d+2).",
        "```",
        "",
        "It is proportional to the Laplacian of a Gaussian. Therefore it decays,",
        "has `int K_LoG dx=0` exactly, and has the same local Hessian `kappa I`",
        "as the two reference kernels. It is a global regularized completion of",
        "local Taylor information, not a derivation of the fundamental kernel.",
        "",
        "## Matched invariants",
        "",
        "For `F_out=-kappa r+c3 r^3+O(r^5)`, the table reports",
        "`c3 L^2/kappa`. The radial integral omits the common unit-sphere area;",
        "zero versus nonzero is unchanged.",
        "",
        "| family | kappa | c3 L^2/kappa | total radial integral |",
        "| --- | ---: | ---: | ---: |",
    ]
    for label, curvature, cubic_value, integral in rows:
        lines.append(
            f"| {label} | {_fmt(curvature)} | {_fmt(cubic_value)} | "
            f"{_fmt(integral)} |"
        )
    lines.extend(
        [
            "",
            "All three families agree only through the linear restoring term.",
            "The two-scale kernel has the opposite first nonlinear force correction",
            "from the matched one-scale and LoG kernels. The historical compact",
            f"branch samples only `R_mem/L={metrics.sampled_radius_over_reference_scale:.6e}`;",
            "at that radius these higher-order differences are not identifiable.",
            "",
            "## Where 26, 27, and 36 come from",
            "",
            "| quantity | formula | value | interpretation |",
            "| --- | --- | ---: | --- |",
            f"| current effective amplitude | `A_att-A_rep q^2` | {_fmt(metrics.effective_amplitude)} | exact local-curvature mapping of `(1,35)` to `(0,26)` |",
            f"| volume ratio | `q^d` | {_fmt(metrics.volume_ratio)} | geometry of `q={metrics.scale_ratio:g}` in `d={metrics.dimension}`; not a fitted coupling |",
            f"| raw amplitude if one additionally sets `A_eff=q^d` | `q^d+A_rep q^2` | {_fmt(metrics.raw_amplitude_if_effective_equals_volume_ratio)} | gives 36, but the extra equality has no present dynamical derivation |",
            f"| zero-mean two-scale attractive amplitude | `A_rep q^(-d)` | {_fmt(metrics.two_scale_zero_mean_attractive_amplitude)} | note the inverse 27; incompatible with the current restoring branch |",
            f"| LoG polynomial amplitude | `A_eff/(d+2)` | {_fmt(metrics.log_polynomial_amplitude)} | normalization-dependent coefficient, not 26/27/35/36 |",
            f"| LoG central depth | `d A_eff/(d+2)` | {_fmt(metrics.log_central_depth)} | also normalization-dependent |",
            "",
            "No invariant in this construction singles out 29. The pair `27/36`",
            "does occur algebraically because `3^3=27` and the q=3 curvature offset",
            "is `3^2=9`, but adding them becomes a model hypothesis, not a result.",
            "The existing amplitude scan found a smooth relaxation branch rather",
            "than a sharp selector at 26, 27, 35, or 36.",
            "",
            "## Decision",
            "",
            "LoG is worth retaining as one fixed zero-mean null family. It combines",
            "decay, exact global compensation, and a prescribed local curvature in",
            "one scale. It does not explain the historical amplitudes, select d=3,",
            "or add phase, spin, or propagation. A dynamic comparison is justified",
            "only after a trajectory samples radii large enough for the predeclared",
            "cubic-force differences to exceed measurement uncertainty.",
            "",
            "## Provenance",
            "",
            f"- Git revision: `{git_revision}`",
            f"- Git status before generation: `{git_status or 'clean'}`",
            "- Script: `experiments/current/kernels/families/log_taylor_kernel_audit.py`",
        ]
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    write_outputs(parse_args())


if __name__ == "__main__":
    main()
