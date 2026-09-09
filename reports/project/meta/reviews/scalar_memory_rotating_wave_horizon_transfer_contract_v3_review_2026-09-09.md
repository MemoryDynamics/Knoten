# Review: Horizonttransfer-Evidenzvertrag v3

Datum: 2026-09-09.

Gepruefte Implementierungsrevision:
`2ca6aa1439acfe26a7ef41f1960aca6a58e921f4`.

Gepruefte CI:
[GitHub Actions run 34311425972](https://github.com/MemoryDynamics/Knoten/actions/runs/34311425972),
erfolgreich fuer die exakte Implementierungsrevision.

Verdict:
**`rotating-wave-horizon-transfer-contract-v3-pass-runner-red-open-target-closed`**.

Der v3-Vertrag schliesst die im vorausgehenden Evidenzreview gefundenen
positiven und negativen Nachweisluecken. Der wissenschaftliche Runner fehlt
weiterhin. Weder dieses Review noch der Vertrag autorisiert einen
Horizontlauf, P5-D-Versuch 4 oder eine Interaktions-, Traegheits- oder
Masseaussage.

## 1. Prospektive Kette und gebundene Artefakte

Das negative Evidenzreview wurde an Revision
`ef7707514468754837ef6a5c5648b73024be82b0` separat eingefroren. Die dritte
Protokollamendierung folgte vor jedem Targetzugriff; eine weitere
Portabilitaetsamendierung wurde notwendig, nachdem Linux-CI
[34310627799](https://github.com/MemoryDynamics/Knoten/actions/runs/34310627799)
die behauptete Plattformdeterministik nativer `sin`-/`cos`-Starts
falsifizierte. Diese Amendierung ist Revision
`75ce9adae6790f4fa86ee7c1a8f85a0a600492a6`, Protokollblob
`671e931a8337b1c31923dbd122085167185e9091`.

Gebundene v3-Artefakte der geprueften Revision:

- Gate-/Validatorblob: `64a824d65d76fd7e838d58c7f07c732efbd9df02`;
- unabhaengiger Auditorblob: `90bfeab8bbdd2d89b95fc1247e6281f50b95b996`;
- Schemablob: `4db175cb95914cf2122a3b57324f802793c8bc50`;
- Gate-Testblob: `89dc8b04e277b453ba77ec3e87856c067c711f69`;
- Auditor-Testblob: `0dda4ae71f312369f4cfc77921536c3611cdb7ae`.

## 2. Rekonstruierte Evidenzbeziehungen

Runner-Validator und Standardbibliothek-Auditor rekonstruieren aus den
gespeicherten primitiven Daten:

- beide aeusseren und inneren Krawczyk-Einschluesse je Rootpanel,
  Newtonkonfiguration, Zentrenabstand und exakten inneren Bildschnitt;
- feste Homotopieintervalle, Boxbreiten, linear interpolierte Boxzentren,
  strikte Inklusion und wirkliche Bildueberlappung;
- Residualausschluss oder strikten Krawczyk-Einschluss jedes klassifizierten
  Ausschlussleaves sowie Kante und maximale Tiefe;
- beide Tailzertifikate, Praezisionsreihenfolge und gemeinsamen Bildschnitt;
- Solverkonfiguration, Eigenwertmoduli, Sortierung, Symmetrieklassifikation,
  Symmetrieeigenwerte und fuehrenden transversalen Panelabstand;
- den binary64-gerundeten H=2400-Root, drei vollstaendige Stoervektoren,
  deren Amplitude und Hashes sowie alle Trajektorienkennzahlen;
- Kontrollschwellen, Gatevoraussetzungen und finale Entscheidungsrangfolge.

Die zwei Arnoldi-Starts werden aus einer 32-bit-LCG und einem expliziten
binary64-Hexwert rekonstruiert. Ihre Hashes sind auf Windows und Linux
identisch; native trigonometrische Bibliothekswerte sind nicht mehr Teil des
Vertrags.

## 3. Falsifikation und Verifikation

Die targetfreien Negativtests verwerfen insbesondere:

- fehlende oder falsch dimensionierte Zertifikate, falsche Boxbreite,
  Center-Behauptung, Bildinklusion und inneren Schnitt;
- falsches Homotopie-s-Intervall, verschobenes Interpolationszentrum und
  erfundene Ueberlappung;
- unbelegten Residualausschluss und falschen Krawczyk-Leaf;
- falschen Tailbildschnitt, Arnoldi-Starthash, Stoerungsvektor oder -hash;
- falsche Eigenwertmoduli, Symmetrieklassifikation und Panelzusammenfassung;
- abweichenden gerundeten Root sowie erfundene Trajektorien- und
  Kontrollsummaries;
- Null-Locher und positive Gates nach abgebrochener Evidenz.

Verifikation:

- 59/59 fokussierte Vertrags- und Auditor-Tests bestanden lokal;
- 1004/1004 Repositorytests bestanden in der offiziellen Linux-CI;
- Ruff und strikter MkDocs-Bau bestanden dort ebenfalls;
- Ergebnis-JSON, Bericht, Publikationsmanifest, unabhaengiger Auditoutput und
  Ergebnisreview blieben abwesend.

## 4. Verbleibende Vertrauensgrenze

Der Auditor ist absichtlich kein zweiter Intervallbackend und kein zweiter
Arnoldi- oder Trajektorienrunner. Er rekonstruiert Inklusionen,
Kardinalitaeten, Hashes, Schwellen und Summary-Beziehungen, berechnet aber
weder Krawczyk-Bilder noch Ritzresiduen oder Dynamik erneut. Diese
wissenschaftliche Numerik muss der spaetere Runner erzeugen und ein separates
Ergebnisreview kritisch beurteilen.

Die synthetische Pass-Fixture ist keine Evidenz fuer einen endlichen oder
unendlichen Root, Stabilitaet oder Branchtransfer. Ein struktureller
`inconclusive`-Record beweist weder Branchverlust noch Instabilitaet.

## 5. Naechste geschlossene Grenze

Geoeffnet ist ausschliesslich ein targetfreier RED-Schritt fuer die
Runner-Orchestrierung mit injizierten synthetischen Backends. Er muss
Newtonleiter, Homotopiestopp, Ausschlussbaum, Tailpanels, Arnoldi-Ausgabe,
Stoerungsarme, Kontrollen und Manifestreihenfolge pruefen und jeden
registrierten Ergebnis- und Zielpfad durch Traps geschlossen halten.

Erst nach Runnerimplementierung, separatem Implementierungs-Readinessreview,
sauberem Commit und gruener exakter CI darf ein einzelner Horizontlauf erneut
zur ausdruecklichen Nutzerentscheidung gestellt werden. P5-D bleibt davon
getrennt und geschlossen.
