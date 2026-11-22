# Direkte Paarwirkung mit quadratisch summierbarem Kreuzantrieb

Stand: 2026-11-22. Fortsetzung des
[Fluchtvergleichs bei fester Gaussbreite](memory_pair_fixed_range_escape_2026-11-22.md).
Keine neue Modellregel, Zielsimulation oder Auswahl eines physikalischen
Mediators. Der Coulomb-/Newton-Schwanz ist hier eine Referenz.

**Ergebnis.** In $d\geq3$ trennt sich das endliche
FIFO-Paar bei unabhaengigem positivem Gaussrauschen
fast sicher, wenn der direkte Kreuzantrieb
beschraenkt ist und schneller als $1/r$ abfaellt
(genauer $O(r^{-p})$ fuer ein $p>1$).
Das umfasst feste Gausskerne und einen regulaer
gemachten $1/r^2$-Kraftschwanz. Die gekoppelten und
ungekoppelten Pfadmasse sind sogar aequivalent.
Der Brownsche Langzeitgrenzprozess bei festen
Kerneln ist derselbe wie ohne Kopplung; das ist
kein Urteil ueber nahe oder metastabile Episoden.

## 1. Annahmen und Referenz

Sei P das freie und Q das direkt gekoppelte
Pfadgesetz aus dem [vorigen Bericht](memory_pair_fixed_range_escape_2026-11-22.md).
Beide beginnen an derselben beliebigen endlichen
konsistenten Historie. Die beschraenkten
Selbstdrifts, Horizonte, Rauschpegel
$\varepsilon_i>0$ und alle Altersgewichte
bleiben fest. Nur Q liest die jeweils fremde
Ortsgeschichte mit

$$
u_{i,n}=-\chi\sum_{\ell=0}^{H-1}w_{j,\ell}
\nabla K(x_{i,n}-x_{j,n-\ell}),\qquad j\ne i.
$$

Wir verlangen endliche nichtnegative Gewichte und
$|\nabla K(z)|\leq C(1+|z|/r_0)^{-p}$ mit
$C,r_0>0$ und $p>1$. Isotropie der **Selbstregel**
wird unten fuer den Brownschen Grenzwert verwendet;
der Fluchtbeweis braucht keine Isotropie von K.
Ein Referenzbeispiel ist das attraktive Potential

$$
K(z)=-\kappa/(|z|^2+a^2)^{1/2},\qquad
|\nabla K(z)|=\kappa|z|/(|z|^2+a^2)^{3/2},\qquad
\kappa,a>0 .
$$

Seine Kraft ist am Ursprung regulaer und faellt
im Fernfeld wie $1/r^2$. Das singulaere Punktpotential
ohne a wird nicht erfasst. In 3D gilt als
explizite Kontrolle
$\int_{\mathbb R^3}|\nabla K|^2\,dz=
3\pi^2\kappa^2/(4a)$, aus der Substitution
$r=a\tan\theta$ im radialen Integral.

## 2. Quadratbudget per Besetzungsabschaetzung

Zerlege unter P die gepaarten Mikroinkremente
wie im [Gauss-Fluchtbeweis](memory_pair_fixed_range_escape_2026-11-22.md)
in unabhaengige Regenerationszyklen. Die gleiche
uniforme Minorisierung gilt, da nur die freien
Selbstdrifts in P eingehen. Waehle die
Blocklaenge L hier mindestens so gross wie
den maximalen Quelllag und die beiden
Selbsthorizonte in Inkrementen.
Schreibe $\tau_m$ fuer den Beginn des m-ten
Zyklus und $R_n=x_{1,n}-x_{2,n}$.
Der Relativort $R_{\tau_m}$ ist die
Position nach dem Anfangssegment und m
unabhaengigen Zyklusverschiebungen.
Jede Zyklusverschiebung besitzt einen
festen nichtentarteten Gaussanteil.
Wie zuvor ist ausser auf einer Menge
mit Wahrscheinlichkeit $O(e^{-c m})$
die bedingte Dichte der Summe hoechstens
$C_1 m^{-d/2}$, nachdem man die
Mischungsflags und die Nicht-Gaussanteile
fixiert hat. Das gilt uniform in jedem
Startversatz.

Fuer das beschraenkte Krafthuellquadrat
$f(z)=(1+|z|/r_0)^{-2p}$ folgt jetzt,
mit Trennung bei Radius $r_0\sqrt m$,

$$
\sup_y E_P[f(R_{\tau_m}+y)]
\leq C_2\left[
m^{-d/2}\int_{|z|\leq r_0\sqrt m} f(z)\,dz
+m^{-p}+e^{-c m}\right]=:G_m .
$$

Die Kugelintegration liefert $O(m^{-p})$
fuer $2p<d$, $O(m^{-d/2}\log(2+m))$
fuer $2p=d$ und $O(m^{-d/2})$ fuer
$2p>d$. Alle drei Schranken sind bei
$p>1,d>2$ summierbar. Im integrablen
Fall, insbesondere beim 3D-$1/r^2$-Schwanz,
genuegt auch direkt die $L^1$-Norm von
f fuer den Dichteanteil. Ein einzelner
unterer Abstandsexponent wuerde fuer
den Coulomb-Schwanz nicht genuegen.

### Warum auch alte Quellorte erfasst werden

Fuer $n\in[\tau_m,\tau_{m+1})$ und
$0\leq\ell\leq H-1\leq L$ liegen n
und $n-\ell$ nicht vor $\tau_{m-1}$.
Der Empfangs-/Depositabstand ist also
$\pm R_{\tau_{m-1}}$ plus ein Versatz,
der allein durch die Inkremente der Zyklen
$m-1,m$ bestimmt wird. Dieselben Zyklen
bestimmen die Anzahl der Summanden.
Die beiden Zyklusmarken sind unabhaengig
von $R_{\tau_{m-1}}$. Die Dichteschranke
fuer die aeltere Summe gilt deshalb nach
Bedingung auf beide Marken, fuer jeden
so bestimmten Versatz. Man braucht keine
unabhaengigen alten Orte innerhalb einer
Historie und keine uniforme Schranke nur
im aktuellen Kopfabstand.

Per gewichtetem Cauchy-Schwarz
$|\sum_\ell w_\ell g_\ell|^2
\leq(\sum_\ell w_\ell)\sum_\ell w_\ell|g_\ell|^2$
ist der erwartete quadratische Input des
m-ten Zyklus hoechstens eine Konstante
mal $G_{m-1} E_P[\tau_{m+1}-\tau_m]$
fuer $m\geq2$. Die mittleren Dauern der
Zyklen und der ersten Segmente sowie
die Krafthuellen sind uniform beschraenkt.
Daher gibt es
einen endlichen **startunabhaengigen**
Wert $M_*$ mit

$$
E_P[S_\infty]\leq M_*<\infty,\qquad
S_\infty=\sum_{n\geq0}|\theta_n|^2,\qquad
\theta_n=(u_{1,n}/\varepsilon_1,u_{2,n}/\varepsilon_2).
$$

Die Inputs werden hier entlang freier Pfade
ausgewertet, nicht durch einen Wechsel der
Kopplung innerhalb eines echten Laufs.

## 3. Fast sichere Flucht und Pfadaequivalenz

Es gilt wieder $Q\geq L_\infty P$ mit
$\log L_\infty=M_\infty-S_\infty/2$,
wobei $M_n=\sum_{j<n}\theta_j^T\xi_{j+1}$
die Martingalsumme unter P ist.
Das erwartete Budget macht diese Summe
$L^2$-beschraenkt, daher $E_PM_\infty=0$.
Jensen liefert

$$
E_P L_\infty\geq e^{E_P\log L_\infty}
\geq e^{-M_*/2}>0 .
$$

Insbesondere hat jedes P-fast sichere
Ereignis unter Q Wahrscheinlichkeit
mindestens $e^{-M_*/2}$. Der vorige
freie Fluchtbeweis liefert $|R_n|\to\infty$
P-fast sicher. Betrachte das gemeinsame
Ereignis E dieser Flucht und des endlichen
Budgets $S_\infty<\infty$. Es haengt
nicht vom Weglassen endlich vieler erster
Schritte ab, sofern man am Schnitt mit
dem **vollen** FIFO-Zustand neu startet.
Die uniforme Schranke gilt so unter Q
auch fuer $Q(E\mid\mathcal F_n)$ zu
jeder Zeit n. Diese bedingten
Wahrscheinlichkeiten konvergieren fast
sicher gegen $1_E$. Da sie alle mindestens
$e^{-M_*/2}$ sind, gilt $Q(E)=1$.

Das ist keine Sammlung angenommener
unabhaengiger Fluchtversuche. Die
Markov-Eigenschaft des augmentierten Zustands
und die Konvergenz des bedingten
Indikators genuegen. Eine konkrete
Verweilzeit folgt nicht aus der im
Allgemeinen sehr kleinen Konstanten.

Umgekehrt ist nun auch unter Q das
Inputquadrat summierbar. Der endliche
Gauss-Dichtequotient fuer den Wechsel
**zurueck** von Q nach P bekommt
eine strikt positive, endliche
Grenzdichte Q-fast sicher, wie zuvor
durch Lokalisierung der Martingalsumme
bei endlichem Budget. Die gleiche
Fatou-/Monotonieargumentation gibt
$Q\ll P$. Zusammen mit $P\ll Q$
sind die vollen Pfadgesetze aequivalent.
Ein Erwartungsbudget unter Q wird
dabei nicht behauptet. Pfadweise gilt
jedoch $n^{-1/2}\sum_{j<n}|\theta_j|\to0$:
Ein fester Praefix wird durch $\sqrt n$
geteilt, der Rest ist durch die
$\ell^2$-Tailnorm beschraenkt.

## 4. Feste Breite verschwindet im diffusiven Langzeitlimes

Die [freie Pfadgrenze](fading_memory_diffusive_transport_2026-11-21.md)
gilt fuer jede feste Ausgangshistorie.
Unter P konvergiert daher das Paar
$n^{-1/2}(x_{i,\lfloor n\tau\rfloor}-x_{i,0})$
zu zwei unabhaengigen Brownschen
Bewegungen mit den jeweiligen isolierten
Kovarianzmatrizen $A_i$.
Die Konvergenz ist asymptotisch unabhaengig
von jedem festen endlichen Praefix:
Bedingt darauf startet der freie Prozess
aus dem neuen FIFO-Zustand, und derselbe
Grenzsatz gilt. Die endliche
Zeitverschiebung und der Ortsversatz
verschwinden nach Skalierung
(uniforme Gauss-Tails begrenzen
die maximalen Spruenge).

Sei H ein beschraenktes Lipschitz-Funktional
des skalierten Pfads und $D=dQ/dP\in L^1(P)$.
Approximiere D in $L^1(P)$ durch
$E_P[D\mid\mathcal F_k]$. Bei festem k
liefert die Praefix-Unabhaengigkeit
denselben Grenzwert der mit diesem Gewicht
multiplizierten Erwartungen von H.
Dann kann k gegen unendlich gehen,
da H beschraenkt ist. Somit gilt
der gleiche Pfadgrenzsatz unter Q.
Das ist Konvergenz in Verteilung;
keine Konvergenz unbeschraenkter
Momente folgt allein aus der
absoluten Stetigkeit.

Der [breite, gleichzeitig geschwaechte Grenzfall](memory_pair_diffusive_limit_2026-11-22.md)
war anders: Dort aendert man den
Kreuzkernel mit der Skalierung und
die Wechselwirkung bleibt. Bei
festem Kernel mit quadratisch summierbarem
Kreuzantrieb bleibt hier nur der
freie Langzeittransport.

## 5. Reichweite und Kontrollen

Ein Coulomb-/Newton-Fernfeld allein
loest damit das Bindungsproblem in
dieser endlichen, direkt getriebenen
und unabhaengig verrauschten Klasse
nicht. Keine Aussage zu
singulaeren Kernen, korreliertem
oder verschwindendem Rauschen,
unendlichem FIFO, langsamerem
Kraftabfall oder Feld-/Quantenbindung.
Weder Gravitation noch ein
gravitatives Rauschgesetz sind
als Input aus Memory hergeleitet.

Der [separate raeumliche Feldrauschvergleich](memory_pair_spatial_noise_2026-11-22.md)
klaert einen Teil der hier offenen korrelierten
Faelle: Eine kurzreichweitige gemeinsame
Stoerung mit positivem unabhaengigem Anteil
erhaelt die Flucht; im reinen Feld bleibt
exakte Ueberlagerung moeglich.

Die Zerlegung benutzt
[Athreya und Neys Regenerationsprinzip](https://repository.ias.ac.in/1112/)
und den Gauss-Spezialfall des
[vorhersagbaren Dichtevergleichs](https://doi.org/10.1070/SM1977v033n02ABEH002421).
Der letzte Schritt ist der bekannte
[Erhaltung mischender Grenzsaetze unter Masswechsel nach Aldous und Eagleson](https://doi.org/10.1214/aop/1176995577),
hier explizit mit endlichen
Praefixen ausgefuehrt.

Die [sechs festen Kontrollen](../../tests/test_memory_pair_summable_cross_drift.py)
pruefen das regulaere Referenzprofil,
sein quadratisches Integral,
die Dichte-/Tail-Aufspaltung
und die Altersindizes ueber zwei
Zyklen. 66 Tests im betroffenen Panel
bestehen. Keine Zielbahn oder
Schwellenanpassung.
