"""Runner contracts tested with synthetic results, never an AL1 eigenproblem."""

from copy import deepcopy
import json
import sys

import numpy as np
import pytest

from experiments.current.reference import nucleon_gaussian_run as runner


def synthetic_levels():
    solution = {
        "solver": {
            "energy": 1.0,
            "metric_norm": 1.0,
            "relative_matrix_residual": 1e-14,
        },
        "observables": {
            "form_factor_p": 1.0,
            "form_factor_n": 0.0,
            "matter_radius2": 2.0,
            "charge_p_radius2": 2.0,
            "charge_n_radius2": 0.0,
            "up_spin": 4 / 3,
            "down_spin": -1 / 3,
        },
    }
    return [{"solutions": [deepcopy(solution), deepcopy(solution)]} for _ in range(3)]


def test_finite_basis_gate_requires_all_levels():
    assert all(runner.finite_basis_checks(synthetic_levels()).values())
    assert not all(runner.finite_basis_checks(synthetic_levels()[:2]).values())


@pytest.mark.parametrize(
    "key,delta",
    [("charge_p_radius2", 0.06), ("charge_n_radius2", 0.06), ("up_spin", 0.003)],
)
def test_energy_plateau_does_not_hide_unconverged_observables(key, delta):
    levels = synthetic_levels()
    for solution in levels[-1]["solutions"]:
        solution["observables"][key] += delta
    checks = runner.finite_basis_checks(levels)
    assert checks["last_energy_change_under_1_MeV"]
    assert not checks[f"last_change_{key}"]


def test_metric_cutoff_sensitivity_is_not_hidden():
    levels = synthetic_levels()
    levels[-1]["solutions"][1]["solver"]["energy"] += 0.0001
    assert not runner.finite_basis_checks(levels)[
        "cutoff_energy_sensitivity_under_0p05_MeV"
    ]


def test_preflight_cannot_select_al1_and_timeout_is_inconclusive(monkeypatch):
    def forbidden():
        raise AssertionError("AL1 selected during synthetic preflight")

    def timeout(*args, **kwargs):
        raise TimeoutError("synthetic deadline")

    monkeypatch.setattr(runner.basis, "declared_al1", forbidden)
    monkeypatch.setattr(runner.basis, "assemble", timeout)
    result = runner.execute("oscillator-preflight", "nucleon")
    assert result["decision"] == "inconclusive"
    assert result["levels"] == []
    assert result["claim_class"] == "synthetic_solver_verification"
    assert not all(result["checks"].values())


def test_existing_output_is_rejected_before_computation(tmp_path, monkeypatch):
    output = tmp_path / "attempt.json"
    output.write_text("existing evidence", encoding="utf-8")
    monkeypatch.setenv("OPENBLAS_NUM_THREADS", "1")
    monkeypatch.setattr(sys, "argv", ["runner", "--output", str(output)])

    def forbidden(*args, **kwargs):
        raise AssertionError("computation started despite existing output")

    monkeypatch.setattr(runner, "execute", forbidden)
    with pytest.raises(FileExistsError):
        runner.main()
    assert output.read_text(encoding="utf-8") == "existing evidence"


def test_result_generation_does_not_mutate_input_matrices():
    matrices = {"overlap": np.eye(2), "hamiltonian": np.diag([1, 2])}
    result = runner.level_result(matrices)
    assert len(result["solutions"]) == 2
    np.testing.assert_array_equal(matrices["hamiltonian"], np.diag([1, 2]))


def test_archived_coefficients_reconstruct_the_same_state_and_observables():
    matrices = {
        "overlap": np.array([[1.0, 0.2], [0.2, 1.0]]),
        "hamiltonian": np.array([[1.0, 0.3], [0.3, 2.0]]),
        "synthetic_observable": np.array([[0.0, 1.0], [1.0, 0.0]]),
    }
    archived = json.loads(json.dumps(runner.level_result(matrices), allow_nan=False))
    for solution in archived["solutions"]:
        coefficients = np.array(solution["solver"]["coefficients"])
        restored = runner.basis.expectations(matrices, coefficients)
        assert restored == pytest.approx(solution["observables"], abs=1e-14)
        np.testing.assert_allclose(
            matrices["hamiltonian"] @ coefficients,
            solution["solver"]["energy"] * matrices["overlap"] @ coefficients,
            atol=1e-14,
        )
