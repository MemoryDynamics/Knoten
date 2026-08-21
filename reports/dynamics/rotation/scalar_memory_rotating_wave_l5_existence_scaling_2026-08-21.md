# Scalar-memory rotating-wave L5 existence and scaling gate

Generated: 2026-08-21T20:52:46.352400+00:00.

Decision: **l5-existence-scaling-pass**.

Execution revision: `a8787cdefd12b86e13928613790708883e2c55e1`.
Frozen protocol revision: `0add69c9898802f192984975786147429586fd8c`.

## Provenance

Frozen input/protocol gate: **True**.
The hash domain is the exact versioned `HEAD:path` Git blob.

## L5 interval panels

| dps | R | Omega | point residual | outer | inner | panel |
| ---: | ---: | ---: | ---: | :---: | :---: | :---: |
| 80 | 0.9435346582 | 1.584515864 | 4.118046072e-84 | True | True | True |
| 120 | 0.9435346582 | 1.584515864 | 1.134548413e-123 | True | True | True |

Cross-precision agreement and enclosure overlap: **True**.

Strict Krawczyk interior inclusion is the local existence and
box-uniqueness certificate. The two precision panels are not
independent interval implementations or a proof-assistant check.

## Independent finite-sum replay

Replay pass: **True**.

- maximum residual: `1.2966343468618799161e-72`
- maximum gain error: `1.2394677749172849218e-68`
- radial/tangential signs: `True`

This replay checks signs, indexing and arithmetic; it is not a
second interval proof.

## L0--L5 scaling

| cell | alpha | R error | Omega error |
| --- | ---: | ---: | ---: |
| L0 | 0.04 | 0.01410430535 | 0.0355335699 |
| L1 | 0.02 | 0.006886989011 | 0.01729287646 |
| L2 | 0.01 | 0.003404198035 | 0.008531906004 |
| L3 | 0.005 | 0.001692504936 | 0.004237785231 |
| L4 | 0.0025 | 0.0008438815925 | 0.002111907176 |
| L5 | 0.00125 | 0.0004213514663 | 0.00105421419 |

| observable | slope | signed error ratio | difference ratio | Richardson rel. | pass |
| --- | ---: | ---: | ---: | ---: | :---: |
| radius | 1.007375713 | 0.4993016438 | 0.4979006639 | 0.002797332036 | True |
| omega | 1.008619753 | 0.4991763851 | 0.4975322942 | 0.003299895309 | True |

## Claim boundary

A full pass supports one locally unique L5 prepared-loop balance
root in the declared boxes and finite L0--L5 first-order scaling.
It does not establish a stable family, spontaneous formation, an
internal phase or torus, intrinsic spin, mechanics or interactions.
