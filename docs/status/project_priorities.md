# Projektprioritaeten

Stand: 2026-07-20.

Diese Seite ist die aktive Arbeitsliste. Sie ersetzt die alte Action Matrix
und den Hardening Plan: Was Codex autonom ziehen kann, steht hier direkt als
Prioritaet; was Haukes Entscheidung braucht, ist als Entscheidungspunkt
markiert.

## Leitentscheidung

**Paper 0 bleibt der mathematische Anker. Der aktuelle wissenschaftliche
Engpass ist nicht mehr ein weiterer Long Run, sondern die Trennung linearer
Memory-Relaxation von echter nichtlinearer Metastabilitaet.**

Begruendung:

- Die Markov-/Transferoperator-Schicht existiert initial im Paketkern und ist
  getestet.
- Die attraktive Ein-Kernel-Ablation reproduziert den bisherigen
  kleinen-Radius-Referenzast bis etwa 1e-8 relativ.
- Der A_att=0..40-Scan zeigt keinen endlichen Phasenuebergang; fuer A_att>=5
  erklaert der lineare Relativmodus den dynamischen Radius auf etwa ein
  Prozent.
- Paper I darf deshalb kompakte co-moving Relaxationswolken berichten, aber
  derzeit keinen isolierten nichtlinearen metastabilen Knoten.
- Das feste-g-Gate, die Spektralfeld-Reprasentation und die direkte
  Realraum-Reconciliation sind abgeschlossen. Kleinere epsilon-Werte skalieren
  den lokalen Radius nur proportional.
- Low-Mode-Closure und N=1M-Bestaetigung stuetzen eine praediktive reduzierte
  Relaxationsbeschreibung. Der Eigenvektor-/Segmentaudit isoliert jedoch
  keinen stabilen einzelnen reellen Modus; die fruehere Formulierung
  "N-stabiler reeller Modus" war zu stark.
- Komplexe Nebenmoden sind weder von `eta=0` getrennt noch segmentstabil und
  tragen keinen Oszillatorclaim.
- Der aktuelle Engpass ist ein shape-bounded/coherent dynamischer Quellmechanismus,

## P0: Abgeschlossen fuer den Moment

### P0.1 Paper 0 einfrieren

Status: erledigt fuer interne Weiterarbeit.

Regeln bleiben:

- allgemeine Memory-Form `(1-lambda_m)rho_n + beta G_sigma`;
- normierte Arbeitskonvention `lambda_m=beta=alpha` nur als Spezialfall;
- sichtbarer Prozess nichtmarkovsch, augmentierter Zustand markovsch;
- keine physikalische Masse, keine Lorentz-/Quanten-/Standardmodell-Claims.

### P0.2 Paper I synchronisieren

Status: erledigt fuer den aktuellen Stand.

Paper I verwendet dieselbe Memory- und Markov-Sprache. Was jetzt fehlt, ist
nicht noch mehr Formulierung, sondern belastbare Evidenz.

### P0.3 Doku-Oberflaeche reduzieren

Status: erledigt in dieser Runde.

Aktive Docs sind jetzt auf sieben Seiten begrenzt:
`index`, `current_status`, `project_priorities`, `THEORETICAL_CONTEXT`,
`repository_map`, `experiment_catalog`, `paper_claims`.

## P1: Jetzt

### P1.1 Long-Run-Kontrollen auswerten

Status: abgeschlossen und durch den Linearitaetsaudit neu eingeordnet.

- Legacy-Sign-Laeufe bleiben nur Vorzeichen-Auditmaterial.
- Korrigierte N=30M/300M-Laeufe zeigen reproduzierbar kompakte co-moving
  Memory-Clouds gegen eta=0.
- Der neue attraktive Ein-Kernel-Scan erklaert den kleinen-Radius-Ast jedoch
  fast vollstaendig als linearen Relativmodus. Das ist eine Relaxations- und
  Kontrolltrennung, noch keine isolierte nichtlineare Metastabilitaet.
- Vor weiteren Long Runs werden bestehende Daten gegen R_linear reconciliiert.
### P1.2 Knotenkriterium v0.6 verwenden

Status: Historische Long-Run-Scores bleiben v0.5. v0.6 behaelt deren sieben
Evidenzkomponenten unveraendert und fuegt fuer neue Checkpoints ein
Stationaritaets-Zulassungsgate hinzu. Shape-bounded/coherent Response bleibt
eine getrennte Transportdiagnostik und wird nicht in den KnotScore
hineingemittelt.

Mit Knotenscore ist zunaechst kein magischer einzelner Zahlenwert gemeint,
sondern ein reproduzierbares Scorecard-Kriterium. Es soll verhindern, dass ein
Knoten nur wegen eines guenstigen Voxels, Seeds oder Einzelplots akzeptiert
wird.

Akzeptanz fuer einen Paper-I-Befund:

- Interagierende Bedingungen trennen sich klar von `eta_zero` in Residence und
  Kompaktheit.
- Ein Claim ueber einen bestimmten Kernelmechanismus trennt sich auch von
  passenden Kernel-Ablationen wie `single_scale`.
- Residence-Ratios sind nicht nur ein Voxel-Artefakt, sondern stabil ueber
  mindestens mehrere feste Voxelgroessen.
- Der Center-of-knot, z.B. Memory-Schwerpunkt, dominanter Residence-Voxel oder
  geglaettetes externes Antwortzentrum, driftet deutlich langsamer als die rohe
  Trajektorie.
- Vor einer Stoerung bestehen Radius und normiertes Shape-Eigenwertspektrum ein
  explizites Stationaritaetsfenster; hohes N allein genuegt nicht.
- Unter Stoerung darf der Knoten rotieren und begrenzt atmen, muss aber
  radiusbeschraenkt und spektral kohaerent bleiben.
- Seed-Robustheit wird als Median/IQR ueber Seeds berichtet, nicht als bester
  Seed.
- Git-Revision, Seeds, Burn-in, Sampling und Runtime sind dokumentiert.
- Ergebnis wird als Report committed, nicht nur als lokale JSON-Datei gelesen.

Ein spaeterer skalarer Score kann daraus entstehen, etwa als normalisierte
Kombination aus Residence, Kompaktheit, Voxel-Stabilitaet, Center-Stabilitaet,
Seed-Robustheit und Kontrolltrennung. Fuer den naechsten Schritt reicht eine
transparente Scorecard.

### P1.3 Jetzt entscheiden und testen

Naechster operativer Schritt:

1. Abgeschlossen: Sign-Konventionsentscheidung. Korrigiert wurde der
   Potentialgradient, nicht `eta` und nicht bloss das Labeling. Report:
   `reports/kernels/corrected_sign/kernel_sign_convention_correction_2026-07-09.md`.
2. Abgeschlossen: korrigierter q=3-Retest. Historische Baseline und
   `single_scale` dispergieren; `rep_zero` bestaetigt den attraktiven Kanal.
   Report: `reports/kernels/corrected_sign/corrected_sign_q3_pilot_2026-07-09.md`.
3. Abgeschlossen: Amplitudenhierarchie. Der Drift-Umschlag liegt zwischen
   `A_att=3.5` und `A_att=9`; kompakte Kandidaten liegen bei `A_att=9..35`.
   Report: `reports/kernels/corrected_sign/amplitude_hierarchy_corrected_sign_q3_2026-07-09.md`.
4. Abgeschlossen: erster AR-Modentest auf `A_att=0.35`, `9`, `35`.
   Ergebnis: langsame Moden bleiben reell; schnelle kleine komplexe Reste
   tragen keinen Oszillatorclaim.
5. Abgeschlossen: Grenzscan unterhalb `A_att=9`; Uebergang bei
   `A_att ~= 7.9`, `chi ~= 0.88`.
6. Abgeschlossen: minimaler Vektorgedaechtnis-Prototyp und erster 2D-Pilot.
   Ergebnis: komplexe AR-Moden treten schon im `eta_v=0`-Fallback auf;
   noch kein isolierter Vektoreffekt.
7. Abgeschlossen: `eta_s=eta_v=0` und `alignment`-Kontrollen. Ergebnis:
   komplexe AR-Paare entstehen schon im Nullkraft-/Random-Walk-Zweig;
   `alignment` erzeugt noch keinen isolierten Oszillator.
8. Abgeschlossen: KPI-Register und fallspezifische Score-Familien sind im
   Experiment-Katalog dokumentiert. `KnotScore` bleibt fuer Metastabilitaet;
   `ModeScore`, `PropagationScore` und `FormationScore` werden getrennt.
9. Abgeschlossen: erster Pareto-M0-Pilot bei `A_att=8`, `M0 in {0.5,1.0,2.0}`.
   Ergebnis: hoeheres `M0` macht Laeufe kompakter, liefert aber im 100k-Pilot
   keinen starken v0.5-KnotScore. Report:
   `reports/long_runs/m0_axis/m0_axis_knot_score_pilot_2026-07-10.md`.
10. Abgeschlossen: korrigiertes skalares Kandidatenfenster bei 1M gehaertet.
    `A_att=20` und `35` tragen hohe v0.5-Kompaktheit/Memory-Shape-Scores;
    `A_att=9` bleibt Boundary-Control. Report:
    `reports/long_runs/scalar_hardening/scalar_hardening_q3_1M_2026-07-10.md`.
11. Abgeschlossen: N-Skalierung mit `burn_in=0` fuer `A_att=20/35`,
    `N=100k..3M`. Ergebnis: kompakte Memory-Clouds bilden schnell;
    Residence-Gain bleibt median unter der Partial-Schwelle. Report:
    `reports/long_runs/scalar_hardening/scalar_n_scaling_q3_2026-07-10.md`.
12. Abgeschlossen: Residence-Messmethodik geschaerft. `long_run_metastability.py`
    schreibt jetzt Center-/Memory-Ball-Residence bei Radiusfaktoren
    `1,2,4,8,16`. Die Summary verwendet den festen Primaerfaktor `2`,
    damit groessere Suchradien die Residence nicht trivialisieren.
13. Abgeschlossen: `N=300M`-Hardening fuer `A_att=20` und `35`, Seeds `1..5`.
    v0.5-Score und Voxel-Residence tragen; die fixe finale Memory-Center-
    Residence zeigt aber Drift/Rezentrierung. Report:
    `reports/long_runs/long_3e8/long_run_3e8_results_2026-07-11.md`.
14. Abgeschlossen: dynamische Center-Trace-Diagnostik als `N=3M`-Pilot fuer
    `A_att=20/35`, Seeds `1..5`, gegen `eta_zero`. Report:
    `reports/long_runs/long_3e8/dynamic_center_trace_q3_N3M_2026-07-12.md`.
    Ergebnis: `dynamic_inside_fraction` und `dynamic_max_run` sind allein nicht
    diskriminierend, weil `eta_zero` im eigenen grossen Memory-Ball ebenfalls
    innen bleibt. Trennend sind dynamischer RMS-Radius, radiusnormalisierte
    Center-Drift und Memory-Shape.
15. Abgeschlossen: cadence-korrigierter Hybrid-Trace fuer `N=1M`,
    `A_att=20/35`, Seeds `1..5`, gegen `eta_zero`. Rund 100 logarithmische
    Punkte definieren Trend-KPIs; ein gleichmaessiges Endfenster mit 10,001
    Punkten (`dt_mem=0.01`, 100 Memory-Zeiten) definiert lokale Spin-KPIs.
    Radius und Trend-Drift trennen robust. Der Spin-Proxy wird im mitbewegten
    Memory-Center-Rahmen berechnet; Achsen- und rohe `L`-Korrelation werden
    getrennt berichtet. Faellt die Korrelation bereits beim ersten messbaren
    Lag unter `1/e`, wird die Dephasierung als `<= dt_mem`-Obergrenze gelesen,
    nicht als exakt bestimmte Zeit. Aktueller Befund: negativer skalarer
    Modenbefund, kein Paper-I-Blocker. Report:
    `reports/long_runs/long_3e8/dynamic_center_spin_trace_q3_N1M_2026-07-12.md`.
16. Abgeschlossen: Epsilon-Dynamic-Center-Sweep fuer `A_att=35`, Seeds `1..3`,
    `N=100k`, `epsilon=0` plus 24 logarithmische Werte `1e-12..1e1`, gegen
    seedgleiche `eta_zero`-Kontrollen. Ergebnis: v0.5-Score-Plateau ab etwa
    `epsilon=1.65e-6` bis `0.741`; bei `epsilon=2.72` kollabiert der aktive
    Lauf auf `eta_zero`-aehnliche Metriken. Die mitbewegte Reanalyse korrigiert
    `L_int=(x-c_mem) wedge d(x-c_mem)/dt_mem`, entfernt aber nur einen kleinen
    Translationsanteil: Spin bleibt negativ (`axis_polarization ~0.017`,
    Dephasierung ein Update). Report:
    `reports/long_runs/epsilon/epsilon_dynamic_center_q3_Aatt35_N100k_2026-07-12.md`.
17. Abgeschlossen: Epsilon-Bestaetigungsslice und `N=30M`-Hybrid-Trace fuer
    `epsilon=1e-4`, `A_att=20/35`, Seeds `1..5`, gegen `eta_zero`. Alle drei
    Bestaetigungswerte `{1.65e-6, 1e-4, 0.015}` lagen im v0.5-Score-Plateau;
    `1e-4` wurde als kleine, aber nicht randstaendige Rauschskala gewaehlt.
    Ergebnis bei `N=30M`: Beide aktiven Kandidaten trennen sich in
    dynamischem Radius, radiusnormalisierter Center-Drift, Memory-Dimension
    und Roundness klar von `eta_zero`. `A_att=35` ist staerker und ist jetzt
    der scalar long-run reference candidate (`radius ~=2.09e-4`,
    `drift/radius ~=0.044`, `D_mem ~=2.94`, `roundness ~=0.843`). Spin bleibt
    negativ: Achsenpolarisation nahe `0.01`, rohe `L`-Dephasierung `<=dt_mem`.
    Report:
    `reports/long_runs/long_3e8/dynamic_center_spin_trace_q3_N30M_eps1em4_2026-07-13.md`.
18. Abgeschlossen: Paper-I-Evidenztabelle fuer den `N=30M`, `epsilon=1e-4`-Referenzslice. Fuer `A_att=35` ist die aktive Memory-Cloud im Median etwa Faktor `4.96` kompakter als `eta_zero`, die radiusnormalisierte Center-Drift ist um Faktor `7.33` getrennt. Report:
    `reports/long_runs/long_3e8/paper_i_evidence_table_N30M_eps1em4_2026-07-13.md`.
19. Abgeschlossen: Long-Run-Trace-AR-Modencheck auf dem gleichmaessigen Endfenster derselben `N=30M`-Laeufe. Komplexe AR-Klassifikationen treten auch in `eta_zero` auf und sind nicht kontrollgetrennt; kein skalarer Photon-/Phasenclaim. Report:
    `reports/long_runs/long_3e8/long_run_trace_ar_modes_N30M_eps1em4_2026-07-13.md`.
20. Abgeschlossen: Feature-Closure auf `A_att=35`, `epsilon=1e-4`, `N=30M`.
    Aktive Shape-/Radius-Scalars zeigen den klarsten Closure-Lift; der
    Spin-Scalar bleibt kein geschlossener Phasenkanal. Report:
    `reports/long_runs/long_3e8/feature_closure_N30M_eps1em4_2026-07-13.md`.
21. Abgeschlossen: 3D-Memory-Shape-Boundary-Notiz fuer den `N=30M`-
    Referenzslice. Ergebnis: `D_mem ~=2.94` bei `A_att=35` ist ein
    seed-stabiler lokaler Memory-Shape-Befund im gewaehlten 3D-Embedding,
    nicht die Ableitung externer/macroskopischer `d=3`-Selektion. Paper II
    uebernimmt die Frage, ob lokale 3D-Memory-Cloud-Geometrie unter
    Ambient-Dimension, Mehrknoten-Wechselwirkung und externer Beobachtung
    robust bleibt. Report:
    `reports/dimensions/memory_shape_boundary_2026-07-13.md`.
22. Leitplanke ab 2026-07-11: Ein einzelner Knoten muss in einem translations-
    invarianten Modell kein fixes absolutes Zentrum besitzen. Fuer Paper I
    zaehlen zunaechst mitbewegte Invarianten: kompakte Memory-Cloud, begrenzter
    lokaler Radius, langsame Center-Drift und Trennung gegen `eta_zero`. Spin-
    Proxies bleiben Observablen fuer Orientierung/Dephasierung. Dephasierungswerte
    am ersten Lag sind zensierte Obergrenzen `<= dt_mem`, nicht exakt aufgeloeste
    Zeiten; kein KnotScore- oder Teilchenspin-Claim.

23. Abgeschlossen: A_att-Transition `d=3` vs. `d=10` bei `N=10M`, Seeds
    `1..5`, `epsilon=1e-4`, Delta-Deposition. Der Report schliesst zugleich
    die `beta=0`/`M0=0`-Referenzluecke. Ergebnis: `D_cov` im d10-kompakt-Ast
    liegt nahe `2.52`, waehrend `D_mem` bis `9.16` steigt; d3 erreicht
    `D_mem ~=2.95`, aber die rohe Spur bleibt bei `D_cov ~=1.8`. Report:
    `reports/long_runs/scalar_hardening/aatt_transition_d3_d10_2026-07-15.md`.
24. Abgeschlossen: 3D-Dimensionsclaim-Audit auf vorhandenen `A_att=35`,
    `epsilon=1e-4`, `N=30M` Case-JSONs fuer `d in {3,4,5,7,10,13,20}`.
    Ergebnis der damaligen Auswertung: kein starker ambient-unabhaengiger
    3D-Claim, weil D_mem, D_p90 und D_p95 mit d wachsen. Der spaetere
    Linearitaetsaudit (Punkt 32) ersetzt auch die fruehere Teaser-Lesart:
    D_mem nahe der Ambient-Dimension ist im isotropen kleinen-Radius-Regime
    zu erwarten. D_spec memory bleibt nur ein historischer Paper-II-
    Hypothesenhinweis. Report:
    reports/dimensions/dimension_claim_audit_2026-07-15.md.
25. Abgeschlossen: D_spec-Sensitivitaetsaudit. Ergebnis: Die `D_spec memory ~=3`-Spur
    ist ein Paper-II-Hypothesenhinweis, aber kein robuster Dimensionsclaim. Die
    bisherige Implementierung war als Legacy-Diagnostik zu lesen; kuenftige
    `spectral_dimension` nutzt symmetrische Kernel-Normalisierung und schreibt
    die verwendete Konvention in Long-Run-Payloads. Report:
    `reports/dimensions/dspec_sensitivity_2026-07-15.md`.

26. Abgeschlossen: Rohsnapshot-D_spec-Pilot. Ergebnis: `N=200k` fuer `d=3`
    und `d=10` mit Seeds 1-3 validiert den neuen `memory_cloud.snapshot`-
    Auswertepfad, ist aber noch keine Langlauf-Evidenz. Heat-Trace-`D_spec`
    reproduziert im Pilot kein robustes Nahe-3-Signal; im `d=10`-Baseline-Fall
    findet der konservative Estimator kein stabiles Skalierungsfenster. Report:
    `reports/dimensions/dspec_raw_snapshot_2026-07-15.md`.

27. Abgeschlossen: N-Abhaengigkeits-Recheck. Ergebnis: Die alte
    `N=100k..3M`-Formation-Skalierung, der kurze `N=200k`-Rohsnapshot-Pilot
    und der `N=30M`-Referenzslice sind in einer Guardrail-Grafik
    zusammengefuehrt. `N=200k` bleibt nur Pipelinecheck; Memory-Shape verhaelt
    sich qualitativ wie zuvor. Exakt `3D` ist kein hartes Kriterium; fuer Paper
    II zaehlen stabile aktive Dimensionen bzw. Response-Raenge gegen Kontrollen.
    Report: `reports/long_runs/scalar_hardening/n_dependence_recheck_2026-07-16.md`.

28. Abgeschlossen: Rohsnapshot-D_spec-Retest. Ergebnis: `N=3M` fuer `d=3`
    und `d=10` mit Seeds 1-5 bestaetigt die Trennung der Dimensionkanaele.
    `d=3`-Baseline bleibt in der gewichteten Shape-Dimension nahe drei, aber
    Heat-Trace-`D_spec` bleibt deutlich unter drei. `d=10`-Baseline bleibt
    shape-hochdimensional und hat kein akzeptiertes Heat-Trace-Skalierungsfenster.
    Damit ist isoliertes `D_spec` kein belastbarer 3D-Claim; naechster Gate ist
    relationaler Response-Rang. Report:
    `reports/dimensions/dspec_raw_snapshot_retest_2026-07-16.md`.

29. Abgeschlossen: analytischer Kernelkompensations-Constraint und
    Fixed-curvature-Sigma-Pilot. Fuer `q>1` sind zweiskaliges `int K=0` und
    lokale Rueckstellung disjunkt. Bei festem `chi=35/9`, `q={2,3,4}`,
    `N=1M`, Seeds `1..5` kollabieren die KPIs bis maximal `1.65e-8` relative
    q-Spanne, weil `R_mem/sigma_rep <=2e-4`. Der aktuelle kompakte Ast misst
    lokale Steifigkeit, nicht separate Kernelbreiten. Reports:
    `reports/kernels/compensation/kernel_compensation_constraint_audit_2026-07-18.md`
    und
    `reports/kernels/compensation/fixed_curvature_sigma_pilot_d3_N1M_2026-07-18.md`.
30. Abgeschlossen: breiter Drei-Skalen-Kompensator und signiertes skalares
    Frozen-Source-Kanal-Gate. Der Kompensator erfuellt `int K=0`, matched die
    lokale q=3-Referenzkruemmung und erzeugt im `d=3`-Referenzslice einen
    Kraftwechsel bei `r/sigma_rep ~=10.91`. Im `N=1M`-Fuenf-Seed-Pilot
    bleiben die gematchten lokalen KPIs bis `2.2e-11` relativ identisch. Auf den `N=100M`-
    Checkpoints in `d=3/10` sind Nullarme und gleiche Labelprodukte bitgenau;
    der Produkt-Flip kehrt die Antwort um. Reports:
    `reports/kernels/compensation/three_scale_zero_mean_pilot_d3_N1M_2026-07-18.md`
    und
    `reports/response/signed_scalar_cross_channel_pilot_2026-07-18.md`.

31. Abgeschlossen: enger Kernel-Core-Audit und curvature-matched Ablation.
    Der aktuelle (1,35)-Referenzkernel besitzt im gesampelten Bereich keinen
    aktiven repulsiven Kern. Der attraktive Ein-Kernel-Punkt (0,26) stimmt
    seedweise ueber alle kontinuierlichen KPIs bis etwa 1e-8 relativ mit der
    Referenz ueberein.
32. Abgeschlossen: attraktiver A_att=0..40-Screening-Scan, N=300k, Seeds 1..5.
    Die Rohmetriken aendern sich glatt; es gibt keinen endlichen
    Phasenuebergang. Fuer A_att>=5 folgt der dynamische Radius der linearen
    Memory-Vorhersage mit 0.94 Prozent medianem und 3.44 Prozent maximalem
    relativen Fehler. D_mem nahe drei ist in diesem d=3-Slice damit primaer
    erwartete isotrope Gaussgeometrie, keine Dimensionsselektion.
33. Abgeschlossen: Feldgleichungs-Bruecke. Der Gausskernel ist exakt als
    Heat-Semigroup-Snapshot in einer Hilfskoordinate darstellbar. Ein
    physisches Relaxations-Diffusionsfeld hat einen anderen Greenkernel und
    erweitert den Markov-Zustand; es ist keine algebraische Umbenennung.
34. Abgeschlossen: Kernel-Familienvergleich, Long-Run-Reconciliation und
    festes-g-R/L-Gate. Bei q=3 gilt fuer curvature-matched Ein- und
    Zweiskalenkernel exakt `A_eff=A_att-9`; die seedweisen KPIs kollabieren
    bis auf numerisches Rauschen. Neun aktive N=30M/300M-Slices folgen dem
    finite-memory linearen Radius mit maximal 1.16 Prozent Fehler. Das
    vorregistrierte R/L-Gate ist formal `inconclusive`: der Radius waechst
    seed-stabil 6.2 Prozent ueberlinear, waehrend D_mem und Roundness stabil
    bleiben. Eine post-hoc Skalenpruefung zeigt, dass feste Voxel den
    Residence-/KnotScore-Befund verzerren; co-moving Residence ist dagegen
    auch fuer eta=0 gesaettigt und nicht diskriminierend. Kein metastabiler
    Skalarast ist damit isoliert.
35. Abgeschlossen: Eigenvektor- und Zeitsegment-Mode-Identity auf fuenf Seeds
    und fuenf Segmenten. Der aktive reelle Kandidat erreicht zwar nahezu
    identische Feature-Subraeume, verfehlt aber Match-/Ratenstabilitaetsgates;
    der komplexe Kandidat ueberlappt mit eta=0 zu mehr als 0.9999.
    Report: `reports/memory/low_mode_identity_audit_2026-07-20.md`.
36. Abgeschlossen und mit v0.6 nachgemessen: autonome und extern angeschobene
    One-Way-Source gegen frozen/free/eta-zero und gepaarte unlaunched Kontrolle.
    Der N100M-Checkpoint besteht ueber alle fuenf Fortsetzungen das
    50-Memory-Time-Stationaritaetsgate. Der 0.1-sigma-Launch verschiebt die
    Source zusaetzlich um 10.944 Radien und bleibt radiusbeschraenkt
    (Faktor 1.55..1.61), verfehlt aber in drei von fuenf Seeds das
    q95-Shape-Spektralgate. Die Targetantwort bleibt mit 2.332e-4 Radien
    sub-threshold. Kein Orbit-, Phasen- oder Propagationsbefund;
    Reziprozitaet bleibt gesperrt.

Aktueller naechster Schritt:

- Der attraktive Ein-Kernel-Ast mit L=sigma_att und
  g=eta M0 A_att/L^2 bleibt die reduzierte skalare Kontrollbaseline. A_att,
  eta und M0 sind darin nicht getrennt identifizierte Physikparameter.
- Kein weiterer dichter Amplituden-, Epsilon- oder Heat-Diffusionsscan: Die
  beobachteten Aeste sind glatt und als Relaxation erklaert.
- Mode-Identity ist abgeschlossen. Tragbar ist reduzierte Vorhersagbarkeit,
  nicht die Identitaet eines einzelnen reellen oder komplexen Eigenmodus.
- Naechster Mechanismusschritt: shape-bounded/coherent Quelltransport
  formulieren und falsifizieren. Ein Punkt-Drive erzeugt zwar beschraenkte
  Translation, aber keine durchgehend kohaerente Shape-Antwort; er ist kein
  Ersatz fuer kontrollierte Ganzzustands-Translation oder lokale
  Felduebertragung.
- Das Gate verlangt gepaarte unlaunched Kontrollen, stationaere Ausgangsform,
  beschraenkte und kohaerente, nicht notwendig starre Source-Shape, eine
  targetseitige Response oberhalb des Rausch-/Frozen-Niveaus und
  Zeitverzoegerung bei lokaler Kopplung.
- Reziproke Kopplung und orientiertes/Vektormemory erst nach Bestehen dieses
  One-Way-Gates; sonst waere ihre Interpretation nicht identifizierbar.
- Residence-/Score-Vergleiche ueber veraenderte Radius-Skalen muessen
  raumnormierte Bins verwenden oder die Voxel/R-Sensitivitaet offen ausweisen.
  Rekreuzung bleibt kein eigenes Ziel.

### P1.4 Alpha/M0 und lokale Moden klaeren

Status: Paketkern, Long-Run-Reconciliation und dimensionsloses R/L-Gate sind getestet. Der Skalarast bleibt Kontrollbaseline; naechster Engpass ist ein minimaler dynamischer Feldzustand mit statischem Greenkernel-, Quellvorzeichen- und eta=0-Gate.

Die nummerierten Punkte 0 bis 8 darunter dokumentieren die historische
Entwicklung. Ihre damalige Kandidatenlesart wird durch P1.3 Punkt 32
ueberschrieben: Kompaktheit allein ist im kleinen-Radius-Ast linear erklaert.

Die allgemeine Memory-Form ist jetzt technisch im Kernmodell abgebildet als
`rho[n+1]=(1-lambda_m)rho[n]+lambda_m M0 G_sigma`. Der alte Spezialfall
`beta=lambda_m=alpha` bleibt `M0=1`. Konsequenz: Alpha-Laeufe muessen
mindestens `lambda_m`, `M0=beta/lambda_m`, Tail-Cutoff und effektive Kopplung
oder `eta/eta_c` gemeinsam dokumentieren.

Prioritaet:

0. Abgeschlossen: Memory-Form, Sign-Konventionsentscheidung, q=3-Retest und
   Amplitudenhierarchie sind umgesetzt; vorhandene v0.5-Daten vor dem Fix
   sind `legacy-sign`.
1. Abgeschlossen: erster AR-Modentest auf den korrigierten kompakten
   Kandidaten. Die langsamen Moden sind reell, nicht stabil komplex.
2. Abgeschlossen: Grenzscan im Bereich `A_att<9`; die Driftgrenze liegt bei
   `A_att ~= 7.9`.
3. Abgeschlossen: 1M-Haertung fuer `A_att in {9,20,35}`. `A_att=20` und
   `35` sind kompakte Kandidaten; Residence-Gain ist noch nicht median-stark.
4. Abgeschlossen: N-Skalierung fuer `A_att=20/35` bis `N=3M`.
   Kompaktheit und Memory-Shape sind schnell stabil; Residence-Gain bleibt
   median unter `2`.
5. Fuer Paper I: dynamische Center-Trace-Diagnostik ist implementiert und im
   `N=30M`-Referenzslice validiert. Die Laeufe tragen co-moving compact
   memory-cloud evidence, aber keinen fixed absolute spatial-knot claim.
   Akzeptiert wird ein zeitlokaler Befund aus Radius, radiusnormalisierter
   Center-Drift und Memory-Shape gegen `eta_zero`; reine dynamic-inside
   Residence ist als Akzeptanzmetric zu schwach.
6. Fuer Paper III: Vektor-/Phasenmemory nur kontrolliert weiterfuehren.
   Der erste Pilot zeigt komplexe AR-Moden bereits im Skalar-Fallback;
   entscheidend ist nun Differenz gegen Nullkraftkontrollen, `lambda_v`-Sensitivitaet und shuffled/randomized-vector.
7. Abgeschlossen: erster M0-Achsenpilot bei festem `A_att=8`. Hoeheres `M0`
   verbessert Kompaktheit und Memory-Form leicht, traegt aber noch keinen
   starken v0.5-KnotScore.
8. Neue Alpha-/Sigma-/A-Scans nur kontrolliert starten: erst Scorecard
   festlegen, dann eine Hauptachse variieren (`lambda_m` bei festem `M0`,
   danach `sigma`, danach Amplitudenverhaeltnis). `M0` bleibt vorerst
   sekundaerer Skalierungshebel, kein breiter Blindscan.

### P1.5 Ressourcenbegrenztes Memory-Feld

Status: Spektrale Reprasentation, Closure, N-Reconciliation und Mode-Identity-Audit abgeschlossen.

- `rho_hat` speichert dasselbe exponentielle skalare Memory mit festem
  O(M)-Zustand. Bei `M=64` benoetigt ein Feldzustand 1040 Bytes.
- Exakte Historien-, Kontraktions-, Massen-, Kraft- und `eta=0`-Tests bestehen.
- Der Epsilon-Slice `1e-8, 1e-6, 1e-4` ergibt `R proportional epsilon` bis
  auf rund `2e-9` relative Streuung von `R/epsilon`.
- Die Feldextension
  `rho_new_hat(k)=exp(-nu k^2)[(1-lambda)rho_hat(k)+lambda G_hat_x(k)]`
  besitzt `nu=0` als bitgenaue Modellkontrolle.
- Fuer Diffusionslaengen pro Memory-Zeit von `0`, `0.3 L`, `1.0 L` waechst
  der aktive Medianradius glatt um Faktor `1.384`; active/control steigt von
  `0.171` auf `0.240`.
- Der Low-Mode-Trace speichert translation-invariante Fourierfeatures und
  Realraum-Stuetzstellen. Die direkte 2000-Update-Historie begrenzt den
  Kraftfehler wie erwartet durch den geometrischen Memory-Schwanz.
- Das N=100k-Gate besteht Closure und Numerik. Die N-Reconciliation stuetzt
  zwei aggregierte aktive Raten, aber nicht die Identitaet eines einzelnen
  segmentstabilen Eigenmodus.
- Der Mode-Identity-Audit verfehlt das strikte Realmodus-Gate: Match-Anteile
  0.72/0.80 und relative Raten-MAD 0.233/0.278 bei 0.2/1.0 Memory-Zeiten.
- Komplexe Feature-Subraeume ueberlappen zwischen aktiv und `eta=0` mit
  mehr als 0.9999. Kein Phasen-, Photon- oder Oszillatorbefund.

Naechstes Gate:

1. Analytische lineare Referenz fuer die komplexen `eta=0`-Nebenmoden
   ableiten und gegen Sampling-/Feature-Artefakte testen.
2. Kuenftig kompakte AR-Matrizen und Segmentstatistiken statt kompletter
   reproduzierter Traces persistieren.
3. Direkte Realraumhistorie bleibt Validierungskanal fuer jede spektrale
   Variante. Harte Propagation bleibt fuer das Heat-Feld ausgeschlossen.
4. Der getrennte One-Way-Quelltest priorisiert nun einen lokalen oder
   orientierten Transportmechanismus; keine weitere Heat-Parameterachse.

### P2.1 Transferoperator auf Long-Run-Daten

Status: Paket-Closure, Low-Mode-Long-Run, Kontrollen und Mode-Identity erledigt; kein oszillatorischer oder metastabiler Transferoperatorbefund.

- `markov.closure` bietet getestete Leave-one-seed-out-Closure,
  Persistence-/Shuffle-Kontrollen, lag-normalisierte AR-Spektren und
  Feature-Eigenvektor-Subraumvergleiche.
- Der skalare Low-Mode-Zustand ist vorhersagbar, aber die segmentweisen Fits
  isolieren keinen stabilen einzelnen reellen Eigenmodus.
- Komplexe Paare sind nicht spezifisch gegen `eta_zero`; ihre aktiven und
  eta-null Feature-Subraeume sind praktisch identisch.
- Naechste Haertung ist die analytische Herkunft der Nullkontrollmoden und
  persistierte Fit-Provenienz, nicht ein weiterer Parametersweep.
- PCCA/HMM/PMM erst bei einem nachgewiesenen nichtlinearen oder mehrzustandigen
  Regime pruefen.

### P2.2 Dimensionsclaim

Status: defensiv lesen; kein `d=3`-Selektionsclaim; aktueller Befund stuetzt eher eine Innen/Aussen-Aufspaltung als eine einzelne Dimensionszahl.

- Archivierter `D_occ ~ 2.8`-Befund: weiterhin separat interessant, aber noch
  nicht durch die aktuelle Reproduktionspipeline abgesichert.
- Seeded d-alpha-N-Scan `d=3..8`, `alpha=0.01/0.02`, `N=30k..300k`,
  Seeds `1..5`: kein stabiles `d=3`-Plateau.
- Kontrollierte Scans vom 2026-07-01:
  - Memory-Zeit: `d=3,5,7`, `alpha=0.005/0.01/0.02`, `beta/alpha=1`,
    `eta*alpha=0.02`, `N=300k/1M`, Seeds `1..5`.
  - Memory-Masse: `d=3,5,7`, `alpha=0.01`, `beta/alpha=0.5/1/2`,
    `N=300k/1M`, Seeds `1..5`.
  - Kernel-Skala: `sigma_att=0.10/0.15/0.225`, sonst gleicher Kernslice.
  - High-N-Referenz: `d=5`, `N=100M`, Seed `1`, `D_occ=2.013`,
    `D_win=2.098`.
- Ergebnis: keine getestete Achse liefert bei `N=1M` ein Near-3-Plateau; die
  automatischen Fensterwerte liegen meist im Bereich `2..2.5`, und der
  High-N-Referenzlauf reproduziert den archivierten Near-3-Wert ebenfalls nicht.
- A_att-Transition 2026-07-15: Im korrigierten Skalarslice zeigt `d=10` im
  kompakten Ast `D_cov ~=2.52`, aber zugleich hohe interne `D_mem`-Werte bis
  `9.16`; `d=3` zeigt `D_mem ~=2.95`, aber die rohe Spur bleibt bei
  `D_cov ~=1.8`. Das ist ein starkes Reconciliation-Signal, aber kein
  makroskopischer `d=3`-Selektionssatz.
- 3D-Audit 2026-07-15: `D_mem`, `D_p90` und `D_p95` wachsen mit der
  bereitgestellten Dimension. Der starke Selektionsclaim bleibt damit offen
  bis negativ. Interessant fuer Paper II ist `D_spec memory`, das bei grossen
  `d` gegen etwa 3 laeuft, waehrend `D_center` fuer einen einzelnen driftenden
  Knoten eher eindimensional bleibt.
- Uniformer Weak-Probe-Pilot 2026-07-16: Die kontrollsubtrahierte
  Memory-Zentrumantwort ist isotrop und vollrangig (`3` in `d=3`, `10` in
  `d=10`); die Formantwort ist ueber Seeds nicht reproduzierbar. Das ist eine
  belastbare Negativkontrolle gegen einen aus uniformer Translation gelesenen
  niedrigdimensionalen Response-Claim, entscheidet aber keine lokalisierte
  relationale Wechselwirkung.

Naechster sinnvoller Schritt ist kein weiterer grosser Blindscan, sondern eine
gezielte Reconciliation der Dimensionsdiagnostik: historische
Parameterdefinitionen, Schaetzfenster, Samplingdichte, Memory-Normierung,
Negativkontrollen, Center-Trace-Dimensionen, Eigenwert-Tail-Schwellen,
D_spec-Skalenempfindlichkeit auf echten Rohwolken und relationale Response-Raenge nebeneinanderstellen.
Neue Dimensionsergebnisse muessen `D_occ`, `D_win`, `valid win`, lokale Slopes
und die zugehoerige Memory-/Center-Geometrie gemeinsam berichten.

### P2.3 Innen/Aussen- und Synchronisationsprogramm

Status: Orientierung begonnen; keine Physikclaims.

Die Leitfrage verschiebt sich von eindeutiger `d=3`-Selektion zu:

```text
Koennen intern hochdimensionale Knoten einen gemeinsamen niedrigdimensionalen
externen Wechselwirkungssektor ausbilden?
```

Prioritaet:

1. Abgeschlossen: vollstaendiger `FiniteMemoryState` sowie gemeinsame
   Translation/orthogonale Rotation von Position und Memory-Puffer.
   Selbstkraft- und Form-Invarianz sind synthetisch getestet.
2. Abgeschlossen: gepaarte uniforme Weak-Probe-Kalibrierung auf den vorhandenen
   `N=3M`, `d=3/10`, Seeds `1..5` Snapshots. `+delta`, `-delta`, ungeprobter
   Pfad und `eta_zero` teilen jeweils dieselbe Zukunftsrauschfolge. Die
   Probestarken `0.03` und `0.10` Memory-Radien sind linear und nicht
   destruktiv. Report:
   `reports/response/weak_probe_calibration_2026-07-16.md`.
3. Abgeschlossen: exakte Seed-Signflip-Inferenz neben deskriptivem
   95-Prozent-Energierang. Mit fuenf Seeds ist `p_min=1/16=0.0625`; der Pilot
   darf daher nur auf 90-Prozent-Niveau explorativ gelesen werden.
4. Abgeschlossen: versionierte Referenzzustands-Checkpoints als kontrollierte
   Absprungbasis. Die kanonischen Entwicklungsreferenzen fuer `N=1e8`,
   `d=3/10`, Seed 1 sind auf sauberer Revision `e8f4af2` gebildet,
   checksum-validiert und mit exakt reproduzierbarem Branch-Replay geprueft.
   Vollstaendig bedeutet hier: `x_N` und alle 600 Punkte der implementierten
   Finite-Memory-Naeherung (`M_stored=0.997595`), nicht der formal unendliche
   exponentielle Schwanz. Report:
   `reports/reference_states/scalar_reference_checkpoints_N100M_2026-07-16.md`.
5. Abgeschlossen: geklonter Frozen-Source-Pilot mit freiem,
   `eta_cross=0`- und `eta_zero`-Arm. Der Response ist isotrop vollrangig,
   nicht niedrigdimensional.
6. Abgeschlossen: statischer Potential-/Kraftaudit und sechs-Punkt-
   Distanzleiter von `5 R_mem` bis `1 sigma_rep`. Der aktuelle Cross-Kernel
   loest die interne Quelle nicht auf; die Antwort ist punktmonopolartig und
   bei `A_att=35` auf allen geprueften Skalen attraktiv.
7. Abgeschlossen: separate signierte skalare Cross-Variable
   `s in {-1,0,+1}` im Cross-Kanal, ohne Aenderung des selbstkonfinierenden
   `rho>=0`-Kanals. `s_target=0`, `s_source=0` und freie Pfade sind bitgenau;
   gleiche Produkte sind identisch, der Produkt-Flip kehrt die Antwort um.
8. Abgeschlossen als Architekturtest: der Cross-Kanal verwendet den
   kruemmungsgematchten Drei-Skalen-Kompensator. Die `N=100M`-Checkpoints in
   `d=3/10` bleiben bei der schwachen Probe nondestruktiv. Nur ein Seed pro
   Dimension bedeutet noch keine statistische Evidenz.
9. Naechstes Gate: mindestens sechs, bevorzugt zehn unabhaengige
   Referenzzustaende ohne Retuning; Seeds als Basin-Sampler auswerten:
   `P(knot type | parameters, seed)`.
10. Danach eine feste Distanzleiter unter- und oberhalb des Kraftwechsels mit
    konstantem `eta_cross`. Selbst- und Cross-Kernel bleiben getrennte
    Modellobjekte; Reichweite und Aufloesung sind gegen `R_mem` auszuweisen.
11. Erst nach Seed- und Distanzgate den Quellknoten einseitig dynamisch machen.
    Reziprokes Lesen mit getrennten Memory-Feldern folgt nach Identitaets- und
    Bilanzdiagnostik. Gemeinsames Memory bleibt eine spaetere Modellvariante.
12. Externen Response-Rang als Rang und Stabilitaet der lokalisierten
    Wechselwirkungs-/Antwortmatrix messen. Exakt `3` wird nicht vorgegeben;
    interessant ist ein kontrollgetrennter niedriger Rang ueber Seeds, Lags,
    Probestarken und Basisrotationen.
13. Spin-/Drehimpuls-Kandidaten erst als co-moving Zirkulation, angular
    momentum oder antisymmetrischer Formtensor im Memory-Profil messen; kein
    Standardmodell-Spin-Claim ohne reproduzierbaren Mehrknoten-/Response-Test.
14. Erst bei reproduzierbarer Synchronisation ueber Seeds und kleine
    Parameterstoerungen ueber Paper-III-Analogien sprechen.

Naechster konkreter Schritt: unabhaengige Referenzzustaende fuer das bestehende
signierte Kanal-Gate bilden und die feste Distanzpruefung ohne Retuning
vorbereiten. Erst nach diesen beiden Kontrollen wird die Quelle dynamisch;
reziproke Dynamik bleibt die darauffolgende Stufe.

### P2.4 Paper II / III Guardrails

- Paper II: Propagation, Response-Observable, `c_eff`, lokale Kopplung.
- Paper III: interne Knotenstruktur, Synchronisation, kollektive Moden.
- Keine Quanten-, Eichgruppen-, Teilchen-, Massen- oder Standardmodellclaims,
  bevor stabile Mehrknoten-Synchronisation und externe Response-Subraeume
  reproduzierbar gemessen sind.

## Laufende Hygiene

- Historische Chatnotizen sind Rohmaterial, keine Quelle.
- Lange Laeufe laufen nicht in CI.
- `spectral_dimension` aus `diagnostics.py` ist Geometrie, kein
  Transferoperator-Spektrum.
- Neue Evidenz braucht Parameter, Seeds, Git-Revision, Runtime und Outputpfad.
- Generierte Daten unter `data/processed/` werden erst nach Review als Report
  zusammengefasst und committed.
