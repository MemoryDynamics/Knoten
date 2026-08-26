# Prospective referee and publication-source audit charter after P4

Date: 2026-08-26.

Status: **frozen before implementation or target access for P4-R-phi.**

This charter defines a broad internal red-team review of the evidence chain
through P4-R-phi. It is additional to, and cannot replace, the gate-specific
P4 and P4-R critical reviews.

An internal referee-style audit is not independent peer review. The authors
and the computational agent share project context and may share blind spots.
The strongest permissible description is therefore **internal adversarial
source-readiness audit**. Independent external reproduction and journal peer
review remain separate future evidence.

## 1. Trigger, scope and non-interference rule

The audit is executed after the immutable P4-R result and its gate-specific
critical review are committed and pushed. It is executed regardless of
whether P4-R passes, fails, returns the scalar null or is inconclusive, because
negative results also require source-quality traceability.

Its scientific scope is the canonical chain needed to understand the current
loop/center/mechanics claims:

1. rotating-wave finite-$H$ existence and its interval trust base;
2. Anchor and L3 local numerical stability;
3. D0 ambient-$SO(2)$ topology and the absence of internal $S^1$ evidence;
4. P2/P2-R Loop--Center response and recovery;
5. P3 finite-ensemble formation/attraction;
6. P4 source/write architecture, exact age ledger and formal fail;
7. P4-R-phi local metrology and discrete phase response.

Unrelated historical kernel, dimensionality and long-run studies are audited
only where a current paper claim depends on them. The audit may identify
future tests or documentation repairs, but it may not:

- change a protocol, result JSON or historical decision;
- remove an arm, recompute a threshold after seeing a result or retune a
  parameter;
- promote P4 from `p4-source-write-architecture-fail`;
- reinterpret a failed gate as passed because a later reconciliation passed;
- authorize P4-R-S unless the independent conditions in Section 8 are met.

## 2. Frozen pre-target base

The charter is written from the clean branch revision

```text
cb863d4a88c1072637116a0296ab9fc20356a675
```

with:

| item | frozen identifier |
| --- | --- |
| P4-R design commit | `0bf9b3020f26acfaf5273c1efab5dcc52d596239` |
| P4-R protocol commit | `cb863d4a88c1072637116a0296ab9fc20356a675` |
| P4-R protocol blob | `b81fa535c1921c2f11f83e5585bf38b05e0a08d5` |
| P4 result JSON blob | `41ddfb5ec2d4c907607995523775072ad12544f7` |
| P4 JSON canonical-LF SHA-256 | `ea0651e206451e5f87ec08ab3f66ec68df2c04bee2d1b9d67219736058a275cc` |
| historical P4 decision | `p4-source-write-architecture-fail` |

At this freeze there is no P4-R runner and no P4-R result artifact. The later
audit must add, without changing this charter, the immutable P4-R result,
gate-review, execution, environment and implementation identifiers.

Three source-readiness gaps are already visible and therefore cannot be
treated as post-result discoveries:

1. no `CITATION.cff` or equivalent repository citation metadata is present;
2. runtime requirements are pinned, but no complete cross-platform lock or
   wheel/hash manifest is present; the historical P4 result records NumPy
   2.4.6 while `requirements.txt` currently pins NumPy 2.3.5;
3. all reported Krawczyk panels use `mpmath.iv` 1.3.0; there is no second
   outward-rounded interval backend or formal proof-assistant verification.

These facts do not invalidate the existing scoped claims by themselves. They
do preclude an unconditional source-ready verdict until they are either
repaired or converted into explicit claim and reproducibility restrictions.

## 3. Required review passes

The audit consists of seven distinct passes. Distinct passes are a procedural
separation, not a claim that different human reviewers performed them.

### A. Claim traceability

Construct a complete claim ledger with one row per current promoted statement:

| required field | content |
| --- | --- |
| `claim_id` | stable identifier |
| `exact_wording` | wording allowed in README/docs/paper |
| `evidence_class` | theorem, conditional certificate, numerical evidence, inference, hypothesis or negative result |
| `protocol` | immutable commit URL and blob |
| `raw_result` | immutable commit URL, Git blob and canonical SHA-256 |
| `critical_review` | immutable review URL |
| `code` | execution and implementation commits/blobs |
| `scope` | candidate, parameter panel, horizon and controls |
| `excluded_claims` | nearby statements not supported |
| `status_consistency` | README, status, priorities and paper register agree |

Every claim without a complete row is major at minimum. A promoted claim that
contradicts its stored decision is critical.

### B. Algebra and model semantics

Re-derive independently from the ground equations:

1. $B_H(z)$ and the normalized finite-memory weights;
2. the chirality-conditioned notch coefficients $a_{s,j}$;
3. coefficient sum, target notch and conjugacy;
4. complex-to-real adjoint slot forces;
5. midpoint discrete-gradient force and matched first-order mobilities;
6. write, finite-history age, actuator and interaction-energy ledgers;
7. local forced-increment identities and the P4-R full-dot envelope.

The pass must try the rejected rivals: raw $c_H$, omitted age work, wrong
chirality, a direct $x$-work reading and an inserted second-order/mass term.
It must state which failures are algebraic, numerical or ontological. No
symbol such as “mass”, “momentum”, “spin” or “center of mass” may be inferred
from notation alone.

### C. Numerical trust base

Audit conditioning and arithmetic rather than reporting only small residuals:

- recompute every decisive scale and threshold margin;
- inspect binary64 cancellation, summation order, BLAS dependence,
  subnormal handling and the 80-digit exact-ratio checkpoints;
- verify that a deliberately corrupted local identity or ledger is rejected;
- rerun the registered Krawczyk examples and known-root regression controls;
- inspect the Krawczyk operator, analytic Jacobian and interval endpoints;
- classify all existence statements as conditional on `mpmath.iv` unless
  a second validated outward-rounded backend reproduces the inclusions.

A second interval backend is required for an unrestricted “source-ready”
verdict on promoted local-existence claims. Without it, only the restricted
verdict is available, and “formally verified” or “independently certified”
remains prohibited.

### D. Design, dependence and falsification

For every gate, distinguish discovery, preregistration, holdout, symmetry
control and post hoc inference. Explicitly audit:

- P2 versus outcome-informed P2-R;
- P4 formal failure versus its passed exact ledger;
- P4 discovery arms versus P4-R holdout arms;
- eight quadrature nodes versus four mirror-distinct phase pairs;
- sign/chirality/half-turn controls versus independent replications;
- null, chiral, directional-fail and inconclusive regions;
- alternative explanations including start-phase conditioning, finite-$H$
  artifacts, numerical floors, prepared-orbit dependence and port fiat.

The audit must search for observations that would falsify the preferred
interpretation. It may not use a confirmatory parameter search as a
substitute.

### E. Clean-checkout reproduction

Use a new checkout at the immutable result/review revision, not the working
tree used to develop the gate. Record OS, architecture, Python, NumPy, SciPy,
mpmath, BLAS identity/thread count and the full installed-package manifest.

Two environments are required where obtainable:

1. the exact environment recorded by the original P4/P4-R target execution;
2. the repository-declared pinned runtime environment.

Run the exact CI Ruff scope, full tests and strict documentation build. Then
reproduce the decisive deterministic artifacts to temporary output paths and
compare:

- decision and all gate booleans exactly;
- integer counts and arm identities exactly;
- canonical JSON structure exactly;
- every decisive floating metric against a predeclared replay tolerance;
- canonical-LF SHA-256 where bytewise reproduction is expected.

A package-version or BLAS difference that changes a scientific decision is
critical. A non-decisive last-bit difference must be quantified and retained,
not hidden by replacing the original artifact.

### F. Independent result recomputation

Write a separate, minimal audit program that parses raw JSON but imports none
of the target runner's reporting or decision functions. It must independently:

1. enumerate the registered arms and detect missing/duplicate entries;
2. recompute threshold contacts, maxima, counts and decision precedence;
3. rebuild phase odd/even traces and the final $A/B$ response table;
4. verify mirror and half-turn pairing without treating them as replication;
5. recompute the exact work-ledger summaries from stored raw terms where
   available;
6. compare every recomputed value with the stored Markdown summary.

The audit program, its tests, output JSON and hashes become review artifacts.
Agreement between two code paths is strong reproducibility evidence but not
mathematical independence if they share the same raw simulation.

### G. Repository and citation readiness

Audit the repository as a citable computational source:

- public immutable commit links for every cited file;
- release tag and artifact manifest with Git blobs and canonical SHA-256;
- `CITATION.cff` or equivalent citation instructions;
- code and data/documentation license coverage;
- exact environment lock or hashed installation manifest;
- one-command clean reproduction instructions with realistic run times;
- machine-readable raw results without broken large-file indirection;
- a changelog or decision ledger that preserves failed and superseded gates;
- no private paths, credentials, machine-specific assumptions or mutable
  branch URLs in a scientific citation.

A GitHub branch is convenient but mutable. Paper citations must resolve to a
commit or release; an archival DOI is recommended when the paper snapshot is
fixed.

## 4. Adversarial test matrix

The executed audit must include at least these attacks:

| attack | expected discriminating outcome |
| --- | --- |
| omit $W_{\rm age}$ | ledger fails by the registered rival diagnostic |
| replace $C_s$ by raw $c_H$ | target work ledger does not close |
| conjugate the wrong chirality | notch/shape controls fail |
| perturb one protocol blob | provenance becomes inconclusive |
| delete or duplicate one arm | registration becomes inconclusive |
| corrupt one local increment by $10^{-8}D_0$ | local metrology fails |
| corrupt one work term by $10^{-8}U_0$ | exact ledger fails |
| reverse one stored response sign | mirror/half-turn or classifier changes |
| treat 32 arms as replications | review flags pseudoreplication |
| recompute with declared and execution NumPy versions | decision must remain invariant or source readiness fails |
| reorder full-dot accumulation | local decision stays invariant; rounding diagnostics remain inside envelope |
| remove conditional Krawczyk wording | claim audit returns major or critical |

Each attack needs an automated test or a documented reason why automation is
impossible. Merely asserting the expected outcome is insufficient.

## 5. Finding schema and severity

All findings are stored both in Markdown and in one machine-readable JSON
array. Each finding has:

```text
finding_id
severity
domain
claim_id
summary
evidence_paths
reproduction_command
observed
expected
scientific_impact
required_remediation
status
```

Severity is frozen as:

- **critical:** decision mismatch, irreproducible decisive artifact, broken
  provenance, algebraic ledger contradiction, missing raw evidence or a
  promoted claim contradicting its gate;
- **major:** material claim overreach, unresolved numerical trust issue,
  pseudoreplication, nonportable environment or missing audit path that can
  be repaired without changing the historical decision;
- **minor:** clarity, navigation, citation ergonomics or non-decisive
  presentation defect;
- **note:** scoped limitation already disclosed and correctly propagated.

Only evidence-backed findings are counted. Absence of a finding is not proof
that no defect exists.

## 6. Required audit artifacts

The later execution must create and push, before any P4-R-S protocol:

```text
reports/project/meta/reviews/p4_publication_source_referee_audit_<date>.md
reports/project/meta/reviews/p4_publication_source_referee_findings_<date>.json
reports/project/meta/reviews/p4_publication_source_claim_trace_<date>.json
reports/project/meta/reviews/p4_publication_source_reproduction_<date>.json
```

Any independent replay program and tests must live in explicit audit paths
and be pinned by blob. Temporary build products are not evidence. The review
must link immutable GitHub commit URLs rather than local paths or branch-head
URLs.

## 7. Frozen verdicts

The audit must return exactly one verdict:

- **`referee-source-ready`:** no open critical or major finding; decisive
  artifacts reproduce from a clean checkout; independent summaries agree;
  citation/environment metadata are complete; and any promoted Krawczyk
  existence claim has a compatible second validated interval backend.
- **`referee-source-ready-with-major-claim-restrictions`:** no open critical
  finding and every decision reproduces, but one or more declared limitations
  prevent an unrestricted source claim. Typical examples are the single
  `mpmath.iv` trust base, finite deterministic panels or missing continuous
  phase control. Every restriction must appear in README, status, claim
  register and paper wording.
- **`referee-not-source-ready`:** any critical finding, nonreproduced
  decision, unresolved algebraic contradiction, missing decisive raw data,
  broken provenance or uncorrected claim/result conflict.

Minor findings may remain open only with owners and a statement that they do
not affect scientific decisions. “No concerns” without the required artifacts
is not a verdict.

## 8. Relation to P4-R-S, paper claims and external review

The referee audit never changes the P4-R decision. The prospective P4-R-S
anchor-scale protocol can be written only if all of the following hold:

1. P4-R-phi returns
   `p4r-phase-averaged-chiral-response-pass`;
2. its gate-specific critical review upholds that decision;
3. this source audit returns `referee-source-ready` or the restricted
   verdict with no restriction that undermines the P4/P4-R port, ledger or
   response claim;
4. all claim-language changes required by the audit are committed and pushed.

A scalar, directional-fail, ledger/metrology-fail or inconclusive P4-R outcome
keeps P4-R-S closed even if the repository is otherwise source-ready. A
`referee-not-source-ready` verdict also keeps P4-R-S closed until a new,
versioned audit resolves the critical findings without altering historical
artifacts.

Paper-level promotion requires immutable commit/release citations and the
exact claim ledger. External peer review or independent reproduction may
later strengthen confidence, but it must be described as new evidence; this
internal charter cannot confer independence on itself.
