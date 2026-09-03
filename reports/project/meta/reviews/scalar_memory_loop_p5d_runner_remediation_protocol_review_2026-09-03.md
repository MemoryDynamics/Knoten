# P5-D runner-remediation protocol review

Date: 2026-09-03.

Reviewed revision: `9e7ab0e1d3cd5d27bf7ad4e23e44238ac670b04c`

Reviewed protocol blob: `18f9fdbc48a9a587b00189597ffe5fa5f1c82ee6`

Freeze CI: [GitHub Actions run 33713342336](https://github.com/MemoryDynamics/Knoten/actions/runs/33713342336), successful for the reviewed revision.

Verdict: **`p5d-remediation-protocol-needs-amendment`**.

## 1. Scope and method

This is a target-free adversarial specification review.  It compares the new
protocol with findings P5-R01--P5-R07, the two incident records, current
runner/auditor control flow and the canonical notation contract.  No
registered arm was evaluated and no result path was created.

## 2. What is adequately fixed

The protocol correctly preserves the scientific estimand and rejects a third
target authorization.  Its `null` semantics for a channel-off mobility
minimum is dimensionally and logically preferable to a finite sentinel.  The
manifest commit point is an honest replacement for the impossible claim of
cross-directory two-file atomicity.  A durable pre-target attempt receipt
also closes the former retry loophole.  The canonical v2 names are consistent
with the active model vocabulary.

These are specification strengths, not implementation evidence.

## 3. Blocking under-specification

| ID | Severity | Finding | Required amendment |
| --- | --- | --- | --- |
| P5-PR01 | high | Attempt receipt and publication manifest are called registered but have no exact path or filename. | Freeze both paths and a path-safe authorization-ID grammar. |
| P5-PR02 | high | The result schema is described as exact but no tracked machine-readable schema artifact, schema digest or authoritative required-key set is named. | Freeze one schema path and require runner and independent auditor to validate against byte-identical content without importing one another. |
| P5-PR03 | high | The protocol lets an authorization supply an API URL. A mutable or foreign endpoint must not be part of the trust root. | Construct a fixed GitHub repository API endpoint from a decimal run ID and require `status=completed`, `conclusion=success` and exact `head_sha`. |
| P5-PR04 | high | The independent auditor is required for the rehearsal but is not explicitly required to reject absent, malformed or hash-mismatched publication manifests. | Make manifest verification the auditor's first production-file gate. |
| P5-PR05 | medium | Protected blobs are described by category, leaving the exact minimum path set open. | Freeze the minimum protected-path set before tests and implementation. |
| P5-PR06 | medium | Historical call count is required but its exact incident bindings are not. | Require both incident-report blobs in the closed governance record. |
| P5-PR07 | medium | Handled cleanup is required without defining ownership after an injected failure. | Limit cleanup to files absent on entry and created by the current call; pre-existing debris must remain untouched and block execution. |

## 4. Falsification coverage

The seven test groups map well to P5-R01--P5-R07, but P5-PR01--P5-PR04 show
that several tests could pass against a locally chosen contract rather than a
prospectively fixed one.  In particular, a mock URL accepted from governance
would make a green CI-binding test circular, while an auditor that reads only
the payload would not establish publication completeness.

## 5. Scientific boundary

**Evidence:** the freeze has green CI and its proposed representation changes
do not alter the reviewed center/write equations.

**Inference:** after the amendments, the protocol can discriminate complete
publication from an infrastructure failure and can technically consume one
future authorization.

**Hypothesis:** any mutual response, interaction, spin, momentum, inertia or
mass.  This review supplies no evidence for those claims.

## 6. Required next action

Amend only the protocol and documentation to resolve P5-PR01--P5-PR07.  Push
the amendment, require green CI and review its exact revision/blob.  Do not
create the governance file, schema, tests or production correction before a
protocol verdict of `p5d-remediation-protocol-sufficient-target-closed`.

## 7. Decision

The conceptual architecture is strong but not yet sufficiently determinate
for a prospective remediation.  The implementation phase remains closed and
the P5-D target remains closed.  This is a specification fail, not a model or
interaction result.
