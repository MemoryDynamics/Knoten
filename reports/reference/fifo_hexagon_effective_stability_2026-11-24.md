# Nichtlineare Naehe zur FIFO-Bahn fuer endliche Zeiten

Stand: 2026-11-24. Dasselbe
[schwerpunktsfreie Sechseck](fifo_center_free_hexagon_2026-11-24.md)
mit gleichen Massen und Radius $1/25$. Keine Modellanpassung,
kein Langzeitlauf und keine native Zieltrajektorie.

**Ergebnis.** In drei Raumdimensionen gibt es auf den festen
Gesamtenergie-, Impuls- und Drehimpulsniveaus eine
nichtlineare Naheschaetzung: Fuer kleine Anfangsabweichung
$\epsilon$ bleibt der reduzierte Zustand fuer mindestens
$c\epsilon^{-4}$ Writes in einer Umgebung der Groesse
$O(\epsilon)$. Dies folgt aus einer Intervallpruefung
der Nichtresonanz bis Grad fuenf und einer endlichen
symplektischen Normalform. Die Konstante $c$ und der
zulaessige Anfangsradius sind hier nicht numerisch bestimmt.
Treue Historie ist als exakte Gleichheit nicht stoerungsstabil;
ihre Fehler bleiben im bewiesenen Fenster aber $O(\epsilon)$.
Keine Aussage ueber ewige oder asymptotische Bindung.

## 1. Vollstaendige Reduktion bei festem Drehimpulsvektor

Auf der Energieflaeche ist die Rotorzeit eine analytische
Funktion von $H_{\rm int}$ nach dem kanonischen Write,
solange der Rotor eine strikt positive kinetische Reserve
hat. Die Energie-Returnkarte ist damit wie bisher
symplektisch. Der Write und der Flug sind raeumlich
aequivariant und erhalten den Gesamtimpuls $P$ und den
Drehimpulsvektor $L$. Fuer die Referenz ist $P=0$ und
der zu der Ebene senkrechte Drehimpuls groesser als
$0.0028$ in den Referenzeinheiten (Intervallkontrolle).

Nach Fixieren von $P=0$ und Quotient durch Translation
verbleiben $24$ Dimensionen im dreidimensionalen
Registerphasenraum. Fixiere nun den gesamten Vektor $L$
auf dem Referenzwert und dividiere durch die Drehungen
um seine Achse. Das Niveau ist lokal regulaer:
Kleine Kippungen veraendern die zwei senkrechten Anteile
von $L$, und Skalieren der Impulse veraendert seinen
axialen Anteil. Die verbleibende Achsendrehung wirkt
lokal frei, da der Kopf-Traeger-Abstand eine nichtnullige
Projektion in die Schreibebene hat. Dies liefert nach
[Marsden und Weinstein](https://www.cds.caltech.edu/~marsden/bib/1974/01-MaWe1974/)
einen lokal glatten, analytischen symplektischen Raum
der Dimension $24-3-1=20$. Die Sechseckreferenz ist
dort ein Fixpunkt schon nach einem Write.

In der Ebene bleiben die sieben inneren Spektralpaare
aus der frueheren Pruefung. Senkrecht dazu verbleiben
drei Paare: Das Paar des frueheren Faktors $u-1$ sind
die gemeinsamen Kippungen der Ebene. Im mitgedrehten
Rahmen werden ihre Erzeuger um $-\pi/3$ gedreht; da
$L\ne0$, bilden sich diese Richtungen invertierbar
auf die Variationen von $L_x,L_y$ ab. Sie sind
somit nicht Teil des festen $L$-Niveaus.
Dies ist der Unterschied zwischen dem linearen
Quernachweis mit beschraenkten Kippungen und der
jetzigen nichtlinearen Rechnung auf dem vollen Quotienten.

## 2. Intervallpruefung der internen Resonanzen

Die zehn Paare im Quotienten haben Winkel
$\theta_j=\arccos(u_j/2)$, bis auf das Vorzeichen
der symplektischen Orientierung. Die
[Intervallkontrollen](../../tests/test_fifo_center_free_hexagon.py)
engen die schon isolierten $u_j$ mit verifizierter
Bisektion ein. Danach werden alle ganzzahligen
Mehrfachindizes $k\ne0$ mit $\|k\|_1\le5$ und die
relevanten Vielfachen $2\pi j$ ueberprueft.
Negation von $k$ ist redundant; wegen
$0<\theta_j<\pi$ reichen $j=-2,-1,0,1,2$.
Die strikten unteren Schranken in Radiant sind:

| Ordnung $\|k\|_1$ | Schranke fuer $|k\cdot\theta-2\pi j|$ |
| --- | --- |
| 1 bis 3 | $0.0058$ |
| 4 | $0.001$ |
| 5 | $0.000024$ |

Die relativ kleine letzte Schranke wird nicht als
praktische Stoerungsamplitude interpretiert.
Vorzeichen der Winkel in kanonischen Koordinaten
aendern diese Pruefung nicht, da alle Vorzeichen
der Mehrfachindizes enthalten sind. Dies sind
Nichtresonanzen des **Ein-Schritt**-Returns, nicht
bloss eines willkuerlich neu getakteten Umlaufs.

## 3. Warum das die Naehe fuer endlich lange Zeiten sichert

Verwende die endliche symplektische Normalform
fuer Abbildungen (methodisch etwa
[Sansottera, Giorgilli und Carletti](https://arxiv.org/abs/1510.06561)).
Nach kanonischer Linearnormierung ist $S$ eine
direkte Summe von Drehungen. Der jeweils fuehrende
nichtlineare homogene Term einer symplektischen
Karte ist ein Hamilton-Vektorfeld. Konjugation
mit lokalen Hamilton-Fluessen entfernt nacheinander
die nichtresonanten Hamilton-Terme der Grade
drei, vier und fuenf. Die Divisoren sind von der
Form $e^{i k\cdot\theta}-1$ mit
$0<\|k\|_1\le5$ und damit alle von null getrennt.
Die einzigen behaltenen Terme in diesen Graden
haben $k=0$: Sie sind im Grad vier ein Polynom
$H_4(I)$ in den Wirkungen $I_j=|z_j|^2/2$.
Es wird weder Konvergenz der ganzen Normalform
noch eine nichtentartete Twist-Matrix vorausgesetzt.

Im neuen lokalen Koordinatensystem hat die Karte
daher die Form

$$
F(z)=S\Phi_{H_4}^{1}(z)+R_5(z),\qquad
\|R_5(z)\|\le C\|z\|^5 .
$$

Die Hauptkarte erhaelt jedes $I_j$ und somit die
euklidische Norm exakt; der analytische Rest hat
die angegebene Schranke in einer genuegend
kleinen Umgebung. Startet $\|z_0\|\le\epsilon$
und liegt die Kugel vom Radius $2\epsilon$ in
dieser Umgebung, liefert Induktion

$$
\|z_n\|\le2\epsilon
\quad\text{fuer}\quad
n\le\left\lfloor\frac1{32 C\epsilon^4}\right\rfloor .
$$

Denn pro Schritt kann die Norm in der doppelten
Kugel hoechstens um $C(2\epsilon)^5$ wachsen.
Die lokale Koordinatenaenderung und der
Symmetriequotient geben daraus die entsprechende
orbitale $O(\epsilon)$-Naehe. Sie halten die
Rotorreserve im selben Fenster von null fern.
Es geht um alle hinreichend kleinen Stoerungen
auf diesen fixierten Niveaus, nicht nur um
eine besonders guenstige Trajektorie. Die
Schranke ist eine mathematische Untergrenze
mit nicht ausgewertetem Restkoeffizienten, kein
numerisch kalibriertes Stabilitaetsfenster.

## 4. Was mit der Historie passiert

Der Kopierfehler $b-y_2$ ist ein glatter,
raeumlich aequivarianter Beobachter und auf
der Referenz null. Fuer den Historienfehler
$y_{j,n}-x_{n-j-1}$ betrachte denselben
Beobachter mit einem Vorlauf von $j+1$
Schritten. Auch er ist in der positiven
Rotor-Domaene glatt, translationsinvariant
und rotationsaequivariant. Daraus folgen
$O(\epsilon)$-Schranken fuer Kopie und
Historie nach den ersten drei Writes im
Naehefenster. Der Vergleich braucht keine
lange ausgerichtete Vorgeschichte: Der
Beobachter liest jeweils nur die letzten
drei Schritte, und seine Norm ist
symmetrieinvariant.

Exakte Gleichheit ist strenger. Gib am
ersten Schnitt dem Traeger den Querimpuls
$+\alpha$ und dem alten letzten Eintrag
$-\alpha$. Da beide Orte am Schnitt gleich
sind, veraendern sich $P$ und $L$ nicht.
Die Mehrenergie $\alpha^2$ wird aus dem
anfangs weiterhin positiven Rotorimpuls
genommen. Alle Ortsdaten und die korrekte
erste Kopie bleiben unveraendert. Nach einem
Flug liegt der Quotient des senkrechten
Kopierfehlers durch $\alpha$ im Grenzwert
zwischen $-0.0162$ und $-0.0159$; beim
juengsten Eintrag liegt die Abweichung
vom wirklich geschriebenen Ort zwischen
$0.1208\alpha$ und $0.1212\alpha$ im
linearen Term. Dies ist per Intervall
zertifiziert und fuer $\alpha=10^{-4}$
durch einen einzelnen autonomen Schritt
gegengerechnet. Die exakte Kopier- und
Historientreue ist also **nicht** invariant
unter allen kleinen Stoerungen, auch wenn
der Fehler kontrolliert klein bleibt.

## 5. Konsequenz

Es gibt jetzt eine nichtlineare endliche
Zeitschranke fuer orbitale Naehe im
isolierten Referenzmodell. Ein
naechster Interaktionsvergleich muss
Impulse, Drehimpuls und Energie zwischen
den Partnern explizit bilanzieren: Die
obige Aussage auf getrennt festen Niveaus
gilt dann nicht automatisch. Ein
gekoppelter Referenztest oder eine
numerische Abschaetzung von $C$ waere
der naechste Pruefstein, nicht die
Interpretation des Sechsecks als Teilchen.
