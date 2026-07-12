# Epsilon Floor Visual Probe

Date: 2026-07-02T03:03:13Z.

## Scope

This visual probe renders the epsilon-floor cases with panel-specific
scales. It is for shape inspection only; absolute sizes are reported in
the table and in the axis-unit annotations.

## Figure

![Epsilon floor flexible trajectories](/figures/draft/epsilon/epsilon_floor_trajectories_flexible_2026-07-02.svg)

## Results

| epsilon | mean radius | median step | turn mean | span xyz |
| ---: | ---: | ---: | ---: | --- |
| `0` | `0` | `0` | `n/a` | `0, 0, 0` |
| `1e-05` | `7.667e-05` | `3.652e-05` | `-0.344` | `3.322e-04, 2.552e-04, 2.880e-04` |
| `1e-10` | `7.667e-10` | `3.652e-10` | `-0.344` | `3.322e-09, 2.552e-09, 2.880e-09` |
| `1e-20` | `7.667e-20` | `3.652e-20` | `-0.344` | `3.322e-19, 2.552e-19, 2.880e-19` |
| `1e-34` | `7.667e-34` | `3.652e-34` | `-0.344` | `3.322e-33, 2.552e-33, 2.880e-33` |

## Reading

- `epsilon=0` is a fixed-point control for the zero-start baseline and
  therefore collapses to a point.
- Positive epsilon cases look shape-similar under flexible scaling because
  this slice is scale-equivalent: lowering epsilon shrinks the trajectory
  without smoothing its directional statistics.
- Use this figure only together with the numeric epsilon-floor report; panel
  scaling deliberately hides absolute size differences.
