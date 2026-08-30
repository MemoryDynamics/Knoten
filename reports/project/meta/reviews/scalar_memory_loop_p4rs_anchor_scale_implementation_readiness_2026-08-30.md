# P4-R-S Anchor-scale implementation-readiness review

Date: 2026-08-30.

Verdict: **`p4rs-implementation-ready`**.

This is a target-free implementation review. It does not inspect, construct or
advance a registered Anchor channel-off or active trajectory, does not predict
the P4-R-S outcome and does not open P5. It authorizes at most one first clean
invocation after this review revision itself is committed, pushed and CI-green.

## 1. Scope and reviewed identity

The reviewed question is deliberately narrower than the later scientific
question:

> Does the implementation faithfully encode the frozen P4-R-S protocol and
> fail closed before target access when its prospective controls are not met?

The reviewed implementation is:

Implementation revision: `d5cc87617a790c7b4be3664e36b261fc0c29ecc2`

Runner blob: `a3f1b2d4f9089d00f3786721ad1dcf13895377f7`

Test blob: `0dc1177d4cd1921c5dd1c6a3c26e1614221979c2`

The implementation revision is a descendant of:

- design freeze 11cabd66d0ba086116b29b3ea3d8a8548560cea1;
- protocol freeze 3797c98c83ed61fa02e939583782fd7213e0b961;
- green source-audit mainline ecdaa8522337880aa1504af8c66924be96e0a9db.

Its complete diff from the protocol freeze adds exactly two paths:

1. experiments/current/dynamics/rotation/scalar_memory_loop_p4rs_anchor_scale_gate.py;
2. tests/test_rotating_wave_p4rs_anchor_scale.py.

No historical P4-R runner, native nonlinear map, candidate definition,
formation utility or source/write implementation changed. The decisive
historical blobs remain:

| dependency | observed blob | frozen blob | status |
| --- | --- | --- | --- |
| historical P4-R runner | 27a3a40dde60b797b58da576b5849ab10b47079f | 27a3a40dde60b797b58da576b5849ab10b47079f | exact |
| source/write implementation | 63d31bc47291f76c65a5633f14436ccd2105fe9a | 63d31bc47291f76c65a5633f14436ccd2105fe9a | exact |
| native nonlinear FIFO map | 9defb5a6876371202e1ba57cea030c997b9c6edd | 9defb5a6876371202e1ba57cea030c997b9c6edd | exact |
| rotating-wave candidate definition | 630beb9952abefea823d91388dcbb2de8f1a2927 | 630beb9952abefea823d91388dcbb2de8f1a2927 | exact |
| phase/formation utilities | 38f16f11a790a64470bab3a34505825cf815e7f0 | 38f16f11a790a64470bab3a34505825cf815e7f0 | exact |

The registered result JSON and report were absent throughout implementation
and review.

## 2. Independent execution evidence

The final local target-free checks were:

| check | result |
| --- | --- |
| P4-R-S-specific test module | 16 passed |
| complete repository test suite | 830 passed in 98.75 s |
| exact CI Ruff scope | all checks passed |
| strict MkDocs build | passed in 1.02 s |
| staged whitespace check | passed |
| target result paths | both absent |
| branch versus upstream after push | 0 ahead, 0 behind |

The pushed implementation revision passed
[GitHub Actions run 33331509204](https://github.com/MemoryDynamics/Knoten/actions/runs/33331509204):

- exact Ruff scope: all checks passed;
- complete test suite: 830 passed in 125.89 s;
- strict MkDocs build: passed in 0.95 s.

The remote job completed successfully in 2 min 55 s. Green CI is treated as
necessary implementation evidence, not evidence for an Anchor response.

## 3. Target-seal audit

Importing the new runner constructs only immutable Python objects and parses no
target trajectory. The registered target functions are named separately:

- _run_anchor_channel_off;
- _run_anchor_active_arm.

The run order is:

1. verify clean, pushed provenance and output absence;
2. verify the committed implementation-readiness review;
3. verify exact frozen dependency blobs and canonical hashes;
4. verify exact Anchor root and static port values;
5. reconstruct the immutable L3 response from raw historical arms;
6. check construction and registration controls;
7. only then call any registered Anchor trajectory.

A monkeypatched test makes provenance raise before readiness and replaces both
target functions with traps. The test observes zero target calls. Inspection
of the test module finds the target-function names only in those monkeypatch
assignments. No pre-target test calls either function.

The runner refuses:

- a dirty tree;
- a revision not descended from both freezes;
- an unpushed or divergent branch;
- changed frozen blobs or canonical hashes;
- absent or non-upheld implementation review;
- changed runner/test blobs after this review;
- pre-existing registered outputs or stale temporary outputs;
- non-registered output paths.

This is stronger than relying on operator discipline alone.

## 4. Equation and architecture audit

The Anchor candidate is constructed once from the exact registered decimal
radius and angle, with alpha=0.01, H=1200 and eta=0.15. The implementation
checks:

- exact decimal membership in both certified-intersection coordinates;
- exact equality with the 120-digit refined root;
- H alpha = 12 and eta/alpha = 15;
- the frozen binary64 values of beta, a0 and G;
- chirality conjugacy;
- positive G=nu reconstructed from the Anchor, not copied from L3;
- the offset as 0.0015 times the parsed Anchor radius.

The only active update is the existing reciprocal_source_write_step applied to
the unchanged native map. The new runner adds no velocity, momentum, mass,
second difference, fitted response tensor, co-rotating controller,
interpolation or target tracking. A source search finds no assignment to an
imported P4-R candidate or threshold global.

The historical runner is used only for reviewed pure helpers:

- nested finiteness checks and complex serialization;
- the exact-ratio 80-digit arithmetic replay;
- JSON conversion.

No imported historical global is mutated. A regression test separately checks
that the L3 candidate and P4-R thresholds retain their original identities and
values.

## 5. Registration and time-grid audit

The exact list order is encoded and tested:

- 16 channel-off arms ordered by phase_index then chirality (+1,-1);
- 32 active arms ordered by phase_index, chirality (+1,-1), then offset sign
  (+1,-1).

The Anchor stores updates 0,5,...,2000. The historical L3 stores
0,10,...,4000. Both have 401 samples and are paired by integer index before
comparison. No interpolation path exists.

The response layer requires exact arm order, exact sample steps, finite traces
and exact phase metadata. It reconstructs odd/even responses from raw active
and matching channel-off traces rather than trusting stored response
summaries.

During pre-freeze adversarial review, one decision-precedence defect was found:
a missing common memory-time grid would initially have entered the generic
cross-scale-failure branch. This was corrected before commit. The final code
and a dedicated regression test now force a missing common grid to
p4rs-inconclusive, as required by the protocol.

## 6. Historical L3 reconstruction audit

The runner reads the immutable 15.9 MB P4-R JSON and never reruns L3. It checks:

- the frozen P4-R and historical P4 decisions;
- exact candidate decimals;
- 32 active and 16 channel-off raw records;
- exact order, phase, chirality, sign, amplitude and completion metadata;
- all 401 stored steps and numerical finiteness;
- inherited validity, ledger and dynamic gates;
- raw reconstruction of every final chirality row and phase profile;
- agreement with stored summaries within 5e-15 absolute;
- agreement of all four frozen means within 5e-15 absolute.

The target-free tests reconstruct:

- A_C = 0.24091330892887405;
- B_C = 0.208421577193625;
- A_Q = 0.303296080377988;
- B_Q = 0.15375308546516817.

These are historical comparator values, not Anchor observations.

## 7. Cross-scale estimand audit

For each scale, phase, chirality and all 401 times the implementation stores
the four real components A_C, B_C, A_Q and B_Q. It then stores the signed
pointwise cross-scale differences.

The decisive metrics match the protocol:

1. four complete-transient RMS distances over 16 times 401 values;
2. four final paired-phase profile RMS distances over eight phases;
3. four final mean absolute differences.

The sole scientific threshold is epsilon_scale=0.05. The combined complex RMS,
signed differences and ratios are serialized only as diagnostics and cannot
replace a componentwise gate.

Synthetic falsification tests distinguish:

- identical-scale pass;
- transient mismatch with matching final profile and means;
- phase-local final mismatch diluted in the complete transient;
- global mean mismatch;
- missing common time grid.

Thus no final-value match can hide a different transient, and no all-time
average can hide a phase-local final discrepancy.

## 8. Ledger and numerical-metrology audit

Every active update accumulates:

- the complete write/age split and interaction ledger;
- force balance and midpoint-force residual;
- both mobility dissipations;
- local center and center-actuator identities;
- full-dot and actuator forward envelopes;
- nondecisional raw-center and age-omission rivals.

The first-update displacement scale is frozen per arm. The forward envelopes
use the candidate-specific gamma_(8H), hence H=1200 for Anchor. The high
precision replay is called at updates 1,1000,2000 for every active arm, giving
96 checks if the complete panel runs.

The synthetic H=17 test checks:

- adjoint virtual work;
- full finite-history age ledger;
- at least one-percent age-omission effect;
- all three full forward envelopes;
- exact-ratio 80-digit replay;
- deliberate corrupted-residual rejection.

Nonzero subnormal participation makes an active arm invalid and therefore
cannot be promoted to a response result.

## 9. Decision-table audit

The tests cover all six registered labels:

- p4rs-inconclusive;
- p4rs-ledger-or-metrology-fail;
- p4rs-anchor-scalar-response;
- p4rs-anchor-chiral-hypothesis-fail;
- p4rs-cross-scale-mismatch;
- p4rs-anchor-scale-transfer-pass.

They also cover the registered precedence:

1. provenance, registration, validity, availability, finite means and common
   time grid;
2. ledger and metrology;
3. nonlinear dynamics and response symmetries;
4. scalar region;
5. directional falsification;
6. positive chiral support followed by scale gates;
7. every gap or insufficient-support case.

A completely stored but scientifically failed channel-off panel keeps the
pipeline false and therefore yields p4rs-inconclusive. An incomplete or
nonfinite channel-off trace aborts without writing a partial target artifact.

## 10. Adversarial findings

### R-S-IMPL-001 — common-grid precedence, fixed before freeze

Severity: blocking if unfixed.

The initial working copy could have labeled a common-grid failure as a
cross-scale mismatch. This conflated invalid metrology with a scientific
scale-transfer falsification. The implementation and decision test were
corrected before d5cc876. The reviewed blob contains the fix.

Status: closed.

### R-S-IMPL-002 — deliberate orchestration duplication

Severity: maintenance note.

The new runner is large because the protocol forbids modification or global
mutation of the historical P4-R runner, while the Anchor has different H,
alpha, eta, update count, sampling stride and reference checkpoints.
Candidate-dependent orchestration is therefore local. Pure reviewed helpers
are reused where safe.

Risk control: exact implementation blobs, full regression suite, synthetic
small-H arithmetic tests and a later result recomputation.

Status: accepted for this frozen gate; do not treat it as a general reusable
scale-runner API.

### R-S-IMPL-003 — fail-closed preflight produces no result artifact

Severity: operational note.

Dirty provenance, absent review, changed dependencies or incomplete
channel-off traces raise before any registered result is written. This means a
preflight-only inconclusive condition has no result JSON rather than a JSON
that could be mistaken for a completed target panel.

Scientific impact: conservative. It cannot generate a false response claim.
The decision function still tests the registered p4rs-inconclusive
precedence for complete inputs.

Status: accepted; preserve the fail-closed behavior.

### R-S-IMPL-004 — publication-source restrictions remain open

Severity: inherited major claim restrictions, not an implementation blocker.

The second interval backend, complete hash-locked environment and
citation/release archive remain open. P4-R-S cannot resolve them and the
runner preserves the source verdict.

Status: open and explicitly propagated.

No unresolved implementation-major finding remains.

## 11. Claim boundary

Even a later p4rs-anchor-scale-transfer-pass would establish only a
deterministic second-cell holdout of the same declared discrete source/write
rule at matched memory time and within the registered effect-size limits.

It would not establish:

- an independent replication;
- a convergence order or all-alpha continuum limit;
- continuous S1 phase invariance;
- a physical actuator;
- material center of mass;
- momentum, inertia, mass or intrinsic spin;
- P5 interaction evidence;
- removal of the three publication-source restrictions.

Every other P4-R-S label keeps P5 closed. Even a reviewed full pass opens only
prospective P5 protocol writing.

## 12. Readiness decision

The implementation is faithful to the frozen equations, arm order, metrology,
L3 reconstruction, scale estimands and decision precedence. It is fully
tested locally and in remote CI, fails closed before target access, refuses
alternative output channels and preserves all immutable historical code and
data.

Therefore the target-free implementation-readiness verdict is:

**`p4rs-implementation-ready`**.

This verdict authorizes exactly one first clean invocation only after:

1. this review is committed and pushed without changing the reviewed runner
   or test blobs;
2. that review revision is CI-green and synchronized with its upstream;
3. the runner's own provenance preflight succeeds;
4. both registered result paths remain absent.

It does not authorize threshold changes, exploratory Anchor previews,
alternative output paths, reruns after observing a result or any P5 claim.
