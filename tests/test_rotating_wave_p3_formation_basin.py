from __future__ import annotations

import copy
import subprocess

from experiments.current.dynamics.rotation import (
    scalar_memory_rotating_wave_p3_formation_basin as p3,
)


def test_p3_registration_matches_frozen_candidate_and_protocol() -> None:
    assert p3.CANDIDATE.candidate_id == p3.CANDIDATE_ID
    assert p3.CANDIDATE.horizon == 2400
    assert p3.THRESHOLDS.active_updates == 12_000
    assert p3.THRESHOLDS.entrance_deadline == 9_000
    assert p3.THRESHOLDS.phase_start == 10_000
    assert p3.THRESHOLDS.sample_every == 10
    assert len(p3.EXPECTED_INITIAL_D0) == 5


def test_static_p3_construction_controls_pass_without_target_continuation() -> None:
    controls = p3._construction_controls()

    assert controls["pass"] is True
    assert controls["target_separation"]["pass"] is True
    assert len(controls["histories"]) == 6
    assert all(row["pass"] for row in controls["histories"])
    assert all(row["pass"] for row in controls["prepared_one_step"])
    noncircular = [row for row in controls["histories"] if row["panel"] != "prepared"]
    assert min(row["chirality_margin"] for row in noncircular) >= 0.1


def test_frozen_p3_protocol_and_dependency_blobs_are_unchanged() -> None:
    assert p3._git_blob(p3.PROTOCOL.as_posix()) == p3.EXPECTED_BLOBS[
        p3.PROTOCOL.as_posix()
    ]
    assert all(
        p3._git_blob(path) == expected
        for path, expected in p3.EXPECTED_BLOBS.items()
    )
    result = subprocess.run(
        [
            "git",
            "diff",
            "--quiet",
            p3.FREEZE_REVISION,
            "HEAD",
            "--",
            p3.PROTOCOL.as_posix(),
        ],
        cwd=p3.ROOT,
        check=False,
    )
    assert result.returncode == 0


def test_nonfinite_stored_metric_is_a_pipeline_failure() -> None:
    row = {
        "expected_d0": 1.0,
        "expected_d0_fraction": 1.0,
        "opposite_d0": 1.0,
        "opposite_d0_fraction": 1.0,
        "alignment_phase": 0.0,
        "translation_reduced_norm": 1.0,
        "translation_reduced_norm_fraction": 1.0,
        "centroid_x": 0.0,
        "centroid_y": 0.0,
        "centroid_norm": 0.0,
    }
    pair = {"plus": {"trace": [row]}, "minus": {"trace": [copy.deepcopy(row)]}}

    assert p3._stored_pair_metrics_finite([pair]) is True
    pair["minus"]["trace"][0]["expected_d0"] = float("nan")
    assert p3._stored_pair_metrics_finite([pair]) is False
