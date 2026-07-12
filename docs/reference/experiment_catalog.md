# Experiment-Katalog

Stand: 2026-07-12.

Diese Datei ist zugleich Experiment-Katalog, Reproduzierbarkeitsnotiz und
Long-Run-Plan. Sie ersetzt die alten Einzeldateien zu Reproduzierbarkeit,
Hardening und Long-Run-Metastabilitaet.

## Kanonische Entry-Points

| Datei | Thema | Status | Naechste Nutzung |
| --- | --- | --- | --- |
| `experiments/current/dynamics/long_run_metastability.py` | Long-N-Metastabilitaetsdiagnostik | aktiv | Knotenscore v0.5, Center-/Memory-Ball-Residence, dynamischer `--trace-every` Memory-Center-Trace, `m0_zero`, `alpha_one`, `matched_deposition`, `zero_mean_two_scale` und weitere Ablationen |
| `experiments/current/dynamics/dynamic_center_trace_report.py` | Aggregation und Plots fuer dynamische Center-/Spin-Traces | aktiv | Methodikreport fuer co-moving Radius, Drift/Radius, Memory-Shape und Spin-Proxy gegen `eta_zero` |
| `experiments/current/dynamics/epsilon_dynamic_center_sweep.py` | Epsilon-Sensitivitaet auf dynamischen Center-/Spin-Benchmarks | aktiv | kurze Schwellenfindung fuer Rauschskala vor laengeren Hybrid-Traces |
| `experiments/current/anchors/anchor_paper_pipeline.py` | Paper-0-Smoke mit Markov-Schicht | aktiv | schneller Sanity-Check |
| `experiments/current/anchors/anchor_sensitivity_analysis.py` | Seed-/Lag-/Voxel-/Kontroll-Sensitivitaet | aktiv | kurze Operator-Pipeline-Checks |
| `experiments/current/dynamics/epsilon_step_balance.py` | Rauschen-vs-Drift-Updatebilanz | aktiv | gezielte Epsilon-/Glattheitsdiagnostik |
| `experiments/current/dynamics/epsilon_floor_visual_probe.py` | flexible 3D-Visualisierung der Epsilon-Floor-Faelle | aktiv | Formvergleich bei extremen Skalen |
| `experiments/current/kernels/kernel_shape_probe.py` | 3D-Fuehrungskoordinatenplot fuer Kernelbreiten und Amplituden | aktiv | visuelle Shape-Diagnostik, keine Long-Run-Evidenz |
| `experiments/current/markov/knot_score_report.py` | Scorecard fuer vorhandene Long-Run-JSONs | aktiv | Knotenscore v0.5 und Paper-I-Evidenzhygiene |
| `experiments/current/dynamics/scalar_n_scaling_report.py` | N-Skalierung korrigierter skalarer Kandidaten | aktiv | Einschwing-/Residence-Skalierung fuer `A_att=20/35` |
| `experiments/current/reference/reference_experiment.py` | kleiner Referenzlauf | aktiv | Smoke-Test |
| `experiments/fractal_analysis/analyze_dimension_claim.py` | Audit des archivierten `D_occ`-Claims | aktiv | Claim-Register |
| `experiments/fractal_analysis/reproduce_dimension_pilot.py` | kleine/mittlere Reproduktion | aktiv | spaetere Dimensionshaertung |
| `experiments/fractal_analysis/plot_d_alpha_n_intensity.py` | d-alpha-N-Heatmaps aus Reproduktions-JSON | aktiv | Seed-/N-Dimensionsberichte |
| `experiments/current/memory/synchronization/` | Innen/Aussen- und Mehrknoten-Synchronisation | geplant | Single-Knot-Observablen und Response-Rank |
| `experiments/cli.py` | kategorisierte Experimentsteuerung | aktiv | Einstieg in Skriptfamilien |
| `experiments/propagation_speed/ballistic_kernel_probe.py` | korrigierter Ein-Kernel-Ballistik-Track mit `eta/eta_c` | aktiv | Sanity-Check fuer skalare Photon-Analogien |

## Long-Run-Metastabilitaet

Hinweis: Alle numerischen Long-Run-Abschnitte bis zum Force-Komponenten-Pilot
vom 2026-07-09 sind `legacy-sign`-Auditmaterial. Korrigierte Evidenz beginnt
mit `reports/kernels/corrected_sign/corrected_sign_q3_pilot_2026-07-09.md` und
`reports/kernels/corrected_sign/amplitude_hierarchy_corrected_sign_q3_2026-07-09.md`.

Kanonischer Start:

```powershell
python experiments/current/dynamics/long_run_metastability.py `
  --steps 10000000 `
  --seeds 1 `
  --conditions baseline `
  --dim 3 `
  --alpha 0.01 `
  --sample-every 1000 `
  --trace-every 100000 `
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
isoliert. Der Report liegt unter `reports/long_runs/controls/long_run_control_report_2026-07-01.md`.

M0-/Alpha-One-Kontrolle 2026-07-08 (`N=100,000,000`, Seeds `1..10`):

| Condition | stored mass | Memory-Horizon | Mean radius | Mean `D_occ` | median best residence | Lesart |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `m0_zero` | `0` | `600` | `212.678` | `1.819` | `8000` Updates / `80 alpha^{-1}` | Null-Feld-Kontrolle, diffundiert weit |
| `alpha_one` | `1` | `6` | `212.678` | `1.819` | `8000` Updates / `8000 alpha^{-1}` | seedgleich zu `m0_zero`; Selbstgradient verschwindet |

Lesart: `alpha=1` ist fuer den symmetrischen selbstzentrierten Kernel effektiv
eine Negativkontrolle, nicht ein konfiniertes Ein-Schritt-Memory-Regime. Report:
`reports/long_runs/m0_axis/long_run_m0_alpha_one_results_2026-07-08.md`.

Matched-Deposition-Pilot 2026-07-08 (`N=100,000`, Seeds `1..5`, Slow Python):

| condition | score median | sample radius median | memory radius median | memory roundness median | Lesart |
| --- | ---: | ---: | ---: | ---: | --- |
| `baseline` | `0.857` | `0.362` | `0.097` | `0.767` | kompakter Delta-Referenzlauf |
| `matched_deposition` | `0.714` | `1.535` | `0.244` | `0.668` | `legacy-sign`: confined, aber breiter/schwaecher |
| `eta_zero` | `n/a` | `5.167` | `0.622` | `0.380` | Negativkontrolle |

Lesart: `matched_gaussian` ist die konservative positive Schreib-/Lese-
Kernel-Variante. Ohne Steifigkeitsrenormierung reduziert die normierte Faltung
in `d=3` die lokale Kraftskala um etwa Faktor `5.66`; der faire naechste Test
ist daher curvature-renormalized matching. Reports:
`reports/kernels/deposition/matched_deposition_kernel_pilot_2026-07-08.md` und
`reports/knot_scores/v0_5_controls/knot_score_v0_5_matched_deposition_100k_2026-07-08.md`.

M0-Achsenpilot 2026-07-10 (`N=100,000`, Seeds `1..5`, korrigiertes Vorzeichen,
`A_att=8`, Score v0.5):

| M0 | score median | residence gain median | sample radius median | memory radius median | memory dimension median | Lesart |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `0.5` | `0.286` | `1.227` | `3.632` | `0.439` | `2.001` | kompakter als Kontrolle, aber keine starke Residence |
| `1.0` | `0.286` | `0.613` | `3.132` | `0.405` | `2.103` | nomineller Spezialfall, weiter schwacher Score |
| `2.0` | `0.286` | `0.971` | `2.596` | `0.408` | `2.204` | kompakter, aber noch kein starker KnotScore |

Lesart: `M0` ist ein echter Skalierungs-/Kopplungshebel und macht den aktiven
Lauf in diesem Slice kompakter. Der 100k-Pilot rechtfertigt aber keinen breiten
M0-Blindscan, weil Residence-Gain, Sample-Kompaktheit und Memory-Kompaktheit
die v0.5-Partial-Schwellen nicht gemeinsam erreichen. Report:
`reports/long_runs/m0_axis/m0_axis_knot_score_pilot_2026-07-10.md`.

Scalar-Haertung 1M 2026-07-10 (`N=1,000,000`, Seeds `1..5`, korrigiertes
Vorzeichen, Score v0.5):

| A_att | score median | candidate seeds | residence gain median | sample compactness median | memory compactness median | memory roundness gain median | memory dim median | Lesart |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `9` | `0.500` | `5/5` | `1.450` | `2.512` | `1.701` | `1.739` | `2.107` | Boundary-/Transition-Kontrolle |
| `20` | `0.857` | `5/5` | `1.237` | `18.929` | `5.960` | `2.161` | `2.712` | balanced compact candidate |
| `35` | `0.857` | `5/5` | `1.040` | `42.768` | `8.674` | `2.347` | `2.868` | tight/round memory-cloud candidate |

Lesart: Das korrigierte Skalarmodell erzeugt im 1M-Pilot seed-robuste kompakte
Memory-Clouds fuer `A_att=20..35`. Der offene Paper-I-Engpass ist jetzt
Residence-Skalierung mit `N`, nicht mehr die blosse Existenz kompakter
Memory-Clouds. Report: `reports/long_runs/scalar_hardening/scalar_hardening_q3_1M_2026-07-10.md`.

N-Skalierung korrigierter skalarer Kandidaten 2026-07-10 (`burn_in=0`,
`N=100k..3M`, Seeds `1..5`, Score v0.5):

| A_att | N range | score median | memory radius trend | raw D_occ trend | D_win trend | residence gain at 3M | Lesart |
| ---: | --- | ---: | --- | --- | --- | ---: | --- |
| `20` | `100k..3M` | `0.857` | `0.087 -> 0.092` | `1.110 -> 2.002` | `1.675 -> 2.016` | `1.584` | balanced compact candidate, Residence offen |
| `35` | `100k..3M` | `0.857` | `0.060 -> 0.060` | `1.042 -> 2.078` | `1.650 -> 2.084` | `1.684` | tighter memory cloud, Residence offen |

Lesart: Die korrigierten Kandidaten bilden kompakte Memory-Clouds schnell. Die
Dimensionen wachsen entlang N in Richtung etwa `2`, waehrend die Memory-Shape-
Dimension frueh nahe `2.7..3.0` liegt. Der offene Punkt ist nicht Formation,
sondern Residence-Konvergenz bzw. Residence-Messmethodik. Report und Plots:
`reports/long_runs/scalar_hardening/scalar_n_scaling_q3_2026-07-10.md`.

Residence-Observable ab 2026-07-10: Long-Run-JSONs enthalten neben
`residence_by_voxel_size` nun `center_residence.sample_center` und, falls die
Memory-Cloud nicht degeneriert ist, `center_residence.memory_center`. Beide
nutzen Ballradien relativ zum jeweiligen mittleren Cloud-Radius mit Faktoren
`1,2,4,8,16`. Die Summary berichtet den festen Primaerfaktor `2` als
`*_primary_max_run_memory_times` und `*_primary_inside_fraction`; der
unbeschraenkte Maximalwert ueber alle Faktoren bleibt nur in der Detail-Payload
als explorative Diagnose. Operativ ist vor allem `memory_center` relevant,
waehrend `sample_center` als Drift-/Pfadkontrolle mitlaufen darf. Diese Felder
sind fuer die naechste N-Skalierung bis `1e8` massgeblich, weil sie weniger
grid- und translationsabhaengig sind als das reine Voxelmaximum.

Dynamischer Center-Trace ab 2026-07-11: Mit `--trace-every N` schreibt
`long_run_metastability.py` zusaetzlich `diagnostics.dynamic_center_trace`.
Gemessen werden die zeitlokale Memory-Center-Spur, RMS-Radius, Distanz des
aktuellen Punkts zum Center, co-moving Inside-Fraction, maximale co-moving
Run-Laenge in Memory-Zeiten und Center-Drift pro Memory-Zeit. Fuer `N=3e8`
ist `--trace-every 100000` ein praktikabler Startpunkt: etwa 3000 Tracepunkte
pro Case, also genug fuer Drift/Residence ohne riesige JSONs. Degenerierte
Nullradius-Traces zaehlen nicht als co-moving Residence-Evidenz.

Trace-Validation 2026-07-12: `--trace-points N --trace-spacing log` erzeugt
explizite logarithmische Trace-Zeitpunkte; bei nichtuniformen Traces werden
co-moving Run-Dauern zeitgewichtet. Der `N=3M`-Pilot fuer `A_att=20/35`, Seeds `1..5`,
zeigt, dass `dynamic_inside_fraction` und `dynamic_max_run` nicht als alleinige
Knotenkriterien taugen. `eta_zero` bleibt im eigenen grossen Memory-Ball
ebenfalls innen. Fuer Paper I sind daher dynamischer RMS-Radius,
radiusnormalisierte Center-Drift pro Memory-Zeit und Memory-Shape die
relevanten co-moving Metriken. Aggregation/Plots:
`experiments/current/dynamics/dynamic_center_trace_report.py`; Report:
`reports/long_runs/long_3e8/dynamic_center_trace_q3_N3M_2026-07-12.md`.

Hybrid-Trace-/Spin-Proxy-Erweiterung 2026-07-12: `--trace-points` plus
`--trace-spacing log` definiert die langfristige Trendspur. Optional fuegt
`--trace-every` zusammen mit `--trace-window-memory-times` ein gleichmaessig
abgetastetes Endfenster an. Nur dieses Fenster darf fuer lokale Geschwindigkeits-, Bivector- und Dephasierungswerte verwendet werden; logarithmische Differenzen
sind dafuer nicht zulaessig. Die Trace-Payload enthaelt `trace.positions`, und
`spin_proxy` dokumentiert `sample_count`, `sample_interval_memory_times`,
`window_span_memory_times`, Amplitude, Winkelgeschwindigkeit,
Achsenpolarisation, Achsen-Dephasierung und die rohe normierte Spin-Bivektor-
Autokorrelation. Wenn die erste `1/e`-Kreuzung schon beim ersten messbaren Lag
liegt, ist die Dephasierungszeit als Obergrenze `<= dt_mem` zu lesen. Der
`N=1M`-Pre-Run findet keine persistente Spinachse; der Befund ist eine
Negativkontrolle, kein Spin-/Photonclaim. Report:
`reports/long_runs/long_3e8/dynamic_center_spin_trace_q3_N1M_2026-07-12.md`.
Naechster Long-Trace-Standard: `N=30M`, `--trace-points 100`,
`--trace-spacing log`, `--trace-every 1`, `--trace-window-memory-times 100`,
keine neue Parameterachse.

Epsilon-Dynamic-Center-Sweep 2026-07-12: `epsilon_dynamic_center_sweep.py`
variiert nur `epsilon` fuer den korrigierten kompakten Referenzkandidaten
`A_att=35`, Seeds `1..3`, `N=100k`, gegen seedgleiche `eta_zero`-Kontrollen.
Der kurze Sweep zeigt ein v0.5-Score-Plateau ab etwa `epsilon=1.65e-6` bis
`epsilon=0.741`; bei `epsilon=2.72` kollabiert der aktive Lauf auf
`eta_zero`-aehnliche Metriken. Unterhalb `~1e-6` bleibt die Form skalenartig,
aber Shape-/Roundness-Gating ist teils degeneriert. Spin bleibt negativ:
Achsenpolarisation nahe null und Dephasierung nach einem Update. Report:
`reports/long_runs/epsilon/epsilon_dynamic_center_q3_Aatt35_N100k_2026-07-12.md`.

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
oder drift-dominierter. Report: `reports/kernels/epsilon/epsilon_step_balance_2026-07-01.md`.

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
`reports/kernels/epsilon/epsilon_floor_probe_2026-07-02.md` und
`reports/kernels/epsilon/epsilon_floor_visual_probe_2026-07-02.md`.

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
`figures/draft/kernels/kernel_shape_probe_2026-07-01.svg` und
`figures/draft/kernels/kernel_seed_probe_2026-07-02.svg`. Zusaetzlich liegen flexible
Varianten mit panel-eigener Skala unter
`figures/draft/kernels/kernel_shape_probe_flexible_2026-07-02.svg` und
`figures/draft/kernels/kernel_seed_probe_flexible_2026-07-02.svg`. Flexible Varianten
zeigen Form, nicht absolute Groesse.

Seedvergleich fuer den Baseline-Case:

| seed | mean radius | median step | turn mean | span xyz |
| ---: | ---: | ---: | ---: | --- |
| `1` | `0.233` | `0.1099` | `-0.342` | `1.01, 0.78, 0.87` |
| `2` | `0.318` | `0.1113` | `-0.351` | `1.08, 0.88, 1.16` |
| `3` | `0.387` | `0.1100` | `-0.346` | `0.76, 0.95, 1.54` |
| `4` | `0.474` | `0.1095` | `-0.340` | `1.75, 0.78, 0.97` |
| `5` | `0.214` | `0.1099` | `-0.343` | `0.85, 0.98, 0.67` |

Legacy-sign-Lesart: Die schwarze Linie in der Figur ist eine geglaettete
Rolling-Mean-Trajektorie; die farbige Linie ist der roh gesampelte Pfad
desselben Cases. Die Tabelle nutzt die alte Gradientenrichtung, in der
`A_rep` lokal bindend und `A_att` ein breiter Gegenkanal war. Deshalb sind
die dortigen `A_att=0`/`A_rep=0`-Vergleiche nur noch Auditmaterial fuer den
Vorzeichenfund. Unter der korrigierten Potentialkonvention muss der Shape-
Probe neu gerechnet werden; dann ist `A_rep` lokal repulsiv und `A_att` breit
attraktiv. Report: `reports/kernels/shape_and_memory/kernel_shape_probe_2026-07-01.md`.


## Knotenscore-Referenz

Die aktuelle Knotenscore-Dokumentation liegt absichtlich in diesem Katalog,
nicht als neue Einzelseite. Die Implementierung liegt in
`src/emergenz_knoten/knot_score.py`; der Report-Generator ist
`experiments/current/markov/knot_score_report.py`.

Der Score ist eine Evidenz-Scorecard, kein mathematischer Knotensatz. Er
bewertet eine aktive Bedingung seedweise gegen die passende `eta_zero`-
Negativkontrolle. Ein hoher Score bedeutet daher: diese Bedingung trennt sich
unter den gewaehlten Observablen von der no-feedback-Kontrolle. Er bedeutet
nicht automatisch stabile Teilchen, physikalische Masse oder einen
zweiskaligen Mechanismus.

Aktuelle produktive Variante ist v0.5:

| Komponente | Messgroesse | Schwellen |
| --- | --- | --- |
| Residence | beste Residence gegen `eta_zero`, in raw updates | partial `>=2`, pass `>=3` |
| Sample-Kompaktheit | `eta_zero`-Radius / Case-Radius | partial `>=3`, pass `>=5` |
| Voxel-Stabilitaet | min/max Residence ueber Voxelgroessen | partial `>=0.15`, pass `>=0.25` |
| Interne Dimension | `D_occ` bzw. gueltiges automatisches Fenster | partial `>=1.25`, pass `>=1.5` |
| Memory-Kompaktheit | `eta_zero`-Memory-Radius / Case-Memory-Radius | partial `>=2`, pass `>=3` |
| Memory-Rundheit | Case/Control-Achsenverhaeltnis | partial `>=1.2`, pass `>=1.5` |
| Memory-Formdimension | Case/Control-Memory-Dimension | partial `>=1.15`, pass `>=1.35` |

v0.5 unterscheidet sich von v0.4 vor allem dadurch, dass Residence in rohen
Updates verglichen wird und Memory-Kompaktheit nur bei nichtdegenerierter
Memory-Cloud zaehlt. Das verhindert, dass `alpha_one` oder `M0=0` durch
Skalierungsartefakte wie Knoten aussehen.
Score-Hygiene: Der Knotenscore bleibt ein metastabilitaetsbezogener Score. Fuer
andere Fragen sind separate, benannte Scorecards sinnvoll, z.B. `ModeScore`
fuer lag-stabile komplexe Slow-Modes, `PropagationScore` fuer ballistische oder
retardierte Antwort und `FormationScore` fuer Geburts-/Burn-in-freie Historien.
Diese Scores duerfen nicht rueckwirkend als Knotenscore ausgegeben werden.
## Knotenscore v0.3

Report vom 2026-07-02: `reports/knot_scores/v0_2_to_v0_4/knot_score_v0_3_2026-07-02.md`.

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

Shape-Pilot 1M vom 2026-07-02: `reports/knot_scores/v0_2_to_v0_4/knot_score_v0_3_shape_pilot_1M_2026-07-02.md`.

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

Report vom 2026-07-02: `reports/knot_scores/v0_2_to_v0_4/knot_score_v0_4_shape_pilot_1M_2026-07-02.md`.

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
stark bleibt. Die spaetere `rep_zero`-Kontrolle zeigt, dass dieser Fall tatsaechlich dispersiv ist; naechster Schritt sind direkte Kraftkomponenten statt ein weiterer reiner Parametersweep.

15-Seed-Erweiterung vom 2026-07-07:

| run | report | baseline median | single_scale median | reading |
| --- | --- | ---: | ---: | --- |
| 1M, Seeds `1..15` | `reports/knot_scores/v0_2_to_v0_4/knot_score_v0_4_seeds_1-15_1M_2026-07-07.md` | `0.857` | `0.857` | gleiche Scorelage |
| 100M, Seeds `1..15` | `reports/knot_scores/v0_2_to_v0_4/knot_score_v0_4_seeds_1-15_100M_2026-07-07.md` | `1.000` | `1.000` | gleiche Scorelage; Quellordner heisst `10M`, JSON sagt `100M`, dirty provenance |

Damit ist Feedback-Confinement robuster, aber der zweiskalige Baseline-Claim
schwaecher. Fuer Paper I ist ein ein- oder feedback-kernelbasierter
Confinement-Claim sauberer als ein spezifischer Zwei-Skalen-Claim.

Kontrollfester v0.5-Score vom 2026-07-08:
`reports/knot_scores/v0_5_controls/knot_score_v0_5_controls_100M_2026-07-08.md`.

v0.5 vergleicht Residence in rohen Updates statt in `alpha^{-1}` und laesst
Memory-Kompaktheit nur bei nichtdegenerierter Memory-Cloud zaehlen. Dadurch
fallen `m0_zero` und `alpha_one` korrekt zusammen.

| condition | n | score median | residence gain median | compactness gain median | memory valid | Lesart |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `baseline` | `15` | `1.000` | `6.667` | `14.767` | `15/15` | aktives Feedback-Confinement |
| `single_scale` | `15` | `1.000` | `8.500` | `15.344` | `15/15` | ebenso stark; kein Zwei-Skalen-Nachweis |
| `m0_zero` | `10` | `0.286` | `1.000` | `1.000` | `0/10` | Null-Feld-Kontrolle |
| `alpha_one` | `10` | `0.286` | `1.000` | `1.000` | `0/10` | Ein-Punkt-Memory degeneriert zu Nullkraft |


## KPI-Register fuer Scores

Die Scores sollen feste Fragen beantworten. KPIs duerfen je Score anders sein,
aber die Scorecard muss vor dem Parameterlauf feststehen.

### KnotScore: Metastabilitaet und Knotenform

Aktuell enthalten oder direkt verwandt:

| KPI | Status | Rolle |
| --- | --- | --- |
| Residence-Gain | in v0.5 | langlebige Rueckkehr/Verweildauer gegen `eta_zero` |
| Sample-Kompaktheit | in v0.5 | rohe Pfadausdehnung gegen Kontrolle |
| Voxel-Stabilitaet | in v0.5 | Schutz gegen Einzelvoxel-Artefakte |
| `D_occ` / Occupancy-Fenster | in v0.5 | interne Nicht-Kollaps-Dimension, kein externer 3D-Claim |
| Memory-Kompaktheit | in v0.5 | eigentliche Knotenform eher ueber Memory-Cloud als rohen Pfad |
| Memory-Rundheit | in v0.5 | anisotrope oder degenerierte Memory-Clouds abwerten |
| Memory-Formdimension | in v0.5 | covariance participation dimension der Memory-Cloud |

Weitere sinnvolle KnotScore-Kandidaten:

| KPI | Quelle | Warum relevant |
| --- | --- | --- |
| Center-Drift | Memory-Schwerpunkt, Residence-Voxel oder geglaettetes Antwortzentrum | Knoten sollten langsamer driften als die rohe Trajektorie |
| Radius-Stabilitaet | Blockweise Memory-/Sample-Radien | stabiler Knoten statt transienter Kollaps/Explosion |
| Survival/Hazard | Residence-Verteilung statt nur Maximum | trennt langlebige Tails von einzelnen Ausreissern |
| Force-Balance | `rep/att`, net-cos, Noise/Drift-Verhaeltnis | Mechanismus-KPI fuer korrigierte Kernel statt nur Geometrie |
| Hessian-/OU-Stabilitaet | lokale Hessian-Eigenwerte um Memory-Zentrum | verbindet Score mit Relaxations-/Stabilitaetsskala |
| Transfer-Spektralluecke | Markov-/Transferoperator | metastabile Menge sollte langsamen Modus plus Gap zeigen |
| CK-/Closure-Fehler | Chapman-Kolmogorov und AR-Residual | Score nur glaubwuerdig, wenn reduzierte Features ausreichend geschlossen sind |
| Seed-Passrate/IQR | Report-Ebene | Score sollte ueber Seeds tragen, nicht nur im Median gluecken |
| Parameter-Robustheit | lokale Nachbarschaft in `A`, `sigma`, `M0`, `lambda` | nachhaltiger als Einzelparameter-Treffer |

### Dimensionsmetriken einordnen

- `D_occ`: box-/occupancyartige interne Ausdehnung. Das ist aktuell die
  KnotScore-Dimensionskomponente.
- `D_cov`: covariance participation ratio der Sample-Cloud. Als
  `sample_shape.effective_dimension` ist es Diagnostik, aber nicht direkt
  v0.5-Scorekomponente.
- `memory_shape_dimension`: ebenfalls covariance participation ratio, aber auf
  der gewichteten Memory-Cloud. Diese Groesse ist in v0.5 ueber den
  Memory-Formdimension-Gain enthalten.
- `D_spec`: spektrale Dimension aus einer lokalen Kernel-/Graphstruktur. Sie
  ist implementiert, aber noch nicht stabil genug als KnotScore-Komponente.
  Sinnvoller Einsatz: als Reconciliation-/Geometrie-KPI oder als Peak-/Band-
  KPI in einem separaten Mode-/GeometryScore.

### ModeScore: oszillatorische oder quantenartige effektive Moden

Ein ModeScore sollte nicht Residence bewerten, sondern die Modenfrage:

| KPI | Idee |
| --- | --- |
| Slow complex pair | fuehrende komplexe Eigenwerte mit `|mu|` ueber Schwelle |
| Lag-stabile Frequenz | `omega = arg(mu)/lag_updates` bleibt ueber Lags stabil |
| Lag-stabile Daempfung | `Gamma = -log(|mu|)/lag_updates` bleibt ueber Lags stabil |
| Control separation | Unterschied zu `eta_s=eta_v=0`, shuffled-vector und `eta_v=0` |
| Residual/Closure | AR- oder Transfermodell residualarm genug |
| Phase coherence | Autokorrelation/PLV einer expliziten Phase oder Orientierung |
| Spectral peak | Peak in Frequenz-/Spektraldiagnostik, aber nur mit Kontrollabstand |

Ein Peak in `D_spec` waere nicht automatisch Mode-Evidenz. Er waere ein
Geometrie-/Skalenhinweis. Fuer ModeScore zaehlt ein reproduzierbarer Peak in
Frequenz, Eigenphase oder Autokorrelation staerker.

### PropagationScore: gerichtete Ausbreitung und Antwort

| KPI | Idee |
| --- | --- |
| MSD-Slope | diffusiv `~1`, ballistisch `~2`, subdiffus/konfiniert `<1` |
| Drift-Persistenz | Geschwindigkeits-/Orientierungsautokorrelation |
| Response-Lag | Stoerung an Knoten A, Antwort an Knoten B mit stabiler Verzogerung |
| Directionality | Antwort staerker entlang Kopplungsrichtung als quer dazu |
| Signal-to-control | Abstand gegen shuffled, `eta=0`, `M0=0` und Fernkopplungs-Ablation |
| Retardierungsrobustheit | Lag bleibt ueber Seeds und Distanzen konsistent |

### FormationScore: Geburt statt stationaerer Auswertung

| KPI | Idee |
| --- | --- |
| Time-to-compactness | Updates bis Memory-Radius unter Schwelle faellt |
| Early seed sensitivity | Streuung ueber Seeds in fruehen Memory-Zeiten |
| Capture probability | Anteil Seeds, die in Kandidatenregime eintreten |
| Overshoot/settling | Radius- oder Kraftantwort ueberschiesst und relaxiert |
| Burn-in-free provenance | `burn_in=0`, Formation nicht herausgeschnitten |

### Praktische Regel fuer Parameterstudien

Vor jeder `beta/M0/sigma/A`-Variation wird festgelegt:

1. Welche Scorecard? `KnotScore`, `ModeScore`, `PropagationScore` oder
   `FormationScore`.
2. Welche Kontrollen? Mindestens `eta_zero`/`M0=0` fuer KnotScore,
   `eta_s=eta_v=0`, `eta_v=0` und shuffled-vector fuer ModeScore.
3. Welche Pass-/Partial-Schwellen? Vor dem Sweep, nicht danach.
4. Welche Aggregation? Median/IQR und Seed-Passrate statt best seed.
5. Welche Parameterachse? Immer nur eine Hauptachse pro Scan, z.B. erst `M0`,
   dann `lambda`, dann `sigma`, dann Amplitudenverhaeltnis.

## Ballistische MSD-Probe

Report vom 2026-07-07: `reports/kernels/propagation/ballistic_kernel_probe_2026-07-07.md`.

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
| `reports/kernels/shape_and_memory/kernel_memory_photon_decision_2026-07-07.md` | Kernel, Memory und Photon-Track | Paper I als effektives Memory-Kernel-Confinement; Zwei-Skalen-Kernel optional; Photon-Track braucht erweiterten Zustand. |
| `reports/project/decisions/alpha_memory_mass_decision_2026-07-08.md` | Alpha, M0 und Ballistikschwelle | `beta=lambda_m M0`; Alpha-Scans kontrolliert ueber `lambda_m`, `M0`, Tail-Cutoff und `eta/eta_c`; Photon-Track erst nach komplexen/coarse-grained Moden. |
| `reports/project/governance/privacy_and_control_plan_2026-07-08.md` | Privacy und M0/Alpha-One-Kontrollen | Privacy-Policy und Kontrollplan; lokale private Klartexte entfernt, `m0_zero` und `alpha_one` bleiben Negativkontrollen. |
| `reports/kernels/deposition/deposition_kernel_audit_2026-07-08.md` | Deposition-Kernel-Audit | Delta ist die Baseline; finite `gaussian` und `matched_gaussian` sind jetzt als effektive Faltung implementiert. |
| `reports/kernels/deposition/matched_deposition_kernel_pilot_2026-07-08.md` | Matched-Deposition-Pilot | Normalisiertes Gaussian-Matching trennt von `eta_zero`, ist im 100k-Pilot aber breiter als Delta; naechster Test braucht Steifigkeitsrenormierung. |
| `reports/kernels/deposition/zero_mean_kernel_decision_2026-07-09.md` | Zero-Mean-Kernel | Kompensierter Zwei-Skalen-Kernel mit `int K=0`; erster Test bei `sigma_att/sigma_rep=1.5`. |
| `reports/kernels/deposition/zero_mean_matched_pilot_100k_2026-07-09.md` | Zero-Mean-/Matched-Pilot | Bei `sigma_att/sigma_rep=1.5` sind Baseline, Zero-Mean und renormiertes Matching praktisch deckungsgleich. |
| `reports/kernels/deposition/kernel_scale_ratio_and_rep_zero_controls_2026-07-09.md` | Scale-Ratio-/Rep-Zero-Kontrollen | Ratios `{1.5,2,3}` isolieren keinen Zero-Mean-Mechanismus; `rep_zero` dispergiert stark und klaert die aktuelle Vorzeichenkonvention. |
| `reports/knot_scores/v0_5_controls/knot_score_v0_5_rep_zero_q3_100k_2026-07-09.md` | Rep-Zero-Scorecard | `single_scale` bleibt baseline-artig, `rep_zero` ist die harte Dispersionskontrolle. |
| `reports/kernels/corrected_sign/force_component_q3_pilot_2026-07-09.md` | Force-Komponenten-Pilot | `legacy-sign`-Pilot, der den Vorzeichenfehler sichtbar machte. |
| `reports/kernels/corrected_sign/kernel_sign_convention_correction_2026-07-09.md` | Sign-Konvention | Korrigiert den Kernelgradienten; bisherige Long-Run-Evidenz ist `legacy-sign` und muss neu gerechnet werden. |
| `reports/kernels/corrected_sign/corrected_sign_q3_pilot_2026-07-09.md` | Corrected-sign q=3 | Historische Baseline `A_att=0.35` dispergiert; `rep_zero` bestaetigt den attraktiven Kanal. |
| `reports/kernels/corrected_sign/amplitude_hierarchy_corrected_sign_q3_2026-07-09.md` | Amplitudenhierarchie | Drift-Umschlag zwischen `A_att=3.5` und `9`; kompakte Kandidaten bei `A_att=9..35`, aber noch keine Long-Run-Knoten. |
| `reports/kernels/mode_probes/ar_mode_probe_corrected_candidates_2026-07-09.md` | AR-Modenprobe | Langsame Moden auf korrigierten Kandidaten bleiben reell; keine stabile komplexe Slow-Mode-Evidenz im skalaren Memory-Modell. |
| `reports/kernels/corrected_sign/transition_boundary_corrected_sign_q3_2026-07-09.md` | Transition Boundary | Zehn Seeds lokalisieren die korrigierte Driftgrenze bei `A_att ~= 7.9`, `chi ~= 0.88`. |
| `reports/long_runs/m0_axis/m0_axis_knot_score_pilot_2026-07-10.md` | M0-Achsenpilot | Bei `A_att=8` macht hoeheres `M0` die Laeufe kompakter, traegt im 100k-Pilot aber noch keinen starken v0.5-KnotScore. |
| `reports/long_runs/scalar_hardening/scalar_hardening_q3_1M_2026-07-10.md` | Scalar-Haertung q=3 1M | `A_att=20` und `35` tragen hohe v0.5-Kompaktheit/Memory-Shape-Scores; Residence-Skalierung bleibt der naechste Engpass. |
| `reports/long_runs/scalar_hardening/scalar_n_scaling_q3_2026-07-10.md` | Scalar-N-Skalierung q=3 | `A_att=20/35`, `N=100k..3M`, `burn_in=0`; kompakte Memory-Clouds bilden schnell, Residence bleibt Engpass. |
| `reports/long_runs/long_3e8/long_run_3e8_launch_2026-07-10.md` | 3e8-Launch | Hintergrundlaeufe fuer `A_att=20/35`, Seeds `1..5`, `N=300M`, mit Center-/Memory-Ball-Residence gestartet. |
| `reports/long_runs/long_3e8/long_run_3e8_results_2026-07-11.md` | 3e8-Resultate | v0.5-Score und Voxel-Residence tragen bei `A_att=20/35`; fixe finale Memory-Center-Residence zeigt Drift/Rezentering und motiviert dynamische Center-Diagnostik. |
| `reports/vector_memory/vector_memory_minimal_design_2026-07-09.md` | Vektorgedaechtnis | Minimalanforderungen fuer einen orientierten Memory-Kanal mit Slow-Mode- und Negativkontrollen. |
| `reports/vector_memory/vector_memory_pilot_initial_2026-07-10.md` | Vektormemory-Pilot | 2D-Transverse-Kurzpilot; komplexe AR-Moden erscheinen schon in `eta_v=0`, also noch kein isolierter Vektoreffekt. |
| `reports/vector_memory/vector_memory_eta_s_zero_control_2026-07-10.md` | Eta-Zero-Vektorkontrolle | Selbst `eta_s=eta_v=0` zeigt komplexe AR-Paare; komplexe Projektionsmoden sind daher noch keine Schwingungsevidenz. |
| `reports/vector_memory/vector_memory_alignment_control_2026-07-10.md` | Alignment-Vektorkontrolle | `alignment` vergroessert schwache/transitionale Radien eher; `A_att=20` bleibt kompakt und ueberwiegend real. |
| `reports/project/meta/repository_cleanup_2026-07-09.md` | Repository-Cleanup | Aktive Docs bleiben bei sieben Seiten; lokale private Klartextnotizen wurden entfernt. |

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
| Knotenstabilitaet | `experiments/current/knot_stability/*.py` | Trajektorien, Knotenvisuals | historische Parameter |
| Dimension Selection | `experiments/dimension_selection/DimensionsHeatmap*.py` | Dimension/Heatmaps | lange Laufzeiten |
| Zwei-Skalen-Kernel | `experiments/dimension_selection/two_scale_kernel/*.py` | Double-Kernel-Regime | unterschiedliche Konventionen |
| Fraktalanalyse | `experiments/fractal_analysis/archive_source/*.py` | Archivquelle `D_occ ~ 2.8` | alte CSVs ohne Seed-Spalten |
| Propagation Speed | `experiments/propagation_speed/PaperII3D_*.py` | Paper-II-Programm | Threshold-Robustheit offen |
| OU-Limit | `experiments/archive/ou_limit/*.py` | analytische Kontrollfiguren | schematisch |
| Legacy | `experiments/archive/legacy/scripts/highN_regime*.py` | historische High-N-Regime | nur gezielt starten |
