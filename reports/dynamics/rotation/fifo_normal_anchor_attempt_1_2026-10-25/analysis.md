# FIFO-Anker: schraege Stoerungen legen eine empfindliche Richtung offen

Stand: 2026-10-25. Der einmalige freigegebene Versuch ist abgeschlossen;
keine Nachsuche, Parameteranpassung oder Wiederholung wurde ausgefuehrt.
Ausfuehrungsrevision: `16f60f5a12281628a55eb5e591fe027418d21a3a`.
Die [eingefrorene Vorabregistrierung](https://github.com/MemoryDynamics/Knoten/blob/16f60f5a12281628a55eb5e591fe027418d21a3a/reports/project/meta/preregistration/fifo_normal_stability_anchor_proposal_2026-10-25.md)
legt Ziel, Winkel, Amplitude, Zeitfenster und Auswertung vorab fest.

## Ergebnis

**Die getestete planare Formstoerung klingt ab, alle getesteten Stoerungen
mit Normalanteil wachsen stark.** Der gesonderte rigorose Normaltest bleibt
bei 80 und 120 Dezimalstellen aufgrund der Intervallaufweitung unentschieden.
Das ist kein Widerspruch: Simulation und Zertifikat beantworten unterschiedlich
starke Fragen. Der Kreis ist damit vorerst kein belegter robuster 3D-Baustein.

| Winkel zur planaren Historienuntermenge | Endabweichung / Anfangsabweichung, beide Vorzeichen |
| ---: | ---: |
| 0 Grad | 0.00046205 bis 0.00046207 |
| 30 Grad | 1206.49 bis 1206.63 |
| 45 Grad | 1705.26 bis 1705.43 |
| 60 Grad | 2087.33 bis 2087.48 |
| 90 Grad | 2408.94 |

Gemessen wird die RMS-Formdistanz der altersmarkierten Historie nach
optimaler Translation und eigentlicher Raumrotation. Reine Orts- und
Orientierungsunterschiede erklaeren dieses Wachstum daher nicht.
Alle zehn Arme starten bei etwa `9.46518e-6`, entsprechend `1e-5*R`.
Nach 2000 nativen deterministischen Updates betraegt die reine
Normalabweichung etwa `0.0228010`, also rund 2.41% des Kreisradius.
Die Winkel beziehen sich auf die Norm des gesamten Historienvektors,
nicht auf identische Verschiebungswinkel an jedem einzelnen Knoten.

![Alle zehn gespeicherten Formantworten; die beiden Vorzeichen liegen weitgehend uebereinander.](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25/shape_response.png?raw=true)

Die reine Normalstoerung hat bei 1000, 1500 und 2000 Updates die Faktoren
23.2281, 237.0001 und 2408.9363. Das Wachstum setzt sich also bis zum Ende
des registrierten Fensters fort. Die reine planare Kontrolle hat nur
eine kleine anfaengliche Verstaerkung (maximal abgetastet etwa 1.00129)
und liegt am Ende bei rund 0.0462% ihrer Anfangsabweichung.
Die gemeinsame ungestoerte Referenz weicht maximal abgetastet um
`2.0895e-15` von ihrer urspruenglichen Kreisform ab. Damit wird die
vorab verlangte Referenzaufloesung klar eingehalten.

## Einordnung des Symmetrieeinwands

**Beobachtung:** Auch die schraegen 30/45/60-Grad-Stoerungen wachsen, mit
beiden Vorzeichen. Der senkrechte Kontrollfall verbirgt das Problem hier
nicht, sondern zeigt die groesste Verstaerkung. Sein Vorzeichenpaar ist
wegen der Spiegelung an der Kreisebene gleich; das ist keine unabhaengige
Replikation. Alle Arme verwenden dieselbe feste raeumliche Musterfamilie.

**Inferenz:** Der fuer diese Familie empfindliche Anteil liegt ausserhalb
der Ebene. Die Endfaktoren folgen naeherungsweise dem Normalanteil
`sin(beta)`; dies ist eine nachtraegliche beschreibende Beobachtung,
kein zusaetzlich registrierter Fit oder neuer Stabilitaetstest.

**Offen:** Ein endliches Wachstumsfenster, selbst mit grossen Faktoren,
ist noch kein Beweis eines Multiplikators ausserhalb des Einheitskreises.
Starke transiente Verstaerkung ist damit nicht mathematisch ausgeschlossen.
Keine Aussage ueber beliebige Muster, andere Amplituden, asymptotische
Rueckkehr, Attraktorwechsel oder Lebensdauer unter Rauschen folgt daraus.

## Warum der rigorose Test unentschieden bleibt

Beide frischen Krawczyk-Pruefungen bestaetigen den Kreisroot. Die
Intervall-Polynomdivision verliert jedoch massiv die Abhaengigkeiten
zwischen wiederholt verwendeten Koeffizienten. Bereits das konstante
Quotientenglied liegt in einem Intervall von etwa
`[-2.3247e660, +2.3247e660]`. Die Schur-Rekursion kann deshalb schon bei
ihrer ersten Vergleichsentscheidung (Grad 1197) nicht fortfahren.
Es gab keinen Timeout; die Panelzeiten betragen 5.765 und 2.797 Sekunden,
einschliesslich 3.328 Sekunden fuer die zehn Zusatzarme im ersten Panel.

Eine direkte Konsistenzdiagnose aus den gespeicherten Koeffizienten:
Fuer `p(z)=g(z)q(z)` mit `g(0)=-1` gilt am exakten Kreisroot
`q(0)=-p(0)`. Das gespeicherte Intervall fuer `p(0)` liegt bei
`5.34250e-9`, mit Breite etwa `1.16e-46` im 120-dps-Panel. Der enorme
Quotientenbereich ist somit keine nachgewiesene physikalische
Verstaerkung dieses Koeffizienten, sondern eine unbrauchbar grobe
Einschliessung. Null in den ebenfalls breiten Restintervallen liefert
keinen zusaetzlichen Beweis. Die Aussage `inconclusive` bleibt unveraendert;
die Identitaet wird nicht nachtraeglich als ersetzter Zertifikatslauf benutzt.

## Konsequenz und naechster Schritt

Die rein planare Stabilitaetsevidenz darf nicht zu einem robusten
dreidimensionalen Knoten hochgestuft werden. Ebenso gibt es hier keinen
Nachweis einer schwachen Wechselwirkung oder einer neuen Teilchenart.
Die Paper-I-Baseline und der separate H=2400-G5-Befund werden nicht durch
dieses H=1200-Ergebnis umgedeutet.

Naechster methodischer Schritt ist eine gezielte Pruefung der vermuteten
wachsenden Normalmode mit einer abhaengigkeitserhaltenden oder direkt
spektralen Zertifikatsmethode, zuerst an synthetischen Gegenkontrollen.
Nicht durch Auswahl anderer Parameter den bisherigen Kreis retten.
Ein weiterer Zieltest benoetigt einen eigenen begrenzten Vertrag und
erneute Freigabe; der vorliegende Versuch ist verbraucht.

## Nachvollziehbarkeit

- [Unveraenderter maschineller Kurzreport](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25/report.md).
- [Ausfuehrungsbeleg und exakte Eingaben](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25/receipt.json).
- [80-dps-Panel samt allen 201 Abtastwerten je Zusatzarm](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25/panel_80.json).
- [120-dps-Panel ohne wiederholte Trajektorien](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25/panel_120.json).
- [Reine Nachverarbeitung fuer die Abbildung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/experiments/current/dynamics/rotation/plot_fifo_oblique.py): liest nur gespeicherte Messwerte, keine Integration oder Parametersuche.

Vor Ausfuehrung bestanden 229 betroffene lokale Regressionstests,
Lint, strikter Dokumentationsbau sowie die vollstaendige GitHub-CI und
beide Paper-I-Reproduzierbarkeitsjobs auf der eingefrorenen Revision.
Diese Softwarekontrollen sind kein unabhaengiges wissenschaftliches Review.
Nach dem Lauf bestehen 233 betroffene lokale Tests, darunter vier reine
Archivpruefungen auf Herkunft, beide Intervallabbrueche, alle Arme und
Abtastwerte, Budget und fehlende Wiederholung. Die Abbildung wurde aus den
gespeicherten Daten erzeugt und visuell geprueft; die Rohdateien wurden
fuer diese Auswertung nicht veraendert.
