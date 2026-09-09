from __future__ import annotations

import copy
from decimal import Decimal, localcontext
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import struct

import numpy as np
import pytest

from emergenz_knoten.rotating_wave_stability import native_fifo_step
from emergenz_knoten.rotating_wave_stability import circular_history


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_transfer_result_schema_v3.json"
)
RUNNER_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_transfer_gate.py"
)
HORIZONS = (600, 900, 1200, 1500, 1800, 2400, 3600)
PARAMETERS = {
    "alpha": 0.01,
    "memory_mass": 1.0,
    "eta": 0.15,
    "sigma_rep": 1.0,
    "sigma_att": 3.0,
    "amplitude_rep": 1.0,
    "amplitude_att": 3.5,
}


def _load_future_module(path: Path, name: str):
    if not path.is_file():
        return _MissingImplementation(path.name)
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class _MissingImplementation:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def __getattr__(self, name: str):
        raise AssertionError(
            f"{self.filename} is intentionally absent in the registered RED "
            "commit; the smallest protocol-conforming implementation is the "
            f"next stage (first requested symbol: {name})"
        )


@pytest.fixture
def gate():
    return _load_future_module(RUNNER_PATH, "horizon_transfer_gate_under_test")


def _contract() -> dict[str, object]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _referenced_name(specification: str) -> tuple[str, str] | None:
    while specification.startswith("nullable:"):
        specification = specification.split(":", 1)[1]
    if ":" not in specification:
        return "primitive_contract", specification
    namespace, name = specification.split(":", 1)
    mapping = {
        "array": "arrays",
        "const": "constants",
        "enum": "enums",
        "object": "objects",
    }
    if namespace == "nullable":
        return "primitive_contract", name
    if namespace not in mapping:
        return None
    return mapping[namespace], name


def test_horizon_contract_has_exactly_seven_semantic_roots() -> None:
    contract = _contract()
    assert contract["root"] == "object:payload"
    assert set(contract["objects"]["payload"]) == {
        "identity",
        "finite_branch",
        "infinite_tail",
        "stability",
        "controls",
        "classification",
        "publication",
    }
    assert contract["constants"]["horizons"] == list(HORIZONS)
    assert contract["strict"] == {
        "allow_additional_fields": False,
        "allow_nonfinite_numbers": False,
        "allow_numpy_scalars": False,
        "allow_self_hash_in_result": False,
    }


def test_horizon_contract_references_resolve_and_publication_has_no_self_hash() -> None:
    contract = _contract()
    primitives = set(contract["primitive_contract"])
    for group in ("arrays", "objects"):
        for definition in contract[group].values():
            values = definition.values()
            for value in values:
                specifications = value if isinstance(value, list) else [value]
                for specification in specifications:
                    if not isinstance(specification, str):
                        continue
                    reference = _referenced_name(specification)
                    if reference is None:
                        assert specification in primitives or specification == "null"
                        continue
                    namespace, name = reference
                    assert name in contract[namespace], (namespace, name)
    publication_contract = json.dumps(
        {
            "publication": contract["objects"]["publication"],
            "artifact": contract["objects"]["artifact"],
        },
        sort_keys=True,
    )
    assert "sha256" not in publication_contract


def _direct_residual(radius: float, theta: float, horizon: int) -> np.ndarray:
    value = np.asarray([math.cos(theta) - 1.0, math.sin(theta)], dtype=float)
    q = 1.0 - PARAMETERS["alpha"]
    for age in range(1, horizon):
        distance = 2.0 * radius * abs(math.sin(0.5 * age * theta))
        phi = -PARAMETERS["amplitude_rep"] / PARAMETERS["sigma_rep"] ** 2 * math.exp(
            -(distance**2) / (2.0 * PARAMETERS["sigma_rep"] ** 2)
        ) + PARAMETERS["amplitude_att"] / PARAMETERS["sigma_att"] ** 2 * math.exp(
            -(distance**2) / (2.0 * PARAMETERS["sigma_att"] ** 2)
        )
        value += (
            PARAMETERS["eta"]
            * PARAMETERS["alpha"]
            * PARAMETERS["memory_mass"]
            * q**age
            * phi
            * np.asarray(
                [1.0 - math.cos(age * theta), math.sin(age * theta)],
                dtype=float,
            )
        )
    return value


def test_finite_formula_and_analytic_jacobian_are_independently_replayed(gate) -> None:
    radius = 0.91
    theta = 0.037
    horizon = 17
    observed = gate.finite_residual_and_jacobian(
        radius=radius,
        theta=theta,
        horizon=horizon,
        precision_dps=80,
    )
    residual = np.asarray(observed["residual"], dtype=float)
    jacobian = np.asarray(observed["jacobian"], dtype=float)
    np.testing.assert_allclose(residual, _direct_residual(radius, theta, horizon), atol=2e-14)
    step = 1e-6
    finite_difference = np.column_stack(
        (
            (_direct_residual(radius + step, theta, horizon) - _direct_residual(radius - step, theta, horizon)) / (2 * step),
            (_direct_residual(radius, theta + step, horizon) - _direct_residual(radius, theta - step, horizon)) / (2 * step),
        )
    )
    np.testing.assert_allclose(jacobian, finite_difference, rtol=2e-6, atol=2e-8)


def _positive_float_bits(value: float) -> int:
    assert value > 0.0 and math.isfinite(value)
    return struct.unpack(">Q", struct.pack(">d", value))[0]


def test_q_representations_compare_equal_binary64_semantics(gate) -> None:
    rows = gate.q_representations(HORIZONS)
    assert [row["horizon"] for row in rows] == list(HORIZONS)
    q64 = 1.0 - float("0.01")
    for row in rows:
        horizon = row["horizon"]
        direct = q64**horizon
        exp_log = math.exp(horizon * math.log(q64))
        assert row["direct_power"] == direct
        assert row["exp_log_power"] == exp_log
        assert row["ulp_difference"] == abs(
            _positive_float_bits(direct) - _positive_float_bits(exp_log)
        )
        assert row["ulp_difference"] <= 2
        assert row["two_ulp_gate"] is True
        assert math.isfinite(row["diagnostic_exp_log1p"])
        with localcontext() as exact_context:
            exact_context.prec = 2 * horizon + 10
            exact_power = format(Decimal("0.99") ** horizon, "f")
        assert row["decimal_power"] == exact_power
        with localcontext() as context:
            context.prec = 70
            decimal_power = Decimal(row["decimal_power"])
            expected_decimal = Decimal("0.99") ** horizon
            assert abs(decimal_power / expected_decimal - 1) < Decimal("1e-65")
    assert rows[-1]["direct_power"] > 0.0


def test_tail_bounds_equal_the_registered_conservative_formulas(gate) -> None:
    with localcontext() as context:
        context.prec = 80
        phi0 = Decimal(1) + Decimal("3.5") / Decimal(9)
        phi1 = (-Decimal("0.5")).exp() * (
            Decimal(1) + Decimal("3.5") / Decimal(27)
        )
        q = Decimal("0.99")
        for horizon in HORIZONS:
            observed = gate.tail_bounds(horizon=horizon, precision_dps=80)
            expected = {
                "residual_bound": Decimal("0.30") * phi0 * q**horizon,
                "jacobian_radius_bound": Decimal("0.60") * phi1 * q**horizon,
                "jacobian_theta_bound": Decimal("0.15")
                * (phi0 + Decimal("2.2") * phi1)
                * q**horizon
                * (Decimal(horizon) + q / Decimal("0.01")),
            }
            for name, value in expected.items():
                outward = float(observed[name])
                assert Decimal.from_float(outward) >= value
                assert Decimal.from_float(math.nextafter(outward, -math.inf)) < value


def test_interval_drift_uses_endpoint_suprema_and_width_mutation_closes_gate(gate) -> None:
    first = {"radius": [0.9, 0.91], "theta": [0.015, 0.0151]}
    second = {"radius": [0.905, 0.915], "theta": [0.01505, 0.01515]}
    upper = gate.interval_drift_upper(
        first,
        second,
        radius_scale=0.946517504804225,
        theta_scale=0.015770381717135,
    )
    exact = max(
        0.015 / 0.946517504804225,
        0.00015 / 0.015770381717135,
    )
    assert upper >= exact
    assert upper <= math.nextafter(exact, math.inf) * (1.0 + 2e-15)
    narrow = gate.drift_gates(previous_upper=2e-7, final_upper=1e-9)
    broad = gate.drift_gates(previous_upper=2e-7, final_upper=1.1e-8)
    assert narrow["pass"] is True
    assert broad["pass"] is False


def test_interval_drift_preserves_sub_binary64_certificate_widths(gate) -> None:
    first = {
        "radius": ["0.946517504804225000000000000000", "0.946517504804225000000000000001"],
        "theta": ["0.015770381717135000000000000000", "0.015770381717135000000000000001"],
    }
    second = {
        "radius": ["0.946517504804225000000000000002", "0.946517504804225000000000000003"],
        "theta": ["0.015770381717135000000000000002", "0.015770381717135000000000000003"],
    }
    upper = gate.interval_drift_upper(
        first,
        second,
        radius_scale=0.946517504804225,
        theta_scale=0.015770381717135,
    )
    assert upper > 0.0
    assert upper >= 3e-30 / 0.015770381717135


def test_homotopy_failure_is_inconclusive_without_complete_local_exclusion(gate) -> None:
    passing = [
        {"strict_interior": True, "overlaps_previous": True} for _ in range(64)
    ]
    assert gate.evaluate_homotopy_slabs(passing) == "pass"
    failing = copy.deepcopy(passing)
    failing[31]["strict_interior"] = False
    assert gate.evaluate_homotopy_slabs(failing) == "inconclusive"


def _eigenpair() -> dict[str, object]:
    vector = [[0.0, 0.0] for _ in range(4800)]
    vector[0] = [1.0, 0.0]
    return {
        "eigenvalue": [0.9, 0.0],
        "modulus": 0.9,
        "normalized_residual": 1e-12,
        "translation_overlap": 0.0,
        "rotation_overlap": 0.0,
        "classification": "transverse",
        "vector": vector,
    }


def test_partial_or_malformed_arnoldi_panels_are_inconclusive(gate) -> None:
    complete = {"status": "complete", "eigenpairs": [_eigenpair() for _ in range(24)]}
    assert gate.evaluate_arnoldi_panel(complete, expected_count=24)["gate_state"] == "pass"
    partial = {"status": "arpack-no-convergence", "eigenpairs": complete["eigenpairs"][:-1]}
    assert gate.evaluate_arnoldi_panel(partial, expected_count=24)["gate_state"] == "inconclusive"
    missing_vector = copy.deepcopy(complete)
    missing_vector["eigenpairs"][0]["vector"] = None
    assert gate.evaluate_arnoldi_panel(missing_vector, expected_count=24)["gate_state"] == "inconclusive"
    high_residual = copy.deepcopy(complete)
    high_residual["eigenpairs"][0]["normalized_residual"] = 1.01e-8
    assert gate.evaluate_arnoldi_panel(high_residual, expected_count=24)["gate_state"] == "inconclusive"


@pytest.mark.parametrize("horizon", (17, 257))
def test_circular_fifo_is_independent_and_matches_shift_semantics(gate, monkeypatch, horizon: int) -> None:
    ages = np.arange(horizon, dtype=float)
    history = np.column_stack(
        (
            np.sin(0.17 * ages) + 0.03 * ages,
            np.cos(0.11 * ages) - 0.02 * ages,
        )
    )
    expected = native_fifo_step(history, **PARAMETERS)
    control = gate.run_circular_control(history, parameters=PARAMETERS)
    assert control["pass"] is True
    assert control["age_hash_equal"] is True
    assert control["new_point_relative_error"] < 5e-14
    assert control["complete_state_relative_error"] < 5e-14

    def forbidden(*args, **kwargs):
        raise AssertionError("circular backend called native_fifo_step")

    monkeypatch.setattr(gate, "native_fifo_step", forbidden, raising=False)
    state = gate.circular_fifo_from_age_order(history)
    advanced = gate.circular_fifo_step(state, **PARAMETERS)
    observed = gate.materialize_circular_fifo(advanced)
    np.testing.assert_allclose(observed, expected, rtol=5e-14, atol=5e-14)


@pytest.mark.parametrize(
    "mutation",
    ("reverse-modulo", "overwrite-before-read", "wrong-oldest-slot"),
)
def test_registered_circular_fifo_mutations_are_detected(gate, mutation: str) -> None:
    ages = np.arange(17, dtype=float)
    history = np.column_stack(
        (0.025 * ages + 0.003 * ages**2, 0.4 * np.sin(0.09 * ages))
    )
    record = gate.run_circular_control(history, parameters=PARAMETERS, mutation=mutation)
    assert record["pass"] is False
    assert record["mutation"] == mutation


def test_eta_zero_history_collapses_to_latest_point(gate) -> None:
    ages = np.arange(17, dtype=float)
    history = np.column_stack((ages / 17.0, np.cos(0.3 * ages)))
    collapsed = gate.eta_zero_collapse(history, steps=18)
    expected = np.repeat(history[[0]], 17, axis=0)
    np.testing.assert_allclose(collapsed, expected, atol=1e-14, rtol=0.0)


@pytest.mark.parametrize("horizon", HORIZONS)
def test_anchor_circle_fifo_and_eta_zero_controls_cover_every_horizon(gate, horizon: int) -> None:
    history = circular_history(
        radius=0.946517504804225,
        theta=0.015770381717135,
        horizon=horizon,
    )
    control = gate.run_circular_control(history, parameters=PARAMETERS)
    assert control["pass"] is True
    collapsed = gate.eta_zero_collapse(history, steps=horizon + 1)
    expected = np.repeat(history[[0]], horizon, axis=0)
    np.testing.assert_allclose(collapsed, expected, atol=1e-14, rtol=0.0)


def _gates(**updates: object) -> dict[str, object]:
    values: dict[str, object] = {
        "G0": "pass",
        "G1F": "pass",
        "G1R": "pass",
        "G2F": "pass",
        "G2R": "pass",
        "G3": "pass",
        "G4": "pass",
        "G5": "pass",
        "G6": "pass",
        "local_branch_excluded": False,
        "large_h_instability_supported": False,
    }
    values.update(updates)
    return values


@pytest.mark.parametrize(
    ("gates", "decision"),
    (
        (_gates(G0="fail"), "rotating-wave-horizon-experiment-invalid"),
        (_gates(G6="fail"), "rotating-wave-horizon-experiment-invalid"),
        (_gates(G1F="fail", local_branch_excluded=True), "registered-local-horizon-branch-loss"),
        (_gates(G3="fail"), "rotating-wave-horizon-branch-drift"),
        (_gates(G5="fail", large_h_instability_supported=True), "rotating-wave-infinite-root-certified-large-h-instability"),
        (_gates(), "rotating-wave-horizon-root-transfer-pass-with-large-h-stability-support"),
        (_gates(G5="inconclusive"), "infinite-memory-local-root-certified-stability-open"),
        (_gates(G2F="inconclusive"), "rotating-wave-horizon-transfer-inconclusive"),
    ),
)
def test_decision_precedence_is_exact_and_only_full_pass_opens_p5(gate, gates, decision) -> None:
    observed = gate.classify_horizon(gates, lower_tail_status="lower-tail-stress-pass")
    assert observed["decision"] == decision
    assert observed["p5_governance_review_open"] is (
        decision == "rotating-wave-horizon-root-transfer-pass-with-large-h-stability-support"
    )


def test_schema_validator_is_fail_closed_for_unknown_and_numpy_values(gate) -> None:
    witness = gate.contract_witness()
    gate.validate_result(witness)
    unknown = copy.deepcopy(witness)
    unknown["identity"]["unknown"] = 1
    with pytest.raises((TypeError, ValueError), match="unknown"):
        gate.validate_result(unknown)
    numpy_value = copy.deepcopy(witness)
    numpy_value["identity"]["parameters"]["alpha"] = np.float64(0.01)
    with pytest.raises((TypeError, ValueError), match="alpha"):
        gate.validate_result(numpy_value)
    numpy_horizon = copy.deepcopy(witness)
    numpy_horizon["finite_branch"]["horizons"][0] = np.int64(600)
    with pytest.raises((TypeError, ValueError), match="horizons"):
        gate.validate_result(numpy_horizon)


def test_publication_writes_two_contents_then_hash_manifest(gate, tmp_path: Path, monkeypatch) -> None:
    payload = gate.contract_witness()
    result_path = tmp_path / "result.json"
    report_path = tmp_path / "result.md"
    manifest_path = tmp_path / "result.publication.json"
    writes: list[Path] = []
    original = gate._atomic_write_bytes

    def recording_write(path: Path, content: bytes) -> None:
        writes.append(Path(path))
        original(path, content)

    monkeypatch.setattr(gate, "_atomic_write_bytes", recording_write)
    gate.publish_result(
        payload,
        result_path=result_path,
        report_path=report_path,
        manifest_path=manifest_path,
    )
    assert writes[-1] == manifest_path
    assert set(writes[:-1]) == {result_path, report_path}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert len(manifest["artifacts"]) == 2
    assert {row["role"] for row in manifest["artifacts"]} == {
        "result-json",
        "readable-report",
    }
    for row in manifest["artifacts"]:
        path = tmp_path / Path(row["path"]).name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
    assert "manifest_sha256" not in manifest


def _classify_witness(gate, payload: dict[str, object], **gate_updates: object) -> None:
    gates = payload["classification"]["gates"]
    gates.update(gate_updates)
    classification = gate.classify_horizon(
        gates,
        lower_tail_status=payload["classification"]["lower_tail_status"],
    )
    payload["classification"].update(classification)
    payload["classification"]["finite_large_h_stability_only"] = bool(
        gates["G5"] == "pass" and gates["G4"] != "pass"
    )


def test_v3_contract_serializes_a_dependent_root_ladder_stop(gate) -> None:
    payload = gate.contract_witness()
    payload["finite_branch"]["root_panels"][4:] = [None, None, None]
    payload["finite_branch"]["homotopies"][1:4] = [None, None, None]
    payload["finite_branch"]["drift"]["center_diagnostics"] = [None, None]
    payload["finite_branch"]["drift"]["interval_upper_bounds"] = [None, None]
    payload["finite_branch"]["drift"]["pass"] = False
    payload["infinite_tail"]["certificate_panels"] = [None, None]
    payload["infinite_tail"]["panel_comparison"]["intersection"] = None
    payload["infinite_tail"]["panel_comparison"]["overlap"] = False
    payload["stability"]["continuation_arms"] = [None, None, None]
    payload["stability"]["exact_arm"] = None
    payload["stability"]["rounded_root"] = None
    for panel in payload["stability"]["arnoldi"].values():
        if isinstance(panel, dict) and "eigenpairs" in panel:
            panel["eigenpairs"] = [None] * len(panel["eigenpairs"])
            panel["status"] = "arpack-no-convergence"
    payload["stability"]["arnoldi"]["panel_agreement"] = {
        "leading_transverse_distance": None,
        "pass": False,
        "symmetry_pass": False,
    }
    payload["stability"]["gates"] = gate._stability_evidence(payload)
    _classify_witness(
        gate,
        payload,
        G1F="inconclusive",
        G2F="inconclusive",
        G3="inconclusive",
        G4="inconclusive",
        G5="inconclusive",
    )
    gate.validate_result(payload)


def test_v3_contract_serializes_a_homotopy_prefix_stop(gate) -> None:
    payload = gate.contract_witness()
    homotopy = payload["finite_branch"]["homotopies"][1]
    homotopy["slabs"][11:] = [None] * 53
    homotopy["slabs"][10]["strict_interior"] = False
    homotopy["slabs"][10]["krawczyk_image"][0][0] = homotopy["slabs"][10]["box"]["radius"][0]
    homotopy["pass"] = False
    homotopy["status"] = "inconclusive"
    payload["finite_branch"]["homotopies"][2:4] = [None, None]
    _classify_witness(gate, payload, G2F="inconclusive")
    gate.validate_result(payload)


def test_v3_contract_serializes_partial_and_missing_vector_arnoldi(gate) -> None:
    partial = gate.contract_witness()
    panel = partial["stability"]["arnoldi"]["primary"]
    panel["eigenpairs"][7:] = [None] * 17
    panel["status"] = "arpack-no-convergence"
    partial["stability"]["arnoldi"]["panel_agreement"].update(
        {"pass": False, "symmetry_pass": False}
    )
    partial["stability"]["gates"] = gate._stability_evidence(partial)
    _classify_witness(gate, partial, G5="inconclusive")
    gate.validate_result(partial)

    missing = gate.contract_witness()
    missing_panel = missing["stability"]["arnoldi"]["primary"]
    missing_panel["eigenpairs"][0]["vector"] = None
    missing_panel["status"] = "missing-vectors"
    missing["stability"]["arnoldi"]["panel_agreement"].update(
        {"pass": False, "symmetry_pass": False}
    )
    missing["stability"]["gates"] = gate._stability_evidence(missing)
    _classify_witness(gate, missing, G5="inconclusive")
    gate.validate_result(missing)


def test_v3_contract_serializes_early_trajectory_stop(gate) -> None:
    payload = gate.contract_witness()
    arm = payload["stability"]["continuation_arms"][0]
    arm["samples"][5:] = [None] * 496
    arm["completed"] = False
    arm["stopped"] = True
    payload["stability"]["gates"] = gate._stability_evidence(payload)
    _classify_witness(gate, payload, G5="inconclusive")
    gate.validate_result(payload)


def test_v3_contract_rejects_null_holes_and_positive_gates_after_stop(gate) -> None:
    hole = gate.contract_witness()
    hole["stability"]["continuation_arms"][0]["samples"][2] = None
    with pytest.raises(ValueError, match="prefix"):
        gate.validate_result(hole)

    false_pass = gate.contract_witness()
    false_pass["finite_branch"]["root_panels"][6] = None
    false_pass["finite_branch"]["homotopies"][3] = None
    false_pass["finite_branch"]["drift"]["center_diagnostics"][1] = None
    false_pass["finite_branch"]["drift"]["interval_upper_bounds"][1] = None
    false_pass["finite_branch"]["drift"]["pass"] = False
    false_pass["infinite_tail"]["certificate_panels"] = [None, None]
    false_pass["infinite_tail"]["panel_comparison"]["intersection"] = None
    false_pass["infinite_tail"]["panel_comparison"]["overlap"] = False
    with pytest.raises(ValueError, match="G1F"):
        gate.validate_result(false_pass)


def test_v3_contract_rejects_evidence_summary_and_instability_lies(gate) -> None:
    partial = gate.contract_witness()
    partial["stability"]["arnoldi"]["primary"]["eigenpairs"][-1] = None
    partial["stability"]["arnoldi"]["primary"]["status"] = (
        "arpack-no-convergence"
    )
    partial["stability"]["arnoldi"]["panel_agreement"].update(
        {"pass": False, "symmetry_pass": False}
    )
    with pytest.raises(ValueError, match="stability.gates"):
        gate.validate_result(partial)

    control = gate.contract_witness()
    control["controls"]["circular_cases"][0]["pass"] = False
    with pytest.raises(ValueError, match="controls.pass"):
        gate.validate_result(control)


def _fake_interval_certificate(*, passed: bool = True) -> dict[str, object]:
    def interval(lower: str, upper: str) -> dict[str, str]:
        return {"lower": lower, "upper": upper}

    return {
        "box": [interval("0.9", "1.0"), interval("0.01", "0.02")],
        "jacobian_box": [
            [interval("1", "1.1"), interval("2", "2.1")],
            [interval("3", "3.1"), interval("4", "4.1")],
        ],
        "krawczyk_image": [
            interval("0.94", "0.96"),
            interval("0.014", "0.016"),
        ],
        "gates": {"krawczyk_strict_interior": passed},
        "pass": passed,
    }


def test_finite_root_adapter_reuses_interval_library_and_maps_v3(
    gate, monkeypatch
) -> None:
    calls: list[tuple[str, dict[str, object]]] = []

    def fake_refine(**kwargs):
        calls.append(("refine", kwargs))
        return {
            "radius": "0.95",
            "theta": "0.015",
            "balance": ["1e-70", "-2e-70"],
            "jacobian": [["1", "2"], ["3", "4"]],
        }

    def fake_certify(**kwargs):
        calls.append(("certify", kwargs))
        return _fake_interval_certificate()

    monkeypatch.setattr(
        gate, "refine_rotating_wave_root", fake_refine, raising=False
    )
    monkeypatch.setattr(
        gate, "certify_rotating_wave_box", fake_certify, raising=False
    )
    record = gate.finite_root_backend_record(
        horizon=1500,
        precision_dps=80,
        start=("0.946", "0.0157"),
    )

    assert [name for name, _ in calls] == ["refine", "certify", "certify"]
    refine = calls[0][1]
    assert refine["iterations"] == 8
    assert refine["precision_dps"] == 80
    assert refine["radius"] == "0.946"
    assert refine["theta"] == "0.0157"
    assert refine["parameters"].horizon == 1500
    assert refine["parameters"].alpha == "0.01"
    assert refine["parameters"].eta == "0.15"
    assert [call[1]["radius_half_width"] for call in calls[1:]] == [
        "1e-8",
        "1e-30",
    ]
    assert record["newton"] == {
        "jacobian": [["1", "2"], ["3", "4"]],
        "precision_dps": 80,
        "radius": "0.95",
        "residual": ["1e-70", "-2e-70"],
        "steps": 8,
        "theta": "0.015",
    }
    assert record["outer_certificate"]["box"] == {
        "radius": ["0.9", "1.0"],
        "theta": ["0.01", "0.02"],
    }
    assert record["inner_certificate"]["krawczyk_image"] == [
        ["0.94", "0.96"],
        ["0.014", "0.016"],
    ]


def test_finite_root_adapter_fails_closed_on_certificate_failure(
    gate, monkeypatch
) -> None:
    monkeypatch.setattr(
        gate,
        "refine_rotating_wave_root",
        lambda **kwargs: {
            "radius": "0.95",
            "theta": "0.015",
            "balance": ["0", "0"],
            "jacobian": [["1", "0"], ["0", "1"]],
        },
        raising=False,
    )
    certificates = iter(
        [_fake_interval_certificate(), _fake_interval_certificate(passed=False)]
    )
    monkeypatch.setattr(
        gate,
        "certify_rotating_wave_box",
        lambda **kwargs: next(certificates),
        raising=False,
    )

    assert gate.finite_root_backend_record(
        horizon=1500,
        precision_dps=120,
        start=("0.946", "0.0157"),
    ) is None


@pytest.mark.parametrize(
    ("horizon", "precision", "start", "error"),
    [
        (1500.0, 80, ("0.946", "0.0157"), ValueError),
        (1500, 160, ("0.946", "0.0157"), ValueError),
        (1500, True, ("0.946", "0.0157"), ValueError),
        (1500, 80, ["0.946", "0.0157"], TypeError),
        (1500, 80, ("nan", "0.0157"), ValueError),
    ],
)
def test_finite_root_adapter_rejects_nonregistered_inputs(
    gate, horizon, precision, start, error
) -> None:
    with pytest.raises(error):
        gate.finite_root_backend_record(
            horizon=horizon,
            precision_dps=precision,
            start=start,
        )


def _fake_homotopy_certificate(
    *,
    radius: str = "0.95",
    theta: str = "0.015",
    radius_half_width: str = "1e-4",
    theta_half_width: str = "1e-6",
    passed: bool = True,
    **kwargs,
) -> dict[str, object]:
    def interval(center: str, half_width: str) -> dict[str, str]:
        with localcontext() as context:
            context.prec = 180
            midpoint = Decimal(center)
            width = Decimal(half_width)
            return {
                "lower": format(midpoint - width, "f"),
                "upper": format(midpoint + width, "f"),
            }

    box = [
        interval(radius, radius_half_width),
        interval(theta, theta_half_width),
    ]
    image = [interval(radius, "5e-5"), interval(theta, "5e-7")]
    record = {
        "box": box,
        "krawczyk_image": image,
        "gates": {"krawczyk_strict_interior": passed},
        "pass": passed,
    }
    if not passed:
        record["krawczyk_image"][0]["lower"] = record["box"][0]["lower"]
    return record


def test_homotopy_adapter_uses_exact_fixed_slab_partition(gate, monkeypatch) -> None:
    calls: list[dict[str, object]] = []

    def fake_homotopy(**kwargs):
        calls.append(kwargs)
        return _fake_homotopy_certificate(**kwargs)

    monkeypatch.setattr(
        gate,
        "certify_rotating_wave_homotopy_box",
        fake_homotopy,
        raising=False,
    )
    payload = gate.contract_witness()
    first = payload["finite_branch"]["root_panels"][2]["newton_120"]
    second = payload["finite_branch"]["root_panels"][3]["newton_120"]
    row = gate.homotopy_backend_record(
        from_horizon=1200,
        to_horizon=1500,
        from_root=(first["radius"], first["theta"]),
        to_root=(second["radius"], second["theta"]),
    )

    assert len(calls) == 64
    assert calls[0]["s_interval"] == ("0", "0.015625")
    assert calls[-1]["s_interval"] == ("0.984375", "1")
    assert calls[0]["radius_half_width"] == "1e-4"
    assert calls[0]["theta_half_width"] == "1e-6"
    assert calls[0]["precision_dps"] == 120
    assert calls[0]["first_parameters"].horizon == 1200
    assert calls[0]["second_parameters"].horizon == 1500
    assert row["status"] == "pass"
    assert row["pass"] is True
    assert len(row["slabs"]) == 64
    assert row["slabs"][0]["overlaps_previous"] is None
    assert all(slab["overlaps_previous"] for slab in row["slabs"][1:])

    payload["finite_branch"]["homotopies"][0] = row
    gate.validate_result(payload)


def test_homotopy_adapter_stops_after_first_failed_slab(gate, monkeypatch) -> None:
    calls = 0

    def fake_homotopy(**kwargs):
        nonlocal calls
        calls += 1
        return _fake_homotopy_certificate(passed=calls != 11, **kwargs)

    monkeypatch.setattr(
        gate,
        "certify_rotating_wave_homotopy_box",
        fake_homotopy,
        raising=False,
    )
    row = gate.homotopy_backend_record(
        from_horizon=1200,
        to_horizon=1500,
        from_root=("0.95", "0.015"),
        to_root=("0.95", "0.015"),
    )

    assert calls == 11
    assert row["status"] == "inconclusive"
    assert row["pass"] is False
    assert row["slabs"][10]["strict_interior"] is False
    assert row["slabs"][11:] == [None] * 53


def test_homotopy_adapter_stops_on_nonoverlapping_root_tubes(
    gate, monkeypatch
) -> None:
    calls = 0

    def fake_homotopy(**kwargs):
        nonlocal calls
        calls += 1
        record = _fake_homotopy_certificate(**kwargs)
        if calls == 2:
            record["box"] = [
                {"lower": "1.0", "upper": "1.1"},
                {"lower": "0.01", "upper": "0.02"},
            ]
            record["krawczyk_image"] = [
                {"lower": "1.04", "upper": "1.06"},
                {"lower": "0.014", "upper": "0.016"},
            ]
        return record

    monkeypatch.setattr(
        gate,
        "certify_rotating_wave_homotopy_box",
        fake_homotopy,
        raising=False,
    )
    row = gate.homotopy_backend_record(
        from_horizon=1200,
        to_horizon=1500,
        from_root=("0.94", "0.015"),
        to_root=("0.96", "0.016"),
    )

    assert calls == 2
    assert row["status"] == "inconclusive"
    assert row["slabs"][1]["strict_interior"] is True
    assert row["slabs"][1]["overlaps_previous"] is False
    assert row["slabs"][2:] == [None] * 62


def test_homotopy_adapter_turns_numeric_singularity_into_inconclusive(
    gate, monkeypatch
) -> None:
    def singular(**kwargs):
        raise ArithmeticError("singular")

    monkeypatch.setattr(
        gate,
        "certify_rotating_wave_homotopy_box",
        singular,
        raising=False,
    )

    row = gate.homotopy_backend_record(
        from_horizon=1200,
        to_horizon=1500,
        from_root=("0.94", "0.015"),
        to_root=("0.96", "0.016"),
    )

    assert row["status"] == "inconclusive"
    assert row["pass"] is False
    assert row["slabs"] == [None] * 64


class _SyntheticRunnerBackend:
    """Primitive donor backend for target-free orchestration tests only."""

    def __init__(
        self,
        gate,
        *,
        failed_root: tuple[int, int] | None = None,
        failed_homotopy: tuple[int, int] | None = None,
        failed_tail_precision: int | None = None,
        complete_exclusion: bool = False,
        incomplete_exclusion: bool = False,
        partial_arnoldi: bool = False,
        stopped_arm: str | None = None,
    ) -> None:
        self.donor = gate.contract_witness()
        self.failed_root = failed_root
        self.failed_homotopy = failed_homotopy
        self.failed_tail_precision = failed_tail_precision
        self.complete_exclusion = complete_exclusion
        self.incomplete_exclusion = incomplete_exclusion
        self.partial_arnoldi = partial_arnoldi
        self.stopped_arm = stopped_arm
        self.calls: list[tuple[object, ...]] = []
        self._roots = {
            panel["horizon"]: panel
            for panel in self.donor["finite_branch"]["root_panels"]
        }
        self._homotopies = {
            (row["from_horizon"], row["to_horizon"]): row
            for row in self.donor["finite_branch"]["homotopies"]
        }

    def direct_replay(self) -> bool:
        self.calls.append(("direct-replay",))
        return True

    def finite_root_panel(
        self,
        *,
        horizon: int,
        precision_dps: int,
        start: tuple[str, str],
    ) -> dict[str, object] | None:
        self.calls.append(("root", horizon, precision_dps, start))
        if self.failed_root == (horizon, precision_dps):
            return None
        panel = self._roots[horizon]
        return copy.deepcopy(
            {
                "newton": panel[f"newton_{precision_dps}"],
                "outer_certificate": panel[f"outer_certificate_{precision_dps}"],
                "inner_certificate": panel[f"inner_certificate_{precision_dps}"],
            }
        )

    def homotopy_edge(
        self,
        *,
        from_horizon: int,
        to_horizon: int,
        from_root: tuple[str, str],
        to_root: tuple[str, str],
    ) -> dict[str, object]:
        self.calls.append(
            ("homotopy", from_horizon, to_horizon, from_root, to_root)
        )
        row = copy.deepcopy(self._homotopies[(from_horizon, to_horizon)])
        if self.failed_homotopy == (from_horizon, to_horizon):
            row["slabs"][11:] = [None] * 53
            row["slabs"][10]["strict_interior"] = False
            row["slabs"][10]["krawczyk_image"][0][0] = row["slabs"][10][
                "box"
            ]["radius"][0]
            row["pass"] = False
            row["status"] = "inconclusive"
        return row

    def local_branch_exclusion(
        self,
        *,
        from_horizon: int,
        to_horizon: int,
        previous_root: tuple[str, str],
    ) -> dict[str, object] | None:
        self.calls.append(
            ("exclusion", from_horizon, to_horizon, previous_root)
        )
        if self.incomplete_exclusion or self.complete_exclusion:
            radius = Decimal(previous_root[0])
            theta = Decimal(previous_root[1])
            local_domain = {
                "radius": [
                    format(radius - Decimal("0.02"), "f"),
                    format(radius + Decimal("0.02"), "f"),
                ],
                "theta": [
                    format(theta - Decimal("0.002"), "f"),
                    format(theta + Decimal("0.002"), "f"),
                ],
            }
            leaves = [
                {
                    "box": {
                        "radius": copy.deepcopy(local_domain["radius"]),
                        "theta": [local_domain["theta"][0], previous_root[1]],
                    },
                    "classification": "residual-excluded",
                    "depth": 1,
                    "krawczyk_image": None,
                    "residual_box": [["1", "2"], ["-1", "1"]],
                    "strict_interior": None,
                }
            ]
            if self.complete_exclusion:
                leaves.append(
                    {
                        "box": {
                            "radius": copy.deepcopy(local_domain["radius"]),
                            "theta": [previous_root[1], local_domain["theta"][1]],
                        },
                        "classification": "residual-excluded",
                        "depth": 1,
                        "krawczyk_image": None,
                        "residual_box": [["1", "2"], ["-1", "1"]],
                        "strict_interior": None,
                    }
                )
            return {
                "from_horizon": from_horizon,
                "to_horizon": to_horizon,
                "local_domain": local_domain,
                "max_depth": 20,
                "status": "all-residual-excluded",
                "leaves": leaves,
            }
        return None

    def tail_certificate_panel(
        self, *, precision_dps: int, root: tuple[str, str]
    ) -> dict[str, object] | None:
        self.calls.append(("tail", precision_dps, root))
        if precision_dps == self.failed_tail_precision:
            return None
        index = {120: 0, 160: 1}[precision_dps]
        return copy.deepcopy(
            self.donor["infinite_tail"]["certificate_panels"][index]
        )

    def arnoldi_panel(
        self,
        *,
        name: str,
        rounded_root: tuple[float, float],
        start: list[float],
    ) -> dict[str, object]:
        self.calls.append(("arnoldi", name, rounded_root, len(start)))
        panel = copy.deepcopy(self.donor["stability"]["arnoldi"][name])
        if self.partial_arnoldi and name == "primary":
            panel["eigenpairs"][7:] = [None] * 17
            panel["status"] = "arpack-no-convergence"
        return panel

    def continuation_arm(
        self,
        *,
        name: str,
        rounded_root: tuple[float, float],
        perturbation: list[float],
    ) -> dict[str, object]:
        self.calls.append(("arm", name, rounded_root, len(perturbation)))
        by_name = {
            row["name"]: row
            for row in self.donor["stability"]["continuation_arms"]
        }
        arm = copy.deepcopy(by_name[name])
        if name == self.stopped_arm:
            arm["samples"][5:] = [None] * 496
            arm["completed"] = False
            arm["stopped"] = True
        return arm

    def exact_arm(self, *, rounded_root: tuple[float, float]) -> dict[str, object]:
        self.calls.append(("exact-arm", rounded_root))
        return copy.deepcopy(self.donor["stability"]["exact_arm"])

    def controls(self) -> dict[str, object]:
        self.calls.append(("controls",))
        return copy.deepcopy(self.donor["controls"])


def _orchestrate(gate, backend: _SyntheticRunnerBackend) -> dict[str, object]:
    donor = backend.donor
    return gate.orchestrate_horizon_transfer(
        backend=backend,
        identity=copy.deepcopy(donor["identity"]),
        publication=copy.deepcopy(donor["publication"]),
    )


def test_runner_red_orchestrates_registered_stages_without_publication(
    gate, monkeypatch
) -> None:
    backend = _SyntheticRunnerBackend(gate)

    def forbidden_publish(*args, **kwargs):
        raise AssertionError("target-free orchestration attempted publication")

    monkeypatch.setattr(gate, "publish_result", forbidden_publish)
    payload = _orchestrate(gate, backend)
    gate.validate_result(payload)

    root_calls = [call[1:3] for call in backend.calls if call[0] == "root"]
    assert root_calls == [
        (horizon, precision)
        for horizon in (1200, 1500, 1800, 2400, 3600, 900, 600)
        for precision in (80, 120)
    ]
    assert [call[1:3] for call in backend.calls if call[0] == "homotopy"] == [
        (1200, 1500),
        (1500, 1800),
        (1800, 2400),
        (2400, 3600),
        (1200, 900),
        (900, 600),
    ]
    assert [call[1] for call in backend.calls if call[0] == "tail"] == [120, 160]
    assert [call[1] for call in backend.calls if call[0] == "arnoldi"] == [
        "primary",
        "convergence",
    ]
    assert backend.calls[-1] == ("controls",)


def test_runner_red_root_stop_is_fail_closed_but_lower_tail_is_independent(gate) -> None:
    backend = _SyntheticRunnerBackend(gate, failed_root=(1500, 80))
    payload = _orchestrate(gate, backend)
    gate.validate_result(payload)

    assert payload["finite_branch"]["root_panels"][3:] == [None] * 4
    assert all(payload["finite_branch"]["root_panels"][index] for index in (0, 1, 2))
    assert any(call[:3] == ("exclusion", 1200, 1500) for call in backend.calls)
    assert not any(
        call[0] in {"tail", "arnoldi", "arm", "exact-arm"}
        for call in backend.calls
    )
    assert payload["classification"]["gates"]["G1F"] == "inconclusive"
    assert payload["classification"]["p5_governance_review_open"] is False


def test_runner_red_partial_arnoldi_never_invents_trajectory_evidence(gate) -> None:
    backend = _SyntheticRunnerBackend(gate, partial_arnoldi=True)
    payload = _orchestrate(gate, backend)
    gate.validate_result(payload)

    assert not any(call[0] in {"arm", "exact-arm"} for call in backend.calls)
    assert payload["stability"]["continuation_arms"] == [None, None, None]
    assert payload["stability"]["exact_arm"] is None
    assert payload["classification"]["gates"]["G5"] == "inconclusive"
    assert payload["classification"]["p5_governance_review_open"] is False


def test_runner_homotopy_stop_keeps_prefix_and_invokes_exclusion(gate) -> None:
    backend = _SyntheticRunnerBackend(gate, failed_homotopy=(1200, 1500))
    payload = _orchestrate(gate, backend)
    gate.validate_result(payload)

    first = payload["finite_branch"]["homotopies"][0]
    assert first["slabs"][:10] == backend._homotopies[(1200, 1500)]["slabs"][:10]
    assert first["slabs"][10]["strict_interior"] is False
    assert first["slabs"][11:] == [None] * 53
    assert payload["finite_branch"]["homotopies"][1:4] == [None] * 3
    assert all(payload["finite_branch"]["homotopies"][index] for index in (4, 5))
    assert any(call[:3] == ("exclusion", 1200, 1500) for call in backend.calls)
    assert payload["classification"]["gates"]["G2F"] == "inconclusive"


def test_runner_tail_stop_is_inconclusive_and_keeps_finite_stability_separate(gate) -> None:
    backend = _SyntheticRunnerBackend(gate, failed_tail_precision=160)
    payload = _orchestrate(gate, backend)
    gate.validate_result(payload)

    assert payload["infinite_tail"]["certificate_panels"][0] is not None
    assert payload["infinite_tail"]["certificate_panels"][1] is None
    assert payload["infinite_tail"]["panel_comparison"] == {
        "intersection": None,
        "overlap": False,
    }
    assert payload["classification"]["gates"]["G4"] == "inconclusive"
    assert payload["classification"]["finite_large_h_stability_only"] is True
    assert payload["classification"]["p5_governance_review_open"] is False


def test_runner_early_trajectory_stop_preserves_null_suffix(gate) -> None:
    backend = _SyntheticRunnerBackend(gate, stopped_arm="radial")
    payload = _orchestrate(gate, backend)
    gate.validate_result(payload)

    arm = payload["stability"]["continuation_arms"][0]
    assert arm["samples"][4] is not None
    assert arm["samples"][5:] == [None] * 496
    assert arm["completed"] is False
    assert arm["stopped"] is True
    assert payload["classification"]["gates"]["G5"] == "inconclusive"
    assert payload["classification"]["p5_governance_review_open"] is False


def test_runner_red_rejects_exclusion_leaves_that_do_not_partition_domain(gate) -> None:
    backend = _SyntheticRunnerBackend(
        gate,
        failed_root=(1500, 80),
        incomplete_exclusion=True,
    )
    with pytest.raises(ValueError, match="partition"):
        _orchestrate(gate, backend)


def test_runner_accepts_complete_exclusion_partition_only_after_root_stop(gate) -> None:
    backend = _SyntheticRunnerBackend(
        gate,
        failed_root=(1500, 80),
        complete_exclusion=True,
    )
    payload = _orchestrate(gate, backend)
    gate.validate_result(payload)
    assert payload["classification"]["decision"] == (
        "registered-local-horizon-branch-loss"
    )
    assert payload["classification"]["p5_governance_review_open"] is False


def test_validator_rejects_complete_exclusion_when_target_root_exists(gate) -> None:
    backend = _SyntheticRunnerBackend(
        gate,
        failed_homotopy=(1200, 1500),
        complete_exclusion=True,
    )
    with pytest.raises(ValueError, match="target root"):
        _orchestrate(gate, backend)

    instability = gate.contract_witness()
    instability["classification"]["gates"][
        "large_h_instability_supported"
    ] = True
    with pytest.raises(ValueError, match="large_h_instability_supported"):
        gate.validate_result(instability)


def test_v3_contract_rejects_root_certificate_and_center_mutations(gate) -> None:
    missing = gate.contract_witness()
    missing["finite_branch"]["root_panels"][2]["outer_certificate_80"] = None
    with pytest.raises((TypeError, ValueError), match="outer_certificate_80"):
        gate.validate_result(missing)

    center = gate.contract_witness()
    center["finite_branch"]["root_panels"][2]["newton_80"]["radius"] = (
        "0.9465175048042250000000000000000000000001"
    )
    with pytest.raises(ValueError, match="center|centers_agree"):
        gate.validate_result(center)

    intersection = gate.contract_witness()
    intersection["finite_branch"]["root_panels"][2]["inner_intersection"][
        "radius"
    ][0] = "0"
    with pytest.raises(ValueError, match="inner_intersection"):
        gate.validate_result(intersection)

    inclusion = gate.contract_witness()
    certificate = inclusion["finite_branch"]["root_panels"][2][
        "outer_certificate_80"
    ]
    certificate["krawczyk_image"][0][0] = certificate["box"]["radius"][0]
    certificate["strict_interior"] = False
    with pytest.raises(ValueError, match="G1F"):
        gate.validate_result(inclusion)


def test_v3_contract_serializes_disjoint_inner_images_as_inconclusive(gate) -> None:
    payload = gate.contract_witness()
    panel = payload["finite_branch"]["root_panels"][0]
    radius = "0.946517504804225"
    with localcontext() as context:
        context.prec = 180
        center = Decimal(radius)
        panel["inner_certificate_80"]["krawczyk_image"][0] = [
            format(center - Decimal("9e-31"), "f"),
            format(center - Decimal("8e-31"), "f"),
        ]
        panel["inner_certificate_120"]["krawczyk_image"][0] = [
            format(center + Decimal("8e-31"), "f"),
            format(center + Decimal("9e-31"), "f"),
        ]
    panel["inner_intersection"] = None
    _classify_witness(gate, payload, G1R="inconclusive")
    gate.validate_result(payload)


def test_v3_contract_rejects_homotopy_and_tail_reconstruction_lies(gate) -> None:
    s_interval = gate.contract_witness()
    s_interval["finite_branch"]["homotopies"][0]["slabs"][7]["s_interval"] = [
        "0",
        "1",
    ]
    with pytest.raises(ValueError, match="s_interval"):
        gate.validate_result(s_interval)

    center = gate.contract_witness()
    box = center["finite_branch"]["homotopies"][0]["slabs"][7]["box"]["radius"]
    with localcontext() as context:
        context.prec = 180
        box[:] = [format(Decimal(value) + Decimal("1e-8"), "f") for value in box]
    with pytest.raises(ValueError, match="center mismatch"):
        gate.validate_result(center)

    overlap = gate.contract_witness()
    slab = overlap["finite_branch"]["homotopies"][0]["slabs"][1]
    with localcontext() as context:
        context.prec = 180
        shifted = Decimal("0.946517504804225") + Decimal("6.5e-5")
        slab["krawczyk_image"][0] = gate._decimal_box(
            format(shifted, "f"), "5e-6"
        )
    with pytest.raises(ValueError, match="overlaps_previous"):
        gate.validate_result(overlap)

    tail = gate.contract_witness()
    tail["infinite_tail"]["panel_comparison"]["intersection"]["theta"][0] = "0"
    with pytest.raises(ValueError, match="panel_comparison"):
        gate.validate_result(tail)


def test_v3_contract_rejects_unproved_exclusion_leaf(gate) -> None:
    payload = gate.contract_witness()
    contract = gate._load_result_schema()
    attempt = gate._witness_value(
        "object:branch_exclusion", contract, fill_nullable=True
    )
    attempt.update(
        {
            "from_horizon": 1200,
            "to_horizon": 1500,
            "local_domain": {
                "radius": ["0.926517504804225", "0.966517504804225"],
                "theta": ["0.013770381717135", "0.017770381717135"],
            },
            "max_depth": 20,
            "status": "all-residual-excluded",
        }
    )
    leaf = attempt["leaves"][0]
    leaf.update(
        {
            "box": copy.deepcopy(attempt["local_domain"]),
            "classification": "residual-excluded",
            "depth": 0,
            "residual_box": [["-1", "1"], ["-1", "1"]],
            "krawczyk_image": None,
            "strict_interior": None,
        }
    )
    payload["finite_branch"]["exclusions"][0] = attempt
    with pytest.raises(ValueError, match="does not exclude zero"):
        gate.validate_result(payload)


def test_v3_contract_rejects_stability_input_mutations(gate) -> None:
    start = gate.contract_witness()
    start["stability"]["arnoldi"]["primary"]["start_sha256"] = "0" * 64
    with pytest.raises((TypeError, ValueError), match="start_sha256"):
        gate.validate_result(start)

    perturbation_hash = gate.contract_witness()
    perturbation_hash["stability"]["continuation_arms"][0][
        "perturbation_sha256"
    ] = "0" * 64
    with pytest.raises(ValueError, match="perturbation_sha256"):
        gate.validate_result(perturbation_hash)

    perturbation_vector = gate.contract_witness()
    perturbation_vector["stability"]["continuation_arms"][2]["perturbation"][3] = 1.0
    with pytest.raises(ValueError, match="perturbation"):
        gate.validate_result(perturbation_vector)

    rounded = gate.contract_witness()
    rounded["stability"]["rounded_root"][0] += 1e-12
    with pytest.raises(ValueError, match="rounded_root"):
        gate.validate_result(rounded)

    dimensionality = gate.contract_witness()
    dimensionality["finite_branch"]["root_panels"][0]["inner_certificate_80"][
        "krawczyk_image"
    ].pop()
    with pytest.raises((TypeError, ValueError), match="krawczyk_image"):
        gate.validate_result(dimensionality)


def test_v3_arnoldi_starts_have_portable_registered_hashes(gate) -> None:
    assert gate._arnoldi_start_hashes() == {
        "primary": "572db16bc576c2eabe9b45af772338780c058e8d148eff00d2cc3041861d1382",
        "convergence": "29efa5c8c189a296b4610f3bfef60ecdba585dd29ffec62baf89af0d1aa8d7f6",
    }


def test_v3_contract_rejects_spectral_summary_lies(gate) -> None:
    classification = gate.contract_witness()
    pair = classification["stability"]["arnoldi"]["primary"]["eigenpairs"][3]
    pair["translation_overlap"] = 1.0
    with pytest.raises(ValueError, match="classification"):
        gate.validate_result(classification)

    modulus = gate.contract_witness()
    modulus["stability"]["arnoldi"]["primary"]["eigenpairs"][3]["modulus"] = 0.8
    with pytest.raises(ValueError, match="modulus"):
        gate.validate_result(modulus)

    agreement = gate.contract_witness()
    agreement["stability"]["arnoldi"]["panel_agreement"][
        "leading_transverse_distance"
    ] = 1e-6
    with pytest.raises(ValueError, match="leading_transverse_distance"):
        gate.validate_result(agreement)


def test_v3_contract_rejects_trajectory_and_control_summary_lies(gate) -> None:
    trajectory = gate.contract_witness()
    trajectory["stability"]["continuation_arms"][0]["final_ratio"] = 0.04
    with pytest.raises(ValueError, match="trajectory summary"):
        gate.validate_result(trajectory)

    exact = gate.contract_witness()
    exact["stability"]["exact_arm"]["maximum_distance"] = 1e-12
    with pytest.raises(ValueError, match="maximum_distance"):
        gate.validate_result(exact)

    control = gate.contract_witness()
    control["controls"]["circular_cases"][0]["pass"] = False
    with pytest.raises(ValueError, match="controls.pass"):
        gate.validate_result(control)
