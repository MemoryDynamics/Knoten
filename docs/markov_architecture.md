# Markov-/Transferoperator-Schicht: Architektur

Stand: 2026-06-29.

Diese Seite erklaert die neue Schicht unter `src/emergenz_knoten/markov/`.
Sie ist bewusst als technische Orientierung geschrieben: Welche Begriffe
meinen was, wie fliesst ein Simulationslauf durch die Pipeline, und wo liegen
die Grenzen der aktuellen Implementierung?

## Warum diese Schicht existiert

Das Modell hat zwei Ebenen:

- `x_n`: sichtbare Position im Update-Schritt `n`.
- `rho_n` bzw. der konkrete Memory-Buffer: gespeicherte Vergangenheit.

Der sichtbare Prozess `x_n` ist im Allgemeinen nicht markovsch, weil sein
naechster Schritt vom Memory-Zustand abhaengt. Der augmentierte Zustand

```text
z_n = (x_n, memory_n)
```

ist dagegen die natuerliche Markov-Einbettung. Die neue Markov-Schicht soll
diese Aussage numerisch operational machen: Aus simulierten Trajektorien
werden reduzierte augmentierte Features, daraus Sample-Paare, daraus
Transition Counts und daraus ein endlicher Operator.

## Keine physikalische Zeit in der Paket-API

Die Schicht verwendet absichtlich keine physikalische Zeitvariable `t`.

Begriffe:

| Symbol / Name | Bedeutung |
| --- | --- |
| `n` | urspruenglicher Update-Index der Simulation |
| `i` | Index eines gespeicherten Samples |
| `z_n` | mathematischer augmentierter Zustand beim Update `n` |
| `z_i` | gespeicherte Feature-Reprasentation eines Samples |
| `sample_lag` oder `ell` | Abstand in Sample-Indizes |
| `lag_updates` | Abstand in urspruenglichen Update-Schritten |
| `lag_time` | rein numerischer Nenner fuer Raten, keine physikalische Zeit |

Eine Reparametrisierung von Updates zu effektiver Zeit gehoert in spaetere
Analyse- oder Paper-Schichten. Sie wird nicht in der Paket-API vorausgesetzt.

## Datenfluss

Minimaler Flow:

```text
SimulationConfig
  -> simulate_augmented_features(...)
  -> samples, sample_steps, augmented_features
  -> lagged pairs (z_i, z_{i+ell})
  -> state labels
  -> transition counts
  -> row-stochastic transition matrix
  -> eigenvalues, implied timescales, CK diagnostics
  -> metastability summaries
```

Wichtig: `augmented_features` sind aktuell reduzierte Features, nicht der
vollstaendige Memory-Zustand. Das ist eine diagnostische Approximation.

## Module

### `features.py`

Zweck: Einen expliziten Memory-Buffer in eine kurze Feature-Reprasentation
ueberfuehren.

Aktuelle Features:

- sichtbare Position `x`;
- gewichteter Memory-Schwerpunkt;
- Offset `x - memory_centroid`;
- Memory-Spread;
- mittlere Distanz des Memory-Buffers zur aktuellen Position;
- gespeicherte Memory-Masse.

Grenze: Diese Features sind verlustbehaftet. Sie beweisen nicht, dass die
reduzierte Projektion selbst markovsch ist.

### `dataset.py`

Zweck: Sample-indexed Trajektorien und Lagged Datasets erzeugen.

Wichtige Objekte:

- `AugmentedTrajectory`: Samples, Update-Indizes, Features und finaler Memory.
- `LaggedDataset`: Paare `(z_i, z_{i+ell})` plus `sample_lag` und optional
  `lag_updates`.

### `transition.py`

Zweck: Aus Features endliche Zustandslabels und Transition-Matrizen schaetzen.

Aktueller Baseline-Pfad:

- Voxel-Labels fuer Features.
- Transition Counts fuer einen Sample-Lag.
- Zeilenstochastische Normalisierung.
- Explizite Behandlung leerer terminaler Zeilen.

Grenze: Voxel sind eine robuste Baseline, aber noch keine finale
metastability decomposition.

### `validation.py`

Zweck: Erste Qualitaetsdiagnostik fuer geschaetzte Operatoren.

Aktuell:

- Vektor-Autokorrelation;
- implied relaxation rates;
- implied timescales;
- Chapman-Kolmogorov-Fehler fuer einfache Matrixvergleiche.

### `metastability.py`

Zweck: Kleine Helfer fuer langsame Moden.

Aktuell:

- fuehrende nichttriviale Eigenwerte;
- einfacher spectral gap.

Das ist noch nicht PCCA, HMM oder PMM.

### `anchor.py`

`src/emergenz_knoten/anchor.py` ist jetzt eine Kompatibilitaets-Fassade.
Fruehere Paper-0-Imports funktionieren weiter, aber die Implementierung liegt
unter `src/emergenz_knoten/markov/`.

## Out of Scope

Die aktuelle Markov-Schicht behauptet nicht:

- physikalische Zeit;
- stationaere effektive Dimension;
- robuste Knotenexistenz ueber Parameterbereiche;
- Lorentz-Kinematik oder endliche Signalgeschwindigkeit;
- dass reduzierte Features die vollstaendige Markov-Eigenschaft exakt
  bewahren;
- dass Voxel-Zustaende die beste Diskretisierung sind.

## Aktueller Reifegrad

Status: initiale Paket- und Teststruktur.

Bereits vorhanden:

- reduzierte augmentierte Features;
- sample-indexed Lagged Datasets;
- Transition Counts und row-stochastic matrices;
- implied rates/timescales;
- einfache CK- und slow-mode helpers;
- Paper-0-Pipeline nutzt die Schicht;
- Tests fuer Kernverhalten.

Noch offen:

- systematische Lag-Sensitivitaet;
- Voxel-/Feature-Sensitivitaet;
- Seed-Bootstrap;
- Negativkontrollen;
- PCCA/HMM/PMM-Fallbacks;
- vollstaendige Memory-Snapshots oder reichere Feature-Familien.
