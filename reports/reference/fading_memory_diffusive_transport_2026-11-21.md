# Nichtentarteter diffusiver Langzeittransport mit exponentiellem Memory

Stand: 2026-11-22; begonnen am 2026-11-21. Analytischer Anschluss an die
[Zukunftskopplung](fading_memory_future_mixing_2026-11-21.md).
Keine Zielbahn, Parameterwahl oder Aenderung der Modellregel.

**Ergebnis.** Bei festem positivem Gaussrauschen und
geometrischem Vergessen ist der langzeitlich skalierte
Ort des einzelnen Skalar-/Alignment-Laufers eine
Brownsche Bewegung mit strikt positiver, isotroper
Kovarianz. Das gilt fuer endliche und unendliche
Historien, ohne Klein-Gain- oder Kleinrauschannahme.
Die effektive Kovarianz ist eine konvergente Summe
von Inkrementkorrelationen. Sie konvergiert auch
beim Abschneiden der Altersgewichte ohne Nachnormierung.
Kein Zahlenwert am nativen Zielkandidaten wurde bestimmt.

## 1. Annahmen und ein beschraenkter Korrektor

Verwendet wird derselbe translationsreduzierte
Zustand $H_n=(v_n,v_{n-1},\ldots)$ wie im
[Kopplungsbeweis](fading_memory_future_mixing_2026-11-21.md).
Bei endlicher Memory werden aeltere Koordinaten
nicht gelesen. Sei $P$ der Uebergangsoperator,
$v_{n+1}=b(H_n)+\varepsilon\xi_{n+1}$ und
$x_n-x_0=\sum_{i=1}^n v_i$.
Der Drift ist beschraenkt durch $B_0$ aus der
untrunkierten Altersgrenze des Kopplungsbeweises,
auch fuer die gekuerzten Modelle. Vorausgesetzt
sind radialer Skalar- und Alignment-Kanal,
isotrope unabhaengige Gauss-Innovationen
und kein aeusserer Antrieb. Das eindeutige
stationaere Gesetz $\pi$ ist O(d)-invariant,
also $\pi b=0$ und $E_\pi v_0=0$.

Zur Kontrolle von $P^n b$ sind keine Stetigkeit
am Nullschritt und kein integrierbarer unendlicher
Zustandsabstand noetig. Der Kopplungsbeweis liefert
einen letzten Neustart T mit
$\Pr(T\geq m)\leq K_0 t^{-m}$, $t>1$.
Fuer zwei Anfangshistorien gilt bei $T\leq n-k$:
Die juengsten k Inkremente zum Zeitpunkt n sind
gleich, also unterscheiden sich ihre Driftmittel
hoechstens um $2B_k$. Sonst genuegt $2B_0$.
Vergleich mit einem stationaeren Start ergibt

$$
\sup_h |P^n b(h)|
\leq2 B_k+2 B_0 K_0 t^{-(n-k+1)}
\qquad (0\leq k\leq n).
$$

Mit $k=\lfloor n/2\rfloor$ und
$B_k\leq B_0\max(s,q)^k$ ist diese Schranke
exponentiell summierbar und gleichmaessig
ueber alle Abschneidehorizonte. Folglich existiert
der absolut und gleichmaessig konvergente
Poisson-Korrektor

$$
g(h)=\sum_{n\geq0}P^n b(h),\qquad g-Pg=b .
$$

Schreibe $C=\|g\|_\infty$. Er kann durch
$4 B_0[(1-\max(s,q))^{-1}+K_0/(t-1)]$
fuer die ganze Horizontfamilie abgeschaetzt
werden. Eingesetzt wird der Korrektor nur
im Beweis, nicht im Simulator.

## 2. Brownscher Grenzprozess und positive Kovarianz

Die Differenzen

$$
m_i=v_i+g(H_i)-g(H_{i-1})
=\varepsilon\xi_i+g(H_i)-Pg(H_{i-1})
$$

sind Martingal-Differenzen, und
$x_n-x_0=\sum_{i=1}^n m_i+g(H_0)-g(H_n)$.
Der zweite Term ist fuer jede Bahn durch $2C$
beschraenkt. Unter $\pi$ ist die Inkrementfolge
wegen der gleichmaessigen Zukunftskopplung
ergodisch; Historienobservablen sind Faktoren
dieser Folge. Definiere

$$
A=E_\pi[m_1m_1^T].
$$

Die skalierte vorhersehbare quadratische Variation
des Martingals konvergiert durch das Ergodentheorem
gegen $\tau A$ auf der skalierten Zeitskala $\tau$.
Gauss-Innovationen und beschraenkter Korrektor
geben gleichmaessig beschraenkte bedingte
vierte Momente. Die skalierten maximalen Spruenge
verschwinden dadurch im quadratischen Mittel;
die Spruenge der vorhersehbaren Variation sind
gleichmaessig von Ordnung $1/n$.
Der mehrdimensionale Martingal-Grenzsatz liefert
damit fuer jedes endliche Zeitintervall

$$
n^{-1/2}(x_{\lfloor n\tau\rfloor}-x_0)
\ \,\Longrightarrow\ \ A^{1/2}W_\tau .
$$

Hier ist W die Standard-Brownsche Bewegung in d
Dimensionen. Die Konvergenz gilt auf dem Pfadraum mit
Skorokhod-J1-Topologie. Wegen der stetigen
Grenzbahn kann man auch linear interpolieren.
Aus der alten Kopplung folgt derselbe Grenzprozess
fuer jede Anfangshistorie: Nach der fast sicher
endlichen letzten Fehlkopplung sind die Inkremente
gleich. Der maximale Ortsunterschied zweier so
gekoppelter Pfade ist fast sicher endlich und durch
$\sqrt n$ geteilt vernachlaessigbar.
Ebenso ist $(x_n-x_0)/n\to0$ fast sicher,
durch Ergodizitaet und diese Kopplung. Endliche
gerichtete Transienten sind nicht ausgeschlossen.

**Strikt positive Diffusion.** Fuer jeden Einheitsvektor
e und jeden alten Zustand gilt punktweise
$|e^T m_i|\geq (|\varepsilon e^T\xi_i|-2C)_+$.
Es ist keine Unabhaengigkeit zwischen Innovation
und Korrektursprung erforderlich. Deshalb gilt mit
$Z\sim N(0,1)$

$$
0<E[(|\varepsilon Z|-2C)_+^2]
\leq e^T A e\leq(\varepsilon+2C)^2 .
$$

Die linke Schranke ist positiv wegen des
unbeschraenkten Gauss-Tails. Sie kann quantitativ
sehr schwach sein. Orthogonale Kovarianz des
Uebergangs und von g liefert $A=a I_d$, $a>0$.
In der Konvention $\partial_t p=D\Delta p$ ist
$D=a/2$ pro Update, keine physikalisch kalibrierte
Zeiteinheit. Der lineare mittlere quadratische
Transport folgt auch ohne Grenzsatz direkt aus der
Martingal-Zerlegung: Gleichmaessige bedingte
zweite Momente ergeben $E|x_n-x_0|^2=O(n)$.

## 3. Exakte Korrelationsformel

Unter $\pi$ sei $\Gamma_j=E[v_0v_j^T]$.
Fuer $j\geq1$ gilt
$E[v_j\mid H_0]=P^{j-1}b(H_0)$, daher fallen
die Korrelationen exponentiell und gleichmaessig
in H. Die Normierung wird durch beide Darstellungen
der stationaeren Verschiebung kontrolliert:

$$
A=\lim_{n\to\infty} n^{-1}E_\pi[(x_n-x_0)(x_n-x_0)^T]
=\Gamma_0+\sum_{j\geq1}(\Gamma_j+\Gamma_j^T).
$$

Links verschwinden die Kreuzterme der beschraenkten
Randkorrektur nach Division durch n; rechts
folgt die uebliche Korrelationssumme durch
Stapelung der stationaeren Inkremente.
Auch aus jedem festen Start gilt derselbe
zweite-Moment-Grenzwert: Die Kopplungsdifferenz der
Orte ist in $L^2$ gleichmaessig beschraenkt, denn die
Norm des j-ten Inkrementunterschieds ist wegen
gleichmaessiger vierter Momente und Gleichheit bei
$T<j$ hoechstens eine Konstante mal
$\Pr(T\geq j)^{1/4}$. Diese Folge ist summierbar.
Die Korrelationsformel
ist keine Fluktuations-Dissipations- oder
Reziprozitaetsrelation. Korrelationen koennen den
freien Diffusionswert erhoehen oder vermindern;
die positive Schranke entscheidet nicht die Richtung.

Die [stationaere Antwortrechnung](fading_memory_stationary_mobility_2026-11-22.md)
leitet die davon verschiedene Innovationskorrelation fuer einen
konstanten Kopfinput her. Die frei kalibrierte Einstein-Proportionalitaet
scheitert bereits im schwach attraktiven skalaren Zwei-Orte-FIFO.

## 4. Fehler des Langzeitkoeffizienten beim Trunkieren

Seien $A_H,A_\infty$ die Kovarianzen mit und ohne
Abschneiden, bei gleichen festen Parametern und
ohne Nachnormierung. Die [Fensterschranke](fading_memory_future_mixing_2026-11-21.md)
gibt fuer die Gesetze der juengsten $j+1$ Inkremente
Totalvariation hoechstens $\delta_H(j+1+C_0)$ mit
$C_0=K_0/(t-1)$ und

$$
\delta_H=2\Phi\!\left(\frac{C_s s^{H_s}+C_v q^{H_v}}
{2\varepsilon}\right)-1 .
$$

Fuer $0<\delta_H\leq1/2$ folgt in fester Dimension
mit einer H-unabhaengigen Konstante

$$
\|A_H-A_\infty\|
=O\!\big(\delta_H[1+\log(1/\delta_H)]^3\big).
$$

Beweis: Das Produkt zweier Komponenten von
Inkrementen hat einen gleichmaessig exponentiellen
Tail. Fuer eine Komponente U gilt
$\Pr(|U|>z)\leq2\exp(-z^2/(8\varepsilon^2))$
bei $z\geq2B_0$, denn ihr bedingter
Gaussmittelwert ist beschraenkt. Also hat $|UV|$
oberhalb $4B_0^2$ eine Tailschranke
$4\exp(-z/(8\varepsilon^2))$.
Clippe das Produkt bei
$M=4B_0^2+8\varepsilon^2\log(1/\delta_H)$
in beiden Gesetzen. Der Rest pro Erwartung
ist $O(\delta_H)$; die geclippte Differenz
ist hoechstens $2M\delta_H(j+1+C_0)$.
Summation bis zu einem Vielfachen von
$1+\log(1/\delta_H)$ und die gleichmaessig
exponentielle Korrelation fuer den Rest
geben die Behauptung. Ist $\delta_H=0$,
sind die Uebergaenge und Koeffizienten identisch.
Die Konstanten sind weder gleichmaessig fuer
$\varepsilon\downarrow0$ noch fuer $s,q\uparrow1$.

## 5. Einordnung, Quellen und Kontrollen

Die Zerlegung nutzt die bekannte
[Martingal-Approximation nach Gordin und Peligrad](https://doi.org/10.3150/10-BEJ276);
zum Pfadgrenzsatz siehe
[Whitt, Satz 2.1](https://arxiv.org/abs/0712.1929).
Der [Aging-Vergleich von Meunier, Milisic und Roux](https://doi.org/10.2139/ssrn.6659876)
hat eine andere, *lineare* Ortswechselwirkung.
Der bestehende
[Volltextabgleich](../../paper/paper_i/research/aging_full_text_comparison_2026-10-25.md)
trennt deren lineare Transportregime von der hier
verwendeten beschraenkten nichtlinearen Regel.
Kein Neuheitsanspruch fuer die Grenzsatzmethode.

Dieser Befund setzt eine Grenze fuer den nackten
isolierten Memory-Laufer: Bei den genannten festen
Parametern ist der Langzeit-Ort diffusiv, weder
persistente ballistische Translation
noch aus der Formstabilitaet folgende Traegheit.
Keine Aussage ueber Wechselwirkung, Gravitation,
Quantenstatistik, metastabile Lebensdauer oder
singulaere Rausch-/Memory-Grenzen.

Die [sechs festen Gegenproben](../../tests/test_fading_memory_diffusive_transport.py)
vergleichen die beiden Kovarianzformeln an einem
loesbaren kuenstlichen Vorzeichenfeedback und
die Gauss-Untergrenze mit direkter Quadratur.
65 Tests im betroffenen Panel bestehen.
Es wird kein nativer Langzeitlauf verwendet.
