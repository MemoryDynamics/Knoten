"""Audit saved attempt-1 records only; do not rerun target calculations."""

from datetime import datetime
from decimal import Decimal
import json
import math
from pathlib import Path

from experiments.current.dynamics.rotation import fifo_normal_anchor as runner


DIRECTORY = Path(__file__).resolve().parents[1] / runner.OUTPUT_REL
REVISION = "16f60f5a12281628a55eb5e591fe027418d21a3a"


def read(name):
    return json.loads((DIRECTORY / name).read_text(encoding="utf-8"))


def test_saved_panels_bind_to_frozen_inputs_and_remain_inconclusive():
    receipt = read("receipt.json")
    assert receipt["metadata"]["execution_revision"] == REVISION
    assert receipt["metadata"]["git_status_at_start"] == ""
    assert receipt["metadata"]["source"]["git_blob"] == runner.INPUT_BLOB
    panels = [read(f"panel_{precision}.json") for precision in (80, 120)]
    for precision, panel in zip((80, 120), panels, strict=True):
        assert panel["status"] == "completed"
        runner._validate_worker_result(panel["result"], receipt["inputs"], precision)
        assert panel["result"]["root_certificate"]["pass"]
    assert (
        runner.classify_panels(panels)
        == read("summary.json")["decision"]
        == "inconclusive"
    )


def test_interval_failure_is_already_present_at_first_reflection():
    for precision in (80, 120):
        result = read(f"panel_{precision}.json")["result"]
        reflections = result["schur"]["reflections"]
        assert len(reflections) == 1
        assert reflections[0]["degree"] == 1197
        coefficient = reflections[0]["coefficient"]
        assert Decimal(coefficient["lower"]) < -1
        assert Decimal(coefficient["upper"]) > 1
        constant = result["normal_polynomial"][-1]
        assert 0 < Decimal(constant["lower"]) < Decimal(constant["upper"]) < 1


def test_saved_probe_has_all_registered_arms_samples_and_consistent_descriptors():
    first = read("panel_80.json")
    record = first["result"]["oblique_probe"]
    runner._validate_probe_record(record, read("receipt.json")["inputs"])
    probe = record["result"]
    assert probe["sample_steps"] == list(range(0, 2001, 10))
    assert len(probe["baseline_distances"]) == 201
    for arm in probe["arms"]:
        assert len(arm["distances"]) == 201
        assert all(math.isfinite(value) and value > 0 for value in arm["distances"])
        assert arm["initial_distance"] == arm["distances"][0]
        assert arm["final_ratio"] == arm["distances"][-1] / arm["initial_distance"]
        assert (
            arm["sampled_peak_ratio"] == max(arm["distances"]) / arm["initial_distance"]
        )
        assert (
            (arm["final_ratio"] < 0.8)
            if arm["angle_degrees"] == 0
            else (arm["final_ratio"] > 1.2)
        )
    assert max(probe["baseline_distances"]) < 0.01 * min(
        a["initial_distance"] for a in probe["arms"]
    )
    assert probe["decision"] == "growth-over-registered-window"


def test_saved_attempt_is_ordered_bounded_and_does_not_repeat_probe():
    first, second = [read(f"panel_{precision}.json") for precision in (80, 120)]
    for panel in (first, second):
        assert 0 < panel["elapsed_seconds"] < 300
    assert datetime.fromisoformat(first["finished_utc"]) <= datetime.fromisoformat(
        second["started_utc"]
    )
    assert first["result"]["oblique_probe"]["status"] == "completed"
    assert "oblique_probe" not in second["result"]
    assert (
        read("summary.json")["oblique_probe"]["decision"]
        == "growth-over-registered-window"
    )
