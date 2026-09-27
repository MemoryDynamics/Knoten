# G1--G3 sealed-input Git-blob portability review

Date: 2026-09-27

Remediated implementation revision: `b8d33c4833ded85513baf0ebcffbd7e836245c9c`

## Incident

Official CI run
[`36304429782`](https://github.com/MemoryDynamics/Knoten/actions/runs/36304429782)
failed five Bridge tests after 1188 other tests passed. Every failure had the
same cause: the registered G4 audit SHA-256 described Windows checkout bytes
with CRLF, whereas the Linux checkout supplied LF bytes. No numerical target
backend was called.

Forensic comparison showed:

- G4 result, G4 manifest, G5 result and G5 manifest had identical checkout
  and Git-blob SHA-256 values;
- only the G4 audit differed: Windows checkout SHA-256
  `366d221e6d14093da48f7a8f4ea1a439d4b26e5635b65c95bcb763bc968a2aa5`,
  canonical Git-blob SHA-256
  `e83309992fe8b964c507930664f557367a50d87d32aedf7bf39ecbe1bb346d19`.

## Remediation review

The third outcome-blind protocol amendment binds every sealed input to
canonical `HEAD:path` Git-blob bytes. Both the production composition loader
and the separately implemented standard-library auditor now retrieve those
bytes through `git cat-file blob`. Schema and still-closed governance bind the
amended protocol and corrected audit digest.

The change does not alter a model parameter, numerical value inside a sealed
record, root box, threshold, gate order or decision rule. A new regression
forbids checkout-byte reads during sealed-component loading. The focused
Bridge/guard suite passes 46 tests. Official CI run
[`36305048454`](https://github.com/MemoryDynamics/Knoten/actions/runs/36305048454)
then passes full Ruff, 1194 tests and strict documentation build on revision
`b8d33c4833ded85513baf0ebcffbd7e836245c9c`.

## Verdict

**`g1-g3-git-blob-portability-remediation-pass-target-closed`**

The first CI failure is a real portability finding and remains part of the
audit trail. The focused remediation closes that finding without producing
or inspecting a G1--G3 target result.
