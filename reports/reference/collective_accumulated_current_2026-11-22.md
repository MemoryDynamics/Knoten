# Der aufsummierte Strom rekonstruiert ein Wellenpotential

Stand: 2026-11-22. Analytische Fortsetzung des
[Dichte-/Richtungsabschlusses](collective_directional_current_2026-11-22.md).
Keine neue native Zieltrajektorie, kein neues Kraftgesetz im Code.

**Ergebnis.** Auch kompakte Richtungsdeposits liefern am vorhandenen
skalaren Lesekanal keinen statischen $1/k^2$-Pol gleichzeitig mit der
Dichtewelle. Es gibt aber eine konstruktive Rekonstruktion ohne
neue Antriebsdynamik: Die seit dem Einschalten akkumulierte
longitudinale Stromdichte ist der Gradient eines Potentials, das im
akustischen Grenzwert sowohl einen Wellenresolventen als auch den
statischen Pol besitzt. Das Potential ist eine neue Auslese, keine
neue Eigenschaft des unveraenderten Kraftports.

## 1. Kompakte Richtungsquelle am bestehenden Port

Verwende die Notation des Dichte-/Richtungsabschlusses: k ist die
raeumliche Wellenzahl, u die Dichtevariation, m der longitudinale
Richtungsdeposit, d der mittlere Schritt. $p(k)=e^{-d_0 k^2}$
mit $d_0=\epsilon^2/2$, $B(k)=\epsilon^2\chi k+O(k^3)$
und $T(k)=\chi+O(k^2)$ sind die Gaussmomente.
Bei kritischem Alignment $g_0\chi=1$ sei
$C=\epsilon^2+b_s>0$, also die quadratische
Wellengeschwindigkeit $v^2=C/(1+\bar j_v)>0$.

Gib zum bisherigen skalaren Quellwert s eine externe
Richtungsquelle $j_s$, die mit demselben Gauss-Vektorleser
wie ein nativer Richtungsdeposit gelesen wird. Hier ist
$j_s$ die longitudinale Komponente ihrer Fouriertransformierten.
Statisch lautet der Schritt

$$
d=g(k)(m+j_s)-ik b_s(k)(u+s).
$$

Die stationaeren Dichte- und Richtungsgleichungen liefern bei
$L=p^{-1}-1$ weiterhin $d=iLu/k$ und $m=i(TL/k-B)u$.
Daraus folgt exakt

$$
\left[(1-gT)\frac{L}{k^2}+\frac{gB}{k}+b_s(k)\right]u
=-b_s(k)s-\frac{i g(k)}{k}j_s .
$$

Der Nenner geht gegen $C\ne0$. Fuer eine kompakte
skalare und vektorielle Quelle mit endlicher Masse bzw.
Variationsnorm sind s und $j_s$ beschraenkt. Darum kann
der alte skalare Reader $\widehat K_s(k)(u+s)$ hoechstens
$O(1/k)$ erreichen, keinen $1/k^2$-Monopol. Hat die
Richtungsquelle ein nichtverschwindendes Gesamtvektormoment
$J_0$, ist der fuehrende neue Term proportional zu
$i\mathbf k\cdot J_0/k^2$, also dipolar. Bei Gesamtvektor
null und endlichem erstem Moment ist $j_s=O(k)$ und auch
der vektorgetriebene Anteil bleibt beschraenkt. Eine
bereits langreichweitige oder mit k singulaer skalierte
Quelle ist davon nicht erfasst.

## 2. Eine andere Auslese aus der Transportbilanz

Die erste Variation der Ortsaktualisierung ist im
Zeitbereich $u_{n+1}=p(u_n-ik d_n)$. Setze fuer eine
Nichtnullmode den longitudinalen Transport

$$
J_n=p d_n-i\frac{1-p}{k}u_n.
$$

Dann gilt $u_{n+1}-u_n=-ik J_n$ exakt. Der zweite Term
ist die Diffusionskorrektur: Im Ortsraum entspricht er
$-\nabla\int_0^{d_0}G_t*u_n\,dt$, wobei $G_t$ der
Waermekern mit Fouriermultiplikator $e^{-t k^2}$ ist.
Hier wird keine inverse Laplace fiktiv als Kraft eingesetzt;
$J_n$ ist ein Bilanzstrom aus dem vorhandenen linearen Schritt.
Die [fruehere Stromnotiz](memory_current_invariants_2026-11-04.md)
zeigte bereits die Nicht-Eindeutigkeit des gesamten Stroms
aus der Dichte. Hier wird nur seine longitudinale Komponente
benutzt; die Gleichheit ist unabhaengig von einem transversalen
Zusatz.

Definiere nun

$$
\Phi_n=\frac{u_n}{k^2},\qquad E_n=ik\Phi_n.
$$

Es gilt $E_{n+1}-E_n=J_n$. Fuer ungestoerte Anfangsdichte
ist somit $E_n=\sum_{m<n}J_m$. Im Ortsraum entspricht
dies dem Gradienten von $(-\Delta)^{-1}u_n$ mit
festgelegtem Nullmodus. Die Zeitakkumulation ist eine
zweite Moeglichkeit, **dieselbe longitudinale Auslese**
zu rekonstruieren. Sie benoetigt eine gemeinsame
Anfangsreferenz; im allgemeinen Fall kommt $E_0$ hinzu.
Sie beweist keine harte Kausalfront fuer die mikroskopische
Gaussregel.

## 3. Exakter Quelltransfer und akustisches Grenzsymbol

Setze wieder $j_s=0$ und nutze dieselbe skalare
Testquelle im zeitabhaengigen Schritt:
$d=gP_v m-ik b_s(k)(P_s u+s)$. Mit der zeitlichen
Konvention $z^n$ ist die lineare Gleichung

$$
\begin{pmatrix}
z-p+p k^2 b_s(k)P_s & i p k gP_v\\
i[B+kT b_s(k)P_s] & z-TgP_v
\end{pmatrix}
\binom{u}{m}
=-\binom{p k^2 b_s(k)}{i k T b_s(k)}s .
$$

Sei $D(k,z)$ die Determinante. Im Zaehler des Dichtetransfers
kuerzen sich exakt die beiden Terme mit $TgP_v$:

$$
\frac{u}{s}=-\frac{p k^2 b_s(k)z}{D(k,z)},\qquad
\frac{\Phi}{s}=-\frac{p b_s(k)z}{D(k,z)}.
$$

Am Richtungs-Schwellenwert, bei endlichen FIFO-Horizonten
und fuer $z=e^{k\lambda}$ nahe der Einheitswurzel, gilt

$$
D(k,e^{k\lambda})=k^2\big[(1+\bar j_v)\lambda^2+C\big]
+O(k^3).
$$

Damit folgt abseits der beiden Polstellen fuer festes
$\lambda$:

$$
k^2\frac{\Phi}{s}\longrightarrow
\frac{-b_s}{(1+\bar j_v)\lambda^2+C}.
$$

Das ist das akustische Symbol eines Wellenpotentials mit
Quellstaerke $-b_s/(1+\bar j_v)$. Bei $b_s\ne0$ und
$\lambda=0$ ist das Residuum $-b_s/C$; auf $\mathbb R^3$
entspricht ein nichtverschwindender Quellmonopol dem
$1/r$-Anteil des statischen Green-Kerns. Fuer eine
periodische Box gilt die Aussage nur fuer Nichtnullmoden
mit Behandlung des Mittelwerts. Bei konservierter Masse
darf der Grenzwert $k\to0$ des stationaeren Symbols nicht
als quasistatische Aenderung des exakt erhaltenen
Nullmodus gelesen werden.

Das Zusammenfuehren von Transportbilanz und dynamischer
Stromgleichung ist in der Akustik bekannt, etwa bei
[Lighthill (1952)](https://doi.org/10.1098/rspa.1952.0060).
Hier ist neu im Bestand die exakte diskrete Strom-/Quellformel
fuer den gewaehlten Gauss-Schreibschritt samt Altersfaktoren.
Diese Aussage ueber das Grenzsymbol ist kein bewiesener
raumzeitlicher Konvergenzsatz fuer beliebige Quellen.

## 4. Warum die Rekonstruktion noch keine Wechselwirkung ist

Das vorhandene Modell reagiert auf lokale gewichtete
Deposits und ihren aktuellen Drift. Es liest weder
$\Phi_n$ noch $E_n$ als Kraft. In einem stationaeren
Nichtnullmodus ist der longitudinale Bilanzstrom $J_n=0$,
obwohl der rekonstruierte Gradient $E_n$ von null
verschieden bleibt. Der tatsaechliche stationaere Schritt ist
exakt $d=(p^{-1}-1)E$, also bei kleiner Wellenzahl um
einen Faktor $O(k^2)$ unterdrueckt. Kein konstanter
Umrechnungsfaktor macht daraus dieselbe Fernkraft.
Ein zeitlich summierbarer Filter von
$J_n$ kann diesen bleibenden Wert nach einem abklingenden
Transport nicht tragen: Sein Faltungswert geht dann gegen
null. Die Rekonstruktion verlangt den ungedaempften
Akkumulator oder aequivalent die raeumliche Poisson-Auslese
mit Rand- und Anfangsdaten. Sie ist nicht durch eine
Umbenennung eines endlichen FIFO-Eintrags gegeben.

Damit ist die naechste Interaktionsprobe praezise:
Koennen die vorhandenen Knoten nach dem Abklingen des
Stroms auf diese akkumulierte Groesse reagieren,
und zwar mit derselben Kopplung in mechanischem Antrieb
und Bahnphase? Der
[Skalarfeld-Benchmark](retarded_scalar_interferometer_2026-11-22.md)
zeigt, wie ein solcher Vertrag aussehen wuerde.
Keine dynamische Speicherung des Akkumulators, reziproke
Kraft oder Quantisierung wird in dieser Notiz behauptet.

Der [Selbstkopplungsvergleich](collective_accumulated_feedback_2026-11-23.md)
prueft inzwischen die einfachste anziehende Rueckwirkung auf die
erzeugende Dichte. Sie liefert eine Jeans-artige Langwelleninstabilitaet,
auch mit Delay gleicher statischer Kopplungsstaerke.

[Feste Kontrollen](../../tests/test_collective_directional_current.py)
pruefen die kompakte Quelle, die diskrete Teleskopidentitaet
und den Potenzialtransfer im statischen und im
akustischen Zeitbereich.
