# Dimension Diagnostics over N: d=10, A_att=35

Date: 2026-07-30T23:02:29Z.

## Question

How do four existing dimension diagnostics vary with N for the matched d=10, A_att=35 scalar endpoint ensemble?

![Dimension diagnostics over N](../../figures/draft/dimensions/dimension_over_n_2026-07-30/dimension_over_n_d10_A35.png)

## Matched endpoint set

- Core parameters are identical at all endpoints.
- Seeds `1,2,3` are present at every endpoint.
- Endpoints: `N={200k,1M,3M,10M,30M,300M}`.
- The source files were produced at several revisions; the 200k source
  records unrelated untracked analysis files. This is an endpoint
  reconciliation, not a single continuously checkpointed run.
- Sampling is every 1,000 updates through `N=30M` and every 10,000 at
  `N=300M`. Therefore `D_cov`, `D_occ`, and `D_win` mix N-dependence
  with sampling-cadence sensitivity at the final point.

## Summary

| N | samples | cadence | D_cov | D_occ | D_win | valid D_win | D_mem |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 200,000 | 200 | 1,000 | 3.241 | 0.064 | n/a | 0/3 | 9.188 |
| 1,000,000 | 1,000 | 1,000 | 2.277 | 0.503 | 1.465 | 1/3 | 9.186 |
| 3,000,000 | 3,000 | 1,000 | 2.456 | 1.036 | 1.664 | 2/3 | 8.933 |
| 10,000,000 | 10,000 | 1,000 | 2.625 | 1.412 | 1.778 | 3/3 | 9.201 |
| 30,000,000 | 30,000 | 1,000 | 1.981 | 1.799 | 1.929 | 3/3 | 8.857 |
| 300,000,000 | 30,000 | 10,000 | 2.619 | 1.636 | 1.606 | 3/3 | 9.268 |

## Reading

- Median `D_mem` remains between `8.857` and `9.268`. This is consistent with
  a near-isotropic cloud in the prescribed ten-dimensional ambient
  space; it is not evidence for selection of three dimensions.
- `D_cov` fluctuates rather than converging monotonically. It describes
  the sampled visible path, not the rank of the memory state.
- Raw `D_occ` and valid `D_win` rise through `N=30M`. Their decrease
  at `N=300M` coincides with the tenfold coarser cadence and cannot be
  assigned to N alone from these files.
- The earliest automatic occupancy fits are invalid. They are shown
  for auditability but must not be interpreted as measured plateaus.

## Occupancy measurement-convergence gate

- raw D_occ evaluable/pass: `False/False`;
  training relative range: `2.576`;
  trend per decade: `1.299`.
- automatic D_win evaluable/pass: `False/False`.
- At least one gate is non-evaluable: sampling cadence changes; endpoint files span multiple code revisions; D_win lacks fully valid fit windows.
- This does not erase a visible settling trend. It means that trend
  cannot yet certify measurement convergence for the stability gate.

## Decision

The earlier qualitative dimension-over-N plot is reproduced, now with
matched seed curves and explicit fit/cadence guards. It does not sharpen
a 3D claim. A discriminating follow-up would use one continuously
checkpointed run with fixed sampling cadence or online covariance/
occupancy accumulators; another endpoint sweep would otherwise repeat
the same sampling ambiguity.

## Claim boundary

- No ambient-independent dimension selection is established.
- No N-only law for occupancy dimension is established.
- `D_mem` is a rotation-invariant endpoint-shape diagnostic, not an
  external spacetime dimension.

## Provenance

- Git revision: `a63e52a6f93db4d90e307114186a10e686348b65`
- Git status before generation: `M docs/reference/experiment_catalog.md
 M docs/reference/repository_map.md
 M docs/status/current_status.md
 M docs/status/paper_claims.md
 M docs/status/project_priorities.md
 M experiments/cli.py
 M experiments/current/dimensions/dimension_over_n_reproduction.py
 M figures/README.md
 M reports/README.md
 M reports/dimensions/n_scaling/dimension_over_n_d10_A35_2026-07-30.md
 M reports/dimensions/n_scaling/dimension_over_n_d10_A35_summary_2026-07-30.json
 M src/emergenz_knoten/__init__.py
 M tests/test_dimension_over_n_reproduction.py
?? experiments/current/kernels/field/active_scalar_delta_field_pilot.py
?? figures/draft/kernels/field_2026-07-31/
?? reports/kernels/field/active_scalar_delta_field_pilot_2026-07-31.json
?? reports/kernels/field/active_scalar_delta_field_pilot_2026-07-31.md
?? src/emergenz_knoten/active_scalar_field.py
?? src/emergenz_knoten/measurement_stability.py
?? tests/test_active_scalar_delta_field_pilot.py
?? tests/test_active_scalar_field.py
?? tests/test_measurement_stability.py`
- Script: `experiments/current/dimensions/dimension_over_n_reproduction.py`
