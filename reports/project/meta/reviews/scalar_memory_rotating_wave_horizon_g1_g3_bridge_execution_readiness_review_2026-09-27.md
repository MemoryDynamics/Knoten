# G1--G3 bridge execution readiness review

Date: 2026-09-27

Implementation revision: `b8d33c4833ded85513baf0ebcffbd7e836245c9c`

Official CI:
https://github.com/MemoryDynamics/Knoten/actions/runs/36305048454

Verdict: **`g1-g3-implementation-ready-target-closed`**

## Evidence

- The third amended protocol is frozen as Git blob
  `97d06fc41ac57f4eb0b90bda5c15c81b3eb36123`, SHA-256
  `dfdb4841b7ce94ac3821697f5d3281d8a17412d0524bdb7ea7ae9d3565062823`.
- Official CI reports `success` for the exact implementation revision:
  full Ruff, 1194 tests and MkDocs `--strict` pass.
- The preceding failed CI run is retained and separately reviewed. It exposed
  checkout-byte hashing of one Markdown input; the corrected implementation
  and independent auditor both use canonical Git-blob bytes.
- The tracked governance is still `closed`, `target_authorized` is false,
  `target_calls_recorded` is empty and no reserved result or receipt exists.
- Synthetic positive authorization and adversarial remote-head, dependency,
  blob, source-drift, mixed-commit and readiness mutations all fail or pass at
  their registered boundary before receipt creation.

## Protected implementation blobs

- Blob `requirements.txt`: `257723e469e56d5e1db0efcaff57c26e71a9ebf5`
- Blob `reports/project/meta/preregistration/scalar_memory_rotating_wave_horizon_g1_g3_bridge_protocol_2026-09-27.md`: `97d06fc41ac57f4eb0b90bda5c15c81b3eb36123`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g1_g3_bridge_result_schema_v1.json`: `6e5b597370575f44b34433e26ed0891dd9259a9d`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g1_g3_bridge_gate.py`: `f7f4873bb53b1092ad78f3f2d3164be53e90f586`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g1_g3_bridge_result_audit.py`: `b24a0a8432536127b40866bb98d3021f69c2b602`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_g1_g3_bridge_execution.py`: `fed1e733045bf053bf40b3b3f41f6d325193a407`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_transfer_gate.py`: `52871500b0d5523967454a5b1a9614d895dcf574`
- Blob `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_horizon_transfer_result_audit.py`: `0402802aa8b1b68efd40eee75920bc81501e620e`
- Blob `src/emergenz_knoten/rotating_wave.py`: `3b70f408ab8bb24e7cc6df4b9c61f54f17a65a4d`
- Blob `src/emergenz_knoten/rotating_wave_dense_continuation.py`: `26043400e721855dc47c512bc36524555d09b089`
- Blob `src/emergenz_knoten/rotating_wave_horizon_stability.py`: `376f263af4891869a7e81969ca05e11ba86735a5`
- Blob `src/emergenz_knoten/rotating_wave_interval.py`: `e269e729c68c8030a6aae222fb4fa67069dd46fd`
- Blob `src/emergenz_knoten/rotating_wave_stability.py`: `9defb5a6876371202e1ba57cea030c997b9c6edd`
- Blob `src/emergenz_knoten/rotating_wave_stability_gate.py`: `630beb9952abefea823d91388dcbb2de8f1a2927`
- Blob `src/emergenz_knoten/strict_json_contract.py`: `221372ea86f857aa4141e2609e46a0dc536c1ab4`
- Blob `tests/test_rotating_wave_horizon_g1_g3_bridge.py`: `6764cd5d2b7cd18cd8c80df43fd58b047f6f5917`
- Blob `tests/test_rotating_wave_horizon_g1_g3_execution.py`: `5c235d3cdba2883e337dd9052044047da160fefa`
- Blob `tests/test_rotating_wave_horizon_transfer.py`: `dff5c1dd4de34868dbc77acf1b7e0f7fb9af8942`

## Remaining boundary

Readiness is not numerical evidence. The target remains sealed until a later
explicit user authorization is encoded in a governance-only commit. A single
authorized execution may then consume one receipt, run the registered ladder,
audit the record and publish its manifest last. No outcome is presupposed.
