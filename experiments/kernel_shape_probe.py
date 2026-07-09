from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
import html
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import SimulationConfig  # noqa: E402
from emergenz_knoten.kernels import double_gaussian_gradient, exponential_weights  # noqa: E402


@dataclass(frozen=True)
class ProbeCase:
    name: str
    sigma_rep: float
    sigma_att: float
    amplitude_rep: float
    amplitude_att: float
    eta: float = 0.15
    epsilon: float = 0.03


DEFAULT_CASES = [
    ProbeCase("baseline", 1.0, 3.0, 1.0, 0.35),
    ProbeCase("att_zero", 1.0, 3.0, 1.0, 0.0),
    ProbeCase("rep_zero", 1.0, 3.0, 0.0, 0.35),
    ProbeCase("strong_local", 1.0, 3.0, 4.0, 0.35),
    ProbeCase("wide_strong", 2.0, 6.0, 16.0, 1.4),
]


def _parse_int_list(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one integer")
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


def _horizon(config: SimulationConfig) -> int:
    return min(config.max_memory, max(1, int(config.memory_factor / config.alpha)))


def simulate_probe_numpy(config: SimulationConfig, *, seed: int) -> np.ndarray:
    """Run a small vectorized finite-memory simulation for visual probes."""

    rng = np.random.default_rng(seed)
    horizon = _horizon(config)
    weights = exponential_weights(config.alpha, horizon)
    memory = np.zeros((horizon, config.dim), dtype=float)
    x = np.zeros(config.dim, dtype=float)
    samples: list[np.ndarray] = []
    idx = 0
    filled = 0

    for step in range(1, config.steps + 1):
        if filled:
            order = (idx - 1 - np.arange(filled)) % horizon
            mem = memory[order]
            grad = double_gaussian_gradient(
                x,
                mem,
                weights[:filled],
                sigma_rep=config.sigma_rep,
                sigma_att=config.sigma_att,
                amplitude_rep=config.amplitude_rep,
                amplitude_att=config.amplitude_att,
            )
        else:
            grad = np.zeros(config.dim, dtype=float)
        x = x + config.epsilon * rng.normal(size=config.dim) - config.eta * grad
        memory[idx] = x
        idx = (idx + 1) % horizon
        filled = min(filled + 1, horizon)
        if step >= config.burn_in and step % config.sample_every == 0:
            samples.append(x.copy())
    return np.asarray(samples, dtype=float)


def _turn_cosine(samples: np.ndarray) -> dict[str, float | None]:
    if len(samples) < 3:
        return {"mean": None, "median": None}
    increments = np.diff(samples, axis=0)
    a = increments[:-1]
    b = increments[1:]
    denom = np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1)
    ok = denom > 0.0
    if not np.any(ok):
        return {"mean": None, "median": None}
    cos = np.einsum("ij,ij->i", a[ok], b[ok]) / denom[ok]
    return {"mean": float(np.mean(cos)), "median": float(np.median(cos))}


def _pca_projection(samples: np.ndarray) -> tuple[np.ndarray, list[float]]:
    centered = samples - samples.mean(axis=0, keepdims=True)
    if centered.shape[1] <= 3:
        coords = centered
        if centered.shape[1] < 3:
            coords = np.pad(centered, ((0, 0), (0, 3 - centered.shape[1])))
    else:
        _, _, vt = np.linalg.svd(centered, full_matrices=False)
        coords = centered @ vt[:3].T
    cov = centered.T @ centered / max(len(centered) - 1, 1)
    evals = np.linalg.eigvalsh(cov)[::-1]
    total = float(np.sum(evals))
    ratios = (evals[:3] / total).astype(float).tolist() if total > 0 else [0.0, 0.0, 0.0]
    return coords[:, :3], ratios


def _rolling_mean(coords: np.ndarray, window: int) -> np.ndarray:
    if window <= 1 or len(coords) < window:
        return coords
    kernel = np.ones(window, dtype=float) / float(window)
    cols = [np.convolve(coords[:, i], kernel, mode="valid") for i in range(coords.shape[1])]
    return np.column_stack(cols)


def _metrics(samples: np.ndarray, coords: np.ndarray) -> dict[str, object]:
    centered = samples - samples.mean(axis=0, keepdims=True)
    radii = np.linalg.norm(centered, axis=1)
    increments = np.linalg.norm(np.diff(samples, axis=0), axis=1)
    net_displacement = float(np.linalg.norm(samples[-1] - samples[0])) if len(samples) else 0.0
    path_length = float(np.sum(increments)) if increments.size else 0.0
    turn = _turn_cosine(samples)
    return {
        "n_samples": int(len(samples)),
        "mean_centered_radius": float(np.mean(radii)) if radii.size else None,
        "max_centered_radius": float(np.max(radii)) if radii.size else None,
        "median_sample_step": float(np.median(increments)) if increments.size else None,
        "path_length": path_length,
        "net_displacement": net_displacement,
        "path_to_chord": path_length / net_displacement if net_displacement > 0 else None,
        "turn_cosine_mean": turn["mean"],
        "turn_cosine_median": turn["median"],
        "plot_span": (coords.max(axis=0) - coords.min(axis=0)).astype(float).tolist(),
    }


def _project_isometric(coords: np.ndarray) -> np.ndarray:
    x = coords[:, 0]
    y = coords[:, 1]
    z = coords[:, 2]
    x2 = 0.8660254038 * (x - y)
    y2 = 0.5 * (x + y) - z
    return np.column_stack([x2, y2])


def _panel_frame(cases: list[dict[str, Any]], panel_w: float, panel_h: float) -> tuple[np.ndarray, float, float]:
    projected: list[np.ndarray] = []
    for case in cases:
        coords = np.asarray(case["projection"], dtype=float)
        projected.append(_project_isometric(coords))
    all_points = np.vstack(projected)
    mins = all_points.min(axis=0)
    maxs = all_points.max(axis=0)
    span = np.maximum(maxs - mins, 1e-12)
    scale = 0.72 * min(panel_w / span[0], panel_h / span[1])
    world_span = max(
        float(max(np.max(np.abs(np.asarray(case["projection"], dtype=float))) for case in cases)),
        1e-12,
    )
    return 0.5 * (mins + maxs), float(scale), world_span


def _scale_projected_points(points: np.ndarray, x0: float, y0: float, width: float, height: float, center: np.ndarray, scale: float) -> np.ndarray:
    centered = points - center[None, :]
    out = np.empty_like(points)
    out[:, 0] = x0 + 0.5 * width + centered[:, 0] * scale
    out[:, 1] = y0 + 0.5 * height + centered[:, 1] * scale
    return out


def _polyline(points: np.ndarray, *, decimals: int = 1) -> str:
    return " ".join(f"{x:.{decimals}f},{y:.{decimals}f}" for x, y in points)


def _fmt_metric(value: object, *, digits: int = 3) -> str:
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return "n/a"
    if not np.isfinite(number):
        return "n/a"
    if number == 0.0:
        return "0"
    if abs(number) < 1.0e-3 or abs(number) >= 1.0e4:
        return f"{number:.{digits}e}"
    return f"{number:.{digits}f}"


def _nice_axis_unit(world_span: float) -> float:
    raw = max(world_span / 4.0, 1e-9)
    exponent = math.floor(math.log10(raw))
    base = 10.0 ** exponent
    for multiplier in (1.0, 2.0, 5.0, 10.0):
        if raw <= multiplier * base:
            return multiplier * base
    return 10.0 * base


def _draw_axis_triad(x: float, y: float, unit: float, scale: float) -> list[str]:
    vectors = {
        "x": (0.8660254038 * unit * scale, 0.5 * unit * scale, "#dc2626"),
        "y": (-0.8660254038 * unit * scale, 0.5 * unit * scale, "#16a34a"),
        "z": (0.0, -1.0 * unit * scale, "#2563eb"),
    }
    parts = [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.3" fill="#0f172a"/>']
    for label, (dx, dy, color) in vectors.items():
        x2 = x + dx
        y2 = y + dy
        parts.extend(
            [
                f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.4"/>',
                f'<text x="{x2 + 4:.1f}" y="{y2 + 4:.1f}" font-family="Arial" font-size="10" fill="{color}">{label}</text>',
            ]
        )
    parts.append(f'<text x="{x - 28:.1f}" y="{y + 30:.1f}" font-family="Arial" font-size="10" fill="#475569">axis unit={unit:.3g}</text>')
    return parts


def _plot_trajectories_svg(
    cases: list[dict[str, Any]],
    figure_path: Path,
    *,
    title: str,
    rolling: int,
    scale_mode: str = "shared",
) -> None:
    panel_w = 430
    panel_h = 360
    margin = 40
    title_h = 58
    cols = 2
    rows = int(np.ceil(len(cases) / cols))
    width = panel_w * cols + margin * (cols + 1)
    height = (panel_h + title_h) * rows + margin * (rows + 1)
    colors = ["#2563eb", "#16a34a", "#dc2626", "#7c3aed", "#ea580c", "#0891b2", "#be123c"]
    if scale_mode not in {"shared", "per-panel"}:
        raise ValueError("scale_mode must be 'shared' or 'per-panel'")
    if scale_mode == "shared":
        global_center, global_scale, world_span = _panel_frame(cases, panel_w, panel_h)
        global_axis_unit = _nice_axis_unit(world_span)
        caption = "shared projected scale across panels; black=rolling mean, color=sampled path"
    else:
        global_center = np.zeros(2, dtype=float)
        global_scale = 1.0
        global_axis_unit = 1.0
        caption = "panel-specific projected scale; compare shapes, not absolute size"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        f'<text x="40" y="28" font-family="Arial" font-size="20" font-weight="700">{html.escape(title)}</text>',
        f'<text x="40" y="48" font-family="Arial" font-size="12" fill="#475569">{caption}</text>',
    ]
    for idx, case in enumerate(cases):
        row = idx // cols
        col = idx % cols
        x0 = margin + col * (panel_w + margin)
        y0 = margin + 24 + row * (panel_h + title_h + margin)
        coords = np.asarray(case["projection"], dtype=float)
        if scale_mode == "shared":
            frame_center = global_center
            frame_scale = global_scale
            axis_unit = global_axis_unit
        else:
            frame_center, frame_scale, panel_world_span = _panel_frame([case], panel_w, panel_h)
            axis_unit = _nice_axis_unit(panel_world_span)
        stride = max(1, int(np.ceil(len(coords) / 2800)))
        plot_coords = coords[::stride]
        projected = _project_isometric(plot_coords)
        scaled = _scale_projected_points(projected, x0, y0 + title_h, panel_w, panel_h, frame_center, frame_scale)
        smooth3 = _rolling_mean(plot_coords, rolling)
        smooth = _scale_projected_points(_project_isometric(smooth3), x0, y0 + title_h, panel_w, panel_h, frame_center, frame_scale)
        metrics = case["metrics"]
        spans = metrics["plot_span"]
        title_text = html.escape(case["name"])
        color = colors[idx % len(colors)]
        parts.extend(
            [
                f'<rect x="{x0}" y="{y0}" width="{panel_w}" height="{panel_h + title_h}" rx="6" fill="#ffffff" stroke="#cbd5e1"/>',
                f'<text x="{x0 + 14}" y="{y0 + 24}" font-family="Arial" font-size="16" font-weight="700" fill="#0f172a">{title_text}</text>',
                f'<text x="{x0 + 14}" y="{y0 + 43}" font-family="Arial" font-size="12" fill="#475569">R={_fmt_metric(metrics["mean_centered_radius"])}, step={_fmt_metric(metrics["median_sample_step"])}, turn={_fmt_metric(metrics["turn_cosine_mean"])}</text>',
                f'<text x="{x0 + 14}" y="{y0 + 58}" font-family="Arial" font-size="11" fill="#64748b">span xyz={spans[0]:.2f}, {spans[1]:.2f}, {spans[2]:.2f}</text>',
                f'<line x1="{x0 + 18}" y1="{y0 + title_h + panel_h * 0.5:.1f}" x2="{x0 + panel_w - 18}" y2="{y0 + title_h + panel_h * 0.5:.1f}" stroke="#e2e8f0" stroke-width="1"/>',
                f'<line x1="{x0 + panel_w * 0.5:.1f}" y1="{y0 + title_h + 18}" x2="{x0 + panel_w * 0.5:.1f}" y2="{y0 + title_h + panel_h - 18}" stroke="#e2e8f0" stroke-width="1"/>',
                f'<polyline points="{_polyline(scaled)}" fill="none" stroke="{color}" stroke-width="0.7" stroke-opacity="0.45"/>',
                f'<polyline points="{_polyline(smooth)}" fill="none" stroke="#020617" stroke-width="1.6" stroke-opacity="0.95"/>',
            ]
        )
        parts.extend(_draw_axis_triad(x0 + 55, y0 + title_h + panel_h - 54, axis_unit, frame_scale))
    parts.append("</svg>")
    figure_path.parent.mkdir(parents=True, exist_ok=True)
    figure_path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def _case_config(base: SimulationConfig, case: ProbeCase) -> SimulationConfig:
    return replace(
        base,
        epsilon=case.epsilon,
        eta=case.eta,
        sigma_rep=case.sigma_rep,
        sigma_att=case.sigma_att,
        amplitude_rep=case.amplitude_rep,
        amplitude_att=case.amplitude_att,
    )


def _local_scales(config: SimulationConfig) -> dict[str, float]:
    """Return local drift scales after the corrected potential-gradient sign."""

    rep_scale = config.eta * config.amplitude_rep / (config.sigma_rep * config.sigma_rep)
    att_scale = config.eta * config.amplitude_att / (config.sigma_att * config.sigma_att)
    return {
        "repulsive_scale": float(rep_scale),
        "attractive_scale": float(att_scale),
        "net_repulsive_scale": float(rep_scale - att_scale),
    }


def _entry_from_samples(name: str, config: SimulationConfig, samples: np.ndarray) -> dict[str, Any]:
    if len(samples) < 3:
        raise RuntimeError("not enough samples; decrease --sample-every or --burn-in")
    projection, pca_energy = _pca_projection(samples)
    return {
        "name": name,
        "config": asdict(config),
        "metrics": _metrics(samples, projection),
        "local_scales": _local_scales(config),
        "pca_energy": pca_energy,
        "projection": projection.astype(float).tolist(),
    }


def _results_table(cases: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| case | sigma_rep | sigma_att | A_rep | A_att | k_rep-eff | mean radius | median step | turn mean | path/chord | PCA energy first 3 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for case in cases:
        metrics = case["metrics"]
        pca = ", ".join(f"{value:.2f}" for value in case["pca_energy"])
        lines.append(
            f"| `{case['name']}` | `{case['config']['sigma_rep']:.3g}` | "
            f"`{case['config']['sigma_att']:.3g}` | `{case['config']['amplitude_rep']:.3g}` | "
            f"`{case['config']['amplitude_att']:.3g}` | "
            f"`{case['local_scales']['net_repulsive_scale']:.4f}` | "
            f"`{metrics['mean_centered_radius']:.3f}` | "
            f"`{metrics['median_sample_step']:.4f}` | "
            f"`{metrics['turn_cosine_mean']:.3f}` | "
            f"`{metrics['path_to_chord']:.1f}` | `{pca}` |"
        )
    return lines


def _seed_table(cases: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| seed | mean radius | median step | turn mean | path/chord | span xyz |",
        "| ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for case in cases:
        metrics = case["metrics"]
        spans = ", ".join(f"{value:.2f}" for value in metrics["plot_span"])
        seed = case.get("seed", case["name"].replace("seed_", ""))
        lines.append(
            f"| `{seed}` | `{metrics['mean_centered_radius']:.3f}` | "
            f"`{metrics['median_sample_step']:.4f}` | `{metrics['turn_cosine_mean']:.3f}` | "
            f"`{metrics['path_to_chord']:.1f}` | `{spans}` |"
        )
    return lines


def build_report(payload: dict[str, Any]) -> str:
    lines = [
        "# Kernel Shape Probe",
        "",
        f"Date: {payload['finished_utc']}.",
        "",
        "## Scope",
        "",
        "This is a targeted visual probe for smoother or rounder 3D trajectories.",
        "It varies only kernel widths/amplitudes across a few motivated cases.",
        "It also compares baseline seeds to test whether the visible course is seed-specific.",
        "It is not a broad parameter sweep and not Paper-I evidence by itself.",
        "",
        "Important sign convention: the package now treats `double_gaussian_gradient`",
        "as the potential gradient of `A_rep G_rep - A_att G_att`.",
        "With `x <- x - eta grad`, `A_rep` is locally repulsive and",
        "the broad `A_att` component is attractive at its active scale.",
        "",
        "The kernel does not impose a hard minimum step length; without inertia",
        "or correlated noise the path can remain jagged even when it is",
        "spatially confined.",
        "",
        "## Figures",
        "",
        f"![Kernel shape probe]({payload['figure_path']})",
        "",
        f"![Kernel shape probe flexible]({payload['flexible_figure_path']})",
        "",
        f"![Kernel seed comparison]({payload['seed_figure_path']})",
        "",
        f"![Kernel seed comparison flexible]({payload['flexible_seed_figure_path']})",
        "",
        "The standard SVGs use a shared projected scale within the figure. The",
        "flexible SVGs use panel-specific scales and should be read for shape rather",
        "than absolute size. The black line is a rolling mean of the same trajectory;",
        "the colored line is the raw sampled path. Axis triads show the coordinate",
        "unit used in each projection.",
        "",
        "## Kernel Cases",
        "",
    ]
    lines.extend(_results_table(payload["cases"]))
    lines.extend(
        [
            "",
            "## Seed Comparison",
            "",
        ]
    )
    lines.extend(_seed_table(payload["seed_cases"]))
    lines.extend(
        [
            "",
            "## Reading",
            "",
            "- In the corrected convention, `A_att=0` is repulsion-only and should",
            "  be treated as a dispersive control rather than a knot-positive case.",
            "- `A_rep=0` is attraction-only and can collapse or confine depending on",
            "  noise, memory scale, and amplitude.",
            "- Increasing the local repulsive scale changes core exclusion, but it",
            "  does not automatically create directionally persistent, round paths.",
            "- Co-scaling amplitudes with kernel width can leave the local",
            "  stiffness scale A/sigma^2 almost unchanged in compact regimes.",
            "- Truly round trajectories in the visible path likely need an added",
            "  persistence mechanism: correlated noise, a velocity/inertial variable,",
            "  rotational/tangential drift, or a smoother center-of-knot observable.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a targeted kernel-shape probe and SVG 3D projection plot."
    )
    parser.add_argument("--steps", type=int, default=80_000)
    parser.add_argument("--burn-in", type=int, default=8_000)
    parser.add_argument("--sample-every", type=int, default=10)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--compare-seeds", type=_parse_int_list, default=[1, 2, 3, 4, 5])
    parser.add_argument("--dim", type=int, default=3)
    parser.add_argument("--epsilon", type=float, default=0.03)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--memory-factor", type=float, default=6.0)
    parser.add_argument("--max-memory", type=int, default=800)
    parser.add_argument("--rolling", type=int, default=25)
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("data/processed/kernel_shape_probe/2026-07-01_seed1/summary.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path("figures/draft/kernel_shape_probe_2026-07-01.svg"),
    )
    parser.add_argument(
        "--seed-figure",
        type=Path,
        default=Path("figures/draft/kernel_seed_probe_2026-07-02.svg"),
    )
    parser.add_argument(
        "--flexible-figure",
        type=Path,
        default=Path("figures/draft/kernel_shape_probe_flexible_2026-07-02.svg"),
    )
    parser.add_argument(
        "--flexible-seed-figure",
        type=Path,
        default=Path("figures/draft/kernel_seed_probe_flexible_2026-07-02.svg"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/kernel_shape_probe_2026-07-01.md"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.steps < 1:
        raise SystemExit("--steps must be positive")
    if args.burn_in < 0 or args.burn_in >= args.steps:
        raise SystemExit("--burn-in must satisfy 0 <= burn_in < steps")
    if args.sample_every < 1:
        raise SystemExit("--sample-every must be positive")
    base = SimulationConfig(
        steps=args.steps,
        dim=args.dim,
        epsilon=args.epsilon,
        eta=args.eta,
        alpha=args.alpha,
        memory_factor=args.memory_factor,
        max_memory=args.max_memory,
        burn_in=args.burn_in,
        sample_every=args.sample_every,
    )

    out_cases = []
    started = _utc_now()
    total_start = time.perf_counter()
    for case in DEFAULT_CASES:
        config = _case_config(base, case)
        print(f"running case={case.name}", flush=True)
        samples = simulate_probe_numpy(config, seed=args.seed)
        out_cases.append(_entry_from_samples(case.name, config, samples))

    seed_cases = []
    baseline = DEFAULT_CASES[0]
    baseline_config = _case_config(base, baseline)
    for seed in args.compare_seeds:
        print(f"running seed comparison seed={seed}", flush=True)
        samples = simulate_probe_numpy(baseline_config, seed=seed)
        entry = _entry_from_samples(f"seed_{seed}", baseline_config, samples)
        entry["seed"] = int(seed)
        seed_cases.append(entry)

    figure = args.figure if args.figure.is_absolute() else ROOT / args.figure
    seed_figure = args.seed_figure if args.seed_figure.is_absolute() else ROOT / args.seed_figure
    flexible_figure = args.flexible_figure if args.flexible_figure.is_absolute() else ROOT / args.flexible_figure
    flexible_seed_figure = args.flexible_seed_figure if args.flexible_seed_figure.is_absolute() else ROOT / args.flexible_seed_figure
    output_json = args.output_json if args.output_json.is_absolute() else ROOT / args.output_json
    report = args.report if args.report.is_absolute() else ROOT / args.report
    _plot_trajectories_svg(
        out_cases,
        figure,
        title="Kernel Shape Probe: shared-scale isometric 3D leading-coordinate projections",
        rolling=args.rolling,
        scale_mode="shared",
    )
    _plot_trajectories_svg(
        out_cases,
        flexible_figure,
        title="Kernel Shape Probe: flexible-scale isometric 3D leading-coordinate projections",
        rolling=args.rolling,
        scale_mode="per-panel",
    )
    _plot_trajectories_svg(
        seed_cases,
        seed_figure,
        title="Baseline Seed Comparison: shared-scale isometric 3D leading-coordinate projections",
        rolling=args.rolling,
        scale_mode="shared",
    )
    _plot_trajectories_svg(
        seed_cases,
        flexible_seed_figure,
        title="Baseline Seed Comparison: flexible-scale isometric 3D leading-coordinate projections",
        rolling=args.rolling,
        scale_mode="per-panel",
    )
    payload: dict[str, Any] = {
        "description": "Targeted kernel shape and seed probe for 3D leading-coordinate trajectories.",
        "started_utc": started,
        "finished_utc": _utc_now(),
        "elapsed_seconds": float(time.perf_counter() - total_start),
        "git_revision": _git_output(["rev-parse", "--short", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "seed": int(args.seed),
        "compare_seeds": [int(seed) for seed in args.compare_seeds],
        "base_config": asdict(base),
        "figure_path": Path(os.path.relpath(figure, report.parent)).as_posix(),
        "flexible_figure_path": Path(os.path.relpath(flexible_figure, report.parent)).as_posix(),
        "seed_figure_path": Path(os.path.relpath(seed_figure, report.parent)).as_posix(),
        "flexible_seed_figure_path": Path(os.path.relpath(flexible_seed_figure, report.parent)).as_posix(),
        "cases": out_cases,
        "seed_cases": seed_cases,
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    report.write_text(build_report(payload), encoding="utf-8")
    print(f"wrote {output_json}", flush=True)
    print(f"wrote {figure}", flush=True)
    print(f"wrote {flexible_figure}", flush=True)
    print(f"wrote {seed_figure}", flush=True)
    print(f"wrote {flexible_seed_figure}", flush=True)
    print(f"wrote {report}", flush=True)


if __name__ == "__main__":
    main()
