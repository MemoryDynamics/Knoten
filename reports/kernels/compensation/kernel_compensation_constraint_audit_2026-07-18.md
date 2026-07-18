# Kernel Compensation Constraint Audit

Date: 2026-07-18T05:44:10Z.

## Question

Can the compact two-scale knot candidates (`A_att=20..35`, `q=3`)
also satisfy `integral K = 0`, and can a sigma variation reconcile the
two requirements without a broad parameter scan?

## Exact Two-Scale Constraint

Write `q=sigma_att/sigma_rep>1` and `a=A_att/A_rep`. For the
unnormalized Gaussian convention in the code, zero integral requires

```text
a_zero = q^(-d).
```

Local inward linear drift around a point deposit requires

```text
chi = a/q^2 > 1, equivalently a > q^2.
```

For every `q>1` and `d>=1`, `q^(-d)<1<q^2`. The two conditions are
therefore disjoint in this two-scale ordering. This is a structural
result, not a failure that can be repaired by a generic sigma sweep.
It is also only a local point-deposit test, not a full knot-existence theorem.

## Existing Reference Points

| d | q | A_att | chi | local curvature | attraction/repulsion integral | zero-mean A_att |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | 3.00000 | 20.00000 | 2.22222 | 1.22222 | 540.00000 | 0.03704 |
| 3 | 3.00000 | 35.00000 | 3.88889 | 2.88889 | 945.00000 | 0.03704 |
| 10 | 3.00000 | 20.00000 | 2.22222 | 1.22222 | 1.18098e+06 | 1.69351e-05 |
| 10 | 3.00000 | 35.00000 | 3.88889 | 2.88889 | 2.06672e+06 | 1.69351e-05 |

The q=3 candidates are locally restoring, but their unnormalized
integrals are attraction dominated by factors from hundreds (d=3)
to millions (d=10). Thus they do not approximate a neutral kernel.

## Figures

- [two_scale_constraint_map](../../../figures/draft/kernels/compensation_2026-07-18/two_scale_constraint_map.png)
- [three_scale_compensation](../../../figures/draft/kernels/compensation_2026-07-18/three_scale_compensation.png)
- [compensated_point_field](../../../figures/draft/kernels/compensation_2026-07-18/compensated_point_field.png)

## Controlled Sigma Test

The next simulation varies one scale ratio only while preserving
`chi=3.8888889`, the q=3, A_att=35 local stiffness ratio.
This separates scale geometry from the already known curvature effect.

| q | A_att at fixed chi | local curvature |
| ---: | ---: | ---: |
| 2.00000 | 15.55556 | 2.88889 |
| 3.00000 | 35.00000 | 2.88889 |
| 4.00000 | 62.22222 | 2.88889 |

Planned fixed parameters: `d=3`, `N=1M`, seeds `1..5`,
`epsilon=1e-4`, `eta=0.15`, `lambda=0.01`, `M0=1`, delta
deposition, `sigma_rep=1`, with seed-matched `eta_zero` controls.
This is a mechanism pilot, not a long-run knot claim.

## Broad Third-Scale Compensation

A minimal neutral extension is

```text
K3 = A_rep G(sigma_rep) - A_att G(sigma_att) + A_comp G(sigma_comp),
A_comp = (A_att sigma_att^d - A_rep sigma_rep^d) / sigma_comp^d.
```

The final broad positive term cancels the integral. Its reduction of
the local restoring curvature is `A_comp/sigma_comp^2`, which decays
rapidly with a broad compensator.

| d | A_att | sigma_comp | A_comp | curvature retained | residual integral coefficient |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | 20.00000 | 5.00000 | 4.31200 | 0.85888 | 0 |
| 3 | 20.00000 | 10.00000 | 0.53900 | 0.99559 | 0 |
| 3 | 20.00000 | 30.00000 | 0.01996 | 0.99998 | 0 |
| 3 | 20.00000 | 100.00000 | 5.39000e-04 | 1.00000 | 0 |
| 3 | 35.00000 | 5.00000 | 7.55200 | 0.89543 | 0 |
| 3 | 35.00000 | 10.00000 | 0.94400 | 0.99673 | 0 |
| 3 | 35.00000 | 30.00000 | 0.03496 | 0.99999 | -1.13687e-13 |
| 3 | 35.00000 | 100.00000 | 9.44000e-04 | 1.00000 | 0 |
| 10 | 20.00000 | 5.00000 | 0.12093 | 0.99604 | 0 |
| 10 | 20.00000 | 10.00000 | 1.18098e-04 | 1.00000 | 0 |
| 10 | 20.00000 | 30.00000 | 2.00000e-09 | 1.00000 | 0 |
| 10 | 20.00000 | 100.00000 | 1.18098e-14 | 1.00000 | 0 |
| 10 | 35.00000 | 5.00000 | 0.21163 | 0.99707 | -2.32831e-10 |
| 10 | 35.00000 | 10.00000 | 2.06671e-04 | 1.00000 | -2.32831e-10 |
| 10 | 35.00000 | 30.00000 | 3.50000e-09 | 1.00000 | 0 |
| 10 | 35.00000 | 100.00000 | 2.06671e-14 | 1.00000 | 0 |

## Decision

1. Do not reinterpret `A_att=20..35` as approximately zero mean.
2. Do not launch an unconstrained sigma sweep.
3. Run the fixed-chi q slice first to test whether compactness is
   controlled mainly by local curvature or also by scale separation.
4. If the compact branch survives that slice, implement one broad
   compensated third-scale pilot with exact integral cancellation.
5. Keep kernel neutrality as a cross-knot/far-field hypothesis, not
   as an axiom of the self-confining scalar memory channel.

## Provenance

- Git revision: `fc7e8928ad35de3424303f557280d5cbca27505e`
- Git status at generation: `clean`
- Script: `experiments/current/kernels/kernel_compensation_audit.py`
