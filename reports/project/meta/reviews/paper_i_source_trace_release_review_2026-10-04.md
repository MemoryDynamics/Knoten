# Paper I: Quellen- und Release-Referee-Pass

Datum: 2026-10-04  
Urteil: `paper-i-source-trace-pass-release-metadata-open`

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

Der Quellenpfad ist nun eindeutig, aber die Einreichung ist noch nicht
archivfest. Es fehlen ein zweiter unabhaengiger Intervallbackend, ein
transitiver Dependency-Lock mit Artefakthashes, eindeutige Autoren- und
Preferred-citation-Metadaten fuer `CITATION.cff` sowie eine unveraenderliche
Release-ID oder DOI. Die bestehenden direkten Python-Pins sind deshalb nicht
als vollstaendiger Lock auszugeben.

Die Auditoren sind vom Produktionsrunner getrennt und rekonstruieren die
Records, teilen aber den wesentlichen `mpmath.iv`-Trust-Stack. Sie sind keine
unabhaengige Intervallreplikation. Ebenso folgt aus der lokalen
Endpunktidentitaet weiterhin keine dynamische $H\to\infty$-Stabilitaet.

## Referee-Urteil

Kein Critical- oder Major-Claimfehler wurde in der Quellenzuordnung gefunden.
Die Reproduktionsanleitung vermeidet einen methodisch unzulaessigen Rerun
verbrauchter Produktionsleases und beschraenkt sich auf Record-, Quell- und
Vertragspruefung. Vor der Bezeichnung "citation ready" bleiben die vier
Releasegrenzen offen; sie sind Infrastruktur- beziehungsweise
Replikationsaufgaben und duerfen die Claimstufe nicht veraendern.
