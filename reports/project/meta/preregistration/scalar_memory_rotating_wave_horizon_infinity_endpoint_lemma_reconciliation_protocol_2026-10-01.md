# Endpoint-Lemma-Reconciliation fuer den Unendlichkeits-Astlink

Datum: 2026-10-01.

Status: **outcome-informiert, vor Implementierung des Reconciliation-Audits eingefroren**.

## 1. Anlass und methodische Einordnung

Attempt 4 ist ein gueltiger, unabhaengig auditierter
`g-infinity-branch-link-inconclusive`-Record. U0--U3 und U5 bestehen; U4
scheitert allein, weil der Produktionscode bytegenaue Gleichheit zweier
unabhaengig outward-gerundeter Darstellungen der registrierten
$10^{-10}$-Box fordert. Die versiegelten G4-Krawczyk-Bilder liegen bereits in
den uniformen Boxen.

Dieses Protokoll wurde nach Kenntnis dieses Ergebnisses formuliert. Es ist
keine prospektive Wiederholung und darf Attempt 4 nicht in einen Pass
umetikettieren. Es friert lediglich die mathematische Frage ein, ob der
publizierte Record das im Ursprungsprotokoll formulierte Endpunktlemma trotz
der staerkeren Implementierungsbedingung traegt.

## 2. Unveraenderliche Inputs

Der Audit liest ausschliesslich bereits publizierte Dateien und bindet deren
Git-Blobs:

- Attempt-4-Resultat: `fe25d5a4e222d98faa8628882726597bf0455b90`;
- Attempt-4-Manifest: `a39388c2012d94b59f9d214457d98611dd096e4b`;
- Attempt-4-Audit: `9e8790256ec08c75e51b2c26c28c8bdb15c3087b`;
- Attempt-4-Ergebnisreview: `792d0c66fd79b2f5501b29eadb304e2b50536410`;
- G1--G3-Attempt-2-Resultat:
  `385a7c736bb2974144dffcea0b11c760f5313a1e`;
- G4-Komponentenresultat:
  `0e6ccaba8665bfcce735f8a8d596224c39fd6323`.

Es gibt keinen numerischen Backend-Aufruf, keine neue Intervallrechnung,
keine Boxanpassung und keinen Zielzugriff.

## 3. Zu pruefendes Lemma

Fuer jedes Praezisionspanel sei $X$ die uniforme Box und
$K_s(X,[0,1])\subset\operatorname{int}X$ das strikte uniforme
Krawczyk-Bild. Die registrierte Regularitaet $\rho_\infty<1$ liefert genau
eine Nullstelle $x(s)\in X$ fuer jedes $s\in[0,1]$.

Fuer $s=1$ sei $X_G$ die versiegelte G4-Box und $K_G(X_G)$ ihr strikt
inneres Krawczyk-Bild. Wenn

\[
K_G(X_G)\subset X,
\]

dann liegt die von G4 zertifizierte $F_\infty$-Nullstelle in $X$. Wegen der
uniformen Eindeutigkeit in $X$ ist sie gleich $x(1)$. Exakte Gleichheit von
$X_G$ und $X$ ist dafuer weder erforderlich noch invariant unter
unabhaengiger outward-Serialisierung.

Fuer $s=0$ muss der Audit die bereits positive G1--G3/G4-Endpunktverknuepfung
und die Lage der endlichen zertifizierten Krawczyk-Bilder in der uniformen
Box analog rekonstruieren. Eine blosse Gleichheit von Mittelpunkttexten
genuegt nicht.

## 4. Harte Gates

Ein Reconciliation-Pass verlangt gleichzeitig:

1. **R0 Provenienz:** alle sechs Git-Blobs, Manifesthashes und vorhandenen
   Auditentscheidungen stimmen;
2. **R1 Unveraenderter Attempt 4:** Entscheidung bleibt `inconclusive`, nur
   U4 ist negativ, U0--U3/U5 und beide Panel-Passes sind positiv;
3. **R2 Uniforme Eindeutigkeit:** beide Panels sind strikt, regulaer und
   haben $\rho_\infty<1$;
4. **R3 Finiter Endpunkt:** der positive G1--G3-H3600-Link ist versiegelt,
   und seine 80-/120-dps-Inner-Images liegen in den jeweiligen uniformen
   Boxen;
5. **R4 Unendlicher Endpunkt:** die 120-/160-dps-G4-Krawczyk-Bilder liegen
   komponentenweise in den jeweiligen uniformen Boxen;
6. **R5 Nichttautologie:** mindestens eine outward-Boxdarstellung ist
   byteungleich; der Audit darf seine Entscheidung nicht aus Boxgleichheit
   ableiten;
7. **R6 Reproduktion:** alle Einschlussrelationen werden mit exakter
   `Decimal`- oder rationaler Ordnung unabhaengig vom Produktionsvalidator
   rekonstruiert.

## 5. Falsifikationskontrollen

Tests muessen mindestens zurueckweisen:

- ein G4-Krawczyk-Bild, das einen uniformen Boxrand auch nur an einer
  Koordinate ueberschreitet;
- ein finites G1--G3-Inner-Image ausserhalb der uniformen Box;
- Boxueberlappung ohne vollstaendige Bildinklusion;
- ein nicht striktes oder nicht regulaeres uniformes Panel;
- eine veraenderte Attempt-4-Entscheidung oder ein zusaetzlich negatives
  U-Gate;
- manipulierte Manifest-, Git- oder Auditbindungen;
- exakte Boxgleichheit als alleinigen Ersatz fuer Bildinklusion.

## 6. Entscheidungs- und Claimgrenze

Bei allen positiven R-Gates lautet das enge Urteil
`g-infinity-endpoint-lemma-reconciled-posthoc`. Andernfalls lautet es
`g-infinity-endpoint-lemma-not-reconciled`.

Ein positiver Audit waere ein outcome-informierter, mathematischer
Reconciliation-Befund auf bereits publizierten Intervallen. Er aendert den
Attempt-4-Record nicht, ist kein unabhaengiger Replikationslauf und kein
zweiter Intervallbackend. Er traegt hoechstens die Aussage, dass die
publizierten Zertifikate das Endpunktlemma unter Bildinklusion erfuellen.
Insbesondere folgt weiterhin keine dynamische $H\to\infty$-Stabilitaet,
globale Eindeutigkeit, Formation, Interaktion, Spin, Traegheit oder Masse.
