"""Audit vector-current coherence already encoded by ordered scalar history."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import subprocess
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from emergenz_knoten import (
    FiniteMemoryState,
    antisymmetric_current_coherence,
    antisymmetric_current_tensor,
    load_finite_memory_checkpoint,
    memory_centroid,
    memory_shape_tensor,
    oriented_history_from_state,
    vector_field_coherence,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
DEFAULT_CHECKPOINT_DIR = Path(
    "data/processed/reference_states/scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Test ordered scalar histories for a coherent vector current."
    )
    parser.add_argument("--checkpoint-dir", type=Path, default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--resolution-ratios", default="100,30,10,5,3,2.5")
    parser.add_argument("--modes", default="displacement,unit")
    parser.add_argument("--primary-ratio", type=float, default=2.5)
    parser.add_argument("--stability-ratio", type=float, default=5.0)
    parser.add_argument("--minimum-distinctness", type=float, default=1.25)
    parser.add_argument("--null-samples", type=int, default=2000)
    parser.add_argument("--null-quantile", type=float, default=0.99)
    parser.add_argument("--direction-cosine-min", type=float, default=0.9)
    parser.add_argument("--null-seed", type=int, default=20_260_721)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/oriented_history_current_audit_2026-07-21.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/response/oriented_history_current_audit_2026-07-21.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/oriented_history_current_audit_2026-07-21.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _rel_from(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _git_output(arguments: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return result.stdout.strip()


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        number = float(value)
        return number if np.isfinite(number) else None
    if isinstance(value, Path):
        return _rel(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def parse_resolution_ratios(text: str) -> list[float]:
    values = [float(part.strip()) for part in text.split(",") if part.strip()]
    if not values or any(not np.isfinite(value) or value <= 0.0 for value in values):
        raise ValueError("resolution ratios must be positive finite values")
    if len(values) != len(set(values)):
        raise ValueError("resolution ratios must not contain duplicates")
    return sorted(values, reverse=True)


def parse_modes(text: str) -> list[str]:
    modes = [part.strip() for part in text.split(",") if part.strip()]
    if not modes or any(mode not in ("displacement", "unit") for mode in modes):
        raise ValueError("modes must contain displacement and/or unit")
    if len(modes) != len(set(modes)):
        raise ValueError("modes must not contain duplicates")
    return modes


def evaluate_current_row(
    state: FiniteMemoryState,
    *,
    radius_ratio: float,
    mode: str,
    null_samples: int,
    null_quantile: float,
    random_seed: int,
    minimum_distinctness: float,
) -> dict[str, Any]:
    """Evaluate local current and an independent-sign conditional null."""

    if null_samples < 100:
        raise ValueError("null_samples must be at least 100")
    if not 0.5 < null_quantile < 1.0:
        raise ValueError("null_quantile must lie between 0.5 and 1")
    radius = float(np.sqrt(max(np.trace(memory_shape_tensor(state)), 0.0)))
    if radius <= 0.0:
        raise ValueError("memory radius must be positive")
    positions, currents, weights = oriented_history_from_state(state, mode=mode)
    positions = positions - memory_centroid(state)[None, :]
    sigma = radius_ratio * radius
    probe = np.zeros(state.dim)
    probe[0] = -sigma
    dx = probe[None, :] - positions
    kernel = np.exp(-0.5 * np.einsum("ij,ij->i", dx, dx) / (sigma * sigma))
    contributions = (weights * kernel)[:, None] * currents
    field = np.sum(contributions, axis=0)
    absolute_current = float(np.sum(np.linalg.norm(contributions, axis=1)))
    coherence = vector_field_coherence(
        probe,
        positions,
        currents,
        weights,
        sigma=sigma,
    )
    rng = np.random.default_rng(random_seed)
    signs = 2.0 * rng.integers(0, 2, size=(null_samples, len(weights))) - 1.0
    null_fields = signs @ contributions
    null_coherence = np.linalg.norm(null_fields, axis=1) / max(
        absolute_current, np.finfo(float).tiny
    )
    null_threshold = float(np.quantile(null_coherence, null_quantile))
    p_upper = float((1 + np.sum(null_coherence >= coherence)) / (null_samples + 1))

    local_weights = weights * kernel
    origin = np.zeros(state.dim)
    circulation_tensor = antisymmetric_current_tensor(
        positions,
        currents,
        local_weights,
        origin=origin,
    )
    circulation_coherence = antisymmetric_current_coherence(
        positions,
        currents,
        local_weights,
        origin=origin,
    )
    wedges = (
        positions[:, :, None] * currents[:, None, :]
        - currents[:, :, None] * positions[:, None, :]
    )
    circulation_contributions = local_weights[:, None, None] * wedges
    absolute_circulation = float(
        np.sum(np.linalg.norm(circulation_contributions, axis=(1, 2)))
    )
    null_circulation = np.linalg.norm(
        signs @ circulation_contributions.reshape(len(weights), -1),
        axis=1,
    ) / max(absolute_circulation, np.finfo(float).tiny)
    circulation_null_threshold = float(np.quantile(null_circulation, null_quantile))
    circulation_p_upper = float(
        (1 + np.sum(null_circulation >= circulation_coherence)) / (null_samples + 1)
    )
    circulation_norm = float(np.linalg.norm(circulation_tensor))
    circulation_direction = (
        circulation_tensor.reshape(-1) / circulation_norm
        if circulation_norm > 0.0
        else np.zeros(state.dim * state.dim)
    )

    field_norm = float(np.linalg.norm(field))
    direction = field / field_norm if field_norm > 0.0 else np.zeros(state.dim)
    distinctness = float(radius_ratio / 2.0)
    return {
        "dim": state.dim,
        "mode": mode,
        "radius": radius,
        "radius_ratio": float(radius_ratio),
        "separation_over_combined_radius": distinctness,
        "eligible_distinctness": bool(distinctness >= minimum_distinctness),
        "field": field,
        "field_direction": direction,
        "field_norm": field_norm,
        "absolute_current": absolute_current,
        "coherence": float(coherence),
        "null_median": float(np.median(null_coherence)),
        "null_q95": float(np.quantile(null_coherence, 0.95)),
        "null_threshold": null_threshold,
        "observed_to_null_threshold": float(
            coherence / max(null_threshold, np.finfo(float).tiny)
        ),
        "p_upper": p_upper,
        "exceeds_null": bool(coherence > null_threshold),
        "circulation_tensor": circulation_tensor,
        "circulation_direction": circulation_direction,
        "circulation_coherence": float(circulation_coherence),
        "circulation_null_threshold": circulation_null_threshold,
        "circulation_observed_to_null_threshold": float(
            circulation_coherence
            / max(circulation_null_threshold, np.finfo(float).tiny)
        ),
        "circulation_p_upper": circulation_p_upper,
        "circulation_exceeds_null": bool(
            circulation_coherence > circulation_null_threshold
        ),
        "mean_step_norm": float(
            np.average(np.linalg.norm(currents, axis=1), weights=weights)
        ),
    }


def run_current_ladder(
    checkpoint_dir: Path,
    *,
    resolution_ratios: Iterable[float],
    modes: Iterable[str],
    null_samples: int,
    null_quantile: float,
    null_seed: int,
    minimum_distinctness: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    paths = sorted(_resolve(checkpoint_dir).glob("*.npz"))
    if not paths:
        raise ValueError(f"no checkpoints found in {_resolve(checkpoint_dir)}")
    for path in paths:
        checkpoint = load_finite_memory_checkpoint(path)
        state = checkpoint.state
        radius = float(np.sqrt(np.trace(memory_shape_tensor(state))))
        ratios = [checkpoint.config.sigma_rep / radius, *resolution_ratios]
        unique_ratios: list[float] = []
        for ratio in ratios:
            if not any(np.isclose(ratio, existing) for existing in unique_ratios):
                unique_ratios.append(float(ratio))
        for mode_index, mode in enumerate(modes):
            for ratio in unique_ratios:
                print(
                    f"running d={state.dim}, mode={mode}, sigma/R={ratio:.6g}",
                    flush=True,
                )
                seed = (
                    null_seed
                    + 1_000_003 * state.dim
                    + 10_009 * mode_index
                    + int(round(1000.0 * ratio))
                )
                row = evaluate_current_row(
                    state,
                    radius_ratio=ratio,
                    mode=mode,
                    null_samples=null_samples,
                    null_quantile=null_quantile,
                    random_seed=seed,
                    minimum_distinctness=minimum_distinctness,
                )
                row.update(
                    {
                        "checkpoint": _rel(path),
                        "seed": checkpoint.formation_seed,
                        "update_index": checkpoint.update_index,
                        "formation_revision": checkpoint.git_revision,
                        "self_readout": bool(
                            np.isclose(ratio, checkpoint.config.sigma_rep / radius)
                        ),
                    }
                )
                rows.append(row)
    return rows


def summarize_gate(
    rows: list[dict[str, Any]],
    *,
    primary_ratio: float,
    stability_ratio: float,
    direction_cosine_min: float,
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    summaries = []
    for dim in sorted({int(row["dim"]) for row in rows}):
        displacement = [
            row for row in rows if row["dim"] == dim and row["mode"] == "displacement"
        ]
        primary = next(
            row
            for row in displacement
            if np.isclose(row["radius_ratio"], primary_ratio)
        )
        stability = next(
            row
            for row in displacement
            if np.isclose(row["radius_ratio"], stability_ratio)
        )
        polar_cosine = float(
            np.dot(primary["field_direction"], stability["field_direction"])
        )
        circulation_cosine = float(
            np.dot(
                primary["circulation_direction"],
                stability["circulation_direction"],
            )
        )
        polar_pass = bool(
            primary["eligible_distinctness"]
            and primary["exceeds_null"]
            and polar_cosine >= direction_cosine_min
        )
        circulation_pass = bool(
            primary["eligible_distinctness"]
            and primary["circulation_exceeds_null"]
            and circulation_cosine >= direction_cosine_min
        )
        summaries.append(
            {
                "dim": dim,
                "primary_ratio": primary_ratio,
                "polar_coherence": primary["coherence"],
                "polar_null_threshold": primary["null_threshold"],
                "polar_p_upper": primary["p_upper"],
                "polar_direction_cosine": polar_cosine,
                "polar_pass": polar_pass,
                "circulation_coherence": primary["circulation_coherence"],
                "circulation_null_threshold": primary["circulation_null_threshold"],
                "circulation_p_upper": primary["circulation_p_upper"],
                "circulation_direction_cosine": circulation_cosine,
                "circulation_pass": circulation_pass,
                "gate_pass": polar_pass or circulation_pass,
            }
        )
    polar_count = sum(summary["polar_pass"] for summary in summaries)
    circulation_count = sum(summary["circulation_pass"] for summary in summaries)
    if polar_count == len(summaries):
        decision = {
            "status": "pass",
            "selected_next_mechanism": "derived_history_current_cross_channel",
        }
    elif circulation_count == len(summaries):
        decision = {
            "status": "pass",
            "selected_next_mechanism": "derived_history_circulation_channel",
        }
    elif polar_count == 0 and circulation_count == 0:
        decision = {
            "status": "fail",
            "selected_next_mechanism": "independent_oriented_memory_state",
        }
    else:
        decision = {
            "status": "inconclusive",
            "selected_next_mechanism": "none_pending_independent_states",
        }
    return summaries, decision


def make_figure(rows: list[dict[str, Any]], path: Path, null_quantile: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    dims = sorted({int(row["dim"]) for row in rows})
    colors = {dim: color for dim, color in zip(dims, ("#1261a0", "#d1495b"))}
    styles = {"displacement": "-", "unit": ":"}
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.0), constrained_layout=True)
    for dim in dims:
        for mode in ("displacement", "unit"):
            selected = sorted(
                (row for row in rows if row["dim"] == dim and row["mode"] == mode),
                key=lambda row: row["radius_ratio"],
            )
            if not selected:
                continue
            x = np.asarray([row["radius_ratio"] for row in selected])
            polar_ratio = np.asarray(
                [row["observed_to_null_threshold"] for row in selected]
            )
            circulation_ratio = np.asarray(
                [row["circulation_observed_to_null_threshold"] for row in selected]
            )
            polar_p = np.asarray([row["p_upper"] for row in selected])
            circulation_p = np.asarray([row["circulation_p_upper"] for row in selected])
            label = f"d={dim}, {mode}"
            axes[0].plot(
                x,
                polar_ratio,
                color=colors[dim],
                linestyle=styles[mode],
                marker="o",
                label=label,
            )
            axes[1].plot(
                x,
                circulation_ratio,
                color=colors[dim],
                linestyle=styles[mode],
                marker="o",
                label=label,
            )
            axes[2].plot(
                x,
                polar_p,
                color=colors[dim],
                linestyle=styles[mode],
                marker="o",
                label=f"polar {label}",
            )
            axes[2].plot(
                x,
                circulation_p,
                color=colors[dim],
                linestyle="--",
                marker="x",
                alpha=0.7,
                label=f"bivector {label}",
            )
    axes[0].set_ylabel("Polar observed / sign-null threshold")
    axes[1].set_ylabel("Bivector observed / sign-null threshold")
    axes[2].set_ylabel("Upper-tail conditional p")
    axes[0].axhline(1.0, color="#555555", linestyle="--", linewidth=0.9)
    axes[1].axhline(1.0, color="#555555", linestyle="--", linewidth=0.9)
    axes[2].axhline(
        1.0 - null_quantile,
        color="#555555",
        linestyle="--",
        linewidth=0.9,
    )
    for axis in axes:
        axis.set_xscale("log")
        axis.set_yscale("log")
        axis.set_xlabel("Current read sigma / R_mem")
        axis.grid(alpha=0.25)
        axis.invert_xaxis()
        axis.legend(fontsize=6)
    fig.suptitle("Ordered scalar history: polar and bivector current null tests")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _fmt(value: float) -> str:
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3 or abs(value) >= 1e3:
        return f"{value:.3e}"
    return f"{value:.4f}"


def _safe_ratio(numerator: float, denominator: float) -> float:
    return float(numerator / max(denominator, np.finfo(float).tiny))


def build_report(payload: dict[str, Any], report_path: Path, figure_path: Path) -> str:
    lines = [
        "# Oriented history-current audit",
        "",
        f"Date: {payload['generated_utc']}",
        "",
        "## Question and null",
        "",
        "Do the ordered points of an existing scalar N=100M checkpoint already",
        "encode a coherent vector current? The displacement current uses adjacent",
        "retained-point differences; unit current is a sensitivity analysis.",
        "An antisymmetric position-current bivector tests circulation separately,",
        "so a closed ring is not rejected merely for zero polar net current.",
        "The conditional null independently flips every current sign while keeping",
        "positions, magnitudes, weights, kernel, and checkpoint fixed.",
        "",
        "This is a derived-observable audit, not a vector-memory interaction,",
        "oscillator, polarization, spin, photon, or particle test.",
        "",
        "## Decision",
        "",
        f"Gate status: **{payload['decision']['status']}**.",
        "",
        "Selected next mechanism: "
        f"**{payload['decision']['selected_next_mechanism']}**.",
        "",
        "The primary gate uses displacement current at sigma/R=2.5. Polar and",
        "bivector channels are evaluated separately; either must exceed sign-null",
        f"q={payload['null_quantile']:.2f} with direction cosine at least",
        f"{payload['direction_cosine_min']:.2f} against sigma/R={payload['stability_ratio']:g}",
        "in every audited embedding to select a derived channel.",
        "",
        "## Primary polar gate",
        "",
        "| d | coherence | null q | observed/null | p_upper | direction cosine | pass |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for summary in payload["case_summaries"]:
        lines.append(
            f"| {summary['dim']} | {_fmt(summary['polar_coherence'])} | "
            f"{_fmt(summary['polar_null_threshold'])} | "
            f"{_fmt(_safe_ratio(summary['polar_coherence'], summary['polar_null_threshold']))} | "
            f"{_fmt(summary['polar_p_upper'])} | "
            f"{_fmt(summary['polar_direction_cosine'])} | "
            f"{'pass' if summary['polar_pass'] else 'fail'} |"
        )
    lines.extend(
        [
            "",
            "## Primary bivector-circulation gate",
            "",
            "| d | coherence | null q | observed/null | p_upper | direction cosine | pass |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for summary in payload["case_summaries"]:
        lines.append(
            f"| {summary['dim']} | {_fmt(summary['circulation_coherence'])} | "
            f"{_fmt(summary['circulation_null_threshold'])} | "
            f"{_fmt(_safe_ratio(summary['circulation_coherence'], summary['circulation_null_threshold']))} | "
            f"{_fmt(summary['circulation_p_upper'])} | "
            f"{_fmt(summary['circulation_direction_cosine'])} | "
            f"{'pass' if summary['circulation_pass'] else 'fail'} |"
        )
    lines.extend(
        [
            "",
            "## Resolution ladder",
            "",
            "| d | mode | self | sigma/R | polar coh | polar/null | polar p | bivector coh | bivector/null | bivector p |",
            "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    ordered = sorted(
        payload["rows"],
        key=lambda row: (row["dim"], row["mode"], -row["radius_ratio"]),
    )
    for row in ordered:
        lines.append(
            f"| {row['dim']} | {row['mode']} | "
            f"{'yes' if row['self_readout'] else 'no'} | "
            f"{_fmt(row['radius_ratio'])} | {_fmt(row['coherence'])} | "
            f"{_fmt(row['observed_to_null_threshold'])} | "
            f"{_fmt(row['p_upper'])} | "
            f"{_fmt(row['circulation_coherence'])} | "
            f"{_fmt(row['circulation_observed_to_null_threshold'])} | "
            f"{_fmt(row['circulation_p_upper'])} |"
        )
    lines.extend(
        [
            "",
            "## Guardrails and next gate",
            "",
            "The sign randomizations are conditional replicates, not independent",
            "formation states. One checkpoint per embedding makes this pipeline",
            "evidence. Joint polar and bivector failure means the retained scalar",
            "history cannot simply be relabelled as a coherent oriented source under",
            "these observables; it does",
            "not prove that an independently evolving vector state is impossible.",
            "",
            "An independent vector-state gate must use at least six formations,",
            "common future noise, channel-off and sign-randomized deposits, a",
            "relational angular/transverse primary observable, source shape bounds,",
            "and a fixed stop rule. Complex AR eigenvalues are secondary only.",
            "",
            "## Figure",
            "",
            f"![History-current audit]({_rel_from(report_path, figure_path)})",
            "",
            "## Reproducibility",
            "",
            f"- Analysis revision: {payload['git_revision']}",
            f"- Summary: {_rel(payload['summary_json'])}",
            f"- Command: {' '.join(payload['command'])}",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    try:
        ratios = parse_resolution_ratios(args.resolution_ratios)
        modes = parse_modes(args.modes)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if not any(np.isclose(args.primary_ratio, ratio) for ratio in ratios):
        raise SystemExit("--resolution-ratios must contain --primary-ratio")
    if not any(np.isclose(args.stability_ratio, ratio) for ratio in ratios):
        raise SystemExit("--resolution-ratios must contain --stability-ratio")
    if "displacement" not in modes:
        raise SystemExit("--modes must contain displacement for the primary gate")
    if not 0.0 < args.direction_cosine_min <= 1.0:
        raise SystemExit("--direction-cosine-min must lie in (0, 1]")
    git_revision = _git_output(["rev-parse", "HEAD"])
    git_status = _git_output(["status", "--short"])
    if git_status and not args.allow_dirty:
        raise SystemExit("history-current audit requires a clean worktree")

    rows = run_current_ladder(
        args.checkpoint_dir,
        resolution_ratios=ratios,
        modes=modes,
        null_samples=args.null_samples,
        null_quantile=args.null_quantile,
        null_seed=args.null_seed,
        minimum_distinctness=args.minimum_distinctness,
    )
    summaries, decision = summarize_gate(
        rows,
        primary_ratio=args.primary_ratio,
        stability_ratio=args.stability_ratio,
        direction_cosine_min=args.direction_cosine_min,
    )
    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_path = _resolve(args.figure)
    make_figure(rows, figure_path, args.null_quantile)
    payload = {
        "schema": "emergenz-knoten.oriented-history-current-audit",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_revision": git_revision,
        "git_status_at_start": git_status,
        "command": ["python", *os.sys.argv],
        "checkpoint_dir": _rel(_resolve(args.checkpoint_dir)),
        "resolution_ratios": ratios,
        "modes": modes,
        "primary_ratio": float(args.primary_ratio),
        "stability_ratio": float(args.stability_ratio),
        "minimum_distinctness": float(args.minimum_distinctness),
        "null_samples": int(args.null_samples),
        "null_quantile": float(args.null_quantile),
        "direction_cosine_min": float(args.direction_cosine_min),
        "null_seed": int(args.null_seed),
        "rows": rows,
        "case_summaries": summaries,
        "decision": decision,
        "summary_json": summary_path,
        "figure": figure_path,
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        build_report(payload, report_path, figure_path),
        encoding="utf-8",
    )
    print(f"wrote {_rel(report_path)}", flush=True)


if __name__ == "__main__":
    main()
