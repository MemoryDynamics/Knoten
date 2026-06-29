# Projektprioritaeten

Stand: 2026-06-29.

Diese Seite ist die aktuelle Arbeitsliste nach dem Paper-0-Sprint. Sie
konsolidiert die offenen Punkte aus Paper-Reviews, Architektur-Doku,
Experiment-Katalog und Reproduzierbarkeitsstatus. Ziel ist eine klare
Reihenfolge, nicht eine vollstaendige Ideensammlung.

## Leitentscheidung

Der naechste wichtigste Schritt ist:

**Die Markov-/Transferoperator-Pipeline auf augmentierten Zustaenden in den
Paketkern heben und reproduzierbar validieren.**

Begruendung:

- Paper 0 definiert den mathematischen Anker bereits ausreichend fuer interne
  Weiterarbeit.
- Paper I, Paper II und spaetere Physikclaims haengen jetzt methodisch daran,
  ob Knoten wirklich als metastabile Regime eines Operators auf `z_n`
  gemessen werden koennen.
- Der Code enthaelt mit `src/emergenz_knoten/anchor.py` bereits einen
  Paper-0-nahen Prototypen, aber noch keine saubere additive
  `src/emergenz_knoten/markov/`-Schicht.
- Ohne lagged augmented datasets, Transition Counts, implied timescales,
  CK-Checks und Sensitivitaetsanalysen bleibt die Operator-Sprache eine gute
  Formulierung, aber noch keine robuste Evidenzpipeline.

## P0: Jetzt

### P0.0 Architektur- und Anforderungsdoku nachziehen

Status: umgesetzt. Vor P0.2 sind Begriffe, Datenfluesse,
Akzeptanzkriterien und Nicht-Claims der Markov-Schicht explizit dokumentiert.

Dokumente:

- [Markov-Architektur](markov_architecture.md)
- [Markov-Anforderungen](markov_requirements.md)

### P0.1 Markov-Paketstruktur schaffen

Status: initial umgesetzt. Der Paper-0-Prototyp aus `anchor.py` wurde in eine
klare, testbare Operator-Schicht unter `src/emergenz_knoten/markov/`
ueberfuehrt; `anchor.py` bleibt als Kompatibilitaets-Fassade bestehen.

Vorgeschlagene Module:

```text
src/emergenz_knoten/markov/
  __init__.py
  features.py
  dataset.py
  transition.py
  validation.py
  metastability.py
```

Minimaler Inhalt:

- `features.py`: reduzierte Memory-Summary-Features fuer `z_n`.
- `dataset.py`: lagged pairs `(z_i, z_{i+ell})`, Sample-Lag vs. Update-Lag.
- `transition.py`: State assignment, Transition Counts, row-stochastic
  operators, terminal-row conventions.
- `validation.py`: implied timescales, einfache Chapman-Kolmogorov-Fehler,
  spectral gaps, Bootstrap ueber Seeds.
- `metastability.py`: fast-invariante Mengen oder mindestens slow-mode
  Diagnostik als erster Schritt.

Akzeptanzkriterien:

- Bestehende `anchor.py`-Funktionen bleiben kompatibel oder werden mit klaren
  Re-Exports weitergefuehrt.
- Tests fuer synthetische Markov-Ketten, terminal rows und nichtmarkovsche
  Projektionen existieren.
- `pytest` bleibt gruen.
- Die Paper-0-Pipeline nutzt die neue Schicht, nicht einen isolierten
  Sonderpfad.

Naechster Ausbau:

- Lag-, Voxel- und Feature-Sensitivitaet systematisch auswerten.
- Seed-Bootstrap und eine kleine Evidenztabelle erzeugen.
- Spaeter PCCA/HMM/PMM-Fallbacks pruefen, falls reduzierte Features nicht
  ausreichend markovsch sind.

### P0.2 Kleine Evidenztabelle fuer Paper 0 erzeugen

Ziel: Aus dem vorhandenen Smoke-Test eine belastbarere Mini-Tabelle machen,
ohne einen grossen Dimensions- oder Physikclaim daraus abzuleiten.

Minimaler Sweep:

- `lambda_m = beta = alpha` als normierte Baseline.
- Zwei bis drei `alpha`-Werte.
- Mindestens drei Seeds pro Wert.
- Fester Lag-Satz, plus eine Lag-Sensitivitaetsvariante.
- Eine Negativkontrolle: `eta=0` oder shuffelte Memory-Summaries.

Zu berichten:

- Residence-Statistik.
- Autokorrelationszeit oder grobe Korrelationslaenge.
- Fuehrende nichttriviale Eigenwerte des Operators.
- Implied timescales bzw. Relaxationsraten.
- Sensitivitaet gegen Lag und Diskretisierung.

Akzeptanzkriterien:

- Ergebnis als maschinenlesbares JSON unter `data/processed/anchor_paper/`.
- Kurzer Report unter `reports/`.
- Eine kompakte Tabelle, die Paper 0 als methodische Demonstration tragen
  kann, aber keine Robustheitsclaims ueber breite Parameterbereiche macht.

## P1: Danach

### P1.1 Paper 0 auf Preprint-/Expert-Feedback-Niveau bringen

Offene Punkte aus dem Review:

- Ein sauberer Theorem-/Proposition-Block fuer einen bounded oder compact
  state-space Spezialfall.
- Explizite Kernelklassen: rein repulsiv, rein attraktiv, zweiskalig
  attraktiv-repulsiv.
- Eine kleine Evidenztabelle aus P0.2.
- Klarere Positionierung gegen self-interacting diffusions und reinforced
  processes.

Ziel: Technischer Diskussionsentwurf fuer Expert-Feedback, noch kein
Journal-Submission-Ziel.

### P1.2 Paper I gegen Paper 0 abgleichen

Ziel: Paper I als Minimalmodell konsistent mit dem neuen Anker halten.

Zu pruefen:

- Nutzt Paper I die allgemeine Memory-Form
  `(1-lambda_m) rho_n + beta G_sigma` oder benennt es bewusst die normierte
  Konvention?
- Sind sichtbarer nichtmarkovscher Prozess und augmentierter Markov-Zustand
  eindeutig getrennt?
- Sind Relaxationsraten nur Stabilitaets- oder mass-like proxies?
- Sind Raumzeit-, Dimensions- und Physikclaims sauber als spaeteres Programm
  markiert?

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

## Kurzantwort

Der naechste wichtigste Schritt ist **P0.1: die Markov-/Transferoperator-
Schicht als echte Paket- und Teststruktur bauen**. Das ist der Engpass, der
Paper 0, Paper I, Dimensionsdiagnostik und Paper II gleichzeitig entwirrt.
