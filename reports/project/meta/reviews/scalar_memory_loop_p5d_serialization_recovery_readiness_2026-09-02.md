# P5-D serialization-recovery readiness review

Date: 2026-09-02.

Verdict: **`p5d-implementation-ready`**.

This is a target-free review of the narrowly frozen serialization recovery.
It does not construct, inspect or advance the registered Anchor--Anchor target
panel and does not predict its decision. The failed first invocation remains
`p5d-inconclusive`: it created no standard artifact and exposed no decision.
Subject to green CI for the commit containing this review, this verdict
authorizes exactly one clean replacement invocation. That invocation is error
recovery, not a replication or a second statistical observation.

## 1. Frozen identity

Implementation revision: `f6da955b388b4f2f4e15632fd567a06fcb5fbf75`

Blob `src/emergenz_knoten/mutual_center_coupling.py`: `86a064692b33514a536b93877d4d5dcf33894c64`

Blob `experiments/current/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_gate.py`: `32a2456c33befac7d4571a0e57c9e43bf57c8e30`

Blob `experiments/current/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_result_audit.py`: `6e9acb9fbd4592d13ab244dd84915653c0aafd04`

Blob `tests/test_mutual_center_coupling.py`: `ad84f6dda132a8fa152f807d22472c6a55659039`

Blob `tests/test_rotating_wave_p5d_mutual_center.py`: `2c16b42ed0386c7a367099998d9da0f8e2b4b446`

Blob `tests/test_rotating_wave_p5d_result_audit.py`: `17a0ae6b5db61b0889a5f0a60b9203809eecbe19`

The recovery implementation descends from the recovery freeze revision
`9fdab8d534ebadfdd155bde55c3c7e509783dd53`. Its protocol blob is
`508b642b12884996ccb87f354e875053bdf36c5a`. The runner verifies both values
before it can initialize the registered panel. The original corrected P5-D
protocol remains pinned at revision
`d7a4c5ec4d40f1899940161877b0ab80b7a8c0c7`, blob
`bf3325d550ae2288d8e4012e0480077abf51032e`.

## 2. Incident boundary and defect reproduction

The first authorized invocation used the clean, upstream-synchronized
readiness revision `5f04aba8770c2dc74b4ac3daa20e67aa59d7c7e2`.
It completed panel construction and then raised `TypeError` at the final
`json.dumps` boundary because a nested `numpy.bool_` is not a standard JSON
scalar. Neither registered JSON nor Markdown, nor their temporary paths,
existed after the exception. No gate, decision or response value was printed,
persisted or inspected.

The failure is independently reproduced by serializing a nested NumPy boolean
without evaluating any P5-D trajectory. Real-arm metrics can be NumPy floating
scalars; comparing them with the frozen Python-float thresholds can yield the
rejected NumPy boolean. This establishes an outcome-blind serializer type
boundary. It does not establish anything about the interaction hypothesis.

## 3. Exact recovery diff

Four of the six implementation blobs are byte-identical to the original
implementation review. Only the runner and its test module differ. Source
review found exactly three production changes:

1. the runner pins and verifies the recovery protocol and points to this new
   recovery-readiness review;
2. the final JSON serializer converts only `numpy.bool_` to `bool`,
   `numpy.integer` to `int`, and `numpy.floating` to `float`;
3. the existing `json.dumps` call retains `allow_nan=False`, sorted keys,
   indentation, digest construction, atomic pair write and overwrite refusal.

Unsupported arrays, complex scalars and arbitrary objects still raise
`TypeError`. Non-finite floats still raise `ValueError`. No permissive array
conversion, string fallback or generic object traversal was added.

A diff against the original implementation found no change to either native
FIFO equation, mutual-center equation, simultaneous-write convention,
notched center, ledger, response reconstruction, decision label or decision
precedence. It likewise found no change to `R`, `theta`, `q`, `H`, `eta`, `G`,
mobility, distances, phases, chiralities, coupling strengths, signs, arm
ordering, update count, sample windows, high-precision references or any
scientific threshold. The recovery therefore changes representation only,
not an estimand or numerical trajectory.

## 4. Target-free falsification evidence

The recovery tests exercise the exact production serializer with the complete
synthetic panel shape: 64 channel-off plus 768 active records. Nested
`numpy.bool_`, signed and unsigned NumPy integers, and `numpy.float32` round
trip to the corresponding JSON scalar types. Python-native boolean, integer
and float values round trip unchanged.

Adversarial cases establish the fail-closed boundary:

- NumPy NaN, positive infinity and negative infinity are rejected under
  `allow_nan=False`;
- a NumPy array, complex scalar and arbitrary object are rejected with
  `TypeError`;
- replacing the recovery-readiness path with an absent path while turning the
  registered panel into a trap raises the seal error and records zero panel
  calls;
- the serializer helper itself calls only the standard JSON encoder and has
  no path to the target runner.

The synthetic 832-record object tests serialization and classifier-shaped
data plumbing only. It is not a generated Anchor--Anchor trajectory and is
not evidence for a mutual response.

## 5. Execution evidence

Final local checks at the implementation revision were:

| check | result |
| --- | --- |
| three affected P5-D test modules | 44 passed in 29.70 s |
| complete repository test suite | 901 passed in 135.95 s |
| exact CI Ruff scope | all checks passed |
| strict MkDocs build | passed in 1.14 s |
| whitespace check | passed |
| standard JSON/Markdown paths | absent |
| standard `.tmp` paths | absent |

The pushed implementation revision passed
[GitHub Actions run 33590997553](https://github.com/MemoryDynamics/Knoten/actions/runs/33590997553):

- exact Ruff scope: all checks passed;
- complete test suite: 901 passed in 172.43 s;
- strict MkDocs build: passed in 1.01 s;
- complete job: green in 3 min 42 s.

This CI result validates implementation and repository consistency only. It is
not a P5-D observation.

## 6. Referee verdict and authorization

The recovery is minimal, outcome-blind, fail-closed and covered at the exact
production serialization boundary. Its provenance guard prevents the
replacement target from running before this review exists; the clean-tree and
exact-upstream guards prevent a locally modified replacement. The standard
and temporary result paths remain absent at this verdict.

The earlier scientific implementation review remains applicable to the
unchanged equations, panel, controls and decision logic. This review does not
weaken its interpretation boundary: even a later pass would show only that
the declared mutual-center port produces the preregistered response while the
registered controls hold. It would not establish spontaneous interaction,
charge, a universal force law, intrinsic spin, momentum, inertia, mass, a
toroidal field topology or a mediator.

Subject to a green CI run for the commit containing this review, exactly one
clean, upstream-synchronized replacement standard invocation is authorized.
If it fails, no automatic retry is permitted. If it creates both standard
artifacts, they must be committed and pushed unchanged before the independent
result auditor is run.
