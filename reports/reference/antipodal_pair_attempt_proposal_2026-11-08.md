# Vorschlag: genau ein antipodaler Paar-Existenztest

Stand: 2026-11-08. **Vorschlag, nicht freigegeben und nicht ausgefuehrt.**
Die frueheren FIFO-/AL1-Freigaben sind nicht anwendbar. Dieser konkrete
Vorschlag verbindet die noch offene Kopplungsentscheidung mit einem
begrenzten ersten Test; seine Implementierung nimmt die Entscheidung
nicht vorweg.

## Fragestellung und Modellentscheidung

Traegt die vorhandene synchrone additive Paarregel bei gleichen
Selbst-/Kreuz-Gains einen antipodalen rotierenden Zustand nahe dem
festgelegten Startwert, dessen Existenz mit einer festen Box zertifiziert
werden kann? Wenn ja: widerlegt bereits der gemeinsame Normalblock
seine lineare Stabilitaet im freien dreidimensionalen Raum?

Dies ist eine vorbereitete gemeinsame Bahn mit gleichem Mittelpunkt,
nicht ein Wasserstoffmodell oder zwei raeumlich getrennte Teilchen.
Es gibt kein von aussen vorgeschriebenes Feld, aber weiterhin die
klassische FIFO-Regel mit ihren vorgegebenen Kernel- und Speicherparametern.
Aus ihrem Ergebnis folgt keine Quantisierung.

**Vorgeschlagene Normierung:** Selbstgain $\eta=0.15$, Kreuzgain
$\chi=0.15$, also gleiche Lesestaerke fuer beide Memory-Quellen.
Das entspricht der direkten gleich gewichteten Summe ihrer Potentiale.
Die Zeilensumme ist damit **0.30**, nicht 0.15. Dieser Zusatz ist eine
zu genehmigende Modellannahme, kein aus QFT oder Ladung abgeleiteter Wert.
Er entspricht der vorhandenen additiven Regel; keine gemeinsame
Budgetnormierung wird heimlich eingefuehrt.

Die Einzelreferenz bei Gain 0.30 wird in diesem ersten Test **nicht**
gerechnet. Erst ein spaeterer belastbarer Stabilitaetsbefund wuerde
einen entsprechenden Gegenvergleich benoetigen, bevor eine spezifisch
kollektive Ursache behauptet werden darf. Deckungsgleiche Historien und
antipodale Historien sind dabei nicht dieselbe Dynamik.

## Festes Panel

| Groesse | Vorgeschlagener Wert |
| --- | --- |
| Geometrie | $x_{B,n}=-x_{A,n}$, gemeinsame Kreisebene, freie normale Stoerungen |
| Historie | $H=1200$, Alter $0,\ldots,1199$, nativer unnormierter FIFO |
| Gewichte | $w_l=0.01(0.99)^l$, $M_0=1$ |
| Selbst-/Kreuzkernel | identischer Double-Gauss-Kernel; $\sigma_r=1$, $\sigma_a=3$, $A_r=1$, $A_a=3.5$; Delta-Deposition |
| Gains | $\eta=\chi=0.15$ |
| Rauschen | null |
| Newton-Start | $r=0.946517504804225$, $\theta=0.015770381717135$ |
| Unbekannte | nur $r,\theta$; keine Modellparameteranpassung |
| Praezision | genau 80 Dezimalstellen |
| Newton-Budget | hoechstens 12 Schritte, keine Daempfung oder Neustarts |
| Zertifikatsbox | je Halbbreite $10^{-30}$ um das Newton-Ergebnis; genau ein Versuch |
| Prozessbudget | ein numerischer Worker, ein Rechenthread, 300-s-Watchdog |
| Nachfolgearbeit im selben Lauf | keine: weder Trajektorien noch volle Spektren, zweite Praezision oder Einzelvergleich |

Die alten Dezimalwerte dienen ausschliesslich als Startwert. Sie sind
**kein Paar-Existenznachweis**, keine Intervallbox und keine Fortsetzung
eines verfolgten Loesungszweiges. Das vorab gewaehlte lokale Verfahren
kann eine anderswo existierende Bahn verfehlen.

Die Quelle ist fest an Commit
`c297f0d8c7f1e118060b7ea845fbb6fa52dcf560`, Pfad
`reports/dynamics/rotation/scalar_memory_rotating_wave_initial_state_spec_2026-08-20.json`
und Git-Blob `09ce359e085b8bb73d002e8c6e61f21717445e88` gebunden.
Der Runner vergleicht die gespeicherten Parameter und Dezimal-Startwerte
ohne neue Ankerrechnung; die Laufquittung speichert zusaetzlich SHA-256.

## Ergebnisse und Abbruch

Der [Methodenbericht](antipodal_pair_method_2026-11-08.md) definiert die
exakten Balancegleichungen, Krawczyk-Gates und den Satz $S_+<0$.
Der vorgeschlagene Lauf darf nur diese drei physikalischen Einordnungen
liefern:

- **Orbit unentschieden:** Newton-Abbruch, nicht bestandene Box,
  Zeitlimit oder technischer Fehler. Kein Nichtexistenz- oder Instabilitaetsbeweis.
- **Orbit zertifiziert, normal instabil:** Existenzgates bestanden
  und gemeinsames Steigungsintervall strikt negativ. Dieser Kandidat
  scheidet als linear stabiler freier 3D-Knoten aus.
- **Orbit zertifiziert, Stabilitaet offen:** Existenzgates bestanden,
  aber der hinreichende Instabilitaetstest entscheidet nicht. Keine
  positive Stabilitaetsklassifikation; volle normale/ebene Bloecke
  einschliesslich Symmetrie- und Jordanpruefung bleiben offen.

Weder Kernel, Gain, Historienlaenge, Startwert, Boxgroesse, Praezision
noch Iterationsbudget duerfen im Anschluss automatisch geaendert werden.
Ein Scheitern rechtfertigt insbesondere keine bestaetigende Suche.

## Ausfuehrungssicherung

Der [Einmal-Runner](../../experiments/current/dynamics/rotation/antipodal_pair_attempt.py)
hat keine Standard-Zielausfuehrung: Import, Hilfe und `--describe`
werten keine Zielkoeffizienten aus. Der Zielpfad verlangt eine konkrete
Autorenfreigabe, deren ausdrueckliche Bestaetigung durch den Operator,
eine Freigabenotiz und den vollen erwarteten Code-Commit. Ein CLI-Flag
ist fuer sich kein Beleg menschlicher Zustimmung.

Vor Ausfuehrung werden ein sauberer Worktree, unveraenderter HEAD,
Python 3.12, mpmath 1.3.0, numerische Modulpfade aus genau diesem
Worktree und die gepinnte Eingabequelle geprueft. Der Worker prueft
seine Modulherkunft, Versionen und Ein-Thread-Umgebung erneut.
Die Rechnung nutzt mpmath ohne BLAS, eigene Threads oder Kindprozesse.

Das atomare Erzeugen des festen Verzeichnisses
`reports/dynamics/rotation/antipodal_pair_attempt_1` verbraucht den Versuch.
Auch Fehler, Unterbrechung oder fehlende Schlussdatei erlauben kein
automatisches Resume. Dateien werden ausschliesslich neu angelegt,
nicht ueberschrieben. Quittung, Panel mit stdout/stderr und Zusammenfassung
halten Parameter, Code-/Quellenidentitaet, Abbruch und Ergebnis fest.
Das Verzeichnis darf nicht fuer einen erneuten Versuch geloescht werden.

Der Elternprozess ueberwacht die Frist, beendet den direkten Worker
bei Ueberschreitung und wartet dessen Ende ab. Prozessstartzeit wird
vom verbleibenden Kommunikationsbudget abgezogen. OS-Prozesserzeugung
und Beendigungsaufwand sind kein Echtzeitversprechen auf exakt 300.000 s
Gesamtdauer. Das folgt dem dokumentierten `Popen.communicate`-/`kill`-
Muster der [Python-3.12-Dokumentation](https://docs.python.org/3.12/library/subprocess.html#subprocess.Popen.communicate).
Keine Shell-Interpolation, kein sichtbares Windows-Fenster, kein
automatischer Ersatzprozess.

Vor Annahme einer Worker-Ausgabe werden Parameter, Startwert,
Iterationsbudget/-spur, Praezision, Box, Zertifikatsgates, binaeres
Steigungsvorzeichen, Klassifikation und Runtime geprueft. Das ist eine
Konsistenzpruefung der gespeicherten Ausgabe, keine unabhaengige zweite
Intervallrechnung oder Schutzbehauptung gegen boesartig manipulierten Code.

## Vorabtests und Status

40 neue [Runner-Kontrollen](../../tests/test_antipodal_pair_runner.py)
bestehen. Sie enthalten einen echten kleinen H=2-Worker, einen nach
einem 0.15-s-Watchdog beendeten kuenstlichen Schlafprozess mit geprueftem terminalem
Handle, veraenderte Ausgaben, Freigabe-/Commit-/Importguards,
Ueberschreibschutz und verbrauchte Versuche nach Fehler/Unterbrechung.
Der H1200-Datensatz wird dabei nur aus Git gelesen, nicht gerechnet.
Im abschliessenden betroffenen Regressionspanel bestehen **245 Tests
in 9.72 s**, einschliesslich des bisherigen Einmal-Runners. Ruff fuer
Quellcode, Tests und aktuelle Experimente sowie der strenge MkDocs-Build
bestehen. Keine vollstaendige Repository-Testsuite. Das feste
Zielverzeichnis existiert nach diesen Tests nicht; kein Versuch verbraucht.

**Die konkrete Autorenentscheidung steht aus.** Bei anderer gewuenschter
Normierung wird der Vorschlag vor Ausfuehrung sichtbar geaendert und
erneut geprueft, nicht im Lauf angepasst. Der volle Ausfuehrungs-Commit
wird erst nach Festschreibung des geprueften Vorschlags verwendet.
Die [Projektprioritaeten](../../docs/status/project_priorities.md) bleiben
die einzige aktive Aufgabenreihenfolge. Paper I und die streng getrennte
QCD-/QFT-Referenz werden durch diesen Vorschlag nicht geaendert.
