# P5-D production-path implementation readiness review

Date: 2026-09-07.

Reviewed implementation revision:
`70a6002eff9d83b71126431c3e7407a3c0d914a5`.

Reviewed CI:
[GitHub Actions run 34164224557](https://github.com/MemoryDynamics/Knoten/actions/runs/34164224557),
successful for that exact implementation revision.

Verdict:
**`p5d-production-boundary-ready-target-closed-horizon-transfer-required`**.

This review is a later documentation artifact and is not part of the reviewed
implementation tree. Immediately before writing it, the implementation
worktree was clean and every blob below was resolved explicitly from the
reviewed revision. A later commit containing only this review does not alter
the evidence revision or imply that CI 34164224557 tested the review itself.

This is a target-free infrastructure verdict. It does not recover the lost
attempt-3 decision, authorize attempt 4, or supply interaction, oscillator,
inertia or mass evidence. The previous
`p5d-runner-ready-target-still-closed` verdict remains falsified by attempt 3;
the present review addresses that specific coverage failure under a new,
separately reviewed protocol.

## 1. Frozen evidence

The exact evidence tree contains:

- Blob `reports/project/meta/preregistration/scalar_memory_loop_p5d_production_path_preflight_protocol_2026-09-06.md`: `acd4d4a4ad1ea9e0baa2594669b1c85c15eff834`
- Blob `reports/project/meta/reviews/scalar_memory_loop_p5d_production_path_preflight_protocol_review_2026-09-06.md`: `501aeffbc60b39c7a95c90c66066217ec2807b0b`
- Blob `reports/project/meta/reviews/scalar_memory_loop_p5d_production_path_preflight_protocol_sufficiency_review_2026-09-06.md`: `cb4a020cfbf1a18edc58297c0a789e468638b11d`
- Blob `reports/project/meta/reviews/scalar_memory_loop_p5d_attempt3_numpy_float_schema_failure_2026-09-05.md`: `7d0c74b2d9f8cd9f97534b1db47fccc73630c072`
- Blob `reports/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_attempt_3.json`: `0f7b0b87ce1bad34a1f93369967fe1fadbcf6394`
- Blob `reports/project/meta/reviews/scalar_memory_finite_h_non_tautology_audit_2026-09-07.md`: `02da3a71aded2f68f55a4babbdb96aa07d693780`
- Blob `src/emergenz_knoten/mutual_center_coupling.py`: `86a064692b33514a536b93877d4d5dcf33894c64`
- Blob `src/emergenz_knoten/orbit_center_actuator.py`: `63d31bc47291f76c65a5633f14436ccd2105fe9a`
- Blob `src/emergenz_knoten/rotating_wave_stability.py`: `9defb5a6876371202e1ba57cea030c997b9c6edd`
- Blob `experiments/current/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_gate.py`: `abad8c2d12b33d8fca953c5e280c943e3468d18d`
- Blob `experiments/current/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_result_audit.py`: `a768b1c292b6ff0aa35aaecf7f0a6fa6951afd62`
- Blob `experiments/current/dynamics/rotation/scalar_memory_loop_p5d_result_schema_v2.json`: `66f77703fe4548ee490fd18e7e3b7d9b0af602ab`
- Blob `tests/test_rotating_wave_p5d_mutual_center.py`: `ed64a1c979e61baf0d9f5a5df8b63da3d5aabebb`
- Blob `tests/test_rotating_wave_p5d_result_audit.py`: `34a0ddd3bb4a38c59b3d2a0af919da9a6183aa59`

The protocol's 41 registered scientific top-level symbols retain AST digest
`8145b57410a87ab8dae4e5112a81db8b538f3ddf5fc66261cd6c453f654b47ac`.
The test fails on a changed registered literal. In particular `_run_arm` and
`_run_registered_panel` retain their frozen scientific AST. No candidate,
history, equation, coupling, panel arm, threshold, reducer or decision rule
changed in this repair.

## 2. Failing-to-passing evidence

Before the correction, the target-trapped preflight produced 12 expected
failures, 3 passes and 38 deselections. The failures localized the absent
native-record boundary, the exact attempt-3 NumPy-float path, unsupported
scalar acceptance, serializer coercion risk and the missing pre-receipt
canary. They were not target observations.

After the smallest P5-local correction:

- the focused preflight passes 16 tests;
- the complete P5 coupling, runner and independent-auditor group passes 84
  tests;
- the repository suite passes 945 tests;
- the configured Ruff scope passes;
- strict MkDocs construction passes;
- official CI lint, tests and strict documentation pass on the exact reviewed
  revision.

An exploratory full-tree Ruff invocation also reports 24 pre-existing issues
in archived or legacy scripts outside the configured CI scope. They were not
modified or hidden by this repair. They are repository debt, but do not
contradict the claim-scoped readiness result.

## 3. What is now demonstrated

The actual `_strip_internal` path used by both frozen returned panel lists is
now a strict numerical-to-record boundary. It recursively converts only
registered NumPy scalar intermediates to exact native JSON primitives,
rejects arrays, complex values, objects and non-finite numbers, strips only
top-level internal fields, selects the off- or active-arm schema from the
mode, and validates that complete arm before returning it for payload
construction.

Binary-preservation tests cover negative zero, the smallest binary64
subnormal, the smallest normal value, a widened float32 and one third.
`struct.pack(">d", ...)` equality checks the represented binary64 value, and
`math.copysign` separately protects signed zero. Boolean and integer identity
remain exact. A schema-invalid arm is rejected at `$arm.completed` before it
can enter a complete payload.

The exact attempt-3 expression
`0.0 / numpy.finfo(float).tiny` is reproduced as `numpy.float64`. Bypassing
the boundary remains a schema failure at the recorded nested field; crossing
the boundary emits the bit-identical native `0.0`. This repairs the observed
producer defect without changing the value.

A schema-derived raw off-arm and active-arm witness traverse the same
boundary in a pure pre-receipt canary. A complete synthetic panel of 64 off
and 768 active arms crosses the boundary and then traverses original-record
validation, strict JSON encoding without `default=`, decoded validation,
report rendering, manifest-last publication and the independently
implemented auditor. Target initialization, target-history construction,
native FIFO stepping, mutual-centre stepping and registered-panel evaluation
are trapped at zero calls throughout the preflight.

Mutation witnesses fail for a changed scientific AST literal, boundary
bypass, NumPy Boolean, NumPy or non-finite metric, stale output and serializer
coercion. The original v2 payload is validated before `json.dumps`; decoded
validation remains a second check rather than the first one.

## 4. Library and independence review

The repair follows the registered hierarchy. Python's standard library owns
record primitives, finiteness, binary witnesses, strict JSON, hashes and
publication. NumPy remains confined to numerical intermediates. No new
runtime dependency was added.

No shared result-contract module was introduced. Only the P5 runner and P5
auditor currently implement the exact v2 semantics, and they intentionally
retain independent validators. The protocol's three-consumer semantic table
condition is therefore not met; keeping the conversion boundary P5-local is
the justified result, not a missed generalization opportunity.

## 5. Claim limits and adverse evidence

The canary is generated from the tracked schema rather than from a real
target arm. The full 64+768 rehearsal is synthetic. These tests establish
representation, wiring, failure behavior, publication and independent audit;
they do not establish the P5-D response.

Because `_run_arm` and `_run_registered_panel` are scientifically frozen,
real arms cross their boundary only after the panel calculation and before
complete-payload construction. The pure canary catches known record defects
before a future receipt, but it cannot guarantee that every unanticipated
runtime defect will fail before target work.

The finite-history representation also remains a separate scientific
restriction. The FIFO is an age-ordered truncation, not a spatial ring, and
the existing controls oppose the narrow claim that it mechanically draws a
circle. But the current scale ladder fixes `H alpha = 12`; it does not prove
root and stability transfer for fixed `alpha` as `H` increases. The earlier
nonselecting `H alpha = 6` sensitivity is adverse evidence against simply
assuming horizon independence.

## 6. Decision boundary

The production-record correction satisfies the amended preflight protocol
for target-free infrastructure readiness. P5-D nevertheless remains
`p5d-inconclusive`, the attempt-3 lease remains consumed, and the existing
governance remains closed. No result, report, manifest or audit is recreated
for attempt 3.

Before any proposal to authorize attempt 4, a separate prospective horizon
protocol must test fixed-`alpha` `H` refinement, tail bounds and transfer of
the certified root, full-FIFO defect and local stability/attraction. A later
governance-only authorization would additionally require an explicit user
decision, a fresh UUID and receipt path, and exact preservation of the blobs
reviewed here.

The narrow verdict is therefore
**`p5d-production-boundary-ready-target-closed-horizon-transfer-required`**.
