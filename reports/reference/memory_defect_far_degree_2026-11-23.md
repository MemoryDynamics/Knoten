# Geschlossene FIFO-Spuren: lokales Vorzeichen und gemeinsamer Fernindex

Stand: 2026-11-23. Analytische Fortsetzung der
[Konstruktion mit beiden lokalen Defektvorzeichen](nonminimal_memory_defects_2026-11-15.md).
Nur gefuellte, vorgegebene Historien und native Gauss-Vektorauslese.
Keine Zieltrajektorie, Parametersuche oder neue Quellenregel.

**Ergebnis.** Jede endliche geschlossene FIFO-Polygonspur,
deren Orte den ganzen affinen Raum aufspannen, hat in der
nativen Gauss-Vektorauslese aussen den globalen Grad $+1$.
Das gilt fuer beliebige positive Speichergewichte, nicht
nur den Tetraeder. Eine positive Summe beliebig vieler
solcher Auslesen hat denselben Fernindex. Die lokalen
Grade addieren sich als Gebietsgrade eines Felds; sie
addieren sich aber nicht unabhaengig beim Ueberlagern
getrennter Kernfelder. Das bekannte lokale Paar $+1/-1$
kann gleichzeitig bestehen, muss im gemeinsamen Feld
jedoch ausserhalb beider Kerne einen Restgrad $+1$ tragen.

## 1. Allgemeiner Grad am grossen Rand

Sei $y_H=y_0$, alle zyklischen Schritte nicht null,
und die $y_j$ spannen $\mathbb R^d$ affin auf.
Mit positiven $w_j$, einheitlicher Breite $\sigma$
und $s_j=|y_j-y_{j+1}|$ fuer native Einheitsrichtungen
(oder $s_j=1$ fuer das Verschiebungsreadout) ist

$$
V(x)=\sum_{j=0}^{H-1}
\frac{w_j}{s_j}(y_j-y_{j+1})
\exp\left(-\frac{|x-y_j|^2}{2\sigma^2}\right).
$$

Fuer eine Einheitsrichtung n und $x=Rn$ setze
$t=R/\sigma^2$, $h_j=n\cdot y_j$, $m=\max h_j$,
$d_j=t(m-h_j)$ und
$a_j=(w_j/s_j)\exp(-|y_j|^2/(2\sigma^2))>0$.
Nach Ausklammern eines positiven Faktors gilt

$$
\operatorname{sgn}(n\cdot V(Rn))
=\operatorname{sgn}\sum_j a_j e^{-d_j}(d_{j+1}-d_j).
$$

Dabei ist $d_H=d_0$. Jeder negative Term hat
Betrag hoechstens $a_j/e$, weil $d_j e^{-d_j}\leq1/e$.
Ist die Gesamtsumme nichtpositiv, kann folglich
auch kein einzelner positiver Term groesser sein
als $\sum_j a_j/e$. In jedem Schritt gilt dann

$$
d_{j+1}\le d_j+\frac{\sum_i a_i}{e\min_i a_i}e^{d_j}.
$$

Beginne am Index mit $d_j=0$ und gehe einmal
die geschlossene Spur entlang. Nach hoechstens
$H-1$ Kanten sind damit alle Defizite durch einen
festen endlichen Wert beschraenkt, unabhaengig
von n und R. Formal ist dies die $(H-1)$-te Iteration
der monotonen rechten Seite ab null. Andererseits
ist das groesste Defizit
$t(\max_j n\cdot y_j-\min_j n\cdot y_j)$.
Die Klammer hat wegen des vollen affinen Spans
ein positives Minimum auf der Einheitssphaere.
Damit waechst das groesste Defizit gleichmaessig
in n gegen unendlich. Also gilt auf jeder
hinreichend grossen Sphaere $n\cdot V(Rn)>0$.

Die lineare Homotopie zum radial nach aussen
gerichteten Feld bleibt dort nullstellenfrei.
Folglich ist der Brouwer-Grad des Innengebiets $+1$.
Es braucht keine Annahme ueber Anzahl oder
Regularitaet der inneren Nullstellen. Der obige
Iterationswert dient als Existenzschranke, nicht
als praktisch brauchbarer Kugelradius. Fuer
endliche R und ungleiche Gewichte kann die radiale
Projektion durchaus negativ sein.

## 2. Zwei entgegengesetzte Kerne sind nicht global neutral

Waehle die beiden bereits konstruierten geschlossenen
Tetraederhistorien mit acht Depositionen (lokaler
Grad $+1$ bzw. $-1$). Richte ihre Kerne im Abstand L
ein und ueberlagere die beiden **Vektorfelder** mit
positiven Lesefaktoren. Jedes Feld hat aus Abschnitt 1
auf hinreichend grossen Kugeln um den gemeinsamen
Ursprung positive radiale Projektion. Ihre Summe
hat daher ebenfalls Grad $+1$, fuer jeden festen
endlichen Abstand. Dasselbe gilt fuer jede endliche
positive Summe solcher geschlossenen Spuren.

Bei hinreichend grossem L bleiben die beiden kleinen
Kernkugeln getrennt und ihre Grade erhalten:
Auf jeder Kugel ist das eigene Feld durch eine
positive Randreserve von null getrennt, waehrend
das andere Feld gaussschwach wird. Damit ist die
Homotopie vom einzelnen Kernfeld zur Ueberlagerung
auf beiden Randkugeln nullstellenfrei.
Gradadditivitaet fuer die **Gebiete
desselben Felds** gibt nun ausserhalb der beiden Kugeln
den erzwungenen Rest $+1-(+1-1)=+1$. Bei zwei lokalen
Pluskernen waere der erzwungene Rest $-1$.
Siehe zur lokalen Gradaddition
[Hatcher, Algebraic Topology, Abschnitt 2.2](https://pi.math.cornell.edu/~hatcher/AT/ATchapters.html).
Eine Zahl einzelner zusaetzlicher Nullstellen oder
ihre genaue Lage wird damit nicht identifiziert.

**Fester Abstand als Kontrolle.** Fuer die
Kernradien $1/6$ genuegt L=20 in den
Einheiten des vorhandenen Tetraederbeispiels.
Der negative Kern hat die bereits bewiesene
Randreserve $w_0\,41/6000$. Fuer den Pluskern
schreibe die Koeffizienten in Tetraederreihenfolge
als $c_i(z)=q^i e^{v_i\cdot z}$. Der gemeinsame Faktor
des Feldes ist $w_0(1+q^4)e^{-(1+|z|^2)/2}>w_0/2$
am Rand. Die Matrix der vier Einheitsschritte
$(v_i-v_{i+1})/\sqrt{8/3}$ hat auf dem
Konstantenkomplement kleinsten Singulaerwert eins:
Die zyklische Differenz hat dort Singulaerwerte
$\sqrt2,2,\sqrt2$ und die Tetraedermatrix skaliert
diesen Raum mit $2/\sqrt3$. Fuer die Projektion P
auf das Konstantenkomplement gilt
$\|Pc\|\ge (\min_i c_i)\|P\log c\|$,
aus der Summe quadrierter paarweiser Differenzen.
Am Rand ist $\min c_i\ge q^3 e^{-1/6}>3/4$
fuer $q=99/100$. Am bekannten Nullpunkt $z_+$ sind
alle $c_i$ gleich, also
$\|P\log c(z)\|=(2/\sqrt3)|z-z_+|$.
Da $|z_+|\le\sqrt{15}/198<1/48$, ist die
Plusreserve groesser als $w_0/20$.
Das andere Feld ist auf jeder Kernkugel durch
$8w_0\exp[-(20-5-1/6)^2/2]$ beschraenkt,
kleiner als beide Randreserven.

## 3. Grenze als Quellenladung

Der Grad ist nicht der Fluss des unnormierten
nativen Feldes. Dessen Fluss durch grosse Kugeln
geht wegen der Gaussfaktoren gegen null, und
$\int\nabla\cdot V=0$. Der Grad beschreibt
die auf dem Rand **normierte** Richtungsabbildung.
Wuerde man diesen Grad als Quellgroesse einsetzen,
koennte man im obigen Paar die erzwungene
Restladung ausserhalb der kleinen Kerne nicht
einfach abziehen. Der
[neutrale Materialvergleich](collective_neutral_material_response_2026-11-23.md)
braucht dagegen eine additiv neutrale Quelle
pro frei verschiebbarem Verbund.

Der Satz gilt fuer endliche geschlossene Spuren
mit positiven Gewichten und gleicher Gaussbreite
je Spur. Offene FIFO-Fenster koennen sogar bei
vollem affinem Span Grad null haben, etwa wenn
alle gespeicherten Schritte in einer offenen
Richtungshalbkugel liegen. Auch fuer unendliche
Ensembles mit nicht vertauschbaren Grenzwerten,
andere Randvertraege oder nichtlineare
Quellenauslesen ist nichts entschieden. Die
Konstruktion erhaelt den Grad nicht unter
beliebigen nativen FIFO-Schritten.

Der [polarisierte Randvergleich](collective_polarized_background_2026-11-23.md)
zeigt einen anderen Randvertrag: Ein konstanter kollektiver
Richtungshintergrund erlaubt Fernindex null. Der schwache
selbstkonsistente homogene Zweig ist aber longitudinal instabil.

[Feste Kontrollen](../../tests/test_nonminimal_memory_defects.py)
pruefen die reskalierte Radialformel, das
Randreserve-Gegenpaar und eine offene Historie.
Die Aussagen ueber alle Richtungen folgen aus
dem Beweis, nicht aus den Stichproben.
