# P3.2d shape-multipole source eligibility

Date: 2026-08-06T21:26:37+00:00.

## Result

Classification: **no control-separated autonomous scalar shape-multipole source**.

- `shape`: baseline 0/5, eta-zero 2/5, shape-bounded 5/5, cross-seed frequency range inf; pass=False.
- `shape_rate`: baseline 0/5, eta-zero 0/5, shape-bounded 5/5, cross-seed frequency range inf; pass=False.

![P3.2d shape multipole](../../figures/draft/response/p32d_shape_multipole_gate_2026-08-06.png)

## Seed diagnostics

| seed | condition | source | peak f | peak/background | shuffle q99 | peak fraction | passing segments | segment frequency range | candidate |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | baseline | shape | 0.068359 | 38.95 | 12.72 | 0.1728 | 4/4 | 0.3333 | False |
| 1 | baseline | shape_rate | 1.0254 | 1.351 | 1.489 | 0.1149 | 0/4 | inf | False |
| 1 | eta_zero | shape | 0.068359 | 332.2 | 25.06 | 0.2637 | 4/4 | 0.5882 | False |
| 1 | eta_zero | shape_rate | 0.18555 | 4.057 | 2.615 | 0.06069 | 0/4 | inf | False |
| 2 | baseline | shape | 0.058594 | 40.01 | 13.36 | 0.1298 | 4/4 | 1 | False |
| 2 | baseline | shape_rate | 1.9238 | 1.298 | 1.469 | 0.1495 | 0/4 | inf | False |
| 2 | eta_zero | shape | 0.068359 | 366.8 | 25.64 | 0.2764 | 4/4 | 0.1429 | True |
| 2 | eta_zero | shape_rate | 0.26367 | 4.287 | 2.612 | 0.06851 | 3/4 | 0.1304 | False |
| 3 | baseline | shape | 0.058594 | 40.24 | 13.1 | 0.1291 | 4/4 | 0.625 | False |
| 3 | baseline | shape_rate | 0.74219 | 1.276 | 1.474 | 0.08202 | 0/4 | inf | False |
| 3 | eta_zero | shape | 0.058594 | 312.3 | 24.63 | 0.197 | 4/4 | 0.5714 | False |
| 3 | eta_zero | shape_rate | 0.3125 | 4.275 | 2.67 | 0.08328 | 2/4 | 0.3273 | False |
| 4 | baseline | shape | 0.058594 | 42.45 | 12.7 | 0.1321 | 4/4 | 1.143 | False |
| 4 | baseline | shape_rate | 0.81055 | 1.307 | 1.415 | 0.09739 | 0/4 | inf | False |
| 4 | eta_zero | shape | 0.058594 | 292.1 | 25.16 | 0.1963 | 4/4 | 0.3333 | False |
| 4 | eta_zero | shape_rate | 0.17578 | 3.821 | 2.534 | 0.06547 | 3/4 | 0.6522 | False |
| 5 | baseline | shape | 0.058594 | 40.63 | 12.62 | 0.1358 | 4/4 | 0.375 | False |
| 5 | baseline | shape_rate | 1.4551 | 1.25 | 1.448 | 0.1553 | 0/4 | inf | False |
| 5 | eta_zero | shape | 0.078125 | 353.6 | 26.32 | 0.3403 | 4/4 | 0.125 | True |
| 5 | eta_zero | shape_rate | 0.24414 | 4.35 | 2.749 | 0.0637 | 3/4 | 0.32 | False |

## Interpretation boundary

This gate tests whether one autonomous scalar shape observable is eligible to source a later tensor channel. It does not insert that channel. A positive spectral peak would not establish propagation, reciprocal loading, spin, charge, dimension, quantization, or a particle identity.

The five future-noise paths still branch from one formation state. They are not five independent knot basins.

## Reproducibility

- preregistration: `reports/project/meta/preregistration/p32d_shape_multipole_preregistration_2026-08-06.md`;
- checkpoint: `data/processed/reference_states/scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16/scalar_Aatt35_d3_seed1_N100000000.npz` at N=100000000;
- git revision: `380b33008d742d46e3b365bb0dfbb2e0d20753ad`;
- git status at start: `clean`;
- runtime: `51.454 s`;
- command: `python experiments/current/memory/synchronization/reciprocity/shape_multipole_eligibility_gate.py`;
- machine-readable summary: `reports/response/source_local/p32d_shape_multipole_gate_2026-08-06.json`.
