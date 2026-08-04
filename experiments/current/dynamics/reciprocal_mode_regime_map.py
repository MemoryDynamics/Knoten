from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path
import subprocess
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
import numpy as np


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten.reciprocal_modes import reciprocal_scalar_memory_modes  # noqa: E402
from emergenz_knoten.reciprocal_regimes import (  # noqa: E402
    stable_complex_cross_gain_interval,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot local reciprocal scalar-memory mode regimes."
    )
    parser.add_argument("--lambda-value", type=float, default=0.01)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--amplitude-rep", type=float, default=1.0)
    parser.add_argument("--amplitude-att", type=float, default=35.0)
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/reciprocal_mode_regime_lambda001_2026-08-04.png"
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/reciprocal_local_mode_gate_2026-08-04.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/response/reciprocal_local_mode_gate_2026-08-04.json"),
    )
    return parser.parse_args()


def _git_output(*args: str) -> str:
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


def _regime_grid(
    lambda_value: float,
    self_gains: np.ndarray,
    cross_gains: np.ndarray,
) -> np.ndarray:
    g, c = np.meshgrid(self_gains, cross_gains)
    q = 1.0 - lambda_value
    trace = 2.0 - lambda_value - q * g - (1.0 + lambda_value) * c
    determinant = q * (1.0 - g - c)
    discriminant = np.square(trace) - 4.0 * determinant
    complex_mode = discriminant < 0.0

    real_root = np.sqrt(np.maximum(discriminant, 0.0))
    real_radius = np.maximum(
        np.abs(0.5 * (trace + real_root)),
        np.abs(0.5 * (trace - real_root)),
    )
    complex_radius = np.sqrt(np.maximum(determinant, 0.0))
    radius = np.where(complex_mode, complex_radius, real_radius)
    stable = radius < 1.0

    regime = np.zeros_like(trace, dtype=np.int8)
    regime[complex_mode & stable] = 1
    regime[~complex_mode & ~stable] = 2
    regime[complex_mode & ~stable] = 3
    return regime


def _plot_panel(
    axis: plt.Axes,
    *,
    lambda_value: float,
    g_limit: tuple[float, float],
    c_limit: tuple[float, float],
    baseline_gain: float,
    title: str,
) -> None:
    self_gains = np.linspace(*g_limit, 700)
    cross_gains = np.linspace(*c_limit, 700)
    regime = _regime_grid(lambda_value, self_gains, cross_gains)
    colors = ListedColormap(["#d9d9d9", "#168b8c", "#d64b3c", "#7856a6"])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], colors.N)
    axis.pcolormesh(
        self_gains,
        cross_gains,
        regime,
        shading="auto",
        cmap=colors,
        norm=norm,
        rasterized=True,
    )
    line_g = np.linspace(*g_limit, 500)
    axis.plot(line_g, line_g, color="#111111", linestyle="--", linewidth=1.0)
    axis.plot(
        line_g,
        1.0 - line_g,
        color="#111111",
        linestyle=":",
        linewidth=1.0,
    )
    threshold = lambda_value / (1.0 + lambda_value)
    axis.axvline(threshold, color="#006c67", linewidth=1.1)
    if g_limit[0] <= baseline_gain <= g_limit[1]:
        axis.axvline(baseline_gain, color="#1f4e79", linewidth=1.6)
        axis.text(
            baseline_gain,
            c_limit[1] * 0.96,
            "current self gain",
            color="#1f4e79",
            rotation=90,
            va="top",
            ha="right",
            fontsize=8,
        )
    axis.set_xlim(g_limit)
    axis.set_ylim(c_limit)
    axis.set_xlabel(r"self gain $g$")
    axis.set_ylabel(r"cross gain $c$")
    axis.set_title(title, fontsize=10)
    axis.grid(False)


def main() -> None:
    args = parse_args()
    curvature = (
        args.amplitude_att / args.sigma_att**2
        - args.amplitude_rep / args.sigma_rep**2
    )
    baseline_gain = args.eta * args.memory_mass * curvature
    threshold = args.lambda_value / (1.0 + args.lambda_value)
    weak_interval = stable_complex_cross_gain_interval(
        args.lambda_value,
        self_gain=0.0,
    )
    baseline_interval = stable_complex_cross_gain_interval(
        args.lambda_value,
        self_gain=baseline_gain,
    )
    witness_cross_gain = 0.02
    witness = reciprocal_scalar_memory_modes(
        args.lambda_value,
        self_gain=0.0,
        cross_gain=witness_cross_gain,
    )

    figure_path = ROOT / args.figure
    report_path = ROOT / args.report
    summary_path = ROOT / args.summary_json
    for path in (figure_path, report_path, summary_path):
        path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.4), constrained_layout=True)
    _plot_panel(
        axes[0],
        lambda_value=args.lambda_value,
        g_limit=(0.0, 0.5),
        c_limit=(0.0, 1.0),
        baseline_gain=baseline_gain,
        title="Full gain range",
    )
    _plot_panel(
        axes[1],
        lambda_value=args.lambda_value,
        g_limit=(0.0, 0.012),
        c_limit=(0.0, 0.065),
        baseline_gain=baseline_gain,
        title="Complex-mode window near the origin",
    )
    fig.suptitle(
        rf"Reciprocal local-memory modes ($\lambda={args.lambda_value:g}$)",
        fontsize=12,
    )
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color="#d9d9d9", label="real, stable"),
        plt.Rectangle((0, 0), 1, 1, color="#168b8c", label="complex, stable"),
        plt.Rectangle((0, 0), 1, 1, color="#d64b3c", label="real, unstable"),
        plt.Rectangle((0, 0), 1, 1, color="#7856a6", label="complex, unstable"),
    ]
    fig.legend(
        handles=legend_handles,
        loc="outside lower center",
        ncol=4,
        frameon=False,
        fontsize=8,
    )
    fig.savefig(figure_path, dpi=220, bbox_inches="tight")
    plt.close(fig)

    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "git_revision": _git_output("rev-parse", "HEAD"),
        "git_status_porcelain": _git_output("status", "--porcelain"),
        "lambda_value": args.lambda_value,
        "complex_window_self_gain_threshold": threshold,
        "baseline": {
            "eta": args.eta,
            "memory_mass": args.memory_mass,
            "local_curvature": curvature,
            "self_gain": baseline_gain,
            "stable_complex_cross_gain_interval": None
            if baseline_interval is None
            else [baseline_interval.lower, baseline_interval.upper],
        },
        "weak_self_gain_witness": {
            "self_gain": 0.0,
            "stable_complex_cross_gain_interval": None
            if weak_interval is None
            else [weak_interval.lower, weak_interval.upper],
            "cross_gain": witness_cross_gain,
            "relative_multipliers": [
                [value.real, value.imag] for value in witness.relative_multipliers
            ],
            "angular_frequency_per_update": witness.relative_angular_frequency,
            "damping_rate_per_update": witness.relative_damping_rate,
        },
        "decision": "instantaneous_reciprocal_baseline_is_a_real_mode_null",
        "next_gate": "paired_off_one_way_reciprocal_and_retarded_reciprocal",
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    report = rf"""# Reciprocal local-mode gate

Status: structural analytic gate. Date: 2026-08-04.

## Question

Can a synchronous reciprocal return channel between two scalar-memory knots
produce a stable complex relative mode without adding inertia or an explicit
wave equation?

## Result

For the local reduction, stable complex modes require both a negative mode
discriminant and multipliers inside the unit circle. A positive cross-gain
window exists only when

$$
g < \frac{{\lambda}}{{1+\lambda}}.
$$

At $\lambda={args.lambda_value:g}$ the threshold is `{threshold:.8g}`. The
current compact-knot baseline has local curvature `{curvature:.8g}` and
$g={baseline_gain:.8g}$, so it has no stable complex cross-gain interval.

For the weak-self witness $g=0$, the stable complex interval is
`({weak_interval.lower:.8g}, {weak_interval.upper:.8g})`. At $c=0.02$ the
frequency is `{witness.relative_angular_frequency:.8g}` per update and the
damping rate is `{witness.relative_damping_rate:.8g}` per update.

The condition $c>g$ is necessary inside the stable complex region. In contrast,
$g+c>1$ makes the determinant negative and therefore gives two real
opposite-sign multipliers. Those multipliers can still both lie inside the unit
circle; this is an alternating real mode, not a harmonic oscillator.

## Interpretation

- **Evidence:** the common/relative formulas match the full four-state matrix;
  the regime boundaries are analytic and unit-tested.
- **Inference:** an instantaneous reciprocal continuation of the current
  compact checkpoints should be treated as a real-mode null and nonlinear
  reconciliation test.
- **Hypothesis:** a retarded reciprocal mediator may create sufficient phase lag
  for a complex mode at compact-knot self gain.
- **Not supported:** charge, flavor, particle identity, spatial rotation, or
  ambient-independent three-dimensional selection.

The complex rotation here is in the state-space plane $(x_-,m_-)$ and already
exists in a one-dimensional spatial model. It cannot by itself explain $d=3$.

## Registered next gate

Use mature stored knot states and common noise in four paired arms:

1. channel off;
2. one-way cross-readout;
3. synchronous instantaneous reciprocal cross-readout;
4. reciprocal readout through one fixed local mediator.

Primary observables are relative-center multipliers, damping, frequency, phase
continuity, radius and shape bounds, and separation from the paired controls.
No cross-gain retuning follows a failed instantaneous arm.

![Reciprocal mode regime map](../../{args.figure.as_posix()})

Machine-readable summary: [{args.summary_json.name}]({args.summary_json.name}).
"""
    report_path.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
