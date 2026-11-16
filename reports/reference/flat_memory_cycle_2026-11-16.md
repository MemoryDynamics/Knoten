# Positive Memory-Vierzyklen mit einem innenliegenden Felddefekt

Stand: 2026-11-16. Fortsetzung der
[vollen Historienantwort](memory_history_response_2026-11-16.md)
und der [Zweiphasen-Kraftbilanz](memory_two_phase_balance_2026-11-16.md).
Keine Zieltrajektorie, Parametersuche oder Aenderung an Paper I.

## Ergebnis und Grenze

Die vorhandene deterministische Regel besitzt eine explizite Familie
nichtplanarer Vierzyklen mit **positivem** Alignment-Gain und rein
attraktivem skalarem Memory. Alle drei Kraftkomponenten sind gleichzeitig
erfuellt. Ein eindeutiger regulaerer +1-Defekt des nativen Vektorreadouts
bewegt sich exakt mit; fuer ein angegebenes offenes Retentionsintervall
liegt er strikt innerhalb der konvexen Huelle der vier Memory-Orte.

Das schliesst eine konkrete Existenzluecke, aber nicht die
Stabilitaetsluecke. Die Kopplungen werden analytisch aus einer vorgegebenen
Geometriefamilie bestimmt. Es ist eine **inverse Existenzkonstruktion**,
keine Parameterprognose, kein generischer Attraktor und kein
Elektromagnetismus. Eine vollstaendige lokale Stabilitaetspruefung eines
festen Vertreters wurde angefragt, bislang nicht ausgefuehrt.
Die Struktur ist weder als Teilchen noch als nichttrivialer Knotentyp
der Bahn identifiziert. Die drei Raumdimensionen werden vorausgesetzt.

## 1. Ein serieller FIFO, keine neuen Agenten

Arbeite mit H_s=H_v=4, epsilon=0, positiven M_s,M_v und Retentionen
0<s,q<1. Die Gewichte sind unveraendert v_j=v0 s^j, w_j=w0 q^j,
v0=(1-s)M_s und w0=(1-q)M_v. Keine Nachnormierung des endlichen Speichers.
Die skalare Kraft bleibt -eta_s grad K, die Vektorkraft +eta_v V.

Setze a=(r,0,h), r,h>0 und

$$
S=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&-1\end{pmatrix},\qquad
S^4=I,\quad\det S=-1,\qquad x_n=S^na.
$$

Die konsistente gefuellte Historie an Phase null ist

$$
Y=\bigl((r,0,h),(0,-r,-h),(-r,0,h),(0,r,-h),(r,0,h)\bigr).
$$

Der fuenfte Ort ist nur der notwendige Vorgaenger der aeltesten
Einheitsrichtung. Alle vier Schrittlaengen sind
L=sqrt(2r^2+4h^2); $p_j=(y_j-y_{j+1})/L$. S ist nur eine
Beschreibung der zu pruefenden Wiederkehr, **kein zusaetzlicher
Rotationsoperator im Update**. Es genuegt, die native Kopfgleichung
Psi(Y)=S a zu beweisen: Die Shiftzeilen und O(3)-Aequivarianz liefern
dann F(Y)=S Y und alle vier Phasen.

Die Ein-Schritt-Bewegung ist uneigentlich. Ihre Zweischritt-Bewegung
Q=S^2 ist eine eigentliche Halbrotation um die z-Achse mit zwei
verschiedenen Hoehen. Damit wird der fruehere Ein-Schritt-Ausschluss
fuer eigentliche Rotationen nicht verletzt.

## 2. Alle Kraftkomponenten auf drei Koeffizienten reduziert

Fuer beliebigen vorhandenen radialen Skalargradienten
grad K(r_vec)=k(|r_vec|^2)r_vec definiere

$$
g=e^{-L^2/(2\sigma^2)},\qquad f=e^{-2r^2/\sigma^2},\qquad
B=\frac{\eta_v w0}{L},\quad
C_1=\eta_s v0\,k(L^2),\quad C_2=\eta_s v0\,k(4r^2).
$$

sigma ist die Vektorbreite. Geometrisch gilt 0<g^2<f<1. Die x-, y-
und halbe z-Inkrementgleichung, durch r,r,h dividiert, lauten

$$
\begin{aligned}
-1={}&-C_1(s+s^3)-2C_2s^2+B(1+gq-fq^2-gq^3),\\
 1={}&-C_1(s-s^3)+B(1-gq-fq^2+gq^3),\\
-1={}&-C_1(s+s^3)+B(1-gq+fq^2-gq^3).
\end{aligned}
$$

Diese Identitaeten werden an vorgeschriebenen, im Allgemeinen
**nicht** selbstreproduzierenden Historien gegen die nativen
Skalar-/Vektorreadouts geprueft. Alle drei Depositionskonventionen
verwenden dabei ihre richtigen effektiven Skalarparameter.

Eliminieren ohne Optimierung ergibt notwendig und hinreichend

$$
\Delta=s^2(1-gq)-q^2(f-gq),\qquad
B=\frac1\Delta,\qquad
C_1=\frac{B(1-gq)}s,\qquad
C_2=\frac{Bq(g-fq)}{s^2}.
$$

Fuer Delta=0 sind die drei Gleichungen widerspruechlich: Die
Elimination verlangt B Delta=1. Positive Vektorkopplung erfordert
Delta>0 und damit C_1>0. Die Kreuzhoehenkraft muss attraktiv sein,
im Einklang mit dem frueheren notwendigen Rueckstellsatz. Das
Verhaeltnis der beiden skalaren Kraftwerte ist nicht frei waehltbar:

$$
\frac{C_2}{C_1}=\frac{q(g-fq)}{s(1-gq)}.
$$

## 3. Ein vorhandener Kernel erfuellt die ganze Bilanz

Nimm den zulaessigen rein attraktiven Teilfall des vorhandenen
Doppelgausskernels: A_rep=0, A_att=A>0, Delta-Deposition und
sigma_att=sigma_vector=sigma. Dann K=-A G_sigma und
k(D)=A G_sigma(sqrt(D))/sigma^2. Es folgt C_2/C_1=f/g, also

$$
s=\frac{qg(g-fq)}{f(1-gq)}.
$$

Dies ist eine hergeleitete Retentionsbeziehung, kein nachtraeglicher
Fit an eine simulierte Bahn. Fuer die offene Geometrieklasse

$$
0<f<1,\qquad f^{3/4}<g<\sqrt f,\qquad 0<q<1
$$

gilt 0<s<q<1. Denn g>f und
s/q=(g^2-fgq)/(f-fgq)<1. Zudem

$$
\Delta=\frac{q^2P(q)}{f^2(1-gq)},\qquad
P(q)=g^4-f^3+fgq(f^2+f-2g^2).
$$

P ist affin in q, mit

$$
P(0)=g^4-f^3>0,\qquad
P(1)=(g-f)\bigl[g^2(g-f)+f^2(1-g)\bigr]>0.
$$

Daher Delta>0 im gesamten angegebenen Intervall. Die Geometrie ist
aequivalent zu 0<h<r/2, mit

$$
r^2=-\frac{\sigma^2}{2}\log f,\qquad
h^2=\frac{\sigma^2}{4}\log(f/g^2).
$$

Die verlangten positiven nativen Gains sind endlich fuer jeden
festen zulaessigen Parametersatz:

$$
\eta_v=\frac{BL}{(1-q)M_v},\qquad
\eta_s=\frac{C_1\sigma^2}{(1-s)M_sAg}.
$$

Einsetzen erfuellt alle drei Gleichungen aus Abschnitt 2, und
damit die komplette native Vierperiode auf gefuellten Historien.
Keine neuen Freiheitsgrade, keine freie Wahl gespeicherter Richtungen
und kein von aussen angelegtes stabilisierendes Feld werden benutzt.
**Nicht bewiesen** ist, dass kleine Stoerungen zu dieser Bahn
zurueckkehren. Insbesondere sind diese Gains nicht physikalisch
kalibriert; Grenzwerte q gegen 0 oder 1 duerfen nicht ungeprueft
als regulare physikalische Grenzfaelle interpretiert werden.

Der regulaere Tetraeder hat h=r/sqrt(2) und g=f, liegt also ausserhalb
dieser Klasse. Bei g=f ergibt dieselbe Elimination das bekannte
s=gq(1-q)/(1-gq) und Delta<0. Der fruehere positive-Gain-Ausschluss
des regulaeren Tetraeders bleibt gueltig.

## 4. Eindeutiger +1-Defekt und exakte Mitbewegung

Die vier Richtungen haben Rang drei und ihre einzige positive
lineare Relation ist p_0+p_1+p_2+p_3=0. Daher kann das Summenfeld
nur dort verschwinden, wo alle vier positiven gewichteten Gauss-
Koeffizienten gleich sind. Da alle y_j gleichen Abstand vom Ursprung
haben, werden deren drei Verhaeltnisgleichungen linear in z. Mit
u=sigma^2 log q<0 lautet die eindeutige Loesung

$$
z_*=(u/r,-u/r,u/(2h)).
$$

Setze c=w0 G_sigma(z_*-y_0)>0. Die raeumliche Feldableitung ist

$$
DV(z_*)=\frac{c}{\sigma^2L}
\begin{pmatrix}2r^2&-2r^2&0\\2r^2&2r^2&0\\0&0&8h^2\end{pmatrix},
\qquad
\det DV(z_*)=\left(\frac{c}{\sigma^2}\right)^3
\frac{64r^4h^2}{L^3}>0.
$$

Der regulaere lokale Index ist +1. In der abgeflachten Familie ist
die kleinste Singulaerzahl 8c h^2/(sigma^2 L)>0. Dies ist eine lokale
Feldreserve, keine dynamische Formstabilitaet. Bei q gegen 1 sinkt
c mit dem nativen Kopfgewicht; die Indexzahl allein misst diese
abnehmende Reserve nicht.

An Phase n gilt V_n(z)=S^n V_0(S^-n z), also z_*(n)=S^n z_*.
Gleichzeitige Transformation von Argument und Vektorwert laesst den
Index auch bei uneigentlichem S unveraendert. Der Defekt wird somit
von derselben exakten nativen Historie immer wieder erzeugt, nicht
an jedem Schritt nachtraeglich eingesetzt.

## 5. Wann der Defekt wirklich innerhalb der Wolke liegt

Die baryzentrischen Koordinaten von z_* bezueglich y0,...,y3 sind

$$
\begin{aligned}
\lambda_0&=1/4+u/(8h^2)+u/(2r^2),&
\lambda_1&=1/4-u/(8h^2)+u/(2r^2),\\
\lambda_2&=1/4+u/(8h^2)-u/(2r^2),&
\lambda_3&=1/4-u/(8h^2)-u/(2r^2).
\end{aligned}
$$

Wegen u<0 ist lambda_0 die kleinste. Alle sind genau dann positiv,
wenn

$$
-\log q<\tau_*:=\frac{2h^2r^2}{\sigma^2(r^2+4h^2)},
\quad\text{also}\quad e^{-\tau_*}<q<1.
$$

Dieses offene Intervall ist fuer jedes feste r,h>0 nichtleer und
mit der ganzen Existenzfamilie vereinbar. Es beweist eine strikte
geometrische Innenlage **entlang der exakten Bahn**, keine
Bindungsenergie und keinen stoerungsstabilen Einzugsbereich. Bei
Gleichheit liegt die Nullstelle auf einer Flaeche der Memory-Huelle;
der Feld-Jacobian bleibt dabei regulaer. Huelle und topologischer
Schutzrand sind nicht dasselbe.

## 6. Literatur und physikalische Einordnung

Wiederkehrende Bewegung durch Eigenmemory ist als solche keine neue
Teilchenphysik. [Bacot et al., PRL 122, 104303 (2019)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.122.104303)
berichten experimentell und numerisch freie multistabile und
oszillatorische Zustaende eines wellengetriebenen Tropfens auf
vibrierter Fluessigkeit. Hier wurden Verlagsmetadaten und Abstract
geprueft, nicht der zugangsbeschraenkte Volltext oder seine numerischen
Resultate reproduziert. Das andere Antriebs-/Wellenmodell liefert
weder unser endliches FIFO noch dessen Ladungsinterpretation.

Der bestehende Vergleich [Kopp/Klapp, PRE 107, 024611 (2023)](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.107.024611)
betrifft repulsives Gaussfeedback mit einem festen Zeitverzug und
persistente Translation. Die Verlagsseite bestaetigt die Korrektur
von Gleichung (6) vom 12.06.2023; diese Gleichung wird hier nicht
verwendet. Kein Transfer einer Literatur-Stabilitaet auf die neue
Vierperiode und kein allgemeiner Neuheitsanspruch aus dieser kurzen
Literaturpruefung.

Unser spezifischer Fortschritt ist die gemeinsame analytische
Konstruktion von nativer positiver Kraftbilanz, nichtplanarer
Wiederkehr, regulaerem Defekt und nachgewiesener Innenlage. Noch
fehlen volle Formstabilitaet, dynamisch geschuetzte Gegenladung,
elektrischer Quellenport, Energiebilanz und Quantenstruktur. Wie
bereits fuer minimale Vier-Depositions-Historien bewiesen, liefert
diese Klasse keinen regulaeren -1-Defekt. Weder Elementarteilchen,
Spin 1/2, Pauli-Prinzip noch Gravitation werden daraus abgeleitet.

## 7. Pruefumfang und angefragter naechster Test

21 neue feste Kontrollen pruefen rationale Kraftidentitaeten,
Positivitaetsfaktorisierung, den regulaeren Gegenfall, alle drei
nativen Depositionskonventionen, Feldnullstelle, Jacobian und beide
Seiten der Innenlagegrenze. Keine Simulation, kein Nullstellensucher,
kein Eigenwert- oder Stabilitaetslauf. Die rationale Substitutionstabelle
ist kein Kandidatenscan und waehlt keinen Gewinner aus.

357 Tests im betroffenen Regressionspanel, Lint im konfigurierten
Bereich und strikter Dokumentationsbau bestehen. Keine vollstaendige
Repository-Testsuite. Die universellen Aussagen folgen aus den
angegebenen algebraischen Beweisen, nicht aus der endlichen Zahl
von Substitutionen. Die nativen Kraftkontrollen pruefen insbesondere
die Vorzeichen und Alterskonvention unabhaengig von der Elimination.

Ein einzelner **separater** lokaler Stabilitaetsauftrag ist angefragt:
g=2/3, f=1/2, q=99/100, sigma=A=M_s=M_v=1 und H_s=H_v=4; daraus
folgen s=1133/1700, r,h und beide Gains exakt nach den obigen Formeln.
Die Innenlage ist schon analytisch gesichert: -log(99/100)<1/99,
log2>69/100 und log(9/8)>2/17 geben tau_*>1/99.
Geplant sind ausschliesslich die vollen 15 konsistenten
Historienkoordinaten mit echten Zwischenzustaenden und begruendeter
Symmetrietrennung, maximal 30 Sekunden auf einem CPU-Thread, ohne
Trajektorie, Nachanpassung, Parametersuche oder automatische Wiederholung.
Die Anfrage ist noch keine Ausfuehrungsfreigabe und kein Befund.

Die aktive Arbeitsreihenfolge wird ausschliesslich in den
[Projektprioritaeten](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/docs/status/project_priorities.md)
gefuehrt. Ein positiver Existenzsatz darf den ausstehenden vollen
Stabilitaetstest nicht durch ein leichteres Erfolgskriterium ersetzen.
