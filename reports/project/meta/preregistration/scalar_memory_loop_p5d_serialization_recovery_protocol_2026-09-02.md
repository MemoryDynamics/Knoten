# P5-D serialization-recovery protocol

Date: 2026-09-02.

Status: **prospectively frozen after an outcome-unobserved serialization
failure and before any replacement P5-D trajectory**.

The first authorized invocation at revision
`5f04aba8770c2dc74b4ac3daa20e67aa59d7c7e2` produced no standard artifact and
no observable decision. The accompanying incident report classifies it as
`p5d-inconclusive`. This protocol permits one narrowly scoped infrastructure
repair; it does not amend any scientific estimand.

## 1. Identified defect

Real-arm D0 and center metrics may be NumPy scalar floats. Comparisons against
the frozen Python-float thresholds can therefore yield `numpy.bool_`. The
standard-library JSON encoder accepts Python `bool` but rejects that NumPy
scalar. The error occurs only while serializing the already constructed final
payload.

The defect is target-independent and exactly reproduced by a nested synthetic
NumPy boolean. No P5-D response, gate or decision was inspected to identify
it.

## 2. Sole permitted code correction

The target runner may add one fail-closed JSON `default` converter used only
by the final `json.dumps` call. It may convert exactly:

```text
numpy.bool_     -> bool
numpy.integer   -> int
numpy.floating  -> float
```

Every other unsupported object, including arrays and complex scalars, must
still raise `TypeError`. `allow_nan=False`, indentation, key sorting, digest,
atomic two-file write and overwrite refusal remain unchanged.

The runner must point to a new recovery-readiness review rather than silently
reusing the superseded first-readiness verdict. It must verify this recovery
protocol's commit and blob before pair initialization.

## 3. Required target-free tests

Before any replacement invocation, tests must establish:

1. nested NumPy boolean, signed/unsigned integer and finite float scalars
   serialize to the corresponding Python JSON scalar types;
2. `numpy.nan`, positive infinity and negative infinity still fail because
   `allow_nan=False`;
3. arrays, complex scalars and arbitrary objects still fail with `TypeError`;
4. the full synthetic 832-arm payload serializes through the exact production
   helper;
5. the helper neither changes Python-native values nor invokes the target;
6. the original six implementation paths are repinned in a new readiness
   review, with only explicitly reviewed recovery changes differing.

The complete repository suite, exact CI Ruff scope and strict MkDocs build
must pass. The registered standard and temporary result paths must remain
absent throughout correction and review.

## 4. Frozen scientific invariants

The recovery may not change:

- Anchor candidate, `R`, `theta`, `q`, `H`, `eta`, `G` or mobility;
- either distance, any phase/chirality map, strength, sign or direction;
- 64 channel-off, 768 active and 832 total arm counts or ordering;
- 2000 updates, sample cadence, late/phase windows or 192 references;
- native FIFO or mutual-center equations, simultaneous-write convention,
  notched center, reservoir accounting or work ledger;
- any local, shape, causality, response, symmetry, distance, strength or
  closed-loop threshold;
- decision labels or precedence;
- standard result paths and raw-result-before-audit ordering.

No cached state or inferred value from the failed process exists or may be
used. The replacement must recompute the same complete panel from the same
clean frozen inputs.

## 5. Recovery freeze sequence

1. commit and push this protocol plus the incident record;
2. wait for green CI and record the protocol commit/blob;
3. implement only the converter, new recovery provenance guard and required
   target-free tests;
4. commit, push and await green implementation CI;
5. write a separate recovery-readiness review that repins all six
   implementation blobs and explicitly verifies zero target calls;
6. commit, push and await green recovery-readiness CI;
7. only then execute exactly one clean replacement standard invocation;
8. if it produces both standard artifacts, commit and push them unchanged
   before running the independent result auditor;
9. if it fails, do not retry automatically; record the new failure and stop.

The replacement is not a second statistical observation or replication. The
eventual result must cite both the failed first invocation and this recovery
freeze.
