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


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_transfer_result_schema_v1.json"
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
    if ":" not in specification:
        return None
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
        with localcontext() as context:
            context.prec = 70
            decimal_power = Decimal(row["decimal_power"])
            expected_decimal = Decimal("0.99") ** horizon
            assert abs(decimal_power / expected_decimal - 1) < Decimal("1e-65")
    assert rows[-1]["direct_power"] > 0.0


def test_tail_bounds_equal_the_registered_conservative_formulas(gate) -> None:
    phi0 = 1.0 + 3.5 / 9.0
    phi1 = math.exp(-0.5) * (1.0 + 3.5 / 27.0)
    q = 0.99
    for horizon in HORIZONS:
        observed = gate.tail_bounds(horizon=horizon, precision_dps=80)
        expected = {
            "residual_bound": 2.0 * 0.15 * phi0 * q**horizon,
            "jacobian_radius_bound": 4.0 * 0.15 * phi1 * q**horizon,
            "jacobian_theta_bound": 0.15
            * (phi0 + 2.0 * 1.1 * phi1)
            * q**horizon
            * (horizon + q / 0.01),
        }
        for name, value in expected.items():
            assert float(observed[name]) >= value
            assert float(observed[name]) <= math.nextafter(value, math.inf) * (1.0 + 2e-15)


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
    history = np.column_stack((0.1 * ages**2, np.sin(0.23 * ages)))
    record = gate.run_circular_control(history, parameters=PARAMETERS, mutation=mutation)
    assert record["pass"] is False
    assert record["mutation"] == mutation


def test_eta_zero_history_collapses_to_latest_point(gate) -> None:
    ages = np.arange(17, dtype=float)
    history = np.column_stack((ages / 17.0, np.cos(0.3 * ages)))
    collapsed = gate.eta_zero_collapse(history, steps=18)
    expected = np.repeat(history[[0]], 17, axis=0)
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
