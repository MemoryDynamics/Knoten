# P5-D replacement non-finite serialization failure

Date: 2026-09-02.

Scientific status: **`p5d-inconclusive`**.

Recovery status: **closed; no further target invocation authorized**.

This is an incident and readiness-coverage review, not a P5-D result review.
The one authorized replacement invocation completed the registered in-memory
panel and then failed closed at final JSON serialization. It produced no
standard or temporary artifact and printed no decision. Therefore no response,
ledger, symmetry or interaction pass/fail is observable from this invocation.

## 1. Frozen execution identity

The replacement ran from clean, upstream-synchronized revision
`6dc1b18dc58dc466342bc8221c988a87557f2c17`. Its recovery implementation was
revision `f6da955b388b4f2f4e15632fd567a06fcb5fbf75`, validated by
[GitHub Actions run 33590997553](https://github.com/MemoryDynamics/Knoten/actions/runs/33590997553).
The separate recovery-readiness revision passed
[GitHub Actions run 33591419247](https://github.com/MemoryDynamics/Knoten/actions/runs/33591419247).

The runner verified recovery protocol revision
`9fdab8d534ebadfdd155bde55c3c7e509783dd53`, protocol blob
`508b642b12884996ccb87f354e875053bdf36c5a`, the six repinned implementation
blobs, clean worktree and exact upstream synchronization before constructing
the pair panel. The process started at 2026-09-02 06:40:37 Europe/Berlin. The
terminal failure was collected later on 2026-09-02; the runner emitted no
progress or scientific field before the traceback.

Before invocation and after failure, all four registered paths were absent:

```text
reports/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_2026-09-01.json
reports/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_2026-09-01.md
reports/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_2026-09-01.json.tmp
reports/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_2026-09-01.md.tmp
```

## 2. Exact failure boundary

The traceback reached `run_gate` after `_run_registered_panel`,
`panel_registration`, `response_controls` and `classify_panel`. The recovered
NumPy-scalar converter completed its role, after which the standard encoder
failed under the deliberately retained `allow_nan=False` contract:

```text
ValueError: Out of range float values are not JSON compliant: inf
```

The exception arose while traversing a dictionary inside a serialized panel
list. No path or value other than the non-finite class was emitted. The
in-memory payload and decision disappeared with the process.

## 3. Outcome-independent guaranteed source

Static control-flow inspection identifies a guaranteed positive-infinity
sentinel in every channel-off arm:

1. `_run_arm` initializes `minimum_dissipation = math.inf`;
2. the variable is updated only inside `if mode != "off"`;
3. `_run_registered_panel` registers 64 arms with `mode == "off"`;
4. `_run_arm` unconditionally stores the value as
   `minimum_mobility_dissipation` in every result dictionary;
5. `_serialize_payload` unconditionally uses `allow_nan=False`.

Consequently every complete registered payload contains at least 64 positive
infinities independent of trajectories, response values, gates or final
decision. The traceback does not name its exact dictionary path, so it would
be too strong to claim that no other non-finite value existed. It is sufficient
that the channel-off sentinel makes successful serialization impossible for
all outcomes.

This is a schema/readiness defect, not numerical evidence of instability. The
sentinel means “ledger metric not applicable in channel-off mode”; it is not a
measured infinite dissipation.

## 4. Falsified readiness claim

The recovery protocol correctly required NaN and infinities to remain rejected,
and the new test demonstrated that rejection. However, the so-called full
synthetic 832-arm serialization fixture reproduced panel cardinality and
classifier-shaped records, not the exact production arm schema. It omitted the
unconditional channel-off infinity sentinel. Thus the following two reviewed
claims were incompatible but not tested together:

- non-finite values must fail closed;
- the complete production payload must serialize.

The replacement invocation falsifies the recovery-readiness coverage, not a
scientific P5-D hypothesis. In retrospect the verdict
`p5d-implementation-ready` was insufficient for target execution. The original
review remains immutable provenance; this incident supersedes its operational
authorization rather than rewriting it.

## 5. Scientific and governance consequence

Both consumed invocations are `p5d-inconclusive`. The first exposed a NumPy
boolean type boundary; the authorized replacement exposed an incompatible
non-finite not-applicable sentinel. Neither produced an artifact or observable
decision. Runtime, full-panel completion and failure only at serialization are
not evidence for or against the mutual-center response.

The recovery protocol explicitly states that a failed replacement must not be
retried automatically. Its sole replacement authorization is consumed. No
third P5-D target invocation, serializer patch, sentinel substitution or
result reconstruction is authorized on this branch.

Any future resumption requires a new prospective governance decision and a
new protocol before code changes. At minimum it would have to define the JSON
meaning of not-applicable metrics (`null`, omission or another explicit finite
representation), audit every production payload leaf for finiteness, serialize
an exact production-schema channel-off arm without a target run, and repeat
implementation/readiness CI. This report deliberately does not select among
those semantics.

Until such a separately authorized protocol exists, P5-D is closed with no
interaction evidence. No claim of spontaneous interaction, charge, force law,
spin, momentum, inertia, mass, toroidal field topology or mediator follows.
