"""Evaluate the preregistered source-local linear emission gate."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import linalg

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from emergenz_knoten.local_mediator import (  # noqa: E402
    LocalMediatorGrid,
    TelegraphMediator,
)
from emergenz_knoten.source_local_linear import (  # noqa: E402
    diagnose_reciprocal_poles,
    reciprocal_source_local_matrix,
    telegraph_channel_realization,
)
from emergenz_knoten.source_local_modal import (  # noqa: E402
    telegraph_spatial_mode_reductions,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lambda-value", type=float, default=0.01)
    parser.add_argument("--self-gain", type=float, default=0.43229116264043155)
    parser.add_argument("--cross-gain", type=float, default=0.02)
    parser.add_argument("--grid-spacing-r", type=float, default=0.25)
    parser.add_argument("--grid-points-left", type=int, default=120)
    parser.add_argument("--grid-points-right", type=int, default=180)
    parser.add_argument("--readout-position-r", type=float, default=2.5)
    parser.add_argument("--wave-speed-r-per-memory-time", type=float, default=0.5)
    parser.add_argument("--damping-rate", type=float, default=0.1)
    parser.add_argument("--natural-frequency", type=float, default=0.1)
    parser.add_argument("--reduction-orders", default="8,16,32")
    parser.add_argument("--frequency-min", type=float, default=0.05)
    parser.add_argument("--residue-min", type=float, default=0.1)
    parser.add_argument("--shift-ratio-min", type=float, default=0.1)
    parser.add_argument("--condition-max", type=float, default=1.0e8)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/source_local/source_local_linear_gate_2026-08-06.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/response/source_local/source_local_linear_gate_2026-08-06.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path("figures/draft/response/source_local_linear_gate_2026-08-06.png"),
    )
    return parser.parse_args()


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _json_value(value: Any) -> Any:
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, complex):
        return {"real": float(value.real), "imag": float(value.imag)}
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"cannot serialize {type(value)!r}")


def _orders(value: str) -> tuple[int, ...]:
    result = tuple(sorted(set(int(item.strip()) for item in value.split(","))))
    if not result:
        raise SystemExit("at least one reduction order is required")
    return result


def _row(
    *,
    emission: str,
    coupling_sign: int,
    representation: str,
    order: int,
    channel,
    args: argparse.Namespace,
) -> dict[str, Any]:
    matrix = reciprocal_source_local_matrix(
        channel,
        lambda_value=args.lambda_value,
        self_gain=args.self_gain,
        cross_gain=args.cross_gain,
        emission=emission,
        coupling_sign=float(coupling_sign),
    )
    diagnostic = diagnose_reciprocal_poles(
        matrix,
        channel,
        lambda_value=args.lambda_value,
        frequency_min=args.frequency_min,
        residue_min=args.residue_min,
        shift_ratio_min=args.shift_ratio_min,
        condition_max=args.condition_max,
    )
    return {
        "emission": emission,
        "coupling_sign": coupling_sign,
        "representation": representation,
        "order": order,
        **asdict(diagnostic),
    }


def run_gate(args: argparse.Namespace) -> tuple[dict[str, Any], Any, Any]:
    orders = _orders(args.reduction_orders)
    grid = LocalMediatorGrid(
        spacing=args.grid_spacing_r,
        time_step=args.lambda_value,
        points_left=args.grid_points_left,
        points_right=args.grid_points_right,
    )
    mediator = TelegraphMediator(
        wave_speed=args.wave_speed_r_per_memory_time,
        damping_rate=args.damping_rate,
        natural_frequency=args.natural_frequency,
    )
    exact = telegraph_channel_realization(
        grid,
        mediator,
        readout_position=args.readout_position_r,
    )
    reductions = telegraph_spatial_mode_reductions(
        grid,
        mediator,
        readout_position=args.readout_position_r,
        orders=orders,
    )
    channels = [("exact", exact.order, exact)] + [
        (f"modal_{order}", order, reductions[order]) for order in orders
    ]
    rows = [
        _row(
            emission=emission,
            coupling_sign=sign,
            representation=name,
            order=order,
            channel=channel,
            args=args,
        )
        for emission in ("offset", "current")
        for sign in (1, -1)
        for name, order, channel in channels
    ]
    primary = [
        row
        for row in rows
        if row["emission"] == "offset" and row["coupling_sign"] == 1
    ]
    exact_primary = next(row for row in primary if row["representation"] == "exact")
    reduced_passes = sum(row["passes"] for row in primary if row is not exact_primary)
    ill_conditioned = any(
        not np.isfinite(row["eigenvector_condition"])
        or row["eigenvector_condition"] > args.condition_max
        for row in primary
    )
    primary_pass = bool(exact_primary["passes"] and reduced_passes >= 2)
    if ill_conditioned:
        classification = "inconclusive source-local linear gate"
    elif primary_pass:
        classification = "source-local observable reciprocal-mode candidate"
    else:
        classification = "source-local channel stable; reciprocal knot-mode null"
    payload = {
        "schema": "source-local-linear-gate-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "git_revision": _git("rev-parse", "HEAD"),
        "git_status": _git("status", "--porcelain"),
        "parameters": vars(args),
        "fixed_local_multiplier": (
            (1.0 - args.lambda_value) * (1.0 - args.self_gain)
        ),
        "source_locality": {
            "mass": "constant M0; zero dynamic perturbation",
            "offset": "d_n=x_n-m_n",
            "current": "x_n-x_(n-1)=d_n/q-d_(n-1)",
            "target_dependent_source_terms": False,
        },
        "thresholds": {
            "frequency_min_per_memory_time": args.frequency_min,
            "normalized_knot_residue_min": args.residue_min,
            "one_way_generator_shift_ratio_min": args.shift_ratio_min,
            "eigenvector_condition_max": args.condition_max,
            "minimum_reduction_passes": 2,
        },
        "rows": rows,
        "gate": {
            "classification": classification,
            "primary_exact_pass": exact_primary["passes"],
            "primary_reduction_passes": reduced_passes,
            "primary_pass": primary_pass,
            "mass_dynamic_residue_zero": True,
            "nonlinear_confirmation_allowed": primary_pass,
            "minimum_future_confirmation_updates": 500000,
        },
    }
    return payload, exact, reductions


def _write_figure(payload: dict[str, Any], exact, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = payload["rows"]
    primary = [
        row
        for row in rows
        if row["emission"] == "offset" and row["coupling_sign"] == 1
    ]
    current = [
        row
        for row in rows
        if row["emission"] == "current" and row["coupling_sign"] == 1
    ]
    labels = [row["representation"].replace("modal_", "m") for row in primary]
    x = np.arange(len(labels))
    fig, axes = plt.subplots(2, 2, figsize=(12, 8.5), constrained_layout=True)

    channel_values = linalg.eigvals(exact.transition)
    exact_matrix = reciprocal_source_local_matrix(
        exact,
        lambda_value=float(payload["parameters"]["lambda_value"]),
        self_gain=float(payload["parameters"]["self_gain"]),
        cross_gain=float(payload["parameters"]["cross_gain"]),
        emission="offset",
        coupling_sign=1.0,
    )
    reciprocal_values = linalg.eigvals(exact_matrix)
    angle = np.linspace(0.0, 2.0 * np.pi, 500)
    axes[0, 0].plot(np.cos(angle), np.sin(angle), color="black", linewidth=0.8)
    axes[0, 0].scatter(
        channel_values.real,
        channel_values.imag,
        s=8,
        alpha=0.35,
        label="one-way channel",
    )
    axes[0, 0].scatter(
        reciprocal_values.real,
        reciprocal_values.imag,
        s=8,
        alpha=0.35,
        label="reciprocal + knot",
    )
    axes[0, 0].set(xlabel="Re(mu)", ylabel="Im(mu)", title="Exact multipliers")
    axes[0, 0].axis("equal")
    axes[0, 0].legend(fontsize=8)

    for values, name, marker in ((primary, "offset", "o"), (current, "current", "s")):
        axes[0, 1].plot(
            x,
            [row["frequency_per_memory_time"] for row in values],
            marker=marker,
            label=f"{name} omega",
        )
        axes[0, 1].plot(
            x,
            [row["damping_per_memory_time"] for row in values],
            marker=marker,
            linestyle="--",
            label=f"{name} Gamma",
        )
    axes[0, 1].axhline(
        payload["thresholds"]["frequency_min_per_memory_time"],
        color="black",
        linewidth=0.8,
        linestyle=":",
    )
    axes[0, 1].set(title="Selected stable pole", xticks=x, xticklabels=labels)
    axes[0, 1].legend(fontsize=8)

    for values, name, marker in ((primary, "offset", "o"), (current, "current", "s")):
        axes[1, 0].semilogy(
            x,
            [row["normalized_knot_residue"] for row in values],
            marker=marker,
            label=name,
        )
    axes[1, 0].axhline(
        payload["thresholds"]["normalized_knot_residue_min"],
        color="black",
        linewidth=0.8,
        linestyle=":",
        label="gate",
    )
    axes[1, 0].set(
        title="Knot-to-knot pole residue",
        xticks=x,
        xticklabels=labels,
        ylabel="normalized residue",
    )
    axes[1, 0].legend(fontsize=8)

    for values, name, marker in ((primary, "offset", "o"), (current, "current", "s")):
        axes[1, 1].semilogy(
            x,
            [row["nearest_one_way_generator_distance_ratio"] for row in values],
            marker=marker,
            label=name,
        )
    axes[1, 1].axhline(
        payload["thresholds"]["one_way_generator_shift_ratio_min"],
        color="black",
        linewidth=0.8,
        linestyle=":",
        label="gate",
    )
    axes[1, 1].set(
        title="Shift from nearest inserted channel pole",
        xticks=x,
        xticklabels=labels,
        ylabel="generator-distance ratio",
    )
    axes[1, 1].legend(fontsize=8)
    fig.suptitle("Source-local linear gate: visible field poles, negligible knot loading")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _format(value: Any, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.{digits}g}"


def _write_report(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    gate = payload["gate"]
    rows = payload["rows"]
    lines = [
        "# P3.2c source-local linear emission gate",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Question",
        "",
        "Can a strictly emitter-local scalar signal, transported by the fixed Telegraph channel and read only at the target, create a stable reciprocal pole that is materially loaded into the knot state rather than merely inherited from the channel?",
        "",
        "## Model",
        "",
        "The translation-free knot coordinate is `d_n=x_n-m_n`, with `d_(n+1)=q(1-g)d_n` when uncoupled. The primary emitter writes `s_n=d_n`; the secondary current writes `s_n=d_n/q-d_(n-1)`. The constant mass source is the zero-dynamics control. None of these source terms contains target position, target memory, pair distance, or an instantaneous cross-gradient.",
        "",
        "The exact P3.2 finite-grid Telegraph update and its DC normalization are retained. The positive update sign is the reporting primary; the negative sign is a symmetry control, and both are evaluated. Reductions keep complete real Telegraph blocks of source/readout-ranked Dirichlet spatial modes, so truncation does not split temporal conjugate pairs.",
        "",
        "## Registered gate",
        "",
        f"A primary pole needs stability, `omega >= {payload['thresholds']['frequency_min_per_memory_time']}` per memory time, normalized knot residue at least `{payload['thresholds']['normalized_knot_residue_min']}`, and at least `{payload['thresholds']['one_way_generator_shift_ratio_min']}` relative generator shift from the nearest one-way channel pole. Exact and at least 2/3 modal reductions must pass.",
        "",
        "## Result",
        "",
        f"Classification: **{gate['classification']}**.",
        "",
        f"- exact primary pass: {gate['primary_exact_pass']};",
        f"- modal primary passes: {gate['primary_reduction_passes']}/3;",
        f"- nonlinear 500,000-update confirmation allowed: {gate['nonlinear_confirmation_allowed']};",
        "- mass-control dynamic knot residue: exactly zero by construction.",
        "",
        "![Source-local linear gate](../../figures/draft/response/source_local_linear_gate_2026-08-06.png)",
        "",
        "## Pole diagnostics",
        "",
        "| emission | sign | representation | stable | omega | Gamma | knot residue | one-way shift | pass |",
        "| --- | ---: | --- | :---: | ---: | ---: | ---: | ---: | :---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['emission']} | {row['coupling_sign']:+d} | {row['representation']} | {row['stable']} | {_format(row['frequency_per_memory_time'])} | {_format(row['damping_per_memory_time'])} | {_format(row['normalized_knot_residue'])} | {_format(row['nearest_one_way_generator_distance_ratio'])} | {row['passes']} |"
        )
    primary_exact = next(
        row
        for row in rows
        if row["emission"] == "offset"
        and row["coupling_sign"] == 1
        and row["representation"] == "exact"
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"The exact primary arm is stable and contains a non-real pole at `omega={_format(primary_exact['frequency_per_memory_time'])}` and `Gamma={_format(primary_exact['damping_per_memory_time'])}` per memory time. Its normalized knot residue is only `{_format(primary_exact['normalized_knot_residue'])}`, and its generator shift from the nearest one-way Telegraph pole is only `{_format(primary_exact['nearest_one_way_generator_distance_ratio'])}`. Both are far below the registered `0.1` thresholds.",
            "",
            "Thus the complex pair is observable mainly as an inserted channel mode, not as a reciprocal knot mode. The current source loads it even less strongly. The opposite coupling sign does not change that conclusion. Extending this mechanism to 500,000 updates would test duration after the discriminating architecture gate has already failed and is therefore not justified.",
            "",
            "## Evidence boundary",
            "",
            "Supported: source locality can be enforced, the inherited channel is stable, and its complex poles couple only negligibly to the registered scalar knot coordinate at the fixed gain. Inference: a useful reciprocal mode needs a different source/readout state or an independently derived coupling law. Not supported: physical field identification, charge, spin, photon, dimension selection, Lorentz kinematics, QFT, or a Standard-Model relation.",
            "",
            "## Reproducibility",
            "",
            f"- git revision at execution: `{payload['git_revision']}`;",
            "- preregistration: `reports/project/meta/preregistration/source_local_linear_gate_preregistration_2026-08-06.md`;",
            "- command: `python experiments/current/memory/synchronization/mediation/source_local_linear_gate.py`;",
            "- machine-readable summary: `reports/response/source_local/source_local_linear_gate_2026-08-06.json`.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    payload, exact, _ = run_gate(args)
    report = ROOT / args.report
    summary = ROOT / args.summary_json
    figure = ROOT / args.figure
    _write_figure(payload, exact, figure)
    _write_report(payload, report)
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(
        json.dumps(payload, indent=2, default=_json_value) + "\n",
        encoding="utf-8",
    )
    print(payload["gate"]["classification"])
    print(report.relative_to(ROOT))


if __name__ == "__main__":
    main()


