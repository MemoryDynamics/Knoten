# Stationaere Antwort und Diffusion am additiven Memory-Kopf

Stand: 2026-11-22. Anschluss an
[Zukunftskopplung](fading_memory_future_mixing_2026-11-21.md) und
[diffusiven Langzeittransport](fading_memory_diffusive_transport_2026-11-21.md).
Keine native Zielbahn, Parameteranpassung oder neue physikalische Regel.

**Ergebnis.** Ein kleiner konstanter additiver Kopfinput
hat in der beschraenkten Skalar-/Alignment-Regel eine
wohldefinierte stationaere lineare Antwort, auch bei
unendlicher geometrischer Memory. Die Antwort ist eine
Korrelation mit der frischen Gauss-Innovation, nicht
mit dem ganzen Inkrement. Deshalb folgt aus der
Brownschen Langzeitgrenze keine Einstein-Proportionalitaet
mit der Kalibrierung des freien Laufs. Die Gleichheit
scheitert bereits bei schwach attraktivem nativem
Zwei-Orte-Skalar-FIFO. Der Input bleibt ein deklarierter
Kopfversatz und keine hergeleitete physikalische Kraft.

## 1. Von der angetriebenen Stationaritaet zur Antwort

Schreibe $h=(v_0,v_{-1},\ldots)$ fuer die relative
Inkrementhistorie und $P_u$ fuer den Uebergang mit
konstantem Input $u\in\mathbb R^d$:

$$
v_1=b(h)+u+Z_1,\qquad Z_1=\varepsilon\xi_1,
\qquad \xi_1\sim N(0,I_d).
$$

Alle Gains und Altersgewichte bleiben fest.
Wir betrachten $\varepsilon>0$, feste geometrische
Retentionen und beschraenkte Gauss-Kraefte. Fuer
endliches Memory wird die irrelevante Vergangenheit
fuer den Vergleich auf derselben Historie mitgefuehrt.
Der gemeinsame Input verschwindet aus allen
Mittelwertdifferenzen in der Zukunftskopplung.
Damit existiert fuer jedes feste u ein eindeutiges
stationaeres Gesetz $\pi_u$ mit denselben
Kopplungskonstanten wie ungezwungen. Die mittlere
Verschiebung pro Update ist

$$
w(u)=u+\pi_u b .
$$

Im radialen, isotropen Basismodell ist $w(0)=0$.
Sei $g=\sum_{n\geq0}P_0^n b$ der beschraenkte
Poisson-Korrektor des ungetriebenen Transports;
$g-P_0g=b$. Weil $\pi_u g=\pi_u P_u g$, gilt **exakt**

$$
w(u)=u+\pi_u(P_u-P_0)g .
$$

Man muss daher keine Dichte der ganzen unendlichen
Historie nach u ableiten. Bei festem alten h hat
nur der neue Schreibort eine verschobene Gaussdichte.
Ihre Ableitung und die integrable zweite Richtungsableitung
liefern gleichmaessig in h

$$
(P_u-P_0)g(h)=J(h)u+O(\|g\|_\infty |u|^2/\varepsilon^2),
\qquad J(h)=\varepsilon^{-2}E_0[g(H_1)Z_1^T\mid H_0=h] .
$$

Das ist Differenzieren der Eingangsdichte, nicht des
moeglicherweise nur messbaren Korrektors.

### Warum Stationaritaet und Ableitung zusammenpassen

Sei $V_k(f)$ die maximale Differenz von f auf Historien
mit k identischen juengsten Inkrementen, und
$\beta=\max(s,q)<1$. Aus der Altersgrenze gilt
$V_k(b)\leq 2B_k=O(\beta^k)$.
Zwei solche Historien lassen sich fuer n weitere Writes
maximal koppeln. Die Wahrscheinlichkeit mindestens einer
Fehlkopplung ist hoechstens $\sum_{i=k}^{k+n-1}a_i$:
Solange alle Writes passen, nimmt die gemeinsame
Fensterlaenge um eins zu. Damit

$$
V_k(P_0^n b)
\leq 2B_{k+n}+2B_0\sum_{i=k}^{k+n-1}a_i=O(\beta^k)
$$

gleichmaessig in n. Unabhaengig davon faellt
$\|P_0^n b\|_\infty$ exponentiell in n.
Aufspalten der Korrektorsumme bei einem Index
proportional zu k ergibt
$V_k(g)=O((k+1)\beta^k)$.
In J kann man bei gleicher neuer Position v die
Korrektoren nach dem Shift mit $V_{k+1}(g)$ vergleichen.
Der $L^1$-Abstand der verschobenen
Gauss-Dichteableitungen ist von Ordnung
$|b(h)-b(h')|/\varepsilon^2$. Somit ist
$V_k(J)=O((k+1)\beta^k)$.

Die Ein-Schritt-Totalvariation von $P_u$ gegen $P_0$
bei gleichem h ist $\delta_u=2\Phi(|u|/(2\varepsilon))-1$.
Die [stationaere Fenster-Teleskopreihe](fading_memory_future_mixing_2026-11-21.md)
gibt deshalb $\|\pi_u^{(k)}-\pi_0^{(k)}\|_{\rm TV}
\leq\delta_u(k+C_0)$ bei festem $C_0$.
Approximiere J durch Ablesen der juengsten k
Inkremente und eine feste Ersatzvergangenheit.
Fuer $\beta^k\leq |u|/\varepsilon$ und kleinstes
solches k ergibt das
$\pi_u J=\pi_0J+O(|u|[1+\log(\varepsilon/|u|)])$
bei festen $\varepsilon,s,q$ und Gains.
Also

$$
w(u)=\Lambda u+O\bigl(|u|^2[1+\log(\varepsilon/|u|)]\bigr),
\qquad \Lambda=I+\pi_0J .
$$

Die gleiche Symmetrie, die $w(0)=0$ ergibt, liefert
$w(Ou)=Ow(u)$ und daher $\Lambda=\lambda I$.
Skalaritaet entscheidet weder Vorzeichen noch Betrag.

## 2. Innovationsantwort ist nicht Schrittkorrelation

Mit der Martingaldifferenz des freien Langzeitbeweises,
$m_1=Z_1+g(H_1)-P_0g(H_0)$, folgt

$$
\varepsilon^2\Lambda=E_0[m_1Z_1^T]
=\varepsilon^2 I+\sum_{j\geq1}E_0[v_{1+j} Z_1^T].
$$

Hier und unten bezeichnet $E_0$ die ungetriebene
stationaere Erwartung. Die letzte Gleichheit folgt
aus der Korrektorsumme und Bedingen auf $H_1$.
Die Summe ist wegen des exponentiellen
Abfalls von $P_0^n b$ absolut konvergent.
Der physikalisch unkalibrierte diffusive
Kovarianzfaktor je Update ist dagegen
$A=E_0[m_1m_1^T]$, nicht die Kreuzkovarianz.
Beide Groessen genuegen der exakten Schranke

$$
A-\varepsilon^2\Lambda\Lambda^T
=E_0[(m_1-\Lambda Z_1)(m_1-\Lambda Z_1)^T]\succeq0 .
$$

Die rechte Seite misst den Teil der effektiven
Inkremente, der nicht linear von der frischen
Innovation erfasst wird. Eine Gleichheit hier
wuerde $m_1=\Lambda Z_1$ fast sicher verlangen.
Weil $m_1-Z_1$ beschraenkt und $Z_1$ vollrangig
und unbeschraenkt ist, muss dann $\Lambda=I$ sein.
Dies ist keine Aussage, dass jeder Korrektor in
diesem Gleichheitsfall konstant waere.

Im freien Modell gilt $A=\varepsilon^2 I$ und
$\Lambda=I$. Eine daran kalibrierte Einstein-Analogie
bei unveraendertem Rauschpegel waere
$A=\varepsilon^2\Lambda$ (aequivalent
$D=(\varepsilon^2/2)\Lambda$ bei $D=A/2$).
Sie ist von der bewiesenen Schranke verschieden
und keine Konsequenz der Symmetrie oder des
Brownschen Langzeitgrenzsatzes.

## 3. Natives attraktives Gegenbeispiel ohne Ziellauf

Nimm im skalaren Kanal nur einen aktiven alten Ort,
$H_s=2$, Delta-Deposition, einen attraktiven
Gaussanteil der Breite $\sigma$ und keinen
Vektorlauf. Durch Zusammenfassen von Gewicht,
Gain und Gaussamplitude schreibt sich der native
Kopf in der relativen Koordinate v exakt als
$b_a(v)=a f(v)$, mit

$$
f(v)=-v e^{-|v|^2/(2\sigma^2)},\qquad a>0 .
$$

Nun vergleiche analytisch bei kleinem a und **festem**
$\varepsilon$. Keine Versuchswerte werden eingesetzt.
Die bedingten Gaussmittelwerte unterscheiden sich
gleichmaessig nur um $O(a)$, sodass der Dobrushin-Faktor
des Ein-Schritt-Kerns $O(a)$ ist. Das stationaere
Inkrementgesetz ist in Totalvariation um $O(a)$
vom freien $N(0,\varepsilon^2 I)$ entfernt.
Wegen Ungeradheit hat f stationaeren Mittelwert null,
und die Poisson-Reihe gibt $g_a=af+O(a^2)$
gleichmaessig. Fuer $Z\sim N(0,\varepsilon^2 I)$ sei

$$
K=E[f(Z)Z^T]
=-\varepsilon^2(1+\varepsilon^2/\sigma^2)^{-(d/2+1)}I .
$$

Im Diffusionsterm ist $\Gamma_0=\varepsilon^2 I+O(a^2)$
durch bedingtes Zentrieren, $\Gamma_1=aK+O(a^2)$,
und die Summe aller hoeheren Lags $O(a^2)$
durch die Dobrushin-Schranke. Im Antwortterm
ist $E[g_a(v_1)Z_1^T]=aK+O(a^2)$, weil
f global Lipschitz ist und der alte Drift $O(a)$
bleibt. Damit

$$
A_a=\varepsilon^2 I+2aK+O(a^2),\qquad
\varepsilon^2\Lambda_a=\varepsilon^2 I+aK+O(a^2),
\qquad A_a-\varepsilon^2\Lambda_a=aK+O(a^2) .
$$

K ist strikt negativ definit. Also scheitert die
frei kalibrierte Proportionalitaet fuer hinreichend
kleine positive a im nativen Modell. Das ist
kein Schluss ueber den offenen Vierzyklus,
andere Eingangsports, eine moegliche andere
Temperaturkalibrierung oder eine physikalische
Fluktuations-Dissipations-Beziehung.

Dieser Inkrementprozess erfuellt auch keine detaillierte
Balance. Sei $p(w\mid v)$ seine bedingte Gaussdichte.
Fuer den Zyklus $0\to y\to z\to0$ gegen seinen
Rueckweg kuerzen sich die quadratischen Terme:

$$
\log\frac{p(y\mid0)p(z\mid y)p(0\mid z)}
{p(z\mid0)p(y\mid z)p(0\mid y)}
=\varepsilon^{-2}[z^Tb_a(y)-y^Tb_a(z)] .
$$

Fuer kollineare y,z mit verschiedenen positiven
Laengen ist dies bei $a>0$ ungleich null. Detaillierte
Balance wuerde das Verhaeltnis wegen Teleskopieren
der stationaeren Dichten zu eins machen. Die Dichte
ist eine positive glatte Gaussmischung, daher kann
eine Balance fast ueberall nicht durch Ausnehmen
dieser Punkte gerettet werden. Wegen gemeinsamer
Vorzeichensymmetrie gilt dieselbe Gegenprobe auch
fuer Zeitumkehr mit Negieren der Inkremente.
Das betrifft nur diesen stationaeren Prozess,
nicht thermodynamische Entropieproduktion oder
einen physikalischen Kraftport.

Der [breite Paargrenzfall](memory_pair_diffusive_limit_2026-11-22.md)
verwendet anschliessend die getrennten Koeffizienten fuer
den deklarierten direkten Gauss-Kreuzkanal. Er zeigt,
wann ein driftfreier Mittelpunkt trotzdem mit dem
Relativrauschen korreliert bleibt.

## 4. Einordnung und feste Gegenproben

[Warren und Allen, PRL 109, 250601 (2012)](https://doi.org/10.1103/PhysRevLett.109.250601)
verwenden die Ableitung der Pfadwahrscheinlichkeit
fuer Antwortkoeffizienten in Brownscher Dynamik.
[Maes, Safaverdi, Visco und van Wijland](https://arxiv.org/abs/1211.2181)
zeigen Sutherland-Einstein-Korrekturen fuer
kontinuierliche Nichtgleichgewichts-Diffusionen mit
Memory. Hier werden weder deren Rausch-/Reibungsvertrag
noch eine mechanische Kraft uebernommen.
Neue Punkte hier sind die stationaere Rechtfertigung
am diskreten Altersfilter und der explizite native
Gauss-Gegenfall zur freien Kalibrierung.

Die [sieben neuen festen Kontrollen](../../tests/test_fading_memory_diffusive_transport.py)
vergleichen Response und Innovationskorrelation
in exakt loesbarem Vorzeichenfeedback. Zusaetzliche
Gauss-Quadraturen pruefen die schwache native
Korrektur; ein Dichteprodukt prueft die Zyklusbilanz.
72 Tests im betroffenen Panel bestehen. Keine Bahn
oder eigenstaendige Stabilitaetsauswertung.
