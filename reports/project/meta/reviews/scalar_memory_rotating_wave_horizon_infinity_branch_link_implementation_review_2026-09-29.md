# Implementierungsreview: uniformer Tail-Branch-Link

Datum: 2026-09-29.

Verdict: **`g-infinity-branch-link-contract-implementation-pass-target-closed`**.

## 1. Umfang

Geprueft wurden:

1. der gemeinsame Intervallkern fuer
   $F_s=F_{3600}+sT_{3600}$ auf $s\in[0,1]$;
2. Resultatschema, semantischer Validator und Klassifikator;
3. erneute Git-Blob-Extraktion der versiegelten G1--G3-/G4-Inputs;
4. getrennter Standardbibliotheksauditor und Manifest-last-Publikation;
5. One-shot-Ausfuehrungsguard und geschlossene Governance;
6. direkte Falsifikations-, Publikations- und Regressionstests.

Es wurde kein reales neues Homotopiepanel berechnet und kein reservierter
Resultat-, Receipt-, Audit- oder Manifestpfad erzeugt.

## 2. Abbildung der Mathematik auf den Code

Die neue Standardbibliotheksfunktion bildet die feste Familie

$$
F_s=F_{3600}+sT_{3600}
$$

direkt ab. Fuer Residuum und beide Jacobi-Spalten multipliziert sie die
registrierten symmetrischen Tailintervalle mit der nichtnegativen
Parameterbox $S=[0,1]$. Diese Ueberapproximation enthaelt jeden exakten
Tailbeitrag der Familie; verlorene Korrelation kann nur zu einem
`inconclusive`, nicht zu einem falschen Pass fuehren.

Neben dem uniformen Krawczyk-Bild wird

$$
I-YD F_S(X)
$$

als Intervallmatrix gespeichert. Die Zeilensummen ihrer absoluten
Intervallobergrenzen rekonstruieren die registrierte
$\ell_\infty$-Normschranke. Validator und Auditor akzeptieren
`uniform_regularity` nur fuer eine outward-gerundete Schranke kleiner eins.

## 3. Vertrag und Unabhaengigkeit

- Der Runner darf genau zwei Panels bei 120 und 160 dps erzeugen. Nach dem
  ersten negativen oder arithmetisch unentscheidbaren Panel stoppt er.
- Skalierungsintervall, Mittelpunkt, Boxbreiten, Tailbounds und Praezisionen
  sind Schema-Konstanten; adaptive Slabs oder Boxen sind nicht vorgesehen.
- G1--G3 und G4 werden nicht erneut gerechnet. Sechs feste kanonische
  Git-Blobs werden gehasht, geparst und auf Entscheidung, Manifestbindung,
  Auditbindung, Endpointkoordinate und Tailbounds geprueft.
- Der Auditor importiert weder Produktionsgate noch `mpmath`, NumPy oder
  SciPy. Er rekonstruiert Schema, Git-Blob-Snapshot, analytische Tailbounds,
  Dezimalrelationen, Regularitaetsnorm, Endpunktbindung, Klassifikation und
  Lesereport mit der Standardbibliothek.
- Der Auditor ist damit unabhaengig von der Entscheidungsauswertung, aber
  weiterhin kein zweiter Intervallbackend.

## 4. Im Review gefundene und behobene Befunde

### 4.1 Major: extrahierter Snapshot war nicht rueckgebunden

Die erste Implementierung fixierte zwar alle sechs Dateihashes, verglich die
im neuen Resultat gespeicherten Endpoint-Boxen aber nicht erneut mit den
Inhalten dieser Git-Blobs. Ein nachtraeglich gemeinsam manipuliertes
Snapshot-/Klassifikationsrecord haette deshalb die rein relationale Pruefung
erreichen koennen.

Behoben: Produktionsvalidator und unabhaengiger Auditor extrahieren den
vollstaendigen Snapshot erneut aus den kanonischen Git-Blobs und verlangen
exakte Gleichheit. Eine Mutation des Snapshots wird fail-closed verworfen.

### 4.2 Moderate: Decimal-Kontext bei Boxrekonstruktion

Die erste Validatorfassung berechnete $c\pm10^{-10}$ nach Verlassen des
200-stelligen `Decimal`-Kontexts erneut mit Standardpraezision. Das erzeugte
einen falschen Negativbefund fuer die echten 120-/160-dps-G4-Boxen, keinen
falschen Pass.

Behoben: erwartete Grenzen und Toleranz werden innerhalb desselben
200-stelligen Kontexts materialisiert. Der echte versiegelte Boxfall ist nun
ein Regressionstest in Gate und Auditor.

Es verbleibt kein bekannter Critical- oder Major-Codebefund.

## 5. Falsifikations- und Regressionsevidenz

Die 27 neuen Tests decken insbesondere ab:

- unzulaessige oder unvollstaendige $s$-Intervalle;
- negative/nichtfinite Tailbounds;
- fehlende strikte Inklusion oder Regularitaet;
- inward-gerundete Normschranken;
- disjunkte Praezisionsbilder;
- Endpoint-, Hash-, Snapshot- und Klassifikationsmutationen;
- geschlossene Governance vor Metadaten-, Receipt- oder Backendzugriff;
- CI-, Blob-, Upstream- und Governance-only-Bindung;
- exklusives Receipt sowie manifest-last Nichtueberschreiben;
- unabhaengige Audit-/Publikationsrekonstruktion mit gemockten Panels.

Der gesamte relevante Rotating-wave-/Horizontverbund besteht danach
**284 Tests**; die vollstaendige Repository-Matrix besteht **1226 Tests**.
Der exakte CI-Ruff-Scope und der strikte Dokumentationsbau sind gruen.

## 6. Verbleibende Grenzen

1. Das reale uniform-tail Zertifikat wurde noch nicht ausgewertet.
2. Offizielle Linux-CI und das daran gebundene Execution-Readinessreview
   stehen noch aus.
3. Die Intervall-Trust-Base bleibt `mpmath.iv==1.3.0`.
4. Ein spaeterer Pass schliesst nur die lokale Rootastluecke, nicht den
   Stabilitaetstransfer nach $H=\infty$.

## 7. Abschluss

Protokoll, Mathematik, Vertrag, Auditor und One-shot-Guard stimmen in der
engen Claimgrenze ueberein. Die targetfreie Implementierung ist lokal
reviewed; Governance bleibt geschlossen. Der naechste zulaessige Schritt ist
der Implementation-Commit mit offizieller CI, danach ein separates
Readinessreview. Erst eine weitere explizite governance-only Einmalfreigabe
darf die zwei realen Panels auswerten.
