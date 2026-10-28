# Einmalige gekoppelte AL1-Referenz: Ausfuehrungsvorschlag

Stand: 2026-10-28. **Status: author-approved, not yet started.** Der Autor
hat beide begrenzten Referenzlaeufe ausdruecklich genehmigt. Freigabe,
Quellstand und anschliessender Verlauf stehen im
[Versuchsprotokoll](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/nucleon_al1_attempt1_2026-10-28.md).
Kriterien und Budget bleiben unveraendert. Keine FIFO-/P5-Freigabe wird
wiederverwendet.

## Frage und Nichtziele

Kann der eingefrorene, gekoppelte Dreiquark-Referenzoperator innerhalb
des festen endlichen Basisbudgets numerisch konsistente Energie,
Groessen- und magnetische Spin-Erwartungswerte liefern? Wie unterscheiden
sich $S=I=1/2$ und $S=I=3/2$ unter derselben Rechnung?

Die gewaehlten Quantenzahlen, Quarkmassen, Ladungen, Confinement und
Quantentheorie sind Inputs. Weder Elementarteilchen-Emergenz noch QCD-
Genauigkeit, Wasserstoffspektrum oder dynamisch erzeugte Spinquantisierung
werden getestet. Das ist kein Ersatz fuer den Memory-Anschluss.

## Eingefrorene Definition

Operator, Vorzeichen, Einheiten und Energieoffset aus dem
[raeumlichen Referenzvertrag](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/docs/reference/nucleon_spatial_reference.md).
Keine Aenderung der AL1-Literaturparameter, kein Protonmassen-/Radiusfit.
Schwerpunktfreie Jacobi-Koordinaten, Gesamt-$L=0$, exakte gemeinsame
Permutationssymmetrisierung von Raum, Spin und Flavor. Vier innere
Nukleonkanaele; ein Vergleichskanal fuer Delta mit $S_z=I_z=1/2$.

Exponenten sind fuer jedes geordnete Paar $(a,b)$ aus dem jeweiligen
Laengensatz und $c\in\{0,0.4\}$ festgelegt:

$$
A(a,b,c)=\begin{pmatrix}a^{-2}&c/(ab)\\c/(ab)&b^{-2}\end{pmatrix}.
$$

| Stufe | Laengensatz in GeV^-1 | Gaussfunktionen | Rohe Dimension N / Delta |
| --- | --- | --- | --- |
| 0 | 0.5, 2, 8 | 18 | 72 / 18 |
| 1 | 0.5, 2, 8, 1, 4 | 50 | 200 / 50 |
| 2 | 0.5, 2, 8, 1, 4, 0.25, 16 | 98 | 392 / 98 |

Dies sind verschachtelte Funktionsmengen, keine Anpassung an gemessene
Teilchengroessen. Lineare Abhaengigkeiten werden pro Stufe sichtbar
entfernt; feste relative Metrikcutoffs $10^{-10}$ und $10^{-12}$.
Keine Zufallsseeds, nachtraegliche Breitenwahl oder automatische
Basisvergroesserung. Die Schwellen unten sind prospektive technische
Kriterien, keine aus QCD hergeleiteten Fehlerschranken.

## Ausfuehrungsgrenzen

- Ein Durchlauf je Sektor, zuerst Nukleon, danach Delta; insgesamt
  hoechstens zwei Prozesse, jeder mit **300 s harter Laufzeitgrenze**.
- Ein CPU/BLAS-Thread, keine GPU und kein Cloud-Job. Der Runner hat
  zusaetzliche interne Deadlines; der Elternprozess muss die harte Grenze
  auch waehrend einer LAPACK-Routine durchsetzen. Dazu dient der
  [Windows-Supervisor](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/experiments/current/reference/run_nucleon_al1_bounded.ps1),
  der Prozess und getrennte Ausgabelogs besitzt. Seine einmalige
  AL1-Ausfuehrung je Sektor ist nun genehmigt. Der Solver startet selbst
  keine Kindprozesse.
- Nur die drei genannten Stufen und zwei Cutoffs pro Stufe. Keine
  Wiederholung eines Zielprozesses, auch nicht nach technischem Fehler.
- Bei technischem Fehler oder Zeitlimit: Panel stoppen, vorhandene
  Dateien sichern, `inconclusive`. Keine Umdeutung leerer/partieller
  Dateien als Ergebnis. Keine automatische Wiederaufnahme.
- Vor Start exakten Runner-/Basis-/Parameter-Commit und Freigabe
  dokumentieren; Ausgabe in neue Dateien. Vorhandene Ausgaben werden
  vor jeder Berechnung mit exklusiver Dateioeffnung geschuetzt.

## Endliche Konsistenzkriterien

| Kriterium | Vorab festgelegte Grenze |
| --- | --- |
| Energie letzte zwei Stufen | Absoluter Unterschied <= 0.001 GeV |
| Variationsmonotonie | Keine Erhoehung > 0.00001 GeV |
| Energieempfindlichkeit auf Metrikcutoff | <= 0.00005 GeV je Stufe |
| Letzte Aenderung der drei Radiusquadrate | Je <= 0.05 GeV^-2 |
| Letzte Aenderung der u/d-Spin-Gewichte | Je <= 0.002 |
| Cutoffempfindlichkeit der Radien / Spin-Gewichte | Je <= 0.005 GeV^-2 / 0.0002 |
| Metriknorm und Ladungsnormierung | Absolute Abweichung < 1e-8 |
| Relatives endliches Matrixresiduum | < 1e-8 |

Ein Pass heisst ausschliesslich `finite-basis-consistency-pass`. Die
endliche Basis liefert dadurch kein Kontinuumszertifikat. Energieplateaus
allein genuegen nicht. Bei numerisch vollstaendiger Rechnung mit
verfehlten Kriterien bleibt der Sektor `inconclusive`; der zweite
vorab genehmigte Sektor darf trotzdem ohne Erweiterung ausgewertet werden.
Eine energetische Reihenfolge wird nur mit ausreichendem Abstand zu
beiden beobachteten numerischen Empfindlichkeiten berichtet, nicht als
allgemeiner Spinselektionsbeweis.

## Archiv und physikalische Grenzen

Alle Stufen und beide Cutoffs behalten, nicht nur das beste Ergebnis.
Exponenten, Zustandskoeffizienten, Metrikspektren/Raenge, Norm, Residuum,
Hamiltonparameter, Versions-/Skripthashes und Laufzeiten archivieren.
Observablen: Energie einschliesslich Offset, kinetische Energie,
mittleres Quarkradiusquadrat, proton-/neutronartige Ladungsradiusquadrate,
u/d-Spin-Gewichte und Ladungsnormierungen. Magnetische Momente folgen
im deklarierten additiven Impulsansatz aus denselben Spin-Gewichten;
keine getrennte magnetische Kalibrierung.

Die Kennzahl $2\langle T\rangle/(3m)$ wird als mittlerer
nichtrelativistischer $v^2$-Proxy berichtet. Ein grosser Wert ist ein
Warnsignal fuer die Naeherung, kein numerischer Solverfehler. Auch ein
technischer Pass ist daher kein physikalischer Praezisionsnachweis.
Weder offene hadronische Zerfallskanaele noch Seequarks, Gluonfelder,
relativistische Stroeme oder atomare Zweiphotonkorrekturen sind enthalten.

## Vor Start bereits geprueft

27 synthetische Solver-/Runner-Tests; exakter 6D-Oszillator in beiden
Spinsektoren; unabhaengige Quadratur und 36-Term-Projektionsvergleich;
vollstaendiger Zustandsexport mit Rekonstruktionstest. Der 18-Gauss-
Preflight liefert im Nukleonsektor Rang 51 aus 72 Rohfunktionen und die
exakten synthetischen Energien/Radien an beiden Cutoffs. Das ist eine
Methodenpruefung, kein bereits ausgefuehrter AL1-Versuch.
