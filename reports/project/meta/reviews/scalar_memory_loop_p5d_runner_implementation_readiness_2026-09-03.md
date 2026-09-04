# P5-D runner implementation readiness review

Date: 2026-09-03.

Implementation revision: `7d7f8a9eecaf72909cc937446d77e7589b48e24a`.

Verdict: **`p5d-runner-ready-target-still-closed`**.

This is a target-free infrastructure verdict. It neither authorizes attempt
3 nor supplies interaction, oscillator, inertia or mass evidence.

## 1. Reviewed contract

The review uses the amended runner-remediation protocol frozen at revision
`ed21f5c33591f311cf14617f0d23fc51cddc2ff7`, blob
`1f94be94bdf4b2512f68b69dcc5b3958e7efe7b6`. Candidate, equations, panel,
thresholds, response reducers and decision precedence were not changed.

The protected implementation table is:

- Blob `src/emergenz_knoten/mutual_center_coupling.py`: `86a064692b33514a536b93877d4d5dcf33894c64`
- Blob `experiments/current/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_gate.py`: `8b16cb0246306347a7115a8f7632e4546412b7fa`
- Blob `experiments/current/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_result_audit.py`: `a768b1c292b6ff0aa35aaecf7f0a6fa6951afd62`
- Blob `experiments/current/dynamics/rotation/scalar_memory_loop_p5d_governance.json`: `65169b7ad5b515731dc16c7dbd1080e97f081eec`
- Blob `experiments/current/dynamics/rotation/scalar_memory_loop_p5d_result_schema_v2.json`: `66f77703fe4548ee490fd18e7e3b7d9b0af602ab`
- Blob `tests/test_rotating_wave_p5d_mutual_center.py`: `2b020579abb53ec14caa8e2b3921d1eb1fb28dd9`
- Blob `tests/test_rotating_wave_p5d_result_audit.py`: `34a0ddd3bb4a38c59b3d2a0af919da9a6183aa59`

The v2 schema content SHA-256 is
`ba9af89e5f2646db31ac0924825a643079fbfaf1d28d70d0696253f1da9cedc6` and is
pinned by the closed governance record.

## 2. Positive evidence

- The local complete suite passed: 929 tests.
- CI run [33918599007](https://github.com/MemoryDynamics/Knoten/actions/runs/33918599007)
  completed successfully on the exact implementation revision. Its lint,
  tests and strict documentation steps all passed.
- The schema validates before serialization and after a strict JSON round
  trip. Both runner and standard-library-only auditor implement independent
  path-aware validators over the same tracked contract.
- One complete synthetic 64 channel-off plus 768 active-arm payload traversed
  validate, serialize, deserialize, validate, render, publish and independent
  audit without entering a registered target arm.
- Channel-off mobility is exactly `null`; active mobility must be finite.
  Unknown or missing keys, wrong lengths, Boolean-as-integer, nonfinite values,
  NumPy scalars and unsupported objects fail with a JSON path.
- An unavailable response has only `available=false` and a reason. Rendering
  does not inspect absent diagnostics.
- JSON and Markdown are prepared and hashed first. The publication manifest
  is renamed last. Failures injected at each of the three rename operations
  leave no valid manifest or partial final result.
- The independent auditor loads and validates the manifest before the result,
  verifies receipt/result/report hashes, and rejects absent or changed
  members.
- The one-shot lease binds the implementation revision, six non-governance
  protected blobs, the closed-governance blob, schema digest, readiness blob
  and a successful official GitHub Actions record. Offline metadata, wrong
  head, failed conclusion and protected-blob drift stop before receipt and
  target.
- The attempt-3 receipt is created exclusively and is never cleaned up. A
  second creation therefore fails and the lease is consumed even if later
  work fails.

## 3. Adversarial findings

No blocking discrepancy remains within the remediation scope. Three claim
restrictions remain material:

1. The successful rehearsal uses synthetic structural data. It is evidence
   for representation and control flow only.
2. Manifest-last publication is a validity protocol, not cross-file
   filesystem atomicity. A host crash may leave unmanifested debris, which is
   correctly not a result and forbids automatic retry after receipt creation.
3. The coupled center port has an exact first-order relaxation nullmodel when
   native center motion is held fixed. A coupled harmonic oscillator would
   require an additional memory-induced pole pair and separate scaling tests;
   it is not entailed by this readiness verdict.

## 4. Authorization boundary

The tracked governance state remains `closed`, `target_authorized=false` and
`authorization=null`. Both previous calls remain recorded as infrastructure
incidents. A prospective attempt 3 requires a new explicit decision followed
  by a governance-only authorization commit that binds this review blob and CI
  run 33918599007. Until then the runner fails before receipt creation, pair
initialization and every registered arm.

Accordingly the narrow verdict is
**`p5d-runner-ready-target-still-closed`**.
