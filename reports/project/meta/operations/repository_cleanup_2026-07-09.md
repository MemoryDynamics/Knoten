# Repository Cleanup

Date: 2026-07-09.

## Scope

This cleanup keeps the active documentation surface small and removes local
private-note clutter from the working tree. It does not rewrite Git history.

## Actions

- Removed local ignored cleartext reviewer handoff notes from `reports/`.
- Renamed the sanitized public privacy/control report to
  `reports/project/governance/privacy_and_control_plan_2026-07-08.md`.
- Updated the seven active MkDocs pages to reflect the current matched
  deposition, v0.5 score, M0/alpha-one controls, and Paper-I claim boundary.
- Kept the active documentation surface at seven MkDocs pages:
  `index`, `current_status`, `project_priorities`, `THEORETICAL_CONTEXT`,
  `repository_map`, `experiment_catalog`, and `paper_claims`.

## Current Scientific Reading

Paper I should currently claim effective memory-feedback confinement against
`eta_zero`, not a necessary two-scale mechanism. The normalized
`matched_deposition` pilot remains confined relative to `eta_zero`, but is
broader than the delta baseline because normalized Gaussian convolution lowers
local stiffness. The next targeted experiment is a curvature-renormalized
matched-deposition condition.

## Privacy State

Tracked files should not contain person-specific reviewer handoff material. A
tracked privacy grep is part of the final validation for this cleanup.
