# Review: tail-augmentiertes Krawczyk-Zertifikat

Datum: 2026-09-10.

Verdict:
**`horizon-tail-krawczyk-adapter-target-free-pass-g4-unmeasured`**.

## 1. Gegenstand

Geprueft wurde ausschliesslich der targetfreie Methodenbaustein fuer Gate G4
des Fixed-alpha-Horizontprotokolls. Er nimmt einen spaeter vom vollstaendigen
Runner gelieferten endlichen Root bei $H=3600$ entgegen. In diesem Review
wurde kein solcher Kandidat berechnet oder eingesetzt, kein Horizontlauf
gestartet und kein P5-D-Versuch autorisiert.

Die allgemeine Intervallroutine liegt in der Standardbibliothek
`src/emergenz_knoten/rotating_wave_interval.py`. Der Experimentadapter in
`scalar_memory_rotating_wave_horizon_transfer_gate.py` legt ausschliesslich
die bereits registrierten Werte $H=3600$, Boxhalbbreite $10^{-10}$ und die
Praezisionen 120 und 160 dps fest und bildet das Resultat in den bestehenden
v3-Vertrag ab.

## 2. Zertifizierte Abbildung

Das Protokoll zerlegt das unendliche Residuum als

$$
F_\infty(R,\theta)=F_H(R,\theta)+T_H(R,\theta).
$$

Aus den registrierten euklidischen Schranken $b_0$, $b_R$ und $b_\theta$
werden komponentenweise outward-rounded Einschliessungen gebildet:

$$
F_\infty(c)\in F_H(c)+[-b_0,b_0]^2,
$$

$$
D F_\infty(X)_{:,R}\in D F_H(X)_{:,R}+[-b_R,b_R]^2,
\qquad
D F_\infty(X)_{:,\theta}\in
D F_H(X)_{:,\theta}+[-b_\theta,b_\theta]^2.
$$

Mit der Inversen des endlichen Punktjacobians als blossem Praekonditionierer
wird danach derselbe gemeinsame Krawczyk-Kern wie fuer die endlichen Roots
verwendet. Nur ein aus den gespeicherten Intervallendpunkten rekonstruierbar
streng inneres Bild wird als Zertifikat serialisiert. Singularitaet,
Nichtinklusion, falscher Typ oder unregistrierte Praezision liefern kein
Panel. Der Adapter erzwingt ausserdem, dass die gesamte Zertifikatsbox in der
registrierten Domain $[0.8,1.1]\times[0.01,0.022]$ liegt; andernfalls waere
insbesondere der verwendete Wert $R_{\max}=1.1$ nicht gerechtfertigt.

Die Umwandlung einer euklidischen Normschranke in dieselbe symmetrische
Schranke fuer jede Komponente ist gueltig, aber konservativ. Es wird keine
unbelegte Korrelation zwischen den beiden Residualkomponenten oder zwischen
Jacobianzeilen vorausgesetzt.

## 3. Falsifikation und Tests

Die neuen Bibliothekstests pruefen, dass eine positive Residualschranke beide
Residualintervalle erweitert und dass $b_R$ nur die Radiusspalte, $b_\theta$
nur die Thetaspalte des Jacobians erweitert. Bei drei Nullschranken stimmen
endliches und augmentiertes Krawczyk-Bild exakt ueberein. Negative,
nichtendliche und falsch typisierte Bounds sowie eine Box mit Nullbreite
werden verworfen. Rootboxen ausserhalb der Domain werden ebenfalls verworfen.

Die Adaptertests pruefen die exakte Weitergabe der registrierten
$H=3600$-Bounds, Boxbreite und Praezision, die v3-Abbildung, den
rekonstruierbaren strikten Einschluss und den fail-closed Rueckgabewert bei
Nichtinklusion. 16 Tail-selektierte Tests und der Linter sind lokal gruen.
Der erste breite fokussierte Lauf fand nur eine zu scharfe
Gleitkomma-Assertion im neuen Test; der Test vergleicht die outward-rounded
Intervallverbreiterung nun in Dezimalarithmetik mit expliziter Rundungstoleranz.
Die Zertifikatsroutine selbst wurde dadurch nicht geaendert. Nach Schliessen
der Domainluecke bestehen 1054 Projekttests; der strikte Dokumentationsbau
und der Linter sind ebenfalls gruen.

## 4. Kritische Grenzen

Der Baustein beweist gegenwaertig keinen Root von $F_\infty$: Ohne einen
spaeteren registrierten $H=3600$-Root gibt es kein ausgewertetes Tailpanel.
Auch ein spaeterer strikter Einschluss waere lokal auf die registrierte Box
beschraenkt und bedingt auf `mpmath.iv` 1.3.0. Der v3-Auditor rekonstruiert
Bounds, Intervallbilder und Gatebeziehungen, ist aber kein zweiter
Intervallbackend. Ein erster Referee-Durchgang fand und schloss vor dem
breiten Testlauf eine fehlende explizite Domainpruefung im Adapter.

Die Bounds verwenden globale Kernelabschatzungen und verlieren Vorzeichen,
Phasenkorrelation und moegliche Tailausloeschung. Ein Scheitern waere daher
numerisch `inconclusive`, kein Beweis gegen einen unendlichen Root. Umgekehrt
enthaelt ein Pass die gesamte zugelassene Tailunsicherheit und ist deshalb
nicht lediglich eine Extrapolation endlicher Rootzentren.

## 5. Claim-Grenze

Belegt ist, dass der vorhandene finite-H-Intervallkern ohne duplizierten
Solver eine analytisch beschraenkte unendliche Restmenge verarbeiten und nur
bei streng innerem Krawczyk-Bild einen v3-konformen Record ausgeben kann.
Nicht belegt sind G4, der Fixed-alpha-Grenztransfer, Stabilitaet des
unendlichen Systems, globale Eindeutigkeit, Formation, interne Topologie,
Interaktion oder Masse.

## 6. Naechster Haltepunkt

Der naechste erlaubte targetfreie Remediationsblock ist der
LCG-Arnoldi-Adapter. Erst danach folgen Trajektorienabbildung,
Backendkomposition und unabhaengiges Readinessreview. Bis zu diesem Review
bleiben Horizonttarget und P5-D-Versuch 4 geschlossen.
