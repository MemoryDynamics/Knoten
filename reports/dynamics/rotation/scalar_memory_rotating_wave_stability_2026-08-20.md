# Scalar-memory rotating-wave source stability

Generated: 2026-08-20T21:44:57.282488+00:00.

Decision: **numerically-stable-source-pass**.

The candidate was evaluated from clean revision
0d9fe68c4a3bddf0e1869a20f9aa9ff2989aaa6c after a zero-defect P0 and frozen D0
contract. No topology, noise or parameter holdout was opened.

## Full-map controls

- Jacobian shape: [2400, 2400]
- Sparse nonzeros: 9596
- Fixed-point max error: 2.45636844e-15
- Analytic symmetry pass: True

## Leading transverse multipliers

| panel | lambda | modulus | residual | panel pass |
| --- | ---: | ---: | ---: | :---: |
| primary | 0.992858455 -0.0200235369i | 0.993060348 | 2.93595497e-13 | True |
| convergence | 0.992858455 -0.0200235369i | 0.993060348 | 4.95650011e-13 | True |

## Registered perturbations

| perturbation | initial distance | max distance | final distance | growth | final/initial | stop |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| exact | 2.82008605e-18 | 5.62349792e-15 | 2.56158844e-15 | 1994.08735 | 908.336978 | completed |
| visible_radial | 8.66795282e-08 | 8.66795282e-08 | 2.74672906e-15 | 1 | 3.1688325e-08 | completed |
| visible_tangential | 7.52248215e-08 | 7.54213502e-08 | 2.51609789e-15 | 1.00261255 | 3.34477084e-08 | completed |
| full_history_transverse | 4.14057033e-09 | 4.14057033e-09 | 2.49555378e-15 | 1 | 6.02707738e-07 | completed |

## Claim boundary

This gate concerns only transverse stability of a prepared spatial
rotating relative equilibrium. It does not establish an internal
phase after quotienting ambient rotation, topology from data,
noise robustness, physical work or mass.
