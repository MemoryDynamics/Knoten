# Fractal Results Quicklook

Datum: 2026-05-22.

Quelle: `Fraktale/resultsN.csv` und verwandte `resultsN*.csv` Dateien.

Wichtig: Dies ist keine Reproduktion, sondern nur eine Auswertung vorhandener
CSV-Artefakte. Die zugehoerige Laufumgebung ist aktuell nicht lauffaehig.

## Ergebnis in einem Satz

Die vorhandene Spur fuer `D_occ ~ 2.8` ist real in den gespeicherten Daten, aber
sie erscheint in `resultsN.csv` vor allem bei langen Laeufen und Embedding
`dim=5` bzw. teilweise `dim=6`, nicht als einfacher `dim=3 -> D=3` Befund.

## Staerkste Einzelwerte

Aus `Fraktale/resultsN.csv`:

| D_occ | N | run | dim |
| ---: | ---: | ---: | ---: |
| 2.8467834357 | 60,000,000 | 4 | 5 |
| 2.8361133081 | 40,000,000 | 0 | 5 |
| 2.8327877024 | 40,000,000 | 2 | 5 |
| 2.8294028612 | 60,000,000 | 1 | 5 |
| 2.8236819955 | 60,000,000 | 2 | 5 |
| 2.8217262110 | 60,000,000 | 0 | 6 |

## Mittelwerte bei `N = 60,000,000`

| Embedding dim | runs | mean D_occ | min | max |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 5 | 1.818847 | 1.782883 | 1.849573 |
| 3 | 10 | 2.372485 | 2.183700 | 2.508012 |
| 4 | 5 | 2.682259 | 2.602638 | 2.745064 |
| 5 | 5 | 2.810559 | 2.766550 | 2.846783 |
| 6 | 5 | 2.695450 | 2.549664 | 2.821726 |
| 7 | 10 | 1.714175 | 1.675863 | 1.773315 |
| 8 | 5 | 1.863930 | 1.828390 | 1.909408 |
| 9 | 5 | 1.923895 | 1.880816 | 1.947442 |

## Interpretation

Das ist ein guter Hinweis auf eine effektive Dimension nahe 3, aber die
paperfaehige Aussage sollte vorsichtig lauten:

> In long finite-size scaling runs, the occupancy dimension approaches values
> near 2.8 for selected higher-dimensional embedding spaces, most prominently
> around embedding dimension 5 in the current CSV artifacts.

Das stuetzt eher eine Aussage "hoeherer abstrakter Zustandsraum organisiert
sich in eine niedrigere effektive Struktur nahe 3" als eine Aussage "ein
dreidimensionaler Embedder gibt direkt `D=3`".

## Haertungsbedarf

- Den genauen Parametervektor fuer diese CSV-Zeilen manifestieren. Aus
  `Fraktale/FD2.py` ist fuer die Scaling-Analyse wahrscheinlich:
  `eps=0.05`, `eta=2`, `alpha=0.01`, `A=1`, `B=3`, `s1=1`, `s2=0.15`.
- Klaeren, ob alle `dim`-Gruppen mit derselben Skriptversion entstanden sind.
- Bootstrapped confidence intervals statt nur min/max.
- Fit von `D(N)` preregistrieren, nicht nachtraeglich Fenster waehlen.
- `D_occ` mit `D_cov` und `D_spec` auf denselben Runs vergleichen.
- Negative Controls mit gleicher Laufzeit und gleichem Auswertungspfad.

## Red Flag, die man produktiv nutzen sollte

Der fruehere kurze Scan `Fraktale/scan_results.txt` zeigt Mittelwerte nur bis
etwa `1.82`. Die Naehe zu 2.8 erscheint also erst in langen
Finite-Size-Laeufen. Das kann echte asymptotische Struktur sein, oder ein
Laufzeit-/Auswerteartefakt. Genau hier sollte die erste harte Reproduktion
ansetzen.
