# Aktueller Stand

Stand: 2026-06-29.

## Repository

- Arbeitsbranch: `main`.
- Remote: `https://github.com/MemoryDynamics/Knoten`.
- Der historische `cleanup`-Stand existiert noch als Referenz, neue Arbeit
  laeuft auf `main`.
- Rohnotizen und Chatverlaufs-Exporte liegen unter
  `docs/historical/chatgpt/`. Sie sind historisches Rohmaterial, keine
  kuratierte Projektdokumentation.

## Code

Der kanonische Paketkern liegt unter `src/emergenz_knoten`:

- `core.py`: `SimulationConfig`, finite-memory Simulation,
  Numba-Variante, Memory-Horizon `min(max_memory, memory_factor / alpha)`.
- `kernels.py`: exponentielle Memory-Gewichte, single/double Gaussian
  Gradienten.
- `diagnostics.py`: `D_cov`, `D_occ`, punktwolkenbasierte
  `spectral_dimension`, Residence-Statistiken, Bootstrap-CI.
- `experiments.py`: Runner und NPZ/JSON-Serialisierung.

Der sichtbare Prozess `x_n` ist wegen der History nichtmarkovsch. Der
augmentierte Zustand `z_n` aus Position und Speicher ist die natuerliche
Markov-Einbettung. Diese Einsicht ist der wichtigste Anschluss fuer Paper 0
und die naechste Implementationsschicht. In den Papers wird diese Schicht
jetzt als Markov-/Koopman-Operator auf Observablen von `z_n` formuliert; die
zugehoerige numerische Operatorpipeline ist aber noch nicht implementiert.
Die konsolidierte Priorisierung steht in `docs/project_priorities.md`.

## Experimente und Daten

Wichtige Entry-Points:

- `experiments/reference_experiment.py`
- `experiments/cli.py`
- `experiments/fractal_analysis/reproduce_dimension_pilot.py`
- `experiments/fractal_analysis/analyze_dimension_claim.py`
- historische High-N-Regime-Skripte unter `experiments/legacy/scripts/`

Kuratierte Ergebnisdaten liegen unter `data/processed/`, besonders:

- `fractal_analysis/`: Dimension-Claim-Audit, Reproduktionspiloten,
  Alpha-Sweep-Smokes.
- `highN_regime/`: Validierungs- und Ensemble-Laeufe fuer Legacy-Regime.
- `reference/`: kleine Referenzlaeufe.
- `sweep_alpha/` und `alpha/`: Alpha-Scan-Artefakte.

## Dimensionsbefund

Belastbar aus dem Archiv:

- Quelle: `experiments/fractal_analysis/Fraktale/resultsN.csv`.
- Staerkster Long-N-Gruppenbefund:
  `embedding dim = 5`, `N = 60,000,000`, fuenf Runs,
  `mean D_occ = 2.810559`, population std etwa `0.029533`.

Belastbar aus neuen Kurzlaeufen:

- Der neue reproduzierbare Pfad trifft bei `50k` und `100k` die archivierte
  Finite-Size-Skala sehr gut und bleibt bei `300k` in derselben Groessenordnung.
- Bei `N <= 60k` ist kein Near-3-`D_occ` sichtbar.
- Die ersten Negativkontrollen trennen den Claim noch nicht stark genug.

Vorsicht:

- Der Near-3-Befund ist kein einfacher `embedding dim = 3 -> D = 3`-Befund.
- Im historischen Fraktalpfad sind `alpha`, Speicher-Cap, gespeicherte
  Gewichtsmasse und effektive Kopplung konfundiert.
- Die aktuellen Diagnostiken `D_cov`, `D_occ` und `D_spec` messen verschiedene
  Dinge und duerfen nicht austauschbar formuliert werden.

## Non-Markovian Gap

Was fehlt fuer eine echte Operator-/MSM-Schiene:

- Memory-Snapshots oder Memory-Summary-Features pro Samplezeitpunkt.
- Lagged datasets.
- Zustandsdiskretisierung oder dynamische Embeddings.
- Transition Counts und Uebergangsmatrizen.
- Implied timescales, Chapman-Kolmogorov-Tests, spectral gaps.
- PCCA-/metastability-Memberships.
- HMM/PMM-Fallback, falls die Projektion auf `x_n` allein nicht markovsch ist.

## Paper-Status

- `paper/paper_i/main.tex`: Minimal Point-Process Dynamics with Memory.
  Inhaltlich aktiv; enthaelt jetzt explizite Non-Markovian/Markov-Embedding-
  Sprache, `z_n` als augmentierte Zustandsnotation und eine Operator-/
  Halbgruppenformulierung.
- `paper/paper_ii/main.tex`: Propagation Speed und Light-Cone-Dynamik.
  Struktur vorhanden; enthaelt jetzt den Anschluss an die Operator-Schicht und
  liest Lorentz-Kinematik als effektive Stabilisatorstruktur des
  makroskopischen Propagationskegels. Die empirische Haertung steht weiterhin
  hinter Paper 0/I.

## Naechste technische Schritte

1. Additive `markov/`-Schicht bauen: Features, lagged data, counts,
   row-stochastic operators, implied timescales, CK-Checks, spectral gaps.
2. Paper-0-Pipeline auf diese Schicht umstellen und eine kleine
   Evidenztabelle mit Seed-, Lag- und Negativkontrollinformationen erzeugen.
3. Paper 0 mit Theoremblock, Kernelklassen und Evidenztabelle auf
   Expert-Feedback-Niveau bringen.
4. Paper I mit Paper 0 abgleichen: allgemeine Memory-Normierung,
   Markov-Einbettung, Stabilitaets-/Mass-Proxy-Sprache.
5. Reproduktionslaeufe im Millionenbereich mit Numba-faehiger Umgebung
   vorbereiten.
