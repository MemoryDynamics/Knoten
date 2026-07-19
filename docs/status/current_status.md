# Aktueller Stand

Stand: 2026-07-19.

## Repository

- Arbeitsbranch: `main`.
- Remote: `https://github.com/MemoryDynamics/Knoten`.
- Der kanonische Paketkern liegt unter `src/emergenz_knoten`.
- Die aktive Doku-Oberflaeche ist auf sieben Dokumente reduziert; historische
  Chat- und Paper-Artefakte bleiben Rohmaterial.
- Cleanup 2026-07-09: lokale ignorierte Klartext-Reviewer-Notizen wurden aus
  dem Workspace entfernt. Der getrackte Privacy-/Control-Report heisst jetzt
  `reports/project/governance/privacy_and_control_plan_2026-07-08.md`.

## Codekern

- `core.py`: `SimulationConfig`, finite-memory Simulation, Numba-Variante,
  Memory-Horizon `min(max_memory, memory_factor / alpha)`, `memory_mass`/`M0`
  sowie ein ringgepufferter Finalzustands-Runner ohne Trajektorienspeicherung.
- `kernels.py`: exponentielle Memory-Gewichte `lambda_m M0 (1-lambda_m)^k`
  sowie konsistente Gaussian-Potential- und Gradient-APIs; `exponential_weights(alpha, horizon)` bleibt der `M0=1`-Wrapper.
- `analytic.py`: dimensionslose Skalarkontrollen, lokale Moden und getestete
  stationaere RMS-Formel fuer den linearen Memory-Relativmodus.
- `field.py`: exakte Gaussian/Heat-Transferidentitaet und getrennte
  Relaxations-Diffusionsfeld-Bruecke.
- `spectral_memory_field.py`/`spectral_memory_runtime.py`: periodische 1D-
  Fourier-Reprasentation desselben exponentiellen Memory mit gecachten O(M)-
  Operatoren; bei 64 Moden belegt ein Feldzustand 1040 Bytes.
- `relaxation_diffusion_memory.py`: kontrollierte modeabhaengige Felddynamik;
  `nu=0` ist bitgenau die bisherige Memory-Dynamik.
- `diagnostics.py`: `D_cov`, historisches `D_occ`, automatische
  Occupancy-Fitfenster (`D_win`), geometrische `spectral_dimension`,
  voxelbasierte Residence-Statistiken, neue Center-/Memory-Ball-Residence, Shape-/Center-Cloud-Metriken und Bootstrap-CI.
- `experiments.py`: Runner und NPZ/JSON-Serialisierung.
- `knot_score.py`: Scorecard-Helfer v0.3-v0.5 fuer Residence, Kompaktheit, Voxelstabilitaet, interne Dimension und Memory-Cloud-Form.
- `vector_memory.py`: erster orientierter Memory-Kanal mit `eta_vector=0`/`vector_mass=0`-Rueckfallkontrollen, Sample-Features und 2D-Transverse-Pilotmodus.
- `state.py`: unveraenderlicher vollstaendiger Finite-Memory-Zustand sowie
  gemeinsame Translation und orthogonale Platzierung von Position und Memory.
- `checkpoints.py`: versionierte, pickle-freie NPZ-Checkpoints mit vollstaendiger
  Finite-Memory-Pruefung, Formation-Provenienz und SHA-256-Arraypruefsummen.
- `weak_probe.py`/`synchronization.py`: gepaarte uniforme Probeantwort mit
  gemeinsamem Zukunftsrauschen, ungeprobtem Pfad, Response-Matrizen und exakter
  Seed-Signflip-Ranginferenz.
- `frozen_source.py`: lokalisierte eingefrorene Quellfelder mit getrennter
  Selbst-/Kreuzkopplung, gepaarten Quelllagen, freiem Pfad und exakter
  Null-Kreuzkopplungskontrolle; Kreuzkopplung kann auf die anfaengliche
  Richtungsdrift oder die realisierte Common-Noise-Bare-Antwort kalibriert werden.
- `markov/`: additive Markov-/Transferoperator-Schicht mit reduzierten
  augmentierten Features, Lagged Datasets, Transition Counts,
  row-stochastic operators, implied timescales, CK-Fehlern und slow-mode
  Helfern.
- `anchor.py`: Kompatibilitaets-Fassade fuer fruehere Paper-0-Imports.

Der sichtbare Prozess `x_n` ist wegen des Speichers im Allgemeinen
nichtmarkovsch. Der augmentierte Zustand `z_n=(x_n,rho_n)` bzw. eine konkrete
Memory-Reprasentation ist die Markov-Einbettung.

Sign-Konvention 2026-07-09: Der Kernelgradient wurde korrigiert. `gaussian_gradient`
ist jetzt der echte Gradient eines positiven Gauss-Potentials; `A_rep` ist im
Update `x <- x - eta grad` lokal repulsiv, `A_att` breit attraktiv. Fruehe
Confinement-Reports bleiben `legacy-sign`-Auditmaterial; korrigierte
Long-Run-, Ablations- und Linearitaetstests liegen inzwischen vor. Report:
`reports/kernels/corrected_sign/kernel_sign_convention_correction_2026-07-09.md`.

## Aktueller Skalarbefund

Der direkte Vergleich von attraktivem Ein-Kernel und zweiskaligem q=3-Kernel
ist abgeschlossen. Bei `A_rep=1`, `sigma_rep=1`, `sigma_att=3` gilt fuer
lokal curvature-matched Kurven exakt `A_eff=A_att-9`; nach dieser
Reparametrisierung stimmen sechs seedweise KPIs bis hoechstens `6.4e-6`
relativ ueberein. Die alte Driftgrenze um `7.9` aus dem rauschstaerkeren
Zweiskalen-Slice ist keine universelle Ein-Kernel-Schwelle bei sechs.

Neun vorhandene aktive `N=30M/300M`-Slices folgen dem endlichen-Memory-
Relativmodus mit `0.76%` medianem und `1.16%` maximalem Radiusfehler. Im
vorregistrierten festen-`g`-Test ueber `R_linear/L={0.03,0.1,0.3}` waechst
der Radius in allen fuenf Seeds glatt etwa `6.2%` staerker als linear; `D_mem`
und Roundness bleiben stabil. Die formale Entscheidung bleibt
`inconclusive`, weil KnotScore und feste-Voxel-Residence sinken. Die getrennte
Skalenpruefung zeigt jedoch: feste Voxel aendern ihre relative Groesse stark,
waehrend co-moving Residence auch fuer `eta=0` gesaettigt und damit nicht
diskriminierend ist. Das traegt eine schwache glatte Kernelkorrektur, keinen
isolierten metastabilen Skalarast. Naechster Modellzweig ist das dynamische
Relaxations-Diffusionsfeld mit eigenem Zustand und Kontrollen.

Reports:
`reports/kernels/core/kernel_family_comparison_d3_N300k_2026-07-19.md`,
`reports/long_runs/scalar_hardening/linear_long_run_reconciliation_2026-07-19.md`,
`reports/kernels/nonlinearity/fixed_g_RL_d3_N300k_A26_2026-07-19.md` und
`reports/kernels/nonlinearity/fixed_g_scale_reconciliation_d3_N300k_A26_2026-07-19.md`.

## Memory-Feld-Gate 2026-07-19

Die spektrale `rho`-Schicht ist zunaechst nur eine Reparametrisierung des
bestehenden exponentiellen Punktgedaechtnisses. Historienausrollung,
pfadweise Kontraktion, Massenerhalt, direkter Gausskraftvergleich und
`eta=0`-Replay sind getestet. Im Fuenf-Seed-Slice fuer
`epsilon in {1e-8,1e-6,1e-4}` ist der aktive relative Radius etwa `0.174` der
seedgleichen Kontrolle, skaliert aber mit Steigung `1.00000000008` exakt
proportional zu epsilon. `32/64/128` Moden liefern denselben dynamischen Radius
bis etwa `1.6e-14` relativ. Kleinere epsilon-Werte erschliessen hier keine neue
intrinsische Laenge und werden nicht weiter gescannt.

Die getrennte Relaxations-Diffusionsextension verwendet pro Mode
`exp(-nu k^2)`. Bei einer Diffusions-RMS-Laenge pro Memory-Zeit von
`0`, `0.3 L`, `1.0 L` steigt der aktive Medianradius von `1.199e-4` auf
`1.660e-4`; active/control steigt glatt von `0.171` auf `0.240`, waehrend der
Feedback-Schritt pro epsilon von `0.507` auf `0.311` sinkt. Gleichzeitig
reduziert die Diffusion die negative Masse der trunkierten Delta-
Rekonstruktion von `0.980` auf `8.42e-4`. Das ist ein sauberer Feldglaettungs-
befund, aber weder Metastabilitaet noch Propagation oder ein neuer Modus.

Reports:
`reports/memory/spectral_rho_field_pilot_2026-07-19.md` und
`reports/memory/relaxation_diffusion_field_pilot_2026-07-19.md`.

Naechster Schritt ist eine seedgepaarte Low-Mode-/AR-Feature-Closure fuer die
vorab festgelegten Diffusionsarme gegen `nu=0` und `eta=0`, gefolgt von Box-
und Modenzahlsensitivitaet. Ein Long Run folgt nur bei einer neuen
kontrollgetrennten Zeitskala.
## Paper-Status

- Paper 0: mathematischer Anker bzw. moegliches Supplement. Es formuliert die
  allgemeine Memory-Form `(1-lambda_m)rho_n + beta G_sigma`, die
  Markov-Einbettung und die kontraktive Memory-Faser. Es behauptet keine
  robuste Knotenexistenz.
- Paper I: Minimalmodell mit synchronisierter Memory- und Markov-Sprache.
  Der aktuelle kleine-Radius-Ast traegt als linearer co-moving
  Relaxationsbefund; nichtlineare Metastabilitaet ist noch nicht isoliert.
- Paper II: Propagation, `c_eff` und Raumzeit-Kinematik bleiben Folgeprogramm.
- Paper III: als Innen/Aussen- und Synchronisationsprogramm neu orientiert;
  QFT-/Standardmodellbruecken bleiben als offene Future-Work-Tuer erhalten,
  aber ohne Claim-Status.

## Aktueller Dimensions-/A_att-Befund

Die folgenden A_att- und Dimensionsdaten bleiben reproduzierbare Beobachtungen,
werden nach dem Linearitaetsaudit aber defensiver gelesen: Shape nahe der
Ambient-Dimension ist im isotropen Relativmodus zu erwarten.

A_att-Transition 2026-07-15: Ein gematchter `N=10M`-Vergleich ueber Seeds
`1..5` fuer `d=3` und `d=10` wurde fuer den korrigierten q=3-Skalarslice
(`epsilon=1e-4`, `M0=1`, Delta-Deposition) ausgewertet. Report:
`reports/long_runs/scalar_hardening/aatt_transition_d3_d10_2026-07-15.md`.

- Die fehlende Report-Referenz fuer `beta=0` ist geschlossen: im Code ist das
  die `M0=0`/`m0_zero`-Kontrolle, dokumentiert in
  `reports/long_runs/scalar_hardening/d10_memory_controls_2026-07-14.md`.
- In `d=10` liegt der kompakte Ast ab `A_att>=9` bei `D_cov ~=2.52`, waehrend
  `D_mem` von `2.49` bis `9.16` weiter ansteigt. Das spricht fuer eine
  Trennung von sichtbarer Sample-Geometrie und interner Memory-Shape, nicht
  fuer eine einzelne Dimensionszahl.
- In `d=3` laeuft `D_mem` bei `A_att=35` auf `2.95` gegen die Einbettungsgrenze,
  waehrend die rohe Ein-Knoten-Spur bei `D_cov ~=1.8` und `D_occ_win ~=1.9`
  bleibt. Ein einzelner driftender Knoten muss die externen Richtungen nicht
  isotrop abtasten.
- `D_spec` ist aktuell eine Point-Cloud-Diffusions-/Spektralgeometrie, kein FFT-
  Fenster und kein Transferoperatorspektrum. Der Sensitivitaetsreport vom
  2026-07-15 zeigt, dass `D_spec memory ~=3` nur ein Hypothesenhinweis ist:
  Bandwidth und kNN-Skala bewegen Kovarianz-Surrogate um order-one Betraege.
  Der Rohsnapshot-Pilot (`N=200k`, `d=3/10`, Seeds 1-3) validiert den echten
  Snapshot-Auswertepfad, reproduziert aber noch kein robustes Heat-Trace-Nahe-3-
  Signal. Der laengere Rohsnapshot-Retest (`N=3M`, `d=3/10`, Seeds 1-5)
  bestaetigt diese Trennung: `d=3` bleibt shape-nahe-drei, aber Heat-Trace
  liegt deutlich darunter; `d=10`-Baseline bleibt shape-hochdimensional ohne
  akzeptiertes Heat-Trace-Skalierungsfenster.
- 3D-Audit 2026-07-15: `D_p90`/`D_p95` bestaetigen, dass die interne
  Memory-Varianz in hohen Einbettungen nicht auf drei Achsen kollabiert.
  Der lokale d=3-Memory-Shape-Wert ist nun eine lineare
  Ambient-Shape-Kontrolle, kein Paper-I-Teaser. Paper II braucht
  relationale oder ambient-unabhaengige Dimensionsobservablen.
  Reports: `reports/dimensions/dimension_claim_audit_2026-07-15.md`,
  `reports/dimensions/dspec_sensitivity_2026-07-15.md`,
  `reports/dimensions/dspec_raw_snapshot_2026-07-15.md`,
  `reports/dimensions/dspec_raw_snapshot_retest_2026-07-16.md`.
- Uniformer Weak-Probe-Pilot 2026-07-16: Vollstaendige `N=3M`-Snapshots fuer
  `d=3/10`, Seeds `1..5`, wurden fuer `0.03` und `0.10` Memory-Radien gepaart
  perturbiert. Die Bare-Position reproduziert `I_d` bis `4.7e-12`; die
  kontrollsubtrahierte Memory-Zentrumantwort ist isotrop vollrangig (`3` bzw.
  `10`), waehrend die Formantwort keinen seed-reproduzierbaren Signflip-Rang
  besitzt. Das ist eine uniforme Vollrang-Negativkontrolle, kein externer
  Dimensionsbefund. Report:
  `reports/response/weak_probe_calibration_2026-07-16.md`.
- Referenzzustands-Checkpoints 2026-07-16: Die kanonischen
  Entwicklungszustaende fuer `N=1e8`, Seed 1 und `d=3/10` sind auf Revision
  `e8f4af2` gebildet, checksum-validiert und mit exakt reproduzierbarem
  Branch-Replay gespeichert. `d=3` endet bei `D_mem=2.860`, `d=10` bei
  `D_mem=9.431`; der einzelne d10-Zustand zeigt damit keinen internen
  Drei-Dimensions-Kollaps. Alle Folgearme starten mit neuem explizitem
  gemeinsamen Zukunftsrauschen; der PRNG-Zustand ist kein Bestandteil von
  `z_N`. Vollstaendigkeit bezieht sich auf den trunkierten 600-Punkte-Puffer
  (`M_stored=0.997595`), nicht auf den formal unendlichen Schwanz. Report:
  `reports/reference_states/scalar_reference_checkpoints_N100M_2026-07-16.md`.

- Frozen-Source-Pilot 2026-07-16: Die beiden kanonischen `N=1e8`-
  Checkpoints wurden als Target und starr eingefrorene geklonte Quelle bei
  einem Abstand von `1 sigma_rep` fortgesetzt. `eta_cross=0` ist bitgenau
  null; die Bare-Kalibrierung trifft `0.03` Target-Radien pro Memory-Zeit,
  und die Jacobi-Matrizen fuer `delta/sigma_rep=0.03/0.10` stimmen relativ
  auf besser als `7.3e-4` ueberein. Die Center-Antwort ist jedoch jeweils
  voll ambient-rangig (`3` bzw. `10`) und zerfaellt in einen radialen sowie
  `d-1` nahezu entartete transversale Kanaele (`|J_parallel/J_perp| ~=1.063`).
  Das ist die erwartete Symmetrie des isotropen skalaren Fernfeldkernels,
  keine externe 3D-Selektion. Report:
  `reports/response/frozen_source_pilot_2026-07-16.md`.

- Frozen-Source-Feld- und Distanzpruefung 2026-07-17: Der reale
  Checkpoint-Feldverlauf stimmt von `5 R_mem` bis `1 sigma_rep` praktisch mit
  einem Punktmonopol ueberein. Beim aktuellen `A_att=35`-Kern gibt es weder
  analytisch noch richtungsweise einen Kraftvorzeichenwechsel; alle geprueften
  Richtungen sind attraktiv. Die Distanzleiter trifft die realisierte Bare-
  Verschiebung von `0.03 R_mem` auf etwa `1e-4` relativ und behaelt in `d=3`
  und `d=10` vollen Ambient-Rang. Die groesste normierte Target-Deformation
  bleibt unter `0.002`. Das ist ein vorzeichenloser skalarer, mass-like
  Kreuzkanal und kein Neutralitaets-, Ladungs-, Reziprozitaets- oder 3D-Claim.
  Reports: `reports/response/frozen_source_field_audit_2026-07-17.md` und
  `reports/response/frozen_source_distance_ladder_2026-07-17.md`.

## Long-Run-Status

Die folgenden Long-Run-Befunde bis einschliesslich Force-Komponenten-Pilot vom
2026-07-09 sind `legacy-sign`-Befunde. Sie erklaeren die Historie und den
Vorzeichenfund, ersetzen aber nicht den korrigierten Retest.

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

Kernel-Shape-Probe 2026-07-02 (`legacy-sign`): Code-Review bestaetigte,
dass die Probe denselben `double_gaussian_gradient` wie der damalige
Paketkern nutzte. Unter der alten Vorzeichenkonvention wirkte `A_rep` lokal
restaurierend und `A_att` als breiter Gegenkanal; deshalb blieb `A_att=0`
kompakt (`mean radius 0.225`), waehrend `A_rep=0` diffundierte (`mean radius
6.620`). Diese Zahlen erklaeren den Vorzeichenfund, sind aber keine Evidenz
fuer das korrigierte Potentialmodell. Die Baseline-Seedvergleiche `1..5`
zeigen trotzdem eine nuetzliche methodische Lektion: unterschiedliche Lage/
Spannweite, aber aehnliche Schritt- und Turn-Metriken. Die Shape-Frage muss
nach der Korrektur neu getestet werden.

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
`reports/knot_scores/v0_2_to_v0_4/knot_score_v0_3_shape_pilot_1M_2026-07-02.md` zeigt: Der rohe
Sample-Pfad bleibt bei allen Bedingungen eher zweidimensional/elongiert
(`sample roundness median ~0.32`). Die aktive Memory-Cloud von `baseline` und
`single_scale` ist dagegen kompakt und deutlich runder (`memory roundness
median ~0.64`, `memory dimension median ~2.68`, `memory radius median ~0.10`).
`eta_zero` hat eine viel groessere Sample-Ausdehnung (`radius median ~16.1`)
und eine weniger runde, niedriger dimensionale Memory-Cloud (`roundness median
~0.33`, `dimension median ~1.64`). Damit spricht der Pilot klar dafuer, die
Knotenform ueber die Memory-Cloud statt ueber den rohen Pfad zu bewerten.

Knotenscore v0.4 2026-07-02: `reports/knot_scores/v0_2_to_v0_4/knot_score_v0_4_shape_pilot_1M_2026-07-02.md`
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

Knotenscore v0.5 mit 100M-Kontrollen 2026-07-08: `reports/knot_scores/v0_5_controls/knot_score_v0_5_controls_100M_2026-07-08.md`
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

Long-Run-Kontrollen 2026-07-08: `experiments/current/dynamics/long_run_metastability.py` kennt
nun `m0_zero` (`memory_mass=0`) und `alpha_one` (`alpha=1`). `m0_zero` ist die
saubere Null-Feld-Kontrolle, `alpha_one` ist der Ein-Schritt-Memory-Grenzfall.
Der 100M-Lauf mit Seeds `1..10` ist abgeschlossen: `m0_zero` und `alpha_one`
liefern seedweise identische Trajektorienmetriken (`D_occ` mean `1.819`, mean
radius `212.678`, mediane beste Residence `8000` Updates). Lesart: bei
`symmetric self-memory` verschwindet der Selbstgradient fuer `alpha=1`; der
Grenzfall ist daher eine Negativkontrolle, kein Knotenregime. Report:
`reports/long_runs/m0_axis/long_run_m0_alpha_one_results_2026-07-08.md`.

Deposition-Kernel-Audit 2026-07-08: Der Paketkern speichert Punktdepositionen
und berechnet die Kraft als Summe ueber `grad K(x-x_k)`. Das ist numerisch
bereits `G=delta`; `sigma_rep` und `sigma_att` sind effektive Interaktions-
laengen, keine separate Depositionsbreite. Report:
`reports/kernels/deposition/deposition_kernel_audit_2026-07-08.md`.

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
`reports/kernels/deposition/matched_deposition_kernel_pilot_2026-07-08.md` und
`reports/knot_scores/v0_5_controls/knot_score_v0_5_matched_deposition_100k_2026-07-08.md`.

Zero-Mean-Kernel-Notiz 2026-07-09: Die neue Condition `zero_mean_two_scale`
setzt `A_att = A_rep (sigma_rep/sigma_att)^d` und erzwingt damit `int K = 0`
fuer den unnormalisierten zweiskaligen Kernel. Der alte Baseline-Slice
`L_att=3`, `A_att=0.35` war nicht kompensiert; ein erster fairer Test ist
`sigma_att=1.5`, wo `A_att=0.296` gilt. Report:
`reports/kernels/deposition/zero_mean_kernel_decision_2026-07-09.md`.

Zero-Mean-/Matched-Pilot 2026-07-09: Der 100k-Pilot bei `sigma_att/sigma_rep=1.5`
zeigt praktisch deckungsgleiche aktive Bedingungen: `baseline`,
`zero_mean_two_scale` und `matched_deposition_renormalized` haben jeweils
`score median 0.857`, Memory-Radius um `0.102..0.103` und trennen sich klar von
`eta_zero`. Lesart: In diesem Kurzlauf dominiert lokale effektive Kruemmung;
die globale Bedingung `int K=0` ist noch nicht als separater Mechanismus
sichtbar. Report: `reports/kernels/deposition/zero_mean_matched_pilot_100k_2026-07-09.md`.

Scale-Ratio-/Rep-Zero-Kontrollen 2026-07-09 (`legacy-sign`): Die 100k-
Piloten fuer `sigma_att/sigma_rep in {2,3}` zeigen unter der alten
Gradientenrichtung, dass `baseline`, `zero_mean_two_scale`,
`matched_deposition_renormalized` und `single_scale` scorecard-nah bleiben,
waehrend `rep_zero` bei `q=3` stark dispersiv wird. Der anschliessende
Force-Komponenten-Pilot machte den Fehler sichtbar: die gemessenen
Memory-Center-Projektionen passten zur alten, nicht zur intendierten
Potentialkonvention. Mit der korrigierten Konvention ist `A_rep` lokal
repulsiv und `A_att` breit attraktiv; diese Kontrollen muessen neu gerechnet
werden. Reports: `reports/kernels/deposition/kernel_scale_ratio_and_rep_zero_controls_2026-07-09.md`
und `reports/kernels/corrected_sign/force_component_q3_pilot_2026-07-09.md`.


Corrected-Sign-Piloten 2026-07-09: Der q=3-Retest nach der
Kernelgradient-Korrektur zeigt, dass `baseline` mit `A_att=0.35` und
`single_scale` repulsionsdominiert dispergieren. Force-Komponenten bestaetigen
die neue Lesart direkt: `A_rep` zeigt vom Memory-Zentrum weg, `A_att` dorthin.
Die Amplitudenhierarchie bei festem `A_rep=1`, `sigma_rep=1`, `sigma_att=3`
findet den Drift-Umschlag zwischen `A_att=3.5` und `A_att=9`. Kompakte
Kandidaten liegen im Kurzpilot bei `A_att=9..35`; `A_att=35` hat die rundeste
Memory-Cloud, aber noch nur kurze Residence. `A_att=350` wirkt uebersteuert.
Reports: `reports/kernels/corrected_sign/corrected_sign_q3_pilot_2026-07-09.md` und
`reports/kernels/corrected_sign/amplitude_hierarchy_corrected_sign_q3_2026-07-09.md`.

AR-Modenprobe 2026-07-09: Auf PCA-reduzierten augmentierten Features fuer
`A_att=0.35`, `9` und `35`, Seeds `1..3`, `N=50,000`, Lags `1,2,5,10`,
werden alle langsamen Moden als reell klassifiziert. Kleine komplexe Paare
treten nur als schnelle Restmoden unter `|mu|<0.2` auf. Lesart: Das korrigierte
skalare Memory-Modell stuetzt Relaxation/Kompaktheit, aber noch keinen
oszillatorischen oder photonartigen Modus. Report:
`reports/kernels/mode_probes/ar_mode_probe_corrected_candidates_2026-07-09.md`.

Grenzscan 2026-07-09: Mit Seeds `1..10`, `N=50,000` und
`A_att=3.5..9.0` wurde die korrigierte Uebergangsgrenze verfeinert.
`rep/att=1` liegt bei `A_att ~= 7.93`, `net cos=0` bei `A_att ~= 7.85`;
also `chi ~= 0.87..0.88`. Report:
`reports/kernels/corrected_sign/transition_boundary_corrected_sign_q3_2026-07-09.md`.

Vektorgedaechtnis-Notiz 2026-07-09: Der naechste Modellschritt fuer
oszillatorische, photonartige oder bosonische Kandidaten ist ein orientierter
Memory-Kanal `p_n` mit klaren Kontrollen (`eta_v=0`, shuffled vector memory,
`M_v=0`, `lambda_v=1`). Report:
`reports/vector_memory/vector_memory_minimal_design_2026-07-09.md`.

Score-Architektur 2026-07-10: Der Experiment-Katalog enthaelt jetzt ein KPI-Register. `KnotScore` bleibt fuer Metastabilitaet/Residence/Kompaktheit reserviert; `ModeScore`, `PropagationScore` und `FormationScore` werden als separate Scorecards gefuehrt. Dimensionen sind eingeordnet: `D_occ` ist die aktuelle KnotScore-Dimensionskomponente, `memory_shape_dimension` ist covariance participation der Memory-Cloud, `D_cov` bleibt Sample-/Shape-Diagnostik und `D_spec` ist vorerst Geometrie-/Reconciliation-KPI statt Scorekomponente.

Initialer Vektormemory-Pilot 2026-07-10: Der Paketkern enthaelt jetzt einen
2D-Transverse-Pilotmodus. Der Kurzlauf mit `burn_in=0`, Seeds `1..3`,
`A_att in {0.35,7.75,8.0,9.0,20.0}` und `eta_v in {0,0.01,0.03}`
zeigt komplexe AR-Klassifikationen bereits in `eta_v=0`-Fallbacks. Die
nachgeschobene `eta_s=eta_v=0`-Kontrolle zeigt ebenfalls komplexe AR-Paare;
diese sind daher zunaechst Feature-/Random-Walk-/Sampling-Moden, keine
Schroedinger- oder Photonenevidenz. Die `alignment`-Kontrolle vergroessert
schwache/transitionale Radien eher; `A_att=20` bleibt kompakt und ueberwiegend
real. Reports: `reports/vector_memory/vector_memory_pilot_initial_2026-07-10.md`,
`reports/vector_memory/vector_memory_eta_s_zero_control_2026-07-10.md` und
`reports/vector_memory/vector_memory_alignment_control_2026-07-10.md`.

M0-Achsenpilot 2026-07-10: Nach Pareto-Regel wurde bei festem korrigiertem
Kandidatenschnitt `A_att=8`, `A_rep=1`, `sigma_att/sigma_rep=3`, `alpha=0.01`
nur `M0 in {0.5,1.0,2.0}` variiert (`N=100,000`, Seeds `1..5`, Score v0.5).
Hoeheres `M0` macht die aktiven Laeufe kompakter: medianer Sample-Radius
`3.632 -> 2.596`, Memory-Shape-Dimension `2.001 -> 2.204`. Der v0.5-Score
bleibt im Median aber bei `0.286`, weil Residence-Gain, Sample-Kompaktheit und
Memory-Kompaktheit die Partial-Schwellen nicht gemeinsam erreichen. Lesart:
`M0` ist ein echter Skalierungs-/Kopplungshebel, aber kein alleiniger
Knotenhebel in diesem Kurzpilot. Report:
`reports/long_runs/m0_axis/m0_axis_knot_score_pilot_2026-07-10.md`.

Scalar-Haertung 1M 2026-07-10: Im korrigierten q=3-Skalarfenster wurden
`A_att in {9,20,35}` bei festem `M0=1`, `alpha=0.01`, Seeds `1..5` und
`N=1,000,000` getestet. `A_att=20` und `35` tragen hohe v0.5-Scores
(`median 0.857`) und trennen sich stark von `eta_zero` in Sample-Kompaktheit,
Memory-Kompaktheit, Memory-Rundheit und Memory-Formdimension. Der Engpass
bleibt Residence-Gain: Median `1.237` fuer `A_att=20`, `1.040` fuer `A_att=35`.
Lesart: Das korrigierte Skalarmodell bildet seed-robuste kompakte
Memory-Clouds; fuer Paper-I-Metastabilitaet muss jetzt Residence-Skalierung mit
laengerem `N` gehaertet werden. Report:
`reports/long_runs/scalar_hardening/scalar_hardening_q3_1M_2026-07-10.md`.

N-Skalierung 2026-07-10: Fuer `A_att=20` und `35` wurde `N in {100k,300k,1M,3M}`
mit `burn_in=0` gemessen, damit das Einschwingen sichtbar bleibt. Ergebnis:
KnotScore v0.5 bleibt fuer beide Kandidaten ueber alle N-Punkte bei Median
`0.857`, die Memory-Radien bleiben nahezu stationaer (`~0.09` fuer `A_att=20`,
`~0.06` fuer `A_att=35`), und die Memory-Shape-Dimension liegt frueh nahe
`2.7..3.0`. Rohes `D_occ`/`D_win` steigen mit N bis etwa `2.0`. Residence-Gain
bleibt dagegen median unter der Partial-Schwelle `2` (`N=3M`: `1.584` bzw.
`1.684`). Lesart: kompakte Memory-Cloud-Formation geschieht schnell; offen ist
Residence-Konvergenz bzw. ein schaerferes Residence-Observable. Report:
`reports/long_runs/scalar_hardening/scalar_n_scaling_q3_2026-07-10.md`.

N-Abhaengigkeits-Recheck 2026-07-16: Der neue Reconciliation-Plot fuehrt die
alte Formation-Skalierung (`N=100k..3M`, `epsilon=0.03`), den kurzen
Rohsnapshot-Pilot (`N=200k`, `epsilon=1e-4`) und den `N=30M`-Referenzslice
zusammen. Lesart: Die Memory-Shape-Formation verhaelt sich qualitativ wie
zuvor; `N=200k` bleibt ein Pipelinecheck und ist fuer Heat-Trace-`D_spec` zu
kurz. Exakt `3D` ist kein hartes Kriterium; fuer Paper II zaehlen stabile
aktive Dimensionen bzw. Response-Raenge gegen Kontrollen. Report:
`reports/long_runs/scalar_hardening/n_dependence_recheck_2026-07-16.md`.

3e8-Resultat 2026-07-11: Die `N=300,000,000`-Laeufe fuer `A_att=20` und
`35`, Seeds `1..5`, sind abgeschlossen. Beide Kandidaten tragen v0.5 deutlich
gegen `eta_zero` (`score median 0.929`; Residence-Gain median `2.833` bzw.
`3.090`). Die Memory-Clouds bleiben kompakt/rund und nahe dreidimensional.
Die fixe finale `memory_center`-Residence ist dagegen kurz und selten, was auf
Drift/Rezentrierung hindeutet. Naechster Schritt ist deshalb dynamische,
zeitlokale Center-Diagnostik statt weiterer Blindscan. Report:
`reports/long_runs/long_3e8/long_run_3e8_results_2026-07-11.md`.
Residence-Update 2026-07-10: Long-Run-Ausgaben schreiben nun
`center_residence.sample_center` und `center_residence.memory_center`. Die
Summary verwendet fuer beide den festen Ballradius-Faktor `2`; groessere
Faktoren bleiben nur als Detaildiagnostik erhalten, damit der Residence-Wert
nicht durch einen zu grossen Suchball trivial wird.

Center-Trace-Update 2026-07-11: `experiments/current/dynamics/long_run_metastability.py`
kann mit `--trace-every` eine zeitlokale Memory-Center-/Radius-Spur schreiben.
Die neue Diagnose `dynamic_center_trace` misst co-moving Inside-Fraction,
maximale co-moving Runs in Memory-Zeiten und Center-Drift pro Memory-Zeit.
Damit wird ein Einzelknoten als mitbewegtes Objekt bewertet, nicht als fixes
absolutes Zentrum. Das ist die naechste Paper-I-Pruefung vor neuen Blindscans.

Dynamic-Center-Validation 2026-07-12: `long_run_metastability.py` kennt nun neben
festem `--trace-every` auch logarithmische explizite Trace-Zeitpunkte ueber
`--trace-points` und `--trace-spacing log`; dynamische Run-Dauern werden fuer
nichtuniforme Tracepunkte zeitgewichtet. Der erste `N=3M`-Trace-Pilot fuer
`A_att=20/35`, Seeds `1..5`, gegen `eta_zero` ist abgeschlossen. Ergebnis:
`dynamic_inside_fraction` und `dynamic_max_run` sind nicht allein trennend,
weil `eta_zero` im eigenen grossen Memory-Ball ebenfalls innen bleibt. Die
trennenden Metriken sind dynamischer RMS-Radius (`0.087/0.062` vs. `0.344`),
radiusnormalisierte Center-Drift pro Memory-Zeit (`0.028/0.017` vs. `0.129`)
und Memory-Shape-Dimension (`2.72/2.88` vs. `1.53`). Report und Plots:
`reports/long_runs/long_3e8/dynamic_center_trace_q3_N3M_2026-07-12.md`.

Spin-Proxy-/Hybrid-Trace 2026-07-12: Der Long-Run kombiniert nun etwa 100
logarithmische Trendpunkte mit einem gleichmaessig abgetasteten Endfenster.
Trend-KPIs und lokale Spin-KPIs werden getrennt berechnet, weil die rohe
Center-Geschwindigkeit und Winkelgeschwindigkeit von der Abtastkadenz
abhaengen. Der `N=1M`-Pre-Run fuer `A_att=20/35`, Seeds `1..5`, verwendet im
letzten Fenster 10,001 Punkte ueber 100 Memory-Zeiten (`dt_mem=0.01`). Die
logarithmischen Trendwerte bestaetigen Radius/Drift-Trennung gegen `eta_zero`.
Der lokale Bivector-Proxy verwendet nun den mitbewegten Rahmen
`L_int=(x-c_mem) wedge d(x-c_mem)/dt_mem`; der Radius bleibt dabei eine
separate Knotenobservable. Der korrigierte Proxy zeigt weiterhin keinen
persistenten skalaren Spinmodus: `axis_polarization ~= 0.01` und Dephasierung
bereits nach einem Update in aktiven Faellen und Kontrollen. Labor- und
mitbewegte Amplituden liegen im Epsilon-Sweep nahe beieinander, daher erklaert
Center-Drift diesen negativen Befund nicht. Kein Spinquantisierungs- oder
Photonclaim. Report:
`reports/long_runs/long_3e8/dynamic_center_spin_trace_q3_N1M_2026-07-12.md`.

Epsilon-Dynamic-Center-Sweep 2026-07-12: Fuer `A_att=35`, Seeds `1..3`,
`N=100k`, `epsilon=0` plus 24 logarithmische Werte `1e-12..1e1`, gegen
seedgleiche `eta_zero`-Kontrollen, zeigt sich ein klares kurzes Score-Plateau:
`score >= 0.75` ab etwa `epsilon=1.65e-6` bis `0.741`. Bei `epsilon=2.72`
werden Radius, Drift, Memory-Dimension und Spin-Proxy praktisch
`eta_zero`-aehnlich. Die nachtraegliche mitbewegte Spin-Reanalyse entfernt
nur einen kleinen Labor-Translationsanteil und bestaetigt den negativen
Orientierungsbefund. Unterhalb `~1e-6` ist die Dynamik skalenartig, aber
Memory-Roundness/Score-Gating teils degeneriert. Operativ: vor dem naechsten
30M-Lauf zuerst einen kurzen Plateau-Bestaetigungsslice fuer `A_att=20/35`
rechnen; `epsilon=0.03` ist nicht mehr als alternativloser Default zu lesen.
Report: `reports/long_runs/epsilon/epsilon_dynamic_center_q3_Aatt35_N100k_2026-07-12.md`.

N30M-Referenzslice 2026-07-13: Der Bestaetigungslauf mit `epsilon=1e-4`, `A_att=20/35`, Seeds `1..5`, gegen `eta_zero` ist ausgewertet. `A_att=35` war im damaligen Score der staerkste skalare Referenzkandidat; der neue Linearitaetsaudit erklaert seinen Radius: dynamischer Radius `~2.09e-4` statt `~1.04e-3` in `eta_zero`, Drift/Radius `~0.044` statt `~0.320`, `D_mem ~2.94` und Roundness `~0.843`. Die Paper-I-Lesart ist co-moving compact memory-cloud evidence, kein fixes absolutes Zentrum. Der Long-Run-Trace-AR-Check findet komplexe Klassifikationen auch in `eta_zero`; damit kein isolierter skalarer Phasen-/Photonmodus. Feature-Closure zeigt den staerksten aktiven Closure-Lift in Shape-/Radius-Scalars, nicht im Spin-Scalar. Reports: `reports/long_runs/long_3e8/paper_i_evidence_table_N30M_eps1em4_2026-07-13.md`, `reports/long_runs/long_3e8/long_run_trace_ar_modes_N30M_eps1em4_2026-07-13.md` und `reports/long_runs/long_3e8/feature_closure_N30M_eps1em4_2026-07-13.md`.

3D-Memory-Shape-Grenze 2026-07-13: Der `D_mem ~=2.94`-Befund wurde als lokales Memory-Shape-Observable geschaerft. Bei `A_att=35` liegen alle fuenf aktiven Seeds eng bei `D_mem=2.914..2.947` und Roundness `0.809..0.849`, waehrend die seedgleichen `eta_zero`-Kontrollen breiter und niedriger streuen (`D_mem=1.312..2.679`, Roundness `0.219..0.626`). Lesart: Paper I darf einen seed-stabilen co-moving Memory-Cloud-Befund im gewaehlten 3D-Embedding berichten. Paper II uebernimmt die offene Frage, ob daraus eine extern/macroskopisch robuste 3D-Selektion unter Ambient-Dimension, Mehrknoten-Wechselwirkung und externer Beobachtung folgt. Report: `reports/dimensions/memory_shape_boundary_2026-07-13.md`.

Ambient-Dimension-Sweep vorbereitet 2026-07-13: Der naechste Paper-II-Brueckentest legt denselben `A_att=35`, `epsilon=1e-4`, `N=30M`-Referenzslice in `d in {4,5,7,10,13,20}` und vergleicht `baseline` gegen `eta_zero`. `long_run_metastability.py` schreibt nun ungewichtetes `D_spec` fuer Sample-Pfad und Memory-Cloud mit begrenzten `spectral_points`; der Ambient-Report aggregiert `D_mem`, `D_spec`, Roundness, Radius und Drift gemeinsam. Launch-Notiz: `reports/dimensions/ambient_memory_shape_sweep_launch_2026-07-13.md`.

Entscheidungsnotiz 2026-07-07: `reports/kernels/shape_and_memory/kernel_memory_photon_decision_2026-07-07.md`
fasst die aktuelle Linie zusammen. Paper I sollte den Mechanismus als
effektives Memory-Kernel-Confinement formulieren. Zwei-Skalen-Kernel bleiben
optionale Erweiterung, nicht Kernclaim. Photon-/Oszillatorfragen brauchen einen
separaten erweiterten Zustand, etwa Velocity-, Phasen- oder Vektormemory.

## Dimensionsbefund

Belastbar aus dem Archiv:

- Quelle: `experiments/fractal_analysis/archive_source/data/n_scaling/resultsN.csv`.
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

## Kernelkompensations-Gate 2026-07-18

Der aktuelle q=3-Referenzkernel (`A_rep=1`, `A_att=20..35`) ist nicht
annaehend zero mean. Mit `q=sigma_att/sigma_rep>1` und
`a=A_att/A_rep` gilt fuer unnormalisierte Gausskerne exakt
`a_zero=q^-d`, waehrend lokale Rueckstellung `a>q^2` verlangt. Diese
Bedingungen sind im zweiskaligen Kernel strukturell disjunkt. Bei q=3 liegt
das integrierte Attraktions-/Repulsionsverhaeltnis in d=3 bei `540..945`.

Der kontrollierte `N=1M`-Test mit `q in {2,3,4}` bei festem
`chi=a/q^2=35/9`, Seeds `1..5` und gemeinsamen seedgleichen
`eta_zero`-Kontrollen ist abgeschlossen. Alle kontinuierlichen KPIs kollabieren
seedweise bis auf maximal `1.65e-8` relative q-Spanne; der groesste finale
Memory-Radius betraegt nur `2.0e-4 sigma_rep`. In diesem kompakten Ast wird also
nur die lokale Taylor-Kruemmung identifiziert, nicht die Zwei-Skalen-Geometrie.

Der breite Drei-Skalen-Pilot ist abgeschlossen. Bei `sigma_comp=10` kann
`int K=0` exakt erfuellt und zugleich die lokale Referenzkruemmung beibehalten
werden. Im `d=3`-Pilot liegt der Kraftwechsel bei `r/sigma_rep ~=10.91`.
Im `N=1M`-Pilot, Seeds `1..5`, bleiben die gematchten lokalen KPIs bis `2.2e-11` relativ
identisch; der rohe Kompensator aendert sie um hoechstens `0.238%`.

Auch das nachgelagerte signierte Kanal-Gate ist als Frozen-Source-
Architekturtest abgeschlossen. Auf den `N=100M`-Checkpoints in `d=3/10` sind
Nullarme und gleiche Labelprodukte bitgenau, der Produkt-Flip kehrt die
Antwort um, und die maximale Radiusstoerung bleibt unter `4.5e-5`. Die aktive
Selbstkopplung reduziert die Pulsantwort von etwa `0.03 R_mem` bei `eta=0`
auf etwa `0.00136 R_mem`. Dies ist noch keine Seed-Evidenz und kein
Ladungsclaim. Reports:
`reports/kernels/compensation/kernel_compensation_constraint_audit_2026-07-18.md`,
`reports/kernels/compensation/fixed_curvature_sigma_pilot_d3_N1M_2026-07-18.md`,
`reports/kernels/compensation/three_scale_zero_mean_pilot_d3_N1M_2026-07-18.md`
und
`reports/response/signed_scalar_cross_channel_pilot_2026-07-18.md`.

## Kernelreduktion und lineares Regime 2026-07-18

Der enge Core-Audit zeigt: Beim bisherigen (A_rep,A_att)=(1,35)-Referenzkernel
ist der nominell repulsive Anteil im tatsaechlich gesampelten Bereich kein
repulsiver Kern. R_mem/sigma_rep liegt nur bei etwa 2e-4. Der attraktive
Ein-Kernel-Fall (0,26) matched die lokale Kruemmung exakt und stimmt bei
N=300k, Seeds 1..5, in Radius, D_mem, Roundness, Drift, D_cov und D_occ bis
etwa 1e-8 relativ mit (1,35) ueberein.

Der vollstaendige A_att=0..40-Screening-Scan ohne A_rep besitzt keine
endliche numerische Uebergangsgrenze. A_att=0 ist bitgenau eta=0; alle
A_att>0 liegen in diesem Slice auf einem glatten Rueckstellungsast. Mit
L=sigma_att, q=1-lambda und g=eta M0 A_att/L^2 lautet der lineare
Relativmodus

    r_(n+1)=q(1-g)r_n+q epsilon xi_n.

Sein stationaerer RMS-Radius ist

    R_linear=sqrt(d) q epsilon / sqrt(1-q^2(1-g)^2).

Fuer A_att>=5 betraegt der mediane relative Fehler des gemessenen dynamischen
Radius nur 0.94 Prozent, maximal 3.44 Prozent. Beim gematchten A_att=26 sagt
die Formel 2.071e-4 voraus; gemessen werden 2.093e-4. Der bisherige N=30M-
Referenzwert um 2.09e-4 liegt auf derselben Vorhersage.

Lesart: Der kleine-Radius-Ast ist derzeit robuste Evidenz fuer einen
co-moving linearen skalaren Relaxationsmodus. Er ist keine Evidenz fuer einen
nichtlinearen metastabilen Knoten oder einen endlichen Phasenuebergang.
Insbesondere ist D_mem nahe drei in d=3 die erwartete isotrope Gaussgeometrie;
sie staerkt keinen Claim emergenter Dreidimensionalitaet. Dies erklaert auch
die reellen AR-Moden und den negativen Spin-/Phasenbefund.

Die dimensionslose Form zeigt ausserdem, dass A_att, eta und M0 im
attraktiven Ein-Kernel-Modell nur ueber ihr Produkt eingehen. Rohe
Amplitudenwerte sind daher keine getrennt identifizierten
Wechselwirkungsstaerken. Die naechste sinnvolle Achse ist R_linear/L bei
festem g, nicht ein weiterer A_att-, eta- oder M0-Blindscan.

Die Feldgleichungs-Bruecke ist implementiert und analytisch getestet. Der
Gausskernel ist exakt ein Heat-Semigroup-Snapshot in einer
Hilfsdiffusionskoordinate. Ein physisches Relaxations-Diffusionsfeld stimmt
nur langwellig ueberein, hat einen Yukawa/Helmholtz-Greenkernel und muss als
eigener Feldzustand in die Markov-Einbettung aufgenommen werden. Es ist ein
Modellwechsel und erzeugt weiterhin keine harte endliche
Ausbreitungsgeschwindigkeit.

Reports:
reports/kernels/core/kernel_core_audit_2026-07-18.md,
reports/kernels/core/attractive_only_regime_scan_d3_N300k_2026-07-18.md und
reports/kernels/field/field_equation_bridge_2026-07-18.md.

## Naechste technische Schritte

1. Fuer die festen Diffusionsarme `0`, `0.3 L`, `1.0 L` Low-Mode-Features
   und seedgepaart dieselben `eta=0`-Kontrollen speichern.
2. AR-/Feature-Closure ueber mehrere Lags testen. Ein Feldmodus zaehlt nur,
   wenn seine Rate gegen `nu=0` und `eta=0` getrennt und lagstabil ist.
3. Boxlaenge und Modenzahl als reine Numeriksensitivitaet pruefen. Nach dem
   exakten linearen Befund keine kleineren epsilon-Werte mehr scannen.
4. Nur bei einem neuen kontrollgetrennten Modus laengere N-Laeufe starten.
   Das aktuelle Heat-Feld traegt keinen endlichen Geschwindigkeitsclaim.
5. Unabhaengige Cross-Kanal-Checkpoints und spaetere Vektormemory-Tests bleiben
   getrennte Folgegates.