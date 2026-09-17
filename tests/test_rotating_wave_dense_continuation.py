from __future__ import annotations

import ast
import inspect
import textwrap

import numpy as np
import pytest

from emergenz_knoten.rotating_wave_dense_continuation import (
    run_dense_continuation,
)
from emergenz_knoten.rotating_wave_stability import (
    circular_history,
    translation_reduced_norm,
)
from emergenz_knoten.rotating_wave_stability_gate import (
    RotatingWaveCandidate,
    StabilityThresholds,
    run_continuation,
)


CANDIDATE = RotatingWaveCandidate(
    candidate_id="dense-continuation-parity",
    radius=0.9,
    theta=0.03,
    alpha=0.1,
    horizon=3,
    memory_mass=1.0,
    eta=0.15,
    sigma_rep=1.0,
    sigma_att=3.0,
    amplitude_rep=1.0,
    amplitude_att=3.5,
)
THRESHOLDS = StabilityThresholds(
    eigen_residual=1e-8,
    symmetry_overlap=0.99,
    symmetry_eigenvalue=1e-7,
    leading_complex_agreement=1e-5,
    leading_modulus_agreement=1e-6,
    unstable_modulus=1.0 + 1e-6,
    stable_modulus=1.0 - 1e-4,
    perturbation_scale_fraction=1e-7,
    continuation_steps=12,
    sample_every=5,
    stopping_radius_fraction=100.0,
    unstable_growth_minimum=100.0,
    stable_transient_growth_maximum=10.0,
    stable_final_ratio_maximum=0.1,
    exact_control_distance_maximum=1e-10,
)


def _normalized_source_tree(function, *, remove_dense_trace: bool) -> str:
    node = ast.parse(textwrap.dedent(inspect.getsource(function))).body[0]
    assert isinstance(node, ast.FunctionDef)
    node.name = "run_continuation"
    if node.body and isinstance(node.body[0], ast.Expr):
        node.body.pop(0)
    if remove_dense_trace:
        class DenseTraceStripper(ast.NodeTransformer):
            def visit_Assign(self, child):
                if any(
                    isinstance(target, ast.Name) and target.id == "distance_trace"
                    for target in child.targets
                ):
                    return None
                return self.generic_visit(child)

            def visit_Expr(self, child):
                call = child.value
                if (
                    isinstance(call, ast.Call)
                    and isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id == "distance_trace"
                    and call.func.attr == "append"
                ):
                    return None
                return self.generic_visit(child)

            def visit_Return(self, child):
                child = self.generic_visit(child)
                if not isinstance(child.value, ast.Dict):
                    return child
                pairs = [
                    (key, value)
                    for key, value in zip(
                        child.value.keys, child.value.values, strict=True
                    )
                    if not (
                        isinstance(key, ast.Constant)
                        and key.value == "distance_trace"
                    )
                ]
                child.value.keys = [key for key, _ in pairs]
                child.value.values = [value for _, value in pairs]
                return child

        node = DenseTraceStripper().visit(node)
        assert isinstance(node, ast.FunctionDef)
    return ast.dump(node, include_attributes=False)


def test_dense_continuation_control_flow_matches_frozen_core_source() -> None:
    assert _normalized_source_tree(
        run_dense_continuation, remove_dense_trace=True
    ) == _normalized_source_tree(run_continuation, remove_dense_trace=False)


@pytest.mark.parametrize("name", ("exact", "radial"))
def test_dense_continuation_is_bitwise_equal_to_frozen_sparse_core(name: str) -> None:
    history = circular_history(
        radius=CANDIDATE.radius,
        theta=CANDIDATE.theta,
        horizon=CANDIDATE.horizon,
    )
    perturbation = np.zeros_like(history)
    if name != "exact":
        perturbation[0, 0] = 1e-8
    reference_norm = translation_reduced_norm(
        history,
        alpha=CANDIDATE.alpha,
        memory_mass=CANDIDATE.memory_mass,
    )

    frozen = run_continuation(
        name,
        perturbation,
        history,
        reference_norm,
        CANDIDATE,
        THRESHOLDS,
    )
    dense = run_dense_continuation(
        name,
        perturbation,
        history,
        reference_norm,
        CANDIDATE,
        THRESHOLDS,
    )

    assert {key: dense[key] for key in frozen} == frozen
    assert len(dense["distance_trace"]) == dense["final_step"] + 1
    assert dense["maximum_distance"] == max(dense["distance_trace"])
    assert all(
        sample["distance"] == dense["distance_trace"][sample["step"]]
        for sample in dense["trace"]
    )
