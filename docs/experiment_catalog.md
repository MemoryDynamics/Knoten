# Experiment-Katalog

Stand: 2026-07-09.

Diese Datei ist zugleich Experiment-Katalog, Reproduzierbarkeitsnotiz und
Long-Run-Plan. Sie ersetzt die alten Einzeldateien zu Reproduzierbarkeit,
Hardening und Long-Run-Metastabilitaet.

## Kanonische Entry-Points

| Datei | Thema | Status | Naechste Nutzung |
| --- | --- | --- | --- |
| `experiments/long_run_metastability.py` | Long-N-Metastabilitaetsdiagnostik | aktiv | Knotenscore v0.3-v0.5, `m0_zero`, `alpha_one`, `matched_deposition` und weitere Ablationen |
| `experiments/anchor_paper_pipeline.py` | Paper-0-Smoke mit Markov-Schicht | aktiv | schneller Sanity-Check |
| `experiments/anchor_sensitivity_analysis.py` | Seed-/Lag-/Voxel-/Kontroll-Sensitivitaet | aktiv | kurze Operator-Pipeline-Checks |
| `experiments/epsilon_step_balance.py` | Rauschen-vs-Drift-Updatebilanz | aktiv | gezielte Epsilon-/Glattheitsdiagnostik |
| `experiments/epsilon_floor_visual_probe.py` | flexible 3D-Visualisierung der Epsilon-Floor-Faelle | aktiv | Formvergleich bei extremen Skalen |
| `experiments/kernel_shape_probe.py` | 3D-Fuehrungskoordinatenplot fuer Kernelbreiten und Amplituden | aktiv | visuelle Shape-Diagnostik, keine Long-Run-Evidenz |
| `experiments/knot_score_report.py` | Scorecard fuer vorhandene Long-Run-JSONs | aktiv | Knotenscore v0.5 und Paper-I-Evidenzhygiene |
| `experiments/reference_experiment.py` | kleiner Referenzlauf | aktiv | Smoke-Test |
| `experiments/fractal_analysis/analyze_dimension_claim.py` | Audit des archivierten `D_occ`-Claims | aktiv | Claim-Register |
| `experiments/fractal_analysis/reproduce_dimension_pilot.py` | kleine/mittlere Reproduktion | aktiv | spaetere Dimensionshaertung |
| `experiments/fractal_analysis/plot_d_alpha_n_intensity.py` | d-alpha-N-Heatmaps aus Reproduktions-JSON | aktiv | Seed-/N-Dimensionsberichte |
| `experiments/synchronization/` | Innen/Aussen- und Mehrknoten-Synchronisation | geplant | Single-Knot-Observablen und Response-Rank |
| `experiments/cli.py` | kategorisierte Experimentsteuerung | aktiv | Einstieg in Skriptfamilien |
| `experiments/propagation_speed/ballistic_kernel_probe.py` | korrigierter Ein-Kernel-Ballistik-Track mit `eta/eta_c` | aktiv | Sanity-Check fuer skalare Photon-Analogien |

## Long-Run-Metastabilitaet

Kanonischer Start:

```powershell
python experiments/long_run_metastability.py `
  --steps 10000000 `
  --seeds 1 `
  --conditions baseline `
  --dim 3 `
  --alpha 0.01 `
  --sample-every 1000 `
  --burn-in 1000000 `
  --max-memory 800 `
  --output-dir data/processed/long_run_metastability/2026-06-29_initial
```

Abgeschlossener Baseline-Lauf:

| Feld | Wert |
| --- | --- |
| Condition | `baseline` |
| Seed | `1` |
| Updates | `10,000,000` |
| Samples | `9001` |
| Laufzeit | `337.997 s` |
| Steps/s | `29,586` |
| Memory-Horizon | `600` |
| gespeicherte Gewichtsmasse | `0.997595` |
| Bestes Residence-Verhaeltnis | `256 alpha^{-1}` |
| `D_cov` / `D_occ` | `1.699` / `1.792` |

Residence nach Voxelgroesse:

| Voxel | visited | knot_count | max updates | max in `alpha^{-1}` |
| ---: | ---: | ---: | ---: | ---: |
| `0.5` | `674` | `529` | `14,000` | `140` |
| `1.0` | `180` | `168` | `20,400` | `204` |
| `2.0` | `56` | `54` | `25,600` | `256` |

Kontrollreport 2026-07-01:

| Condition | Best residence mean +/- SD in `alpha^{-1}` | Mean centered radius | Lesart |
| --- | ---: | ---: | --- |
| `baseline` | `437.6 +/- 323.1` | `3.880` | kompakt, langlebig, seed-variabel |
| `eta_zero` | `80.0 +/- 12.2` | `57.284` | echte Negativkontrolle |
| `single_scale` | `697.7 +/- 534.6` | `3.734` | Kernel-Ablation, keine Negativkontrolle |

Lesart: Memory-Gradient-Feedback trennt sich deutlich von `eta_zero`; der
zweiskalige Baseline-Kernel ist aber noch nicht als notwendiger Mechanismus
isoliert. Der Report liegt unter `reports/long_run_control_report_2026-07-01.md`.

M0-/Alpha-One-Kontrolle 2026-07-08 (`N=100,000,000`, Seeds `1..10`):

| Condition | stored mass | Memory-Horizon | Mean radius | Mean `D_occ` | median best residence | Lesart |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `m0_zero` | `0` | `600` | `212.678` | `1.819` | `8000` Updates / `80 alpha^{-1}` | Null-Feld-Kontrolle, diffundiert weit |
| `alpha_one` | `1` | `6` | `212.678` | `1.819` | `8000` Updates / `8000 alpha^{-1}` | seedgleich zu `m0_zero`; Selbstgradient verschwindet |

Lesart: `alpha=1` ist fuer den symmetrischen selbstzentrierten Kernel effektiv
eine Negativkontrolle, nicht ein konfiniertes Ein-Schritt-Memory-Regime. Report:
`reports/long_run_m0_alpha_one_results_2026-07-08.md`.

Matched-Deposition-Pilot 2026-07-08 (`N=100,000`, Seeds `1..5`, Slow Python):

| condition | score median | sample radius median | memory radius median | memory roundness median | Lesart |
| --- | ---: | ---: | ---: | ---: | --- |
| `baseline` | `0.857` | `0.362` | `0.097` | `0.767` | kompakter Delta-Referenzlauf |
| `matched_deposition` | `0.714` | `1.535` | `0.244` | `0.668` | weiter confined, aber breiter/schwaecher |
| `eta_zero` | `n/a` | `5.167` | `0.622` | `0.380` | Negativkontrolle |

Lesart: `matched_gaussian` ist die konservative positive Schreib-/Lese-
Kernel-Variante. Ohne Steifigkeitsrenormierung reduziert die normierte Faltung
in `d=3` die lokale Kraftskala um etwa Faktor `5.66`; der faire naechste Test
ist daher curvature-renormalized matching. Reports:
`reports/matched_deposition_kernel_pilot_2026-07-08.md` und
`reports/knot_score_v0_5_matched_deposition_100k_2026-07-08.md`.

## Epsilon-Step-Balance

Gezielter Baseline-Run vom 2026-07-01:

| epsilon | median noise | median repulsive step | median net drift | median noise/repulsive | mean turn cosine |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `0.03` | `0.04624` | `0.01281` | `0.01231` | `3.615` | `-0.070` |
| `0.015` | `0.02312` | `0.00643` | `0.00618` | `3.598` | `-0.071` |
| `0.01` | `0.01541` | `0.00429` | `0.00412` | `3.594` | `-0.071` |
| `0.005` | `0.00771` | `0.00215` | `0.00206` | `3.593` | `-0.071` |

Lesart: Kleineres `epsilon` skaliert in diesem Slice Noise, Drift und Radius
fast gemeinsam herunter. Es macht die Trajektorie kleiner, aber nicht glatter
oder drift-dominierter. Report: `reports/epsilon_step_balance_2026-07-01.md`.

Epsilon-Floor-Run vom 2026-07-02:

| epsilon | median total step | median noise/drift | turn mean | zero-step fraction | mean radius |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `0` | `0` | `n/a` | `n/a` | `1.000` | `0` |
| `1e-5` | `1.594e-05` | `3.738` | `-0.071` | `0` | `2.351e-04` |
| `1e-10` | `1.594e-10` | `3.738` | `-0.071` | `0` | `2.351e-09` |
| `1e-20` | `1.594e-20` | `3.738` | `-0.071` | `0` | `2.351e-19` |
| `1e-34` | `1.594e-34` | `3.738` | `-0.071` | `0` | `2.351e-33` |

Lesart: Exakt `epsilon=0` ist fuer den Nullstart ein deterministischer
Fixpunkt. Jedes positive getestete `epsilon` skaliert die Bewegung fast exakt
linear, ohne die Richtungsstatistik zu glaetten. Reports:
`reports/epsilon_floor_probe_2026-07-02.md` und
`reports/epsilon_floor_visual_probe_2026-07-02.md`.

## Kernel-Shape-Probe

Punktueller 3D-Fuehrungskoordinaten-Run vom 2026-07-02:

| case | sigma_rep | sigma_att | A_rep | A_att | k_eff | mean radius | median step | turn mean | path/chord |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `1` | `3` | `1` | `0.35` | `0.1442` | `0.233` | `0.1099` | `-0.342` | `1202.3` |
| `att_zero` | `1` | `3` | `1` | `0` | `0.1500` | `0.225` | `0.1090` | `-0.348` | `1238.7` |
| `rep_zero` | `1` | `3` | `0` | `0.35` | `-0.0058` | `6.620` | `0.1519` | `0.059` | `48.9` |
| `strong_local` | `1` | `3` | `4` | `0.35` | `0.5942` | `0.075` | `0.0707` | `-0.430` | `2746.5` |
| `wide_strong` | `2` | `6` | `16` | `1.4` | `0.5942` | `0.075` | `0.0707` | `-0.430` | `2752.4` |

Die zugehoerigen Shared-Scale-SVGs sind
`figures/draft/kernel_shape_probe_2026-07-01.svg` und
`figures/draft/kernel_seed_probe_2026-07-02.svg`. Zusaetzlich liegen flexible
Varianten mit panel-eigener Skala unter
`figures/draft/kernel_shape_probe_flexible_2026-07-02.svg` und
`figures/draft/kernel_seed_probe_flexible_2026-07-02.svg`. Flexible Varianten
zeigen Form, nicht absolute Groesse.

Seedvergleich fuer den Baseline-Case:

| seed | mean radius | median step | turn mean | span xyz |
| ---: | ---: | ---: | ---: | --- |
| `1` | `0.233` | `0.1099` | `-0.342` | `1.01, 0.78, 0.87` |
| `2` | `0.318` | `0.1113` | `-0.351` | `1.08, 0.88, 1.16` |
| `3` | `0.387` | `0.1100` | `-0.346` | `0.76, 0.95, 1.54` |
| `4` | `0.474` | `0.1095` | `-0.340` | `1.75, 0.78, 0.97` |
| `5` | `0.214` | `0.1099` | `-0.343` | `0.85, 0.98, 0.67` |

Lesart: Die schwarze Linie in der Figur ist eine geglaettete Rolling-Mean-
Trajektorie; die farbige Linie ist der roh gesampelte Pfad desselben Cases.
`k_eff = eta(A_rep/sigma_rep^2 - A_att/sigma_att^2)` ist die lokale
restaurierende Skala in der aktuellen Euler-Konvention. Deshalb zerfaellt
`A_att=0` nicht: der `A_rep`-Anteil ist lokal bindend. Die schaerfere
Dispersionskontrolle ist `A_rep=0`, die hier den Radius stark vergroessert.
Der Baseline-Seedvergleich spricht fuer ein robustes kompaktes Regime, aber
nicht fuer identische Trajektorien; Seed `5` zeigt zudem, dass `path/chord`
bei sehr kleinem Endpunktabstand schlecht konditioniert sein kann.
Report: `reports/kernel_shape_probe_2026-07-01.md`.


## Knotenscore v0.3

Report vom 2026-07-02: `reports/knot_score_v0_3_2026-07-02.md`.

Der Score mittelt aktuell vier Komponenten: Residence-Gain, Kompaktheit gegen
`eta_zero`, Voxel-Stabilitaet und interne Occupancy-Dimension `D_occ`. `D_occ`
ist ein Nicht-Kollaps-/Innenraum-Signal, kein externer 3D-Nachweis.

| condition | n | score mean | score median | residence gain median | compactness gain median | voxel stability median | D_occ median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `5` | `0.925` | `1.000` | `3.975` | `14.764` | `0.503` | `1.815` |
| `single_scale` | `5` | `0.875` | `0.875` | `5.675` | `15.340` | `0.188` | `1.816` |

Lesart: Der Score trennt interagierende Bedingungen klar von `eta_zero` in
Residence und Kompaktheit. `D_occ` bestaetigt nicht-kollabierte interne
Ausdehnung, trennt aber Baseline und `single_scale` nicht. Der spezifisch
zweiskalige Baseline-Mechanismus ist daher weiterhin nicht isoliert. Neue
Long-Run-JSONs enthalten nun `sample_shape` und `memory_cloud`; die alten
10M-JSONs enthalten diese Formmetriken noch nicht.

Shape-Pilot 1M vom 2026-07-02: `reports/knot_score_v0_3_shape_pilot_1M_2026-07-02.md`.

| condition | score median | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `0.875` | `2.005` | `0.323` | `1.090` | `2.678` | `0.642` | `0.098` |
| `eta_zero` | `n/a` | `2.001` | `0.318` | `16.098` | `1.639` | `0.331` | `0.508` |
| `single_scale` | `0.750` | `2.006` | `0.323` | `1.049` | `2.683` | `0.644` | `0.096` |

Lesart: Der rohe Pfad ist kein guter Rundheitsindikator, weil alle drei
Bedingungen aehnliche Sample-Rundheit zeigen. Die Memory-Cloud trennt dagegen
aktive Feedbackbedingungen von `eta_zero`: deutlich kompakter, runder und
hoeher dimensional. Baseline und `single_scale` bleiben auch hier praktisch
nicht unterschieden.

## Knotenscore v0.4

Report vom 2026-07-02: `reports/knot_score_v0_4_shape_pilot_1M_2026-07-02.md`.

v0.4 behaelt die vier v0.3-Komponenten bei und fuegt drei Memory-Cloud-
Komponenten hinzu: Kompaktheit gegen `eta_zero`, Rundheits-Gain und
Formdimensions-Gain. Der rohe Sample-Pfad bleibt Diagnostik, nicht
Knotenform-Kriterium.

| condition | score mean | score median | residence gain median | sample compactness median | voxel stability median | D_occ median | memory compactness median | memory roundness gain median | memory dimension gain median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `0.900` | `0.929` | `2.150` | `14.740` | `0.451` | `1.846` | `5.208` | `2.110` | `1.634` |
| `single_scale` | `0.886` | `0.857` | `1.843` | `15.314` | `0.357` | `1.847` | `5.321` | `2.117` | `1.637` |

Lesart: v0.4 macht den Memory-Cloud-Knotenbegriff expliziter und trennt die
aktiven Bedingungen klar von `eta_zero`. Es isoliert aber weiterhin keinen
notwendigen zweiskaligen Baseline-Mechanismus, weil `single_scale` fast gleich
stark bleibt. Der naechste Kontrollschritt ist daher `amplitude_rep = 0` als
echte Dispersionsablation in genau demselben 1M-Shape-Pilot-Protokoll.

15-Seed-Erweiterung vom 2026-07-07:

| run | report | baseline median | single_scale median | reading |
| --- | --- | ---: | ---: | --- |
| 1M, Seeds `1..15` | `reports/knot_score_v0_4_seeds_1-15_1M_2026-07-07.md` | `0.857` | `0.857` | gleiche Scorelage |
| 100M, Seeds `1..15` | `reports/knot_score_v0_4_seeds_1-15_100M_2026-07-07.md` | `1.000` | `1.000` | gleiche Scorelage; Quellordner heisst `10M`, JSON sagt `100M`, dirty provenance |

Damit ist Feedback-Confinement robuster, aber der zweiskalige Baseline-Claim
schwaecher. Fuer Paper I ist ein ein- oder feedback-kernelbasierter
Confinement-Claim sauberer als ein spezifischer Zwei-Skalen-Claim.

Kontrollfester v0.5-Score vom 2026-07-08:
`reports/knot_score_v0_5_controls_100M_2026-07-08.md`.

v0.5 vergleicht Residence in rohen Updates statt in `alpha^{-1}` und laesst
Memory-Kompaktheit nur bei nichtdegenerierter Memory-Cloud zaehlen. Dadurch
fallen `m0_zero` und `alpha_one` korrekt zusammen.

| condition | n | score median | residence gain median | compactness gain median | memory valid | Lesart |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `baseline` | `15` | `1.000` | `6.667` | `14.767` | `15/15` | aktives Feedback-Confinement |
| `single_scale` | `15` | `1.000` | `8.500` | `15.344` | `15/15` | ebenso stark; kein Zwei-Skalen-Nachweis |
| `m0_zero` | `10` | `0.286` | `1.000` | `1.000` | `0/10` | Null-Feld-Kontrolle |
| `alpha_one` | `10` | `0.286` | `1.000` | `1.000` | `0/10` | Ein-Punkt-Memory degeneriert zu Nullkraft |

## Ballistische MSD-Probe

Report vom 2026-07-07: `reports/ballistic_kernel_probe_2026-07-07.md`.

Der korrigierte skalare Ein-Kernel-Test nutzt `lambda` als tatsaechliche
Memory-Relaxation und fuer die selbstabstossende Ballistik-Probe das
Drift-Vorzeichen `+ eta * grad`. Am 2026-07-08 wurde zusaetzlich die
Schwellenlogik korrigiert: der Sweep laeuft ueber `r=eta/eta_c` mit
`eta_c=lambda_m/((1-lambda_m)M0 a0)`, waehrend der analytische Residualtest
`gamma=eta lambda_m M0 a0` verwendet. Ergebnis des bisherigen 2026-07-07-
Reports: keine ballistische Skalierung. Deterministische Faelle relaxieren
oder stagnieren; rauschgetriebene Faelle liegen bei maximaler MSD-Slope etwa
`1.138`, nicht nahe `2`.

Lesart: Das skalare overdamped Memory-Modell ist derzeit keine tragfaehige
Photon- oder harmonischer-Oszillator-Probe. Vor physikalischer Skalierung mit
`hbar nu`, `mc^2` oder grossen/kleinen Zahlen braucht es erst ein
dimensionsloses oszillierendes oder ballistisches Regime, vermutlich mit
Velocity-, Phasen- oder Vektormemory.

## Entscheidungsnotizen

| Datei | Thema | Lesart |
| --- | --- | --- |
| `reports/kernel_memory_photon_decision_2026-07-07.md` | Kernel, Memory und Photon-Track | Paper I als effektives Memory-Kernel-Confinement; Zwei-Skalen-Kernel optional; Photon-Track braucht erweiterten Zustand. |
| `reports/alpha_memory_mass_decision_2026-07-08.md` | Alpha, M0 und Ballistikschwelle | `beta=lambda_m M0`; Alpha-Scans kontrolliert ueber `lambda_m`, `M0`, Tail-Cutoff und `eta/eta_c`; Photon-Track erst nach komplexen/coarse-grained Moden. |
| `reports/privacy_and_control_plan_2026-07-08.md` | Privacy und M0/Alpha-One-Kontrollen | Privacy-Policy und Kontrollplan; lokale private Klartexte entfernt, `m0_zero` und `alpha_one` bleiben Negativkontrollen. |
| `reports/deposition_kernel_audit_2026-07-08.md` | Deposition-Kernel-Audit | Delta ist die Baseline; finite `gaussian` und `matched_gaussian` sind jetzt als effektive Faltung implementiert. |
| `reports/matched_deposition_kernel_pilot_2026-07-08.md` | Matched-Deposition-Pilot | Normalisiertes Gaussian-Matching trennt von `eta_zero`, ist im 100k-Pilot aber breiter als Delta; naechster Test braucht Steifigkeitsrenormierung. |
| `reports/repository_cleanup_2026-07-09.md` | Repository-Cleanup | Aktive Docs bleiben bei sieben Seiten; lokale private Klartextnotizen wurden entfernt. |

## Reproduzierbarkeitsregeln

Jeder Lauf, der als Evidenz genutzt wird, braucht:

- Parameter und Condition;
- Seed-Liste;
- Git-Revision und Arbeitsbaumstatus;
- Burn-in, Sampling und Outputpfad;
- Runtime und Steps/s;
- maschinenlesbares JSON unter `data/processed/`;
- nach Review einen datierten Report unter `reports/`.

Lange Laeufe gehoeren nicht in CI und nicht in die normale Testsuite.

## Markov-/Operator-Status

Initial vorhanden:

- reduzierte Memory-Summary-Features pro Sample;
- Lagged datasets auf Sample-Indizes;
- Transition Counts und Uebergangsmatrizen;
- implied timescales und einfache Chapman-Kolmogorov-Fehler;
- kleine Seed-/Lag-/Voxel-/Kontroll-Sensitivitaet.

Weiter offen:

- vollstaendige Memory-Traces oder reichere Feature-Familien;
- systematischer Bootstrap;
- PCCA-/HMM-/PMM-basierte metastabile Zustandsmodelle;
- Long-Run-Transferoperatoren statt Kurzlauf-Sanity-Checks.

## Effektive Dimension

Archiv:

| embedding dim | N | runs | mean D_occ | Lesart |
| ---: | ---: | ---: | ---: | --- |
| 5 | 60,000,000 | 5 | 2.810559 | staerkster Near-3-Long-N-Befund |
| 3 | 60,000,000 | 10 | 2.372485 | nicht der staerkste Long-N-Punkt |
| 4 | 60,000,000 | 5 | 2.682259 | nahe, aber unter dim 5 |
| 6 | 60,000,000 | 5 | 2.695450 | ein Run gewinnt gegen dim 5 |

Konsequenz: archivierter Long-N-Near-3-Befund mit plausibler
Reproduktionskopplung, kein Nachweis eindeutiger 3D-Selektion.

Seeded d-alpha-N-Scan 2026-06-30:

| Scan | Ergebnis | Lesart |
| --- | --- | --- |
| `d=3..8`, `alpha=0.01/0.02`, `N=30k/100k/300k`, Seeds `1..5` | `D_cov`-Naehe zu 3 wandert von `d=3` ueber `d=5` zu `d=6/7` | kein stabiles `d=3`-Plateau; eher endliche-N-/Fitfenster-/Schaetzerabhaengigkeit |

## Innen/Aussen- und Synchronisationsprogramm

Neuer geplanter Pfad:

| Stufe | Ziel | Messgroessen |
| --- | --- | --- |
| Einzelknoten | stabile externe und interne Observablen extrahieren | center, shape tensor, radius, mode coefficients, residence |
| Basin-Statistik | Seeds als Attraktionskanal-Sampler behandeln | `P(knot type | parameters, seed)` |
| Zwei-Knoten-Pilot | Synchronisation von zwei Knoten testen | cross-correlation, phase-locking, response delay |
| Externer Subraum | gemeinsame makroskopische Wechselwirkungsstruktur messen | response matrix, response rank, subspace stability |

Guardrail: Diese Stufe behauptet keine Quantenfeldtheorie. Sie prueft nur, ob
synchronisierte Knoten kollektive externe Observablen ausbilden.

## Historische Skriptfamilien

| Familie | Dateien | Relevanz | Risiko |
| --- | --- | --- | --- |
| Knotenstabilitaet | `experiments/knot_stability/*.py` | Trajektorien, Knotenvisuals | historische Parameter |
| Dimension Selection | `experiments/dimension_selection/DimensionsHeatmap*.py` | Dimension/Heatmaps | lange Laufzeiten |
| Zwei-Skalen-Kernel | `experiments/dimension_selection/2SkalenKernel/*.py` | Double-Kernel-Regime | unterschiedliche Konventionen |
| Fraktalanalyse | `experiments/fractal_analysis/Fraktale/*.py` | Archivquelle `D_occ ~ 2.8` | alte CSVs ohne Seed-Spalten |
| Propagation Speed | `experiments/propagation_speed/PaperII3D_*.py` | Paper-II-Programm | Threshold-Robustheit offen |
| OU-Limit | `experiments/ou_limit/*.py` | analytische Kontrollfiguren | schematisch |
| Legacy | `experiments/legacy/scripts/highN_regime*.py` | historische High-N-Regime | nur gezielt starten |
