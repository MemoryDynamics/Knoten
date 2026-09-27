# G1--G3 bridge attempt 1 homotopy-record failure

Date: 2026-09-27

Status: **`g1-g3-inconclusive-homotopy-record-validation-failure`**

## Provenance

- Authorization UUID: `84e81fc5-a78c-4a2a-9fb3-f771bd154688`
- Execution revision: `750ef3b3faa35c7d1cbbc4ef33f44079b80f4656`
- Reviewed implementation revision:
  `b8d33c4833ded85513baf0ebcffbd7e836245c9c`
- Official implementation CI:
  `https://github.com/MemoryDynamics/Knoten/actions/runs/36305048454`
- Receipt:
  `reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_g1_g3_bridge_receipt_2026-09-27.json`
- Receipt SHA-256:
  `24a4b346532defc7e8d940921d10702f2f05f1d7126e9fe8d31aa0a0b32713ce`

## Observed boundary

The one-shot guard passed and created the exclusive receipt before target
work. After the numerical orchestration returned, the semantic validator
stopped before audit or publication at

```text
$.finite_branch.homotopies[0].slabs[0].box.radius: center mismatch
```

No result JSON, readable report, independent-audit JSON or publication
manifest was written. No root coordinate, interval or partial gate decision
was printed or persisted. The receipt consumes attempt 1 and forbids an
automatic rerun.

## Code-level diagnosis

The homotopy backend constructs the registered box with `mpmath.iv` at 120
decimal digits and records its outward-rounded endpoints. The homotopy
validator nevertheless requires their decimal midpoint and width to equal the
ideal center and width exactly. The root-certificate validator in the same
module already uses the correct stronger representation check: the ideal box
must be contained in the recorded outward box, and excess inflation must stay
below a precision-scaled bound.

Synthetic tests used exactly symmetric mock endpoints, so they did not expose
this production-only record-boundary mismatch. The exception is therefore a
pipeline incident, not evidence of branch loss or homotopy failure.

## Consequence

Attempt 1 is inconclusive. It establishes no G1--G3 branch connection and no
negative scientific outcome. A retry requires an outcome-blind protocol
amendment, a falsification test with outward-rounded mock endpoints, complete
review and CI, and a new explicit user authorization.
