# Dimension Claim Seed Audit

Datum: 2026-06-13

Quelle:

- `experiments/fractal_analysis/archive_source/data/n_scaling/resultsN.csv`
- Analyse-Skript: `experiments/fractal_analysis/analyze_dimension_claim.py`

## Ergebnis

Der archivierte `D_occ ~ 2.8/3`-Befund ist in `resultsN.csv` reproduzierbar
nachvollziehbar, aber er muss seed- und embedding-bewusst formuliert werden.

Staerkster Gruppenbefund:

| embedding dim | N | runs | mean D_occ | min | max | population std |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 60,000,000 | 5 | 2.810559 | 2.766550 | 2.846783 | 0.029533 |

Staerkster Einzelwert:

| embedding dim | N | run | D_occ |
| ---: | ---: | ---: | ---: |
| 5 | 60,000,000 | 4 | 2.846783 |

## Largest-N Vergleich

Bei `N = 60,000,000`:

| embedding dim | runs | mean D_occ | min | max |
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

Die belastbare Formulierung ist aktuell:

> In the archived finite-size occupancy data, the strongest effective
> dimension signal near 3 appears in a higher embedding space, most clearly
> for embedding dimension 5 at `N = 60,000,000`, where five runs cluster around
> `D_occ = 2.81`.

Nicht belastbar waere dagegen:

> The current data prove that the model uniquely selects three dimensions.

Fuer diese staerkere Aussage fehlen noch:

- frische seed-kontrollierte Reproduktion
- Negativkontrollen
- robuste Fitfenster
- Vergleich von `D_occ`, `D_cov` und `D_spec` auf denselben Laeufen
- klare Begruendung, warum embedding `dim=5` die effektiv physikalische
  Dimension nahe 3 staerkt

## Naechster Reproduktionsschritt

Der naechste sinnvolle Lauf ist kein kompletter Blind-Sweep, sondern ein
gezieltes Seed-Ensemble fuer den historischen Gewinner:

```text
embedding dim = 5
N ladder = 1e6, 6e6, 15e6, 40e6, 60e6
seeds/runs >= 10, besser 20
diagnostics = D_occ, D_cov, D_spec
negative controls = shuffled memory, eta=0, single-scale kernel
```

Da die lokalen `.venv`-Umgebungen aktuell defekt sind, sollte vor diesem Lauf
eine neue saubere Python-Umgebung erstellt werden.
