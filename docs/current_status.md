# Aktueller Stand

Stand: 2026-07-01.

## Repository

- Arbeitsbranch: `main`.
- Remote: `https://github.com/MemoryDynamics/Knoten`.
- Der kanonische Paketkern liegt unter `src/emergenz_knoten`.
- Die aktive Doku-Oberflaeche ist auf sieben Dokumente reduziert; historische
  Chat- und Paper-Artefakte bleiben Rohmaterial.

## Codekern

- `core.py`: `SimulationConfig`, finite-memory Simulation, Numba-Variante,
  Memory-Horizon `min(max_memory, memory_factor / alpha)`.
- `kernels.py`: exponentielle Memory-Gewichte und Gaussian-Kernelgradienten.
- `diagnostics.py`: `D_cov`, historisches `D_occ`, automatische
  Occupancy-Fitfenster (`D_win`), geometrische `spectral_dimension`,
  Residence-Statistiken und Bootstrap-CI.
- `experiments.py`: Runner und NPZ/JSON-Serialisierung.
- `markov/`: additive Markov-/Transferoperator-Schicht mit reduzierten
  augmentierten Features, Lagged Datasets, Transition Counts,
  row-stochastic operators, implied timescales, CK-Fehlern und slow-mode
  Helfern.
- `anchor.py`: Kompatibilitaets-Fassade fuer fruehere Paper-0-Imports.

Der sichtbare Prozess `x_n` ist wegen des Speichers im Allgemeinen
nichtmarkovsch. Der augmentierte Zustand `z_n=(x_n,rho_n)` bzw. eine konkrete
Memory-Reprasentation ist die Markov-Einbettung.

## Paper-Status

- Paper 0: mathematischer Anker bzw. moegliches Supplement. Es formuliert die
  allgemeine Memory-Form `(1-lambda_m)rho_n + beta G_sigma`, die
  Markov-Einbettung und die kontraktive Memory-Faser. Es behauptet keine
  robuste Knotenexistenz.
- Paper I: Minimalmodell mit synchronisierter Memory- und Markov-Sprache. Die
  starke Knoten-Evidenz muss aus Long-Runs und Kontrollen kommen.
- Paper II: Propagation, `c_eff` und Raumzeit-Kinematik bleiben Folgeprogramm.
- Paper III: als Innen/Aussen- und Synchronisationsprogramm neu orientiert;
  QFT-/Standardmodellbruecken bleiben als offene Future-Work-Tuer erhalten,
  aber ohne Claim-Status.

## Long-Run-Status

Der Kontrollreport vom 2026-07-01 fuehrt die vorhandenen fuenf Seeds fuer
`baseline`, `eta_zero` und `single_scale` zusammen.

| Condition | Best residence mean +/- SD in `alpha^{-1}` | Mean centered radius | Lesart |
| --- | ---: | ---: | --- |
| `baseline` | `437.6 +/- 323.1` | `3.880` | kompakt und langlebig, aber seed-variabel |
| `eta_zero` | `80.0 +/- 12.2` | `57.284` | echte Negativkontrolle, diffundiert weit |
| `single_scale` | `697.7 +/- 534.6` | `3.734` | keine Negativkontrolle, sondern starke Kernel-Ablation |

Lesart: Memory-Gradient-Feedback erzeugt in diesem Slice kompakte
Long-Residence-Regime relativ zu `eta_zero`. Der zweiskalige Baseline-Kernel
ist dadurch aber noch nicht als notwendiger Mechanismus isoliert, weil
`single_scale` ebenfalls kompakt und oft noch langlebiger ist. `D_cov` und
`D_occ` trennen die Bedingungen in diesem Kontrollsatz nicht zuverlaessig.

Konsequenz fuer Paper I: tragbar ist derzeit ein vorsichtiger Befund zu
self-interaction-induced confinement gegenueber `eta_zero`. Noch nicht tragbar
ist ein starker Claim eines spezifisch zweiskaligen stabilen Knotenmechanismus.

## Dimensionsbefund

Belastbar aus dem Archiv:

- Quelle: `experiments/fractal_analysis/Fraktale/resultsN.csv`.
- Staerkster Long-N-Gruppenbefund: `embedding dim = 5`, `N = 60,000,000`,
  fuenf Runs, `mean D_occ = 2.810559`, population std etwa `0.029533`.

Belastbar aus den neuen kontrollierten Reproduktionslaeufen vom 2026-07-01:

- Die allgemeine Memory-Variante ist technisch umgesetzt:
  `rho_{n+1}=(1-lambda_m)rho_n+beta G_sigma`, mit altem Spezialfall
  `beta=lambda_m=alpha`.
- Kernel-Skalen-, Memory-Zeit- und Memory-Masse-Scans sind abgeschlossen und
  reportgebunden committed.
- Der einzelne High-N-Referenzlauf `d=5`, `N=100,000,000`, `alpha=0.01`,
  `beta/alpha=1`, `sigma_att=0.15`, Seed `1`, liefert `D_occ=2.013`,
  automatisches Fenster `D_win=2.098`, `D_cov=1.337`, `D_spec=1.210`.
- Bei `N=1,000,000`, Seeds `1..5`, zeigt keine getestete Achse ein stabiles
  Plateau nahe `D=3`. Die groessten historischen `D_occ`-Mittelwerte liegen
  unter `1.6`; die automatischen Fensterwerte `D_win` liegen meist eher um
  `2..2.5`.
- Niedrigeres `beta/alpha` kann in dieser Pipeline `D_occ` erhoehen, erzeugt
  aber keine robuste Dreidimensionalitaet.

Lesart: Der archivierte Near-3-Befund bleibt als historischer/high-N-Befund
interessant, ist aber nicht durch die aktuelle kontrollierte Reproduktions-
pipeline bestaetigt. Die neue `D_win`-Diagnostik zeigt, dass Fitfensterwahl
eine zentrale Fehlerquelle war. Fuer Paper I/II darf daraus kein `d=3`-Selektionsclaim
abgeleitet werden. Der naechste wissenschaftliche Schritt ist Reconciliation:
Parameterdefinitionen, Schaetzfenster, Sampling, historische Skripte und
Negativkontrollen gegeneinander pruefen.

## Naechste technische Schritte

1. Strengeres Knotenkriterium v0.2 definieren: Residence, Kompaktheit,
   Voxel-Stabilitaet und Trennung von `eta_zero` gemeinsam bewerten.
2. Long-Run-Ausgabe um reduzierte Center-/Shape-Stabilitaetsmetriken erweitern,
   damit kuenftige Laeufe echte Lokalisierung besser von Voxel-Residence
   unterscheiden.
3. Erst danach weitere einparametrige Kernel-Ablationen starten, z.B.
   `amplitude_rep = 0`, um die Rolle der einzelnen Kernelkomponenten zu klaeren.
4. Paper-I-Evidenztabelle erst formulieren, wenn das Knotenkriterium und die
   naechsten Ablationen die gewaehlte Claim-Sprache tragen.
5. Dimension-Reproduction bleibt Reconciliation-Aufgabe, nicht Blindscan.
6. Transferoperatorfeatures fuer Long-Run-Daten erweitern, sobald das
   Knotenkriterium stabil ist.
