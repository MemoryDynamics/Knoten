# Kritischer FIFO: Fluktuationen und nichtlineare Grenze

Stand: 2026-11-21. Fortsetzung der
[statischen Fernantwort im Mittelfeld](collective_fifo_screening_2026-11-21.md).
Keine neue Produktionsregel, kein Vielteilchen-Ziellauf und keine
Auswertung der offenen Vierzyklus-Stabilitaet.

**Ergebnis.** Die Gaussinnovationen erregen lange Dichtewellen mit
Varianz der Ordnung $k^2/N$ pro Schritt. Am kritischen Punkt sinkt
ihre lineare Relaxationsrate aber wie $k^4$. Der lineare stationaere
Vergleich liefert deshalb Fluktuationen von der Ordnung $1/(Nk^2)$.
Der aus demselben Update hergeleitete nichtlineare Zweitharmonische
Term verstaerkt den Test: Bei typischer linearer Amplitude waechst
sein relatives Gewicht in einer 3D-Box bei fester Teilchendichte
wie $L^{3/2}$. Die lineare $1/r$-Antwort allein kontrolliert somit
ihre eigene Grossskalenfortsetzung nicht. Das ist ein konkret
berechneter Stoerungsindikator, kein Beweis eines Phasenuebergangs
oder des Verschwindens der Fernantwort.

## 1. Exakte bedingte Innovation

Betrachte auf dem d-dimensionalen Torus der Kantenlaenge L die
bereits deklarierte [additive N-Verallgemeinerung](collective_memory_stability_2026-11-07.md),
hier mit gleicher Teilchenmasse $\rho_0L^d/N$ und unabhaengigen
Gausskicks. Die bedingt auf die gesamte
FIFO-Vergangenheit bekannten driftverschobenen Koepfe seien Y_j.
Darauf folgen unabhaengige Gausskicks mit Varianz $2d_0 I$.
Alle Aussagen dieses Abschnitts gelten sogar fuer beliebige
solche vorhersagbaren Y_j. Es ist keine Produktannahme ueber ihre
gemeinsame Vergangenheit noetig.

Fuer die erlaubten Wellenvektoren definiere den relativen Dichtemodus
$u_{n+1}(k)=N^{-1}\sum_j e^{-i k\cdot X_{j,n+1}}$, den analogen
Modus $\widetilde u_n$ der Y_j und $p_k=e^{-d_0|k|^2}$. Wrapping
veraendert diese Exponentialfaktoren nicht. Subtrahiere den bedingten
Mittelwert und schreibe $\zeta_{n+1}(k)=u_{n+1}(k)-p_k\widetilde u_n(k)$.
Fuer die ganze Vergangenheit $\mathcal F_n$ ergibt sich

$$
\begin{aligned}
\mathbb E[\zeta_{n+1}(k)\mid\mathcal F_n]&=0,\\
\mathbb E[\zeta_{n+1}(k)\overline{\zeta_{n+1}(l)}\mid\mathcal F_n]
&=\frac{p_{k-l}-p_kp_l}{N}\widetilde u_n(k-l).
\end{aligned}
$$

Beweis: Kreuzterme verschiedener Teilchen verschwinden nach
Zentrierung wegen der bedingten Unabhaengigkeit; beim selben
Teilchen liefert die charakteristische Funktion den Faktor
$p_{k-l}$. Insbesondere gilt **exakt**
$\mathbb E[|\zeta_{n+1}(k)|^2\mid\mathcal F_n]=(1-p_k^2)/N$.
Der Nullmodus ist rauschfrei. Innovationsschritte sind
zeitlich unkorreliert, aber weder unabhaengige Moden noch
Gaussinnovationen fuer die empirische Dichte werden angenommen.

## 2. Was die lineare Rauschrechnung leistet

Ersetze nur den bedingten Drift durch den **linearen** History-Block
$C_k$ des kritischen Dichtevergleichs und behalte die obige diagonale
Innovationsvarianz. Die daraus berechnete stationaere zweite
Momentenbilanz ist eine Referenz, kein Stationaritaetsbeweis fuer
die nichtlineare N-Regel. Bei jeder Nichtnullwelle ist $C_k$ Schur-stabil.
Fuer den ersten Einheitsvektor $e_0$ gilt daher in dieser Referenz

$$
V_k=\frac{1-p_k^2}{N}\sum_{m\ge0}|e_0^T C_k^m e_0|^2.
$$

Bei festem H ist der langsame Eigenwert $r_k=1-D_4|k|^4+O(|k|^6)$
separiert, wobei $D_4=d_0a+d_0^2/2$ und a der Gaussbreitenparameter
des Kernels ist. Der zugehoerige Projektor liefert im Kopfeingang
und Kopfausgang den Faktor $1+O(|k|^2)$: Bei k=0 ist jeder
Kopfeintrag nach einem Impuls konstant. Alle anderen Eigenwerte
gehen gegen null. Auf dem komplementaeren invarianten Raum gibt
es fuer kleine k eine uniforme geometrische Potenzschranke, etwa
durch einen festen Resolventenkreis um null mit Radius kleiner eins.
Die Impulssumme besitzt somit den fuehrenden Term
$[1+O(|k|^2)]/(1-r_k^2)$; die Kreuz- und Restterme sind beschraenkt.
Mit $1-p_k^2=2d_0|k|^2+O(|k|^4)$ folgt

$$
V_k=\frac{d_0}{N D_4|k|^2}[1+O(|k|^2)].
$$

Das Ergebnis verlangt den stationaeren linearen Grenzwert zuerst
bei festem k und ist fuehrend auch fuer H=1 dasselbe. In 3D bei
festem $N/L^3$ geht die Varianz der kleinsten Nichtnullwelle sogar
wie $L^{-1}$ gegen null. Die absolute Varianz allein liefert also
**keinen** Zusammenbruchsbefund. Entscheidend ist ihr Verhaeltnis
zum Amplitudenbereich, in dem der lineare Drift dominiert.

## 3. Nichtlinearer Vergleich aus dem selben Pushforward

Setze k=|k|>0 in den folgenden skalaren Formeln und waehle entlang
dieser Raumrichtung eine reelle Grundwelle $\alpha_n\cos\theta$
mit $\theta=\mathbf k\cdot x$. Es wird die relative Dichte
$(\rho-\rho_0)/\rho_0$ expandiert, d.h. der Fourierkoeffizient
der reellen Welle ist $\alpha_n/2$. Waehle die lineare, freie
Historie $\alpha_{n-a}=r_k^{-a}\alpha_n$, ohne externen Treiber.
Ihre Phase aendert sich im Kopftransport um
$-c_k\alpha_n\sin\theta$, wobei am kritischen Punkt

$$
c_k=d_0 k^2e^{-a k^2}P(r_k)=r_k/p_k-1=d_0k^2+O(k^4).
$$

Bei zunaechst ausgeschalteter zweiter Harmonischer lautet ihr
tatsaechlicher nach dem Pushforward und dem Gausskick erzeugter
Cosinuskoeffizient

$$
2p_{2k}\left\langle(1+\alpha_n\cos\theta)
\cos(2\theta-2c_k\alpha_n\sin\theta)\right\rangle_\theta
=p_{2k}(c_k+c_k^2)\alpha_n^2+O(\alpha_n^4).
$$

Die beiden Summanden stammen getrennt von Dichte mal Verschiebung
und von der quadratischen Verschiebung. Dies ist eine lokale
Taylorrechnung mit k fest; der Rest ist kein globaler Fehlerbeweis.
Ist eine zweite Harmonische bereits von Ordnung $\alpha^2$
vorhanden, kommt auf dieser Ordnung ihre eigene lineare FIFO-Antwort
hinzu. Die beiden Seiten mischen sich nicht linear.

Fuer den **getriebenen Anteil** der Zweitharmonischen ansatzweise
$\beta_n=B_k\alpha_n^2$ ist das Zeitverhaeltnis $r_k^2$, nicht 1.
Der genaue Koeffizient der zweiten Ordnung ist

$$
B_k=\frac{p_{2k}(c_k+c_k^2)}{
r_k^2-p_{2k}[1+4d_0k^2e^{-4ak^2}P(r_k^2)]}
=\frac{d_0}{14 D_4 k^2}[1+O(k^2)].
$$

Der Nenner folgt direkt aus der vollen Rekursion der zweiten
Harmonischen. Zur fuehrenden Ordnung geht der 2k-Block wie
$1-16 D_4 k^4$ zurueck, waehrend $r_k^2=1-2D_4 k^4$.
Das ergibt den Faktor 14; ein statischer Nenner haette 16.
Zusaetzliche homogene Transienten sind dabei nicht mitgezaehlt.
Die Rechnung behauptet keinen invariant reduzierten Attraktor
und keine stationaere Verteilung fuer die zweite Harmonische.

## 4. Entscheidung fuer den Fernfeldpfad

Die reelle Amplitude einer einzelnen zufaelligen Mode ist betragsmaessig
$2|u_k|$. Setzt man als **Vergleichsgroesse** die lineare RMS-Amplitude
$2\sqrt{V_k}$ in die obige deterministische Umwandlung ein, ist der
relative Zweitharmonische Beitrag asymptotisch

$$
|B_k|\,2\sqrt{V_k}\sim
\frac{d_0}{7D_4}\sqrt{\frac{d_0}{D_4}}\;\frac{1}{\sqrt N k^3}.
$$

Fuer $k=2\pi/L$, festes $H$ und feste Parameter, sowie $N/L^d$ konstant
skaliert der Indikator wie $L^{3-d/2}$, in 3D also wie $L^{3/2}$.
Kleine absolute Dichteabweichung und gleichzeitig schlecht
geordnete Stoerungsreihe sind moeglich. **Ein grosser Wert ist
keine Vorhersage des nichtlinearen Resultats:** Der Vergleich setzt
ein kohaerentes Abklingen der Grundwelle an; in der verrauschten
N-Dynamik sind Phasen und Modenkopplungen zufaellig. Hohe Moden,
Rueckwirkung auf die Grundwelle und der gemeinsame Zeit-/Groessen-
Grenzwert wurden nicht kontrolliert. Es wird auch keine universelle
kritische Dimension oder Renormierungsgruppe daraus behauptet.

**Gegenprobe mit zufaelliger Phase.** Im expliziten H=1-Vergleich
ersetze die Grundwelle durch einen stationaeren zirkulaeren komplexen
Gauss-AR(1) mit Faktor $r=r_k$ und Varianz $V=V_k$; das separate
Rauschen der zweiten Harmonischen bleibt ausgeschaltet. Deren getriebener
Fourierkoeffizient erfuellt in diesem einseitigen Vergleich
$v_{n+1}=s v_n+f u_n^2$ mit $s=r_{2k}$ und
$f=2p_{2k}(c_k+c_k^2)$. Der Faktor 2 setzt den Cosinuskoeffizienten
in komplexe Fourierkoeffizienten um. Die Gaussmomentenformel liefert
$\mathbb E[u_n^2\overline{u_{n-j}^2}]=2V^2 r^{2|j|}$. Einsetzen in
die doppelte geometrische Impulssumme ergibt exakt

$$
\mathbb E|v|^2=2 f^2 V^2\,
\frac{1+s r^2}{(1-s^2)(1-s r^2)},\qquad
\frac{\sqrt{\mathbb E|v|^2}}{\sqrt V}
\sim \frac{d_0}{6D_4}\sqrt{\frac{d_0}{D_4}}\frac{1}{\sqrt N k^3}.
$$

Zufaellige Phase aendert hier den Vorfaktor, nicht die Potenz.
Die Rechnung isoliert nur den durch die Grundwelle getriebenen
Anteil, ohne Rueckkopplung, andere Moden oder Nachweis eines
Gauss-Grenzprozesses der nativen kritischen N-Regel.

Damit ist ein naechster diskriminierender Vertrag benannt: Fuer denselben
deklarierten Massenskalierungs- und Zeitgrenzgang die tatsaechliche
nichtlineare Dichteantwort und die zweite Harmonische gegen diese
lineare Referenz kontrollieren, bevor der statische Pol als robuste
Fernwirkung verwendet wird. Der r^-1-Befund bleibt eine Mittelfeld-
Referenz; er schliesst die Bruecke zu Gravitation und Quantentheorie
nicht. Keine Freigabe eines neuen Vielteilchenlaufs.

## 5. Literatur und Gegenkontrollen

- [Dean, J. Phys. A 29, L613 (1996)](https://arxiv.org/pdf/cond-mat/9611104),
  Gl. (17)-(19): exaktes, konserviertes Dichterauschen fuer
  kontinuierliche wechselwirkende Langevin-Teilchen. Hier ist die
  direkte diskrete Fourier-Kovarianz abgeleitet, keine solche SPDE als
  Input eingesetzt.
- [Gajendragad und Saha, arXiv:2510.17444v2](https://arxiv.org/html/2510.17444v2),
  mikroskopischer Anschluss und Diskussion: konservierte
  kollektive Dichte mit gedaechtnisabhaengigem Transport ist bekannte
  aktive Materie. Ihr zeitkontinuierlicher verzoegerter
  Cahn-Hilliard-Ansatz mit zusaetzlichen Wechselwirkungen und
  endlicher Wellenzahl-Instabilitaet ist nicht der hiesige diskrete
  attraktive FIFO an seiner Langwellenschwelle.
- [Chavanis, arXiv:0803.0263, Abschnitt 2.1](https://arxiv.org/abs/0803.0263):
  Fluktuationen nahe einer Mittelfeldschwelle koennen eine naive
  Faktorisierung untergraben. Kein Transfer seiner kritischen
  Exponenten; die obigen Faktoren sind aus diesem FIFO berechnet.

Gezielte Primaerquellenpruefung, keine Reproduktion ihrer Numerik.
Die [festen Tests](../../tests/test_collective_fifo_fluctuations.py)
pruefen die bedingte Kovarianz durch Gaussquadratur, das lineare
Zweitmoment mit der vollen Lyapunovgleichung, den quadratischen
Pushforward unabhaengig per Fourierquadratur und den zweiten
Harmonischen samt Unterscheidung zum statischen Nenner. Eine weitere
Lyapunovkontrolle prueft die Gaussmomenten-Gegenprobe. Keine neue
Teilchentrajektorie oder Parametersuche.

Verifikation: 97 Tests im gezielten Panel bestanden, davon 13 neue
Kontrollen. Enthalten sind auch der bisherige Fernfeldvergleich, die
kollektive Stabilitaetsrechnung, das Fernfeldinventar und Markdown-
Formelkontrollen. Keine volle Repository-Suite.
