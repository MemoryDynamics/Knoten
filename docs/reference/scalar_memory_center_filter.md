# Skalares Gedächtnis, Center-Filter und Rotation

Stand: 2026-08-22.

Diese Seite ist eine Notationsbrücke zwischen dem kanonischen Knotenkern,
der lokalen Center-Reduktion und möglichen Rotationsarchitekturen. Sie führt
keine neue Physik ein. Die Center-Gleichungen und der lineare No-go-Satz sind
algebraische Aussagen innerhalb der jeweils genannten Näherung. Für den
vollen nichtlinearen K0-H-Kern liegt inzwischen zusätzlich ein prospektiv
gefundener und lokal numerisch stabiler räumlicher Rotating-wave-Kandidat
vor. Dieser positive Befund ist weder eine interne Phase nach dem
\(SO(2)\)-Quotienten noch ein Masse- oder Arbeitsresultat.

Eine entscheidende Trennung ist dabei: \(B_H\) ist als gewichteter Readout
der Historie exakt linear. Die Kraftkopplung des Double-Gaussian-Kerns ist es
nicht. Am endlichradigen Kreis ist ihre korrekte lokale lineare Beschreibung
der vollstaendige FIFO-Jacobian mit altersabhaengigen
\(2\times2\)-Hessianbloecken, nicht automatisch der skalare Ursprungsschluss
\(-g_H(x-c_H)\).

## 1. Ausgangspunkt: die Größen des Knotenkerns

Der kanonische skalare Update lautet

\[
x_{n+1}
=x_n+\varepsilon\xi_n-\eta\nabla(K*\rho_n)(x_n),
\]

\[
\rho_{n+1}(y)
=q\,\rho_n(y)+\beta G_\sigma(y-x_{n+1}),
\qquad
q=1-\alpha,
\qquad
\beta=\alpha M_0.
\]

Dabei ist \(n\) nur der Updateindex. Eine physikalische Zeit entsteht erst
durch einen zusätzlich festgelegten Zeitschritt. Im normierten Paper-I-Fall
gilt \(M_0=1\) und damit \(\beta=\alpha\).

| Größe | Bedeutung | Wovon sie abhängt |
| --- | --- | --- |
| \(\alpha=\lambda_m\) | pro Update vergessener Anteil | Basismodellparameter |
| \(q=1-\alpha\) | pro Update erhaltener Anteil | nur \(\alpha\) |
| \(\beta=\alpha M_0\) | neu deponierte Masse | \(\alpha,M_0\) |
| \(H\) | Zahl der explizit gespeicherten Altersklassen | Backend oder Versuchsdesign |
| \(N\) | insgesamt simulierte Updates | Beobachtungsdesign, nicht Filterdynamik |
| \(M_H=M_0(1-q^H)\) | im gefüllten FIFO gespeicherte Masse | \(\alpha,H,M_0\) |
| \(\kappa_K\) | lokale rückstellende Krümmung des effektiven Readkernels | Kernelamplituden, -breiten und Deposition |
| \(g_H=\eta M_H\kappa_K\) | lokale Rückstellung pro Update | \(\eta,\alpha,H,M_0,\kappa_K\) |
| \(B_H(z)\) | normierter Center-Filter | nur \(\alpha,H,z\) |

Im Produktionsbackend wird \(H\) aus der endlichen Speichervorgabe als

\[
H
=\min\!\left(
H_{\max},
\max\!\left[1,\left\lfloor\frac{C_{\rm mem}}{\alpha}\right\rfloor\right]
\right)
\]

gebildet. Die registrierten Kontinuum- und A2-Leitern verwenden stattdessen
\(H=\lceil C/\alpha\rceil\). Dieser Rundungsunterschied von höchstens einer
Altersklasse muss in exakten Reproduktionen angegeben werden.
\(C_{\rm mem}\) und \(H_{\max}\) heißen im Code memory_factor und
max_memory; sie sind Backendvorgaben, keine neuen dynamischen Felder.

Insbesondere ist

\[
B_H=B_H(\alpha,H;z),
\]

nicht \(B_H(\eta,N;z)\). Der Kraftgain \(\eta\) tritt erst über \(g_H\) in
die geschlossene Center-Dynamik ein. \(N\) ändert weder \(B_H\) noch \(g_H\);
es bestimmt nur, wie lange diese Dynamik beobachtet wird. Außerdem ist der
Filter \(B_H\) nicht mit dem physischen Projekt-Gate B zu verwechseln.

Für Delta-Deposition und den aktuellen Double-Gaussian-Readkernel ist

\[
\kappa_K
=\frac{A_{\rm att}}{\sigma_{\rm att}^2}
-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}.
\]

Bei geglätteter Deposition muss stattdessen die Krümmung des effektiven
Kernels \(K*G_\sigma\) eingesetzt werden.

## 2. \(B_H(z)\) ist exakt eine endliche geometrische Reihe

Im vollständig gefüllten endlichen Gedächtnis trägt Alter \(j\) die rohe
Masse

\[
w_j=\alpha M_0q^j,
\qquad j=0,\ldots,H-1.
\]

Daraus folgen

\[
M_H=\sum_{j=0}^{H-1}w_j
=M_0(1-q^H)
\]

und die normierten Centergewichte

\[
\bar w_j=\frac{w_j}{M_H}
=\frac{\alpha q^j}{1-q^H},
\qquad
\sum_{j=0}^{H-1}\bar w_j=1.
\]

Der Gedächtnisschwerpunkt ist damit schlicht

\[
c_n=\sum_{j=0}^{H-1}\bar w_j x_{n-j}.
\]

Die lesbarste Form des Filters ist daher die Polynomsumme

\[
\boxed{
B_H(z)
=\sum_{j=0}^{H-1}\bar w_jz^{-j}
=\frac{\alpha}{1-q^H}
\sum_{j=0}^{H-1}(qz^{-1})^j
}.
\]

Erst danach sollte die kompakte Quotientenform stehen:

\[
B_H(z)
=\frac{\alpha}{1-q^H}
\frac{1-q^Hz^{-H}}{1-qz^{-1}}.
\]

Beide Formen sind exakt identisch. Die Summenform zeigt unmittelbar die
Gewichte, Positivität und Normierung \(B_H(1)=1\). Sie vermeidet außerdem
scheinbare Singularitäten der Quotientenform, die als endliches Polynom
immer hebbar sind.

Im Zeitbereich ist derselbe Filter

\[
c_{n+1}
=q c_n
+\frac{\alpha}{1-q^H}x_{n+1}
-\frac{\alpha q^H}{1-q^H}x_{n-H+1}.
\]

Der letzte Term ist die exakt aus dem FIFO ausscheidende Altersklasse. Wird
er weggelassen, ist das keine exakte finite-\(H\)-Dynamik mehr.

## 3. Die drei verschiedenen Grenzübergänge

Die folgenden Grenzoperationen dürfen nicht vertauscht oder sprachlich
zusammengezogen werden:

1. Bei festem \(\alpha>0\) und \(H\to\infty\) gilt \(q^H\to0\) und

   \[
   B_\infty(z)
   =\sum_{j=0}^{\infty}\alpha q^jz^{-j}
   =\frac{\alpha}{1-qz^{-1}}
   =\frac{\alpha z}{z-q}.
   \]

2. Im Kontinuumslimes \(\alpha\to0\) mit \(H=\lceil C/\alpha\rceil\)
   bleibt die physische Gedächtnislänge \(C=\alpha H\) fest und
   \(q^H\to e^{-C}\). Das ist bei endlichem \(C\) gerade nicht derselbe
   Grenzübergang wie \(q^H\to0\).

3. \(N\to\infty\) verlängert nur Laufzeit und Statistik. Der Filter bleibt
   bei festen \(\alpha,H\) unverändert.

Für \(n<H\) kommt zusätzlich die Initialisierung eines noch nicht gefüllten
Gedächtnisses hinzu. Alle obigen stationären finite-\(H\)-Formeln beziehen
sich auf den gefüllten FIFO oder eine äquivalent vorbereitete Historie.

## 4. Lokale Center-Dynamik ohne Symbolsprung

In einer kompakten Wolke kann der native Readout lokal als

\[
-\eta\nabla(K*\rho_n)(x_n)
\simeq-g_H(x_n-c_n)
\]

geschrieben werden. Mit dem für Gate A2 gewählten normierten
Center-Input \(f_n\) lautet der deterministische lineare Update

\[
x_{n+1}
=(1-g_H)x_n+g_Hc_n+\alpha f_n.
\]

Das langsame Center-Tempo ist

\[
v^c_n=\frac{c_{n+1}-c_n}{\alpha}.
\]

Um eine Kollision mit dem Depositionskernel \(G_\sigma\) zu vermeiden, ist
für den Transfer die Bezeichnung \(T_{f\to v^c,H}\) informativer. Sie ist
identisch mit dem historischen A2-Symbol \(G_H\):

\[
\boxed{
T_{f\to v^c,H}(z)
\equiv G_H^{\rm(A2)}(z)
=
\frac{(z-1)B_H(z)}
{(z-1)+g_H[1-B_H(z)]}
}.
\]

Der scheinbare Quotient \(0/0\) bei \(z=1\) ist hebbar. Mit dem normierten
mittleren Alter

\[
\bar j_H
=\sum_{j=0}^{H-1}j\bar w_j
=\frac{q}{\alpha}-\frac{Hq^H}{1-q^H}
\]

lautet der exakte DC-Wert

\[
T_{f\to v^c,H}(1)
=\frac{1}{1+g_H\bar j_H}.
\]

Die bisherige Nennerform

\[
z-(1-g_H)-g_HB_H(z)
\]

ist algebraisch dieselbe Gleichung. Die neue Form zeigt deutlicher:
\(z-1\) ist die diskrete Differenz, und \(g_H[1-B_H]\) ist die
Rückkopplung über den Gedächtnislag.

Vollständig in den Grundgrößen ausgeschrieben ist

\[
T_{f\to v^c,H}(z)
=
\frac{(z-1)\displaystyle
\sum_{j=0}^{H-1}
\frac{\alpha(1-\alpha)^j}{1-(1-\alpha)^H}z^{-j}}
{(z-1)+
\eta M_0[1-(1-\alpha)^H]\kappa_K
\left[
1-\displaystyle\sum_{j=0}^{H-1}
\frac{\alpha(1-\alpha)^j}{1-(1-\alpha)^H}z^{-j}
\right]}.
\]

Diese lange Form ist kein neues Modell. Sie löst nur die Abkürzungen
\(q\), \(M_H\), \(g_H\) und \(B_H\) wieder auf.

## 5. Wo die diskrete Gleichung zweiter Ordnung wirklich gilt

Im untruncierten exponentiellen Filter, also bei festem \(\alpha\) und
\(H=\infty\), verschwindet der FIFO-Randterm. Setze

\[
g_\infty=\eta M_0\kappa_K,
\qquad
a=q(1-g_\infty).
\]

Dann folgt nach Eliminieren von \(x_n\) exakt

\[
c_{n+1}-c_n
=a(c_n-c_{n-1})+\alpha^2 f_n.
\]

Äquivalent:

\[
\boxed{
\frac{c_{n+1}-2c_n+c_{n-1}}{\alpha^2}
+
\frac{1-a}{\alpha}
\frac{c_n-c_{n-1}}{\alpha}
=f_n
}.
\]

Das ist die gesuchte diskrete Gleichung zweiter Ordnung. Für die
small-step-Familie \(g_\infty=\chi\alpha\) und \(t=\alpha n\) gilt

\[
\frac{1-a}{\alpha}
=1+\chi-\chi\alpha
\longrightarrow 1+\chi,
\]

also formal

\[
\ddot c+(1+\chi)\dot c=f.
\]

Die Eins vor \(\ddot c\) ist eine Folge der gewählten Zeit- und
Inputnormierung. In dimensionalen Variablen

\[
\tau\dot c=x-c,
\qquad
\dot x=-\kappa(x-c)+\mu F
\]

lautet die eliminierte Gleichung

\[
\frac{\tau}{\mu}\ddot c
+
\frac{1+\kappa\tau}{\mu}\dot c
=F.
\]

Damit ist \(m_{\rm filter}=\tau/\mu>0\) eine exakt identifizierbare
Filterträgheit. Ohne mikroskopisch ausgewählten \(F\,dc\)-Port ist sie noch
keine Materialmasse.

Für endliches \(H\) ist die exakte Dynamik wegen des ausscheidenden
Historienpunkts dagegen eine Delay-/FIFO-Gleichung höherer Ordnung. Eine
zweite Ordnung ist dort nur Grenzmodell oder reduzierte Approximation; der
exakte finite-\(H\)-Transfer bleibt \(T_{f\to v^c,H}\).

## 6. Warum Vergessen allein keinen Kreis erzeugt

Ein skalares zweidimensionales Gedächtnis hat unter reinem Vergessen den
Operator \(qI\). Er kontrahiert beide Komponenten gleich und besitzt nur den
reellen Eigenwert \(q\). Die räumliche Dimension zwei fügt daher noch keine
Rotation hinzu.

Selbst wenn eine externe Rotation \(\mathcal R(\theta)\) angesetzt wird,

\[
p_{n+1}=q\mathcal R(\theta)p_n,
\]

sind die Eigenwerte zwar \(qe^{\pm i\theta}\), aber
\(\lVert p_n\rVert=q^n\lVert p_0\rVert\). Für \(0<q<1\) entsteht eine
gedämpfte Spirale, kein stabiler Kreis. Vergessen kann einen Phasenlag
bereitstellen; die Rotation und die Energiezufuhr müssen aus anderen Termen
kommen.

### Linearer No-go-Satz für den passiven Centerabschluss

Für positive normierte Gewichte gilt auf dem Einheitskreis

\[
|B_H(e^{i\omega})|
\leq\sum_j\bar w_j=1.
\]

Eine autonome harmonische Mode des lokalen Centerabschlusses müsste

\[
e^{i\omega}-(1-g_H)
=g_HB_H(e^{i\omega})
\]

erfüllen. Für \(0<g_H<1\) und \(\omega\neq0\) ist jedoch

\[
\left|e^{i\omega}-(1-g_H)\right|^2
=g_H^2+2(1-g_H)(1-\cos\omega)
>g_H^2,
\]

während die rechte Seite höchstens den Betrag \(g_H\) hat. Das ist ein
Widerspruch. Im lokalen passiven Centerabschluss kann daher keine
nichttriviale Einheitskreismode und kein linearer Hopf- beziehungsweise
Neimark-Sacker-Übergang auftreten.

Der Satz gilt nicht automatisch für die volle nichtlineare
Double-Gaussian-Historie, für signierte effektive Rückkopplung oder für einen
weit entfernten, nicht durch eine lokale Bifurkation erzeugten Zyklus. Genau
diese Lücke macht einen direkten Rotating-wave-Test sinnvoll.

## 7. Quellennahe Kandidaten für stabiles Kreiseln

### 7.1 Erste Wahl: Rotating wave im unveränderten zweidimensionalen K0-H

Die wissenschaftlich stärkste Variante führt zunächst keinen neuen
Rotationszustand ein. Identifiziere \(\mathbb R^2\) mit \(\mathbb C\) und
setze im rauschfreien nativen Modell

\[
x_n=R e^{in\theta},
\qquad R>0,\quad 0<\theta<\pi.
\]

Sei \(W_{\rm eff}=K*G_\sigma\) der effektive radialsymmetrische Readkernel und

\[
\varphi(r)=\frac{W_{\rm eff}'(r)}{r}.
\]

Am Ursprung ist \(\varphi(0)\) als stetiger Grenzwert zu verstehen; der
\(j=0\)-Summand verschwindet ohnehin durch \(1-e^{-ij\theta}=0\).

Mit den ursprünglichen rohen Gewichten \(w_j=\alpha M_0q^j\) reduziert sich
der vollständige Update auf eine einzige komplexe
Selbstkonsistenzgleichung:

\[
\boxed{
e^{i\theta}-1
+
\eta\sum_{j=0}^{H-1}
\alpha M_0q^j
\varphi\!\left(2R\left|\sin\frac{j\theta}{2}\right|\right)
(1-e^{-ij\theta})
=0
}.
\]

Real- und Imaginärteil sind zwei Gleichungen für \(R\) und \(\theta\). Für
Delta-Deposition ist beim Double-Gaussian-Kernel

\[
\varphi(r)
=-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}
e^{-r^2/(2\sigma_{\rm rep}^2)}
+
\frac{A_{\rm att}}{\sigma_{\rm att}^2}
e^{-r^2/(2\sigma_{\rm att}^2)}.
\]

Für die analytische und numerische Prüfung ist die Aufspaltung in radiale
und tangentiale Summen am transparentesten:

\[
A_H(R,\theta)
=\sum_{j=1}^{H-1}w_j\varphi(r_j)(1-\cos j\theta),
\qquad
S_H(R,\theta)
=\sum_{j=1}^{H-1}w_j\varphi(r_j)\sin j\theta,
\]

\[
r_j=2R\left|\sin\frac{j\theta}{2}\right|,
\qquad
w_j=\alpha M_0(1-\alpha)^j.
\]

Die komplexe Gleichung ist exakt äquivalent zu

\[
\boxed{
1-\cos\theta=\eta A_H,
\qquad
\sin\theta=-\eta S_H
}.
\]

Für \(\eta>0\) und \(0<\theta<\pi\) sind daher
\(A_H>0\) und \(S_H<0\) notwendig. Außerdem müssen die zwei unabhängig
bestimmten Gains

\[
\eta_R=\frac{1-\cos\theta}{A_H},
\qquad
\eta_T=-\frac{\sin\theta}{S_H}
\]

übereinstimmen. Das ist der diskriminierende Zweikomponententest; ein bloßes
Minimum eines Radiusfehlers genügt nicht.

Dieser Test bleibt vollständig bei
\(\alpha,\eta,H,M_0,A_{\rm rep},A_{\rm att},
\sigma_{\rm rep},\sigma_{\rm att}\). \(N\) wird erst für die anschließende
Stabilitätsmessung gebraucht.

### 7.1.1 Prospektives Resultat vom 20. August 2026

Die vorab fixierte Discovery verwendete \(d=2\), Delta-Deposition,
\(\varepsilon=0\), \(M_0=A_{\rm rep}=\sigma_{\rm rep}=1\),
\(\sigma_{\rm att}=3\), \(C=12\) und getrennte Mechanismus- und
Kontrollamplituden. Ohne Nachjustieren der nativen Parameter ergab die erste
registrierte finite-\(H\)-Verfeinerung

\[
\alpha=0.01,\quad H=1200,\quad\eta=0.15,\quad A_{\rm att}=3.5,
\]

\[
\boxed{
R=0.946517504804225,
\qquad
\theta=0.015770381717135
}.
\]

Dabei sind
\(\eta_R=0.149999999999945\), \(\eta_T=0.15\) und die komplexe
finite-\(H\)-Residualnorm \(4.53\,10^{-17}\). Ein unabhängiger Aufruf des
produktiven Double-Gaussian-Kernels auf der expliziten 1200-Punkte-Historie
ergibt \(7.98\,10^{-17}\) Ein-Schritt-Fehler. Die drei registrierten
Kontrollen \(A_{\rm att}=0,9,35\) lieferten in der vorab festgelegten Suchbox
keine zulässige radiale Nullstelle.

Im vollständigen \(2400\)-dimensionalen mitrotierenden FIFO-Zustand stimmen
zwei eingefrorene Arnoldi-Panels für den führenden transversalen
Ein-Schritt-Multiplikator überein:

\[
\lambda_\perp
=0.992858455252-0.020023536920i,
\qquad
|\lambda_\perp|=0.993060347711<1.
\]

Radiale, tangentiale und volle Historienstörungen der registrierten Größe
kehren innerhalb von 5000 Updates bis zum Gleitkommafloor zurück. Das ist ein
**lokaler numerischer Stabilitätspass** für die vorbereitete relative
Gleichgewichtslösung. ARPACK ist keine vollständige Spektraleinschließung;
Formation, Basin-Größe, Rauschen, \(H\)-Robustheit und der versiegelte
\(A_{\rm att}=7\)-Holdout bleiben offen.

Wegen der Spiegelsymmetrie gehört zu einer Lösung mit \(+\theta\) immer eine
gespiegelte Lösung mit \(-\theta\). Das Modell wählt damit keine Händigkeit
vorab; eine beobachtete Wahl müsste spontan und seedabhängig erfolgen.

Eine Gleitkomma-Nullstelle belegt zunächst nur numerische Existenz. Der
ausgeführte Jacobian-Test prüft die vollständige finite-\(H\)-Map im
mitrotierenden System und kalibriert die symmetriebedingten Richtungen für
Translation und globale Rotation. Weil nur die führenden 24 beziehungsweise
36 Ritzpaare und keine zertifizierte Einschließung aller Eigenwerte vorliegen,
bleibt die mathematisch strenge Formulierung „lokal numerisch stabil“.

Der Pass liefert zunächst eine dynamische, durch räumliche Symmetrie erzeugte
\(SO(2)\)-Gruppenbahn mit Kreistopologie. Nach ambientem
\(SO(2)\)-Quotienten ist diese Gruppenbahn ein Punkt. Das native Schreiben
und Vergessen ist zudem ein offener
Source-/Sink-Prozess; ohne dessen Arbeitsbilanz ist der Kreis kein
konservatives Kreisel- oder Massengesetz.

### 7.1.2 Lokale Existenzzertifikate und gematchter Grenzast

Die spätere Prüfung ersetzt die bloße Gleitkomma-Nullstelle durch eine
computerassistierte lokale Aussage. Für die exakte finite Summe werden die
beiden nativen Gleichungen

\[
F_R(R,\theta)=\cos\theta-1+\eta A_H(R,\theta)=0,
\]

\[
F_T(R,\theta)=\sin\theta+\eta S_H(R,\theta)=0
\]

direkt mit analytischer Jacobi-Matrix und gerichteter Intervallarithmetik
ausgewertet. Ein Krawczyk-Einschluss zertifiziert in der registrierten lokalen
Box genau eine Nullstelle mit

\[
R=0.94651750480422396099\ldots,
\qquad
\theta=0.01577038171713499190\ldots .
\]

Unter der unveränderten Skalierung

\[
H\alpha=12,
\qquad
\frac{\eta}{\alpha}=15
\]

besitzen auch die vier zusätzlichen Zellen

\[
(\alpha,H)\in
\{(0.04,300),(0.02,600),(0.005,2400),(0.0025,4800)\}
\]

lokal eindeutige finite-\(H\)-Nullstellen auf demselben vorregistrierten
Ast. Die zugehörigen Radien und skalierten Frequenzen nähern sich beim
Halbieren von \(\alpha\) mit Differenzquotienten gegen \(1/2\).

Der passende Kontinuumsgrenzwert muss bei genau demselben Gain definiert
werden. Mit

\[
u(t)=1-\cos(\Omega t),
\qquad
\chi(t)=R^2u(t),
\qquad
r(t)^2=2\chi(t)
\]

lautet der Double-Gaussian-Faktor ohne Betrags- oder Wurzelstelle

\[
\varphi(\chi)
=-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}
e^{-\chi/\sigma_{\rm rep}^2}
+\frac{A_{\rm att}}{\sigma_{\rm att}^2}
e^{-\chi/\sigma_{\rm att}^2}.
\]

Damit bleibt \(q=1-\alpha\) im aktuellen Referenztext eindeutig der
Vergessensfaktor. Das historische Reconciliation-Protokoll verwendete fuer
dieselbe Hilfsgroesse noch den Namen \(q(t)\); seine eingefrorene Notation
wird aus Provenienzgruenden nicht rueckwirkend geaendert.

Bei \(C=12\) sind die zwei Grenzgleichungen

\[
I_R(R,\Omega)
=M_0\int_0^C e^{-t}\varphi(\chi(t))u(t)\,dt=0,
\]

\[
\Omega+15I_T(R,\Omega)=0,
\qquad
I_T=M_0\int_0^C e^{-t}\varphi(\chi(t))\sin(\Omega t)\,dt.
\]

Drei vorab fixierte Gauss--Legendre-Panels ergeben

\[
\boxed{
R_\infty=0.9431133067695404,
\qquad
\Omega_\infty=1.5855700777178037
}.
\]

Die Panelspannen betragen \(4.77\,10^{-15}\) in \(R\) und
\(4.15\,10^{-14}\) in \(\Omega\). Gegen diesen korrekt bei
\(\eta/\alpha=15\) definierten Zielwert bestehen die fünf zertifizierten
Zellen alle ursprünglichen Skalierungsgates: Die Log-Log-Steigungen sind
\(1.0094\) und \(1.0110\), die feinsten Anchor-Fehlerquotienten etwa
\(0.248\) und die relativen Richardson-Fehler \(0.00562\) und \(0.00662\).

Ein spaeter eingefrorener Foundation-Audit implementiert die Summen und
Integrale nochmals unabhaengig in `mpmath`. Tanh--Sinh und Gauss--Legendre
liefern uebereinstimmend

\[
R_\infty=0.943113306769543632\ldots,
\qquad
\Omega_\infty=1.585570077717788707\ldots,
\]

und alle fuenf finite-Summen-Residualreplays liegen unter
\(8\,10^{-72}\). Das reduziert Implementations- und Rundungsrisiko, ersetzt
aber weiterhin keinen Intervallbeweis fuer die Kontinuumsintegrale.

Der erste Leiterlauf behält dennoch formal die Entscheidung
`certified-roots-nonconvergent`: Sein eingefrorener Discovery-Guide gehörte
nachweislich zu \(\widehat\eta=15.016345187237246\), nicht zu 15. Die
anschließende prospektive Reconciliation korrigiert diesen Zieldefinitionsfehler,
ohne das historische Ergebnis umzubenennen.

Damit ist \(x_n=Re^{in\theta}\) hier mehr als ein harmonischer Ansatz: Die
Reduktion ist algebraisch exakt, und sechs lokale finite-Summen-Nullstellen
sind computerassistiert zertifiziert. Die sechste, separat prospektierte
L5-Zelle besteht zusaetzlich den direkten 70-stelligen Summen-Replay und alle
signierten First-order-Gates ohne Retuning. Der Kontinuumsroot bleibt hingegen
ein hochgenaues numerisches Quadraturresultat ohne Intervalleinschluss. Weder
globale Eindeutigkeit noch Formation, nichtlokale Stabilität, internes
\(S^1\), Arbeit, Trägheit oder Masse folgen daraus.

### 7.2 Zweite Wahl: explizites zweikomponentiges Rotationsgedächtnis

Falls der native Rotating-wave-Test negativ ausfällt, ist eine minimale
Erweiterung ein interner Quadraturzustand \(p_n\in\mathbb R^2\). Eine
synthetische Positivkontrolle wäre

\[
p_{n+1}
=\mathcal R(\theta)
\left[(1+s)p_n-b\lVert p_n\rVert^2p_n\right].
\]

Für \(0<s<1\) und \(b>0\) besitzt sie nahe
\(\lVert p\rVert=\sqrt{s/b}\) einen gesättigten Kreis. Diese Gleichung setzt
Rotation, linearen Gain und Sättigung ausdrücklich ein; sie darf deshalb
nur als Positivkontrolle oder klar bezeichnete neue Architektur gelten.
Eine Emergenzbehauptung wäre erst zulässig, wenn diese Terme aus einem
eingefrorenen Read-/Write-Mechanismus des Gedächtnisses abgeleitet werden.

Ein bloßes skalares Gedächtnis in einem zweidimensionalen Ortsraum und ein
echtes zweikomponentiges internes Gedächtnis sind somit nicht dasselbe.

## 8. Center-konjugierte Aktuatorarchitektur

Auf effektiver Ebene ist die sauberste Architektur bereits sichtbar. Eine
Wechselwirkung

\[
U_{\rm int}(c_H-Q)
\]

definiert mit einem diskreten Gradienten gleiche und entgegengesetzte
Center- und Außenkräfte. Der Input wird im lokalen Zustandsupdate mit der
registrierten Skalierung \(+\alpha f_n\) eingebracht, der Arbeitsoutput ist
\(\Delta c_n\). Für die fünf registrierten A2-Zellen erlaubt die
finite-\(H\)-Positive-Real-Zertifizierung diese passive effektive
Realisierung.

Sie löst aber noch nicht das mikroskopische Selektionsproblem. Für

\[
c_H=\sum_{j=0}^{H-1}\bar w_jy_j
\]

lautet die virtuelle Arbeit

\[
\delta c_H=\sum_j\bar w_j\delta y_j,
\qquad
F_j=\bar w_jF_c,
\qquad
\sum_jF_j\cdot\delta y_j=F_c\cdot\delta c_H.
\]

Im bestehenden K0-H sind die \(y_j\) gespeicherte vergangene Positionen,
keine aktuierbaren materiellen Freiheitsgrade. Die adjungierte
Kraftverteilung ist dort daher eine mathematische Realisierung, keine
naturgegebene Mikromechanik.

Es gibt drei sauber getrennte Optionen:

1. Den Center-Port als effektiven passiven Wrapper verwenden und nur
   Filterträgheit beanspruchen.
2. Die Historieneinträge zu dynamischen Trägern machen und Deposition,
   Alterung, Ausscheiden, Gegenkraft und Randarbeit explizit bilanzieren.
   Das ist eine neue Architektur und kann zugleich explizite Masse
   einführen.
3. Einen physisch motivierten Source-/Write-Aktuator herleiten und zeigen,
   dass sein diskretes Arbeitsfunktional nach Elimination tatsächlich
   \(F_c\Delta c\), nicht \(F\Delta x\), ergibt.

Für eine Publikation ist Option 1 bereits mathematisch sauber, aber
ontologisch schmal. Für eine Behauptung emergenter physischer Masse ist
Option 2 oder 3 notwendig.

**P4-Ergebniskorrektur.** Der inzwischen ausgefuehrte Option-3-Test musste
fuer die rotierende L3-Schleife raw \(c_H\) durch den exakt aus demselben
\(B_H\) konstruierten chirality-konditionierten Orbit-Center \(C_s\)
ersetzen: raw \(c_H\) traegt auf dem Zielorbit die rotierende Amplitude
`0.505881`, also etwa `0.5354 R_3`. Der Source-/Write-/Age-Ledger von
\(C_s\) schliesst numerisch,
waehrend ein per fiat eingesetztes \(F\,dc_H\) deutlich nicht schliesst. Das
registrierte P4-Gesamtgate bleibt dennoch formal gescheitert. Insbesondere
zeigt die volle nichtlineare Antwort in allen 24 Armen eine grosse
chirality-odd Querkomponente statt der vorregistrierten nahezu skalaren
Geradeausbewegung. Damit ist Option 3 als konkrete Algebra demonstriert, aber
nicht als physisch zugelassene Gesamtmechanik oder Masse identifiziert.
Die alten $x/y$-Arme rotierten nur den Aktuator bei festgehaltener
History-Phase; sie belegen daher noch keine diskret phasengemittelte isotrope
oder antisymmetrische Suszeptibilitaet. P4-R-phi darf diese neue Hypothese nur
mit ungeoeffneten History-Phasen und aufgeloester Residualmetrologie testen.

## 9. Anschluss an die kanonische Gate-Folge

Diese Referenz definiert Algebra und Claim-Grenzen, aber keine eigene laufende
Prioritaetenliste. Der aktuelle Befund steht im
[Projektstatus](../status/current_status.md), die einzige prospektive
Abhaengigkeitskette in den
[Projektprioritaeten](../status/project_priorities.md).

Fuer diese Kette liefert die Center-Reduktion drei unveraenderliche
Anforderungen:

1. Das Loop--Center-Kompatibilitaetsgate muss \(c_H\),
   \(r=x-c_H\) und den exakten finite-\(H\)-Readout \(B_H\) am selben
   eingefrorenen Schleifenkandidaten verwenden. Der skalare Ursprungstransfer
   mit \(g_H\) ist fuer L3 wegen \(g_H<0\) nicht zulaessig. Die lokale
   Antwort muss daher aus dem unabhaengig konstruierten vollen FIFO-Jacobian
   vorhergesagt werden; neu gefittete Pole, Gains oder Koeffizienten waeren
   keine Bestaetigung der Reduktion.
2. Der effektive passive Wrapper ist eine Positivkontrolle. Ein physischer
   Masseclaim erfordert weiterhin dynamische Memory-Traeger oder einen
   hergeleiteten und prospektiv bestandenen Source-/Write-Aktuator samt
   Gegenkraft, Randarbeit und Source-/Sink-Ledger. Der formal gescheiterte
   P4-Lauf erfuellt diese Freigabe nicht.
3. Eine interne Kreiskoordinate muss den ambienten \(SO(2)\)-Quotienten
   ueberleben. Sie ist weder Voraussetzung fuer die effektive
   Center-Filtertraegheit noch deren Konsequenz.

Damit bleiben die Claims auch nach einer methodischen Zusammenfuehrung
getrennt: Kompatible Loop-/Center-Koordinaten sind noch keine physische Masse,
und ein positiver Filterkoeffizient ist noch kein interner \(S^1\)-Zyklus.
