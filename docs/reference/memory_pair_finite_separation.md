# Getrennte Memory-Strukturen: Form, Mittelung und Reziprozitaet

Stand: 2026-10-29. Analytischer Anschluss an
[Paarreduktion](memory_pair_reduction.md) und
[Potentialbilanz](memory_pair_energy.md). Keine neue Dynamik, kein
Ziellauf und kein bereits gebundener oder stabiler Teilchentraeger.
Die Gleichungen gelten im vorgegebenen euklidischen Eingaberaum, nicht
nur in 3D; eine physikalische aeussere Dimension wird nicht hergeleitet.

**Ergebnis:** Bei endlichem Abstand ist die native Kreuzantwort durch
aktuellen Punktversatz, Quellform und einen expliziten Rest bestimmt.
Eine reziproke gemittelte Paarwirkung ist unter eingefrorenen,
stationaeren und zwischen den Traegern unabhaengigen inneren Verteilungen
moeglich. Stationaritaet der Einzelverteilungen allein genuegt nicht:
zeitversetzte Kreuzkorrelationen koennen eine mittlere Unwucht erhalten.
Damit ist ein pruefbarer statistischer Anschluss bestimmt, kein Nachweis,
dass die vorhandenen gekoppelten Knoten seine Voraussetzungen erfuellen.

## 1. Momentane Antwort bei endlichem Abstand

Verwende die unveraenderte Regel in
[`reciprocal_nodes.py`](https://github.com/MemoryDynamics/Knoten/blob/19195a3504a860278d9514a3140cf982fee85dbb/src/emergenz_knoten/reciprocal_nodes.py).
Fuer die momentanen gewichteten Memory-Center $c_i$ definiere

$$
R=c_A-c_B,\quad u_i=x_i-c_i,\quad z_{i\ell}=y_{i\ell}-c_i,
\quad p_{i\ell}=w_{i\ell}/W_i,\quad W_i=\sum_\ell w_{i\ell}>0,
\quad \Sigma_i=\sum_\ell p_{i\ell}z_{i\ell}z_{i\ell}^{T}.
$$

Dann gilt $\sum_\ell p_{i\ell}z_{i\ell}=0$. Der gemeinsame effektive
Kreuzkernel $K$ enthaelt die im Code festgelegte Deposition. Schreibe
$g=\nabla K$, $J=D^2K$, $T=D^3K$; bei einem geraden radialen $K$ sind
$g,T$ ungerade und $J$ gerade. Der native Kreuzdrift ist $b_i^\times
=-\chi G_{i\leftarrow j}$. Taylorentwicklung **um $R$, nicht um null**:

$$
\begin{aligned}
\frac{G_{A\leftarrow B}}{W_B}
 &=g(R)+J(R)u_A+\tfrac12T(R):(u_Au_A^T+\Sigma_B)+r_A,\\
\frac{G_{B\leftarrow A}}{W_A}
 &=-g(R)+J(R)u_B-\tfrac12T(R):(u_Bu_B^T+\Sigma_A)+r_B.
\end{aligned}
$$

Hier bezeichnet $[T:M]_a=\sum_{bc}T_{abc}M_{bc}$ eine Vektorkontraktion.
Die **quellen-normalisierte Unwucht** ist daher exakt

$$
\mathcal D:=\frac{G_{A\leftarrow B}}{W_B}
+\frac{G_{B\leftarrow A}}{W_A}
=J(R)(u_A+u_B)
+\tfrac12T(R):(u_Au_A^T-u_Bu_B^T+\Sigma_B-\Sigma_A)+r_A+r_B.
$$

Schon der aktuelle Punktversatz erzeugt einen Term erster Ordnung.
Bei $u_A=u_B=0$ bleibt die Differenz der Quellformtensoren. Gleicher
rms-Radius, also gleiche Spur von $\Sigma$, bestimmt diese Antwort nicht.
Eine feste 90-Grad-Drehung einer anisotropen Quelle aendert sie bereits
bei unveraenderter Groesse. Ein Ausloeschen der gezeigten Terme zweiter
Ordnung beweist noch keine exakte Balance aller hoeheren Momente.

Der Monopolterm hat formal das gemeinsame Potential
$U_0(R)=\chi W_AW_BK(R)$. Definiere fuer den gesamten Kreuzdrift die
**deklarierte** Normierung $F_i=W_i b_i^\times$. Nur ihre Monopolanteile
sind die Kraefte aus $U_0$; insgesamt gilt
$F_A+F_B=-\chi W_AW_B\mathcal D$. Dies ist keine unabhaengige
Bestimmung physikalischer Mobilitaeten oder Massen. Fuer die gepaarte
Ein-Schritt-Centerantwort gilt weiterhin
$\delta_\times c_i=\beta_i\delta_\times x_i$ mit
$\beta_i=w_{i0}/W_i$: Der entsprechende deklarierte Centerfaktor ist
$\beta_i/W_i$, nicht automatisch derselbe Punktfaktor $1/W_i$.

## 2. Kontrollierter Rest und Grenze der Punktnaeherung

Setze $s_A=|u_A|+\max_\ell|z_{B\ell}|$ und
$m_{3,A}=\sum_\ell p_{B\ell}|u_A-z_{B\ell}|^3$. Mit
$M_k(R,s)=\sup_{|v-R|\leq s}\|D^kK(v)\|$ in multilinearer Operatornorm
folgen direkt aus dem Taylorrest

$$
|r_A|\leq\frac{M_4(R,s_A)}6m_{3,A},\qquad
\left|\frac{G_{A\leftarrow B}}{W_B}-g(R)\right|
\leq\|J(R)\|\,|u_A|
+\frac{M_3(R,s_A)}2\bigl(|u_A|^2+\operatorname{tr}\Sigma_B\bigr).
$$

Die B-Schranken folgen durch Austausch und $R\mapsto-R$.
Fuer $K(v)=\sum_m A_m e^{-|v|^2/(2\sigma_m^2)}$ sind verwendbare,
gegebenenfalls grobe Schranken explizit. Mit
$d_-=(|R|-s)_+$ und $d_+=|R|+s$:

$$
\begin{aligned}
M_3(R,s)&\leq\sum_m|A_m|e^{-d_-^2/(2\sigma_m^2)}
\left(\frac{d_+^3}{\sigma_m^6}+\frac{3d_+}{\sigma_m^4}\right),\\
M_4(R,s)&\leq\sum_m|A_m|e^{-d_-^2/(2\sigma_m^2)}
\left(\frac{d_+^4}{\sigma_m^8}+\frac{6d_+^2}{\sigma_m^6}
+\frac3{\sigma_m^4}\right).
\end{aligned}
$$

Die Faktoren 3 bzw. 6 und 3 kommen aus den symmetrisierten Kronecker-
Termen der dritten und vierten Gaussableitung.
Die Schranken sind dimensionsunabhaengig. Sie garantieren einen
**absoluten**, nicht automatisch kleinen oder relativen Fehler.

Bei Gausskerneln reicht insbesondere "Quellradius viel kleiner als
Abstand" nicht fuer eine gute relative Punktnaeherung. Eine normierte
Quelle aus zwei Punkten $\pm\rho$ auf einer Achse und
$K(r)=e^{-r^2/(2\sigma^2)}$ liefert fuer $R>\rho$

$$
\frac{\tfrac12[g(R-\rho)+g(R+\rho)]}{g(R)}
=e^{-\rho^2/(2\sigma^2)}
\left[\cosh\frac{R\rho}{\sigma^2}
-\frac\rho R\sinh\frac{R\rho}{\sigma^2}\right].
$$

Bei festem $\rho>0$ waechst dieses Verhaeltnis fuer $R\to\infty$, obwohl
$\rho/R\to0$ und beide Antworten absolut verschwinden. Die relevante
Variation enthaelt $R\rho/\sigma^2$, nicht nur $\rho/R$. Bei einer
Kernelmischung koennen zusaetzlich Nullstellen durch Termaufhebung
auftreten; relative Fehler brauchen deshalb eine untere Schranke auf
das verglichene Signal. Keine Wiederherstellung eines Coulomb-Schwanzes.

## 3. Wann Mittelung eine reziproke Wolkenwirkung ergibt

Hier sind $C_A,C_B$ **festgehaltene Referenzcenter** und
$R=C_A-C_B$. Sie sind nicht mit den momentanen, im Inneren eventuell
oszillierenden Memory-Centern $c_i$ aus Abschnitt 1 gleichgesetzt.
Schreibe konsistente Historien als
$x_i(n)=C_i+v_i(n)$, $y_{i\ell,n}=C_i+v_i(n-\ell)$.
Nehme einen gemeinsam stationaeren inneren Prozess an und definiere

$$
\mathcal G_\ell(R)=\mathbb E\,g(R+v_A(n)-v_B(n-\ell)),
\qquad \ell\in\mathbb Z.
$$

Aus Stationaritaet und Ungeradheit von $g$ folgt ohne Unabhaengigkeit

$$
\boxed{\overline{\mathcal D}
=\sum_\ell p_{B\ell}\mathcal G_\ell(R)
-\sum_\ell p_{A\ell}\mathcal G_{-\ell}(R).}
$$

Identische Altersgewichte und $\mathcal G_\ell=\mathcal G_{-\ell}$
genuegen fuer diese mittlere Balance. Stationaritaet allein garantiert
die zweite Bedingung nicht. Bei ungleichen Altersgewichten reicht
selbst diese Lagsymmetrie nicht, solange $\mathcal G_\ell$ vom Lag abhaengt.

Eine staerkere, einfache hinreichende Annahme ist Unabhaengigkeit der
beiden inneren Prozesse zu allen beteiligten Lags, mit stationaeren
Randverteilungen $P_A,P_B$. Dann ist fuer jeden Lag

$$
\mathcal G_\ell(R)=\bar g(R)
=\iint g(R+a-b)\,dP_A(a)\,dP_B(b),
$$

und $\overline{\mathcal D}=0$ auch bei verschiedenen Altersgewichten.
Bei fuer die Ableitung **festgehaltenen Verteilungen** besitzt diese
mittlere Antwort das deklarierte Potential

$$
\bar U(R)=\chi W_AW_B\iint K(R+a-b)\,dP_A(a)\,dP_B(b),\qquad
\bar F_A=-\nabla_R\bar U=-\bar F_B.
$$

Das ist gerade die bekannte Wolken-Wolken-Faltung, die
[`rigid_full_memory_pair_interaction`](https://github.com/MemoryDynamics/Knoten/blob/19195a3504a860278d9514a3140cf982fee85dbb/src/emergenz_knoten/quasistatic_pair.py)
bereits als separates statisches Kopplungsgesetz auswertet. Neu ist hier
nur die bedingte Zuordnung zur gemittelten **nativen** Kreuzantwort.
Weder die Faltung noch die allgemeine Idee statistischer Mittelung wird
als neue Theorie beansprucht. Einsetzen der Wolkenkopplung in den nativen
Simulator waere weiterhin eine Modellentscheidung, keine durch diese
Rechnung genehmigte Aenderung.

Fuer Abweichungen vom Produktvergleich gilt unmittelbar die Diagnose

$$
|\overline{\mathcal D}|
\leq\sum_\ell p_{B\ell}|\mathcal G_\ell-\bar g|
+\sum_\ell p_{A\ell}|\mathcal G_{-\ell}-\bar g|.
$$

Diese Groessen sind im gekoppelten Zustand zu bestimmen. Ihre Kleinheit
folgt weder aus einem kleinen Radius noch aus stationaeren Einzelwolken.
Auch eine reziproke mittlere Antwort allein muss nicht der Produktfaltung
entsprechen: Zeitkorrelationen koennen ihren Betrag veraendern, ohne
eine Unwucht zu erzeugen.

## 4. Positive Kontrolle und stationaere Gegenprobe

Die positive Softwarekontrolle mittelt unabhaengig ueber einen Vier-
und einen Sechsphasenzyklus, mit verschiedenen Formen, Quellengewichten
und optional verschiedenen Altersgewichten. Alle 24 Phasenpaare gehen
ein. Die native Feldsumme stimmt nach deklarierter Normierung mit der
vorhandenen Wolkenkopplung ueberein. Das ist ein endliches stationaeres
**Produktensemble**, kein Nachweis, dass eine einzelne native Bahn dieses
Ensemble abtastet. Schon die beiden kommensurablen Zyklen erfordern fuer
ein solches Zeitmittel eine gesonderte Ergodizitaets-/Mischungspruefung.

Die Gegenprobe verwendet zwei gleich grosse Vierphasenzyklen mit
$v_A(n)=a(\cos\theta_n,\sin\theta_n,0)$,
$\theta_n=\theta_0+n\pi/2$, und $v_B(n)=v_A(n+1)$.
Die gemeinsame Anfangsphase ist gleichverteilt. Beide Einzelverteilungen
und der gemeinsame Prozess sind stationaer. Fuer $H=2$ gilt jedoch

$$
\mathcal G_1(R)=g(R),\qquad
\mathcal G_{-1}(R)=\frac14\sum_{k=0}^3g(R+2a e_k),\qquad
e_k=(\cos(k\pi/2),\sin(k\pi/2),0).
$$

Bei gleichen Altersgewichten bleibt
$\overline{\mathcal D}=p_1(\mathcal G_1-\mathcal G_{-1})$ im Allgemeinen
ungleich null. Der feste Test mit $a=0.35$, $R=(2,0.4,0.1)$,
$K=e^{-|r|^2/2}-3e^{-|r|^2/8}$ und nativen H=2-Gewichten bei
$\alpha=1/2$ bestaetigt diese Identitaet. Ohne relative Phasenverschiebung
verschwindet die Unwucht, der Betrag stimmt aber noch nicht mit dem
unabhaengigen Produktvergleich ueberein.
**Diese vorgegebenen Zyklen sind keine nachgewiesenen Loesungen der
nativen Dynamik und kein neuer FIFO-Kreis- oder Stabilitaetslauf.**

## 5. Was fuer einen dynamischen Abschluss noch kontrolliert werden muss

Festgehaltene Center sind eine zusaetzliche Naeherung. Fuer eine bewegte
Quellreferenz $C_B(n)$ tritt im echten Abstand der Zusatz
$C_B(n)-C_B(n-\ell)$ auf. Die globale Hessianschranke fuer Gaussmischungen
$L_2=\sum_m|A_m|/\sigma_m^2$ liefert

$$
\left|\frac{G_{A\leftarrow B}^{\rm echt}-G_{A\leftarrow B}^{\rm frozen}}{W_B}\right|
\leq L_2\sum_\ell p_{B\ell}|C_B(n)-C_B(n-\ell)|
\leq L_2 V_B\sum_\ell p_{B\ell}\ell,
$$

falls $|C_B(n+1)-C_B(n)|\leq V_B$. Der Memory-Horizont allein ist also
kein Separationsparameter; wichtig ist die Bewegung ueber die
gewichteten Alterslags. Zwei synthetische Kontrollen pruefen den Null-
und einen nichttrivialen Bewegungsfall. Die Schranke kontrolliert nur
das Einfrieren innerhalb der Historie, noch keinen langen Mittelungs-
oder Bahnfehler.

Ebenso duerfen abstandsabhaengige innere Verteilungen $P_i(R)$ nicht
stillschweigend in die obige Potentialableitung eingesetzt werden:
Die Ableitung von $\bar U$ erhaelt dann weitere Verteilungsableitungen.
Eine begruendete Potential-of-mean-force-Konstruktion waere gesondert
noetig. Gemeinsame Stationaritaet, Mischung, kontrollierte Langzeitreste,
physikalische Kraftnormierung und die FIFO-/Mediumsenergie bleiben
offen. Das neue Mittelungsresultat liefert insbesondere keine
Traegheitsmasse, Ladungsquantisierung, Wasserstoffbindung oder Gravitation.

## 6. Literatur und Verifikation

[Ivlev et al., Physical Review X 5, 011035 (2015), Abschnitt II A](https://journals.aps.org/prx/pdf/10.1103/PhysRevX.5.011035)
konstruieren fuer eine spezielle konstante Nichtreziprozitaet einen
Pseudo-Hamiltonian durch Umnormierung von Massen und Wechselwirkungen.
Das ist ein wichtiger Vergleich fuer unsere deklarierte Normierung,
kein Satz ueber den vorliegenden Historienprozess. Unsere Form-/Lagreste
sind im Allgemeinen keine konstanten skalaren Asymmetrieparameter.

[Shi, Moessner, Alert und Bukov, Nature Physics 22, 1350-1359 (2026)](https://pmc.ncbi.nlm.nih.gov/articles/PMC13461368/)
geben eine Hamilton-Einbettung mit Hilfsvariablen und erhaltenem Constraint
an. Im dort erlaeuterten XY-Beispiel verschwindet der Hamiltonian auf
dem Constraint identisch: Er erzeugt die Dynamik, ist aber nicht die
Energie des urspruenglichen Systems. Das bestaetigt die notwendige
Trennung von formaler Hamiltonstruktur und physikalischer Energie.
Geprueft wurden Einleitung und Abschnitt "Constrained Hamiltonian
embedding", nicht der allgemeine Supplementbeweis oder eine Anwendung
auf unseren diskreten FIFO. Eine solche Einbettung waere noch keine
Herleitung von Quantentheorie oder eines physikalischen Mediums.

[Zehn synthetische Tests](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_memory_pair_finite_separation.py)
pruefen Form-/Restformeln und Ein-Schritt-Zuordnung in 3D/Punktdeposition
und 5D/Gaussdeposition, dritte Ableitungen gegen unabhaengige
Hessiandifferenzen, gleiche Radien bei verschiedener Form, die relative
Gaussfernfehlerkontrolle, bewegte Quellen und die beiden Arten der
Phasenmittelung. Kein Parameterscan, kein neuer stabiler Knoten, kein
physikalischer Teilchenbefund.

Verifikation am 2026-10-29: **133 betroffene Tests bestanden in 3.38 s**,
einschliesslich der zehn neuen Kontrollen, bisherigen Paar-/Kernel- und
Wolkenkopplungstests, AL1-Archivchecks und Dokumentationsregressionen.
Lint und strikter MkDocs-Bau bestehen. Keine vollstaendige Repository-
Testsuite und kein dynamischer Mittelungsnachweis. Produktionsregel,
Paper I und archivierte Zielbefunde bleiben unveraendert.
Die einzige aktive Arbeitsreihenfolge steht in den
[Projektprioritaeten](../status/project_priorities.md).
