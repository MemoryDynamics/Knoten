# Spontane Richtungsordnung und die Grenze eines neutralen Fernrands

Stand: 2026-11-23. Fortsetzung des
[Dichte-/Richtungsabschlusses](collective_directional_current_2026-11-22.md)
und des [Fernindexsatzes](memory_defect_far_degree_2026-11-23.md).
Deklarierter homogener Mittelfeldabschluss mit nativer Ein-Schritt-Regel,
kein neuer Vielknoten- oder Zieltrajektorienlauf.

**Ergebnis.** Die vorhandene Normierung der Gauss-Schritte ergibt
oberhalb der Alignment-Schwelle einen nichtlinearen homogenen Zweig
mit spontaner Polarisation. Ein solcher eingefrorener Hintergrund
kann den gemeinsamen Fernindex auf null setzen, ohne die lokalen
Grade $+1/-1$ zu beseitigen. Genau der beliebig schwache polarisierte
Zweig nahe der Schwelle ist jedoch gegen longitudinale Dichtewellen
instabil. Eine stabile neutrale Materialumgebung folgt daraus nicht.

## 1. Exakte Amplitude ohne vorgegebene Richtung

Sei $Z\sim N(0,I_3)$ und $d=a e$ die mittlere Verschiebung
im homogenen Zustand, $a\ge0$, $|e|=1$. Die neue
Richtungsdichte pro relativer Dichte ist der Mittelwert
der normierten Verschiebung $d+\epsilon Z$. Setze
$x=a/\epsilon$ und $f(x)=\mathbb E[(x+Z_1)/|x e+Z|]$
in einer Basis entlang e. Es gilt

$$
\frac{f(x)}{x}=L(x)
=\sqrt{\frac2\pi}\int_0^1(1-v^2)e^{-x^2v^2/2}\,dv.
$$

Hier wird $L(0)$ stetig fortgesetzt. Die Formel
folgt aus $r^{-1}=\pi^{-1/2}\int_0^\infty
t^{-1/2}e^{-tr^2}dt$ und der verschobenen
Gaussintegration: Der Erwartungswert im Integral
ist $x(1+2t)^{-5/2}e^{-t x^2/(1+2t)}$.
Setze $v=\sqrt{2t/(1+2t)}$. Die Winkelverteilung
gehoert zur projizierten Normalfamilie, vgl.
[Wang und Gelfand (2013)](https://doi.org/10.1016/j.stamet.2012.07.005).

Der homogene Alignment-Port hat Faktor $g_0>0$,
einschliesslich Dichte, Gewichtssumme und gaussischer
Leseflaeche. Bei konstanten Deposits sind normierte
Altersgewichte ohne Einfluss auf den Fixpunkt.
Die skalare homogene Kraft verschwindet. Fuer einen
nichtverschwindenden Zustand gilt exakt

$$
1=(g_0/\epsilon)L(x),\qquad
\beta=(g_0/\epsilon)L(0),\qquad L(0)=2\sqrt{2/\pi}/3.
$$

$L(x)$ faellt streng fuer $x>0$ und geht gegen null.
Daher existiert eine eindeutige **Amplitude** fuer
$\beta>1$, aber jede Richtung e ist moeglich. Bei
$\beta\le1$ gibt es nur die unpolarisierte Loesung.
Mit $\delta=\beta-1>0$ liefert
$L(x)/L(0)=1-x^2/10+O(x^4)$ den Aufgang
$a^2=10\epsilon^2\delta+O(\delta^2)$.

Der radiale Schleifengewinn
$r=(g_0/\epsilon)f'(x)$ liegt strikt zwischen null
und eins: $f'(x)>0$ folgt aus Monotonie der normierten
axialen Komponente fuer festes transversales Z;
$f'(x)=L(x)+xL'(x)<L(x)$. Fuer endliche nichtnegative
Altersgewichte liegen damit alle radialen
Uniformmoden innerhalb des Einheitskreises. In
den Richtungs-Tangenten ist der Gain genau eins,
passend zur freien Wahl von e. Die radiale Luecke
$\Delta=1-r=2\delta+O(\delta^2)$ folgt aus derselben
Taylorreihe. Dies sind Aussagen bei exakt
homogener Dichte, nicht bei endlicher Wellenzahl.

## 2. Longitudinale Dichtekopplung macht den schwachen Zweig instabil

Betrachte eine Wellenzahl k parallel zu e und
einen polaren Grundschritt $D=a+\epsilon Z$
(vektoriell $a e+\epsilon Z$).
Schreibe $p(k)=\exp(-iak-\epsilon^2k^2/2)$,
$B(k)=\mathbb E[\hat D_1 e^{-ikD_1}]$ und
$T(k)=\partial_a B(k)$. Das **Schreiben am neuen Ort**
liefert im linearen Block
$zu=p(u-ikd')$, $zm=B(k)u+T(k)d'$:
u ist Dichtevariation, m Richtungsdichte und
$d'$ die Driftvariation. Fuer normierte endliche
Altersfilter $P_v$, $P_s$ ist
$d'=g(k)P_v(z)m-ik b_s(k)P_s(z)u$.
Die beiden raeumlichen Lesesymbole seien glatt
und gerade bei null, mit $g(0)=g_0$.
Eliminieren von m liefert fuer den Dichteast

$$
z=p(k)[1-ikL_*(k,z)],\qquad
L_*(k,z)=\frac{g(k)P_v(z)B(k)-ik b_s(k)P_s(z)z}
                 {z-g(k)P_v(z)T(k)}.
$$

Bei $z=1,k=0$ ist der Nenner $\Delta>0$ und
$L_*(0,1)=a/\Delta$. Die Dichtewurzel ist
fuer jedes feste $\delta>0$ lokal einfach.
Setze $\ell=\sum_j j\omega_j$ fuer das mittlere
Vektoralter,
$B_1=\mathbb E[\hat D_1D_1]$ und
$T_1=\partial_a B_1$. Mit
$c=a+a/\Delta$ ergibt Einsetzen von $z=1-ick+O(k^2)$

$$
L_* = a/\Delta+ikL_1+O(k^2),\qquad
L_1=\frac{a\ell c-g_0B_1-b_s(0)}{\Delta}
    +\frac{a[c(1+r\ell)-g_0 T_1]}{\Delta^2}.
$$

Daraus folgt
$\log z=-ick+[L_1+a^2/(2\Delta^2)-\epsilon^2/2]k^2+O(k^3)$.
$B_1$ bleibt beschraenkt und $T_1=O(a)$,
weil $B_1$ eine glatte gerade Funktion von a ist.
Fuer jedes feste endliche Altersprofil und
beschraenkte skalare Abstimmung hat der reelle
$k^2$-Koeffizient somit den positiven fuehrenden Term

$$
\frac{5}{4}\epsilon^2(1+\ell)\delta^{-2}
       +O(\delta^{-1}).
$$

Bei hinreichend kleiner positiver $\delta$ wachsen
daher hinreichend lange **longitudinale**
Dichtewellen. Man nimmt k klein bei jeweils festem
$\delta$; dies ist keine uniforme Extrapolation
zu festen k an die Schwelle. Das Ergebnis
erfasst weder die volle Stabilitaet weiter
oberhalb der Schwelle noch den nichtlinearen
Endzustand. Die Bandinstabilitaet nahe polarer
Ordnung hat enge Parallelen in
[Bertin, Droz und Gregoire (2009)](https://arxiv.org/abs/0907.4688).
Die hier verwendeten diskreten Koeffizienten
und der Divergenzexponent folgen aus der
konkreten Gauss-Schreibregel, nicht aus
einer Uebernahme ihrer hydrodynamischen Gleichungen.

## 3. Was ein eingefrorener polarisierter Rand leistet

Das Feld zweier geschlossener lokaler Historien faellt
im Fernbereich gaussisch ab. Addiert man einen
konstanten Hintergrundvektor $V_b\ne0$, dann ist
die normierte Richtung auf einer hinreichend
grossen Kugel homotop zur Konstantenrichtung
$V_b/|V_b|$: Der Rest hat dort Betrag kleiner
als $|V_b|$. Der Fernindex ist damit null.
Ist $|V_b|$ kleiner als beide freien Randreserven
der Kernkugeln, bleiben deren Grade $+1$ und $-1$.
Der erzwungene **Restgrad** wird dadurch null,
ohne die Abwesenheit weiterer Nullstellen zu
garantieren. Das ist ein Randvergleich, kein
Nachweis einer selbstkonsistenten
Defekt-/Hintergrund-Ueberlagerung.

Eine [feste Randkontrolle](../../tests/test_nonminimal_memory_defects.py)
verwendet beim bisherigen Kernabstand 20 die
Hintergrundamplitude $w_0/300$. Sie ist kleiner als
beide Kernreserven nach Abzug der Kreuzstoerung
und groesser als die Gaussobergrenze auf der
gemeinsamen Kugel mit Radius 35.

Der homogene polare Zweig liefert eine
solche konstante Richtung spontan und erlaubt
beliebig kleine Amplituden. Aber Abschnitt 2
zeigt, dass gerade dieser schwache Hintergrund
kein belastbarer stationaerer Modus des
gekoppelten Mittelfelds ist. Eine nichtlineare
inhomogene Phase oder ein stabiler Bereich
weiter weg waren in dieser Rechnung offen.
Der [Anschluss fuer den ganzen polaren Zweig](collective_polarized_full_branch_2026-11-23.md)
schliesst den homogenen attraktiven Hintergrund
inzwischen bei jeder Amplitude aus; repulsive
und inhomogene Faelle bleiben gesondert.
Selbst bei einem
stabilen polarisierten Rand waere ein
topologischer Grad noch keine mechanische
oder quantenmechanische Quellenladung.

[Feste Integrations- und Matrixkontrollen](../../tests/test_collective_polarized_background.py)
pruefen den homogenen Fixpunkt, die radiale Luecke
und die longitudinale Wachstumsrate direkt an
der linearisierten Schrittregel. Keine Trajektorie
wird gestartet und kein Bereich numerisch abgesucht.
