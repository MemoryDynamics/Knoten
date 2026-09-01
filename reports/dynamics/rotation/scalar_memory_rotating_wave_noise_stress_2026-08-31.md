# N0 resolved-noise rotating-wave stress result

Decision: **`n0-noise-stability-window-bracketed`**  
Cross-scale interpretation: **`compatible`**  
Zero control: **True**  
Execution revision: `1ea46d86588d0a2e60021439fae4d6a5ef04406e`  
JSON SHA256: `487023fe0a7bf197a400f4c8a5ef086a6ddf6d59c679ca2395a2913ee38079bc`

## Registered grid

| chi | decision |
|---:|---|
| `1e-22` | `inconclusive` |
| `1e-21` | `inconclusive` |
| `1e-20` | `inconclusive` |
| `1e-19` | `inconclusive` |
| `1e-18` | `inconclusive` |
| `1e-17` | `inconclusive` |
| `1e-16` | `inconclusive` |
| `1e-15` | `all-cell-stable` |
| `1e-14` | `all-cell-stable` |
| `1e-13` | `all-cell-stable` |
| `1e-12` | `all-cell-stable` |
| `1e-11` | `all-cell-stable` |
| `1e-10` | `all-cell-stable` |
| `1e-09` | `all-cell-stable` |
| `1e-08` | `all-cell-stable` |
| `1e-07` | `all-cell-stable` |
| `1e-06` | `all-cell-stable` |
| `1e-05` | `all-cell-stable` |
| `1e-04` | `all-cell-stable` |
| `1e-03` | `stress-fail` |
| `1e-02` | `stress-fail` |

## Scaling check

| candidate | available | slope | compatible |
|---|---:|---:|---:|
| Anchor | True | 0.93626 | True |
| L3 | True | 0.870355 | True |

## Claim boundary

Finite-time numerical orbital robustness only; no physical noise calibration, stationary formation, interaction, spin, inertia or mass.

The registered PNG uses logarithmic axes only for nonnegative
stability metrics. Its x-y trajectory panel has linear equal-aspect axes.
The display-only positive log floor is `1e-18`;
open downward triangles mark exact zeros and no decision uses the floor.
