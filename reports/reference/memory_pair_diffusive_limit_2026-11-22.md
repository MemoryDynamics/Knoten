# Diffusiver Grenzfall der breiten direkten Memory-Paarkopplung

Stand: 2026-11-22. Analytischer Anschluss an die
[vorhandene skalare Paarkopplung](../../docs/reference/hydrogen_pair_audit.md),
den [Einzellaeufer-Transport](fading_memory_diffusive_transport_2026-11-21.md)
und seine [stationaere Kopfantwort](fading_memory_stationary_mobility_2026-11-22.md).
Keine Zielbahn, Parametersuche oder Aenderung des Solvers.

**Ergebnis.** Der explizite Grenzfall eines breiten
direkten Gauss-Kreuzkernels liefert eine gekoppelte
Ortsdiffusion. Die fremde Historie geht auf dieser
Skala nur durch ihre gesamte Quellenmasse ein.
Die eigene Memory bestimmt weiterhin zwei verschiedene
Koeffizienten: die Antwort auf den Kopfinput und
die freie Diffusion. Gleiche Quellenmassen und ein
gemeinsamer Kreuzkernel genuegen daher nicht fuer
eine verschwindende mittlere Mittelpunktdrift.
Fuer ein beschraenktes radiales Gauss-Potential gibt
es auf freiem Raum keine stationaere Abstandsverteilung
dieses Grenzprozesses. Das ist kein Urteil ueber alle
nativen Paarpfade oder quantenmechanische Bindung.

## 1. Welche Skala wirklich untersucht wird

Zwei Laeufer i=1,2 haben je ein festes, gefuelltes,
endliches FIFO, raumverschiebungsinvarianten
beschraenkten Selbstdrift $b_i(h_i)$ und iid isotrope
Gaussinnovationen $Z_{i,n+1}$ mit positiver Varianz,
unabhaengig zwischen den Laeufern. Fuer den
vorhandenen Solver ist $b_i$ der skalare Selbstkanal.
Der Beweis braucht nur die schon geprueften Annahmen
fuer den jeweiligen isolierten Kanal. Die
alten Orts- und Richtungsdaten koennen als
relative Inkremente $h_i$ parametrisiert werden.

Der direkte Kreuzinput liest wie im skalaren
Paarsolver synchron die alte fremde Ortsgeschichte.
Bei Delta-Deposition, Kreuzstaerke $\chi\geq0$ und
radialem Gauss-Potential K benutze
$K_\delta(r)=K(\delta r)$ mit $\delta\downarrow0$.
Fuer einen Doppelgauss bedeutet dies nur,
dass beide Kreuzbreiten durch $\delta$ geteilt
werden; die Kreuzamplituden und alle Selbstparameter
bleiben gleich. Der Kopfzusatz ist exakt

$$
u_{i,n}=-\chi\delta\sum_{\ell=0}^{H-1}w_{j,\ell}
\nabla K\big(\delta(x_{i,n}-x_{j,n-\ell})\big),\qquad j\ne i .
$$

Das ist ein **gemeinsamer Weitbereichs- und
Schwachkopplungsgrenzfall**, nicht der Grenzwert
eines festen mikroskopischen Kreuzkernels.
Setze $X_{i,n}=\delta x_{i,n}$ und
$n(\tau)=\lfloor\tau/\delta^2\rfloor$.
Die skalierten Startorte konvergieren zu festen
Orten, die anfaenglichen relativen Mikroinkremente
sind gleichmaessig beschraenkt. Die Orte selbst
duerfen anfangs Abstaende der Ordnung $1/\delta$
haben. Die Horizonte und Rauschpegel sind fest.

Definiere $W_j=\sum_\ell w_{j,\ell}$,
$F_i(X_i,X_j)=-\chi W_j\nabla K(X_i-X_j)$.
Der Kreuzinput ist gleichmaessig $O(\delta)$.
Weil $\nabla K$ global Lipschitz ist und die
Mikroinkremente gleichmaessig beschraenkte erste
Momente haben, folgt bei festem H

$$
E|u_{i,n}-\delta F_i(X_{i,n},X_{j,n})|
\leq\chi\delta^2\|D^2 K\|_\infty
\sum_\ell w_{j,\ell} E|x_{j,n}-x_{j,n-\ell}|
=O(\delta^2).
$$

Damit ist der kumulierte Fehler auf der skalierten
Ortsskala $O(\delta)$ in $L^1$ fuer jedes feste
Zeitintervall. Die Altersverteilung wurde nicht
vorab durch einen Punkt ersetzt; diese Schranke
rechtfertigt den Ersatz auf genau dieser Skala.

## 2. Kontrolle der schnelleren Selbsthistorien

Fuer den ungekoppelten Uebergang $P_i$ existieren
ein eindeutiges relatives Gesetz $\pi_i$ und
gleichmaessige Totalvariationsmischung.
Sei $g_i-P_i g_i=b_i$ der beschraenkte Korrektor.
Die Kopplung aendert bedingt auf den alten
Paarzustand nur den Gaussmittelwert von v um u;
nenne den so geschriebenen Operator $P_{i,u}$.
Die korrigierten skalierten Orte
$\widetilde X_{i,n}=X_{i,n}+\delta g_i(h_{i,n})$
erfuellen exakt

$$
\Delta\widetilde X_{i,n}
=\delta m_{i,n+1}+\delta\left[u_{i,n}
+(P_{i,u_{i,n}}-P_i)g_i(h_{i,n})\right],
$$

wobei

$$
m_{i,n+1}=Z_{i,n+1}+g_i(h_{i,n+1})
-P_{i,u_{i,n}}g_i(h_{i,n})
$$

eine Martingaldifferenz ist. Bedingt auf die ganze
bisherige Historie sind die beiden Differenzen
unabhaengig, da beide Inputs schon vorher feststehen
und die neuen Gaussinnovationen getrennt sind.
Ihre vierten Momente sind gleichmaessig beschraenkt.
Durch Gauss-Dichtedifferentiation wie bei der
stationaeren Antwort gilt
$(P_{i,u}-P_i)g_i=J_i(h_i)u+O(|u|^2)$ uniform,
mit beschraenktem $J_i$. Die bedingte
Kovarianz von $m_i$ unterscheidet sich vom
ungetriebenen Wert $Q_i(h_i)$ gleichmaessig um
$O(|u|)$: Bei demselben Integrationswert fuer
den neuen Schritt ist die Aenderung von m
$O(|u|)$, und die Gauss-Dichtedifferenz
hat auch mit quadratischer Gewichtung die
$L^1$-Ordnung $O(|u|)$.

### Mittelung ohne Annahme stationaerer Selbsttrajektorien

Fuer jedes beschraenkte zentrierte Readout f der
endlichen Selbsthistorie loest die TV-Mischung
eine beschraenkte Poisson-Gleichung $w-P_iw=f$.
Fuer eine beschraenkte glatte Funktion U der
langsamen Orte zerlege

$$
f(h_{i,n})
=w(h_{i,n})-w(h_{i,n+1})
+[w(h_{i,n+1})-P_{i,u_{i,n}}w(h_{i,n})]
+[(P_{i,u_{i,n}}-P_i)w(h_{i,n})].
$$

In $\delta^2\sum_{n<n(\tau)}U(X_n)f(h_{i,n})$
liefert partielle Summation im ersten Term
einen beschraenkten Rand und eine Summe ueber
$|U(X_{n+1})-U(X_n)|$. Ihr Erwartungswert ist
nach der Skalierung $O(\delta)$, da jeder
skalierte Schritt Erwartungsbetrag $O(\delta)$ hat.
Der zweite Term ist eine Martingalsumme
mit Maximum $O(\delta)$ in $L^2$ auf dem
Zeitintervall. Der dritte ist gleichmaessig
$O(\delta)$ wegen $u_{i,n}=O(\delta)$ und der
Gauss-TV-Schranke. Folglich verschwindet
die Summe uniform in der skalierten Zeit
in Wahrscheinlichkeit. Das gilt komponenteweise
fuer $J_i-\pi_iJ_i$ mit U aus $F_i$ und
fuer $Q_i-\pi_iQ_i$ mit $U=1$.
Es werden keine nativen Bahnphasen stationaer gesetzt.

## 3. Gekoppelte SDE als Grenzprozess

Die korrigierten Orte unterscheiden sich
gleichmaessig nur um $O(\delta)$ von den alten
Orten. Die mittleren Driftinkremente liefern
unter obiger Mittelung
$\int_0^\tau (I+\pi_iJ_i)F_i(X_s)\,ds$.
Die skalierte gemeinsame Martingalsumme hat
im Grenzwert zeitlineare vorhersehbare
Kovarianz mit Diagonalbloecken
$A_i=\pi_i Q_i$ und verschwindenden
Kreuzbloecken. Die beschraenkten vierten Momente
kontrollieren die maximalen Spruenge.
Der Martingal-Pfadgrenzsatz und stetige
Abhaengigkeit derselben Lipschitz-Integralgleichung
vom additiven Pfad liefern auf jedem endlichen
skalierten Zeitintervall:

$$
dX_i=\Lambda_i F_i(X_i,X_j)\,d\tau
+ A_i^{1/2}dB_i ,
\qquad \Lambda_i=I+\pi_iJ_i .
$$

Die $B_i$ sind unabhaengige Standard-Brownsche
Bewegungen. $A_i$ und $\Lambda_i$ sind exakt die
unabhaengig abgeleiteten isolierten Koeffizienten,
nicht zwei Anpassungen an Paardaten. Dies ist
Pfadkonvergenz in Verteilung, kein quantitativer
Fehler fuer eine konkrete lange Simulation.

## 4. Relativort, Mittelpunkt und Bindung

Isotropie liefert $\Lambda_i=\lambda_i I$,
$A_i=a_i I$, $a_i>0$. Setze
$c_i=\chi\lambda_i W_j$ ($j\ne i$) und
$R=X_1-X_2$. Wegen $K(-R)=K(R)$ ist

$$
dR=-(c_1+c_2)\nabla K(R)\,d\tau
+ \sqrt{a_1+a_2}\,dB .
$$

Die Drift des einfachen Mittelpunkts ist
$(c_2-c_1)\nabla K(R)/2$. Bei aktivem Kernel
verschwindet sie fuer alle Abstaende genau
bei $c_1=c_2$. Das ist eine Antwortbedingung,
keine Impulserhaltung. Fuer $c_1,c_2>0$
ist der einzige gewichtete, driftfreie
Mittelpunkt mit Gewichtssumme eins

$$
C_*=(c_2 X_1+c_1 X_2)/(c_1+c_2).
$$

Sein Rauschinkrement hat Kreuzkovarianz mit
$dR$ gleich
$(c_2a_1-c_1a_2)I\,d\tau/(c_1+c_2)$.
Driftfreiheit und unabhaengige Relativ-/Center-
Antriebe sind deshalb genau dann gemeinsam
moeglich, wenn $a_1/c_1=a_2/c_2$.
Bei gleichen Quellenmassen koennen die beiden
Selbstkanaele diese Bedingung verletzen:
Der [schwach attraktive skalare Vergleich](fading_memory_stationary_mobility_2026-11-22.md)
liefert gegen den freien Kanal bereits einen
Unterschied erster Ordnung in diesem Verhaeltnis.
Die Gewichte sind keine unabhaengig
bestimmten physikalischen Massen.

**Keine stationaere Relativbindung im Grenzprozess.**
Falls eine invariante Wahrscheinlichkeit in
ganz $\mathbb R^d$ existierte, koennte man sie
ueber Orthogonaltransformationen mitteln.
Eine nur fuer den Radius postulierte stationaere
Verteilung wuerde ebenfalls eine radiale
invariante Wahrscheinlichkeit erzeugen, da
der Uebergang mit Rotationen kommutiert.
Wegen gleichmaessiger Elliptizitaet und glatter
Koeffizienten haette sie eine glatte radiale
Dichte $p(r)$. Aus der stationaeren
Vorwaertsgleichung ergibt sich konstanter
radialer Fluss
$r^{d-1}(D_R p'+(c_1+c_2)K'p)$,
mit $D_R=(a_1+a_2)/2>0$.
Regularitaet am Ursprung erzwingt Fluss null
(in d=1 ist die Dichte gerade).
Damit waere

$$
p(r)=C\exp[-(c_1+c_2)K(r)/D_R].
$$

Weil K beschraenkt ist, ist diese Dichte
nur mit $C=0$ integrierbar. Also gibt es keine
normierbare invariante Abstandsverteilung.
Lokale Aufenthaltszeiten oder Attraktion
sind davon zu unterscheiden. Die Aussage
gilt dem skalierten Grenzprozess, nicht
einer stillschweigenden Vertauschung von
$\delta\downarrow0$ mit stationaerem
Langzeitverhalten des nativen Paars.

Der [separate Fluchtbeweis](memory_pair_fixed_range_escape_2026-11-22.md)
schliesst stationaere Abstaende spaeter auch bei festen
Gaussbreiten in $d\geq3$ aus. Er wechselt das Pfadgesetz
statt die beiden Grenzwerte zu vertauschen.

## 5. Reichweite, Literatur und Kontrollen

Die Mittelung durch eine Poisson-Gleichung
hat Vorbilder in der
[Diffusionsapproximation von Pardoux und Veretennikov](https://arxiv.org/abs/math/0506596)
und die Martingal-Konvergenz folgt der
[mehrdimensionalen Pfadversion](https://arxiv.org/abs/0712.1929).
Hier ist der diskrete Kreuzterm der vorhandenen
Gauss-Historien die konkret kontrollierte
Kopplung, keine abgeleitete Fernfeldkraft.
Weder gravitative Universalitaet, Coulomb-Schwanz,
Spin noch ein atomarer Spektralbenchmark
folgen aus der Orts-SDE.

Die [fuenf festen Kontrollen](../../tests/test_memory_pair_diffusive_limit.py)
vergleichen die native Kreuzgradient-Skalierung,
die Altersrestschranke und den Mittelpunkt-/Relativort-
Abgleich. Verwendet werden keine Zufallspfade,
Stabilitaetskandidaten oder eingestellten Zielparameter.
53 Tests im betroffenen Panel bestehen.
