# Review: skalarer Center-Inertial-Port

Date: 2026-08-16.

Status: kritisches Ergebnisreview des prospektiv registrierten
Center-Force-/Work-Gates. Alle nachfolgend als post hoc bezeichneten
Diagnosen veraendern keine Gateentscheidung.

Ein nachgelagerter [Referee-Audit](scalar_memory_center_mass_referee_audit_2026-08-16.md)
trennt die passive Inertialdarstellung noch schaerfer von einem physischen
Masseclaim. Insbesondere sind die Einheitsmasse, die Phase-/COM-Semantik und
die physische Konjugation von \(f\,dc\) nicht aus dem Gate hergeleitet.

## Kurzurteil

Der neue Input/Output-Port entscheidet die registrierten Alternativen
eindeutig:

| Gate | Ergebnis |
|---|:---:|
| G0 Port- und Experimentvaliditaet | pass |
| G1 Center-Antwort, Arbeit und Referenz-Closure | pass |
| G2I positive effektive Center-Traegheit | pass |
| G2O konkurrierende overdamped Center-Position | fail |

Unter dem mathematischen Port \((f,\dot c)\) ist der normalisierte
Memory-Center ein positiver effektiver Traegheitskandidat. Der relative
Zustand \(r=x-c\) ist seine Geschwindigkeit, der dimensionslose
Massenschaetzer konvergiert gegen eins, und die positive Speicherbilanz
schliesst.

Das ist noch kein Nachweis physikalischer Masse. Die Center-Gleichung und
\(m=1\) folgen strukturell aus Zustandswahl und Kraftnormierung. Numerisch
getestet wurde, ob der vollstaendige nichtlineare Finite-H-Simulator diese
lokale Struktur tatsaechlich realisiert.

## Kein Vorzeichenfehler, sondern zwei Ausgaenge

Im lokalen Kontinuumsgrenzwert gilt

\[
\dot c=r,\qquad
\dot r=-\Gamma r+f+\sqrt{2D}\,\xi,\qquad
\Gamma=1+\chi=5.
\]

Damit folgt

\[
\ddot c+5\dot c=f+\sqrt{2D}\,\xi
\]

und

\[
{\dot C(s)\over F(s)}={1\over s+5}.
\]

Unter der registrierten dimensionslosen Inputnormierung sind daher

\[
m=1,\qquad \gamma=5.
\]

Der zuvor getestete sichtbare Ausgang bleibt dagegen

\[
x=c+r=c+\dot c
\]

mit

\[
{\dot X(s)\over F(s)}={s+1\over s+5}.
\]

Das letzte negative sichtbare-Port-Ergebnis wird somit nicht umklassifiziert.
Es gilt fuer \(x\) und \(f\,dx\); das positive Ergebnis gilt fuer \(c\) und
\(f\,dc\).

Post hoc laesst sich die Readout-Abhaengigkeit noch schaerfer schreiben. Fuer
die affine Familie

\[
y_a=c+a r
\]

ist

\[
{\dot Y_a(s)\over F(s)}={1+a s\over s+5}.
\]

Innerhalb dieser Familie ist \(a=0\), also der reine Center, der einzige
Readout ohne Hochfrequenz-Feedthrough. Diese Eindeutigkeit war kein
registriertes Gate, reduziert aber die Beliebigkeit der Center-Wahl.

## Positive Arbeitsspeicherung

Mit

\[
E={1\over2}|r|^2
\]

gilt deterministisch

\[
\dot E=f\cdot\dot c-5|\dot c|^2.
\]

Der Speicher ist positiv, die Dissipation nichtnegativ und die Portleistung
ist \(f\cdot\dot c\). Damit besitzt der lokale Center-Port eine regulaere
passive inertiale Darstellung.

Fuer einen Rechteckpuls der Breite \(\delta\), Flaeche \(J\) und
\(z=5\delta\) lauten die exakten Kontinuumsvorhersagen

\[
{r(\delta)\over J}={1-e^{-z}\over z},
\]

\[
{\Delta c(\delta)\over J}
=\delta\,{z-1+e^{-z}\over z^2},
\]

\[
{W_c\over J^2}={z-1+e^{-z}\over z^2}.
\]

Erst nach \(\alpha\to0\) gilt fuer \(\delta\to0\)

\[
r/J\to1,\qquad
\Delta c/J\to0,\qquad
W_c/J^2\to1/2.
\]

Die Verwendung aufgeloester Pulse statt eines singulaeren nativen
Ein-Schritt-Impulses war daher notwendig, um eine reine
Endpunktkonventionsentscheidung zu vermeiden.

## Prospektive Ergebnisse

Protokoll, Schwellen, Alpha-Familie, Rechteckpulse, Breitenleiter,
Formation-Seeds 16--20 und MSD-Seed 20260817 wurden vor Implementierung und
vor Erzeugung der prospektiven Antworten festgeschrieben. Der Lauf erfolgte
auf dem sauberen, zuvor gepushten Freeze f2bfa4b.

### Feste Pulsbreite \(\delta=0.2\)

| alpha | inferred \(m\) | inferred \(\gamma\) | \(W_c/J^2\) | Ledgerrest/Arbeit |
|---:|---:|---:|---:|---:|
| 0.0400 | 0.937218 | 5.041794 | 0.465924 | 0.172160 |
| 0.0200 | 0.969335 | 5.020534 | 0.415595 | 0.097006 |
| 0.0100 | 0.984836 | 5.010226 | 0.391424 | 0.051607 |
| 0.0050 | 0.992459 | 5.005149 | 0.379575 | 0.026644 |
| 0.0025 | 0.996239 | 5.002630 | 0.373708 | 0.013551 |

Am Holdout liegt der Center-Kontinuumsfehler bei 0.003904, der
Relativ-/Geschwindigkeitsfehler bei 0.002297 und der Arbeitsfehler zur
Kontinuumsreferenz bei 0.015845. Die Antworten des nichtlinearen Simulators
liegen nur etwa \(2.0\times10^{-5}\) von der exakten linearen
Finite-H-Referenz entfernt.

### Holdout-Pulsbreitenleiter

| \(\delta\) | \(\Delta c/J\) | erste force-off Geschwindigkeit/J | beob. \(W_c/J^2\) | Kontinuum \(W_c/J^2\) |
|---:|---:|---:|---:|---:|
| 0.40 | 0.114556 | 0.428362 | 0.286389 | 0.283834 |
| 0.20 | 0.074742 | 0.627038 | 0.373708 | 0.367879 |
| 0.10 | 0.043839 | 0.781245 | 0.438392 | 0.426123 |
| 0.05 | 0.024288 | 0.878808 | 0.485756 | 0.460813 |

Center-Verschiebung nimmt mit engerem Puls strikt ab; persistente
Geschwindigkeit und endliche Arbeit nehmen in Richtung ihrer
Impulsgrenzwerte zu. Der Massenschaetzer bleibt ueber die Leiter bei
0.996237--0.996239 und der Daempfungsschaetzer bei 5.002616--5.002630.

### Stationaere Center-MSD

Die registrierte Kurzzeitsteigung ist

\[
1.972302
\]

gegen 1.970784 fuer die exakte diskrete Kovarianz und 1.971683 fuer den
Kontinuumsprozess. Der Monte-Carlo-Fehler zur exakten diskreten Referenz
betraegt 0.003347. Das selektiert die ballistische \(t^2\)- und verwirft die
diffusive \(t\)-Signatur im festen lokalen Fenster.

## Validitaetskontrollen

- Force-off-Klonrest: exakt null.
- Maximaler Finite-H-Rekurrenzrest: \(2.60\,10^{-16}\).
- Raw-paired- gegen Odd-Response-Arbeitsidentitaet:
  maximal \(1.40\,10^{-13}\).
- Mirror-even-Leakage: maximal \(4.28\,10^{-8}\).
- Staerkenabhaengigkeit: maximal \(6.59\,10^{-11}\).
- Groesster lokaler Radius: \(R/\sigma_{\rm rep}=0.009444\).
- Simultane Forced/Control-Radiusspanne: 0.998762--1.001241.

Die Antwort bleibt damit im registrierten lokalen und perturbativen Bereich.
Die fuenf Seeds pruefen verschiedene nichtlineare Formationshintergruende;
Odd-Mirroring und Common Noise reduzieren die stochastische Antwortvarianz
absichtlich.

## Was strukturell und was numerisch ist

### Strukturell

- Die zweite Ordnung von \(c\), der Transfer \(1/(s+5)\) und der positive
  Speicher \(r^2/2\) folgen algebraisch aus dem augmentierten lokalen Zustand.
- \(m=1\) folgt aus der festgelegten Kraftnormierung. Es ist kein spontan
  selektierter Zahlenwert.
- Die ballistische Center-MSD folgt daraus, dass \(c\) ein Integral des
  stationaeren OU-artigen Zustands \(r\) ist.
- Der sichtbare \(x\)-Readout behaelt seinen direkten Feedthrough und seine
  diffusive Kurzzeit-MSD.

### Numerisch

- Der nichtlineare Finite-H-Pfad reproduziert die strukturelle
  Center-/Geschwindigkeitsantwort im kleinen lokalen Radiusfenster.
- Die separate Arbeit \(f\,dc\) stimmt zwischen rohen gespiegelten Zweigen
  und Odd-Response bis zur Rundungsgrenze ueberein.
- Arbeits- und Speicherledger konvergieren mit Alpha.
- Pulsbreiten- und MSD-Holdouts unterscheiden die registrierten
  Center-Alternativen ohne Response-Renormierung.

Die Simulation validiert somit die nichtlineare Einbettung. Sie entdeckt
nicht nachtraeglich die bereits analytisch vorhandene Center-Gleichung.

## Kritische Grenzen

1. **Port- und Observable-Wahl.** Der Center ist ein normalisierter,
   history-abhaengiger Readout. Dass \(f\,dc\) ein passiver mathematischer Port
   ist, beweist noch nicht, dass eine mikroskopische externe Kraft physisch an
   \(c\) statt an \(x\) koppelt.
2. **Massennormierung.** Eine Reskalierung von Centerkoordinate und
   konjugierter Kraft aendert die numerische Masseneinheit. Ohne SI- oder
   anderweitig unabhaengige Einheiten ist \(m=1\) eine interne Normierung.
3. **Arbeits-Doppelgrenze.** Die Breitenleiter laeuft bei festem
   \(\alpha=0.0025\). Beim kleinsten Puls liegt der diskrete Arbeitswert
   5.4 Prozent ueber der Kontinuumsreferenz, weil nur 20 native Schritte den
   Puls aufloesen. Der Wert 0.485756 ist daher kein eigenstaendiger
   Praezisionsnachweis des Grenzwerts 1/2.
4. **Lokaler Slice.** Die Impulse betragen nur 0.5 und 1 Prozent des
   Kontinuumsradius. Groessere Auslenkungen, Kernskalen und nichtlineare
   Langzeitdynamik wurden nicht getestet.
5. **Freie statt gebundene Masse.** Der Center ist eine freie integrierte
   Relaxationsmode und diffundiert langfristig. Der Test zeigt weder ein
   stabiles Teilchen noch eine gebundene Trajektorie.
6. **Statistische Rolle der Seeds.** Common Noise und Mirroring dienen der
   kausalen Antwortisolierung. Fuenf Formation-Seeds sind keine
   populationsweite Unsicherheitsquantifizierung.
7. **Keine universelle Emergenz.** Der Center ist aus dem Memory bereits als
   augmentierter Zustand vorhanden. Ob seine inertiale Darstellung
   physikalisch privilegiert ist, bleibt eine separate Hypothese.

## Wissenschaftlich zulaessige Lesart

### Evidenz

Der normalisierte skalare Memory-Center besitzt unter dem prospektiv
definierten Port \((f,\dot c)\) eine positive, passive und numerisch
geschlossene Inertialdarstellung im lokalen Kontinuumsgrenzwert.

### Inferenz

Das bestehende skalare Memory enthaelt eine inertial realisierbare
coarse-grained Koordinate, ohne dass ein separater Momentumzustand eingefuehrt
wurde. Positive Speicherbilanz und Null-Feedthrough machen diese Aussage
staerker als eine beliebige formale zweite Differenz; die Gleichung bleibt
jedoch eine Zustandselimination und kein physikalischer Masseclaim.

### Nicht gezeigt

Es ist nicht gezeigt, dass \(c\) die beobachtbare physische Knotenposition
ist, dass reale Arbeit durch \(f\,dc\) und nicht \(f\,dx\) gegeben ist, dass
die Masseneinheit modellintern selektiert wird oder dass der Befund ausserhalb
der lokalen Taylor- und Pulsfamilie transferiert.

## Naechster diskriminierender Schritt

Ein weiterer Alpha-Punkt allein waere wenig informativ. Der naechste Test
sollte die Center-Lesart statt nur ihre bekannte Rechteckantwort angreifen:

1. \(m=1\) und \(\gamma=5\) ohne Refit einfrieren;
2. neue Seeds und ungesehene glatte, dreieckige sowie sinusoidale
   Kraftprofile verwenden;
3. Center-, sichtbare und affine \(c+a r\)-Readouts gleichzeitig auswerten;
4. positive Speicherbilanz und Null-Feedthrough fuer den Center verlangen;
5. danach erst Impulsstaerke und lokalen Radius deutlich vergroessern.

Besteht nur der Center ohne Profilfit, waere die effektive Inertiallesart
transferiert. Scheitert sie, bleibt das aktuelle Ergebnis eine exakte, aber
protokollspezifische Zustandsdarstellung.

## Referenzen

- [Center-Port-Praeregistrierung](../preregistration/scalar_memory_center_inertial_port_protocol_2026-08-16.md)
- [Center-Port-Ergebnis](../../../dynamics/limits/scalar_memory_center_inertial_port_gate_2026-08-16.md)
- [Vorheriges sichtbares Force-/Work-Review](scalar_memory_force_work_port_review_2026-08-16.md)
