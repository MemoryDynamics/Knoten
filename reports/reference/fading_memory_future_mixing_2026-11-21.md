# Exponentielles Vergessen der kuenftigen FIFO-Inkremente

Stand: 2026-11-21. Analytischer Anschluss an
[Pfadzeichen und FIFO](fifo_spin_path_memory_2026-11-21.md)
und [stetige Invariantengrenzen](fading_memory_limits_2026-11-04.md).
Keine Simulation, Zielauswertung oder neue Wechselwirkungsregel.

**Ergebnis.** Bei festem nichtentartetem Gaussrauschen und
festem exponentiellem Vergessen verliert die *zukuenftige
Schrittfolge* die statistische Abhaengigkeit von beliebigen
Anfangshistorien exponentiell, auch bei unendlichem
Skalar-/Alignment-Gedaechtnis. Die relative Historie besitzt
genau ein stationaeres Gesetz. Das ist keine Mischung des
gesamten unendlichen Speichers in Totalvariation: Sein
deterministisch verschobener Tail bleibt unterscheidbar.
Fuer ein endliches FIFO folgt eine dimensionsfreie
Totalvariationsschranke aus dem Quadratbudget der Altersgewichte.
Bei gleicher Gewichtsnormierung konvergieren feste stationaere
Fenster beim Abschneiden mit der Rate des verworfenen Tails.

## 1. Der relevante Rest nach k gemeinsamen Inkrementen

Wir betrachten gefuellte Historien in inkrementbasierter,
translationsreduzierter Form $h=(v_0,v_{-1},\ldots)$.
Die Ortsdifferenz am Alter j ist die Summe der j juengsten
Inkremente; die Alignment-Richtung am gleichen Alter ist
$p_j=v_{-j}/|v_{-j}|$, mit Nullrichtung beim Nullschritt.
Die bedingte neue Verteilung ist $N(b(h),\varepsilon^2 I_d)$
mit festem $\varepsilon>0$ und unabhaengigen Innovationen.
Der Drift b enthaelt nur die beschraenkte skalare Gausskraft
und den beschraenkten Gauss-Alignment-Kanal. Sei $L_K$ eine
globale Schranke von $|\nabla K|$. Die Vektorgaussfunktion
ist hoechstens eins, die Richtungsnorm ebenfalls.

Sind die k juengsten Inkremente zweier Historien gleich,
stimmen skalare Gaussbeitraege fuer $j\leq k$ und
Vektorbeitraege fuer $j<k$ ueberein. Die aelteste noch
unbestimmte Richtung kann also *einen Eintrag juenger*
sein als der aelteste noch unbestimmte Ort. Mit festen
nichtnegativen Gewichten ist folglich

$$
\tfrac12|b(h)-b(h')|\leq B_k
=|\eta_s|L_K\sum_{j>k} w_{s,j}
 +|\eta_v|\sum_{j\geq k} w_{v,j}.
$$

Bei unendlichen geometrischen Gewichten
$w_{s,j}=(1-s)M_s s^j$, $w_{v,j}=(1-q)M_v q^j$,
$0<s,q<1$, ist $B_k=C_s s^{k+1}+C_v q^k$,
mit $C_s=|\eta_s|L_K M_s$, $C_v=|\eta_v|M_v$.
Fuer endliche Horizonte werden die Summen genau an der
FIFO-Kante abgeschnitten. Mit
$L=\max(H_s-1,H_v)$ ist $B_L=0$ und ein gemeinsamer
L-Block ist der gesamte relative Zustand. Bei beiden
Laengen werden die tatsaechlichen Inkremente gleichgesetzt,
nicht nur Richtungsvektoren oder Feldmesswerte.

Die Totalvariation ($\sup_A |P(A)-Q(A)|$) zweier
gleichkovarianter Gaussgesetze betraegt
$2\Phi(|b(h)-b(h')|/(2\varepsilon))-1$:
Die Halbebene mit der groesseren Dichte trennt nur
entlang der Mittelwertdifferenz. Somit ist die
Ein-Schritt-Abweichung hoechstens

$$
a_k=2\Phi(B_k/\varepsilon)-1<1.
$$

Die Folge $a_k$ faellt und ist im unendlichen Modell
exponentiell summierbar, denn
$a_k\leq\sqrt{2/\pi}\,B_k/\varepsilon$.

## 2. Unendlicher Speicher: Kopplung mit letztem Neustart

Kopple bei zwei laufenden Historien in jedem Update
die bedingten Gaussgesetze maximal. Eine gleichverteilte
Hilfszahl bestimmt das Scheitern der Kopplung mit der
tatsaechlichen Abweichungswahrscheinlichkeit. Im Erfolg
zieht man aus dem gemeinsamen Dichteanteil, andernfalls
aus den beiden Restdichten. Das ist ein Beweiswerkzeug,
kein veraendertes Rauschen in einer Einzelbahn.

Konstruiere mit denselben Hilfszahlen eine Hilfskette
$J_0=0$: Von j springt sie mit Wahrscheinlichkeit
$a_j$ auf null, sonst auf $j+1$. Weil $a_j$ monoton
faellt, ist die Zahl der zuletzt exakt gemeinsamen
inkrementellen Schritte stets mindestens J. Ohne Neustart
der Hilfskette an einem Update kann also auch die
echte Kopplung nicht an diesem Update scheitern.

Aus einem Neustart heraus ist die Wahrscheinlichkeit
keines weiteren Neustarts
$p_\infty=\prod_{j\geq0}(1-a_j)>0$. Die Fehlerlaenge
eines einzelnen Anlaufs hat die defekte Verteilung

$$
r_\ell=a_{\ell-1}\prod_{j=0}^{\ell-2}(1-a_j),
\quad\ell\geq1,\qquad \sum_\ell r_\ell=1-p_\infty .
$$

Wegen $r_\ell\leq a_{\ell-1}$ gibt es ein $t>1$ mit
$R(t)=\sum_{\ell\geq1} r_\ell t^\ell<1$.
Der Zeitpunkt T des letzten Neustarts (null falls
keiner) hat durch Erneuerung das Exponentialmoment
$E[t^T]=p_\infty/(1-R(t))$. Beim Ereignis $T<n$
sind alle Inkremente ab Zeitpunkt n gemeinsam. Also gilt
fuer beliebige Startgeschichten h,h'

$$
\left\|\mathcal L_h(v_n,v_{n+1},\ldots)
-\mathcal L_{h'}(v_n,v_{n+1},\ldots)\right\|_{\rm TV}
\leq\frac{p_\infty}{1-R(t)}t^{-n}.
$$

Die gemeinsam gezogene Zukunft und die unendliche
gesamte Historie darf man nicht verwechseln. Nach n
Schritten bleibt jedes alte Inkrement deterministisch
am entsprechend um n verschobenen Altersindex. Zwei
verschiedene deterministische Starts haben dort auch
dann disjunkte volle Zustandsgesetze, wenn ihre
zukuenftigen Schrittfolgen fast vollstaendig koppeln.

## 3. Existenz und Eindeutigkeit relativer Stationaritaet

Fixiere eine Fensterbreite k. Vergleiche das k-Fenster
am Zeitpunkt n ab festem Start mit demjenigen am
Zeitpunkt $n+m$: Der zweite Prozess hat am Zeitpunkt m
irgendeine zufaellige Historie, und die Zukunftsschranke
ist uniform auch ueber diese. Daher sind die
k-Fenstergesetze in Totalvariation Cauchy, mit Abstand
hoechstens der obigen Schranke bei $n-k+1$. Die Limits
sind konsistent und bestimmen durch den Erweiterungssatz
ein Gesetz $\pi$ auf der unendlichen relativen Historie.

Sei f eine beschraenkte Zylinderfunktion, die nur die
k juengsten Inkremente liest. Fuer $\ell\geq k$ kann man
in P f alle Alterskoordinaten jenseits der juengsten
$\ell$ durch eine feste Geschichte ersetzen. Der
gleichmaessige Fehler ist hoechstens
$\operatorname{osc}(f)a_\ell$ durch die
Ein-Schritt-Schranke. Zuerst kann man bei festem
$\ell$ den Fenstergesetz-Grenzwert verwenden und dann
$\ell$ gegen unendlich schicken. Damit
$\int P f\,d\pi=\int f\,d\pi$, also $\pi P=\pi$.
Jedes andere stationaere Gesetz muesste dieselben
Fensterlimits haben und ist deshalb gleich $\pi$.
Dieser Beweis benoetigt keine Stetigkeit der normierten
Schrittrichtung am Nullschritt. Bei isotropem Rauschen
und radialen Kerneln ist $\pi$ O(d)-invariant, weil
eine globale Orthogonaltransformation ein weiteres
stationaeres Gesetz liefern wuerde.

## 4. Ein endlicher FIFO-Block: Quadratbudget statt Produkt

Eine staerkere endliche Schranke folgt aus der
Gaussstruktur. Vergleiche zwei Anfangshistorien entlang
ein und desselben vorgeschlagenen Ausgabe-Praefixes
von Laenge k. Die beiden naechsten Mittelwerte
$m_\pm$ haben Abstand hoechstens $2B_k$. Setze
$m=(m_++m_-)/2$, $u=(m_+-m_-)/(2B_k)$ bei
$B_k>0$ und $u=0$ sonst. Beide Folgeverteilungen
entstehen aus demselben bedingt definierten Kanal:

$$
Y_k=m+\varepsilon\left[u X_k +(I-uu^T)^{1/2}Z_k\right],
\qquad X_k\sim N(\pm B_k/\varepsilon,1),\qquad
Z_k\sim N(0,I_d).
$$

Die Mittelwerte stimmen, und die beiden
Kovarianzbeitraege addieren sich zu $\varepsilon^2 I_d$.
Der Kanal berechnet m,u aus bereits **ausgegebenem**
Praefix unter beiden Startannahmen, nicht aus dem
versteckten Vorzeichen. Frische unabhhaengige
skalare $X_k$ und unabhaengige $Z_k$ erlauben genau
diese schrittweise Nachbearbeitung. Daher ist die
Totalvariation des gesamten ausgegebenen Blocks
hoechstens die der unabhaengigen skalaren Gaussdaten,
also

$$
\sup_{h,h'}\|P^L(h,\cdot)-P^L(h',\cdot)\|_{\rm TV}
\leq 1-2\Phi\!\left(-\frac{(\sum_{k=0}^{L-1} B_k^2)^{1/2}}
{\varepsilon}\right).
$$

Eine Umkehr der Altersreihenfolge aendert die Distanz
nicht. Der so bestimmte Dobrushin-Faktor ist strikt
kleiner als eins und kontrahiert Blockgesetze,
also auch gegen ihr eindeutiges stationaeres Gesetz.
Fuer die geometrische Obergrenze bleibt das
Quadratbudget bei wachsendem Horizont beschraenkt:

$$
\sum_{k\geq0}(C_s s^{k+1}+C_v q^k)^2
=\frac{C_s^2 s^2}{1-s^2}
+\frac{2 C_s C_v s}{1-sq}+\frac{C_v^2}{1-q^2}.
$$

Dies verbessert die Struktur des frueheren
[skalaren Minorisierungsvergleichs](../../paper/paper_i/research/finite_memory_stationarity_2026-10-21.md):
kein Faktor aus der Ortsdimension und keine identische
Maximalschranke fuer bereits gemeinsam geschriebene
Altersanteile. Ein fester Block dauert aber weiterhin
L Updates; die Blockrechnung allein liefert keine
gleichmaessige Zeitskala bei $L\to\infty$.

## 5. Was die Trunkierung in stationaeren Fenstern kostet

Sei $P_H$ derselbe Uebergang, nur mit ab Alter $H_s$
bzw. $H_v$ abgeschnittenen Gewichten, **ohne**
Nachnormierung. Wir koennen $P_H$ auf der unendlichen
Inkrementhistorie schreiben, indem er ihre fernen
Eintraege ignoriert. Die Kopplungs- und Existenzbeweise
gelten auch hier mit der unendlichen Altersgrenze als
gemeinsamer Obergrenze. Nenne das stationaere Gesetz
$\pi_H$ und das des untrunkierten Modells $\pi_\infty$.

Am gleichen Start unterscheiden sich die Driftmittel
durch hoechstens $D_H=C_s s^{H_s}+C_v q^{H_v}$.
Deshalb ist die Ein-Schritt-Totalvariation der beiden
Kerne am gleichen Zustand hoechstens
$\delta_H=2\Phi(D_H/(2\varepsilon))-1$.
Die alten Inkremente werden in beiden Faellen gleich
verschoben. Fuer eine beschraenkte k-Zylinderfunktion f
gibt Stationaritaet unter $P_H$ die Teleskopreihe

$$
(\pi_H-\pi_\infty)f
=\sum_{j=0}^{\infty}\pi_H(P_H-P_\infty)P_\infty^j f.
$$

Schreibe $K_0=p_\infty/(1-R(t))$. Der Oszillationspreis
des j-ten Summanden ist fuer $j<k$ hoechstens
$\operatorname{osc}(f)$ und fuer $j\geq k$ hoechstens
$\operatorname{osc}(f)K_0 t^{-(j-k+1)}$ durch die
Zukunftskopplung. Dieselbe Schranke rechtfertigt den
Grenzterm der Teleskopreihe. Damit gilt fuer die
stationaeren Gesetze der k juengsten Inkremente

$$
\|\pi_H^{(k)}-\pi_\infty^{(k)}\|_{\rm TV}
\leq\delta_H\left(k+\frac{K_0}{t-1}\right).
$$

Das ist eine feste-Fenster-Aussage bei festem
Rauschen und Retentionen. Sie sagt nichts ueber
ungleichmaessige Rauschgrenzwerte oder zeitintegrierte
Transportgroessen aus.

## 6. Reichweite, Literatur und Gegenproben

Das Statement betrifft nur festes $\varepsilon>0$
und festes exponentielles Vergessen. Die Konstanten
koennen extrem unguenstig sein; daraus folgt keine
praktisch kurze Lebensdauer eines metastabilen Knotens.
Die absolute Ortskoordinate wurde abgezogen. Kein
Diffusionskoeffizient, kein physikalischer Phasenport,
keine Quantenstatistik und kein Limes fuer verschwindendes
Rauschen sind damit abgeleitet. Unterschiede im
unendlich alten Tail werden nicht als unterscheidbare
stationaere Bewegungssektoren ausgewiesen.

[Bressaud, Fernandez und Galves (1999)](https://arxiv.org/abs/math/9806132)
benutzen fuer endliche Alphabete dieselbe Art von
Ruecksetzkopplung bei Ketten mit kompletter Vorgeschichte.
Die hier verwendete Gauss-Ueberlappung, Altersgrenze
und Existenzkonstruktion spezifizieren die Uebertragung
auf die unbeschraenkten reellen Inkremente des Modells.
Der Vergleich mit skalaren Gaussdaten in Abschnitt 4
entspricht dem Prinzip der [Gauss-Komposition von Dong,
Roth und Su](https://doi.org/10.1111/rssb.12454).
Es wird kein Datenschutzresultat beansprucht; der
gemeinsame Kanal ist explizit angegeben.

Die [acht festen Kontrollen](../../tests/test_fading_memory_future_mixing.py)
pruefen die Alterskanten gegen native Kraftbausteine
an Nicht-Orbits, das Gauss-Quadratbudget und eine
formal auswertbare Neustartverteilung. Es wird kein
verrauschter Ziellauf und keine Stichprobe zur Mischung
verwendet. Die Gesetze folgen aus den Beweisen.
59 Tests im betroffenen Panel bestehen.
