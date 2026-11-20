"""Synthetic payloads and tiny child controls; no new positive target evaluation."""

from fractions import Fraction
import io
import json
import sys

from mpmath import iv
import numpy as np
import pytest

from emergenz_knoten import flat_memory_stability as method
from emergenz_knoten.rotating_wave_interval import _interval_record
from experiments.current.dynamics.rotation import flat_memory_cycle_stability as runner


def _synthetic_result():
    return {
        "schema": method.SCHEMA,
        "inputs": dict(runner.INPUTS),
        "decision": method.CERTIFIED,
        "method_consistent": True,
        "certificate": {
            "inputs": dict(runner.INPUTS),
            "precision_dps": method.PRECISION_DPS,
            "decision": method.CERTIFIED,
            "interior_certified": True,
            "form_product": _interval_record(iv.mpf(2), 30),
            "interior_margin": _interval_record(iv.mpf(1), 30),
        },
        "diagnostics": {
            "checks_passed": True,
            "form_quotient": [[0] * 8 for _ in range(8)],
            "reduced_full_matrix": [[0] * 15 for _ in range(15)],
            "form_eigenvalues_approximate": [[0, 0] for _ in range(8)],
            "form_product_approximate": 2.0,
            "errors": dict.fromkeys(
                [
                    "orbit_residual",
                    "invariant_subspace_residual",
                    "return_residual",
                    "form_trace_residual",
                ],
                0.0,
            ),
        },
    }


@pytest.mark.parametrize(
    "lower,upper,decision",
    [
        ("1.1", "1.2", method.CERTIFIED),
        ("-1.2", "-1.1", method.CERTIFIED),
        ("1", "1", method.UNRESOLVED),
        ("-1", "-1", method.UNRESOLVED),
        ("-2", "2", method.UNRESOLVED),
        ("0.1", "0.9", method.UNRESOLVED),
    ],
)
def test_only_strict_interval_product_violation_certifies_growth(
    lower, upper, decision
):
    assert method.classify_product(iv.mpf([lower, upper])) == decision


@pytest.mark.parametrize("value", ["inf", "-inf", "nan"])
def test_nonfinite_interval_never_certifies(value):
    with pytest.raises(FloatingPointError):
        method.classify_product(iv.mpf(value))


def test_product_formula_accepts_exact_formal_coefficients_without_a_model():
    b, s, g, q, radial, height = map(
        Fraction, ["2", "1/3", "1/4", "2/5", "3/10", "1/20"]
    )
    c_one = b * (1 - g * q) / s
    gamma = 4 * height / (2 * radial + 4 * height)
    independent = (b * q**3 * g) ** 2 * (
        c_one * s**3 * (gamma - 4 * height) - 4 * b * q**3 * g * height
    )
    assert method.form_product(b, s, g, q, radial, height) == independent


@pytest.mark.parametrize(
    "inputs",
    [
        {},
        {"f": "1/2", "g": "1/2", "q": "1/2"},
        {"f": "-1", "g": "1/2", "q": "1/2"},
        {"f": 0.5, "g": "1/2", "q": "1/2"},
    ],
)
def test_invalid_family_is_rejected_without_changing_precision(inputs):
    before = iv.dps
    with pytest.raises((TypeError, ValueError)):
        method.product_certificate(inputs)
    assert iv.dps == before


def test_interval_precision_restored_after_internal_failure(monkeypatch):
    monkeypatch.setattr(
        method,
        "family_parameters",
        lambda inputs: tuple(map(Fraction, ["1/4", "2/5", "1/2", "1/3", "2", "3"])),
    )

    def fail(*arguments):
        raise RuntimeError("synthetic arithmetic failure")

    monkeypatch.setattr(method, "form_product", fail)
    before = iv.dps
    with pytest.raises(RuntimeError, match="synthetic"):
        method.product_certificate({"synthetic": True})
    assert iv.dps == before


@pytest.mark.parametrize(
    "kind", ["pass", "inconclusive", "diagnostic_failure", "product_mismatch"]
)
def test_combination_never_promotes_floating_point_stability(monkeypatch, kind):
    result = _synthetic_result()
    certificate, diagnostics = result["certificate"], result["diagnostics"]
    if kind == "inconclusive":
        certificate["decision"] = method.UNRESOLVED
        diagnostics["spectral_radius_approximate"] = 0.1
    elif kind == "diagnostic_failure":
        diagnostics = {"checks_passed": False}
    elif kind == "product_mismatch":
        diagnostics["form_product_approximate"] = 0.0
    monkeypatch.setattr(method, "product_certificate", lambda inputs: certificate)
    monkeypatch.setattr(
        method,
        "build_history",
        lambda inputs: (np.zeros((5, 3)), np.eye(3), method.VectorMemoryConfig()),
    )
    monkeypatch.setattr(method, "history_diagnostics", lambda *arguments: diagnostics)
    observed = method.evaluate({"synthetic": True})
    expected = {
        "pass": method.CERTIFIED,
        "inconclusive": method.UNRESOLVED,
        "diagnostic_failure": "method-inconsistent",
        "product_mismatch": "method-inconsistent",
    }[kind]
    assert observed["decision"] == expected
    json.dumps(observed, allow_nan=False)


def test_authorization_guard_precedes_source_or_numerical_access(monkeypatch):
    monkeypatch.setattr(
        runner, "_metadata", lambda *arguments: pytest.fail("guard must run first")
    )
    with pytest.raises(PermissionError):
        runner.execute_once(expected_revision="a" * 40)


def test_default_cli_does_not_execute(monkeypatch):
    monkeypatch.setattr(
        runner, "execute_once", lambda **arguments: pytest.fail("no default execution")
    )
    with pytest.raises(SystemExit) as caught:
        runner.main([])
    assert caught.value.code == 2


def test_wrong_worker_payload_never_evaluates_target(monkeypatch):
    for key, value in runner.THREAD_ENV.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setattr(sys, "stdin", io.StringIO("{}"))
    monkeypatch.setattr(
        method, "evaluate", lambda *arguments: pytest.fail("must not evaluate")
    )
    with pytest.raises(ValueError, match="payload"):
        runner.main(["--worker"])


@pytest.mark.parametrize(
    "mutation",
    ["inputs", "equality", "interior", "method", "dimension", "missing_error", "nan"],
)
def test_invalid_claims_are_rejected(mutation):
    result = _synthetic_result()
    if mutation == "inputs":
        result["inputs"] = {}
    elif mutation == "equality":
        result["certificate"]["form_product"] = _interval_record(iv.mpf(1), 30)
    elif mutation == "interior":
        result["certificate"]["interior_margin"] = _interval_record(iv.mpf(0), 30)
    elif mutation == "method":
        result["method_consistent"] = False
    elif mutation == "dimension":
        result["diagnostics"]["form_quotient"].pop()
    elif mutation == "missing_error":
        result["diagnostics"]["errors"].pop("return_residual")
    else:
        result["diagnostics"]["form_product_approximate"] = float("nan")
    with pytest.raises((ValueError, KeyError)):
        runner.validate_result(result)


@pytest.mark.parametrize("midpoint", ["nan", "inf", "999"])
def test_midpoint_text_cannot_bypass_binary_endpoint_check(midpoint):
    result = _synthetic_result()
    result["certificate"]["form_product"]["midpoint"] = midpoint
    with pytest.raises(ValueError):
        runner.validate_result(result)


@pytest.mark.parametrize("status", ["completed", "timeout", "error", "changed-source"])
def test_one_shot_attempt_retains_receipt_and_never_retries(
    monkeypatch, tmp_path, status
):
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(runner, "OUTPUT_REL", runner.Path("attempt"))
    metadata = {"revision": "a" * 40, "sources": [{"synthetic": True}]}
    monkeypatch.setattr(runner, "_metadata", lambda revision: metadata)
    monkeypatch.setattr(
        runner,
        "_sources",
        lambda: [] if status == "changed-source" else metadata["sources"],
    )
    calls = []

    def capture(command, inputs):
        calls.append((command, inputs))
        return {
            "status": "completed" if status == "changed-source" else status,
            "elapsed_seconds": 0.01,
            "result": _synthetic_result()
            if status in {"completed", "changed-source"}
            else None,
        }

    monkeypatch.setattr(runner, "capture", capture)
    summary = runner.execute_once(
        expected_revision="a" * 40, authorization_confirmed=True
    )
    assert summary["decision"] == (
        method.CERTIFIED if status == "completed" else method.UNRESOLVED
    )
    receipt = json.loads((tmp_path / "attempt/receipt.json").read_text())
    assert receipt["seconds"] == 30 and receipt["inputs"] == runner.INPUTS
    with pytest.raises(FileExistsError):
        runner.execute_once(expected_revision="a" * 40, authorization_confirmed=True)
    assert len(calls) == 1


def test_synthetic_child_has_single_thread_environment():
    command = [
        sys.executable,
        "-c",
        "import json,os; print(json.dumps({k:os.environ[k] for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']}))",
    ]
    panel = runner.capture(command, {"synthetic": True}, seconds=5)
    assert panel["status"] == "completed"
    assert set(panel["result"].values()) == {"1"}


def test_synthetic_sleeping_child_is_killed_without_retry():
    panel = runner.capture(
        [sys.executable, "-c", "import time; time.sleep(3)"], {}, seconds=0.1
    )
    assert panel["status"] == "timeout" and panel["returncode"] != 0
    assert panel["result"] is None


def test_synthetic_malformed_child_output_is_not_a_result():
    panel = runner.capture([sys.executable, "-c", "print('not-json')"], {}, seconds=5)
    assert panel["status"] == "error" and panel["result"] is None


def test_real_module_description_reads_sources_without_target_work():
    panel = runner.capture(
        [sys.executable, "-m", runner.__name__, "--describe"], {}, seconds=10
    )
    assert panel["status"] == "completed"
    assert panel["result"]["target_evaluated"] is False
    assert panel["result"]["sources"] == runner._sources()
    assert panel["result"]["inputs"] == runner.INPUTS


@pytest.mark.parametrize(
    "revision,status,expected",
    [
        ("short", b"", "full frozen"),
        ("b" * 40, b"", "mismatch"),
        ("a" * 40, b" M dirty", "clean"),
    ],
)
def test_revision_and_cleanliness_fail_closed(monkeypatch, revision, status, expected):
    monkeypatch.setattr(
        runner,
        "_git",
        lambda *arguments: b"a" * 40 if arguments[0] == "rev-parse" else status,
    )
    with pytest.raises(ValueError, match=expected):
        runner._metadata(revision)


def test_sources_are_bound_to_this_worktree(monkeypatch, tmp_path):
    records = runner._sources()
    assert len(records) == len(runner.SOURCE_MODULES)
    assert all(len(item["sha256"]) == 64 for item in records)
    monkeypatch.setattr(method, "__file__", str(tmp_path / "other.py"))
    with pytest.raises(ValueError):
        runner._sources()
