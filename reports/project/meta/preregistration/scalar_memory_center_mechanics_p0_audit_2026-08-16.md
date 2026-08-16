# P0 audit: scalar memory-center effective mechanics

Date: 2026-08-16.

Decision: **`P0-pass-center-effective-mechanics`** with zero manifest defects.

This is a provenance and branch-authorization result, not new evidence for
mass. It promotes no opened center response to confirmatory status. Instead,
all scalar continuum, visible-port and center-port runs through seeds 1--20
are frozen as discovery evidence, and only Gate A is opened for the named
center candidate.

## Candidate and exact scope

The frozen candidate is `scalar-memory-center-effective-mechanics-v1` in the
canonical K0 scalar-memory architecture. Its narrow claim is that the
normalized finite-
\(H\) memory center \(c\) has a positive passive effective-inertial
realization under the explicitly mathematical port \((f,\dot c)\) in the
registered local matched-alpha regime.

The [manifest](scalar_memory_center_mechanics_p0_manifest_2026-08-16.json)
contains the complete noise, memory, kernel, coupling, integration, horizon,
boundary, input and initialization tuple. It identifies the clean discovery
revision `f2bfa4b402a52a5082dc4cd5644f5e7822eac064`, hashes the procedural
initial-state sources and every material discovery artifact, records every
inspected seed and parameter ladder, and seals new seeds 21--25 plus an
untouched \((\alpha,C,H)=(0.003125,15,4800)\) transfer cell.

The machine audit recomputes every declared SHA-256 digest under the explicit
`sha256-canonical-lf-text-v1` policy and verifies the full Git commit. Text
line endings are normalized to LF before hashing; binary files remain raw.
Its result is:

| item | result |
|---|:---:|
| schema and frozen status | pass |
| candidate, architecture and claim scope | pass |
| full parameter and initialization contract | pass |
| initial-state source hashes | pass |
| discovery ledger and artifact hashes | pass |
| disjoint confirmatory seeds and sealed holdout | pass |
| total defects | **0** |

## Branch authorization

P0 opens only **A: physical port derivation**. It does not authorize a new
response simulation before A closes.

The topology branch is independent and remains sealed:

| gate | status after this P0 |
|---|---|
| A | authorized |
| B | blocked until A passes |
| C | blocked until B passes |
| E | blocked until B passes |
| F1 | blocked until A and B pass |
| D0--D5, F0 | `sealed-no-s1-candidate` |

The distinct [S1 candidate audit](s1_candidate_p0_audit_2026-08-16.md) still
fails with 27 candidate-completeness defects. The center has poles \(0\) and
\(-5\), supplies no S1 candidate, and cannot open D0 by passing a mechanics
manifest.

## Why the retrospective freeze is admissible

The center-port protocol was prospective for its original seeds 16--20, but
the present A--F program was written after those results were seen. Therefore
the old prospective label cannot be recycled: those runs are discovery data
for the new mechanics program. P0 is admissible precisely because it records
that contamination rather than counting the old gate twice. Any future
numerical confirmation must use the newly sealed seeds and untouched cell.

## Reproduction

    python experiments/current/topology/s1_p0_manifest_gate.py --manifest reports/project/meta/preregistration/scalar_memory_center_mechanics_p0_manifest_2026-08-16.json --audit-output reports/project/meta/preregistration/scalar_memory_center_mechanics_p0_audit_2026-08-16.json

The recorded [machine audit](scalar_memory_center_mechanics_p0_audit_2026-08-16.json)
returns exit code zero. The same validator defaults to the independent S1
manifest and returns exit code one there, as required.

## Claim boundary

- **Evidence:** the named center candidate and all discovery choices are
  reproducibly frozen; P0 has no completeness defect.
- **Authorized inference:** Gate A may now ask whether the existing
  microscopic coupling derives \(F_c\,dc\).
- **Not inferred:** physical work, SI mass, material COM semantics, additive
  momentum, S1 topology, phase or autonomous oscillation.
