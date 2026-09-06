# P5-D production-path preflight protocol

Date: 2026-09-06.

Status: **prospectively amended after protocol review, target-free,
implementation closed**.

The amendment closes P5-PF01--P5-PF06 from the separately committed review at
revision `ed8313bec76de0c5c68ea8dae32fa8e469dc58ba`, review blob
`501aeffbc60b39c7a95c90c66066217ec2807b0b`. Its CI run
[34058955186](https://github.com/MemoryDynamics/Knoten/actions/runs/34058955186)
succeeded before this amendment. No production code or target was touched.

This protocol responds to the attempt-3 incident. It authorizes no code
change and no fourth target invocation. Its first purpose is to define what a
target-free repair would have to prove while keeping P5-D on the repository's
main transition law and using standard infrastructure at the correct layer.

## 1. Fixed evidence and scientific freeze

The following facts are fixed before this protocol:

- attempts 1--3 are `p5d-inconclusive` infrastructure incidents;
- attempt 3 consumed authorization UUID
  `c948bdf3-01f6-43b0-aef9-d4d1a4373be1` and has an immutable receipt;
- attempt 3 completed the in-memory panel, response reduction and
  classification, but no decision was printed, observed or published;
- the first v2 validation rejected a finite `numpy.float64` in a Channel-off
  rival fraction;
- no JSON result, Markdown report, publication manifest or independent audit
  exists for attempt 3.

The protected scientific implementation remains unchanged:

| Path | frozen blob |
| --- | --- |
| `src/emergenz_knoten/mutual_center_coupling.py` | `86a064692b33514a536b93877d4d5dcf33894c64` |
| `src/emergenz_knoten/orbit_center_actuator.py` | `63d31bc47291f76c65a5633f14436ccd2105fe9a` |
| `src/emergenz_knoten/rotating_wave_stability.py` | `9defb5a6876371202e1ba57cea030c997b9c6edd` |

Because scientific and infrastructure code coexist in the P5 runner, the
freeze additionally registers a standard-library AST fingerprint. Parse the
frozen runner with `ast.parse`, select the following 41 top-level assignments,
class and functions in source order, serialize each node using
`ast.dump(annotate_fields=True, include_attributes=False)`, join them with one
line feed and hash the UTF-8 bytes with SHA-256:

```text
CANDIDATE_ID RADIUS_DECIMAL THETA_DECIMAL CANDIDATE
EXPECTED_WRITE_GAIN EXPECTED_MOBILITY PHASES DISTANCE_FRACTIONS
CHIRALITY_PAIRS KAPPAS KAPPA_VALUES SIGNS P5DThresholds THRESHOLDS
_pair _complex expected_base_keys expected_active_keys reflection_key
swap_half_turn_key swap_direction _base_key _active_key panel_registration
_all_finite _history_sha256 _trace_map _response_trace response_controls
_aggregate_response_gates _inside _trace_rms decision_from_gates
classify_panel _initial_pair _sample_loop _phase_metrics
_step_ledger_metrics _run_arm _high_precision_reference
_run_registered_panel
```

The registered digest is
`8145b57410a87ab8dae4e5112a81db8b538f3ddf5fc66261cd6c453f654b47ac`.
Missing, duplicated, unknown or changed registered symbols fail. The
attribute-free AST permits comments and formatting changes but preserves
literals, operators, call targets and control flow. In particular `_run_arm`
and `_run_registered_panel` may not change during this remediation.

Candidate, histories, equations, panel membership and ordering, coupling
strengths, thresholds, reducers and classification precedence are frozen.
This protocol may not be used to inspect, recover, approximate or infer the
lost attempt-3 decision.

## 2. Mainline equation and vocabulary boundary

The model begins with the Paper-I transition law

$$
x_{n+1}=x_n+\varepsilon\xi_n-\eta\nabla\Phi_n(x_n),
\qquad \Phi_n=K\ast\rho_n,
$$

$$
\rho_{n+1}=(1-\lambda_{\rm m})\rho_n
+\beta_\rho G_\sigma(\mathord\cdot-x_{n+1}).
$$

The finite-$H$ rotating-wave branch is an explicit state representation of
this law. Its normalized specialization uses
$\lambda_{\rm m}=\beta_\rho=\alpha$, $q=1-\alpha$ and an ordered FIFO state.
The P5 port adds the separately named $\kappa_{\rm pair}$ and derived
$\gamma_{\rm w}$ and $\mu_{\rm w}$; it does not rename $\alpha$,
$\varepsilon$, $\eta$, $H$, $M_0$ or the kernel quantities.

The exact isolated port nullmodel remains

$$
d^+=\frac{2d^\star-\kappa_{\rm pair}
(\mu_{{\rm w},A}+\mu_{{\rm w},B})d^-}
{2+\kappa_{\rm pair}(\mu_{{\rm w},A}+\mu_{{\rm w},B})}.
$$

No preflight or serialization correction may insert a second-order term,
oscillator, inertia or mass into this equation. Such claims require a later
complex-pole and scaling gate.

## 3. Library hierarchy

Implementation review must enforce the following order.

### 3.1 Python standard library first

Use `dataclasses` and `typing` for explicit record boundaries, `math.isfinite`
for scalar finiteness, `json` with `allow_nan=False` for encoding and strict
round trips, `hashlib` for content digests, and `pathlib`/`os.replace` for
same-filesystem temporary publication. Use `uuid`, `datetime` and
`subprocess` only where the existing governance contract already requires
them.

No new runtime dependency such as a generic schema or model-validation
package is justified for this narrow repair. A dependency proposal would
require a separate comparison showing a capability that the tracked v2
contract and standard library cannot provide.

### 3.2 NumPy is confined to the numerical layer

NumPy remains the standard numerical library for histories, vectorized
arithmetic and metrology. A numerical producer may deliberately construct a
native Python `float`, `int` or `bool` when it crosses into a result record.
After that boundary, NumPy scalars and zero-dimensional arrays are contract
violations.

Validation order is exact. A schema primitive first checks built-in type
identity: `type(value) is float`, `type(value) is int` or
`type(value) is bool` according to its registered branch. Boolean is never an
integer or number. Only a value already proven to be a native float reaches
`math.isfinite`.

Every deliberate NumPy-floating to Python-float conversion must preserve the
represented binary64 value. Tests compare `struct.pack(">d", source_as_f64)`
with `struct.pack(">d", converted)`. Signed zero additionally uses
`math.copysign`; float32 widening is compared with the exact binary64 value of
the already rounded float32 source.

The serializer may not silently coerce an unsupported object through a
`default=` callback. The original record must validate before encoding; the
decoded JSON record must validate again after a strict round trip.

### 3.3 Existing internal libraries are reused by semantics, not by name

`src/emergenz_knoten/checkpoints.py` is the reference pattern for versioned
metadata, no-pickle persistence, digests and a same-filesystem temporary
rename. It is not reused directly for P5 JSON reports because its `.npz`
array and overwrite semantics differ.

`src/emergenz_knoten/diagnostics.py::_finite_float` is not a suitable result
contract: it maps non-finite values to `None`, while P5 must distinguish
registered not-applicability from an invalid measured number. The many local
experiment `_jsonable` helpers are also not authoritative because most
silently coerce NumPy values without an exact schema.

The current P5 schema and its independently implemented auditor remain the
claim-scoped authority. Reuse must not collapse runner and auditor into the
same validation implementation.

### 3.4 Extension gate for a shared project library

The inventory at this freeze found 31 current modules defining a local JSON
conversion helper, six defining local atomic-output helpers and only the two
P5 modules implementing the exact v2 schema validator. This is evidence of
duplication, but not evidence that all semantics are interchangeable.

The first P5 correction must therefore remain claim-scoped. Promotion into a
new shared `src/emergenz_knoten` result-contract module is permitted only
after all of the following hold:

1. at least three current pipelines require the same primitive-type,
   non-finite and overwrite semantics;
2. their schemas distinguish `null` from invalid non-finite measurements in
   the same way;
3. mutation tests demonstrate that a common helper fails closed in every
   consumer;
4. one compatibility review shows that migration changes no stored artifact,
   equation, threshold or decision;
5. runner and independent auditor do not share the same claim-level validator.

Until then, extending the project library would freeze an unproven abstraction
and is forbidden.

The number three is a conservative review trigger, not proof of equivalence.
A promotion proposal must name the candidate pipelines and compare accepted
types, non-finite handling, `null`, overwrite policy, schema strictness,
auditor independence and backward compatibility in one evidence table. If
three identical rows cannot be established, P5 stays local and the narrow
remediation is not blocked.

## 4. Exact defect and permitted future correction

The attempt-3 defect is outcome-independent. In a Channel-off arm,
`coupling == 0` makes the energy floor `numpy.finfo(float).tiny` win. Division
of native zero rival maxima by that NumPy scalar produces six finite
`numpy.float64` zeros. The strict v2 validator correctly rejects them.

A future implementation protocol may permit only these infrastructure
changes:

- a pure claim-scoped publishable-record constructor at the existing
  `_strip_internal` boundary, with explicit native primitive outputs for the
  complete nested arm;
- an explicit native finite energy-scale constructor preserving the exact
  numerical value;
- native primitive construction for every registered metric, gate and count;
- validation of every publishable off/active arm returned by that boundary
  before complete-payload construction;
- validation of the original complete payload before `json.dumps`;
- strict encoding without a NumPy-coercing `default=` callback;
- the already required decoded-payload validation and manifest-last
  publication.

It may not change any arithmetic value, missing/not-applicable semantics,
scientific loop, stored field, schema key, arm order, threshold or decision.
If an explicit primitive conversion changes a binary64 value, signed zero or
Boolean meaning, implementation stops for a protocol amendment.

## 5. Target-free preflight matrix

Before any implementation can be called ready, all of the following must pass
without a registered trajectory:

1. **Incident reproducer:** a pure expression reproduces the exact
   `0.0 / numpy.finfo(float).tiny -> numpy.float64` type path and the existing
   validator rejects all six affected paths.
2. **Producer-boundary test:** the proposed pure record constructors receive
   representative Python and NumPy intermediates and emit only exact native
   JSON primitives with unchanged numerical values.
3. **Adversarial scalar matrix:** Python and NumPy Boolean, signed integers,
   float32/float64, zero-dimensional arrays, signed zero, smallest normal and
   subnormal values, NaN, positive/negative infinity and unsupported objects
   each have a registered accept/reject outcome.
4. **Exact arm-shape and wiring witnesses:** one Channel-off and one active
   raw record pass through the actual `_strip_internal` boundary used by the
   unchanged live `_run_registered_panel`; hand-written publishable
   dictionaries are forbidden. Every nested trace, ledger, gate and summary
   leaf is checked. A source-level AST assertion proves the frozen panel calls
   this boundary for both returned lists. The off mobility minimum is only
   `null`; every active minimum is finite.
5. **Complete panel rehearsal:** 64+768 records created through those same
   constructors traverse original validation, strict encoding, round-trip
   validation, report rendering, manifest-last publication and the independent
   auditor in temporary paths.
6. **Target traps:** initialization, native FIFO stepping,
   `mutual_center_step` and registered panel evaluation are trapped and remain
   at zero calls throughout every preflight test.
7. **Mutation falsifiers:** reintroducing the NumPy energy floor at the record
   boundary, bypassing `_strip_internal`, changing a scientific AST node, a
   NumPy Boolean gate, a non-finite active metric, a stale output or a
   serializer `default=` coercion makes the rehearsal fail.

Synthetic witnesses test representation and control flow only. They are not
P5-D data and may not be described as interaction evidence.

## 6. Early failure and publication boundary

A future authorized runner must execute a pure, target-free record canary
before creating its one-shot receipt. The canary passes a nested raw off and
active witness through the actual publishable-record boundary and complete
schema without calling initialization or dynamics.

The scientific AST freeze deliberately keeps `_run_arm` and
`_run_registered_panel` byte-semantically unchanged. Therefore real arm
records are validated at the existing `_strip_internal` return boundary,
after the registered panel has run but before payload construction. Moving
validation inside the scientific loops would require a separate scientific
protocol amendment. The pre-receipt canary, exact wiring proof and mutation
tests are the outcome-blind controls against another known producer defect;
they are not a guarantee against every runtime failure.

No per-arm scientific record, partial decision or opaque checkpoint may be
persisted before the registered publication manifest. A validation failure
after receipt creation consumes the authorization and remains inconclusive.
The independent auditor still reads the manifest first.

## 7. Required sequence

1. commit and push this protocol and require green CI;
2. conduct a separate target-free adversarial protocol review;
3. only a sufficient review may authorize failing preflight tests;
4. implement the smallest claim-scoped producer correction that passes them;
5. run affected tests, the complete suite, Ruff and strict documentation;
6. commit, push and require green implementation CI;
7. conduct a separate readiness review over exact blobs and mutation results.

Future closed governance and readiness records must bind the amended protocol
blob, this negative-review blob, attempt-3 incident and receipt blobs, the
scientific AST symbol set and digest, runner, independent auditor, v2 schema
and every new preflight test. Any later authorization-only commit must
preserve those bindings and would require a fresh attempt-4 UUID plus an
exclusive attempt-4 receipt path defined by a separate governance amendment.
This paragraph does not authorize either artifact.

Even a positive readiness review leaves P5-D closed. Attempt 4 would require
a later governance-only authorization commit and a new explicit user decision.

## 8. Stop conditions and verdict boundary

The work stops with no target authorization if any of the following occurs:

- a scientific blob, frozen estimand, registered AST symbol or digest changes;
- the preflight cannot catch the attempt-3 producer path without target data;
- the live publishable panel can bypass its registered record boundary;
- unsupported values are silently coerced or runner and auditor lose
  independent claim-level validation;
- a proposed shared library lacks a three-consumer semantic evidence table;
- any test evaluates a registered arm or writes a registered result path;
- exact numerical equality across the producer boundary is not demonstrated.

The next review may return only
`p5d-production-preflight-protocol-sufficient-target-closed` or
`p5d-production-preflight-protocol-needs-amendment`. Neither verdict is P5-D
evidence, oscillator evidence or permission to run attempt 4.
