# Fractal Parameter Landscape Reading

Datum: 2026-06-13

## Scope

Gelesene Quellen:

- `experiments/fractal_analysis/Fraktale/FD2.py`
- `experiments/fractal_analysis/Fraktale/Fraktaldimension.py`
- `experiments/fractal_analysis/Fraktale/fit_n_plot.py`
- `experiments/fractal_analysis/Fraktale/analyze_peaks.py`
- `experiments/fractal_analysis/Fraktale/results.csv`
- `experiments/fractal_analysis/Fraktale/resultsN.csv`
- `experiments/fractal_analysis/Fraktale/resultsN_*.csv`
- `docs/ChatGPT Chatverlaeufe/Fraktaldimensionen.md`
- `experiments/fractal_analysis/reproduce_dimension_pilot.py`

Ziel war nicht ein neuer Sweep, sondern eine belastbare Lesart der vorhandenen
Fraktal- und Dimensionsdaten als Grundlage fuer die naechsten Laeufe.

## Two Distinct Evidence Classes

Die vorhandenen Dateien mischen zwei verschiedene Experimentklassen, die
getrennt bleiben muessen.

### Short Parameter Scan

Quelle: `results.csv` und `scan_results.txt`.

Skriptpfad: `FD2.py`, Funktion `parameter_scan()`.

Parameter:

- `N = 300,000`
- `eps in {0.02, 0.05, 0.1, 0.2}`
- `alpha in {0.005, 0.01, 0.02}`
- `B in {2, 3, 4}`
- `dim in {2, 3, 4, 5}`
- nominal 5 runs per point, aber ohne explizite Seed-Spalte

Wichtig: Dieser Scan erreicht keine Near-3-Dimension. In `results.csv` gibt es
keine Zeile mit `Deff > 2.2`.

Top-Gruppen nach Mittelwert:

| eps | alpha | B | dim | runs | mean Deff | min | max |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.05 | 0.005 | 4 | 4 | 5 | 1.816135 | 1.524920 | 1.996965 |
| 0.05 | 0.005 | 3 | 3 | 5 | 1.801598 | 1.642168 | 1.868423 |
| 0.02 | 0.020 | 4 | 2 | 9 | 1.773209 | 1.751294 | 1.792898 |
| 0.05 | 0.020 | 2 | 3 | 5 | 1.771996 | 1.701491 | 1.845098 |

Ueber `eps`, `B` und Runs gemittelt ist in diesem kurzen Scan fuer alle drei
Alpha-Werte `dim=3` der beste Embedder:

| alpha | best dim | mean Deff |
| ---: | ---: | ---: |
| 0.005 | 3 | 1.728157 |
| 0.010 | 3 | 1.711680 |
| 0.020 | 3 | 1.693022 |

Das ist ein short-N-Befund. Er darf nicht mit dem long-N-Near-3-Befund
gleichgesetzt werden.

### Long Finite-Size Scan

Quelle: `resultsN.csv` und `resultsN_*.csv`.

Skriptpfad: `FD2.py`, Funktion `scaling_analysis()`.

Rekonstruierter Parametervektor:

- `eps = 0.05`
- `eta = 2`
- `alpha = 0.01`
- `A = 1`
- `B = 3`
- `sigma_rep = 1`
- `sigma_att = 0.15`
- `max_memory = 300`
- `points = traj[20000::10]`
- historischer Box-Counting-Schaetzer

Dieser Scan ist die eigentliche Quelle des `D_occ ~ 2.8`-Befunds. Die beste
Embedding-Dimension driftet mit `N`:

| N | best dim by group mean | mean D_occ |
| ---: | ---: | ---: |
| 50,000 | 2 | 1.340937 |
| 100,000 | 2 | 1.546269 |
| 300,000 | 3 | 1.730075 |
| 1,000,000 | 3 | 2.121150 |
| 2,500,000 | 3 | 2.281537 |
| 6,000,000 | 4 | 2.432605 |
| 15,000,000 | 6 | 2.678042 |
| 40,000,000 | 5 | 2.778427 |
| 60,000,000 | 5 | 2.810559 |

Bei `N = 60,000,000` ist die Run-Struktur:

| run | D_occ dim=3 | D_occ dim=4 | D_occ dim=5 | D_occ dim=6 | best dim |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 2.357146 | 2.658142 | 2.766550 | 2.821726 | 6 |
| 1 | 2.483793 | 2.602638 | 2.829403 | 2.549664 | 5 |
| 2 | 2.411544 | 2.745064 | 2.823682 | 2.661830 | 5 |
| 3 | 2.379472 | 2.723595 | 2.786378 | 2.747719 | 5 |
| 4 | 2.230470 | 2.681857 | 2.846783 | 2.696309 | 5 |

Interpretation: Der Near-3-Befund ist kein direkter `dim=3 -> D=3`-Befund.
Er ist ein long-N-Befund in hoeherem Einbettungsraum, vor allem `dim=5`, mit
mindestens einem Run, in dem `dim=6` staerker ist.

## Alpha Is Not A Single Isolated Knob

Im historischen Fraktal-Skript ist die Updategleichung:

```text
x[n] = x[n-1] + eps * noise + eta * alpha * force
```

Damit veraendert `alpha` gleichzeitig:

- die Speicher-Zerfallsrate
- die nominelle Speicherlaenge `int(5 / alpha) + 1`
- wegen `max_memory = 300` die tatsaechlich gespeicherte Gesamtmasse
- die effektive Kraftkopplung `eta * alpha`

Fuer die bisherige Alpha-Menge:

| alpha | uncapped horizon | used horizon | stored weight mass | eta * alpha |
| ---: | ---: | ---: | ---: | ---: |
| 0.005 | 1001 | 300 | 0.777708 | 0.010 |
| 0.010 | 501 | 300 | 0.950959 | 0.020 |
| 0.020 | 251 | 251 | 0.993723 | 0.040 |

Das ist eine harte Konfundierung. Ein Alpha-Sweep mit historischem Cap ist
interessant, aber er beantwortet nicht allein die Frage "Was macht alpha?".
Er beantwortet eher:

> Was macht alpha, wenn zugleich Speicher-Masse, Cutoff und Kraftskala
> mitveraendert werden?

## Seed/Run Caveat

Die historischen CSVs enthalten eine Spalte `run`, aber keine explizit
protokollierten Seeds. Deshalb ist `run` aktuell nur ein Wiederholungsindex,
keine reproduzierbare Seed-ID.

Konsequenz:

- Aussagen wie "seed 1 waehlt Dimension 3" sind mit den CSVs allein nicht
  belastbar.
- Fuer neue Sweeps muessen Seeds explizit in Manifest und Ergebnisdatei
  stehen.
- Ein Ergebnis sollte immer als Verteilung ueber Seeds formuliert werden:
  mean, min/max, bootstrap CI, und best-dim-Haeufigkeit.

## Model-Family Caveat

Der Fraktal-Archivpfad ist nicht identisch mit dem spaeteren kanonischen Kern:

- Fraktalarchiv: `eps=0.05`, `eta=2`, `alpha=0.01`, `B=3`, `sigma_att=0.15`,
  Update mit `+ eta * alpha * force`.
- Kanonischer Paper-II-Kern: anderer Parameterbereich, anderer attraktiver
  Skalenbereich, Updatekonvention `x + epsilon noise - eta * grad`.

Die Resultate duerfen daher nicht ohne Mapping vermischt werden. Fuer Paper-
Haertung braucht es entweder:

1. eine bewusste Entscheidung, den Fraktal-Archivpfad als eigenes Modellregime
   zu behandeln, oder
2. eine Migration des Near-3-Befunds in den kanonischen Kern mit dokumentierter
   Parameterabbildung.

## Proposed Next Sweeps

### Sweep 1: Historical Alpha Sweep

Ziel: reproduzieren, wie der archivierte Pfad auf `alpha` reagiert.

Parameter:

- `dim in {3, 4, 5, 6}`
- `alpha in {0.005, 0.0075, 0.01, 0.015, 0.02}`
- `eps = 0.05`
- `eta = 2`
- `B = 3`
- `sigma_rep = 1`
- `sigma_att = 0.15`
- `max_memory = 300`
- `N ladder = {300k, 1M, 2.5M}` als erste ressourcenschonende Stufe
- 3 Seeds initial, 5 Seeds fuer Kandidaten

Wert: Dieser Sweep bleibt historisch kompatibel.

Grenze: Er bleibt absichtlich konfundiert.

### Sweep 2: Fixed Memory-Mass Alpha Sweep

Ziel: Alpha-Effekt von Speicher-Cap-Artefakten trennen.

Variante:

- `max_memory = ceil(5 / alpha) + 1` fuer jede Alpha-Stufe, sofern Ressourcen
  reichen, oder
- feste Tail-Mass-Definition, z.B. Horizon so waehlen, dass mindestens 95 %
  der exponentiellen Gewichtsmasse enthalten sind.

Wert: Testet, ob die beobachtete Dimension wirklich an der Zerfallsrate haengt
oder am historischen Cap.

### Sweep 3: Fixed Coupling Sweep

Ziel: Alpha-Effekt von Kraftskalen-Effekt trennen.

Variante:

- historische Kopplung: `eta = 2`
- normierte Kopplung: `eta * alpha = 0.02`, also `eta = 0.02 / alpha`

Wert: Testet, ob die Dimensionsverschiebung durch Speicherzeit oder durch
Kraftstaerke entsteht.

### Sweep 4: Controls Only After Signal

Negativkontrollen sind teuer. Sie sollten nicht blind fuer alle Punkte laufen,
sondern zuerst dort, wo Baseline `D_occ > 2` zeigt.

Prioritaet:

1. `shuffled_memory`, weil diese Kontrolle direkt die Altersstruktur des
   Speichers trifft.
2. `eta_zero`, als Brownian/Random-Walk-artiger Nullpfad.
3. `single_scale`, um zu testen, ob die zweite Skala wirklich notwendig ist.

## Immediate Action Items

1. GitHub default branch auf `main` setzen. Lokal und remote existiert `main`;
   GitHub zeigt ohne UI/API-Umstellung vermutlich noch auf `master`.
2. Numba-faehige Projektumgebung dokumentieren oder reparieren. Die Codex-
   Runtime hatte kein `numba`, PowerShell laut Nutzer aber offenbar schon.
3. `reproduce_dimension_pilot.py` um einen Alpha-Sweep-Modus erweitern, statt
   neue Einzelskripte zu erzeugen.
4. Ergebnisformat erweitern: `seed`, `alpha`, `eta`, `eta_alpha`,
   `used_horizon`, `stored_weight_mass`, `condition`, `D_occ`, `D_cov`,
   `D_spec`.
5. Erste Laufmatrix: historical alpha sweep bis `N=300k/1M/2.5M`, dann anhand
   der besten Punkte entscheiden, ob `6M` lokal vertretbar ist.
