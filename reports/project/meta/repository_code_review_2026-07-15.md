# Repository Code Review

Stand: 2026-07-15  
Review-Basis: `75c5e80` (`main`, identisch zu `origin/main` zu Review-Beginn)  
Umsetzung: [Repository Code Review - Remediation](repository_code_review_remediation_2026-07-15.md)

Scope: kanonischer Paketkern unter `src/emergenz_knoten`, aktive Analyse- und
Reportpfade unter `experiments/current`, Tests, CI und aktuelle
Dimensions-/Paper-I-Datenfluesse.

## Kurzfazit

Das Repository ist strukturell deutlich besser als die historische
Experimentlandschaft vermuten laesst: Paketkern, aktive Entry-Points, Tests und
kuratierte Reports sind klar getrennt. Die komplette Testsuite und der strikte
Dokumentationsbuild laufen durch.

Trotzdem gibt es vier correctness-relevante Befundgruppen, die vor neuen
Dimensions-, Shape- oder Transferoperator-Claims behoben werden sollten:

1. Zwei Memory-Shape-Ausgaben entsprechen nicht ihrer dokumentierten Bedeutung:
   `mean_radius` ist trotz uebergebener Gewichte ungewichtet, und
   `axis_ratio_min_max` ignoriert kollabierte Achsen.
2. `spectral_dimension` ist nach der Korrektur der symmetrischen
   Kernel-Normalisierung weiterhin kein kalibrierter Dimensionsschaetzer. Die
   eigenen Rank-Kontrollen zeigen, dass ein Rank-15-Gauss-Cloud bei der
   Defaultskala einen Wert nahe drei liefern kann.
3. Die Transferoperator-Helfer entfernen alle Eigenwerte mit Betrag eins als
   "stationaer". Dadurch verschwinden periodische oder nichtmischende Modi wie
   `lambda=-1`, und die Spektralluecke kann falsch oder undefiniert werden.
4. Mehrere Reportpfade validieren nicht, dass Faelle wirklich ueber denselben
   Parameter-Slice aggregiert beziehungsweise gegen einen gematchten Kontrolllauf
   verglichen werden.

Die aktuelle Paper-I-Hauptzahl fuer den co-moving Radius stammt aus dem separat
gewichteten dynamischen RMS-Pfad und ist von Befund CR-01 nicht betroffen. Auch
`D_mem` selbst wird aus der gewichteten Kovarianz berechnet. Betroffen sind vor
allem Memory-Kompaktheits-Scorecards, finale Memory-Center-Residence-Radien,
degenerierte Shape-Kontrollen, `D_spec`-Interpretationen und zukuenftige
Transferoperator-/Modenanalysen.

## Priorisierte Findings

### CR-01 — Hoch: `mean_radius` einer gewichteten Memory-Cloud ist ungewichtet

Fundstellen:

- `src/emergenz_knoten/diagnostics.py:94-127`
- `src/emergenz_knoten/knot_score.py:153-156,292-316`
- `experiments/current/dynamics/long_run_metastability.py:1327-1334`

`shape_statistics` normalisiert die Gewichte und verwendet sie fuer Zentrum und
Kovarianz. Der anschliessend ausgegebene `mean_radius` wird aber als
`radii.mean()` ueber alle gespeicherten Altersklassen gebildet. Der ebenfalls
ausgegebene `rms_radius` ist dagegen ueber die Kovarianz korrekt gewichtet.

Minimalbeispiel:

```text
points = [[0], [10]], weights = [0.999, 0.001]
weighted center                 = 0.01
reported mean_radius            = 5.0
true weighted mean radius       = 0.01998
reported weighted rms_radius    = 0.31607
```

Auswirkung:

- `memory_mean_radius()` dokumentiert den Wert als Radius der gewichteten
  Memory-Cloud und verwendet ihn fuer den Memory-Kompaktheitsgewinn.
- Der finale `memory_center`-Residence-Test verwendet denselben Wert als
  Basisradius.
- Reports bezeichnen die Kennzahl als Memory-Radius, ohne den tatsaechlich
  ungewichteten Altersklassen-Mittelwert offenzulegen.

Fuer den aktuellen `d=3`, `A_att=35`, `N=30M`-Slice sinkt der Kontroll-/Aktiv-
Kompaktheitsgewinn beim Ersatz durch den gewichteten RMS-Radius seedweise von
`7.72..12.76` auf `4.31..6.49`. Die Score-Komponente bliebe damit in diesem
Slice oberhalb ihrer Pass-Schwelle, ihre berichtete Groesse ist aber deutlich
ueberhoeht. Andere Slices nahe einer Schwelle koennen ihre Klassifikation
aendern.

Empfehlung:

- `mean_radius = sum(normalized_weights * radii)` verwenden.
- Den bisherigen Wert bei Bedarf explizit als `unweighted_mean_radius`
  versionieren, statt seine Semantik still zu aendern.
- Betroffene KnotScore- und Memory-Center-Residence-Reports nach der
  Metrikversionierung neu erzeugen.
- Einen stark unbalancierten Gewichtstest wie das Minimalbeispiel aufnehmen.

### CR-02 — Hoch: Kollabierte Clouds koennen als perfekt rund erscheinen

Fundstellen:

- `src/emergenz_knoten/diagnostics.py:97-119`
- `src/emergenz_knoten/knot_score.py:136-162,294-316`

Fuer `axis_ratio_min_max` werden Eigenwerte unterhalb eines Floors entfernt;
das Minimum wird danach nur unter den verbleibenden positiven Eigenwerten
gesucht. Damit misst die Kennzahl die Rundheit im intrinsisch nichtkollabierten
Unterraum, obwohl Dokumentation und Verbraucher sie als Rundheit in der
Einbettung behandeln.

Reproduktion in 3D:

```text
Cloud                         covariance eigenvalues     axis_ratio_min_max
exakte Linie                  [0.34, 0, 0]                1.0
isotroper Kreis/Plane         [0.5, 0.5, 0]               1.0
```

Beide Clouds besitzen in der 3D-Einbettung kollabierte Achsen. Ein Wert von
`1.0` widerspricht der Docstring-Aussage, kollabierte Clouds sollten gegen null
gehen. Der KnotScore verwendet diesen Wert als `memory_roundness` und zaehlt
bereits seine Existenz zusammen mit `D_mem` als nichtdegenerierte Shape.

Die aktuellen vollrangigen `N=30M`-Referenzclouds sind nicht das
Minimalgegenbeispiel; dort ist die berichtete Min/Max-Ratio numerisch sinnvoll.
Der Fehler ist besonders relevant fuer `epsilon=0`, `alpha=1`, kleine Samples,
eingefrorene Kontrollen und zukuenftige Dimensionskollaps-Tests.

Empfehlung:

- Zwei explizite Metriken einfuehren:
  `ambient_axis_ratio_min_max = sqrt(lambda_min_all/lambda_max)` und optional
  `intrinsic_axis_ratio_min_max` auf dem positiven Unterraum.
- `memory_shape_valid` an Rang beziehungsweise kumulative Varianz koppeln, nicht
  nur an das Vorhandensein zweier Zahlen.
- Tests fuer Linie, Plane und volle isotrope 3D-Cloud aufnehmen.

### CR-03 — Hoch: `D_spec` ist weiterhin nicht als Dimension kalibriert

Fundstellen:

- `src/emergenz_knoten/diagnostics.py:439-501`
- `experiments/current/dynamics/long_run_metastability.py:1068-1103`
- `experiments/current/dynamics/dspec_sensitivity_report.py:259-318`
- `reports/dimensions/dspec_sensitivity_2026-07-15.md`

Die symmetrische Normalisierung behebt den frueheren algebraischen Fehler, eine
nichtsymmetrische row-normalisierte Matrix an `eigvalsh` zu uebergeben. Die
anschliessende Kennzahl

```text
log(number_of_selected_eigenvalues) / log(lambda_max / mean(lambda))
```

ist jedoch weder ueber einen Heat-Trace-Skalierungsbereich noch ueber eine
Eigenwert-Zaehllaw kalibriert. Sie wird im Long-Run-Pfad weiterhin mit genau
einem Default-Bandwidth-Faktor als `dimension` gespeichert.

Die bereits committed Rank-Kontrollen belegen das Problem bei
`bandwidth_factor=1`:

```text
true Gaussian rank     reported heat proxy
1                      1.624
3                      1.788
10                     2.760
15                     3.051
```

Eine unabhaengige Wiederholung mit Rank 15 ergab fuer `n=120,240,480` Werte von
etwa `2.78, 2.88, 3.15`. Ein Wert nahe drei kann damit gerade aus einer deutlich
hoeherdimensionalen Cloud entstehen. Der Sensitivitaetsreport zieht bereits die
richtige Claim-Grenze; die Produktions-API und das gespeicherte Feld tragen aber
weiter den staerkeren Namen `spectral_dimension` beziehungsweise `D_spec`.

Empfehlung:

- Bis zur Kalibrierung in neuen Runs als `spectral_geometry_proxy` benennen oder
  hinter einer expliziten Experimental-Option deaktivieren.
- Roh-Snapshots plus Gewichtsinformation persistieren und mehrere Bandwidth-/kNN-
  Skalen pro Fall speichern.
- Einen etablierten skalenbasierten Schaetzer implementieren, etwa die Steigung
  des Heat-Traces/Return-Probability-Fensters oder eine validierte
  Eigenwert-Zaehllaw.
- Akzeptanztests muessen bekannte Linien, Flaechen, Sphaeren/Manifolds, volle
  Gauss-Clouds, verschiedene Punktzahlen und verrauschte Einbettungen abdecken.
- Kein einzelnes `D_spec ~= 3` in Claim-Tabellen aufnehmen; der bestehende
  Guardrail sollte verbindlich bleiben.

### CR-04 — Hoch: Periodische und reduzible Operator-Modi werden entfernt

Fundstellen:

- `src/emergenz_knoten/markov/validation.py:151-187`
- `src/emergenz_knoten/markov/metastability.py:10-38`
- `experiments/current/anchors/anchor_sensitivity_analysis.py:165-182`

`implied_relaxation_rates`, `implied_timescales` und
`leading_nontrivial_eigenvalues` klassifizieren ueber `abs(lambda) ~= 1`.
Damit wird nicht nur der stationaere Perron-Eigenwert `+1` entfernt, sondern
auch ein periodischer Eigenwert `-1`, komplexe Einheitskreis-Modi und weitere
`+1`-Eigenwerte einer reduziblen Kette.

Minimalbeispiel fuer die deterministische Zwei-Zustands-Flip-Kette:

```text
P = [[0, 1], [1, 0]]
eigenvalues                  = [1, -1]
implied_relaxation_rates     = []
implied_timescales           = []
leading_nontrivial           = []
spectral_gap                 = NaN
```

Mathematisch besitzt die Kette einen nicht abklingenden periodischen Modus und
eine Spektralluecke von null. Gerade fuer zukuenftige Phasen-, Oszillations- und
slow-mode-Analysen ist das derzeitige Verhalten riskant.

Empfehlung:

- Stationaritaet anhand der Naehe zu `lambda=+1` behandeln, nicht anhand des
  Betrags allein.
- Nur einen Perron-Modus entfernen, wenn Irreduzibilitaet/Einfachheit belegt ist;
  weitere `+1`-Modi muessen eine Luecke von null signalisieren.
- `lambda=-1` und komplexe Einheitskreis-Modi als nicht abklingend mit
  unendlicher Timescale beziehungsweise Rate null behalten.
- Periodische, reduzible und komplexe Testmatrizen ergaenzen.

### CR-05 — Mittel: Eigenwert- und Ratenarrays sind nicht indexgleich

Fundstellen:

- `src/emergenz_knoten/markov/validation.py:151-163`
- `src/emergenz_knoten/markov/transition.py:147-160`

`implied_relaxation_rates` gibt alle sortierten Eigenwerte zurueck, entfernt
stationaere Werte aber nur aus der separat aufgebauten Ratenliste. Fuer

```text
P = [[0.9, 0.1], [0.2, 0.8]], lag_time=2
```

entsteht `eigenvalues=[1.0, 0.7]`, aber `rates=[0.178337...]`. Index null der
Rate gehoert also nicht zu Index null der Eigenwerte. Die Dataclass
`TransferOperatorEstimate` legt beide Arrays nebeneinander ab, ohne diese
Nichtausrichtung zu kennzeichnen.

Empfehlung:

- Entweder dasselbe Filter auf beide Arrays anwenden und ein Paar
  `(nonstationary_eigenvalues, rates)` liefern,
- oder ein gleichlanges Ratenarray mit explizitem Marker fuer stationaere Modi
  verwenden.
- Im Datentyp die Zuordnung als strukturierte Mode-Records statt paralleler
  Arrays abbilden.

### CR-06 — Mittel: "Matched controls" sind in generischen Reports nicht erzwungen

Fundstellen:

- `experiments/current/markov/knot_score_report.py:78-98,174-208`
- `experiments/current/dynamics/ambient_dimension_memory_shape_report.py:231-250`
- aehnliche Gruppierungslogik in
  `experiments/current/dynamics/dynamic_center_trace_report.py:387-405`

Der generische KnotScore-Loader reduziert alle Eingaben auf
`(condition, seed)`, behaelt bei Kollisionen den Fall mit den meisten Schritten
und paart den aktiven Fall anschliessend nur ueber den Seed mit `eta_zero`.
Dimension, `alpha`, `epsilon`, Kernelparameter, Memory-Masse, Schrittzahl und
Sampling werden nicht als Matching-Key validiert. Bei frei uebergebenen
`--source-dir`-Listen kann so ein numerisch plausibler, aber physikalisch nicht
gematchter Score entstehen.

Der Ambient-Report gruppiert nur nach `(dim, condition)`, obwohl mehrere
Source-Verzeichnisse erlaubt sind. Unterschiedliche `steps` oder weitere
Parameter werden gemeinsam aggregiert; das Feld `steps` wird danach schlicht
vom ersten Gruppeneintrag uebernommen.

Die aktuell committed Standardreports verwenden weitgehend homogene
Verzeichnisse. Das Risiko liegt in Wiederverwendung und Erweiterung der
generischen Entry-Points.

Empfehlung:

- Einen kanonischen Case-Key beziehungsweise Config-Hash definieren, der alle
  fuer den Vergleich erforderlichen Parameter enthaelt.
- Kontrollpaarung bei jeder Abweichung hart abbrechen und die Differenzen
  ausgeben.
- Doppelte `(config_hash, condition, seed)`-Faelle nicht still ueberschreiben.
- Aggregatoren muessen Homogenitaet pruefen oder `steps` und relevante Parameter
  in den Gruppierungsschluessel aufnehmen.

### CR-07 — Mittel: Konfigurationsvalidierung ist unvollstaendig und dupliziert

Fundstellen:

- `src/emergenz_knoten/core.py:50-81`
- `src/emergenz_knoten/markov/dataset.py:64-86`
- `experiments/current/dynamics/long_run_metastability.py:1609-1647`

Die kanonische Core-Validierung prueft unter anderem nicht, ob `epsilon`, `eta`,
`amplitude_rep` und `amplitude_att` endlich sind. Die Markov-Simulation besitzt
eine abweichende Kopie der Validierung, in der unter anderem Burn-in,
Memory-Faktor und Kernelbreiten fehlen. Der Long-Run-Pfad prueft wiederum eine
eigene Teilmenge und ruft die Core-Validierung nicht auf.

Reproduktion:

```text
SimulationConfig(epsilon=NaN)       wird akzeptiert und erzeugt NaN-Samples
SimulationConfig(eta=NaN)           wird akzeptiert und erzeugt NaN-Samples
SimulationConfig(amplitude_rep=NaN) wird akzeptiert und erzeugt NaN-Samples
Markov-Simulation mit burn_in=-2    wird akzeptiert
```

In Reportpfaden mit `allow_nan=False` faellt der Fehler dadurch oft erst nach
einem Lauf beim Serialisieren auf.

Empfehlung:

- Eine einzige oeffentliche Validierungsfunktion oder `SimulationConfig`-
  `__post_init__` verwenden.
- Alle numerischen Parameter mindestens auf Endlichkeit und ihre dokumentierten
  Wertebereiche pruefen.
- Jeder Simulator und Runner muss dieselbe Validierung aufrufen.
- Parametrisierte Negativtests fuer alle Felder ergaenzen.

### CR-08 — Niedrig: Entry-Point- und Quality-Gates sind hinter dem Repo-Stand

Fundstellen:

- `experiments/cli.py:24-33`
- `.github/workflows/ci.yml`
- `requirements-dev.txt`

Die Dynamics-Liste der CLI enthaelt die neuen kritischen Skripte
`aatt_transition_report.py`, `dimension_claim_audit.py` und
`dspec_sensitivity_report.py` nicht. Der dokumentierte zentrale Entry-Point
findet damit gerade die aktuellen Dimensions-Guardrails nicht.

Die CI fuehrt Tests und einen strikten MkDocs-Build aus, aber keinen Linter,
keine Typpruefung und keine kleinen mathematischen Invariantentests ausserhalb
der Pytest-Suite. `ruff` ist in der lokalen Dev-Umgebung und in
`requirements-dev.txt` nicht vorhanden.

Empfehlung:

- CLI-Katalog aus einem deklarativen Manifest oder automatischer Discovery
  erzeugen und auf existierende Skripte testen.
- Mindestens `ruff check`, optional eine schrittweise Typpruefung, in die CI
  aufnehmen.
- Die in diesem Review verwendeten mathematischen Minimalgegenbeispiele als
  Regressionstests einbauen.

## Verifikation

Ausgefuehrt auf Python 3.12.13 mit den gepinnten Runtime-Abhaengigkeiten:

```text
pytest tests -q --basetemp .pytest-tmp/code-review
117 passed

pytest tests -q --basetemp .pytest-tmp/code-review-werror -W error
117 passed

python -m compileall -q src experiments/current experiments/fractal_analysis
                         experiments/propagation_speed tests
erfolgreich

python -m mkdocs build --strict
erfolgreich

python -m pip check
No broken requirements found.
```

Der erste lokale Pytest-Aufruf ohne `--basetemp` traf auf einen gesperrten
globalen Windows-Temp-Ordner; dies war ein Sandbox-/Umgebungsproblem. Mit einem
Workspace-Temp-Verzeichnis lief dieselbe Suite vollstaendig durch.

## Empfohlene Reihenfolge

1. CR-01 und CR-02 gemeinsam korrigieren, Shape-Metriken versionieren und die
   betroffenen Score-/Residence-Reports neu erzeugen.
2. CR-04 und CR-05 vor jeder weiteren Transferoperator-, Phasen- oder
   Modeninterpretation beheben.
3. `D_spec` gemaess CR-03 umbenennen beziehungsweise deaktivieren, dann den
   bereits geplanten Roh-Cloud- und Skalen-Retest mit kalibriertem Schaetzer
   durchfuehren.
4. CR-06 und CR-07 als Reproduzierbarkeits-Barriere vor neuen Sweeps schliessen.
5. CLI und CI nachziehen und alle Minimalgegenbeispiele dauerhaft als
   Regressionstests verankern.

## Claim-Auswirkung

- **Paper I, dynamischer co-moving RMS-Radius:** nicht durch CR-01 betroffen.
- **Paper I, gewichtetes `D_mem`:** die gewichtete Kovarianzformel ist von CR-01
  nicht betroffen.
- **Paper I, Roundness im aktuellen vollrangigen Referenzslice:** kein belegter
  Zahlenwechsel durch CR-02; die Metrik ist aber fuer degenerierte Kontrollen
  nicht sicher.
- **KnotScore-Memory-Kompaktheit und Memory-Center-Residence:** durch CR-01
  betroffen und neu zu rechnen.
- **`D_spec ~=3`:** bleibt zu Recht ein Hypothesenhinweis ohne Claim-Status;
  CR-03 bestaetigt, dass ein einzelner Wert keine Dimension belegt.
- **Transferoperator-/slow-mode-/Phasenclaims:** vor Behebung von CR-04/CR-05
  nicht belastbar.
