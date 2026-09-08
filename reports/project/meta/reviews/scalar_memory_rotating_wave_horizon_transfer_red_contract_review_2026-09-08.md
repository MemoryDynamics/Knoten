# RED-Review: Ergebnisvertrag fuer den Rotating-wave-Horizonttransfer

Datum: 2026-09-08.

Gepruefte RED-Revision:
`66644f4b0c708bf71f250610e47d759ecb8e4679`.

Verdict:
**`rotating-wave-horizon-transfer-red-contract-complete-implementation-open-target-closed`**.

Der prospektiv registrierte Ergebnisvertrag und die targetfreien Tests sind
vor Runner- und Auditorcode committed. Dieser Review dokumentiert nur den
erwarteten RED-Zustand. Er enthaelt keinen neuen Root, keine
Horizonttrajektorie, kein Arnoldi-Panel und keine P5-D-Autorisierung.

## 1. Gebundene Artefakte

- Ergebnisschema, Blob `48f2324b9b4915c4f4a1ad31903e9f24242387fa`;
- Runner-Vertragstests, Blob `b252e9af9a5f06dea3a18316b6fdd0ba7f8f5935`;
- Auditor-Vertragstests, Blob `951c1d3e76bf357e8347e7afbe0cd0f5205111c1`.

Das Schema besitzt exakt die sieben Rootobjekte `identity`, `finite_branch`,
`infinite_tail`, `stability`, `controls`, `classification` und
`publication`. Es schliesst unbekannte Felder, nichtendliche Zahlen,
NumPy-Skalare und einen selbstreferenziellen Ergebnishash aus. Genau zwei
Inhaltsartefakte gehen dem Manifest voraus; ihre Hashes gehoeren in das
spaetere Manifest und nicht in den Resultrecord.

## 2. Beobachteter RED-Zustand

Der gezielte Lauf sammelt ohne Import- oder Fixture-Abbruch und endet mit:

```text
2 passed, 28 failed
```

Die zwei bestandenen Tests pruefen die reine Vertragsstruktur und alle
internen Typreferenzen. Jeder der 28 Fehlschlaege nennt als erste fehlende
Grenze ein Symbol des noch nicht vorhandenen registrierten Runners oder des
noch nicht vorhandenen unabhaengigen Auditors. Es gibt keinen numerischen
Fehlschlag und keinen Targetzugriff.

Die roten Tests decken ab:

1. finite Residualformel und analytischen Jacobian gegen eine unabhaengige
   kleine direkte Summe;
2. dezimales `q=0.99`, semantikgleiche binary64-Pfade und die getrennte
   `log1p`-Diagnostik;
3. die drei konservativen Tailbounds;
4. outward-konservative Intervall-Drift und Breitenmutation;
5. fail-closed Homotopieunterbrechung;
6. partielle, vektorlose oder residualfehlerhafte Arnoldi-Panels;
7. unabhaengige zyklische FIFO-Semantik, drei Mutationen und
   `eta=0`-Kollaps;
8. alle sieben Entscheidungsraenge und die einzige P5-oeffnende Entscheidung;
9. strikte Schemawerte und Manifest-last-Publikation;
10. manifest-first Hashpruefung sowie unabhaengige Auditor-Rekonstruktionen.

Der unveraenderte Bestandsumfang besteht separat mit `945 passed`. Ruff fuer
beide neuen Tests und der strikte Dokumentationsbau bestehen. Der
Gesamttestsatz ist absichtlich rot, solange die zwei registrierten Module
fehlen.

## 3. Kritische Grenzen

Der Vertrag ist ein projektspezifisches fail-closed Typmodell, kein
allgemeines JSON-Schema. Seine Aussage haengt spaeter von zwei getrennten
Validatorimplementierungen ab. Der vollstaendige 4800-komponentige
Eigenvektor ist registriert und kann die Ergebnisdatei gross machen; das ist
eine bewusste Konsequenz der Forderung, Vektoren statt nur Ritzwerte zu
speichern.

Die Tests definieren eine Implementierungsschnittstelle. Ein spaeteres
Gruenwerden belegt zunaechst nur Formel-, Vertrags-, Kontroll- und
Publikationssemantik. Krawczyk-Einschluesse, Arnoldi-Spektrum und
Trajektorien bleiben bis zum separat autorisierten Horizontlauf unbeobachtet.

## 4. Naechste Grenze

Geoeffnet ist ausschliesslich die kleinste targetfreie Implementierung, die
diese 28 Tests gruen macht. Sie darf keine registrierte Rootmitte berechnen,
keine Horizontgeschichte fortsetzen, keinen H=2400-Arnoldi-Holdout auswerten
und keinen registrierten Ergebnis-, Report-, Manifest- oder Auditpfad
schreiben.

Nach der Implementierung sind Gesamttests, Ruff, strikte Dokumentation,
gruenes CI und ein separates Implementierungs-Readinessreview erforderlich.
P5-D und Versuch 4 bleiben geschlossen.
