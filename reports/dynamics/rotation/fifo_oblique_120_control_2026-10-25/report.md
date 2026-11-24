# FIFO: 120-Grad-Symmetriekontrolle bestanden

Lauf: 2026-10-25. Auswertung abgeschlossen: 2026-10-26.
Einmaliger, ausdruecklich angeforderter Zusatz am unveraenderten H=1200-Anker.
Ausfuehrungsrevision: `8150e3f65c414c4fc1326dd44c32f49a788af588`.
[Vorhersage und Toleranzen vor dem Lauf](https://github.com/MemoryDynamics/Knoten/blob/8150e3f65c414c4fc1326dd44c32f49a788af588/reports/project/meta/preregistration/fifo_oblique_120_control_2026-10-25.md).

## Beobachtung

**Beide 120-Grad-Kurven stimmen mit den gespeicherten 60-Grad-Kurven
bei umgekehrtem Gesamtvorzeichen ueberein.** Alle 201 abgetasteten
Formdistanzen je Paar bestehen die vorab festgelegte Toleranzpruefung.

| Neuer Arm | Vergleich | Neuer Endfaktor | Alter Endfaktor | Groesste absolute Kurvendifferenz |
| --- | --- | ---: | ---: | ---: |
| 120 Grad, - | 60 Grad, + | 2087.4775253218772 | 2087.4775253218663 | 1.00614e-16 |
| 120 Grad, + | 60 Grad, - | 2087.333257063465 | 2087.333257063462 | 3.12250e-17 |

Endfaktor bedeutet Formdistanz nach 2000 Updates geteilt durch die
Anfangsformdistanz. Die Kurvendifferenz betrifft die unnormierten
RMS-Formdistanzen. Die ungestoerte Referenz stimmt an allen Abtastpunkten
exakt mit der gespeicherten Referenz ueberein. Die groesste Abweichung
beansprucht etwa `4.86e-7` der vorab festgelegten Toleranz
`1e-11*R + 1e-8*abs(reference)`.

Neu integriert wurden nur zwei 120-Grad-Arme und eine gemeinsame Referenz,
mit RMS-Amplitude `1e-5*R`, in float64, ohne Rauschen oder Parameterwechsel.
Die alten 60-Grad-Ergebnisse aus Revision
`fdbd24fd437187a4db185d413f4c3bd022104b3b` wurden nur gelesen.
Auch das Normalzertifikat wurde nicht wiederholt. Laufzeit des Workers
einschliesslich Start: 2.235 Sekunden, innerhalb des 60-Sekunden-Budgets.
Die Unterbrechung vor Fertigstellung dieses Berichts betraf nur die
Dokumentation; sie hat keinen zusaetzlichen Ziellauf ausgeloest.

## Bedeutung und Grenze

Mit `D(beta)=cos(beta)*P+sin(beta)*N` und der Spiegelung S an der
Kreisebene gilt `D(120)=-S D(60)`. Deshalb gehoeren die entgegengesetzten
Gesamtvorzeichen zusammen. Der radiale Kernel und die FIFO-Verschiebung
kommutieren mit S, auch nichtlinear. Die Formdistanz nach eigentlicher
Rotation und Translation ist unter gemeinsamer Spiegelung invariant.
120 Grad bezeichnet hier den orientierten Mischwinkel in der P/N-Basis;
der Hauptwinkel zur planaren Untermenge bleibt 60 Grad.

Die Daten bestaetigen die erwartete Umsetzung dieser Modellsymmetrie
auf Rundungsniveau. Das ist eine Code- und Symmetrieplausibilisierung,
keine unabhaengige Replikation und keine Bestaetigung realer Physik.
Die algebraische Symmetrie folgt aus dem Modell; die Wachstumsfaktoren
bleiben ein explorativer Befund fuer diesen Anker, diese Muster und
dieses Zeitfenster.

Der [vorherige Wachstumsbefund und das unentschiedene Normalzertifikat](https://github.com/MemoryDynamics/Knoten/blob/fdbd24fd437187a4db185d413f4c3bd022104b3b/reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25/analysis.md)
werden nicht zu einem allgemeinen Instabilitaetsbeweis hochgestuft.
Offen bleibt echte wachsende Normalmode versus transiente Verstaerkung.

## Daten und Pruefung

- [Ausfuehrungsbeleg, feste Eingaben und Herkunftshash](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_oblique_120_control_2026-10-25/receipt.json).
- [Vollstaendige neue Kurven und Laufzeit](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_oblique_120_control_2026-10-25/probe.json).
- [Maschineller Vergleich aller Abtastpunkte](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_oblique_120_control_2026-10-25/summary.json).

Vor Ausfuehrung bestanden 249 betroffene lokale Tests, Lint und strikter
Dokumentationsbau. Kleine Kontrollgeometrien pruefen die nichtlineare
Spiegelungskovarianz, Vorzeichenpaarung, ganze Kurven und die
Prozessabbruchgrenze. Dies ersetzt kein unabhaengiges Fachreview.
Nach Abschluss der Dokumentation bestehen 250 betroffene lokale Tests,
einschliesslich eines reinen Archiv-Audits von Herkunft, Laufzeit,
Vollstaendigkeit und erneutem Vergleich der gespeicherten Kurven.
