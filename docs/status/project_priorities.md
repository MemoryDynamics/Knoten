# Projektprioritaeten

Stand: 2026-07-15.

Diese Seite ist die aktive Arbeitsliste. Sie ersetzt die alte Action Matrix
und den Hardening Plan: Was Codex autonom ziehen kann, steht hier direkt als
Prioritaet; was Haukes Entscheidung braucht, ist als Entscheidungspunkt
markiert.

## Leitentscheidung

**Paper 0 ist als mathematischer Anker ausreichend. Der naechste Engpass ist
Paper-I-Evidenz nach Korrektur der Kernel-Vorzeichenkonvention.**

Begruendung:

- Die Markov-/Transferoperator-Schicht existiert initial im Paketkern und ist
  getestet.
- Paper 0 behauptet keine robuste Knotenexistenz und braucht daher keine
  weiteren Long-Run-Daten, um als technischer Anker nuetzlich zu sein.
- Paper I darf robuste Knoten erst behaupten, wenn Residence, Kompaktheit,
  Voxel-Stabilitaet und Kontrolltrennung gemeinsam tragen.

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

Status: erledigt im Kontrollreport `reports/long_runs/controls/long_run_control_report_2026-07-01.md`.

Ergebnis:

- Die bisherigen Long-Run-Kontrollen waren reproduzierbar, gehoeren aber zur
  `legacy-sign`-Konvention.
- Der Kernelgradient wurde korrigiert, damit `A_rep` lokal repulsiv und
  `A_att` breit attraktiv im Sinn von `K=A_rep G_rep-A_att G_att` wirkt.
- Paper-I-Evidenz muss deshalb neu aufgebaut werden. Alte Reports bleiben als
  Audit der Vorzeichenhistorie nuetzlich, nicht als Evidenz fuer das
  korrigierte Potentialmodell.

Paper-I-Lesart: offen bis zum korrigierten Retest. Der aktuelle Claim lautet
nur: Das Modell und die Diagnostik sind definiert; die stabile Knotenexistenz
muss unter korrigierter Sign-Konvention neu gehaertet werden.

### P1.2 Knotenkriterium v0.5 verwenden

Status: Scorecard v0.5 ist das aktuelle Kandidatenkriterium; sie nutzt raw update residence und gated degenerierte Memory-Clouds.

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
- Shape-/Radius-Metriken bleiben ueber mehrere Memory-Zeiten begrenzt.
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
    Ergebnis: Paper I darf den lokalen 3D-Memory-Shape-Befund im gewaehlten
    3D-Slice als Teaser nutzen. Ein starker ambient-unabhaengiger 3D-Claim
    wird nicht gestuetzt, weil `D_mem`, `D_p90` und `D_p95` mit `d` wachsen.
    Paper-II-Hebel ist `D_spec memory`, das bei grossen `d` in Richtung 3
    laeuft. Report: `reports/dimensions/dimension_claim_audit_2026-07-15.md`.

Aktueller naechster Schritt:

- Paper-I-Text und ggf. Supplement auf Evidenztabelle, Feature-Closure und die
  defensiv formulierte Memory-Shape-/3D-Teaser-Grenze synchronisieren.
- Keine Photon-, Spin-, physikalische Masse- oder feste-Zentrum-Sprache in
  Paper I; skalares Memory ist erste Grobkoernung fuer
  Kompaktheit/Radius/Relaxation.
- Paper-II-Dimensionsfrage methodisch weiter treiben: zuerst D_spec-
  Bandbreiten-/kNN-Sensitivitaet, dann relationaler Response-Rang mit zweitem
  Knoten oder schwachem externem Feld. Keine weiteren Dimensions-Blindscans
  als Hauptpfad.
- Erst danach gezielte `lambda_m`/`sigma`/Amplitudenachsen in der neuen
  Scorecard-Sprache fortsetzen.

### P1.4 Alpha/M0 und lokale Moden klaeren

Status: Paketkern korrigiert; `N=30M`-Reanalyse ist erledigt, naechster Schritt ist Paper-I-Synchronisierung auf Evidenztabelle, 3D-Memory-Shape und Feature-Closure.

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

### P2.1 Transferoperator auf Long-Run-Daten

Status: Long-Run-Trace-AR und Feature-Closure erledigt; noch kein geschlossener Transferoperatorbefund.

- Abgeschlossen: Block-AR auf dem `N=30M`-Endfenster. Komplexe Klassifikationen sind nicht kontrollgetrennt von `eta_zero`.
- Abgeschlossen: Feature-Closure. Aktive Shape-/Radius-Scalars sind vorhersagbar; Spin-Scalar nicht.
- Naechste Haertung: Memory-Summary-Features laengerer Laeufe und Feature-Closure-Kriterien speichern.
- Lag-/Voxel-/Feature-Sensitivitaet wiederholen.
- PCCA/HMM/PMM-Fallbacks erst dann pruefen.

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

Naechster sinnvoller Schritt ist kein weiterer grosser Blindscan, sondern eine
gezielte Reconciliation der Dimensionsdiagnostik: historische
Parameterdefinitionen, Schaetzfenster, Samplingdichte, Memory-Normierung,
Negativkontrollen, Center-Trace-Dimensionen, Eigenwert-Tail-Schwellen,
D_spec-Skalenempfindlichkeit und relationale Response-Raenge nebeneinanderstellen.
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

1. Einzelknoten-Observablen extrahieren: Zentrum, Formtensor, Radius,
   lokale Moden, optionale Phase, Residence.
2. Seeds als Basin-Sampler auswerten: `P(knot type | parameters, seed)`.
3. Zwei-Knoten-Synchronisation testen: shared memory, weak cross-potential,
   no-coupling control. Mesonartige Zwei-Knoten-Bindung und baryonartige
   Drei-Knoten-Bindung sind getrennte Folgeprogramme, nicht Voraussetzung fuer
   den Einzelknoten-Score.
4. Externen Response-Rang messen: nicht interne Dimension, sondern Rang und
   Stabilitaet der Wechselwirkungs-/Antwortmatrix. Eine spaetere Ladungs-
   diagnose muss als Antwort auf andere Knoten definiert werden, nicht als
   isoliertes Ein-Knoten-Label.
5. Spin-/Drehimpuls-Kandidaten erst als co-moving Zirkulation, angular
   momentum oder antisymmetrischer Formtensor im Memory-Profil messen; kein
   Standardmodell-Spin-Claim ohne reproduzierbaren Mehrknoten-/Response-Test.
6. Erst bei reproduzierbarer Synchronisation ueber Seeds und kleine
   Parameterstoerungen ueber Paper-III-Analogien sprechen.

Naechster konkreter Schritt nach Paper-I-Confinement: `experiments/current/memory/synchronization/` mit
Single-Knot-Observable-Extractor und synthetischen Tests fuer Phase-Locking,
Cross-Correlation und Response-Rank fuellen.

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
