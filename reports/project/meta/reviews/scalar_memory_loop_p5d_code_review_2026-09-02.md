# P5-D code review after the closed recovery

Date: 2026-09-02

Reviewed revision: `4f229d4c6fcf58e7d97f399c82f799040e994d9e`

Verdict: **`p5d-runner-not-ready-no-target-authorized`**

## 1. Scope and method

This is a target-free adversarial review of the P5-D model path, runner,
serializer, output transaction, provenance guard and independent auditor. No
registered arm was executed. Static algebra was checked against the source;
small local probes exercised only guards and report/output helpers.

The review separates three layers:

- **evidence:** source expressions, existing tests and reproduced helper
  behavior;
- **inference:** consequences that follow deterministically from those
  expressions;
- **hypothesis:** physical interpretations not established by the code.

## 2. Algebraic review

The finite-memory weights, native FIFO update, notched-center coefficients,
center-conjugate write port, reciprocal implicit-midpoint force and work
ledger are mutually consistent at the level reviewed. In particular,
$C^+-C^\star=\alpha|c_0|^2F$ and the registered write dissipation
$\alpha|\overline{c_0}F|^2$ are non-negative. The one-way and reciprocal force
signs agree with the declared separation $d=C_A-C_B$ and potential
$U=\kappa|d|^2/2$.

This is not a derivation of interaction or mass. The force law and its
potential are inserted. Eliminating the visible FIFO slot yields a second
difference driven by the difference of two history-dependent gradients, not
a demonstrated Newton law with constant positive mass.

## 3. Blocking findings

| ID | Severity | Reproduced finding | Consequence |
| --- | --- | --- | --- |
| P5-R01 | critical | `_verify_provenance()` accepted clean upstream HEAD `4f229d4` although the documented recovery is closed. | The runner does not technically enforce the governance state and could start another target panel. |
| P5-R02 | critical | Every channel-off arm initializes `minimum_dissipation=math.inf` and serializes it unchanged; at least 64 non-finite values are therefore guaranteed. Existing full-panel fixtures are classifier-shaped, not exact `_run_arm` payloads. | The production schema was never exercised end-to-end before either target call. |
| P5-R03 | critical | `_all_finite(np.float32(np.nan))` and the independent auditor's `_finite(...)` both returned `True`; arbitrary unsupported objects also returned `True`. | Registration and audit are fail-open for unknown scalar types and can accept non-finite data. |
| P5-R04 | high | Injecting failure into the second final rename left the final JSON present and the final Markdown absent. | `_write_complete_outputs()` is two sequential atomic renames, not an atomic two-file publication. |
| P5-R05 | high | `_render_report({"response": {"available": false}, ...})` raised `KeyError: 'diagnostics'`. | Once non-finite registration makes response unavailable, report creation has a deterministic next failure. |
| P5-R06 | high | The readiness parser trusts mutable Markdown and extracts a CI run identifier without verifying its conclusion or binding that run to the reviewed commit. | Provenance can pass without proving that the cited CI validated the exact readiness state. |
| P5-R07 | medium | There is no recursive exact payload-schema validation with JSON path and expected type before target execution; strict JSON serialization is the first complete production-schema check. | Hours of target work can be lost to a locally detectable schema defect, as happened twice. |

## 4. Reproduction evidence

The following target-free observations were reproduced from the reviewed
source:

```text
guard_accepts_closed_branch=4f229d4c6fcf58e7d97f399c82f799040e994d9e
second_rename_failure: final_json=True, final_report=False
python_float_nan: gate=False, auditor=False
numpy_float32_nan: gate=True, auditor=True
unsupported_object: gate=True, auditor=True
unavailable_response_report: KeyError 'diagnostics'
```

The two target incidents remain infrastructure failures. They do not count as
negative interaction arms because neither produced the preregistered complete
payload and decision.

## 5. Required remediation gates

Before any new target authorization, a separate change must demonstrate all
of the following without running the registered panel:

1. a machine-readable closed/open governance state enforced by the runner;
2. an exact typed payload schema generated from production-shaped arm data;
3. fail-closed recursive finite/type validation in runner and auditor;
4. explicit semantics and recovery tests for partial two-file publication;
5. a report path that handles unavailable response by construction;
6. cryptographic binding of protocol, readiness review, implementation, CI
   conclusion and commit;
7. a full local serialize--deserialize--audit rehearsal before target access.

## 6. Scientific claim boundary

**Evidence:** the implemented algebra is a coherent controlled port for two
prepared rotating-memory cells.

**Inference:** after runner remediation it may support a discriminating test
of reciprocal versus one-way center response.

**Hypothesis:** interaction, charge, spin, momentum, inertia and mass emerge
from the underlying memory law. None of these hypotheses is established by
P5-D.

## 7. Decision

P5-D remains closed and `p5d-inconclusive`. No third target call, sentinel
substitution or implementation patch is authorized by this review. The next
work item is a separately reviewed remediation specification and test suite,
followed only then by a new explicit prospective authorization decision.
