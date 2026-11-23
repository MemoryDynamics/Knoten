# Sechs Bahnphasen reichen nicht fuer einen negativen 4D-Defekt

Stand: 2026-11-23. Analytischer Anschluss an den
[nativen Fuenf-Deposit-Defekt](native_fifo_five_deposit_defect_2026-11-23.md),
den [minimalen Vorzeichensatz](memory_defect_recurrence_2026-11-14.md#1-alle-minimalen-regulaeren-defekte-haben-dasselbe-vorzeichen)
und die [3D-Zweischalenzeugen](nonminimal_memory_defects_2026-11-15.md).
Vorgegebene gefuellte Fenster, keine native Zieltrajektorie
oder Parametersuche.

**Ergebnis.** Jede geschlossene voll affine Spur mit genau
$d+2$ Richtungsdeposits hat im nativen Gauss-Readout genau eine
Nullstelle. Sie ist regulaer und hat Index $+1$, fuer beliebige
positive Gewichte und eine gemeinsame Breite. In 4D braucht ein
regulaerer negativer Index auf einer periodischen Bahn folglich
mindestens **sieben zeitliche Bahnphasen**, auch wenn das Fenster
mehrere Umlaeufe enthaelt. Andererseits erlauben bereits zehn
vorgegebene, geschlossene 4D-Deposits beide lokalen Vorzeichen
bei identischen nativen Gewichten. Weder native Regeneration
noch elektrischer Quellencharakter werden damit nachgewiesen.

## 1. Der geschlossene erste nichtminimale Fall

Seien $H=d+2$, $y_H=y_0$ und $u_j=y_j-y_{j+1}\ne0$.
Die $y_j$ spannen $\mathbb R^d$ affin auf. Verwende

$$
V(x)=\sum_{j=0}^{H-1}
 \frac{w_j}{s_j}u_j e^{-\|x-y_j\|^2/(2\sigma^2)},\qquad
s_j=\|u_j\|,
$$

mit $w_j>0$ und gemeinsamer $\sigma>0$; $s_j=1$ waere
ebenfalls zulaessig. Die Matrix der $u_j$ hat Rang $d$,
also einen zweidimensionalen Kern. Wegen Ringschluss
enthaelt er $\boldsymbol{1}$. Waehle als zweite Richtung
$v\ne0$ mit $\sum_j v_j=0$. Jede positive Nullrelation ist
nach Normierung auf Mittelwert eins eindeutig
$r_j(t)=1+t v_j$, wobei

$$
 -1/\max v<t<-1/\min v.
$$

Die einzige affine Relation der Orte ist proportional zu
$\ell_j=v_j-v_{j-1}$ (zyklische Indizes), denn
$\sum_j(v_j-v_{j-1})y_j=\sum_j v_ju_j=0$ und $\sum_j\ell_j=0$.
Nach Entfernen des gemeinsamen Gaussfaktors und
Logarithmieren bleiben unbekannt ein Ort $x$ und eine
additive Konstante (logarithmische Gesamtnormierung).
Sie koennen genau dann die Koeffizienten $r_j(t)$
realisieren, wenn

$$
f(t):=\sum_j(v_j-v_{j-1})\log(1+t v_j)
=\sum_j\ell_j\left[\log(w_j/s_j)-\frac{\|y_j\|^2}{2\sigma^2}\right].
$$

Bei gegebenem $t$ ist der lineare Rest fuer $x$ und die
Konstante eindeutig loesbar, weil die Orte vollen affinen
Rang haben. Der Ringschluss liefert dabei die entscheidende
Spezialstruktur im Ableitungsterm:

$$
f'(t)=\sum_j(v_j-v_{j-1})\,g_t(v_j),\qquad
g_t(z)=\frac{z}{1+tz}.
$$

$g_t$ ist strikt steigend auf dem ganzen betrachteten
Werteintervall, denn $g'_t(z)=(1+tz)^{-2}>0$. Fuer jedes
Paar ist das Produkt im Summanden mindestens das Integral
von $g_t$ von $v_{j-1}$ bis $v_j$, unabhaengig von der
Orientierung des Integrals, und strikt groesser bei
ungleichen Endpunkten. Die Integrale teleskopieren auf null.
Somit ist $f'(t)>0$.
Am linken Rand gehen die Koeffizienten auf dem Maximum
von $v$ gegen null; die Summe von $\ell_j$ dort ist strikt
positiv, auch bei mehreren Maxima. Daher $f\to-\infty$.
Analog ist die Summe auf dem Minimum strikt negativ und
am rechten Rand $f\to+\infty$. Es existiert genau eine
endliche Loesung.

**Regularitaet.** Liegt $h$ im Kern der Feldableitung am
Nullpunkt, muss die logarithmische Variation der
Koeffizienten (bis auf einen gemeinsamen Faktor)
die Form $y_j\cdot h/\sigma^2=A+Bv_j/r_j(t)$ haben.
Das folgt, weil die unnormierte Variation im selben
zweidimensionalen Kern wie $r$ liegt. Multiplikation
mit $\ell$ ergibt $0=B f'(t)$, also $B=0$.
Damit ist $y_j\cdot h$ konstant, und der volle affine
Rang erzwingt $h=0$. Der
[Fernindexsatz fuer geschlossene Spuren](memory_defect_far_degree_2026-11-23.md)
gibt Gesamtgrad $+1$; da es genau diese eine regulaere
Nullstelle gibt, ist das auch ihr lokaler Index.

### Erhoehung des Horizonts ersetzt keine neue Bahnphase

Hat eine periodische Bahn $P$ Phasen und enthaelt das
Fenster mindestens $P$ Deposits, lassen sich die
wiederholten Orte und Richtungen je Phase mit einem
aufsummierten positiven Gewicht zusammenfassen. Das
gilt auch fuer Fensterlaengen, die kein Vielfaches von
$P$ sind. Bei $P=d+2$ gilt daher der neue Satz, bei
$P=d+1$ der bisherige Simplexsatz. Kleinere $P$ haben
keinen vollen affinen Rang. Ist der Horizont kuerzer als
$P\le d+2$, sind es hoechstens $d+1$ aktive Deposits;
der bisherige Satz gilt dann auch ohne Ringschluss.
Nullschritte koennen vor der Betrachtung gestrichen
werden, da sie nicht zum Feld beitragen und den
Ringschluss nicht brechen.

Folglich gibt es auf keiner periodischen 4D-Bahn mit
hoechstens sechs Phasen einen regulaeren Minusdefekt
dieses Readouts, selbst wenn die Bahn dynamisch
stabil waere. Offene Sechs-Deposit-Fenster ohne
solche Wiederkehr werden hier nicht klassifiziert.

## 2. Zehn geschlossene 4D-Deposits als Zeugen beider Vorzeichen

Seien $v_0,\ldots,v_4$ die fuenf Einheitsvektoren eines
zentrierten regulaeren 4D-Simplex. Damit
$\sum_i v_i=0$ und $\sum_i v_i v_i^T=(5/4)I$.
Fuer ein orthogonales $J$ waehle entweder $J=I$ oder
$J=I-2v_0v_0^T$. **Nicht** die ganze Spur wird gespiegelt;
stattdessen wird die Verbindung der nahen Punkte zu
ihren aeusseren Nachfolgern geaendert:

$$
y_{2i}=v_i,\qquad y_{2i+1}=v_i-6Jv_i,\qquad y_{10}=y_0.
$$

Dann sind die nativen Einheitsrichtungen an den nahen
Punkten genau $Jv_i$. Die aeusseren Orte haben Norm
mindestens fuenf. In beiden Faellen: $\sigma=1$,
Memory-Masse eins, $q=999/1000$, $w_j=(1-q)q^j$.
Alle Richtungen sind die normalisierten Schritte der
jeweiligen Spur, keine eingesetzten Vorzeichenlabels.
Ein reines Umkehren aller Richtungen wuerde in 4D
das Vorzeichen der Determinante nicht wechseln.

Schreibe fuer den analytischen Vergleich $F=V/w_0$ und
$F_0(z)=\sum_i Jv_iG_1(z-v_i)$. Es gilt $F_0(0)=0$
und $A=DF_0(0)=\kappa J$ mit $\kappa=(5/4)e^{-1/2}>3/4$.
Auf dem geschlossenen Ball $B$ mit Radius $1/8$:

- Die Hesse-Operatornorm eines nahen Gaussfaktors ist
  kleiner als $3/4$ (Abstaende zwischen $7/8$ und $9/8$);
  daher $\|DF_0(z)-A\|\le15/32$.
- Die Abweichung der nahen Altersgewichte hat Summe
  hoechstens $20(1-q)=1/50$. Ihr Ableitungsbeitrag
  ist hoechstens $9/400$.
- Die aeusseren Abstaende sind mindestens $39/8$.
  $e^{-r^2/2}<10^{-4}$ dort und $r e^{-r^2/2}$ ist fallend;
  der aeussere Ableitungsbeitrag ist kleiner als $1/400$.

Damit $\|DF-A\|<15/32+1/40<1/2$. Die Abbildung
$z\mapsto z-A^{-1}F(z)$ ist eine Kontraktion mit
Lipschitz-Konstante kleiner als $2/3$. Ihr Wert in null
hat Betrag kleiner als $(4/3)(1/50+1/2000)<1/24$.
Also bildet sie $B$ in sein Inneres ab. Es gibt genau
eine Nullstelle in $B$, und die geradlinige
Homotopie von $DF$ nach $A$ bleibt invertierbar.
Damit ist ihr Index $\det J$, also $+1$ bzw. $-1$.
Der Ball liegt strikt innerhalb des nahen Simplex
(Inradius $1/4$). Die minimale Zahl von Deposits
fuer Minus in einem geschlossenen Fenster liegt
damit zwischen sieben und zehn; der genaue Wert
bleibt offen.

## 3. Konsequenz fuer den nativen Anschluss

Der Minuszeuge ist ein statisch zulaessiger
Memory-Zustand, kein wiederkehrender Orbit.
Sein Fernindex bleibt $+1$, also muss der Bereich
ausserhalb der kleinen Kernkugel den Gesamtindex
$+2$ tragen. Ein lokales Minus ist somit keine
isolierte Gegenladung. Naechster diskriminierender
Test ist eine echte laengere native Wiederkehr, die
einen Minusdefekt mit kontrollierter Randreserve
phaseweise reproduziert; mehr Speicher bei derselben
kurzen Bahn ist dafuer nachweislich wirkungslos.

Der Uebergang zu einer logarithmischen Gleichung
in positiven Nullraumkoordinaten folgt der
bekannten Idee der
[Gale-Dualitaet von Bihan und Sottile](https://arxiv.org/abs/0706.3745v4).
Die zyklische Differenzform und ihre strikte
Monotonie folgen hier eigens aus dem FIFO-Ringschluss.
Die [festen Kontrollen](../../tests/test_fifo_defect_phase_threshold.py)
pruefen die geschlossene Sechsphase, Fensterlaengen
aus ganzen und angebrochenen Umlaeufen und beide
Vorzeichenzeugen. Die Eindeutigkeit folgt aus
den Beweisen, nicht aus Stichproben einer
Nullstellensuche.
