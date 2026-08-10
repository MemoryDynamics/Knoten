# P3.2 reduced DMD pole-identity audit

Date: 2026-08-06T19:43:43+00:00.

## Registered result

Classification: **no control-separated pole identity**.

The audit uses only stored visible-state fits. A complex pole must match
at least 10/12 cells across ranks 8,16,32 and depths 100,150,200,250,
remain seed-stable at every paired noise correlation, and be absent from
the same cells in the retarded one-way control.

![Pole identity audit](../../figures/draft/response/hankel_pole_identity_audit_2026-08-06.png)

| seed | noise corr. | anchors | identity tracks | reciprocal cells | one-way cells | omega | Gamma |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 15 | 1 | 10 | 7 | 0.1031 | 0.003955 |
| 1 | 0.9 | 15 | 1 | 10 | 7 | 0.1031 | 0.004003 |
| 1 | 0.99 | 15 | 1 | 10 | 7 | 0.1028 | 0.004241 |
| 2 | 0 | 15 | 2 | 11 | 7 | 0.104 | 0.007523 |
| 2 | 0.9 | 15 | 2 | 11 | 8 | 0.1037 | 0.006698 |
| 2 | 0.99 | 15 | 1 | 10 | 6 | 0.1039 | 0.005619 |
| 3 | 0 | 15 | 0 | 9 | 9 | 0.1391 | 0.006082 |
| 3 | 0.9 | 15 | 0 | 9 | 9 | 0.1392 | 0.006006 |
| 3 | 0.99 | 15 | 0 | 9 | 8 | 0.1391 | 0.005863 |

## Cross-seed and control gate

Cross-correlation candidates: 4.
Control-separated survivors: 0.

The correlation ladder reuses the same innovations at different
relative amplitudes. It is a robustness check, not three independent
ensembles. Only future-noise seeds count as independent units.

A pole recurring in the one-way arm is a delay/noise/mediator feature,
not evidence for a reciprocal knot mode.

## Decision

P3.2 is closed without a new 500,000-update run. The next step is P3.2c: source-local emission/readout analysis before another mechanism simulation.

No physical oscillation, spin, photon, dimension, or particle claim
follows from this prescreen.

## Reproducibility

- source: `reports/response/reciprocal/long_horizon_hankel_gate_2026-08-04.json`;
- source git revision: `d1c7a03b207d93b9ab5330db0ffef57cc9c17515`;
- no simulation was run;
- [machine-readable summary](hankel_pole_identity_audit_2026-08-06.json).
