"""Synthetic archive evaluator checks; never evaluate the target coefficients."""

from copy import deepcopy
from fractions import Fraction as F
import json
import sys

import pytest

from experiments.current.dynamics.rotation import fifo_archived_normal_slope as runner


def endpoint(value):
    value = F(value)
    assert value.denominator & (value.denominator - 1) == 0
    exponent = -(value.denominator.bit_length() - 1)
    mantissa = abs(value.numerator)
    if mantissa == 0:
        return [0, 0, 0, 0]
    while mantissa % 2 == 0:
        mantissa //= 2
        exponent += 1
    return [int(value < 0), mantissa, exponent, mantissa.bit_length()]


def interval(lower, upper=None):
    return {
        "lower_binary": endpoint(lower),
        "upper_binary": endpoint(lower if upper is None else upper),
    }


@pytest.mark.parametrize(
    "value", [0, 1, -2, F(7, 8), F(1, 2**400), F(2**400 + 1, 2**400)]
)
def test_binary_exact_roundtrip(value):
    assert runner.binary_fraction(endpoint(value)) == value


@pytest.mark.parametrize(
    "raw",
    [
        [0, 0, 0, -1],
        [1, 0, 0, 0],
        [2, 1, 0, 1],
        [0, 2, 0, 2],
        [0, 3, 0, 1],
        [False, 1, 0, 1],
        [0, 1, 100001, 1],
        [0, 1, 0],
    ],
)
def test_invalid_binary_rejected(raw):
    with pytest.raises(ValueError):
        runner.binary_fraction(raw)


def test_reversed_interval_rejected():
    with pytest.raises(ValueError, match="reversed"):
        runner.interval_bounds(interval(1, 0))


@pytest.mark.parametrize(
    "root,decision",
    [
        (F(5, 4), runner.CERTIFIED),
        (F(1, 2), runner.UNRESOLVED),
        (F(-5, 4), runner.UNRESOLVED),
        (F(1), runner.UNRESOLVED),
    ],
)
def test_translation_preserving_polynomial(root, decision):
    # p=(z-1)(z-root); c1=-root. A negative unstable root must not pass.
    result = runner.evaluate_polynomial(
        [interval(1), interval(-1 - root), interval(root)]
    )
    assert result["decision"] == decision
    assert runner.read_fraction(result["slope"]["upper"]) == 1 - root


def test_multilag_index_and_sign():
    # c1=-1/8, c2=-3/4; p'(1)=1-1/8-3/2=-5/8.
    result = runner.evaluate_polynomial(
        [interval(1), interval(F(-15, 8)), interval(F(1, 8)), interval(F(3, 4))]
    )
    assert runner.read_fraction(result["slope"]["lower"]) == F(-5, 8)
    assert result["decision"] == runner.CERTIFIED


def test_negative_midpoint_with_zero_upper_is_not_a_pass():
    result = runner.evaluate_polynomial([interval(1), interval(-3, -2), interval(1, 2)])
    assert result["decision"] == runner.UNRESOLVED
    assert runner.read_fraction(result["slope"]["lower"]) == -1
    assert runner.read_fraction(result["slope"]["upper"]) == 0


def test_no_float_rounding_at_one():
    delta = F(1, 2**400)
    result = runner.evaluate_polynomial(
        [interval(1), interval(-2 - delta), interval(1 + delta)]
    )
    assert result["decision"] == runner.CERTIFIED
    assert runner.read_fraction(result["slope"]["upper"]) == -delta


@pytest.mark.parametrize(
    "records",
    [
        [interval(1)],
        [interval(2), interval(-2), interval(1)],
        [interval(1), interval(99), interval(1)],
    ],
)
def test_bad_polynomial_rejected(records):
    with pytest.raises(ValueError):
        runner.evaluate_polynomial(records)


def panel(precision, lower, upper):
    return {
        "precision_dps": precision,
        "status": "completed",
        "result": {
            "slope": {
                "lower": runner.fraction_record(F(lower)),
                "upper": runner.fraction_record(F(upper)),
            }
        },
    }


def test_joint_decision_requires_overlap_and_two_completed_panels():
    assert runner.classify([panel(80, -2, -1), panel(120, -2, -1)]) == runner.CERTIFIED
    assert runner.classify([panel(80, -2, 0), panel(120, -2, -1)]) == runner.UNRESOLVED
    assert (
        runner.classify([panel(80, -4, -3), panel(120, -2, -1)])
        == "method-inconsistent"
    )
    assert (
        runner.classify(
            [panel(80, -2, -1), {"precision_dps": 120, "status": "timeout"}]
        )
        == runner.UNRESOLVED
    )
    with pytest.raises(ValueError):
        runner.classify([panel(120, -2, -1), panel(80, -2, -1)])


def test_archive_validation_rejects_missing_gates_or_identity(monkeypatch):
    monkeypatch.setattr(runner.anchor, "_validate_worker_result", lambda *args: None)
    valid = {
        "status": "completed",
        "precision_dps": 80,
        "result": {
            "decision": "inconclusive",
            "root_certificate": {"pass": True, "gates": {"synthetic": True}},
        },
    }
    assert runner.validate_panel(valid, {}, 80) == valid["result"]
    for mutation in ("status", "precision", "root", "gates", "decision"):
        invalid = deepcopy(valid)
        if mutation == "status":
            invalid["status"] = "timeout"
        elif mutation == "precision":
            invalid["precision_dps"] = 120
        elif mutation == "root":
            invalid["result"]["root_certificate"]["pass"] = False
        elif mutation == "gates":
            invalid["result"]["root_certificate"]["gates"] = {}
        else:
            invalid["result"]["decision"] = "root-not-certified"
        with pytest.raises(ValueError):
            runner.validate_panel(invalid, {}, 80)


def test_worker_only_reads_archive_and_never_recertifies(monkeypatch):
    synthetic = {
        "normal_polynomial": [interval(1), interval(F(-9, 4)), interval(F(5, 4))],
        "decision": "inconclusive",
    }
    monkeypatch.setattr(
        runner, "load_archive", lambda name: ({"result": synthetic}, {"path": name})
    )
    monkeypatch.setattr(
        runner, "validate_panel", lambda p, inputs, precision: p["result"]
    )

    def forbidden(*args, **kwargs):
        pytest.fail("no model or root evaluation allowed")

    monkeypatch.setattr(runner.anchor, "certify_normal_fifo_box", forbidden)
    monkeypatch.setattr(runner.anchor, "run_oblique_probe", forbidden)
    assert runner.worker(80, {})["decision"] == runner.CERTIFIED


def test_authorization_and_exclusive_writes(tmp_path):
    with pytest.raises(PermissionError):
        runner.execute_once(expected_revision="unused")
    path = tmp_path / "result.json"
    runner.anchor._write_json(path, {"saved": True})
    with pytest.raises(FileExistsError):
        runner.anchor._write_json(path, {})
    assert json.loads(path.read_text()) == {"saved": True}


def test_capture_success_and_timeout_are_not_retried():
    success = runner.capture(
        [
            sys.executable,
            "-c",
            "import json,sys; print(json.dumps(json.load(sys.stdin)))",
        ],
        {"synthetic": True},
        seconds=10,
    )
    assert success["status"] == "completed"
    assert success["result"] == {"synthetic": True}
    timeout = runner.capture(
        [sys.executable, "-c", "import time; time.sleep(10)"], {}, seconds=0.1
    )
    assert timeout["status"] == "timeout"
    assert timeout["returncode"] is not None


def test_one_shot_parent_writes_receipt_then_exactly_two_workers(monkeypatch, tmp_path):
    inputs, provenance = {"synthetic": True}, {"source": "synthetic"}
    old_receipt = {
        "inputs": inputs,
        "metadata": {
            "execution_revision": runner.ARCHIVE_EXECUTION,
            "git_status_at_start": "",
            "source": provenance,
        },
    }
    monkeypatch.setattr(runner.anchor, "ROOT", tmp_path)
    monkeypatch.setattr(
        runner.anchor,
        "_execution_metadata",
        lambda revision: {"execution_revision": revision},
    )
    monkeypatch.setattr(
        runner.anchor, "load_registered_input", lambda: (inputs, provenance)
    )
    monkeypatch.setattr(
        runner, "load_archive", lambda name: (old_receipt, {"path": name})
    )
    commands = []

    def fake_capture(command, received):
        assert received == inputs
        assert (tmp_path / runner.OUTPUT_REL / "receipt.json").exists()
        commands.append(command)
        result = panel(int(command[-1]), -2, -1)
        result["result"].update(schema=runner.SCHEMA, precision_dps=int(command[-1]))
        return result

    monkeypatch.setattr(runner, "capture", fake_capture)
    summary = runner.execute_once(
        expected_revision="synthetic", authorization_confirmed=True
    )
    assert summary["decision"] == runner.CERTIFIED
    assert [command[-1] for command in commands] == ["80", "120"]
    assert all(command[1:3] == ["-m", runner.__name__] for command in commands)
    with pytest.raises(FileExistsError):
        runner.execute_once(expected_revision="synthetic", authorization_confirmed=True)
    assert len(commands) == 2


def test_cli_help_never_loads_archive(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("help must not read any target archive")

    monkeypatch.setattr(runner, "load_archive", forbidden)
    with pytest.raises(SystemExit) as raised:
        runner.main(["--help"])
    assert raised.value.code == 0
