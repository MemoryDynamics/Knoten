# Paar-Diagnose: bewegte Quellen und unabhaengige Replikationen

Stand: 2026-11-01. **Algebra, Softwarekontrollen und Statistikvertrag;
kein Ziellauf oder Replay.** Anschluss an den
[Diagnose-Vorabcheck](memory_pair_diagnostic_preflight_2026-10-29.md).
Die dortigen Snapshot-Schranken und alten Laufgenehmigungen bleiben
unveraendert. Das Ausfuehrungsprotokoll ist weiterhin nicht freigegeben.

**Ergebnis:** Der native Gradient laesst sich jetzt aus dichten Punktdaten
rekonstruieren und exakt in eingefrorenen Readout plus lineare und
nichtlineare Bewegungsbeitraege zerlegen. Fuer die Statistik ist ein
gleichzeitig/laggleich gekreuzter Vergleich unabhaengiger Gesamtlaeufe
definiert. Anders als der bisherige Zeitproduktvergleich benoetigt sein
endlicher Erwartungswert keine Stationaritaet. Die einfachste globale
Konfidenzschranke ist fuer ein kleines Panel jedoch uninformativ.

## 1. Rekonstruktion und Geometriebilanz

Der [reine Auswerter](../../src/emergenz_knoten/pair_path_diagnostics.py)
rekonstruiert jeden Memory-Center aus der vollstaendigen Anfangshistorie
und den danach geschriebenen Punkten. Mit normierten Altersgewichten
$p_i$ gilt

$$
c_i(n)=\sum_{\ell=0}^{\min(n,H_i)-1}p_{i\ell}x_i(n-\ell)
+\mathbf1_{n<H_i}\sum_{\ell=n}^{H_i-1}p_{i\ell}y_{i,\ell-n}(0).
$$

Die erste Summe ist bei $n=0$ leer. Der Anfangspunkt wird nicht mit dem
neuesten Anfangsdepot gleichgesetzt. Die Rekonstruktion verwendet eine
Faltung fuer neue Punkte und den expliziten Anfangsrest, keinen Solver.
Die anschliessende Geometrieauswertung fordert $a\geq\max_iH_i$ fuer
das Messfenster $[a,b)$: Alle dort gelesenen Depots stammen dann aus den
gespeicherten neuen Punkten und alle benoetigten Center sind bekannt.

Setze $v_i(n)=x_i(n)-c_i(n)$, $R(n)=c_A(n)-c_B(n)$ und waehle $R_*$
vorab. Fuer A sind der echte und der eingefrorene Leseabstand

$$
z=x_A(n)-x_B(n-\ell),\qquad z_0=R_*+v_A(n)-v_B(n-\ell),\qquad
\delta=z-z_0=R(n)-R_*+c_B(n)-c_B(n-\ell).
$$

Fuer B wechseln das Vorzeichen des Abstandsterms und der Quellindex.
Fuer $g(z)=\kappa z+r(z)$ wird der Fehler **exakt** ausgewiesen:

$$
\Delta G_i=\kappa\left\langle\sum_\ell p_{j\ell}\delta_{i\ell}\right\rangle
+\left\langle\sum_\ell p_{j\ell}[r(z_{i\ell})-r(z_{0,i\ell})]\right\rangle.
$$

Alle Gradienten sind quellen-normalisiert; Kreuzdrift und deklarierte
Kraefte erfordern weiterhin ihre zuvor spezifizierten Faktoren. Mit
$L_2=\sum_s|A_s|/\sigma_s^2$ bleibt die globale Schranke

$$
|\Delta G_A|\leq L_2\left(\langle|R(n)-R_*|\rangle
+\sum_\ell p_{B\ell}\langle|c_B(n)-c_B(n-\ell)|\rangle\right).
$$

Zusaetzlich folgt fuer den nichtlinearen Rest aus der Gauss-Hesseformel
$\|Dr(z)\|\leq3C_3|z|^2$, mit
$C_3=\tfrac12\sum_s|A_s|/\sigma_s^4$. Integration entlang des Segments
von $z_0$ nach $z$ liefert die lokale Schranke

$$
|r(z)-r(z_0)|\leq3C_3\max(|z|,|z_0|)^2|\delta|.
$$

Die gewichtete Fenstersumme dieser Schranke wird separat ausgegeben.
Ein kleiner nichtlinearer Fehler erlaubt nicht, den moeglicherweise
groesseren linearen Bewegungsbeitrag zu ignorieren. Ein konstruierter
gleichfoermig bewegter Paarzustand mit unveraendertem Centerabstand
liefert explizit einen nichtverschwindenden Historienfehler. Blosses
Nachzentrieren entfernt ihn nicht. Diese vorgeschriebene Bahn ist kein
neuer nativer Bewegungs- oder Stabilitaetsbefund.

## 2. Was der Zeitproduktvergleich nicht entscheiden kann

Der bisherige Auswerter vergleicht innerhalb einer Bahn aktuelle Punkte
mit einem Produkt zeitlich gemischter Randverteilungen. Dies ist eine
exakte **deskriptive** Groesse, aber ohne Stationaritaet/Mischung kein
Schaetzer fuer das Produkt der Verteilungen zur jeweils gleichen Zeit.
Ein neuer Gegencheck verwendet zwei identische deterministische Trends:
Der Zeitproduktkontrast ist ungleich null, obwohl die beiden Zufalls-
prozesse als degenerierte Verteilungen unabhaengig sind. Das widerlegt
nicht die bisherige Algebra; es verhindert ihre falsche statistische Deutung.

Stattdessen seien $Z_j=(A_j,B_j)$ unabhaengige, identisch vorbereitete
Gesamtlaeufe bei festem Anfangszustand. Innerhalb eines Laufs duerfen
beide Knoten und alle Zeiten beliebig abhaengig sein. Definiere

$$
h_A(A_j,B_k)=\frac1T\sum_{n=a}^{b-1}\sum_\ell p_{B\ell}
g(R_*+v_{A,j}(n)-v_{B,k}(n-\ell)).
$$

Es werden **dieselben Zeiten und Lags** gekreuzt, nicht unterschiedliche
Zeiten zufaellig umgeordnet. Der entsprechende B-Readout verwendet
$-R_*$ und $p_A$. Fuer zwei Gesamtlaeufe ist

$$
D_A(Z_1,Z_2)=\tfrac12[h_A(A_1,B_1)+h_A(A_2,B_2)
-h_A(A_1,B_2)-h_A(A_2,B_1)].
$$

Sein Erwartungswert ist genau die Differenz von gemeinsamem Readout und
dem Produktreadout unabhaengiger Replikationen. Das ist ein endlicher,
am gewaehlten Anfangszustand bedingter Erwartungswert, **kein stationaerer
Langzeitkoeffizient**. Er setzt identische Vorbereitung und unabhaengige
Rauschstroeme der Gesamtlaeufe voraus. Geteilte zufaellige Vorbereitung,
ergebnisabhaengige Auswahl oder nachtraeglich je Lauf angepasste
Referenzabstaende koennen diese Zuordnung ungueltig machen. $v_i$ wird
aus der eigenen Historie gebildet; eine gemeinsame, von beiden Knoten
abhaengige Ausrichtung ist hier nicht eingesetzt.

Der lineare Anteil von $h$ ist additiv in Ziel- und Quellbahn und hebt
sich in $D_i$ **fuer jede einzelne Datenkombination** auf. Deshalb kann
der stabile `expm1`-Rest verwendet werden, ohne eine Linearantwort zu
fitten. Gemeinsame deterministische Trends liefern nun $D_i=0$.
Eine vollstaendig ausgezaehlte nichtstationaere Vorzeichenverteilung
prueft getrennt unabhaengige und gekoppelte Knoten. Kein Monte Carlo und
keine Zielparameter werden dafuer benutzt. Diese Konstruktion ist ein
gepaarter statistischer Vergleich, kein neuer physikalischer Mechanismus.

## 3. Eine gueltige, aber fuer kleine Panels zu grobe Schranke

Fuer die volle Gaussmischung gilt global

$$
|g(z)|\leq M_g=e^{-1/2}\sum_s|A_s|/\sigma_s,\qquad |D_i|\leq2M_g.
$$

Aus $2m$ unabhaengigen Gesamtlaeufen werden **vorab disjunkte Paare**
gebildet. Dann sind die $m$ Kontraste unabhaengig. Fuer $J$ vorab
deklarierte skalare Komponenten folgt mit Wahrscheinlichkeit mindestens
$1-\alpha$ gleichzeitig

$$
|\overline D_{i,q}-\mathbb E D_{i,q}|
\leq 4M_g\sqrt{\frac{\log(2J/\alpha)}{2m}}.
$$

Dies ist Hoeffdings Schranke plus Vereinigungsabschaetzung, keine neue
Statistiktheorie. Zeitkorrelationen innerhalb einer Bahn stoeren diese
Anwendung nicht. **Die Stichprobengroesse ist $m$, nicht $T$, $TH$ oder
die Anzahl aller ueberlappenden Kreuzpaarungen.** Bei mehreren Fenstern
oder Abstaenden ist deren vorab deklarierte Gesamtzahl in $J$ zu beachten;
es ist keine zeituniforme oder optional-stopping-gueltige Aussage.

Fuer den unveraenderten alten Kernel $(A_{rep},A_{att},\sigma_{rep},
\sigma_{att})=(1,35,1,3)$ gilt $M_g=7.68272$. Ein hypothetisches Panel
von fuenf Gesamtlaeufen liefert unter dieser disjunkten Konstruktion
hoechstens zwei Paare. Bei $J=6$ fuer zwei Richtungen in 3D und
$\alpha=0.05$ ergibt sich die Halbbreite **35.9717**, groesser als der
globale Betragbereich $2M_g=15.3654$. Das ist praktisch keine neue
Einschraenkung. Die alte Snapshot-Restschranke um $10^{-10}$ ersetzt
weder den globalen Wertebereich noch eine probabilistische Bahnschranke.

Die Rechnung zeigt die Unbrauchbarkeit **dieses konservativen Zertifikats
fuer dieses kleine Panel**, keine allgemeine untere Schranke an den
Stichprobenbedarf und keinen Beweis, dass staerkere Verfahren scheitern.
Die Anzahl der Laeufe darf nicht automatisch erhoeht werden. Erforderlich
ist zuerst eine begruendete engere Bahn-/Varianz-/Mischungskontrolle oder
eine ausdruecklich begrenzte deskriptive Fragestellung ohne Signifikanzclaim.
Eine Hoeffding-Schranke fuer beobachtete Maxima waere ungueltig: Die
verwendete Schranke muss vorab den gesamten Zufallsbereich abdecken.
Abschneiden und Verwerfen von Ausreissern braucht eine eigene Fehlerbilanz.

## 4. Literatur, Verifikation und offener Anschluss

[Hoeffding, JASA 58, 13-30 (1963)](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf),
Beweis von Theorem 2, Gleichungen (4.11)--(4.16), insbesondere die
MGF-Schranke $\mathbb E e^{h(X-\mathbb EX)}\leq e^{h^2(b-a)^2/8}$: Die Voraussetzungen sind Unabhaengigkeit und feste
Wertebereiche. Geprueft wurden die zugaenglichen OCR-Auszuege des
Originalartikels; die PDF-Oeffnung lieferte keinen lesbaren Volltext.
Die Anwendung oben ist eine eigene direkte Spezialisierung dieses
Standardresultats. Es wird keine Zeitreihen-Unabhaengigkeit daraus
abgeleitet und keine andere Resampling-Methode ungeprueft eingesetzt.

Sechzehn [synthetische Tests](../../tests/test_pair_path_diagnostics.py)
decken FIFO-Center bei H=1/3/5, native Feldsummen und beide Geometrieschranken
in 2D/5D, stationaere und bewegte Quellen, den Trend-Gegencheck, exakt
ausgezaehlte unabhaengige/gekoppelte Replikationsverteilungen, Hoeffding-
Skalierung/Mehrfachheit und Eingabegrenzen ab. Keine Zielbahnen berechnet.

Das deterministische Fehlerbudget ist implementiert, aber noch nicht
an nativen Paarbahnen gemessen. Die Konfidenzformel betrifft exakte
Readouts; Rundungs-, Rohdaten- und Implementierungsfehler sind zusaetzlich
zu kontrollieren. Auch ein spaeter praeziser endlicher Erwartungswert
waere keine Energie-, Massen-, Ladungs-, Quanten- oder Gravitationsherleitung.
Die [Projektprioritaeten](../../docs/status/project_priorities.md) fuehren
die weitere Arbeit; es existiert weiterhin keine neue Laufgenehmigung.

Verifikation: **172 betroffene Tests bestanden in 8.39 s**, einschliesslich
der 16 neuen Kontrollen und der bisherigen Paar-, Kernel-, Archiv- und
Dokumentationsregressionen. Konfigurierter Lintcheck und strikter MkDocs-
Bau bestehen. Keine vollstaendige Repository-Testsuite; kein statistisch
aufgeloester nativer Paarbefund und kein Nachweis effektiver Teilchenphysik.
