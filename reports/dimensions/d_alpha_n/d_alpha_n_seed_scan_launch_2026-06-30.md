# d-alpha-N Seed Scan Launch

Date: 2026-06-30.

## Purpose

This report records the first seeded d-alpha-N scan following the seed-1
intensity pilot. The goal is to test whether the near-3 effective-dimension
signal survives seed variation and higher supplied embedding dimensions.

## Launched Process

- PID: `31456`
- Commit immediately before launch: `a7c447e`
- Branch: `main`
- Working tree at launch: clean
- stdout: `tmp/d_alpha_n_seed_scan_d3-8_alpha0102_n30k-300k_seed1-5.out.log`
- stderr: `tmp/d_alpha_n_seed_scan_d3-8_alpha0102_n30k-300k_seed1-5.err.log`

## Command

```powershell
python experiments/fractal_analysis/reproduce_dimension_pilot.py `
  --dims 3,4,5,6,7,8 `
  --alpha-list 0.01,0.02 `
  --steps-list 30000,100000,300000 `
  --conditions baseline `
  --seeds 1,2,3,4,5 `
  --engine auto `
  --output data/processed/fractal_analysis/d_alpha_n_seed_scan_d3-8_alpha0102_n30k-300k_seed1-5.json `
  --report-output reports/dimensions/d_alpha_n/d_alpha_n_seed_scan_d3-8_alpha0102_n30k-300k_seed1-5_2026-06-30.md
```

## Parameter Grid

- supplied embedding dimensions: `d = 3, 4, 5, 6, 7, 8`
- alpha values: `0.01, 0.02`
- step counts: `30,000`, `100,000`, `300,000`
- seeds: `1, 2, 3, 4, 5`
- condition: `baseline`
- total runs: `6 * 2 * 3 * 5 = 180`

## Scientific Reading

The supplied dimension `d` is not yet an emergent dimension. It is the ambient
state-space dimension made available to the process. A genuine emergent
three-dimensional signature would mean that, for some parameter range and for
`d >= 3`, the observed effective dimension remains close to 3 across seeds,
larger `N`, and negative controls.

The seed-1 pilot suggested `d=3, alpha=0.01/0.02` as a candidate, but it also
showed that `d=4` can move close to 3 at `N=100,000`. This scan therefore keeps
dimensions above 3 in the grid instead of only refining `d=3`.

## Acceptance Criteria For A Useful Signal

A useful candidate plateau should satisfy all of the following:

1. It is stable across seeds, not a single-seed outlier.
2. It is stable or sharpening along the `N` ladder.
3. It persists for supplied dimensions `d > 3`, if the project hypothesis is
   that excess microscopic dimensions collapse effectively.
4. It separates from `eta_zero`, `single_scale`, and later shuffled-memory
   controls before being used as Paper-I evidence.

This launch does not test controls yet. It only resolves the seeded baseline
surface over `d`, `alpha`, and `N`.
