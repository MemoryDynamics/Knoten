# N-Dependence Recheck

Date: 2026-07-16T04:25:39Z.

## Scope

This is a reconciliation plot, not a new long run. It combines three already
available evidence layers:

- scalar formation scaling `N=100k..3M`, `epsilon=0.03`, `A_att in {20,35}`;
- the `N=30M`, `epsilon=1e-4` scalar reference slice;
- the short `N=200k` raw-memory-snapshot D_spec pilot.

The parameter sets are not identical, so the figure should be read as a
sanity check for qualitative N-behavior, not as a fitted scaling law.

## Figures

- [n_dependence_recheck_overview_2026-07-16](../../../figures/draft/scalar_n/n_dependence_recheck_2026-07-16/n_dependence_recheck_overview_2026-07-16.png)

## Scalar N-Scaling Summary

| A_att | N | memory D | memory radius | roundness | D_win | residence gain |
| ---: | ---: | --- | --- | --- | --- | --- |
| `20` | `100,000` | 2.787 [2.758, 2.817] | 0.087 [0.087, 0.089] | 0.722 [0.721, 0.723] | 1.675 | 1.429 |
| `20` | `300,000` | 2.919 [2.896, 2.924] | 0.092 [0.081, 0.094] | 0.816 [0.791, 0.819] | 1.803 | 1.560 |
| `20` | `1,000,000` | 2.712 [2.643, 2.818] | 0.085 [0.085, 0.092] | 0.673 [0.657, 0.722] | 1.897 | 1.237 |
| `20` | `3,000,000` | 2.723 [2.631, 2.730] | 0.092 [0.091, 0.096] | 0.655 [0.645, 0.709] | 2.016 | 1.584 |
| `35` | `100,000` | 2.936 [2.934, 2.940] | 0.060 [0.059, 0.060] | 0.833 [0.832, 0.843] | 1.650 | 0.911 |
| `35` | `300,000` | 2.953 [2.900, 2.965] | 0.060 [0.057, 0.061] | 0.856 [0.792, 0.874] | 1.865 | 1.423 |
| `35` | `1,000,000` | 2.868 [2.845, 2.892] | 0.060 [0.059, 0.061] | 0.772 [0.745, 0.784] | 1.953 | 1.091 |
| `35` | `3,000,000` | 2.885 [2.849, 2.912] | 0.060 [0.060, 0.062] | 0.786 [0.777, 0.829] | 2.084 | 1.684 |

## N30M Reference Summary

| A_att | condition | N | memory D | memory radius | roundness | drift/r per tau_mem |
| ---: | --- | ---: | --- | --- | --- | --- |
| `20` | `baseline` | `30,000,000` | 2.803 [2.783, 2.857] | 2.897e-04 [2.849e-04, 2.902e-04] | 0.719 [0.696, 0.752] | 0.072 |
| `20` | `eta_zero` | `30,000,000` | 1.903 [1.480, 2.411] | 0.002 [0.002, 0.002] | 0.453 [0.223, 0.577] | 0.320 |
| `35` | `baseline` | `30,000,000` | 2.941 [2.920, 2.944] | 1.976e-04 [1.965e-04, 2.012e-04] | 0.843 [0.814, 0.847] | 0.044 |
| `35` | `eta_zero` | `30,000,000` | 1.903 [1.480, 2.411] | 0.002 [0.002, 0.002] | 0.453 [0.223, 0.577] | 0.320 |

## Raw Snapshot Pilot

| dim | condition | N | shape D | heat D_spec | valid heat windows |
| ---: | --- | ---: | --- | --- | --- |
| `3` | `baseline` | `200,000` | 2.949 [2.894, 2.956] | 1.574 [1.574, 1.652] | 7.000 |
| `3` | `eta_zero` | `200,000` | 2.122 [1.680, 2.125] | 1.102 [1.041, 1.133] | 6.000 |
| `10` | `baseline` | `200,000` | 9.173 [8.860, 9.175] | - | 0.000 |
| `10` | `eta_zero` | `200,000` | 3.100 [2.883, 3.444] | 0.917 [0.891, 0.933] | 6.000 |

## Reading

- Exact `3D` is not the right hard acceptance criterion. A physically
  relevant sector may be flattened or effectively lower-dimensional under
  angular-momentum-like constraints; the stronger criterion is stable
  active dimension or response rank, contrasted against controls.
- The old `N=100k..3M` scalar scaling behaves as before: compact memory
  clouds form early, while residence is noisy and not monotone.
- The `N=30M` reference slice is qualitatively consistent on memory shape
  but uses a different epsilon scale, so it should not be used to fit the
  older N-curve.
- The `N=200k` raw snapshot point is a pipeline check. It is too short to
  settle the D_spec question and does not reproduce a robust near-three
  Heat-Trace signal.

## Two-Knot Guardrail

For a future response-rank test, start in a weak-probe regime rather than a
free collision regime: separate memories, large initial separation,
`eta_cross << eta_self`, and a small controlled displacement or field kick.
The first observable should be a linear response matrix, not whether two
free knots merge or become tangled.

Machine-readable summary: `reports/long_runs/scalar_hardening/n_dependence_recheck_summary_2026-07-16.json`.
Git revision while building: `fd9127951dfb239881e9da5b39da01039cdfaba8`.
Git status while building: `?? experiments/current/dynamics/n_dependence_recheck_report.py; ?? figures/draft/scalar_n/n_dependence_recheck_2026-07-16/; ?? reports/long_runs/scalar_hardening/n_dependence_recheck_summary_2026-07-16.json; ?? tests/test_n_dependence_recheck_report.py`.
