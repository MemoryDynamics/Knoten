# Raeumlich korreliertes Gaussrauschen: Trennung oder exakte Ueberlagerung

Stand: 2026-11-22. Getrennter Rauschfeld-Referenzvergleich zum
[direkten Paar mit quadratischem Inputbudget](memory_pair_summable_cross_drift_2026-11-22.md).
Kein aus Memory hergeleitetes Feld, keine Solver-Aenderung oder Zielbahn.

**Ergebnis.** Ein kurzes raeumliches Korrelationsprofil
allein bindet zwei verschiedene Laeufer nicht stationaer.
Mit jedem festen positiven unabhaengigen Rauschanteil
erfolgt in $d\geq3$ weiterhin fast sichere Trennung
im hier betrachteten endlichen FIFO. Ohne diesen Anteil
ist eine exakt gemeinsame Bahn identischer Laeufer
invariant. Von verschiedenen Kopfpositionen aus
bleibt jedoch positive Fluchtwahrscheinlichkeit,
und eine stationaere Verteilung getrennter Orte
ist ausgeschlossen. Ein homogenes isotropes skalares
Korrelationsprofil kann keine vollkommen korrelierte
Schale in positivem Abstand erzeugen.

## 1. Ein klarer Feldvertrag ohne Felddynamik

Die endlichen Selbsthistorien, beschraenkten
Selbstkraefte und direkten Kreuzantriebe $u_i$
bleiben wie im
[vorigen Vergleich](memory_pair_summable_cross_drift_2026-11-22.md).
Die Kreuzkraft ist global beschraenkt und faellt
wie $O(r^{-p})$, $p>1$, also auch im regulaeren
invers-quadratischen Referenzfall. Wir ersetzen
hier **nur** die gemeinsame Statistik der
frischen Innovationsvektoren.

Jedes Update liest an beiden alten Kopfpositionen
ein neues, von der Vergangenheit unabhaengiges,
homogenes Gaussfeld $G_n$. Seine d Komponenten
sind unabhaengige Kopien eines skalaren Felds
mit Einheitsvarianz und radialer Korrelation
$\rho(|x-y|)$, $\rho(0)=1$.
Wir setzen $\rho(r)=O(r^{-q})$ mit $q>1$ und
verwenden einen gueltigen nichtkonstanten
Kovarianzkern, etwa
$\rho(r)=\exp(-r^2/(2\ell^2))$, $\ell>0$.
Mit unabhaengigen Standard-Gaussvektoren
$\zeta_{i,n}$ und festem Anteil $0\leq\nu\leq1$
lautet der Rauschbeitrag fuer Laeufer i

$$
\varepsilon_i\left[
\sqrt{1-\nu}\,G_n(x_{i,n})+\sqrt\nu\,\zeta_{i,n}
\right],\qquad \varepsilon_i>0 .
$$

Alle Komponenten bleiben am einzelnen Ort
gleich stark verrauscht. Der Parameter $\nu$
aendert nur den gemeinsamen Anteil. Es gibt
keine Feldgleichung, Ausbreitung oder
Rueckwirkung. Der Fall $\nu=1$ ist
unabhaengiges Rauschen, $\nu=0$ das reine
gemeinsame Referenzfeld.

Sei P wieder das freie Paar mit unabhaengigem
Rauschen und unveraendertem Selbstdrift,
Q das Paar mit Kreuzdrift und obigem Feldrauschen.
Nach Abzug der Selbstdrifts und Division durch
die jeweiligen $\varepsilon_i$ sind die
bedingten Ein-Schritt-Gesetze $N(0,I_{2d})$ unter
P und $N(\theta,A_c)$ unter Q:

$$
\theta=(u_1/\varepsilon_1,u_2/\varepsilon_2),\qquad
c=(1-\nu)\rho(|R|),\quad R=x_1-x_2,\qquad
A_c=\begin{pmatrix}I_d&cI_d\\cI_d&I_d\end{pmatrix}.
$$

Die Eigenwerte sind $1+c$ und $1-c$, je d-mal.
Die Relativinnovation hat Kovarianz
$(\varepsilon_1^2+\varepsilon_2^2-2c\varepsilon_1\varepsilon_2)I_d$.
Bei gleichen Rauschpegeln und reinem Gaussfeld
verschwindet sie am gemeinsamen Ort und ist im
Nahbereich von Ordnung $|R|^2$, in der Ferne
aber wieder von derselben Groesse wie bei
unabhaengigen Innovationen.

## 2. Warum ein echtes Korrelationsfeld keine perfekte Schale hat

Angenommen, fuer ein $a>0$ gilt $|\rho(a)|=1$.
Fuer jedes feste Paar von Orten im Abstand a
folgt aus der Varianz der Differenz bzw. Summe:
$G(x+u)=sG(x)$ fast sicher fuer $|u|=a$,
$s=\rho(a)\in\{-1,1\}$. Das ist eine
Gleichheit fuer die jeweils betrachteten endlich
vielen Orte, keine Annahme ueber alle
unabzaehlbaren Punkte einer Realisierung.

Jeder Vektor w mit $|w|\leq2a$ ist in
$d\geq2$ die Differenz von zwei Vektoren
u,v der Laenge a. Waehle
$u=h+w/2$, $v=h-w/2$, $h\perp w$,
$|h|^2=a^2-|w|^2/4$. Beide Feldwerte
bei $x+u,x+v$ sind $sG(x)$ und damit gleich.
Also $\rho(|w|)=1$ fuer alle diese w.
Verketten solcher Schritte macht die
Korrelation konstant eins. Das widerspricht
der nichtkonstanten Feldannahme (und im
Minusfall bereits der Annahme am Radius a).
Folglich ist $|\rho(r)|<1$ fuer jedes
$r>0$. Eine willkuerlich eingesetzte perfekte
Korrelation am gewuenschten Paarabstand waere
kein solches Feld.

## 3. Der Dichtevergleich hat jetzt zwei Budgets

Unter dem freien Gesetz P gilt fuer jeden
Start nach der
[Regenerations-Besetzungsabschaetzung](memory_pair_summable_cross_drift_2026-11-22.md)
gleichmaessig

$$
E_P\sum_{n\geq0}\left(|\theta_n|^2+c_n^2\right)<\infty .
$$

Der erste Term erfasst wieder alle alten
Quelldeposits. Der zweite nutzt dieselbe
Besetzungsschranke mit Lag null und dem
quadratischen Korrelationsprofil.
Damit sind beide Tails auch P-fast sicher
summierbar. Der Beweis folgt nicht aus
einer blossen punktweisen Fernabstandsannahme.

Fuer $|c|<1$ und $z\sim N(0,I_{2d})$ ist
der Logquotient der neuen zu den freien
bedingten Dichten

$$
\ell(z)=-\tfrac12\log\det A_c
-\tfrac12[(z-\theta)^TA_c^{-1}(z-\theta)-z^Tz].
$$

Sein negatives bedingtes Mittel $D_{P,Q}$
und seine Schwankungsvarianz unter P sind

$$
D_{P,Q}=\tfrac12[\operatorname{tr}(A_c^{-1})-2d
+\log\det A_c+\theta^TA_c^{-1}\theta],\qquad
\operatorname{Var}_P(\ell)
=\tfrac12\operatorname{tr}[(A_c^{-1}-I)^2]+|A_c^{-1}\theta|^2 .
$$

Die Varianz folgt, weil die zentrierte
quadratische und die lineare Gaussform
orthogonal sind. Fuer $|c|\leq c_*<1$
sind beide Ausdruecke durch Konstanten
mal $c^2+|\theta|^2$ beschraenkt.
Zum Beispiel ist $\log\det A_c=d\log(1-c^2)\leq0$
und $\operatorname{tr}(A_c^{-1})-2d=2dc^2/(1-c^2)$,
also

$$
D_{P,Q}\leq\frac{dc^2}{1-c_*^2}
+\frac{|\theta|^2}{2(1-c_*)}.
$$

Fuer die umgekehrte Dichtedifferenz kann
man $z=\theta+A_c^{1/2}\xi$ unter Q
einsetzen. Das negative Mittel des
umgekehrten Logs ist
$D_{Q,P}=(-\log\det A_c+|\theta|^2)/2$,
seine Varianz ist
$\operatorname{tr}[(A_c-I)^2]/2+|A_c^{1/2}\theta|^2$.
Auch diese Groessen sind im gleichen
quadratischen Budget kontrolliert.

## 4. Was sich bei einem unabhaengigen Rest aendert

**Fester unabhaengiger Anteil $\nu>0$.**
Dann gilt die globale Schranke $|c|\leq1-\nu<1$.
Unter P summieren sich die bedingten
Logmittel, und ihre Zentrierungen
bilden eine $L^2$-beschraenkte Martingalsumme.
Der Grenzquotient $L_\infty$ ist strikt
positiv und erfuellt $Q\geq L_\infty P$
durch Fatou auf endlichen Ereignissen
und monotone Fortsetzung. Jensen und
die startunabhaengige Budgetgrenze ergeben
$E_PL_\infty\geq e^{-M_*}>0$ mit
festem endlichem $M_*$. Dies liefert
fuer die Flucht und das gemeinsame
endliche Quadratbudget einen
startunabhaengigen positiven Q-Anteil.
Beide Eigenschaften bleiben beim
Neustart aus dem vollen FIFO erhalten.
Der bedingte Ereignisindikator muss
daher wieder fast sicher gegen eins
konvergieren, wie im
[vorigen Argument](memory_pair_summable_cross_drift_2026-11-22.md).
Das umgekehrte Logbudget ist nun
Q-fast sicher ebenfalls endlich,
also $Q\ll P$ per Lokalisierung
und Fatou. Damit bleiben auch die
freien Brownschen Pfadgrenzen bei
festen Parametern erhalten.
Keine Aussage ueber die Zeit bis
zur Trennung.

**Reines gemeinsames Feld $\nu=0$.**
Starte mit $R_0\ne0$. Unter P und Q
ist jeder spaetere Kopfabstand
fast sicher von null verschieden:
Die naechste relative Gaussverteilung
bei $R\ne0$ ist nichtentartet.
Alle endlichen Dichtequotienten
sind so wohldefiniert.
Unter P sind wegen $\sum c_n^2<\infty$
nur endlich viele $|c_n|>1/2$.
Deren Logquotienten sind endlich,
aber nicht uniform beschraenkt.
Fuer die uebrigen Schritte gelten
die quadratischen Schranken
mit $c_*=1/2$; die entsprechend
maskierte Martingalsumme konvergiert.
Folglich wieder $P\ll Q$ und
positive Fluchtwahrscheinlichkeit
aus jedem getrennten Start,
aber ohne hier bewiesene uniforme
Untergrenze nahe der Diagonale.
Eine invariante Wahrscheinlichkeit
mit positiver Masse ausserhalb
$R=0$ ist ausgeschlossen:
Sie haette positiven Fluchtanteil,
waehrend stationaere Marginale
diesen durch Fatou ausschliessen.

Bei identischen Knoten, gleichen
$\varepsilon_i$ und identischen ganzen
Historien bleibt die Diagonale dagegen
genau invariant. Beide lesen dann
denselben Rauschwert und dieselben
Driftterme. Der auf der Diagonale
wirksame Einzelprozess hat einen
beschraenkten Drift und positiven
Gaussrauschen; sein relatives
endliches Gedaechtnis hat daher eine
stationaere Verteilung. Das liefert
ein zusammenfallendes stationaeres
Paar, **keinen** endlichen Bindungsradius.
Unterschiedliche Rauschpegel erhalten
die Diagonale nicht, weil dann selbst
ein gemeinsamer Feldwert die relative
Innovation nicht beseitigt.
Ob von getrennten Starts manche
Bahnen asymptotisch synchronisieren,
bleibt offen.

## 5. Reichweite und Quellen

Die betrachtete gemeinsame Stoerung
ist ein klassisches zeitlich frisches
Feld. Der
[Zweipunktbezug bei isotropen stochastischen Fluessen](https://www.jstor.org/stable/2243856)
hat eine verwandte Kovarianzstruktur,
aber eine andere kontinuierliche
Dynamik. Der
[Dichtevergleich nach Kabanov, Liptser und Shiryaev](https://doi.org/10.1070/SM1977v033n02ABEH002421)
wird hier mit explizitem
Gauss-Logquotienten ausgefuehrt.
Zeitgedaechtnis des Feldes,
langsamere Korrelation, spezielle
nichtisotrope Tensorfelder,
Rangsperren oder Quantisierung
werden nicht ausgeschlossen
oder hergeleitet.

Die [sieben festen Kontrollen](../../tests/test_memory_pair_spatial_noise.py)
pruefen Schalen-Geometrie, gemeinsame
und relative Kovarianz sowie beide
Logdichte-Momente mit exakter
Gauss-Quadratur. 73 Tests im betroffenen Panel
bestehen. Keine stochastische
Zielbahn und keine neue Solver-Regel.
