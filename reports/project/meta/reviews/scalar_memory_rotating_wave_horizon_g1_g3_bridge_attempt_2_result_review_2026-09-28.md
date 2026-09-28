# Kritisches Ergebnisreview: G1--G3-Bruecke Attempt 2

Datum: 2026-09-28.

Verdict: **`g1-g3-local-fixed-alpha-root-branch-connected-reviewed-pass`**.

## Gegenstand

Dieses Review bewertet den einmalig autorisierten Attempt 2 der registrierten
G1--G3-Horizontbruecke. Der Lauf verwendet unveraendert
$\alpha=0.01$, $q=0.99$, $\eta=0.15$ und $\varepsilon=0$ sowie die
finite Leiter

$$
1200\to1500\to1800\to2400\to3600
$$

und den getrennten lower-tail-Stressast $1200\to900\to600$.

Die publizierte Entscheidung lautet
`rotating-wave-root-branch-connected-with-h2400-local-stability-support`.
Der unabhaengige Standardbibliotheksauditor urteilt
`g1-g3-bridge-independent-audit-agrees`; eine erneute Manifestpruefung nach
dem Lauf bestaetigt alle Artefakthashes.

## Primaere Evidenz

- Alle sieben 80-/120-dps-Rootpanels fuer
  $H=(600,900,1200,1500,1800,2400,3600)$ bestehen Krawczyk-
  Eindeutigkeit, Praezisionsabgleich und Kreuzinklusion.
- Alle sechs registrierten affinen Gleichungshomotopien besitzen jeweils
  64/64 strikt eingeschlossene Scheiben: insgesamt 384/384. Alle 378
  erforderlichen Nachbarbildschnitte bestehen.
- Die getrennten direkten 70-dps-Summenreplays bestehen an allen sieben
  Horizonten; die maximalen Residuen liegen zwischen
  $2.83\times10^{-72}$ und $6.54\times10^{-72}$ und damit weit unter
  $10^{-45}$.
- Die normierte outward-rounded Drift sinkt von
  $d^{\rm up}_{1800,2400}=4.5978984\times10^{-9}$ auf
  $d^{\rm up}_{2400,3600}=2.5859006\times10^{-11}$. Das Verhaeltnis ist
  $0.0056241$. Der zweite Wert liegt sowohl unter $10^{-8}$ als auch unter
  der registrierten Kontraktionsgrenze
  $0.01d^{\rm up}_{1800,2400}+10^{-14}=4.5988984\times10^{-11}$.
- Die gegenseitigen Krawczyk-Inklusionen verbinden das neue $H=2400$-Panel
  mit der versiegelten G5-Komponente und das neue $H=3600$-Panel mit der
  versiegelten G4-Komponente.
- G6 besteht alle neun Shift-/Circular-FIFO-Vergleiche, alle sieben
  $\eta=0$-Kontrollen und erkennt die drei registrierten FIFO-Mutanten.

Damit bestehen G0, G1F, G1R, G2F, G2R, G3, G4, G5, G6 sowie beide
Endpunktlinks. Der lokale Ausschlussfalsifikator meldet keinen ausgeschlossenen
Ast; er wird fuer den positiven Befund nicht als zusaetzliche Existenzsuche
interpretiert.

## Kritische Einordnung

Der positive Befund schliesst die bislang offene logische Luecke zwischen den
isolierten Komponenten: Innerhalb der registrierten lokalen Boxen und des
gemeinsamen Intervall-Vertrauenskerns gehoeren die finite Rootleiter, der
direkt stabilitaetsgepruefte Root bei exakt $H=2400$ und der lokale
$F_\infty$-Root zur selben zertifizierten Rootfamilie.

Das ist staerker als blosse Koordinatennaehe. Die Astidentitaet beruht auf
strikten Krawczyk-Einschluessen jeder Homotopiescheibe, Nachbarueberlappungen
und gegenseitigen Endpunktinklusionen. Die fallende Drift liefert zusaetzliche
Skalierungsevidenz, ist aber allein kein Grenzwertbeweis.

Folgende Einschraenkungen bleiben wesentlich:

1. Die Kanten verwenden die preregistrierte affine Homotopie
   $F_a+s(F_b-F_a)$; sie stellen keine physische kontinuierliche Dynamik in
   einem reellen Horizontparameter dar.
2. `mpmath.iv` ist der gemeinsame Vertrauenskern von Zertifikaten und
   Recordaudit. Der Auditor rekonstruiert Beziehungen und Hashes, ist aber
   kein zweiter Intervallbackend.
3. Die direkte Stabilitaetsevidenz stammt weiterhin nur von exakt $H=2400$
   und ist kein Intervallbeweis des vollstaendigen Spektrums.
4. Der G4-Endpunkt ist ein lokaler $F_\infty$-Rootbeweis, kein
   $H\to\infty$-Stabilitaetsbeweis.
5. G6 bestaetigt Implementierungssemantik. Exakte Nullfehler in diesen
   deterministischen Vergleichsarmen sind keine physikalische Evidenz.
6. Der Lauf beweist weder globale Eindeutigkeit oder einen offenen Basin,
   noch generische Formation, Interaktion, interne $S^1$-Phase, Spin,
   Traegheit oder Masse.

## Provenienz und Publikation

- Attempt: `2`;
- Autorisierungs-ID: `e5ac3f5a-513f-47df-baa0-48a38aff3afc`;
- Implementierungscommit:
  `bdc033293b74ce2115a3006d13d1ba749bb3ef93`;
- Ausfuehrungscommit:
  `f9a6fcf45d1e3beeb81fe001be077076e429316b`;
- offizieller CI-Run: `36354118411`;
- Ergebnis-SHA-256:
  `31bff4d3f1dfbede5060b43622aacd597b79a6f8b67ec09f2119d35759a0669d`;
- Manifest-SHA-256:
  `394410f55fd3610a122f319c544296d7614185e6f2eae86bae6eb8a64962b31d`.

Das Manifest wurde zuletzt publiziert und danach unabhaengig erneut
verifiziert. Receipt, Ergebnis, lesbarer Report, Audit und Manifest sind
vorhanden. Die Attempt-2-Autorisierung ist verbraucht und muss nach Aufnahme
der Artefakte wieder geschlossen werden.

## Zulassbarer Claim

Zulaessig ist:

> Bei festem $\alpha=0.01$ verbindet eine lokal Krawczyk-zertifizierte,
> preregistrierte finite Horizontleiter den direkt stabilitaetsgeprueften
> $H=2400$-Root mit dem lokalen $F_\infty$-Root; die zertifizierte Drift
> faellt auf der letzten gemessenen Stufe deutlich und alle registrierten
> Implementierungskontrollen bestehen.

Nicht zulaessig bleibt insbesondere:

> Die gesamte Familie sei fuer $H\to\infty$ stabil, global eindeutig,
> spontan gebildet oder bereits ein Nachweis von Interaktion, Spin,
> Traegheit beziehungsweise physikalischer Masse.
