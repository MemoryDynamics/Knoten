# Referee-Audit: erzeugt der skalare Memory-Center Masse?

Date: 2026-08-16.

Status: post-hoc konzeptioneller Audit nach dem prospektiv ausgefuehrten
Center-Port-Gate. Der Audit aendert dessen registrierte Gateentscheidung nicht,
bewertet aber, welche physikalische Aussage daraus folgen darf.

## Empfehlung: major revision

Das mathematische und numerische Ergebnis ist belastbar, wenn der Claim eng
formuliert wird:

> Im lokalen Taylor-Regime besitzt der normalisierte exponentielle
> Memory-Center unter dem ausdruecklich gewaehlten Port \((f,\dot c)\) eine
> passive freie Inertialdarstellung. Der nichtlineare Finite-\(H\)-Simulator
> reproduziert diese Darstellung fuer die registrierten kleinen Stoerungen.

Nicht belastbar ist derzeit die staerkere Aussage, dass das kanonische Modell
eine physikalische Masse erzeugt oder deren Wert bestimmt. Drei dafuer
notwendige Identifikationen sind noch offen: \(c\) als materieller
Massenschwerpunkt, \(f\,dc\) als physische Arbeit und eine von Einheiten sowie
Portgain unabhaengige Massenskala.

Das Resultat ist ausserdem kein harmonischer Oszillator. Die homogene
Center-Gleichung hat die Pole \(0\) und \(-\Gamma\), keinen Rueckstellterm
\(\omega_0^2c\) und kein komplexes Polpaar. Sie beschreibt eine freie
gedaempfte Kramers-/Langevin-Realisierung, sofern die mechanische
Interpretation des Ports zulaessig ist.

## Claim-Matrix

| Aussage | Status | Begruendung |
|---|---|---|
| \(c\) ist der Schwerpunkt des gespeicherten skalaren Memory-Measures | exakt per Definition | \(c=\int y\rho(y)dy/\int\rho(y)dy\) beziehungsweise gewichteter Mittelpunkt der gespeicherten Pfadpunkte |
| Die lokale untrunkierte Dynamik von \(c\) besitzt eine Gleichung zweiter Ordnung | strukturell bewiesen | folgt durch Eliminieren von \(x-c\) aus zwei Gleichungen erster Ordnung |
| Der Center-Port ist passiv und hat keinen Hochfrequenz-Feedthrough | strukturell bewiesen | Speicher \(E=|x-c|^2/2\), Mobilitaet \(\dot C/F=1/(s+\Gamma)\) |
| Der nichtlineare Finite-\(H\)-Code realisiert diese lokale Reduktion | numerisch gestuetzt | prospektive Seeds 16--20, Alpha-Leiter, Pulsbreitenleiter und MSD-Arm |
| \(c\) ist der Schwerpunkt einer materiell konservierten Knotenmasse | offen | \(\rho\) ist bisher Occupancy-Historie mit lokaler Vernichtung und Neudeposition, keine materielle Kontinuitaetsdichte |
| \(x\) ist eine physische Phase | derzeit nicht definiert | im Variablenvertrag ist \(x\in\mathbb R^d\) sichtbare Position/Zustandsrepraesentant; Periodizitaet, Wicklung und Phasensymmetrie fehlen |
| \(f\,dc\) ist die von einer externen Kraft verrichtete physische Arbeit | offen | der implementierte Input wird additiv in den \(x\)-Update geschrieben; die Konjugation an \(c\) wurde als Testport gewaehlt |
| Eine positive physikalische Masse emergiert | nicht gezeigt | der positive Koeffizient folgt aus Memory-Zeitskala und Inputgain; beide sind im Gate normiert |

## 1. Was der Center im kanonischen Modell ist

Fuer die kontinuierliche untrunkierte Memory-Idealisierung kann das
normierte skalare Feld als

\[
\partial_t\rho(y,t)
=-{1\over\tau}\rho(y,t)
+{M_0\over\tau}G_\sigma(y-x(t))
\]

geschrieben werden. Fuer einen zentrierten Depositionskernel und
\(\int\rho=M_0\) ist

\[
c(t)={1\over M_0}\int y\rho(y,t)\,dy,
\qquad
\tau\dot c=x-c.
\]

Damit ist \(c\) exakt der geometrische Schwerpunkt des aktuell gespeicherten
Memory-Feldes. Seine Bewegung entsteht hier jedoch durch exponentielles
Loeschen alter und Deponieren neuer Feldmasse. Sie ist nicht die Folge eines
lokalen Transportgesetzes
\(\partial_t\rho+\nabla\cdot j=0\) fuer konservierte Materie. Ein geometrischer
Schwerpunkt eines Source-/Sink-Feldes ist daher noch kein mechanischer
Massenschwerpunkt.

Die Normierung entfernt zudem \(M_0\) aus der Center-Gleichung. Das ist fuer
einen Schwerpunkt mathematisch normal, bedeutet aber, dass der bisherige
Center-Port keine Traegheit proportional zur gespeicherten Memory-Masse
testet. In der gematchten Alpha-Familie wird \(\eta\) ausserdem so angepasst,
dass die lokale Rate \(\chi\) trotz gespeicherter Masse fest bleibt.

## 2. Die zweite Ordnung ist eine exakte Zustandselimination

Im idealen untrunkierten diskreten lokalen Modell gelten mit
\(q=1-\alpha\), \(r_n=x_n-c_n\) und lokalem Gain \(g\)

\[
x_{n+1}=x_n-g r_n+\alpha f_n+\varepsilon\xi_n,
\]

\[
c_{n+1}=q c_n+\alpha x_{n+1}.
\]

Setzt man \(a=q(1-g)\) und
\(\Delta c_n=c_{n+1}-c_n\), folgt ohne Fit

\[
\Delta c_n
=a\,\Delta c_{n-1}+\alpha^2 f_n+\alpha\varepsilon\xi_n.
\]

Aequivalent dazu ist

\[
{c_{n+1}-2c_n+c_{n-1}\over\alpha^2}
+\Gamma_\alpha{c_n-c_{n-1}\over\alpha}
=f_n+{\varepsilon\over\alpha}\xi_n,
\]

mit

\[
\Gamma_\alpha={1-a\over\alpha}.
\]

Fuer die registrierte Skalierung \(g=\chi\alpha\) wird

\[
\Gamma_\alpha=1+\chi-\chi\alpha
\longrightarrow 1+\chi.
\]

Der Koeffizient vor der diskreten Beschleunigung ist hier exakt eins, weil
der Center pro Schritt mit \(\alpha\) erneuert und der neue Testinput als
\(\alpha f_n\) eingesetzt wurde. Das ist eine konsistente Normierung, aber
keine numerisch entdeckte Massenselektion.

Der Kontinuumsgrenzwert lautet

\[
\dot c=r,
\qquad
\dot r=-(1+\chi)r+f+\sqrt{2D}\,\xi,
\]

und damit

\[
\ddot c+(1+\chi)\dot c=f+\sqrt{2D}\,\xi.
\]

Die zweite Ordnung fuegt keinen neuen Freiheitsgrad hinzu. Sie schreibt den
bereits augmentierten Zustand \((c,r)\) als \((c,\dot c)\). Genau das darf als
inertiale Realisierung bezeichnet werden; es reicht allein nicht fuer eine
ontologische Aussage ueber Masse.

## 3. Dimensionsbehaftete Form und Identifizierbarkeit

Die Normierungsabhaengigkeit wird sichtbar, wenn Memory-Zeit und Inputgain
nicht auf eins gesetzt werden:

\[
\tau\dot c=x-c,
\qquad
\dot x=-\kappa(x-c)+\mu F+\sigma\xi.
\]

Elimination von \(x\) ergibt

\[
\tau\ddot c+(1+\kappa\tau)\dot c
=\mu F+\sigma\xi,
\]

also nach Division durch \(\mu\)

\[
m_{\rm eff}\ddot c+\gamma_{\rm eff}\dot c
=F+{\sigma\over\mu}\xi,
\]

\[
m_{\rm eff}={\tau\over\mu},
\qquad
\gamma_{\rm eff}={1+\kappa\tau\over\mu}.
\]

Eine positive effektive Masse kann somit als Produkt aus Memory-Zeit und
inverser mikroskopischer Mobilitaet gelesen werden. Das waere eine sinnvolle
coarse-grained Materialgroesse, wenn \(\tau\), \(\mu\), die Zeit- und
Kraftskala unabhaengig physikalisch kalibriert waeren. Im aktuellen Projekt
ist der Updateindex noch keine vorausgesetzte physikalische Zeit, \(f\) ist
ein generalisierter Testinput und \(\tau=\mu=1\) wurde durch die
Kontinuumskonvention gesetzt. Deshalb ist insbesondere \(m=1\) nicht
identifiziert.

Auch eine Reskalierung \(c\mapsto b c\) und des zugeordneten Kraftoutputs
veraendert die numerische Impedanz. Erst ein unabhaengig festgelegtes
Laengen-, Zeit- und Kraftprotokoll entfernt diese Freiheit.

## 4. Warum die passive Bilanz wichtig, aber nicht hinreichend ist

Mit \(E=|r|^2/2\) gilt im deterministischen lokalen Modell

\[
\dot E=f\cdot r-\Gamma|r|^2
=f\cdot\dot c-\Gamma|\dot c|^2.
\]

Damit ist \((f,\dot c)\) ein mathematisch legitimer passiver Port. Das ist
mehr als das beliebige Hinschreiben einer zweiten Differenz: Die Mobilitaet
ist positiv-reell, der Speicher positiv und der Center hat keinen direkten
Hochfrequenz-Feedthrough.

Es bleibt jedoch eine Portfrage. Der implementierte Kontrollterm wird in den
sichtbaren Update von \(x\) eingesetzt. Falls derselbe Input als physische
Kraft an \(x\) interpretiert wird, waere die naheliegende Leistung
\(f\cdot\dot x\). In den normierten Variablen gilt

\[
x=c+r=c+\dot c,
\qquad
f\cdot\dot x=f\cdot\dot c+f\cdot\dot r.
\]

Die Wahl des Ausgangs verschiebt somit einen dynamischen Leistungsanteil.
Eine physische Center-Arbeit benoetigt eine externe Kopplungsenergie oder ein
Virtual-Work-Argument, aus dem gerade \(F\cdot dc\) folgt. Passivitaet zeigt,
dass diese Kopplung moeglich ist; sie zeigt nicht, dass sie im Basismodell
bereits die physische Kopplung ist.

Auch der fruehere Koeffizient \(m=-4\) fuer den sichtbaren \(x\)-Port ist
deshalb keine negative Materie. Er entsteht nur beim niederfrequenten
Abgleich des Feedthrough-Transfers
\((s+1)/(s+5)\) mit einer ungeeigneten globalen Newton-Form. Der Transfer ist
nicht von der Form \(1/(ms+\gamma)\). Antimaterie wuerde diesen
Readout-Unterschied ohnehin nicht erklaeren; sie besitzt keine negative
Traegheitsmasse.

Fuer die affine Readout-Familie \(y_a=c+a r\) gilt zwar

\[
{\dot Y_a(s)\over F(s)}={1+a s\over s+\Gamma},
\]

sodass \(a=0\) als einziger dieser Readouts keinen Feedthrough besitzt. Das
reduziert die Beliebigkeit innerhalb dieser Familie. Das Kriterium war aber
post hoc, und Null-Feedthrough allein identifiziert noch keinen materiellen
Ort. Insbesondere kann die Ausgangsskalierung des Centers weiterhin den
scheinbaren Massenwert aendern.

## 5. Die vorgeschlagene Phase-/Schwerpunkt-Lesart

Die beabsichtigte Semantik

\[
x=\text{schneller Phasen-/Traegerzustand},
\qquad
c=\text{Massenschwerpunkt}
\]

ist eine interessante Modellhypothese, aber noch nicht Bestandteil des
kanonischen Variablenvertrags.

Derzeit ist \(x\in\mathbb R^d\) eine sichtbare Position oder ein
Zustandsrepraesentant. Eine buchstaebliche Phase lebt dagegen auf
\(S^1\), einem Torus oder einer anderweitig identifizierten zyklischen
Mannigfaltigkeit. Dafuer fehlen bisher Periodizitaet, Wicklungszahl,
Branch-cut-invariante Differenzen und ein zirkulaerer statt linearer
Schwerpunkt. Die Fourierfaktoren \(e^{-ikx}\) machen \(x\) nicht selbst zu
einer intrinsischen Phase; sie kodieren die Phase einer raeumlichen
Fouriermode.

Wenn `Phase` nur informell den schnellen momentanen Traegerpunkt meint, ist
die Rechnung konsistent. Dann sollte der Claim vorerst auch genau so lauten.
Wenn eine echte interne Phase gemeint ist, muessen Zustandsraum und
Center-Abbildung zuerst neu definiert werden. Eine Phase und ein raeumlicher
Massenschwerpunkt koennen nicht ohne explizite Abbildung subtrahiert werden.

## 6. Was die Numerik wirklich bestaetigt

Der prospektive Lauf ist als Implementations- und Grenztest stark:

- G0 schliesst Vorzeichen-, Integrations-, Mirroring- und grobe
  Nichtlinearitaetsfehler im registrierten Slice weitgehend aus.
- Die Antworten liegen etwa \(2\times10^{-5}\) von der exakten linearen
  Finite-\(H\)-Referenz entfernt. Damit realisiert der vollstaendige
  nichtlineare Pfad die lokale Reduktion in diesem Radiusfenster.
- Alpha- und Pulsbreitenleiter zeigen die erwartete Annaeherung an die
  konstruierte Kontinuumsantwort.
- Der Arbeitsledger zeigt, dass der gewaehlte Center-Port numerisch dieselbe
  positive Speicherstruktur besitzt wie die analytische Reduktion.

Die elf G2I-Komponenten sind jedoch keine elf unabhaengigen Hinweise auf
Masse. Pulsantwort, force-off-Geschwindigkeit, Arbeit und ballistische
Kurzzeit-MSD folgen alle aus demselben OU-Zustand \(r\) und demselben Transfer
\(1/(s+\Gamma)\). Die exakte Finite-\(H\)-Referenz wird aus derselben
Updatearchitektur abgeleitet. Der Lauf prueft daher Einbettung und numerische
Konsistenz, nicht eine konkurrierende mikroskopische Entstehungserklaerung.

Die Praeregistrierung verhindert nachtraegliches Schwellen- und
Seed-Tuning. Sie beseitigt nicht die strukturelle Nichtidentifizierbarkeit
des Outputs oder der Krafteinheit.

## 7. Nicht vertauschte Grenzwerte

Mindestens vier Approximationen sind getrennt zu halten:

1. \(\alpha\to0\): diskreter zu kontinuierlichem Update;
2. \(C=\alpha H\to\infty\): trunciertes zu untrunkiertem Memory;
3. \(R/\sigma\to0\): nichtlinearer Kernel zur lokalen Taylor-Dynamik;
4. \(\delta\to0\): aufgeloester Kraftpuls zum Impuls.

Im Gate gilt \(C=12\) fest. Daher fuehrt \(H\to\infty\) entlang der
Alpha-Leiter nicht zugleich zum untrunkierten Memory; die physische
Tail-Ausdehnung bleibt konstant. Fuer den kontinuierlichen truncierten Center

\[
c_C(t)={1\over \tau(1-e^{-C/\tau})}
\int_0^C e^{-a/\tau}x(t-a)\,da
\]

gilt vielmehr

\[
\tau\dot c_C
={x(t)-e^{-C/\tau}x(t-C)\over1-e^{-C/\tau}}-c_C.
\]

Bei \(C/\tau=12\) ist der Tailfaktor \(e^{-12}\) klein, aber nicht null.
Die exakte Finite-\(H\)-Referenz behandelt diesen Effekt; eine uniforme lokale
ODE-Aussage benoetigt trotzdem einen separaten \(C\)-Audit oder eine explizite
Fehlerschranke.

Ebenso wurde die Pulsbreitenleiter nur bei der feinsten Alpha und die
Nichtlinearitaet nur bei Impulsen von 0.5 und 1 Prozent des lokalen Radius
geprueft. Die Grenzwerte wurden daher nicht als kommutierender Mehrfachgrenzwert
nachgewiesen.

## 8. Entscheidende Falsifikationstests

Ein weiterer Fit derselben Rechteckantwort wuerde die physikalische Frage
nicht entscheiden. Die folgenden Tests greifen jeweils eine noch offene
Identifikation an.

### A. Port-Herleitung vor weiterer Simulation

Eine externe Wechselwirkung \(U_{\rm ext}(c,t)\) festlegen und zeigen, dass

\[
F=-\partial_c U_{\rm ext},
\qquad
\delta W=F\cdot\delta c
\]

aus der mikroskopischen Kopplung folgt. Kann nur ein additiver \(x\)-Input
begruendet werden, bleibt \(f\,dc\) ein alternativer mathematischer Supply,
nicht die physische Arbeit.

### B. Unabhaengige Skalen- und Massengates

Memory-Zeit \(\tau\), Inputmobilitaet \(\mu\) und Memory-Masse \(M_0\)
unabhaengig variieren, ohne \(\eta\) oder den Kraftgain auf das erwartete
Resultat zurueckzutunen. Die Filterrealisierung sagt vorab

\[
m_{\rm fit}=\tau/\mu
\]

und fuer den normierten Center keine \(M_0\)-Abhaengigkeit voraus. Eine
materielle COM-Hypothese muss dagegen angeben, ob \(F\) Gesamtkraft oder Kraft
pro Masse ist, und daraus eine additive Massen- und Beschleunigungsskalierung
ableiten. Ohne diese Unterscheidung ist ein \(M_0\)-Scan nicht interpretierbar.

### C. Komposition und Impulsbilanz

Zwei getrennte Knoten mit vorab festgelegten Massen \(M_1,M_2\) kombinieren.
Erforderlich waeren mindestens

\[
C={M_1c_1+M_2c_2\over M_1+M_2},
\qquad
P=M_1\dot c_1+M_2\dot c_2,
\]

sowie Erhaltung des Gesamtimpulses unter gleichen und entgegengesetzten
internen Kraeften, gegebenenfalls zusammen mit dem Impuls des Memory-Feldes.
Das ist ein deutlich schaerferer Massentest als eine weitere
Ein-Knoten-Pulsantwort.

### D. Phase operationalisieren oder umbenennen

Fuer eine echte Phase muessen Topologie, Periodizitaet, Wicklung und
branch-cut-invariante Centerbildung vorregistriert werden. Scheitert das, ist
`schneller Traegerpunkt` die wissenschaftlich sauberere Bezeichnung fuer
\(x\).

### E. Transfer ohne Refit

Erst danach \(m\), \(\gamma\) und den Port einfrieren und neue Seeds sowie
dreieckige, glatte, sinusoidale und chirp-artige Kraftprofile testen. Das
prueft Profiltransfer und Nichtlinearitaet. Selbst ein Pass bestaetigt jedoch
primaer die LTI-Realisierung; er ersetzt Port-, Skalen- und Kompositionsgate
nicht.

### F. Mechanische Symmetrien und offene-System-Grenze

Pruefen, ob \(r\) unter einer definierten Zeitumkehr wie eine Geschwindigkeit
transformiert, wie der kausale Memory-Center unter Boosts reagiert und ob eine
Fluktuations-Dissipationsrelation mit unabhaengig definierter Temperatur
existiert. Wegen der Daempfung darf ein effektives Medium einen bevorzugten
Ruherahmen besitzen. Ohne Gesamtbath und Impulsledger darf daraus aber keine
fundamentale oder abgeschlossene Mechanik abgeleitet werden.

## Schlussurteil

Der Referee-Einwand `zweite Ordnung hingeschrieben und Masse abgelesen` trifft
einen staerkeren physikalischen Claim, aber nicht die gesamte geleistete Arbeit.
Es wurde nicht bloss eine beliebige Gleichung postuliert: Der Center folgt aus
dem vorhandenen Memory, der Port besitzt eine positive Speicherbilanz, und die
nichtlineare Finite-\(H\)-Einbettung bestand einen prospektiven numerischen
Test.

Trotzdem bleibt der Kernmechanismus eine Zustandselimination eines
exponentiellen Source-/Sink-Memorys. Der Wert \(m=1\) ist in der aktuellen
Normierung eingebaut. Wissenschaftlich haltbar ist daher eine **positive
passive Center-Inertialdarstellung**. **Emergente physikalische Masse** bleibt
eine Hypothese, bis Observable, Port, Einheitensystem und additive
Impulsbilanz unabhaengig geschlossen sind.

## Referenzen

- [Center-Port-Praeregistrierung](../preregistration/scalar_memory_center_inertial_port_protocol_2026-08-16.md)
- [Center-Port-Ergebnis](../../../dynamics/limits/scalar_memory_center_inertial_port_gate_2026-08-16.md)
- [Vorheriges kritisches Center-Port-Review](scalar_memory_center_inertial_port_review_2026-08-16.md)
- [Sichtbarer Force-/Work-Port](../../../dynamics/limits/scalar_memory_force_work_port_gate_2026-08-16.md)
- [S1-Phasen- und Masse-Falsifikationsprogramm](../../decisions/s1_phase_mass_falsification_program_2026-08-16.md)
