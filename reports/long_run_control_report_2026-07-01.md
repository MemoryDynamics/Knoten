# Long-Run Control Report

Date: 2026-07-01.

## Scope

This report combines the matched five-seed long-run ensembles for the canonical `dim=3`, `alpha=0.01`, `n=10^7` setting. It is the first control report for the Paper-I knot-evidence question.

Conditions:

- `baseline`: full current kernel configuration.
- `eta_zero`: true negative control with `eta = 0`, hence no memory-gradient feedback.
- `single_scale`: kernel-class ablation with `amplitude_att = 0`; this is still a self-interacting dynamics and should not be read as a no-knot negative control.

All cases use `steps = 10,000,000`, `burn_in = 1,000,000`, `sample_every = 1000`, `dim = 3`, `alpha = 0.01`, `epsilon = 0.03`, `eta = 0.15` except for `eta_zero`, and seeds `1..5`.

Source case directories:

- `data/processed/long_run_metastability/2026-06-29_initial`
- `data/processed/long_run_metastability/2026-06-30_baseline_seeds`
- `data/processed/long_run_metastability/2026-06-30_controls`
- `data/processed/long_run_metastability/2026-06-30_eta_zero_seeds`
- `data/processed/long_run_metastability/2026-06-30_single_scale_seeds`

## Completeness Check

| Condition | Seeds found | Missing seeds |
| --- | --- | --- |
| `baseline` | `1,2,3,4,5` | `none` |
| `eta_zero` | `1,2,3,4,5` | `none` |
| `single_scale` | `1,2,3,4,5` | `none` |

The source JSON files were generated across several repository revisions, but the recorded base parameters match across the combined cases. This report is therefore a statistical synthesis of already produced runs, not a fresh simulation.

## Seed-Level Results

| Condition | Seed | Best residence (`alpha^-1`) | Best voxel | Max @ 0.5 | Max @ 1.0 | Max @ 2.0 | `D_cov` | `D_occ` | Mean radius |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `1` | `256.0` | `2.0` | `140.0` | `204.0` | `256.0` | `1.699` | `1.792` | `5.483` |
| `baseline` | `2` | `406.7` | `2.0` | `130.0` | `255.0` | `406.7` | `2.061` | `1.859` | `2.202` |
| `baseline` | `3` | `207.5` | `2.0` | `123.3` | `162.5` | `207.5` | `2.519` | `1.849` | `3.053` |
| `baseline` | `4` | `318.0` | `2.0` | `160.0` | `205.0` | `318.0` | `1.422` | `1.815` | `5.097` |
| `baseline` | `5` | `1000.0` | `2.0` | `140.0` | `290.0` | `1000.0` | `1.516` | `1.791` | `3.566` |
| `eta_zero` | `1` | `80.0` | `2.0` | `15.0` | `40.0` | `80.0` | `1.699` | `1.727` | `80.886` |
| `eta_zero` | `2` | `100.0` | `2.0` | `10.0` | `40.0` | `100.0` | `2.061` | `1.818` | `32.493` |
| `eta_zero` | `3` | `70.0` | `2.0` | `15.0` | `30.0` | `70.0` | `2.520` | `1.784` | `45.080` |
| `eta_zero` | `4` | `80.0` | `2.0` | `10.0` | `40.0` | `80.0` | `1.421` | `1.765` | `75.281` |
| `eta_zero` | `5` | `70.0` | `2.0` | `30.0` | `40.0` | `70.0` | `1.515` | `1.732` | `52.682` |
| `single_scale` | `1` | `780.0` | `1.0` | `90.0` | `780.0` | `300.4` | `1.699` | `1.794` | `5.276` |
| `single_scale` | `2` | `567.5` | `2.0` | `106.7` | `238.0` | `567.5` | `2.061` | `1.860` | `2.119` |
| `single_scale` | `3` | `290.0` | `2.0` | `165.0` | `161.2` | `290.0` | `2.519` | `1.852` | `2.939` |
| `single_scale` | `4` | `273.8` | `2.0` | `170.0` | `136.9` | `273.8` | `1.422` | `1.816` | `4.905` |
| `single_scale` | `5` | `1577.1` | `2.0` | `115.0` | `186.7` | `1577.1` | `1.516` | `1.794` | `3.432` |

## Condition Summary

| Condition | Metric | Mean | SD | Median | Min | Max |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `baseline` | best residence (`alpha^-1`) | `437.633` | `323.063` | `318.000` | `207.500` | `1000.000` |
| `baseline` | max residence @ voxel 0.5 | `138.667` | `13.864` | `140.000` | `123.333` | `160.000` |
| `baseline` | max residence @ voxel 1.0 | `223.300` | `49.643` | `205.000` | `162.500` | `290.000` |
| `baseline` | max residence @ voxel 2.0 | `437.633` | `323.063` | `318.000` | `207.500` | `1000.000` |
| `baseline` | `D_cov` | `1.843` | `0.450` | `1.699` | `1.422` | `2.519` |
| `baseline` | `D_occ` | `1.821` | `0.032` | `1.815` | `1.791` | `1.859` |
| `baseline` | mean centered radius | `3.880` | `1.383` | `3.566` | `2.202` | `5.483` |
| `baseline` | max centered radius | `7.678` | `2.179` | `7.270` | `4.903` | `10.683` |
| `eta_zero` | best residence (`alpha^-1`) | `80.000` | `12.247` | `80.000` | `70.000` | `100.000` |
| `eta_zero` | max residence @ voxel 0.5 | `16.000` | `8.216` | `15.000` | `10.000` | `30.000` |
| `eta_zero` | max residence @ voxel 1.0 | `38.000` | `4.472` | `40.000` | `30.000` | `40.000` |
| `eta_zero` | max residence @ voxel 2.0 | `80.000` | `12.247` | `80.000` | `70.000` | `100.000` |
| `eta_zero` | `D_cov` | `1.843` | `0.451` | `1.699` | `1.421` | `2.520` |
| `eta_zero` | `D_occ` | `1.765` | `0.038` | `1.765` | `1.727` | `1.818` |
| `eta_zero` | mean centered radius | `57.284` | `20.406` | `52.682` | `32.493` | `80.886` |
| `eta_zero` | max centered radius | `112.943` | `32.226` | `106.961` | `71.985` | `157.488` |
| `single_scale` | best residence (`alpha^-1`) | `697.679` | `534.579` | `567.500` | `273.750` | `1577.143` |
| `single_scale` | max residence @ voxel 0.5 | `129.333` | `36.029` | `115.000` | `90.000` | `170.000` |
| `single_scale` | max residence @ voxel 1.0 | `300.568` | `270.616` | `186.667` | `136.923` | `780.000` |
| `single_scale` | max residence @ voxel 2.0 | `601.766` | `558.598` | `300.435` | `273.750` | `1577.143` |
| `single_scale` | `D_cov` | `1.843` | `0.450` | `1.699` | `1.422` | `2.519` |
| `single_scale` | `D_occ` | `1.823` | `0.032` | `1.816` | `1.794` | `1.860` |
| `single_scale` | mean centered radius | `3.734` | `1.331` | `3.432` | `2.119` | `5.276` |
| `single_scale` | max centered radius | `7.391` | `2.097` | `6.999` | `4.721` | `10.282` |

## Paired Seed Differences

Positive values mean the baseline has longer best residence than the control for the same seed.

| Control | Seed differences baseline - control | Mean | Median |
| --- | --- | ---: | ---: |
| `eta_zero` | `176.0, 306.7, 137.5, 238.0, 930.0` | `357.633` | `238.000` |
| `single_scale` | `-524.0, -160.8, -82.5, 44.2, -577.1` | `-260.045` | `-160.833` |

## Interpretation

1. The true no-feedback control `eta_zero` is clearly separated from the interacting conditions. Its best residence is `80.0 +/- 12.2 alpha^-1`, while baseline is `437.6 +/- 323.1 alpha^-1` and `single_scale` is `697.7 +/- 534.6 alpha^-1`.
2. `eta_zero` also diffuses over a much larger region: mean centered radius is `57.284 +/- 20.406`, compared with `3.880 +/- 1.383` for baseline and `3.734 +/- 1.331` for `single_scale`. This supports the weaker claim that memory-gradient feedback creates compact long-residence regimes relative to free/no-feedback motion.
3. `single_scale` does not behave like a negative control. It is as compact as baseline and often more persistent. Therefore the current data do not show that the two-scale baseline kernel is necessary for long-lived residence.
4. `D_cov` and `D_occ` are not decisive knot diagnostics in this control set. `D_occ` stays near `1.8` for all three conditions, and `D_cov` is dominated by seed-to-seed geometry rather than condition separation.
5. The current `candidate_long_lived` threshold is too permissive for Paper-I evidence: even `eta_zero` satisfies it. Future reports need a criterion that combines residence, compactness, voxel sensitivity, and separation from controls.

## Evidence Status

Current conservative statement:

```text
In the tested long-run slice, memory-gradient feedback produces compact
long-residence regimes relative to the eta=0 control. The existence of
a specifically two-scale attractive-repulsive knot mechanism is not yet
supported, because the single-scale ablation remains compact and long-lived.
```

Paper-I status: this is useful evidence for self-interaction-induced confinement, but not yet sufficient for a strong claim of robust dynamical knots tied to the baseline two-scale kernel.

## Next Steps

1. Reclassify `single_scale` as a kernel-class ablation, not a negative control.
2. Define a stricter knot score from existing diagnostics: residence above control, compactness relative to `eta_zero`, stability across voxel sizes, and seed robustness.
3. Extend the long-run output with reduced shape/center stability metrics so future runs can distinguish genuine localized regimes from coarse voxel residence.
4. Add one further one-parameter kernel ablation only after the score is fixed, e.g. an `amplitude_rep = 0` long-scale-only condition, to map which kernel component provides confinement.
5. Only after these criteria separate baseline or a chosen kernel class from controls should a Paper-I evidence table be promoted.
