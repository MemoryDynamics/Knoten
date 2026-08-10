# Review der relevanten Dynamik- und Modenmodule

Stand: 2026-08-04  
Review-Basis: `254b51b`; Correctness-Fix: `3a68e58`; saubere
Reproduktionen: P3.1 auf `3a68e58`, P3.2 auf `9b6bd5e`.

## Kurzurteil

Der Updatekern und die Ringpufferfortsetzung zeigen im geprueften Pfad keinen
neuen Vorzeichen- oder Altersindexfehler. Der wichtigste Defekt lag in der
Messschicht: Der isotrope `2 x 2`-Modenfit verwendete einen einzigen
Mittelwert und Intercept fuer alle Ambientkoordinaten. Dadurch konnte ein
exakter komplexer Modus um koordinatenspezifische Gleichlagen als reelles
Modenpaar erscheinen.

Dieser Fehler ist behoben und durch ein konstruiertes Gegenbeispiel getestet.
Die unveraenderten P3.1-/P3.2-Laeufe bleiben danach dennoch bei `0/60` bzw.
`0/80` nichtreellen Segmentfits. Der registrierte **AR(1)-Messnullbefund** ist
damit robust. Er ist aber kein Beweis, dass der augmentierte Telegraph-Zustand
keine komplexen Moden besitzt.

Die Vermutung eines zu grossen relativen Rauschens ist plausibel und gezielt
testbar. Ein weiterer roher Epsilon- oder Lambda-Sweep waere dagegen derzeit
methodisch falsch.

## Priorisierte Findings

### DR-01 - Hoch, behoben: koordinatenspezifische Gleichlagen wurden vermischt

Betroffen waren `fit_isotropic_relative_mode` und die nachfolgende
Phasenkohaerenz. Der alte Fit poolte Zeit und Ambientkoordinaten, zog danach
aber nur einen globalen Mittelwert ab. Eine feste Trennung entlang der ersten
Achse und Nullgleichlagen in den Querachsen erzeugen verschiedene affine
Fixed Effects, obwohl dieselbe isotrope Uebergangsmatrix gilt.

Konstruiertes Gegenbeispiel:

```text
A = [[0.96, -0.12], [0.12, 0.96]]
wahre Eigenwerte                 = 0.96 +/- 0.12 i
alter gepoolter Fit              = 0.999883, 0.960680
altes Residuenverhaeltnis        = 9.90e-4
```

Der Fehler war gefaehrlich, weil selbst das kleine Residuum die reelle
Fehlklassifikation nicht sichtbar machte. Der korrigierte Panel-Fit verwendet
einen gemeinsamen isotropen Uebergang, aber einen Intercept je Koordinate.
Der Regressionstest rekonstruiert Matrix und komplexes Paar bis `1e-12`.

Nachlauf: P3.1 bleibt `0/60`, P3.2 `0/80`. Die bisherigen Klassifikationen
aendern sich numerisch nicht, ihre Messdefinition ist nun korrekt.

### DR-02 - Hoch, offen: P3.2 beobachtet keinen Markov-abgeschlossenen Zustand

Der Telegraph-Arm evolviert mindestens Feld und konjugierten Impuls. Der
primaere Fit sieht nur `(x_-, m_-)`. Nach Projektion des verborgenen
Mediatorzustands ist dieses Paar im Allgemeinen ein ARMA-/Delay-Prozess und
kein AR(1)-Markovzustand. Reelle `2 x 2`-Regressionswerte schliessen daher
komplexe Eigenwerte des augmentierten Systems nicht aus.

Belastbare Aussage:

```text
Im registrierten koordinatenbereinigten (x_-,m_-)-AR(1)-Readout wurde kein
stabiler komplexer Modus gefunden.
```

Nicht belastbar waere:

```text
Das retardiert gekoppelte augmentierte System besitzt keine komplexe Mode.
```

Vor einer Mechanismusentscheidung braucht es entweder exponierte reduzierte
Feld-/Impulsobservablen oder einen vorregistrierten Hankel-/Delay-Fit mit
Lag-Stabilitaet und synthetischen Observability-Kontrollen.

### DR-03 - Hoch, offen: ein Lambda-Sweep waere aktuell konfundiert

In einem gespeicherten `FiniteMemoryState` liegen die exponentiellen Gewichte
bereits fest. Die direkten Fortsetzungen verwenden diese Gewichte; `alpha` in
einem nachtraeglich geaenderten `SimulationConfig` reparametrisiert den Zustand
nicht. Im Telegraph-Pfad wuerde es zusaetzlich den Mediator-Zeitschritt aendern.
Ein Config-Override waere deshalb keine saubere Lambda-Variation.

Zusaetzlich gilt fuer den endlichen Speicher

```text
H = min(max_memory, floor(memory_factor/lambda)),
M_ret/M0 = 1 - (1-lambda)^H.
```

Bei `lambda=0.001`, `max_memory=800` waeren nur etwa `55.1%` statt etwa
`99.75%` der beabsichtigten stationaeren Masse enthalten. Lambda und
Trunkierung wuerden gemeinsam variiert.

Auch analytisch rettet Lambda den direkten aktuellen Ast nicht. Mit
`g=0.432291` und `c=0.02` existiert fuer kein Lambda ein komplexes direktes
Fenster, weil darin `c>g` notwendig ist. Bei festem `g` oeffnet sich irgendein
Fenster erst fuer

```text
lambda > g/(1-g) = 0.761466,
```

und verlangt ungefaehr `c=0.44..0.57`; bei `lambda=1` kollabiert das Fenster
wieder auf eine reelle Doppelwurzel. Das waere ein anderer Kurzzeitmemory- und
Starkkopplungsast, keine moderate Korrektur von `lambda=0.01, c=0.02`.

### DR-04 - Mittel, offen: die relative Rauschleistung ist sehr gross

Fuer den verwendeten `d=3`-Checkpoint gilt

```text
R                         = 2.1165e-4
epsilon                   = 1.0e-4
RMS Rauschschritt/Knoten  = sqrt(3) epsilon / R = 0.818 R
RMS in x_-                = sqrt(3/2) epsilon / R = 0.579 R
```

Die zwei Knoten besitzen unabhaengige Rauschstreams. Diese Streams sind nur
ueber die Kontrollarme hinweg identisch; "common noise" bedeutet hier nicht
gemeinsames Rauschen zwischen den Knoten. Relative schwache Moden koennen so
schlecht identifizierbar sein.

Ein global kleineres Epsilon ist jedoch kein guter erster Test. Fruehere
Ein-Knoten-Slices zeigen im linearen Regime, dass Radius, Rauschen und Drift
proportional mitskalieren und das dimensionslose Rausch-/Driftverhaeltnis nahe
konstant bleibt.

Der diskriminierende Test haelt die marginale Rauschvarianz jedes Knotens
fest und variiert nur die Korrelation:

```text
xi_1 = sqrt((1+rho)/2) xi_c + sqrt((1-rho)/2) xi_r
xi_2 = sqrt((1+rho)/2) xi_c - sqrt((1-rho)/2) xi_r.
```

Fuer `rho={0,0.9,0.99}` sinkt der relative RMS-Schritt von `0.579 R` auf
`0.183 R` und `0.0579 R`, ohne die Einzelknoten-Rauschleistung zu aendern.

### DR-05 - Mittel, offen: der isotrope Fit ist kein raeumlicher Spinfit

Der aktuelle gemeinsame `2 x 2`-Fit koppelt sichtbare und Memorykoordinate
innerhalb derselben Ambientachse. Eine Rotation von `x` nach `y` oder ein
antisymmetrischer raeumlicher Generator liegt ausserhalb dieser Modellklasse.
Der Fit testet eine Phase zwischen `x_-` und `m_-`, nicht Spin oder Orbit im
ambienten Raum. Dafuer braucht es getrennt einen rotationskovarianten
`2d x 2d`-Fit oder vorregistrierte antisymmetrische Winkelobservablen.

### DR-06 - Mittel, offen: `path_gradient.coupling` ist nur ein Schalter

Der Parameter namens `coupling` skaliert in `_continuation.path_gradient` den
Gradienten nicht. Nur der Spezialfall `coupling == 0` liefert frueh null; die
eigentliche Skalierung geschieht anschliessend im Aufrufer. Die aktuellen
Paarpfade multiplizieren genau einmal und sind numerisch konsistent. Die API
laedt aber zu Doppel- oder Fehlskalierung ein und sollte auf einen expliziten
Boolean `enabled` umgestellt oder in Gradient plus Schritt getrennt werden.

### DR-07 - Mittel, behoben: Plotfehler vernichteten teure Ergebnisse

Die aktiven Synchronisationsskripte schrieben Figur, Report und erst danach
die JSON-Summary. Ein real aufgetretener PNG-Berechtigungsfehler verwarf so
einen abgeschlossenen 175-Sekunden-Lauf. Die maschinenlesbare Summary wird nun
vor dem Plot persistiert; ein Regressionstest erzwingt dieses Verhalten.

### DR-08 - Evidenzgrenze: Zukunftsseeds sind keine Formationsseeds

P3.1/P3.2 verwenden fuenf Zukunftsrauschpfade aus demselben reifen
`N=100M`-Checkpoint. Das testet Pfadrobustheit innerhalb eines Basins, nicht
Basin- oder Anfangsbedingungsrobustheit. Eine positive Modenkandidatur braeuchte
anschliessend unabhaengige Formationszustaende; fuer den jetzigen negativen
Screen ist die Einschraenkung explizit zu erhalten.

## Was derzeit nicht als Fehler erscheint

- Der korrigierte Zwei-Gauss-Vorzeichenpfad stimmt zwischen Kern und
  Fortsetzung ueberein.
- Der Ringpuffer bleibt alterssortiert; die juengste Deposition wird vor dem
  naechsten Update an den Kopf geschrieben.
- Checkpoints pruefen Horizont, Gewichtsfunktion, Arraychecksummen und
  `x == memory[0]`.
- Channel-off und direkter P3.1-Kontrollarm werden bitgenau gegen bestehende
  Implementierungen getestet.
- Die `lambda=1`-Randbedingung des analytischen Fensterhelfers ist korrigiert:
  Determinante und Minimaldiskriminante erlauben dort kein nichtreelles Paar.

## P3.2a/b-Nachlauf

Beide Reviewtests liefen auf dem sauberen Commit `b296d66`:

1. **Projektionsgrenze teilweise aufgeloest:** Der sichtbare
   `(x_-,m_-)`-Delayzustand ist in 9/9 retardiert reziproken Fortsetzungen
   praediktiv geschlossen und spektral konditioniert
   (`kappa=46.8..81.0`), ohne tiefenstabiles Segmentmatching. Das stuetzt
   den sichtbaren Delay-Nullbefund.
2. **Augmentierter Zustand weiter offen:** Feld plus Impuls verbessern den
   Holdout nur um `-1.94%..+0.20%`, waehrend die Delaymatrix
   `kappa=1.55e16..1.93e16` erreicht. Die 33/36 komplex passenden Segmente
   sind damit nicht identifizierbar und kein Gegenbeweis zum Nullbefund.
3. **Relative Noise getestet:** Die Knotenmarginalen bleiben fest, die
   relative RMS-Leiter stimmt numerisch. Sinkende relative Diffusion bindet
   staerker, erzeugt aber keinen kontrollgetrennten Modus.
4. **Ambientfit negativ:** Er ist komplex in 9/9 reziproken, aber bereits 6/9
   Kanal-aus-Pfaden und deshalb nicht kontrollgetrennt.

## Naechste zwei Tests

1. **Langhorizont abgeschlossen; Pole-Prescreen:** Alle 45 festen
   Seed-/Rausch-/Rangdeltas verschlechtern sich bis 12500 Updates, effektiver
   Rang waechst ohne Plateau und Rang 16/32 trennt sich nicht vom Einwegarm.
   Vor einem neuen Lauf duerfen nur die bereits gespeicherten DMD-Pole auf
   Rang-/Tiefen-/Kontrollidentitaet geprueft werden. Kein Ueberlebender beendet
   P3.2; nur ein Ueberlebender oeffnet einen vorregistrierten Segmentlauf.
2. **Quelllokale Regel erst danach:** Emission und Readout ohne
   zielabhaengigen momentanen Cross-Gradienten formulieren und das reduzierte
   lineare Spektrum vor einer Vollsimulation bestimmen.

Eine Lambda-Kampagne bleibt gesperrt. Fuer jedes Lambda waeren neue kompatible
Formationszustaende, ein fester Tailfehler sowie eine vorab deklarierte
Invariante fuer `D=epsilon^2/(2 lambda)` oder den diskreten Rauschschritt
noetig; beides kann nicht gleichzeitig konstant genannt werden.
