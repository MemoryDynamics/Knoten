# P5-D amended runner-remediation protocol sufficiency review

Date: 2026-09-03.

Reviewed revision: `ed21f5c33591f311cf14617f0d23fc51cddc2ff7`

Reviewed protocol blob: `1f94be94bdf4b2512f68b69dcc5b3958e7efe7b6`

Amendment CI: [GitHub Actions run 33713983036](https://github.com/MemoryDynamics/Knoten/actions/runs/33713983036), successful for the reviewed revision.

Verdict: **`p5d-remediation-protocol-sufficient-target-closed`**.

## 1. Scope

This target-free review asks only whether the amended protocol resolves
P5-PR01--P5-PR07 sufficiently to start adversarial tests and infrastructure
implementation.  It does not review such an implementation, authorize a
target call or evaluate any registered arm.

## 2. Amendment closure

| Finding | Closure in amended protocol |
| --- | --- |
| P5-PR01 | fixed attempt-3 receipt and publication-manifest paths plus canonical lowercase UUIDv4 grammar |
| P5-PR02 | fixed tracked v2 schema path, content digest, exact keys/types/lengths and `additional_properties=false` |
| P5-PR03 | fixed `gh api` repository route constructed only from a positive integer; exact id, repository, status, conclusion and head checks |
| P5-PR04 | manifest validation and receipt/path/hash agreement precede production payload interpretation in the independent auditor |
| P5-PR05 | exactly seven minimum protected paths are frozen |
| P5-PR06 | both historical incident-report blobs are required in closed governance |
| P5-PR07 | cleanup is limited to the six files absent on entry and created by the current call; the attempt receipt is durable |

All seven specification findings are therefore closed at the reviewed blob.

## 3. Internal consistency

The trust chain is non-circular.  Implementation CI validates a closed
governance state and the six other protected blobs.  A later authorization-
only commit may alter exactly the governance file, names that CI result and
repeats the protected identities.  The runner verifies the local diff and
remote GitHub metadata before consuming the fixed receipt.

The publication contract also distinguishes three states unambiguously:

- receipt absent: target not entered;
- receipt present and valid manifest absent: consumed but inconclusive
  attempt;
- receipt and hash-valid manifest present: published result available for
  audit.

## 4. Representation and notation

`minimum_mobility_dissipation=null` is restricted to channel-off records and
means that no mobility ledger was evaluated.  Active records retain the
unchanged finite threshold.  Canonical metadata names $b_s$,
$\gamma_{\rm w}$, $\mu_{\rm w}$ and $u_{64}$ without retroactively changing
historical v1 artifacts or internal aliases.

## 5. Residual risks

The protocol cannot itself prove that two independent validators agree, that
cleanup works under injected failures or that GitHub metadata is checked
before target entry.  Those are deliberately falsifiable implementation
requirements.  Host termination can leave partial files, but the durable
receipt and absent manifest classify that case without permitting an
automatic retry.  Filesystem or GitHub compromise remains outside this local
trust model.

## 6. Scientific boundary

**Evidence:** the amended protocol closes all findings from its first review
and passed repository CI.

**Inference:** adversarial tests and minimal infrastructure corrections may
now be written against a determinate contract.

**Hypothesis:** interaction, spin, momentum, inertia or mass.  None is tested
or supported here.

## 7. Decision

The test-and-implementation phase of the runner remediation is open.  It must
start with the closed governance record, machine-readable schema and failing
tests, then make the smallest corrections needed.  P5-D target access remains
closed regardless of implementation outcome; only a later independent
readiness review may assess runner readiness, and even a ready verdict cannot
authorize attempt 3.
