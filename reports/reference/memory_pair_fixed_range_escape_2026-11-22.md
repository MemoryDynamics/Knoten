# Direkter Gauss-Kanal: Flucht bei fester Breite und positivem Rauschen

Stand: 2026-11-22. Analytischer Anschluss an den
[breiten Paargrenzfall](memory_pair_diffusive_limit_2026-11-22.md)
und die [vorhandene direkte Regel](../../docs/reference/hydrogen_pair_audit.md).
Kein Langzeitlauf, keine Zielpraeparation und keine neue Dynamik.

**Ergebnis.** In $d\geq3$ besitzt das direkt gekoppelte
endliche FIFO-Paar mit festen Gaussbreiten und positivem,
unabhaengigem Gaussrauschen von **jedem** konsistenten
Start aus positive Wahrscheinlichkeit, im Abstand
gegen unendlich zu laufen. Damit gibt es keine
stationaere Abstandsverteilung, auch nicht bei fester
mikroskopischer Breite. Der Beweis verwendet keine
Weitbereichsskalierung und keine Klein-Gain-Annahme.
Er beweist weder Flucht mit Wahrscheinlichkeit eins
noch eine kurze Aufenthaltsdauer eines nahen Paars.

Eine [spaetere Besetzungsabschaetzung](memory_pair_summable_cross_drift_2026-11-22.md)
erhaelt ein startunabhaengiges erwartetes Quadratbudget.
Sie schaerft die Flucht auf Wahrscheinlichkeit eins
und erfasst auch regulaere Potenzen $r^{-p}$ mit $p>1$.
Der vorliegende Beweis allein beansprucht diese Schaerfung nicht.

## 1. Regel und Ort der offenen Frage

Seien $x_{1,n},x_{2,n}\in\mathbb R^d$ die beiden
aktuellen Orte, $R_n=x_{1,n}-x_{2,n}$,
und $v_{i,n}=x_{i,n}-x_{i,n-1}$.
Die relativen Selbsthistorien $h_{i,n}$ werden aus
endlich vielen Inkrementen rekonstruiert.
Der beschraenkte Selbstdrift $b_i(h_{i,n})$
ist translationsinvariant. Die nativen
skalaren Gauss-Selbstkraefte erfuellen
$|b_i|\leq B_i<\infty$ ohne Begrenzung der
gespeicherten Orte. Die feste direkte Kopplung liest

$$
u_{i,n}=-\chi\sum_{\ell=0}^{H-1}w_{j,\ell}
\nabla K(x_{i,n}-x_{j,n-\ell}),\qquad j\ne i ,
$$

mit endlichen Gewichten, festem $\chi$ und K als
endlicher Summe radialer Gaussfunktionen fester
positiver Breite. In beiden Richtungen wird aus
dem alten Zustand gelesen; die neuen
Gaussinnovationen $\varepsilon_i\xi_{i,n+1}$
sind mit $\varepsilon_i>0$ unabhaengig.
Betrachte den gefuellten Prozess auf freiem
Raum. Die Anfangshistorie ist beliebig,
aber endlich und konsistent.

Der alte Quelleintrag kann trotz des
heutigen Abstands nahe am Empfaenger liegen.
Es gibt daher im vollen Zustand **keine**
uniforme Gauss-Schranke allein in $|R_n|$.
Auch aus einem Brownschen Skalenlimes folgt
nicht, ob der feste Prozess in einfachen
Schritten selten zu einem Ursprung zurueckkehrt.
Wir kontrollieren stattdessen die tatsaechlichen
Pfade des ungekoppelten Systems.

## 2. Das freie Paar verlaesst wachsende Kugeln

Nenne P das Pfadgesetz ohne Kreuzinput, mit
unveraendertem Selbstdrift und gleicher
Anfangshistorie. Waehle eine feste Blocklaenge
$L\geq1$, nach der jedes Inkrement der alten
Selbsthistorien durch neue ersetzt ist
(fuer das skalare FIFO kann $L=\max(1,H-1)$
gewaehlt werden). Der volle Blockausgang
besteht aus beiden geordneten Inkrementfolgen.
Fuer die bedingte Dichte eines einzelnen
Schritts gilt mit beliebigem $|m|\leq B_i$

$$
\varphi_{\varepsilon_i}(v-m)
\geq 2^{-d/2}e^{-B_i^2/\varepsilon_i^2}
\varphi_{\varepsilon_i/\sqrt2}(v) .
$$

Die [skalare Minorisierung](../../paper/paper_i/research/finite_memory_stationarity_2026-10-21.md)
liefert durch Multiplikation ueber L
Schritte und beide Laeufer eine **gemeinsame
Blockkomponente** $p\nu$ mit $p>0$.
Hier ist $\nu$ das Produkt zentrierter
Gaussdichten mit den angegebenen reduzierten
Varianzen. Der wahre bedingte Block wird
so geschrieben: Mit unabhaengiger Muenze
mit Wahrscheinlichkeit p ziehe $\nu$, sonst
die normierte Restdichte.
Das veraendert das marginale Pfadgesetz nicht.

Ein Zyklus beginnt **vor** einem gelungenen
Gaussblock und endet unmittelbar vor dem
naechsten gelungenen Block. Der Gaussblock
am Anfang uebernimmt keine alte Geschichte.
Nach ihm haengen Restbloecke und ihre Zahl
nur von seinen eigenen Inkrementen und den
neuen Ziehungen ab. Weil die Ortsverschiebung
ignoriert wird, sind zyklische Relativverschiebungen
$D_m$ und Zykluslaengen gemeinsam iid,
unabhaengig von der Position vor dem ersten
gelungenen Block. Die Laenge in Bloecken ist
geometrisch. Mit Wahrscheinlichkeit p folgt
auf den Anfangsblock sofort der naechste
gelungene Block. In diesem Fall ist $D_m$
ein zentrierter Gaussvektor mit Kovarianz
$L(\varepsilon_1^2+\varepsilon_2^2)I_d/2$.
Die Verteilung von $D_m$ hat also einen
festen echten Gaussanteil, ungeachtet der
Restdichte. Man darf den ersten gelungenen
Block nicht dem vorherigen Zyklus zuschlagen:
Seine Ausgangshistorie waere dann mit
dem vorherigen Verschiebungsbetrag korreliert.

Schreibe $\tau_m$ fuer die Zeit vor dem
m-ten nachfolgenden gelungenen Block.
Bedingt auf die Mischungskomponenten der
m unabhaengigen Zyklusverschiebungen und
die restlichen Summanden gilt: Sind
mindestens $pm/2$ davon Gaussanteile,
hat die Summe eine Dichte hoechstens
$C m^{-d/2}$, unabhaengig von der Mitte.
Das Gegenereignis ist fuer einen
Binomialzaehler exponentiell klein.
Fuer jedes $\gamma>0$ folgt daher

$$
P(|R_{\tau_m}|\leq m^\gamma)
\leq C m^{-d(1/2-\gamma)}+e^{-c m}
$$

mit festen positiven Konstanten. Waehle
$0<\gamma<(d-2)/(2d)$. Die rechte Seite
ist summierbar; auf den Zyklusgrenzen
waechst der Abstand also fast sicher
schliesslich mindestens wie $m^\gamma$.

Zwischen den Grenzen haben die Blockanzahl
pro Zyklus exponentielle Tails und die
einzelnen Mikroinkremente wegen ihres
beschraenkten Gaussmittels Gauss-Tails.
Zweimal Borel-Cantelli liefert Zyklenlaenge
$O(\log m)$ und Inkrementgroesse
$O(\sqrt{\log n})$ fast sicher
(fuer hinreichend spaete m bzw. n).
Das Gesetz der grossen Zahlen fuer die
Zyklenlaengen liefert $\tau_m\asymp m$.
Somit ist die Auslenkung innerhalb eines
Zyklus $O((\log m)^{3/2})=o(m^\gamma)$.
Nach Abzug der endlich vielen alten
Schritte bleibt auch jeder Abstand zu
jedem aktiven fremden Deposit schliesslich
mindestens eine positive Konstante mal $n^\gamma$.
Alle Wahrscheinlichkeiten bis hier gelten
unter dem freien Gesetz P, nicht schon
unter dem gekoppelten.

## 3. Flucht behaelt positive Wahrscheinlichkeit

Kontrolliere auf **denselben Koordinatenpfaden**
den Kreuzinput, den das gekoppelte Gesetz Q
anwenden wuerde. Eine feste Gaussableitung
faellt exponentiell in der quadrierten
Distanz, notfalls mit vergroesserter Breite.
Aus dem Abstand zu allen alten Deposits
folgt unter P fast sicher

$$
\sum_{n\geq0}|\theta_n|^2<\infty,qquad
\theta_n=(u_{1,n}/\varepsilon_1,u_{2,n}/\varepsilon_2).
$$

Der Rauschvektor $\xi_{n+1}$
fasst die beiden standardisierten freien
Innovationen zusammen. Der Quotient
der Pfaddichten bis N ist exakt

$$
L_N=\frac{dQ_N}{dP_N}
=\exp\left(\sum_{n<N}\theta_n^T\xi_{n+1}
-\tfrac12\sum_{n<N}|\theta_n|^2\right).
$$

Das folgt aus den bedingten Gaussdichten;
die Abschnitte des Pfades werden nicht als
unabhaengig behandelt. Die Inputs sind
vorhersagbar. Die Martingalsumme im
Exponenten konvergiert auf endlicher
quadratischer Energie fast sicher
(Stopp **vor** Ueberschreiten einer
festen Budgetgrenze ergibt jeweils eine
$L^2$-beschraenkte Martingalsumme).
Also $L_N\to L_\infty>0$ P-fast sicher.

Fuer jedes endliche Pfadereignis A gibt
Fatou $Q(A)\geq E_P[1_A L_\infty]$.
Die Ungleichung geht durch die monotone
Klasse auf alle Pfadereignisse ueber.
So behaelt jedes unter P positive
Ereignis unter Q positive
Wahrscheinlichkeit. Insbesondere

$$
Q(|R_n|\to\infty)>0 .
$$

Keine Gleichheit $Q=L_\infty P$ und
keine uniforme Integrabilitaet von $L_N$
wird angenommen. Die Richtung ist
$P\ll Q$, nicht automatisch $Q\ll P$.

## 4. Was dies ueber Bindung entscheidet

Das Fluchtereignis hat von jedem
zulaessigen Start positive Wahrscheinlichkeit.
Das gilt durch Integration also auch
bei jedem zufaelligen Startgesetz.
Gaebe es ein solches Gesetz mit
stationaerem Abstands-Marginal, wuerde
fuer jedes $R>0$ Fatou ergeben

$$
Q(|R_n|\to\infty)\leq
\liminf_{n\to\infty}Q(|R_n|>R)
=Q(|R_0|>R) .
$$

Die rechte Seite geht gegen null,
Widerspruch. Sogar allgemeine uniforme
Straffheit des Abstandsprozesses ist so
ausgeschlossen. Das laesst lange nahe
Episoden, eine kleine Fluchtwahrscheinlichkeit
und bedingte Bindung unter Selektion offen.
Zwei Dimensionen, entartetes Rauschen,
unendliche Horizonte oder langreichweitige
Mediatoren sind nicht von diesem
Satz fuer feste Gaussbreiten erfasst.

Die [Regenerationsidee von Athreya und Ney](https://repository.ias.ac.in/1112/)
und die [vorhersagbaren Dichtekriterien von Kabanov,
Liptser und Shiryaev](https://doi.org/10.1070/SM1977v033n02ABEH002421)
ordnen die mathematischen Schritte ein.
Der spezifische Beitrag ist ihre explizite
Verknuepfung mit dem FIFO-Block, seinen
alten Quelldeposits und dem quadratischen
Budget des festen Gauss-Kreuzterms.

Die [sieben festen Kontrollen](../../tests/test_memory_pair_fixed_range_escape.py)
pruefen Dichteminorisierung, Gaussanteil
der Blocksumme, vorhersehbaren
Dichtequotienten und eine verzoegerte Quelle.
60 Tests im betroffenen Panel bestehen. Keine
gepaarte Langzeitbahn und kein Stabilitaetskandidat
wird ausgefuehrt.
