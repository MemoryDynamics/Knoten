# Zweiphasige Memory: native Bilanzen und notwendige Rueckstellung

Stand: 2026-11-16. Fortsetzung des
[FIFO-/Fixraumvertrags](memory_rigid_regeneration_2026-11-16.md).
Keine neue Zielbahn, Parametersuche, Simulationsregel oder Aenderung an Paper I.

## Ergebnis

Fuer die beschraenkte zweiphasige relative Wiederkehr sind die beiden
nativen Kopfkraefte jetzt explizit auf dieselbe Historie zurueckgefuehrt.
Ihre Achsenbilanzen liefern einen diskriminierenden Existenztest:

**Bei positivem Alignment reicht der Vektorkanal allein nicht aus**,
wenn der Vektorhorizont ganze Umlaufperioden umfasst. Dasselbe gilt
im untrunkierten Vergleich und unter einer angegebenen hinreichenden
Tailbedingung fuer andere endliche Horizonte. Ein rein repulsiver
skalarer Kanal behebt dieses Hindernis nicht. Der vorhandene skalare
Kanal muss eine quantitativ ausreichende positive Rueckstellbilanz tragen.

Das ist kein allgemeines No-go fuer FIFO, kein Stabilitaetssatz und
kein Nachweis, dass externe QFT-Felder erforderlich waeren. Der
skalare Memory-Kanal ist bereits vorhanden. Allein seine Staerke zu
erhoehen waere weder ein Existenz- noch ein physikalischer Nachweis.

## 1. Ein Bahnzustand, zwei notwendige Kopfgleichungen

Wir untersuchen den rauschfreien beschraenkten Teil des vorherigen
Vertrags. Nach Verschieben des Koordinatenursprungs ist die relative
Bewegung eine eigentliche nichttriviale Rotation Q in 3D, ohne
axialen Schraubvorschub. Sei e ihre normierte feste Achse, a,b die
beiden noch unbestimmten Phasenorte und d=e dot (b-a) ungleich null:

$$
x_{2k}=Q^ka,\qquad x_{2k+1}=Q^kb.
$$

Die eingehenden Richtungen an a und b sind

$$
p_a=\frac{a-Q^{-1}b}{l_a},\quad l_a=|a-Q^{-1}b|,
\qquad p_b=\frac{b-a}{l_b},\quad l_b=|b-a|.
$$

Es gilt e dot p_a=-d/l_a und e dot p_b=d/l_b. Die gesamten
gefuellten Historien, einschliesslich unterschiedlicher skalarer und
vektorieller Horizonte, folgen ohne frei gewaehlte Richtungen:

| Alter | Phase a: Ort / Richtung | Phase b: Ort / Richtung |
|---|---|---|
| j=2l | Q^{-l}a / Q^{-l}p_a | Q^{-l}b / Q^{-l}p_b |
| j=2l+1 | Q^{-(l+1)}b / Q^{-(l+1)}p_b | Q^{-l}a / Q^{-l}p_a |

Die skalaren Gewichte seien v_j=(1-s)M_s s^j, die vektoriellen
w_j=w0 q^j mit w0=(1-q)M_v, 0<s,q<1, M_s>=0 und M_v>0. Fuer
grad K(r)=k(|r|^2)r lautet die vorhandene Doppelgauss-Konvention

$$
k(D)=-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}e^{-D/(2\sigma_{\rm rep}^2)}
+\frac{A_{\rm att}}{\sigma_{\rm att}^2}e^{-D/(2\sigma_{\rm att}^2)}.
$$

Bei Gaussdeposition sind dies die vorhandenen effektiven Parameter,
nicht die unmodifizierten Lesebreiten. Mit den Tabellenwerten y_Xj,p_Xj
sind die vollen drei Komponenten beider nativen Kopfbedingungen

$$
b-a=-\eta_s\sum_{j<H_s}v_jk(|a-y_{aj}|^2)(a-y_{aj})
+\eta_v\sum_{j<H_v}w_jG_\ell(a-y_{aj})p_{aj},
$$

$$
Qa-b=-\eta_s\sum_{j<H_s}v_jk(|b-y_{bj}|^2)(b-y_{bj})
+\eta_v\sum_{j<H_v}w_jG_\ell(b-y_{bj})p_{bj}.
$$

Die Richtungen werden aus den wirklich zugehoerigen Schritten gewonnen.
Insbesondere ist die naechste Richtung an a p_b, nicht p_a. Keine
Kraft darf zwischen den Phasen umgeschaltet werden. Die folgenden
Achsenbedingungen ersetzen die vier weiteren reellen Querkomponenten
dieser Gleichungen nicht.

## 2. Zwei gekoppelte Achsenbilanzen

Definiere die skalaren Kreuzhoehen-Summen mit **nativen Gewichten**

$$
T_X=\sum_{\substack{j<H_s\\j\ {\rm ungerade}}}
v_j k(|x_X-y_{Xj}|^2),\qquad x_a=a,\quad x_b=b.
$$

Nur diese ungeraden Eintraege haben eine andere Achsenhoehe. Die
vektoriellen Summen werden ohne den gemeinsamen Kopfaktor w0 notiert:

$$
E_X=\sum_{\substack{j<H_v\\j\ {\rm gerade}}}q^jG_\ell(x_X-y_{Xj}),
\qquad O_X=\sum_{\substack{j<H_v\\j\ {\rm ungerade}}}q^jG_\ell(x_X-y_{Xj}).
$$

Mit U_a=E_a/l_a-O_a/l_b und U_b=E_b/l_b-O_b/l_a folgt exakt

$$
1=\eta_s T_a-\eta_v w0\,U_a,\qquad
1=\eta_s T_b-\eta_v w0\,U_b.
$$

Hier wurde nur durch das nichtverschwindende d geteilt. Das Vorzeichen
von d spielt keine Rolle. Positive T_X bedeuten in dieser Achsenbilanz
Anziehung zur jeweils anderen Hoehe. U_X kann einzeln beide Vorzeichen
haben; eine einzelne Phase reicht nicht zur Beurteilung.

## 3. Der entscheidende Zweimal-zwei-Test

Sei

$$
\mathcal D=E_aE_b-O_aO_b,
\qquad L=\begin{pmatrix}E_a&-O_a\\-O_b&E_b\end{pmatrix},
\qquad \lambda_a=E_b+O_b,\quad\lambda_b=E_a+O_a.
$$

E_a,E_b>=1 und lambda_a,lambda_b>0. Fuer jeden Horizont gilt rein
algebraisch

$$
\lambda_aU_a+\lambda_bU_b
=\mathcal D\left(\frac1{l_a}+\frac1{l_b}\right).
$$

Falls die Determinante positiv ist, koennen U_a und U_b nicht beide
nichtpositiv sein. Aus den
beiden Kopfgleichungen folgt sogar die gewichtete Rueckstellbedingung

$$
\eta_s(\lambda_aT_a+\lambda_bT_b)
=\lambda_a+\lambda_b+
\eta_v w0\,\mathcal D\left(\frac1{l_a}+\frac1{l_b}\right).
$$

**Fuer eta_v>=0** ist die rechte Seite positiv, bei eta_v>0 strikt
groesser als lambda_a+lambda_b. Deshalb sind eta_s=0 und ebenso
eta_s>=0 zusammen mit T_a,T_b<=0 ausgeschlossen. Dies gilt insbesondere
bei ausschliesslich repulsivem Skalargradienten an allen gelesenen
Kreuzabstaenden. Es fordert nicht T_a>0 und T_b>0 einzeln, sondern
zunaechst deren angegebene gewichtete Kombination.

Bei negativen eta_v gilt diese Schlussfolgerung nicht. Auch Dcal<=0
beweist weder Existenz noch Stabilitaet; dann greift nur dieses
hinreichende Ausschlusskriterium nicht.

## 4. Positive Determinante bei ganzen Umlaufperioden

Sei zuerst H_v=2N, t=q^2 und Q^N=I. N darf mehrere volle Rotations-
perioden enthalten; der Skalarhorizont H_s ist davon unabhaengig.
Definiere k_j=G_ell(a-Q^{-j}b),

$$
C=\sum_{j=0}^{N-1}t^jk_j,\quad
D=\sum_{j=0}^{N-1}t^jG_\ell(b-Q^{-j}a).
$$

Der Buchstabe D ohne Kalligraphie bezeichnet hier die Kreuzsumme,
nicht die Determinante. Dann sind

$$
O_a=\frac{C-(1-t^N)k_0}{q},\qquad O_b=qD.
$$

### Positivitaet des symmetrisierten Altersoperators

Der Gausskernel besitzt eine Hilbertraumdarstellung
G_ell(x-y)=<phi_x,phi_y>. Sie folgt direkt aus seiner positiven
Gauss-Fourierdichte: Fuer jede endliche Koeffizientenfolge ist die
Gramform ein Integral von |sum_i c_i exp(i omega dot x_i)|^2 gegen
ein positives Gaussmass. Der isotrope Kernel macht
U phi_y=phi_{Q^{-1}y} zu einem unitaeren Operator.

Setze P=(I-tU)^{-1}. Fuer 0<t<1 konvergiert die Neumannreihe und

$$
\frac{P+P^*}{2}=\frac12 I+\frac{1-t^2}{2}P^*P>0.
$$

Dies folgt durch Multiplikation mit I-tU und dessen Adjungiertem.
Wegen U^N=I ist der endliche Operator
P_N=sum_{j=0}^{N-1}t^jU^j=(1-t^N)P. Also ist auch sein symmetrischer
Anteil positiv. Seine Gram-Matrix an phi_a,phi_b ist

$$
\begin{pmatrix}E_a&(C+D)/2\\(C+D)/2&E_b\end{pmatrix}\succeq0.
$$

Damit erhaelt man die explizite strikte Reserve

$$
\mathcal D
\geq\frac{(C-D)^2}{4}+(1-t^N)k_0D>0.
$$

k0,D sind strikt positiv. Kein angenaeherter Nullstellensucher oder
numerischer Eigenwertpass wird fuer diesen Satz gebraucht. Der
Beweis verwendet sowohl die positive Definitheit als auch die
strikte punktweise Positivitaet des Gausskernels; Positivitaet
einzelner Matrixeintraege allein genuegt nicht.

### Untrunkiert und ein zusaetzlicher gerader Eintrag

Im untrunkierten Vergleich gilt derselbe Beweis mit P statt P_N und
O_a=(C-k0)/q. Dann Dcal>=(C-D)^2/4+k0D>0, auch ohne endliche Ordnung
von Q. Das ersetzt keine endliche native Rechnung durch ein anderes
Modell; es ist ein gesonderter analytischer Vergleich.

Beim Uebergang von H_v=2N zu 2N+1 wird nur je ein positiver Beitrag
zu E_a und E_b ergaenzt, O_a und O_b bleiben gleich. Jede positive
Determinantenreserve des geraden Praefixes bleibt daher positiv.
Insbesondere sind 2N und 2N+1 mit Q^N=I beide abgedeckt.

## 5. Andere endliche Horizonte: den Tail nicht unterschlagen

Ohne Q^N=I gilt weiterhin die exakte Identitaet

$$
O_a=\frac{C-k_0+t^Nk_N}{q},\qquad O_b=qD,
\quad P_N=P-t^NU^NP.
$$

Die Symmetrisierung eines beliebigen abgeschnittenen P_N ist nicht
automatisch positiv. Eine formale Gegenkontrolle ist N=3, t=99/100
und ein zweidimensionaler Rotationsoperator mit cos(theta)=-1/4:
Sein symmetrischer Teil hat den Skalarwert
1-t/4-7t^2/8=-8407/80000<0. Dies ist eine Operatorkontrolle, kein
nativer Orbit und kein Beweis, dass die konkrete Gauss-Grammatrix oder
Dcal bei einer beliebigen Memory-Geometrie negativ sein muss.

Eine konservative hinreichende Bedingung fuer den endlichen Fall ist

$$
\mu_N=\frac1{1+t}-\frac{t^N}{1-t}\geq0,
\qquad k_0>t^Nk_N.
$$

Denn Re(P)>=I/(1+t), ||P||<=1/(1-t) und U ist unitaer.
Daraus folgt Re(P_N)>=mu_N I. Die gleiche Gram-Abschaetzung liefert

$$
\mathcal D\geq\frac{(C-D)^2}{4}+(k_0-t^Nk_N)D>0.
$$

Das Nichtbestehen dieser Bedingungen ist kein Existenzpass. Fuer
beliebige endliche Horizonte bleibt die direkt aus den nativen
Summen bestimmte Determinante der gueltige Test; eine rigorose
numerische Anwendung braucht eingeschlossene Eingaben und Summen.
Hier wird kein neues Kandidatenpanel danach durchsucht.

## 6. Notwendige Staerke des vorhandenen attraktiven Kanals

Unter den zusaetzlichen Konventionen eta_s>=0, A_rep>=0, A_att>=0
gilt T_X<=(A_att/sigma_att^2) W_s,odd, mit

$$
W_{s,\rm odd}=\sum_{\substack{j<H_s\\j\ {\rm ungerade}}}v_j
=(1-s)M_s\,\frac{s(1-s^{2\lfloor H_s/2\rfloor})}{1-s^2}.
$$

Fuer Dcal>0 und eta_v>=0 verlangt jede solche native Zweiphasenloesung

$$
\eta_s\frac{A_{\rm att}}{\sigma_{\rm att}^2}W_{s,\rm odd}
\geq1+\frac{\eta_v w0\,\mathcal D(1/l_a+1/l_b)}{\lambda_a+\lambda_b}.
$$

Bei gefalteter Gaussdeposition wieder die effektiven A_att,sigma_att
verwenden. Dies ist eine notwendige Obergrenzenpruefung, kein Vorschlag,
die linke Seite durch Gain-Fitting passend zu machen.

Die Hoehendifferenz d kuerzt sich aus der Achsenbedingung heraus.
Einfach beide Hoehen naeher zusammenzuschieben beseitigt diese Huerde
fuer d ungleich null daher nicht. Unter einer zusaetzlich deklarierten
Zeitverfeinerung eta_s=h kappa_s mit festen Massen, Amplituden und
Breiten verschwindet die linke Seite fuer h gegen null; diese spezielle
Zweiphasenklasse bleibt dann nicht bestehen, solange Dcal>0 und
eta_v>=0. Das entscheidet nicht, ob der diskrete Schritt physikalisch
mikroskopisch oder nur numerisch zu verstehen ist. Eine erforderliche
endliche Schrittstaerke ist nicht automatisch ein Simulationsartefakt.

### Vorzeichenkontrolle am bekannten instabilen Vierzyklus

Fuer den bereits existierenden
[negativen-Gain-Kontrollfall](memory_defect_recurrence_2026-11-14.md)
ist Q=R^2 und H_v=4. Die beiden Achsenbilanzen liefern jeweils
eta_s T=-37/2 und eta_v w0 U=-39/2, also 1=-37/2-(-39/2).
Der neue Ausschluss fuer eta_v>=0 widerspricht dieser Kontrolle nicht.
Ihr negativer Alignment-Gain und ihr bewiesener wachsender
Floquet-Multiplikator bleiben unveraendert; kein Rettungsversuch.

## 7. Literatur und Verifikation

Primaerabgleich zur verwendeten Kernel-Eigenschaft: I. J. Schoenberg,
*Metric Spaces and Positive Definite Functions*, Transactions of the
American Mathematical Society 44(3), 522-536 (1938),
[Originalscan](https://pages.stat.wisc.edu/~wahba/stat860public/pdf1/schoenberg.1938.pdf),
[DOI](https://doi.org/10.1090/S0002-9947-1938-1501980-0).
Gelesen und visuell geprueft: S. 524-525, Abschnitt 2, Eigenschaften
I-III und Gl. 2-4. Dort wird die positive Definitheit der Gaussfunktion
ueber ihre positive Fourierdarstellung begruendet. Die Verlags-DOI-Seite
war beim Abruf gesperrt; Titel, Autor, Band und Seiten stehen im Scan.
Die enge Titel-/Erratumsuche vom 16.11.2026 ergab keinen Korrekturtreffer;
das ist keine umfassende Garantie und kein Gesamt-Review der Arbeit.
Die native Zweiphasenbilanz und die obigen Altersoperator-Grenzen sind
hier hergeleitet, keine Resultate, die Schoenberg zugeschrieben werden.

`tests/test_memory_two_phase_balance.py` kontrolliert feste endliche
Historien gegen die vorhandenen nativen Kraftprimitive, verschiedene
Depositionskonventionen und unterschiedlich lange Horizonte, die
Determinanten-/Tailidentitaeten, die Operatorkontrolle und den bekannten
negativen-Gain-Vierzyklus. Kein neuer Orbit, Scan oder Lauf. Die erste
Testfassung hatte sechs ungueltige Depositions-Testeingaben: Fuer Delta-
und matched_gaussian-Deposition muss die zusaetzliche Schreibbreite null
sein. Nach Korrektur dieser Eingaben bestehen alle 21 neuen Kontrollen.
Ein dazwischen angefragter erneuter Test wurde wegen eines Limits der
Freigabepruefung nicht gestartet; nach Fortsetzung wurde er ausgefuehrt.
Keine Modellregel oder wissenschaftliche Bedingung wurde dafuer geaendert.

Abschliessend bestanden 298 Tests im betroffenen Defekt-/Rekurrenz-,
Vektormemory-, Normalantwort-, Strom-/Phasen-, Zustands- und Markdown-
Panel sowie Ruff im konfigurierten Bereich und strikter MkDocs-Bau.
Keine vollstaendige Repository-Testsuite, kein unabhaengiger
mathematischer Review und kein neuer validierter Orbitnachweis.

Offen bleiben die gleichzeitigen Querbilanzen, ein regulaerer gebundener
Defekt an beiden Phasen, die volle History-Stabilitaet und der Anschluss
an eine erhaltene physikalische Quelle. Die Rueckstellhuerde ist vor
jedem spaeteren Existenz-/Stabilitaetsversuch zu beachten; sie liefert
keinen Grund, jetzt eine neue Feldvariable oder Kopplung einzubauen.
