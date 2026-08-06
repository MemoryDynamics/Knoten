# P3.2d shape-multipole source eligibility: preregistration

Date: 2026-08-06.

## Question

Does the mature scalar knot autonomously generate one emitter-local shape
multipole with narrow-band temporal structure that persists across time
segments and future-noise paths and separates from a self-interaction-off
control?

This is a source-eligibility test. It does not insert a tensor mediator and it
does not test propagation, reciprocal loading, spin, charge, dimension, or a
particle interpretation.

## Data-availability correction

The existing long traces retain centres, radii, dimensions, and spin proxies,
but not the full time-dependent memory-shape tensor. P3.2 computed that tensor
internally but persisted only aggregate shape distances. Therefore a literal
stored-data postprocessor cannot answer the registered question.

The minimal correction is a deterministic autonomous continuation from the
already committed mature `d=3`, `N=100M`, formation-seed-1 checkpoint. No
interaction channel, mediator, gain, kernel, lambda, epsilon, or formation
parameter is searched.

## Fixed design

- future-noise seeds: `1,2,3,4,5`;
- continuation: `150000` updates = `1500` memory times at `lambda=0.01`;
- sampling: every `10` updates = `0.1` memory time; hidden dynamics still
  advances at every update;
- burn-in: first `100` memory times;
- conditions: registered scalar baseline and paired `eta=0` self-interaction
  control with the same future noise;
- four equal post-burn segments;
- frequency band: `0.05..2` cycles per memory time;
- within-path null: 64 deterministic permutations of one-memory-time blocks.

For each shape tensor `S_n`, define the dimensionless centered traceless
multipole

```text
Q_n = S_n / tr(S_n) - I/d.
```

Both `Q_n` and its finite-difference rate `Delta Q_n / Delta tau` are tested.
The full flattened symmetric tensor is retained; duplication of off-diagonal
entries preserves the Frobenius norm and does not select an axis.

## Fixed spectral gate

Welch spectra are summed over tensor components. A seed/source candidate needs:

1. full-trace peak/background ratio at least `5`;
2. peak-band power fraction at least `0.10`;
3. peak/background ratio above the 99th percentile of the 64 block-shuffle
   nulls;
4. at least three of four segments with peak/background at least `5` and
   peak-band fraction at least `0.05`;
5. relative segment-frequency range at most `0.25`.

The source-level gate passes only if:

- at least four of five baseline seeds are candidates;
- their median peak frequencies have relative range at most `0.25`;
- at most one of five paired `eta=0` paths is a candidate;
- all baseline paths remain shape-bounded (`q95(radius/radius_0) <= 1.10` and
  `max(radius/radius_0) <= 1.20`).

Either `Q` or `Delta Q / Delta tau` may pass. A failure closes this scalar
shape-multipole source route at the registered resolution. It does not prove
that no tensor mode exists at any scale and does not by itself justify vector
memory. A pass only authorizes a separately preregistered tensor-mediator
loading test.
