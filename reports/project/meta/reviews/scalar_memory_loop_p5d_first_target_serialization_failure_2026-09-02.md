# P5-D first-target serialization failure

Date: 2026-09-02.

Status: **`p5d-inconclusive`**.

This incident record is not a P5-D result review. The first authorized
standard invocation reached final payload serialization and then failed
closed. No standard JSON, Markdown report, temporary standard artifact or
printed decision exists. Consequently no response, ledger, symmetry or
scientific pass/fail may be inferred from this attempt.

## 1. Frozen execution identity

The attempted revision was
`5f04aba8770c2dc74b4ac3daa20e67aa59d7c7e2`, exactly synchronized with
`origin/codex/p5-interaction-design` and clean immediately before invocation.
Its readiness CI was
[33561126377](https://github.com/MemoryDynamics/Knoten/actions/runs/33561126377).
The six scientific implementation blobs were those pinned by the preceding
`p5d-implementation-ready` review.

The Python process started on 2026-09-01 at 23:30:47 Europe/Berlin. The
operator collected the terminal failure on 2026-09-02. The runner emitted no
progress or scientific fields before failing.

Immediately before invocation all four registered result and temporary paths
were absent. They were also absent after failure:

```text
reports/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_2026-09-01.json
reports/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_2026-09-01.md
reports/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_2026-09-01.json.tmp
reports/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_2026-09-01.md.tmp
```

## 2. Exact failure boundary

The traceback reached `run_gate` after `_run_registered_panel`,
`panel_registration`, `response_controls` and `classify_panel`. It failed at
the first final `json.dumps(payload, allow_nan=False, ...)` call with:

```text
TypeError: Object of type bool is not JSON serializable
```

The class name is misleading. A target-free minimal reproducer shows that a
threshold comparison on `numpy.float64` returns `numpy.bool`/`numpy.bool_`,
which the standard-library encoder does not accept:

```text
value = numpy.float64(0.1) <= 1.0
type(value) == numpy.bool
json.dumps({"nested": {"gate": value}}) -> TypeError
```

Several real-arm maxima begin as Python floats but can become NumPy scalar
values when updated from D0 or center measurements. Their final comparisons
therefore can produce NumPy booleans. The synthetic 832-arm panel used plain
Python booleans and did not exercise that final scalar-type boundary.

## 3. Scientific consequence

The stack location proves only that the in-memory panel reached the final
serialization stage. Although the code had computed an in-memory decision,
it was neither printed, observed nor persisted and disappeared when the
process exited. Reconstructing or guessing it from runtime duration, absence
of an earlier exception, analytic center-only expectations or a new parameter
search is forbidden.

The attempt is therefore classified by the protocol's fail-closed pipeline
rule as `p5d-inconclusive`. It is not a failed interaction hypothesis and not
a passed gate. The first invocation is consumed and cannot simply be repeated
under the old readiness verdict.

## 4. Recovery boundary

Only a separately frozen serializer correction may proceed. It must leave
candidate, histories, equations, panel, ordering, strengths, thresholds,
decision precedence and standard paths unchanged. It must be implemented and
tested without another registered trajectory, committed and CI-checked, then
receive a new target-free readiness review. Only that chain may authorize one
replacement invocation.

The replacement, if authorized, is error recovery, not an independent
replication. This incident remains part of the permanent provenance and must
be cited by the eventual raw result and critical result review.
