# Stabilitaetsausschluesse fuer den abgeflachten FIFO-Vierzyklus

Stand: 2026-11-21. Analytische Gebietsaussagen aus der
[3D-Spur](memory_shape_quotient_2026-11-16.md) und dem
[Normalblock](four_cycle_extra_dimensions_2026-11-20.md).
Kein Parameterscan, keine Zieltrajektorie, kein einzelner
nativer Kandidat ausgewertet.

**Ergebnis.** In der gleichbreiten attraktiven Familie ist
ein auf der exakten Bahn innenliegender Feldnullpunkt mit
sehr kleinem Bahnradius **nicht** vereinbar mit 3D-Formstabilitaet.
Sehr grosse Hoehe ist ebenfalls ausgeschlossen, auch ohne
Innenlageannahme. Eine vierte Ortsdimension hat fuer
innenliegende Defekte einen groesseren Ausschlussbereich:
Bei $f\geq 1/2$ waechst der echte Normalformfehler trotz
moeglicher 3D-Stabilitaet. Dies ist auch eine nichtlineare
Abstossung von der eingebetteten Bahn fuer Stoerungen mit
nichtverschwindendem Vierervolumen, nicht fuer starre Kippungen.

Bei festem Seitenverhaeltnis und fester normierter Vergessensrate
hat der Normalfaktor genau einen Uebergang zwischen Wachstum
und Kontraktion. Nahe dem oberen Seitenverhaeltnisrand bleibt
kein voll stabiler eingebetteter Vierzyklus mit innenliegendem
Defekt uebrig: Die 4D- und 3D-Ausschluesse ueberdecken sich.

## 1. Modellklasse und gemeinsame Abschaetzungen

Verwendet wird die [positive abgeflachte Familie](flat_memory_cycle_2026-11-16.md)
mit $H_s=H_v=4$, ohne Rauschen, Delta-Deposition, gemeinsamem
Skalar-/Vektor-Gaussradius $\sigma$ und rein attraktivem
Skalarkernel. Schreibe

$$
R=r^2/\sigma^2,\quad Z=h^2/\sigma^2,\quad
t=Z/R\in(0,1/4),\quad f=e^{-2R},\quad g=e^{-(R+2Z)}.
$$

Die Existenzgleichungen geben $0<s<q<1$ und
$B=1/\Delta>0$. Aus

$$
\Delta=(1-gq)s^2-q^2(f-gq)
$$

folgt durch $s<q$ ohne weitere Parameterrechnung

$$
0<\Delta<q^2(1-f)<\min(1,2R).
$$

Strikte Innenlage im urspruenglichen 3D-Tetraeder ist
gleichbedeutend mit

$$
-\log q<\frac{2ZR}{R+4Z}=\frac{2t}{1+4t}R<R/4.
$$

Im Folgenden bezeichnet Innenlage immer diese Ausgangsgeometrie.
Der Gaussfeld-Nullpunkt ist nach Einbettung kein regulaerer
isolierter Punktdefekt des 4D-Felds, sondern Teil einer Linie.
Alle Parameter bleiben waehrend einer Stoerung fest. Aussagen
entlang einer Familie vergleichen verschiedene Modelle, nicht
eine Parameter-Nachregelung des Orbits.

## 2. Zwei intrinsische 3D-Ausschluesse

Die Summe der acht echten mitgedrehten 3D-Formmultiplikatoren ist

$$
T=-4Z+B U,\qquad
U=\gamma-gq^3+2Rgq+(2R-4Z)fq^2-4Z,\qquad
\gamma=\frac{4Z}{2R+4Z}<1/3 .
$$

Sobald $T<-8$, besitzt mindestens eine Formmode Betrag groesser
eins. Verschiebungen, Drehungen und der aelteste Laengen-Nullfaktor
haben keinen Beitrag zu T.

**Kleiner Radius mit Innenlage.** Aus $g>e^{-3R/2}$ und
$q>e^{-R/4}$ folgt $gq^3>e^{-9R/4}$. Damit

$$
U<\tfrac13-e^{-9R/4}+4R
<-\tfrac23+\tfrac{25}{4}R.
$$

Die zweite Abschaetzung verwendet $e^{-x}>1-x$ fuer $x>0$.
Fuer $R\leq 8/267$ ist die rechte Seite hoechstens $-16R$.
Mit $B>1/(2R)$ folgt $T<-8$. Die Schranke gilt **gleichmaessig**
in t und q unter strikter Innenlage; sie schickt q nicht bei
fester Geometrie gegen null.

**Grosse Hoehe ohne Innenlageannahme.** Mit $q<1$,
$g\leq e^{-R}$ und $f=e^{-2R}$ folgt

$$
U<\tfrac13+2R(e^{-R}+e^{-2R})-4Z
\leq\tfrac13+3/e-4Z<\tfrac{11}{6}-4Z.
$$

Das verwendet das Maximum von $x e^{-x}$ bei $x=1$ und
$e>2$. Fuer $Z\geq 5/4$ ist U negativ. Da $B>1$,
ist $T<11/6-8Z\leq -49/6<-8$. Beide Zahlen sind
hinreichende Ausschlussschranken, keine scharfen Grenzwerte.

## 3. Radiusgrenze in einer weiteren Ortsdimension

Pro weiterer Ortsdimension ist der echte Ein-Schritt-Formfaktor
$\kappa=Bq^3g>0$. Aus der Kraftbilanz folgt exakt

$$
\kappa>1\quad\Longleftrightarrow\quad
s^2(1-gq)<fq^2.
$$

Bei Innenlage gilt $q>f^{1/8}$, waehrend $g>f^{3/4}$.
Also $gq>f^{7/8}>f$. Fuer $f\geq 1/2$ folgt $gq>1-f$;
wegen $s<q$ ist die rechte Ungleichung dann strikt erfuellt.
**Eine 4D-Einbettung scheitert damit bereits transversal**,
unabhaengig von den noch offenen intrinsischen 3D-Moden.
Die Aussage betrifft keine vier internen Spinorkomponenten.

### Genau ein normaler Uebergang entlang eines Strahls

Halte t und $u=-\log q/R$ fest, mit
$0<u<2t/(1+4t)$. Damit bleibt die Innenlage bei jeder
Variation von R erhalten. Setze

$$
a=1+2t,\quad A=a+u,\quad b=2-a+u,\quad c=6-4a>0.
$$

Aus $s=qg(g-fq)/(f(1-gq))$ ergibt sich als exakter Test

$$
J(R)=e^{cR}\frac{(1-e^{-bR})^2}{1-e^{-AR}},\qquad
\kappa>1\ \Longleftrightarrow\ J(R)<1,
$$

mit umgekehrter Ungleichung fuer Kontraktion. Denn
$J=g^2(g-fq)^2/[f^3(1-gq)]$. Es gilt $0<b<A$.
Die Funktion $x/(e^{xR}-1)$ faellt fuer festes $R>0$
streng in x. Daher

$$
\frac{d}{dR}\log J
=c+\frac{2b}{e^{bR}-1}-\frac{A}{e^{AR}-1}>0 .
$$

J geht bei $R\downarrow0$ gegen null und bei
$R\uparrow\infty$ gegen unendlich. Es gibt genau ein
$R_*(t,u)$ mit $J=1$: darunter echter Normalformzuwachs,
darueber Kontraktion dieser Mode allein. An der Grenze
ist der lineare Ringschlussfehler konstant. Pro Viererperiode
gilt fuer den vollen linearen Normalblock
$N^4z-z=(z_0-z_4)(1,1,1,1,1)^T$:
Der sekulaere lineare Anteil ist eine Translation, kein
Wachstum der reinen Formabweichung. Die nichtlineare
Stabilitaet genau an der Grenze bleibt offen.

### Ein ganzes ausgeschlossenes Seitenverhaeltnisband

Ein expliziter, konservativer Bereich ist
$999/4000\leq t<1/4$. Setze $R_0=5/(4t)$, sodass
$R\geq R_0$ wegen $Z\geq 5/4$ schon in 3D instabil ist.
Fuer $R_0$ gelten mit $u<1/4$ die einfachen Schranken

$$
b R_0<4,\qquad cR_0\leq 10/999<1/81.
$$

Da $b<A$, ist $J(R_0)<e^{cR_0}(1-e^{-bR_0})$.
Aus $e<3$ folgt $e^{-bR_0}>e^{-4}>1/81>cR_0$.
Somit $1-e^{-bR_0}<1-cR_0\leq e^{-cR_0}$ und
$J(R_0)<1$. Wegen Monotonie gilt das fuer jedes
$R\leq R_0$. Also gibt es in diesem Seitenverhaeltnisband
bei strikter Innenlage **keinen stabilen eingebetteten
Vierzyklus**: Bis zur Hoehenschranke wirkt der Normalblock,
danach die intrinsische 3D-Instabilitaet.

## 4. Nichtlineare Bedeutung der transversalen Abstossung

Schreibe $W(Y)$ fuer das orientierte Vierervolumen und
$a_4(Y)$ fuer den Koeffizienten des aeltesten Vorgaengers.
Die [native exakte Bilanz](four_cycle_extra_dimensions_2026-11-20.md)
gibt $W(Y^+)=a_4(Y)W(Y)$ und am Orbit $|a_4(Y_*)|=\kappa$.
Ist $\kappa>1$, waehle $1<\rho<\kappa$. Stetigkeit bei
nichtverschwindenden Schritten und euklidische Invarianz
von $|a_4|$ liefern einen euklidisch invarianten Nahbereich
aller Orbitsphasen mit $|a_4|>\rho$. Relative Punktabstaende
sind darin beschraenkt, also auch $\|W\|\leq M$.

Jede anfangs vierdimensional aufgespannte Geschichte in
diesem Bereich muss ihn verlassen: Waere sie n Schritte
darin, gaelte $\|W(Y_n)\|\geq\rho^n\|W(Y_0)\|$,
was spaetestens fuer $n>\log(M/\|W(Y_0)\|)/\log\rho$
widerspruechlich ist. Solche Anfangshistorien liegen
beliebig nahe am Orbit, etwa durch eine kleine
Normalauslenkung des aeltesten Vorgaengers bei festem
aktiven Tetraeder. Starre Kippung hat dagegen $W=0$
und ist nicht von dieser Abstossung betroffen. Die
Bilanz beschreibt keine globale Dimensionsauswahl,
keine Lebensdauer unter Rauschen und keinen Spin.

## 5. Einordnung und Kontrollen

[Sarkar, PRE 112, 054111 (2025)](https://doi.org/10.1103/t7nk-4p57)
untersucht ebenfalls Transversalstabilitaet unter
Eigenmemory. Das dortige kontinuierliche Skalarfeld
mit spatiotemporaler Faltung ist nicht das hier
verwendete feste Skalar-/Alignment-FIFO. Im verwandten
Rotationsproblem von [Sidorenko und Thunberg](https://arxiv.org/html/2610.28341v1)
werden Zusatzrichtungen getrennt behandelt; kein
Stabilitaetsergebnis wird auf das FIFO uebertragen.

Die [sechs festen neuen Kontrollen](../../tests/test_four_cycle_stability_exclusions.py)
pruefen die Algebra mit formalen Faktoren ausserhalb der
Existenzfamilie, die rationalen Schranken und die
Grenzkollision im formalen Normalblock. Die
Gebietssaetze folgen aus den analytischen Schranken,
nicht aus Stichproben. 111 Tests im betroffenen Panel
bestehen. Keine Aussage ueber einen Auswertungswert am
offenen positiven 3D-Kandidaten.
