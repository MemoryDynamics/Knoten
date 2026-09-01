# P5-D mutual-center implementation-readiness review

Date: 2026-09-01.

Verdict: **`p5d-implementation-ready`**.

This is a target-free source and falsification review. It does not construct,
inspect or advance a registered Anchor--Anchor pair trajectory and does not
predict the P5-D decision. It authorizes at most one first invocation of the
frozen standard target after this review revision itself is committed, pushed
and CI-green.

## 1. Reviewed identity and scope

The reviewed question is narrower than the later scientific question:

> Does the implementation faithfully encode the frozen P5-D protocol, expose
> every registered falsification branch and fail closed before pair-state
> construction when provenance or readiness is absent?

Implementation revision: `88dc1d647e45db79fe7af517d3644ef88cc9eee7`

Blob `src/emergenz_knoten/mutual_center_coupling.py`: `86a064692b33514a536b93877d4d5dcf33894c64`

Blob `experiments/current/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_gate.py`: `fcb639f78766b2a3fede707889583b7b6b9c2600`

Blob `experiments/current/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_result_audit.py`: `6e9acb9fbd4592d13ab244dd84915653c0aafd04`

Blob `tests/test_mutual_center_coupling.py`: `ad84f6dda132a8fa152f807d22472c6a55659039`

Blob `tests/test_rotating_wave_p5d_mutual_center.py`: `26176dd9ff8ad2b47d1d5c6e7831e64926e3a64d`

Blob `tests/test_rotating_wave_p5d_result_audit.py`: `17a0ae6b5db61b0889a5f0a60b9203809eecbe19`

The revision descends from the corrected and serialization-amended protocol
freeze `d7a4c5ec4d40f1899940161877b0ab80b7a8c0c7`, whose protocol blob is
`bf3325d550ae2288d8e4012e0480077abf51032e`. That freeze in turn descends
from the target-free design audit. No registered P5-D result JSON or Markdown
file existed during implementation, local review or implementation CI.

## 2. Independent execution evidence

The final local target-free checks were:

| check | result |
| --- | --- |
| P5-D-specific tests | 36 passed |
| affected status/source-contract tests | 14 passed |
| complete repository test suite | 893 passed in 131.80 s |
| exact CI Ruff scope | all checks passed |
| strict MkDocs build | passed |
| staged whitespace check | passed |
| registered result paths | both absent |
| implementation branch after push | exact upstream synchronization |

The pushed implementation revision passed
[GitHub Actions run 33559217777](https://github.com/MemoryDynamics/Knoten/actions/runs/33559217777):

- exact Ruff scope: all checks passed;
- complete test suite: 893 passed in 163.97 s;
- strict MkDocs build: passed in 0.95 s.

The remote job completed successfully in 3 min 37 s. Green CI is necessary
implementation evidence, not evidence for a mutual response.

A whole-repository `ruff check .` additionally exposes 24 pre-existing issues
in archived programs and old paper figure scripts outside the CI lint scope.
They are repository debt. They do not enter any P5-D source path and do not
change this gate verdict, but publication hardening should not hide them.

## 3. Target-seal and provenance audit

Importing the runner defines constants and functions only. The only standard
entry point is `run_gate`, and its first operation is `_verify_provenance`.
The guard runs before `_run_registered_panel`, while pair histories are first
constructed inside the registered-panel path.

The guard refuses:

- a missing or non-upheld readiness review;
- a protocol revision, protocol blob or inherited dependency blob mismatch;
- any change to one of the six reviewed implementation blobs;
- a dirty worktree;
- a local HEAD different from its configured upstream;
- a non-standard output path;
- an existing standard result or stale standard temporary output.

A monkeypatched regression test turns the panel function into a trap and
forces provenance failure. It observes zero panel calls. Another test forces
the first arm to stop and verifies that the complete panel aborts immediately.
The output writer is atomic and refuses overwrite. Hence a stopped or partial
panel cannot become either standard result artifact.

The registered target paths remain absent at this verdict. This review does
not relax the clean/upstream guard: the sole target invocation is permissible
only after this review commit is itself pushed and CI-green.

## 4. Equation and architecture audit

The implementation uses two separate finite-H Anchor histories. Each native
FIFO update is computed before either write. All simultaneous writes use that
same pre-write pair state. The four modes implement exactly:

1. channel-off: two unchanged native updates;
2. A to B: only B receives the midpoint-solved adjoint write;
3. B to A: only A receives the midpoint-solved adjoint write;
4. reciprocal: equal and opposite midpoint-solved center forces and both
   adjoint writes.

The pair step contains no velocity, momentum, second difference, target
phase, target distance, target trajectory, fitted transfer tensor or mass.
The measured notched centers enter the force; the initial distance is used
only for registration and normalization, not as a target separation.

The protocol correction is encoded exactly: `phi_A=phi_m`, `phi_B=-phi_m`,
reflection maps `m -> 7-m` with both chiralities negated, and A/B swap plus
half turn maps `m -> (3-m) mod 8` with roles and one-way directions swapped.
Both coupling signs are covered. Static tests also verify translation and
rotation covariance and that the two initial history arrays do not alias.

## 5. Twelve required pre-target falsification checks

Every item in protocol section 16 is represented by a direct test or an
adversarial synthetic-panel test:

| # | frozen requirement | observed evidence |
| ---: | --- | --- |
| 1 | exact reciprocal and two one-way midpoint solutions | all three modes and both coupling signs match the frozen closed forms; an 80-digit static replay also passes |
| 2 | translation, rotation, reflection and A/B swap | finite-history covariance tests cover all transformations; the corrected panel maps are involutions |
| 3 | exact channel-off nativity | both histories are bitwise equal to separately evaluated native steps |
| 4 | source bit equality in both one-way arms | the non-receiving source history, force and write increment remain exactly native/zero |
| 5 | closed synthetic finite-history pair ledger | force, midpoint, per-loop split and full pair ledgers close within their direct arithmetic tests |
| 6 | fail for one flipped reciprocal force sign | the flipped-force-A rival is resolved by more than `1e-5` of its synthetic interaction scale |
| 7 | fail for omitted A or B age work | omitted-A, omitted-B and omitted-both rivals are each resolved by more than `1e-5` |
| 8 | fail for raw-center substitution | the raw-center ledger rival is resolved by more than `1e-5` |
| 9 | fail for replacing reciprocal trace by one-way sum | exact synthetic superposition yields `p5d-independent-superposition`, never a pass |
| 10 | fail for incomplete matrix | removing one active arm makes response reconstruction unavailable and the independent auditor returns inconclusive |
| 11 | decision precedence for every branch | all seven gate families and the full pass are enumerated; a double failure confirms ledger-before-loop precedence |
| 12 | imports/tests do not invoke the target | import is inert; provenance-before-panel trap observes no target call |

The positive synthetic fixture spans the exact `64 + 768 = 832` registered
arm keys. It is deliberately constructed to pass every response family and
therefore tests serialization, matching and classifier wiring, not the Anchor
dynamics. A corrupted swap trace and source-contamination fixtures separately
demonstrate that those controls can fail.

## 6. Panel, time grid and high-precision scope

The runner constructs exactly 64 base keys in the frozen order: two distance
fractions, eight phase indices and four chirality pairs. It serializes 64
channel-off arms, followed by 768 active arms ordered by base key, coupling
strength, sign and direction. Every arm must complete all 2000 active updates;
each active step evaluates finite-state, collision, loop-shape, chirality,
local metrology and ledger gates.

Each arm stores 101 dynamics samples at steps `0,20,...,2000`. Late and phase
windows begin at the registered updates 1800 and 1500. The runner generates
exactly 192 raw 80-digit references: three checkpoints for each of the 64
`kappa_high`, positive-sign, reciprocal arms. These references replay local
checkpoint arithmetic; they are not 192 independent trajectories.

The eight phase nodes contain four relative phases plus half-turn mates, and
all 832 arms are algebraic/symmetry controls. Neither number is a replication
count.

## 7. Ledger, response and decision reconstruction

For every active update the runner evaluates force, write force, history
increment, pre/native/post-write notched and raw centers, local center/write
identity, binary64 full-dot envelope, mobility dissipation, complete age work
and pair work. One-way modes include the missing counterport as an explicit
reservoir term. Online reducers retain all decision-relevant signed sums,
extrema, minima and counts.

The response layer subtracts the base-key-matched double-channel-off trace.
It reconstructs both one-way responses, the reciprocal response, and the
closed-loop excess over their sum. It then applies the frozen force-sign,
support, strength, distance, swap, reflection and scaling thresholds in the
registered precedence order. No single endpoint can rescue a failed late
window or structural gate.

The separate result auditor uses the Python standard library only and imports
neither the target runner nor NumPy, SciPy or mpmath. It independently
reconstructs panel order, thresholds, stored reducer gates, response controls,
causality and the final decision. Tests show that it detects a false stored
summary, incomplete panel, exact superposition, source contamination and a
numeric ledger-reducer corruption. Its own output is atomic and
non-overwriting.

There is an explicit audit boundary: the compact standard JSON does not store
the complete complex local state for all `768 * 2000 = 1,536,000` active
updates. Therefore the auditor reapplies thresholds to stored online reducers
and raw checkpoints; it cannot independently replay every local operation.
An external full replay requires the pinned runner and frozen input blobs.
Calling this auditor an independent trajectory reproduction would be false.

## 8. Referee assessment and authorization

The implementation is internally coherent, fail-closed and adequately
falsified for the first registered run. The algebraic architecture is still
inserted by construction. A later target pass could establish only that the
prepared Anchor loops carry this declared mutual port while preserving the
registered loop and ledger properties.

It would not establish spontaneous interaction, charge, a universal force
law, intrinsic spin, conserved material momentum, inertia, mass, a toroidal
internal topology or a field mediator. The deterministic P5-D panel also says
nothing about noisy P5-C/P5-I robustness.

Subject to a green CI for the commit containing this review, exactly one clean
standard P5-D target invocation is authorized. No parameter, panel member,
threshold, decision branch or serialization rule may be changed between this
verdict and that invocation.
