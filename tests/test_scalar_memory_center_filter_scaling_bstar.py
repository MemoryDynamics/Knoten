from __future__ import annotations

import math

import numpy as np
import pytest

from experiments.current.dynamics.scaling import (
    scalar_memory_center_filter_scaling_bstar as bstar,
)


def test_case_decouples_memory_time_mobility_and_memory_load() -> None:
    first = bstar.make_case(
        tau=0.8,
        input_mobility=1.25,
        memory_mass=0.7,
    )
    second = bstar.make_case(
        tau=1.6,
        input_mobility=0.625,
        memory_mass=1.4,
    )

    assert first.eta == second.eta == bstar.FIXED_ETA
    assert first.predicted_filter_mass == pytest.approx(0.64)
    assert second.predicted_filter_mass == pytest.approx(2.56)
    assert second.local_kappa > first.local_kappa
    assert first.horizon < second.horizon


@pytest.mark.parametrize(
    ("tau", "mobility", "mass"),
    [
        (0.0, 1.0, 1.0),
        (1.0, 0.0, 1.0),
        (1.0, 1.0, 0.0),
        (bstar.TIME_STEP, 1.0, 1.0),
    ],
)
def test_case_rejects_nonphysical_numerical_parameters(
    tau: float,
    mobility: float,
    mass: float,
) -> None:
    with pytest.raises(ValueError):
        bstar.make_case(
            tau=tau,
            input_mobility=mobility,
            memory_mass=mass,
        )


def test_generic_impedance_fit_recovers_synthetic_coefficients() -> None:
    step = 0.01
    root = 0.93
    coefficient = 0.004
    force = np.zeros(160, dtype=float)
    force[:20] = 5.0
    velocity = np.zeros_like(force)
    for index in range(force.size):
        previous = velocity[index - 1] if index else 0.0
        velocity[index] = root * previous + coefficient * force[index]
    center = np.concatenate(([0.0], np.cumsum(step * velocity)))

    fit = bstar.fit_discrete_impedance(center, force, time_step=step)

    assert fit["valid"]
    assert fit["relative_root"] == pytest.approx(root, abs=2.0e-14)
    assert fit["force_coefficient"] == pytest.approx(
        coefficient,
        abs=2.0e-14,
    )
    assert fit["inferred_mass"] == pytest.approx(step / coefficient)
    assert fit["normalized_fit_residual"] < 1.0e-13


def test_exact_finite_h_nonregistered_method_cell_recovers_filter_mass() -> None:
    case = bstar.make_case(
        tau=0.8,
        input_mobility=1.25,
        memory_mass=0.7,
    )

    result = bstar.exact_finite_h_response(case)

    assert result["fit"]["valid"]
    assert result["mass_relative_error_theory"] < 2.0e-3
    assert result["damping_relative_error_theory"] < 2.0e-3


def test_log_scaling_fit_recovers_independent_exponents() -> None:
    cells = []
    for tau, mobility, mass in (
        (1.0, 1.0, 1.0),
        (0.7, 0.8, 0.6),
        (0.7, 1.4, 1.8),
        (1.6, 0.8, 1.8),
        (1.6, 1.4, 0.6),
    ):
        observed = tau / mobility
        cells.append(
            {
                "case": {
                    "tau": tau,
                    "input_mobility": mobility,
                    "memory_mass": mass,
                },
                "synthetic": {"median_inferred_mass": observed},
            }
        )

    fit = bstar.fit_log_scaling_law(cells, estimand="synthetic")

    assert fit["rank"] == 4
    assert fit["intercept"] == pytest.approx(0.0, abs=1.0e-12)
    assert fit["tau_exponent"] == pytest.approx(1.0, abs=1.0e-12)
    assert fit["mobility_exponent"] == pytest.approx(-1.0, abs=1.0e-12)
    assert fit["memory_mass_exponent"] == pytest.approx(0.0, abs=1.0e-12)


def test_state_matched_history_preserves_newest_first_order() -> None:
    case = bstar.make_case(
        tau=0.5,
        input_mobility=1.0,
        memory_mass=1.0,
    )
    archive = np.arange(
        (case.horizon + 3) * bstar.DIM,
        dtype=float,
    ).reshape(case.horizon + 3, bstar.DIM)

    state = bstar.state_matched_initial_state(case, archive)

    assert state.head == 0
    assert np.array_equal(state.x, archive[0])
    assert np.array_equal(state.history, archive[: case.horizon])
    assert len(state.digest) == 64


def test_registered_factorial_split_is_full_rank_and_preserves_old_seals() -> None:
    training = bstar.registered_training_cases()
    holdout = bstar.registered_holdout_case()
    tuples = {
        (
            case.tau,
            case.input_mobility,
            case.memory_mass,
        )
        for case in training
    }

    assert len(training) == 8
    assert bstar.BASELINE_TUPLE in tuples
    assert bstar.HOLDOUT_TUPLE not in tuples
    assert (
        holdout.tau,
        holdout.input_mobility,
        holdout.memory_mass,
    ) == bstar.HOLDOUT_TUPLE
    design = np.asarray(
        [
            [
                1.0,
                math.log(case.tau),
                math.log(case.input_mobility),
                math.log(case.memory_mass),
            ]
            for case in training
        ]
    )
    assert np.linalg.matrix_rank(design) == 4
    assert set(bstar.FORMATION_SEEDS).isdisjoint({21, 22, 23, 24, 25})
