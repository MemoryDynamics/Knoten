# 3e8 Long-Run Results

Date: 2026-07-11.

Source launch report: `reports/long_run_3e8_launch_2026-07-10.md`.

Local source summaries:

- `C:\tmp\knoten-longrun-3e8-Aatt20-20260710\summary.json`
- `C:\tmp\knoten-longrun-3e8-Aatt35-20260710\summary.json`

Both jobs completed successfully. Each output directory contains five
`baseline` cases, five `eta_zero` cases, and `summary.json`. Both `stderr.log`
files were empty.

## Parameters

Shared parameters:

- steps: `300000000`
- dim: `3`
- seeds: `1..5`
- conditions: `baseline,eta_zero`
- epsilon: `0.03`
- eta: `0.15`
- alpha: `0.01`
- memory_mass: `1.0`
- sigma_rep: `1.0`
- sigma_att: `3.0`
- amplitude_rep: `1.0`
- A_att: `20` or `35`
- memory_factor: `6.0`
- max_memory: `600`
- burn_in: `0`
- sample_every: `200`
- deposition: default `delta`

Wall time per amplitude job was about `10.38 h`.

## Main Summary

Values are medians over seeds `1..5`. Residence values are reported in memory
times, i.e. units of `alpha^{-1}` updates.

| A_att | condition | v0.5 score | voxel residence | residence gain | memory-center residence | memory-center inside fraction | memory dim | memory roundness |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 20 | baseline | 0.929 | 147.692 | 2.833 | 24.000 | 4.07e-05 | 2.822 | 0.724 |
| 20 | eta_zero | n/a | 52.000 | n/a | 10.000 | 3.33e-06 | 1.321 | 0.229 |
| 35 | baseline | 0.929 | 160.679 | 3.090 | 46.000 | 1.51e-04 | 2.926 | 0.822 |
| 35 | eta_zero | n/a | 52.000 | n/a | 10.000 | 3.33e-06 | 1.321 | 0.229 |

Interquartile ranges:

| A_att | metric | q25 | median | q75 |
| ---: | --- | ---: | ---: | ---: |
| 20 | v0.5 score | 0.929 | 0.929 | 0.929 |
| 20 | residence gain | 2.769 | 2.833 | 2.840 |
| 20 | voxel residence | 141.636 | 147.692 | 149.529 |
| 20 | memory-center residence | 22.000 | 24.000 | 48.000 |
| 20 | memory dim | 2.670 | 2.822 | 2.871 |
| 20 | memory roundness | 0.638 | 0.724 | 0.766 |
| 35 | v0.5 score | 0.929 | 0.929 | 1.000 |
| 35 | residence gain | 2.884 | 3.090 | 4.284 |
| 35 | voxel residence | 144.209 | 160.679 | 214.206 |
| 35 | memory-center residence | 44.000 | 46.000 | 54.000 |
| 35 | memory dim | 2.889 | 2.926 | 2.942 |
| 35 | memory roundness | 0.783 | 0.822 | 0.841 |

## Seed-Level Scorecard

| A_att | seed | score | residence gain | voxel residence | memory compaction gain | memory roundness gain | memory-center residence |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 20 | 1 | 0.929 | 2.833 | 141.636 | 10.243 | 2.001 | 48.000 |
| 20 | 2 | 1.000 | 3.692 | 192.000 | 5.762 | 2.764 | 24.000 |
| 20 | 3 | 0.929 | 2.769 | 149.529 | 8.706 | 3.318 | 22.000 |
| 20 | 4 | 0.929 | 2.840 | 147.692 | 5.711 | 2.122 | 12.000 |
| 20 | 5 | 0.929 | 2.130 | 106.512 | 11.620 | 4.602 | 60.000 |
| 35 | 1 | 1.000 | 4.284 | 214.206 | 16.209 | 2.197 | 54.000 |
| 35 | 2 | 1.000 | 3.090 | 160.679 | 8.462 | 3.415 | 46.000 |
| 35 | 3 | 0.929 | 2.631 | 142.098 | 13.338 | 3.997 | 44.000 |
| 35 | 4 | 0.857 | 7.021 | 365.067 | 8.065 | 2.311 | 22.000 |
| 35 | 5 | 0.929 | 2.884 | 144.209 | 19.257 | 5.225 | 98.000 |

## Interpretation

The `3e8` runs substantially strengthen the v0.5 evidence for compact
memory-cloud confinement against the seed-matched `eta_zero` control. Both
candidate amplitudes pass the score threshold in every seed, with median score
`0.929`. The voxel-residence gain rises above the v0.5 partial threshold:
median gain is `2.833` for `A_att=20` and `3.090` for `A_att=35`.

The memory-cloud shape also separates cleanly from `eta_zero`: baseline memory
shape dimensions are near three and roundness is much larger than the control.
This supports a conservative Paper-I claim of self-interaction-induced compact
memory-cloud regimes in this parameter slice.

However, the fixed final `memory_center` residence is much weaker than the
voxel maximum and has a very small inside fraction over the whole trajectory.
This is not a failure of confinement by itself. It means the observable is
measuring residence near the final memory center only. Over `3e8` updates the
compact region appears to drift, switch, or be repeatedly re-centered. The
current data therefore support a compact co-moving memory-cloud interpretation
more strongly than an immobile spatial knot interpretation.

The global `sample_center` residence is not useful at this scale: its radius is
set by the full long trajectory and becomes almost non-discriminating. It should
remain a drift-control field, not a knot acceptance metric.

## Decision

This carries the Paper-I evidence better than the previous `3M` runs, but it
also sharpens the next methodological requirement.

Supported now:

- `A_att=20` and `A_att=35` are robust scalar candidates in the corrected-sign
  q=3 slice.
- The active runs separate from `eta_zero` in v0.5 score, voxel residence,
  memory compactness, memory shape dimension, and memory roundness.
- `A_att=35` is the tighter and rounder candidate; `A_att=20` remains slightly
  more balanced and less extreme.

Not yet supported:

- a claim of a fixed spatial knot over the full `3e8` trajectory;
- a claim that the final memory center is the correct long-run residence
  observable;
- any photon, oscillator, dimensional-selection, or particle interpretation.

## Next Step

Do not start another broad parameter scan yet.

The next technical step should be a time-local center diagnostic:

1. Record a coarse `memory_center_trace` and `memory_radius_trace` during
   simulation, for example every `10^4` or `10^5` updates.
2. Measure center drift per memory time relative to memory radius.
3. Measure co-moving residence around the contemporaneous memory center, not
   only around the final center.
4. Compare the dynamic-center metrics against `eta_zero`.
5. Re-run a smaller validation first, e.g. `N=3M` or `30M`, before another
   overnight `3e8` run.

If the dynamic center remains compact and slowly moving relative to `eta_zero`,
Paper I can state a much cleaner result: long-lived compact co-moving
memory-cloud regimes rather than fixed-position knots.
