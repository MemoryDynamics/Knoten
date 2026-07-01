# Projektprioritaeten

Stand: 2026-07-01.

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
  - High-N-Referenz: `d=5`, `N=100M`, Seed `1`, `D_occ=2.013`.
- Ergebnis: keine getestete Achse liefert bei `N=1M` ein Near-3-Plateau; der
  High-N-Referenzlauf reproduziert den archivierten Near-3-Wert ebenfalls nicht.

Naechster sinnvoller Schritt ist kein weiterer grosser Blindscan, sondern eine
gezielte Reconciliation des Archivbefunds: historische Parameterdefinitionen,
Schaetzfenster, Samplingdichte, Memory-Normierung und Negativkontrollen
nebeneinanderstellen.

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
