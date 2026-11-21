# Translation und Kippen unter einem konstanten FIFO-Kopfinput

Stand: 2026-11-21. Erweiterung der
[axialen Antwort](four_cycle_axial_response_2026-11-21.md) auf
beliebige Richtungen des deklarierten Kopfinputs.
Keine neue Dynamik, native Zielbahn oder Kandidatenauswertung.

**Ergebnis.** In der linearisierten Vierphasenantwort trennt die
Symmetrie Translation von Kippen. Der Translationstensor darf
quer in der Umlaufebene reagieren, mit umgekehrtem Vorzeichen bei
Spiegelung der Zirkulation. Ein separater Tensor kann die Umlaufachse
kippen. Die axiale Antwort erkennt keinen dieser Beitraege.
Ist die Form strikt linear stabil, liefern aktiver Schwerpunkt und
ueber vier Phasen gemittelter Feldnullpunkt dieselbe lineare
Translationsrate; eine einzelne Nullpunktphase kann eine zusaetzliche
scheinbare Drift aus dem Kippen enthalten. Die Koeffizienten des
nativen Kandidaten sind nicht ausgewertet.

## 1. Vom Kopf zur saekularen Pose

Sei $Y_*=(a_0,a_{-1},\ldots,a_{-4})$ ein exakter nativer
Vierzyklus in sechs Lage- und neun gelifteten Formkoordinaten.
$a_n=S^n(r,0,h)^T$, $r,h>0$, und S ist die Vierteldrehung
um z mit anschliessender Spiegelung von z. Im Folgenden wirkt
S auf einer Historie eintragsweise. Die aktiven vier Orte
haben Schwerpunkt null. Der rauschfreie native Schritt F
ist nahe dem Orbit glatt, $F(Y_*)=S Y_*$, und wir setzen
$F_{\epsilon b}(Y)=F(Y)+\epsilon\mathcal E b$ mit
$\mathcal E b=(b,0,0,0,0)$. b ist ein konstanter polarer
Vektor im Labor, kein Kraftgesetz.

Mit $L=S^{-1}DF(Y_*)$ gehorcht die mitgedrehte Variation
$u_n=S^{-n}\partial_\epsilon Y_n|_0$ der Rekursion

$$
u_{n+1}=L u_n+\mathcal E S^{-n-1}b .
$$

Nach je vier Schritten stimmen Labor und mitgedrehter Rahmen
ueberein. Der Vierphasenblock und sein Eingang sind

$$
P=L^4,\qquad G=\sum_{k=0}^3 L^k\mathcal E S^k,\qquad
u_{4(m+1)}=P u_{4m}+G b .
$$

Die Pose ist in diesem zentrierten Referenzrahmen als
sechsdimensionaler Tangentialraum eindeutig eingebettet:

$$
\mathcal R(t,\omega)_j=t+\omega\times a_{-j}\quad (j=0,\ldots,4).
$$

P fixiert jede dieser sechs Richtungen. Fuer die Zerlegung
sei vorausgesetzt, dass der Quotient von P modulo dieser
Richtungen **keinen Eigenwert 1** besitzt. Das schliesst im
Quotienten von L alle vierten Einheitswurzeln aus und ist
mehr als die Bedingung fuer die axiale Zweischrittfortsetzung.
Der Pose-Raum und $\operatorname{im}(P-I)$ sind dann
komplementaer. Sei $\Pi$ der Projektor auf die Pose entlang
dieses Bildes. Er kommutiert mit L.

Definiere die beiden linearen Antworten pro Update mittels

$$
\mathcal R(D b,C b)=\tfrac14\Pi G b .
$$

Sie sind z.B. durch ein lineares Gleichungssystem ohne
Langzeitlauf bestimmbar: Zerlege $G=(P-I)U+4\mathcal R(D,C)$,
mit den Spalten von U in einem beliebigen festen Schnitt
zum Posenraum. Der Schnitt ist fuer D und C unerheblich.
Bei $u_0=0$ gilt exakt

$$
u_{4m}=m\Pi G b+\sum_{k=0}^{m-1}P^k(I-\Pi)G b .
$$

Nur falls der Formblock strikt Schur-stabil ist, ist der
zweite Term beschraenkt und konvergiert. Die projizierte
Rate existiert auch bei blosser Nichtresonanz, ist dann
aber nicht automatisch die dominante Antwort. Alle Raten
hier beziehen sich auf die Ableitung bei $\epsilon=0$
vor dem Grenzfall vieler Perioden, nicht auf eine
Langzeitloesung bei festem nichtnulligem Input.

## 2. Was Symmetrie erlaubt und was sie verbietet

Wegen $S^4=I$ und $\Pi L^4=\Pi$ folgt $L\Pi G S=\Pi G$.
L wirkt auf Posekoordinaten als
$(t,\omega)\mapsto(S^{-1}t,(\det S)S^{-1}\omega)$:
$\omega$ ist ein axialer Vektor. Daher gelten

$$
DS=SD,\qquad CS=(\det S)SC=-SC .
$$

Die Loesungen ueber den reellen Zahlen haben exakt die Formen

$$
D=
\begin{pmatrix}
\mu_\perp&-\mu_{\rm q}&0\\
\mu_{\rm q}&\mu_\perp&0\\
0&0&\mu_z
\end{pmatrix},
\qquad
C=
\begin{pmatrix}
c&d&0\\
d&-c&0\\
0&0&0
\end{pmatrix}.
$$

Die Vierteldrehung auf xy hat kein reelles Eigenpaar
mit Eigenwert +1 oder -1, sodass Kopplungen zwischen Ebene
und Achse fehlen. In der Ebene kommutiert D mit der
Vierteldrehung, waehrend C antikommutiert. Auf der Achse
annulliert C den Input. Ein Wechsel der Startphase
$Y_*\mapsto S^jY_*$ transformiert diese Tensoren wie
$D\mapsto S^j D S^{-j}$ und
$C\mapsto(\det S)^j S^j C S^{-j}$, also bleiben
beide in den **gleichen Laborkoordinaten** unveraendert.

Fuer einen axialen Input reduziert sich $G e_z$ auf
$\sum_{k=0}^3(-1)^k L^k\mathcal E e_z$. Der linke axiale
Translationskovektor aus der Zweischrittanalyse hat
Eigenwert -1. Anwendung auf die Summe ergibt sofort
$\mu_z=\chi$ aus der axialen Rechnung, nicht viermal
$\chi$. Die Querrate $\mu_{\rm q}$ und das Kippen
bleiben dabei ungemessen.

Bei Spiegelung des gesamten altersmarkierten Orbits
mit $U=\operatorname{diag}(1,-1,1)$ gilt wegen nativer
O(3)-Kovarianz $D'=UDU^{-1}$ und
$C'=(\det U)UCU^{-1}$. Damit kehrt nur der antisymmetrische
Translationsbeitrag $\mu_{\rm q}$ sein Vorzeichen um,
waehrend $\mu_\perp,\mu_z$ gleich bleiben. Das ist ein
Spiegelvergleich zweier Zirkulationen, keine Zeitumkehr-
oder Reziprozitaetsaussage. Eine skalare isotrope
Translationsantwort verlangt $\mu_\perp=\mu_z$ und
$\mu_{\rm q}=0$; ohne Kippen braucht sie zusaetzlich $C=0$.

## 3. Wann eine fast starre Bahnlage als Antwort scheitert

Angenommen, es gibt eine glatte Fortsetzung vom fest
orientierten $Y_*$, die nach vier Schritten bei Input
$\epsilon b$ bis auf Translation zurueckkehrt. Durch
Differenzieren und Projektion mit $\Pi$ folgt notwendig
$C b=0$. Falls $c^2+d^2>0$, ist das nur fuer axiale
Anstoesse moeglich: Der ebene C-Block hat Determinante
$-(c^2+d^2)$. Bei zusaetzlich erlaubter Drehung um b
(die Rotationssymmetrie, die den Input festhaelt) gilt
als schwaechere notwendige Bedingung $C b\parallel b$.
Ein schraeger Anstoss mit axialer und lateraler Komponente
erfuellt sie bei nichtnulligem C nicht. Rein laterale
Anstoesse kommen nur entlang der beiden Eigenachsen des
ebenen C-Blocks infrage. Das sind keine Existenzsaetze
fuer die verbleibenden Richtungen, und andere Anfangs-
orientierungen oder zeitabhaengige Lagen bleiben offen.

## 4. Schwerpunkt und mitwandernder Nullpunkt

Bei strikt stabilem Formblock und regularem Feldnullpunkt
$z_*(Y)$ in der betrachteten Umgebung gilt an Phase j
mit $z_j=z_*(S^jY_*)=S^j z_0$:

$$
\left.\partial_\epsilon z_*(Y_{4m+j})\right|_0
=4m\big[D b+(C b)\times z_j\big]+O(1).
$$

Denn $DF^j$ transportiert dieselbe starre Tangente
in die Phase j, und die Ableitung des aequivarianten
Feldnullpunkts auf einer Posetangente ist entsprechend
Translation plus Kreuzprodukt. Der beschraenkte
Formterm und die letzten j Inputs gehen in $O(1)$ ein.
Fuer den Schwerpunkt der vier aktiven Orte entfaellt
das Kreuzprodukt bereits in jeder Phase, da ihr
Referenzschwerpunkt null ist. Fuer den Nullpunkt entfaellt
es im Mittel ueber alle vier Phasen, weil
$\sum_{j=0}^3S^j=0$ und somit $\sum_j z_j=0$.
Die Rate einer einzelnen Nullpunktphase ist also ohne
Kippmessung nicht allgemein eine Translationsrate.

## 5. Diskriminierender Anschluss und Quellen

Fuer einen spaeter getrennt freigegebenen Benchmark genuegen
nach der Spektralpruefung ein axialer und ein lateraler
Kopfinput, um die fuenf linearen Koeffizienten zu messen.
Die gespiegelte Zirkulation kontrolliert das Vorzeichen
der Querrate; Phase und Mittelwert des Defekts trennen
Kippen von Translation. Bis dahin ist weder $\mu_{\rm q}\ne0$
noch eine Skalarmobilitaet am nativen Kandidaten belegt.
Auch ein skalarer Antwortwert waere kein Massennachweis,
keine Rueckwirkung und kein Paar-Kopplungsgesetz.

Antisymmetrische Querantworten sind aus anderen Modellen
bekannt, etwa bei
[Hargus, Epstein und Mandadapu, PRL 127, 178001 (2021)](https://doi.org/10.1103/PhysRevLett.127.178001)
fuer Diffusion und in
[PRE 113, L042104 (2026)](https://doi.org/10.1103/k8vq-dw2w)
fuer getriebene Tracer in chiralen Fluiden. Hier wird
weder eine Diffusionsrelation noch ein Fluidmodell
angenommen. Der fruehere [P4-R-Querbefund](../../docs/status/paper_claims.md)
betrifft zudem einen anderen, explizit konstruierten Source-/Write-Port.
Das hier ist eine Symmetrie- und Projektoraussage fuer
den nativen periodischen FIFO mit deklariertem Kopfinput.

Die [vier neuen festen Kontrollen](../../tests/test_four_cycle_axial_response.py)
verwenden ausschliesslich kuenstliche lagekovariante
Kopfableitungen. Sie demonstrieren nichtverschwindende
Quer-/Kippraten als **formale** Moeglichkeit, die
Spiegelkontrolle, die Phasenmittelung sowie die
Kompatibilitaet mit der axialen Reduktion.
105 Tests im betroffenen Panel bestehen. Keine Simulation
eines Zielorbits und keine Aenderung an Paper I.
