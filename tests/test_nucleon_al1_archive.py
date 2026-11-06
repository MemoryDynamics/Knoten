"""Checks on saved target data only; never execute or reconstruct AL1 matrices."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from experiments.current.reference import nucleon_al1_archive_summary as summary
from experiments.current.reference.nucleon_gaussian_run import finite_basis_checks


ROOT = Path(__file__).resolve().parents[1]


def archive(sector):
    path = ROOT / "reports/reference" / f"{sector}_al1_attempt1_2026-10-28.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("sector", ["nucleon", "delta"])
def test_saved_runs_retain_all_levels_cutoffs_and_original_gate(sector):
    report = archive(sector)
    assert report["decision"] == "finite-basis-consistency-pass"
    assert report["checks"] == finite_basis_checks(report["levels"])
    assert all(report["checks"].values())
    assert report["openblas_num_threads"] == "1"
    assert 0 < report["elapsed_seconds"] < report["budget_seconds"] == 300
    assert [level["gaussians"] for level in report["levels"]] == [18, 50, 98]
    assert len(summary.summarize(report)["rows"]) == 6


@pytest.mark.parametrize("sector", ["nucleon", "delta"])
def test_archived_states_and_observables_satisfy_algebraic_identities(sector):
    report = archive(sector)
    for level in report["levels"]:
        assert len(level["exponents"]) == level["gaussians"]
        for solution in level["solutions"]:
            solver, obs = solution["solver"], solution["observables"]
            dimension = solver["raw_dimension"]
            assert len(solver["coefficients"]) == dimension
            assert len(solver["metric_eigenvalues"]) == dimension
            assert np.isfinite(solver["coefficients"]).all()
            assert 0 < solver["rank"] <= dimension
            assert obs["hamiltonian"] == pytest.approx(solver["energy"], abs=1e-12)
            assert obs["up_spin"] + obs["down_spin"] == pytest.approx(1, abs=1e-12)
            assert obs["charge_p_radius2"] + obs["charge_n_radius2"] == pytest.approx(
                obs["matter_radius2"], abs=1e-12
            )
            assert obs["mean_constituent_v2_proxy"] == pytest.approx(
                2 * obs["kinetic"] / (3 * report["hamiltonian"]["mass"])
            )


def test_moment_and_units_are_arithmetic_not_a_refit():
    report = archive("nucleon")
    synthetic = deepcopy(report)
    for level in synthetic["levels"]:
        for solution in level["solutions"]:
            solution["observables"].update(
                up_spin=4 / 3,
                down_spin=-1 / 3,
                charge_p_radius2=1 / summary.HBARC_GEV_FM**2,
            )
    for row in summary.summarize(synthetic)["rows"]:
        assert row["mu_p_in_e_over_2m"] == pytest.approx(1)
        assert row["mu_n_in_e_over_2m"] == pytest.approx(-2 / 3)
        assert row["charged_rms_NR_fm"] == pytest.approx(1)
    actual = summary.summarize(report)["rows"][-1]
    assert actual["neutral_radius2_NR_fm2"] < 0
    assert actual["moment_ratio_relative_difference_from_PDG"] > abs(
        (-2 / 3) / summary.PDG_MOMENT_RATIO - 1
    )
    # Delta was run at S_z=1/2, not maximal polarization: no mislabeled moment.
    assert "mu_p_in_e_over_2m" not in summary.summarize(archive("delta"))["rows"][-1]


def test_pair_summary_does_not_promote_observed_changes_to_error_certificate():
    result = summary.compare(archive("nucleon"), archive("delta"))
    assert result["finite_basis_ordering_separated"]
    assert result["delta_minus_nucleon_MeV"] > 300
    assert not result["continuum_error_certified"]
    assert not result["memory_emergence_claimed"]


def test_saved_summary_and_input_hashes_are_reproducible_from_archives():
    directory = ROOT / "reports/reference"
    saved = json.loads(
        (directory / "nucleon_al1_attempt1_summary_2026-10-28.json").read_text(
            encoding="utf-8"
        )
    )
    hashes = saved.pop("input_sha256")
    assert saved == summary.compare(archive("nucleon"), archive("delta"))
    for name, expected in hashes.items():
        assert hashlib.sha256((directory / name).read_bytes()).hexdigest() == expected


@pytest.mark.parametrize(
    "mutation", ["incomplete", "different_model", "different_source"]
)
def test_noncomparable_archives_are_rejected(mutation):
    nucleon, delta = archive("nucleon"), archive("delta")
    if mutation == "incomplete":
        delta["levels"].pop()
    elif mutation == "different_model":
        delta["hamiltonian"]["mass"] += 0.001
    else:
        delta["script_sha256"]["nucleon_gaussian_run.py"] = "changed"
    with pytest.raises(ValueError):
        summary.compare(nucleon, delta)


def test_failing_sector_does_not_inherit_pair_pass():
    nucleon, delta = archive("nucleon"), archive("delta")
    delta["decision"] = "inconclusive"
    assert not summary.compare(nucleon, delta)["finite_basis_ordering_separated"]
