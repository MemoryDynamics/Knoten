"""Execute the frozen P2-R sign-sensitive long-recovery gate."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import hashlib
import importlib.metadata
import importlib.util
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Any

import numpy as np

from emergenz_knoten.loop_center_response import (
    co_rotating_fifo_forced_step,
    registered_zero_sum_waveforms,
)
from emergenz_knoten.rotating_wave_stability import (
    circular_history,
    co_rotating_fifo_step,
    rotation_translation_quotient_distance,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
P2_SCRIPT = Path(
    "experiments/current/dynamics/rotation/"
    "scalar_memory_loop_center_p2_gate.py"
)
PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_loop_center_p2r_long_recovery_protocol_2026-08-25.md"
)
P2_PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_loop_center_p2_protocol_2026-08-25.md"
)
P2_RESULT = Path(
    "reports/dynamics/rotation/scalar_memory_loop_center_p2_2026-08-25.json"
)
P2_REVIEW = Path(
    "reports/project/meta/reviews/scalar_memory_loop_center_p2_review_2026-08-25.md"
)
DEFAULT_REPORT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_center_p2r_long_recovery_2026-08-25.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_center_p2r_long_recovery_2026-08-25.json"
)

FREEZE_REVISION = "76145d7bd8ede06d5ae4f3a4166a452794a9e3ae"
EXPECTED_P2_SHA256 = (
    "697b9e9782fa5ba8cf694f8a84c6a931171cdec8a53b42605cb6b7971bc20656"
)
EXPECTED_BLOBS = {
    PROTOCOL.as_posix(): "9422397d04b7c64bcb6e98451f967b98de4020ab",
    P2_RESULT.as_posix(): "69cca249c5fb919f9c95b8e24cc230646f6a49c8",
    P2_REVIEW.as_posix(): "7404931c683ff740a0bce8bcd85d6a49b0acd91e",
    P2_SCRIPT.as_posix(): "542c0112a63dfefcee62b7e2238238017f26db72",
    "src/emergenz_knoten/loop_center_response.py": (
        "a8b8a002be3a3e4d75f8bd6b00989f1dafe61e0b"
    ),
}

CHECKPOINT_UPDATE = 2400
TOTAL_UPDATES = 4400
WINDOWS = (
    ("W1", 3201, 3600),
    ("W2", 3601, 4000),
    ("W3", 4001, 4400),
)
REPLAY_ABSOLUTE_TOLERANCE = 5.0e-15
REPLAY_RELATIVE_TOLERANCE = 5.0e-12
SIGNED_SLOPE_MAXIMUM = 0.0
LOG_RATE_MINIMUM = 0.2
LOG_RATE_MAXIMUM = 1.5
SAMPLED_INCREASE_MAXIMUM = 0.01
FINAL_RATIO_MAXIMUM = 5.0e-4
SIGNAL_FLOOR_FRACTION = 1.0e-8
LATE_GROWTH_FACTOR = 1.25
PROBE_OFF_FRACTION = 1.0e-10
TRACE_EVERY = 10


def _load_p2_module() -> Any:
    path = ROOT / P2_SCRIPT
    name = "scalar_memory_loop_center_p2_gate_frozen"
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load frozen P2 runner")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


P2 = _load_p2_module()
CANDIDATE = P2.CANDIDATE


def _git_output(arguments: list[str]) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return result.stdout.strip()


def _git_blob(path: str) -> str:
    return _git_output(["rev-parse", f"HEAD:{path}"])


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _verify_provenance() -> tuple[dict[str, Any], dict[str, Any]]:
    status = _git_output(["status", "--short"])
    if status:
        raise RuntimeError("P2-R target gate requires a clean prospective revision")
    revision = _git_output(["rev-parse", "HEAD"])
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", FREEZE_REVISION, revision],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("published P2-R freeze revision is not an ancestor")
    observed_blobs = {path: _git_blob(path) for path in EXPECTED_BLOBS}
    if observed_blobs != EXPECTED_BLOBS:
        raise RuntimeError("one or more frozen P2-R dependencies changed")
    p2_path = ROOT / P2_RESULT
    if _sha256(p2_path) != EXPECTED_P2_SHA256:
        raise RuntimeError("authoritative P2 JSON hash changed")
    old = json.loads(p2_path.read_text(encoding="utf-8"))
    if old.get("decision") != "loop-center-matrix-local-fail":
        raise RuntimeError("P2-R requires the immutable P2 fail")
    if old.get("candidate_id") != CANDIDATE.candidate_id:
        raise RuntimeError("P2-R candidate does not match P2")
    script_path = Path(__file__).resolve().relative_to(ROOT).as_posix()
    return (
        {
            "clean_pre_run_status": status,
            "revision": revision,
            "freeze_revision": FREEZE_REVISION,
            "freeze_is_ancestor": True,
            "expected_blobs": EXPECTED_BLOBS,
            "observed_blobs": observed_blobs,
            "implementation_blob": _git_blob(script_path),
            "p2_sha256": EXPECTED_P2_SHA256,
            "p2_decision": old["decision"],
        },
        old,
    )


def _close(old: float, replay: float) -> tuple[bool, float, float]:
    tolerance = REPLAY_ABSOLUTE_TOLERANCE + REPLAY_RELATIVE_TOLERANCE * abs(old)
    error = abs(replay - old)
    return error <= tolerance, error, tolerance


def _flatten_replay_metrics(payload: dict[str, Any]) -> dict[str, float | bool | str]:
    values: dict[str, float | bool | str] = {
        "decision": payload["decision"],
        "scalar.decision": payload["scalar_origin_comparator"]["decision"],
        "scalar.g_h": payload["scalar_origin_comparator"]["g_h"],
        "scalar.pole": payload["scalar_origin_comparator"][
            "untruncated_scalar_pole"
        ],
    }
    for name, value in payload["gates"].items():
        values[f"gate.{name}"] = value
    control_metrics = {
        "fixed_point": ("maximum_component_error", "pass"),
        "unrelated_joint_jacobian": ("relative_error", "pass"),
        "center_recurrence": ("maximum_absolute_error", "pass"),
        "phase_covariance": ("maximum_normalized_error", "pass"),
        "probe_off": ("final_d0", "pass"),
    }
    for name, keys in control_metrics.items():
        for key in keys:
            values[f"control.{name}.{key}"] = payload["controls"][name][key]
    row_keys = (
        "complete_and_finite",
        "state_tangent_relative_rms",
        "center_velocity_tangent_relative_rms",
        "even_state_relative_rms",
        "single_sign_remainder_relative_rms",
        "normalized_odd_collapse_relative_rms",
        "tangent_center_velocity_rms",
        "signal_above_floor",
        "maximum_d0_fraction",
        "final_d0_ratio",
        "tail_slope_fraction_per_memory_time",
        "pass",
    )
    for panel in ("primary", "waveform_holdout"):
        for row in payload[panel]:
            identity = (
                f"{panel}.{row['waveform']}.{row['direction']}."
                f"{float(row['amplitude_fraction']):.12g}"
            )
            for key in row_keys:
                values[f"{identity}.{key}"] = row[key]
    for row in payload["quadratic_remainder_slopes"]:
        identity = f"slope.{row['direction']}"
        values[f"{identity}.secant"] = row["secant_slope"]
        values[f"{identity}.pass"] = row["pass"]
    return values


def _compare_full_replay(
    old: dict[str, Any], replay: dict[str, Any]
) -> dict[str, Any]:
    expected = _flatten_replay_metrics(old)
    observed = _flatten_replay_metrics(replay)
    mismatches = []
    maximum_ratio = 0.0
    for name, old_value in expected.items():
        replay_value = observed.get(name)
        if isinstance(old_value, bool) or isinstance(old_value, str):
            if replay_value != old_value:
                mismatches.append(
                    {"metric": name, "old": old_value, "replay": replay_value}
                )
            continue
        passed, error, tolerance = _close(float(old_value), float(replay_value))
        maximum_ratio = max(maximum_ratio, error / tolerance)
        if not passed:
            mismatches.append(
                {
                    "metric": name,
                    "old": old_value,
                    "replay": replay_value,
                    "error": error,
                    "tolerance": tolerance,
                }
            )
    return {
        "metric_count": len(expected),
        "maximum_error_to_tolerance_ratio": maximum_ratio,
        "mismatches": mismatches,
        "pass": not mismatches,
        "replayed_decision": replay["decision"],
    }


def _least_squares_slope(x: np.ndarray, y: np.ndarray) -> float:
    centered = x - np.mean(x)
    denominator = float(np.dot(centered, centered))
    if denominator <= 0.0:
        return math.nan
    return float(np.dot(centered, y - np.mean(y)) / denominator)


def window_metrics(
    distances: np.ndarray,
    *,
    checkpoint_peak: float,
    start: int,
    end: int,
) -> dict[str, Any]:
    """Return the frozen sign, log-rate, envelope and signal diagnostics."""

    if distances.shape != (TOTAL_UPDATES,):
        raise ValueError("distances must contain the complete P2-R trace")
    values = np.asarray(distances[start - 1 : end], dtype=float)
    steps = np.arange(start, end + 1, dtype=float)
    memory_time = CANDIDATE.alpha * steps
    signed_slope = _least_squares_slope(
        memory_time,
        values / checkpoint_peak,
    )
    log_rate = -_least_squares_slope(memory_time, np.log(values))
    sample_mask = (steps.astype(int) % TRACE_EVERY) == 0
    sampled = values[sample_mask]
    increases = sampled[1:] / sampled[:-1] - 1.0
    maximum_increase = float(np.max(increases))
    minimum_fraction = float(np.min(values) / checkpoint_peak)
    gates = {
        "negative_signed_slope": bool(signed_slope < SIGNED_SLOPE_MAXIMUM),
        "log_rate": bool(LOG_RATE_MINIMUM <= log_rate <= LOG_RATE_MAXIMUM),
        "sampled_increase": bool(maximum_increase <= SAMPLED_INCREASE_MAXIMUM),
    }
    return {
        "start": start,
        "end": end,
        "signed_slope_fraction_per_memory_time": signed_slope,
        "log_decay_rate_per_memory_time": log_rate,
        "maximum_sampled_ten_update_increase": maximum_increase,
        "minimum_fraction_of_checkpoint_peak": minimum_fraction,
        "gates": gates,
        "pass": all(gates.values()),
    }


def _old_row_map(old: dict[str, Any]) -> dict[tuple[str, str, float], dict[str, Any]]:
    rows = old["primary"] + old["waveform_holdout"]
    return {
        (row["waveform"], row["direction"], float(row["amplitude_fraction"])): row
        for row in rows
    }


def _checkpoint_comparison(
    *,
    plus_distances: np.ndarray,
    minus_distances: np.ndarray,
    old_row: dict[str, Any],
) -> dict[str, Any]:
    plus = plus_distances[:CHECKPOINT_UPDATE]
    minus = minus_distances[:CHECKPOINT_UPDATE]
    maximum_plus = float(np.max(plus))
    maximum_minus = float(np.max(minus))
    maximum = max(maximum_plus, maximum_minus)
    final_ratio = max(
        float(plus[-1] / maximum_plus),
        float(minus[-1] / maximum_minus),
    )
    tail_slope = max(
        P2._tail_slope(plus.tolist(), maximum_plus),
        P2._tail_slope(minus.tolist(), maximum_minus),
    )
    replayed = {
        "maximum_d0": maximum,
        "maximum_d0_fraction": maximum / CANDIDATE.radius,
        "final_d0_ratio": final_ratio,
        "tail_slope_fraction_per_memory_time": tail_slope,
    }
    comparisons = {}
    passed = True
    for name, value in replayed.items():
        close, error, tolerance = _close(float(old_row[name]), value)
        comparisons[name] = {
            "old": old_row[name],
            "replay": value,
            "error": error,
            "tolerance": tolerance,
            "pass": close,
        }
        passed = passed and close
    return {
        "checkpoint_peak_plus": maximum_plus,
        "checkpoint_peak_minus": maximum_minus,
        "metrics": comparisons,
        "pass": passed,
    }


def _branch_recovery(
    distances: np.ndarray,
    *,
    checkpoint_peak: float,
) -> dict[str, Any]:
    windows = {
        name: window_metrics(
            distances,
            checkpoint_peak=checkpoint_peak,
            start=start,
            end=end,
        )
        for name, start, end in WINDOWS
    }
    final_ratio = float(distances[-1] / checkpoint_peak)
    w3_start = WINDOWS[-1][1]
    signal_minimum = float(
        np.min(distances[w3_start - 1 :]) / checkpoint_peak
    )
    late_growth = float(
        np.max(distances[CHECKPOINT_UPDATE:]) / checkpoint_peak
    )
    gates = {
        "windows": all(row["pass"] for row in windows.values()),
        "final_ratio": bool(final_ratio <= FINAL_RATIO_MAXIMUM),
        "signal_floor": bool(signal_minimum >= SIGNAL_FLOOR_FRACTION),
        "late_growth": bool(late_growth <= LATE_GROWTH_FACTOR),
    }
    return {
        "checkpoint_peak": checkpoint_peak,
        "windows": windows,
        "final_ratio": final_ratio,
        "signal_minimum_fraction": signal_minimum,
        "maximum_post_checkpoint_fraction": late_growth,
        "gates": gates,
        "pass": all(gates.values()),
    }


def _run_long_row(
    *,
    history: np.ndarray,
    waveform_name: str,
    waveform: np.ndarray,
    direction_name: str,
    direction: np.ndarray,
    amplitude: float,
    old_row: dict[str, Any],
) -> dict[str, Any]:
    plus = history.copy()
    minus = history.copy()
    off = history.copy()
    plus_distances = np.empty(TOTAL_UPDATES)
    minus_distances = np.empty(TOTAL_UPDATES)
    trace = []
    complete = True
    completed = 0
    for step_index in range(TOTAL_UPDATES):
        force = P2._force_at_step(
            waveform,
            step_index=step_index,
            amplitude=amplitude,
            direction=direction,
        )
        plus = co_rotating_fifo_forced_step(
            plus,
            force_lab=force,
            step_index=step_index,
            theta=CANDIDATE.theta,
            **CANDIDATE.step_parameters(),
        )
        minus = co_rotating_fifo_forced_step(
            minus,
            force_lab=-force,
            step_index=step_index,
            theta=CANDIDATE.theta,
            **CANDIDATE.step_parameters(),
        )
        off = co_rotating_fifo_step(
            off,
            theta=CANDIDATE.theta,
            **CANDIDATE.step_parameters(),
        )
        if not all(np.isfinite(value).all() for value in (plus, minus, off)):
            complete = False
            break
        plus_distance, _ = rotation_translation_quotient_distance(
            plus,
            off,
            alpha=CANDIDATE.alpha,
            memory_mass=CANDIDATE.memory_mass,
        )
        minus_distance, _ = rotation_translation_quotient_distance(
            minus,
            off,
            alpha=CANDIDATE.alpha,
            memory_mass=CANDIDATE.memory_mass,
        )
        plus_distances[step_index] = plus_distance
        minus_distances[step_index] = minus_distance
        completed = step_index + 1
        if completed % TRACE_EVERY == 0 or completed in (
            1,
            CHECKPOINT_UPDATE,
            TOTAL_UPDATES,
        ):
            trace.append(
                {
                    "step": completed,
                    "plus_d0": plus_distance,
                    "minus_d0": minus_distance,
                }
            )

    if not complete or completed != TOTAL_UPDATES:
        return {
            "waveform": waveform_name,
            "direction": direction_name,
            "amplitude_fraction": amplitude,
            "complete_and_finite": False,
            "completed_updates": completed,
            "pass": False,
            "trace": trace,
        }

    checkpoint = _checkpoint_comparison(
        plus_distances=plus_distances,
        minus_distances=minus_distances,
        old_row=old_row,
    )
    plus_recovery = _branch_recovery(
        plus_distances,
        checkpoint_peak=checkpoint["checkpoint_peak_plus"],
    )
    minus_recovery = _branch_recovery(
        minus_distances,
        checkpoint_peak=checkpoint["checkpoint_peak_minus"],
    )
    off_distance, _ = rotation_translation_quotient_distance(
        off,
        history,
        alpha=CANDIDATE.alpha,
        memory_mass=CANDIDATE.memory_mass,
    )
    return {
        "waveform": waveform_name,
        "direction": direction_name,
        "amplitude_fraction": amplitude,
        "complete_and_finite": True,
        "completed_updates": completed,
        "checkpoint_replay": checkpoint,
        "plus": plus_recovery,
        "minus": minus_recovery,
        "probe_off_final_d0": off_distance,
        "pass": bool(
            checkpoint["pass"] and plus_recovery["pass"] and minus_recovery["pass"]
        ),
        "trace": trace,
    }


def _evaluate_decision(
    *,
    full_replay: dict[str, Any],
    rows: list[dict[str, Any]],
    probe_off_pass: bool,
) -> tuple[str, dict[str, bool]]:
    complete = all(row["complete_and_finite"] for row in rows)
    checkpoint_replay = complete and all(
        row["checkpoint_replay"]["pass"] for row in rows
    )
    signal = complete and all(
        row[branch]["gates"]["signal_floor"]
        for row in rows
        for branch in ("plus", "minus")
    )
    recovery = complete and all(row["pass"] for row in rows)
    gates = {
        "full_p2_replay": full_replay["pass"],
        "complete_traces": complete,
        "checkpoint_replay": checkpoint_replay,
        "signals_above_floor": signal,
        "recovery": recovery,
        "probe_off": probe_off_pass,
    }
    if not full_replay["pass"] or not complete or not checkpoint_replay or not signal:
        decision = "p2r-sign-sensitive-long-recovery-inconclusive"
    elif all(gates.values()):
        decision = "p2r-sign-sensitive-long-recovery-pass"
    else:
        decision = "p2r-sign-sensitive-long-recovery-fail"
    return decision, gates


def run_gate() -> dict[str, Any]:
    """Run the complete old-P2 replay and the frozen long-recovery extension."""

    started = time.perf_counter()
    provenance, old = _verify_provenance()
    replay = P2.run_gate()
    full_replay = _compare_full_replay(old, replay)

    history = circular_history(
        radius=CANDIDATE.radius,
        theta=CANDIDATE.theta,
        horizon=CANDIDATE.horizon,
    )
    waveforms = registered_zero_sum_waveforms(P2.PROBE_UPDATES)
    old_rows = _old_row_map(old)
    rows = []
    for direction_name, direction in P2.DIRECTIONS.items():
        for amplitude in P2.PRIMARY_AMPLITUDES:
            key = ("sine_cycle", direction_name, amplitude)
            rows.append(
                _run_long_row(
                    history=history,
                    waveform_name="sine_cycle",
                    waveform=waveforms["sine_cycle"],
                    direction_name=direction_name,
                    direction=direction,
                    amplitude=amplitude,
                    old_row=old_rows[key],
                )
            )
        key = ("hann_doublet", direction_name, P2.HOLDOUT_AMPLITUDE)
        rows.append(
            _run_long_row(
                history=history,
                waveform_name="hann_doublet",
                waveform=waveforms["hann_doublet"],
                direction_name=direction_name,
                direction=direction,
                amplitude=P2.HOLDOUT_AMPLITUDE,
                old_row=old_rows[key],
            )
        )

    maximum_off = max(row.get("probe_off_final_d0", math.inf) for row in rows)
    off_threshold = PROBE_OFF_FRACTION * CANDIDATE.radius
    probe_off_pass = bool(maximum_off <= off_threshold)
    decision, gates = _evaluate_decision(
        full_replay=full_replay,
        rows=rows,
        probe_off_pass=probe_off_pass,
    )
    return {
        "schema_version": 1,
        "gate": "P2-R sign-sensitive L3 long recovery",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "elapsed_seconds": time.perf_counter() - started,
        "candidate_id": CANDIDATE.candidate_id,
        "provenance": provenance,
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": importlib.metadata.version("numpy"),
            "scipy": importlib.metadata.version("scipy"),
        },
        "protocol": {
            "path": PROTOCOL.as_posix(),
            "freeze_revision": FREEZE_REVISION,
            "checkpoint_update": CHECKPOINT_UPDATE,
            "total_updates": TOTAL_UPDATES,
            "windows": [
                {"name": name, "start": start, "end": end}
                for name, start, end in WINDOWS
            ],
            "thresholds": {
                "replay_absolute": REPLAY_ABSOLUTE_TOLERANCE,
                "replay_relative": REPLAY_RELATIVE_TOLERANCE,
                "signed_slope_maximum": SIGNED_SLOPE_MAXIMUM,
                "log_rate_minimum": LOG_RATE_MINIMUM,
                "log_rate_maximum": LOG_RATE_MAXIMUM,
                "sampled_increase_maximum": SAMPLED_INCREASE_MAXIMUM,
                "final_ratio_maximum": FINAL_RATIO_MAXIMUM,
                "signal_floor_fraction": SIGNAL_FLOOR_FRACTION,
                "late_growth_factor": LATE_GROWTH_FACTOR,
                "probe_off_fraction": PROBE_OFF_FRACTION,
            },
            "outcome_informed": True,
            "parameter_retuning": False,
            "p2_decision_relabel_allowed": False,
        },
        "full_p2_replay": full_replay,
        "rows": rows,
        "probe_off": {
            "maximum_final_d0": maximum_off,
            "threshold": off_threshold,
            "pass": probe_off_pass,
        },
        "gates": gates,
        "decision": decision,
        "historical_p2_decision": old["decision"],
        "claim_boundary": {
            "established_if_pass": (
                "continued sign-consistent local recovery of the prepared L3 "
                "loop through 20 recovery memory times in the frozen panel"
            ),
            "not_established": (
                "relabeling of P2, independent replication, scalar-origin "
                "Center eligibility, formation, finite basin, microscopic "
                "center-conjugate actuator, work, or physical mass"
            ),
        },
    }


def _format(value: float) -> str:
    return f"{value:.6g}"


def render_report(payload: dict[str, Any], *, summary_sha256: str) -> str:
    """Render the P2-R Markdown report from its authoritative payload."""

    lines = [
        "# P2-R sign-sensitive L3 long recovery",
        "",
        f"Date: {payload['generated_at_utc'][:10]}.",
        "",
        f"Decision: **`{payload['decision']}`**.",
        "",
        "This is an outcome-informed reconciliation of the immutable P2 tail",
        "failure. It does not rename the historical P2 decision.",
        "",
        "## Replay controls",
        "",
        "| control | observed | pass |",
        "| --- | ---: | :---: |",
        (
            "| complete old-P2 scalar metrics | "
            f"{payload['full_p2_replay']['metric_count']} metrics, max "
            f"error/tolerance {_format(payload['full_p2_replay']['maximum_error_to_tolerance_ratio'])} | "
            f"{payload['full_p2_replay']['pass']} |"
        ),
        (
            "| long-run 2400 checkpoint replay | all eight response rows | "
            f"{payload['gates']['checkpoint_replay']} |"
        ),
        (
            "| extended probe off | "
            f"{_format(payload['probe_off']['maximum_final_d0'])} | "
            f"{payload['probe_off']['pass']} |"
        ),
        "",
        "## Sign-sensitive recovery",
        "",
        "Each range below is over the three frozen late windows.",
        "",
        "| waveform | direction | amplitude | branch | signed slope range | log-rate range | max sampled increase | final/peak | signal min | pass |",
        "| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | :---: |",
    ]
    for row in payload["rows"]:
        for branch_name in ("plus", "minus"):
            branch = row[branch_name]
            windows = list(branch["windows"].values())
            slopes = [item["signed_slope_fraction_per_memory_time"] for item in windows]
            rates = [item["log_decay_rate_per_memory_time"] for item in windows]
            increases = [item["maximum_sampled_ten_update_increase"] for item in windows]
            lines.append(
                f"| {row['waveform']} | {row['direction']} | "
                f"{_format(row['amplitude_fraction'])} | {branch_name} | "
                f"{_format(min(slopes))} .. {_format(max(slopes))} | "
                f"{_format(min(rates))} .. {_format(max(rates))} | "
                f"{_format(max(increases))} | {_format(branch['final_ratio'])} | "
                f"{_format(branch['signal_minimum_fraction'])} | {branch['pass']} |"
            )
    lines.extend(
        [
            "",
            "## Decision and limits",
            "",
            f"Gate components: `{json.dumps(payload['gates'], sort_keys=True)}`.",
            "",
            f"The historical P2 decision remains **`{payload['historical_p2_decision']}`**.",
            "P2-R changes only the observation horizon and the prospectively",
            "declared sign-sensitive recovery question. A pass supports local",
            "recovery of one prepared loop; it is neither an independent",
            "replication nor evidence for formation, a scalar Center mass, a",
            "microscopic actuator, work or physical mass.",
            "",
            "## Provenance",
            "",
            f"- freeze revision: `{payload['provenance']['freeze_revision']}`;",
            f"- execution revision: `{payload['provenance']['revision']}`;",
            f"- source P2 SHA-256: `{payload['provenance']['p2_sha256']}`;",
            f"- P2-R JSON SHA-256: `{summary_sha256}`;",
            f"- elapsed seconds: `{_format(payload['elapsed_seconds'])}`;",
            f"- Python / NumPy / SciPy: `{payload['runtime']['python']}` / "
            f"`{payload['runtime']['numpy']}` / `{payload['runtime']['scipy']}`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    arguments = parser.parse_args()

    payload = run_gate()
    summary = ROOT / arguments.summary
    report = ROOT / arguments.report
    summary.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report.write_text(
        render_report(payload, summary_sha256=_sha256(summary)),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "decision": payload["decision"],
                "historical_p2_decision": payload["historical_p2_decision"],
                "report": report.relative_to(ROOT).as_posix(),
                "summary": summary.relative_to(ROOT).as_posix(),
                "elapsed_seconds": payload["elapsed_seconds"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
