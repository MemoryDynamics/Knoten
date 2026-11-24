# Endliche Bahnschranke fuer das symmetrische Memory-Paar

Stand: 2026-11-01. Analytische Fortsetzung des
[Geometrie-/Statistikanschlusses](memory_pair_geometry_statistics_2026-11-01.md).
Keine Zielsimulation, kein Replay, keine neuen Zufallszahlen, keine
Parametersuche. Der gespeicherte Anfangszustand wird einmal eingelesen.

## Ergebnis und Grenze

Fuer identische, reziprok gekoppelte Knoten mit dem alten attraktiven
Gausskernel laesst sich eine endliche Hochwahrscheinlichkeits-Schranke
aus der unveraenderten Dynamik ableiten. Nichtlinearitaet und endlicher
FIFO-Rand werden eingeschlossen, nicht weggelassen. Die festen
Auswertungswerte sind vor der Rechnung **N=50000, S=0.01, z=10**.

Die numerische Auswertung der unten bewiesenen Bedingung liefert
`0.008172970685054261 < 0.01`, mit einem inneren Offsetbudget
`U=0.0037830430577533154`. Die Vereinigungsabschaetzung ergibt
`delta=3.5006809740545107e-14` fuer eine ganze Bahn. Dies betrifft das
**exakt reell gerechnete Modell mit unabhaengigen idealen Gaussinnovationen**.
Die eingesetzten Konstanten sind mit binary64 ausgewertet, nicht durch
gerichtete Intervalle eingeschlossen. Insbesondere ist dies kein
Rundungs-/PRNG-Zertifikat des nativen Simulators und keine nachtraegliche
Wahrscheinlichkeitsaussage ueber die schon ausgefuehrten Seeds.

Fuer den zuvor definierten, nichtlinearen Replikationskontrast sinkt das
bedingte Betragsbudget von global 15.37 auf etwa `7.60e-7`. Die beispielhafte
simultane 95-Prozent-Halbbreite fuer zwei disjunkte Paare und sechs
Koordinaten betraegt trotzdem `1.78e-6`, also mehr als dieses Betragsbudget.
**Dieser konkrete kleine Hoeffding-Test koennte null selbst bei maximalem
beobachtetem Kontrast nicht ausschliessen.** Das ist keine allgemeine
untere Schranke fuer erforderliche Laufzahlen und keine Poweranalyse
eines besseren Schaetzers. Keine automatische Panelvergroesserung.

Die Schranke kontrolliert lokale Paar-/Memory-Abstaende, nicht den
absoluten gemeinsamen Ort. Keine Stationaritaet, asymptotische Bindung,
Unabhaengigkeit der beiden Knoten, physikalische Masse, Energie,
Teilchenidentifikation oder Quantenmechanik folgt daraus.

## 1. Annahmen und exakte Aufspaltung

Gleiche positive geometrische Gewichte, gleiche Selbst-/Kreuzkernel,
gleiche Rauschstaerke und synchrone reziproke Abfrage seien vorausgesetzt:

$$
q=1-\alpha,\quad w_l=M\alpha q^l,\quad W=M(1-q^H),\quad
\beta=\frac{\alpha}{1-q^H},\quad \theta=\beta q^H.
$$

Es gelten $0<\alpha\leq1$, $H\geq1$, $M>0$, $0<\chi\leq\eta$ und
$\epsilon\geq0$. Anfangspunkte und gefuellte Historien sind deterministisch
festgelegt. Insbesondere muss $x_i(0)$ nicht gleich $Y_{i,0}$ sein.
Die Innovationen $\xi_{i,n}$ sind ueber Knoten, Zeit und Koordinaten
unabhaengige Standardnormalvariablen. Eine zufaellige Vorbereitung darf
nur nach expliziter Konditionierung auf einen gemeinsamen festen
Checkpoint verwendet werden; shared random preparations sind nicht
automatisch unabhaengige Replikationen.

Schreibe den effektiven Kernel, nach etwaiger Depositionsfaltung, als

$$
K(r)=A_r e^{-r^2/(2\sigma_r^2)}-A_a e^{-r^2/(2\sigma_a^2)},\quad
0<\sigma_r\leq\sigma_a,\quad A_r\geq0,\quad A_a>0,
$$

$$
\kappa=A_a/\sigma_a^2-A_r/\sigma_r^2>0,\quad
C_3=\tfrac12(A_r/\sigma_r^4+A_a/\sigma_a^4),\quad
L=(\eta+\chi)WC_3.
$$

Dann ist $\nabla K(z)=k(|z|)z$, mit $0<k(r)\leq A_a/\sigma_a^2$.
Dies folgt aus der Ordnung der Breiten und dem positiven Koeffizienten
am Ursprung, nicht aus einer lokalen Taylornaeherung. Vorausgesetzt sei

$$
(\eta+\chi)W A_a/\sigma_a^2\leq1.
$$

Damit ist jeder rauschfreie native Punktschritt eine konvexe Kombination
des alten Punktes und beider Historien. Setze
$g=\eta\kappa W$, $h=\chi\kappa W$, $s=1-g-h$ und $\lambda=qs$.
Es gilt $s\geq0$, $g\geq h>0$, $0\leq\lambda<1$.
Aus der [exakten FIFO-Identitaet](../../docs/reference/memory_pair_reduction.md):

$$
x_i^+=s x_i+g c_i+h c_j+\epsilon\xi_i+R_i,\qquad
c_i^+=q c_i+\alpha x_i^++t_i,\quad t_i=\theta(x_i^+-o_i).
$$

Solange der Durchmesser des gesamten aktuellen Pools aus beiden Punkten
und beiden Historien hoechstens $S$ ist, gilt $|R_i|\leq LS^3$.
Bei $|\epsilon\xi_i|\leq b$ liefert die globale Konvexitaet zudem
$|t_i|\leq\theta(S+b)=:T$. Hier ist **keine** bereits bewiesene
Schranke fuer den neuen Zustand eingesetzt; das vermeidet einen
Zirkelschluss beim ersten Austritt.

Fuer gemeinsame und relative Variablen

$$
X=(x_A+x_B)/2,\quad C=(c_A+c_B)/2,\quad V=X-C,\quad
D=x_A-x_B,\quad E=c_A-c_B
$$

und $B_\pm=(\epsilon\xi_A+R_A)\pm(\epsilon\xi_B+R_B)$,
$t_\pm=t_A\pm t_B$ gilt exakt:

$$
V^+=\lambda V+qB_+/2-t_+/2,\qquad
C^+=C+\alpha(sV+B_+/2)+t_+/2,
$$

$$
\begin{pmatrix}D^+\\E^+\end{pmatrix}
=A\begin{pmatrix}D\\E\end{pmatrix}
+\begin{pmatrix}1\\\alpha\end{pmatrix}B_-
+\begin{pmatrix}0\\1\end{pmatrix}t_-,\qquad
A=\begin{pmatrix}s&g-h\\\alpha s&q+\alpha(g-h)\end{pmatrix}.
$$

Beide Zeilensummen von $A$ sind strikt kleiner als eins und die Eintraege
nichtnegativ. Somit ist $A$ stabil. Die Summe seiner nichtnegativen
Propagatoren ergibt

$$
(I-A)^{-1}\binom{1}{\alpha}=\frac1{2h}\binom11,\qquad
(I-A)^{-1}\binom01=\frac1{2\alpha h}\binom{g-h}{g+h}.
$$

## 2. Lineare Gaussantwort, ohne eine Bahn zu erzeugen

Der Vergleichsprozess hat denselben Anfangszustand und dieselben
Innovationen, aber $R=t=0$. Er dient nur der Fehlerzerlegung. Er ist
nicht der behauptete Ersatz fuer die volle nichtlineare FIFO-Dynamik.
Seine zentrierte Relativkovarianz wird gleichmaessig in der Zeit durch
die stationaere Vergleichsmatrix $P$ beschraenkt:

$$
P=APA^T+2\epsilon^2 vv^T,\qquad v=(1,\alpha)^T.
$$

Die Loesung ist die konvergente Reihe $\sum_{j\geq0}A^j
(2\epsilon^2vv^T)(A^T)^j$. Endlich gestartete Kovarianzen sind deren
Teilsummen. Das setzt **keine Stationaritaet des nativen Paars** voraus.
Der Rechner verwendet `scipy.linalg.solve_discrete_lyapunov`;
Tests vergleichen mit einer unabhaengig aufsummierten Impulsreihe.

Die gemeinsame Innovation hat pro Koordinate Varianz $\epsilon^2/2$.
Fuer $X$ ist ihre Impulsantwort

$$
w_j=a_0+a_1\lambda^j,\qquad
a_0=\frac{\alpha}{1-\lambda},\quad
a_1=\frac{q(g+h)}{1-\lambda},\quad a_0+a_1=1.
$$

Fuer jeden Lag $1\leq\ell\leq H$ wird die Varianz von $X_n-X_{n-\ell}$
durch

$$
V_X(\ell)=\frac{\epsilon^2}{2}\left[
a_0^2\ell+\frac{2a_0a_1(1-\lambda^\ell)}{1-\lambda}
+\frac{2a_1^2(1-\lambda^\ell)}{1-\lambda^2}\right]
\leq V_X(H)
$$

beschraenkt. Herleitung: neue Impulse geben $\sum_{j<\ell}w_j^2$,
aeltere $\sum_{j\geq0}(w_{j+\ell}-w_j)^2$; die zweite Summe bis
unendlich zu verlaengern vergroessert die Varianz. Zeitliche
Unabhaengigkeit der resultierenden Inkremente wird nicht behauptet.
Da gemeinsame und relative Gaussinnovation unabhaengig sind, gilt fuer
den inneren Offset $u_i=x_i-c_i=V\pm(D-E)/2$ die Varianzschranke

$$
V_u=\frac{\epsilon^2q^2}{2(1-\lambda^2)}
+\tfrac14(1,-1)P(1,-1)^T.
$$

## 3. Anfangshistorie und simultanes Ereignis

Setze mit den tatsaechlichen Anfangshistorien

$$
d_0=\max\{|D_0|,|E_0|,\max_l|Y_{A,l}-Y_{B,l}|\},\quad
e_0=\max_l|(Y_{A,l}+Y_{B,l})/2-X_0|,\quad v_0=|V_0|.
$$

Die deterministische relative Vergleichsantwort ist durch $d_0$
beschraenkt. Jede gemeinsame deterministische Verschiebung zwischen
nichtnegativen Zeiten ist hoechstens $(g+h)v_0/(1-\lambda)$.
Die zusaetzlichen $2e_0$ erfassen zwei Anfangsdeposits; ein gemischtes
Paar aus neuem Punkt und Anfangsdeposit braucht nur $e_0$ und einen
Lag gegen $X_0$. Solche gemischten Paare existieren nur waehrend der
ersten $H$ Updates. Deshalb genuegt dieselbe Lagvarianzschranke.

Betrachte fuer $n=1,\ldots,N$ alle zentrierten Koordinaten von $D_n$,
beiden $u_{i,n}$, beiden rohen Innovationen und den gemeinsamen
Inkrementen mit $1\leq\ell\leq\min(H,n)$. Es sind hoechstens
$K=Nd(H+5)$ skalare Gaussgroessen. Aus exponentieller Markov-Ungleichung
und $\mathbb E e^{tZ}=e^{t^2/2}$ folgt
$\Pr(|Z|>z)\leq2e^{-z^2/2}$. Die Vereinigungsabschaetzung liefert ein
simultanes Ereignis mit Fehlerwahrscheinlichkeit

$$
\delta=\min\{1,2Nd(H+5)e^{-z^2/2}\}.
$$

Keine Unabhaengigkeit zwischen den $K$ Groessen ist erforderlich.
Auf diesem Ereignis sind alle Innovationsnormen durch
$b=\epsilon z\sqrt d$ beschraenkt, und fuer den linearen Vergleich
genuegt das Pooldurchmesserbudget

$$
S_{\rm lin}=d_0+2e_0+\frac{g+h}{1-\lambda}v_0
+z\sqrt d\,[\sqrt{P_{00}}+\sqrt{V_X(H)}].
$$

## 4. Nichtlinearer Abschluss durch ersten Austritt

Bis einschliesslich des ersten moeglichen Austrittsschritts folgt aus
den positiven Resolventen und $|R_i|\leq LS^3$, $|t_i|\leq T$:

$$
|D-D^{\rm lin}|\leq\frac{LS^3}{h}
+\frac{g-h}{\alpha h}T=:B_D,
$$

$$
|E-E^{\rm lin}|\leq\frac{LS^3}{h}
+\frac{g+h}{\alpha h}T,
\qquad
|V-V^{\rm lin}|\leq\frac{qLS^3+T}{1-\lambda}.
$$

Schreibe die gemeinsame Stoerung als $X^{\rm err}=C^{\rm err}+V^{\rm err}$.
Die Summe von hoechstens $H$ Centerinkrementen plus zwei $V$-Endpunkten
beschraenkt ihre Lagdifferenz durch

$$
B_X=\frac{H\alpha+2q}{1-\lambda}LS^3+
\left[H\left(1+\frac{\alpha s}{1-\lambda}\right)
+\frac2{1-\lambda}\right]T.
$$

Anfaengliche Deposits besitzen Stoerung null. Fuer gemischte Paare gilt
derselbe Ausdruck, da deren positive Zeit hoechstens $H$ betraegt.
Mit $|x_i(k)-x_j(l)|\leq|X(k)-X(l)|+(|D(k)|+|D(l)|)/2$ folgt:

$$
\boxed{S_{\rm lin}+B_D+B_X<S.}
$$

Wenn diese feste Bedingung gilt, liegt bereits der Anfangspool unter
$S$, und auch der vermeintlich erste Austrittspunkt samt verbleibender
Historie liegt strikt darunter. Widerspruch. Daher bleibt der ganze
Pool fuer alle $0\leq n\leq N$ innerhalb des Durchmesserbudgets, ausser
auf einem Ereignis von Wahrscheinlichkeit hoechstens $\delta$.

Dasselbe Ereignis liefert

$$
|u_{i,n}|\leq U:=v_0+d_0+z\sqrt{dV_u}
+\left[\frac q{1-\lambda}+\frac1h\right]LS^3
+\left[\frac1{1-\lambda}+\frac g{\alpha h}\right]T.
$$

Dies ist eine endliche Nichtaustrittsschranke. $X$ kann trotzdem
diffundieren; weder absolute Einschliessung noch unendliche Lebensdauer
oder ein stationaeres Mass ist bewiesen.

## 5. Statistik ohne nachtraegliche Auswahl guter Laeufe

Sei $D^{\rm rep}$ der bereits definierte Kontrast aus zwei unabhaengigen
gesamten Paarlaeufen, bei gleichem festen Referenzabstand $R_*$ und festem
Zeit-/Lagfenster nach vollstaendigem Ersatz der Anfangshistorie.
Sein linearer Anteil verschwindet exakt. Global gilt
$|D^{\rm rep}|\leq2M_g$, mit
$M_g=e^{-1/2}(A_r/\sigma_r+A_a/\sigma_a)$.

Definiere das **beobachtbare** Ereignis $F$ durch Einhaltung beider
Pool-/Offsetbudgets ueber den ganzen vorgegebenen Horizont. Das oben
verwendete Gaussereignis impliziert $F$, also $\Pr(F^c)\leq\delta$.
Ein spaeterer Runner muesste diese Kriterien fuer jeden Lauf speichern.
Fuer jedes vorher festgelegte disjunkte Replikationspaar definiere

$$
Y=D^{\rm rep}\,1_{F_1\cap F_2}.
$$

Bei Verletzung wird **null eingesetzt, nicht das Paar entfernt**.
Damit bleiben die Anzahl und die Unabhaengigkeit der Paare erhalten.
Auf $F_1\cap F_2$ haben auch gekreuzte Readouts Abstaende hoechstens
$|R_*|+2U$. Die kubische Restschranke und lineare Aufhebung ergeben

$$
|Y|\leq B:=\min\{2C_3(|R_*|+2U)^3,2M_g\},\quad
|\mathbb ED^{\rm rep}-\mathbb EY|\leq2M_g\min(1,2\delta).
$$

Fuer $m$ disjunkte unabhaengige Paare und $J$ vorab bestimmte skalare
Koordinaten ist eine simultane zweiseitige Halbbreite

$$
2B\sqrt{\frac{\log(2J/a)}{2m}}+2M_g\min(1,2\delta)
$$

bei Fehlerwahrscheinlichkeit hoechstens $a$. Die erste Summe ist die
bekannte Hoeffding-Ungleichung fuer Intervalle $[-B,B]$, die zweite die
unkonditionierte Trunkierungsverzerrung. Es wird nicht auf beobachteten
Erfolg konditioniert und kein seltener Ausreisser ohne Kosten ignoriert.
Rundungsfehler sind hier noch nicht addiert.

## 6. Reproduzierbare Auswertung und Grenzen

[JSON mit Hashes und allen Konstanten](memory_pair_path_envelope_2026-11-01.json),
[reiner Rechner](../../src/emergenz_knoten/pair_path_envelope.py),
[Archivauswertung](../../experiments/current/reference/memory_pair_path_envelope.py),
[synthetische Tests](../../tests/test_pair_path_envelope.py).

| Groesse | Numerische Auswertung |
| --- | ---: |
| Konvexitaetskoeffizient | 0.6088534882 |
| Lineares Durchmesserbudget | 0.00740938637 |
| Relative Stoerung | 0.00058866158 |
| Gemeinsame Lagstoerung | 0.00017492274 |
| Abstand zur Abschlussgrenze | 0.00182702931 |
| Maximale Differenz gespeicherter/berechneter geometrischer Gewichte | 1.735e-18 |
| Trunkierungsverzerrung des Kontrasts | 1.076e-12 |

Die kleine Gewichtsdifferenz ist ausgewiesen, aber kein Ersatz fuer einen
vollstaendigen Rundungsnachweis. Der Satz benutzt exakt geometrische
Gewichte; das Beispiel deutet die endlichen gespeicherten Koordinaten
als feste reelle Anfangswerte. Die numerische Auswertung und 18 kleine
Tests pruefen Identitaeten, Impulsantwort/Kovarianz, Anfangsdeposits,
Translationsinvarianz, unzulaessige Parameter und Nichtabschluss. Die
nativen Kontrollen sind zwei konstruierte H=30-Faelle mit je sieben
Updates, keine Fortsetzung des H=600-Zielzustands.

Verifikation: 190 betroffene Tests bestanden (einschliesslich dieser 18),
vollstaendige konfigurierte Ruff-Pruefung und strikter MkDocs-Build
bestanden. Diese Softwarechecks ersetzen nicht die oben offengelegte
fehlende gerichtete numerische Einschliessung.

Der naechste wissenschaftliche Engpass ist damit konkreter: Vor einem
neuen Panel muss die **aufzuloesende nichtlineare Kontrastgroesse**
begruendet werden. Eine analytische fuehrende Korrektur am linearen
Gaussvergleich ist dafuer sinnvoller als eine blinde Erhoehung der
Laufzahl. Ein belastbares Ausfuehrungsprotokoll braucht daneben die
Uebertragung auf numerische Arithmetik, festgelegte Fenster und
Ausfallbehandlung. Keine neuen Runs sind mit diesem Bericht freigegeben.

## Quellen und Prueftiefe

Die modellspezifische Aufspaltung und Nichtaustrittsbedingung sind oben
hergeleitete Analyse, kein aus der Literatur uebernommener FIFO-Satz.
Verwendet werden nur elementare Standardbausteine:

- [Shalizi, Lecture 5, 2021](https://www.stat.cmu.edu/~cshalizi/sml/21/lectures/05/lecture-05.html):
  Abschnitte exponentielle Markov-Ungleichung und Gauss-MGF gelesen;
  daraus hier die zweiseitige Gauessche Tail- und Vereinigungsabschaetzung.
- [SciPy: solve_discrete_lyapunov](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve_discrete_lyapunov.html):
  offizielle Gleichungskonvention $APA^T-P+Q=0$ geprueft. Lokal
  SciPy 1.16.3; die versionsspezifische Webadresse war nicht abrufbar.
  Die Konvention wird ausserdem direkt durch die Tests geprueft.
- [Hoeffding 1963, Originalartikel](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf):
  Theorem 2 in der im vorherigen Bericht offengelegten OCR-Prueftiefe;
  keine erneute Volltextpruefung beansprucht. Die Anwendung benutzt
  unabhaengige ganze Replikationspaare, keine abhaengigen Zeitschritte.
