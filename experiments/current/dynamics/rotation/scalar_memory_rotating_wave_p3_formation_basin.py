"""Execute the frozen P3 L3 formation and sampled-basin gate."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import UTC, datetime
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import subprocess
import time
from typing import Any

import numpy as np

from emergenz_knoten.rotating_wave_formation import (
    FormationThresholds,
    evaluate_layered_decision,
    normalized_memory_weights,
    raw_mirror_error,
    registered_history_pairs,
    run_achiral_control,
    run_fifo_only_control,
    run_mirrored_pair,
    target_history,
)
from emergenz_knoten.rotating_wave_stability import (
    native_fifo_step,
    rotation_matrix,
    rotation_translation_quotient_distance,
)
from emergenz_knoten.rotating_wave_stability_gate import RotatingWaveCandidate


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_p3_formation_basin_protocol_2026-08-26.md"
)
P1_RESULT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_l3_stability_2026-08-22.json"
)
P1_REVIEW = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_l3_stability_review_2026-08-22.md"
)
P2_RESULT = Path(
    "reports/dynamics/rotation/scalar_memory_loop_center_p2_2026-08-25.json"
)
P2_REVIEW = Path(
    "reports/project/meta/reviews/scalar_memory_loop_center_p2_review_2026-08-25.md"
)
P2R_RESULT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_center_p2r_long_recovery_2026-08-25.json"
)
P2R_REVIEW = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_loop_center_p2r_long_recovery_review_2026-08-25.md"
)
DEFAULT_REPORT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_p3_formation_basin_2026-08-26.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_p3_formation_basin_2026-08-26.json"
)

FREEZE_REVISION = "0fd79b3636fe09c377a51200414e46bdf9eb6a9f"
EXPECTED_P2R_SHA256 = (
    "484d0c614471980f81a242e3656ccea7793bd4c832f6138621cee575c36c1423"
)
EXPECTED_BLOBS = {
    PROTOCOL.as_posix(): "33f0826d1a727fb7812ed30ae95b9453e5b2dab8",
    P1_RESULT.as_posix(): "18821ed0235e5e915424f61c665be86d569d58cc",
    P1_REVIEW.as_posix(): "8fa25608f165789662ca1fb92d2507791dc143ea",
    P2_RESULT.as_posix(): "69cca249c5fb919f9c95b8e24cc230646f6a49c8",
    P2_REVIEW.as_posix(): "7404931c683ff740a0bce8bcd85d6a49b0acd91e",
    P2R_RESULT.as_posix(): "d6ac2d4bb522e73e69af03a0d1548e7c893c2e84",
    P2R_REVIEW.as_posix(): "240fbebe3419547670fce40a871387e6674e378a",
    "src/emergenz_knoten/rotating_wave_stability.py": (
        "9defb5a6876371202e1ba57cea030c997b9c6edd"
    ),
    "src/emergenz_knoten/rotating_wave_stability_gate.py": (
        "630beb9952abefea823d91388dcbb2de8f1a2927"
    ),
}

CANDIDATE_ID = "k0h-rw-l3-aatt3p5-alpha0p005-h2400-eta0p075-v1"
RADIUS_DECIMAL = (
    "0.944805811705743656419366118422595657454474452804188781825799206245348"
    "464567689511866917417017911971955244464"
)
THETA_DECIMAL = (
    "0.007906661462435523749384967030309742461978034595274092598156965831417"
    "08245813094145986593003659167675765833059"
)
CANDIDATE = RotatingWaveCandidate(
    candidate_id=CANDIDATE_ID,
    radius=float(RADIUS_DECIMAL),
    theta=float(THETA_DECIMAL),
    alpha=0.005,
    horizon=2400,
    memory_mass=1.0,
    eta=0.075,
    sigma_rep=1.0,
    sigma_att=3.0,
    amplitude_rep=1.0,
    amplitude_att=3.5,
)
THRESHOLDS = FormationThresholds()

EXPECTED_TARGET_SEPARATION = 1.1134199709942472
EXPECTED_INITIAL_D0 = {
    "ellipse_e0p03": 0.03229444319841298,
    "ellipse_e0p10": 0.1079491520241994,
    "warped_geometry_holdout": 0.1082191303711561,
    "wrong_rate_ellipse": 0.6318738063717837,
    "damped_hook_holdout": 0.6787314983982393,
}
STATIC_TOLERANCE = 5.0e-13
INITIAL_CHIRALITY_MARGIN = 0.1
PREPARED_ONE_STEP_TOLERANCE = 1.0e-14


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


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _verify_provenance() -> dict[str, Any]:
    status = _git_output(["status", "--short"])
    if status:
        raise RuntimeError("P3 target gate requires a clean prospective revision")
    revision = _git_output(["rev-parse", "HEAD"])
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", FREEZE_REVISION, revision],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("published P3 freeze revision is not an ancestor")
    observed_blobs = {path: _git_blob(path) for path in EXPECTED_BLOBS}
    if observed_blobs != EXPECTED_BLOBS:
        raise RuntimeError("one or more frozen P3 dependencies changed")
    if _sha256(ROOT / P2R_RESULT) != EXPECTED_P2R_SHA256:
        raise RuntimeError("authoritative P2-R JSON hash changed")

    p1 = _load_json(P1_RESULT)
    p2 = _load_json(P2_RESULT)
    p2r = _load_json(P2R_RESULT)
    if p1.get("decision") != "numerically-stable-source-pass":
        raise RuntimeError("P3 requires the reviewed P1 pass")
    if p2.get("decision") != "loop-center-matrix-local-fail":
        raise RuntimeError("P3 must preserve the historical P2 fail")
    if p2r.get("decision") != "p2r-sign-sensitive-long-recovery-pass":
        raise RuntimeError("P3 requires the reviewed P2-R pass")
    candidate = p1.get("candidate", {})
    if candidate.get("candidate_id") != CANDIDATE_ID:
        raise RuntimeError("P1 candidate identifier does not match P3")
    if candidate.get("radius_decimal") != RADIUS_DECIMAL:
        raise RuntimeError("P1 radius decimal does not match P3")
    if candidate.get("theta_decimal") != THETA_DECIMAL:
        raise RuntimeError("P1 theta decimal does not match P3")
    if p2r.get("candidate_id") != CANDIDATE_ID:
        raise RuntimeError("P2-R candidate identifier does not match P3")

    script_path = Path(__file__).resolve().relative_to(ROOT).as_posix()
    module_path = "src/emergenz_knoten/rotating_wave_formation.py"
    return {
        "clean_pre_run_status": status,
        "revision": revision,
        "freeze_revision": FREEZE_REVISION,
        "freeze_is_ancestor": True,
        "expected_blobs": EXPECTED_BLOBS,
        "observed_blobs": observed_blobs,
        "implementation_blobs": {
            script_path: _git_blob(script_path),
            module_path: _git_blob(module_path),
        },
        "p1_decision": p1["decision"],
        "p2_decision": p2["decision"],
        "p2r_decision": p2r["decision"],
        "p2r_sha256": EXPECTED_P2R_SHA256,
    }


def _construction_controls() -> dict[str, Any]:
    pairs = registered_history_pairs(CANDIDATE)
    targets = {
        1: target_history(CANDIDATE, chirality=1),
        -1: target_history(CANDIDATE, chirality=-1),
    }
    weights = normalized_memory_weights(CANDIDATE)
    separation, _ = rotation_translation_quotient_distance(
        targets[-1],
        targets[1],
        alpha=CANDIDATE.alpha,
        memory_mass=CANDIDATE.memory_mass,
    )
    separation_fraction = separation / CANDIDATE.radius
    target_separation = {
        "observed_fraction": separation_fraction,
        "expected_fraction": EXPECTED_TARGET_SEPARATION,
        "absolute_error": abs(separation_fraction - EXPECTED_TARGET_SEPARATION),
        "tolerance": STATIC_TOLERANCE,
        "pass": bool(
            abs(separation_fraction - EXPECTED_TARGET_SEPARATION)
            <= STATIC_TOLERANCE
        ),
    }

    rows: list[dict[str, Any]] = []
    for pair in pairs:
        plus = pair["plus"]
        minus = pair["minus"]
        plus_expected, _ = rotation_translation_quotient_distance(
            plus,
            targets[1],
            alpha=CANDIDATE.alpha,
            memory_mass=CANDIDATE.memory_mass,
        )
        minus_expected, _ = rotation_translation_quotient_distance(
            minus,
            targets[-1],
            alpha=CANDIDATE.alpha,
            memory_mass=CANDIDATE.memory_mass,
        )
        plus_opposite, _ = rotation_translation_quotient_distance(
            plus,
            targets[-1],
            alpha=CANDIDATE.alpha,
            memory_mass=CANDIDATE.memory_mass,
        )
        plus_fraction = plus_expected / CANDIDATE.radius
        minus_fraction = minus_expected / CANDIDATE.radius
        opposite_fraction = plus_opposite / CANDIDATE.radius
        expected = EXPECTED_INITIAL_D0.get(pair["name"], 0.0)
        static_error = abs(plus_fraction - expected)
        mirror_distance = raw_mirror_error(plus, minus, weights=weights)
        noncircular = pair["panel"] != "prepared"
        gates = {
            "shape_and_finite": bool(
                plus.shape == (CANDIDATE.horizon, 2)
                and minus.shape == plus.shape
                and np.isfinite(plus).all()
                and np.isfinite(minus).all()
            ),
            "static_value": bool(static_error <= STATIC_TOLERANCE),
            "mirrored_static_distance": bool(
                abs(plus_fraction - minus_fraction) <= STATIC_TOLERANCE
            ),
            "raw_reflection": bool(mirror_distance <= STATIC_TOLERANCE),
            "seed_chirality": bool(
                not noncircular
                or opposite_fraction - plus_fraction >= INITIAL_CHIRALITY_MARGIN
            ),
        }
        rows.append(
            {
                "name": pair["name"],
                "panel": pair["panel"],
                "plus_expected_fraction": plus_fraction,
                "minus_expected_fraction": minus_fraction,
                "plus_opposite_fraction": opposite_fraction,
                "chirality_margin": opposite_fraction - plus_fraction,
                "registered_expected_fraction": expected,
                "static_absolute_error": static_error,
                "raw_mirror_error": mirror_distance,
                "gates": gates,
                "pass": bool(all(gates.values())),
            }
        )

    one_step_rows = []
    for sign in (1, -1):
        observed = native_fifo_step(
            targets[sign],
            **CANDIDATE.step_parameters(),
        )
        expected = targets[sign] @ rotation_matrix(sign * CANDIDATE.theta).T
        error = float(np.max(np.abs(observed - expected)))
        one_step_rows.append(
            {
                "chirality": sign,
                "maximum_component_error": error,
                "threshold": PREPARED_ONE_STEP_TOLERANCE,
                "pass": bool(error <= PREPARED_ONE_STEP_TOLERANCE),
            }
        )
    return {
        "target_separation": target_separation,
        "histories": rows,
        "prepared_one_step": one_step_rows,
        "pass": bool(
            target_separation["pass"]
            and all(row["pass"] for row in rows)
            and all(row["pass"] for row in one_step_rows)
        ),
    }


def _flatten_active_arms(
    pairs: list[dict[str, Any]],
    *,
    panel: str,
) -> list[dict[str, Any]]:
    return [
        pair[branch]
        for pair in pairs
        if pair["panel"] == panel
        for branch in ("plus", "minus")
    ]


def _stored_pair_metrics_finite(pairs: list[dict[str, Any]]) -> bool:
    keys = (
        "expected_d0",
        "expected_d0_fraction",
        "opposite_d0",
        "opposite_d0_fraction",
        "alignment_phase",
        "translation_reduced_norm",
        "translation_reduced_norm_fraction",
        "centroid_x",
        "centroid_y",
        "centroid_norm",
    )
    return bool(
        all(
            math.isfinite(float(row[key]))
            for pair in pairs
            for branch in ("plus", "minus")
            for row in pair[branch]["trace"]
            for key in keys
        )
    )


def run_gate() -> dict[str, Any]:
    """Execute the frozen P3 target calculation."""

    started = time.perf_counter()
    provenance = _verify_provenance()
    construction = _construction_controls()
    registered = registered_history_pairs(CANDIDATE)
    pair_results = []
    for pair in registered:
        pair_results.append(
            run_mirrored_pair(
                name=pair["name"],
                panel=pair["panel"],
                plus_history=pair["plus"],
                minus_history=pair["minus"],
                candidate=CANDIDATE,
                thresholds=THRESHOLDS,
            )
        )

    fifo_only = run_fifo_only_control(CANDIDATE, THRESHOLDS)
    achiral = run_achiral_control(CANDIDATE, THRESHOLDS)
    prepared = [pair for pair in pair_results if pair["panel"] == "prepared"]
    basin_arms = _flatten_active_arms(pair_results, panel="basin")
    formation_arms = _flatten_active_arms(pair_results, panel="formation")
    registration = {
        "pair_names": [pair["name"] for pair in pair_results],
        "prepared_pairs": len(prepared),
        "basin_arms": len(basin_arms),
        "formation_arms": len(formation_arms),
        "pass": bool(
            [pair["name"] for pair in pair_results]
            == [
                "prepared_circle",
                "ellipse_e0p03",
                "ellipse_e0p10",
                "warped_geometry_holdout",
                "wrong_rate_ellipse",
                "damped_hook_holdout",
            ]
            and len(prepared) == 1
            and len(basin_arms) == 6
            and len(formation_arms) == 4
        ),
    }
    controls = {
        "provenance": True,
        "construction": bool(construction["pass"]),
        "registration": bool(registration["pass"]),
        "metric_evaluation": _stored_pair_metrics_finite(pair_results),
        "prepared": bool(len(prepared) == 1 and prepared[0]["pass"]),
        "mirror_equivariance": bool(
            all(pair["mirror"]["pass"] for pair in pair_results)
        ),
        "fifo_only_negative": bool(fifo_only["pass"]),
        "achiral_negative": bool(achiral["pass"]),
    }
    pipeline_controls = bool(all(controls.values()))
    decision, gates = evaluate_layered_decision(
        pipeline_controls=pipeline_controls,
        basin_arms=basin_arms,
        formation_arms=formation_arms,
    )
    return {
        "schema_version": 1,
        "gate": "P3 L3 formation and sampled finite basin",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "elapsed_seconds": time.perf_counter() - started,
        "candidate_id": CANDIDATE_ID,
        "candidate": {
            **asdict(CANDIDATE),
            "radius_decimal": RADIUS_DECIMAL,
            "theta_decimal": THETA_DECIMAL,
            "deposition_kernel": "delta",
            "epsilon": 0.0,
        },
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
            "thresholds": asdict(THRESHOLDS),
            "target_separation_fraction": EXPECTED_TARGET_SEPARATION,
            "initial_d0_fractions": EXPECTED_INITIAL_D0,
            "static_tolerance": STATIC_TOLERANCE,
            "initial_chirality_margin": INITIAL_CHIRALITY_MARGIN,
            "no_target_fit": True,
        },
        "construction_controls": construction,
        "registration": registration,
        "pairs": pair_results,
        "negative_controls": {
            "fifo_only": fifo_only,
            "achiral": achiral,
        },
        "pipeline_controls": controls,
        "gates": gates,
        "decision": decision,
        "claim_boundary": {
            "established_if_full_pass": (
                "attraction to the reviewed L3 relative equilibrium for the "
                "ten registered noncircular arms in five mirror pairs, "
                "including four target-blind arms"
            ),
            "not_established": (
                "open basin ball or volume, generic or spontaneous formation, "
                "chirality selection from symmetric data, noise robustness, "
                "internal S1, mechanics, interaction, work or mass"
            ),
        },
    }


def _format(value: float | int | None) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return str(value)
    return f"{value:.6g}"


def render_report(payload: dict[str, Any], *, summary_sha256: str) -> str:
    """Render the human-readable P3 report from the authoritative payload."""

    lines = [
        "# P3 L3 formation and sampled finite basin",
        "",
        f"Date: {payload['generated_at_utc'][:10]}.",
        "",
        f"Decision: **`{payload['decision']}`**.",
        "",
        "The target-informed sampled-basin panel and target-blind formation",
        "panel are reported separately. Mirror branches are symmetry controls,",
        "not independent replications.",
        "",
        "## Pipeline controls",
        "",
        "| control | pass |",
        "| --- | :---: |",
    ]
    for name, passed in payload["pipeline_controls"].items():
        lines.append(f"| {name} | {passed} |")
    lines.extend(
        [
            "",
            "## Active histories",
            "",
            "| panel | family | branch | initial D0/R | entrance | dwell max | final D0/R | opposite min | phase mean | phase RMS error | stop | pass |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | :---: |",
        ]
    )
    for pair in payload["pairs"]:
        for branch_name in ("plus", "minus"):
            arm = pair[branch_name]
            if pair["panel"] == "prepared":
                dwell_maximum = arm["maximum_own_target_fraction"]
                final_fraction = arm["trace"][-1]["expected_d0_fraction"]
                entrance = 0
                opposite = arm["opposite_minimum_fraction"]
            else:
                dwell_maximum = arm["dwell_maximum_fraction"]
                final_fraction = arm["final_fraction"]
                entrance = arm["first_entrance_step"]
                opposite = arm["opposite_dwell_minimum_fraction"]
            lines.append(
                f"| {pair['panel']} | {pair['name']} | {branch_name} | "
                f"{_format(arm['initial_expected_d0_fraction'])} | "
                f"{_format(entrance)} | {_format(dwell_maximum)} | "
                f"{_format(final_fraction)} | {_format(opposite)} | "
                f"{_format(arm['phase']['mean_increment'])} | "
                f"{_format(arm['phase']['rms_error'])} | "
                f"{arm['stop_reason']} | {arm['pass']} |"
            )
    fifo = payload["negative_controls"]["fifo_only"]
    achiral = payload["negative_controls"]["achiral"]
    lines.extend(
        [
            "",
            "## Negative controls",
            "",
            "| control | primary diagnostic | pass |",
            "| --- | ---: | :---: |",
            (
                "| eta=0 FIFO collapse | final reduced norm/R "
                f"{_format(fifo['trace'][-1]['translation_reduced_norm_fraction'])} | "
                f"{fifo['pass']} |"
            ),
            (
                "| active achiral invariant subspace | maximum absolute y "
                f"{_format(achiral['maximum_absolute_y'])} | {achiral['pass']} |"
            ),
            "",
            "## Decision and limits",
            "",
            f"Gate components: `{json.dumps(payload['gates'], sort_keys=True)}`.",
            "",
            "A full pass concerns only the registered finite ensemble. A",
            "basin-only outcome does not establish target-blind formation and",
            "does not open P4. No outcome proves an open basin volume, generic",
            "formation, chirality selection from symmetric data, mechanics or",
            "mass.",
            "",
            "## Provenance",
            "",
            f"- freeze revision: `{payload['provenance']['freeze_revision']}`;",
            f"- execution revision: `{payload['provenance']['revision']}`;",
            f"- JSON SHA-256: `{summary_sha256}`;",
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
                "report": report.relative_to(ROOT).as_posix(),
                "summary": summary.relative_to(ROOT).as_posix(),
                "elapsed_seconds": payload["elapsed_seconds"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
