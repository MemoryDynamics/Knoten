# d10 Memory Controls and A_att Sweep

Date: 2026-07-14.

## Scope

This note records three targeted controls for the scalar finite-memory
model at ambient dimension `d=10`:

1. a short `beta=0` reference via `M0=0`,
2. a long `N=300M` confirmation of the `A_att=35` d10 memory geometry,
3. a screening sweep over `A_att` at `N=10M`.

The runs use the corrected q=3 scalar two-scale kernel slice with
`epsilon=1e-4`, `eta=0.15`, `alpha=0.01`, `A_rep=1`, `sigma_rep=1`,
`sigma_att=3`, delta deposition, `memory_factor=6`, `max_memory=800`,
and seeds `1..5` unless noted otherwise.

## beta=0 / M0=0 Reference

In the current parameterization `beta = lambda M0`. Therefore the
`beta=0` control is represented by `M0=0`, implemented as condition
`m0_zero`.

Source:
`data/processed/long_run_metastability/beta_zero_reference_Aatt_35_N1M_d10_seed1-5_eps1em4_2026-07-14`

| condition | N | seeds | D_occ mean | D_mem mean | D_spec mem mean | radius mean | drift/r mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 1,000,000 | 5 | 0.465 | 9.049 | 2.769 | 3.836e-4 | 0.116 |
| m0_zero | 1,000,000 | 5 | 0.704 | 0.000 | 0.000 | 0.000 | 0.000 |

Reading: `M0=0` is a degenerate no-memory-field control. The circular
position buffer still exists internally, but all memory weights vanish,
the self-potential is skipped, and weighted memory-center diagnostics
collapse to the current point. This is useful as a strict beta-zero
check, but it is not interchangeable with `eta_zero`, where the weighted
memory trace still exists but does not feed back into motion.

## d10 N-Stability at A_att=35

Sources:

- `data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N30M_d10_seed1-5_eps1em4_2026-07-13`
- `data/processed/long_run_metastability/ambient_dim_memory_shape_Aatt_35_N300M_d10_seed1-5_eps1em4_foreground_2026-07-14`

| run | condition | seeds | D_occ mean | D_occ window mean | D_cov mean | D_spec sample mean | D_mem mean | D_mem sd | D_spec mem mean | D_spec mem sd | radius mean | drift/r mean |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| N30M | baseline | 5 | 1.813 | 1.848 | 1.947 | 1.304 | 9.033 | 0.192 | 2.714 | 0.069 | 3.813e-4 | 0.049 |
| N300M | baseline | 5 | 1.684 | 1.555 | 2.634 | 1.350 | 9.186 | 0.139 | 2.732 | 0.108 | 3.813e-4 | 0.028 |
| N30M | eta_zero | 5 | 1.686 | 1.603 | 1.946 | 1.304 | 2.492 | 0.584 | 1.288 | 0.013 | 2.045e-3 | 0.330 |
| N300M | eta_zero | 5 | 1.654 | 1.509 | 2.634 | 1.350 | 2.896 | 0.664 | 1.314 | 0.085 | 2.043e-3 | 0.206 |

Reading: the d10 baseline memory geometry is stable from `N=30M` to
`N=300M`. `D_mem` remains near 9 and `D_spec_mem` remains near 2.7; the
radius is unchanged, while radius-normalized drift decreases at longer
N. This supports N-stability of the d10 memory shape, but it does not
support a drift toward a universal 3D memory dimension at d10.

## A_att Sweep at d10

Source pattern:
`data/processed/long_run_metastability/Aatt_sweep_d10_N10M_Aatt_*_seed1-5_eps1em4_2026-07-14`

All rows are baseline-only, `N=10M`, seeds `1..5`.

| A_att | D_occ | D_occ window | D_cov | D_spec sample | D_mem | D_mem sd | D_spec mem | D_spec mem sd | roundness | radius | drift/r | residence |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1.0957 | 1.0662 | 1.1107 | 1.1935 | 1.0000 | 0.0000 | 1.1909 | 0.0000 | 0.0001 | 3.0559 | 1.0523 | 0.0 |
| 0.1 | 1.0821 | 1.0610 | 1.1299 | 1.1940 | 1.0000 | 0.0000 | 1.1909 | 0.0000 | 0.0001 | 2.9582 | 1.0523 | 0.0 |
| 0.35 | 1.0852 | 1.0804 | 1.2214 | 1.1972 | 1.0000 | 0.0000 | 1.1909 | 0.0000 | 0.0001 | 2.7177 | 1.0523 | 0.0 |
| 1 | 1.1945 | 1.1614 | 2.2036 | 1.3159 | 1.0006 | 0.0004 | 1.1909 | 0.0000 | 0.0001 | 2.1380 | 1.0508 | 0.0 |
| 3 | 1.1044 | 1.0882 | 2.0575 | 1.2820 | 1.9276 | 0.0011 | 1.3687 | 0.0005 | 0.0002 | 0.8822 | 0.2495 | 0.0 |
| 6 | 0.8489 | 1.5255 | 3.9565 | 1.5573 | 1.7058 | 0.0026 | 1.3008 | 0.0002 | 0.0005 | 0.4632 | 0.1270 | 21.3 |
| 9 | 1.4002 | 1.4069 | 2.5238 | 1.3566 | 2.4889 | 0.5219 | 1.3302 | 0.1116 | 0.1048 | 0.0020 | 0.4801 | 973.0 |
| 20 | 1.4160 | 1.7615 | 2.5266 | 1.3570 | 8.2819 | 0.2222 | 2.3873 | 0.1203 | 0.4893 | 5.3825e-4 | 0.1059 | 377.6 |
| 35 | 1.3883 | 1.7523 | 2.5316 | 1.3580 | 9.1562 | 0.1376 | 2.7440 | 0.1331 | 0.6142 | 3.8222e-4 | 0.0650 | 227.1 |

Reading:

- `A_att <= 1` does not produce compact knots in this slice. The memory
  cloud is effectively one-dimensional, very elongated, and has no
  residence signal.
- `A_att=3` and `A_att=6` are still weak or diffuse. The radius remains
  macroscopic relative to the compact `A_att=20/35` cases.
- `A_att=9` is a transition region: compactification appears, but
  `D_mem` is seed-sensitive and drift/r remains high.
- `A_att=20` and `A_att=35` produce compact high-dimensional memory
  clouds in d10. `A_att=35` is rounder and more compact than `A_att=20`.

## Current Interpretation

The d10 data now support a conservative statement:

> For the corrected q=3 scalar kernel slice at `epsilon=1e-4`, compact
> long-lived memory structures require sufficiently strong attractive
> coupling. At d10, the selected `A_att=35` regime is stable in N from
> `30M` to `300M`, but its memory-shape dimension remains high rather
> than drifting toward three.

This sharpens the Paper-II situation. The previous 3D language should
not be phrased as an ambient-dimension-independent theorem. The more
defensible claim is a geometry-reconciliation problem: trajectory
spectral observables, memory spectral observables, and memory-shape
observables measure different aspects of the same finite-memory state.

## Next Targeted Runs

The next useful A_att refinement is not another broad sweep. The
transition region should be probed with `A_att in {7, 8, 9, 10, 12, 15}`
at d10, preferably first with `N=10M` and seeds `1..5`, then only the
most informative candidates at `N=30M`.
