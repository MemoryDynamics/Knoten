# Portability reconciliation of the rotating-wave foundation audit

Date: 2026-08-21.

Status: frozen second pipeline-reconciliation protocol. It is committed before
the corrections below are implemented or the audit is rerun. The L5 cell and
the \(A_{\rm att}=7\) holdout remain sealed.

## 1. Observed failures

The numerical foundation audit passed locally from revision
`8e1cf13083d343cdebb0d7d315d34a017164c827`, and its reviewed repository
integration candidate was committed as
`68e926e93452242b9444d0fdbaacad51b8947dd9`. GitHub Actions nevertheless
exposed two provenance-pipeline defects before main-line integration.

First, `actions/checkout` used its default one-commit shallow clone. Two
existing provenance tests intentionally require older recorded commits to be
present. In CI those valid revisions therefore appeared as
`unknown-code-revision`; a complete local clone passed the same tests.

Second, six of the nine frozen SHA-256 values were calculated over a Windows
working-tree representation with CRLF line endings. Git stores the same text
artifacts canonically as LF blobs. A clean Linux checkout therefore observed
different bytes even though no versioned artifact content had changed. Direct
comparison with the exact `HEAD:path` Git blobs gives:

| source | frozen worktree SHA-256 | canonical Git-blob SHA-256 |
| --- | --- | --- |
| discovery JSON | `ab47cb3168561e4d9d9535981bda598bfa9815c3c593f65b6fd28d1874c561cb` | `f9c6409fccd9b3e02c83497428a24ad2d5dfb78d2134bfe4314baaec9e13e830` |
| initial-state JSON | `4ab3f657cfa68bcd38d73c0722cd718a94e413b33fc46c17bb995b3637808dd2` | unchanged |
| P0 manifest JSON | `3d89d2fe390c24765b23a834ad682b626f5ce3025b44f508afb1509b7fd6efb1` | unchanged |
| P0 audit JSON | `5ddde8005dd261bbd2aa8bd72906a7395f53d8bb666fb1ce5e9bb5686cdcde4c` | `1ab03eddb4d19d41c14abb3d5e289a6b607e558ebc6d66bc2624c99c70d4329e` |
| D0 contract Markdown | `4ad70cd38efb87e97509fe253987a6ac0a6dce9555cc37457eaba54a5f822bb2` | unchanged |
| stability JSON | `8b168d702d335dc5833f63c44cd2aa9b7c762a7ad6ac3ce36b87553a62114930` | `43b0d7f5e5ba81dc35d4a2e9d138d3663a3d98b67bcb09ed2d4572d5a01eb86f` |
| interval-certificate JSON | `77558d09f5114a549384916fc15c2dc6113b1c6eb4a2f77f6a3646d6ff2df20c` | `63dc4158c0d8a9543230b656b7602feef76a48a2a75fbe6a6e001cb81082a840` |
| refinement-ladder JSON | `9e76e34911261b263278004281822e2b4d36025181e1b9b9daf899aa28770301` | `1ba774daf0bf3395c1d0a356a31c8f5aab17eca76de7b32029f49b456cefb279` |
| continuum-reconciliation JSON | `8457536836b3fe1f4dc6d83fc74f57b39447978bd62574e5eedbb40294f4cd10` | `8008f3846678e8920c1193468e1cacd078ff2c45b2903fbc4ac130431bd68658` |

The byte-domain ambiguity invalidates the portability of Gate A, not any
finite sum, interval inclusion, continuum integral, stability diagnostic or
scaling result. The earlier local pass remains visible in Git history and
must not be represented as a cross-platform pass.

## 2. Authorized corrections

Exactly the following corrections are authorized:

1. Set `actions/checkout` to `fetch-depth: 0`, so historical-revision gates
   evaluate the repository history they claim to audit.
2. Define the immutable hash domain as the exact versioned Git blob
   `HEAD:path`, update the six platform-dependent expected values to the
   canonical hashes above, and report that domain in every audit row. The
   nine source artifacts themselves must not change.
3. Add regression assertions for the hash domain and keep the existing
   historical-revision tests active in CI.
4. Point the executable to this protocol, distinguish the new decision as
   `foundation-audit-portability-reconciliation-pass-scoped`, and rerun every
   original A--E gate from a clean committed revision.

Hashing the Git blob is not a relaxation: it makes the immutable object the
one actually committed and distributed by the repository. The audit's clean-
worktree precondition continues to reject uncommitted semantic changes.

No input artifact, candidate value, model parameter, sign convention,
quadrature method, precision, Newton count, partition, residual threshold,
gain threshold, branch corridor, certificate condition, stability condition,
continuum target or scaling threshold may change.

## 3. Decision rule

The rerun passes only if all five original composite gates pass and the nine
canonical Git-blob hashes plus all recorded ancestor revisions validate in a
full-history clone. A gate failure gives
`foundation-audit-portability-reconciliation-fail`; an exception gives
`foundation-audit-portability-reconciliation-inconclusive`.

Even a pass remains scoped to five locally existence-certified prepared
finite-memory loops, one locally numerically stable prepared anchor, and a
numerically reconciled fixed-gain continuum branch. It does not authorize a
stable family, spontaneous formation, internal \(S^1\), work, inertia or mass.
