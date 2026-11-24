# Thermisches Medium, FIFO-Antwort und die Grenze der Zeitabtastung

Stand: 2026-11-22. Fortsetzung des
[Gaussschen Zwei-Bahn-Vergleichs](fifo_gaussian_influence_2026-11-22.md).
Analytische Oszillatorreferenz mit festen Spektralkontrollen,
kein neuer nativer Ziellauf, kein Abgleich durch Nachfit.

**Ergebnis.** Werden alle relevanten Frequenzen eines thermischen
Mediums durch die FIFO-Zeitproben aufgeloest, ist eine nichttriviale
reine FIFO-Verzoegerung mit exakt weisser Dephasierung unvereinbar.
Ein Lag in der kausalen Antwort kann dabei unendlich viele Lags
in der Dephasierung erzwingen. Ohne diese Aufloesungsannahme
gibt es dagegen positive thermische Realisierungen fuer dieselben
weissen FIFO-Daten. Sie unterscheiden sich zwischen den Abtastzeiten.
Die abgetastete Positivitaetsgrenze allein bestimmt also keinen
kontinuierlichen physikalischen Medienkanal.

## 1. Was betrachtet wird

Das diskrete hermitesche Spektrum des vorigen Tests ist
$h(\theta)=\nu(\theta)+s(\theta)$, mit $\nu$ gerade und
$s(\theta)=\sum_{j=1}^{H-1}\gamma_j\sin(j\theta)$.
Hier bezeichnet $\nu(\theta)$ das Spektrum der Dephasierung,
nicht die Varianz nativer Ortsinnovationen. Bei weissem
Rauschen ist $\nu(\theta)=\nu$ konstant.

Fuer die Positivkontrolle koppeln kontrollierte Historien zu
Zeiten $n\Delta$ impulsartig linear an ein stationaeres
hermitesches Badobservable $X(t)$, wobei $\Delta>0$ der
Abtastabstand ist. Sei $u=\omega\Delta$ die dimensionslose
kontinuierliche Frequenz und $b=\beta\hbar/\Delta>0$.
Fuer $B_{nm}=\langle X(m\Delta)X(n\Delta)\rangle$ verwende
die Konvention

$$
B_{nm}=\int_{\mathbb R}e^{i(n-m)u}p(u)\,\frac{du}{2\pi},
\qquad p(-u)=e^{-bu}p(u)\quad(u>0).
$$

Die zweite Gleichung ist thermisches Detailgleichgewicht des
nicht symmetrisierten Spektrums. Fuer einen Oszillator ergibt
es sich aus den Gewichten $1+n_\beta$ und $n_\beta$ der
beiden Frequenzen und damit aus derselben Kopplung, nicht
aus einem separaten Dephasierungsfit. Siehe
[Callen und Welton (1951)](https://doi.org/10.1103/PhysRev.83.34)
und [Feynman und Vernon (1963), Abschnitt IV](https://doi.org/10.1016/0003-4916(63)90068-X).
Der symmetrische Teil von B liefert den Rauschterm;
der Kommutatorteil liefert die kausalen Koeffizienten
$\gamma_j=2\operatorname{Im}B_{n,n-j}$ in der Konvention
des bisherigen Einflussfunktionals. Bei linearen
Oszillatoren ist der Kommutator eine Zahl und die zeitgeordnete
Gausssche Auswertung exakt. Eine etwaige lokale konservative
Phase ist von diesem Spektraltest getrennt.

Die diskreten Daten sehen nur das gefaltete Spektrum
$h(\theta)=\sum_{k\in\mathbb Z}p(\theta+2\pi k)$,
$-\pi<\theta<\pi$. Das folgt direkt aus dem Exponenten
fuer ganzzahlige Zeitabstaende. Verschiedene Kopplungsprofile
oder Abtastmittelungen waeren andere Messvertraege.

## 2. Aufgeloestes Bad: die Fluktuationen sind nicht frei

Hat p nur Stuetzstellen mit $|u|\le\pi$, gibt es fast ueberall
keine Frequenzfaltung. Bei endlicher positiver Temperatur folgt
fuer $0<\theta<\pi$

$$
\frac{h(-\theta)}{h(\theta)}=e^{-b\theta}
\quad\Longrightarrow\quad
\nu(\theta)=s(\theta)\coth(b\theta/2).
$$

Die Gleichung der Spektren gilt auch bei Nullstellen, ohne
Division durch $h(\theta)$. Notwendig ist $s(\theta)\ge0$
auf dem positiven Halbbereich. Bei zwei Verzugskoeffizienten
ist dies genau $\gamma_1\ge2|\gamma_2|$, denn
$s(\theta)=\sin\theta(\gamma_1+2\gamma_2\cos\theta)$.
Das ist keine Aussage ueber ein gefaltetes oder
ausserhalb des Gleichgewichts betriebenes Bad.

Bei endlich vielen Lags verschwindet s gegen $\theta=\pi$.
Die thermisch erforderliche $\nu(\theta)$ verschwindet dort
ebenfalls und kann daher keine positive Konstante sein.
Die Nichtexistenz gilt trotz der moeglichen Positivitaet
des rein diskreten Spektrums. Im Vakuum lautet die aufgeloeste
Bedingung stattdessen $h(-\theta)=0$; ein nichttriviales
$h=\nu+s$ mit konstanter $\nu$ und endlicher Sinussumme
kann ebenfalls nicht auf einem ganzen Halbintervall verschwinden.

**Konstruktive Alternative.** Fuer exakt einen Lag mit
$\gamma_1>0$ nimmt man als Spektrum auf dem positiven Halbband
$p(\theta)=2s(\theta)/(1-e^{-b\theta})$ und ergaenzt den
durch Detailgleichgewicht bestimmten negativen Ast. Das
entspricht einer nichtnegativen Oszillatorkopplung mit
thermischen Gewichten. Der eine Antwortlag bleibt erhalten,
aber das Rauschen ist zeitlich korreliert. Fuer die geraden
Spektralkoeffizienten $N_m=\pi^{-1}\int_0^\pi
\nu(\theta)\cos(m\theta)\,d\theta$ folgt bei $0<b<\infty$

$$
N_m=-\frac{\gamma_1\coth(b\pi/2)}{\pi}
\frac{(-1)^m}{m^2}+o(m^{-2}).
$$

Zweimalige partielle Integration ergibt den Randbeitrag
$[(-1)^m\nu'(\pi)-\nu'(0)]/(\pi m^2)$. Hier ist
$\nu'(0)=0$, $\nu'(\pi)=-\gamma_1\coth(b\pi/2)$ und
der verbleibende Kosinuskoeffizient von $\nu''$ geht gegen
null. Der Schwanz betrifft genau diesen scharf am
Nyquist-Band endenden Referenzkanal, nicht alle moeglichen
thermischen Medien.

## 3. Frequenzfaltung: exakte Alternative und Mindestbandbreite

Sei nun $h_\pm=h(\pm\theta)=\nu\pm s(\theta)$ und
$\nu> s_*:=\max|s|$. Fuer $0<\theta<\pi$ waehle zwei
positive physikalische Frequenzbaender
$u_1=2\pi M+\theta$ und $u_2=2\pi(M+1)-\theta$.
Sie fallen bei der Abtastung auf entgegengesetzte Seiten
des diskreten Spektrums. Mit $q_i=e^{-bu_i}$ setze

$$
p(u_1)=\frac{h_+-q_2h_-}{1-q_1q_2},\qquad
p(u_2)=\frac{h_--q_1h_+}{1-q_1q_2}.
$$

Fuer festes hinreichend grosses M sind beide Gewichte
nichtnegativ, etwa wenn
$e^{-2\pi bM}\le(\nu-s_*)/(\nu+s_*)$.
Setze $p(-u_i)=q_i p(u_i)$ und alle anderen Frequenzen
auf null. Die Faltung liefert dann exakt
$p(u_1)+q_2 p(u_2)=h_+$ und
$p(u_2)+q_1 p(u_1)=h_-$. Ein thermisches lineares
Oszillatorbad kann diese Spektraldichte mit Kopplungsgewicht
$(1-e^{-bu})p(u)$ auf den positiven Baendern tragen.
Hier wird nur der stationaere Gausssche Medienkanal fuer
vorgegebene Historien realisiert, keine native Knotenbahn.
Verschiedene M liefern dieselben Werte an *allen* ganzzahligen
Abstaenden, aber im Allgemeinen andere Zwischenwerte.

Bei einer endlichen physikalischen Grenzfrequenz
$\Omega_{\max}$ ist andererseits fuer jede Falte das
Verhaeltnis gepaarter Spektralbeitraege zwischen
$e^{-\beta\hbar\Omega_{\max}}$ und
$e^{+\beta\hbar\Omega_{\max}}$. Beim Summieren
nichtnegativer Beitraege bleibt diese Schranke erhalten.
Deshalb gilt fuer $s_*>0$ und $\nu>s_*$ notwendig

$$
\Omega_{\max}\ge
\frac{1}{\beta\hbar}\log\frac{\nu+s_*}{\nu-s_*}.
$$

Bei $\nu=s_*$ ist kein endliches $\Omega_{\max}$ moeglich:
Die gefalteten Spektralverhaeltnisse kommen in Umgebungen
der Extrema beliebig nahe an null bzw. werden beliebig gross.
Das betrifft jede endliche positive Temperatur, nicht den
Vakuum-Grenzfall. Die Schranke ist notwendig, die explizite
Zwei-Band-Konstruktion ist eine separate hinreichende
Referenz oberhalb der Positivitaetsgrenze.

## 4. Diskriminator fuer einen physikalischen Anschluss

Zuerst das Abtast-/Kopplungsverfahren festlegen. Ein
aufgeloestes thermisches Medium muss Antwort und
Dephasierung mit fester spektraler Relation erzeugen.
Ein Treffer nur an FIFO-Zeiten kann dagegen ein
hochfrequentes Medium verbergen, das bei einer anderen
Abtastung anders ausfaellt. Vergleich bei zusaetzlichen
Zwischenzeiten oder mit unabhaengig bestimmter Bandbreite
trennt diese Faelle. Erst ein solcher Medienbefund waere
mit dem gemeinsamen [Kraft- und Bahnphasentest](memory_gravity_action_phase_2026-11-22.md)
zu verbinden. Keine thermische Herkunft der nativen
Innovationen, keine lokale Feldtheorie und kein
Gravitations- oder Quantennachweis.

[Feste Kontrollen](../../tests/test_fifo_thermal_sampling.py):
berechnete thermische Korrelationen, zwei gefaltete Baeder
mit identischen FIFO-Koeffizienten und ein Beispiel,
das bei positiver diskreter Matrix am UV-Test scheitert.
