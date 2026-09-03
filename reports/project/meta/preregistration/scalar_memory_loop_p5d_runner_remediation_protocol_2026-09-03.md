# P5-D runner-remediation protocol

Date: 2026-09-03.

Status: **prospectively frozen, target-free and closed**.

This protocol responds to the seven blocking findings P5-R01--P5-R07 in the
target-free P5-D code review.  It authorizes specification, tests and minimal
infrastructure corrections only.  It does not authorize a third P5-D target
call, change a scientific estimand or reinterpret either inconclusive call.

## 1. Fixed history and scope

Evidence fixed before this protocol:

- the first call stopped at final JSON serialization on a NumPy Boolean;
- the sole replacement stopped at final JSON serialization on a guaranteed
  channel-off infinity sentinel;
- neither call published a complete result or an observable decision;
- the closed-state review verdict is
  `p5d-runner-not-ready-no-target-authorized`;
- the center/write algebra reviewed there remains unchanged.

The remediation may change only governance, result representation,
validation, rendering, publication and their tests.  Candidate, equations,
panel, ordering, thresholds, response reducers and decision precedence remain
frozen.  No registered arm may be evaluated during this work.

## 2. Machine-readable governance and one-shot lease

A tracked JSON document named
`experiments/current/dynamics/rotation/scalar_memory_loop_p5d_governance.json`
is the sole executable governance source.  Its initial state is `closed`,
`target_authorized` is false, the two inconclusive calls are recorded, and
`authorization` is null.  Markdown may explain this state but may not open it.

The runner must parse and validate that document before output preparation,
pair initialization or any arm evaluation.  Only a future, separately
reviewed `authorized_once` state may contain an authorization object.  That
object must bind an identifier, the remediation-protocol blob, protected
implementation blobs, a readiness-review blob, and one successful GitHub CI
run with its run identifier, API URL and head commit.  At execution time the
runner must retrieve the official run metadata and fail closed unless its
head and conclusion equal the authorization.  Clean-worktree and exact-
upstream checks remain necessary but are not sufficient.

Before pair initialization, an authorized runner must create one registered
attempt receipt atomically and without overwrite.  It contains the
authorization identifier, UTC time, current commit and governance digest.
Its existence consumes the authorization even if computation or publication
later fails.  Offline metadata verification, a stale receipt, an unknown
field or any mismatch must stop before this receipt and before the target.

## 3. Result schema and vocabulary

The corrected result is schema
`scalar-memory-loop-p5d-mutual-center-v2`.  Validation is recursive,
path-aware and exact: dictionaries have registered required keys and reject
unknown keys; arrays have registered element types and lengths; Boolean is
not accepted as integer; numbers must be finite; unsupported Python or NumPy
objects fail closed.  Every error names the JSON path, expected type and
observed type.  Validation runs before serialization and again after a strict
JSON round trip.  The independent auditor implements its own equivalent
validator without importing the runner or NumPy.

Channel-off arms encode `minimum_mobility_dissipation` as JSON `null`, because
no mobility work is evaluated.  Their ledger gate is explicitly
`not_applicable_channel_off`.  Active arms require a finite numerical minimum
and apply the unchanged lower threshold.  Thus `null` is semantics, not a
replacement numerical sentinel.

New v2 metadata uses the canonical vocabulary: `notch_response` for $b_s$,
`write_gain` for $\gamma_{\rm w}$, `write_mobility` for $\mu_{\rm w}$ and
`unit_roundoff` for $u_{64}$.  Historical v1 code aliases such as
`OrbitCenterReadout.beta` remain readable and are translated only at the
schema boundary.  No unversioned bulk rename is permitted.

## 4. Unavailable response and publication transaction

An unavailable response has exactly `available=false`, a registered `reason`
and no diagnostics.  Classification returns `p5d-inconclusive`.  Report
rendering branches on availability and must never dereference absent
diagnostics.

JSON and Markdown are prepared as exclusive temporary files, parsed or
render-checked, and hashed before either final path is touched.  They are then
moved to their registered final paths.  A third, registered publication
manifest is written and atomically renamed last.  It binds schema,
authorization identifier, attempt-receipt digest, both relative paths, both
SHA-256 digests and publication time.

Only a valid manifest whose hashes match both files constitutes a published
result.  A handled failure removes this invocation's temporary and partial
final files.  After process or host failure, partial files may remain, but no
manifest means no result; the consumed attempt receipt forbids an automatic
retry.  Existing partials, temporaries or a manifest always fail closed and
require a separately reviewed incident procedure.  The implementation must
not claim cross-file filesystem atomicity.

## 5. Provenance trust boundary

The future readiness record is data, not authority by prose.  Its protected
blob table must cover the model kernel, runner, independent auditor,
governance schema, exact payload-schema implementation and all P5-D tests.
The authorization document repeats these digests and binds the successful CI
run to the implementation commit.  A later authorization-only commit is
allowed to change the governance document but none of the protected blobs.

This arrangement avoids a self-referential commit hash: CI validates the
implementation commit; the later authorization commit names that CI and the
exact protected blobs.  The runner verifies both the remote CI assertion and
the local blobs.  A Markdown verdict, run number without API verification or
branch name alone cannot authorize execution.

## 6. Target-free falsification matrix

Before an implementation can be called runner-ready, seven test groups must
all pass without evaluating a registered arm:

1. closed, malformed and prose-only governance states stop before receipt and
   before a target trap; a valid synthetic authorization is consumed once;
2. official CI metadata is mocked at the transport boundary and wrong head,
   non-success conclusion, offline response and protected-blob drift fail;
3. exact production-shaped off and active arm records validate, with `null`
   accepted only for the off mobility minimum and every active minimum finite;
4. nested NumPy NaN/infinity, unsupported scalars or objects, Boolean-as-int,
   missing/unknown keys and wrong lengths fail with exact JSON paths in runner
   and independent auditor;
5. unavailable response serializes, classifies inconclusive and renders a
   report without diagnostics;
6. injected first-file, second-file and manifest publication failures never
   create a valid manifest; handled failures clean partials and pre-existing
   debris blocks publication;
7. a complete synthetic 64+768 production-schema payload passes
   validate--serialize--deserialize--validate--render--publish--independent-
   audit rehearsal in temporary paths, while target traps record zero calls.

The final group tests representation and control flow only.  Synthetic traces
are not Anchor--Anchor trajectories and cannot supply interaction evidence.

## 7. Sequence and decision boundary

The permitted sequence is:

1. commit this protocol, push it and require green CI;
2. conduct and commit a separate target-free protocol review;
3. add the closed governance document and failing adversarial tests;
4. implement only the smallest correction that makes those tests pass;
5. run affected tests, the complete suite, Ruff and strict documentation;
6. commit, push and require green implementation CI;
7. conduct a separate target-free readiness review.

The readiness review may end only in `p5d-runner-ready-target-still-closed` or
`p5d-runner-not-ready-no-target-authorized`.  Even the ready verdict leaves
the governance state closed.  A third target call would require another
prospective authorization document and commit after that verdict; it is not
part of this protocol or the present work.
