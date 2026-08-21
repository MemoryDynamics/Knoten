# Prospective reconciliation of the rotating-wave foundation audit

Date: 2026-08-21.

Status: frozen pipeline-reconciliation protocol. The initial foundation audit
was executed from clean revision
`c726ee2c5072b2fa09ea27a939fa93172bcc86f9`. Its immutable result is retained
as `scalar_memory_rotating_wave_foundation_audit_initial_implementation_fail_2026-08-21`.

## 1. Observed failure

Gates A, C, D and E passed. Gate B failed in all five cells only because the
implementation evaluated the registered condition

$$
\eta/\alpha=15
$$

by strict equality of binary `mpmath.mpf` values. That does not implement
Section 4 of the frozen protocol, which explicitly requires exact decimal
arithmetic.

All scientific parts of Gate B were already positive in the failed run:

- maximum finite-sum residual below $8\times10^{-72}$;
- maximum inferred-gain error below $6\times10^{-69}$;
- required radial and tangential signs in all five cells;
- exact decimal $H\alpha=12$ in all five cells.

The continuum panels, their cross-agreement and all original scaling gates
also passed. The observed failure is therefore an audit implementation defect,
not evidence against the rotating-wave branch. The historical failed decision
must nevertheless not be overwritten or renamed.

The initial Markdown renderer also printed its positive reviewer paragraph
unconditionally despite the machine decision `foundation-audit-fail`. The
JSON decision and gates are authoritative. The reconciled renderer must emit
a positive verdict only for a composite pass; this presentation safeguard may
not alter any gate.

## 2. Single authorized correction

Replace only the two registered scaling checks by Python `Decimal` cross
products constructed directly from the stored decimal strings:

$$
\operatorname{Decimal}(\alpha)H=12,
\qquad
\operatorname{Decimal}(\eta)=15\operatorname{Decimal}(\alpha).
$$

Division and binary floating-point equality are forbidden for these two
booleans. Add a unit test covering all five frozen cells.

No source hash, candidate value, quadrature method, precision, Newton count,
partition, residual threshold, gain threshold, branch corridor, certificate
condition, stability condition, continuum target comparison or scaling
threshold may change.

As a non-computational safeguard, condition the rendered positive verdict on
the composite pass and add a unit test for the failed rendering path.

## 3. Rerun and decisions

After committing and pushing this protocol and the single implementation
correction, rerun the complete audit from a clean revision. Do not reuse the
previously generated booleans; all hashes, sums, continuum integrals and
scaling diagnostics must be recomputed.

Decision is `foundation-audit-reconciliation-pass-scoped` only if all five
original composite gates pass. A remaining gate failure is
`foundation-audit-reconciliation-fail`; an exception is
`foundation-audit-reconciliation-inconclusive`.

The original claim boundary remains unchanged. The L5 refinement cell and
the $A_{\rm att}=7$ holdout remain sealed.
