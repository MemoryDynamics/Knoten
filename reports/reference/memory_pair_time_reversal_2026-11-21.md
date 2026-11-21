# Zeitumkehrtest fuer endliche Memory-Paare

Stand: 2026-11-21. Anschluss an den [endlichen Paartransfer](memory_pair_dynamic_reciprocity_2026-11-21.md).
Keine neue Modellregel oder Zielsimulation. Die Rechnung betrachtet
eine lineare Gauss-Referenz, keine vollstaendige Knotenbahn.

**Befund.** Bei aktivem attraktivem Kanal und endlichem $H\ge2$
verhindern verschiedene geometrische Altersfilter die Zeitumkehrsymmetrie
der **gemeinsamen Center-Inkremente**. Das gilt fuer jedes positive
Verhaeltnis der beiden unabhaengigen Kopf-Rauschvarianzen. Zugleich kann
der deterministische Center-Transfer exakt reziprok sein. Den Unterschied
koennen zwei einzeln beobachtete Center-Zeitreihen nicht erkennen; der
Zeittest braucht ihre verzoegerten Kreuzkorrelationen.

## 1. Stationaere Beobachtung trotz freier Translation

Wie im Paartransfer-Bericht linearisieren wir eine raeumliche
Eigenkomponente um konstante stationaere Historien. Seien

$$
x_i(n+1)=s_i x_i(n)+g_i c_i(n)+h_i c_j(n)+\xi_i(n),
\quad
c_i(n)=\sum_{\ell=0}^{H-1}p_{i\ell} x_i(n-\ell),\quad i\ne j,
$$

mit $g_i,h_i>0$, $s_i=1-g_i-h_i\ge0$ und normierten geometrischen
$p_{i\ell}=q_i^\ell/\sum_{a=0}^{H-1}q_i^a$ bei $0<q_i<1$.
Die beiden Kopfinnovationen $\xi_i$ sind mittelwertfrei, zwischen
Zeiten und Kanaelen unabhaengig und gaussverteilt mit
Varianzen $\sigma_i^2>0$. Die Kopplung und alle Gewichte bleiben fest.
Negative Gains, korreliertes oder gefiltertes Rauschen und ungleiche
Speicherlaengen sind nicht von diesem Klassifikationssatz erfasst.

Die volle $2H$-dimensionale History-Matrix M ist zeilenstochastisch
und nichtnegativ. Jeder Kopf liest beide ganzen Historien mit
positiven Koeffizienten; die Shiftzeilen fuehren alle Altersplaetze
zum jeweiligen Kopf zurueck. Damit ist der Graph irreduzibel, und
positive Kopfschleifen machen ihn aperiodisch. Perron-Frobenius
liefert genau eine einfache Einheitswurzel, die gemeinsame
Translation; alle uebrigen Multiplikatoren sind strikt im Einheitskreis.

Die absoluten Center werden unter Rauschen nicht als stationaer
angenommen. Stattdessen beobachte
$v_i(n)=c_i(n)-c_i(n-1)$. Die Differenz entfernt die freie Translation
aus dem Transfer; der stabile Formzustand und die direkte
Innovationsantwort liefern einen stationaeren Gaussprozess fuer v.
Bei Pfadumkehr werden beide Inkremente gemeinsam negiert und die
Zeitreihen rueckwaerts gelesen (bis auf einen Indexshift). Die
gemeinsame Negation aendert die zentrierte Gaussverteilung nicht.
Zeitumkehrsymmetrie bedeutet daher hier genau symmetrische
Lagmatrizen $R(m)=\mathbb E[v(n+m)v(n)^T]$ fuer alle m bzw. eine
reelle Kreuzspektraldichte. Die Gaussannahme macht diese Bedingung
hinreichend, weil alle endlichen Verteilungen durch ihre Kovarianzen
bestimmt sind.

## 2. Exakte Klassifikation mit dem Altersfilter

Setze in der Notation des Paartransfer-Berichts

$$
P_i(z)=\sum_\ell p_{i\ell}z^{-\ell},\qquad
A_i(z)=\frac{z-s_i}{P_i(z)}-g_i,\qquad
\Delta(z)=A_A(z)A_B(z)-h_Ah_B.
$$

Die Center-Gleichung hat Diagonaleintraege $A_i$ und
Kreuzeintraege $-h_i$. Der Transfer von den Kopfinnovationen zu
den Center-Inkrementen ist

$$
\frac{1-z^{-1}}{\Delta(z)}
\begin{pmatrix}A_B(z)&h_A\\ h_B&A_A(z)\end{pmatrix}.
$$

Bei $z=e^{i\omega}$ ergibt Multiplikation mit der diagonalen
Rauschkovarianz und dem hermitesch adjungierten Transfer

$$
\operatorname{Im}S_{AB}^{v}(\omega)=
\frac{|1-z^{-1}|^2}{|\Delta(z)|^2}
\left[\sigma_A^2h_B\operatorname{Im}A_B(z)
-\sigma_B^2h_A\operatorname{Im}A_A(z)\right].
$$

Die gemeinsame Translationsnullstelle bei $z=1$ wird ueber
den bereits stationaeren Inkrementtransfer behandelt, nicht
durch eine fiktive stationaere Ortskovarianz.

**Satz.** Fuer gleiches $H\ge2$ und die obigen Annahmen sind die
beiden Center-Inkremente gemeinsam zeitumkehrsymmetrisch genau dann,
wenn gleichzeitig

$$
q_A=q_B,\qquad s_A=s_B,\qquad \sigma_A^2 h_B=\sigma_B^2 h_A.
$$

**Beweis der Notwendigkeit.** Auf dem Einheitskreis ist
$2i\,\operatorname{Im}A_i(z)=A_i(z)-A_i(z^{-1})$. Wenn sich die
Klammer fuer alle Frequenzen aufhebt, sind die so erhaltenen
gewichteten rationalen Funktionen identisch. Die Nullstellen von
$P_i$ liegen bei $q_i e^{2\pi i m/H}$, $m=1,\ldots,H-1$.
Keine davon kann der nichtnegative reelle Wert $s_i$ sein.
Jede ist damit ein Pol von $A_i(z)-A_i(z^{-1})$ im offenen
Einheitskreis, da die reziproken Pole ausserhalb liegen.
Unterschiedliche $q_i$ ergeben disjunkte Polkreise, sodass
kein positiver konstanter Rauschfaktor sie ausgleichen kann.

Bei gleichem q sind beide P identisch. Vergleiche das lineare
Wachstum bei $z\to\infty$: $A_i(z)\sim z/p_{i0}$ und
$A_i(z^{-1})$ bleibt beschraenkt. Das erzwingt gleiche
Gewichte $\sigma_A^2 h_B=\sigma_B^2 h_A$. Danach kann die
Differenz der beiden rationalen Funktionen nur verschwinden,
wenn $s_A=s_B$, weil $1/P(z)-1/P(z^{-1})$ nicht null ist.
Andere reelle konstante Anteile $g_i$ fallen aus der Differenz
heraus. Die drei Bedingungen sind durch Einsetzen auch hinreichend.
Fuer $H=1$ ist $P_i=1$; dort bleibt nur die Rauschbedingung.
Dies ist ein konkreter FIFO-Effekt, nicht eine allgemeine
Unmoeglichkeit von zeitumkehrsymmetrischen beobachteten Prozessen.

Der deterministische Testantrieb $+\mu_i F_i$ ist hiervon
getrennt. Seine Center-Kreuzantwort laesst sich stets durch
$h_A\mu_B=h_B\mu_A$ symmetrisieren; dieselbe Differenzbildung
multipliziert beide Antworten mit $1-z^{-1}$. Dieser Ausgleich
ersetzt keine der obigen stochastischen Bedingungen.

## 3. Endlicher Lag-Test und Bedeutung

Ein exakt nichtverschwindendes
$R_{AB}(m)-R_{BA}(m)$ belegt die statistische Zeitrichtung
im Beobachtungspaar. Im linearen endlichen Modell genuegen
die **ersten $2H-1$ positiven Lags** fuer die algebraische
Entscheidung. Im Translationsquotienten mit Matrix M_s der
Dimension $2H-1$ hat jede Inkrementausgabe eine Form aus
stabilem Zustand plus direkter Innovation. Daher kann man
$R(m)$ fuer $m\ge1$ als $J M_s^{m-1} Q$ mit festen J,Q
schreiben; der direkte Innovationsbeitrag ist in Q enthalten.
Cayley-Hamilton liefert eine Rekursion der Ordnung hoechstens
$2H-1$ fuer den antisymmetrischen Eintrag. Verschwindet er
exakt an so vielen aufeinanderfolgenden Lags ab eins, ist er
fuer alle Lags null. Bei Daten sind Fehlerintervalle und
eine unveraenderte Vorzeichenkonvention separat noetig.

**Physikalische Grenze.** Dies ist beobachtbare
Pfad-Zeitumkehr, nicht mechanischer Arbeitsport, lokales
detailliertes Gleichgewicht der vollen FIFO-Historie oder
eine gemessene Entropieproduktion. Zwei symmetrische
Einzelautokorrelationen und symmetrische mittlere Anstoesse
reichen insbesondere nicht fuer einen Gleichgewichtsabschluss.
Die Aussage widerlegt weder jede Fluktuations-Dissipations-
Beziehung mit anderen Annahmen noch eine nichtlineare
Quantisierung. Sie schliesst den direkten Schluss von
Center-Reziprozitaet auf reversibles gemeinsames Rauschen
bei heterogenem Memory im angegebenen Ansatz aus.

## 4. Literatur und Kontrolle

[Seara, Machta und Murrell, arXiv:1911.10696v3, Abschnitt II](https://arxiv.org/pdf/1911.10696)
verwenden frequenzaufgeloeste Gauss-Kreuzkovarianzen zur
Zeitumkehrdiagnostik und unterscheiden beobachtete Zeitrichtung
von thermodynamischer Identifikation. Die Polkreis-
Klassifikation fuer den endlichen FIFO und der endliche Lag-Test
folgen hier aus der konkreten diskreten Rekursion; kein
Entropieschaetzer oder nichtlineares Ergebnis wird importiert.

Die [festen Kontrollen](../../tests/test_memory_pair_time_reversal.py)
vergleichen den geschlossenen Transfer mit der vollen
History-Resolvente und einem unabhaengigen stabilen
Lyapunov-Quotienten. Sie pruefen den H=1-Gegenfall,
gleiche Retention mit unterschiedlichen $s_i$, Rauschmismatch
und einen reziproken Mittelwerttransfer mit asymmetrischen
Kreuzfluktuationen. Eine zusaetzliche Gegenprobe loest aus der
linearen Kovarianzgleichung genau ein vorgegebenes Lag null und
zeigt den verbleibenden Unterschied im naechsten Lag; kein Fit
an empirische Daten. Keine Stichprobe oder Auswertung eines
offenen Stabilitaetskandidaten.

Verifikation: 52 Tests im gezielten Panel bestanden, davon neun
neue Kontrollen. Das Panel umfasst zudem den Paartransfer,
die native Paarreduktion, endliche Abstaende, Potentialbilanz
und Markdown-Formeln. Keine volle Repository-Suite.
