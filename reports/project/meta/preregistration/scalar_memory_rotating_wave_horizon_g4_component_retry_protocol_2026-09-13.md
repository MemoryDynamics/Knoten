# Prospektives Protokoll: einmaliger G4-Komponenten-Retry

Datum: 2026-09-13.

Status: **nach neuer Nutzerfreigabe und vor Retry eingefroren**.

## 1. Anlass und Versuchstrennung

Der erste autorisierte G4-Komponentenprozess ist als
`g4-experiment-invalid-outward-box-validation` dokumentiert. Er erzeugte
keinen gueltigen Record und darf nicht nachtraeglich als Pass oder Fail
gelesen werden. Die neue Nutzeranweisung „Na dann - weiter“ autorisiert genau
einen getrennten Retry nach abgeschlossener Remediation.

## 2. Unveraenderte wissenschaftliche Inputs

Es gelten weiterhin $\alpha=0.01$, $q=0.99$, $M_0=1$, $\eta=0.15$,
$A_{\rm rep}=1$, $\sigma_{\rm rep}=1$, $A_{\rm att}=3.5$,
$\sigma_{\rm att}=3$ und $H=3600$. Newton startet unveraendert bei
$(R,\theta)=(0.946517504804225,0.015770381717135)$ und fuehrt acht Schritte
mit 120 dps aus. Endliche Boxen, Tailbox, Domain, Tailformeln und die beiden
Praezisionen 120/160 dps bleiben unveraendert.

Es gibt keine Parametersuche, keinen alternativen Start, keine
Boxvergroesserung und keine adaptive Praezision.

## 3. Einzige methodische Aenderung

Die Recordpruefung verlangt nicht mehr dezimal identische Endpunkte
`center +/- half_width`. Stattdessen muss die von `mpmath.iv` serialisierte
Box das ideale Dezimalintervall vollstaendig enthalten, und jeder
outward-Ueberschuss muss kleiner als

$$
\max(1,|c|)\,10^{4-p}
$$

sein, wobei $c$ die jeweilige Rootkoordinate und $p$ die registrierte
Dezimalpraezision ist. Damit ist die garantierte outward-Rundung erlaubt,
eine wissenschaftlich relevante Boxaenderung aber weiterhin ausgeschlossen.
Runner, unabhaengiger Auditor und gemeinsamer Horizontvalidator pruefen
dieselbe Relation.

## 4. Ablauf und Publikation

Der Runner verlangt einen sauberen Commit, `mpmath==1.3.0`, den Hash dieses
Retry-Protokolls und noch nicht vorhandene Zielartefakte. Danach folgen
endlicher Root, 120-dps-Tailpanel und 160-dps-Tailpanel in dieser Reihenfolge.
Nach dem ersten regulaeren Fehlschlag stoppt der abhaengige Pfad.

Ergebnis-JSON und Lesereport werden vor dem Hashmanifest geschrieben. Der
Standardbibliothek-Auditor rekonstruiert Hashes, Bounds, Boxen,
Panelueberlappung, Klassifikation und Lesereport ohne Import des Runners oder
Horizontgates. Die kanonischen Pfade bleiben
`reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_g4_component_2026-09-13.*`,
weil der Erstlauf dort keine Artefakte erzeugt hat.

## 5. Entscheidungen und Claimgrenze

`g4-local-infinite-root-pass` verlangt ein vollstaendiges endliches
Rootzertifikat sowie zwei strikt einschliessende, ueberlappende Tailpanels.
Ein regulaerer Zertifikatsfehlschlag ergibt `g4-inconclusive`; ein erneuter
Provenienz-, Typ-, Hash-, Schema- oder Publikationsfehler ergibt
`g4-experiment-invalid`.

Auch ein Pass belegt nur lokale Existenz eines Roots von $F_\infty$ in der
registrierten Box. Branchidentitaet, Stabilitaet, Formation,
Zwei-Schleifen-Transfer, Interaktion, interne Phase und Masse bleiben offen.

## 6. Vorbedingungen und Stopregeln

Vor dem Retry muessen die outward-Kontrollen kleine backendtypische
Ueberschuesse akzeptieren und groessere Boxabweichungen verwerfen. Der
gesamte Testbestand, der exakte CI-Lint-Scope und der strikte
Dokumentationsbau muessen lokal und fuer denselben GitHub-Commit gruen sein.
Der Arbeitsbaum muss sauber sein. Ein Major/Critical-Reviewfund stoppt den
Retry.

Nach dem Zielstart gibt es kein Retuning und keinen weiteren Retry. Ein
unerwarteter technischer Abbruch wird erneut als invalid dokumentiert.

## 7. Autorisierung

Die ausdrueckliche Nutzerfreigabe vom 2026-09-13 autorisiert genau diesen
einen korrigierten Komponenten-Retry nach den genannten Vorbedingungen. Sie
autorisiert weder den vollstaendigen Fixed-$\alpha$-Horizontlauf noch
LCG-Arnoldi/G5, P5-D-Versuch 4 oder den historischen G4-Zwei-Knoten-Transfer.
