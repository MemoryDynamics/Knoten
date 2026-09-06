# P5-D production-path preflight protocol

Date: 2026-09-06.

Status: **prospectively frozen, target-free, implementation closed**.

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

## 4. Exact defect and permitted future correction

The attempt-3 defect is outcome-independent. In a Channel-off arm,
`coupling == 0` makes the energy floor `numpy.finfo(float).tiny` win. Division
of native zero rival maxima by that NumPy scalar produces six finite
`numpy.float64` zeros. The strict v2 validator correctly rejects them.

A future implementation protocol may permit only these infrastructure
changes:

- pure claim-scoped record constructors with explicit native primitive
  outputs;
- an explicit native finite energy-scale constructor preserving the exact
  numerical value;
- native primitive construction for every registered metric, gate and count;
- validation of each completed arm record before it enters the panel;
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
4. **Exact arm-shape witnesses:** one Channel-off and one active record use the
   same production record constructors, not hand-written dictionaries. The
   off mobility minimum is only `null`; every active minimum is finite.
5. **Complete panel rehearsal:** 64+768 records created through those same
   constructors traverse original validation, strict encoding, round-trip
   validation, report rendering, manifest-last publication and the independent
   auditor in temporary paths.
6. **Target traps:** initialization, native FIFO stepping,
   `mutual_center_step` and registered panel evaluation are trapped and remain
   at zero calls throughout every preflight test.
7. **Mutation falsifiers:** reintroducing the NumPy energy floor at the record
   boundary, a NumPy Boolean gate, a non-finite active metric, a stale output
   or a serializer `default=` coercion makes the rehearsal fail.

Synthetic witnesses test representation and control flow only. They are not
P5-D data and may not be described as interaction evidence.

## 6. Early failure and publication boundary

A future authorized runner must execute a pure, target-free record canary
before creating its one-shot receipt. After receipt creation, each real arm
must be schema-validated immediately when its record is completed. This does
not prevent all runtime failures, but it prevents a known record defect from
remaining hidden until all 832 arms have run.

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

Even a positive readiness review leaves P5-D closed. Attempt 4 would require
a later governance-only authorization commit and a new explicit user decision.

## 8. Stop conditions and verdict boundary

The work stops with no target authorization if any of the following occurs:

- a scientific blob or frozen estimand changes;
- the preflight cannot catch the attempt-3 producer path without target data;
- unsupported values are silently coerced at serialization;
- runner and auditor lose independent claim-level validation;
- a proposed shared library lacks three semantically identical consumers;
- any test evaluates a registered arm or writes a registered result path;
- exact numerical equality across the producer boundary is not demonstrated.

The next review may return only
`p5d-production-preflight-protocol-sufficient-target-closed` or
`p5d-production-preflight-protocol-needs-amendment`. Neither verdict is P5-D
evidence, oscillator evidence or permission to run attempt 4.
