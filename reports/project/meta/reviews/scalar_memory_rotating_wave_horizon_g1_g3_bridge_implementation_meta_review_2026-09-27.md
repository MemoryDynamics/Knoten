# G1--G3 bridge implementation meta-review

Date: 2026-09-27

Reviewed implementation revision: `735b0559984348acbac5ad097b194f36a80814e9`

## Question and scope

This review asks whether the registered G1--G3 bridge can be authorized for
one numerical execution without silently changing the scientific question,
rerunning the sealed G4/G5 components, or accepting an unauditable result.
It reviews the protocol/schema binding, numerical adapters, orchestration,
semantic validation, independent record audit, publication order and
execution guard. It does not inspect a target result because no target call
has occurred.

## Evidence reviewed

- The protocol and schema bind the fixed parameter set, seven horizons,
  two precision panels, six 64-slab homotopies, direct finite-sum replay,
  endpoint inclusions, controls, decision precedence and claim boundary.
- The bridge backend exposes finite roots, homotopies, local exclusion,
  direct replay and FIFO controls. It exposes neither the G4 tail solver nor
  the G5 Arnoldi/trajectory runner.
- Five sealed G4/G5 result, manifest and audit files are hash-checked before
  their endpoint roots are extracted.
- Validator and standard-library auditor independently reconstruct all
  decision-relevant Boolean fields from stored intervals, decimals, hashes
  and partition witnesses. Publication writes result, report and audit before
  a hash manifest and refuses overwrites.
- The tracked governance remains `closed`, records no target call and is
  checked before numerical modules are imported.
- Focused bridge and execution tests pass: `45 passed`. The complete local CI
  mirror passes `1193` tests, full Ruff and MkDocs `--strict` under the pinned
  dependency set.

## Findings and remediation history

1. **Resolved major -- free G0/G6 assertions.** The first contract allowed a
   direct-replay Boolean and FIFO-control verdicts that could not be
   reconstructed. The amended schema stores signed primitive sums, residuals,
   complete error metrics and expected/observed age-history hashes. Validator
   and auditor now recompute their gates.
2. **Resolved major -- publication paths not fully bound.** The result now
   carries distinct registered paths; the manifest and independent audit bind
   those paths and their bytes. The manifest is written last.
3. **Resolved major -- weak authorization test surface.** The one-shot guard
   now has a positive synthetic authorization test and adversarial tests for
   remote-head substitution, dependency drift, protected-blob drift,
   post-review source drift, mixed authorization commits and a false
   readiness verdict. Every mutation fails before receipt creation.
4. **Resolved defect -- interval witness shape.** A synthetic certificate
   initially used an invalid interval-Jacobian shape. The strict schema and
   tests now require a two-by-two matrix whose entries are outward intervals.
5. **Resolved defect -- high-precision zero portability.** Direct replay no
   longer relies on the backend-specific `mp.zero` convenience value.

No unresolved Critical or Major code finding remains in this target-free
review.

## Residual limitations

- The standard-library auditor is independent of the target runner and
  third-party numerical packages, but it is a record/hash/relationship audit,
  not a second interval-arithmetic implementation.
- Krawczyk and homotopy evidence remains local to the registered boxes and
  fixed-alpha ladder. Even a positive result would not prove global root
  uniqueness or stability at infinite memory.
- G4 local infinite-memory existence and G5 local finite-H stability are
  sealed inputs. The bridge can identify their local root branch; it cannot
  promote G4 into a stability theorem.
- Official GitHub CI is still required before authorization; local tests,
  lint and strict documentation build already pass.

## Verdict

**`g1-g3-implementation-pass-readiness-ci-open-target-closed`**

The implementation is coherent enough to proceed to full CI and a separate
readiness review. It is not yet authorized for a target call. A successful
readiness review must bind the exact protected blobs and official CI run;
only a later explicit user authorization may open the one-shot governance.
