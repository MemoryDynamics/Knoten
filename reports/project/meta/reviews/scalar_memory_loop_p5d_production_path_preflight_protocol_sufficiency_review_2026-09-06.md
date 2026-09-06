# P5-D production-path preflight protocol sufficiency review

Date: 2026-09-06.

Reviewed amended protocol revision:
`70a5d451c4678a7542fdad20896b5963b6d76633`.

Reviewed amended protocol blob:
`acd4d4a4ad1ea9e0baa2594669b1c85c15eff834`.

Reviewed CI:
[GitHub Actions run 34059264028](https://github.com/MemoryDynamics/Knoten/actions/runs/34059264028),
successful for the exact amended-protocol revision.

Verdict:
**`p5d-production-preflight-protocol-sufficient-target-closed`**.

This is a target-free protocol sufficiency review. It authorizes only the
construction of initially failing, target-trapped preflight tests followed by
the smallest claim-scoped infrastructure correction allowed by the amended
protocol. It supplies no P5-D result, does not reopen the consumed attempt-3
lease and does not authorize attempt 4.

## 1. Scope and evidence boundary

The review compares the amended protocol with the six findings in the
separately committed negative review at revision
`ed8313bec76de0c5c68ea8dae32fa8e469dc58ba`, blob
`501aeffbc60b39c7a95c90c66066217ec2807b0b`. It also checks consistency with
the attempt-3 incident, immutable receipt, current runner, independent
auditor, v2 schema and the three protected scientific source blobs named by
the protocol.

No attempt-3 in-memory decision was inspected, reconstructed or inferred.
No registered trajectory, target initialization, FIFO step or mutual-centre
step was evaluated for this review.

## 2. Closure of the blocking findings

### P5-PF01 -- closed at protocol level

The amendment registers 41 exact scientific top-level symbols from the P5
runner and the standard-library AST/SHA-256 procedure that fingerprints them.
The registered digest is
`8145b57410a87ab8dae4e5112a81db8b538f3ddf5fc66261cd6c453f654b47ac`.
The procedure fails on missing, duplicated, unknown or syntax-changed
registered nodes while ignoring comments and source coordinates.

The protected set includes candidate and threshold assignments, panel
registration, reducers, decision/classification logic, `_run_arm` and
`_run_registered_panel`. Together with the three frozen `src` blobs, this is
a machine-verifiable barrier against changing the equations, panel,
estimands, thresholds or decision rule during the infrastructure repair.

### P5-PF02 -- closed at protocol level

The amendment fixes the sole permitted producer boundary at the existing
`_strip_internal` return path while freezing `_run_arm` and
`_run_registered_panel`. It requires off and active raw records to traverse
that actual boundary, checks every nested trace, ledger, gate and summary
leaf, and adds a source-level wiring assertion for both live returned lists.
A constructor-bypass mutation is explicitly required to fail.

This is stronger than a hand-written publishable-dictionary rehearsal: the
future tests must demonstrate that the unchanged production panel is wired to
the tested record boundary, although target functions remain trapped.

### P5-PF03 -- closed at protocol level

The primitive contract now specifies exact built-in type identity before any
finiteness check: `type(value) is float`, `type(value) is int` or
`type(value) is bool` according to the schema branch. Boolean is explicitly
excluded from integer and numeric branches. `math.isfinite` is applied only
after native-float identity is established.

The original record must validate before encoding; strict encoding forbids a
NumPy-coercing `default=` callback; and the decoded JSON record must validate
again. The adversarial matrix and mutation falsifiers cover the relevant
bypass paths.

### P5-PF04 -- closed at protocol level

The amendment requires `struct.pack(">d", ...)` equality across every
deliberate NumPy-floating to native-float boundary, plus `math.copysign` for
signed zero. It states the correct reference for float32 widening: the exact
binary64 value of the already rounded float32 source. Normal, subnormal and
signed-zero cases are included in the mandatory adversarial matrix.

These witnesses test representation preservation rather than merely ordinary
numeric equality.

### P5-PF05 -- closed at protocol level

Future closed readiness and governance records must bind the amended protocol,
negative review, attempt-3 incident and receipt, scientific symbol set and
digest, runner, auditor, v2 schema and every new preflight test. A later
authorization-only commit must preserve those bindings and define both a
fresh attempt-4 UUID and exclusive receipt path through a separate governance
amendment.

The requirement is prospective and does not itself create or authorize an
attempt-4 lease.

### P5-PF06 -- closed as a library-governance condition

The amendment treats three consumers as a review trigger, not proof. Any
shared result-contract proposal must name the candidate pipelines and compare
accepted types, non-finite handling, `null`, overwrite policy, schema
strictness, auditor independence and backward compatibility in one evidence
table. Failure to establish three identical semantic rows leaves P5 local and
does not block the narrow repair.

Therefore the current standard-library-first, P5-local boundary is justified;
no shared project library or new dependency is authorized by this review.

## 3. Mainline consistency

The amended protocol retains the Paper-I transition law

$$
x_{n+1}=x_n+\varepsilon\xi_n-\eta\nabla\Phi_n(x_n),
\qquad \Phi_n=K\ast\rho_n,
$$

$$
\rho_{n+1}=(1-\lambda_{\rm m})\rho_n
+\beta_\rho G_\sigma(\mathord\cdot-x_{n+1}),
$$

and identifies the normalized finite-$H$ specialization
$\lambda_{\rm m}=\beta_\rho=\alpha$, $q=1-\alpha$. The exact isolated P5
port remains first order. No mass, inertia, oscillator or second-order term is
introduced by the remediation protocol.

This is a necessary restraint: a successful serialization repair can make a
registered interaction result observable, but cannot provide complex-pole,
oscillator or inertial evidence.

## 4. Residual limitations and falsifiers

- The AST digest is a syntax-level invariant, not a proof of mathematical
  equivalence under changes elsewhere in the import environment. The frozen
  scientific source blobs and later exact provenance bindings are therefore
  still required.
- Because `_run_arm` and `_run_registered_panel` are frozen, validation of
  real publishable arms occurs after the full panel and before payload
  construction. This protects the scientific freeze at the cost of not
  providing the earliest possible runtime failure.
- Synthetic 64+768 records establish representation, wiring, publication and
  audit behavior only. They cannot confirm the P5-D interaction claim.
- A green implementation suite would establish readiness only for a later
  authorization decision. It cannot retroactively recover attempt 3 or make
  attempt 4 permissible.

Any test that reaches a registered target, any changed scientific AST digest,
any constructor bypass, any unsupported scalar accepted before encoding, or
any missing provenance binding invalidates this verdict.

## 5. Authorized next boundary

The next repository change may add target-free tests that initially fail for
the known producer defect and the registered mutations. Only after those
tests exist may the smallest P5-local producer correction be implemented.
The complete suite, Ruff, strict documentation, exact implementation blobs
and a separate readiness review remain mandatory.

P5-D therefore remains **`p5d-inconclusive`** and target-closed.
