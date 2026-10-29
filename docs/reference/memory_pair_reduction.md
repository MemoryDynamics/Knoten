# Memory-Paar: exakter Rest und bedingte Filtertraegheit

Stand: 2026-10-29. Analytische Fortsetzung des
[direkten Paar-Audits](hydrogen_pair_audit.md), keine Zielsimulation und
keine neue Modellregel. Referenzbasis ist
[`reciprocal_nodes.py` am Commit 0c471dc](https://github.com/MemoryDynamics/Knoten/blob/0c471dc5e040cdc85ecb744db1bf8ed913854f59/src/emergenz_knoten/reciprocal_nodes.py).

**Ergebnis:** Die native Paardynamik hat eine exakte Center-Gleichung mit
explizitem FIFO-Rand und nichtlinearem Rest. Die unten betrachtete autonome
Gleichung zweiter Ordnung laesst diese Terme weg. Im lokalen,
untrunkierten kontinuierlichen Vergleich besitzt sie eine positive
Filtertraegheit bei deklarierter Kraftnormierung. Weder diese Normierung
noch physikalische Arbeit und Teilchenmassen folgen dadurch aus Memory.
Fuer den rein attraktiven isotropen Vierzustandsabschluss gibt es zudem
eine enge analytische Grenze fuer freie schwach gedaempfte Schwingungen.

Die Einzelcenter-Filteridentitaet und $m_{\rm filter}=\tau/\mu_F$ stehen
bereits in der [Center-Notiz](scalar_memory_center_filter.md).
Neu hier sind ihre exakte Zuordnung zum heterogenen nativen Paar samt
Restschranke, die gemeinsame Kraftnormierungsbedingung und die
Anwendung einer bekannten Spektralschranke. Keine neue allgemeine
Traegheits- oder Laplace-Theorie wird beansprucht.

## 1. Exakter endlicher FIFO

Fuer $i=A,B$, $k\ne i$, seien $y_{ij,n}$ die nach Alter geordneten
Historienpunkte, $j=0,\ldots,H-1$, und

$$
q_i=1-\alpha_i,\quad w_{ij}=M_{0i}\alpha_i q_i^j,\quad
W_i=M_{0i}(1-q_i^H),\quad
\beta_i=\frac{\alpha_i}{1-q_i^H},\quad
c_{i,n}=\frac{\sum_jw_{ij}y_{ij,n}}{W_i}.
$$

Es gelten $0<\alpha_i\leq1$, $M_{0i}>0$ und gefuellter FIFO mit fester
Laenge. Die allgemeine State-API laesst auch andere positive Gewichte zu;
die folgende Identitaet setzt ausdruecklich **geometrische** Altersgewichte
voraus. Bezeichne den vor dem Schritt aeltesten Punkt mit
$o_{i,n}=y_{i,H-1,n}$. Nach synchronem Bewegungsupdate und FIFO-Schieben:

$$
c_{i,n+1}=q_i c_{i,n}+\alpha_i x_{i,n+1}+t_{i,n+1},\qquad
t_{i,n+1}=\beta_iq_i^H(x_{i,n+1}-o_{i,n}).
$$

Das folgt direkt durch Indexverschiebung der gewichteten Summe und
$\beta_i-\alpha_i=\beta_iq_i^H$. Fuer konsistente Bahninitialisierung ist
$o_{i,n}=x_{i,n-H+1}$; die Form mit $o$ gilt auch fuer beliebig vorbereitete
gefuellte Historien. Bei $\alpha_i=1$ ist $t=0$; bei $H=1$ kompensiert
der Randterm exakt die kuenstlich erscheinende Relaxation.

Schreibe den unveraenderten nativen Update als Identitaet

$$
x_{i,n+1}=s_i x_{i,n}+g_i c_{i,n}+h_i c_{k,n}+u_{i,n}+R_{i,n},
\qquad s_i=1-g_i-h_i.
$$

Hier sind $u_{i,n}=\epsilon_i\xi_{i,n}$ die tatsaechlichen additiven
Innovationen; die Identitaet gilt ebenso fuer einen deklarierten
additiven Testinput. Die festen lokalen Koeffizienten sind

$$
g_i=\eta_i\kappa_iW_i,\qquad h_i=\chi\kappa_\times W_k,
$$

mit Selbst-/Kreuzkruemmung am Ursprung der effektiven, bereits mit der
Deposition gefalteten Kernel. Fuer $K(z)=\sum_s A_s
e^{-|z|^2/(2\sigma_s^2)}$ ist $\kappa_K=-\sum_s A_s/\sigma_s^2$.
Ohne expliziten `cross_readout` stammt der gemeinsame Kreuzkernel aus der
ersten Konfiguration. Die Kreuz-Depositionskonvention stammt auch bei
explizitem Kreuzkernel aus der ersten Konfiguration, wie im Paar-Audit
dokumentiert.

Der Rest ist **definiert**, nicht zu null gesetzt:

$$
R_{i,n}=-\eta_i\left[G_i^{\rm self}-\kappa_iW_i(x_{i,n}-c_{i,n})\right]
-\chi\left[G_{i\leftarrow k}-\kappa_\times W_k(x_{i,n}-c_{k,n})\right].
$$

Setze $v_{i,n}=c_{i,n}-c_{i,n-1}$, eine Differenz pro Update, keine
bereits dimensionierte Geschwindigkeit. Aus
$\alpha_i x_{i,n}=c_{i,n}-q_i c_{i,n-1}-t_{i,n}$ folgt fuer $n\geq1$
nach einem bereits ausgefuehrten FIFO-Schritt exakt:

$$
\boxed{v_{i,n+1}=q_i s_i v_{i,n}
-\alpha_i h_i(c_{i,n}-c_{k,n})+\alpha_i u_{i,n}
+\alpha_i R_{i,n}+t_{i,n+1}-s_i t_{i,n}.}
$$

Die Vorzeichen von $g,h$ muessen fuer diese Identitaet nicht positiv sein.
Mitgefuehrte Rand- und Restterme enthalten weiterhin die volle Historie.
Die Gleichung ist daher **kein autonomer Zwei-Center-Abschluss**.

## 2. Was die weggelassenen Terme kontrolliert

Aus $|1-e^{-z}|\leq z$ fuer $z\geq0$ folgt fuer jeden solchen Kernel

$$
\left|G_K(x)-\kappa_K W(x-c)\right|
\leq B_K(x):=
\left(\sum_s\frac{|A_s|}{2\sigma_s^4}\right)
\sum_jw_j|x-y_j|^3.
$$

Damit gilt $|R_i|\leq|\eta_i|B_{{\rm self},i}
+\chi B_{\times,k}$ und fuer den gesamten Rest der Center-Gleichung

$$
|\mathcal R_{i,n}|\leq
\alpha_i\bigl(|\eta_i|B_{{\rm self},i,n}+\chi B_{\times,k,n}\bigr)
+\beta_iq_i^H\left(
|x_{i,n+1}-o_{i,n}|+|s_i|\,|x_{i,n}-o_{i,n-1}|\right).
$$

Das ist eine exakte, gegebenenfalls grobe obere Schranke auf einem
vorliegenden Zustand, kein bereits kleiner Fehler. Insbesondere:

- Ein kleines $q_i^H$ reicht ohne Kontrolle der auftretenden Abstaende
  nicht fuer einen kleinen FIFO-Rest.
- Ein kompakter Einzelknoten reicht nicht fuer die lokale Kreuznaeherung:
  auch die Abstaende zum **anderen** Gedaechtnis gehen kubisch ein.
  Ein weit getrenntes atomartiges Paar wird nicht durch die Entwicklung
  beider Kernel am Ursprung kontrolliert.
- Ein kleiner Ein-Schritt-Rest begrenzt noch nicht den Langzeitfehler.
  Dazu braucht es zusaetzlich Stabilitaets-/Propagatorschranken.

Fuer $\alpha_i=\Delta t/\tau_i+O(\Delta t^2)$ und festen physischen
Horizont $H\Delta t\to T$ bleibt $q_i^H\to e^{-T/\tau_i}$.
Dieser Grenzwert entfernt den FIFO-Rand nicht. Die untrunkierte Theorie
setzt einen anderen Grenzgang voraus; eine kleine Zeitschrittweite
allein rechtfertigt ihn nicht.

## 3. Kontinuierlicher lokaler Vergleich

Erst **nach** untrunkiertem exponentiellem Memory und lokalem quadratischem
Kernelabschluss betrachte den deterministischen, isotropen Vergleich

$$
\dot x_i=-a_i(x_i-c_i)-b_i(x_i-c_k)+\mu_iF_i,\qquad
\tau_i\dot c_i=x_i-c_i.
$$

Formal entspricht dies $g_i=a_i\Delta t$, $h_i=b_i\Delta t$,
$u_i=\mu_iF_i\Delta t$ im kleinen Zeitschritt. Es ist hier kein
Konvergenzsatz fuer das volle nichtlineare FIFO und kein stochastischer
Energieabschluss. $F_i$ ist ein **deklarierter** glatter Input mit
$\mu_i>0$; sein physikalischer Kraft-/Arbeitsbezug ist nicht geliefert.

Elimination von $x_i=c_i+\tau_i\dot c_i$ ergibt exakt innerhalb dieses
Vergleichsmodells

$$
\tau_i\ddot c_i+[1+\tau_i(a_i+b_i)]\dot c_i
+b_i(c_i-c_k)=\mu_i F_i.
$$

Somit lauten die formalen Koeffizienten

$$
m_i^{\rm filter}=\frac{\tau_i}{\mu_i},\qquad
\gamma_i=\frac{1+\tau_i(a_i+b_i)}{\mu_i},\qquad
k_i=\frac{b_i}{\mu_i}.
$$

Eine gemeinsame reziproke Paarenergie mit unveraenderten Centerkoordinaten
und Kraftports erfordert $k_A=k_B=:k$. Fuer den nativen gemeinsamen
lokalen Kreuzkanal $b_A=\zeta W_B$, $b_B=\zeta W_A$, $\zeta>0$, ist dies
aequivalent zu

$$
W_B\mu_B=W_A\mu_A.
$$

Die $W_i$ meinen hier die Quellengewichte des untrunkierten Vergleichs.
Gleiche Mobilitaeten genuegen bei ungleichen Quellengewichten nicht.
Mit frei waehlbaren positiven Mobilitaeten kann die Bedingung hingegen
erzwungen werden, etwa durch $\mu_i\propto1/W_i$. Die dann entstehende
Proportionalitaet $m_i^{\rm filter}\propto\tau_iW_i$ waere Folge der
gewaehlten Kraftnormierung, **kein gemessenes Massengesetz**.

Unter genau dieser zusaetzlichen Reziprozitaetsannahme ist das Verhaeltnis
allerdings nicht mehr unabhaengig waehlbar:

$$
\frac{m_A^{\rm filter}}{m_B^{\rm filter}}
=\frac{\tau_AW_A}{\tau_BW_B}.
$$

Bei identischen Relaxationszeiten und Quellengewichten liefert dieser
Abschluss gleiche Filtertraegheiten. Unterschiedliche Selbstrelaxationen
$a_i$ aendern hier die Daempfung, nicht diesen Traegheitskoeffizienten.
Eine geometrische Knotengroesse kommt in diese lokale Formel nicht vor.
Das ist eine bedingte Konsistenzanforderung fuer den gemeinsamen
Massen-/Wechselwirkungstest, keine Ableitung des Proton-Elektron-
Verhaeltnisses. Nachtraeglich passend gewaehlte $W_i$ oder $\tau_i$ waeren
Inputs, keine emergente Massenvorhersage. Fuer das volle nichtlineare FIFO
bleiben formabhaengige effektive Antworten damit ausdruecklich offen.

Bei gemeinsamem $k>0$ und $\gamma_i>0$ besteht algebraisch

$$
E=\frac12\sum_i m_i^{\rm filter}|\dot c_i|^2
+\frac{k}{2}|c_A-c_B|^2,\qquad
\dot E=\sum_i F_i\cdot\dot c_i-\sum_i\gamma_i|\dot c_i|^2.
$$

Diese Bilanz ist an den gewaehlten Center-Arbeitsport $F_i\,dc_i$ gebunden.
Ein Eingriff am aktuellen Punkt haette stattdessen die Leistung
$F_i\cdot\dot x_i=F_i\cdot\dot c_i+
\tau_iF_i\cdot\ddot c_i$. Der Unterschied darf nicht stillschweigend
entfallen. Ebenso ist der formale Gesamtimpuls nicht erhalten:
$\dot P=\sum_iF_i-\sum_i\gamma_i\dot c_i$ mit
$P=\sum_i m_i^{\rm filter}\dot c_i$.
Ein physikalisches Medium, das diese Arbeit und diesen Impuls aufnimmt,
ist dadurch nicht konstruiert. Fuer Rauschen kaemen stochastische
Energieterme hinzu; eine Fluktuations-Dissipations-Beziehung ist kein Input
der hier geprueften nativen Paardynamik.

## 4. Grenze freier Moden im attraktiven Vierzustandsabschluss

Nehme nun $a_i\geq0$, $b_i>0$, $\tau_i>0$ und $F_i=0$ an.
Pro entkoppelter Raumkomponente hat $z=(x_A,c_A,x_B,c_B)^T$ den Generator

$$
Q=\begin{pmatrix}
-(a_A+b_A)&a_A&0&b_A\\
1/\tau_A&-1/\tau_A&0&0\\
0&b_B&-(a_B+b_B)&a_B\\
0&0&1/\tau_B&-1/\tau_B
\end{pmatrix}.
$$

Alle Nebendiagonalen sind nichtnegativ und die Zeilensummen null;
$-Q$ ist eine gerichtete Laplace-Matrix. Die vier gerichteten Kreuz-/
Relaxationskanten bilden einen zusammenhaengenden Zyklus. Es gibt eine
gemeinsame Translationsmode bei null, alle anderen Moden klingen ab.

Der bekannte Spektralsektor fuer nichtnullige Eigenwerte einer
Laplace-Matrix der Ordnung $n$,
$|\arg\nu|\leq\pi/2-\pi/n$, ist in
[Agaev und Chebotarev (2005), S. 2, Gleichung (4)](https://arxiv.org/pdf/math/0508176)
mit Verweis auf Dmitriev und Dynkin angegeben. Seine Anwendung auf
$n=4$ und $\lambda=-\nu$ ergibt

$$
|\operatorname{Im}\lambda|\leq-\operatorname{Re}\lambda.
$$

Fuer eine freie komplexe Normalmode $\lambda=-\delta+i\omega$ folgt
somit nach einer Periode $T=2\pi/|\omega|$ die **modale** Daempfung

$$
\frac{A(t+T)}{A(t)}=e^{-\delta T}\leq e^{-2\pi}
\simeq0.00186744.
$$

Das sind hoechstens 0.187 Prozent der vorherigen Modenamplitude, kein
freier langlebiger Oszillator in diesem Abschluss. Das Resultat gilt auch
bei ungleichen $a,b,\tau$ und ohne die Kraft-Reziprozitaetsbedingung aus
Abschnitt 3. Die Kraftnormierung aendert die freien Eigenwerte nicht.

Die Schranke ist scharf: $a_A=a_B=0$, $\tau_A=\tau_B=\tau$ und
$b_A=b_B=1/\tau$ liefern
$\{0,-2/\tau,(-1+i)/\tau,(-1-i)/\tau\}$.
Bei identischen Parametern bestaetigt auch die relative Gleichung
$\tau\ddot r+[1+\tau(a+b)]\dot r+2br=0$ dieselbe Grenze, denn
$[1+\tau(a+b)]^2\geq(1+\tau b)^2\geq4\tau b$.

**Geltungsbereich:** Kontinuierlich, lokal linear, isotrop, untrunkiert,
attraktive Vorzeichen, vier skalare Zustaende je entkoppelter Komponente.
Mehr Raumdimensionen allein wiederholen hier dieselben Bloecke.
Zusaetzliche innere Relaxationsmoden, der volle FIFO, anisotrope Kopplung,
negative Kruemmungen oder nichtlineare endliche Abstaende sind damit
nicht beurteilt. Ebenso wenig betrifft die Aussage erzwungene Antwort,
Rauschspektren, allgemeine nichtnormale Transienten oder quantenmechanische
stationaere Zustaende. **Kein allgemeines No-go fuer Knoten, Atome oder
emergente Physik; kein Nachweis einer schwachen Wechselwirkung.**

## 5. Verifikation und Konsequenz

[14 neue synthetische Tests](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_memory_pair_reduction.py)
pruefen die endliche Center-Identitaet gegen den unveraenderten nativen
Simulator: zwei konstruierte H=5-Paare, je sieben Schritte, ungleiche
Gewichte/Relaxationen, 3D mit Punktdeposition und 4D mit Gaussdeposition.
Beide Historien lesen denselben alten Paarzustand, auch ueber den
Ringpufferumlauf hinweg. Rand- und nichtlinearer Rest sind in diesen
Kontrollen jeweils nachweislich nicht null.

Weitere Checks betreffen die Endfaelle $\alpha=1$ und $H=1$, die kubische
Schranke, exakte Koordinatentransformation der kontinuierlichen Gleichung,
formale Energiebilanz, drei feste Vierzustandsmatrizen und die scharfe
Zykluskontrolle. Eine feste negative Selbstkruemmung verletzt die
Spektralschranke und sichert damit ihre Vorzeichenbeschraenkung ab.
Die allgemeinen Aussagen folgen aus der Algebra und dem zitierten Satz,
nicht aus den endlich vielen Testpunkten. Keine Parametersuche oder
Wiederverwendung einer FIFO-/P5-/AL1-Ausfuehrungsfreigabe.

Verifikation am 2026-10-29: **111 betroffene Tests bestanden in 2.90 s**,
darunter die 14 neuen Checks, bisherige Paar-/Moden-/Kerneltests,
AL1-Archivkontrollen und Dokumentationstests. Lint, strikter MkDocs-Bau
und Patchpruefung bestehen. Keine vollstaendige Repository-Testsuite;
die Produktionsdynamik und alle archivierten Zielbefunde bleiben unveraendert.

Der Anschluss an den Wasserstoff-Benchmark ist damit enger bestimmt:
Ein gefitteter zweiter Ableitungsterm genuegt weder fuer Masse noch fuer
eine tragfaehige innere Teilchenmode. Eine weitergehende Reduktion muss
ihren Rest und Beobachtungsbereich kontrollieren sowie Kraft und Arbeit
unabhaengig festlegen. Ein angenommener Quanten-/Coulombbaustein aus der
Referenzrechnung schliesst diese Luecke nicht. Die naechste Arbeitswahl
steht ausschliesslich in den [Projektprioritaeten](../status/project_priorities.md).
