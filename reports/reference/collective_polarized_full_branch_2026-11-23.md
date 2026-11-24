# Langwellen auf dem gesamten homogenen polaren FIFO-Zweig

Stand: 2026-11-23. Fortsetzung des
[homogenen Richtungsabschlusses](collective_polarized_background_2026-11-23.md).
Dieselbe deklarierte 3D-Mittelfeldregel mit am neuen Ort
geschriebenen, normierten Gauss-Schritten. Kein nativer
Vielknotenlauf, keine Parametersuche und kein Nachweis
einer stabilen Phase.

**Ergebnis.** Jeder nichtverschwindende homogene polare
Zustand ist im attraktiven skalaren Langwellenkanal
instabil, nicht nur der schwache Zweig nahe der Schwelle.
Entlang der Polarisation waechst eine Dichtemode wie
$k^2$, quer dazu bereits wie $|k|$ bei strikter Anziehung.
Repulsion kann beide Richtungen stabilisieren, aber nur
als **getrennte Langwellenbedingungen**. Eine zu grosse
skalare Verzoegerung schliesst nahe der Schwelle sogar
ihre gleichzeitige Erfuellung aus.

## 1. Longitudinaler Befund fuer jede feste Amplitude

Schreibe $a>0$ fuer den homogenen Drift, $x=a/\epsilon$,
$m(a)=f(x)$ fuer die axiale mittlere Einheitsrichtung
und $g_0 m(a)=a$. Sei $r=g_0 m'(a)$,
$\Delta=1-r>0$, $\ell_v$ das mittlere Alter des
normierten nichtnegativen Vektorfilters und
$b=b_s(0)$ der skalare Langwellenfaktor.
Die Driftvariation ist $-i\mathbf k b\,u$ an
fester Dichtevariation $u$; $b>0$ ist abweisend.

Die longitudinalen Momente des frueheren
Abschlusses lassen sich durch die Gauss-Score-Identitaet
vereinfachen:

$$
B_1=a\,m(a)+\epsilon^2m'(a),\qquad
T_1=m(a)+a m'(a)+\epsilon^2m''(a).
$$

Einsetzen in den bekannten diskreten Dichteast
ergibt fuer $\log z=-i c k+\Gamma_L k^2+O(k^3)$,
mit $c=a+a/\Delta$,

$$
\Gamma_L=\mathcal P-\frac{b}{\Delta},\qquad
\mathcal P=
\frac{(1+r)(a^2-\epsilon^2\Delta^2)}{2\Delta^3}
+\frac{\ell_v(1+\Delta)a^2}{\Delta^3}
-\frac{a\epsilon^2g_0m''(a)}{\Delta^2}.
$$

Jeder Summand in $\mathcal P$ ist nichtnegativ,
der erste und letzte strikt positiv. Denn
partielle Integration in $L(x)=f(x)/x$ ergibt

$$
f'(x)=2\sqrt{2/\pi}\int_0^1 t^2 e^{-x^2t^2/2}\,dt>0,
\qquad
f''(x)=-2x\sqrt{2/\pi}\int_0^1 t^4e^{-x^2t^2/2}\,dt<0.
$$

Zudem $\Delta=-xL'(x)/L(x)=x^2\langle t^2\rangle_x$,
mit der positiven Dichte proportional zu
$(1-t^2)e^{-x^2t^2/2}$ auf $(0,1)$. Fuer $x\le1$
ist $\Delta<x$, fuer $x\ge1$ folgt dasselbe aus
$0<r<1$. Daher $\mathcal P>0$ fuer alle $a>0$.
Insbesondere ist $\Gamma_L>0$ bei $b\le0$,
auch ohne Skalarport. Bei Repulsion daempft
der Ast in fuehrender Ordnung genau fuer
$b>b_L:=\Delta\mathcal P$. Gleichheit laesst
hoehere Ordnungen offen.

## 2. Richtungsmoden und instabiler Winkelbereich

Waehle $e_1$ entlang der Polarisation, $\mathbf k$
in der Ebene $(e_1,e_2)$ und setze
$\mathbf k=k(n_1,n_2,0)$ mit $|\mathbf n|=1$.
Bezeichne die Markierungsantwort der normierten
Schritte mit $B(\mathbf k)$ und ihre Driftableitung
mit $T(\mathbf k)$, wie im frueheren Bericht.
Die Driftvariation in Richtung $e_1$ fuehrt
in nullter Ordnung zu $d'_1=(a/\Delta)u$.
Die $e_2$-Antwort hat dann eine exakte Kuerzung:

$$
B_2=-ikn_2\,\epsilon^2/g_0+O(k^2),\qquad
T_{21}=-ikn_2\,U+O(k^2),\qquad
U=-\frac{\epsilon^2\Delta}{a g_0}.
$$

$B_2 u+T_{21}d'_1$ verschwindet in erster
Ordnung. Die Identitaeten entstehen aus dem
Gauss-Score und der Rotationssuszeptibilitaet
$m(a)/a=1/g_0$, nicht aus einem vorgesetzten
Druckgesetz. Die Verzoegerung der Orientierung
setzt $p_v=1+\ell_v$ als Faktor vor ihre
erste Zeitableitung. Definiere
$v=(a-\epsilon^2\Delta/a)/p_v$.
Die beiden Geschwindigkeiten, zu denen
$\log z=-ik v_{\pm}+O(k^2)$ gehoert (ausser
bei zusammenfallenden Wurzeln), sind die
Eigenwerte von

$$
\begin{pmatrix}
c n_1 & n_2\\
b n_2/p_v & v n_1
\end{pmatrix}.
$$

Die Diskriminante lautet
$(c-v)^2n_1^2+4b n_2^2/p_v$.
Bei $b<0$ ist sie in einem offenen Winkelbereich
um die Ausbreitung senkrecht zur Polarisation
negativ. Eine der zwei Moden waechst dort
linear in $k$; genau senkrecht ist der fuehrende
Wachstumskoeffizient $\sqrt{-b/p_v}$.
Bei $b>0$ sind die beiden Geschwindigkeiten
reell, was allein **keine** Daempfung beweist.
Der entartete Fall $b=0,n_1=0$ wird durch
die Geschwindigkeitsmatrix nicht entschieden.

Eine reine $e_3$-Richtungsstoerung ist anders:
Sie koppelt wegen Paritaet weder an die Dichte
noch an die anderen beiden Richtungen. Ihr
Symbol erfuellt $z=g(\mathbf k)P_v(z)T_{33}(\mathbf k)$,
wobei $T_{33}$ der Fourier-Mittelwert mit
nichtnegativer Gewichtsfunktion
$D_3^2/(\epsilon^2|D|)$ ist und $g_0 T_{33}(0)=1$.
Fuer $\mathbf k\ne0$ ist
$|T_{33}(\mathbf k)|<T_{33}(0)$ wegen der
kontinuierlichen Gauss-Verteilung. Mit
$|g(\mathbf k)|\le g_0$ und
$|P_v(z)|\le1$ fuer $|z|\ge1$ gibt es dort
keinen nichtdaempfenden Multiplikator.
Das ist nicht der gekoppelte Dichteast.

## 3. Wann repulsive Querwellen daempfen

Fuer $\mathbf k=k e_2$ und $b>0$ sei
$\ell_s$ das mittlere Alter des normierten
endlichen Skalarfilters,
$m_2=\sum_j j(j+1)\omega_j$ fuer die
Vektorgewichte $\omega_j$, und $\sigma_v$
die raeumliche Breite der Gauss-Vektorlese.
Dann gilt

$$
\log z=\pm i\sqrt{b/p_v}\,k+\Gamma_T k^2+O(k^3),
\qquad
\Gamma_T=
\frac{-D_T-\epsilon^2p_v/2-\epsilon^2p_v/\Delta
      +b\,d_s}{2p_v},
$$

$$
D_T=\frac{\sigma_v^2}{2}+\frac{\epsilon^2}{2}
 \left(1-\frac{\Delta}{x^2}\right)>0,\qquad
d_s=\ell_s-\frac{m_2}{2p_v}.
$$

Herleitung in Kurzform: Setze $G=g(k)P_v(z)$,
$L_x=z-GT_{11}$ und eliminiere die radiale
Drift. Fuer die Querdrift $d'_2$ ergibt sich
$N d'_2=R u$ mit

$$
N=z-GT_{22}-G^2T_{21}T_{12}/L_x,\qquad
R=G B_2+G^2 T_{21}B_{\parallel}/L_x
-ik b_s(k)P_s(z)z ,
$$

wobei $B_{\parallel}$ die erste Komponente
von $B(\mathbf k)$ bezeichnet. Mit $w=z-1$,
$\phi=e^{-\epsilon^2 k^2/2}$ ist die
charakteristische Gleichung $(z-\phi)N=-ik\phi R$.
Die Gauss-Score-Identitaeten geben
$T_{12}=-ik(m+U)+O(k^3)$ und fuer den
$-k^2/2$-Koeffizienten von $g_0 T_{22}$
den Wert $3\epsilon^2(1-\Delta/x^2)$.
Der Beitrag der radialen Elimination kuerzt
zwei Drittel davon in $N$. Damit

$$
N=p_v w-\tfrac12 m_2w^2+D_T k^2+O(k^3),\qquad
R=-ik\Big[b+
  \big(\epsilon^2p_v/\Delta+b(1-\ell_s)\big) w\Big]+O(k^3),
$$

fuer $w=O(k)$. Im zweiten Ausdruck liefert
die Kuerzung aus Abschnitt 2 genauer
$\epsilon^2 P_v(z)(z-P_v(z))/(z-rP_v(z))$
als gewichteten Koeffizienten neben dem
Skalarport. Einsetzen in die charakteristische
Gleichung und Umrechnen von $w$ auf $\log z$
ergibt $\Gamma_T$.

Bei $d_s\le0$ daempfen die repulsiven Querwellen
immer in dieser Ordnung. Bei $d_s>0$ verlangen
sie die obere Schranke
$b<b_T:=(D_T+\epsilon^2p_v/2+\epsilon^2p_v/\Delta)/d_s$.
Nahe der Schwelle $\delta=\beta-1\downarrow0$
gilt $\Delta\sim2\delta$ und

$$
b_L\sim(5/2)\epsilon^2p_v/\delta,\qquad
b_T\sim\epsilon^2p_v/(2d_s\delta).
$$

Damit ist fuer jedes feste $d_s>1/5$ die
gleichzeitige Laengs- und Querdaempfung bei
hinreichend kleiner $\delta$ **unmoeglich**,
auch mit frei waehlbarer repulsiver Staerke.
Bei $d_s=1/5$ entscheidet diese Asymptotik
nicht. Bei $\ell_s=0$ und $b>b_L$ daempfen
beide hier untersuchten Achsen in fuehrender
Ordnung; schraege Dichtewellen in Ordnung
$k^2$ und endliche Wellenzahlen sind damit
nicht abgedeckt.

## 4. Tragweite und Kontrollen

Der eingefrorene polare Rand kann kinematisch
den Fernindex der Kernfelder auf null setzen.
Der zugehoerige homogene attraktive dynamische
Abschluss scheitert aber auf dem ganzen Zweig.
Repulsion ist kein allgemeiner Stabilitaetsnachweis,
und bei zu grossem Altersversatz ist sie nahe
der Schwelle schon auf den zwei Hauptachsen
unzureichend. Das schliesst weder andere
inhomogene Hintergruende noch ein separates
Quellenfeld aus und liefert weder Gravitation
noch Quantenphasen.

[Bertin, Droz und Gregoire](https://arxiv.org/abs/0907.4688)
finden in einem anderen kinetischen Modell
eine stabile Region fern vom Uebergang.
[Tu, Toner und Ulm](https://arxiv.org/abs/cond-mat/9710222)
zeigen anisotrope Schallmoden in einem
anderen Richtungsmodell. Hier folgen Kuerzung,
Winkelbereich und Altersgrenze aus der
diskreten FIFO-Schreibregel, nicht aus der
Uebernahme einer ihrer Zustandsgleichungen.

Die [festen Integrations- und Matrixkontrollen](../../tests/test_collective_polarized_background.py)
werten die markierte Gauss-Schreibantwort
geometrisch direkt aus. Sie pruefen die
longitudinale Schwelle, die schraege Dispersion,
repulsive Daempfung und Antidaempfung bei
vorgegebener Verzoegerung sowie den reinen
quer zur Ebene liegenden Richtungsmodus.
Kein nativer Lauf und keine Parametersuche.
