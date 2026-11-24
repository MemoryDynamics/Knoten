# Passiver Rauschvergleich fuer endliche Memory-Paare

Stand: 2026-11-21. Anschluss an den [Abgleich weisser Anstoesse](memory_pair_white_noise_2026-11-21.md).
Analytischer Referenztest, keine neue Badkopplung, kein Ziellauf.

**Befund.** Mit einem explizit deklarierten Arbeitsanschluss kann man
fuer zwei FIFO-Speicherplaetze ein positives, zeitlich korreliertes
Rauschspektrum aus der linearen Paarantwort bestimmen. Bis auf eine
gemeinsame Skala ist dieses Spektrum durch das Vergleichskriterium
festgelegt. Laengere, langsam vergessende FIFO-Kanaele koennen am
selben Anschluss bei manchen Frequenzen aktiv sein: Dann ist ein
passives Bad ausgeschlossen, auch wenn sein Rauschen zeitlich
beliebig korreliert sein darf. Nicht jede endliche Retention ist
davon betroffen.

## 1. Zeitindex und deklarierter Arbeitsanschluss

Verwende dieselbe attraktive lineare Geometrie wie im
[Paartransfer](memory_pair_dynamic_reciprocity_2026-11-21.md), mit
$g_i,h_i>0$, $s_i=1-g_i-h_i\ge0$ und gemeinsamen endlichen H.
Die Mittelpunktvariation $c_i(n)$ liest die normierten
$P_i(z)=\sum_{\ell=0}^{H-1}q_i^\ell z^{-\ell}/\sum_\ell q_i^\ell$,
$0<q_i<1$. Der Antrieb $+\mu_i F_i(n)$ wird am Kopf des
Updates $n\to n+1$ addiert. Als Vergleichsarbeit gilt
$F_i(n)[c_i(n+1)-c_i(n)]$. Das ist **derselbe** Update,
nicht der bereits vorher abgeschlossene Schritt. Der Center-
Arbeitsport ist deklariert, nicht mikroskopisch nachgewiesen;
siehe den [Aktuatorabgleich](../../docs/reference/scalar_memory_center_filter.md#8-center-konjugierte-aktuatorarchitektur).

Setze $u_i(n)=c_i(n+1)-c_i(n)$, $D=\operatorname{diag}(\mu_A,\mu_B)$
und $A_i(z)=(z-s_i)/P_i(z)-g_i$ wie zuvor. Mit
$\mathcal A_{ii}=A_i,\ \mathcal A_{ij}=-h_i$ folgt exakt die
inverse Antriebsantwort

$$
Z(z)u(z)=F(z),\qquad Z(z)=\frac{D^{-1}\mathcal A(z)}{z-1}.
$$

Die Wahl $h_A/\mu_A=h_B/\mu_B=\kappa>0$ macht Z symmetrisch
(im Sinne der Transposition). Die gemeinsame freie Translation
verhindert keine stationaeren Inkremente. Auf dem Einheitskreis
betrachten wir z ungleich 1, so dass $Y=Z^{-1}$ existiert:
Die History-Matrix hat abgesehen von der Translation alle
Eigenwerte strikt im Einheitskreis, wie im Zeitumkehrtest gezeigt.

Fuer einen harmonischen anliegenden Kraftvektor f ist die
gemittelte deklarierte Arbeit proportional zu
$\operatorname{Re}(f^\dagger Y f)$. Das Vorzeichen ist gleich
dem von $u^\dagger\operatorname{Herm}Z\,u$ bei $f=Zu$.
Hier bezeichnet $\operatorname{Herm}Z=(Z+Z^\dagger)/2$.
Getestet wird harmonische Passivitaet, nicht schon ein
physikalisches Speichergesetz fuer beliebige Anfangszustaende.

## 2. Was das Rauschspektrum dann leisten muesste

Als **Referenzkriterium** am genau so zeitlich zugeordneten Port
fordern wir die klassische Nyquist-Form
$S_u(z)=2\Theta\operatorname{Herm}Y(z)$ mit $\Theta>0$
(eine deklarierte Skala, keine abgeleitete Temperatur).
Da Kopf-Rauschen $\xi$ im Kraftport als $D^{-1}\xi$ wirkt,
ist die einzige dazu passende Spektraldichte

$$
S_\xi(z)=2\Theta D\operatorname{Herm}Z(z)D.
$$

Dies folgt durch Multiplikation mit Z und seinem Adjungierten;
umgekehrt gilt $Y\operatorname{Herm}Z\,Y^\dagger
=\operatorname{Herm}Y$. Eine negative Eigenrichtung macht
ein stationaeres Rauschen mit diesem Spektrum unmoeglich.
Bei positiver Spektraldichte ist der stationaere Gaussprozess
weiterhin eine konstruierte Referenz, kein hergeleitetes Bad.
Weil Y symmetrisch ist, ist das so bestimmte Inkrementspektrum
reell und die Gauss-Inkremente sind gemeinsam zeitumkehrsymmetrisch.

Schreibe $G_i(z)=(A_i(z)-h_i)/(z-1)$; die scheinbare Singularitaet
bei z=1 ist hebbar. Weil $\operatorname{Re}(z-1)^{-1}=-1/2$
auf dem Einheitskreis, gilt

$$
\operatorname{Herm}Z
=\operatorname{diag}\left(\frac{\operatorname{Re}G_A}{\mu_A},
                          \frac{\operatorname{Re}G_B}{\mu_B}\right)
-\frac{\kappa}{2}\begin{pmatrix}1&-1\\-1&1\end{pmatrix}.
$$

Insbesondere ist die Kreuzkovarianz des benoetigten Kopf-Rauschens
zeitlich weiss ($S_{\xi,AB}=\Theta\kappa\mu_A\mu_B$ konstant).
Die nichttriviale zeitliche Struktur sitzt in den Einzel-
Autokovarianzen. Das ist nicht das gemeinsame weisse Rauschen
aus dem vorherigen Test.

## 3. Positivfall und Gegenbeispiel

Fuer $H=2$ gilt durch Polynomdivision exakt

$$
G_i(z)=1+q_i-\frac{q_i(s_i+q_i)}{z+q_i}.
$$

Der Realteil von $1/(z+q_i)$ ist auf dem Einheitskreis
hoechstens $1/(1+q_i)$ (er waechst monoton mit $\operatorname{Re}z$).
Daher $\operatorname{Re}G_i\ge1+q_i(1-s_i)/(1+q_i)\ge1$.
Kongruenz mit $D^{1/2}$ liefert die untere Schranke
$1-(h_A+h_B)/2>0$ fuer den kleinsten Eigenwert der
skalierten Dissipationsmatrix. Das benoetigte Spektrum existiert
fuer beliebige $q_A,q_B$ in diesem H=2-Vergleich, nicht nur bei der
besonderen Zweiplatz-Loesung mit weissem Rauschen. Konkret lauten
seine Einzelkorrelationen fuer positive Lags m

$$
R_{\xi,ii}(m)=-\Theta\mu_i q_i(s_i+q_i)(-q_i)^{m-1},\qquad
R_{\xi,ii}(0)=\Theta\mu_i[2(1+q_i)-h_i].
$$

Die Kovarianz ist reell und mit $R_{\xi,ii}(-m)=R_{\xi,ii}(m)$.
Das Spektrum hat einen endlichen Grenzwert bei z=1.
Auch bei groesserem festem H gibt es positive Bereiche:
Der Ausdruck $(1-P_i(z))/(z-1)$ ist gleichmaessig durch
das mittlere FIFO-Alter beschraenkt, und $P_i$ geht fuer $q_i\to0$
gleichmaessig gegen 1. Damit geht $G_i$ gleichmaessig gegen 1,
und der positive Abstand $1-(h_A+h_B)/2$ bleibt fuer hinreichend
kleine positive Retentionen erhalten.

Das positive H=2-Spektrum hat auch eine explizite **kausale**
Realisierung. Ein gemeinsamer weisser Einheitsprozess mit
Kopfkoeffizienten $\sqrt{\Theta\kappa}\,(\mu_A,\mu_B)$
liefert den Kreuzterm. Danach bleibt je Kopf das positive
Einzelspektrum $2\Theta\mu_i(\operatorname{Re}G_i-h_i)$.
Mit $b=1+q_i-h_i$ und $x=\cos\omega$ ist der Klammerausdruck
$(n_0+n_1x)/|1+q_i z^{-1}|^2$, wobei

$$
n_0=b(1+q_i^2)-q_i^2(s_i+q_i),\qquad
n_1=2bq_i-q_i(s_i+q_i).
$$

Aus $n_0>|n_1|$ folgen
$\alpha^2=(n_0+\sqrt{n_0^2-n_1^2})/2$ und
$\beta=n_1/(2\alpha)$ mit $\alpha>0$.
Zwei unabhaengige weisse Einheitsprozesse durch die stabilen
Filter $\sqrt{2\Theta\mu_i}(\alpha+\beta z^{-1})/(1+q_i z^{-1})$
realisieren die beiden Restspektren genau. Damit gibt es einen
expliziten Referenzprozess ohne angepasste Spektralparameter
ausser $\Theta$; er ist keine aus Knoten hergeleitete Umgebung.

**Langsames Vergessen kann den Port aktiv machen.**
Zum Grenztest $q_i\to1$ bei festem H verwende ausserhalb der
nichttrivialen H-ten Einheitswurzeln den uniformen Filter
$P_i=(1-z^{-H})/[H(1-z^{-1})]$. Dann ist

$$
\operatorname{Re}(\mu_i Z_{ii})=
\frac H2\left[1-s_i\cos\omega+
s_i\sin\omega\cot\left(\frac{H\omega}{2}\right)\right]
+\frac{g_i}{2},\qquad z=e^{i\omega}.
$$

Fuer $H\ge3$ und $s_i>0$ ist $\sin(2\pi/H)>0$.
Von links gegen die erste positive Resonanz $2\pi/H$ geht
der Kotangens gegen minus unendlich. Man kann also eine
feste Nichtresonanzfrequenz mit negativem Realteil waehlen.
Durch Stetigkeit bleibt das Vorzeichen bei diesem z fuer
hinreichend grosses, aber **strikt kleineres** $q_i<1$ bestehen.
Der negative Diagonaleintrag genuegt; die andere Seite des
Paares kann ihn nicht durch eine Rauschkovarianz reparieren.
Die History-Formmoden sind dabei weiterhin linear stabil.
Passivitaet folgt mithin nicht schon aus mechanischer
Modenstabilitaet oder reziprokem Mittelwerttransfer.

## 4. Einordnung und Kontrolle

[Jung, Hanke und Schmid, arXiv:1808.00270, Abschnitt II.3](https://arxiv.org/html/1808.00270)
konstruieren korrelierte Gausskraefte zu einer deklarierten
diskreten Gedaechtnisreibung; sie diskutieren auch das Scheitern
bei nichtpositivem Kovarianztensor. Hier sind weder ihr
Integrator noch ihr mikroskopischer Arbeitsanschluss unterstellt.
Das Nyquist-Kriterium ist ein ausgewiesener Vergleich, nicht
eine aus FIFO folgende thermodynamische Identitaet.

Die [festen Kontrollen](../../tests/test_memory_pair_time_reversal.py)
vergleichen die Impedanz mit der vollen History-Resolvente,
die H=2-Lags mit Fourierkoeffizienten und den positiven
mit einem aktiven H=4-Fall. Kein Nachfit, keine Trajektorie.
Ein physikalischer Anschluss muesste Leistungskonjugation,
Rauschen und dissipative Antwort gemeinsam aus dem Modell
herleiten und den gueltigen Frequenzbereich benennen.
Andere Zeitindizes, Antriebe oder eine externe dynamische
Rueckwirkung sind eigene Modellannahmen. Kein neuer
Kraft-, Feld- oder Quantennachweis.

Verifikation: 63 gezielte Tests bestanden, darin sechs neue
Kontrollen einschliesslich des kausalen Faktors und der
exakten rationalen Vorzeichenkontrolle des aktiven Beispiels.
Das Panel umfasst zudem Paartransfer, Paarreduktion,
endlichen Abstand, Potentialbilanz und Markdown-Formeln.
Keine volle Repository-Suite.
