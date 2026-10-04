# Paper I: Quellen- und Release-Referee-Pass

Datum: 2026-10-04  
Urteil: `paper-i-source-trace-and-release-metadata-pass-archive-open`

## Umfang

Geprueft wurden die materiellen Claims beider Paper-I-Fassungen gegen
Resultatrecords, Ausfuehrungscommits, Codepfade, Audits, Tests und explizite
Negativgrenzen. Es wurde kein numerischer Ziellauf wiederholt und keine
verbrauchte One-shot-Governance geoeffnet.

## Befund

Die neue Supplementspur fuehrt sechs und damit bewusst weniger als sieben
Claims. C1--C2 decken den skalaren Paper-I-Hauptbefund und seine kontrollierte
Abgrenzung ab. C3--C6 trennen finite Rootastverbindung, direkte lokale
$H=2400$-Stabilitaetsevidenz, lokalen $F_\infty$-Root und die outcome-
informierte post-hoc Endpunktreconciliation.

Jeder Claim besitzt mindestens einen Resultat-, Code- und Testpfad. Alle
Pfade existieren sowohl im aktuellen Checkout als auch im eingefrorenen
Evidenzcommit `1bbaa4752907f0bf34e2a4bc8635426042c5a652`.
Ein eigener Vertrag prueft ausserdem die positiven Entscheidungen von G1--G5
und bewahrt die negative Attempt-4-Entscheidung unveraendert. Damit kann die
post-hoc Reconciliation nicht stillschweigend in einen prospektiven Pass
umetikettiert werden.

## Kritische Grenzen

Der Quellenpfad ist nun eindeutig. Ein mit Python 3.12 erzeugter transitiver
Lock bindet 50 Pakete und 1219 PyPI-Artefakthashes; seine Installation mit
`--require-hashes` besteht in einem frischen Zielordner. `CITATION.cff`
uebernimmt Titel und Autor H. Horn aus der Langfassung, ohne ORCID, Journal
oder DOI zu erfinden, und besteht die CFF-1.2.0-Schemavalidierung.

Die Einreichung ist dennoch nicht archivfest. Es fehlen ein zweiter
unabhaengiger Intervallbackend und eine unveraenderliche Release-ID oder DOI.

Die Auditoren sind vom Produktionsrunner getrennt und rekonstruieren die
Records, teilen aber den wesentlichen `mpmath.iv`-Trust-Stack. Sie sind keine
unabhaengige Intervallreplikation. Ebenso folgt aus der lokalen
Endpunktidentitaet weiterhin keine dynamische $H\to\infty$-Stabilitaet.

## Referee-Urteil

Kein Critical- oder Major-Claimfehler wurde in der Quellenzuordnung gefunden.
Die Reproduktionsanleitung vermeidet einen methodisch unzulaessigen Rerun
verbrauchter Produktionsleases und beschraenkt sich auf Record-, Quell- und
Vertragspruefung. Vor der Bezeichnung "archivally released" bleiben die zwei
Releasegrenzen offen; sie sind Infrastruktur- beziehungsweise
Replikationsaufgaben und duerfen die Claimstufe nicht veraendern.

Beide Manuskriptfassungen verweisen mit dem unveraenderlichen Commit
`ace7000351b7c4ccba8f9cfc8b7464c3361993f2` direkt auf diese Evidenzspur. Der
externe Leser ist damit nicht auf einen beweglichen Branchzustand angewiesen.
