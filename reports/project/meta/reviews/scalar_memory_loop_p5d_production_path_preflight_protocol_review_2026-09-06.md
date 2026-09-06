# P5-D production-path preflight protocol review

Date: 2026-09-06.

Reviewed protocol revision:
`79e24f3fd3916f1b29bdf86620962cb998a37cda`.

Reviewed protocol blob:
`e0f373ff378d4b3b6d4933add30647d598fb8c49`.

Reviewed CI:
[GitHub Actions run 34058713729](https://github.com/MemoryDynamics/Knoten/actions/runs/34058713729),
successful for the exact protocol revision.

Verdict: **`p5d-production-preflight-protocol-needs-amendment`**.

This is a target-free protocol review. It supplies no P5-D result and does
not authorize preflight implementation or attempt 4.

## 1. Evidence reviewed

The review checked the new protocol against the attempt-3 incident blob
`7d0c74b2d9f8cd9f97534b1db47fccc73630c072`, receipt blob
`0f7b0b87ce1bad34a1f93369967fe1fadbcf6394`, the v2 schema, the current runner
and auditor, the canonical vocabulary and the implemented-equations page.

A repository inventory found 31 current experiment modules with local JSON
conversion helpers, six modules with local atomic-output helpers and only the
runner/auditor pair with exact v2 schema validation. This supports the
protocol's decision not to create a universal result library yet. It does not
by itself prove that any three helpers have identical semantics.

## 2. Positive findings

- The Paper-I transition law, finite-$H$ specialization and exact first-order
  port nullmodel remain explicit.
- Scientific quantities use the canonical distinction between $\alpha$,
  $\varepsilon$, $\eta$, $H$, $M_0$, $\kappa_{\rm pair}$,
  $\gamma_{\rm w}$ and $\mu_{\rm w}$.
- The protocol correctly separates NumPy numerical work from native JSON
  records and forbids serializer-side silent coercion.
- Standard-library-first implementation and the refusal to add a schema
  dependency are proportionate to the defect.
- Existing checkpoint and diagnostics helpers are evaluated by semantics
  instead of being reused merely because their names appear similar.
- The proposed target traps, mutation tests, complete synthetic panel and
  manifest-last audit rehearsal address the observed class of coverage gap.
- No target, result path, equation, threshold or decision is opened.

## 3. Blocking findings

### P5-PF01 -- scientific freeze is not machine-verifiable

The protocol pins three `src` blobs, but the modifiable P5 runner itself
contains candidate constants, panel construction, thresholds, reducers and
classification next to representation code. Prose says these objects remain
frozen, yet no exact symbol set or digest would detect a scientific edit in a
future infrastructure patch.

The amendment must require a standard-library `ast`/`hashlib` fingerprint of
the exact scientific top-level assignments and functions in the frozen runner
blob. The protected symbol list and expected digest must be registered before
implementation. Unknown, missing, duplicated or changed symbols must fail.
Comments and formatting may be normalized; literals, operators, call targets
and control flow may not.

### P5-PF02 -- constructor tests do not prove production wiring

Passing pure record constructors can coexist with the live runner continuing
to assemble a nested dictionary directly. This was the structural weakness of
the earlier hand-written full-panel rehearsal.

The amendment must require a wiring test that proves every off/active arm,
trace, ledger, gate and summary record in the live panel path is returned by
the registered constructors. A mutation that bypasses any constructor must
fail. Numerical target functions remain trapped; synthetic intermediates may
exercise only the wiring and record boundary.

### P5-PF03 -- primitive validation order is underspecified

`math.isfinite(numpy.float64(...))` succeeds, so finiteness alone does not
enforce the native boundary. Python also treats Boolean as a subclass of
integer.

Every primitive validator must first use exact built-in type identity
(`type(value) is float`, `int` or `bool` as registered), reject Boolean in
integer/number branches, and only then apply `math.isfinite` to a native
float. The original payload must pass this rule before `json.dumps` is
called.

### P5-PF04 -- exact floating-value preservation lacks a metric

The protocol requires unchanged numerical values and includes signed zero in
the adversarial matrix. Ordinary equality cannot distinguish `0.0` from
`-0.0`, while decimal comparison does not prove binary64 identity.

The amendment must require standard-library `struct.pack` equality for each
finite binary64 value crossing from a NumPy scalar to a native float, plus an
explicit `math.copysign` assertion for signed zero. Intentional float32 to
binary64 widening must equal the exact value represented by the source
float32, not an unavailable pre-rounding real number.

### P5-PF05 -- future provenance bindings are incomplete

The sequence mentions a readiness review but does not state what a future
implementation or authorization must pin. After three incidents, prose-only
lineage is insufficient.

The amendment must require future closed governance and readiness records to
bind at least the amended protocol blob, this review blob, the attempt-3
incident and receipt blobs, the scientific AST fingerprint, P5 runner,
auditor, schema and all new preflight tests. A later authorization-only commit
must preserve those bindings and use a fresh attempt-4 UUID and exclusive
receipt path. This requirement does not itself authorize that schema or
commit.

## 4. Major non-blocking clarification

### P5-PF06 -- shared-library promotion needs an evidence record

Three consumers are a conservative trigger, not proof of shared semantics.
Before any common `src` module is proposed, the three candidates must be named
and compared in a table covering accepted types, non-finite handling, `null`,
overwrite policy, schema strictness, auditor independence and backward
compatibility. Failure to find three identical rows means the claim-scoped
P5 implementation remains local; it must not block the narrow remediation.

## 5. Required amendment

The protocol becomes sufficient only if it closes P5-PF01--P5-PF05 and makes
P5-PF06 explicit. The appropriate sequence remains:

1. commit this negative review without editing the protocol;
2. amend the protocol in a later commit;
3. require green CI for the amended blob;
4. conduct a separate sufficiency review;
5. only a sufficient verdict may open target-free failing tests.

Until that sequence completes, P5-D remains `p5d-inconclusive`, the
attempt-3 lease remains consumed, implementation remains closed and no fourth
target invocation is authorized.
