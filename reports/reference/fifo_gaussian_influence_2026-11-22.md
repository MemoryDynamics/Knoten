# Wann eine lineare FIFO-Antwort mit einem Quantenmedium vereinbar ist

Stand: 2026-11-22. Fortsetzung des
[Einbahn-Wirkungstests](memory_single_path_action_2026-11-22.md).
Deklarierter Gaussscher Zwei-Bahn-Vergleich, kein neuer nativer
Ziellauf und keine Quantisierung des FIFO.

**Ergebnis.** Fuer eine lineare kausale Antwort und einen
Gaussschen Zweigvergleich gibt es eine exakte Positivitaetsgrenze.
Im Zweizeitenbeispiel genuegen unterhalb der Grenze schon drei
vorbereitete Historien zum Ausschluss, obwohl jeder einzelne
Paarvergleich einen Betrag hoechstens eins hat. An und oberhalb
der Grenze laesst sich eine solche Umgebung im gegebenen Fenster
durch eine Folge kontrollierter Vakuumverschiebungen realisieren.
Fuer einen zeittranslationsinvarianten FIFO mit weissem
Phasenrauschen folgt daraus eine explizite Frequenzschranke.

## 1. Vertrag und Positivitaet

Zwei unabhaengig kontrollierte reelle Historien $x,y\in\mathbb R^m$
beinhalten je m Zeitproben. In normierten Einheiten setze

$$
F(x,y)=\exp\left(i(x-y)^T R\frac{x+y}{2}
                 -\frac12(x-y)^T N(x-y)\right),
\qquad N=N^T\in\mathbb R^{m\times m}.
$$

$R$ ist die reelle lineare Antwort im Phasenexponenten,
$N$ die angesetzte Dephasierungs-Kovarianz. Der Ansatz hat
keine implizite Umrechnung eines nativen Drifts in Wirkung.
Sei die Umgebung zunaechst in festem Zustand $\rho$,
unabhaengig von der gewaehlt vorgegebenen Historie. Jede
Historie steuert eine unitaere Entwicklung $U_x$ derselben
Umgebung. Dann ist
$F(x,y)=\operatorname{tr}(U_x\rho U_y^\dagger)$.
Die Matrizen mit Eintraegen $F(x_i,x_j)$ sind Gram-Matrizen
(in transponierter Skalarproduktkonvention) und muessen fuer
jede endliche Familie positiv semidefinit sein. Die
Einflussdarstellung folgt
[Feynman und Vernon (1963), Abschnitt II](https://doi.org/10.1016/0003-4916(63)90068-X).

Setze $S=(R+R^T)/2$, $A=(R-R^T)/2$ und $B=N+iA$.
Dann gilt fuer $f(x)=\exp(ix^T Sx/2-x^T Nx/2)$

$$
F(x,y)=f(x)\overline{f(y)}\exp(x^T B y).
$$

**Satz.** Genau dann sind alle diese Matrizen positiv
semidefinit, wenn $B\succeq0$.

Fuer Hinreichendheit faktorisiere $B=L^\dagger L$.
Die Matrix $x_i^T Bx_j$ ist eine Gram-Matrix; ihr
elementweises Exponential ist wegen der Potenzreihe
und des Schur-Produktsatzes ebenfalls positiv semidefinit.
Die Faktoren $f$ aendern das nicht. Zur Notwendigkeit
waehle $x_0=0$ und $x_j=\delta e_j$. Nach Division der
Zeilen- und Spaltenfaktoren ist der Schur-Komplementblock
ueber dem Eintrag $F(0,0)=1$ gleich
$(\exp(\delta^2 B_{jk})-1)_{jk}$. Dividiere durch $\delta^2$
und lasse $\delta\to0$. Wegen der Abgeschlossenheit
des positiven Kegels folgt $B\succeq0$.

Fuer zwei Zeitproben ergibt sich die notwendige Bedingung
$N_{jj}N_{kk}-N_{jk}^2\geq A_{jk}^2$. Sie beschraenkt den
**gemischten** Phasenbeitrag, nicht eine konservative
Einzelbahndifferenz. Fuer die drei Historien $0,u e_j,v e_k$
hat das Produkt der drei Einflussfaktoren rund um den
Vergleichszyklus die abgewickelte Phase $uv A_{jk}$.
Die reine Phase $x^T Sx/2-y^T Sy/2$ kuerzt sich darin heraus.
Ein nichtverschwindender gemischter Beitrag kann also im
Ansatz nicht mit $N=0$ einhergehen. Eine vorgegebene
konservative Hoehenphase wie im
[Gravitationsvergleich](memory_gravity_action_phase_2026-11-22.md)
ist von dieser Daempfungsschranke allein nicht betroffen.

## 2. Konstruktive Medienreferenz fuer kausales R

Sei $R$ untere Dreiecksmatrix und $B=L^\dagger L$.
Man verwende bosonische Vakuummoden; die Verdrahtung wird
nicht aus Memory hergeleitet. Zur Zeit j werde die
Weyl-Verschiebung $D(a_j x_j)$ angewendet, mit
$a_j=\overline{Le_j}$. Die Konjugation wird in einer
festen orthonormalen Modenbasis genommen. Fuer geordnete
Kicks liefert die Weyl-Relation

$$
D(a)D(b)=e^{-i\operatorname{Im}(a^\dagger b)}D(a+b).
$$

Der Endzustand ist deshalb der kohaerente Zustand mit
Amplitude $\beta_x=\sum_j a_j x_j$ und der zusaetzlichen
Phase $\sum_{j>k}A_{jk}x_jx_k$. Weil R kausal ist, gilt
$A_{jk}=R_{jk}/2$ fuer $j>k$. Ein lokaler Phasenfaktor
$\exp(i\sum_j R_{jj}x_j^2/2)$ vervollstaendigt den
Einzelbahnterm $x^T Sx/2$. Der Ueberlapp der
Endzustaende liefert den Rest, denn
$\beta_y^\dagger\beta_x=x^T B y$ und
$\|\beta_x\|^2=x^T Nx$. Das ergibt genau das F aus Abschnitt 1.
Kohaerente Zustandsueberlappe und Verschiebungen sind
bekannt, siehe [Glauber (1963)](https://doi.org/10.1103/PhysRev.131.2766).
Die Konstruktion betrifft den Einfluss auf kontrollierte
Historien, nicht die autonome Bewegung eines quantisierten
Teilchens. Vakuum, Moden und die quantenmechanische
Zustandsregel sind Inputs der Positivkontrolle.

## 3. Spektraltest mit endlicher Erinnerung

Am konstanten Zustand hat der vorhandene skalare Memory-Drift
pro linearer Ortskomponente die Form
$-\eta\kappa\sum_{j=1}^{H-1}w_j(x_n-x_{n-j})$,
wenn $\kappa$ die effektive Kernelkruemmung am Ursprung
bezeichnet. In einem **deklarierten** Einflussfenster
nehme R dieselbe Verzugsstruktur an, mit zu normierenden
Koeffizienten $R_{n,n-j}=\gamma_j$. Der Diagonaleintrag
veraendert die folgende Schranke nicht. Fuer $N=\nu I$
lautet der exakte Test im endlichen Fenster

$$
\nu\geq \left\|\frac{R-R^T}{2}\right\|_{2}.
$$

Denn die Eigenwerte von $iA$ treten in entgegengesetzten
Paaren auf. Fuer nur einen aktiven Lag $\gamma_1$ und m
Proben ist die Grenze $|\gamma_1|\cos(\pi/(m+1))$:
Diagonale unitare Umphasung macht $iA$ zur reellen
symmetrischen Nachbar-Kopplungsmatrix. Ihre Sinusmoden
haben die entsprechenden Cosinus-Eigenwerte.

Fuer **alle** endlichen Fenster gilt genau dann Positivitaet,
wenn

$$
\nu\geq\sup_\theta
\left|\sum_{j=1}^{H-1}\gamma_j\sin(j\theta)\right|.
$$

Das hermitesche Toeplitz-Symbol ist
$h(\theta)=\nu+\sum_j\gamma_j\sin(j\theta)$.
Ist es nichtnegativ, drueckt Fourier-Inversion jede
endliche Matrix als Gram-Matrix der Funktionen
$\sqrt{h(\theta)}e^{-in\theta}$ aus, im Mass
$d\theta/(2\pi)$. Damit ist dieselbe Modenkopplung
fuer alle Fenster verfuegbar, nicht pro Fenster neu angepasst.
Ist h irgendwo negativ, konvergieren die Rayleigh-Quotienten
abgeschnittener ebener Wellen bei dieser Frequenz gegen h:
Jeder Lag j traegt den Randfaktor $1-j/m$. Dann verletzt
ein genuegend grosses Fenster die Positivitaet. Die
ungerade Sinussumme hat symmetrische Extrema und liefert
den Betrag in der Schranke.

## 4. Entscheidender naechster Anschluss

$\nu$ ist **nicht** die native Varianz der Kopfinnovation.
Die Zuordnung einer klassischen Ortsstoerung zu
Dephasierung in einem Zwei-Historien-Vergleich wuerde
einen unabhaengig fixierten Arbeits-, Wirkungs- und
Messvertrag benoetigen. Die Bedingung ist daher noch keine
numerische Aussage ueber den realisierten nativen FIFO.
Sie schliesst aber eine rauschfreie Einsetzung seiner
verzoegerten Antwort in genau dieses Einflussfunktional aus.
Umgekehrt ist eine konsistente positive Referenz moeglich;
sie hat noch keine Lokalitaet, universelle Massenkopplung
oder aus den Knoten abgeleitete Moden.

Entscheidend ist nun, aus **demselben** Kandidatenmedium die
Antwortkoeffizienten und die unabhaengig messbare Sichtbarkeit
bei Rekombination zu bestimmen. Der Test stellt beide
gegen dieselbe Positivitaetsgrenze, statt eine Hoehenphase
und die Dephasierung getrennt anzupassen.

Die [thermische Abtastgegenprobe](fifo_thermal_sampling_2026-11-22.md)
ergaenzt eine staerkere Bedingung: Aufgeloestes Detailgleichgewicht
vertraegt nur farbige Dephasierung fuer die endliche Verzugsantwort.
Weisse abgetastete Daten koennen dennoch durch hochfrequente
Gleichgewichtsbaeder entstehen, die sich zwischen den Proben unterscheiden.

Die [feste Referenzimplementierung](../../experiments/current/reference/fifo_gaussian_influence.py)
und die [Kontrollen](../../tests/test_fifo_gaussian_influence.py)
pruefen das negative Dreipfadbeispiel, die Vakuumrealisierung
an und oberhalb der Grenze und dieselbe Spektralstruktur in
mehreren Fenstern. Keine Parameter- oder Stabilitaetssuche.
