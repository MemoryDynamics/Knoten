# Reziprozitaet beim endlichen Memory-Paar

Stand: 2026-11-21. Analytische Fortsetzung der
[Paarreduktion](../../docs/reference/memory_pair_reduction.md).
Keine neue Modellregel, kein Ziellauf und keine Aussage zur Stabilitaet
des offenen Memory-Vierzyklus.

## Befund

Bei derselben endlichen FIFO-Dynamik und denselben additiven Anstoessen
kann die Kreuzantwort der beiden **Memory-Center** exakt symmetrisch sein,
obwohl die der **aktuellen Orte** asymmetrisch bleibt. Im linearen
stationaeren Fall unterscheiden die normierten Altersfilter diese
beiden Antworten exakt. Unterschiedliche Filter lassen sich beim
Ortsreadout nicht durch zwei konstante Mobilitaeten ausgleichen.
Damit ist auch ein symmetrischer Center-Transfer noch kein Nachweis
einer reziproken physikalischen Kraft.

Der [anschliessende Zeitumkehrtest](memory_pair_time_reversal_2026-11-21.md)
zeigt fuer unabhaengige Gauss-Kopfinnovationen: Verschiedene geometrische
Altersfilter lassen die Center-Inkremente gemeinsam irreversibel, auch
wenn die deterministische Center-Antwort symmetrisiert wurde.

## 1. Native Linearisierung mit vollem FIFO

Berechnet wird die gepaarte Antwort des bestehenden synchronen
[Skalarpaares](../../docs/reference/hydrogen_pair_audit.md) um zwei
konstante gefuellte Historien an Orten $X_A,X_B$. Die Selbstkraft
verschwindet dort. Fuer den gemeinsamen radialen Kreuzkernel $K$ sei
$\nabla K(X_A-X_B)=0$, sodass beide Grundorte ohne Antrieb feststehen.
Das gilt am Zusammenfall; fuer getrennte Orte muss es eigens gelten.
Eine beliebige getrennte Momentaufnahme waere keine stationaere Basis.

Die Selbst-Hessians am Ursprung sind Vielfache der Identitaet;
der gemeinsame Kreuz-Hessian $J=D^2K(X_A-X_B)$ ist symmetrisch und
wegen der Geradheit an beiden Vorzeichen des Abstands gleich. In jeder
seiner Eigenrichtungen entkoppelt die erste Variation skalar. Schreibe
$x_i(n)$ fuer die Ortsvariation und $c_i(n)$ fuer die Center-Variation:

$$
c_i(n)=\sum_{\ell=0}^{H-1}p_{i\ell}x_i(n-\ell),\qquad
p_{i\ell}=w_{i\ell}/W_i,\quad W_i=\sum_\ell w_{i\ell}>0.
$$

Die native Kopfableitung ist fuer $i\ne j$

$$
x_i(n+1)=s_i x_i(n)+g_i c_i(n)+h_i c_j(n)+\mu_i F_i(n),
\quad s_i=1-g_i-h_i.
$$

$g_i$ ist die native Selbstkruemmung mit Gain und Memory-Masse,
$h_i=\chi\kappa W_j$ mit dem betrachteten Eigenwert $\kappa$ von J.
$\mu_i>0$ ist eine deklarierte Skalierung des additiven Testantriebs,
keine hergeleitete Kraftmobilitaet. Alle FIFO-Alter einschliesslich
des Rands bleiben erhalten. Der weitere Vergleich betrifft einen
**aktiven** Kanal $\chi\kappa\ne0$; ohne ihn sind beide Kreuzantworten
trivial null.

## 2. Orts- und Center-Transfer

Mit der diskreten Transferkonvention $x_i(n)\propto z^n$ und
verschwindender Anfangsstoerung definiere

$$
P_i(z)=\sum_{\ell=0}^{H-1}p_{i\ell}z^{-\ell},\qquad
d_i(z)=z-s_i-g_iP_i(z),\qquad
D(z)=d_A(z)d_B(z)-h_Ah_BP_A(z)P_B(z).
$$

Die zwei Gleichungen haben Diagonalen $d_i$ und Kreuzterme $-h_i P_j$.
Inversion liefert abseits von Polen fuer Antrieb $F$ und das jeweilige
Readout:

$$
H^x_{A\leftarrow B}=\frac{h_A\mu_B P_B}{D},\qquad
H^x_{B\leftarrow A}=\frac{h_B\mu_A P_A}{D},
$$

$$
H^c_{A\leftarrow B}=\frac{h_A\mu_B P_A P_B}{D},\qquad
H^c_{B\leftarrow A}=\frac{h_B\mu_A P_A P_B}{D}.
$$

Reziprozitaet bedeutet hier **Gleichheit der Kreuztransfers als rationale
Funktionen**, aequivalent zur Gleichheit aller kausalen Kreuz-
Impulskoeffizienten. Sie meint weder nur gleiche Betraege bei einer
Frequenz noch detailliertes Gleichgewicht oder Zeitumkehrsymmetrie.
Der gemeinsame Translationsmodus kann einen Pol bei $z=1$ erzeugen.
Die Normierung $P_A(1)=P_B(1)=1$ wird erst nach Kuerzen des gemeinsamen
Nenners verwendet; sie ist keine Behauptung endlicher DC-Suszeptibilitaet.

| Readout zum selben Punktantrieb | Notwendig und hinreichend im aktiven Kanal |
| --- | --- |
| Beide Memory-Center | $h_A\mu_B=h_B\mu_A$, also $W_B\mu_B=W_A\mu_A$ |
| Beide aktuellen Orte | Dieselbe Normierungsbedingung **und** $P_A=P_B$, also alle normierten Altersgewichte gleich |

Die Center-Bedingung war im untrunkierten kontinuierlichen Vergleich
bereits bekannt. Hier ist sie fuer den gesamten linearen endlichen FIFO
hergeleitet; dazu kommt die schaerfere Ortsbedingung. Die Selbstdrifts
gehen in den gemeinsamen Nenner ein und koennen die Ortsasymmetrie
nicht durch Nachstellen beseitigen.

## 3. Messbare Unterscheidung ohne Anpassung

Nach Center-Normierung ist das Verhaeltnis der beiden Orts-Kreuzantworten,
wo definiert, genau $P_B/P_A$. Es ist unabhaengig von der gemeinsamen
Polstruktur. Fuer $z=e^{i\omega}$, kleine dimensionslose Kreisfrequenz
$\omega$ pro Update, ergibt sich

$$
\frac{P_B}{P_A}=1-i\omega(\bar\ell_B-\bar\ell_A)+O(\omega^2),
\qquad \bar\ell_i=\sum_\ell\ell p_{i\ell}.
$$

Bei gleichem $H>1$ und geometrischen Gewichten $p_\ell\propto q^\ell$
ist $d\bar\ell/d\log q=\operatorname{Var}(\ell)>0$ fuer $0<q<1$.
Ungleiche Retentionen liefern damit schon eine unterschiedliche lineare
Phase, auch wenn sehr langsame Antworten nach Kuerzen des Nenners
zunaechst gleich erscheinen. Bei $H=1$ fehlt diese Filterobstruktion.

Der Zeitbereich liefert eine direkte Gegenprobe: Ein Einheitsimpuls
$F_B(0)$ aendert zuerst $x_B(1)$; die erste Kreuzantwort ist
$x_A(2)=h_A\mu_B p_{B0}$. Bei Vertauschung gilt entsprechend
$x_B(2)=h_B\mu_A p_{A0}$. Man kann diese beiden Zahlen durch eine
abweichende Normierung gleich machen. Ist die gemeinsame Zahl $a\ne0$,
bleibt beim naechsten Schritt fuer geometrische Filter mit $H\geq2$
jedoch die Differenz $a(q_B-q_A)$: Die Beitraege aus dem gemeinsamen
Nenner sind dann gleich und heben sich weg. Ein einzelner Abtastzeitpunkt
kann die Nichtreziprozitaet also verbergen.

Dieser Testvertrag betrifft nur die oben deklarierten linearen
Ein-/Ausgaenge. Ein zur Centerkoordinate mechanisch konjugierter
Arbeitsport wurde nicht identifiziert. Gleichheit der Transferfunktionen
garantiert keine Impulserhaltung, keine stabile Trennung und keinen
Coulomb-Schwanz. Nichtlineare rotierende oder verrauschte Knoten brauchen
einen eigenen Antwortnachweis; insbesondere ist ihr periodischer oder
zufaelliger Jacobian nicht der hier benutzte stationaere Operator.

## 4. Literatur und Gegenkontrollen

Gezielte Primaerquellensuche am 2026-11-21 zu Memory-Interaktion und
Transferreziprozitaet; kein systematischer Review. Der nahe Preprint
[Banerjee et al., arXiv:2611.17257v1 (12. November 2026)](https://arxiv.org/html/2611.17257v1),
Abschnitt .4 und Anhang C, berichtet reziproke und nichtreziproke
effektive Wechselwirkungen im eindimensionalen stochastischen
Gittermodell mit geteilten Depositionsspuren. Die effektiven Potentiale
werden aus Ensembletrajektorien gefittet, nicht aus unseren endlichen
Altersfiltern oder einem Center-/Orts-Transfer. Die breite Idee
"Wechselwirkung und Nichtreziprozitaet durch Memory" ist damit
kein eigenstaendiger Neuheitsclaim. Keine Reproduktion ihrer Numerik.

[Van der Schaft, Sepulchre und Chaffey, arXiv:2504.02062v1, Abschnitt 2](https://arxiv.org/html/2504.02062v1)
formulieren Transfer- und Impulssymmetrie fuer kontinuierliche lineare
Systeme. Hier verwenden wir die diskrete Entsprechung fuer festgelegte
Ein-/Ausgaenge, keine importierte Passivitaets- oder Hamilton-Struktur.
Die konkrete Trennung ueber $P_B/P_A$ folgt aus der endlichen FIFO-Regel.

Die [festen Kontrollen](../../tests/test_memory_pair_dynamic_reciprocity.py)
vergleichen den reduzierten Transfer mit der vollen History-Resolvente,
pruefen die fruehen Impulskoeffizienten exakt rational und vergleichen
die Linearisierung mit nativen Gauss-Gradienten an einer fest
vorgegebenen getrennten stationaeren Kontrollgeometrie. Keine
Parametersuche, keine Stichproben physikalischer Paare.

Verifikation: 43 Tests im gezielten Panel bestanden, davon neun neue
Kontrollen. Das Panel umfasst ausserdem Paarreduktion, endlichen
Abstand, Potentialbilanz und Markdown-Formeln. Keine vollstaendige
Testsuite und keine neue Zielfahrt.
