# Archive-only FIFO normal slope check

Status at registration: explicitly authorized by the author, not executed.
Approval: "Ja, nur die archivierten Koeffizienten pruefen". This is a new
bounded analysis of saved data, not reuse of the original simulation approval.

## Fixed inputs and budget

- Candidate: `k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1`, unchanged parameters.
- Immutable archive revision: `fdbd24fd437187a4db185d413f4c3bd022104b3b`.
- Input directory: `reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25`.
- Only `receipt.json`, `panel_80.json`, `panel_120.json` are used from that
  archive. The receipt is bound to original execution
  `16f60f5a12281628a55eb5e591fe027418d21a3a` and its registered root input.
- One subprocess per dataset, ordered 80 then 120, at most 30 seconds each,
  including interpreter startup, archive read and arithmetic. No retry.
- No new root, kernel, trajectory, parameter or eigensolver evaluation.
- Execution requires reviewed code, passing synthetic tests, a clean frozen
  revision, an exclusive output directory and a receipt before any target work.

## Arithmetic and decision

The saved descending polynomial is `[1, sum(c)-1, -c1, ..., -c_(H-1)]`.
Decode finite binary interval endpoints into exact rational numbers; ignore
display strings. Compute the interval for `S=1+sum(j*c_j)` with integer
weights. There is no additional floating-point summation error.

A strictly negative upper endpoint proves a real normal-form multiplier
greater than one by the elementary argument in section 6 of the
[method contract](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/docs/reference/fifo_normal_stability_contract.md).
Both datasets must have negative upper endpoints and overlapping intervals
for the combined `positive-real-normal-mode-certified` decision. Disjoint
intervals imply `method-inconsistent`; all other combined outcomes remain
`not-established`, never a stability pass.

This trusts the original root/coefficient enclosure and its `mpmath.iv`
backend; it does not independently recertify them. The previous inconclusive
Schur result remains unchanged. No exact growth rate, nonlinear endpoint,
formation, particle interpretation or conclusion about all FIFO states follows.

Synthetic controls cover decoding, sign/index mapping, zero boundaries,
non-pass counterexamples, exactness beyond float64, archive validation,
authorization, exclusive writes and timeout termination before target execution.

## Closure

Executed once per archived dataset on 2026-10-26 from frozen revision
`a155b7b5daad3c31f2c4c8b84bdf6699a946f70b`, after 198 local tests,
lint and strict documentation build passed. Both runs completed below
30 seconds and returned `positive-real-normal-mode-certified`.
[Result and limits](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_archived_normal_slope_2026-10-26/report.md).
Authorization consumed; no repeat or further target execution is authorized.
