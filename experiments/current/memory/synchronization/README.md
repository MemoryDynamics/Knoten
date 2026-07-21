# Synchronization and External Response

Status: active measurement programme.

The package diagnostics live in `src/emergenz_knoten/synchronization.py`.
Complete retained-memory states and rigid placement are implemented in
`src/emergenz_knoten/state.py`; paired weak pulses live in
`src/emergenz_knoten/weak_probe.py`, and localized fixed-source continuation
lives in `src/emergenz_knoten/frozen_source.py`. One-way dynamic-source
continuation and relational orbital observables live in
`src/emergenz_knoten/coupled_nodes.py`.

## Core Question

```text
Do two or more metastable knots develop reproducible collective modes in a
common low-dimensional external response sector?
```

This question replaces the weaker requirement that one trajectory or memory
cloud have an occupancy dimension near three. Exact rank three is not assumed.

## Experimental Ladder

1. Complete-state placement: transform visible position and every retained
   memory point together. Verify self-force and shape equivariance.
2. Uniform weak-probe calibration: `+delta`, `-delta`, and unprobed branches
   share future noise; `eta_zero` measures the bare direct response.
3. Frozen localized source: clone and translate a full source-knot state, then
   perturb its location while the target remains dynamic.
4. Static field and distance audit: measure potential, radial drift, parity
   residuals, kernel resolution, and target deformation before interpreting an
   apparent attraction.
5. Independent scalar cross-readout: separate the autonomous self-kernel from
   spatial cross-resolution and compare rigid source orientations with a point
   monopole at matched centre response.
6. Ordered-history current audit: derive polar displacement/unit currents and
   antisymmetric circulation from adjacent retained points; compare both with
   an independent-sign null before adding a new state.
7. Signed scalar cross-channel: separate source sign from the non-negative
   self-confining memory and require `q=0` plus sign-reversal controls.
8. One-way dynamic coupling: source evolves but does not read the target.
9. Nondestructive source transport: preserve source shape against a paired
   unlaunched continuation before interpreting target response.
10. Reciprocal coupling with separate memory fields only after step 9 passes.
11. Shared memory only as a later, separately normalized model variant.

## Completed Uniform Calibration

The 2026-07-16 pilot reused the complete 600-point final memory buffers from
the `N=3M`, `A_att=35`, `epsilon=1e-4`, `d=3/10`, seeds `1..5` runs.

- probe displacement fractions: `0.03` and `0.10` initial memory radii;
- pulse duration: one memory time;
- lags: `0, 0.25, 1, 3, 10` memory times;
- maximum bare-position identity error: `4.7e-12`;
- maximum even probe-induced radius disturbance: `1.8e-6`;
- memory-centre residual: isotropic full rank (`3` in `d=3`, `10` in `d=10`);
- shape residual: no seed-reproducible sign-flip rank and decay to numerical
  scale by ten memory times.

This is a negative control for low-dimensional inference from a uniform force.
The direct field spans the supplied basis by construction. The first
relationally meaningful rank test is therefore the localized frozen source.

Report: `reports/response/weak_probe_calibration_2026-07-16.md`.

## Frozen-Source Implementation

`frozen_source_response.py` loads the checksum-validated `N=100M` checkpoints,
uses the same complete state as target and rigidly translated source, and places
one unperturbed source at a fixed reference offset. The complete source state is
then translated locally by `+delta/-delta` along each basis direction. Perturbed
branches, the baseline-source branch, and a free no-source branch share future
noise. Self-coupling `eta` and source cross-coupling `eta_cross` remain separate.
`eta_cross=0` must reproduce every free path exactly; `eta_zero` retains the
localized source force and provides the bare-response control. One fixed
interaction strength is calibrated from the baseline source force; two local
translation scales test finite-difference convergence before any independent-seed
or dynamic-source claim.


## Clone-Pilot Result

At one effective `sigma_rep`, the calibrated source is thousands of target
memory radii away. The `d=3` and `d=10` center Jacobians are correspondingly
full ambient rank and split into one radial plus `d-1` nearly degenerate
transverse sectors. This is an isotropic scalar far-field response, not an
external-dimension measurement.

Report: `reports/response/frozen_source_pilot_2026-07-16.md`.

## Field Audit and Distance Ladder

The 2026-07-17 static audit evaluates the complete retained `N=100M` source
states. In the canonical `A_rep=1`, `A_att=35`, `sigma_att/sigma_rep=3` slice,
the attractive curvature dominates already at the origin and the point-source
force has no sign crossing. Every audited direction is inward from `5 R_mem`
through `1 sigma_rep`.

The source radius is only about `2.1e-4 sigma_rep` in `d=3` and
`3.8e-4 sigma_rep` in `d=10`. Directional, tangential, parity-odd, and
point-monopole residuals are at numerical scale even at `5 R_mem`. The current
read kernel therefore does not resolve the internal source shape.

The paired distance ladder calibrates every separation to the same realized
bare displacement (`0.03 R_mem` per memory time) under common future noise.
Center and shape Jacobians remain full ambient rank at all six distances.
Near-field target deformation is distance dependent but remains below `0.002`;
this is a small tidal/nonlinear target effect, not source-structure resolution
or an external-dimension signal. These are pathwise results from one canonical
checkpoint per dimension.

Reports: `reports/response/frozen_source_field_audit_2026-07-17.md` and
`reports/response/frozen_source_distance_ladder_2026-07-17.md`.

## Independent Cross-Readout Gate

The package now distinguishes the source self-kernel from an explicit
`ScalarReadoutKernel`. Omitting it is exactly backward compatible. Supplying a
different cross-readout changes only the target response; the autonomous source
path is unchanged. Every resolution is calibrated to the same bare centre
response, so readout width is not confounded with force magnitude.

The preregistered static ladder rotates the complete `N=100M` source along its
principal axes and compares its drift field with a point monopole. The primary
shape signal is the largest orientation-dependent drift difference divided by
the point drift. A 1% exploratory threshold and a minimum centre separation of
1.25 combined memory radii decide whether a scalar shape signal exists before
opening a local/retarded mediator or oriented-memory branch. This is a
pipeline gate from one checkpoint per dimension, not interaction evidence.

The clean 2026-07-21 run fails that gate in both audited embeddings. At the
closest eligible separation (`sigma_rep/R_mem=2.5`), orientation spread is
`1.96e-3` in `d=3` and `4.32e-4` in `d=10`; the corresponding calibrated
orientation-dependent displacements are `5.98e-5` and `1.52e-5 R_mem` per
memory time. The original self-readout remains pointlike at `2.15e-10` and
`3.01e-10`. No finite-source or orientation onset reaches 1% before the
chosen distinctness boundary.

Decision: the next relational-shape mechanism is an oriented memory/current
channel, not another direct scalar readout narrowing. A local or retarded
scalar mediator remains deferred for a separate locality or propagation-time
question. This pathwise result does not rule out scalar near-field structure
for other independently formed knots.

Report: `reports/response/scalar_cross_readout_resolution_2026-07-21.md`.

## Interaction-Sign Decision

The implemented memory weights are non-negative. The current cross-field is
therefore an unsigned scalar monopole and has no knot-specific charge label.
This is parity-even, not parity-free: spatial parity and charge sign are
different symmetries. Charge neutrality would suppress a signed monopole; it
would not explain the universal attraction measured here.

The minimal charge-like test is a separate signed scalar cross-channel while
the established scalar self-confinement channel stays unchanged. Vector memory
is reserved for observables that actually require orientation, phase,
circulation, or polarization.

## Completed Signed-Channel Architecture Gate

`signed_cross_channel.py` implements an externally assigned
`s_target*s_source` factor only in the frozen-source cross force. The cross
potential uses the broad zero-integral, curvature-matched third scale; the
target self-channel remains the canonical non-negative scalar memory.

The 2026-07-18 pilot on the checksum-validated `N=100M` checkpoints in `d=3`
and `d=10` gives:

- bitwise identity of source-zero, target-zero, and explicit free paths;
- bitwise identity for equal label products;
- pulse-response reversal when the label product changes sign;
- maximum radius disturbance below `4.5e-5`;
- active pulse displacement about `0.00136 R_mem` versus the calibrated
  `eta=0` displacement about `0.03 R_mem`.

This validates the software and control architecture only. There is one
checkpoint per dimension, the labels are inputs rather than emergent
observables, and the source is frozen. The next gates are 6-10 independent
states without retuning and fixed-coupling distances below and above the
compensated force crossing.

Report: `reports/response/signed_scalar_cross_channel_pilot_2026-07-18.md`.

## One-Way Dynamic-Source Gate

`one_way_dynamic_source_pilot.py` continues one autonomous source and four
common-target-noise paths: dynamic source, frozen source, free target, and
eta-zero target. Relative velocity is decomposed into radial and tangential
components; the antisymmetric tensor `r wedge v` measures orientation without
assuming three dimensions.

The autonomous source moves only `1.6..4.5` internal radii in 200 memory
times, while one `sigma_rep` is about 4724 radii. Dynamic-minus-frozen target
motion remains `2.1e-5..6.8e-5` radii, and angular coherence and dephasing do
not separate from the free control.

A paired point launch of `0.1 sigma_rep` over ten memory times produces
`10.944` radii of additional source-centre displacement, but only
`3.137e-4` radii of target response. Its source radius differs from the
identical unlaunched continuation by `46..59%`. The imposed drive therefore
does not transport an intact knot. Reciprocal coupling is deferred until a
one-way source can move without losing shape.

Reports: `reports/response/one_way_dynamic_source_pilot_2026-07-20.md` and
`reports/response/one_way_launched_source_pilot_2026-07-20.md`.


## Observables

A target knot provides:

- co-moving visible and memory centres;
- weighted memory shape tensor and radius;
- delayed centre and shape response matrices;
- odd central response `(+delta - -delta)/(2 delta)`;
- even disturbance `(+delta + -delta)/2` against the unprobed path;
- residence or identity-loss diagnostics for later multi-knot runs.

Response rank has two distinct meanings:

- descriptive energy rank from the singular-value spectrum;
- seed-reproducible rank against an exact sign-flip or bootstrap null.

Five seeds have only 16 unique two-sided singular-value sign patterns, so
`p_min=1/16=0.0625`. The uniform pilot uses 90% only as an exploratory gate.
The source-knot validation needs at least six and preferably ten independent
seed states for a conventional 5% decision.

## Frozen-Source Acceptance Criteria

- target and source identities remain distinct;
- response is linear over at least two small source perturbations;
- source-on effects separate from no-source and `eta_zero` controls;
- rank and singular subspace are stable over lag and basis rotation;
- cloned-state calibration is followed by independent-seed validation;
- distance and cross-coupling are scaled by knot radius, kernel range, and
  displacement per memory time rather than selected by a broad blind scan.

## Guardrails

- Do not call a uniform-force rank an emergent spatial dimension.
- Do not call synchronized modes quantum fields.
- Do not call internal labels charge, color, or flavor until they remain stable
  under controlled interactions.
- Do not require internal embedding dimension three.
- Do not infer neutrality from universal attraction in an unsigned scalar
  channel.
- Treat seeds as basin samplers and avoid counting multiple times from one seed
  as independent evidence.
