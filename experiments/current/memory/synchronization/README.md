# Synchronization and External Response

Status: active measurement programme.

The package diagnostics live in `src/emergenz_knoten/synchronization.py`.
Complete retained-memory states and rigid placement are implemented in
`src/emergenz_knoten/state.py`; paired weak pulses live in
`src/emergenz_knoten/weak_probe.py`.

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
4. One-way dynamic coupling: source evolves but does not read the target.
5. Reciprocal coupling with separate memory fields.
6. Shared memory only as a later, separately normalized model variant.

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
- Treat seeds as basin samplers and avoid counting multiple times from one seed
  as independent evidence.
