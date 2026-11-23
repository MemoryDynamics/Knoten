# Der Kernel-Oszillator bezahlt den FIFO-Schritt

Stand: 2026-11-24. Deklarierter Skalarvergleich zum
[reziproken Kernel-Oszillator](fifo_kernel_oscillator_energy_2026-11-24.md).
Keine Aenderung der nativen Regel, keine Zieltrajektorie,
kein thermischer Badabschluss und keine Quanteninterpretation.

**Ergebnis.** Ein energiegleicher FIFO-Schreibschritt ist moeglich,
wenn die Gesamtenergie das Minimum nach dem Schreiben erreicht.
Eine Phasenaenderung des Oszillators, auch nach Zufallsvorgabe,
kann den spaeteren Kernel aendern, ohne Energie zu laden.
Das bezahlt keine dauerhaft ueberdaempfte Bewegung und macht
das FIFO nicht umkehrbar.

## 1. Verfuegbare Energie und Schreibschwelle

Wir schreiben bei festem Kopf $x$ von der alten Historie $Y$ auf
$Y^+$. Neben der bisherigen Gesamtenergie gibt es keinen zweiten
Puffer. Quadratische Ergaenzung trennt das Minimum von der
Anregungsenergie:

$$
E=F_Y+R,\qquad
F_Y=U_0(x;Y)-U_1(x;Y)^2/(2\kappa),\qquad
R=\tfrac12\left[\kappa(a-a_Y)^2+p^2/I\right],
\qquad a_Y=-U_1(x;Y)/\kappa .
$$

Die FIFO-Verschiebung bestimmt $Y^+$. Fuer ein energieerhaltendes
Schreiben muss daher $R^+=R-(F_{Y^+}-F_Y)\ge0$ gelten.
Dies ist notwendig und hinreichend fuer die Existenz eines neuen
Oszillatorzustands. Ist das neue Minimum zu hoch, meldet die
Referenz den Fall. Sie setzt keine Regel fuer ausgelassene Writes ein.

Eine Rueckbuchung nur im Impuls wuerde bei festem $a$ verlangen,
dass die alte kinetische Energie die feste Schreibarbeit deckt.
Sie kann am Umkehrpunkt scheitern, obwohl $R$ ausreicht.
Ein festes Zweiplatzbeispiel mit Retention $1/2$ und altem
Gaussfaktor $1/2$ hat positive Schreibkosten bei festgehaltenem
$a$ und $p=0$. Das Minimum steigt aber nur um $53/512$,
waehrend $R=9/32$ ist. Der bezahlte Schritt laesst $R^+=91/512$ uebrig.

## 2. Phasentreuer Schritt oder energiegleiche Stoerung

In den zentrierten Energiekoordinaten
$z=(\sqrt\kappa(a-a_Y),p/\sqrt I)$ gilt $R=|z|^2/2$.
Fuer $R,R^+>0$ waehlt die Referenz

$$
z^+=\sqrt{R^+/R}\,\mathcal R_\xi z
$$

mit planarer Drehung $\mathcal R_\xi$ und rekonstruiert danach
die Amplitude um $a_{Y^+}$. Fuer $\xi=0$ ist dies die eindeutige
Naechstpunktwahl in den zentrierten Koordinaten. Die Wahl ist
gesetzt, nicht aus dem FIFO hergeleitet. Fuer ein beliebiges
$\xi$, auch zufaellig gewaehlt, bleibt $R^+$ gleich.
Die festen Phasenproben zeigen: Kein direkter Kick in $x$ ist
noetig, aber der naechste Positionsschritt liest ein anderes $a$
und kann anders ausfallen. Das ist kein thermischer Nachweis.

Bei $R^+=0$ gibt es nur den neuen Ruhezustand. Bei $R=0<R^+$
fehlt die alte Phase; eine neue Phase muss ausdruecklich als
Input deklariert werden. Die Energiebilanz allein waehlt sie nicht.

## 3. Flaechenerhaltung und Informationsverlust

Bei festen $x,Y,Y^+$ ist $F_{Y^+}-F_Y$ konstant.
In Wirkungs-Winkel-Koordinaten ($J=R/\omega$,
$\omega=\sqrt{\kappa/I}$) ist der regulaere Transfer eine
Translation von $J$ und eine Drehung der Phase um die feste
Realisation $\xi$. Damit bleibt die symplektische Flaechenform
im Oszillatorraum erhalten, obwohl der Radius wechselt.
Das gilt nur abseits der Nullradien und bei festgehaltenen Historien.

Der volle FIFO-Schritt ist trotzdem nicht umkehrbar.
Als Gegenprobe halte $x=0$ fest und ersetze nur den aeltesten
Deposit durch zwei verschiedene Punkte mit gleichem Abstand
zum Kopf. Die alten radialen Auslesen und $R$ sind identisch.
Beim Schreiben verschwindet der einzige Unterschied; bei
gleicher Phasenrealisation resultiert derselbe neue Zustand.
Die Kontrolle fuehrt dies am zusammengesetzten Schritt bei
Mobilitaet null aus. Energieerhaltung ist also kein Nachweis
einer Hamiltonschen oder unitaeren Entwicklung der vorhandenen
Freiheitsgrade.

Das Behalten statt Vernichten von Historieninformation ist der
methodische Bezug zu
[Bennett (1973)](https://www.cs.princeton.edu/courses/archive/fall06/cos576/papers/bennett73.html).
Hier wird keine thermische Untergrenze pro geloeschtem Eintrag
berechnet. In einer reversiblen Erweiterung muesste ein anderer
Freiheitsgrad den alten Eintrag tatsaechlich aufnehmen.

## 4. Langzeitgrenze des geschlossenen Referenzbudgets

Hinter dem passiven Bewegungs- und Oszillatorschritt liefert
der bezahlte Schreibschritt $E_{n+1}-E_n=W_{x,n}\le0$,
unabhaengig von $\xi_n$. Fuer feste Gauss-Amplituden und
festen Horizont gibt es $|U_i|\le C_i$ und damit die untere
Schranke $E_{\min}=-C_0-C_1^2/(2\kappa)$. Aus der
quadratischen Ergaenzung folgt zudem
$|a|\le C_1/\kappa+\sqrt{2(E_0-E_{\min})/\kappa}$.
Damit existiert eine uniforme obere Hesse-Schranke
$L_{\max}$ in der Positionsrichtung. Bei festem $\eta>0$
und $\eta L_{\max}<2$ liefert das Gradienten-Abstiegslemma

$$
\left(\frac1\eta-\frac{L_{\max}}2\right)
\sum_{n=0}^{N-1}|x_{n+1}-x_n|^2
\le E_0-E_{\min}.
$$

Die Schranke gilt fuer jede Folge vorgegebener Phasen.
Falls alle Writes zulaessig bleiben, geht
$|x_{n+1}-x_n|$ gegen null. Ein vom geschlossenen Budget
finanzierter dauerhafter Zyklus mit nichtverschwindender
Bewegung ist in dieser ueberdaempften Referenz ausgeschlossen.
Statische gebundene Zustaende oder inerte konservative
Vergleichsdynamiken sind damit nicht ausgeschlossen.
Phasenrauschen kann den Drift beeinflussen, nicht diesen Verbrauch bezahlen.

[Code](../../experiments/current/reference/fifo_kernel_oscillator.py)
und [feste Kontrollen](../../tests/test_fifo_kernel_oscillator.py)
pruefen Energieschwelle, Umkehrpunkt, Phasenvariation,
bedingte Flaechenerhaltung und den Verlust des alten Eintrags.
Der naechste physikalische Vergleich ist ein Speicher, der
den alten Eintrag aufnimmt, oder ein offenes Bad mit
definierter Energiezufuhr.

Der [reversible Traegervergleich](fifo_reversible_carrier_2026-11-24.md)
speichert den ausgeschiedenen Eintrag und bilanziert
die Registerarbeit mit einem separaten Taktimpuls.
Er zeigt auch die globale kanonische Grenze der
hier verwendeten phasentreuen Aktionstranslation.
