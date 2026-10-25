# FIFO normal stability: bounded anchor proposal

Date: 2026-10-25. Status: **authorized with a pre-run oblique amendment; not executed**.
This fixes a single target before inspecting any of its normal stability
outcomes. It does not reopen G5 or P5, change the model, or authorize a
parameter search. The bounded execution runner is now implemented and
tested without target execution. The
[initial proposal](https://github.com/MemoryDynamics/Knoten/blob/927922df21a88e87d17200d02acb5ffa0a3d6a3f/reports/project/meta/preregistration/fifo_normal_stability_anchor_proposal_2026-10-25.md)
preserves the pre-run target and budget; these have not changed.
The author has now explicitly approved the bounded attempt and requested
oblique perturbations as well. The fixed supplement below is recorded
before the first target evaluation. This authorization does not reopen
other targets or permit automatic retries.

## Question and selection

Does the original certified finite-H rotating-wave anchor have strictly
decaying linear normal form modes, after removing exactly the normal
translation and two plane tilts?

Select `k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1`, the original H=1200
existence-certified anchor. This is a pre-existing reference with a
finite certificate, not a choice based on a new normal spectrum. The
H=2400 G5 result is a different target and is not imported as a 3D pass.

Frozen input:

- Repository revision: `eb51fcf4ef3ab022112d523229be87b27d73f562`.
- Source: `reports/dynamics/rotation/scalar_memory_rotating_wave_interval_certificate_2026-08-21.json`.
- Git blob: `fc6e816c6895e408693fbde176afdaee963c20b9`.
- Historical certificate execution: `8ce6c00713cbac24ebaec337bd339f1944dbcc35`.
- Fixed center: the source's unique `precision_dps=120` panel, `inner.center`.
- Fixed half-widths: that panel's `inner.half_width`, both `1e-40`.
- Parameters: `alpha=0.01`, `horizon=1200`, `memory_mass=1.0`, `eta=0.15`,
  `sigma_rep=1.0`, `sigma_att=3.0`, `amplitude_rep=1.0`, `amplitude_att=3.5`,
  with the source decimal strings retained exactly.

Use the same chosen center and widths at both precisions. Do not use the
readability-only `certified_intersection`, rounded report displays, a
freshly refined center, or an adaptively narrowed box. Read from the
pinned Git object and verify its blob and target identity. A working-copy
file with the same name is not a provenance substitute.

## Method and budget

Use the [normal-stability adapter](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/src/emergenz_knoten/fifo_normal_stability.py):
fresh finite Krawczyk check, full root-box coefficient enclosure, exact
cubic symmetry division with interval remainder, and interval Schur
recursion on the entire degree-1197 quotient. Keep all additional modes.

- Exactly two precision panels, 80 and 120 decimal digits, in that order.
- At most one attempt per panel, at most 300 seconds wall time per panel.
- Sequential execution, no parameter variation or root search.
- Stop the active worker when its panel budget expires. Report the timeout;
  do not silently retry. The second predefined panel may still run.
- No extra precision, horizon, geometry, model, noise or long-lifetime
  study. The only added trajectories are the fixed oblique supplement below,
  inside the existing first-panel deadline.

Before target execution, freeze the runner revision and verify synthetic
tests for fixed-input selection, provenance rejection, timeout handling,
result persistence, and classification. Record clean execution revision,
Python/mpmath versions, exact inputs, elapsed time and both panel outputs.
Preserve errors and inconclusive panels as well as successes.

### Runner readiness

The [runner](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/experiments/current/dynamics/rotation/fifo_normal_anchor.py)
reads and hashes the pinned Git blob, selects the same 120-dps source
center for both panels, requires a clean explicitly named execution
revision, and checks that the adapter and interval modules were loaded
from that worktree. The reviewed runtime is Python 3.12 with mpmath 1.3.0.

Each panel is a separate subprocess. Its monotonic deadline accounts for
startup time; on expiry the parent kills and reaps that worker. Operating-
system termination and report-writing overhead can make the reported total
wall time slightly exceed the 300-second worker budget; this is reported,
not additional numerical execution. There is no automatic retry.

The fixed output directory is
`reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25`.
Exclusive creation prevents a second attempt from overwriting an existing
one. A receipt is flushed before numerical work; start markers and complete
panel records are saved separately, followed by a summary and readable
report. A marker alone is not evidence of a live process or a result.
An interrupted attempt is not automatically resumed.

The explicit execution acknowledgement flag is an operator safeguard,
not evidence of human consent by itself. The generic stdin worker is an
internal execution mechanism, not an authorization boundary. No command
using target inputs may be invoked until the author has approved this
bounded evaluation. Before invocation, record the approved scope and
freeze the tested runner's full Git revision.

Local verification: 34 runner controls pass, including pinned-source
inspection without numerical evaluation, source and import rejection,
default no-execution behavior, ordered classification, durable separate
results and overwrite refusal. A real small non-root H=4 worker checks
the subprocess bridge. A real timeout worker is killed before a delayed
file-writing side effect. With adapter, polynomial, interval, structure
and documentation regressions, **207 tests pass**. These are method and
execution controls, not a new anchor stability result or independent
scientific review.

### Authorized oblique supplement, fixed before execution

The actual anchor has theta approximately 0.01577 radians, not pi/2.
The pi/2 circles used earlier were small synthetic method controls.
Here an angle means the angle of a history perturbation relative to the
planar subspace in the unweighted full-history Euclidean norm. It is not
the angular spacing of consecutive history nodes, nor a fixed angle at
every individual node.

At a planar circle the radial-kernel map is reflection symmetric: its
linearization separates planar and normal variations. Consequently an
oblique linear variation is the sum of the two block responses. A pure
normal test cannot certify the planar block; the fixed supplementary
nonlinear probes also expose possible mixed finite-time behavior.

- Reuse the same frozen center and parameters, converted to float64.
  This supplement is not an 80-digit trajectory calculation.
- Form the envelope `cos(2*j*theta)+0.3*sin(3*j*theta)`. Multiply it by the
  local radial unit vector for the planar pattern, and by the normal unit
  vector for the normal pattern.
- Project the planar pattern off the two planar translations and the
  in-plane rigid rotation. Project the normal pattern off the normal
  translation and the two infinitesimal plane tilts. Normalize each to
  unit RMS across the H age-labelled nodes. This projects known tangent
  vectors, not numerically selected near-neutral eigenmodes.
- Combine the patterns as `cos(beta)*P+sin(beta)*N`, at beta = 0, 30, 45,
  60 and 90 degrees, with both overall signs. These are ten arms, including
  pure planar/normal controls. Use one fixed RMS amplitude `1e-5*R`.
- Evolve each arm and a common unperturbed reference for exactly 2000
  deterministic native FIFO updates (`alpha*n=20`); no stochastic drive,
  root refinement, amplitude adaptation or reselection of patterns.
- Sample every ten updates, including the initial and final states.
  Read out shape RMS after optimal translation and proper 3D rotation,
  preserving age labels. Report final/initial and maximum sampled/initial
  distances. The latter is not a bound between samples. Alignment defines
  a shape observable, not a claim that orientation is physically a gauge.
- If the maximum sampled reference shape drift from its initial circle
  is at least 1% of the smallest initial arm distance, label the window
  `unresolved-baseline-drift`. Otherwise any final ratio above 1.2 gives
  `growth-over-registered-window`; all below 0.8 gives
  `contraction-over-registered-window`; otherwise it is unresolved.
  These thresholds are descriptive, not stability certificates.
- Execute this supplement once, after the normal calculation in the
  80-dps worker, only if the root was certified. It shares that worker's
  original 300-second deadline. The 120-dps worker does not repeat it.
  Timeout, nonfinite arithmetic or other failure yields a technical
  non-result, not instability; no automatic fallback is authorized.

The linear normal decision and supplementary finite-window description
remain separate in all reports. One amplitude, spatial pattern and finite
window cannot establish an all-mode result, nonlinear basin or lifetime.
Target-free controls check proper alignment, all six removed rigid
tangents, registered angles, agreement with the existing planar kernel,
first-order block additivity and complete sampling.
With this amendment, **229 affected regression tests pass locally**,
including 56 runner/probe controls. Lint and the strict documentation
build also pass. No target calculation is included in those tests.

## Decision rules

Each panel retains the adapter's result:

- `strictly-schur`: all normal form roots are strictly inside the unit
  circle under the mpmath.iv trust basis and the fresh root certificate.
- `not-strictly-schur`: strict normal form stability is excluded; this
  alone does not distinguish a neutral mode from positive growth.
- `inconclusive`: interval comparisons do not resolve the question.
- `root-not-certified`: the existence precondition was not established.
- `inconsistent-symmetry-factor`: method-consistency failure, not physics.
- Timeout or exception: technical non-result, not instability.

Call the two-panel result strictly stable only if both panels return
`strictly-schur`; call it not strictly stable only if both return
`not-strictly-schur`. Conflicting decisive results are a method-consistency
failure. Any other combination remains inconclusive at the proposal level;
retain each individual conditional result without promoting it to a
two-panel pass. Do not reinterpret inconclusive as evidence for either
physical outcome.

## Claim boundary and authorization

A strict result would add one local linear normal-stability result for
the prepared H=1200 anchor. It would not establish the planar form block
rigorously, nonlinear basin size, generic formation, noise lifetime,
topological protection, dimension selection, quantum behavior, or a
physical weak interaction. A second precision is not an independent
interval backend. No new target evaluation has been made to prepare this
proposal or its oblique amendment; constructed H=4 controls and small
oblique probes are only method tests.

Author approval for this specific bounded evaluation has been received.
Freeze and verify the amended runner before execution. There is no
automatic fallback after an inconclusive result.
