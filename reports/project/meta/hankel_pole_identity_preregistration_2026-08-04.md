# P3.2 reduced DMD pole-identity preregistration

Date: 2026-08-04.

## Question

Do the already stored visible-state Hankel fits contain a stable complex pole
that persists across retained rank and history depth and is absent from the
retarded one-way control?

## Fixed data and scope

- input: `reports/response/long_horizon_hankel_gate_2026-08-04.json`;
- primary layer: visible relative state `(x_-,m_-)` only;
- conditions: retarded reciprocal versus retarded one-way;
- independent units: future-noise seeds `1,2,3`;
- paired amplitude checks: node-noise correlations `0,0.9,0.99`;
- no new simulation and no gain, lambda, epsilon, kernel, cadence, or feature
  change.

The field/momentum layer is excluded from pole claims because its stored design
matrices are rank deficient (`kappa` around `1e16`).

## Candidate poles

For every stored eigenvalue `mu` retain one member of each conjugate pair when

1. `Im(mu) > 1e-8`;
2. `0 < |mu| < 1`;
3. frequency `omega = |arg(mu)| / Delta t >= 0.05` per memory time;
4. damping `Gamma = -log|mu| / Delta t <= 1` per memory time.

Here `Delta t = alpha * closure_stride_updates = 0.5` memory times.

## Identity gate

The identity grid is fixed before pole inspection:

- retained ranks `{8,16,32}`;
- delay depths `{100,150,200,250}`, corresponding to
  `{5000,7500,10000,12500}` updates;
- anchor cell: rank `32`, depth `250`.

A pole matches an anchor when both

- relative frequency difference is at most `25%`;
- relative damping difference is at most `25%`, with a damping denominator
  floor of `0.05` per memory time.

A seed/correlation track must match at least `10/12` grid cells and include
every retained rank and every depth at least once. A correlation-level
candidate requires matching tracks in at least `2/3` independent seeds with
seed-median frequency and damping ranges at most `25%`.

Because the three correlation levels reuse the same innovations at different
relative amplitudes, they are robustness checks, not independent replicates.
A promoted candidate must pass at every correlation level and its aggregated
frequency and damping must remain within `25%` across the correlation ladder.

## Control separation and decision

For each reciprocal track, apply the same fixed anchor match to the one-way
condition. A candidate is control separated only when the one-way arm matches
fewer than `6/12` cells for at least `2/3` seeds at every correlation.

- **pass:** one reciprocal candidate satisfies identity and control separation;
- **fail:** no reciprocal candidate satisfies identity, or every survivor is
  also present in the one-way control;
- **inconclusive:** numerical or schema failure prevents application of the
  registered gate.

Only a pass permits a new time-segment simulation. A fail closes P3.2 and moves
the project to the preregistered source-local emission/readout analysis P3.2c.
No physical oscillation, spin, photon, dimension, or particle claim follows
from the prescreen alone.
