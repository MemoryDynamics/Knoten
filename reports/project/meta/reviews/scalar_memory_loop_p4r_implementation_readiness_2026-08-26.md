# P4-R-phi implementation-readiness review

Date: 2026-08-26.

Decision: **`implementation-ready-for-first-registered-target-run`**.

This is a pre-target software and protocol-conformance review. It is not a
P4-R result, does not inspect a registered P4-R trajectory and does not alter
the historical P4 decision `p4-source-write-architecture-fail`. At the time
of this review, neither registered P4-R output path exists.

## 1. Frozen basis and scope

The implementation is downstream of, and checks at runtime, the following
prospective freezes:

| item | immutable identifier |
| --- | --- |
| P4-R design commit | `0bf9b3020f26acfaf5273c1efab5dcc52d596239` |
| P4-R protocol commit | `cb863d4a88c1072637116a0296ab9fc20356a675` |
| P4-R protocol blob | `b81fa535c1921c2f11f83e5585bf38b05e0a08d5` |
| source-referee charter commit | `071c9d33c8611d0a1ef1cb3da620acb7dcdb5f7d` |
| source-referee charter blob | `2bc9bba4c2c5f9184201987f2f97faac2c91aec5` |
| historical P4 JSON SHA-256 | `ea0651e206451e5f87ec08ab3f66ec68df2c04bee2d1b9d67219736058a275cc` |
| source/write blob before reconciliation | `d8de95f4f46adc43c37d6d1affdc73be14f70ec3` |

The target runner refuses to start unless the worktree is clean, its current
revision is fully synchronized with the configured upstream, both freeze
commits are ancestors, every frozen dependency blob matches and the
historical P4 JSON retains both its hash and formal decision.

## 2. Native-equation preservation

### Evidence

The reusable source/write step exposes four values that were previously
temporary or implicit:

1. the native provisional FIFO history;
2. the pre-addition write increment of slot zero;
3. the pre-addition actuator increment;
4. the prescribed orbit-center increment.

The advanced state still evaluates the same expressions in the same
binary64 association as the historical implementation:

```text
history_increment = alpha * complex_to_vector(write_force)
advanced[0] += history_increment
actuator_increment = alpha * mobility * external_force
q_after = q_before + actuator_increment
```

The native FIFO map, force law, candidate, coupling strength, mobility,
readout coefficients and state-update order are unchanged. The historical P4
source/write and regression tests pass with the extended record type.

### Inference

The extension is observational for the state trajectory: it makes
pre-addition operands available to a cancellation-safe diagnostic but does
not add a force, state, fit parameter or integration order.

### Remaining limitation

This is source-level and regression evidence, not a compiler-level proof of
bitwise equivalence across every Python/NumPy implementation. The registered
execution therefore records the exact runtime and implementation blobs.

## 3. Arithmetic-metrology review

The implementation follows the frozen distinction between two claims:

- local slot identities are evaluated on the actual forced-increment scale;
- cancellation-dominated differences of two order-one full dot products are
  checked against conservative binary64 forward-error envelopes.

The weighted bound uses `math.fsum`, the frozen `gamma_(8H)` factor and an
outward final `nextafter`. The implementation checks normal-or-exact-zero
validity not only for source operands but also for coefficient/history
magnitudes, weighted terms, sums, insertion bounds, local bounds, full
residuals and final envelopes. A nonzero subnormal value makes the arm
invalid and the panel inconclusive.

At updates 1, 2000 and 4000, every active arm is independently reevaluated at
80 decimal digits. Each binary64 component enters `mpmath` through
`float.as_integer_ratio()`, so decimal formatting cannot silently perturb the
reference operand. The replay checks both containment in the full envelope
and the distance from the stored binary64 residual.

Deliberately corrupting a stored full residual by `1e-8` fails both the
binary64 envelope test and the high-precision-distance test. Injecting a
nonzero subnormal pre-addition increment invalidates the normal-number gate.

Passing this layer would show compatibility with the declared forward model.
It would not constitute interval arithmetic, formal verification or a second
independent trajectory implementation.

## 4. Registration, dependence and decision review

The runner serializes the exact prospective order:

- 16 channel-off arms: phase index, then chirality `(+1, -1)`;
- 32 active arms: phase index, then chirality `(+1, -1)`, then offset sign
  `(+1, -1)`.

The response is recomputed from raw active and matching channel-off traces;
it does not trust the convenience response stored by an active arm. Full
traces must have exactly the registered 401 sample steps and finite values.

The implementation treats phase and chirality relations as covariance, not
replication:

- all 16 unique cross-chirality mirror pairs are checked under complex
  conjugation;
- all 16 unique half-turn pairs are checked under multiplication by `-1`;
- the eight phase averages are retained explicitly, including their four
  mirror-related pairs;
- the six-of-eight support rule is a deterministic sign-support gate, not a
  binomial test or confidence statement.

Synthetic traces recover a prescribed positive transverse response exactly,
pass both covariance maps and recover eight-of-eight support. A registered
three-percent sign-even contaminant fails the frozen two-percent even/odd
gate. Duplicate or missing arms make the panel unavailable.

Decision-table tests cover scalar, positive-chiral, directional-fail and
inconclusive regions. They also confirm the frozen precedence: invalidity
dominates a ledger failure; a valid ledger/metrology failure cannot be
promoted by dynamics; and a failed symmetry, odd-signal or dynamical gate
remains inconclusive.

## 5. Implementation blobs before commit

These are the Git blob identifiers calculated from the reviewed working-tree
contents. The registered target additionally records the committed `HEAD`
blobs and refuses an unpushed revision.

| path | reviewed blob |
| --- | --- |
| `experiments/current/dynamics/rotation/scalar_memory_loop_p4r_phase_metrology_gate.py` | `d4e89d5f72a6cb07bed42f83a3b52d0fce742351` |
| `src/emergenz_knoten/orbit_center_actuator.py` | `63d31bc47291f76c65a5633f14436ccd2105fe9a` |
| `tests/test_orbit_center_actuator.py` | `7e770cd9dc6a4d410c0593dc909512eb27945abb` |
| `tests/test_rotating_wave_p4r_phase_metrology.py` | `7ef573cbfafc1bf196e5ae5944853c4c1cb67f07` |

## 6. Pre-target verification

No pre-target test calls `_run_active_arm`, `_run_channel_off` or `run_gate`.
The tests use only historical P4 static controls, frozen-grid construction and
synthetic small-H or synthetic response records.

| verification | result |
| --- | --- |
| focused source/write, historical P4 and P4-R tests | 26 passed |
| complete repository test suite | 796 passed |
| exact CI Ruff scope (`src`, `tests`, `experiments/current`, `experiments/cli.py`) | passed |
| strict MkDocs build | passed |
| default P4-R JSON before target | absent |
| default P4-R report before target | absent |

The default-output guards are themselves tested: the registered paths are
recognized, writes use a same-directory temporary file followed by an atomic
replace and a stale temporary file causes refusal. The target runner checks
for an existing registered JSON or report before any target trajectory is
advanced.

## 7. Adversarial limitations retained for the result review

1. The run is deterministic and single-environment; exact reproduction on a
   second clean environment remains part of the later source-referee audit.
2. `gamma_(8H)` is deliberately conservative but is still an analytical
   binary64 model around NumPy dot products, not an outward-rounded BLAS
   certificate.
3. The 80-digit replay independently reevaluates arithmetic only at three
   stored states per arm. It does not integrate an independent trajectory.
4. Eight-node quadrature can alias phase harmonics of order 8, 16 and above.
5. The 32 active arms contain algebraic controls, not 32 independent samples.
6. Only one new perturbation amplitude is registered; no amplitude scaling
   follows from any outcome.
7. A positive P4-R result would remain outcome-informed reconciliation after
   the P4 discovery panel. It cannot erase or rename the P4 fail.

## 8. Readiness verdict

The implementation matches the frozen scope, contains discriminating
synthetic failures, preserves the historical state update and passes the
repository-wide pre-target checks. It is therefore ready for exactly one
first registered P4-R-phi execution from the clean pushed commit containing
this review.

This verdict authorizes calculation, not a scientific claim. The first JSON
and report must be committed and pushed unchanged before their gate-specific
critical review. The separately frozen publication-source referee audit is
mandatory after that review regardless of whether P4-R passes, fails, lands
in the scalar region or remains inconclusive.
