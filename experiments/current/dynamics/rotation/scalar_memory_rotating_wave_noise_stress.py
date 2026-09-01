"""Execute the frozen N0 resolved-noise rotating-wave stress ladder."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import UTC, datetime
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import time
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from experiments.current.dynamics.rotation import (
    scalar_memory_loop_p4r_phase_metrology_gate as p4r,
)
from experiments.current.dynamics.rotation import (
    scalar_memory_loop_p4rs_anchor_scale_gate as p4rs,
)
from emergenz_knoten.rotating_wave_formation import target_history
from emergenz_knoten.rotating_wave_noise import (
    brownian_refinement_paths,
    dimensionless_noise_amplitude,
    grid_cell_decision,
    injection_resolution,
    ladder_decision,
    noisy_native_fifo_step,
    resolved_arm_pass,
    visible_orbit_observables,
)
from emergenz_knoten.rotating_wave_stability import (
    native_fifo_step,
    rotation_translation_quotient_distance,
    translation_reduced_norm,
)
from emergenz_knoten.rotating_wave_stability_gate import (
    RotatingWaveCandidate,
    registered_perturbations,
)


ROOT = p4r.ROOT
PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_noise_stress_protocol_2026-08-31.md"
)
DESIGN_AUDIT = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_noise_stress_design_audit_2026-08-31.md"
)
READINESS_REVIEW = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_noise_stress_implementation_readiness_2026-09-01.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_noise_stress_2026-08-31.json"
)
DEFAULT_REPORT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_noise_stress_2026-08-31.md"
)
DEFAULT_FIGURE = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_noise_stress_2026-08-31.png"
)

DESIGN_FREEZE_REVISION = "6b17f9562baed07f842e1cb9f3a565652371f5d4"
PROTOCOL_FREEZE_REVISION = "67d6dfcba73f4422c228cdf393fc65bf9564e532"
EXPECTED_FROZEN_BLOBS = {
    PROTOCOL.as_posix(): "0b380f94a7e2d7b871911d2159cf2b48ec37fd30",
    DESIGN_AUDIT.as_posix(): "f947f428dff1069603bad7053826b438c2bb66cc",
    "src/emergenz_knoten/rotating_wave_noise.py": (
        "531a6911261797a7e2a924f5f1f58a4d8002448d"
    ),
    "src/emergenz_knoten/rotating_wave_stability.py": (
        "9defb5a6876371202e1ba57cea030c997b9c6edd"
    ),
    "src/emergenz_knoten/rotating_wave_stability_gate.py": (
        "630beb9952abefea823d91388dcbb2de8f1a2927"
    ),
    "src/emergenz_knoten/rotating_wave_formation.py": (
        "38f16f11a790a64470bab3a34505825cf815e7f0"
    ),
}

CHI_GRID = (0.0,) + tuple(10.0**exponent for exponent in range(-22, -1))
SEEDS = (2026083101, 2026083102, 2026083103)
POSITIVE_DISPLAY_FLOOR = 1.0e-18
CANDIDATES = (
    ("Anchor", p4rs.CANDIDATE, p4rs.RADIUS_DECIMAL, p4rs.THETA_DECIMAL, 2000, 5),
    ("L3", p4r.CANDIDATE, p4r.RADIUS_DECIMAL, p4r.THETA_DECIMAL, 4000, 10),
)


def _git(arguments: list[str]) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _is_ancestor(ancestor: str, revision: str) -> bool:
    return (
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, revision],
            cwd=ROOT,
            check=False,
            capture_output=True,
        ).returncode
        == 0
    )


def _verify_provenance() -> dict[str, Any]:
    status = _git(["status", "--short"])
    if status:
        raise RuntimeError("registered N0 execution requires a clean worktree")
    for output in (DEFAULT_SUMMARY, DEFAULT_REPORT, DEFAULT_FIGURE):
        if (ROOT / output).exists() or (ROOT / (output.as_posix() + ".tmp")).exists():
            raise RuntimeError(f"registered N0 output already exists: {output}")
    revision = _git(["rev-parse", "HEAD"])
    if not _is_ancestor(DESIGN_FREEZE_REVISION, revision):
        raise RuntimeError("design freeze is not in execution history")
    if not _is_ancestor(PROTOCOL_FREEZE_REVISION, revision):
        raise RuntimeError("clarified protocol freeze is not in execution history")
    for path, expected in EXPECTED_FROZEN_BLOBS.items():
        actual = _git(["rev-parse", f"HEAD:{path}"])
        if actual != expected:
            raise RuntimeError(f"frozen dependency changed: {path}")
    review_commit = _git(["log", "-1", "--format=%H", "--", str(READINESS_REVIEW)])
    if not review_commit or not _is_ancestor(review_commit, revision):
        raise RuntimeError("committed readiness review is required")
    upstream = _git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    ahead, behind = _git(
        ["rev-list", "--left-right", "--count", f"{upstream}...HEAD"]
    ).split()
    if (ahead, behind) != ("0", "0"):
        raise RuntimeError("execution revision must be fully pushed")
    return {
        "revision": revision,
        "branch": _git(["branch", "--show-current"]),
        "upstream": upstream,
        "readiness_review_commit": review_commit,
        "frozen_blobs": EXPECTED_FROZEN_BLOBS,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "timestamp_utc": datetime.now(UTC).isoformat(),
    }


def _sample_metrics(
    base: np.ndarray,
    pair: np.ndarray,
    reference: np.ndarray,
    candidate: RotatingWaveCandidate,
    reference_norm: float,
    target_visible_radius: float,
) -> dict[str, Any]:
    base_metrics = _sample_base_metrics(
        base,
        reference,
        candidate,
        reference_norm,
        target_visible_radius,
    )
    pair_d0, _ = rotation_translation_quotient_distance(
        pair,
        base,
        alpha=candidate.alpha,
        memory_mass=candidate.memory_mass,
    )
    return {**base_metrics, "pair_d0": pair_d0}


def _sample_base_metrics(
    base: np.ndarray,
    reference: np.ndarray,
    candidate: RotatingWaveCandidate,
    reference_norm: float,
    target_visible_radius: float,
) -> dict[str, Any]:
    base_d0, _ = rotation_translation_quotient_distance(
        base,
        reference,
        alpha=candidate.alpha,
        memory_mass=candidate.memory_mass,
    )
    visible = visible_orbit_observables(
        base,
        alpha=candidate.alpha,
        memory_mass=candidate.memory_mass,
        target_theta=candidate.theta,
    )
    return {
        "d0": base_d0,
        "d0_fraction": base_d0 / reference_norm,
        "d0_over_radius": base_d0 / candidate.radius,
        "radius_relative_error": abs(
            float(visible["visible_radius"]) - target_visible_radius
        )
        / target_visible_radius,
        "phase_error": float(visible["wrapped_phase_error"]),
        "positive_chirality": bool(visible["positive_chirality"]),
        "newest": [float(base[0, 0]), float(base[0, 1])],
    }


def run_candidate_cell(
    *,
    candidate: RotatingWaveCandidate,
    chi: float,
    noise: np.ndarray,
    seed: int,
    steps: int,
    sample_every: int,
) -> dict[str, Any]:
    """Run one candidate/chi/seed cell; useful with small synthetic candidates."""

    if noise.shape != (steps, 2):
        raise ValueError("noise shape does not match the registered step count")
    reference = target_history(candidate, chirality=1)
    perturbation = registered_perturbations(
        reference, scale=1.0e-7 * candidate.radius
    )["full_history_transverse_plus"]
    base = reference.copy()
    pair = reference + perturbation
    reference_norm = translation_reduced_norm(
        reference,
        alpha=candidate.alpha,
        memory_mass=candidate.memory_mass,
    )
    target_visible_radius = float(
        visible_orbit_observables(
            reference,
            alpha=candidate.alpha,
            memory_mass=candidate.memory_mass,
            target_theta=candidate.theta,
        )["visible_radius"]
    )
    epsilon = dimensionless_noise_amplitude(
        chi=chi, radius=candidate.radius, alpha=candidate.alpha
    )
    initial = _sample_metrics(
        base, pair, reference, candidate, reference_norm, target_visible_radius
    )
    initial_pair = float(initial["pair_d0"])
    trace = [{"step": 0, "tau": 0.0, **initial}]
    intended = {"base": [], "pair": []}
    effective = {"base": [], "pair": []}
    bitwise_native = True
    active = {"base": True, "pair": True}
    finite = {"base": True, "pair": True}
    final_step = {"base": 0, "pair": 0}
    stop_reason = {"base": "completed", "pair": "completed"}
    start = time.perf_counter()
    for step in range(1, steps + 1):
        for arm in ("base", "pair"):
            if not active[arm]:
                continue
            old = base if arm == "base" else pair
            result = noisy_native_fifo_step(
                old,
                epsilon=epsilon,
                noise=noise[step - 1],
                **candidate.step_parameters(),
            )
            if chi == 0.0:
                bitwise_native = bool(
                    bitwise_native
                    and np.array_equal(
                        result.history,
                        native_fifo_step(old, **candidate.step_parameters()),
                    )
                )
            if arm == "base":
                base = result.history
            else:
                pair = result.history
            intended[arm].append(result.intended_increment)
            effective[arm].append(result.effective_increment)
            final_step[arm] = step
            finite[arm] = bool(np.isfinite(result.history).all())
            if not finite[arm]:
                active[arm] = False
                stop_reason[arm] = "non-finite-state"
        if step % sample_every == 0:
            sampled: dict[str, Any] = {
                "step": step,
                "tau": candidate.alpha * step,
                "pair_d0": None,
            }
            base_crossed = False
            if active["base"]:
                sampled.update(
                    _sample_base_metrics(
                        base,
                        reference,
                        candidate,
                        reference_norm,
                        target_visible_radius,
                    )
                )
                if float(sampled["d0_fraction"]) >= 0.25:
                    base_crossed = True
            if active["pair"] and active["base"]:
                pair_d0, _ = rotation_translation_quotient_distance(
                    pair,
                    base,
                    alpha=candidate.alpha,
                    memory_mass=candidate.memory_mass,
                )
                sampled["pair_d0"] = pair_d0
                if pair_d0 / reference_norm >= 0.25:
                    active["pair"] = False
                    stop_reason["pair"] = "quotient-stop-threshold"
            if base_crossed:
                active["base"] = False
                stop_reason["base"] = "quotient-stop-threshold"
            trace.append(sampled)
        if not any(active.values()):
            break
    intended_arrays = {
        arm: np.asarray(values, dtype=float) for arm, values in intended.items()
    }
    effective_arrays = {
        arm: np.asarray(values, dtype=float) for arm, values in effective.items()
    }
    resolutions = {
        arm: injection_resolution(intended_arrays[arm], effective_arrays[arm])
        for arm in ("base", "pair")
    }
    base_trace = [row for row in trace if "d0_fraction" in row]
    pair_trace = [row for row in trace if row.get("pair_d0") is not None]
    d0_fractions = np.asarray(
        [row["d0_fraction"] for row in base_trace], dtype=float
    )
    radius_errors = np.asarray(
        [row["radius_relative_error"] for row in base_trace], dtype=float
    )
    pair_distances = np.asarray(
        [row["pair_d0"] for row in pair_trace], dtype=float
    )
    late = [
        row
        for row in base_trace
        if 15.0 <= float(row["tau"]) <= 20.0
    ]
    late_d0 = np.asarray([row["d0_fraction"] for row in late], dtype=float)
    late_phase = np.asarray([row["phase_error"] for row in late], dtype=float)
    metrics: dict[str, float | bool] = {
        "completed": all(final_step[arm] == steps for arm in ("base", "pair"))
        and all(stop_reason[arm] == "completed" for arm in ("base", "pair")),
        "finite": all(finite.values()),
        "maximum_d0_fraction": float(np.max(d0_fractions)),
        "late_rms_d0_fraction": (
            float(np.sqrt(np.mean(late_d0 * late_d0))) if late_d0.size else math.inf
        ),
        "maximum_radius_relative_error": float(np.max(radius_errors)),
        "late_rms_phase_error_over_theta": (
            float(np.sqrt(np.mean(late_phase * late_phase))) / candidate.theta
            if late_phase.size
            else math.inf
        ),
        "positive_chirality_fraction": float(
            np.mean([bool(row["positive_chirality"]) for row in base_trace])
        ),
        "maximum_pair_growth": float(np.max(pair_distances) / initial_pair),
        "final_pair_ratio": float(pair_distances[-1] / initial_pair),
        "stopped": any(reason != "completed" for reason in stop_reason.values()),
    }
    dynamic_pass = resolved_arm_pass(metrics)
    return {
        "candidate_id": candidate.candidate_id,
        "chi": chi,
        "epsilon": epsilon,
        "D_over_R_squared": chi * chi / 2.0,
        "seed": seed,
        "steps_expected": steps,
        "steps_completed": min(final_step.values()),
        "arm_steps_completed": final_step,
        "sample_every": sample_every,
        "reference_d0_norm": reference_norm,
        "target_visible_radius": target_visible_radius,
        "initial_pair_d0": initial_pair,
        "bitwise_native_zero": bitwise_native,
        "stopped": any(reason != "completed" for reason in stop_reason.values()),
        "stop_reason": stop_reason,
        "resolutions": resolutions,
        "metrics": metrics,
        "dynamic_pass": dynamic_pass,
        "trace": trace,
        "runtime_seconds": time.perf_counter() - start,
    }


def _cell_status(result: dict[str, Any]) -> str:
    rows = [
        (result["resolutions"][arm]["classification"], result["dynamic_pass"])
        for arm in ("base", "pair")
    ]
    return grid_cell_decision(rows)


def _scaling_fit(results: list[dict[str, Any]], candidate_id: str) -> dict[str, Any]:
    stable = [
        row
        for row in results
        if row["candidate_id"] == candidate_id
        and row["chi"] > 0.0
        and _cell_status(row) == "all-cell-stable"
    ]
    grouped: dict[float, list[dict[str, Any]]] = {}
    for row in stable:
        grouped.setdefault(float(row["chi"]), []).append(row)
    chosen: list[tuple[float, list[dict[str, Any]]]] = []
    nonzero_grid = CHI_GRID[1:]
    for start in range(len(nonzero_grid) - 3):
        window = nonzero_grid[start : start + 4]
        if all(value in grouped and len(grouped[value]) == len(SEEDS) for value in window):
            chosen = [(value, grouped[value]) for value in window]
            break
    if not chosen:
        return {
            "available": False,
            "compatible": False,
            "reason": "no-four-consecutive-stable-resolved-cells",
        }
    x_values: list[float] = []
    y_values: list[float] = []
    for _, rows in chosen:
        x_seed = [
            float(row["resolutions"]["base"]["effective_rms"])
            / next(c.radius for _, c, *_ in CANDIDATES if c.candidate_id == candidate_id)
            for row in rows
        ]
        y_seed = [float(row["metrics"]["late_rms_d0_fraction"]) for row in rows]
        x_values.append(float(np.exp(np.mean(np.log(x_seed)))))
        y_values.append(float(np.exp(np.mean(np.log(y_seed)))))
    slope, intercept = np.polyfit(np.log(x_values), np.log(y_values), 1)
    return {
        "available": True,
        "slope": float(slope),
        "intercept": float(intercept),
        "compatible": bool(0.75 <= slope <= 1.25),
        "chi_values": [chi for chi, _ in chosen],
    }


def run_gate() -> dict[str, Any]:
    provenance = _verify_provenance()
    paths = {seed: brownian_refinement_paths(seed) for seed in SEEDS}
    results: list[dict[str, Any]] = []
    start = time.perf_counter()
    for name, candidate, radius_decimal, theta_decimal, steps, sample_every in CANDIDATES:
        for chi in CHI_GRID:
            for seed in SEEDS:
                fine, coarse = paths[seed]
                noise = coarse if name == "Anchor" else fine
                row = run_candidate_cell(
                    candidate=candidate,
                    chi=chi,
                    noise=noise,
                    seed=seed,
                    steps=steps,
                    sample_every=sample_every,
                )
                row["candidate_name"] = name
                row["radius_decimal"] = radius_decimal
                row["theta_decimal"] = theta_decimal
                results.append(row)
    zero_pass = all(
        row["bitwise_native_zero"]
        and row["dynamic_pass"]
        and float(row["metrics"]["maximum_d0_fraction"]) <= 1.0e-10
        for row in results
        if row["chi"] == 0.0
    )
    grid: list[dict[str, Any]] = []
    for chi in CHI_GRID[1:]:
        rows = [row for row in results if row["chi"] == chi]
        arm_rows = [
            (row["resolutions"][arm]["classification"], row["dynamic_pass"])
            for row in rows
            for arm in ("base", "pair")
        ]
        grid.append(
            {"chi": chi, "decision": grid_cell_decision(arm_rows), "arm_count": len(arm_rows)}
        )
    decision = ladder_decision(row["decision"] for row in grid)
    if not zero_pass:
        decision = "n0-inconclusive"
    scaling = {
        name: _scaling_fit(results, candidate.candidate_id)
        for name, candidate, *_ in CANDIDATES
    }
    return {
        "schema": "scalar-memory-rotating-wave-noise-stress-v1",
        "decision": decision,
        "zero_control_pass": zero_pass,
        "cross_scale_interpretation": (
            "compatible"
            if all(row["available"] and row["compatible"] for row in scaling.values())
            else "inconclusive"
        ),
        "provenance": provenance,
        "registration": {
            "chi_grid": CHI_GRID,
            "seeds": SEEDS,
            "candidate_order": [name for name, *_ in CANDIDATES],
            "candidate_parameters": [asdict(candidate) for _, candidate, *_ in CANDIDATES],
            "brownian_refinement": "anchor[k]=(fine[2k]+fine[2k+1])/sqrt(2)",
        },
        "grid": grid,
        "scaling": scaling,
        "figure": {
            "positive_log_floor": POSITIVE_DISPLAY_FLOOR,
            "zero_marker": "downward-open-triangle-at-display-floor",
            "decision_uses_display_floor": False,
        },
        "results": results,
        "runtime_seconds": time.perf_counter() - start,
        "claim_boundary": (
            "Finite-time numerical orbital robustness only; no physical noise calibration, "
            "stationary formation, interaction, spin, inertia or mass."
        ),
    }


def _median_by_candidate_chi(
    payload: dict[str, Any], key: str
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    output: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for name, *_ in CANDIDATES:
        points = []
        for chi in CHI_GRID[1:]:
            rows = [
                row
                for row in payload["results"]
                if row["candidate_name"] == name and row["chi"] == chi
            ]
            values = []
            for row in rows:
                value: Any = row
                for part in key.split("."):
                    value = value[part]
                values.append(float(value))
            points.append(float(np.median(values)))
        output[name] = (np.asarray(CHI_GRID[1:]), np.asarray(points))
    return output


def render_figure(payload: dict[str, Any], path: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13, 10), constrained_layout=True)
    floor = float(payload.get("figure", {}).get("positive_log_floor", 1.0e-18))
    for name, (x, y) in _median_by_candidate_chi(
        payload, "metrics.late_rms_d0_fraction"
    ).items():
        axes[0, 0].loglog(x, np.maximum(y, floor), marker="o", label=name)
    axes[0, 0].axhline(0.05, color="black", linestyle="--", linewidth=1)
    axes[0, 0].set(xlabel=r"$\chi$", ylabel=r"late RMS $D_0/\|Y_*\|_{D0}$")
    axes[0, 0].legend()

    for name, (x, y) in _median_by_candidate_chi(
        payload, "resolutions.base.effective_to_intended_rms"
    ).items():
        shown = np.maximum(y, floor)
        axes[0, 1].loglog(x, shown, marker="o", label=f"{name} ratio")
        zero = y == 0.0
        axes[0, 1].scatter(
            x[zero], shown[zero], marker="v", facecolors="none", edgecolors="black"
        )
    for name, (x, y) in _median_by_candidate_chi(
        payload, "resolutions.base.nonzero_fraction"
    ).items():
        shown = np.maximum(y, floor)
        axes[0, 1].loglog(x, shown, linestyle="--", label=f"{name} nonzero")
        zero = y == 0.0
        axes[0, 1].scatter(
            x[zero], shown[zero], marker="v", facecolors="none", edgecolors="black"
        )
    axes[0, 1].axhline(0.5, color="black", linestyle=":", linewidth=1)
    axes[0, 1].set(xlabel=r"$\chi$", ylabel="effective ratio / nonzero fraction")
    axes[0, 1].legend(fontsize=8)

    for name, (x, y) in _median_by_candidate_chi(
        payload, "metrics.maximum_radius_relative_error"
    ).items():
        axes[1, 0].loglog(
            x, np.maximum(y, floor), marker="o", label=f"{name} radius"
        )
    for name, (x, y) in _median_by_candidate_chi(
        payload, "metrics.late_rms_phase_error_over_theta"
    ).items():
        axes[1, 0].loglog(
            x, np.maximum(y, floor), linestyle="--", label=f"{name} phase/theta"
        )
    axes[1, 0].set(xlabel=r"$\chi$", ylabel="orbital error")
    axes[1, 0].legend(fontsize=8)

    stable = [
        row["chi"] for row in payload["grid"] if row["decision"] == "all-cell-stable"
    ]
    failures = [
        row["chi"] for row in payload["grid"] if row["decision"] == "stress-fail"
    ]
    selections: list[tuple[str, float, str]] = []
    if stable:
        selections.append(("last stable", max(stable), "-"))
    higher_failures = [value for value in failures if not stable or value > max(stable)]
    if higher_failures:
        selections.append(("first fail", min(higher_failures), "--"))
    if not selections:
        selections.append(("terminal", CHI_GRID[-1], "-"))
    for label, selected, style in selections:
        for name, *_ in CANDIDATES:
            row = next(
                item
                for item in payload["results"]
                if item["candidate_name"] == name
                and item["chi"] == selected
                and item["seed"] == SEEDS[0]
            )
            xy = np.asarray(
                [sample["newest"] for sample in row["trace"] if "newest" in sample]
            )
            axes[1, 1].plot(
                xy[:, 0], xy[:, 1], linestyle=style, label=f"{name} {label} {selected:.0e}"
            )
    axes[1, 1].set_aspect("equal", adjustable="box")
    axes[1, 1].set(xlabel="x (linear)", ylabel="y (linear)", title="representative orbits")
    axes[1, 1].legend()
    fig.suptitle(f"N0 noise stress: {payload['decision']}")
    fig.savefig(path, dpi=180, format="png")
    plt.close(fig)


def render_report(payload: dict[str, Any], *, json_sha256: str) -> str:
    lines = [
        "# N0 resolved-noise rotating-wave stress result",
        "",
        f"Decision: **`{payload['decision']}`**  ",
        f"Cross-scale interpretation: **`{payload['cross_scale_interpretation']}`**  ",
        f"Zero control: **{payload['zero_control_pass']}**  ",
        f"Execution revision: `{payload['provenance']['revision']}`  ",
        f"JSON SHA256: `{json_sha256}`",
        "",
        "## Registered grid",
        "",
        "| chi | decision |",
        "|---:|---|",
    ]
    lines.extend(f"| `{row['chi']:.0e}` | `{row['decision']}` |" for row in payload["grid"])
    lines.extend(
        [
            "",
            "## Scaling check",
            "",
            "| candidate | available | slope | compatible |",
            "|---|---:|---:|---:|",
        ]
    )
    for name, row in payload["scaling"].items():
        slope = "n/a" if not row["available"] else f"{row['slope']:.6g}"
        lines.append(f"| {name} | {row['available']} | {slope} | {row['compatible']} |")
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            payload["claim_boundary"],
            "",
            "The registered PNG uses logarithmic axes only for nonnegative",
            "stability metrics. Its x-y trajectory panel has linear equal-aspect axes.",
            f"The display-only positive log floor is `{payload['figure']['positive_log_floor']}`;",
            "open downward triangles mark exact zeros and no decision uses the floor.",
            "",
        ]
    )
    return "\n".join(lines)


def _resolved(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _validate_paths(summary: Path, report: Path, figure: Path) -> None:
    expected = (DEFAULT_SUMMARY, DEFAULT_REPORT, DEFAULT_FIGURE)
    supplied = (summary, report, figure)
    for given, target in zip(supplied, expected, strict=True):
        if _resolved(given).resolve() != (ROOT / target).resolve():
            raise RuntimeError("N0 permits only the registered output paths")
        final = _resolved(given)
        if final.exists() or final.with_name(final.name + ".tmp").exists():
            raise RuntimeError(f"refusing existing output or temporary: {final}")


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_safe(item) for item in value]
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def _write_outputs(payload: dict[str, Any], summary: Path, report: Path, figure: Path) -> None:
    finals = tuple(_resolved(path) for path in (summary, report, figure))
    temporaries = tuple(path.with_name(path.name + ".tmp") for path in finals)
    for path in (*finals, *temporaries):
        if path.exists():
            raise RuntimeError(f"refusing existing output or temporary: {path}")
    for path in finals:
        path.parent.mkdir(parents=True, exist_ok=True)
    serial = json.dumps(_json_safe(payload), allow_nan=False, indent=2, sort_keys=True) + "\n"
    digest = hashlib.sha256(serial.encode("utf-8")).hexdigest()
    try:
        temporaries[0].write_text(serial, encoding="utf-8")
        temporaries[1].write_text(
            render_report(payload, json_sha256=digest), encoding="utf-8"
        )
        render_figure(payload, temporaries[2])
        for temporary, final in zip(temporaries, finals, strict=True):
            temporary.replace(final)
    except Exception:
        for path in (*temporaries, *finals):
            path.unlink(missing_ok=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--figure", type=Path, default=DEFAULT_FIGURE)
    args = parser.parse_args()
    _validate_paths(args.summary, args.report, args.figure)
    payload = run_gate()
    _write_outputs(payload, args.summary, args.report, args.figure)
    print(json.dumps({"decision": payload["decision"]}))


if __name__ == "__main__":
    main()
