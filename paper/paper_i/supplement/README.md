# Paper I evidence and reproducibility trace

Status: 2026-10-04. This repository supplement maps each material Paper I
claim to a frozen result, its implementation, an audit or test, and an
explicit exclusion. The machine-readable source is
[`evidence_manifest.json`](evidence_manifest.json).

## Trust boundary

The evidence bundle is frozen at Git commit
[`1bbaa4752907f0bf34e2a4bc8635426042c5a652`](https://github.com/MemoryDynamics/Knoten/tree/1bbaa4752907f0bf34e2a4bc8635426042c5a652).
The first manuscript consolidation is frozen at
[`668e97cdfff0d313d327a8e359918260a4b64835`](https://github.com/MemoryDynamics/Knoten/tree/668e97cdfff0d313d327a8e359918260a4b64835)
and passed [CI 37158282045](https://github.com/MemoryDynamics/Knoten/actions/runs/37158282045).
Git commit identity fixes the bytes; the execution commits stored in the
manifest preserve the earlier numerical provenance.

The Krawczyk statements are conditional computer-assisted proofs under the
declared equations, tail bounds, floating-point-to-interval adapters, and the
single `mpmath.iv` interval backend. The independent auditors reconstruct
records and decisions but do not constitute an independent interval-library
replication.

## Claim map

| ID | Narrow supported statement | Primary record | Boundary that remains open |
| --- | --- | --- | --- |
| C1 | Nine finite long-run slices agree with the retained-mass linear radius law to 0.76% median and 1.15% maximum relative error. | [linear reconciliation](../../../reports/long_runs/scalar_hardening/linear_long_run_reconciliation_2026-07-19.md) | no isolated nonlinear object, inertia, or mass |
| C2 | Matched kernels collapse locally; the fixed-$g$ nonlinearity gate remains preregistered inconclusive. | [kernel comparison](../../../reports/kernels/core/kernel_family_comparison_d3_N300k_2026-07-19.md), [fixed-$g$ gate](../../../reports/kernels/nonlinearity/fixed_g_scale_reconciliation_d3_N300k_A26_2026-07-19.md) | no nonlinear transition or universal kernel equivalence |
| C3 | Seven local finite-$H$ roots and six Krawczyk homotopy edges form one fixed-$\alpha$ branch. | [G1--G3 result](../../../reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_g1_g3_bridge_attempt_2_2026-09-27.md) | no global uniqueness, generic formation, or mechanics |
| C4 | Two local spectral panels and three nonlinear perturbation arms support stability at exactly $H=2400$. | [G5 result](../../../reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_attempt_3_2026-09-17.md) | no full interval spectrum or horizon transfer |
| C5 | Two high-precision panels certify a local $F_\infty$ root under registered tail bounds. | [G4 result](../../../reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_g4_component_2026-09-13.md) | no finite-branch identity or dynamical stability by itself |
| C6 | Existing Krawczyk-image inclusions reconcile the finite/infinite local endpoint identity post hoc. | [endpoint reconciliation](../../../reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_infinity_endpoint_lemma_reconciliation_2026-10-01.md) | Attempt 4 remains inconclusive; no second backend or $H\to\infty$ stability |

## Verification

Install the pinned direct runtime and test dependencies, then verify the
manifest contract and the corresponding record contracts:

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
python -m pip install -e .
python -m pytest tests/test_paper_i_evidence_trace.py \
  tests/test_linear_long_run_reconciliation.py \
  tests/test_kernel_family_comparison.py \
  tests/test_fixed_g_scale_reconciliation.py \
  tests/test_rotating_wave_horizon_g1_g3_bridge.py \
  tests/test_rotating_wave_horizon_g5_component.py \
  tests/test_rotating_wave_horizon_g4_component.py \
  tests/test_rotating_wave_horizon_infinity_endpoint_lemma_reconciliation.py -q
```

These commands verify frozen records, source relationships, and decision
contracts. They intentionally do not rerun consumed one-shot production
leases. Re-executing such a gate would be a new experiment and requires new
prospective governance rather than a reproduction shortcut.

## Release boundary

This trace closes the path-to-source ambiguity but not archival release
readiness. Four items remain: a second interval backend, a transitive lock
with artifact hashes, unambiguous author/preferred-citation metadata for
`CITATION.cff`, and an immutable release identifier or DOI. None of these
administrative or replication steps may broaden the scientific claims.
