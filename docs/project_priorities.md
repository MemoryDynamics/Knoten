# Projektprioritaeten

Stand: 2026-06-29.

Diese Seite ist die aktuelle Arbeitsliste nach dem Paper-0- und
Markov-Paket-Sprint. Sie priorisiert die naechsten Arbeitsschritte und trennt
bewusst zwischen mathematischem Anker, Paper-I-Evidenz und spaeteren
Emergenzprogrammen.

## Leitentscheidung

Der naechste wichtigste Schritt ist jetzt:

**Paper 0 als technischen Anker einfrieren, Paper I konsistent dazu ziehen und
parallel eine echte `n >= 10^7`-Metastabilitaetskampagne laufen lassen.**

Begruendung:

- Die Markov-/Transferoperator-Schicht existiert initial als Paketstruktur
  unter `src/emergenz_knoten/markov/` und ist mit Tests abgesichert.
- Paper 0 traegt als mathematische Einordnung bzw. moegliches Supplement:
  Modell, exponentielles Gedaechtnis, Markov-Einbettung, kontraktive
  Gedaechtnisfaser und metastabilitaetsfaehige Diagnostik.
- Paper 0 traegt noch nicht als eigenstaendiges numerisches Knotenpaper. Die
  kleinen Sensitivitaetslaeufe sind Pipeline-Sanity-Checks, keine robuste
  Knotenexistenz-Evidenz.
- Fuer Paper I ist die kritische Evidenzfrage jetzt empirisch: treten
  langlebige Knoten in reproduzierbaren Long-Runs auf, insbesondere bei
  `n > 10^7`, und trennen sie sich von einfachen Negativkontrollen?

## P0: Jetzt

### P0.0 Markov-Schicht und Anforderungen

Status: umgesetzt.

Vorhanden:

- [Markov-Architektur](markov_architecture.md)
- [Markov-Anforderungen](markov_requirements.md)
- `src/emergenz_knoten/markov/`
- `tests/test_markov.py`
- kleine Seed-/Lag-/Voxel-/Kontroll-Sensitivitaet fuer die Paper-0-Pipeline

Naechster Ausbau bleibt sinnvoll, ist aber nicht mehr der Blocker fuer Paper
0: reichere Memory-Features, Bootstrap ueber Seeds, PCCA/HMM und bessere
Chapman-Kolmogorov-Validierung.

### P0.1 Paper 0 einfrieren

Ziel: Paper 0 als konservativen technischen Anker und moegliches Supplement
fuer Paper I rahmen.

Konkrete Regeln:

- Keine Verkaufsrhetorik fuer robuste Knotenexistenz.
- Die numerische Pipeline nur als methodische Demonstration oder Sanity-Check
  lesen.
- Allgemeine Speicherform
  `(1-lambda_m) rho_n + beta G_sigma` fuehren; die `alpha`-Form ist die
  normierte Konvention `lambda_m=beta=alpha`.
- Aussagen zu `d=3`, endlicher Signalgeschwindigkeit, Lorentzkinematik,
  Quantenmechanik, Standardmodell und physikalischen Massen bleiben Future
  Work bzw. Paper II/III.

Akzeptanzkriterium: Das Paper beantwortet nur
`Modell definieren -> Markov-Einbettung beweisen -> Metastabilitaet messbar
machen`.

### P0.2 Paper I gegen Paper 0 synchronisieren

Ziel: Paper I soll dieselbe mathematische Sprache verwenden, ohne seine
Minimalmodell-Lesbarkeit zu verlieren.

Zu synchronisieren:

- allgemeine Speicherform und normierte `alpha`-Konvention;
- sichtbarer nichtmarkovscher Prozess vs. augmentierter Markov-Zustand;
- `t=alpha n` nur als effektive Reparametrisierung nach Speicherskala;
- Relaxationsraten nur als Stabilitaets- oder mass-like proxies;
- Paper II/III als Folgeprogramme, nicht als Resultate von Paper I.

### P0.3 Long-Run-Metastabilitaet starten

Ziel: Die Beobachtung pruefen, dass metastabile Knoten meist erst bei
`n > 10^7` sichtbar werden.

Dokument:

- [Long-Run Metastability Plan](long_run_metastability_plan.md)

Kanonischer Entry-Point:

```text
experiments/long_run_metastability.py
```

Start klein, aber echt:

- `n=10^7`;
- ein Baseline-Seed;
- danach `eta_zero` und `single_scale`;
- Residence-Zeiten in Update-Einheiten und in Einheiten von `alpha^{-1}`;
- spaeter mehrere Seeds und ggf. groessere `n`.

Nicht verwechseln: Diese Kampagne ist fuer Paper I. Paper 0 braucht sie nicht,
solange Paper 0 keine robuste Knotenexistenz behauptet.

## P1: Naechste Auswertung

### P1.1 Erste Long-Run-Ergebnisse bewerten

Sobald der erste Hintergrundlauf fertig ist:

- JSON auf Vollstaendigkeit pruefen;
- Residence-Ratios gegen Voxelgroesse lesen;
- Laufzeit und Steps/s fuer weitere Seeds abschaetzen;
- entscheiden, ob zuerst mehr Seeds oder zuerst Negativkontrollen laufen.

### P1.2 Paper-I-Evidenztabelle aufbauen

Erst nach Long-Run-Ergebnissen:

- Baseline vs. `eta_zero` vs. `single_scale`;
- mehrere Seeds;
- Residence-Verteilungen statt Einzelbilder;
- Autokorrelation und Dimension nur als Nebenbefunde;
- klare Fail Conditions dokumentieren.

### P1.3 Transferoperator-Schicht erweitern

Nach den ersten Long-Runs:

- Memory-Summary-Features laengerer Laeufe speichern;
- Lag-/Voxel-Sensitivitaet auf Long-Run-Daten wiederholen;
- PCCA/HMM/PMM-Fallbacks pruefen;
- Slow modes gegen Residence-Statistik validieren.

## P2: Spaeter

### P2.1 Dimensionsclaim reproduzieren

Ziel: Den archivierten `D_occ ~ 2.8`-Befund mit expliziten Seeds,
Negativkontrollen und Fitfenster-Sensitivitaet haerten.

Nicht vorher behaupten:

- eindeutige `d=3`-Selektion;
- allgemeine Nichtlokalisierung fuer `d >= 4`;
- harte Dimensionsableitung aus Rekurrenzargumenten.

### P2.2 Paper II: Propagation und `c_eff`

Ziel: Erst nach P0/P1 eine saubere Antwortpipeline fuer Zwei-Knoten- oder
Kick/no-kick-Experimente bauen.

Noetig:

- vorab definierte Response-Observable;
- Onset-Detection mit Threshold-/Smoothing-Sensitivitaet;
- `t_onset(L)`-Fits mit Fehlerbalken;
- Nullmodelle: Memory-Randomisierung, diffusive Baseline, direkte
  Fernkopplungskontrolle.

### P2.3 Paper III und Standardmodell-/Quantenprogramm

Status: bewusst geparkt.

Erst anfassen, wenn:

- metastabile Operatorregime reproduzierbar sind;
- Relaxationsskalen robust gemessen werden;
- Mehrknoten-Wechselwirkungen und Propagation empirisch sauberer sind.

## Laufende Hygiene

- Historische Chatnotizen bleiben Rohmaterial, keine zitierfaehigen Quellen.
- Neue Evidenz braucht Parameter, Seeds, Git-Revision, Runtime und
  Outputpfad.
- `spectral_dimension` aus `diagnostics.py` bleibt eine Geometrie-Diagnostik,
  kein Transferoperator-Spektrum.
- Paper-Claims werden konsequent als `definition`, `numerical observation`
  oder `conjecture` markiert.
- Long-Run-Ausgaben unter `data/processed/` bleiben generiert; relevante
  Resultate werden erst nach Pruefung als Report committed.

## Kurzantwort

Paper 0 traegt als mathematischer Anker. Der naechste wichtigste Schritt fuer
die Projekt-Evidenz ist **nicht** ein weiteres Kurzlaufdiagramm, sondern der
erste echte Long-Run mit `n >= 10^7`, danach Negativkontrollen und erst dann
eine belastbare Paper-I-Evidenztabelle.
