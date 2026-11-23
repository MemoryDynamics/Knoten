# Ein radialer Referenzkernel fuer zwei entgegengesetzte FIFO-Defekte

Stand: 2026-11-23. Anschluss an die
[Kraftobstruktion des symmetrischen Minuszeugen](fifo_negative_phase_recurrence_2026-11-23.md).
Vier vorausgesetzte Ortsdimensionen, keine Zieltrajektorie,
Parametersuche oder Aenderung des nativen Doppel-Gauss-Kernels.

**Ergebnis.** Zwei leicht deformierte Zehn-Phasen-Spuren mit
Index $+1$ bzw. $-1$ sind exakte periodische Loesungen
derselben rauschfreien FIFO-Regel **mit einem frei interpolierten
radialen Skalarprofil**. Beide benutzen dieselben Speichergewichte
und denselben aktiven Gauss-Vektorport. Das ist ein inverser
Machbarkeitsbenchmark, kein Nachweis fuer den nativen Kernel,
keine spontane Bildung und insbesondere kein wechselwirkendes
Plus-Minus-Paar. Dieselbe exakte Wiederkehr vertraegt beliebig
starke lineare Instabilitaet, weil die Anpassung die Steigungen
des Kraftprofils nicht festlegt.

## 1. Kontrollierte Geometrie und native Kraftform

Die [Referenzdatei](../../experiments/current/reference/fifo_inverse_radial_pair.py)
enthaelt beide Zehnpunktfolgen als ganzzahlige Koordinaten geteilt
durch $10^8$. Ihre einzelnen Orte weichen um weniger als
$\varepsilon=1/200$ von den vorherigen Plus- bzw. Minuszeugen ab.
Die Abweichung wird koordinatenweise durch rationale
Quadratvergleiche mit der exakten Helmert-Darstellung des
regulaeren Simplex kontrolliert. Alle $45+45=90$ quadrierten
Paarabstaende innerhalb der jeweiligen Zyklen sind gemeinsam
verschieden. Die kleinste positive Differenz ist exakt
$234034976171/10^{16}$.

Wir verwenden $H_s=H_v=10$, Vektorretention $q=999/1000$,
die Vektorbreite eins, Masse eins und Gain eins. Der skalare
Altersfaktor ist $s^j$ mit $s=1/2$; der gemeinsame Faktor
des juengsten Gewichts ist im Kraftprofil $f$ absorbiert.
Das Update hat die gewohnte Form

$$
x^+=x+V_{\rm FIFO}(x)+\sum_j s^j f(D_j)(x-y_j),
\qquad D_j=\|x-y_j\|^2.
$$

Ein Profil $f$ dieser Form definiert ein glattes radiales
Potential mit Ableitung $-f(D)/2$ bezueglich $D$. Das Profil
ist **nicht** auf zwei Gaussfunktionen beschraenkt. Es hat
keine expliziten Phasen-, Knoten- oder Ladungslabels.

## 2. Warum exakt ein gemeinsames Profil ausreicht

Bezeichne die Punkte einer Spur neueste zuerst als $x_i$,
indiziert modulo zehn. An Phase $i$ muss der Kopf $x_{i-1}$
geschrieben werden. Fuer ein ungeordnetes Paar $\{i,j\}$
mit $i<j$ setze $D_{ij}=\|x_i-x_j\|^2$. Der unbekannte
Wert $f(D_{ij})$ hat in den vier Gleichungen von Kopf $i$
die Spalte $2^{-(j-i)}(x_i-x_j)$ und in denen von Kopf $j$
die Spalte $-2^{-(10-j+i)}(x_i-x_j)$. Alle anderen
Eintraege dieser Spalte sind null. So entsteht pro Spur
eine Matrix $M$ der Groesse $40\times45$ und das System

$$
M c=b,\qquad
b_i=x_{i-1}-x_i-V_{\rm FIFO}(x_i).
$$

Der Rang ist **exakt** 40. Dazu multipliziere $M$ mit
$10^8\,2^9$. In lexikographischer Paarreihenfolge bilden
die nullbasierten Spalten $0,\ldots,37,39,40$ einen
quadratischen Minor. Seine Determinante modulo $65537$
ist $23994$ im Plusfall und $6152$ im Minusfall.
Beide sind von null verschieden. Das Zertifikat verwendet
keine gerundete Rangtoleranz und gilt fuer jede rechte
Seite, hier also auch fuer den unveraenderten Vektorport.
Fuer die numerische Kontrolle wird die Loesung kleinster
euklidischer Norm des **vollen** Systems verwendet,
nicht die schlechter konditionierte Minorloesung.

Die beiden Wertetabellen haben disjunkte Abstandsargumente.
Deshalb laesst sich **eine** glatte Funktion fuer ihre
Vereinigung bauen. Um jedes $D_e$ waehle einen Traeger
mit Halbbreite $h$ gleich einem Drittel des kleinsten
Abstandsgaps. Sei $\psi(u)=\exp[-u^2/(1-u^2)]$ fuer
$|u|<1$ und null ausserhalb. Dann

$$
f_m(D)=\sum_e \psi((D-D_e)/h)\,[c_e+m(D-D_e)]
$$

realisiert fuer beliebiges $m$ exakt $f_m(D_e)=c_e$
und $f_m'(D_e)=m$. Damit ist die Kopfgleichung an
allen 20 vorbereiteten Phasen erfuellt, die Shiftzeilen
reproduzieren die jeweilige Chronologie. Der inaktive
Skalar-Selbstterm hat Abstand null und traegt nichts bei.
Die numerische Ein-Schritt-Kontrolle der Kopfwerte
liegt absolut unter $10^{-9}$. Die Existenz folgt aus
dem exakten Rang und der Interpolation, nicht aus
einer tolerierten numerischen Bahnabweichung.

## 3. Die beiden Vorzeichen ueberleben die Deformation

Verwende die [phasengleichen Referenzfelder](fifo_negative_phase_recurrence_2026-11-23.md#2-vorbereiteter-zehn-phasen-zeuge-behaelt-seinen-index)
$F_0(z)=\sum_i Jv_i G_1(z-v_i)$, $A=DF_0(0)=\kappa J$,
$\kappa>3/4$. Fuer den Ball $|z|\leq1/8$ gilt
$\|D^2F_0\|\le15/4$. Ein naher Schritt hatte Laenge
sechs und aendert sich um hoechstens $2\varepsilon$.
Seine Einheitsrichtung aendert sich daher um
hoechstens $2\varepsilon/3$.
Die globalen Schranken $\|\nabla G_1\|,\|D^2G_1\|\le1$
begrenzen den Deformationsfehler der fuenf Nahterme
im Feld und in seiner Ableitung jeweils durch
$(25/3)\varepsilon$. Jeder Punkt der deformierten
Fernschale bleibt von jedem Auswertungspunkt im Ball
mindestens $5-\varepsilon-1/8$ entfernt; die frueheren
Schranken $1/2000$ (Feld) und $1/400$ (Ableitung)
gelten weiterhin.

Fuer das native Feld geteilt durch $w_0$ ist am Rand
die Abweichung von $Az$ somit kleiner als

$$
\frac{15}{512}+\frac{3}{160}+\frac1{2000}
  +\frac{25}{3}\varepsilon <\frac{3}{32}<|Az|.
$$

Die Terme sind Taylorrest, fehlende Nahgewichte,
Fernfeld und Deformation. Die Homotopie zu $Az$
hat also in jeder Phase Grad $\det J$.
Zudem $\|DF-A\|<15/32+9/320+1/400+(25/3)\varepsilon<0.55$,
so dass $F$ auf dem Ball injektiv ist und seine
Ableitung dort dasselbe Determinantenvorzeichen hat.
Somit liegt in jeder Phase genau ein regulaerer
Defekt mit dem angegebenen Index in der Kernkugel.
Die fuenf Nahpunkte spannen weiterhin die volle affine
Dimension auf: Ihre konvexe Huelle enthaelt mindestens
den konzentrischen Ball vom Radius $1/4-\varepsilon$,
wie man in jeder Stuetzrichtung am maximalen Ortsfehler
sieht.
Der negative Kern bleibt wegen des bisherigen
Fernindexsatzes keine isolierte Gegenladung.

## 4. Was der inverse Kernel nicht bestimmt

Die Werte $c_e$ schliessen die periodische Kraftbilanz,
nicht ihre Ableitung. Der Parameter $m$ in $f_m$
aendert keine der beiden Bahnen. In der vollen
Ein-Schritt-Historienableitung traegt er linear bei;
nur die neue Kopfzeile haengt von ihm ab. Ihr
linker $4\times4$-Block erhaelt den Zusatz $mB_i$,
mit

$$
B_i=2\sum_{j=1}^{9}s^j(x_i-y_j)(x_i-y_j)^T>0.
$$

Die strikte Positivitaet folgt aus dem vollen affinen
Span der zehn Orte. Teile die Ableitung des vollen
Periodenupdates durch $m^{10}$ und lasse $m\to+\infty$.
Der Grenzoperator hat nur die erste Blockzeile
besetzt, mit dem invertierbaren Produkt der zehn
$B_i$ links oben. Sein Spektralradius ist positiv.
Damit werden die Floquet-Multiplikatoren fuer passende
grosse $m$ **unbeschraenkt** gross. Dies konstruiert
keine stabile Alternative; es zeigt, warum die
Kraftanpassung Stabilitaet nicht voraussagt.

Auch die Naehe zum symmetrischen Minuszeugen ist
kein regulaerer Grenzgang. Bei festem $s,q$ und
Vektorgain hat seine unverformte Fernphase eine
nachgewiesene, von null verschiedene Querreserve
ausserhalb der skalaren Driftrichtung. Fuer
kleine Ortsdeformation $\delta$ aendern sich die
Abstandsargumente und radialen Einheitsfaktoren
stetig um $O(\delta)$ (die Schrittlaengen sind
nicht null). Ein auf dem beanspruchten Abstandsintervall
einheitlich beschraenktes und Lipschitz-stetiges
Profil aenderte die skalare Querkraft nur um
$O(\delta[\|f\|_\infty+\operatorname{Lip}f])$.
Zum Ausgleich der festen Querreserve muesste
diese Summe mindestens von Ordnung $1/\delta$
wachsen. Die hier gewaehlten sehr schmalen
Interpolationsfenster ($h\approx7.80\cdot10^{-6}$)
sind daher kein Hinweis auf einen glatten,
massstabstreuen Grenzkernel.

Die Vollsysteme haben numerisch Konditionszahlen
von etwa $9.8\cdot10^5$ und $1.6\cdot10^4$.
Dies sind Modellwarnungen, keine Unsicherheit des
exakten Existenzzertifikats. Eine physikalische
Weiterarbeit braucht einen **vorab** beschraenkten
Kernel, eine unabhaengige Stabilitaetspruefung und
erst danach einen Test gemeinsamer Feldrueckwirkung.
Inverses Design isotroper Potentiale ist auch in
anderen Modellen bekannt, siehe
[Rechtsman, Stillinger und Torquato (2005)](https://arxiv.org/abs/cond-mat/0508495).
Dort geht es um spontane Selbstorganisation einer
Gleichgewichtsstruktur, nicht um eine verzoegerte
periodische FIFO-Kraftbilanz.

Die [festen Kontrollen](../../tests/test_fifo_inverse_radial_pair.py)
verifizieren Rang, Abstandsaufloesung und Deformationsschranke
exakt, sowie Kopfwerte, Vorzeichen und die Veraenderbarkeit
der Steigung in der numerischen Referenz. Keine native
Zieltrajektorie und kein Stabilitaetsscan.
