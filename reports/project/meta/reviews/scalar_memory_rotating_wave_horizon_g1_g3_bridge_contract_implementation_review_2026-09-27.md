# G1--G3 bridge contract implementation review

Date: 2026-09-27  
Scope: target-free schema, semantic validator and orchestration only  
Target access: none

## Verdict

`major-amendment-required-target-closed`

The root, homotopy, drift and endpoint-identity paths are fail-closed.  The
first concrete-backend review nevertheless found that G0 and parts of G6
were represented by unverified summary booleans inherited from the v3
horizon-transfer prototype.  A target result built on that contract would
not contain enough primitive evidence for the promised independent audit.

## Findings

### HGB-I01 -- Major: G0 direct replay is a free boolean

The protocol requires direct finite-sum replays, but the schema stores only
`direct_replay_pass`.  The orchestrator asks the backend for a boolean before
any new root exists, so neither the validator nor a future auditor can
reconstruct the replay.

Required remediation: store one ordered replay row per available root,
including the evaluated center, signed residual components and signed sums;
freeze precision and threshold before target access; reconstruct all summary
booleans from those primitives.  The forward rows decide G0, while missing or
failed lower-tail rows may only close the separately reported stress branch.

### HGB-I02 -- Major: G6 mutation detection is a free boolean

The inherited mutation rows contain only a name and `detected=true`.  No
recorded error allows reconstruction.  The extra `drift-width` row is also
not a FIFO mutation and therefore does not belong to the runtime G6 panel.

Required remediation: keep the three registered FIFO mutations only and
store their one-step new-point and complete-state errors.  Reconstruct
`detected` from the frozen `5e-14` threshold.  Drift-width mutation remains a
target-free validator test, not runtime evidence.

### HGB-I03 -- Major: FIFO age-order identity is not auditable

The circular-control record stores one hash, while the semantic validator
checks only the numerical errors.  The promised equality of the input age
order and its circular materialization is therefore absent from the result
contract.

Required remediation: store expected and observed age-history SHA-256 values
and require exact equality.  Also freeze and validate the nine case IDs, not
only their horizons.

## Non-findings and retained boundaries

- No new root, homotopy, G4, G5, trajectory or spectral computation was run.
- The cross-precision and sealed-endpoint Krawczyk inclusions are reconstructed
  from decimal interval endpoints rather than trusted booleans.
- The finite-branch prefix stop rules and local-exclusion precedence remain
  appropriate.
- This amendment cannot authorize a target run.  A new sufficiency review,
  complete target-free tests and the registered authorization sequence remain
  mandatory.
