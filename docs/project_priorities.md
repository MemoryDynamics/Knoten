# Projektprioritaeten

Stand: 2026-07-09.

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

Status: erledigt im Kontrollreport `reports/long_run_control_report_2026-07-01.md`.

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
   `reports/kernel_sign_convention_correction_2026-07-09.md`.
2. Abgeschlossen: korrigierter q=3-Retest. Historische Baseline und
   `single_scale` dispergieren; `rep_zero` bestaetigt den attraktiven Kanal.
   Report: `reports/corrected_sign_q3_pilot_2026-07-09.md`.
3. Abgeschlossen: Amplitudenhierarchie. Der Drift-Umschlag liegt zwischen
   `A_att=3.5` und `A_att=9`; kompakte Kandidaten liegen bei `A_att=9..35`.
   Report: `reports/amplitude_hierarchy_corrected_sign_q3_2026-07-09.md`.
4. Jetzt: Block-Markov-/AR-Moden auf `A_att=9` und `A_att=35` testen.
5. Photon-/Welleninterpretationen bleiben pausiert, bis ein komplexer oder
   propagierender effektiver Modus gemessen ist.

Wenn der Score traegt:

- Paper-I-Evidenztabelle mit vorsichtiger Claim-Sprache.
- Transferoperatorfeatures auf Long-Run-Daten.

Wenn der Score nicht traegt:

- Residence-Kriterium und Kernelkonventionen ueberarbeiten;
- keine starke Knotenbehauptung in Paper I.

### P1.4 Alpha/M0 und lokale Moden klaeren

Status: Paketkern korrigiert; naechster Schritt ist Reanalyse statt Blindscan.

Die allgemeine Memory-Form ist jetzt technisch im Kernmodell abgebildet als
`rho[n+1]=(1-lambda_m)rho[n]+lambda_m M0 G_sigma`. Der alte Spezialfall
`beta=lambda_m=alpha` bleibt `M0=1`. Konsequenz: Alpha-Laeufe muessen
mindestens `lambda_m`, `M0=beta/lambda_m`, Tail-Cutoff und effektive Kopplung
oder `eta/eta_c` gemeinsam dokumentieren.

Prioritaet:

0. Abgeschlossen: Memory-Form, Sign-Konventionsentscheidung, q=3-Retest und
   Amplitudenhierarchie sind umgesetzt; vorhandene v0.5-Daten vor dem Fix
   sind `legacy-sign`.
1. Jetzt: auf den korrigierten kompakten Kandidaten blockweise coarse-grainen
   und lineare AR-/Transfermoden auf reelle, negative oder komplexe
   Eigenwerte pruefen.
2. Wenn die langsamen Moden rein reell bleiben, den skalaren Memory-Track als
   Relaxationsmodell behandeln und den Vektor-/Phasenmemory-Track priorisieren.
3. Neue Alpha-Scans nur kontrolliert starten: `lambda_m` bei festem `M0` und
   festem Tail-Mass-Cutoff, danach `M0` bei festem `lambda_m`.
4. Photon-/Wellenrichtung pausieren, bis ein stabiler komplexer oder
   propagierender effektiver Modus gemessen ist.

## P2: Spaeter

### P2.1 Transferoperator auf Long-Run-Daten

- Memory-Summary-Features laengerer Laeufe speichern.
- Lag-/Voxel-/Feature-Sensitivitaet wiederholen.
- PCCA/HMM/PMM-Fallbacks erst dann pruefen.

### P2.2 Dimensionsclaim

Status: defensiv lesen; kein `d=3`-Selektionsclaim.

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

Naechster sinnvoller Schritt ist kein weiterer grosser Blindscan, sondern eine
gezielte Reconciliation des Archivbefunds: historische Parameterdefinitionen,
Schaetzfenster, Samplingdichte, Memory-Normierung und Negativkontrollen
nebeneinanderstellen. Neue Dimensionsergebnisse muessen `D_occ`, `D_win`,
`valid win` und lokale Slopes gemeinsam berichten.

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
   no-coupling control.
4. Externen Response-Rang messen: nicht interne Dimension, sondern Rang und
   Stabilitaet der Wechselwirkungs-/Antwortmatrix.
5. Erst bei reproduzierbarer Synchronisation ueber Seeds und kleine
   Parameterstoerungen ueber Paper-III-Analogien sprechen.

Naechster konkreter Schritt nach Paper-I-Confinement: `experiments/synchronization/` mit
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
