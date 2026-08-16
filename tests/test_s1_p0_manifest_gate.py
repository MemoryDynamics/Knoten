import hashlib
import json

import pytest

from experiments.current.topology.s1_p0_manifest_gate import (
    PROJECT_ROOT,
    audit_manifest,
    build_audit_record,
    load_manifest,
)


def complete_manifest():
    digest = "b" * 64
    return {
        "schema_version": "1.0",
        "manifest_status": "frozen",
        "candidate_id": "candidate-example-001",
        "candidate_claim": "stationary internal recurrent mode",
        "architecture_level": "K1",
        "time_law": "native-discrete-map",
        "code_revision": "a" * 40,
        "working_tree_status": "clean",
        "quarantined_predecessor_relation": "new architecture, not an old point",
        "full_parameter_tuple": {
            "noise": {"epsilon": 0.01},
            "memory": {"alpha": 0.02, "mass": 1.0},
            "kernel": {"family": "declared-example"},
            "coupling": {"self": 0.1, "cross": 0.0},
            "integration": {"law": "native update"},
            "horizon_and_boundary": {"horizon": 500, "boundary": "open"},
            "external_system": {"mode": "none-autonomous"},
            "initialization": {"rule": "fixed hashed state"},
        },
        "initial_state_source_and_hashes": [
            {"source": "data/processed/example.npz", "sha256": digest}
        ],
        "discovery_provenance": {
            "seeds": [1, 2],
            "run_lengths_and_cadence": {"steps": 1000, "cadence": 10},
            "forcing_and_external_system": {"mode": "none-autonomous"},
            "observables_inspected": ["raw center", "shape tensor"],
            "parameter_cells_or_optimizers_inspected": ["one fixed cell"],
            "selection_rule": "fixed before candidate selection",
            "artifacts_and_hashes": [
                {"path": "reports/example.json", "sha256": digest}
            ],
        },
        "confirmatory_design": {
            "seed_generation_rule": "sha256(protocol commit || index)",
            "untouched_parameter_holdout": {"cell": "declared-neighbor"},
            "new_seeds_disjoint_from_discovery": True,
            "target_data_opened": False,
        },
    }


def test_complete_manifest_passes_structural_audit():
    assert audit_manifest(complete_manifest()) == []


def test_placeholders_dirty_tree_and_unsealed_target_fail_together():
    manifest = complete_manifest()
    manifest["candidate_id"] = "pending"
    manifest["working_tree_status"] = "dirty"
    manifest["confirmatory_design"]["target_data_opened"] = True
    manifest["discovery_provenance"]["artifacts_and_hashes"][0]["sha256"] = "bad"

    issues = audit_manifest(manifest)
    codes = {issue.code for issue in issues}
    paths = {issue.path for issue in issues}

    assert "missing-or-placeholder" in codes
    assert "dirty-discovery-worktree" in codes
    assert "target-data-not-sealed" in codes
    assert "invalid-sha256" in codes
    assert "candidate_id" in paths


@pytest.mark.parametrize("architecture", ["new", "K4", "scalar-ish"])
def test_architecture_level_must_name_a_registered_or_explicit_new_level(
    architecture,
):
    manifest = complete_manifest()
    manifest["architecture_level"] = architecture
    assert "invalid-architecture-level" in {
        issue.code for issue in audit_manifest(manifest)
    }


def test_unknown_full_commit_is_rejected_when_repository_check_is_enabled():
    manifest = complete_manifest()
    manifest["code_revision"] = "0" * 40
    assert "unknown-code-revision" in {
        issue.code for issue in audit_manifest(manifest, repository_root=PROJECT_ROOT)
    }


def test_repository_artifact_content_must_match_declared_hash(tmp_path):
    state_path = tmp_path / "state.bin"
    discovery_path = tmp_path / "discovery.json"
    state_path.write_bytes(b"state")
    discovery_path.write_bytes(b"discovery")

    manifest = complete_manifest()
    manifest["initial_state_source_and_hashes"] = [
        {
            "source": state_path.name,
            "sha256": hashlib.sha256(state_path.read_bytes()).hexdigest(),
        }
    ]
    manifest["discovery_provenance"]["artifacts_and_hashes"] = [
        {
            "path": discovery_path.name,
            "sha256": "c" * 64,
        }
    ]

    issues = audit_manifest(manifest, repository_root=tmp_path)
    mismatch_paths = {
        issue.path for issue in issues if issue.code == "artifact-hash-mismatch"
    }
    assert mismatch_paths == {"discovery_provenance.artifacts_and_hashes[0].sha256"}


def test_audit_record_blocks_d0_and_d1_on_any_issue():
    manifest_path = (
        PROJECT_ROOT / "reports/project/meta/preregistration/"
        "s1_candidate_p0_manifest_2026-08-16.json"
    )
    issues = audit_manifest(load_manifest(manifest_path))
    record = build_audit_record(
        manifest_path,
        issues,
        generated_at="2026-08-16T08:30:00+00:00",
    )

    assert record["decision"] == "fail"
    assert record["issue_count"] == len(issues)
    assert record["downstream"]["D0"] == "blocked"
    assert record["downstream"]["D1"] == "blocked"


def test_manifest_root_must_be_an_object(tmp_path):
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(["not", "an", "object"]), encoding="utf-8")
    with pytest.raises(ValueError, match="JSON object"):
        load_manifest(path)
