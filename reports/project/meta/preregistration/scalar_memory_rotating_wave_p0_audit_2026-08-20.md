# P0 audit: scalar-memory rotating-wave candidate

Date: 2026-08-20.

Decision: **P0-pass with zero provenance defects**.

Candidate:

\[
\text{k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1}.
\]

The machine audit validates the claim-scoped manifest against schema 1.1,
the canonical text-hash policy, the full native parameter tuple, the exact
initial-history specification, every registered discovery artifact and the
confirmatory seals.

## Frozen facts

- Architecture: native K0-H scalar memory.
- Time law: native discrete map.
- Deterministic candidate:
  \(\alpha=0.01,\ H=1200,\eta=0.15,\varepsilon=0\),
  \(A_{\rm rep}=1,\ A_{\rm att}=3.5\),
  \(\sigma_{\rm rep}=1,\sigma_{\rm att}=3\).
- Circle:
  \(R=0.946517504804225\),
  \(\theta=0.015770381717135\).
- Discovery code revision:
  \(ed98a8872fec3478f3c0c996dec22fd88e1c1bb9\), clean at execution start.
- Discovery used no random seed, trajectory, external clock or topology
  statistic.
- The \(A_{\rm att}=7.0\) parameter holdout remains sealed.
- Later noisy confirmation, if authorized, uses only seeds 101 through 105.

## Branch decision

P0 opens only D0. It does not open center-mechanics Gates A/B/C/E/F1 and does
not transfer any center-mass result into the rotating-wave branch.

D0 must now state whether the candidate object is:

1. a spatial rotating relative equilibrium before quotienting ambient
   rotations; or
2. an internal phase that survives the physically appropriate symmetry
   quotient.

Candidate-targeted topology remains blocked. A stability linearization may be
specified only after D0 fixes this object and its symmetry action.

The machine-readable audit is
reports/project/meta/preregistration/scalar_memory_rotating_wave_p0_audit_2026-08-20.json.
