from __future__ import annotations

import copy
from decimal import Decimal, localcontext
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g5_component_gate.py"
)
AUDITOR_PATH = ROOT / (
    "experiments/current/dynamics/rotation/"
    "scalar_memory_rotating_wave_horizon_g5_component_result_audit.py"
)


def _load():
    specification = importlib.util.spec_from_file_location(
        "g5_component_runner_under_test", RUNNER_PATH
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


@pytest.fixture
def runner():
    return _load()


@pytest.fixture
def auditor():
    specification = importlib.util.spec_from_file_location(
        "g5_component_auditor_under_test", AUDITOR_PATH
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def _certificate(root: tuple[str, str], half_width: str):
    with localcontext() as context:
        context.prec = 180
        width = Decimal(half_width)
        centers = [Decimal(value) for value in root]
        return {
            "box": {
                coordinate: [
                    format(center - width, "f"),
                    format(center + width, "f"),
                ]
                for coordinate, center in zip(
                    ("radius", "theta"), centers, strict=True
                )
            },
            "interval_backend": "mpmath.iv",
            "jacobian_box": [
                [["1", "1"], ["0", "0"]],
                [["0", "0"], ["1", "1"]],
            ],
            "krawczyk_image": [
                [format(center, "f"), format(center, "f")] for center in centers
            ],
            "strict_interior": True,
        }


def _finite(root: tuple[str, str] = ("0.95", "0.015")):
    return {
        "inner_certificate": _certificate(root, "1e-30"),
        "newton": {
            "jacobian": [["1", "0"], ["0", "1"]],
            "precision_dps": 120,
            "radius": root[0],
            "residual": ["0", "0"],
            "steps": 8,
            "theta": root[1],
        },
        "outer_certificate": _certificate(root, "1e-8"),
    }


def _preflight(runner, *, passed: bool):
    root = _finite()["newton"]
    gates = {
        "finite": True,
        "fixed_point": passed,
        "jacobian_structure": True,
        "native_circle_covariance": True,
        "pass": passed,
        "symmetries": True,
        "weight_identity": True,
    }
    retained = 1.0 - 0.99**2400
    record = {
        "candidate": {
            "candidate_id": "fixed-alpha-horizon-h2400-v1",
            "horizon": 2400,
            "radius": float(root["radius"]),
            "theta": float(root["theta"]),
        },
        "equation": {
            "alpha": 0.01,
            "amplitude_att": 3.5,
            "amplitude_rep": 1.0,
            "deposition_weight": 0.01,
            "equation_id": runner.EQUATION_ID,
            "eta": 0.15,
            "memory_mass": 1.0,
            "noise_amplitude": 0.0,
            "q": 0.99,
            "sigma_att": 3.0,
            "sigma_rep": 1.0,
        },
        "gates": gates,
        "jacobian": {
            "dimension": 4800,
            "nnz": 19196,
            "sha256": "a" * 64,
            "shape": [4800, 4800],
        },
        "memory": {
            "closed_form_retained_weight": retained,
            "direct_retained_weight": retained,
            "identity_absolute_error": 0.0,
        },
        "orbit": {
            "co_rotating_fixed_point_max_abs_error": 0.0 if passed else 2e-14,
            "history_sha256": "b" * 64,
            "native_circle_covariance_max_abs_error": 0.0,
        },
        "portability": "same-platform-binary64-transcendentals",
        "schema": "scalar-memory-rotating-wave-g5-preflight-v1",
        "symmetry": {
            "pass": True,
            "residual_maximum": 1e-10,
            "rotation_relative_residual": 0.0,
            "translation_x_relative_residual": 0.0,
            "translation_y_relative_residual": 0.0,
        },
        "thresholds": {
            "fixed_point_maximum": 1e-14,
            "symmetry_residual_maximum": 1e-10,
        },
    }
    content = json.dumps(
        record, allow_nan=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return {"record": record, "record_sha256": hashlib.sha256(content).hexdigest()}


def _identity(runner):
    return {
        "authorization": {
            "attempt": runner.REGISTERED_ATTEMPT,
            "attempt_receipt_path": runner.ATTEMPT_RECEIPT_PATH,
            "attempt_receipt_sha256": "c" * 64,
            "authorization_id": "00000000-0000-4000-8000-000000000000",
            "ci_run_id": 1,
            "governance_sha256": "d" * 64,
            "implementation_revision": "e" * 40,
            "upstream_revision": "a" * 40,
        },
        "created_utc": "2026-09-14T00:00:00+00:00",
        "dependencies": {"mpmath": "1.3.0", "numpy": "2.4.2", "scipy": "1.17.1"},
        "equation_id": runner.EQUATION_ID,
        "execution_commit": "a" * 40,
        "parameters": copy.deepcopy(runner.PARAMETERS),
        "protocol_path": runner.PROTOCOL.relative_to(runner.ROOT).as_posix(),
        "protocol_sha256": "b" * 64,
        "schema": runner.SCHEMA,
        "start": list(runner.START),
    }


def _publication(runner):
    return {
        "artifacts": [
            {"path": runner.RESULT_NAME, "role": "result-json"},
            {"path": runner.REPORT_NAME, "role": "readable-report"},
        ],
        "manifest_path": runner.MANIFEST_NAME,
        "manifest_published_last": True,
    }


def test_runner_and_auditor_register_only_attempt_3(runner, auditor):
    assert runner.REGISTERED_ATTEMPT == auditor.REGISTERED_ATTEMPT == 3
    assert runner.ATTEMPT_RECEIPT_PATH == auditor.ATTEMPT_RECEIPT_PATH
    assert runner.RESULT_NAME == auditor.RESULT_NAME


class _FiniteFailureBackend:
    def finite_root(self):
        return None

    def __getattr__(self, name):
        raise AssertionError(f"closed stage was called: {name}")


def test_missing_finite_root_closes_every_dependent_stage(runner):
    payload = runner.assemble_component(
        backend=_FiniteFailureBackend(),
        identity=_identity(runner),
        publication=_publication(runner),
    )

    assert payload["finite_root"] is None
    assert payload["preflight"] is None
    assert payload["trajectories"] == {
        "exact_control": None,
        "perturbation_arms": [None, None, None],
    }
    assert payload["classification"]["decision"] == "g5-inconclusive"


class _PreflightBackend:
    def __init__(self, runner, *, passed: bool):
        self.runner = runner
        self.passed = passed
        self.calls = []

    def finite_root(self):
        self.calls.append("finite")
        return _finite()

    def preflight(self, **kwargs):
        self.calls.append(("preflight", kwargs))
        return _preflight(self.runner, passed=self.passed)

    def arnoldi_panel(self, **kwargs):
        self.calls.append(("arnoldi", kwargs["name"]))
        return self.runner._empty_panel(kwargs["name"])

    def __getattr__(self, name):
        raise AssertionError(f"closed stage was called: {name}")


def test_failed_preflight_closes_arnoldi_and_trajectories(runner):
    backend = _PreflightBackend(runner, passed=False)
    payload = runner.assemble_component(
        backend=backend,
        identity=_identity(runner),
        publication=_publication(runner),
    )

    assert [call[0] if isinstance(call, tuple) else call for call in backend.calls] == [
        "finite",
        "preflight",
    ]
    assert payload["classification"]["gates"]["preflight"] is False


def test_complete_preflight_runs_both_panels_but_partial_panels_close_trajectories(runner):
    backend = _PreflightBackend(runner, passed=True)
    payload = runner.assemble_component(
        backend=backend,
        identity=_identity(runner),
        publication=_publication(runner),
    )

    assert backend.calls[2:] == [("arnoldi", "primary"), ("arnoldi", "convergence")]
    assert payload["preflight"]["record"]["gates"]["pass"] is True
    assert payload["trajectories"]["perturbation_arms"] == [None, None, None]
    assert payload["classification"]["decision"] == "g5-inconclusive"


def test_contract_rejects_unknown_fields_and_numpy_scalars(runner):
    payload = runner.assemble_component(
        backend=_FiniteFailureBackend(),
        identity=_identity(runner),
        publication=_publication(runner),
    )
    unknown = copy.deepcopy(payload)
    unknown["extra"] = True
    with pytest.raises(ValueError, match="exact object payload"):
        runner.validate_payload(unknown)

    nonnative = copy.deepcopy(payload)
    nonnative["identity"]["parameters"]["eta"] = np.float64(0.15)
    with pytest.raises(ValueError, match="number"):
        runner.validate_payload(nonnative)


def test_independent_auditor_accepts_targetfree_inconclusive_record(runner, auditor):
    payload = runner.assemble_component(
        backend=_FiniteFailureBackend(),
        identity=_identity(runner),
        publication=_publication(runner),
    )

    result = auditor.audit_payload(payload)

    assert result["pass"] is True
    assert result["decision"] == "g5-inconclusive"
    assert "not independently recomputed" in result["trust_base"]


def test_independent_auditor_rejects_preflight_hash_and_false_decision(runner, auditor):
    backend = _PreflightBackend(runner, passed=True)
    payload = runner.assemble_component(
        backend=backend,
        identity=_identity(runner),
        publication=_publication(runner),
    )
    assert auditor.audit_payload(payload)["pass"] is True

    bad_hash = copy.deepcopy(payload)
    bad_hash["preflight"]["record_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="record_sha256"):
        auditor.audit_payload(bad_hash)

    false_decision = copy.deepcopy(payload)
    false_decision["classification"]["decision"] = (
        "g5-local-direct-stability-pass"
    )
    false_decision["classification"]["G5"] = "pass"
    with pytest.raises(ValueError, match="classification"):
        auditor.audit_payload(false_decision)


def test_independent_auditor_rejects_nonnull_hole(runner, auditor):
    payload = runner.assemble_component(
        backend=_FiniteFailureBackend(),
        identity=_identity(runner),
        publication=_publication(runner),
    )
    pair = _pair(0.9 + 0.0j, "transverse")
    pair["vector"] = [[0.0, 0.0] for _ in range(4800)]
    payload["arnoldi"]["primary"]["eigenpairs"][1] = pair

    with pytest.raises(ValueError, match="prefix"):
        auditor.audit_payload(payload)


def test_independent_auditor_has_no_numerical_or_runner_imports():
    import ast

    tree = ast.parse(AUDITOR_PATH.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".", 1)[0])

    assert imported.isdisjoint({"numpy", "scipy", "mpmath"})
    assert "scalar_memory_rotating_wave_horizon_g5_component_gate" not in imported


def _write_receipt(payload, directory: Path) -> Path:
    authorization = payload["identity"]["authorization"]
    receipt = {
        "attempt": authorization["attempt"],
        "authorization_id": authorization["authorization_id"],
        "ci_run_id": authorization["ci_run_id"],
        "created_utc": "2026-09-15T00:00:00+00:00",
        "governance_sha256": authorization["governance_sha256"],
        "implementation_revision": authorization["implementation_revision"],
        "revision": payload["identity"]["execution_commit"],
        "schema": "scalar-memory-rotating-wave-horizon-g5-attempt-receipt-v1",
    }
    content = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8")
    path = directory / Path(payload["identity"]["authorization"]["attempt_receipt_path"]).name
    path.write_bytes(content)
    authorization["attempt_receipt_sha256"] = hashlib.sha256(content).hexdigest()
    return path


def test_publication_is_manifest_last_nonoverwriting_and_independently_audited(
    runner, auditor, tmp_path
):
    payload = runner.assemble_component(
        backend=_FiniteFailureBackend(),
        identity=_identity(runner),
        publication=_publication(runner),
    )
    receipt = _write_receipt(payload, tmp_path)

    paths = runner.publish_payload(payload, directory=tmp_path)
    audit = auditor.audit_publication(
        result_path=paths["result"],
        report_path=paths["report"],
        manifest_path=paths["manifest"],
        receipt_path=receipt,
    )

    assert audit["publication_pass"] is True
    assert paths["manifest"].stat().st_mtime_ns >= paths["report"].stat().st_mtime_ns
    with pytest.raises(FileExistsError, match="overwrite"):
        runner.publish_payload(payload, directory=tmp_path)


def test_publication_audit_rejects_mutated_companion_report(runner, auditor, tmp_path):
    payload = runner.assemble_component(
        backend=_FiniteFailureBackend(),
        identity=_identity(runner),
        publication=_publication(runner),
    )
    receipt = _write_receipt(payload, tmp_path)
    paths = runner.publish_payload(payload, directory=tmp_path)
    paths["report"].write_text("mutated\n", encoding="utf-8")

    with pytest.raises(ValueError, match="artifact hash"):
        auditor.audit_publication(
            result_path=paths["result"],
            report_path=paths["report"],
            manifest_path=paths["manifest"],
            receipt_path=receipt,
        )


def test_publication_audit_rejects_mutated_attempt_receipt(runner, auditor, tmp_path):
    payload = runner.assemble_component(
        backend=_FiniteFailureBackend(),
        identity=_identity(runner),
        publication=_publication(runner),
    )
    receipt = _write_receipt(payload, tmp_path)
    paths = runner.publish_payload(payload, directory=tmp_path)
    receipt.write_text("{}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="receipt: hash mismatch"):
        auditor.audit_publication(
            result_path=paths["result"],
            report_path=paths["report"],
            manifest_path=paths["manifest"],
            receipt_path=receipt,
        )


def _pair(value: complex, classification: str):
    return {
        "classification": classification,
        "eigenvalue": [value.real, value.imag],
        "modulus": abs(value),
        "normalized_residual": 0.0,
        "rotation_overlap": 1.0 if classification == "rotation" else 0.0,
        "translation_overlap": 1.0 if classification == "translation" else 0.0,
        "vector": [[1.0, 0.0]],
    }


def test_classification_requires_transient_bound_as_well_as_final_contraction(runner):
    theta = 0.015
    translations = [
        _pair(complex(np.cos(theta), np.sin(theta)), "translation"),
        _pair(complex(np.cos(theta), -np.sin(theta)), "translation"),
    ]
    pairs = translations + [_pair(1.0 + 0.0j, "rotation"), _pair(0.8 + 0.1j, "transverse")]
    panels = {
        "primary": {"status": "complete", "eigenpairs": copy.deepcopy(pairs)},
        "convergence": {"status": "complete", "eigenpairs": copy.deepcopy(pairs)},
    }
    panels["panel_agreement"] = runner.panel_agreement(
        panels["primary"], panels["convergence"], theta=theta
    )
    arms = [
        {"completed": True, "stopped": False, "final_ratio": 0.05, "growth_factor": 11.0}
        for _ in range(3)
    ]
    payload = {
        "arnoldi": panels,
        "preflight": {"record": {"gates": {"pass": True}}},
        "trajectories": {
            "exact_control": {"completed": True, "stopped": False, "maximum_distance": 0.0},
            "perturbation_arms": arms,
        },
    }

    result = runner.classification(payload)

    assert result["gates"]["stable_spectrum"] is True
    assert result["gates"]["perturbation_contraction"] is False
    assert result["decision"] == "g5-inconclusive"


def _off_grid_arm():
    dense = [1.0] + [0.05] * 5000
    dense[1] = 2.0
    return {
        "completed": True,
        "dense_distances": dense,
        "final_distance": 0.05,
        "final_ratio": 0.05,
        "growth_factor": 2.0,
        "initial_distance": 1.0,
        "maximum_distance": 2.0,
        "maximum_step": 1,
        "samples": [
            {"distance": dense[10 * index], "step": 10 * index}
            for index in range(501)
        ],
        "stopped": False,
    }


def test_trajectory_summary_uses_dense_trace_for_off_grid_maximum(runner, auditor):
    arm = _off_grid_arm()

    runner._verify_trajectory(arm, path="$.synthetic")
    auditor._verify_trajectory(arm, path="$.synthetic")


@pytest.mark.parametrize(
    ("mutation", "message"),
    (
        ("null-hole", "form a prefix"),
        ("negative", "invalid distance"),
        ("nonfinite", "invalid distance"),
        ("short", "completion state mismatch"),
        ("initial", "summary mismatch"),
        ("final", "summary mismatch"),
        ("final-ratio", "summary mismatch"),
        ("growth", "summary mismatch"),
        ("maximum", "summary mismatch"),
        ("maximum-step", "summary mismatch"),
        ("sample", "dense projection mismatch"),
    ),
)
def test_dense_trajectory_mutations_fail_closed(runner, auditor, mutation, message):
    arm = _off_grid_arm()
    if mutation == "null-hole":
        arm["dense_distances"][2] = None
    elif mutation == "negative":
        arm["dense_distances"][2] = -1.0
    elif mutation == "nonfinite":
        arm["dense_distances"][2] = float("nan")
    elif mutation == "short":
        arm["dense_distances"].pop()
    elif mutation == "initial":
        arm["initial_distance"] = 0.5
    elif mutation == "final":
        arm["final_distance"] = 0.1
    elif mutation == "final-ratio":
        arm["final_ratio"] = 0.1
    elif mutation == "growth":
        arm["growth_factor"] = 1.0
    elif mutation == "maximum":
        arm["maximum_distance"] = 1.0
    elif mutation == "maximum-step":
        arm["maximum_step"] = 2
    else:
        arm["samples"][1]["distance"] = 0.5

    for verifier in (runner._verify_trajectory, auditor._verify_trajectory):
        with pytest.raises(ValueError, match=message):
            verifier(arm, path="$.synthetic")


def test_v2_schema_requires_fixed_length_dense_trace(runner, auditor):
    payload = runner.assemble_component(
        backend=_CompleteBackend(runner),
        identity=_identity(runner),
        publication=_publication(runner),
    )
    payload["trajectories"]["perturbation_arms"][0]["dense_distances"].pop()

    with pytest.raises(ValueError, match="length"):
        runner.validate_payload(payload)
    with pytest.raises(ValueError, match="length"):
        auditor.audit_payload(payload)


class _CompleteBackend(_PreflightBackend):
    def __init__(self, runner):
        super().__init__(runner, passed=True)
        self.vector = [[0.0, 0.0] for _ in range(4800)]
        self.vector[0] = [1.0, 0.0]

    def arnoldi_panel(self, **kwargs):
        name = kwargs["name"]
        self.calls.append(("arnoldi", name))
        count, ncv, tolerance, iterations = self.runner.PANEL_CONFIGURATIONS[name]
        theta = kwargs["rounded_root"][1]
        pairs = [
            _pair(complex(np.cos(theta), np.sin(theta)), "translation"),
            _pair(complex(np.cos(theta), -np.sin(theta)), "translation"),
            _pair(1.0 + 0.0j, "rotation"),
        ]
        pairs.extend(
            _pair(0.8 - 1e-6 * index + 0.01j, "transverse")
            for index in range(count - 3)
        )
        for pair in pairs:
            pair["vector"] = self.vector
        pairs.sort(key=lambda pair: pair["modulus"], reverse=True)
        return {
            "eigenpairs": pairs,
            "expected_count": count,
            "max_iterations": iterations,
            "ncv": ncv,
            "requested_count": count,
            "start_sha256": self.runner._vector_sha256(kwargs["start"]),
            "status": "complete",
            "tolerance": tolerance,
        }

    def continuation_arm(self, **kwargs):
        self.calls.append(("continuation", kwargs["name"]))
        dense = [1.0] + [0.05] * 5000
        samples = [
            {"distance": dense[10 * index], "step": 10 * index}
            for index in range(501)
        ]
        return {
            "amplitude": 1e-7 * kwargs["rounded_root"][0],
            "completed": True,
            "dense_distances": dense,
            "final_distance": 0.05,
            "final_ratio": 0.05,
            "growth_factor": 1.0,
            "initial_distance": 1.0,
            "maximum_distance": 1.0,
            "maximum_step": 0,
            "name": kwargs["name"],
            "perturbation": list(kwargs["perturbation"]),
            "perturbation_sha256": self.runner._vector_sha256(
                kwargs["perturbation"]
            ),
            "samples": samples,
            "stopped": False,
        }

    def exact_arm(self, **kwargs):
        self.calls.append("exact")
        return {
            "completed": True,
            "dense_distances": [0.0] * 5001,
            "maximum_distance": 0.0,
            "maximum_step": 0,
            "samples": [
                {"distance": 0.0, "step": 10 * index} for index in range(501)
            ],
            "stopped": False,
        }


def test_full_synthetic_record_serializes_within_registered_size_budget(
    runner, auditor, tmp_path
):
    payload = runner.assemble_component(
        backend=_CompleteBackend(runner),
        identity=_identity(runner),
        publication=_publication(runner),
    )
    receipt = _write_receipt(payload, tmp_path)
    encoded = json.dumps(
        payload, allow_nan=False, indent=2, sort_keys=True
    ).encode("utf-8")

    assert payload["classification"]["decision"] == (
        "g5-local-direct-stability-pass"
    )
    assert 1_000_000 < len(encoded) < 30_000_000
    assert auditor.audit_payload(payload)["pass"] is True
    paths = runner.publish_payload(payload, directory=tmp_path)
    assert paths["result"].stat().st_size < 30_000_000
    assert auditor.audit_publication(
        result_path=paths["result"],
        report_path=paths["report"],
        manifest_path=paths["manifest"],
        receipt_path=receipt,
    )["publication_pass"] is True


def test_zero_ritz_vector_is_rejected_by_runner_and_auditor(runner, auditor):
    payload = runner.assemble_component(
        backend=_CompleteBackend(runner),
        identity=_identity(runner),
        publication=_publication(runner),
    )
    payload["arnoldi"]["primary"]["eigenpairs"][0]["vector"] = [
        [0.0, 0.0] for _ in range(4800)
    ]

    with pytest.raises(ValueError, match="zero Ritz vector"):
        runner.validate_payload(payload)
    with pytest.raises(ValueError, match="zero Ritz vector"):
        auditor.audit_payload(payload)
