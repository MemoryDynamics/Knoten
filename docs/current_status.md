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
- `markov/`: erste additive Markov-/Transferoperator-Schicht mit reduzierten
  augmentierten Features, Sample-Lag-Datasets, Transition Counts,
  row-stochastic operators, implied timescales, CK-Fehlern und einfachen
  metastability helpers.
- `anchor.py`: Kompatibilitaets-Fassade fuer fruehere Paper-0-Imports; die
  Implementierung liegt jetzt unter `markov/`.

Der sichtbare Prozess `x_n` ist wegen der History nichtmarkovsch. Der
augmentierte Zustand `z_n` aus Position und Speicher ist die natuerliche
Markov-Einbettung. Diese Schicht ist inzwischen initial im Paketkern angelegt
und wird von der Paper-0-Anchor-Pipeline genutzt. Die aktuelle Priorisierung
ist jetzt: Paper 0 als technischen Anker einfrieren, Paper I dazu
synchronisieren und parallel eine Long-Run-Metastabilitaetskampagne mit
`n >= 10^7` laufen lassen.

Wichtige Dokumente:

- `docs/project_priorities.md`
- `docs/markov_architecture.md`
- `docs/markov_requirements.md`
- `docs/long_run_metastability_plan.md`

## Experimente und Daten

Wichtige Entry-Points:

- `experiments/reference_experiment.py`
- `experiments/cli.py`
- `experiments/fractal_analysis/reproduce_dimension_pilot.py`
- `experiments/fractal_analysis/analyze_dimension_claim.py`
- `experiments/long_run_metastability.py`
- historische High-N-Regime-Skripte unter `experiments/legacy/scripts/`

Kuratierte Ergebnisdaten liegen unter `data/processed/`, besonders:

- `fractal_analysis/`: Dimension-Claim-Audit, Reproduktionspiloten,
  Alpha-Sweep-Smokes.
- `highN_regime/`: Validierungs- und Ensemble-Laeufe fuer Legacy-Regime.
- `reference/`: kleine Referenzlaeufe.
- `long_run_metastability/`: generierte Long-Run-Ausgaben nach Abschluss.
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

## Long-Run- und Operator-Gap

Was fuer eine vollwertige Paper-I-Evidenz- und Operator-/MSM-Schiene noch
fehlt:

- Long-Run-Laeufe mit `n >= 10^7`, mehreren Seeds und Negativkontrollen.
- Residence-Ratios in Einheiten von `alpha^{-1}` statt nur kurzer Trajektorienbilder.
- Vollstaendige Memory-Snapshots oder staerkere Memory-Feature-Varianten pro
  Samplezeitpunkt; die aktuelle Schicht nutzt reduzierte Summary-Features.
- Systematische Zustandsdiskretisierung jenseits einfacher Voxel.
- Lag-, Voxel- und Feature-Sensitivitaet mit Seed-Bootstrap.
- PCCA-/metastability-Memberships.
- HMM/PMM-Fallback, falls die Projektion auf reduzierte Features noch zu viel
  Gedachtnis versteckt.

## Paper-Status

- `paper/paper_0/main.tex`: mathematischer Anker bzw. moegliches Supplement.
  Es definiert die allgemeine Speicherform, beweist Markov-Einbettung und
  Pfadkontraktion und verkauft keine robuste Knotenexistenz.
- `paper/paper_i/main.tex`: Minimal Point-Process Dynamics with Memory.
  Inhaltlich aktiv; enthaelt jetzt die allgemeine Speicherform mit normierter
  `alpha`-Konvention, Non-Markovian/Markov-Embedding-Sprache, `z_n` als
  augmentierte Zustandsnotation und eine Operator-/Halbgruppenformulierung.
- `paper/paper_ii/main.tex`: Propagation Speed und Light-Cone-Dynamik.
  Struktur vorhanden; enthaelt den Anschluss an die Operator-Schicht, bleibt
  aber ein spaeteres Folgeprogramm hinter Paper 0/I.

## Naechste technische Schritte

1. Paper 0 als technischen Anker bzw. moegliches Supplement einfrieren.
2. Paper I mit Paper 0 abgleichen: allgemeine Memory-Form,
   Markov-Einbettung, Stabilitaets-/Mass-Proxy-Sprache.
3. Einen ersten echten Long-Run mit `n >= 10^7` im Hintergrund starten.
4. Nach Abschluss zuerst Laufzeit, Residence-Ratios und Voxel-Sensitivitaet
   lesen, dann `eta_zero` und `single_scale` als Negativkontrollen starten.
5. Erst danach eine belastbare Paper-I-Evidenztabelle formulieren.
