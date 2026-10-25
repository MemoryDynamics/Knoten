# FIFO: gezielte 120-Grad-Symmetriekontrolle

2026-10-25. Status vor Ausfuehrung: vom Autor ausdruecklich angefordert,
noch nicht gerechnet. Separater Zusatz zum abgeschlossenen Ankertest;
keine Wiederholung des Normalzertifikats und keine Parametersuche.

## Vorhersage und Grenze

Fuer die schon definierten planar/normalen Formmuster P,N sei
`D(beta) = cos(beta)*P + sin(beta)*N`. Der Winkel ist jetzt ein
orientierter Mischwinkel in dieser Musterbasis; der geometrische
Hauptwinkel zur planaren Untermenge ist bei 120 Grad ebenfalls 60 Grad.
Die Reflexion S an der Kreisebene laesst P und die Ausgangshistorie Y
fest und kehrt N um. Deshalb gilt exakt

`D(120) = -S D(60)` und `Y + s*delta*D(120) = S(Y - s*delta*D(60))`.

Der vorhandene deterministische radiale Kernel samt FIFO-Verschiebung
erfuellt `F(SX)=S F(X)`. Das gilt nicht nur fuer die Linearisierung.
Auch die verwendete Formdistanz ist unter gemeinsamer Spiegelung
invariant: Die Menge der eigentlichen Rotationen bleibt unter
Konjugation `Q -> S Q S` erhalten. Die ungestoerte Referenz bleibt planar.
Daher ist die Vorhersage fuer jeden Zeitpunkt in exakter Arithmetik:

- 120 Grad, Vorzeichen +: dieselbe Formdistanz wie 60 Grad, Vorzeichen -.
- 120 Grad, Vorzeichen -: dieselbe Formdistanz wie 60 Grad, Vorzeichen +.

Gleiches Gesamtvorzeichen ist nicht die exakte Paarung. Die alten
60-Grad-Endfaktoren unterscheiden sich geringfuegig zwischen den Vorzeichen.
Ein passender neuer Lauf waere eine Implementierungs-/Symmetriekontrolle,
keine unabhaengige Replikation oder Bestaetigung der Physik des Modells.
Die Exploration bleibt auf den vorbereiteten Kreis und dieses Muster
begrenzt; allgemeine Stabilitaet folgt nicht aus dem Test.

## Fester Umfang

- Derselbe urspruengliche H=1200-Anker, gleiche exakten Inputstrings,
  gleiche float64-Konvertierung, NumPy-Version, Kernel und Musterprojektion.
- Nur die zwei neuen 120-Grad-Arme mit Gesamtvorzeichen -/+ und eine
  ungestoerte Referenz; RMS-Amplitude `1e-5*R`, 2000 Updates, Abtastung
  alle zehn Updates einschliesslich Anfang und Ende, kein Rauschen.
- Vergleich mit den unveraenderten gespeicherten 60-Grad-Armen aus
  `fdbd24fd437187a4db185d413f4c3bd022104b3b`,
  `reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25/panel_80.json`.
  Lesen aus dem gepinnten Git-Objekt; Herkunftshash im Ausfuehrungsbeleg.
- Uebereinstimmung fuer alle 201 Formdistanzen je Paar und die Referenz
  bei `abs(new-old) <= 1e-11*R + 1e-8*abs(old)`.
  Toleranzen werden vor Ausfuehrung festgelegt und nicht nachjustiert.
  Berichten: maximale absolute Abweichung, groesster Toleranzanteil,
  beide Endfaktoren. Jede Ueberschreitung ist ein zu untersuchender
  Symmetrie-/Implementierungsbefund, kein neuer physikalischer Effekt.
- Genau ein subprocess-begrenzter Versuch, maximal 60 Sekunden inklusive
  Workerstart; bei Abbruch technisches Nicht-Ergebnis, kein automatischer
  Neuversuch. Exklusives Ausgabeverzeichnis
  `reports/dynamics/rotation/fifo_oblique_120_control_2026-10-25`.
- Vorher Code und kleine Nicht-Ziel-Kontrollen pruefen, Revision committen
  und pushen. Der Standardwinkelumfang des alten Runners bleibt unveraendert.

Die angeforderte Kontrolle wird zunaechst abgeschlossen. Die danach
offene Aufgabe bleibt die Unterscheidung zwischen echter wachsender
Normalmode und transienter Verstaerkung; dieser Zusatz ist kein neuer
asymptotischer Zertifikatsversuch.

Vor Ausfuehrung: 249 betroffene lokale Tests bestanden, darunter die
voll nichtlineare Reflexionskovarianz, die Vorzeichenpaarung, der Vergleich
ganzer kleiner Kontrolltrajektorien und ein echter Workerabbruch ohne
Zielinput. Lint und strikter Dokumentationsbau bestehen ebenfalls.
