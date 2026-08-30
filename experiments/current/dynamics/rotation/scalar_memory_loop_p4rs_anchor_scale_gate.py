"""Execute the frozen P4-R-S Anchor-scale transfer gate."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from decimal import Decimal
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import re
import subprocess
import time
from typing import Any

import numpy as np

from experiments.current.dynamics.rotation import (
    scalar_memory_loop_p4r_phase_metrology_gate as p4r,
)
from emergenz_knoten.loop_center_response import memory_center as vector_memory_center
from emergenz_knoten.orbit_center_actuator import (
    OrbitCenterReadout,
    SourceWriteRoundingMetrology,
    SourceWriteStep,
    adjoint_slot_forces,
    build_orbit_center_readout,
    candidate_orbit_center_readout,
    complex_to_vector,
    memory_center,
    orbit_center,
    readout_payload,
    real_inner,
    reciprocal_source_write_step,
    source_write_rounding_metrology,
)
from emergenz_knoten.rotating_wave_formation import (
    FormationThresholds,
    phase_increment_metrics,
    target_history,
)
from emergenz_knoten.rotating_wave_stability import (
    native_fifo_step,
    rotation_matrix,
    rotation_translation_quotient_distance,
)
from emergenz_knoten.rotating_wave_stability_gate import RotatingWaveCandidate


ROOT = p4r.ROOT
PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_loop_p4rs_anchor_scale_protocol_2026-08-30.md"
)
DESIGN_AUDIT = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_loop_p4rs_anchor_scale_design_audit_2026-08-30.md"
)
READINESS_REVIEW = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_loop_p4rs_anchor_scale_implementation_readiness_2026-08-30.md"
)
P4R_RESULT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p4r_phase_metrology_2026-08-26.json"
)
P4R_REVIEW = Path(
    "reports/project/meta/reviews/"
    "scalar_memory_loop_p4r_phase_metrology_review_2026-08-27.md"
)
P4R_PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_loop_p4r_phase_metrology_protocol_2026-08-26.md"
)
HISTORICAL_P4R_RUNNER = Path(
    "experiments/current/dynamics/rotation/"
    "scalar_memory_loop_p4r_phase_metrology_gate.py"
)
P4_RESULT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p4_source_write_2026-08-26.json"
)
ANCHOR_INTERVAL_RESULT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_interval_certificate_2026-08-21.json"
)
ANCHOR_STABILITY_RESULT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_stability_2026-08-20.json"
)
SOURCE_AUDIT = Path(
    "reports/project/meta/reviews/"
    "p4_publication_source_referee_audit_2026-08-27.md"
)
SOURCE_FINDINGS = Path(
    "reports/project/meta/reviews/"
    "p4_publication_source_referee_findings_2026-08-27.json"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p4rs_anchor_scale_2026-08-30.json"
)
DEFAULT_REPORT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_loop_p4rs_anchor_scale_2026-08-30.md"
)

DESIGN_FREEZE_REVISION = "11cabd66d0ba086116b29b3ea3d8a8548560cea1"
PROTOCOL_FREEZE_REVISION = "3797c98c83ed61fa02e939583782fd7213e0b961"
EXPECTED_HEAD_BLOBS = {
    PROTOCOL.as_posix(): "e88557a77ed2937a0e65dc7880311a0804432f8b",
    DESIGN_AUDIT.as_posix(): "dec2f0c281f19fadc02412b04a78f78f0793422a",
    P4R_RESULT.as_posix(): "2a668a4c70820bceb0ff84fa1932878d9130aabf",
    P4R_REVIEW.as_posix(): "1d25e9db083d91fdfd521f44e0951a1ddd9e2c37",
    P4R_PROTOCOL.as_posix(): "b81fa535c1921c2f11f83e5585bf38b05e0a08d5",
    HISTORICAL_P4R_RUNNER.as_posix(): (
        "27a3a40dde60b797b58da576b5849ab10b47079f"
    ),
    "src/emergenz_knoten/orbit_center_actuator.py": (
        "63d31bc47291f76c65a5633f14436ccd2105fe9a"
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
    ANCHOR_INTERVAL_RESULT.as_posix(): (
        "fc6e816c6895e408693fbde176afdaee963c20b9"
    ),
    ANCHOR_STABILITY_RESULT.as_posix(): (
        "1c9d5746c9553d9cb8031b58258e6d613f1633d9"
    ),
    P4_RESULT.as_posix(): "41ddfb5ec2d4c907607995523775072ad12544f7",
    SOURCE_AUDIT.as_posix(): "273acc3a86a9f3757e853236ce386f064835194c",
    SOURCE_FINDINGS.as_posix(): (
        "9cf16689a3b8931842e6ef500f555212ac8f5b36"
    ),
}
EXPECTED_CANONICAL_SHA256 = {
    P4R_RESULT.as_posix(): (
        "807cf915d1602d87a779e7bf587387559b1b19d7de60dc43c6e1e220b73682c8"
    ),
    P4_RESULT.as_posix(): (
        "ea0651e206451e5f87ec08ab3f66ec68df2c04bee2d1b9d67219736058a275cc"
    ),
    ANCHOR_INTERVAL_RESULT.as_posix(): (
        "63dc4158c0d8a9543230b656b7602feef76a48a2a75fbe6a6e001cb81082a840"
    ),
    ANCHOR_STABILITY_RESULT.as_posix(): (
        "43b0d7f5e5ba81dc35d4a2e9d138d3663a3d98b67bcb09ed2d4572d5a01eb86f"
    ),
}
IMPLEMENTATION_PATHS = (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_loop_p4rs_anchor_scale_gate.py",
    "tests/test_rotating_wave_p4rs_anchor_scale.py",
)

CANDIDATE_ID = "k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1"
RADIUS_DECIMAL = (
    "0.946517504804223960990626662735384935160072399313332184824852189820406"
    "142783597632634323623097735558253263801"
)
THETA_DECIMAL = (
    "0.015770381717134991901268964141341323131632114098006250776592366366328"
    "4306507309780740587352166842324150748019"
)
CANDIDATE = RotatingWaveCandidate(
    candidate_id=CANDIDATE_ID,
    radius=float(RADIUS_DECIMAL),
    theta=float(THETA_DECIMAL),
    alpha=0.01,
    horizon=1200,
    memory_mass=1.0,
    eta=0.15,
    sigma_rep=1.0,
    sigma_att=3.0,
    amplitude_rep=1.0,
    amplitude_att=3.5,
)
EXPECTED_ANCHOR_STATIC = {
    "beta_real": 0.2923957083606503,
    "beta_imag": -0.45093731944942195,
    "write_real": 0.004999787409710969,
    "write_imag": 0.6340870653534046,
    "write_gain": 0.4020914043226352,
}
EXPECTED_L3_MEANS = {
    "A_C": 0.24091330892887405,
    "B_C": 0.208421577193625,
    "A_Q": 0.303296080377988,
    "B_Q": 0.15375308546516817,
}


@dataclass(frozen=True)
class P4RSThresholds:
    """Frozen Anchor panel, inherited gates and scale-transfer limits."""

    active_updates: int = 2_000
    sample_every: int = 5
    late_start: int = 1_800
    phase_start: int = 1_500
    coupling_strength: float = 0.25
    offset_fraction: float = 1.5e-3
    maximum_d0_fraction: float = 0.01
    late_d0_fraction: float = 0.002
    opposite_d0_fraction: float = 0.5
    final_separation_fraction: float = 0.10
    projection_minimum: float = 0.20
    projection_maximum: float = 0.80
    energy_ratio_maximum: float = 0.01
    phase_mean_error_fraction: float = 0.01
    phase_rms_error_fraction: float = 0.05
    step_ledger_relative: float = 5.0e-11
    cumulative_ledger_relative: float = 5.0e-9
    force_relative: float = 5.0e-12
    local_displacement_relative: float = 5.0e-12
    actuator_displacement_relative: float = 5.0e-12
    even_response_relative: float = 0.02
    signal_fraction: float = 0.25
    coefficient_tolerance: float = 5.0e-13
    center_tolerance_fraction: float = 1.0e-12
    channel_off_d0_fraction: float = 1.0e-10
    covariance_fraction: float = 1.0e-11
    scalar_null_maximum: float = 0.05
    chiral_minimum: float = 0.10
    sign_support_minimum: int = 6
    scale_tolerance: float = 0.05
    reconstruction_tolerance: float = 5.0e-15
    reference_dps: int = 80
    reference_steps: tuple[int, ...] = (1, 1_000, 2_000)


THRESHOLDS = P4RSThresholds()
PHASES = tuple((2 * index + 1) * math.pi / 8.0 for index in range(8))
ANCHOR_STEPS = tuple(
    range(0, THRESHOLDS.active_updates + 1, THRESHOLDS.sample_every)
)
L3_STEPS = tuple(2 * step for step in ANCHOR_STEPS)
MEMORY_TIMES = tuple(0.05 * index for index in range(len(ANCHOR_STEPS)))


def _git_output(arguments: list[str]) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return result.stdout.strip()


def _git_blob(path: str, *, revision: str = "HEAD") -> str:
    return _git_output(["rev-parse", f"{revision}:{path}"])


def _canonical_lf_sha256(path: Path) -> str:
    content = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(content).hexdigest()


def _is_ancestor(ancestor: str, revision: str) -> bool:
    check = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, revision],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return check.returncode == 0


def _parse_readiness_review(text: str) -> dict[str, str]:
    patterns = {
        "implementation_revision": (
            r"Implementation revision:\s*\x60([0-9a-f]{40})\x60"
        ),
        "runner_blob": r"Runner blob:\s*\x60([0-9a-f]{40})\x60",
        "test_blob": r"Test blob:\s*\x60([0-9a-f]{40})\x60",
        "ci_run": r"actions/runs/([0-9]+)",
        "verdict": r"Verdict:\s*\*\*\x60([^\x60]+)\x60\*\*",
    }
    parsed: dict[str, str] = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match is None:
            raise RuntimeError(f"readiness review lacks {key}")
        parsed[key] = match.group(1)
    if parsed["verdict"] != "p4rs-implementation-ready":
        raise RuntimeError("P4-R-S implementation readiness was not upheld")
    return parsed


def _verify_implementation_review(revision: str) -> dict[str, Any]:
    review_path = ROOT / READINESS_REVIEW
    if not review_path.exists():
        raise RuntimeError("P4-R-S readiness review is absent")
    parsed = _parse_readiness_review(review_path.read_text(encoding="utf-8"))
    implementation_revision = parsed["implementation_revision"]
    if not _is_ancestor(implementation_revision, revision):
        raise RuntimeError("reviewed implementation is not an ancestor")
    runner_blob = _git_blob(
        IMPLEMENTATION_PATHS[0], revision=implementation_revision
    )
    test_blob = _git_blob(
        IMPLEMENTATION_PATHS[1], revision=implementation_revision
    )
    if runner_blob != parsed["runner_blob"] or test_blob != parsed["test_blob"]:
        raise RuntimeError("readiness review records different implementation blobs")
    if (
        _git_blob(IMPLEMENTATION_PATHS[0]) != runner_blob
        or _git_blob(IMPLEMENTATION_PATHS[1]) != test_blob
    ):
        raise RuntimeError("reviewed P4-R-S implementation changed after review")
    review_commit = _git_output(
        ["log", "-1", "--format=%H", "--", READINESS_REVIEW.as_posix()]
    )
    if not review_commit or not _is_ancestor(review_commit, revision):
        raise RuntimeError("readiness review is not committed in execution history")
    return {
        **parsed,
        "review_path": READINESS_REVIEW.as_posix(),
        "review_blob": _git_blob(READINESS_REVIEW.as_posix()),
        "review_commit": review_commit,
    }


def _verify_provenance() -> dict[str, Any]:
    status = _git_output(["status", "--short"])
    if status:
        raise RuntimeError("P4-R-S requires a clean prospective revision")
    if (ROOT / DEFAULT_SUMMARY).exists() or (ROOT / DEFAULT_REPORT).exists():
        raise RuntimeError("registered P4-R-S output already exists")
    revision = _git_output(["rev-parse", "HEAD"])
    for ancestor in (DESIGN_FREEZE_REVISION, PROTOCOL_FREEZE_REVISION):
        if not _is_ancestor(ancestor, revision):
            raise RuntimeError(f"required freeze is not an ancestor: {ancestor}")
    observed = {path: _git_blob(path) for path in EXPECTED_HEAD_BLOBS}
    if observed != EXPECTED_HEAD_BLOBS:
        raise RuntimeError("one or more frozen P4-R-S dependencies changed")
    observed_hashes = {
        path: _canonical_lf_sha256(ROOT / path)
        for path in EXPECTED_CANONICAL_SHA256
    }
    if observed_hashes != EXPECTED_CANONICAL_SHA256:
        raise RuntimeError("one or more canonical historical hashes changed")

    p4r_result = json.loads((ROOT / P4R_RESULT).read_text(encoding="utf-8"))
    p4_result = json.loads((ROOT / P4_RESULT).read_text(encoding="utf-8"))
    interval = json.loads(
        (ROOT / ANCHOR_INTERVAL_RESULT).read_text(encoding="utf-8")
    )
    stability = json.loads(
        (ROOT / ANCHOR_STABILITY_RESULT).read_text(encoding="utf-8")
    )
    findings = json.loads(
        (ROOT / SOURCE_FINDINGS).read_text(encoding="utf-8")
    )
    source_text = (ROOT / SOURCE_AUDIT).read_text(encoding="utf-8")
    review_text = (ROOT / P4R_REVIEW).read_text(encoding="utf-8")
    decisions = {
        "p4r": p4r_result.get("decision"),
        "p4": p4_result.get("decision"),
        "interval": interval.get("decision"),
        "stability": stability.get("decision"),
        "source": findings.get("verdict"),
    }
    expected_decisions = {
        "p4r": "p4r-phase-averaged-chiral-response-pass",
        "p4": "p4-source-write-architecture-fail",
        "interval": "interval-certified-unique-root-pass",
        "stability": "numerically-stable-source-pass",
        "source": "referee-source-ready-with-major-claim-restrictions",
    }
    if decisions != expected_decisions:
        raise RuntimeError("one or more frozen prerequisite decisions changed")
    if "p4r-phase-averaged-chiral-response-pass-upheld" not in review_text:
        raise RuntimeError("P4-R review no longer upholds the stored decision")
    if (
        "P5 remains closed until P4-R-S itself returns a reviewed full pass"
        not in source_text
    ):
        raise RuntimeError("publication-source audit no longer keeps P5 closed")
    major_findings = [
        row for row in findings.get("findings", []) if row.get("severity") == "major"
    ]
    if len(major_findings) != 3:
        raise RuntimeError("publication-source major restrictions changed")

    upstream = _git_output(
        ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"]
    )
    ahead_behind = _git_output(
        ["rev-list", "--left-right", "--count", f"HEAD...{upstream}"]
    ).split()
    if ahead_behind != ["0", "0"]:
        raise RuntimeError("P4-R-S requires a fully pushed execution revision")
    readiness = _verify_implementation_review(revision)
    return {
        "clean_pre_run_status": status,
        "revision": revision,
        "design_freeze_revision": DESIGN_FREEZE_REVISION,
        "protocol_freeze_revision": PROTOCOL_FREEZE_REVISION,
        "freeze_revisions_are_ancestors": True,
        "expected_head_blobs": EXPECTED_HEAD_BLOBS,
        "observed_head_blobs": observed,
        "canonical_sha256": observed_hashes,
        "implementation_readiness": readiness,
        "implementation_blobs": {
            path: _git_blob(path) for path in IMPLEMENTATION_PATHS
        },
        "upstream": upstream,
        "upstream_synchronized": True,
        "origin": _git_output(["remote", "get-url", "origin"]),
        "decisions": decisions,
        "open_major_source_restrictions": [
            row["finding_id"] for row in major_findings
        ],
        "default_outputs_absent_at_start": True,
    }


def _expected_active_keys() -> list[tuple[int, int, int]]:
    return [
        (phase_index, chirality, offset_sign)
        for phase_index in range(8)
        for chirality in (1, -1)
        for offset_sign in (1, -1)
    ]


def _expected_channel_off_keys() -> list[tuple[int, int]]:
    return [
        (phase_index, chirality)
        for phase_index in range(8)
        for chirality in (1, -1)
    ]


def _active_key(arm: dict[str, Any]) -> tuple[int, int, int]:
    return (
        int(arm["phase_index"]),
        int(arm["chirality"]),
        int(arm["offset_sign"]),
    )


def _channel_off_key(arm: dict[str, Any]) -> tuple[int, int]:
    return int(arm["phase_index"]), int(arm["chirality"])


def _registered_panel(
    active_arms: list[dict[str, Any]],
    channel_off_arms: list[dict[str, Any]],
) -> bool:
    return bool(
        [_active_key(arm) for arm in active_arms] == _expected_active_keys()
        and [_channel_off_key(arm) for arm in channel_off_arms]
        == _expected_channel_off_keys()
    )


def _phase_history(*, chirality: int, phase_index: int) -> np.ndarray:
    base = target_history(CANDIDATE, chirality=chirality)
    return base @ rotation_matrix(PHASES[phase_index]).T


def _anchor_root_controls() -> dict[str, Any]:
    interval = json.loads(
        (ROOT / ANCHOR_INTERVAL_RESULT).read_text(encoding="utf-8")
    )
    radius = Decimal(RADIUS_DECIMAL)
    theta = Decimal(THETA_DECIMAL)
    certified = interval["certified_intersection"]
    refined = interval["panels"][-1]["refined"]
    interval_membership = {
        "radius": bool(
            Decimal(certified["radius"]["lower"])
            <= radius
            <= Decimal(certified["radius"]["upper"])
        ),
        "theta": bool(
            Decimal(certified["theta"]["lower"])
            <= theta
            <= Decimal(certified["theta"]["upper"])
        ),
    }
    refined_agreement = {
        "radius": refined["radius"] == RADIUS_DECIMAL,
        "theta": refined["theta"] == THETA_DECIMAL,
    }
    plus = candidate_orbit_center_readout(CANDIDATE, chirality=1)
    minus = candidate_orbit_center_readout(CANDIDATE, chirality=-1)
    observed_static = {
        "beta_real": plus.beta.real,
        "beta_imag": plus.beta.imag,
        "write_real": plus.coefficients[0].real,
        "write_imag": plus.coefficients[0].imag,
        "write_gain": plus.write_gain,
    }
    static_errors = {
        key: abs(observed_static[key] - expected)
        for key, expected in EXPECTED_ANCHOR_STATIC.items()
    }
    conjugacy_error = max(
        abs(minus.beta - plus.beta.conjugate()),
        float(
            np.max(
                np.abs(minus.coefficients - np.conjugate(plus.coefficients))
            )
        ),
    )
    executable_offset = THRESHOLDS.offset_fraction * CANDIDATE.radius
    gates = {
        "candidate_id": interval.get("candidate_id") == CANDIDATE_ID,
        "exact_interval_membership": all(interval_membership.values()),
        "exact_refined_root": all(refined_agreement.values()),
        "binary64_parse": bool(
            CANDIDATE.radius == float(RADIUS_DECIMAL)
            and CANDIDATE.theta == float(THETA_DECIMAL)
        ),
        "matched_h_alpha": Decimal("0.01") * Decimal(1200) == Decimal(12),
        "matched_eta_alpha": Decimal("0.15") / Decimal("0.01") == Decimal(15),
        "frozen_static_values": max(static_errors.values())
        <= THRESHOLDS.coefficient_tolerance,
        "conjugacy": conjugacy_error <= THRESHOLDS.coefficient_tolerance,
        "positive_equal_mobility": bool(
            plus.write_gain > 0.0
            and plus.write_gain == abs(complex(plus.coefficients[0])) ** 2
        ),
        "computed_offset": executable_offset == 0.0014197762572063359,
    }
    return {
        "radius_decimal": RADIUS_DECIMAL,
        "theta_decimal": THETA_DECIMAL,
        "radius_binary64": CANDIDATE.radius,
        "theta_binary64": CANDIDATE.theta,
        "certified_intersection": certified,
        "refined_root": {
            "radius": refined["radius"],
            "theta": refined["theta"],
        },
        "interval_membership": interval_membership,
        "refined_agreement": refined_agreement,
        "observed_static": observed_static,
        "expected_static": EXPECTED_ANCHOR_STATIC,
        "static_absolute_errors": static_errors,
        "conjugacy_error": conjugacy_error,
        "write_gain": plus.write_gain,
        "actuator_mobility": plus.write_gain,
        "executable_offset": executable_offset,
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _registration_controls() -> dict[str, Any]:
    mirror_errors = []
    half_turn_errors = []
    for phase_index in range(8):
        plus = _phase_history(chirality=1, phase_index=phase_index)
        minus_mate = _phase_history(
            chirality=-1,
            phase_index=7 - phase_index,
        )
        expected_mirror = plus.copy()
        expected_mirror[:, 1] *= -1.0
        mirror_errors.append(float(np.max(np.abs(minus_mate - expected_mirror))))
        half = _phase_history(
            chirality=1,
            phase_index=(phase_index + 4) % 8,
        )
        half_turn_errors.append(float(np.max(np.abs(half + plus))))
    old_phases = (0.0, math.pi / 2.0, math.pi, 3.0 * math.pi / 2.0)
    old_distance = min(
        abs(math.remainder(phase - old, 2.0 * math.pi))
        for phase in PHASES
        for old in old_phases
    )
    tolerance = THRESHOLDS.covariance_fraction * CANDIDATE.radius
    gates = {
        "eight_unique_phases": len(set(PHASES)) == 8,
        "unopened_phase_grid": old_distance > 0.0,
        "unopened_amplitude": (
            THRESHOLDS.offset_fraction not in p4r.p4.THRESHOLDS.offset_fractions
        ),
        "mirror_pairing": max(mirror_errors) <= tolerance,
        "half_turn_pairing": max(half_turn_errors) <= tolerance,
        "active_registration": len(_expected_active_keys()) == 32,
        "channel_off_registration": len(_expected_channel_off_keys()) == 16,
        "memory_time_samples": (
            len(ANCHOR_STEPS) == len(L3_STEPS) == len(MEMORY_TIMES) == 401
        ),
        "integer_step_pairing": all(
            anchor == 5 * index and l3 == 10 * index
            for index, (anchor, l3) in enumerate(
                zip(ANCHOR_STEPS, L3_STEPS, strict=True)
            )
        ),
        "memory_time_pairing": all(
            math.isclose(
                CANDIDATE.alpha * anchor,
                p4r.CANDIDATE.alpha * l3,
                rel_tol=0.0,
                abs_tol=1.0e-15,
            )
            for anchor, l3 in zip(ANCHOR_STEPS, L3_STEPS, strict=True)
        ),
    }
    return {
        "phases": list(PHASES),
        "active_order": [list(key) for key in _expected_active_keys()],
        "channel_off_order": [
            list(key) for key in _expected_channel_off_keys()
        ],
        "anchor_steps": list(ANCHOR_STEPS),
        "l3_steps": list(L3_STEPS),
        "memory_times": list(MEMORY_TIMES),
        "minimum_old_phase_distance": old_distance,
        "maximum_mirror_history_error": max(mirror_errors),
        "maximum_half_turn_history_error": max(half_turn_errors),
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _small_h_algebraic_control() -> dict[str, Any]:
    readout = build_orbit_center_readout(
        alpha=0.08,
        horizon=17,
        theta=0.19,
        chirality=1,
    )
    rng = np.random.default_rng(20260830)
    variation = rng.normal(size=(17, 2))
    center_force_vector = np.asarray([0.17, -0.31])
    slot_forces = adjoint_slot_forces(center_force_vector, readout=readout)
    center_variation = orbit_center(variation, readout=readout)
    virtual_work_error = abs(
        float(np.sum(slot_forces * variation))
        - real_inner(complex(*center_force_vector), center_variation)
    )
    force_sum_error = float(
        np.linalg.norm(np.sum(slot_forces, axis=0) - center_force_vector)
    )

    ages = np.arange(17)
    old = np.column_stack(
        (
            0.1 * ages + np.sin(0.37 * ages),
            -0.05 * ages + np.cos(0.23 * ages),
        )
    )
    old_values = old[:, 0] + 1j * old[:, 1]
    new_values = np.concatenate(([complex(0.7, -0.4)], old_values[:-1]))
    force = complex(0.3, -0.2)
    write_force = readout.coefficients[0].conjugate() * force
    write_work = real_inner(write_force, new_values[0] - old_values[0])
    age_displacement = complex(
        np.dot(
            readout.coefficients[1:],
            old_values[:-1] - old_values[1:],
        )
    )
    age_work = real_inner(force, age_displacement)
    center_work = real_inner(
        force,
        complex(np.dot(readout.coefficients, new_values - old_values)),
    )
    full_work_error = abs(write_work + age_work - center_work)
    truncated_fraction = abs(age_work) / max(
        abs(center_work),
        abs(write_work) + abs(age_work),
    )
    gates = {
        "adjoint_virtual_work": virtual_work_error
        <= THRESHOLDS.coefficient_tolerance,
        "adjoint_force_sum": force_sum_error
        <= THRESHOLDS.coefficient_tolerance,
        "full_age_ledger": full_work_error
        <= THRESHOLDS.coefficient_tolerance,
        "age_omission_nontrivial": truncated_fraction >= 0.01,
    }
    return {
        "virtual_work_error": virtual_work_error,
        "force_sum_error": force_sum_error,
        "write_work": write_work,
        "age_work": age_work,
        "center_work": center_work,
        "full_work_error": full_work_error,
        "truncated_ledger_fraction": truncated_fraction,
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _construction_controls() -> dict[str, Any]:
    plus = candidate_orbit_center_readout(CANDIDATE, chirality=1)
    minus = candidate_orbit_center_readout(CANDIDATE, chirality=-1)
    target_plus = target_history(CANDIDATE, chirality=1)
    target_minus = target_history(CANDIDATE, chirality=-1)
    ages = np.arange(CANDIDATE.horizon, dtype=float)
    notch_plus = complex(
        np.dot(plus.coefficients, np.exp(-1j * CANDIDATE.theta * ages))
    )
    values = {
        "q_power_h": (1.0 - CANDIDATE.alpha) ** CANDIDATE.horizon,
        "weight_zero": float(plus.weights[0]),
        "beta_real": plus.beta.real,
        "beta_imag": plus.beta.imag,
        "beta_abs": abs(plus.beta),
        "write_real": plus.coefficients[0].real,
        "write_imag": plus.coefficients[0].imag,
        "write_gain": plus.write_gain,
        "raw_center_amplitude": abs(memory_center(target_plus, readout=plus)),
        "wrong_chirality_amplitude": abs(
            orbit_center(target_plus, readout=minus)
        ),
    }
    static_errors = {
        key: abs(values[key] - expected)
        for key, expected in EXPECTED_ANCHOR_STATIC.items()
    }
    coefficient = {
        "sum_error_plus": abs(complex(np.sum(plus.coefficients)) - 1.0),
        "sum_error_minus": abs(complex(np.sum(minus.coefficients)) - 1.0),
        "notch_error_plus": abs(notch_plus),
        "conjugacy_error": max(
            abs(minus.beta - plus.beta.conjugate()),
            float(
                np.max(
                    np.abs(
                        minus.coefficients - np.conjugate(plus.coefficients)
                    )
                )
            ),
        ),
    }
    translation = np.asarray([0.37, -0.21])
    phase = rotation_matrix(math.pi / 7.0)
    transformed = target_plus @ phase.T + translation
    translated_center = orbit_center(transformed, readout=plus)
    target_centers = {
        "plus": abs(orbit_center(target_plus, readout=plus)),
        "minus": abs(orbit_center(target_minus, readout=minus)),
        "translated_error": float(
            np.linalg.norm(complex_to_vector(translated_center) - translation)
        ),
    }
    small_h = _small_h_algebraic_control()

    q0 = np.asarray([1.0e-3 * CANDIDATE.radius, 0.0])
    off = reciprocal_source_write_step(
        target_plus,
        q0,
        candidate=CANDIDATE,
        readout=plus,
        coupling_strength=0.0,
    )
    native = native_fifo_step(target_plus, **CANDIDATE.step_parameters())
    bitwise_off = bool(np.array_equal(off.history, native))
    active = reciprocal_source_write_step(
        target_plus,
        q0,
        candidate=CANDIDATE,
        readout=plus,
        coupling_strength=THRESHOLDS.coupling_strength,
    )
    shift = np.asarray([0.31, -0.27])
    shifted = reciprocal_source_write_step(
        target_plus + shift,
        q0 + shift,
        candidate=CANDIDATE,
        readout=plus,
        coupling_strength=THRESHOLDS.coupling_strength,
    )
    translation_error = max(
        float(np.max(np.abs(shifted.history - active.history - shift))),
        float(np.max(np.abs(shifted.actuator - active.actuator - shift))),
    )
    rotation = rotation_matrix(0.61)
    rotated = reciprocal_source_write_step(
        target_plus @ rotation.T,
        rotation @ q0,
        candidate=CANDIDATE,
        readout=plus,
        coupling_strength=THRESHOLDS.coupling_strength,
    )
    rotation_error = max(
        float(np.max(np.abs(rotated.history - active.history @ rotation.T))),
        float(np.max(np.abs(rotated.actuator - rotation @ active.actuator))),
    )
    reflected = reciprocal_source_write_step(
        target_minus,
        q0 * np.asarray([1.0, -1.0]),
        candidate=CANDIDATE,
        readout=minus,
        coupling_strength=THRESHOLDS.coupling_strength,
    )
    expected_reflection = active.history.copy()
    expected_reflection[:, 1] *= -1.0
    reflection_error = max(
        float(np.max(np.abs(reflected.history - expected_reflection))),
        float(
            np.max(
                np.abs(
                    reflected.actuator
                    - active.actuator * np.asarray([1.0, -1.0])
                )
            )
        ),
    )
    coefficient_limit = THRESHOLDS.coefficient_tolerance
    center_limit = THRESHOLDS.center_tolerance_fraction * CANDIDATE.radius
    covariance_limit = THRESHOLDS.covariance_fraction * CANDIDATE.radius
    gates = {
        "frozen_static_values": max(static_errors.values()) <= coefficient_limit,
        "coefficient_identities": max(coefficient.values()) <= coefficient_limit,
        "target_centers": max(target_centers.values()) <= center_limit,
        "raw_center_nonzero": values["raw_center_amplitude"]
        >= 0.5 * CANDIDATE.radius,
        "wrong_chirality_negative": values["wrong_chirality_amplitude"]
        >= 0.5 * CANDIDATE.radius,
        "small_h_algebra": small_h["pass"],
        "channel_off_bitwise": bitwise_off,
        "translation_covariance": translation_error <= covariance_limit,
        "rotation_covariance": rotation_error <= covariance_limit,
        "reflection_covariance": reflection_error <= covariance_limit,
    }
    return {
        "readouts": {
            "plus": readout_payload(plus),
            "minus": readout_payload(minus),
        },
        "values": values,
        "expected_static": EXPECTED_ANCHOR_STATIC,
        "static_absolute_errors": static_errors,
        "coefficient_controls": coefficient,
        "target_center_controls": target_centers,
        "small_h_algebraic_control": small_h,
        "covariance_controls": {
            "translation_error": translation_error,
            "rotation_error": rotation_error,
            "reflection_error": reflection_error,
        },
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _sample_metrics(
    state: np.ndarray,
    actuator: np.ndarray,
    *,
    step: int,
    chirality: int,
    readout: OrbitCenterReadout,
    targets: dict[int, np.ndarray],
    coupling_strength: float,
) -> dict[str, Any]:
    own, alignment = rotation_translation_quotient_distance(
        state,
        targets[chirality],
        alpha=CANDIDATE.alpha,
        memory_mass=CANDIDATE.memory_mass,
    )
    opposite, _ = rotation_translation_quotient_distance(
        state,
        targets[-chirality],
        alpha=CANDIDATE.alpha,
        memory_mass=CANDIDATE.memory_mass,
    )
    center = orbit_center(state, readout=readout)
    raw = vector_memory_center(
        state,
        alpha=CANDIDATE.alpha,
        memory_mass=CANDIDATE.memory_mass,
    )
    q_value = complex(float(actuator[0]), float(actuator[1]))
    return {
        "step": int(step),
        "center": p4r.p4._complex_pair(center),
        "actuator": p4r.p4._complex_pair(q_value),
        "separation": abs(center - q_value),
        "expected_d0_fraction": own / CANDIDATE.radius,
        "opposite_d0_fraction": opposite / CANDIDATE.radius,
        "alignment_phase": alignment,
        "raw_memory_center": [float(raw[0]), float(raw[1])],
        "interaction_energy": (
            0.5 * coupling_strength * abs(center - q_value) ** 2
        ),
    }


def _high_precision_reference(
    step: SourceWriteStep,
    metrology: SourceWriteRoundingMetrology,
    *,
    readout: OrbitCenterReadout,
    update: int,
) -> dict[str, Any]:
    """Replay one stored transition with the reviewed exact-ratio routine."""

    return p4r._high_precision_reference(
        step,
        metrology,
        readout=readout,
        update=update,
    )


def _run_anchor_channel_off(
    *,
    phase_index: int,
    chirality: int,
) -> dict[str, Any]:
    """Advance one registered Anchor channel-off trajectory."""

    readout = candidate_orbit_center_readout(CANDIDATE, chirality=chirality)
    state = _phase_history(chirality=chirality, phase_index=phase_index)
    actuator = np.zeros(2)
    targets = {
        sign: target_history(CANDIDATE, chirality=sign) for sign in (1, -1)
    }
    trace = [
        _sample_metrics(
            state,
            actuator,
            step=0,
            chirality=chirality,
            readout=readout,
            targets=targets,
            coupling_strength=0.0,
        )
    ]
    bitwise = True
    finite = True
    for update in range(1, THRESHOLDS.active_updates + 1):
        expected = native_fifo_step(state, **CANDIDATE.step_parameters())
        result = reciprocal_source_write_step(
            state,
            actuator,
            candidate=CANDIDATE,
            readout=readout,
            coupling_strength=0.0,
        )
        finite = bool(finite and p4r.p4._all_finite(result))
        if not finite:
            break
        bitwise = bool(bitwise and np.array_equal(result.history, expected))
        state = result.history
        actuator = result.actuator
        if update % THRESHOLDS.sample_every == 0:
            sample = _sample_metrics(
                state,
                actuator,
                step=update,
                chirality=chirality,
                readout=readout,
                targets=targets,
                coupling_strength=0.0,
            )
            finite = bool(finite and p4r.p4._all_finite(sample))
            if not finite:
                break
            trace.append(sample)
    maximum_d0 = max(row["expected_d0_fraction"] for row in trace)
    maximum_center = max(
        abs(complex(*row["center"])) / CANDIDATE.radius for row in trace
    )
    gates = {
        "complete": trace[-1]["step"] == THRESHOLDS.active_updates,
        "finite": finite,
        "bitwise_native": bitwise,
        "prepared_orbit": maximum_d0
        <= THRESHOLDS.channel_off_d0_fraction,
        "stationary_orbit_center": maximum_center
        <= THRESHOLDS.channel_off_d0_fraction,
    }
    return {
        "name": f"phase-{phase_index}-s{chirality:+d}-channel-off",
        "phase_index": phase_index,
        "phase": PHASES[phase_index],
        "chirality": chirality,
        "trace": trace,
        "maximum_d0_fraction": maximum_d0,
        "maximum_center_fraction": maximum_center,
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _run_anchor_active_arm(
    *,
    phase_index: int,
    chirality: int,
    offset_sign: int,
    baseline: dict[str, Any],
) -> dict[str, Any]:
    """Advance one registered active Anchor trajectory."""

    readout = candidate_orbit_center_readout(CANDIDATE, chirality=chirality)
    state = _phase_history(chirality=chirality, phase_index=phase_index)
    delta = THRESHOLDS.offset_fraction * CANDIDATE.radius
    signed_direction = complex(float(offset_sign), 0.0)
    actuator = complex_to_vector(delta * signed_direction)
    targets = {
        sign: target_history(CANDIDATE, chirality=sign) for sign in (1, -1)
    }
    trace = [
        _sample_metrics(
            state,
            actuator,
            step=0,
            chirality=chirality,
            readout=readout,
            targets=targets,
            coupling_strength=THRESHOLDS.coupling_strength,
        )
    ]
    initial_energy = 0.5 * THRESHOLDS.coupling_strength * delta**2
    initial_force_scale: float | None = None
    initial_displacement_scale: float | None = None
    maxima = {
        "work_split": 0.0,
        "ledger": 0.0,
        "force_balance": 0.0,
        "midpoint": 0.0,
        "center_local": 0.0,
        "coupling_local": 0.0,
        "center_full": 0.0,
        "coupling_full": 0.0,
        "actuator_full": 0.0,
        "center_envelope_ratio": 0.0,
        "coupling_envelope_ratio": 0.0,
        "actuator_envelope_ratio": 0.0,
        "truncated_ledger": 0.0,
        "raw_center_ledger": 0.0,
    }
    minimum_margins = {
        "center_full": math.inf,
        "coupling_full": math.inf,
        "actuator_full": math.inf,
    }
    cumulative = {
        "work_split": 0.0,
        "ledger": 0.0,
        "write_work": 0.0,
        "age_work": 0.0,
        "center_work": 0.0,
        "raw_center_work": 0.0,
        "external_work": 0.0,
        "truncated_ledger": 0.0,
        "raw_center_ledger": 0.0,
        "write_dissipation": 0.0,
        "external_dissipation": 0.0,
    }
    minimum_dissipation = math.inf
    normal_operands = True
    finite = True
    complete = True
    stop_reason = "completed"
    reference_checks: list[dict[str, Any]] = []
    for update in range(1, THRESHOLDS.active_updates + 1):
        result = reciprocal_source_write_step(
            state,
            actuator,
            candidate=CANDIDATE,
            readout=readout,
            coupling_strength=THRESHOLDS.coupling_strength,
        )
        if not p4r.p4._all_finite(result):
            finite = False
            complete = False
            stop_reason = "nonfinite-transition"
            break
        metrology = source_write_rounding_metrology(result, readout=readout)
        if not p4r.p4._all_finite(metrology):
            finite = False
            complete = False
            stop_reason = "nonfinite-metrology"
            break
        normal_operands = bool(normal_operands and metrology.normal_operands)
        if initial_force_scale is None:
            initial_force_scale = abs(result.center_force)
            initial_displacement_scale = (
                CANDIDATE.alpha * readout.write_gain * initial_force_scale
            )

        maxima["work_split"] = max(
            maxima["work_split"], abs(result.work_split_residual)
        )
        maxima["ledger"] = max(maxima["ledger"], abs(result.ledger_residual))
        maxima["force_balance"] = max(
            maxima["force_balance"], abs(result.force_balance_residual)
        )
        maxima["midpoint"] = max(
            maxima["midpoint"], abs(result.midpoint_force_residual)
        )
        maxima["center_local"] = max(
            maxima["center_local"], abs(metrology.center_local_residual)
        )
        maxima["coupling_local"] = max(
            maxima["coupling_local"], abs(metrology.coupling_local_residual)
        )
        maxima["center_full"] = max(
            maxima["center_full"], abs(metrology.center_full_residual)
        )
        maxima["coupling_full"] = max(
            maxima["coupling_full"], abs(metrology.coupling_full_residual)
        )
        maxima["actuator_full"] = max(
            maxima["actuator_full"], abs(metrology.actuator_full_residual)
        )
        center_ratio = abs(metrology.center_full_residual) / max(
            metrology.center_full_envelope,
            np.finfo(float).tiny,
        )
        coupling_ratio = abs(metrology.coupling_full_residual) / max(
            metrology.coupling_full_envelope,
            np.finfo(float).tiny,
        )
        actuator_ratio = abs(metrology.actuator_full_residual) / max(
            metrology.actuator_full_envelope,
            np.finfo(float).tiny,
        )
        maxima["center_envelope_ratio"] = max(
            maxima["center_envelope_ratio"], center_ratio
        )
        maxima["coupling_envelope_ratio"] = max(
            maxima["coupling_envelope_ratio"], coupling_ratio
        )
        maxima["actuator_envelope_ratio"] = max(
            maxima["actuator_envelope_ratio"], actuator_ratio
        )
        minimum_margins["center_full"] = min(
            minimum_margins["center_full"],
            metrology.center_full_envelope
            - abs(metrology.center_full_residual),
        )
        minimum_margins["coupling_full"] = min(
            minimum_margins["coupling_full"],
            metrology.coupling_full_envelope
            - abs(metrology.coupling_full_residual),
        )
        minimum_margins["actuator_full"] = min(
            minimum_margins["actuator_full"],
            metrology.actuator_full_envelope
            - abs(metrology.actuator_full_residual),
        )
        maxima["truncated_ledger"] = max(
            maxima["truncated_ledger"],
            abs(result.truncated_ledger_residual),
        )
        maxima["raw_center_ledger"] = max(
            maxima["raw_center_ledger"],
            abs(result.raw_center_ledger_residual),
        )

        cumulative["work_split"] += result.work_split_residual
        cumulative["ledger"] += result.ledger_residual
        cumulative["write_work"] += result.write_work
        cumulative["age_work"] += result.age_work
        cumulative["center_work"] += result.center_work
        cumulative["raw_center_work"] += result.raw_center_work
        cumulative["external_work"] += result.external_work
        cumulative["truncated_ledger"] += result.truncated_ledger_residual
        cumulative["raw_center_ledger"] += result.raw_center_ledger_residual
        cumulative["write_dissipation"] += result.write_mobility_dissipation
        cumulative["external_dissipation"] += (
            result.external_mobility_dissipation
        )
        minimum_dissipation = min(
            minimum_dissipation,
            result.write_mobility_dissipation,
            result.external_mobility_dissipation,
        )
        if update in THRESHOLDS.reference_steps:
            reference_checks.append(
                _high_precision_reference(
                    result,
                    metrology,
                    readout=readout,
                    update=update,
                )
            )
        state = result.history
        actuator = result.actuator
        if update % THRESHOLDS.sample_every == 0:
            sample = _sample_metrics(
                state,
                actuator,
                step=update,
                chirality=chirality,
                readout=readout,
                targets=targets,
                coupling_strength=THRESHOLDS.coupling_strength,
            )
            if not p4r.p4._all_finite(sample):
                finite = False
                complete = False
                stop_reason = "nonfinite-sample"
                break
            trace.append(sample)

    if initial_force_scale is None or initial_displacement_scale is None:
        initial_force_scale = 0.0
        initial_displacement_scale = 0.0
    baseline_by_step = {row["step"]: row for row in baseline["trace"]}
    response_trace = []
    for row in trace:
        control = baseline_by_step[row["step"]]
        response_trace.append(
            {
                "step": row["step"],
                "center": p4r.p4._complex_pair(
                    complex(*row["center"]) - complex(*control["center"])
                ),
                "actuator": p4r.p4._complex_pair(
                    complex(*row["actuator"])
                    - complex(*control["actuator"])
                ),
            }
        )
    final = trace[-1]
    final_response = response_trace[-1]
    final_center = complex(*final["center"])
    final_actuator = complex(*final["actuator"])
    response_center = complex(*final_response["center"])
    response_actuator = complex(*final_response["actuator"])
    final_separation_ratio = abs(final_center - final_actuator) / delta
    center_projection = real_inner(signed_direction, response_center) / delta
    actuator_projection = (
        real_inner(signed_direction, response_actuator) / delta
    )
    energy_ratio = final["interaction_energy"] / initial_energy
    late = [row for row in trace if row["step"] >= THRESHOLDS.late_start]
    late_maximum_d0 = (
        max(row["expected_d0_fraction"] for row in late) if late else None
    )
    late_opposite_minimum = (
        min(row["opposite_d0_fraction"] for row in late) if late else None
    )
    phase_thresholds = FormationThresholds(
        active_updates=THRESHOLDS.active_updates,
        sample_every=THRESHOLDS.sample_every,
        phase_start=THRESHOLDS.phase_start,
    )
    phase = phase_increment_metrics(
        trace,
        chirality=chirality,
        candidate=CANDIDATE,
        thresholds=phase_thresholds,
    )
    maximum_center_response = max(
        abs(complex(*row["center"])) for row in response_trace
    ) / delta
    force_scale = max(initial_force_scale, np.finfo(float).tiny)
    displacement_scale = max(
        initial_displacement_scale, np.finfo(float).tiny
    )
    reference_pass = bool(
        len(reference_checks) == len(THRESHOLDS.reference_steps)
        and all(row["pass"] for row in reference_checks)
    )
    ledger_gates = {
        "work_split_step": maxima["work_split"] / initial_energy
        <= THRESHOLDS.step_ledger_relative,
        "total_ledger_step": maxima["ledger"] / initial_energy
        <= THRESHOLDS.step_ledger_relative,
        "work_split_cumulative": abs(cumulative["work_split"]) / initial_energy
        <= THRESHOLDS.cumulative_ledger_relative,
        "total_ledger_cumulative": abs(cumulative["ledger"]) / initial_energy
        <= THRESHOLDS.cumulative_ledger_relative,
        "force_balance": maxima["force_balance"] / force_scale
        <= THRESHOLDS.force_relative,
        "midpoint_force": maxima["midpoint"] / force_scale
        <= THRESHOLDS.force_relative,
        "center_local": maxima["center_local"] / displacement_scale
        <= THRESHOLDS.local_displacement_relative,
        "coupling_local": maxima["coupling_local"] / displacement_scale
        <= THRESHOLDS.local_displacement_relative,
        "center_full_envelope": (
            maxima["center_envelope_ratio"] <= 1.0
            and minimum_margins["center_full"] >= 0.0
        ),
        "coupling_full_envelope": (
            maxima["coupling_envelope_ratio"] <= 1.0
            and minimum_margins["coupling_full"] >= 0.0
        ),
        "actuator_update_relative": maxima["actuator_full"]
        / displacement_scale
        <= THRESHOLDS.actuator_displacement_relative,
        "actuator_update_envelope": (
            maxima["actuator_envelope_ratio"] <= 1.0
            and minimum_margins["actuator_full"] >= 0.0
        ),
        "high_precision_reference": reference_pass,
        "nonnegative_mobility": (
            math.isfinite(minimum_dissipation)
            and minimum_dissipation >= -1.0e-30
        ),
    }
    dynamic_gates = {
        "maximum_d0": max(row["expected_d0_fraction"] for row in trace)
        <= THRESHOLDS.maximum_d0_fraction,
        "late_d0": (
            late_maximum_d0 is not None
            and late_maximum_d0 <= THRESHOLDS.late_d0_fraction
        ),
        "opposite_chirality": (
            late_opposite_minimum is not None
            and late_opposite_minimum >= THRESHOLDS.opposite_d0_fraction
        ),
        "final_separation": final_separation_ratio
        <= THRESHOLDS.final_separation_fraction,
        "center_projection": THRESHOLDS.projection_minimum
        <= center_projection
        <= THRESHOLDS.projection_maximum,
        "actuator_projection": THRESHOLDS.projection_minimum
        <= actuator_projection
        <= THRESHOLDS.projection_maximum,
        "interaction_energy": energy_ratio
        <= THRESHOLDS.energy_ratio_maximum,
        "phase": bool(phase["pass"]),
        "informative_signal": maximum_center_response
        >= THRESHOLDS.signal_fraction,
    }
    validity_gates = {
        "complete": (
            complete and trace[-1]["step"] == THRESHOLDS.active_updates
        ),
        "finite": finite,
        "normal_operands": normal_operands,
    }
    return {
        "name": f"phase-{phase_index}-s{chirality:+d}-q{offset_sign:+d}",
        "phase_index": phase_index,
        "phase": PHASES[phase_index],
        "chirality": chirality,
        "offset_sign": offset_sign,
        "offset_fraction": THRESHOLDS.offset_fraction,
        "offset": delta,
        "stop_reason": stop_reason,
        "trace": trace,
        "response_trace": response_trace,
        "residual_scales": {
            "initial_energy": initial_energy,
            "initial_force": initial_force_scale,
            "initial_coupling_displacement": initial_displacement_scale,
        },
        "residual_maxima": maxima,
        "minimum_envelope_margins": minimum_margins,
        "cumulative_work": cumulative,
        "minimum_mobility_dissipation": minimum_dissipation,
        "high_precision_references": reference_checks,
        "maximum_d0_fraction": max(
            row["expected_d0_fraction"] for row in trace
        ),
        "late_maximum_d0_fraction": late_maximum_d0,
        "late_opposite_minimum_fraction": late_opposite_minimum,
        "final_separation_ratio": final_separation_ratio,
        "center_projection_ratio": center_projection,
        "actuator_projection_ratio": actuator_projection,
        "energy_ratio": energy_ratio,
        "maximum_center_response_ratio": maximum_center_response,
        "phase_metrics": phase,
        "validity_gates": validity_gates,
        "ledger_gates": ledger_gates,
        "dynamic_gates": dynamic_gates,
        "valid": bool(all(validity_gates.values())),
        "ledger_pass": bool(all(ledger_gates.values())),
        "dynamic_pass": bool(all(dynamic_gates.values())),
        "nondecisional_rivals": {
            "truncated_age_ledger": {
                "maximum_residual": maxima["truncated_ledger"],
                "cumulative_residual": cumulative["truncated_ledger"],
            },
            "raw_memory_center_ledger": {
                "maximum_residual": maxima["raw_center_ledger"],
                "cumulative_residual": cumulative["raw_center_ledger"],
            },
        },
    }


def _trace_complex(arm: dict[str, Any], component: str) -> np.ndarray:
    return np.asarray(
        [complex(*row[component]) for row in arm["trace"]],
        dtype=np.complex128,
    )


def _rms(values: np.ndarray) -> float:
    array = np.asarray(values, dtype=float)
    return float(math.sqrt(float(np.mean(array**2))))


def _unavailable_response(reason: str) -> dict[str, Any]:
    gates = {
        "registered_complete_finite_panel": False,
        "odd_signal_resolved": False,
        "even_response": False,
        "mirror_equivariance": False,
        "half_turn_equivariance": False,
    }
    return {
        "available": False,
        "reason": reason,
        "steps": [],
        "memory_times": [],
        "even_response": [],
        "mirror_equivariance": [],
        "half_turn_equivariance": [],
        "phase_chirality_response": [],
        "phase_profiles": [],
        "means": {key: None for key in EXPECTED_L3_MEANS},
        "positive_phase_support": {"center": 0, "actuator": 0},
        "gates": gates,
        "pass": False,
    }


def _response_controls(
    active_arms: list[dict[str, Any]],
    channel_off_arms: list[dict[str, Any]],
    *,
    radius: float,
    delta: float,
    expected_steps: tuple[int, ...],
    alpha: float,
) -> dict[str, Any]:
    if not _registered_panel(active_arms, channel_off_arms):
        return _unavailable_response("misregistered-panel")
    all_arms = [*active_arms, *channel_off_arms]
    if any(
        tuple(row["step"] for row in arm["trace"]) != expected_steps
        or not p4r.p4._all_finite(arm["trace"])
        for arm in all_arms
    ):
        return _unavailable_response("incomplete-or-nonfinite-traces")
    if any(
        float(arm.get("phase", PHASES[int(arm["phase_index"])]))
        != PHASES[int(arm["phase_index"])]
        for arm in all_arms
    ):
        return _unavailable_response("phase-registration-mismatch")

    active = {_active_key(arm): arm for arm in active_arms}
    controls = {
        _channel_off_key(arm): arm for arm in channel_off_arms
    }
    responses: dict[tuple[int, int, int, str], np.ndarray] = {}
    for phase_index, chirality, offset_sign in _expected_active_keys():
        arm = active[(phase_index, chirality, offset_sign)]
        baseline = controls[(phase_index, chirality)]
        for component in ("center", "actuator"):
            responses[
                (phase_index, chirality, offset_sign, component)
            ] = _trace_complex(arm, component) - _trace_complex(
                baseline, component
            )

    even_rows: list[dict[str, Any]] = []
    response_rows: list[dict[str, Any]] = []
    response_index: dict[tuple[int, int], dict[str, Any]] = {}
    for phase_index in range(8):
        for chirality in (1, -1):
            row: dict[str, Any] = {
                "phase_index": phase_index,
                "phase": PHASES[phase_index],
                "chirality": chirality,
            }
            even_row: dict[str, Any] = {
                "phase_index": phase_index,
                "chirality": chirality,
            }
            component_passes = []
            for component in ("center", "actuator"):
                plus = responses[(phase_index, chirality, 1, component)]
                minus = responses[(phase_index, chirality, -1, component)]
                odd = (plus - minus) / (2.0 * delta)
                even = (plus + minus) / (2.0 * delta)
                odd_rms = float(
                    math.sqrt(float(np.mean(np.abs(odd) ** 2)))
                )
                even_rms = float(
                    math.sqrt(float(np.mean(np.abs(even) ** 2)))
                )
                resolved = bool(math.isfinite(odd_rms) and odd_rms > 0.0)
                ratio = even_rms / odd_rms if resolved else None
                passed = bool(
                    resolved
                    and ratio is not None
                    and math.isfinite(ratio)
                    and ratio <= THRESHOLDS.even_response_relative
                )
                a_trace = np.asarray(odd.real, dtype=float)
                b_trace = np.asarray(-chirality * odd.imag, dtype=float)
                row[f"{component}_odd_final"] = p4r.p4._complex_pair(
                    complex(odd[-1])
                )
                row[f"{component}_A_trace"] = a_trace.tolist()
                row[f"{component}_B_trace"] = b_trace.tolist()
                row[f"{component}_A_final"] = float(a_trace[-1])
                row[f"{component}_B_final"] = float(b_trace[-1])
                even_row[f"{component}_odd_rms"] = odd_rms
                even_row[f"{component}_even_rms"] = even_rms
                even_row[f"{component}_even_to_odd_rms"] = ratio
                even_row[f"{component}_odd_resolved"] = resolved
                component_passes.append(passed)
            even_row["pass"] = bool(all(component_passes))
            even_rows.append(even_row)
            response_rows.append(row)
            response_index[(phase_index, chirality)] = row

    mirror_rows = []
    for phase_index in range(8):
        for offset_sign in (1, -1):
            plus = active[(phase_index, 1, offset_sign)]
            minus = active[(7 - phase_index, -1, offset_sign)]
            center_error = float(
                np.max(
                    np.abs(
                        _trace_complex(minus, "center")
                        - np.conjugate(_trace_complex(plus, "center"))
                    )
                )
                / radius
            )
            actuator_error = float(
                np.max(
                    np.abs(
                        _trace_complex(minus, "actuator")
                        - np.conjugate(_trace_complex(plus, "actuator"))
                    )
                )
                / radius
            )
            mirror_rows.append(
                {
                    "plus_phase_index": phase_index,
                    "minus_phase_index": 7 - phase_index,
                    "offset_sign": offset_sign,
                    "center_error_fraction": center_error,
                    "actuator_error_fraction": actuator_error,
                    "pass": max(center_error, actuator_error)
                    <= THRESHOLDS.covariance_fraction,
                }
            )

    half_turn_rows = []
    for phase_index in range(4):
        for chirality in (1, -1):
            for offset_sign in (1, -1):
                first = active[(phase_index, chirality, offset_sign)]
                second = active[
                    (phase_index + 4, chirality, -offset_sign)
                ]
                center_error = float(
                    np.max(
                        np.abs(
                            _trace_complex(second, "center")
                            + _trace_complex(first, "center")
                        )
                    )
                    / radius
                )
                actuator_error = float(
                    np.max(
                        np.abs(
                            _trace_complex(second, "actuator")
                            + _trace_complex(first, "actuator")
                        )
                    )
                    / radius
                )
                half_turn_rows.append(
                    {
                        "phase_index": phase_index,
                        "mate_phase_index": phase_index + 4,
                        "chirality": chirality,
                        "offset_sign": offset_sign,
                        "mate_offset_sign": -offset_sign,
                        "center_error_fraction": center_error,
                        "actuator_error_fraction": actuator_error,
                        "pass": max(center_error, actuator_error)
                        <= THRESHOLDS.covariance_fraction,
                    }
                )

    profiles = []
    for phase_index in range(8):
        plus = response_index[(phase_index, 1)]
        minus = response_index[(phase_index, -1)]
        profiles.append(
            {
                "phase_index": phase_index,
                "phase": PHASES[phase_index],
                "A_C": 0.5
                * (plus["center_A_final"] + minus["center_A_final"]),
                "B_C": 0.5
                * (plus["center_B_final"] + minus["center_B_final"]),
                "A_Q": 0.5
                * (plus["actuator_A_final"] + minus["actuator_A_final"]),
                "B_Q": 0.5
                * (plus["actuator_B_final"] + minus["actuator_B_final"]),
            }
        )
    means = {
        key: math.fsum(row[key] for row in profiles) / len(profiles)
        for key in EXPECTED_L3_MEANS
    }
    support = {
        "center": sum(row["B_C"] > 0.0 for row in profiles),
        "actuator": sum(row["B_Q"] > 0.0 for row in profiles),
    }
    gates = {
        "registered_complete_finite_panel": True,
        "odd_signal_resolved": all(
            row["center_odd_resolved"] and row["actuator_odd_resolved"]
            for row in even_rows
        ),
        "even_response": all(row["pass"] for row in even_rows),
        "mirror_equivariance": all(row["pass"] for row in mirror_rows),
        "half_turn_equivariance": all(
            row["pass"] for row in half_turn_rows
        ),
    }
    return {
        "available": True,
        "reason": None,
        "steps": list(expected_steps),
        "memory_times": [alpha * step for step in expected_steps],
        "even_response": even_rows,
        "mirror_equivariance": mirror_rows,
        "half_turn_equivariance": half_turn_rows,
        "phase_chirality_response": response_rows,
        "phase_profiles": profiles,
        "means": means,
        "phase_averaged_transverse_response": {
            "center": means["B_C"],
            "actuator": means["B_Q"],
        },
        "positive_phase_support": support,
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _load_l3_reference() -> dict[str, Any]:
    payload = json.loads((ROOT / P4R_RESULT).read_text(encoding="utf-8"))
    active_arms = payload.get("active_arms", [])
    channel_off_arms = payload.get("channel_off_arms", [])
    delta = THRESHOLDS.offset_fraction * p4r.CANDIDATE.radius
    response = _response_controls(
        active_arms,
        channel_off_arms,
        radius=p4r.CANDIDATE.radius,
        delta=delta,
        expected_steps=L3_STEPS,
        alpha=p4r.CANDIDATE.alpha,
    )

    stored = payload.get("response_controls", {})
    stored_rows = {
        (int(row["phase_index"]), int(row["chirality"])): row
        for row in stored.get("phase_chirality_response", [])
    }
    stored_profiles = {
        int(row["phase_index"]): row
        for row in stored.get("phase_averages", [])
    }
    row_errors = []
    for row in response.get("phase_chirality_response", []):
        old = stored_rows.get((row["phase_index"], row["chirality"]))
        if old is None:
            row_errors.append(math.inf)
            continue
        row_errors.extend(
            (
                abs(row["center_A_final"] - old["center_longitudinal"]),
                abs(row["center_B_final"] - old["center_transverse"]),
                abs(row["actuator_A_final"] - old["actuator_longitudinal"]),
                abs(row["actuator_B_final"] - old["actuator_transverse"]),
            )
        )
    profile_errors = []
    for row in response.get("phase_profiles", []):
        old = stored_profiles.get(row["phase_index"])
        if old is None:
            profile_errors.append(math.inf)
            continue
        profile_errors.extend(
            (
                abs(row["B_C"] - old["center_transverse"]),
                abs(row["B_Q"] - old["actuator_transverse"]),
            )
        )
    stored_means = stored.get("phase_averaged_transverse_response", {})
    mean_errors = [
        abs(response["means"]["B_C"] - stored_means.get("center", math.inf)),
        abs(
            response["means"]["B_Q"]
            - stored_means.get("actuator", math.inf)
        ),
    ]
    frozen_mean_errors = {
        key: abs(response["means"][key] - expected)
        for key, expected in EXPECTED_L3_MEANS.items()
    }
    exact_metadata = bool(
        payload.get("candidate_id") == p4r.CANDIDATE_ID
        and payload.get("candidate", {}).get("radius_decimal")
        == p4r.RADIUS_DECIMAL
        and payload.get("candidate", {}).get("theta_decimal")
        == p4r.THETA_DECIMAL
        and payload.get("decision")
        == "p4r-phase-averaged-chiral-response-pass"
        and payload.get("historical_p4", {}).get("decision")
        == "p4-source-write-architecture-fail"
    )
    arm_metadata = bool(
        _registered_panel(active_arms, channel_off_arms)
        and all(
            arm.get("phase") == PHASES[int(arm["phase_index"])]
            and arm.get("offset_fraction") == THRESHOLDS.offset_fraction
            and arm.get("stop_reason") == "completed"
            and arm.get("valid") is True
            and arm.get("ledger_pass") is True
            and arm.get("dynamic_pass") is True
            for arm in active_arms
        )
        and all(arm.get("pass") is True for arm in channel_off_arms)
    )
    reconstruction_error = max(
        [*row_errors, *profile_errors, *mean_errors],
        default=math.inf,
    )
    gates = {
        "immutable_decisions_and_candidate": exact_metadata,
        "exact_order_and_arm_metadata": arm_metadata,
        "complete_finite_raw_reconstruction": response.get("available", False),
        "historical_response_gates": bool(response.get("pass", False)),
        "stored_summary_reconstruction": reconstruction_error
        <= THRESHOLDS.reconstruction_tolerance,
        "frozen_final_means": max(frozen_mean_errors.values())
        <= THRESHOLDS.reconstruction_tolerance,
    }
    return {
        "source_path": P4R_RESULT.as_posix(),
        "source_canonical_sha256": EXPECTED_CANONICAL_SHA256[
            P4R_RESULT.as_posix()
        ],
        "candidate_id": p4r.CANDIDATE_ID,
        "candidate": {
            **asdict(p4r.CANDIDATE),
            "radius_decimal": p4r.RADIUS_DECIMAL,
            "theta_decimal": p4r.THETA_DECIMAL,
        },
        "delta": delta,
        "raw_arm_counts": {
            "active": len(active_arms),
            "channel_off": len(channel_off_arms),
        },
        "reconstruction_maximum_absolute_error": reconstruction_error,
        "frozen_mean_errors": frozen_mean_errors,
        "response": response,
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _response_row_index(
    response: dict[str, Any],
) -> dict[tuple[int, int], dict[str, Any]]:
    return {
        (int(row["phase_index"]), int(row["chirality"])): row
        for row in response["phase_chirality_response"]
    }


def _profile_index(
    response: dict[str, Any],
) -> dict[int, dict[str, Any]]:
    return {
        int(row["phase_index"]): row for row in response["phase_profiles"]
    }


def _compare_scales(
    anchor: dict[str, Any],
    l3: dict[str, Any],
) -> dict[str, Any]:
    labels = {
        "A_C": "center_A_trace",
        "B_C": "center_B_trace",
        "A_Q": "actuator_A_trace",
        "B_Q": "actuator_B_trace",
    }
    anchor_rows = _response_row_index(anchor)
    l3_rows = _response_row_index(l3)
    trace_differences = []
    flattened: dict[str, list[float]] = {key: [] for key in labels}
    for phase_index, chirality in _expected_channel_off_keys():
        first = anchor_rows[(phase_index, chirality)]
        second = l3_rows[(phase_index, chirality)]
        row: dict[str, Any] = {
            "phase_index": phase_index,
            "chirality": chirality,
        }
        for label, key in labels.items():
            difference = (
                np.asarray(first[key], dtype=float)
                - np.asarray(second[key], dtype=float)
            )
            row[label] = difference.tolist()
            flattened[label].extend(difference.tolist())
        trace_differences.append(row)
    transient_rms = {
        label: _rms(np.asarray(values, dtype=float))
        for label, values in flattened.items()
    }
    combined_complex_rms = {
        "center": _rms(
            np.sqrt(
                np.asarray(flattened["A_C"]) ** 2
                + np.asarray(flattened["B_C"]) ** 2
            )
        ),
        "actuator": _rms(
            np.sqrt(
                np.asarray(flattened["A_Q"]) ** 2
                + np.asarray(flattened["B_Q"]) ** 2
            )
        ),
    }

    anchor_profiles = _profile_index(anchor)
    l3_profiles = _profile_index(l3)
    profile_rows = []
    profile_values: dict[str, list[float]] = {key: [] for key in labels}
    for phase_index in range(8):
        row: dict[str, Any] = {
            "phase_index": phase_index,
            "phase": PHASES[phase_index],
        }
        for label in labels:
            difference = (
                anchor_profiles[phase_index][label]
                - l3_profiles[phase_index][label]
            )
            row[label] = difference
            profile_values[label].append(difference)
        profile_rows.append(row)
    profile_rms = {
        label: _rms(np.asarray(values, dtype=float))
        for label, values in profile_values.items()
    }

    mean_rows = {}
    for label in labels:
        anchor_mean = float(anchor["means"][label])
        l3_mean = float(l3["means"][label])
        difference = anchor_mean - l3_mean
        mean_rows[label] = {
            "anchor": anchor_mean,
            "l3": l3_mean,
            "signed_difference": difference,
            "absolute_difference": abs(difference),
            "ratio": anchor_mean / l3_mean if l3_mean != 0.0 else None,
        }
    common_grid = bool(
        tuple(anchor["steps"]) == ANCHOR_STEPS
        and tuple(l3["steps"]) == L3_STEPS
        and len(anchor["memory_times"]) == len(l3["memory_times"]) == 401
        and all(
            math.isclose(first, second, rel_tol=0.0, abs_tol=1.0e-15)
            for first, second in zip(
                anchor["memory_times"],
                l3["memory_times"],
                strict=True,
            )
        )
    )
    trace_gates = {
        label: value <= THRESHOLDS.scale_tolerance
        for label, value in transient_rms.items()
    }
    profile_gates = {
        label: value <= THRESHOLDS.scale_tolerance
        for label, value in profile_rms.items()
    }
    mean_gates = {
        label: row["absolute_difference"] <= THRESHOLDS.scale_tolerance
        for label, row in mean_rows.items()
    }
    gates = {
        "common_memory_time_grid": common_grid,
        "complete_transient": all(trace_gates.values()),
        "final_phase_profile": all(profile_gates.values()),
        "final_means": all(mean_gates.values()),
    }
    return {
        "scale_tolerance": THRESHOLDS.scale_tolerance,
        "common_memory_times": list(MEMORY_TIMES),
        "trace_differences": trace_differences,
        "transient_rms": transient_rms,
        "combined_complex_rms_nondecisional": combined_complex_rms,
        "profile_differences": profile_rows,
        "profile_rms": profile_rms,
        "mean_comparison": mean_rows,
        "trace_gates": trace_gates,
        "profile_gates": profile_gates,
        "mean_gates": mean_gates,
        "gates": gates,
        "pass": bool(all(gates.values())),
    }


def _decision(
    *,
    pipeline: bool,
    active_arms: list[dict[str, Any]],
    channel_off_arms: list[dict[str, Any]],
    response: dict[str, Any],
    cross_scale: dict[str, Any],
) -> tuple[str, dict[str, bool]]:
    registration = _registered_panel(active_arms, channel_off_arms)
    validity = bool(
        registration and all(arm.get("valid", False) for arm in active_arms)
    )
    ledger = bool(
        registration
        and all(arm.get("ledger_pass", False) for arm in active_arms)
    )
    dynamics = bool(
        registration
        and all(arm.get("dynamic_pass", False) for arm in active_arms)
    )
    response_available = bool(response.get("available", False))
    response_pass = bool(response.get("pass", False))
    means = response.get("means", {})
    finite_means = bool(
        all(
            key in means and math.isfinite(float(means[key]))
            for key in EXPECTED_L3_MEANS
        )
    )
    center_mean = float(means["B_C"]) if finite_means else math.nan
    actuator_mean = float(means["B_Q"]) if finite_means else math.nan
    scalar_region = bool(
        finite_means
        and abs(center_mean) <= THRESHOLDS.scalar_null_maximum
        and abs(actuator_mean) <= THRESHOLDS.scalar_null_maximum
    )
    positive_chiral_region = bool(
        finite_means
        and center_mean >= THRESHOLDS.chiral_minimum
        and actuator_mean >= THRESHOLDS.chiral_minimum
    )
    support = response.get("positive_phase_support", {})
    sign_support = bool(
        support.get("center", 0) >= THRESHOLDS.sign_support_minimum
        and support.get("actuator", 0) >= THRESHOLDS.sign_support_minimum
    )
    directional_fail = bool(
        finite_means
        and (
            center_mean <= -THRESHOLDS.chiral_minimum
            or actuator_mean <= -THRESHOLDS.chiral_minimum
            or (
                abs(center_mean) >= THRESHOLDS.chiral_minimum
                and abs(actuator_mean) >= THRESHOLDS.chiral_minimum
                and math.copysign(1.0, center_mean)
                != math.copysign(1.0, actuator_mean)
            )
        )
    )
    scale_pass = bool(cross_scale.get("pass", False))
    common_grid = bool(
        cross_scale.get("gates", {}).get("common_memory_time_grid", False)
    )

    if (
        not pipeline
        or not registration
        or not validity
        or not response_available
        or not finite_means
        or not common_grid
    ):
        decision = "p4rs-inconclusive"
    elif not ledger:
        decision = "p4rs-ledger-or-metrology-fail"
    elif not dynamics or not response_pass:
        decision = "p4rs-inconclusive"
    elif scalar_region:
        decision = "p4rs-anchor-scalar-response"
    elif directional_fail:
        decision = "p4rs-anchor-chiral-hypothesis-fail"
    elif positive_chiral_region and sign_support and not scale_pass:
        decision = "p4rs-cross-scale-mismatch"
    elif positive_chiral_region and sign_support and scale_pass:
        decision = "p4rs-anchor-scale-transfer-pass"
    else:
        decision = "p4rs-inconclusive"
    return decision, {
        "pipeline": pipeline,
        "registration": registration,
        "valid_active_arms": validity,
        "response_available": response_available,
        "reciprocal_ledger_and_metrology": ledger,
        "nonlinear_loop_dynamics": dynamics,
        "response_symmetry_and_odd_signal": response_pass,
        "finite_response_means": finite_means,
        "scalar_region": scalar_region,
        "positive_chiral_region": positive_chiral_region,
        "positive_phase_support": sign_support,
        "directional_fail_region": directional_fail,
        "common_memory_time_grid": common_grid,
        "cross_scale_transfer": scale_pass,
    }


def _runtime_metadata() -> dict[str, Any]:
    config = getattr(np.__config__, "CONFIG", {})
    build_dependencies = (
        config.get("Build Dependencies", {}) if isinstance(config, dict) else {}
    )
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": importlib.metadata.version("numpy"),
        "scipy": importlib.metadata.version("scipy"),
        "mpmath": importlib.metadata.version("mpmath"),
        "blas": build_dependencies.get("blas", {}),
    }


def run_gate() -> dict[str, Any]:
    """Execute the once-only registered Anchor target calculation."""

    started = time.perf_counter()
    provenance = _verify_provenance()
    root_controls = _anchor_root_controls()
    l3_reference = _load_l3_reference()
    construction = _construction_controls()
    registration = _registration_controls()
    pre_target_pass = bool(
        root_controls["pass"]
        and l3_reference["pass"]
        and construction["pass"]
        and registration["pass"]
    )
    if not pre_target_pass:
        raise RuntimeError(
            "P4-R-S pre-target controls failed; classified as inconclusive "
            "without opening the registered panel"
        )

    channel_off_arms = [
        _run_anchor_channel_off(
            phase_index=phase_index,
            chirality=chirality,
        )
        for phase_index, chirality in _expected_channel_off_keys()
    ]
    channel_off_traces_complete = all(
        tuple(row["step"] for row in arm["trace"]) == ANCHOR_STEPS
        and p4r.p4._all_finite(arm["trace"])
        for arm in channel_off_arms
    )
    if not channel_off_traces_complete:
        raise RuntimeError(
            "Anchor channel-off trace is incomplete; refusing a partial "
            "target result"
        )
    channel_off = {
        _channel_off_key(arm): arm for arm in channel_off_arms
    }
    active_arms = [
        _run_anchor_active_arm(
            phase_index=phase_index,
            chirality=chirality,
            offset_sign=offset_sign,
            baseline=channel_off[(phase_index, chirality)],
        )
        for phase_index, chirality, offset_sign in _expected_active_keys()
    ]
    anchor_response = _response_controls(
        active_arms,
        channel_off_arms,
        radius=CANDIDATE.radius,
        delta=THRESHOLDS.offset_fraction * CANDIDATE.radius,
        expected_steps=ANCHOR_STEPS,
        alpha=CANDIDATE.alpha,
    )
    cross_scale = _compare_scales(
        anchor_response,
        l3_reference["response"],
    )
    pipeline = bool(
        pre_target_pass and all(arm["pass"] for arm in channel_off_arms)
    )
    decision, gates = _decision(
        pipeline=pipeline,
        active_arms=active_arms,
        channel_off_arms=channel_off_arms,
        response=anchor_response,
        cross_scale=cross_scale,
    )
    return {
        "schema_version": 1,
        "gate": "P4-R-S Anchor-scale transfer of the discrete loop response",
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
        "runtime": _runtime_metadata(),
        "protocol": {
            "path": PROTOCOL.as_posix(),
            "design_audit": DESIGN_AUDIT.as_posix(),
            "design_freeze_revision": DESIGN_FREEZE_REVISION,
            "freeze_revision": PROTOCOL_FREEZE_REVISION,
            "thresholds": asdict(THRESHOLDS),
            "phases": list(PHASES),
            "active_order": [list(key) for key in _expected_active_keys()],
            "channel_off_order": [
                list(key) for key in _expected_channel_off_keys()
            ],
            "no_target_fit": True,
            "no_interpolation": True,
            "no_mass_spin_momentum_or_p5_claim": True,
        },
        "anchor_root_controls": root_controls,
        "registration_controls": registration,
        "construction_controls": construction,
        "l3_reference": l3_reference,
        "channel_off_arms": channel_off_arms,
        "active_arms": active_arms,
        "anchor_response": anchor_response,
        "cross_scale": cross_scale,
        "gates": gates,
        "decision": decision,
        "claim_boundary": {
            "established_if_full_pass": (
                "a deterministic second-cell Anchor holdout of the same "
                "declared source/write rule at matched memory time, with the "
                "registered discrete chiral response and effect-size limits"
            ),
            "not_established": (
                "an independent replication, a continuum convergence order, "
                "continuous phase invariance, a physical actuator, momentum, "
                "intrinsic spin, inertia, material center of mass, physical "
                "mass, P5 evidence, or an unrestricted publication source"
            ),
        },
    }


def render_report(payload: dict[str, Any], *, summary_sha256: str) -> str:
    means = payload["anchor_response"]["means"]
    transient = payload["cross_scale"]["transient_rms"]
    profiles = payload["cross_scale"]["profile_rms"]
    lines = [
        "# P4-R-S Anchor-scale transfer result",
        "",
        f"Decision: {payload['decision']}.",
        "",
        "## Registered response",
        "",
        (
            "Anchor final means: "
            f"A_C={means['A_C']:.17g}, B_C={means['B_C']:.17g}, "
            f"A_Q={means['A_Q']:.17g}, B_Q={means['B_Q']:.17g}."
        ),
        (
            "Complete-transient RMS differences: "
            + ", ".join(
                f"{key}={value:.6g}" for key, value in transient.items()
            )
            + "."
        ),
        (
            "Final-profile RMS differences: "
            + ", ".join(
                f"{key}={value:.6g}" for key, value in profiles.items()
            )
            + "."
        ),
        "",
        "## Claim boundary",
        "",
        payload["claim_boundary"]["established_if_full_pass"]
        if payload["decision"] == "p4rs-anchor-scale-transfer-pass"
        else "The conditional full-pass claim boundary was not activated.",
        "",
        "Not established: " + payload["claim_boundary"]["not_established"] + ".",
        "",
        "The three publication-source major restrictions remain open.",
        "",
        "## Provenance",
        "",
        f"Execution revision: {payload['provenance']['revision']}.",
        f"Protocol freeze: {PROTOCOL_FREEZE_REVISION}.",
        f"Machine-readable JSON SHA-256: {summary_sha256}.",
        "",
    ]
    return "\n".join(lines)


def _json_safe(value: Any) -> Any:
    return p4r._json_safe(value)


def _resolved(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _validate_default_output_paths(summary: Path, report: Path) -> None:
    if _resolved(summary).resolve() != (ROOT / DEFAULT_SUMMARY).resolve():
        raise RuntimeError("P4-R-S permits only the registered JSON output")
    if _resolved(report).resolve() != (ROOT / DEFAULT_REPORT).resolve():
        raise RuntimeError("P4-R-S permits only the registered report output")
    for path in (_resolved(summary), _resolved(report)):
        if path.exists():
            raise RuntimeError(f"refusing to overwrite registered output: {path}")
        temporary = path.with_name(path.name + ".tmp")
        if temporary.exists():
            raise RuntimeError(f"refusing stale temporary output: {temporary}")


def _write_complete_outputs(
    *,
    summary_path: Path,
    summary_content: str,
    report_path: Path,
    report_content: str,
) -> None:
    paths = (summary_path, report_path)
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() or path.with_name(path.name + ".tmp").exists():
            raise RuntimeError(f"refusing existing output or temporary: {path}")
    summary_temporary = summary_path.with_name(summary_path.name + ".tmp")
    report_temporary = report_path.with_name(report_path.name + ".tmp")
    summary_temporary.write_text(summary_content, encoding="utf-8")
    report_temporary.write_text(report_content, encoding="utf-8")
    summary_temporary.replace(summary_path)
    report_temporary.replace(report_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    args = parser.parse_args()
    _validate_default_output_paths(args.summary, args.report)
    payload = _json_safe(run_gate())
    serialized = json.dumps(
        payload,
        allow_nan=False,
        indent=2,
        sort_keys=True,
    ) + "\n"
    summary_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    report = render_report(payload, summary_sha256=summary_hash)
    _write_complete_outputs(
        summary_path=_resolved(args.summary),
        summary_content=serialized,
        report_path=_resolved(args.report),
        report_content=report,
    )
    print(
        json.dumps(
            {"decision": payload["decision"], "json_sha256": summary_hash}
        )
    )


if __name__ == "__main__":
    main()
