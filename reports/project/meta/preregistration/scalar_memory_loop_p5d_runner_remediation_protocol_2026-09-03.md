# P5-D runner-remediation protocol

Date: 2026-09-03.

Status: **prospectively amended after protocol review, target-free and
closed**.

The amendment resolves P5-PR01--P5-PR07 from the separately committed review
at revision `5a9d01aec9604787a047486ba9d2da2bf7cff9d3`, whose CI run
33713661926 succeeded.  No implementation file or target was touched between
the initial freeze and this amendment.

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

The exact receipt path for the only possible next attempt is
`reports/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_attempt_3.json`.
Authorization identifiers use lowercase canonical UUIDv4 syntax
`[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}`.
The fixed path, exclusive creation and UUID equality between governance and
receipt jointly enforce one-shot use; an identifier never enters a path.

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

The authoritative machine-readable structural contract is
`experiments/current/dynamics/rotation/scalar_memory_loop_p5d_result_schema_v2.json`.
It has its own schema identifier and SHA-256 digest.  Runner and auditor load
the same tracked bytes but implement independent validation code.  The
contract registers every object key, array element type and fixed or bounded
length; any explicitly variable diagnostic map registers its finite value
type and complete allowed-key enumeration.  `additional_properties` is false
at every object node.  The governance document pins the contract digest.

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

The exact manifest path is
`reports/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_2026-09-01.publication.json`.
The JSON and Markdown paths remain the two original registered paths.  The
independent production auditor must load the manifest first, validate its
schema and reject absent, malformed or mismatched receipt, paths and hashes
before reading or interpreting the payload.

Only a valid manifest whose hashes match both files constitutes a published
result.  A handled failure removes this invocation's temporary and partial
final files.  After process or host failure, partial files may remain, but no
manifest means no result; the consumed attempt receipt forbids an automatic
retry.  Existing partials, temporaries or a manifest always fail closed and
require a separately reviewed incident procedure.  The implementation must
not claim cross-file filesystem atomicity.

Cleanup ownership is exact: on entry all six final/temporary result and
manifest paths must be absent; the call records which files it creates and a
handled failure may unlink only that recorded set.  It may never remove a
pre-existing file.  The attempt receipt is deliberately excluded from
cleanup because it records consumed authorization.

## 5. Provenance trust boundary

The future readiness record is data, not authority by prose.  Its protected
blob table contains exactly these seven minimum paths:

1. `src/emergenz_knoten/mutual_center_coupling.py`;
2. `experiments/current/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_gate.py`;
3. `experiments/current/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_result_audit.py`;
4. `experiments/current/dynamics/rotation/scalar_memory_loop_p5d_governance.json`;
5. `experiments/current/dynamics/rotation/scalar_memory_loop_p5d_result_schema_v2.json`;
6. `tests/test_rotating_wave_p5d_mutual_center.py`;
7. `tests/test_rotating_wave_p5d_result_audit.py`.

The authorization document repeats the six non-governance implementation
digests, the closed governance blob and the schema content digest, and binds
the successful CI run to the implementation commit.  A later
authorization-only commit may change exactly the governance path and no
other protected path; the runner verifies that exact diff.  This sole
exception replaces the closed governance object with its schema-valid
`authorized_once` form and does not alter code or the scientific contract.

The closed governance record also pins the HEAD blob of each incident report:
`reports/project/meta/reviews/scalar_memory_loop_p5d_first_target_serialization_failure_2026-09-02.md`
and
`reports/project/meta/reviews/scalar_memory_loop_p5d_replacement_nonfinite_serialization_failure_2026-09-02.md`.

This arrangement avoids a self-referential commit hash: CI validates the
implementation commit; the later authorization commit names that CI and the
exact protected blobs.  The runner verifies both the remote CI assertion and
the local blobs.  A Markdown verdict, run number without API verification or
branch name alone cannot authorize execution.

Remote verification invokes `gh api` only for the constructed route
`repos/MemoryDynamics/Knoten/actions/runs/{run_id}`, where `run_id` is a
positive decimal integer.  No URL, host, owner or repository supplied by the
governance document is followed.  The returned object must have the same
integer `id`, `repository.full_name=MemoryDynamics/Knoten`,
`status=completed`, `conclusion=success` and `head_sha` equal to the
authorized implementation revision.  Command failure, malformed JSON or any
mismatch fails before receipt creation.

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
