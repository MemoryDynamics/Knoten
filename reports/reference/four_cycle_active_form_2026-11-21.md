# Acht aktive Formkoordinaten und die Bewegung des Vierzyklus

Stand: 2026-11-21. Analytischer Anschluss an
[Vierzyklus](flat_memory_cycle_2026-11-16.md) und
[Formstabilitaet](memory_orbital_binding_2026-11-16.md).
Keine neue Dynamik und keine Auswertung des angefragten positiven
Stabilitaetskandidaten.

**Ergebnis.** Die native Vierphasenregel schliesst nichtlinear auf
vier Orten und einer alten Einheitsrichtung. Die Laenge des
aeltesten Schritts ist in diesem aktiven Zustand nicht vorhanden.
Nach Abzug von Lage und Orientierung bleiben in 3D lokal acht
Formkoordinaten. Auch auf diesem kleineren Zustand kann der
Vierzyklus nicht exakt starr durch ein reines Kopf-Update
verschoben oder gedreht werden: Die aufeinanderfolgenden Fenster
teilen drei nichtkollineare, altersmarkierte Orte. Eine quantitative
Schranke trennt Bewegung der eingepassten Pose von Formabweichung.
In vier Ortsdimensionen reicht das gemeinsame Dreieck nicht;
die gespeicherte Richtung schliesst dort die verbleibende Drehfreiheit
fuer den eingebetteten tetraedrischen Zyklus.

## 1. Exakter nichtlinearer Zustandsabschluss

Betrachte gefuelltes, konsistentes Skalar-/Alignment-Memory
mit $H_s=H_v=4$ und nichtverschwindenden Schritten im betrachteten
lokalen Bereich. Alle Parameter bleiben fest. Schreibe den vollen
Positionslift als $(y_0,y_1,y_2,y_3,y_4)$, neueste zuerst.
Fuer $j=0,1,2,3$ sei $p_j=(y_j-y_{j+1})/|y_j-y_{j+1}|$.
Die native [Implementierung](../../src/emergenz_knoten/vector_memory.py)
liest die skalaren Deposits an den vier Orten $y_0,\ldots,y_3$
und die Richtungsdeposits an denselben Orten. Die ersten drei
Richtungen folgen aus diesen vier Orten; die aelteste Richtung
$p_3$ muss zusaetzlich erhalten bleiben. $y_4$ kommt nirgends
sonst vor.

Setze daher $X=(y_0,y_1,y_2,y_3,p_3)$. Sei $\Psi(X)$ der
unveraenderte native Kopf, optional mit einem additiven
Testinput, der nur von X und extern deklarierten Daten abhaengt.
Die Reduktion von Lage und Orientierung unten betrifft den
rauschfreien, euklidisch aequivarianten Schritt ohne externen Input.
Fuer einen nichtverschwindenden neuen Schritt ist

$$
X^+=(\Psi(X),y_0,y_1,y_2,p_2).
$$

Beweis: In der neuen Historie ist $p_2$ die Richtung von
altem $y_3$ zu altem $y_2$ und damit die nun aelteste Richtung.
Die anderen neuen Richtungen lassen sich aus den vier
neuen Orten rekonstruieren. Zwei geliftete Zustaende mit
gleichen X unterscheiden sich nur durch
$y_4=y_3-\ell p_3$, $\ell>0$. Sie liefern exakt dasselbe
Readout und dasselbe Update. Im Positionslift erfuellt die
neu aelteste Schrittlaenge $\ell^+=|y_2-y_3|$; sie ist eine
Funktion von X und unabhaengig von der vorherigen Laenge.
Das ist eine **nichtlineare** Faktorisierung, nicht ein
aus dem linearen Nullmultiplikator vermuteter Abschluss.
Das Ergebnis gilt nicht fuer einen zusaetzlichen Testinput,
der explizit auf den verworfenen $y_4$ zugreift.

Der aktive Zustand hat $4\cdot3+2=14$ Freiheitsgrade.
Die vorherige [altersmarkierte Rahmenkarte](memory_orbital_binding_2026-11-16.md)
liefert aus den vier ersten Orten sechs euklidische
Lage-/Orientierungskoordinaten und sechs Positionsformkoordinaten.
Die im selben Rahmen ausgedrueckte alte Einheitsrichtung besitzt
lokal zwei Kugelkoordinaten. Die Karte hat somit **acht aktive**
lokale Formkoordinaten. Bei wirksamem Alignment-Kanal geht die
aelteste Richtung in den Kopf ein; sie darf nicht mit der alten
Laenge verworfen werden. Im Neun-Koordinaten-Lift steht
die Laenge nach dieser Trennung in einer eigenen Nullspalte;
im passenden Blockdreieck folgt der schon bekannte Nullfaktor.
Der bedingte Bindungsbeweis in der groesseren Karte bleibt gueltig.
Kein Eigenwert oder Stabilitaetsradius wird hier ausgewertet.

## 2. Warum die aktive Form nicht exakt starr mitwandert

Sei $a_n=S^n(r,0,h)^T$ die bekannte zentrierte Vierfolge, mit
$r,h>0$ und der im Existenzbericht definierten uneigentlichen
Ein-Schritt-Symmetrie S. Die nativen Phasen sind in $a_n$
bereits enthalten. Eine zusaetzliche Pose wird durch
$g_n(a)=Q_n a+t_n$ mit $Q_n\in SO(3)$ dargestellt.
Verglichen werden dieselben Alterslabels, kein nachtraegliches
Umsortieren oder Spiegeln der Vierfolge.

Passen die vier aktiven realen Orte in zwei benachbarten Fenstern
$g_n(a_{n-j})$ und $g_{n+1}(a_{n+1-j})$ exakt, so muessen beide
Posen auf den drei geteilten Referenzorten
$a_n,a_{n-1},a_{n-2}$ uebereinstimmen.
Diese Punkte sind nichtkollinear. Eine eigentliche Drehung,
die zwei unabhaengige Differenzen fixiert, fixiert auch ihr
Kreuzprodukt; danach ist auch die Translation eindeutig.
Also $g_{n+1}=g_n$. Die alte aktive Richtung wurde fuer
diesen Ausschluss nicht benoetigt. Eine ohne Alterslabels
gemessene Wolkenform oder eine Spiegelung ist ein anderes
Problem. Das Resultat verbietet **keine** veraenderte oder
asymptotisch nahezu starre Fortsetzung.

Fuer genannte Posen mit maximalen Ortsfehlern $\delta_n,\delta_{n+1}$
sei $D=\delta_n+\delta_{n+1}$. Setze $\Delta Q=Q_{n+1}-Q_n$,
$\Delta t=t_{n+1}-t_n$ und m gleich dem Schwerpunkt der
drei gemeinsamen Referenzorte a. Aus den geteilten Orten folgt

$$
3|\Delta t+\Delta Q m|^2+
\sum_{a}|\Delta Q(a-m)|^2\le 3D^2.
$$

Die zentrierte Dreiecksmatrix $B=\sum_a(a-m)(a-m)^T$ hat die
positiven Eigenwerte $2r^2$ und $2(r^2+4h^2)/3$, unabhaengig
von der Phase. Dies folgt zum Beispiel fuer die Dreierfolge
$(r,0,h),(0,r,-h),(-r,0,h)$ direkt durch Zentrierung.
Nenne den kleineren Wert $\lambda_2$. Eine Differenz zweier
eigentlich raeumlicher Rotationen hat zwei gleiche nichtnullige
Singulaerwerte $\|\Delta Q\|_2$ und einen Nullwert, sofern sie
nicht selbst null ist. Deshalb ist
$\operatorname{tr}(\Delta Q B\Delta Q^T)\ge\lambda_2\|\Delta Q\|_2^2$:
Hoechstens die groessere Eigenrichtung kann im Nullraum verschwinden.
Also

$$
\|\Delta Q\|_2\le\sqrt{3/\lambda_2}\,D,\qquad
|\Delta t|\le(1+|m|\sqrt{3/\lambda_2})D.
$$

Damit ist Pose pro Update nicht kostenlos: Eine endliche
Poseaenderung braucht entsprechend grosse Formabweichungen.
Das sind kinematische Schranken, kein Mobilitaetsgesetz, kein
Zeitkontinuums-Grenzwert und keine Energieaussage.

### Vier Ortsdimensionen: Die gespeicherte Richtung liefert den vierten Punkt

Bette dieselben Referenzorte mit vierter Koordinate null ein und
erlaube $Q_n,Q_{n+1}\in SO(4)$. Drei gemeinsame Orte lassen nun
eine Drehung in der zweidimensionalen Normalebene des Dreiecks zu.
Beim Vergleich des **gesamten aktiven Zustands** muss aber auch die
aelteste Richtung des neuen Fensters passen. Sie ist der normierte
tatsaechliche Schritt von $x_{n-3}$ nach $x_{n-2}$. Das alte Fenster
enthaelt beide Endpunkte. Bei exakter Formuebereinstimmung stimmen
beide Posen daher auch auf der Referenzdifferenz
$a_{n-2}-a_{n-3}$ ueberein. Diese liegt nicht in der Ebene des
gemeinsamen Dreiecks ($r,h>0$). Die relative Drehung fixiert somit
drei unabhaengige Richtungen und wegen Determinante +1 auch die
verbleibende Normale. Die Pose ist wieder fest. Das gilt fuer
die vierte **Ortsdimension**, nicht fuer vier interne Spinorkomponenten.

Auch eine Fehlerschranke ist moeglich. Sei $L=|a_{n-2}-a_{n-3}|$,
sei $p$ die im neuen Fenster gespeicherte aelteste Einheitsrichtung
und sei $\epsilon_p=|p-Q_{n+1}(a_{n-2}-a_{n-3})/L|$.
Der aus neuem Fenster rekonstruierte Vergleichspunkt
$x_{n-2}-Lp$ liegt hoechstens $\delta_{n+1}+L\epsilon_p$
vom neuen Fit fuer $a_{n-3}$ entfernt. Seine Distanz zu $x_{n-3}$
ist der alte Schrittlaengenfehler, hoechstens $2\delta_n$.
Damit ist der Fehler zwischen den beiden Fits fuer
$a_{n-3}$ hoechstens $E=\delta_{n+1}+3\delta_n+L\epsilon_p$.

Alle vier Referenzorte sind gemeinsam zentriert. Ihre Streumatrix
ist $B_4=\operatorname{diag}(2r^2,2r^2,4h^2,0)$.
Rechts liefern die drei geteilten Orte den Term $3D^2$, der
ergaenzte vierte Ort den Term $E^2$:

$$
4|\Delta t|^2+\operatorname{tr}(\Delta Q B_4\Delta Q^T)
\le 3 D^2+E^2 .
$$

Fuer $b=\|\Delta Q\|_2>0$ besitzt $\Delta Q$ mindestens zwei
Singulaerwerte der Groesse $b$: Die relative eigentliche 4D-Drehung
zerfaellt in zwei ebene Drehbloecke. Der zugehoerige zweidimensionale
rechte Singulaerraum schneidet die dreidimensionale Stuetzebene
von $B_4$ in mindestens einer Richtung. Also ist der Spurterm
mindestens $\min(2r^2,4h^2)b^2$. Die so erhaltene Schranke zeigt,
warum ein 4D-Vergleich nur von Ortsfehlern die alte Richtung nicht
ersetzen kann.

## 3. Scharfe Zusatzdiagnose bei vollstaendiger Positionshistorie

Wenn alle fuenf Orte archiviert sind, ist der Abstand
$d_n=|x_n-x_{n-4}|$ ein ausrichtungsfreier Ringschluss-Test.
Fuer die optimale maximale Positionsabweichung $\delta^*_5$
zu einer beliebig starr platzierten, korrekt gephasten
Fuenferhistorie gilt $\delta^*_5\ge d_n/2$: Der juengste und der
aelteste Referenzort sind identisch, also muss ein gemeinsamer
Vergleichspunkt mindestens um den halben Endpunktabstand
abweichen.

- Bei einem einzelnen additiven Kopfkick k auf der exakten
  Referenz ist $\delta^*_5=|k|/2$. Die Translation der Referenz
  um $k/2$ erreicht die untere Schranke.
- Fuer die vorgeschriebene gleichfoermige Drift $x_n=a_n+n v$
  ist $\delta^*_5=2|v|$. Die Translation um $(n-2)v$ erreicht
  sie fuer alle fuenf Orte. Das ist keine native Driftloesung.

Diese Zahl ist ein Test des **Positionslifts**, keine
Funktion von acht aktiven Formkoordinaten: Aendern von
$\ell$ kann $d_n$ aendern, obwohl X gleich bleibt.
Aus vier Orten und $p_3$ allein darf $d_n$ nicht mit einer
erfundenen alten Schrittlaenge rekonstruiert werden.
Die Ueberlappungsschranke aus Abschnitt 2 hingegen verwendet
ausschliesslich die aktiven Orte.

## 4. Einordnung und Gegenkontrollen

[Horn, J. Opt. Soc. Am. A 4, 629 (1987), Abschnitte 1.B und 2.A-B](https://people.csail.mit.edu/bkph/papers/Absolute_Orientation.pdf)
behandelt die eindeutige starre Lage aus nichtkollinearen
Punktkorrespondenzen und Schwerpunktzentrierung. Die
FIFO-Ueberlappung, die quantitative Schranke und der Blockabschluss
folgen hier direkt aus den jeweiligen gespeicherten Orten.
Diese elementare Geometrie wird nicht als neue Orientierungs-
theorie oder Quantisierung gedeutet.

Die [21 festen Kontrollen](../../tests/test_four_cycle_active_form.py)
verwenden vorhandene Gaussreadouts und FIFO-Shiftprimitive an
festen Nicht-Orbits, pruefen die alte Laengenfreiheit gegen eine
aktive Richtungsstoerung und die Posen-/Ringschlussschranken an
synthetischen Fenstern. In 4D wird ein Scharniervergleich geprueft:
Er passt an den gemeinsamen Orten, aber nicht an der Schrittrichtung.
Alle 98 Tests im betroffenen Panel bestehen. Keine Parametersuche,
kein Lauf am angefragten Kandidaten und keine Tragfaehigkeitsbehauptung.
Ein kuenftiger mechanischer oder gravitativer Test muss die
aktive Formabweichung neben der Centerbewegung ausweisen;
der ausstehende volle Formtest bleibt Voraussetzung.
