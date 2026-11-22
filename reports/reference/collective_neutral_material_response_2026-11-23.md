# Freie neutrale Verbunde ohne aeusseren Anker

Stand: 2026-11-23. Analytische Referenz nach dem
[Vergleich zwischen freier und verankerter Materie](collective_medium_matter_split_2026-11-23.md).
Kein neuer nativer Knotenlauf. Interne Rueckstellung und
vorzeichenbehaftete Quellenkopplungen sind Inputs.

**Ergebnis.** Ein frei verschiebbarer, neutraler Verbund kann
das Feld rueckkoppeln, ohne dessen Wellenzweig oder den
statischen $1/k^2$-Pol der Fremdquellenantwort zu verlieren.
Die Rueckwirkung laeuft dann ueber eine intern rueckgestellte
Polarisation. Ein Netto-Monopol koppelt dagegen an die freie
Translation, mit einem strikt positiven Polgewicht, das keine
interne Mode aufheben kann. Globale Neutralitaet ohne Bindung
der entgegengesetzten Quellen genuegt nicht.

## 1. Anschlusspunkt und frei bewegliche Materialeinheit

Behalte den [FIFO-Feldblock](collective_directional_current_2026-11-22.md)
bei kritischer Ausrichtung mit ungekuerztem linearem Nenner $D(k,z)$.
Schreibe $b_s=b_s(0)<0$, $C=\epsilon^2+b_s>0$ und
$A=1+\bar j_v$. Fuer $k>0$ ist die Feld-Auslese $\Phi=u/k^2$.
Der [skalare Quelltransfer](collective_accumulated_current_2026-11-22.md)
lautet

$$
D(k,z)u=-p(k)b_s(k)zk^2(s_{\rm ext}+w),
$$

wobei $s_{\rm ext}$ eine vorgegebene Fremdquelle und w
die lineare Antwort der Materie ist.

Eine Materialeinheit enthalte n longitudinal verschiebbare
Bestandteile mit Verschiebungsvektor X, positiven Mobilitaeten
$M=\operatorname{diag}(\mu_a)$ und zusammenhaengender
interner Federsteifigkeit $K=K^T\succeq0$,
$\ker K=\operatorname{span}\{\boldsymbol1\}$. Die hier
gepruefte Langwellenreferenz setzt einen gemeinsamen
Bezugsort bzw. dieselbe raeumliche Quellenform fuer die
Bestandteile vor der Verschiebung. Eine permanente interne
Dipolgeometrie und multipolare Quellkorrekturen sind nicht
enthalten. Derselbe reelle Vektor q gewichtet die Quellen
und den externen Antrieb. Fuer die zeitliche Mode $z^n$
lauten die gesetzten Materialgleichungen

$$
zX=p_m(k)[(I-MK)X+M q\,ik\Phi],\qquad
w=-ik q^T X,\qquad p_m(k)=e^{-D_m k^2},\quad D_m>0.
$$

Die Faltung $p_m$ steht fuer die gemeinsame diffusive
Verschiebung der Materialeinheit, nicht fuer eine
unabhaengige Stoerung jeder Feder. Weil $K\boldsymbol1=0$,
gibt es keinen extern fixierten Anker. Bei $k=0$ ist
die Quellenvariation $w=0$; die Rechnung betrifft
Nichtnullmoden und keine Aenderung der Gesamtladung.
Die Kraefte stammen auf **Materialseite** von der
quadratischen inneren Federenergie und derselben
gesetzten skalaren Quellenkopplung. Das beweist
keine Hamiltonsche Dynamik des aktiven FIFO-Feldblocks.

## 2. Exakte Trennung und kein Vorzeichentrick

Setze $Y=M^{-1/2}X$, $a=M^{1/2}q$ und
$R=I-M^{1/2}K M^{1/2}$. Dann ist R symmetrisch.
Fuer seine Orthonormalmoden $e_i$ mit Retentionen
$r_i$ ergibt die Elimination

$$
\frac{w}{u}=p_m(k)\sum_i \frac{a_i^2}{z-p_m(k)r_i},
\qquad a_i=e_i^Ta.
$$

Hier enthaelt der Faktor u wieder das Produkt $k^2\Phi$.
Alle Residuen sind Quadrate, weil Quelle und Antrieb
mit demselben q gekoppelt werden. Mit
$e_0=M^{-1/2}\boldsymbol1/\|M^{-1/2}\boldsymbol1\|$
gilt fuer die Translation $r_0=1$ und

$$
a_0^2=\frac{(\sum_a q_a)^2}{\sum_a\mu_a^{-1}}.
$$

Das Vorzeichen des Netto-Monopols spielt im
Rueckwirkungspol keine Rolle. Gilt $a_0\ne0$,
laesst die Addition gedaempfter interner Moden
diesen Pol nicht verschwinden. Mit $b_s<0$
erhaelt man im gemeinsamen Feldnenner
$D_{\rm eff}=D+p b_s(k)zk^2(w/u)$ denselben
wachsenden Zweig wie bei der
[freien diffundierenden Materie](collective_medium_matter_split_2026-11-23.md):

$$
z=1+\left(\frac{(-b_s)a_0^2}{A}\right)^{1/3}
k^{2/3}+O(k^{4/3}).
$$

Dazu setze $z=1+k^{2/3}\lambda$; die intern
relaxierenden Moden tragen nur einen regulaeren
Anteil bei, waehrend der Translationspol $1/(z-p_m)$
den fuehrenden Term liefert. Werden Bestandteile
in mehrere ungebundene Komponenten getrennt,
addieren sich ihre Translationsgewichte, je eines
pro frei verschiebbarer Komponente. Damit genuegt
$\sum_a q_a=0$ ueber **alle** Komponenten nicht.
Es muss jede frei verschiebbare Komponente neutral
sein. Die Kontrollfaelle behalten deshalb die
Ladungen gleich und schalten nur die innere Feder ab.

## 3. Neutrale, gebundene Positivkontrolle

Sind $a_0=0$ und $0<r_i<1$ in den aktiven
internen Moden, verschwindet die Translation exakt
aus dem Quelltransfer. Sie bleibt als eigenstaendiger
Modus $z=p_m(k)$ erhalten. Setze
$\nu_i=(-b_s)a_i^2$ fuer die internen Moden.
Dann folgt

$$
\frac{D_{\rm eff}(k,e^{k\lambda})}{k^2}
\longrightarrow A\lambda^2+C_{\rm eff},\qquad
C_{\rm eff}=C-\sum_{i\ne0}\frac{\nu_i}{1-r_i}.
$$

Fuer $C_{\rm eff}>0$ bleiben
$v_{\rm eff}^2=C_{\rm eff}/A$ und
$\Phi/s_{\rm ext}\sim -b_s/(C_{\rm eff} k^2)$.
Der Pol betrifft eine **Fremdquelle**; der neutrale
Verbund selbst liefert keinen Monopol. Der sichtbare
Rueckkanal ist seine interne Polarisation.
Bei der bereits verwendeten Feldreferenz mit
Vektoraltern $(2/3,1/3)$ und $b_s=-\epsilon^2/2$
erhoeht die Polarisation den kubischen
Koeffizienten von $k^2\log z$ um
$\sum_{i\ne0}\nu_i r_i/(1-r_i)^2$ und vermindert
die quadrierte Wellengeschwindigkeit. Der
$k^2$-Daempfungsbeweis des verankerten Falls
gilt deshalb modeweise auch hier. Das restliche
Translationsrelaxieren kommt fuer kleine
Nichtnullmoden aus $p_m(k)<1$, nicht aus einer
Verankerung. Keine Stabilitaetsaussage fuer alle k
oder fuer nichtlineare Materialformation.

Die Trennung von neutraler Translation und
innerer Polarisation hat eine strukturelle
Parallele zur akustischen Summenregel bei
[Pick, Cohen und Martin (1970)](https://doi.org/10.1103/PhysRevB.1.910).
Wir beanspruchen diese Regel nicht als Neuheit
und setzen den skalaren Referenzkanal nicht
mit Elektrodynamik im Festkoerper gleich. Neu
ist der Anschluss an den konkreten diskreten
FIFO-Feldnenner samt $k^{2/3}$-Gegenfall.

## 4. Grenze fuer die Massenroute

Bei massenproportionalen Kopplungen $q_a\propto m_a>0$
ist jeder endliche materielle Verbund nichtneutral.
Seine innere Bindung kann das freie Quellenmoment
nicht in eine nur intern rueckgestellte
Polarisation umwandeln. Der positive Vergleich
liefert deshalb eine moegliche **separate**
vorzeichenbehaftete Mediumantwort, nicht die
Herleitung eines universellen Gravitationsports.
Die Quelleigenschaft q sowie der Feder- und Driftport
wurden gesetzt. Es ist zu pruefen, welche
vorzeichenbehaftete, additiv erhaltene Quelle ein
nativer Knotenverband ueberhaupt traegt; die
[vorhandene Kontinuitaetsbilanz](memory_current_invariants_2026-11-04.md)
allein definiert sie nicht. Eine quantenmechanische
Phase oder Eichkopplung wurde nicht eingefuehrt.

[Feste Matrixkontrollen](../../tests/test_collective_directional_current.py)
pruefen die nichtnegativen Residuen, geladene und
neutrale gebundene Referenzen sowie Neutralitaet
ohne innere Bindung. Keine Parametersuche.
