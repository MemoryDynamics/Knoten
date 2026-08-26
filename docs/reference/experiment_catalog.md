# Experiment-Katalog

Stand: 2026-08-21.

Diese Datei ist zugleich Experiment-Katalog, Reproduzierbarkeitsnotiz und
Long-Run-Plan. Sie ersetzt die alten Einzeldateien zu Reproduzierbarkeit,
Hardening und Long-Run-Metastabilitaet.

## Kanonische Entry-Points

| Datei | Thema | Status | Naechste Nutzung |
| --- | --- | --- | --- |
| `experiments/current/dynamics/long_runs/long_run_metastability.py` | Long-N-Metastabilitaetsdiagnostik | aktiv | Knotenscore v0.5, Center-/Memory-Ball-Residence, dynamischer `--trace-every` Memory-Center-Trace, `m0_zero`, `alpha_one`, `matched_deposition`, `zero_mean_two_scale` und weitere Ablationen |
| `experiments/current/dynamics/long_runs/stability_gate_audit.py` | Checkpoint-/Holdout-Stabilitaet | aktiv | vier Alterscheckpoints, spaeter Holdout und lokale Radiusfenster; retrospektive Methodik, keine Formationszeit |
| `experiments/current/dynamics/centering/dynamic_center_trace_report.py` | Aggregation und Plots fuer dynamische Center-/Spin-Traces | aktiv | Methodikreport fuer co-moving Radius, Drift/Radius, Memory-Shape und Spin-Proxy gegen `eta_zero` |
| `experiments/current/dynamics/long_runs/paper_i_evidence_table.py` | Paper-I-Evidenztabelle aus Long-Run-Summaries | aktiv | konservative Claim-Tabelle fuer co-moving scalar-knot Evidenz |
| `experiments/current/dimensions/aatt_transition_report.py` | A_att-Uebergang `d=3` vs. `d=10` | aktiv | Dimensions-Reconciliation, beta=0/M0=0-Referenzverweis und KPI-Kurven ueber `A_att` |
| `experiments/current/dimensions/dimension_claim_audit.py` | 3D-Dimensionsclaim-Audit | aktiv | Claim-Leiter, `D_p90`/`D_p95`, low-pass Center-Trace-Dimensionen und Paper-II-Reconciliation |
| `experiments/current/dimensions/dspec_sensitivity_report.py` | D_spec-Sensitivitaet | aktiv | Legacy-D_spec, symmetrische Heat-Kernel-Skalen, kNN-Skalen und Kovarianz-Surrogate fuer Paper-II-Guardrail |
| `experiments/current/dimensions/dspec_raw_snapshot_report.py` | Rohsnapshot-D_spec | aktiv | Heat-Trace-/Scale-Audit auf echten `memory_cloud.snapshot`-Punkten; Pilot-Gate vor Response-Rang |
| `experiments/current/dimensions/dimension_over_n_reproduction.py` | Dimensionen ueber N | abgeschlossen | drei gematchte Seeds an sechs Endpunkten; separates D_occ/D_win-Messkonvergenzgate markiert den gemischten Cadence-/Revisionssatz als nicht auswertbar |
| `experiments/current/dynamics/centering/epsilon_dynamic_center_sweep.py` | Epsilon-Sensitivitaet auf dynamischen Center-/Spin-Benchmarks | aktiv | kurze Schwellenfindung fuer Rauschskala vor laengeren Hybrid-Traces |
| `experiments/current/anchors/anchor_paper_pipeline.py` | Paper-0-Smoke mit Markov-Schicht | aktiv | schneller Sanity-Check |
| `experiments/current/anchors/anchor_sensitivity_analysis.py` | Seed-/Lag-/Voxel-/Kontroll-Sensitivitaet | aktiv | kurze Operator-Pipeline-Checks |
| `experiments/current/dynamics/epsilon/epsilon_step_balance.py` | Rauschen-vs-Drift-Updatebilanz | aktiv | gezielte Epsilon-/Glattheitsdiagnostik |
| `experiments/current/dynamics/epsilon/epsilon_floor_visual_probe.py` | flexible 3D-Visualisierung der Epsilon-Floor-Faelle | aktiv | Formvergleich bei extremen Skalen |
| `experiments/current/kernels/families/kernel_shape_probe.py` | 3D-Fuehrungskoordinatenplot fuer Kernelbreiten und Amplituden | aktiv | visuelle Shape-Diagnostik, keine Long-Run-Evidenz |
| `experiments/current/kernels/families/kernel_compensation_audit.py` | Zero-Integral-/Kruemmungs-Constraint | aktiv | analytische q-d-Map, exakter dreiskaliger Kompensator und lokale/Fernfeld-Profile |
| `experiments/current/kernels/controls/fixed_curvature_sigma_pilot.py` | kontrollierter Sigma-Verhaeltnis-Pilot | aktiv | `q={2,3,4}` bei festem `chi`, Seeds `1..5`, gemeinsame seedgleiche `eta_zero`-Kontrollen |
| `experiments/current/kernels/controls/three_scale_compensation_pilot.py` | breiter Zero-Integral-Kompensator | aktiv | q=3-Referenz gegen exaktes `int K=0`, Kruemmungsmatching, statisches Fernfeld und seedgleiche `eta_zero`-Kontrollen |
| `experiments/current/kernels/families/kernel_core_audit.py` | enger Kernel-Core-Audit | aktiv | logarithmischer Nahfeld-, Kraftkomponenten- und Kruemmungsvergleich; curvature-matched A_rep=0-Ablation |
| `experiments/current/kernels/families/log_taylor_kernel_audit.py` | LoG-/Taylor-Kernel-Audit | abgeschlossen | fester analytischer Vergleich von `(1,35)`, `(0,26)` und zero-mean LoG bei gleicher lokaler Kruemmung; trennt exaktes `A_eff=26` von der unbelegten `27/36`-Identifikation |
| `experiments/current/kernels/families/attractive_only_regime_scan.py` | dimensionsloser attraktiver Ein-Kernel-Scan | aktiv | A_att=0..40, gemeinsame eta=0-Kontrollen, lineare Relativradius-Referenz und matched (1,35)/(0,26)-Vergleich |
| `experiments/current/kernels/families/kernel_family_comparison.py` | Ein-/Zweiskalen-Familienvergleich | abgeschlossen | Rohamplituden- und `A_eff=A_att-9`-Achse, seedweise KPI-Kollapspruefung |
| `experiments/current/dynamics/long_runs/linear_long_run_reconciliation.py` | finite-memory Long-Run-Radiuscheck | abgeschlossen | vorhandene N=30M/300M-Slices gegen gespeicherte-Masse-Relativmodus pruefen |
| `experiments/current/dynamics/scaling/scalar_memory_continuum_limit_gate.py` | registrierter skalarer Finite-Tail-/Alpha-Grenztest | abgeschlossen, formal inadäquat | Seed-1--5-Erstlauf; G1/G2-Komponenten bestehen diagnostisch, bleiben aber durch den nicht interventionsspezifischen zeitversetzten Radius-G0 blockiert |
| `experiments/current/dynamics/scaling/scalar_memory_continuum_limit_reconciliation.py` | prospektive Kontinuumsgrenz-Reconciliation | abgeschlossen, lokaler konditionaler Pass | neue Seeds 6--10, simultane Branch-vs-Control-Radien, unveraenderte Tail-/Alpha-/Holdout-Gates; kontrollierter Relaxationsgrenzwert, kein Masse- oder Impulsclaim |
| `experiments/current/dynamics/scaling/scalar_memory_force_work_port_gate.py` | prospektiver skalarer Force-/Work-Port | abgeschlossen, overdamped Pass / endliche Traegheit negativ | neue Seeds 11--15; G0/G1/G2O pass, alle vier G2I-Komponenten fail; direkter Feedthrough, divergierende Impulsarbeit und diffusive Kurzzeit-MSD |
| `experiments/current/dynamics/scaling/scalar_memory_center_inertial_port_gate.py` | prospektiver Center-Force-/Work-Port | abgeschlossen, positiver effektiver Inertialpass | neue Seeds 16--20; f dc, aufgeloeste Rechteckpulse und Center-MSD; G0/G1/G2I pass, alle vier overdamped-Center-Komponenten fail; lokaler Port-/Readout-Claim, keine SI-Masse |
| `experiments/current/dynamics/scaling/scalar_memory_center_finite_h_port_a2.py` | finite-H Center-Port A2-Zertifikat | abgeschlossen, analytischer effektiver-Port-Pass | alle fuenf registrierten Zellen bestehen globalen Small-Gain-/Positive-Real-Bound und Grid-Sanitycheck; oeffnet nur B-star-Filtertests, nicht physisches B |
| `experiments/current/dynamics/scaling/scalar_memory_center_filter_scaling_bstar.py` | nichtphysischer Center-Filter-Skalierungstest B-star | abgeschlossen, Joint-Holdout-Pass | state-matched und reformed Fits ergeben tau-Exponent 1, mu-Exponent -1 und M0-Exponent 0; Holdout-Masse 3.99997 gegen Vorhersage 4. Bleibt Systemidentifikation und zaehlt nicht als physisches B. |
| `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_discovery.py` | prospektive native Rotating-wave-Discovery | abgeschlossen, finite-H-Existenzpass | analytische Kontinuumssuche mit Kontrollen, danach erste registrierte Verfeinerung bei festen nativen Parametern; Residual 4.53e-17, keine Stabilitaets- oder Masseaussage |
| `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_stability_gate.py` | Voll-FIFO-Quellenstabilitaet des eingefrorenen Rotating-wave-Kandidaten | abgeschlossen, lokaler numerischer Pass | 2400-dimensionaler mitrotierender Jacobian, zwei Arnoldi-Panels und drei Stoerungen ueber 5000 Updates; keine vollstaendige Spektraleinschliessung, Formation, Rausch- oder interne-S1-Aussage |
| `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_interval_certificate.py` | Intervallzertifikat des finite-H-Anchor-Roots | abgeschlossen, lokaler Existenz-/Eindeutigkeitspass | zwei Multipraezisionspanels, analytischer Jacobian und strikte Krawczyk-Einschluesse fuer die exakte finite Summe; lokale registrierte Box, kein globaler Root- oder Stabilitaetsbeweis |
| `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_refinement_ladder.py` | gematchte finite-H-Rootleiter | abgeschlossen, fuenf Roots zertifiziert / formaler Target-Fail | fuenf Zellen bei H alpha=12 und eta/alpha=15 bestehen alle lokalen Zertifikate; historische Entscheidung `certified-roots-nonconvergent`, weil der eingefrorene Kontinuumsguide zu Gain 15.016345 statt 15 gehoerte |
| `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_continuum_reconciliation.py` | prospektive Fixed-gain-Kontinuums-Reconciliation | abgeschlossen, Reconciliation-Pass | drei vorab fixierte Quadraturpanels loesen die nativen Grenzgleichungen bei eta/alpha=15; alle unveraenderten Skalierungsgates der vorhandenen Leiter bestehen, ohne den historischen Target-Fail umzubenennen |
| `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_foundation_audit.py` | kritischer Foundation-Audit der gesamten Rotating-wave-Kette | abgeschlossen, portability-scoped Reconciliation-Pass | neun kanonische Git-Blob-Hashes und sechs Revisionen aus Vollhistorie, unabhaengige 70-stellige finite-Summen-Replays aller fuenf Zellen, Tanh--Sinh-/Gauss--Legendre-Kontinuum und unabhaengiges Skalierungs-Replay; bewahrt Decimal-Fail und nichtportablen Zwischenpass und begrenzt Stabilitaet auf den Anchor |
| `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_l5_existence_scaling.py` | prospektiver L5-Existenz-/Skalierungsholdout | abgeschlossen, scoped L5-Pass | sechster lokaler Root bei alpha=0.00125, H=9600, eta=0.01875; beide 80/120-dps-Krawczyk-Panels, direkter 70-dps-Summen-Replay und alle signierten First-order-Gates bestehen; kein zweiter Intervallbackend oder Stabilitaetsclaim |
| `experiments/current/dynamics/rotation/scalar_memory_rotating_wave_l3_stability_gate.py` | prospektives P1-Nicht-Anchor-Stabilitaetsgate | abgeschlossen, lokaler numerischer Pass | L3 bei alpha=0.005, H=2400, eta=0.075; 32/48 groesste Ritzpaare mit getrennten Starts und sechs gespiegelte Stoerungsarme ueber 10000 Updates; keine vollstaendige Spektraleinschliessung, stabile Familie oder Formation |
| `experiments/current/topology/s1_control_pipeline.py` | kandidatenunabhaengige H0/H1-Methodenkontrollen | Methodentraining aktiv, keine Kandidatenanalyse | volle Vietoris--Rips-Persistenz auf Kreis/Hopf, Torus, Disk, Intervall, Dampfspirale und endlichem 12-Zyklus; eigener ungeoeffneter Validation-Seed, kein Cutoff und kein S1-/Phasenclaim |
| `experiments/current/topology/s1_p0_manifest_gate.py` | claim-spezifischer P0-Kandidaten-/Discovery-Freeze | S1 fail mit 27 Defekten; Center-Mechanik pass mit 0 Defekten | validiert Vollparameter, plattformstabile kanonische Text-/rohe Binaerhashes, Discovery und Confirmatory-Seals; oeffnet je Manifest nur D0 oder A. Der Center-Pass versiegelt D0--D5 explizit, der S1-Fail versiegelt den Ziellauf. |
| `experiments/current/kernels/controls/fixed_g_nonlinearity_slice.py` | vorregistriertes festes-g-R/L-Gate | abgeschlossen | `R_linear/L={0.03,0.1,0.3}`, fuenf Seeds, eta=0, unveraenderte Composite-Entscheidungsregel |
| `experiments/current/kernels/controls/fixed_g_scale_reconciliation.py` | Residence-/Score-Skalenaudit | abgeschlossen | feste Voxel gegen co-moving Residence trennen; post-hoc Lesart ohne Umklassifizierung |
| `experiments/current/kernels/field/field_equation_bridge.py` | Feldgleichungs-Bruecke | aktiv | exakter Gaussian/Heat-Semigroup-Check gegen nur langwellig gematchtes Relaxations-Diffusionsfeld |
| `experiments/current/kernels/field/local_field_operator_audit.py` | lokale Feldoperator-Basis | abgeschlossen | fester analytischer Gaussian-k4-, Zero-Mean-, Finite-k-Stabilitaets- und Ambient-Rang-Audit; kein Feldsweep |
| `experiments/current/kernels/field/write_read_reparameterization_audit.py` | Write-/Read-Faktorisierung | abgeschlossen | drei Seeds und je 10,000 Updates; Pfad-/Feld-/Gradientengleichheit bis `1.43e-14`; trennt Dirac-Identitaet von konstantem kraftfreiem Kernel |
| `experiments/current/kernels/field/active_scalar_delta_field_pilot.py` | aktives lokales Delta-Quellfeld | abgeschlossen | drei Seeds, Gaussian-/stable-finite-k-/active-, cubic-off-, source-off- und eta-zero-Arme plus Zeit-/Gitterkonvergenz; klassischer Mechanismuspass, nicht feedback-spezifisch |
| `experiments/current/markov/knot_score_report.py` | Scorecard fuer vorhandene Long-Run-JSONs | aktiv | Knotenscore v0.5 und Paper-I-Evidenzhygiene |
| `experiments/current/markov/long_run_trace_ar_report.py` | AR-Modendiagnostik auf gespeicherten Long-Run-Traces | aktiv | Block-Markov-/AR-Check auf reelle vs. komplexe Slow-Modes gegen `eta_zero` |
| `experiments/current/markov/feature_closure_report.py` | Feature-Closure auf gespeicherten Long-Run-Traces | aktiv | Leave-one-seed-out AR-Skill gegen shuffled und persistence controls |
| `experiments/current/dynamics/scaling/scalar_n_scaling_report.py` | N-Skalierung korrigierter skalarer Kandidaten | aktiv | Einschwing-/Residence-Skalierung fuer `A_att=20/35` |
| `experiments/current/dimensions/n_dependence_recheck_report.py` | N-Abhaengigkeits-Reconciliation | aktiv | Formation-Skalierung, `N=30M`-Referenz und Rohsnapshot-Pilot in einer Guardrail-Grafik |
| `experiments/current/reference/reference_experiment.py` | kleiner Referenzlauf | aktiv | Smoke-Test |
| `experiments/fractal_analysis/analyze_dimension_claim.py` | Audit des archivierten `D_occ`-Claims | aktiv | Claim-Register |
| `experiments/fractal_analysis/reproduce_dimension_pilot.py` | kleine/mittlere Reproduktion | aktiv | spaetere Dimensionshaertung |
| `experiments/fractal_analysis/plot_d_alpha_n_intensity.py` | d-alpha-N-Heatmaps aus Reproduktions-JSON | aktiv | Seed-/N-Dimensionsberichte |
| `experiments/current/memory/synchronization/calibration/weak_probe_response.py` | gepaarte externe Weak-Probe-Kalibrierung | aktiv | uniforme Vollrang-Negativkontrolle; Basis fuer lokalisierten eingefrorenen Quellknoten |
| `experiments/current/memory/synchronization/calibration/frozen_source_response.py` | gepaarter lokalisierter Frozen-Source-Pilot | aktiv | geklonte `N=1e8`-Quelle; `eta_cross=0`, `eta_zero`, feste Kreuzkopplung, zwei lokale Verschiebungsskalen; Fernfeld-Symmetrieaudit |
| `experiments/current/memory/synchronization/calibration/frozen_source_field_audit.py` | statischer Potential-/Kraftaudit | aktiv | reale Checkpoint-Felder gegen Punktmonopol; Kraftvorzeichen, Paritaetsrest, Tangentialanteil und interne Quellenaufloesung |
| `experiments/current/memory/synchronization/calibration/frozen_source_distance_ladder.py` | realisiert kalibrierte Frozen-Source-Distanzleiter | aktiv | sechs Abstaende in `R_mem`/`sigma_rep`; Common-Noise-Targetdeformation, Response-Rang und Linearitaetskontrolle |
| `experiments/current/memory/synchronization/calibration/scalar_cross_readout_resolution.py` | statischer Cross-Readout-Aufloesungstest | aktiv | getrennte Selbst-/Cross-Kernel; starre Hauptachsenorientierungen gegen Punktmonopol bei fester kalibrierter Zentrumantwort |
| `experiments/current/memory/synchronization/one_way/oriented_history_current_audit.py` | geordneter History-Current-Audit | abgeschlossen | negatives Polar-/Bivektor-Gate gegen Random-Sign-Null; waehlt eigenstaendig evolvierenden orientierten Zustand |
| `experiments/current/memory/synchronization/one_way/oriented_vector_one_way_gate.py` | passiver eigenstaendiger Vektormemory-Kanal | abgeschlossen | 6/6 Pass gegen channel-off, globalen Flip, 16 Random-Sign-Nullen und Ein-Schritt-Kontrolle; konstruiertes Mechanismusgate, kein Physikclaim |
| `experiments/current/memory/synchronization/one_way/oriented_vector_fixed_pair_distance_gate.py` | feste Kopplung ueber unabhaengige Vektormemory-Paare | abgeschlossen | 6/6 zyklische Paare bestehen Nah-, Kontroll-, Shape- und Distanzgate; Instantanreadout und Gauss-Abschwaechung bleiben Modellinputs |
| `experiments/current/memory/synchronization/mediation/local_oriented_mediator_gate.py` | lokale orientierte Mediatorarchitekturen | abgeschlossen | Relaxations-Diffusion und Telegraph bestehen je 5/5 Holdouts; eingesetzte Transportregeln bleiben mechanistisch unbestimmt |
| `experiments/current/memory/synchronization/mediation/oriented_source_mediator_identifiability.py` | autonome Source-/Transfer-Identifizierbarkeit | abgeschlossen | 6/6 Sources bestehen; beide Regeln sind breitbandig unterscheidbar, aber persistent/Ein-Schritt-Kontrast 0.951..1.008 zeigt keine Persistenzspezifitaet |
| `experiments/current/memory/synchronization/mediation/dynamic_common_source_mediator_gate.py` | dynamischer Common-Source-Mediator-Holdout | abgeschlossen, negativ | beide Regeln 6/6 Response-/Shape-/Distanzpass; robuste Trace-Trennung nur 4/6 statt 5/6, daher keine Mechanismusauswahl |
| `experiments/current/memory/synchronization/one_way/signed_cross_channel_pilot.py` | signierter skalarer Frozen-Source-Kanal | aktiv | kompensierter Cross-Kernel; bitgenaue Null-/Produktarme, Label-Flip, `eta_zero` und Nondestruktionskontrolle |
| `experiments/current/memory/synchronization/one_way/one_way_dynamic_source_pilot.py` | einseitig dynamische Source mit gepaarten Kontrollen | aktiv | N100M-Checkpoint, 50-Memory-Time-Stationaritaetsfenster, Shape-Tensoren, frozen/free/eta-zero/unlaunched und relationale Phasengates |
| `experiments/current/memory/synchronization/one_way/one_way_interaction_age_audit.py` | N-Abhaengigkeit einer dauerhaften One-Way-Wechselwirkung | aktiv | common-prefix Auswertung bei `+20k..+3M`; Target-Radius, Shape-Spektrum und Kontrollabstand vor einem laengeren oder reziproken Lauf |
| `experiments/current/memory/synchronization/reciprocity/reciprocal_full_knot_gate.py` | synchron reziproker Vollknotenabgleich | abgeschlossen, negatives Modengate | `N=100M`, fuenf common-noise Fortsetzungen, fester Gain; direkte Bindung/Relaxation ohne komplexe Segmentmode |
| `experiments/current/memory/synchronization/reciprocity/retarded_reciprocal_full_knot_gate.py` | reziproker Vollknoten ueber festen Telegraph-Kanal | abgeschlossen, negatives Modengate | Mediator/Response/Shape 5/5, aber alle 80 rohen Segmentfits reell; retardierte Bindung schwaecher als direkt, kein komplexer beobachtbarer AR(1)-Modus |
| `experiments/current/memory/synchronization/reciprocity/same_law_reciprocal_jacobian_audit.py` | reife Self-/Cross-Hessians unter identischem Gesetz | abgeschlossen, formal inconclusive | `eta=0.15` bleibt reell; direkt gemessene `G,C(R)` statt Frequenzfit; `C-G` wechselt ueber feste Distanzen das Vorzeichen |
| `experiments/current/memory/synchronization/reciprocity/same_law_common_scale_followup.py` | ein gemeinsamer Self-/Cross-Gain | abgeschlossen, lokale Eligibility | bei `R=sigma_rep` gemeinsames stabiles komplexes Eta-Intervall `0.0009965..0.0026549` ueber 13 Richtungsfaelle; noch keine Kraftbilanz |
| `experiments/current/memory/synchronization/reciprocity/same_law_affine_balance_gate.py` | affiner Rest an lokal komplexen Geometrien | abgeschlossen, negativ | alle vier Abstandsgruppen 0/13; kompakte Self-Konfinierung und endlicher Pair-Kraftnullpunkt desselben Zweigauss-Kernels sind inkompatibel; kein Low-g-Pilot |
| `experiments/current/memory/closure/continuity_constrained_memory_gate.py` | lokales Dichte-Strom-Memory ohne externe Orientierung | abgeschlossen, strukturell mit Grenzen | sechs Identitaeten bestanden; longitudinale komplexe Pole oberhalb exakter Schwelle, aber keine statische Kraftbilanz, transversale Phase oder Dimensionsselektion; kein Pilot |
| `experiments/current/memory/closure/dynamic_green_kernel_selection_gate.py` | separater adjungierter Gradientenmediator `(m,p)` | abgeschlossen, struktureller Modellkandidat | zwoelf Gates; nicht kanonisches rho oder P3.8a-j; exakte Residueninversion, `u*=1.0387`, Barriere `3.91920 ell`, lineares Minimum `6.99092 ell`; keine Knotensimulation oder Koeffizientenselektion |
| `experiments/current/memory/synchronization/reciprocity/quasistatic_two_knot_discrimination.py` | P3.8c starre Vollmemory-Paardiskrimination | abgeschlossen, konditionaler Pass | ein d3-Seed bei N100M; entgegengesetzte Kraftvorzeichen bei `R=5 ell`, Action/Reaction und zweiter-Ordnung-Punktgrenze; keine Dynamik, kein Gain-Fit, keine Mechanismusselektion |
| `experiments/current/memory/synchronization/reciprocity/dynamic_two_knot_mediator_gate.py` | P3.8d diskrete `(m,p,R)`-Energie- und Zwei-Quellen-Dynamik | abgeschlossen, konditionaler Existenzpass | Source-work/Damping/Cross-off/Zeitschritt bestanden; `R0=5,8` erreichen Basin nahe `6.99`; Punktquellen, gesetztes `nu=1`, UV-sensitive Fruehtransienten, keine Closure aus `z=(x,rho)` |
| `experiments/current/memory/closure/emergent_modal_state_gate.py` | historisches P3.8e Finite-`k`-Gate | superseded-methodologically-inconclusive | Rohantwort bleibt Auditmaterial; freies/gedaempftes AR(2) redundant und Panel-Hankel-Rang durch Residuen verzerrbar |
| `experiments/current/memory/closure/emergent_modal_state_reconciliation.py` | korrigierte P3.8e-Identifikation | abgeschlossen, Null nicht verworfen / holdout-limited | active/eta0 getrennt, sichtbares Readout withheld, gemeinsame Ziele, korrigierter Hankeloperator; 0/5, alle gepoolten Pole reell, Memory-Holdoutenergie 0.2..0.8%, kR-Inputbasis stark kollinear |
| `experiments/current/memory/representations/curate_p38f_state_bundle.py` | kuratiertes P3.8f-Fuenf-State-Bundle | abgeschlossen | vollstaendige N=3M-Finite-Memory-Zustaende, Quell-/Checkpoint-Hashes und validierte Altersgewichte fuer Seeds 1..5 |
| `experiments/current/memory/closure/p38f_canonical_write_gate.py` | P3.8f-a kanonischer zero-net Write-Port | abgeschlossen, G0 pass / G1 inconclusive | gespiegelte Trajektorienpulse, zwei Staerken, drei Achsen, eta=0 und no-kick; nach Translationsabzug 0/5 informative relative/Kraft-Holdouts, daher G2/G3 blockiert |
| `experiments/current/memory/synchronization/reciprocity/measurement_closure_relative_noise_gate.py` | P3.2 Mess-Closure, Relative Noise und Langhorizont-Hankel-Audit | abgeschlossen | gemeinsame Zielzeiten; alle 45 gepaarten Designzellen verschlechtern sich, drei unabhaengige Seed-Mediane stimmen im Vorzeichen ueberein, Rang waechst ohne Plateau und hochrangiger Trend ist nicht kontrollgetrennt |
| experiments/current/memory/synchronization/reciprocity/hankel_pole_identity_cli.py | P3.2 gespeicherter DMD-Pol-Identity-Stoptest | abgeschlossen, negativ | vier korrelationsuebergreifende Kandidaten, aber null kontrollgetrennte Ueberlebende; Seeds 1/2 ueberlappen im Einwegarm, Seed 3 verfehlt 10/12 |
| `experiments/current/memory/synchronization/mediation/source_local_linear_gate.py` | P3.2c source-lokales lineares Emissionsgate | abgeschlossen, negativ | exakter Telegraphkanal stabil, aber Offset-Knot-Residuum `3.54e-5` und Einweg-Polverschiebung `0.00622`; Stromsource noch schwacher, 0/3 Modenreduktionen bestehen |
| `experiments/current/memory/synchronization/reciprocity/p32_accumulation_control.py` | vorregistrierte P3.2-500k-Akkumulationskontrolle | abgeschlossen, negativ | zwei Zukunftsrauschpfade und vier Arme; starke Pfaddivergenz ist im Einwegarm nahezu gleich, daher keine kontrollgetrennte reziproke Akkumulation |
| `experiments/current/memory/synchronization/reciprocity/shape_multipole_eligibility_gate.py` | P3.2d autonomes Shape-Multipol-Eligibility-Gate | abgeschlossen, negativ | Baseline `Q` und `Delta Q/Delta tau` jeweils 0/5; Niederfrequenzpeak segmentinstabil und im `eta=0`-Arm staerker; kein Tensor-Mediator autorisiert |
| `experiments/current/memory/representations/reference_state_checkpoints.py` | vollstaendige Finite-Memory-Referenzzustaende | aktiv | saubere `N=1e8`, `d=3/10` Absprungzustande fuer gepaarte Folgearme |
| `experiments/current/memory/representations/spectral_rho_field_pilot.py` | O(M)-Fourier-Reprasentation des exponentiellen rho | abgeschlossen | Historien-/Kraftaequivalenz, epsilon-Stoppregel und Modenzahlgate |
| `experiments/current/memory/representations/relaxation_diffusion_field_pilot.py` | modeabhaengige Relaxations-Diffusionsfelderweiterung | abgeschlossen | feste Diffusionsarme `0/0.3L/1.0L` mit `nu=0`- und `eta=0`-Kontrollen |
| `experiments/current/memory/closure/low_mode_ar_feature_closure.py` | Low-Mode-/AR-Closure | aktiv | gepaarte Seeds, Realraumhistorie, Persistence/Shuffle, Box-/Modenzahlgate und N=1M-Bestaetigung |
| `experiments/current/memory/closure/reconcile_low_mode_ar_runs.py` | Short-/Long-Reconciliation | aktiv | gemeinsame Lags und vorregistrierte N-Stabilitaet fuer reelle versus komplexe Moden |
| `experiments/current/memory/closure/low_mode_identity_audit.py` | Feature-Eigenvektor- und Zeitsegmentaudit | aktiv | physische Subraumueberlappung, Match-Anteil und Raten-/Frequenzstabilitaet ueber Seeds und Segmente |
| `experiments/current/memory/closure/eta_zero_raw_mode_null_audit.py` | exakte rohe `eta=0`-Modenreferenz | abgeschlossen, negativ | N=1M-Kadenz; reeller Fourier-Zustandsblock, Rohfit-/Segmentleckage gegen archivierte ausgerichtete AR-Paare |
| `experiments/current/memory/representations/carrier_memory_metric_comparison.py` | Kovarianz-/Predictive-/RKHS-Metrik auf `h=p` | abgeschlossen, negativ | 0/6 zyklische Paare; lineare Tangente und Cadence stabil, aber absolute Metrikskala und Klassifikation nicht reconciliiert; oeffnet nur balancierte Vollmemory-Feature-Closure |
| `experiments/current/memory/closure/balanced_full_memory_feature_gate.py` | balancierte Vollmemory-Closure | abgeschlossen, negativ | generischer Rang-1-Delaymodus; Flat-/Age-Shuffle-identisch und schlechter Fern-Holdout; kein knotenspezifischer konjugierter Zustand |
| `experiments/current/memory/closure/inertial_vector_field_analytic_gate.py` | inertialer Vektorfeld-Strukturtest | abgeschlossen, konstruktiver Strukturpass | exakter klassischer Oszillator nach Einfuehrung von `(m,pi)`; keine Kopplung an den kanonischen Simulator und keine Parameteridentifikation |
| `experiments/cli.py` | kategorisierte Experimentsteuerung | aktiv | Einstieg in Skriptfamilien |
| `experiments/propagation_speed/ballistic_kernel_probe.py` | korrigierter Ein-Kernel-Ballistik-Track mit `eta/eta_c` | aktiv | Sanity-Check fuer skalare Photon-Analogien |

## Ressourcenbegrenztes rho-Feld

`spectral_rho_field_pilot.py` stellt das bestehende exponentielle skalare
Memory auf einer periodischen 1D-Box mit `M+1` komplexen Fourierkoeffizienten
dar. Bei `M=64` sind das 1040 Bytes pro Zustand. Die Implementierung ist gegen
die explizite Historie, pfadweise Kontraktion, Massenkonstanz, direkten
Gausskraftvergleich und `eta=0` getestet. Im Fuenf-Seed-Slice
`epsilon={1e-8,1e-6,1e-4}` bleibt `R/epsilon` bis rund `2e-9` relativ konstant;
32 bis 128 Moden liefern denselben dynamischen Radius bis etwa `1.6e-14`.
Kleinere epsilon-Werte werden in diesem Regime nicht weiter verfolgt. Report:
`reports/memory/representations/spectral_rho_field_pilot_2026-07-19.md`.

`relaxation_diffusion_field_pilot.py` erweitert genau eine Achse:

```text
rho_new_hat(k)=exp(-nu k^2)[(1-lambda)rho_hat(k)+lambda G_hat_x(k)].
```

`nu=0` ist bitgenau die alte Dynamik. Fuer Diffusions-RMS-Laengen pro
Memory-Zeit `0`, `0.3L`, `1.0L`, fuenf Seeds und seedgleiche `eta=0`-Kontrollen
steigt der aktive Medianradius glatt um Faktor `1.384`; active/control steigt
von `0.171` auf `0.240`, und der Feedback-Schritt pro epsilon sinkt von
`0.507` auf `0.311`. Dies ist kontrollierte Feldglaettung ohne isolierten
neuen Modus. Report:
`reports/memory/representations/relaxation_diffusion_field_pilot_2026-07-19.md`.

Die Low-Mode-Closure ist nun ausgefuehrt. Translation-invariante Moden und
Realraum-Stuetzstellen sind leave-one-seed-out vorhersagbar; die direkte
Realraumhistorie, 32/64/128 Moden und matched-resolution Boxen bestehen ihre
Darstellungsgates. Beim N=1M-Lauf bleiben die zwei gemeinsamen
interpretierbaren aktiven Lags mit -2.9 und +9.0 Prozent innerhalb des
10-Prozent-Gates. Der 5.8-Prozent-Unterschied der aggregierten Raten ist nur
deskriptiv, da die vollstaendigen Lag-Gitter abweichen. Das im Kurzlauf
explorativ ausgewaehlte Verhaeltnis 0.3 wurde fuer N=1M eingefroren.

Komplexe Nebenmoden sind negativ reconciliiert: Sie treten auch fuer `eta=0`
auf, ihre Frequenz driftet mit N um rund 55 Prozent, und Q faellt
`0.342 -> 0.140`. Naechster Einsatz ist Mode-Identity ueber Eigenvektoren,
Zeitsegmente und eine analytische lineare Kontrolle, nicht ein weiterer
Diffusionssweep. Reports:
`reports/memory/closure/low_mode_ar_feature_closure_2026-07-19.md`,
`reports/memory/closure/low_mode_ar_feature_closure_long_N1M_2026-07-19.md` und
`reports/memory/closure/low_mode_ar_long_run_reconciliation_2026-07-19.md`.
## Referenzzustands-Checkpoints

Der Checkpoint-Runner speichert nur den finalen augmentierten Zustand der
implementierten Finite-Memory-Naeherung. Bei `alpha=0.01`, `memory_factor=6`
und `max_memory=800` sind das `x_N`, 600 altersgeordnete Memory-Punkte und
600 Gewichte. Die vorherigen `N` Positionen werden nicht benoetigt. Die
gespeicherte Gewichtsmasse ist `1-(1-alpha)^600 ~= 0.9976`; der formale
unendliche exponentielle Schwanz bleibt eine bekannte Trunkierungsnaeherung.

Der Runner verlangt einen sauberen Worktree und schreibt Git-Revision,
Formation-Seed, Parameter, Updatealter und Array-Pruefsummen in jedes
pickle-freie NPZ. Folgeexperimente laden dasselbe `z_N` und verwenden fuer
alle verglichenen Arme eine neue explizite gemeinsame Zukunftsrauschfolge.

```powershell
python experiments/current/memory/representations/reference_state_checkpoints.py `
  --steps 100000000 `
  --dims 3,10 `
  --seeds 1 `
  --workers 2 `
  --epsilon 1e-4 `
  --eta 0.15 `
  --alpha 0.01 `
  --memory-mass 1 `
  --deposition-kernel delta `
  --sigma-rep 1 `
  --sigma-att 3 `
  --amplitude-rep 1 `
  --amplitude-att 35
```

Seed 1 je Dimension ist eine kanonische Entwicklungsreferenz, keine
Ensemble-Evidenz. Fuer Signifikanztests werden spaeter mindestens sechs,
vorzugsweise zehn unabhaengige Seedzustaende pro relevante Basin-/Score-Klasse
gebildet.

Der Lauf vom 2026-07-16 ist abgeschlossen. Beide Dateien wurden auf Revision
`e8f4af2` gebildet und mit Schema-/Checksum-Reload, Transformationsinvarianz
und exakt reproduzierbarem Paired-Branch-Replay geprueft. Der finale
`d=3`-Zustand besitzt `D_mem=2.860`, der `d=10`-Zustand `D_mem=9.431`; dies
ist eine Entwicklungsbasis und kein Dimensionsclaim. Report:
`reports/reference_states/scalar_reference_checkpoints_N100M_2026-07-16.md`.

## Long-Run-Metastabilitaet

Hinweis: Alle numerischen Long-Run-Abschnitte bis zum Force-Komponenten-Pilot
vom 2026-07-09 sind `legacy-sign`-Auditmaterial. Korrigierte Evidenz beginnt
mit `reports/kernels/corrected_sign/corrected_sign_q3_pilot_2026-07-09.md` und
`reports/kernels/corrected_sign/amplitude_hierarchy_corrected_sign_q3_2026-07-09.md`.

Stabilitaetsprotokoll 2026-07-30: Der kanonische `d=10`, `A_att=35`-Slice
verwendet `N={1M,3M,10M,30M}` als vier Alterscheckpoints und `N=300M` als
separaten Holdout. Alle 5 Seeds bestehen Radiusbereich `<=10%`, Radius-CV
`<=15%`, absoluten Radiustrend pro Dekade `<=5%`, normalisierte
Shape-Spektrum-TV `<=10%` und vier lokale Radiusfenster plus Holdout. Der
Befund ist retrospektiv-provisorisch: Legacy-Traces enthalten lokal keinen
zeitaufgeloesten Shape-Tensor und bestimmen nicht die erste Formationszeit.
Report: `reports/long_runs/stability/checkpoint_stability_gate_d10_A35_2026-07-30.md`.

Kanonischer Start:

```powershell
python experiments/current/dynamics/long_runs/long_run_metastability.py `
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
`experiments/current/dynamics/centering/dynamic_center_trace_report.py`; Report:
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
Long-Trace-Standard: `N=30M`, `--trace-points 100`, `--trace-spacing log`,
`--trace-every 1`, `--trace-window-memory-times 100`, keine neue Parameterachse.
Der abgeschlossene `N=30M`-Run fuer `epsilon=1e-4`, `A_att=20/35`, Seeds
`1..5`, gegen `eta_zero` bestaetigt die co-moving scalar-knot Evidenz. Der
staerkere Referenzkandidat ist `A_att=35`: kleinerer dynamischer Radius,
langsamere radiusnormalisierte Center-Drift, `D_mem ~=2.94` und Roundness
`~=0.843`. Spin bleibt negativ (`axis_polarization ~=0.01`, rohe
`L`-Dephasierung `<=dt_mem`). Report:
`reports/long_runs/long_3e8/dynamic_center_spin_trace_q3_N30M_eps1em4_2026-07-13.md`.

Paper-I-Evidenztabelle 2026-07-13: `experiments/current/dynamics/long_runs/paper_i_evidence_table.py` verdichtet den `N=30M`-Hybrid-Trace in eine konservative Claim-Tabelle. Fuer `A_att=35`, `epsilon=1e-4` ist der aktive Lauf im Median etwa Faktor `4.96` kompakter als `eta_zero`, und die radiusnormalisierte Center-Drift ist um etwa Faktor `7.33` getrennt. Raw Voxel-Residence bleibt eine Guardrail, aber keine Hauptakzeptanzmetrik. Report: `reports/long_runs/long_3e8/paper_i_evidence_table_N30M_eps1em4_2026-07-13.md`.

Long-Run-Trace-AR 2026-07-13: `experiments/current/markov/long_run_trace_ar_report.py` fittet Block-AR-Maps auf dem gleichmaessig abgetasteten Endfenster derselben `N=30M`-Laeufe. Komplexe Klassifikationen treten auch in `eta_zero` auf und sind nicht als aktiver skalarer Phasen-/Photonmodus isoliert. Fuer Paper I ist der Befund neutral bis negativ fuer Oszillationssprache, aber kompatibel mit Relaxations-/Kompaktheitsevidenz. Report: `reports/long_runs/long_3e8/long_run_trace_ar_modes_N30M_eps1em4_2026-07-13.md`.

Feature-Closure 2026-07-13: `experiments/current/markov/feature_closure_report.py`
prueft Leave-one-seed-out AR-Skill gegen shuffled und persistence controls. Der
aktive skalare Referenzlauf zeigt den staerksten Closure-Lift in
Shape-/Radius-Scalars (`AR R2 ~=0.50` bei `0.1` Memory-Zeiten), nicht im
Spin-Scalar. `eta_zero` kann hohe raw `R2` in Geometrie zeigen, aber oft als
Persistence-Effekt. Lesart: skalares Memory eignet sich fuer erste
Grobkoernung von Kompaktheit/Radius/Relaxation; Phasen-Sektoren bleiben
Vector-/Tensor-/Internal-Memory-Future-Work. Report:
`reports/long_runs/long_3e8/feature_closure_N30M_eps1em4_2026-07-13.md`.

A_att-Transition 2026-07-15: `experiments/current/dimensions/aatt_transition_report.py`
verdichtet die `N=10M`-Runs fuer `d=3` und `d=10` zu KPI-Kurven ueber
`A_att`. Der Report enthaelt die gematchten Punkte `A_att in {7,8,9,10,12,15}`
plus vorhandene Referenzen bei `20` und `35` und verweist explizit auf die
`beta=0`/`M0=0`-Kontrolle. Lesart: `D_cov`, `D_occ_window`, `D_mem` und
`D_spec_mem` sind unterschiedliche Messkanale; das Ergebnis stuetzt eine
Innen/Aussen-Reconciliation, aber keinen externen `d=3`-Claim. Report:
`reports/long_runs/scalar_hardening/aatt_transition_d3_d10_2026-07-15.md`.

Epsilon-Dynamic-Center-Sweep 2026-07-12: `epsilon_dynamic_center_sweep.py`
variiert nur `epsilon` fuer den korrigierten kompakten Referenzkandidaten
`A_att=35`, Seeds `1..3`, `N=100k`, gegen seedgleiche `eta_zero`-Kontrollen.
Der kurze Sweep zeigt ein v0.5-Score-Plateau ab etwa `epsilon=1.65e-6` bis
`epsilon=0.741`; bei `epsilon=2.72` kollabiert der aktive Lauf auf
`eta_zero`-aehnliche Metriken. Der `N=1M`-Bestaetigungsslice fuer
`epsilon in {1.65e-6,1e-4,0.015}` und `A_att=20/35` bestaetigt dieses Plateau;
`epsilon=1e-4` wurde fuer den `N=30M`-Run gewaehlt. Reports:
`reports/long_runs/epsilon/epsilon_dynamic_center_q3_Aatt35_N100k_2026-07-12.md`,
`reports/long_runs/epsilon/epsilon_confirm_q3_Aatt20_N1M_2026-07-12.md`,
`reports/long_runs/epsilon/epsilon_confirm_q3_Aatt35_N1M_2026-07-12.md`.

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

Die sieben numerischen Evidenzkomponenten stammen weiterhin aus v0.5.
Fuer neu erzeugte zeitaufgeloeste Checkpoints ist v0.6 das aktuelle
Zulassungsprotokoll:

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
v0.6 veraendert den numerischen v0.5-Score nicht. Es fuegt davor ein
Stationaritaetsgate ein, weil ein grosses Updatealter N allein keine
stationaere Knotenform beweist. Im ungestoerten Vorlauffenster werden der
Memory-Radius R und

    p_n = eig(S_n) / trace(S_n)

aus dem Memory-Shape-Tensor S_n gemessen. Der Checkpoint ist vorlaeufig
stationaritaetsgeeignet, wenn alle drei Bedingungen gelten:

1. relative Medianradiusdrift zwischen Fensterhaelften hoechstens 0.10,
2. Radius-Variationskoeffizient hoechstens 0.15,
3. Total-Variation der medianen normierten Eigenwertspektren hoechstens 0.10.

Die Schwellen sind vorregistrierte Pilottoleranzen, keine Naturkonstanten.
Rotation aendert p_n nicht und wird daher nicht als Formverlust gewertet.
Fuer Transport kommt eine getrennte gepaarte Diagnose hinzu:
symmetrischer Radiusfaktor hoechstens 2, mediane Spektraldistanz hoechstens
0.10 und q95 hoechstens 0.25. Damit sind kontrollierte Rotation und begrenztes
Atmen erlaubt; starre shape preservation wird nicht verlangt.

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
stark bleibt. Die spaetere `rep_zero`-Kontrolle und der Linearitaetsaudit ersetzen diese Zwischenlesart: direkte Kraftkomponenten und gematchte Ablationen isolieren keinen notwendigen Zweiskalenmechanismus.

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
| Shape-Stationaritaet | Eligibility-Gate in v0.6 | Vorlauf-Radius und normiertes Eigenwertspektrum; hohes N allein reicht nicht |

KnotScore v0.6 bewertet eine statistisch gebundene Identitaet, keine starre
Geometrie. Das normierte Eigenwertspektrum ist rotationsinvariant; begrenztes
Atmen und kohaerente Rotation sind daher zulaessig. Ein Knoten muss weder
gaussfoermig noch ringfoermig sein und auch keine permanente harmonische Mode
tragen. Dauerhafte oder intermittierende Atmungs-/Rotationssignale werden
getrennt im ModeScore geprueft.

Die aktuelle Halbfenster-/CV-Pruefung kann seltene Formverluste oder
Regimewechsel uebersehen. Vor einer KnotScore-v0.7-Aenderung werden deshalb
zunaechst nur auditierende Huellenmetriken protokolliert: Radius-Quantilfaktor,
Anteil und maximale Dauer von Shapespektrum-Ausreissern sowie Rueckkehrzeit in
die vorab definierte Huelle. Diese Groessen werden erst nach Kalibrierung gegen
Nullkontrollen zu Gates; sie werden nicht post hoc in laufende Scores
eingerechnet.

Weitere sinnvolle KnotScore-Kandidaten:

| KPI | Quelle | Warum relevant |
| --- | --- | --- |
| Center-Drift | Memory-Schwerpunkt, Residence-Voxel oder geglaettetes Antwortzentrum | Knoten sollten langsamer driften als die rohe Trajektorie |
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

#### ModeScore v0.2: intermittierende statt permanente Moden

Falls gekoppelte Knotendynamik ueberwiegend chaotisch ist und nur zeitweise
harmonisch wirkende Atmungs- oder Rotationsabschnitte erzeugt, ist ein einziges
AR-Modell ueber den gesamten Trace zu streng und zugleich artefaktanfaellig.
Die primaere Einheit ist dann ein vorab definiertes Modenereignis:

| KPI | Rolle |
| --- | --- |
| Event-Duty-Cycle und Ereignisrate | wie oft eine kontrollgetrennte Mode aktiv ist |
| Burst-Dauer / Survival | Persistenz innerhalb eines Ereignisses statt globale Dauerperiodizitaet |
| Within-event Frequenz und Q | Frequenzkonzentration nur im aktiven Segment |
| Within-event Phasenkontinuitaet | kohaerente Phase innerhalb, nicht zwingend zwischen Bursts |
| Frequenzverteilung ueber Fenster/Seeds | wiederkehrende Modenfamilie statt Best-Window |
| Event-triggered Average | typische Form-, Radius- oder Orientierungsantwort um den Modenbeginn |
| Kontroll- und Surrogatabstand | gegen channel-off, `eta_v=0`, Random-Sign sowie Block-/Phasenshuffle |
| Multiple-testing Korrektur | Schutz vor zufaelligen Peaks bei vielen Fenstern/Frequenzen |

Schwellen und Frequenzbaender muessen vor der Parametersuche feststehen. Eine
einzelne schoene Periode, das beste Zeitfenster oder ein Peak ohne
Surrogatabstand zaehlt nicht als positive Mode-Evidenz.

### Gemeinsames Feldgesetz statt knotenspezifischer Kernel

Dass verschiedene Knoten dasselbe Potentialgesetz erfahren, ist eine
Universality-/Interaction-Frage und keine KnotScore-Komponente. Dafuer muessen
mindestens Kopplung, Kernelregel und Zustandsupdate ueber unabhaengige
Formationszustaende fest bleiben. Unterschiedliche Knoten duerfen verschiedene
interne Zustaende oder Multipolmomente derselben Dynamik tragen; der Kernel
darf aber nicht pro Knotentyp nachjustiert werden.

Eine Taylorentwicklung eines effektiven Potentials um einen Zustand liefert
lokale Kruemmungen und nichtlineare Antwortkoeffizienten. Sie bestimmt weder den
fundamentalen Kernel noch begruendet sie bereits eine Quantenfeldtheorie. Vor
QFT-Sprache stehen deshalb feste-Kopplungs-, Distanz-, Reziprozitaets-,
Retardierungs- und Mehrknotenkontrollen sowie eine konsistente
Erhaltungs-/Bilanzstruktur.

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

## Attraktiver Ein-Kernel- und Linearitaetsgate

Der N=300k-Screening-Scan verwendet d=3, epsilon=1e-4, eta=0.15,
lambda=0.01, M0=1, Delta-Deposition, A_rep=0, A_att=0..40 und Seeds 1..5.
Jeder aktive Seed teilt seine Rauschfolge mit der eta=0-Kontrolle. A_att=0
ist bitgenau eta=0.

Die primaere x-Achse ist g_tau=eta M0 kappa/lambda; A_att wird nur als
sekundaere Achse gezeigt. Im Ein-Kernel-Modell ist
g=eta M0 A_att/L^2 die identifizierbare Kopplung. A_att, eta und M0 sind
aus der Trajektorie nicht getrennt bestimmbar.

Die Rohmetriken Radius, Drift/Radius, D_mem, Roundness und Compactness Gain
aendern sich glatt. Der groesste gerankte Schritt ist der exakte Nullarm
A_att=0 nach 1; danach fallen die Aenderungsscores monoton ab. Es gibt keinen
detektierten endlichen Phasenuebergang und keinen Grund fuer einen dichteren
N=1M-Scan um KnotScore-Schwellen.

Fuer A_att>=5 stimmt der gemessene dynamische Radius mit

    R_linear=sqrt(d) q epsilon / sqrt(1-q^2(1-g)^2)

im Median auf 0.94 Prozent, maximal 3.44 Prozent ueberein. Die
curvature-matched Faelle (A_rep,A_att)=(1,35) und (0,26) stimmen in allen
geprueften kontinuierlichen KPIs bis etwa 1e-8 relativ ueberein. Der naechste
Der Familienvergleich zeigt fuer q=3 exakt `A_eff=A_att-9`; nach dieser
Reparametrisierung kollabieren die Kurven. Die bisherige A_att-Grenze um 7.9
bleibt ein historischer Befund des rauschstaerkeren A_rep=1-Slices.

Die Reconciliation von neun aktiven N=30M/300M-Slices ergibt 0.76 Prozent
medianen und 1.16 Prozent maximalen finite-memory Radiusfehler. Im
vorregistrierten festen-g-Gate waechst der Radius von R/L=0.03 nach 0.3 in
allen fuenf Seeds 6.2 Prozent ueber die lineare Skalierung hinaus; D_mem und
Roundness bleiben stabil. Die Composite-Regel bleibt formal `inconclusive`.
Der post-hoc Skalenaudit zeigt, dass feste Voxel Residence und KnotScore
veraendern, waehrend co-moving Residence auch fuer eta=0 gesaettigt ist.
Lesart: schwache glatte Kernelkorrektur, kein isolierter metastabiler Ast.

Die Feldgleichungs-Bruecke trennt zwei Aussagen: Ein Gausskernel ist exakt ein
Heat-Semigroup-Snapshot in einer Hilfskoordinate. Ein physisches
Relaxations-Diffusionsfeld hat dagegen einen Helmholtz/Yukawa-Greenkernel,
muss in den augmentierten Zustand aufgenommen werden und ist eine neue
Modellklasse.

## Entscheidungsnotizen

| Datei | Thema | Lesart |
| --- | --- | --- |
| `reports/project/decisions/s1_phase_mass_falsification_program_2026-08-16.md` | S1-Phase und Masse-Falsifikation | Claim-spezifischer Programm-Charter: S1-P0 bleibt ohne Kandidat geschlossen; Center-P0 oeffnet nur A. A identifiziert aus dem vorhandenen additiven x-Input keinen eindeutigen physischen Port, waehrend der mathematische passive Center-Port bestehen bleibt. |
| `reports/project/meta/reviews/s1_phase_mass_falsification_program_review_2026-08-16.md` | zweiter Referee-Pass des S1-/Masse-Charters | Als Programmgrenze und fuer kandidatenunabhaengige Methodenarbeit geeignet; der S1-P0 blockiert weiterhin jeden S1-Ziellauf. Diskreter p-Zyklus ist nicht S1, Raw-cloud-Permutation ist Invarianz statt Null, Seed ist Replikationseinheit und offene Impulsbilanz schliesst Feld/Bath ein. |
| `reports/topology/s1_control_pipeline_2026-08-16.md` | synthetischer S1-Topologie-Smoke-Test | Method-training-only: erwartete Ein-/Zwei-Generator-Kontrollen und absichtlich gefaehrlicher endlicher 12-Zyklus; keine Schwellenkalibrierung, keine Kandidatendaten, Validation-Split ungeoeffnet. |
| `reports/project/meta/preregistration/s1_candidate_p0_audit_2026-08-16.md` | ausgefuehrter P0-Kandidaten-/Provenienz-Audit | `P0-fail-no-eligible-candidate-record`: kein eindeutiger neuer Parametersatz mit kompletter Discovery-Provenienz; 27 maschinenlesbare Defekte, D0/D1 blockiert. Alte komplexe Eligibility-, AR- und Quenchpunkte bleiben quarantiniert. |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_discovery_2026-08-20.md` | native Rotating-wave-Discovery | Prospektiver Existenzpass fuer einen rauschfreien d=2-K0-H-Kreis bei alpha=0.01, H=1200, eta=0.15 und A_att=3.5. Zwei Residualkomponenten sowie Produktionskernel stimmen bis etwa 1e-16; Kontrollen 0, 9 und 35 ohne zulaessige radiale Nullstelle in der Suchbox. |
| `reports/project/meta/preregistration/scalar_memory_rotating_wave_d0_contract_2026-08-20.md` | Rotating-wave D0 | D0 besteht fuer die translationsreduzierte raeumliche SO(2)-Gruppenbahn. Nach ambientem Rotationsquotienten kollabiert sie zum Punkt; interne S1-Phase nicht etabliert. |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_stability_2026-08-20.md` | Voll-FIFO-Rotating-wave-Stabilitaet | Prospektiver lokaler numerischer Pass: fuehrender transversaler Multiplikator 0.99306035 in zwei Panels; drei kleine Stoerungen kontrahieren ueber 5000 Updates. Keine komplette Spektraleinschliessung oder Formation. |
| `reports/project/meta/reviews/scalar_memory_rotating_wave_stability_review_2026-08-20.md` | kritisches Rotating-wave-Stabilitaetsreview | Begrenzt den Befund auf einen vorbereiteten lokalen Attraktor. Ein-Schritt-Multiplikatoren sind keine Monodromie eines nachgewiesenen ganzzahligen Periodenorbits; Horizon, Basin, Rauschen, interne Phase, Arbeit und Masse bleiben offen. |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_interval_certificate_2026-08-21.md` | finite-H-Root-Intervallzertifikat | Strikter Krawczyk-Einschluss in 80 und 120 Stellen zertifiziert genau einen Root in der registrierten lokalen Box; Vorzeichen und beide erforderlichen Gains enthalten den nativen Zielwert. |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_refinement_ladder_2026-08-21.md` | gematchte Rootleiter | Alle fuenf Zellen sind lokal zertifiziert und bilden eine First-order-Cauchyfolge. Der vorregistrierte Vergleich zum falschen Gain-Guide verfehlt zwei Richardson-Gates und behaelt formal `certified-roots-nonconvergent`. |
| `reports/project/meta/reviews/scalar_memory_rotating_wave_refinement_ladder_review_2026-08-21.md` | kritisches Rootleiter-Review | Trennt starke zellweise Evidenz vom formalen Target-Fail und weist den bereits im Discovery-JSON sichtbaren Gain-Mismatch 15.016345 gegen exakt 15 aus. |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_continuum_reconciliation_2026-08-21.md` | Fixed-gain-Kontinuums-Reconciliation | Prospektiver Post-result-Pass: R_inf=0.9431133068 und Omega_inf=1.5855700777 bei exakt eta/alpha=15; alle urspruenglichen Skalierungsgates bestehen mit deutlicher Marge. |
| `reports/project/meta/reviews/scalar_memory_rotating_wave_continuum_reconciliation_review_2026-08-21.md` | kritisches Kontinuums-Reconciliation-Review | Wertet den korrigierten Grenzast als starke numerische First-order-Evidenz, nicht als Intervall-/All-alpha-Beweis oder neue Holdout-Replikation; historische Leiterentscheidung bleibt unveraendert. |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_l5_existence_scaling_2026-08-21.md` | prospektiver L5-Existenz-/Skalierungstest | `l5-existence-scaling-pass`: sechster lokaler Root, unabhaengiger Punktsummen-Replay und signierte L5/L4- sowie Differenzquotienten nahe 0.5; oeffnet nur die Prospektierung genau einer Nicht-Anchor-Stabilitaetszelle. |
| `reports/project/meta/reviews/scalar_memory_rotating_wave_l5_existence_scaling_review_2026-08-21.md` | kritisches L5-Review | Bestaetigt komfortable Krawczyk-, Korridor- und Skalierungsmargen, begrenzt den Pass aber auf lokale computerassistierte Existenz unter `mpmath.iv`; zweiter Intervallbackend, Stabilitaet, Formation, internes S1 und Interaktionen bleiben offen. |
| `reports/project/meta/preregistration/scalar_memory_rotating_wave_l3_stability_protocol_2026-08-22.md` | prospektives P1-L3-Stabilitaetsprotokoll | Zelle, zwei Arnoldi-Starts, 32/48 Panels, sechs gespiegelte Stoerungen, 50 Memory-Zeiten sowie Pass/Fail/Inconclusive vor dem ersten L3-Spektrum eingefroren. |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_l3_stability_2026-08-22.md` | P1-L3-Nicht-Anchor-Stabilitaet | `numerically-stable-source-pass`: fuehrender transversaler Multiplikator 0.99649340 stimmt in beiden Panels ueberein; alle sechs Stoerungsarme kontrahieren, exakter Arm bleibt unter 2.23e-14. |
| `reports/project/meta/reviews/scalar_memory_rotating_wave_l3_stability_review_2026-08-22.md` | kritisches P1-L3-Review | Haelt lokale numerische Stabilitaetsevidenz an einer zweiten Skala aufrecht, weist aber Paneltrunkierung, unvollstaendige Spektraleinschliessung, duennes lokales Stoerungsensemble und getrennte Mechanik aus; oeffnet nur P2. |
| `reports/project/meta/reviews/scalar_memory_loop_center_linearization_audit_2026-08-25.md` | P2-Linearisierungs-Audit | Trennt exakte nichtlineare Kreisexistenz, lokalen P1-Jacobian und exakten linearen Center-Readout. Falsifiziert den skalaren Ursprungsschluss fuer L3 wegen negativem \(g_H\) und waehlt den vollen FIFO-Tangentialoperator als lokale Vergleichstheorie. |
| `reports/project/meta/preregistration/scalar_memory_loop_center_p2_protocol_2026-08-25.md` | prospektives P2-Loop--Center-Protokoll | Friert Kandidat, zwei zero-net Wellenformen, drei Amplituden, Vorzeichen-/Richtungs-/Phasenkontrollen, Tangentenfehler, quadratische Resttermskalierung und D0-Recovery vor der ersten Zielantwort ein. |
| `reports/dynamics/rotation/scalar_memory_loop_center_p2_2026-08-25.md` | P2 lokale Loop--Center-Antwort | `loop-center-matrix-local-fail`: volle Tangentenantwort, Resttermskalierung und Kontrollen bestehen deutlich; alle Arme scheitern nur an der absoluten Tail-Slope-Grenze. |
| `reports/project/meta/reviews/scalar_memory_loop_center_p2_review_2026-08-25.md` | kritisches P2-Review | Haelt den formalen Fail aufrecht. Post hoc sind alle gespeicherten Tail-Steigungen negativ und monoton fallend; das absolute Kriterium misst Flatness statt Drift. Keine Uebertragung der Filtermasse und kein P3. |
| `reports/project/meta/preregistration/scalar_memory_loop_center_p2r_long_recovery_protocol_2026-08-25.md` | P2-R Sign-sensitive Long-Recovery-Protokoll | Outcome-informierte Reconciliation mit unveraendertem L3-Kandidaten und 16 alten Armen; friert drei neue disjunkte Fenster bis 20 Memory-Zeiten, signierte Steigungen, Abklingraten, Checkpoint-Peak- und numerische-Floor-Kontrollen vor weiterem Targetzugriff ein. |
| `reports/dynamics/rotation/scalar_memory_loop_center_p2r_long_recovery_2026-08-25.md` | P2-R lange Loop--Center-Rueckkehr | `p2r-sign-sensitive-long-recovery-pass`: 120 alte Metriken und acht Checkpoints exakt reproduziert; alle 48 neuen Fenster zeigen negative Steigung und aufgeloeste Abklingrate, Final-/Checkpoint-Peak maximal `4.4103e-6`. Historischer P2-Fail unveraendert. |
| `reports/project/meta/reviews/scalar_memory_loop_center_p2r_long_recovery_review_2026-08-25.md` | kritisches P2-R-Review | Haelt den outcome-informierten Pass fuer Rueckkehr einer vorbereiteten L3-Schleife aufrecht und oeffnet nur P3 Formation/Basin. Keine unabhaengige Replikation, keine eindeutige Pol-/Massenzuordnung und keine physische Portherleitung. |
| `reports/project/meta/preregistration/scalar_memory_rotating_wave_p3_formation_basin_protocol_2026-08-26.md` | prospektives P3 Formation/Basin-Protokoll | Trennt sechs target-informierte Basin-Arme von vier target-blinden Formationsarmen, friert Eintritt, 15-Memory-Time-Dwell, Phase, Spiegelung sowie eta=0-/achirale Negativkontrollen vor jeder P3-Fortsetzung ein. |
| `reports/dynamics/rotation/scalar_memory_rotating_wave_p3_formation_basin_2026-08-26.md` | P3 L3 Formation und sampled basin | `p3-formation-basin-pass`: alle zehn nichtkreisfoermigen Arme erreichen spaetestens nach 9.4 Memory-Zeiten den L3-Zielorbit und verweilen bis Memory-Zeit 60; alle Kontrollen bestehen. |
| `reports/project/meta/reviews/scalar_memory_rotating_wave_p3_formation_basin_review_2026-08-26.md` | kritisches P3-Review | Haelt finite-ensemble attraction aus fuenf Geometrien in zwei gesetzten Chiralitaeten aufrecht und oeffnet nur P4. Kein offener Basin-Ball, keine generische/spontane Formation, Mechanik oder Masse. |
| `reports/project/meta/preregistration/scalar_memory_center_mechanics_p0_audit_2026-08-16.md` | Center-Mechanik P0 | `P0-pass-center-effective-mechanics`: kompletter K0-Center-Kandidat, alle Seeds 1--20 als Discovery quarantiniert, neue Seeds und Transferzelle versiegelt; 0 Defekte, nur A autorisiert, D0--D5 ohne S1-Kandidat versiegelt. |
| `reports/project/meta/reviews/scalar_memory_center_physical_port_gate_a_2026-08-16.md` | Center Gate A: physische Portherleitung | Physischer Center-Port nicht identifiziert, mathematischer passiver Port bleibt. Ein x-konjugierter Port hat f dx=f dc+f dr; ein effektives U_ext(c,Q) transformiert jedoch zur selben additiven x-Gleichung. Ohne mikroskopischen Aktuator und finite-H-Grenzledger bleiben B/C/E/F1 blockiert. |
| `reports/kernels/shape_and_memory/kernel_memory_photon_decision_2026-07-07.md` | Kernel, Memory und Photon-Track | Paper I als effektives Memory-Kernel-Confinement; Zwei-Skalen-Kernel optional; Photon-Track braucht erweiterten Zustand. |
| `reports/project/decisions/alpha_memory_mass_decision_2026-07-08.md` | Alpha, M0 und Ballistikschwelle | `beta=lambda_m M0`; Alpha-Scans kontrolliert ueber `lambda_m`, `M0`, Tail-Cutoff und `eta/eta_c`; Photon-Track erst nach komplexen/coarse-grained Moden. |
| `reports/project/governance/privacy_and_control_plan_2026-07-08.md` | Privacy und M0/Alpha-One-Kontrollen | Privacy-Policy und Kontrollplan; lokale private Klartexte entfernt, `m0_zero` und `alpha_one` bleiben Negativkontrollen. |
| `reports/kernels/deposition/deposition_kernel_audit_2026-07-08.md` | Deposition-Kernel-Audit | Delta ist die Baseline; finite `gaussian` und `matched_gaussian` sind jetzt als effektive Faltung implementiert. |
| `reports/kernels/deposition/matched_deposition_kernel_pilot_2026-07-08.md` | Matched-Deposition-Pilot | Normalisiertes Gaussian-Matching trennt von `eta_zero`, ist im 100k-Pilot aber breiter als Delta; naechster Test braucht Steifigkeitsrenormierung. |
| `reports/kernels/deposition/zero_mean_kernel_decision_2026-07-09.md` | Zero-Mean-Kernel, historisch | Vor korrigierter Sign-/Kruemmungsanalyse; der spaetere Constraint-Audit zeigt die Unvereinbarkeit von lokaler Rueckstellung und `int K=0` im breiten zweiskaligen Attraktionskernel. |
| `reports/kernels/deposition/zero_mean_matched_pilot_100k_2026-07-09.md` | Zero-Mean-/Matched-Pilot | Bei `sigma_att/sigma_rep=1.5` sind Baseline, Zero-Mean und renormiertes Matching praktisch deckungsgleich. |
| `reports/kernels/deposition/kernel_scale_ratio_and_rep_zero_controls_2026-07-09.md` | Scale-Ratio-/Rep-Zero-Kontrollen | Ratios `{1.5,2,3}` isolieren keinen Zero-Mean-Mechanismus; `rep_zero` dispergiert stark und klaert die aktuelle Vorzeichenkonvention. |
| `reports/kernels/compensation/kernel_compensation_constraint_audit_2026-07-18.md` | Kernelkompensations-Constraint | Exakter Nachweis: fuer `q>1` sind `a=q^-d` und lokale Rueckstellung `a>q^2` zweiskalig disjunkt; definiert Fixed-chi-Slice und breiten dritten Kompensator. |
| `reports/kernels/compensation/fixed_curvature_sigma_pilot_d3_N1M_2026-07-18.md` | Fixed-curvature-Sigma-Pilot | `q={2,3,4}`, `chi=35/9`, `N=1M`, Seeds `1..5`: gepaarte KPI-Spannen maximal `1.65e-8`, da `R_mem/sigma_rep<=2e-4`; separate Breiten sind im kompakten Ast nicht identifizierbar. |
| `reports/kernels/compensation/three_scale_zero_mean_pilot_d3_N1M_2026-07-18.md` | Drei-Skalen-Zero-Integral-Pilot | Exaktes `int K=0`, Kraftwechsel bei `r/sigma_rep~=10.91` und lokales Kruemmungsmatching; gematchte Fuenf-Seed-KPIs stimmen bis `2.2e-11` relativ mit q=3 ueberein. |
| `reports/kernels/core/kernel_core_audit_2026-07-18.md` | enger Core-Audit | A_rep=1 ist bei R_mem/sigma_rep ungefaehr 2e-4 kein aktiver repulsiver Kern; (0,26) ist die curvature-matched Ablation zu (1,35). |
| `reports/kernels/core/attractive_only_regime_scan_d3_N300k_2026-07-18.md` | attraktiver A_att=0..40-Scan | Glatter linearer Relaxationsast, kein endlicher Phasenuebergang; A_rep im aktuellen Regime bis etwa 1e-8 relativ nicht identifizierbar. |
| `reports/kernels/core/kernel_family_comparison_d3_N300k_2026-07-19.md` | Kernel-Familienvergleich | Rohachsen sind exakt um neun Amplitudeneinheiten verschoben; auf A_eff kollabieren die seedweisen KPIs bis maximal 6.4e-6 relativ. |
| `reports/kernels/core/log_taylor_kernel_audit_2026-07-28.md` | LoG-/Taylor-Kernel-Audit | LoG liefert bei gematchter lokaler Kruemmung einen exakt zero-mean, abklingenden Nullkernel. `26` folgt exakt aus der bisherigen Kruemmung; `27` und `36` treten nur unter einer zusaetzlichen unbelegten Identifikation auf, `29` gar nicht. |
| `reports/long_runs/scalar_hardening/linear_long_run_reconciliation_2026-07-19.md` | Long-Run-Linearitaet | Neun aktive N=30M/300M-Slices liegen maximal 1.16 Prozent vom finite-memory Radius entfernt; eta=0 zeigt die Grenze des Absolutbenchmarks. |
| `reports/dynamics/limits/scalar_memory_continuum_limit_gate_2026-08-15.md` | registrierter Grenztest, Erstlauf | Formal `experiment-inadequate`: der zeitversetzte Kontrollradius verfehlt G0; G1/G2-Komponenten bleiben trotz bestandener numerischer Schwellen blockiert. |
| `reports/dynamics/limits/scalar_memory_continuum_limit_reconciliation_2026-08-15.md` | prospektive Grenztest-Reconciliation | Alle korrigierten Gates bestehen mit Seeds 6--10; Branch/Control-Radien `0.999606..1.000398`, Finite-H-Fehler etwa `1e-5`, Holdout-Kontinuumsfehler `0.003006`. Nur scaling-konditionale reelle Relaxation, keine emergente Masse. |
| `reports/dynamics/limits/scalar_memory_force_work_port_gate_2026-08-16.md` | skalarer Force-/Work-Port | G0, G1 und G2O bestehen; G2I scheitert in allen vier Komponenten. Holdout: Feedthrough 1, post-pulse Geschwindigkeit/J -3.990101, alpha W/J^2 1, MSD-Slope 0.959048. Negative finite-inertial Signatur nur fuer den kanonischen additiven Port. |
| `reports/dynamics/limits/scalar_memory_center_inertial_port_gate_2026-08-16.md` | skalarer Center-Inertial-Port | G0, G1 und alle elf positiven Center-Inertial-Komponenten bestehen; overdamped-Center 0/4. Holdout m=0.996239, gamma=5.002630, Center-MSD-Slope 1.972302. Sichtbares x bleibt overdamped; passive lokale Center-Realisierung, kein physischer Masseclaim. |
| `reports/project/meta/reviews/scalar_memory_center_mass_referee_audit_2026-08-16.md` | Referee-Audit zu Center und Masse | Major revision fuer jeden physischen Masseclaim: zweite Ordnung ist Zustandselimination, m=1 folgt aus \(\tau=\mu=1\), c ist bisher Source-/Sink-Memory-Centroid und x keine operationalisierte Phase. Port-, Skalen-, Kompositions- und Impulsgates bleiben offen. |
| `reports/kernels/nonlinearity/fixed_g_RL_d3_N300k_A26_2026-07-19.md` | festes-g-R/L-Gate | Vorregistriert formal inconclusive; seed-stabile 6.2 Prozent Radiusabweichung, aber stabile Memory-Shape. |
| `reports/kernels/nonlinearity/fixed_g_scale_reconciliation_d3_N300k_A26_2026-07-19.md` | Residence-Skalenaudit | Feste Voxel sind radiusabhaengig; co-moving Residence ist fuer aktiv und eta=0 gesaettigt. Keine unabhaengige Metastabilitaetsstuetze. |
| `reports/kernels/field/field_equation_bridge_2026-07-18.md` | Feldgleichungs-Bruecke | Exakte Heat-Hilfsdarstellung des Gausskerns; physisches Relaxations-Diffusionsfeld nur low-k-gematcht und eigener Markov-Zustand. |
| `reports/kernels/field/local_field_operator_audit_2026-07-29.md` | Lokaler Feldoperator-Audit | Eingeschraenkte Ableitungsbasis; Gaussian-k4-Match, `s0=0`-Zero-Mean, Finite-k-Schwelle bei `a2=-2` und exakte `H I_d`-Ambient-Rang-Null. Keine Quantisierungs- oder d=3-Evidenz. |
| `reports/kernels/field/write_read_reparameterization_audit_2026-07-30.md` | Write-/Read-Reparametrisierung | Exakte lineare Faktorisierung in drei Seeds numerisch bestaetigt; maximale Pfad-, relative Feld- und Gradientenfehler `7.11e-15`, `2.25e-15`, `1.43e-14`. Keine neue Felddynamik. |
| `reports/kernels/field/active_scalar_delta_field_pilot_2026-07-31.md` | aktives Delta-Quellfeld | Zeit-/Gitterfehler `6.12e-7`/`7.50e-11`; beschraenkte aktive `k=1`-Mode, cubic-off-Divergenz und exakte source-off-Null. Eta-zero bildet dasselbe Muster, daher nur klassische Finite-k-Musterbildung. |
| `reports/memory/representations/spectral_rho_field_pilot_2026-07-19.md` | spektrales rho-Gate | Exakte Historien-/Kraftkontrollen, O(M)-Zustand, lineare Epsilon-Skalierung und 32/64/128-Modenkonvergenz. |
| `reports/memory/representations/relaxation_diffusion_field_pilot_2026-07-19.md` | Diffusionsfeld-Pilot | Glatte Feldglaettung fuer drei vorab festgelegte Laengen; kein neuer Ast. |
| `reports/memory/closure/low_mode_ar_feature_closure_2026-07-19.md` | Low-Mode-Closure | Fuenf Seeds, Realraum-/Aufloesungsgates und Closure; komplexe Paare nicht eta-null-spezifisch. |
| `reports/memory/closure/low_mode_ar_feature_closure_long_N1M_2026-07-19.md` | N=1M-Modenlauf | 10,000 Memory-Zeiten; aggregierte reelle Rate bleibt von eta=0 getrennt, komplexe Nebenmoden bleiben in eta=0. |
| `reports/memory/closure/low_mode_ar_long_run_reconciliation_2026-07-19.md` | Short-/Long-Reconciliation | Zwei gemeinsame aggregierte aktive Raten bleiben unter 10 Prozent; komplexe Frequenz driftet 55 Prozent und scheitert dem Kontrollgate. |
| `reports/memory/closure/low_mode_identity_audit_2026-07-20.md` | Mode-Identity-Audit | Reelle Kandidaten verfehlen Match-/Ratenstabilitaetsgate; komplexe aktive und eta-zero Subraeume ueberlappen >0.9999. |
| `reports/memory/closure/eta_zero_raw_mode_null_audit_2026-07-31.md` | exakte Rohmoden-Null | Roher `eta=0`-Operator sowie gepoolte und seedweise N=1M-Fits bleiben reell; nur kleine Segmentleckage, daher bestehende komplexe Paare als Darstellungs-/Fitmoden klassifiziert. |
| `reports/knot_scores/v0_5_controls/knot_score_v0_5_rep_zero_q3_100k_2026-07-09.md` | Rep-Zero-Scorecard | `single_scale` bleibt baseline-artig, `rep_zero` ist die harte Dispersionskontrolle. |
| `reports/kernels/corrected_sign/force_component_q3_pilot_2026-07-09.md` | Force-Komponenten-Pilot | `legacy-sign`-Pilot, der den Vorzeichenfehler sichtbar machte. |
| `reports/kernels/corrected_sign/kernel_sign_convention_correction_2026-07-09.md` | Sign-Konvention | Korrigiert den Kernelgradienten; bisherige Long-Run-Evidenz ist `legacy-sign` und muss neu gerechnet werden. |
| `reports/kernels/corrected_sign/corrected_sign_q3_pilot_2026-07-09.md` | Corrected-sign q=3 | Historische Baseline `A_att=0.35` dispergiert; `rep_zero` bestaetigt den attraktiven Kanal. |
| `reports/kernels/corrected_sign/amplitude_hierarchy_corrected_sign_q3_2026-07-09.md` | Amplitudenhierarchie | Drift-Umschlag zwischen `A_att=3.5` und `9`; kompakte Kandidaten bei `A_att=9..35`, aber noch keine Long-Run-Knoten. |
| `reports/kernels/mode_probes/ar_mode_probe_corrected_candidates_2026-07-09.md` | AR-Modenprobe | Langsame Moden auf korrigierten Kandidaten bleiben reell; keine stabile komplexe Slow-Mode-Evidenz im skalaren Memory-Modell. |
| `reports/kernels/corrected_sign/transition_boundary_corrected_sign_q3_2026-07-09.md` | Transition Boundary | Zehn Seeds lokalisieren die korrigierte Driftgrenze bei `A_att ~= 7.9`, `chi ~= 0.88`. |
| `reports/long_runs/m0_axis/m0_axis_knot_score_pilot_2026-07-10.md` | M0-Achsenpilot | Bei `A_att=8` macht hoeheres `M0` die Laeufe kompakter, traegt im 100k-Pilot aber noch keinen starken v0.5-KnotScore. |
| `reports/long_runs/scalar_hardening/scalar_hardening_q3_1M_2026-07-10.md` | Scalar-Haertung q=3 1M | Historischer Zwischenstand mit hohen v0.5-Kompaktheit/Memory-Shape-Scores; spaeter durch die lineare Radiusreconciliation enger eingeordnet. |
| `reports/long_runs/scalar_hardening/scalar_n_scaling_q3_2026-07-10.md` | Scalar-N-Skalierung q=3 | `A_att=20/35`, `N=100k..3M`, `burn_in=0`; kompakte Memory-Clouds bilden schnell, Residence bleibt Engpass. |
| `reports/long_runs/scalar_hardening/n_dependence_recheck_2026-07-16.md` | N-Abhaengigkeits-Recheck | `N=100k..3M`, `N=200k`-Rohsnapshot-Pilot und `N=30M`-Referenz in einer Grafik; `N=200k` ist nur Pipelinecheck, Memory-Shape bleibt qualitativ konsistent. |
| `reports/long_runs/long_3e8/long_run_3e8_launch_2026-07-10.md` | 3e8-Launch | Hintergrundlaeufe fuer `A_att=20/35`, Seeds `1..5`, `N=300M`, mit Center-/Memory-Ball-Residence gestartet. |
| `reports/long_runs/long_3e8/long_run_3e8_results_2026-07-11.md` | 3e8-Resultate | v0.5-Score und Voxel-Residence tragen bei `A_att=20/35`; fixe finale Memory-Center-Residence zeigt Drift/Rezentering und motiviert dynamische Center-Diagnostik. |
| `reports/long_runs/long_3e8/dynamic_center_spin_trace_q3_N30M_eps1em4_2026-07-13.md` | N30M-Hybrid-Trace | Historischer Skalar-Referenzslice; Spin-Proxy negativ und Radius spaeter als linearer Finite-Memory-Modus erklaert. |
| `reports/long_runs/long_3e8/paper_i_evidence_table_N30M_eps1em4_2026-07-13.md` | Paper-I-Evidenztabelle | Co-moving Radius, Drift/Radius, Memory-Dimension und Roundness trennen `A_att=35` klar von `eta_zero`; keine Spin-/Photon-/Masseclaims. |
| `reports/dimensions/ambient_memory/memory_shape_boundary_2026-07-13.md` | 3D-Memory-Shape-Grenze | Historische Shape-Beobachtung; `D_mem ~=2.94` wird im linearen isotropen 3D-Regime als erwartete Ambient-Geometrie gelesen, nicht als Selektionshinweis. |
| `reports/dimensions/ambient_memory/ambient_memory_shape_sweep_launch_2026-07-13.md` | Ambient-Dimension-Launch | Paper-II-Brueckentest fuer `d=4,5,7,10,13,20`; aggregiert `D_mem`, ungewichtete Sample-/Memory-`D_spec`, Roundness, Radius und Drift gegen `eta_zero`. |
| `reports/long_runs/scalar_hardening/aatt_transition_d3_d10_2026-07-15.md` | A_att-Transition d3/d10 | `D_cov` und `D_mem` trennen sich im d10-kompakt-Ast; `beta=0`/`M0=0`-Referenz ist verlinkt; Paper-II-Reconciliation, kein Selektionsclaim. |
| `reports/dimensions/claims/dimension_claim_audit_2026-07-15.md` | 3D-Dimensionsclaim-Audit | `D_mem`/`D_p90`/`D_p95` stuetzen keinen ambient-unabhaengigen 3D-Claim; auch die fruehere Teaser-Lesart ist durch den Linearitaetsaudit ersetzt. |
| `reports/dimensions/sensitivity/dspec_sensitivity_2026-07-15.md` | D_spec-Sensitivitaet | Legacy-D_spec ist skalenempfindlich; spaetere Rohsnapshots und Response-Rang-Kontrollen bestaetigen keinen robusten externen `D_spec ~=3`-Claim. |
| `reports/dimensions/raw_snapshots/dspec_raw_snapshot_2026-07-15.md` | Rohsnapshot-D_spec-Pilot | `N=200k`-Pilot validiert den echten Snapshot-Auswertepfad; Heat-Trace-`D_spec` reproduziert noch kein robustes Nahe-3-Signal; langer Rohsnapshot-Retest bleibt Gate vor Response-Rang. |
| `reports/dimensions/raw_snapshots/dspec_raw_snapshot_retest_2026-07-16.md` | Rohsnapshot-D_spec-Retest | `N=200k` plus `N=3M`, `d=3/10`; Shape- und Heat-Trace-Dimension bleiben getrennt, der spaetere Response-Rang ist isotrop voll ambient-rangig. |
| `reports/response/calibration/weak_probe_calibration_2026-07-16.md` | uniforme Weak-Probe-Kalibrierung | Vollstaendige `N=3M`, `d=3/10`, Seeds `1..5` Memory-Zustaende; Zentrumantwort isotrop vollrangig, Formantwort nicht seed-reproduzierbar, Probestarken linear und nichtdestruktiv. |
| `reports/reference_states/scalar_reference_checkpoints_N100M_2026-07-16.md` | kanonische N100M-Referenzzustaende | Checksum-validierte vollstaendige Finite-Memory-Zustaende fuer `d=3/10`, Seed 1; reproduzierbare Absprungbasis fuer Frozen-Source- und spaetere Mehrknotenarme. |
| `reports/response/calibration/frozen_source_pilot_2026-07-16.md` | Frozen-Source-Clone-Pilot | Geklonte `N=100M`-Quelle bei `1 sigma_rep`; exakte Nullkontrolle und isotroper voller Ambient-Rang, kein externer 3D-Befund. |
| `reports/response/calibration/frozen_source_field_audit_2026-07-17.md` | Frozen-Source-Feldaudit | Der aktuelle `A_att=35`-Kern ist auf allen geprueften Radien attraktiv; reale d3/d10-Quellen sind fuer den Cross-Kernel bereits bei `5 R_mem` punktmonopolartig. |
| `reports/response/calibration/frozen_source_distance_ladder_2026-07-17.md` | Frozen-Source-Distanzleiter | Gleiche realisierte Bare-Antwort ueber sechs Abstaende; kleine distanzabhaengige Targetdeformation, aber voller Ambient-Rang und keine Quellenstruktur-/Ladungsevidenz. |
| `reports/response/scalar/scalar_cross_readout_resolution_2026-07-21.md` | Skalarer Cross-Readout-Aufloesungstest | Getrennte Selbst-/Cross-Kernel und feste Antwortkalibrierung; 1%-Orientierungsgate scheitert in `d=3/10` vor der Distanzgrenze. |
| `reports/response/oriented/oriented_vector_one_way_gate_2026-07-25.md` | Eigenstaendiger orientierter One-Way-Kanal | 6/6 `d=3`-Seeds bestehen Nulltrennung, Ein-Schritt-Persistenzgewinn, Flip, Transversalitaet und Shape-Bounds; Orientierung und direktes Readout bleiben Modellinputs. |
| `reports/response/oriented/oriented_vector_fixed_pair_distance_gate_2026-07-26.md` | Feste-Kopplung-/Distanzgate | 6/6 unabhaengige zyklische Paare bestehen bei globalem `eta_v`; Fern/Nah `9.36e-4..2.80e-3`; konstruiertes instantanes Gauss-Readout, keine Lokalitaets- oder QFT-Evidenz. |
| `reports/response/scalar/signed_scalar_cross_channel_pilot_2026-07-18.md` | Signierter Cross-Channel-Pilot | Je ein `N=100M`-Checkpoint in `d=3/10`: bitgenaue Null-/Produktkontrollen, Antwortumkehr beim Labelprodukt-Flip, aktive Abschirmung gegen `eta_zero` und geringe Radiusstoerung; Architektur-, kein Ladungsbefund. |
| `reports/response/one_way/one_way_dynamic_source_pilot_2026-07-20.md` | autonome One-Way-Quelle | Source bewegt sich nur wenige interne Radien gegenueber der Kernelbreite; Target-Dynamic-vs.-Frozen bleibt sub-threshold, Phase wie freie Kontrolle. |
| `reports/response/one_way/one_way_launched_source_pilot_2026-07-20.md` | gepaarter Source-Launch mit v0.6 | N100M-Source besteht das Vorlaufgate; 10.944 Radien Zusatzverschiebung, Radiusfaktor 1.55..1.61, Shape-q95 in 3/5 Seeds ueber Gate und 2.332e-4 Target-Radien Response; beschraenkt, aber nicht durchgehend formkohaerent. |
| `reports/response/one_way/one_way_interaction_age_N1M_2026-07-21.md` | One-Way-Interaction-Age bis N101M | Fuenf gepaarte Fortsetzungen: 5/5 spaetes Shape-Plateau, 0/5 kontrollgetrennte Formmodifikation; lineare Zentrumtranslation ohne Evidenz fuer einen neuen Knotentyp. |
| `reports/response/one_way/one_way_interaction_age_N3M_2026-07-21.md` | One-Way-Interaction-Age bis N103M | 20 Altersfenster: scheinbare Shape-Halbwelle ist mit freier Kontrolle korreliert (0.999953), gepaarter Differenzspan nur 0.142 Prozent; weiterhin 0/5 Formmodifikation. |
| `reports/response/reciprocal/reciprocal_full_knot_gate_2026-08-04.md` | P3.1 direkter reziproker Vollknoten | Alle 60 Segmentfits reell; Kanal-aus exakt und reziproke Response/Shape 5/5. Endabstand `0.31..0.88 R` statt `2.78..9.21 R`; Bindung/Relaxation, keine komplexe Mode. |
| `reports/response/reciprocal/retarded_reciprocal_full_knot_gate_2026-08-04.md` | P3.2 fester Telegraph-Rueckkanal | Mediator/Response/Shape 5/5, aber 0/80 rohe komplexe Segmentfits; Endabstand `0.58..1.21R`, keine beobachtbare AR(1)-Rotation und noch keine quelllokale Feldtheorie. |
| `reports/response/reciprocal/same_law_reciprocal_jacobian_audit_2026-08-11.md` | P3.7a Same-law-Jacobians | Checkpoint-Gain reell und formal inconclusive; direkte `G,C`-Messung auf vollstaendigen `d=3/10`-Zustaenden. |
| `reports/response/reciprocal/same_law_common_scale_followup_2026-08-11.md` | P3.7a Common-Scale-Folgeaudit | Ein gemeinsames Eta liefert lokale stabile komplexe Vollmatrixmoden 13/13 bei `R=sigma_rep`; nur Kruemmungs-Eligibility. |
| `reports/response/reciprocal/same_law_affine_balance_gate_2026-08-11.md` | P3.7b Affinbilanz | 0/13 je Abstand; endliche Relativdrift und analytisches kompaktes Same-law-No-go blockieren den Pilot. |
| `reports/memory/closure/continuity_constrained_memory_gate_2026-08-11.md` | P3.8a Kontinuitaetsmemory | monopolfreie stationaere Innovation und exakte longitudinale Phasenschwelle; Strom und Konstitutivkoeffizienten bleiben neue Modellinhalte. |
| `reports/memory/closure/dynamic_green_kernel_selection_gate_2026-08-11.md` | P3.8b adjungierter Gradientenmediator | Reviewkorrigierter separater `(m,p)`-Zustand; exakte Residueninversion gegen unendliche Quadratur, Nullmode null, Barriere `3.91920 ell`, lineares Minimum `6.99092 ell`; keine kanonische rho-Folge. |
| `reports/response/reciprocal/quasistatic_two_knot_discrimination_2026-08-12.md` | P3.8c quasistatische Zwei-Knoten-Diskrimination | Starre N100M-Wolken; entgegengesetzte Kraftvorzeichen bei `R=5 ell`, Action/Reaction, Punktgrenze und symmetrisierter Sichtpunkt-Memory-Vergleich bestanden; ein punktartiger d3-Seed, neue Cross-Geometrie, keine Dynamik oder Mechanismusselektion. |
| `reports/response/reciprocal/dynamic_two_knot_mediator_gate_2026-08-12.md` | P3.8d dynamisches Mediator-/Energiegate | Konditionaler Existenzpass fuer neuen `(m,p,R)`-Kanal; Energie und Kontrollen schliessen, beide Startseiten erreichen getrenntes Basin; erster-Ordnung-Kontrolle fast gleiche Separation, UV-sensitive Quench-Amplituden, keine Emergenz aus kanonischem Memory. |
| `reports/memory/closure/emergent_modal_state_reconciliation_2026-08-13.md` | korrigierte P3.8e-Reconciliation | Historische Identifikation superseded; korrigiert 0/5, aktive AR(2)-Pole durchgehend reell, kein Holdout-Vorteil, kein isolierter Hankel-Rang 2; kein skalares No-go wegen energiearmem Memory-Holdout und kollinearer Inputbasis. |
| `reports/memory/closure/p38f_canonical_write_gate_2026-08-15.md` | P3.8f-a kanonischer Write-Port | G0 5/5 pass; nach Entfernung der globalen Translation bleibt der relative Positions-/Kraftkanal nur etwa 0.12 Memory-Zeiten messbar und besteht 0/3 Holdouts in 0/5 Seeds. G1 inconclusive, G2/G3 blockiert; keine Zustands- oder Parameteridentifikation. |
| `reports/response/reciprocal/measurement_closure_relative_noise_gate_2026-08-04.md` | P3.2a/b Mess-Closure und relative Noise | Sichtbarer Delayzustand 9/9 identifizierbar ohne stabiles Modenmatching; Feld/Impuls bringt keinen Holdout-Gewinn und ist bei `kappa~1e16` spektral unbestimmt. `rho` verstaerkt Bindung, nicht Oszillation. |
| `reports/response/reciprocal/long_horizon_hankel_gate_2026-08-04.md` | P3.2 Langhorizont-Hankel | Alle 45 gepaarten Designzellen positiv, drei unabhaengige Seed-Mediane ebenfalls; median `+0.1203`; effektiver Rang waechst, Feld/Impuls hilft nicht und Rang 16/32 trennt sich nicht vom Einwegarm. Keine laengere Persistenz- oder Modenevidenz. |
| `reports/response/reciprocal/hankel_pole_identity_audit_2026-08-06.md` | P3.2 gespeicherter Pol-Identity-Audit | Kandidat omega~0.103 in Seeds 1/2, aber 6..8/12 gleiche Einwegzellen; Seed 3 nur 9/12. Vier korrelationsuebergreifende Kandidaten, null kontrollgetrennte Ueberlebende; kein neuer 500k-Lauf. |
| `reports/response/source_local/source_local_linear_gate_2026-08-06.md` | P3.2c source-lokales lineares Gate | Exakte und reduzierte Kanaele stabil; komplexer Pol bleibt praktisch ein eingefuegter Telegraphpol, nicht knotengeladen. Kein 500k-Lauf. |
| `reports/long_runs/long_3e8/long_run_trace_ar_modes_N30M_eps1em4_2026-07-13.md` | Long-Run-Trace-AR | Komplexe AR-Klassifikationen sind nicht kontrollgetrennt; scalar model bleibt Relaxations-/Kompaktheitsbefund. |
| `reports/long_runs/long_3e8/feature_closure_N30M_eps1em4_2026-07-13.md` | Feature-Closure | Aktive Shape-/Radius-Scalars haben den klarsten Closure-Lift; Spin-Scalar bleibt kein geschlossener Phasenkanal. |
| `reports/vector_memory/vector_memory_minimal_design_2026-07-09.md` | Vektorgedaechtnis | Minimalanforderungen fuer einen orientierten Memory-Kanal mit Slow-Mode- und Negativkontrollen. |
| `reports/vector_memory/vector_memory_pilot_initial_2026-07-10.md` | Vektormemory-Pilot | 2D-Transverse-Kurzpilot; komplexe AR-Moden erscheinen schon in `eta_v=0`, also noch kein isolierter Vektoreffekt. |
| `reports/vector_memory/vector_memory_eta_s_zero_control_2026-07-10.md` | Eta-Zero-Vektorkontrolle | Selbst `eta_s=eta_v=0` zeigt komplexe AR-Paare; komplexe Projektionsmoden sind daher noch keine Schwingungsevidenz. |
| `reports/vector_memory/vector_memory_alignment_control_2026-07-10.md` | Alignment-Vektorkontrolle | `alignment` vergroessert schwache/transitionale Radien eher; `A_att=20` bleibt kompakt und ueberwiegend real. |
| `reports/project/meta/operations/repository_cleanup_2026-07-09.md` | Repository-Cleanup | Aktive Docs bleiben bei sieben Seiten; lokale private Klartextnotizen wurden entfernt. |

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
- Long-Run-Trace-AR und Feature-Closure auf dem `N=30M`-Endfenster sind als erste Reanalyse-Schritte vorhanden;
- Long-Run-Transferoperatoren mit reicheren Features statt Kurzlauf-Sanity-Checks.

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

Aktiver gestufter Pfad:

| Stufe | Status | Messgroessen |
| --- | --- | --- |
| Vollstaendiger Zustand | erledigt | gemeinsame Translation/Rotation von `x` und Memory, Kraft-/Form-Invarianz |
| Uniformer Weak Probe | erledigt; isotrope Vollrang-Negativkontrolle | paired response, Nullpfad, `eta_zero`, Signflip-Rang, Linearitaet |
| Eingefrorener Quellknoten | erledigt; Punktmonopol und voller Ambient-Rang | lokalisierte Antwort, Distanzleiter, Null-/Vorzeichenarme |
| Einseitig dynamische Source | aktuelles negatives Gate | gepaarte unlaunched Source, Identity-Retention, Target-Readout, relationale Orientierung |
| Zerstoerungsarmer Source-Transport | naechstes Mechanismusgate | koharente Ganzzustandsbewegung oder lokaler/retardierter Feldkanal |
| Reziproke getrennte Memories | gesperrt bis One-Way-Gate besteht | Balance, Identitaet, Cross-Korrelation, Verhedderungs-/Kollisionskontrolle |
| Gemeinsames Memory | eigene Modellvariante | Massennormierung, Identitaetsverlust, kollektive Moden |

Guardrail: Diese Stufe behauptet keine Quantenfeldtheorie. Uniforme Vollrang-
Antwort ist keine emergente Dimension; nur lokalisierte, kontrollgetrennte und
seed-reproduzierbare relationale Antworten koennen Paper-II-Evidenz werden.

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
