# Native 4D-Wiederkehr: ein Fuenfzyklus, aber kein robuster Traeger

Stand: 2026-11-23. Anschluss an die
[native Vierervolumenbilanz](four_cycle_extra_dimensions_2026-11-20.md#5-exakte-volumenbilanz-jenseits-der-linearisierung)
und getrennt vom [bilanzierten internen Referenzschritt](fifo_balanced_volume_2026-11-23.md).
Vier **Ortsdimensionen**, rauschfreie Skalar-/Alignment-Regel,
keine neue Zustandsvariable, Simulation oder Parametersuche.

**Ergebnis.** Fuer volle vierdimensionale Form ist gebundene,
starre Ein-Schritt-Wiederkehr bei positivem Alignment ausgeschlossen.
Bei negativem Alignment braucht sie mindestens einen abstossenden
Skalarbeitrag. Ein zweifach rotierender nichtregulaerer Fuenfzyklus
erfuellt diese Bedingung mit einem einzigen repulsiven Gauss-Kernel
und schliesst die komplette native Kraftbilanz. Dennoch ist er
analytisch instabil, und sein natives Vektorreadout besitzt
keine Feldnullstelle. Existenz und Traegerbildung sind hier
ausdruecklich verschiedene Ergebnisse.

## 1. Was eine starre Wiederkehr erfordert

Setze $H_v=4$, $H_s\leq4$. Bezeichne mit $d_j=y_j-y_{j+1}$
die vier gespeicherten Schritte, juengster zuerst, und mit
$D_j=\|y_0-y_j\|^2$ die quadrierten Abstaende. Der
radiale Skalargradient sei $\nabla K(z)=k(\|z\|^2)z$.
Dann ist das neue Inkrement

$$
d^+=\sum_{k=1}^4 c_k d_{k-1},\quad
c_k=\frac{\eta_v w_{k-1}e^{-D_{k-1}/(2\sigma_v^2)}}{\|d_{k-1}\|}
 -\sum_{j=k}^{H_s-1}\gamma_j,\qquad
\gamma_j=\eta_s v_j k(D_j).
$$

Hier bezeichnen $w_j,v_j$ die nativen gefuellten Gewichte;
eine leere Summe ist null. Die skalare Kraft nutzt
$y_0-y_j=\sum_{l=0}^{j-1}d_l$ und kann die aelteste Richtung
$d_3$ deshalb nicht direkt beisteuern. Die bereits bekannte
Volumenbilanz lautet in dieser Schreibweise $W^+=-c_4 W$.
Mit aktiver aeltester Richtung und $W\ne0$ ist das Vorzeichen
von $c_4$ das des Vektorgains. Mit $c_4=0$ geht der Vollrang
sofort verloren. Exakt planare rauschfreie Startfenster
gewinnen durch diese Regel keinen Rang.

Eine starre Wiederkehr bedeute $x_{n+1}=R x_n+t$ mit
festem orthogonalem $R$ und festem $t$. Dann drehen alle
Schritte mit $R$, haben gleiche Laenge $L$ und sind bei
Vollrang zyklisch: $d_0,R^{-1}d_0,R^{-2}d_0,R^{-3}d_0$
sind eine Basis. Die Kopfgleichung, mit $R^3$ multipliziert,
macht daher

$$
p(z)=z^4-c_1z^3-c_2z^2-c_3z-c_4
$$

zum charakteristischen Polynom von $R$: Es annulliert
einen zyklischen Vektor und damit die ganze Basis.
Insbesondere $\det R=-c_4$.

- **Positiver Gain.** $R$ muss uneigentlich sein. In vier Dimensionen
  hat dann $R$ mindestens einen Fixvektor: Die nichtreellen
  Eigenwerte kommen paarweise, und die Anzahl der $-1$-Werte
  ist ungerade. Schritte haben in jeder Fixrichtung eine
  konstante Projektion. Fuer eine gebundene Bahn muss sie
  null sein. Das widerspricht ihrem Vollrang.
- **Negativer Gain.** $R$ ist eigentlich und sein charakteristisches
  Polynom reziprok, da die Eigenwerte paarweise invers sind und
  $\det R=1$. Deshalb $c_4=-1$ und $c_1=c_3$. Einsetzen liefert

$$
\gamma_1+\gamma_2
=\frac{\eta_v}{L}
 \left(w_0-w_2 e^{-D_2/(2\sigma_v^2)}\right)<0,
$$

  wobei nicht gespeicherte skalare Terme als null zaehlen.
  Der Vergleich $w_0>w_2$ gilt fuer das aktive exponentiell
  vergessende FIFO. Eine rein attraktive skalare Kraft
  ($\gamma_j\ge0$ an den abgefragten Abstaenden) oder kein
  Skalarport kann das nicht erfuellen. Eine isokline Drehung
  genuegt ebenfalls nicht: Ihr einzelner zyklischer
  Schrittraum ist hoechstens zweidimensional. Das ist keine
  Aussage ueber eine allgemeine mehrphasige Spinabbildung.

Die starre Annahme ist fuer diese Ausschluesse wesentlich.
Aus der Volumenbilanz allein folgt bei positivem Gain
fuer einen echten vollrangigen periodischen Orbit nur
gerade Periode, also mindestens sechs Schritte: Bei
hoechstens vier Orten ist die affine Huelle zu klein,
fuenf ist ungerade. Eine solche Sechsperiode wird hier
nicht behauptet.

## 2. Exakte native Fuenfperiode mit Gegenkopplung

Nutze in zwei orthogonalen Ebenen gleichzeitig die Winkel
$2\pi/5$ und $4\pi/5$. Sei $R$ diese Doppeldrehung und
$x_n=R^n x_0$, mit positiven Radien in beiden Ebenen.
Sein Polynom ist $1+z+z^2+z^3+z^4$; damit verlangt die
Kopfgleichung $c_1=c_2=c_3=c_4=-1$.
Es genuegt $D_1=2\log 5$ und $D_2=D_3=2\log 10$ zu setzen.
Die beiden Radienquadrate folgen linear aus

$$
\begin{pmatrix}a&b\\b&a\end{pmatrix}
\begin{pmatrix}r_1^2\\r_2^2\end{pmatrix}
=\begin{pmatrix}D_1\\D_2\end{pmatrix},
\qquad a=(5-\sqrt5)/2,\quad b=(5+\sqrt5)/2.
$$

Beide sind positiv, weil
$a/b<1/2<D_1/D_2<1<b/a$. Zusammen mit den verschiedenen
Drehwinkeln folgt Vollrang der vier Schritte: Ein reelles
Polynom, das den Startschritt annulliert, muss beide
verschiedenen reellen quadratischen Rotationspolynome
teilen, also mindestens Grad vier haben.

Waehle beide Breiten und Memory-Massen gleich eins und
Delta-Deposition. Setze Vektorretention $q=1/2$ und
$\eta_v=-160 L$ mit $L=\sqrt{D_1}$. Die vier reinen
Vektorkoeffizienten sind dann $(-80,-8,-2,-1)$.
Mit skalarem Kernel $K=+G_1$, Retention $s=1/6$ und
$\eta_s=2592$ (also $\eta_s v_0=2160$) ergeben sich
$(\gamma_1,\gamma_2,\gamma_3)=(-72,-6,-1)$.
Damit ist $c_k=-1$ fuer alle $k$, exakt. Die native
Kopfgleichung an einer Phase und orthogonale Aequivarianz
sichern alle fuenf Schritte. Die Zahlen sind eine inverse
Existenzkonstruktion, keine kalibrierten Teilchenparameter.

**Warum nicht der regulaere Simplex?** Bei gleichen Sehnen
ist der Vektor-Gaussfaktor fuer die drei nichtjuengsten
Deposits gleich $g<1$. Normiert auf $c_4=-1$ haben die
reinen Vektorbeitraege die negativen Betraege
$(1/(gq^3),q^{-2},q^{-1},1)$. Aus $c_k=-1$ folgt,
dass die benachbarten Differenzen dieser Betraege
proportional zu $-\gamma_j$ sind. Das letzte Verhaeltnis
der Differenzen ist $q$, das erste
$q(1-q)/(g^{-1}-q)<q$. Ein radialer Skalar-Kernel sieht
bei allen drei Abfragen denselben Abstand, koennte also
nur ein einziges Retentionsverhaeltnis liefern. Dies
schliesst den regulaeren Fuenfpunkt-Simplex in dieser
Klasse aus, unabhaengig von der radialen Skalarform.

## 3. Analytischer Instabilitaetsnachweis

Arbeite im mitdrehenden Rahmen der fuenf gespeicherten
Positionen ($20$ reelle Koordinaten). Sei $J_0$ der
Kopf-Jacobian nach der juengsten Position bei festgehaltenen
alten Positionen. Die Shiftzeilen haben keine Diagonalbloecke.
Die Spur der vollen Ein-Schritt-Ableitung im mitdrehenden
Rahmen ist daher $\operatorname{tr}(R^{-1}J_0)$.
Schreibe $r_j=y_0-y_j$ und $p_0=d_0/L$. Der
Einheitsrichtungs-Jacobian ist in $J_0$ enthalten:

$$
J_0=-(72r_1r_1^T+6r_2r_2^T+r_3r_3^T)
 +80p_0p_0^T
 +8d_1r_1^T+2d_2r_2^T+d_3r_3^T.
$$

Die Vielfachen der Identitaet heben sich als
$1+72+6+1-80=0$ weg. Fuer zyklische Schritte gilt
$d_0\cdot d_1=\log(2/5)$ und $d_0\cdot d_2=-\log2$:
Allgemein ist $d_0\cdot d_j=(D_{j-1}+D_{j+1}-2D_j)/2$.
Die gleiche zyklische Identitaet in den Rang-eins-Termen ergibt

$$
\operatorname{tr}(R^{-1}J_0)
=\left(71-\frac{40}{\log5}\right)\log(5/2)-21\log2
>26.7>20.
$$

Die strikten Schranken $\log5>1.6$, $\log(5/2)>0.9$ und
$\log2<0.7$ folgen aus der Reihe
$\log x=2\sum_{k\ge0}((x-1)/(x+1))^{2k+1}/(2k+1)$,
mit geometrischer Restschranke fuer $\log2$.
Mindestens ein Eigenwert der vollen Ableitung muss also
Betrag groesser eins haben. Wegen $R^5=I$ entspricht die
Ableitung ueber die volle Periode der fuenften Potenz
dieser mitdrehenden Ableitung. Eine Symmetrierichtung
des periodischen Orbits kann diese wachsende Mode
nicht erklaeren. Kein Parameterscan, Eigenwertlauf oder
neuer Test eines frueher angefragten Stabilitaetskandidaten
wird hier verwendet.

## 4. Folgerung fuer den Traeger

Die vier nativen Richtungsdeposits des Fuenfzyklus sind
linear unabhaengig. Da alle ihre Gausskoeffizienten positiv
sind, kann das Vektorreadout an keinem endlichen Ort
null werden. Der Kandidat kann somit nicht gleichzeitig
den gesuchten regulaeren Punktdefekt in 4D tragen.
Fuer dieses Vektorreadout mit positiven Gaussgewichten sind zur Nullstelle
mit vollem Rang mindestens fuenf Richtungsdeposits noetig.
Mehr Richtungsdeposits oder echte mehrphasige Formdynamik
sind unterscheidbare naechste Wege, nicht schon Loesungen.
Es folgt keine Quantisierung, kein 720-Grad-Readout und
keine Kopplung an eine Ortskraft anderer Knoten.

Der [Anschluss mit fuenf Richtungsdeposits](native_fifo_five_deposit_defect_2026-11-23.md)
liefert eine native Familie mit innenliegendem $+1$-Defekt,
schliesst aber deren dynamische Stabilitaet analytisch aus.

Repulsive verzoegerte Eigenwechselwirkung und persistente
Bewegung sind aus anderen Modellen bekannt; siehe
[Kopp und Klapp, PRE 107, 024611 (2023)](https://doi.org/10.1103/PhysRevE.107.024611).
Dort ist es ein rauschbehaftetes Teilchen mit einem festen
Zeitverzug. Die Arbeit ist ein physikalischer Vergleich,
keine Quelle fuer die Vierplatzbilanz, Fuenfperiode oder Spur.

Die [festen Kontrollen](../../tests/test_native_fifo_four_volume_rotation.py)
setzen die Kraft an allen fuenf vorgeschriebenen Phasen
in die nativen Readouts ein, pruefen die rationalen
Koeffizienten und vergleichen die Spurformel mit der
implementierten vollen Kopfableitung. Die Aussagen zur
Existenz, zum Ausschluss und zur Instabilitaet folgen aus
den Rechnungen, nicht aus der numerischen Wiederkehr
einer simulierten Trajektorie.
