# 3D Memory-Shape Boundary Note

Date: 2026-07-13.

## Scope

This note sharpens the current `D_mem ~= 3` finding without turning it into a macroscopic dimension-selection claim. It separates three layers:

1. Paper I may report a local, co-moving memory-cloud shape diagnostic in the corrected scalar reference slice.
2. Paper II owns the future question whether such local geometry becomes a robust external/macroscopic three-dimensional description.
3. No current result proves that arbitrary ambient dimensions collapse to three external dimensions.

Source aggregate: `reports/long_runs/long_3e8/dynamic_center_spin_trace_q3_N30M_eps1em4_summary_2026-07-13.json`.

## Observable

`D_mem` is the covariance participation dimension of the weighted memory cloud, not an occupancy dimension and not a dimension-selection theorem. If `lambda_i` are the eigenvalues of the weighted memory covariance, then

```text
D_mem = (sum_i lambda_i)^2 / sum_i lambda_i^2.
```

`roundness` is a complementary shape observable. In the current reports it tracks how isotropic the occupied memory cloud is; values closer to `1` indicate a less axis-degenerate cloud. The current 3D statement needs both observables: `D_mem ~= 3` alone would be weak if the cloud were broad, drifting, or strongly axis-degenerate.

## Seedwise N30M Evidence

Fixed slice: `d=3`, `epsilon=1e-4`, `N=30,000,000`, seeds `1..5`, corrected q=3 scalar kernel, active candidates `A_att in {20,35}`, matched `eta_zero` controls.

| A_att | condition | seed | dynamic radius | drift/radius/memtime | D_mem | roundness |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| `20` | baseline | `1` | `2.918e-04` | `0.077` | `2.948` | `0.870` |
| `20` | baseline | `2` | `2.916e-04` | `0.072` | `2.672` | `0.661` |
| `20` | baseline | `3` | `2.931e-04` | `0.078` | `2.857` | `0.752` |
| `20` | baseline | `4` | `2.895e-04` | `0.061` | `2.803` | `0.719` |
| `20` | baseline | `5` | `2.873e-04` | `0.057` | `2.783` | `0.696` |
| `20` | eta_zero | `1` | `1.055e-03` | `0.336` | `2.679` | `0.626` |
| `20` | eta_zero | `2` | `1.035e-03` | `0.381` | `1.312` | `0.223` |
| `20` | eta_zero | `3` | `1.021e-03` | `0.320` | `1.480` | `0.219` |
| `20` | eta_zero | `4` | `1.014e-03` | `0.265` | `2.411` | `0.577` |
| `20` | eta_zero | `5` | `1.061e-03` | `0.231` | `1.903` | `0.453` |
| `35` | baseline | `1` | `2.088e-04` | `0.045` | `2.914` | `0.809` |
| `35` | baseline | `2` | `2.087e-04` | `0.044` | `2.920` | `0.814` |
| `35` | baseline | `3` | `2.094e-04` | `0.055` | `2.941` | `0.847` |
| `35` | baseline | `4` | `2.075e-04` | `0.039` | `2.944` | `0.843` |
| `35` | baseline | `5` | `2.074e-04` | `0.036` | `2.947` | `0.849` |
| `35` | eta_zero | `1` | `1.055e-03` | `0.336` | `2.679` | `0.626` |
| `35` | eta_zero | `2` | `1.035e-03` | `0.381` | `1.312` | `0.223` |
| `35` | eta_zero | `3` | `1.021e-03` | `0.320` | `1.480` | `0.219` |
| `35` | eta_zero | `4` | `1.014e-03` | `0.265` | `2.411` | `0.577` |
| `35` | eta_zero | `5` | `1.061e-03` | `0.231` | `1.903` | `0.453` |

## Aggregate Reading

| A_att | condition | seeds | radius median [q1,q3] | drift/r median [q1,q3] | D_mem median [q1,q3] | roundness median [q1,q3] |
| ---: | --- | ---: | --- | --- | --- | --- |
| `20` | baseline | `5` | `2.916e-04 [2.895e-04,2.918e-04]` | `0.072 [0.061,0.077]` | `2.803 [2.783,2.857]` | `0.719 [0.696,0.752]` |
| `20` | eta_zero | `5` | `1.035e-03 [1.021e-03,1.055e-03]` | `0.320 [0.265,0.336]` | `1.903 [1.480,2.411]` | `0.453 [0.223,0.577]` |
| `35` | baseline | `5` | `2.087e-04 [2.075e-04,2.088e-04]` | `0.044 [0.039,0.045]` | `2.941 [2.920,2.944]` | `0.843 [0.814,0.847]` |
| `35` | eta_zero | `5` | `1.035e-03 [1.021e-03,1.055e-03]` | `0.320 [0.265,0.336]` | `1.903 [1.480,2.411]` | `0.453 [0.223,0.577]` |

The strongest current scalar reference is `A_att=35`. Across all five seeds, its active memory cloud is compact, slowly drifting in radius-normalized units, nearly full-dimensional within the chosen 3D embedding, and comparatively round:

- active `D_mem` range: `2.914..2.947`;
- active roundness range: `0.809..0.849`;
- matched `eta_zero` `D_mem` range: `1.312..2.679`;
- matched `eta_zero` roundness range: `0.219..0.626`.

## Paper Boundary

Paper-I-safe statement:

> In the corrected scalar reference slice, the active co-moving memory cloud is compact, slower-drifting than the matched `eta_zero` control, and has a seed-stable covariance participation dimension close to three in the chosen 3D embedding.

Paper-II question:

> Does this local 3D memory-cloud geometry persist under ambient-dimension changes, multi-knot interactions, and external coarse observation strongly enough to define an effective macroscopic three-dimensional space?

Not supported yet:

- a theorem selecting `d=3`;
- collapse from arbitrary high-dimensional initial state space to three external dimensions;
- a Lorentz, finite-propagation, photon, spin, or mass claim;
- a claim that `D_mem` and archived `D_occ` measure the same thing.

## Next Hardening Steps

1. Recompute the `A_att=35`, `epsilon=1e-4` reference in at least one higher ambient embedding with the same co-moving memory-shape observables.
2. Report `D_mem`, roundness, radius, and drift/radius together; never use `D_mem` alone as acceptance criterion.
3. Add a two-knot external-observer test before claiming that local memory shape is an externally shared dimension.
4. Keep archived `D_occ`/`D_win` scans as a separate reconciliation track.
