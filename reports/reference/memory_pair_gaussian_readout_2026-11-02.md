# Nichtlinearer Readout im linearen Gaussvergleich

Stand: 2026-11-02; begonnen am 2026-11-01. Fortsetzung der
[endlichen Bahnschranke](memory_pair_path_envelope_2026-11-01.md).
**Analytische Erwartungswerte, keine neue Zielsimulation, kein Replay,
keine Parametersuche.** Der nichtlineare Kernel wird auf dem ausdruecklich
linearen Vergleichsprozess ausgewertet. Das ist keine Gaussannahme fuer
die native nichtlineare FIFO-Dynamik.

## Ergebnis und Entscheidung

Die erwartete nichtlineare Kontrastgroesse ist fuer den Vergleich nun
bestimmt, einschliesslich des Anfangstransienten und aller 600 Quellalter
im festen Fenster $10000\leq n<50000$. Fuer die erste Richtung:

| Groesse | Numerische Auswertung, interne Modelleinheiten |
| --- | ---: |
| Vollstaendiges Gaussintegral, erste Koordinate | 1.3611831152e-14 |
| Fuehrender kubischer Term | 1.3611837840e-14 |
| Globale obere Schranke des kubischen Restfehlers | 3.6051e-17 |
| Norm des linearen Referenzgradienten | 1.5286083074e-3 |
| Kontrast / linearer Referenzgradient | etwa 8.90e-12 |
| Bisherige obere Schranke des Transfers zur nativen Dynamik | 3.4789e-7 |

Die zweite Richtung ist in dieser Auswertung numerisch entgegengesetzt.
Die Schranke fuer den Modelltransfer ist rund 25 Millionen Mal groesser
als der berechnete Kontrast. **Das ist eine Luecke der Fehlerkontrolle,
keine Messung eines so grossen tatsaechlichen Modellfehlers.** Auch der
getrennte Beitrag seltener Ausnahmen ist mit 2.15e-12 bereits groesser
als der Vergleichskontrast. Deshalb ist dessen Vorzeichen/Amplitude
nicht als native Vorhersage aufgeloest.

Zudem besitzt der Mittelwerttest eine exakte Symmetrieblindheit: Ist
die mittlere Abfrageverschiebung null, liefern alle zentrierten
Gaussverteilungen fuer den ungeraden Gradienten null, auch bei
verschiedenen Kovarianzen und vorhandener Kopplung. Nichtnull ist ein
hinreichender Hinweis gegen die betreffende Produktgleichheit, null
jedoch kein Nachweis von Unabhaengigkeit.

**Konsequenz:** Kein kleines Nachweispanel fuer diesen mittleren
Readout am alten Anker vorbereiten und keine automatische Laufzahl-
oder Parametererhoehung. Die bisherige Diagnosevorbereitung ist mit
diesem begrenzten Resultat abgeschlossen; ihre fehlende native
Aufloesung wird nicht durch eine Vergleichsvorhersage ersetzt.
Fuer den Wasserstoff-Durchstich sind jetzt wieder die notwendigen
Strukturbedingungen entscheidend: physikalisch begruendete Energie-/
Arbeitsbilanz und eine geeignete langreichweitige Wechselwirkung.
Vorhandene skalare/vektorielle Memory- und Kernelvarianten sind daran
zu messen, bevor eine neue physikalische Regel zur Autorenentscheidung
vorgelegt wird. Ein nachgewiesener kleiner Korrelationskontrast waere
ohnehin noch keine Ladung, Masse, Bindung oder Quantisierung.

## 1. Welcher Vergleich exakt gerechnet wird

Notation und Anfangszustand stammen unveraendert aus der Bahnschranke.
Setze dort nur $R_i=t_i=0$. Dann gilt fuer die inneren Variablen:

$$
V_{n+1}=\lambda V_n+\frac{q\epsilon}{2}(\xi_{A,n}+\xi_{B,n}),\qquad
Z_{n+1}=AZ_n+\epsilon v(\xi_{A,n}-\xi_{B,n}),
$$

$$
Z=(D,E)^T,\quad v=(1,\alpha)^T,\quad e=(1,-1)^T,\quad
u_A=V+\tfrac12e^TZ,\quad u_B=V-\tfrac12e^TZ.
$$

Die dreidimensionale Zustandsangabe $(V,D,E)$ ist **pro raeumlicher
Koordinate** gemeint; sie behauptet keine emergente Raumdimension.
Gemeinsamer Ort $X$ besitzt eine neutrale Mode und wird nicht als
stationaer angenommen. $V,Z$ sind stabile lineare Filter.

Die Koeffizienten $g,h$ enthalten weiterhin die alte endliche Masse $W$.
Das Weglassen von $t$ entfernt aber den dynamischen FIFO-Rand. Ein
Readout ueber 600 Alterslags macht diesen Vergleich nicht wieder zu
einem exakten H=600-FIFO-Modell.

Fuer feste Anfangswerte und unabhaengige ideale Gaussinnovationen:

$$
P=APA^T+2\epsilon^2vv^T,\quad
P_n=P-A^nP(A^T)^n,\quad
s_V=\frac{\epsilon^2q^2}{2(1-\lambda^2)},\quad
s_{V,n}=s_V(1-\lambda^{2n}),
$$

$$
\mu_{A,n}=\lambda^nV_0+\tfrac12e^TA^nZ_0,\quad
\mu_{B,n}=\lambda^nV_0-\tfrac12e^TA^nZ_0,\quad
s_{u,n}=s_{V,n}+\tfrac14e^TP_ne.
$$

Alle Kovarianzen in diesen Formeln sind pro raeumlicher Koordinate.
Durch isotropes Rauschen sind die raeumlichen Kovarianzmatrizen ein
skalares Vielfaches von $I_d$, trotz der nichtverschwindenden
deterministischen Anfangsmittelwerte.

Fuer $k=n-\ell\geq0$ ist die zeitversetzte Kreuzkovarianz

$$
c_{n\ell}=\operatorname{Cov}(u_A(n),u_B(k))_{aa}
=\lambda^\ell s_{V,k}-\tfrac14e^TA^\ell P_ke.
$$

Die umgekehrte Knotenrichtung besitzt hier denselben Skalar. Im
stationaeren **inneren Vergleich**, nicht im nativen Modell, ersetzt
man $P_k,s_{V,k}$ durch $P,s_V$.

Fuer A ist die mittlere Abfrageverschiebung
$m_{n\ell}=R_*+\mu_{A,n}-\mu_{B,k}$. Gemeinsame und zwischen Replikationen
gekreuzte Abfrage haben denselben Mittelwert, aber Varianzen

$$
v_{\rm joint}=s_{u,n}+s_{u,k}-2c_{n\ell},\qquad
v_{\rm prod}=s_{u,n}+s_{u,k}.
$$

Fuer B wird $R_*$ negiert und A/B werden vertauscht. Die Erwartung des
bereits definierten disjunkten Replikationskontrasts ist daher die
Zeit-/Altersmittelung der Differenz dieser beiden Gaussintegrale.
Es werden keine Zeitpunkte als unabhaengige Stichproben gezaehlt.

## 2. Vollstaendiges Gaussintegral

Schreibe $K(z)=\sum_s A_s e^{-|z|^2/(2\sigma_s^2)}$, hier mit
$A_s=(1,-35)$ und $\sigma_s=(1,3)$. Quadratische Ergaenzung fuer
$Z\sim N(m,vI_d)$ und anschliessende Ableitung nach $m$ liefern

$$
\mathbb E\nabla K(Z)=
-m\sum_s\frac{A_s}{\sigma_s^2}
\left(1+\frac{v}{\sigma_s^2}\right)^{-d/2-1}
\exp\left[-\frac{|m|^2}{2(\sigma_s^2+v)}\right].
$$

Die Ableitung unter dem Integral ist wegen glatter beschraenkter
Gaussgradienten zulaessig; bei $v=0$ gilt die stetige Fortsetzung.
Allgemeiner ersetzt eine feste Kovarianz $\Sigma\succeq0$ den Skalar:
Jeder Summand ist

$$
-A_s\det(I+\Sigma/\sigma_s^2)^{-1/2}
e^{-m^T(\sigma_s^2I+\Sigma)^{-1}m/2}
(\sigma_s^2I+\Sigma)^{-1}m.
$$

Die skalare Implementierung nutzt keine Differenz zweier fast gleicher
voller Gradienten. Mit $L_s(v)=-(d/2+1)\log(1+v/\sigma_s^2)
-|m|^2/[2(\sigma_s^2+v)]$ wird die Exponentialdifferenz durch
`log1p` und `expm1` ausgewertet. Insbesondere

$$
L_s(v_j)-L_s(v_p)=
-(d/2+1)\log\left(1+\frac{v_j-v_p}{\sigma_s^2+v_p}\right)
+\frac{|m|^2(v_j-v_p)}{2(\sigma_s^2+v_j)(\sigma_s^2+v_p)}.
$$

Der groessere Exponent dient als Basis; das `expm1`-Argument ist
nichtpositiv. Das vermeidet Ausloeschung der winzigen Differenz und
unnuetige positive Exponentialueberlaeufe. Es ersetzt kein Intervall-
zertifikat. Eine unabhaengige 80-Dezimalstellen-Rechnung prueft die
Differenz direkt, weitere kleine Faelle nutzen Gauss-Hermite-Quadratur.

## 3. Fuehrende Korrektur und Symmetrieblindheit

Die globale Tayloridentitaet lautet

$$
\nabla K(z)=\kappa z+a_3z|z|^2+r_5(z),\quad
a_3=\frac12\sum_s\frac{A_s}{\sigma_s^4},\quad
|r_5(z)|\leq C_5|z|^5,\quad
C_5=\frac18\sum_s\frac{|A_s|}{\sigma_s^6}.
$$

Dabei ist $a_3=23/81$ ein **vorzeichenbehafteter Koeffizient** und
nicht die fruehere Betragsschranke $C_3=58/81$.
Die Restungleichung folgt aus $|e^{-t}-1+t|\leq t^2/2$ fuer $t\geq0$.
Fuer $Z\sim N(m,\Sigma)$ ergibt die Entwicklung $Z=m+\zeta$:

$$
\mathbb E[Z|Z|^2]=m(|m|^2+\operatorname{tr}\Sigma)+2\Sigma m.
$$

Zentrierte ungerade Gaussmomente verschwinden. Der kubische
gemeinsam-minus-Produkt-Kontrast ist somit allgemein

$$
a_3[(\operatorname{tr}\Delta\Sigma)I+2\Delta\Sigma]m.
$$

Mit Kreuzkovarianz $C=\operatorname{Cov}(u_A,u_B)$ gilt
$\Delta\Sigma=-(C+C^T)$. Im isotropen Vergleich reduziert sich das zu

$$
\boxed{\Delta G^{(3)}_{n\ell}=-2a_3(d+2)c_{n\ell}m_{n\ell}.}
$$

Der lineare Term verschwindet fuer beliebige Kopplung; der kubische
Term braucht sowohl eine Kreuzkovarianz als auch eine geeignete
mittlere Verschiebung. Bei $m=0$ verschwindet sogar das vollstaendige
Gaussintegral. Das ist eine Eigenschaft dieser Observablen, nicht
Abwesenheit der Kopplung. Auch bei $m\ne0$ kann die Kontraktion mit
$\Delta\Sigma$ oder die Altersmittelung Information verlieren.

Ein explizites globales Restbudget fuer jede Gaussdifferenz ist

$$
C_5\{M_6(m,v_j)^{5/6}+M_6(m,v_p)^{5/6}\},
$$

$$
M_6(m,v)=|m|^6+3(d+4)v|m|^4+
3(d+2)(d+4)v^2|m|^2+d(d+2)(d+4)v^3.
$$

Hier wurde $\mathbb E|Z|^5\leq(\mathbb E|Z|^6)^{5/6}$ verwendet.
Das Budget wird ueber genau dieselben Zeiten und Altersgewichte
gemittelt; keine lokale Taylorannahme an beobachteten Radien.

## 4. Was den Transfer zur nativen Dynamik verhindert

Bezeichne die vorherige ganze-Bahnen-Gaussmenge mit $G$, auf der sowohl
die native Bahn als auch ihr mit denselben Innovationen gekoppelter
linearer Vergleich kontrolliert sind. Die Bahnschranke gibt

$$
|u_i-u_i^{\rm lin}|\leq E_u=
\left[\frac q{1-\lambda}+\frac1h\right]LS^3+
\left[\frac1{1-\lambda}+\frac g{\alpha h}\right]T.
$$

Auf $G$ ist $|u_i|\leq U$, und der lineare Offset hat das kleinere
Budget $U-E_u$. Daher sind die vier Abfrageverschiebungen eines
Replikationskontrasts jeweils durch $r_*=|R_*|+2U$ beschraenkt.
Fuer den Rest nach Abzug des linearen Gradienten gilt
$|r(z)-r(z')|\leq3C_3\max(|z|,|z'|)^2|z-z'|$.
Jede Verschiebung aendert sich um hoechstens $2E_u$. Die vier Terme
mit Betrag der Kontrastgewichte insgesamt zwei liefern

$$
|D^{\rm rep}-D^{\rm rep}_{\rm lin}|\leq12C_3r_*^2 E_u
\quad\hbox{auf }G_1\cap G_2.
$$

Ausserhalb gilt die globale Differenzschranke $4M_g$, denn jeder
vollstaendige Gradienten-Kontrast ist durch $2M_g$ beschraenkt.
Die linearen Anteile heben sich in jedem Kontrast exakt auf; das
globale Budget wird nicht auf einen unbeschraenkten Taylorrest
angewendet. Insgesamt:

$$
|\mathbb ED^{\rm rep}-\mathbb ED^{\rm rep}_{\rm lin}|
\leq12C_3r_*^2E_u+4M_g\min(1,2\delta).
$$

Die numerisch ausgewertete rechte Seite ist `3.4788526624e-7`.
Sie ist gueltig unter den gleichen idealisierten arithmetischen und
Rauschannahmen wie die Bahnschranke; keine Rundungszertifizierung.
Eine so grobe obere Schranke erlaubt weder das Vorzeichen noch die
Amplitude des winzigen Vergleichssignals auf das native Modell zu
uebertragen. Sie beweist umgekehrt nicht, dass eine schaerfere Analyse
unmoeglich waere oder das native Signal gross sein muesste.

## 5. Auswertung und Quellen

[Vollstaendige Zahlen und Quellenhashes](memory_pair_gaussian_readout_2026-11-02.json),
[Erwartungswertrechner](../../src/emergenz_knoten/pair_gaussian_readout.py),
[feste Archivauswertung](../../experiments/current/reference/memory_pair_gaussian_readout.py),
[Tests](../../tests/test_pair_gaussian_readout.py).

Die Auswertung dauerte etwa 18.7 Sekunden auf einem BLAS-Thread.
Sie summiert die festen 40000 Auswertezeiten und 600 Quellalter, erzeugt
aber keine Punktbahnen, neuen Zufallszahlen oder Parametersuche.
Die gespeicherte Praeparation und das Vorzeichen $R_*=c_A-c_B$ bleiben
explizit erhalten. Der kleine gemeinsame Anfangstransient unterlaeuft
bei diesen spaeten Zeiten die binary64-Darstellung; keine exakte
Symmetrieaussage wird aus den identischen letzten Ziffern abgeleitet.

17 neue synthetische Tests pruefen Gaussintegral/Quadratur, direkte
80-dps-Differenz, kubische Schranke, Spiegel-/Austauschvorzeichen,
Nullmittel-Blindheit, finite Momente gegen eine unabhaengige 3x3-
Kovarianzrekursion, das komplette kleine Fenster samt Lags, deterministischen
Trend und unzulaessige Eingaben. Keine dieser Kontrollen ist eine native
H=600-Zielsimulation oder ein statistischer Powernachweis.

Verifikation: 207 betroffene Tests bestanden (darunter die 17 neuen),
vollstaendige konfigurierte Ruff-Pruefung und strikter MkDocs-Build
bestanden. Das prueft Software und Dokumentation, nicht die weiterhin
offene native Signalgroesse oder den gesamten Materiebenchmark.

Literatureinordnung: Die Kovarianzableitung von Gauss-Erwartungswerten
ist ein Standardresultat, kein neuer Memory-Satz.
[Voigtlaender, A General Version of Price's Theorem](https://arxiv.org/pdf/1710.03576),
Version 2 vom 2020-06-01, Einleitung, Theorem 1 und Abschnitt 1.2
(Seiten 1--3) wurden gelesen. Theorem 1 begruendet die glatte Abhaengigkeit
geeigneter Gauss-Erwartungswerte von positiver Kovarianz und die
Ableitung ueber raeumliche Ableitungen. Hier genuegen quadratische
Ergaenzung und elementare Gaussmomente; die Formeln sind oben
hergeleitet. Die Arbeit behauptet keine Gaussverteilung der nativen
FIFO-Zustaende und liefert keinen Fehler fuer diesen Modelltransfer.
Der Gesamtbeweis in Abschnitt 4 wurde nicht neu vollstaendig auditiert.
