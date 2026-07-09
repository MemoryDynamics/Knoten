# Aktueller Stand

Stand: 2026-07-09.

## Repository

- Arbeitsbranch: `main`.
- Remote: `https://github.com/MemoryDynamics/Knoten`.
- Der kanonische Paketkern liegt unter `src/emergenz_knoten`.
- Die aktive Doku-Oberflaeche ist auf sieben Dokumente reduziert; historische
  Chat- und Paper-Artefakte bleiben Rohmaterial.
- Cleanup 2026-07-09: lokale ignorierte Klartext-Reviewer-Notizen wurden aus
  dem Workspace entfernt. Der getrackte Privacy-/Control-Report heisst jetzt
  `reports/privacy_and_control_plan_2026-07-08.md`.

## Codekern

- `core.py`: `SimulationConfig`, finite-memory Simulation, Numba-Variante,
  Memory-Horizon `min(max_memory, memory_factor / alpha)` und `memory_mass`/`M0`
  als getrennte Speicher-Masse.
- `kernels.py`: exponentielle Memory-Gewichte `lambda_m M0 (1-lambda_m)^k` und Gaussian-Kernelgradienten; `exponential_weights(alpha, horizon)` bleibt der `M0=1`-Wrapper.
- `diagnostics.py`: `D_cov`, historisches `D_occ`, automatische
  Occupancy-Fitfenster (`D_win`), geometrische `spectral_dimension`,
  Residence-Statistiken, Shape-/Center-Cloud-Metriken und Bootstrap-CI.
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

Epsilon-Step-Balance 2026-07-01: Bei `epsilon=0.03,0.015,0.01,0.005`
bleibt der mediane Noise/Repulsion-Quotient nahe `3.6` und die mittlere
Richtungskorrelation nahe `-0.071`. Kleineres `epsilon` allein macht den
Lauf kleiner, aber nicht glatter oder drift-dominierter.

Epsilon-Floor-Probe 2026-07-02: Bei `epsilon=0` und Nullstart friert der
Prozess exakt ein (`zero-step fraction 1.0`). Fuer positive Werte bis
`epsilon=1e-34` skalieren Noise, Drift, totaler Schritt und Radius linear mit,
waehrend `noise/drift` nahe `3.74` und `turn mean` nahe `-0.071` bleiben.
Damit ist `epsilon` in diesem Slice Symmetriebrecher und Skalenfaktor, aber
kein Glattheitsregler. Eine flexible 3D-Visualisierung zeigt entsprechend
form-aehnliche positive Epsilon-Faelle bei sehr unterschiedlichen absoluten
Skalen.

Kernel-Shape-Probe 2026-07-02: Code-Review bestaetigt, dass die Probe jetzt
denselben `double_gaussian_gradient` wie der Paketkern nutzt. In der aktuellen
Euler-Konvention wirkt `A_rep` lokal restaurierend, waehrend `A_att` diese
Skala abschwaecht. Daher bleibt `A_att=0` kompakt (`mean radius 0.225`),
waehrend `A_rep=0` deutlich diffundiert (`mean radius 6.620`). Die Baseline-
Seedvergleiche `1..5` zeigen unterschiedliche Lage/Spannweite, aber aehnliche
Schritt- und Turn-Metriken (`median step` etwa `0.110`, `turn mean` etwa
`-0.34`). Der Grundverlauf ist daher eher Regime-/Kernel-getrieben als eine
reine Seed-Kopie. Zusaetzlich liegen jetzt flexible SVGs mit panel-eigener
Skala vor; sie sind fuer Formvergleich gedacht, nicht fuer absolute Groesse.
`strong_local` und `wide_strong` reduzieren den Radius auf `0.075`, erzeugen
aber weiter keine runden Bahnen (`turn mean` etwa `-0.43`). Runde sichtbare
Trajektorien brauchen wahrscheinlich Persistenz, einen Inertialterm,
tangentiale Drift oder eine geglaettete Center-Observable.

Knotenscore v0.3 2026-07-02: Die Scorecard auf vorhandenen Long-Run-JSONs
bewertet Residence-Gain, Kompaktheit gegenueber `eta_zero`,
Voxel-Stabilitaet und interne Occupancy-Dimension `D_occ`. Baseline erzielt
`score mean 0.925`, `median 1.000`; `single_scale` erzielt ebenfalls hoch
(`mean 0.875`, `median 0.875`). `D_occ` liegt bei beiden Bedingungen um
`1.8` und dient derzeit als Nicht-Kollaps-Signal, nicht als externer
3D-Nachweis. Die Scorecard traegt Feedback-Confinement gegenueber `eta_zero`,
isoliert aber weiter keinen spezifisch zweiskaligen Baseline-Mechanismus. Neue
Long-Run-Ausgaben schreiben jetzt `sample_shape` und `memory_cloud` mit; die
archivierten 10M-JSONs enthalten diese Formmetriken noch nicht.

Shape-Pilot 1M 2026-07-02: Fuer `baseline`, `eta_zero` und `single_scale`
wurden Seeds `1..5` mit `N=1,000,000`, `burn-in=100,000` und
`sample_every=200` neu geschrieben. Der Report
`reports/knot_score_v0_3_shape_pilot_1M_2026-07-02.md` zeigt: Der rohe
Sample-Pfad bleibt bei allen Bedingungen eher zweidimensional/elongiert
(`sample roundness median ~0.32`). Die aktive Memory-Cloud von `baseline` und
`single_scale` ist dagegen kompakt und deutlich runder (`memory roundness
median ~0.64`, `memory dimension median ~2.68`, `memory radius median ~0.10`).
`eta_zero` hat eine viel groessere Sample-Ausdehnung (`radius median ~16.1`)
und eine weniger runde, niedriger dimensionale Memory-Cloud (`roundness median
~0.33`, `dimension median ~1.64`). Damit spricht der Pilot klar dafuer, die
Knotenform ueber die Memory-Cloud statt ueber den rohen Pfad zu bewerten.

Knotenscore v0.4 2026-07-02: `reports/knot_score_v0_4_shape_pilot_1M_2026-07-02.md`
erweitert v0.3 um Memory-Cloud-Kompaktheit, Memory-Cloud-Rundheits-Gain und
Memory-Cloud-Formdimensions-Gain gegenueber dem seedgleichen `eta_zero`.
Baseline erreicht im 1M-Shape-Pilot `score median 0.929`, `single_scale`
`median 0.857`. Beide aktiven Bedingungen trennen sich damit klar von
`eta_zero` in Residence, Kompaktheit und Memory-Cloud-Shape. Baseline bleibt
gegenueber `single_scale` aber nicht isoliert; der Befund stuetzt also weiter
Feedback-Confinement, noch keinen spezifisch zweiskaligen Mechanismus.

Knotenscore v0.4 mit Seeds `1..15` 2026-07-07: Die 1M-Auswertung liefert fuer
`baseline` und `single_scale` jeweils `score median 0.857`; die 100M-Auswertung
liefert fuer beide `score median 1.000`. Auch Memory-Cloud-Radius,
Memory-Rundheit und Memory-Formdimension bleiben praktisch deckungsgleich. Der
Befund wird damit robuster, aber enger: Der aktive Kernel erzeugt stabile
Memory-Cloud-Confinement-Regime gegenueber `eta_zero`, der zweiskalige Anteil
ist in diesem Parameterschnitt aber nicht als notwendig nachweisbar. Der
100M-Quellsatz liegt in einem `10M` benannten Ordner, enthaelt aber
`steps=100000000` und wurde laut `summary.json` mit dirty Worktree erzeugt.

Knotenscore v0.5 mit 100M-Kontrollen 2026-07-08: `reports/knot_score_v0_5_controls_100M_2026-07-08.md`
verwendet raw update counts fuer Residence und wertet Memory-Kompaktheit nur
bei nichtdegenerierter Memory-Cloud. Ergebnis: `baseline` und `single_scale`
bleiben hoch (`score median 1.000`, `score mean 0.948`), waehrend `m0_zero`
und `alpha_one` seedgleich niedrig liegen (`score median 0.286`, Residence-
Gain `1.000`, Compactness-Gain `1.000`). Der Score korrigiert damit den
cross-alpha-Artefakt der v0.4-Memory-Zeit-Skalierung und bestaetigt: aktives
Memory-Feedback erzeugt Confinement, der zweiskalige Baseline-Kernel ist in
diesem Slice nicht isoliert.

Ballistik-/Photon-Pilot 2026-07-07: Die korrigierte skalare Ein-Kernel-Probe
nutzt die Memory-Relaxation `lambda` tatsaechlich als Exponentialgewicht und
fuer den selbstabstossenden Test das Drift-Vorzeichen `+ eta * grad`. Trotzdem
zeigt der Sweep keine ballistische MSD-Skalierung: deterministische Faelle
relaxieren bzw. stagnieren, rauschgetriebene Faelle liegen bei maximaler
MSD-Slope etwa `1.138`, weit unter dem ballistischen Zielwert `2`. Das stuetzt
die Einschaetzung, dass ein skalares overdamped Memory-Modell allein keinen
harmonischen Oszillator oder photonartigen Modus traegt.

Alpha-/M0-Korrektur 2026-07-08: Die allgemeine Memory-Form wird im Paketkern
jetzt als `rho[n+1]=(1-lambda_m)rho[n]+lambda_m M0 G_sigma` abgebildet.
Der alte Spezialfall `beta=lambda_m=alpha` ist `M0=1`. Die Ballistikprobe
verwendet nun `eta_c=lambda_m/((1-lambda_m)M0 a0)` statt `gamma_c` als rohe
Eta-Schwelle. Konsequenz: Alpha-Scans muessen `lambda_m`, gespeicherte Masse
`M0=beta/lambda_m`, Tail-Cutoff und effektive Kopplung getrennt berichten;
weitere Blindscans sind weniger wertvoll als die geplante Block-Markov-/AR-
Reanalyse vorhandener Long-Runs auf reelle versus komplexe langsame Moden.


Privacy-/Provenance-Notiz 2026-07-09: Personenbezogene Review-Klartexte
gehoeren nicht in den getrackten Public-Repo-Stand. Die lokalen ignorierten
Klartextnotizen wurden entfernt; die oeffentliche Spur ist eine sanitisierte
Policy-/Control-Notiz. Neue Long-Run-JSONs protokollieren weiter `git_status`.

Long-Run-Kontrollen 2026-07-08: `experiments/long_run_metastability.py` kennt
nun `m0_zero` (`memory_mass=0`) und `alpha_one` (`alpha=1`). `m0_zero` ist die
saubere Null-Feld-Kontrolle, `alpha_one` ist der Ein-Schritt-Memory-Grenzfall.
Der 100M-Lauf mit Seeds `1..10` ist abgeschlossen: `m0_zero` und `alpha_one`
liefern seedweise identische Trajektorienmetriken (`D_occ` mean `1.819`, mean
radius `212.678`, mediane beste Residence `8000` Updates). Lesart: bei
`symmetric self-memory` verschwindet der Selbstgradient fuer `alpha=1`; der
Grenzfall ist daher eine Negativkontrolle, kein Knotenregime. Report:
`reports/long_run_m0_alpha_one_results_2026-07-08.md`.

Deposition-Kernel-Audit 2026-07-08: Der Paketkern speichert Punktdepositionen
und berechnet die Kraft als Summe ueber `grad K(x-x_k)`. Das ist numerisch
bereits `G=delta`; `sigma_rep` und `sigma_att` sind effektive Interaktions-
laengen, keine separate Depositionsbreite. Report:
`reports/deposition_kernel_audit_2026-07-08.md`.

Matched-Deposition-Update 2026-07-08: Der Code kennt jetzt `delta`, `gaussian`
und `matched_gaussian`. Die Condition `matched_deposition` verwendet eine
positive, normalisierte Gauss-Deposition mit derselben Breite wie die jeweilige
Lesekomponente und rechnet sie als effektiven Faltungskernel aus. Der 100k-
Slow-Python-Pilot trennt weiter klar von `eta_zero`, ist aber schwaecher als
die Delta-Baseline (`score median 0.714` vs. `0.857`, Memory-Radius `0.244`
vs. `0.097`). Lesart: Matching allein erzeugt nicht sofort staerkere Knoten,
weil die normierte Faltung in `d=3` die lokale Steifigkeit um etwa Faktor
`5.66` reduziert. Naechster fairer Test ist eine curvature-renormalized
matched condition, nicht direkt ein 100M-Lauf. Reports:
`reports/matched_deposition_kernel_pilot_2026-07-08.md` und
`reports/knot_score_v0_5_matched_deposition_100k_2026-07-08.md`.

Zero-Mean-Kernel-Notiz 2026-07-09: Die neue Condition `zero_mean_two_scale`
setzt `A_att = A_rep (sigma_rep/sigma_att)^d` und erzwingt damit `int K = 0`
fuer den unnormalisierten zweiskaligen Kernel. Der alte Baseline-Slice
`L_att=3`, `A_att=0.35` war nicht kompensiert; ein erster fairer Test ist
`sigma_att=1.5`, wo `A_att=0.296` gilt. Report:
`reports/zero_mean_kernel_decision_2026-07-09.md`.

Entscheidungsnotiz 2026-07-07: `reports/kernel_memory_photon_decision_2026-07-07.md`
fasst die aktuelle Linie zusammen. Paper I sollte den Mechanismus als
effektives Memory-Kernel-Confinement formulieren. Zwei-Skalen-Kernel bleiben
optionale Erweiterung, nicht Kernclaim. Photon-/Oszillatorfragen brauchen einen
separaten erweiterten Zustand, etwa Velocity-, Phasen- oder Vektormemory.

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

1. Paper-I-Claim-Sprache auf Feedback-Confinement gegenueber `eta_zero`
   zuschneiden; keinen notwendigen zweiskaligen Baseline-Mechanismus behaupten.
2. `amplitude_rep = 0` weiter als echte Dispersionsablation nutzen, aber nicht
   zur Rettung des zweiskaligen Claims, sondern zur Klaerung, ob ein einzelner
   restaurierender Kernel fuer Paper I genuegt.
3. Photon-/Ballistik-Track getrennt halten: erst ein dimensionsloses
   oszillierendes oder ballistisches Regime in einem erweiterten Modell zeigen,
   dann mit `hbar nu`, `mc^2` oder grossen/kleinen Zahlen skalieren.
4. Falls sichtbar runde Bahnen ein eigenes Ziel bleiben: erst einen kleinen
   Persistenz-/Inertial-Pilot definieren, statt weitere Kernelparameter blind
   nach optischer Rundheit zu durchsuchen.
5. Dimension-Reproduction bleibt Reconciliation-Aufgabe, nicht Blindscan.
6. Transferoperatorfeatures fuer Long-Run-Daten erweitern, sobald das
   Knotenkriterium stabil ist.
