# Projektprioritaeten

Stand: 2026-09-30.

Dies ist die einzige aktive Arbeitsreihenfolge des Repositorys. Der
[Stand bis 2026-09-09](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/docs/archive/status/project_priorities_through_2026-09-09.md)
ist archiviert. Katalog, Status und Reports duerfen Befunde und Blocker
nennen, aber keine zweite Prioritaetenliste fuehren.

Eingefrorene Voraussetzungen bleiben
`p4rs-anchor-scale-transfer-pass`,
`n0-noise-stability-window-bracketed-reviewed-pass` und
`p5d-mutual-center-design-identifiable`. Neu abgeschlossen ist
`g1-g3-local-fixed-alpha-root-branch-connected-reviewed-pass`.
**P5-D Versuch 3 technisch inconclusive: Pipeline geschlossen**; die
**Attempt-3-Lease ist verbraucht**.
Diese Befunde ordnen Prioritaet 1 ein, sind aber keine weiteren Arbeitspunkte.

## Eine Liste

1. **Unendlichkeits-Astluecke schliessen.** Den natuerlichen Tail-Link
   $F_s=F_{3600}+sT_{3600}$ als uniformes Krawczyk-/Regularitaetsgate
   pruefen. Attempt 1 ist durch einen konservativ abgefangenen
   Dezimalserialisierungsfehler technisch inconclusive. Zuerst exakte
   Binaer-zu-Dezimal-Endpunkte targetfrei implementieren und adversarial
   reviewen. Amendment und Remediation sind inzwischen positiv targetfrei
   reviewed; offizielle CI und blobgebundenes Readinessreview sind ebenfalls
   positiv abgeschlossen. Attempt 2 wurde dennoch durch die nachgeschaltete
   28-stellige `Decimal`-Summation technisch inconclusive. Als Naechstes muss
   Attempt 3 dieselbe Relation targetfrei mit exakten rationalen Summen
   auswerten. Das enge Amendment ist inzwischen positiv reviewt; erst nach
   targetfreier Implementierung und Review ebenfalls gruen. Offizielle CI und
   blobgebundenes Readinessreview waren positiv; der einmalige Lauf scheiterte
   jedoch noch vor dem Gate-Import an einer nicht gebundenen
   NumPy--Numba-Inkompatibilitaet. Attempt 3 ist technisch inconclusive und
   verbraucht. Vor Attempt 4 muessen `requirements.txt`, `pyproject.toml` und
   die exakten Runtime-Versionen geschuetzt sowie Gate und Auditor vor dem
   Receipt targetfrei importiert werden. Wissenschaftliche Parameter und
   Schwellen bleiben eingefroren. Dies ist kein
   $H\to\infty$-Stabilitaetsgate.
2. **Paper I konsolidieren -- nach 1.** Modellkern, skalare Evidenz,
   Rotating-wave-Ast und Abgrenzungen in der Sprache von $q$, $g$, $H$,
   $B_H$, $c$ und $\mu$ zusammenfuehren. Zulaessig sind nur lokal oder
   kontrolliert belegte Existenz-, Stabilitaets-, Skalierungs- und
   Center-Port-Aussagen; interne Phase, physikalische Masse und Interaktion
   bleiben getrennte Hypothesen.
3. **Vorbereiteten Orbit und gebildeten Knoten trennen -- nach 2.** Festlegen,
   ob Paper I ueberhaupt einen Formationsclaim benoetigt. Erst dann darf ein
   gepaartes Formation-/KnotScore-Protokoll fuer den Rotating-wave-FIFO
   entstehen. Ein Score auf einer vorbereiteten exakten Kreisgeschichte ohne
   `eta_zero`- und Formationskontrolle waere nicht entscheidend und wird nicht
   nachgetragen.
4. **Zertifikats- und Release-Hardening -- parallel zu 1--3.** Einen
   zweiten unabhaengigen Intervallbackend, reproduzierbare Dependency-Hashes,
   `CITATION.cff` und eine zitierbare Release vorbereiten. Diese Punkte
   erhoehen Pruefbarkeit, ersetzen aber kein wissenschaftliches Gate.
5. **Interaktionsprogramm neu autorisieren -- nach Paper-I-Claimreview.** P5-D bleibt
   `inconclusive`. Ein weiterer Ziellauf braucht ein separates
   outcome-blindes Protokoll, eine neue explizite Freigabe und einen sauberen
   Readiness-Commit. Vorher ist nur targetfreie Methodenarbeit erlaubt.
6. **Repository fortlaufend kuratieren -- bei jedem abgeschlossenen Block.**
   Aktive Seiten auf hoechstens sieben gleichrangige Elemente begrenzen,
   historische Detailregister ins Archiv verschieben, Standardbibliotheken
   erweitern statt Runnerlogik zu duplizieren und Status/Claims nach jedem
   Review synchronisieren.

## Aktueller Haltepunkt

G4, G5 und die verbindende G1--G3-Leiter sind positiv und unabhaengig
auditiert. Attempt 2 verbindet bei festem $\alpha=0.01$ alle sieben lokalen
finite Rootpanels, sechs Homotopiekanten und die versiegelten endlichen
G5-/G4-Endpunkte bei $H=2400/3600$; direkte Stabilitaetsevidenz bleibt auf
exakt $H=2400$ begrenzt. G4 zertifiziert separat einen lokalen
$F_\infty$-Root, aber noch keinen Transfer $F_{3600}\to F_\infty$.
Governance ist nach dem verbrauchten Lauf wieder geschlossen. Das
abschliessende Metareview urteilt
`finite-branch-paper-i-ready-with-explicit-infinity-gap`. Der aktuelle
Haltepunkt ist der konservativ gestoppte Attempt 1 des uniformen
Tail-Branch-Link-Gates. Das Receipt ist verbraucht; ein Resultatrecord wurde
nicht publiziert. Der Abbruch betrifft die unabhaengige Dezimalserialisierung
von Defektmatrix und Zeilensumme und ist kein mathematisches Negativergebnis.
Attempt 2 ist trotz positiver Remediation, CI und Readiness an einer zweiten,
nun synthetisch reproduzierten Decimal-Kontextstelle vor Publikation
gescheitert. Beide Receipts sind verbraucht; kein Resultatrecord existiert.
Attempt 3 ist trotz rationaler Remediation, CI und Readiness vor jeder
Zielauswertung an einer nicht vollstaendig gebundenen Runtime gescheitert.
Alle drei Receipts sind verbraucht; kein Resultatrecord existiert.
Prioritaet 1 ist das enge Attempt-4-Dependency-/Preflight-Amendment mit
Import-vor-Receipt-Semantik. Das Protokoll ist eingefroren und positiv
reviewt; targetfreie Implementierung, 52 fokussierte Tests, die gesamte
1251-Test-Matrix, Ruff, strict Docs und das Implementierungsreview sind nun
gruen. Offizieller Linux-CI-Nachweis und blobgebundene Readiness sind
ebenfalls positiv abgeschlossen. Der einmalige Standardlauf ist gueltig
publiziert, aber formal U4-inconclusive: nur die bytegenaue Gleichheit zweier
outward-Boxdarstellungen scheitert, waehrend beide uniformen Zertifikate und
die G4-Bildinklusion bestehen. Als Naechstes folgt kein Retry, sondern ein
targetfreier, explizit outcome-informierter Endpoint-Lemma-Audit. Sein
Protokoll ist nun vor der Auditimplementierung eingefroren und kritisch
reviewt. Paper I
folgt entweder
auf ein valides spaeteres Ergebnis oder mit weiterhin expliziter
Unendlichkeitsluecke. Methodischer Stand und Evidenzgrenzen stehen im
[Experimentkatalog](../reference/experiment_catalog.md).
