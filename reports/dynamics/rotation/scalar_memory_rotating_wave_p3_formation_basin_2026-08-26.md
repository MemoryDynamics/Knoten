# P3 L3 formation and sampled finite basin

Date: 2026-08-26.

Decision: **`p3-formation-basin-pass`**.

The target-informed sampled-basin panel and target-blind formation
panel are reported separately. Mirror branches are symmetry controls,
not independent replications.

## Pipeline controls

| control | pass |
| --- | :---: |
| provenance | True |
| construction | True |
| registration | True |
| metric_evaluation | True |
| prepared | True |
| mirror_equivariance | True |
| fifo_only_negative | True |
| achiral_negative | True |

## Active histories

| panel | family | branch | initial D0/R | entrance | dwell max | final D0/R | opposite min | phase mean | phase RMS error | stop | pass |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | :---: |
| prepared | prepared_circle | plus | 2.08109e-18 | 0 | 7.42269e-15 | 1.6988e-15 | 1.11342 | 0.00790666 | 1.05262e-16 | completed | True |
| prepared | prepared_circle | minus | 2.08109e-18 | 0 | 7.42269e-15 | 1.6988e-15 | 1.11342 | -0.00790666 | 1.05262e-16 | completed | True |
| basin | ellipse_e0p03 | plus | 0.0322944 | 530 | 6.21978e-15 | 2.36542e-15 | 1.11342 | 0.00790666 | 9.79117e-17 | completed | True |
| basin | ellipse_e0p03 | minus | 0.0322944 | 530 | 6.21978e-15 | 2.36542e-15 | 1.11342 | -0.00790666 | 1.00305e-16 | completed | True |
| basin | ellipse_e0p10 | plus | 0.107949 | 1010 | 1.0235e-14 | 5.61642e-15 | 1.11342 | 0.00790666 | 1.02476e-16 | completed | True |
| basin | ellipse_e0p10 | minus | 0.107949 | 1010 | 1.0235e-14 | 5.61642e-15 | 1.11342 | -0.00790666 | 1.02476e-16 | completed | True |
| basin | warped_geometry_holdout | plus | 0.108219 | 880 | 1.02878e-14 | 2.182e-15 | 1.11342 | 0.00790666 | 1.0191e-16 | completed | True |
| basin | warped_geometry_holdout | minus | 0.108219 | 880 | 1.02878e-14 | 2.182e-15 | 1.11342 | -0.00790666 | 1.06064e-16 | completed | True |
| formation | wrong_rate_ellipse | plus | 0.631874 | 1720 | 5.62717e-14 | 2.83294e-15 | 1.11342 | 0.00790666 | 9.99309e-17 | completed | True |
| formation | wrong_rate_ellipse | minus | 0.631874 | 1720 | 5.62717e-14 | 2.83294e-15 | 1.11342 | -0.00790666 | 9.79532e-17 | completed | True |
| formation | damped_hook_holdout | plus | 0.678731 | 1880 | 5.89449e-14 | 2.36051e-15 | 1.11342 | 0.00790666 | 1.72272e-16 | completed | True |
| formation | damped_hook_holdout | minus | 0.678731 | 1880 | 5.89449e-14 | 2.36051e-15 | 1.11342 | -0.00790666 | 1.72272e-16 | completed | True |

## Negative controls

| control | primary diagnostic | pass |
| --- | ---: | :---: |
| eta=0 FIFO collapse | final reduced norm/R 1.32779e-15 | True |
| active achiral invariant subspace | maximum absolute y 0 | True |

## Decision and limits

Gate components: `{"basin_registration": true, "formation_registration": true, "pipeline_controls": true, "sampled_basin": true, "target_blind_formation": true}`.

A full pass concerns only the registered finite ensemble. A
basin-only outcome does not establish target-blind formation and
does not open P4. No outcome proves an open basin volume, generic
formation, chirality selection from symmetric data, mechanics or
mass.

## Provenance

- freeze revision: `0fd79b3636fe09c377a51200414e46bdf9eb6a9f`;
- execution revision: `1463234052c8fc76ed310fd0be4a864ea7ce01e8`;
- JSON SHA-256: `42469985488ee73e2bd8bb1c6dc4cd339b58684b85f2743fa1b2df340e82fc2b`;
- elapsed seconds: `65.7877`;
- Python / NumPy / SciPy: `3.12.13` / `2.4.6` / `1.18.0`.
