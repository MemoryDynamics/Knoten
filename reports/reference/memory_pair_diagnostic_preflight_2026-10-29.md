# Paar-Diagnose: lineare Blindheit des Mittelwerttests

Stand: 2026-10-29. **Methodischer Vorabcheck und Diagnoseentwurf, nicht
ausfuehrungsreif oder freigegeben.** Keine Zielbahn berechnet, kein Replay,
keine neue Kopplung und keine Parameteranpassung. Anschluss an
[Mittelungsbedingungen](../../docs/reference/memory_pair_finite_separation.md)
und [Archiv-/Fensterpruefung](memory_pair_archive_audit_2026-10-29.md).

**Entscheidender Befund:** Bei einem linearen Gradienten kann selbst
perfekte Phasenkopplung denselben mittleren Readout wie ein Produkt
unabhaengiger Randverteilungen liefern. Ein kleiner mittlerer Balance-
oder Produktfehler bestaetigt deshalb nicht den gesuchten nichttrivialen
Mittelungsmechanismus. Die Diagnose muss den bekannten linearen Anteil,
Fenster-/Randverteilungseffekte und verbleibenden Lagkontrast trennen.
Dies ist eine Identifizierbarkeitsgrenze dieser Observable, kein No-go
fuer effektive Mechanik oder andere Observablen.

## 1. Exakte endliche Datenzerlegung

Waehle ein Fenster $I=[a,b)$ mit $T=b-a$ auf **lueckenlos synchronisierten**
Punktfolgen $v_A(n),v_B(n)$ und einen festgehaltenen Referenzabstand $R$.
Die normierten Altersgewichte $p_{i\ell}$ duerfen verschieden sein.
Alle benoetigten Vergangenheitswerte muessen vorliegen. Es wird hier
weder Stationaritaet noch Unabhaengigkeit vorausgesetzt. Mit $g=\nabla K$:

$$
F_A=\frac1T\sum_{n\in I}\sum_\ell p_{B\ell}
g(R+v_A(n)-v_B(n-\ell)),\qquad
F_B=\frac1T\sum_{n\in I}\sum_\ell p_{A\ell}
g(-R+v_B(n)-v_A(n-\ell)).
$$

$F_i$ sind hier **quellen-normalisierte Gradienten**, keine physikalisch
identifizierten Kraefte. Definiere empirische Gegenwarts- und gemischte
Vergangenheitsverteilungen

$$
\mu_i=\frac1T\sum_{n\in I}\delta_{v_i(n)},\qquad
Q_i=\frac1T\sum_{n\in I}\sum_\ell p_{i\ell}\delta_{v_i(n-\ell)}.
$$

Vergleiche drei explizite Produkte:

$$
P_0=\iint g(R+u-v)\,d\mu_A(u)d\mu_B(v),\quad
P_A=\iint g(R+u-v)\,d\mu_A(u)dQ_B(v),\quad
P_B=\iint g(-R+v-u)\,d\mu_B(v)dQ_A(u).
$$

Die **lagangepassten Produktkontraste** sind $C_A=F_A-P_A$ und
$C_B=F_B-P_B$. Anders als $F_A-P_0$ vergleichen sie dieselben aktuellen
und historischen Randverteilungen. $P_A-P_0$ bzw. $P_B+P_0$ erfassen
deren endliche Fensterverschiebung. Fuer den geraden Kernel ist $g$
ungerade, daher ist der umgekehrte Gegenwartsproduktwert $-P_0$.

Die marginale Vergangenheitsmischung laesst sich ohne $T^2H$-Schleife
auswerten: Auf den Quellindizes $a-H_i+1,\ldots,b-1$ lauten ihre
Gewichte $q_i=(\mathbf1_T/T)*\operatorname{reverse}(p_i)$, wobei $*$
die diskrete Faltung bezeichnet. Damit kostet die genaue Auswertung
$O(T(H_A+H_B)+T^2)$; Blockbildung senkt den Speicherbedarf, nicht diese
Rechenordnung. Das ist noch keine Laufzeitfreigabe fuer grosse Fenster.

## 2. Warum der lineare Anteil keine Unabhaengigkeit erkennt

Fuer $g(z)=\kappa z$ haengt jeder dieser Erwartungswerte nur von den
jeweiligen ersten Momenten ab. Daher gilt **fuer beliebige endliche
Folgen**, auch korrelierte und nichtstationaere,

$$
C_A=C_B=0,\qquad
F_A-P_0=L_A:=\kappa\left(\langle v_B\rangle_I
-\sum_\ell p_{B\ell}\langle v_B(n-\ell)\rangle_I\right),
$$

$$
F_B+P_0=L_B:=\kappa\left(\langle v_A\rangle_I
-\sum_\ell p_{A\ell}\langle v_A(n-\ell)\rangle_I\right).
$$

Die $L_i$ sind reine Rand-/Mittelwertverschiebungen. Bei vollstaendigen
Perioden eines periodischen Beispiels verschwinden sie exakt. Zwei
identische oder fest phasenversetzte Zyklen bestehen damit den linearen
Produktvergleich trotz perfekter Abhaengigkeit. Es wird kein linearer
Koeffizient an diese Daten gefittet: $\kappa=D^2K(0)$ ist vorgegeben.
Eine lineare effektive Wechselwirkung kann trotzdem sinnvoll sein;
dieser Test wuerde nur keine zusaetzliche Struktur gegen sie nachweisen.

Fuer den wirklichen effektiven Gausskernel, einschliesslich etwaiger
Write-/Read-Faltung, schreibe $g(z)=\kappa z+r(z)$. Der
[Auswerter](../../src/emergenz_knoten/pair_lag_diagnostics.py) liefert exakt

$$
F_A-P_0=L_A+M_A+C_A,\qquad F_B+P_0=L_B+M_B+C_B,
$$

wobei $M_A=P_A^{(r)}-P_0^{(r)}$ und
$M_B=P_B^{(r)}+P_0^{(r)}$ die **nichtlinearen** marginalen
Fensterverschiebungen sind. Der Index $(r)$ bedeutet Auswertung nur des
Rests. Die linearen Anteile von $C_i$ verschwinden identisch; diese
Kontraste werden deshalb direkt aus $r$ berechnet. Blosses Abziehen der
$L_i$ wuerde $M_i$ irrtuemlich als Kopplungsrest mitzaehlen.

Auch $C_i\ne0$ ist allein kein statistischer Interaktionsnachweis:
gemeinsame zeitliche Trends, endliche Stichproben und fehlende Mischung
koennen solche empirischen Kontraste erzeugen. Umgekehrt beweist $C_i=0$
bei einem festen Kernel/Abstand keine Unabhaengigkeit der Prozesse.
Das Produkt ist ein Vergleich, keine durch Umordnen gewonnene unabhaengige
Replikation und kein automatisch gueltiger Permutations-p-Wert.

## 3. Restgroesse und stabile Auswertung

Fuer $K(z)=\sum_s A_s e^{-|z|^2/(2\sigma_s^2)}$ gilt wie in der
[Paarreduktion](../../docs/reference/memory_pair_reduction.md)

$$
\kappa=-\sum_s A_s/\sigma_s^2,\qquad
|r(z)|\leq C_3|z|^3,\qquad C_3=\frac12\sum_s|A_s|/\sigma_s^4.
$$

Insbesondere $|C_A|\leq C_3(m_{3,A}^{\rm lag}+m_{3,A}^{\rm product})$,
mit den dritten Abstandsmomenten derselben gemessenen Paarung und des
lagangepassten Produkts; analog fuer B. Eine kleine obere Schranke ist
kein positiver Nachweis eines messbaren Restes. Der Code berechnet $r$
ueber `expm1`, also $-\sum_s(A_s/\sigma_s^2)z\,\operatorname{expm1}(-|z|^2/(2\sigma_s^2))$, statt zwei fast gleiche
volle Gradienten zu subtrahieren. Das vermeidet diese Ausloeschung,
ersetzt aber keine Rundungs-/Statistikfehlerschranke.

Eine ausschliesslich geometrische
[Auswertung des archivierten P3.1-Anfangscheckpoints](memory_pair_initial_readiness_2026-10-29.json)
verwendet die alten Abstaende, Rotation und Kernelparameter unveraendert:
$H=600$, $d=3$, $R_{\rm rms}=2.11653\,10^{-4}$,
$|R|=5.29134\,10^{-4}$, $\kappa=26/9$, $C_3=58/81$.

| Richtungsreadout | Norm des linearen Gradienten | Kubische obere Schranke | Schranke / linear |
| --- | --- | --- | --- |
| A liest B | $1.81421\,10^{-3}$ | $2.18578\,10^{-10}$ | $1.20481\,10^{-7}$ |
| B liest A | $1.86069\,10^{-3}$ | $2.34254\,10^{-10}$ | $1.25896\,10^{-7}$ |

Das sind quellen-normalisierte **Ein-Zustands-Schranken**, numerisch in
binary64 ausgewertet, keine Intervallzertifikate. Sie beschraenken weder
die spaetere Bahn noch direkt den gesuchten Zeitkontrast $C_i$. Ein
Prozentvergleich koennte an diesem Anfangszustand aber offenkundig keine
Abweichung von der lokalen Linearantwort identifizieren. Eine konkrete
Power- oder Lauflaengenbehauptung folgt daraus nicht. Es gab keine neue
Simulation; der erste reine Auswertungsaufruf stoppte bereits beim
Import wegen eines unvollstaendigen Abhaengigkeitspfads. Mit dem bereits
vorhandenen vollstaendigen Pfad wurde danach diese Arithmetik ausgefuehrt.

## 4. Anschluss an bewegte native Knoten

Wenn $v_i(n)=x_i(n)-c_i(n)$ mit den momentanen Memory-Centern verwendet
wird, ist der eingefrorene Readout noch nicht der native Gradient.
Mit $R(n)=c_A(n)-c_B(n)$ und festem $R_*$ gilt exakt

$$
x_A(n)-x_B(n-\ell)=R_*+v_A(n)-v_B(n-\ell)
+[R(n)-R_*]+[c_B(n)-c_B(n-\ell)].
$$

Die globale Hessianschranke $L_2=\sum_s|A_s|/\sigma_s^2$ gibt

$$
|\langle G_{A\leftarrow B}/W_B\rangle-F_A^{\rm frozen}|
\leq L_2\left(\langle|R(n)-R_*|\rangle
+\sum_\ell p_{B\ell}\langle|c_B(n)-c_B(n-\ell)|\rangle\right).
$$

Bei B wird die Quellbewegung von A eingesetzt. Der Auswerter berechnet
diese Geometriefehler **noch nicht**; sie duerfen nicht als null gelten.
Die Wahl des Referenzabstands und der Fenster ist vor einem Ziellauf
festzulegen. Zeitabhaengiges Nachzentrieren oder Ausrichten ist keine
kostenlose stationaere Eichung. Es erfordert die entsprechende
Historienkorrektur. Insbesondere wird die gemeinsame Translation nicht
aus den Relativdaten weggeworfen und danach als unbewegte Quelle behandelt.

## 5. Anforderungen vor einer Ausfuehrung

Der deterministische Auswertevertrag steht; das statistische und
technische Ausfuehrungsprotokoll bleibt offen. Erforderlich sind:

1. Dichte Roharchivierung gemaess Archivvertrag, exakte Indizierung und
   Abgleich der aus den Rohdaten rekonstruierten nativen Gradienten.
2. Festgelegte Fenster/Referenzabstaende und getrenntes Fehlerbudget fuer
   Centerbewegung, Randverteilungen, Rundung und endliche Statistik.
3. Auswertung von $L_i$, $M_i$, $C_i$ und den Restschranken neben dem
   vollen mittleren Readout; keine nachtraegliche lineare Nachanpassung.
4. Ein begruendetes Unsicherheitsverfahren fuer zeitkorrelierte Folgen.
   Fenstervariation allein beweist keine Stationaritaet; viele Fenster
   derselben Bahn sind keine unabhaengigen Replikationen. Neue Rauschpfade
   aus einem Checkpoint pruefen nur dieses Formationsbecken bedingt.
5. Entscheidungsgrenzen, Laufzeitbudget, gepruefter begrenzter Runner und
   gesonderte Autorenfreigabe. Bis dahin keine Wiederholung von P3.1.

Ein nicht aufgeloester nichtlinearer Kontrast heisst **kein Nachweis ueber
die bekannte lineare Antwort hinaus**, nicht Bestaetigung der allgemeinen
Produktannahme. Ein aufgeloester Kontrast kann diese konkrete Produkt-
naeherung begrenzen; er identifiziert weder Quarks noch Ladung oder Masse.
Selbst ein kontrollierter mittlerer Drift ist noch kein autonomer
Langzeitabschluss mit physikalischer Arbeit, Energie oder Quantisierung.
Die [Projektprioritaeten](../../docs/status/project_priorities.md) bleiben
die einzige aktive Arbeitsreihenfolge.

## 6. Literaturabgleich und Tests

[Schreiber und Schmitz, *Surrogate time series*, arXiv:chao-dyn/9909037v1](https://arxiv.org/pdf/chao-dyn/9909037),
Einleitung, Abschnitte 7.2 und 8: Geprueft wurden die Unterscheidung
zwischen nichtlinearem System und identifizierbarer Nichtlinearitaet der
Observable sowie die Warnung vor falschen Nullhypothesen bei
Nichtstationaritaet. Hier wird kein Surrogat-p-Wert implementiert.

[Legoll und Lelievre, *Effective dynamics using conditional expectations*, arXiv:0906.4865v1](https://arxiv.org/pdf/0906.4865),
Einleitung und Voraussetzungen/Aussage von Proposition 3.1: Ein passender
Gleichgewichts-Readout und kontrollierte Dynamik sind verschiedene
Anforderungen. Der dortige Marginalfehler nutzt unter anderem uniforme
bedingte logarithmische Sobolev-Ungleichungen und Kopplungsschranken fuer
eine ueberdaempfte Gibbs-Langevin-Dynamik. Diese Voraussetzungen sind fuer
unseren FIFO nicht gezeigt; der Beweis wurde hier nicht uebertragen.

[Glatzel und Schilling, arXiv:2107.01111v4](https://arxiv.org/pdf/2107.01111),
Einleitung und Diskussion von Gleichungen (21)--(23): Nichtlineares
Potential mittlerer Kraft, linearer Memoryterm und eine einfache
Fluktuations-Dissipations-Beziehung folgen nicht allgemein gemeinsam
aus Projektion. Ein entsprechender Ansatz fuer unsere Knoten waere
weiter zu begruenden. Keine neue Hamiltonstruktur aus diesem Vergleich.

Vierzehn [kleine Tests](../../tests/test_pair_lag_diagnostics.py) bestehen:
native Gradienten gegen die endliche Zerlegung bei ungleichen Horizonten
in 2D/5D, explizite lagangepasste Produkte gegen Faltungsgewichte,
phasengekoppelte lineare Fehlpositive, Restschranken, kubische Skalierung,
70-stellige Kontrollen fuer `expm1`, ungueltige Eingaben und unabhaengiger
statischer Platzierungsabgleich des gespeicherten Checkpoints. Die Zyklen
sind vorgeschriebene Folgen, keine nachgewiesenen nativen Bahnen.

Verifikation: **156 betroffene Tests bestanden in 3.78 s**, einschliesslich
der 14 neuen Kontrollen und der bisherigen Paar-, Kernel-, Archiv- und
Dokumentationsregressionen. Konfigurierter Lintcheck und strikter MkDocs-
Bau bestehen. Keine vollstaendige Repository-Testsuite und keine
experimentelle Validierung einer neuen effektiven Teilchenmechanik.
