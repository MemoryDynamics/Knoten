# FIFO normal stability: bounded anchor proposal

Date: 2026-10-25. Status: **proposed, not authorized, not executed**.
This fixes a single target before inspecting any of its normal stability
outcomes. It does not reopen G5 or P5, change the model, or authorize a
parameter search. The bounded execution runner is not implemented yet.

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
- No extra precision, horizon, geometry, model, trajectory, noise or
  long-lifetime study under this proposal.

Before target execution, freeze the runner revision and verify synthetic
tests for fixed-input selection, provenance rejection, timeout handling,
result persistence, and classification. Record clean execution revision,
Python/mpmath versions, exact inputs, elapsed time and both panel outputs.
Preserve errors and inconclusive panels as well as successes.

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
proposal; constructed H=4 controls are only method tests.

Author approval for this specific bounded evaluation is required before
execution. There is no automatic fallback after an inconclusive result.
