# Native Rotating Waves: Gleichungen, Evidenz und Grenzen

Stand: 2026-08-21.

Diese Seite ist die kanonische Frontdoor fuer den positiven raeumlichen
Schleifenast des unveraenderten skalaren K0-H-Modells. Das kritische
Reviewergebnis lautet:

> Die vorhandene Kette ist eine solide mathematische und numerische Basis fuer
> vorbereitete raeumliche Schleifen. Exakte lokale finite-H-Existenz ist in
> fuenf Zellen zertifiziert. Stabilitaet ist bislang nur am Anchor lokal
> numerisch gestuetzt. Formation, internes S1, Arbeit, Traegheit und Masse sind
> nicht nachgewiesen.

Der Name *Schleife* ist hier praeziser als *Knoten*: Das nachgewiesene Objekt
ist eine kreisfoermige raeumliche relative Gleichgewichtsbahn. Es ist weder
eine topologische Verknotung noch bereits ein materielles Teilchen.

## 1. Ausgangsgleichung ohne Oszillatorpostulat

Im rauschfreien nativen Modell gilt

\[
x_{n+1}=x_n-\eta\nabla(K*\rho_n)(x_n),
\]

\[
\rho_{n+1}(y)
=q\rho_n(y)+\alpha M_0\delta(y-x_{n+1}),
\qquad q=1-\alpha.
\]

K0-H wertet dieses Feld durch die letzten \(H\) Depositionen aus; das ist die
explizite endliche Trunkierung des K0-Memorys. Ein gefuellter FIFO mit \(H\)
Altersklassen besitzt daher die rohen Gewichte

\[
w_j=\alpha M_0q^j,
\qquad j=0,\ldots,H-1.
\]

\(H\) ist die gespeicherte Historienlaenge. \(N\) ist nur die Zahl der
beobachteten Updates und kommt in der Selbstkonsistenzgleichung nicht vor.
Die ausfuehrliche Bruecke zwischen \(q,\alpha,H,M_0,\eta,g_H\) und dem
Centerfilter steht unter
[Center-Filter und Rotation](scalar_memory_center_filter.md).

Der dortige Filter

\[
B_H(z)=\frac{\alpha}{1-q^H}
\sum_{j=0}^{H-1}(qz^{-1})^j
\]

ist exakt eine endliche geometrische Reihe. Er beschreibt die lineare,
normierte Centerbildung. Die volle Schleifengleichung ist dagegen im
Allgemeinen **keine** einzelne geometrische Reihe: Der nichtlineare Faktor
\(\varphi(r_j)\) haengt selbst vom Alter \(j\) ueber den jeweiligen
Chordabstand ab. \(B_H\) bleibt die richtige lineare Referenz, ersetzt aber
nicht die nichtlineare finite Summe.

## 2. Exakte Kreisreduktion

Identifiziere die Ebene mit \(\mathbb C\) und setze eine vorbereitete Historie

\[
x_n=R e^{in\theta},
\qquad R>0,\quad 0<\theta<\pi.
\]

Im aktuellen Koordinatensystem hat der Abstand zur Altersklasse \(j\)

\[
r_j=2R\left|\sin\frac{j\theta}{2}\right|,
\qquad
\chi_j=R^2(1-\cos j\theta)=\frac{r_j^2}{2}.
\]

Fuer den Double-Gaussian-Kernel ist

\[
\varphi(\chi)
=-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}
 e^{-\chi/\sigma_{\rm rep}^2}
 +\frac{A_{\rm att}}{\sigma_{\rm att}^2}
 e^{-\chi/\sigma_{\rm att}^2}.
\]

Der Vergessensfaktor heisst ausschliesslich \(q=1-\alpha\); \(\chi\) ist die
quadratische halbe Chordlaenge. Damit lauten die radialen und tangentialen
Summen

\[
A_H(R,\theta)
=\sum_{j=1}^{H-1}w_j\varphi(\chi_j)(1-\cos j\theta),
\]

\[
S_H(R,\theta)
=\sum_{j=1}^{H-1}w_j\varphi(\chi_j)\sin(j\theta).
\]

Direktes Einsetzen in den nativen Update ergibt exakt

\[
\boxed{
F_R=\cos\theta-1+\eta A_H=0,
\qquad
F_T=\sin\theta+\eta S_H=0
}.
\]

Fuer \(\eta>0\) sind \(A_H>0\) und \(S_H<0\) notwendig. Zwei unabhaengige
Gainbestimmungen muessen uebereinstimmen:

\[
\eta_R=\frac{1-\cos\theta}{A_H},
\qquad
\eta_T=-\frac{\sin\theta}{S_H}.
\]

Diese zwei Gleichungen folgen aus dem originalen ersten-Ordnungs-Update. Es
wurde kein harmonischer Oszillator und kein Massenterm hineingeschrieben.

Wegen Spiegelinvarianz gehoert zu \(+\theta\) stets eine Loesung mit
\(-\theta\). Die Gleichungen selektieren keine Haendigkeit.

## 3. Warum der Kontinuumslimes ebenfalls keine Masse einsetzt

Setze

\[
t=\alpha j,
\qquad
\theta=\alpha\Omega,
\qquad
\eta=\alpha\widehat\eta,
\qquad
H\alpha=C.
\]

Dann konvergiert \(q^j=(1-\alpha)^j\) gegen \(e^{-t}\). Mit

\[
u(t)=1-\cos(\Omega t),
\qquad
\chi(t)=R^2u(t)
\]

werden die Grenzintegrale

\[
I_R=M_0\int_0^C e^{-t}\varphi(\chi(t))u(t)\,dt,
\]

\[
I_T=M_0\int_0^C e^{-t}\varphi(\chi(t))\sin(\Omega t)\,dt.
\]

Die radiale endliche Gleichung besitzt auf der linken Seite erst Ordnung
\(\alpha^2\), waehrend \(\eta A_H\) Ordnung \(\alpha\) hat. Daher muss in
fuehrender Ordnung \(I_R=0\) gelten. Tangential folgt

\[
\boxed{I_R(R,\Omega)=0,
\qquad
\Omega+\widehat\eta I_T(R,\Omega)=0}.
\]

Das ist eine singulaere geometrische Balance des Memory-Updates, keine
Newtonsche Zentripetalkraftgleichung. Eine spaetere effektive
Zweitordnungsbeschreibung muesste separat aus Response und Arbeit
identifiziert werden.

## 4. Evidenzleiter

| Stufe | Ergebnis | Was sie nicht zeigt |
| --- | --- | --- |
| Discovery | nativer finite-H-Residualroot bei \(\alpha=0.01,H=1200,\eta=0.15,A_{\rm att}=3.5\) | Intervallbeweis, Stabilitaet, Formation |
| P0/D0 | Provenienz ohne Defekt; Objekt ist translationsreduzierte ambiente \(SO(2)\)-Gruppenbahn | internes S1 |
| Anchor-Stabilitaet | zwei Arnoldi-Panels: \(|\lambda_\perp|=0.9930603477\); drei kleine Stoerungen kontrahieren | vollstaendige Spektraleinschliessung, Basin |
| Anchor-Zertifikat | strikter Krawczyk-Einschluss; lokal genau eine finite-Summen-Nullstelle | globale Eindeutigkeit |
| L0--L4 | fuenf lokal eindeutige Roots bei \(H\alpha=12,\eta/\alpha=15\) | Stabilitaet der Nicht-Anchor-Zellen |
| Historische Leiter | formal `certified-roots-nonconvergent`, weil der eingefrorene Guide Gain 15.016345 statt 15 hatte | darf nicht rueckwirkend umbenannt werden |
| Fixed-gain-Reconciliation | alle urspruenglichen Skalierungsgates gegen den korrekt bei 15 definierten Kontinuumsroot bestehen | all-alpha-Theorem, Kontinuumsintervall |
| Foundation-Audit | alle fuenf finite Summen und der Kontinuumsroot unabhaengig in Multipraezision reproduziert | neue Holdout-Replikation oder Stabilitaetsbeweis |

Der unabhaengige Audit findet

\[
R_\infty
=0.9431133067695436321754560922\ldots,
\]

\[
\Omega_\infty
=1.5855700777177887067789751487\ldots.
\]

Tanh--Sinh und Gauss--Legendre stimmen auf der ausgewiesenen 70-stelligen
Ausgabe ueberein. Die fuenf separat ausgewerteten finite-Summen-Residuen
liegen unter \(8\times10^{-72}\), die beiden Gainbestimmungen pro Zelle
innerhalb \(6\times10^{-69}\) des registrierten Gains.

Der erste Foundation-Auditlauf bleibt als
`initial_implementation_fail` erhalten. Er scheiterte ausschliesslich, weil
der Code die registrierte Dezimalidentitaet \(0.60/0.04=15\) als strikte
binaere `mpmath`-Gleichheit implementierte. Eine prospektiv eingefrorene
Pipeline-Reconciliation ersetzte nur diesen Check durch exakte
Dezimal-Kreuzprodukte und wiederholte alle Gates. Das positive Urteil beruht
auf diesem vollstaendigen Re-Run, nicht auf einer nachtraeglich geaenderten
Schwelle.

Die erste GitHub-Linux-Pruefung entdeckte danach einen zweiten reinen
Provenienzdefekt: Sechs erwartete SHA-256-Werte beschrieben die
CRLF-Arbeitsbaumdarstellung, nicht die kanonischen LF-Git-Blobs; ein
Shallow-Checkout mit nur einem Commit konnte ausserdem aeltere, gueltige
Ausfuehrungsrevisionen nicht sehen. Ein zweites, wiederum vor der
Implementierung eingefrorenes Protokoll beschraenkte die Korrektur auf die
Hashdomaene `git-head-blob`, vollstaendige Checkout-Historie und zugehoerige
Regressionstests. Der erneute A--E-Vollaudit aus Commit `0bc74ac` besteht.
Kein Inputartefakt, Parameter oder wissenschaftlicher Schwellenwert wurde
geaendert.

## 5. Was „stabil“ derzeit bedeutet

Der Anchor ist ein Fixpunkt der mitrotierenden \(2400\)-dimensionalen
Voll-FIFO-Map bis zum numerischen Floor. Die zwei berechneten Gruppen von 24
und 36 groessten Ritzwerten stimmen beim fuehrenden transversalen Paar sehr
gut ueberein. Das ist starke lokale numerische Evidenz.

Es ist dennoch kein vollstaendiger Beweis, weil ARPACK nicht alle 2400
Eigenwerte intervallartig einschliesst. Zudem wurde nur ein winziger lokaler
Stoerungsradius getestet. Deshalb sind die zulaessigen Formulierungen:

- „lokal numerisch stabiler vorbereiteter Anchor“;
- „fuenf lokal existenzzertifizierte Schleifenzellen“.

Nicht zulaessig sind derzeit:

- „fuenf stabile Knoten“;
- „spontan entstehende Schleife“;
- „robustes Attraktorbecken“.

## 6. Topologie- und Mechanikgrenze

Die Menge aller global gedrehten Kopien einer vorbereiteten Loesung ist

\[
\{\mathcal R_\varphi Y_*:\varphi\in S^1\}.
\]

Dieses \(S^1\) stammt aus der ambienten Raumrotation. Nach Quotientieren von
\(SO(2)\) bleibt ein Punkt. Persistent Homology auf der unquotientierten Bahn
wuerde daher die bekannte Gruppensymmetrie wiederfinden und keine neue
knoteninterne Phase beweisen.

Auch Mechanik bleibt getrennt. Schreiben und Vergessen bilden einen offenen
Source-/Sink-Prozess. Ohne einen mikroskopisch reziproken Aktuator und
Arbeitsledger folgt aus der Bahn weder konservatives Kreiseln noch
Traegheitsmasse.

## 7. Naechstes erlaubtes Gate

Nach Integration dieses Reviews ist genau eine weitere Skalenzelle
priorisiert:

\[
\boxed{(\alpha,H,\eta)=(0.00125,9600,0.01875)}.
\]

Sie erhaelt vor Ausfuehrung ein eigenes Protokoll und wird zunaechst nur auf
lokale finite-Summen-Existenz, Astkorridor, exakte Dezimalskalierung und
First-order-Diskrimination geprueft. Ein positives Existenzresultat darf nicht
automatisch als Stabilitaetspass gelesen werden. Nicht-Anchor-Stabilitaet ist
das naechste sequentielle Gate; erst danach kommen Formation, Basin und
Rauschen.

Der \(A_{\rm att}=7\)-Holdout bleibt versiegelt. Topologie- und Massegates
bleiben logisch getrennt.

## 8. Reproduzierbarer Einstieg

- Die Reihenfolge der Programme steht im
  [Experiment-Ledger auf GitHub](https://github.com/MemoryDynamics/Knoten/blob/main/experiments/current/dynamics/rotation/README.md).
- Reports, historische Entscheidungen und Reviews stehen im
  [Evidenz-Ledger auf GitHub](https://github.com/MemoryDynamics/Knoten/blob/main/reports/dynamics/rotation/README.md).
- Der maschinenlesbare Abschluss ist der
  [Foundation-Audit](https://github.com/MemoryDynamics/Knoten/blob/main/reports/dynamics/rotation/scalar_memory_rotating_wave_foundation_audit_2026-08-21.json).
