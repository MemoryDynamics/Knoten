# Repository Code Review - Remediation

Stand: 2026-07-15
Ausgangsreview: [Repository Code Review](repository_code_review_2026-07-15.md)
Scope: Umsetzung der Findings CR-01 bis CR-08 sowie angrenzender Fehler, die
waehrend der Korrektur und Verifikation gefunden wurden.

## Ergebnis

Alle acht Findings aus dem Review sind im Code behoben und mit
Regressionstests abgedeckt. Historische Ergebnisdateien wurden bewusst nicht
still umgeschrieben. Sie bleiben reproduzierbar, tragen aber weiterhin die
damals berechneten Metriken. Neue beziehungsweise neu erzeugte Reports
verwenden die korrigierten Definitionen.

| Finding | Status | Umsetzung |
| --- | --- | --- |
| CR-01 | behoben | Der mittlere Radius einer gewichteten Cloud verwendet jetzt dieselben normalisierten Gewichte wie Zentrum und Kovarianz. Der alte Wert bleibt als `unweighted_mean_radius` explizit verfuegbar. |
| CR-02 | behoben | `axis_ratio_min_max` misst jetzt die Rundheit in der ambienten Einbettung und wird bei kollabierten Achsen null. `axis_ratio_intrinsic_min_max` erhaelt die alte intrinsische Interpretation. |
| CR-03 | behoben | Der Default-`D_spec` basiert auf einer skalenaufgeloesten Heat Trace und liefert nur bei einem stabilen Plateau einen Skalar. Die alte Heuristik bleibt ausschliesslich als `legacy_row` verfuegbar. |
| CR-04 | behoben | Genau ein Eigenwert nahe +1 wird als stationaerer Perronmodus entfernt. Periodische -1-Moden und weitere +1-Moden bleiben erhalten und ergeben korrekt eine Spektralluecke von null. |
| CR-05 | behoben | Relaxationseigenwerte und Raten sind jetzt ausgerichtete Arrays. Das vollstaendige Spektrum bleibt separat in `eigenvalues`; die zu den Raten gehoerenden Werte stehen in `relaxation_eigenvalues`. |
| CR-06 | behoben | Reportloader lehnen doppelte Faelle, gemischte Kohorten und nicht gematchte Case/Control-Konfigurationen ab. Neue Long-Run-Faelle speichern zusaetzlich `base_config`. |
| CR-07 | behoben | Core-, Markov-, Vektor- und Long-Run-Simulation verwenden dieselbe zentrale Konfigurationsvalidierung. Nichtendliche Parameter und ungueltige Integer/Burn-in-Werte werden vor der Simulation abgewiesen. |
| CR-08 | behoben | Alle aktiven Dynamics-Skripte sind im CLI-Katalog; CI installiert und startet Ruff vor Tests und Dokumentationsbuild. Ein Regressionstest prueft die Katalogvollstaendigkeit. |

## Spektraldimension

Die neue Diagnose baut einen dichtekorrigierten Diffusionskernel auf einer
lokalen k-Nachbar-Skala. Aus den Eigenwerten des normalisierten
Graph-Laplacians wird

[
Z(t) = sum_i exp(-tmu_i)
]

und daraus die skalenabhaengige Dimension

[
d_s(t) = -2,rac{dlog Z(t)}{dlog t}
]

berechnet. Kurzzeitige Diskretisierungsartefakte und die endliche
Langzeitsaettigung werden aus der Fenstersuche ausgeschlossen. Nur ein
zusammenhaengendes, ausreichend breites und lokal stabiles Plateau erzeugt
einen skalaren Wert. Fehlt dieses Plateau, ist das Ergebnis absichtlich
`NaN` statt einer scheinpraezisen Dimensionszahl.

Die Kalibrierungstests treffen fuer einen diskretisierten Kreis etwa
`D_spec = 1` und fuer einen flachen 2-Torus etwa `D_spec = 2`. Die
problematischen hochrangigen Gauss-Surrogate werden nicht mehr zwangsweise auf
einen plausibel aussehenden Skalar abgebildet.

Methodische Anker sind die Diffusion-Maps-Konstruktion von
[Coifman und Lafon](https://pmc.ncbi.nlm.nih.gov/articles/PMC1140422/) und die
Definition der Spektraldimension ueber den Abfall der
[Random-Walk-Rueckkehrwahrscheinlichkeit](https://arxiv.org/abs/1711.00836).
Die Implementierung bleibt eine konservative endliche Punktwolken-Diagnose,
kein theorematischer Dimensionsbeweis.

## API- und Datenmigration

Folgende Semantiken haben sich absichtlich geaendert:

- `shape_statistics()["mean_radius"]` ist bei uebergebenen Gewichten nun
  gewichtet. Der fruehere Wert steht unter `unweighted_mean_radius`.
- `axis_ratio_min_max` ist ambient; fuer die Rundheit nur im aktiven
  Unterraum ist `axis_ratio_intrinsic_min_max` zu verwenden.
- `spectral_dimension(...)` verwendet standardmaessig die neue
  Heat-Trace-Diagnose. Historische Reproduktion erfordert explizit
  `normalization="legacy_row"`.
- `implied_relaxation_rates` gibt ein gefiltertes, zu den Raten
  ausgerichtetes Eigenwertarray zurueck.
- `TransferOperatorEstimate` enthaelt neu `relaxation_eigenvalues`.
- Neue Long-Run-Case-JSONs enthalten sowohl die konditionierte `config` als
  auch die unveraenderte `base_config`.

Bereits gespeicherte JSON- und Markdown-Ergebnisse behalten ihre historischen
Werte. Insbesondere Memory-Kompaktheits-Scorecards,
Memory-Center-Residence-Radien und alle `D_spec`-Aussagen muessen aus den
Quelldaten neu erzeugt werden, bevor sie als korrigierte Resultate zitiert
werden.

Die Paper-I-Hauptdiagnosen aus dynamischem gewichteten RMS-Radius und
gewichteter Kovarianzdimension `D_mem` verwenden bereits andere, korrekte
Pfade. Sie wurden durch CR-01 nicht numerisch veraendert.

## Zusaetzlich behobene Fehler

Waehrend der Umsetzung wurden weitere konkrete Defekte gefunden:

- score-versionsabhaengige Defaultpfade verhindern, dass ein v0.4/v0.5-Lauf
  versehentlich die v0.3-Ausgabe ueberschreibt;
- Summaries filtern jetzt auch unendliche Werte statt nur `NaN`;
- ein durch den neuen Defaultpfad sichtbarer fehlender
  `output_json`-Bindungsschritt wurde durch Ruff gefunden und korrigiert;
- Punktwolken, Lag-Zeiten und Transfermatrizen werden auf endliche Werte
  geprueft;
- der Markov-Datensatz besitzt keine abweichende Kopie der
  Simulationsvalidierung mehr;
- CLI-Vollstaendigkeit wird automatisch gegen alle Skripte unter
  `experiments/current` getestet.

## Verifikation

Die finale Verifikation umfasst:

- `131 passed` mit Warnungen als Fehler;
- `ruff check` fuer `src`, `tests`, `experiments/current` und das
  Experiment-CLI;
- `mkdocs build --strict`;
- `pip check`;
- `compileall` fuer Paket, aktive Experimente und Tests;
- direkte Gegenbeispiele fuer gewichtete Radien, Rangdefizienz, periodische
  und reduzible Markov-Ketten, gemischte Reportkonfigurationen sowie
  nichtendliche Eingaben.

## Verbleibende Hinweise

Die neue Heat-Trace-Implementierung verwendet eine dichte Distanz- und
Eigenwertberechnung und ist daher fuer die derzeitigen Diagnose-Stichproben,
nicht fuer beliebig grosse Punktwolken gedacht. Fuer groessere Datenmengen
waere ein sparse kNN/Lanczos-Pfad eine eigenstaendige Performance-Aufgabe.

Neue korrigierte wissenschaftliche Reports sollten erst nach einem gezielten
Re-Run der jeweils zitierten Kohorte committed werden. Diese Remediation
aendert Code und Tests, erfindet aber keine Ersatzdaten fuer historische
Simulationen.
