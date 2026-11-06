"""Recompute only saved-data comparisons, not target trajectories."""

import json

from experiments.current.dynamics.rotation import fifo_oblique_120 as runner


def test_saved_control_is_bound_complete_and_matches_opposite_sign_reference(
    monkeypatch,
):
    def forbidden(**kwargs):
        raise AssertionError("evidence audit must not integrate trajectories")

    monkeypatch.setattr(runner, "run_oblique_probe", forbidden)
    directory = runner.anchor.ROOT / runner.OUTPUT_REL

    def read(name):
        return json.loads((directory / name).read_text(encoding="utf-8"))

    receipt, record, summary = [
        read(name) for name in ("receipt.json", "probe.json", "summary.json")
    ]
    assert (
        receipt["metadata"]["execution_revision"]
        == "8150e3f65c414c4fc1326dd44c32f49a788af588"
    )
    assert receipt["metadata"]["git_status_at_start"] == ""
    assert record["status"] == "completed"
    assert 0 < record["elapsed_seconds"] < receipt["seconds"] == 60
    reference, provenance = runner.load_reference(receipt["inputs"])
    assert provenance == receipt["reference"]
    result = record["result"]
    assert result["sample_steps"] == list(range(0, 2001, 10))
    assert result["settings"]["angles_degrees"] == [120]
    assert summary == {
        "status": "completed",
        **runner.compare_curves(result, reference),
    }
    assert summary["decision"] == "mirror-control-pass"
    assert all(pair["max_absolute_difference"] < 2e-16 for pair in summary["pairs"])
