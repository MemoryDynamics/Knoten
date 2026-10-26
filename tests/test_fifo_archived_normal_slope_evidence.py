"""Check saved slope results only; never repeat the target coefficient sum."""

from datetime import datetime
from fractions import Fraction as F
import json
from pathlib import Path

from experiments.current.dynamics.rotation import fifo_archived_normal_slope as runner


DIRECTORY = Path(__file__).resolve().parents[1] / runner.OUTPUT_REL
EXECUTION = "a155b7b5daad3c31f2c4c8b84bdf6699a946f70b"
HASHES = {
    80: "5c3e1cfba7f50e35183332ed74497a38857f124ef5ceefd0233d920bb0c6fd95",
    120: "682067781a845115a4df058134d55795ed4c3ff24debba25665f64cbfca4830c",
}


def read(name):
    return json.loads((DIRECTORY / name).read_text(encoding="utf-8"))


def test_saved_endpoints_are_strictly_negative_and_overlap(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("no target recalculation or archive coefficient loading")

    monkeypatch.setattr(runner, "evaluate_polynomial", forbidden)
    monkeypatch.setattr(runner, "load_archive", forbidden)
    panels = [read(f"panel_{precision}.json") for precision in (80, 120)]
    for panel in panels:
        assert panel["status"] == "completed"
        result = panel["result"]
        lower, upper = [
            runner.read_fraction(result["slope"][key]) for key in ("lower", "upper")
        ]
        assert F("-0.327646") < lower <= upper < F("-0.327645")
        assert result["decision"] == runner.CERTIFIED
        assert result["lag_count"] == 1199
        assert result["archived_schur_decision"] == "inconclusive"
    summary = read("summary.json")
    assert summary["panels"] == panels
    assert runner.classify(panels) == summary["decision"] == runner.CERTIFIED


def test_saved_provenance_and_one_shot_budget():
    receipt = read("receipt.json")
    assert receipt["metadata"]["execution_revision"] == EXECUTION
    assert receipt["metadata"]["git_status_at_start"] == ""
    assert receipt["precision_panels"] == [80, 120]
    assert receipt["seconds_per_panel"] == 30
    assert receipt["archive_receipt"]["revision"] == runner.ARCHIVE_REVISION
    previous = datetime.fromisoformat(receipt["started_utc"])
    for precision in (80, 120):
        marker = read(f"panel_{precision}_started.json")
        panel = read(f"panel_{precision}.json")
        assert (
            previous
            <= datetime.fromisoformat(marker["started_utc"])
            <= datetime.fromisoformat(panel["started_utc"])
        )
        previous = datetime.fromisoformat(panel["finished_utc"])
        assert 0 < panel["elapsed_seconds"] < 30
        assert panel["returncode"] == 0
        assert panel["stderr"] == ""
        source = panel["result"]["source"]
        assert source["revision"] == runner.ARCHIVE_REVISION
        assert source["path"] == f"{runner.ARCHIVE_PATH}/panel_{precision}.json"
        assert source["sha256_git_blob_bytes"] == HASHES[precision]
    assert previous <= datetime.fromisoformat(read("summary.json")["finished_utc"])
