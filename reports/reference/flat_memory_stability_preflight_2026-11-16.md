# Memory-Vierzyklus: begrenzte Stabilitaetspruefung vorbereitet

Stand: 2026-11-16. **Vorbereitung, kein Ergebnis des Zielkandidaten.**
Die konkrete Autorenfreigabe fuer die einmalige Auswertung steht aus.
Paper I bleibt unveraendert.

## Befund und Reichweite

Das Pruefprogramm fuer den bereits angefragten Vertreter der
[positiven Vierphasenfamilie](flat_memory_cycle_2026-11-16.md) ist
implementiert. Es verwendet die volle Historienableitung und den
[analytisch begruendeten Acht-Formmoden-Quotienten](memory_shape_quotient_2026-11-16.md).
Es wurde **nicht** am neuen positiven Kandidaten ausgefuehrt.
Der Ziel-Versuchsordner existiert bei Abschluss dieser Vorbereitung nicht.

Das Programm kann unter den dokumentierten analytischen Voraussetzungen
lokales Formwachstum durch eine rigorose Produktverletzung bescheinigen.
Es kann keinen positiven Stabilitaetsnachweis liefern: Liegt das Produkt
nicht strikt ausserhalb von [-1,1], bleibt das Ergebnis offen, auch wenn
alle Gleitkomma-Eigenwerte innerhalb des Einheitskreises liegen.
Eine spaetere Schur-/Intervallpruefung waere dann ein eigener Schritt.

## Festgelegter Umfang

- Exakte Eingaben f=1/2, g=2/3, q=99/100; H_s=H_v=4, epsilon=0.
- Sigma, beide Memory-Massennormierungen und attraktive Amplitude sind
  eins; repulsive Amplitude null. Geometrie, skalare Retention und Gains
  folgen ausschliesslich aus der bewiesenen Familie.
- Eine Kindprozess-Auswertung, hoechstens 30 Sekunden bis zum Abbruch,
  einschliesslich Prozessstart; numerische Thread-Umgebungen auf eins.
  Aufraeumen und Protokollieren koennen nach dem Abbruch stattfinden.
- Keine Zieltrajektorie, Parametersuche, Nachanpassung oder Wiederholung.
  Vier lokale Update-Kompositionen pruefen den Rueckkehroperator;
  sie sind kein Langzeitlauf und keine Lebensdauerprobe.
- Quellenstand muss ein sauberer Worktree an einer vollstaendig angegebenen
  Commit-ID sein. Quellpfade, SHA-256-Pruefsummen und Laufzeitversionen
  werden protokolliert und Quellen nach dem Lauf erneut abgeglichen.

Der exklusive Versuchsordner wird vor dem einzigen Worker angelegt.
Ein Timeout oder Fehler verbraucht diesen Versuch ebenfalls; vorhandene
Ergebnisse werden weder ueberschrieben noch automatisch neu gerechnet.
Import, Hilfe und `--describe` fuehren keine Zielauswertung durch.
Die Ausfuehrungsoption bestaetigt nur eine vorher erteilte menschliche
Freigabe; sie erteilt diese nicht selbst.

## Numerischer Nachweisweg

1. Exakte rationale Familienparameter werden vor jeder Intervallrechnung
   validiert. Mit mpmath.iv 1.3.0 bei 80 Dezimalstellen werden das
   analytische Formprodukt und die strikte Innenlagemarge eingeschlossen.
   Die Entscheidung nutzt die exakten binaeren Intervallendpunkte,
   nicht gerundete Dezimaldarstellungen.
2. Eine getrennte float64-Kontrolle setzt die native Historie und feste
   Gains ein. Sie prueft alle vier Orbitphasen, die sieben begruendet
   entfernten Richtungen, den wirklichen vierfachen Ableitungsoperator
   und die Spur des Acht-Formmoden-Quotienten. Normierte Konsistenzfehler
   duerfen 1e-9 nicht ueberschreiten.
3. Das Produkt der numerischen Quotientenmatrix muss zur Intervallmitte
   passen. Ihre acht Eigenwerte und beide Matrizen werden nur als
   Diagnose gespeichert. Eine kleine numerische Spektralradiusangabe
   darf nicht zu einem Stabilitaetsurteil fuehren.
4. Ein zertifizierter Befund verlangt strikt positive Innenlagemarge,
   Produktbetrag rigoros ueber eins und bestandene Methodenabgleiche.
   Andernfalls lautet das Ergebnis offen oder methodisch inkonsistent.

Die Intervallaussage betrifft den analytischen Orbit mit reellen,
aus den Formeln definierten Parametern. Die float64-Konfiguration ist
eine Implementierungskontrolle, kein gesondert zertifizierter Orbit der
gerundeten Parameter. Vertrauen setzt die geprueften analytischen
Identitaeten und die Intervallbibliothek voraus, keinen formalen
Beweisassistenten.

## Kontrollen und Abdeckung

49 neue feste Kontrollen pruefen strikte Intervallgrenzen, nichtendliche
Werte, Quellen-/Freigabeschranken, harte Zeitbegrenzung, exklusive
Protokollierung und verweigerten Zweitstart. Die echte lokale
Ableitungsroutine wird nur am bereits bekannten negativen-Gain-
Kontrollorbit und einer abgewiesenen Off-Orbit-Stoerung geprueft.
Dort reproduziert sie das bekannte Produkt (27/8)*ln(2).
Alle positiven Worker-Ergebnisse in den Runnertests sind synthetische
Payloads mit ersetzten Rechenstufen, keine ausgewerteten Kandidaten.

Das betroffene Panel umfasst 453 bestandene Tests einschliesslich
32 vorhandener synthetischer Kontrollen des wiederverwendeten
Intervallendpunkt-Lesers. Lint und strikter Dokumentationsbau bestehen.
Dies ist keine vollstaendige Repository-Testsuite und keine neue
Literaturrecherche.

## Quellen und offene Entscheidung

Die wissenschaftlichen Voraussetzungen stehen im
[Existenzbericht](flat_memory_cycle_2026-11-16.md), im
[Historienableitungsbericht](memory_history_response_2026-11-16.md) und
im [Formquotientenbericht](memory_shape_quotient_2026-11-16.md).
Implementierung: `src/emergenz_knoten/flat_memory_stability.py` und
`experiments/current/dynamics/rotation/flat_memory_cycle_stability.py`.
Neue Tests: `tests/test_flat_memory_stability_runner.py` und die
Ergaenzungen in `tests/test_memory_defect_recurrence.py`.

Der naechste konkrete Entscheidungspunkt bleibt die ausstehende Freigabe
des einen begrenzten Ziellaufs; die aktive Reihenfolge steht allein in
den [Projektprioritaeten](../../docs/status/project_priorities.md).
Bis dahin kein positiver oder negativer Stabilitaetsbefund fuer diesen
Vertreter. Auch ein spaeterer Befund entscheidet weder Bildung und
Lebensdauer noch elektrische Ladung, Gegenladung, Spin oder Teilchenart.
