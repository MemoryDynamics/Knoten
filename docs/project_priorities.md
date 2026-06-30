# Projektprioritaeten

Stand: 2026-06-30.

Diese Seite ist die aktive Arbeitsliste. Sie ersetzt die alte Action Matrix
und den Hardening Plan: Was Codex autonom ziehen kann, steht hier direkt als
Prioritaet; was Haukes Entscheidung braucht, ist als Entscheidungspunkt
markiert.

## Leitentscheidung

**Paper 0 ist als mathematischer Anker ausreichend. Der naechste Engpass ist
Paper-I-Evidenz: Baseline gegen Negativkontrollen und Seeds haerten.**

Begruendung:

- Die Markov-/Transferoperator-Schicht existiert initial im Paketkern und ist
  getestet.
- Paper 0 behauptet keine robuste Knotenexistenz und braucht daher keine
  weiteren Long-Run-Daten, um als technischer Anker nuetzlich zu sein.
- Paper I darf robuste Knoten erst behaupten, wenn Long-Run-Baseline und
  Kontrollen klar getrennt sind.

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

Status: naechster operativer Schritt.

Baseline ist abgeschlossen:

- `n=10^7`, Seed `1`, `alpha=0.01`, `dim=3`;
- bestes Residence-Verhaeltnis `256 alpha^{-1}`;
- Laufzeit etwa `338 s`;
- noch keine robuste Evidenz ohne Kontrollen.

Aktuell liegen vor:

1. Baseline-Seed-Ensemble `1..5`.
2. `eta_zero`-Seed-Ensemble `1..5`.
3. `single_scale`-Seed-Ensemble `1..5`.

Als Naechstes: alle drei Bedingungen in einem Kontrollreport vergleichen.

### P1.2 Auswertung nach Kontrollen

Akzeptanz fuer einen Paper-I-Befund:

- Baseline trennt sich klar von `eta_zero` und `single_scale`.
- Residence-Ratios sind nicht nur ein Voxel-Artefakt.
- Git-Revision, Seeds, Burn-in, Sampling und Runtime sind dokumentiert.
- Ergebnis wird als Report committed, nicht nur als lokale JSON-Datei gelesen.

### P1.3 Danach entscheiden

Wenn die Kontrollen tragen:

- mehrere Seeds fuer Baseline und Kontrollen;
- Voxel- und Sampling-Sensitivitaet;
- Paper-I-Evidenztabelle.

Wenn die Kontrollen nicht tragen:

- Parameterdiagnose statt Paper-Claim;
- pruefen, ob Residence-Kriterium, Kernelklasse oder Speicherhorizont zu grob
  sind;
- keine starke Knotenbehauptung in Paper I.

## P2: Spaeter

### P2.1 Transferoperator auf Long-Run-Daten

- Memory-Summary-Features laengerer Laeufe speichern.
- Lag-/Voxel-/Feature-Sensitivitaet wiederholen.
- PCCA/HMM/PMM-Fallbacks erst dann pruefen.

### P2.2 Dimensionsclaim

- Archivierten `D_occ ~ 2.8`-Befund separat mit expliziten Seeds,
  Negativkontrollen und Fitfenster-Sensitivitaet haerten.
- Seeded d-alpha-N-Scan `d=3..8`, `alpha=0.01/0.02`, `N=30k..300k`,
  Seeds `1..5`, defensiv lesen: kein stabiles `d=3`-Plateau.
- Keine eindeutige `d=3`-Selektion behaupten.

### P2.3 Paper II / III

- Paper II: Propagation, Response-Observable, `c_eff`, lokale Kopplung.
- Paper III: Quanten-/Standardmodellprogramm.
- Beide bleiben Folgeprogramme hinter reproduzierbarer Metastabilitaet.

## Laufende Hygiene

- Historische Chatnotizen sind Rohmaterial, keine Quelle.
- Lange Laeufe laufen nicht in CI.
- `spectral_dimension` aus `diagnostics.py` ist Geometrie, kein
  Transferoperator-Spektrum.
- Neue Evidenz braucht Parameter, Seeds, Git-Revision, Runtime und Outputpfad.
- Generierte Daten unter `data/processed/` werden erst nach Review als Report
  zusammengefasst und committed.
