# N0 implementation-readiness review

Date: 2026-09-01  
Verdict: **`n0-implementation-ready-for-one-registered-run`**  
Scope: target-free review of the resolved-noise rotating-wave runner; this
does **not** open P5 or constitute an N0 result.

## 1. Frozen ancestry and CI evidence

| item | immutable identifier |
|---|---|
| design freeze | `6b17f9562baed07f842e1cb9f3a565652371f5d4` |
| final clarified protocol freeze | `67d6dfcba73f4422c228cdf393fc65bf9564e532` |
| implementation freeze | `04c960e66601e8f8afb497ebf70a6a3973a23c6e` |
| implementation CI | [GitHub run 33466828805](https://github.com/MemoryDynamics/Knoten/actions/runs/33466828805), success |
| protocol blob | `0b380f94a7e2d7b871911d2159cf2b48ec37fd30` |
| design-audit blob | `f947f428dff1069603bad7053826b438c2bb66cc` |
| runner blob | `918113a5be429b80b8911f5f1684a50c2717387a` |
| runner-test blob | `7384c6d776aa2f4f089e9108bbe3d3d212c333db` |
| primitive-test blob | `b0a968dd4bd38a7b600992bbc689e99c4eba17c1` |

The implementation-freeze revision was clean and exactly synchronized with
`origin/codex/p4rs-noise-stress`. The three registered JSON, Markdown and PNG
outputs and their `.tmp` siblings were absent. The target grid has not been
executed.

## 2. Review method

The review compared the runner line by line against the prospective protocol,
then used only synthetic short-history cells. It did not call `run_gate()` and
did not advance either registered candidate over the registered grid.

Local evidence on the implementation freeze:

- `853 passed` in the complete test suite;
- CI-scope Ruff check over `src`, `tests` and `experiments/current`: pass;
- strict MkDocs build: pass;
- synthetic runner and primitive tests: pass;
- PNG written successfully through the registered `.png.tmp` suffix;
- status-frontdoor tests require N0 before P5.

Legacy lint findings outside `src`, `tests` and `experiments/current` predate
N0 and are not changed or hidden by this review.

## 3. Prospective registration audit

The implementation preserves:

1. exact ordered `chi=0,1e-22,...,1e-2` grid;
2. exact seeds `2026083101..03`;
3. Anchor then L3, increasing grid, seed, base then pair order;
4. `PCG64` fine path and exact pairwise Brownian aggregation for Anchor;
5. `epsilon=chi R sqrt(alpha)` and serialized `D/R^2=chi^2/2`;
6. prepared positive-chirality histories with the registered full-history
   transverse perturbation of norm `1e-7 R`;
7. common noise for base and transverse pair;
8. 401 registered samples through common memory time `tau=20`;
9. intended versus actually represented binary64 increments;
10. separate unresolved, partially resolved and resolved labels;
11. translation- and proper-rotation-quotiented D0 metrology;
12. frozen radius, edge-phase, chirality and pair-contraction gates;
13. all cells executed after a failure, with only the crossing arm stopped;
14. no interpolation between registered amplitudes;
15. display-only log floor, explicit zero markers and linear equal-aspect x-y
    axes;
16. registered output paths, overwrite refusal and cleanup on a failed write.

## 4. Defects found before target inspection

Three non-cosmetic inconsistencies were found and fixed prospectively:

| defect | consequence if retained | correction |
|---|---|---|
| protocol used `D0/R` although the design froze `D0/reference_D0_norm` | scale-dependent gate drift | restored the design denominator; kept `D0/R` only as secondary metrology |
| stop text retained `0.25 R` | stopping and pass metrics used different norms | restored `0.25 reference_D0_norm` |
| first runner stopped both arms when one crossed | early pair failure truncated the base trajectory | separate active state, step count and stop reason per arm; synthetic regression added |

The committed protocol history exposes both clarifications. No result, target
trace, seed response or boundary estimate was available when they were made.

## 5. Fail-closed behavior

The runner refuses execution unless:

- the design and clarified protocol commits are ancestors of `HEAD`;
- every frozen source/document blob matches;
- this readiness review is committed in the execution history;
- the tree is clean and exactly synchronized with its upstream;
- all registered final and temporary outputs are absent.

Non-finiteness, missing late samples, quotient stopping, incomplete arm
execution or malformed resolution data cannot become a pass. A resolved arm
crossing any primary gate makes its grid cell fail. Unresolved and partially
resolved low-amplitude cells are retained and cannot be relabelled as stable.

## 6. Remaining limitations

- The three seeds are deterministic stress arms, not physical replications.
- Anchor and L3 are two prepared cells, not a convergence sequence.
- The horizon is finite (`tau=20`); no stationary noisy invariant measure is
  tested.
- Brownian refinement supplies a controlled cross-scale comparison but not a
  derivation of a continuum stochastic law.
- Binary64 resolution is measured for this implementation and coordinate
  scale only.
- A bracket is a registered decade interval, not an exact critical amplitude.
- The scan cannot calibrate Planck's constant or support interaction, spin,
  inertia or mass language.

## 7. Readiness decision

The implementation is ready for **one** registered N0 execution after this
review commit itself is pushed and CI-green. That run must produce the three
complete registered artifacts without source changes. The raw result must
then be committed before an independent recomputation and separate critical
result review.

P5 remains sealed until that result review explicitly updates the priority
gate. A runner pass or attractive diagram alone is insufficient.

