# P4-R-phi phase-averaged source/write response

Date: 2026-08-26.

Decision: **`p4r-phase-averaged-chiral-response-pass`**.

This is the first execution of the prospectively frozen eight-phase
holdout and binary64 metrology protocol. The phase nodes are a
deterministic quadrature with four mirror-related pairs, not
independent statistical replications.

## Gate summary

| gate | status |
| --- | :---: |
| `pipeline` | pass |
| `registration` | pass |
| `valid_active_arms` | pass |
| `response_available` | pass |
| `reciprocal_ledger_and_metrology` | pass |
| `nonlinear_loop_dynamics` | pass |
| `response_symmetry_and_odd_signal` | pass |
| `finite_phase_averages` | pass |
| `scalar_region` | fail |
| `positive_chiral_region` | pass |
| `positive_phase_support` | pass |
| `directional_fail_region` | fail |

## Frozen phase classifier

| quantity | center | actuator |
| --- | ---: | ---: |
| phase-averaged transverse response | 0.208422 | 0.153753 |
| positive phase nodes | 8/8 | 8/8 |

| phase node | center transverse | actuator transverse |
| ---: | ---: | ---: |
| 0 | 0.207528 | 0.152257 |
| 1 | 0.209315 | 0.15525 |
| 2 | 0.209315 | 0.15525 |
| 3 | 0.207528 | 0.152257 |
| 4 | 0.207528 | 0.152257 |
| 5 | 0.209315 | 0.15525 |
| 6 | 0.209315 | 0.15525 |
| 7 | 0.207528 | 0.152257 |

## Arithmetic metrology

| diagnostic maximum over 32 active arms | value |
| --- | ---: |
| `center_local_relative` | 4.48686e-16 |
| `coupling_local_relative` | 4.48686e-16 |
| `center_envelope_ratio` | 2.155e-05 |
| `coupling_envelope_ratio` | 2.15494e-05 |
| `actuator_envelope_ratio` | 0.0248926 |

All active arms include 80-decimal-digit exact-ratio replays at
updates 1, 2000 and 4000. Passing a full-dot envelope establishes
compatibility with the declared rounding model, not a formal
interval proof.

## Interpretation boundary

Established by this registered pass: a registered eight-node discrete phase-averaged chiral response of the reciprocal source/write L3 loop for the single frozen perturbation amplitude.

Not established: continuous phase independence, amplitude scaling, material center of mass, physical mass, spin, conserved momentum, noise robustness, P4-R-S or P5.

The historical P4 decision remains `p4-source-write-architecture-fail`.

## Provenance

- Protocol freeze revision: `cb863d4a88c1072637116a0296ab9fc20356a675`.
- Execution revision: `59dc8875cf991e3d7472db1496c9ae8ffae16ca8`.
- Runtime: Python `3.12.13`, NumPy `2.4.6`, SciPy `1.18.0`, mpmath `1.3.0`.
- Machine-readable JSON SHA-256: `807cf915d1602d87a779e7bf587387559b1b19d7de60dc43c6e1e220b73682c8`.
