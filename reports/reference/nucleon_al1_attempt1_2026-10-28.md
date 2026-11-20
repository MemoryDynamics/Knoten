# AL1-Referenz, Versuch 1: Freigabe und Ergebnisprotokoll

Stand: 2026-10-29. Status: **beide Laeufe abgeschlossen; Freigabe verbraucht**.
Das Vorabprotokoll (2026-10-28, 22:41 UTC) wurde vor Start in Commit
[`db5b57a`](https://github.com/MemoryDynamics/Knoten/commit/db5b57a)
festgehalten. Es folgten genau ein Nukleon- und ein Delta-Prozess.

## Freigabe und unveraenderter Vertrag

Der Autor antwortete in diesem Chat auf die konkrete Frage nach je einem
raeumlichen AL1-Lauf fuer Nukleon (Spin 1/2) und Delta (Spin 3/2):
"Ja, beide begrenzten Referenzlaeufe". Genehmigt sind je hoechstens fuenf
Minuten, ein CPU-Thread, drei feste Basisstufen, keine Parameteranpassung
und keine automatische Wiederholung. Die Referenztheorie bleibt strikt
vom Emergenznachweis aus Memory getrennt.

Der [vorab festgelegte Vertrag](../project/meta/preregistration/nucleon_al1_reference_proposal_2026-10-28.md)
gilt unveraendert. Zuerst Nukleon, dann Delta; ein technischer Fehler oder
Zeitlimit stoppt das gesamte Panel. Eine vollstaendige, aber numerisch
`inconclusive` Rechnung erlaubt den zweiten bereits genehmigten Sektor.
Kein FIFO-, P5-, Elektronen- oder Wasserstoff-Ziellauf ist freigegeben.

## Eingefrorene Quellen und Ausgabe

Solver-, Parameter- und Supervisor-Commit:
[`558608448070f4ef11b6282bb444c4e6e0998404`](https://github.com/MemoryDynamics/Knoten/commit/558608448070f4ef11b6282bb444c4e6e0998404).
Der Worktree war vor Dokumentation der Freigabe sauber. Seit dem
bestandenen synthetischen Preflight wurde der Solver nicht geaendert.

SHA-256 vor Start:

| Datei | Hash |
| --- | --- |
| `nucleon_gaussian_run.py` | `49b40dfdd5792c1f0cc94ebc76dc0920b97153971375bf951e530536835d0fde` |
| `nucleon_gaussian_basis.py` | `8ce519310b51071e06644ce13061bc51e369a3fe6de12fc2fce542974ead523f` |
| `nucleon_spatial_preflight.py` | `fb5a666d162fe0a12d0dc7177856d21e9637f70157eee0a53ff36e8bf8d1b2cb` |
| `nucleon_spin_flavor_reference.py` | `b28ed878bb1fb0a401c2c4404af25b7a474ac0d3fc97c764f8b708ebea77bc72` |
| `run_nucleon_al1_bounded.ps1` | `9d7a041a82ceabe0c9a31448054b8e56be045e5436e25857a8c6aa23e62972aa` |

Runtime: Python aus dem gebuendelten Codex-Runtime-Verzeichnis;
`PYTHONPATH=C:/tmp/paper-i-final-deps;C:/tmp/knoten-pytest;src`.
Der Supervisor setzt `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`,
startet den Python-Prozess unsichtbar und besitzt die harte 300-s-Grenze.
Die Ausgabeoeffnung ist exklusiv; bestehende Versuche werden nicht ersetzt.

Reservierte neue Namen unter `reports/reference/`:

- `nucleon_al1_attempt1_2026-10-28.json`, samt `.stdout.log` und `.stderr.log`.
- `delta_al1_attempt1_2026-10-28.json`, samt `.stdout.log` und `.stderr.log`.

Ausfuehrungsform je Sektor: `run_nucleon_al1_bounded.ps1 -Python <runtime>
-Sector <nucleon|delta> -OutputName <oben genannter Dateiname>`.
Kein Prozess war zum Zeitpunkt dieses Vorabprotokolls gestartet.

## Ergebnis

**Beide Sektoren: `finite-basis-consistency-pass`.** Alle drei Stufen
und beide Cutoffs sind vorhanden; alle 17 vorab festgelegten Kriterien
pro Sektor bestehen. Beide Prozesse endeten mit Exitcode 0, die
Fehlerlogs sind leer. Keine Wiederholung oder Parameteranpassung.

| Sektor | Prozessfenster am 28.10. UTC, nach Logzeitstempeln | Solverzeit | Status |
| --- | --- | --- | --- |
| Nukleon, $S=I=1/2$ | 22:42:37.7 bis 22:42:58.9 | 20.406 s | endlicher Konsistenz-Pass |
| Delta, $S=I=3/2$ | 22:43:19.5 bis 22:43:40.6 | 20.407 s | endlicher Konsistenz-Pass |

Der Supervisor setzte fuer beide Prozesse die drei Threadvariablen auf 1;
der Python-Report bestaetigt `OPENBLAS_NUM_THREADS=1`. Es gab keinen
Timeout. Die Kill-Verzweigung des Supervisors wurde daher nicht ausgefuehrt
und wird durch diesen Versuch nicht als runtime-getestet ausgegeben.

Rohdaten: [Nukleon](nucleon_al1_attempt1_2026-10-28.json),
[Delta](delta_al1_attempt1_2026-10-28.json), jeweils samt
[Nukleon-stdout](nucleon_al1_attempt1_2026-10-28.json.stdout.log),
[Nukleon-stderr](nucleon_al1_attempt1_2026-10-28.json.stderr.log),
[Delta-stdout](delta_al1_attempt1_2026-10-28.json.stdout.log) und
[Delta-stderr](delta_al1_attempt1_2026-10-28.json.stderr.log).
Alle Exponenten, Zustandskoeffizienten, Metrikspektren, Normen und
Observablen bleiben erhalten, auch die grobe Stufe 0.

### Numerische Ergebnisse

Energien einschliesslich Ruheenergie und vereinbartem Offset, **keine
Bindungsenergien relativ zu freien Quarks**. Der confinierende Operator
besitzt hier keine freie Dreiquarkschwelle. Bei beiden Cutoffs stimmen
je Stufe die ausgegebenen Energien und Observablen ueberein; daher werden
sie hier nur einmal gezeigt. Die JSON-Dateien behalten beide Loesungen.

| Stufe | Gaussfunktionen | Nukleonenergie / MeV | Rang N / roh | Deltaenergie / MeV | Rang Delta / roh |
| --- | --- | --- | --- | --- | --- |
| 0 | 18 | 1165.065613 | 51 / 72 | 1558.248968 | 18 / 18 |
| 1 | 50 | 930.750085 | 145 / 200 | 1242.130794 | 50 / 50 |
| 2 | 98 | 930.733035 | 287 / 392 | 1242.105567 | 98 / 98 |

Letzte Energieaenderung: 0.017049 MeV fuer N und 0.025227 MeV fuer Delta.
Maximales relatives endliches Matrixresiduum: $5.82\,10^{-17}$ bzw.
$1.07\,10^{-16}$. Die Radien- und Spin-Kriterien bestehen ebenfalls.
Die Metrikkondition in der letzten Stufe liegt bei etwa $4.07\,10^7$.

Die endliche Energiedifferenz ist
$E_\Delta-E_N=311.372531$ MeV. Sie ist gross gegenueber der Summe der
beobachteten letzten Energieaenderungen und Cutoffunterschiede
(0.042276 MeV). Das stuetzt die Reihenfolge **in den geprueften endlichen
Raeumen**. Diese Summe ist keine rigorose Fehlerschranke. Es wurden weder
saemtliche Quantenzahlsektoren verglichen noch Spinquantisierung erzeugt.

Wichtige Grenzen der Abnahme: Die zwei Cutoffs behalten jeweils denselben
Unterraum; ihr identisches Ergebnis ist keine unabhaengige Konvergenzprobe.
Stufe 2 ergaenzt sehr kurze/lange Skalen, verdichtet aber nicht systematisch
alle mittleren Breiten und Winkelkorrelationen. Ein kleines letztes
Energiedelta begrenzt deshalb den fehlenden Kontinuumsanteil nicht. Die
angegebenen Ziffern dienen der Reproduzierbarkeit, nicht einer behaupteten
physikalischen Praezision. Ein unabhaengiger numerischer Methodenvergleich
zum identischen Hamiltonoperator bleibt offen.

### Physikalische Diagnostik, ohne Nachfit

Letzte Stufe, dieselbe gekoppelte Wellenfunktion fuer alle Groessen:

| Groesse | Nukleon | Delta |
| --- | --- | --- |
| Mittlerer Quark-rms-Radius / fm | 0.494643 | 0.578021 |
| Geladener NR-Impulsradius / fm | 0.524588 | 0.578021 |
| Neutraler NR-Ladungsradius **zum Quadrat** / fm^2 | -0.0305212 | 0 |
| u-Spin-Gewicht | 1.31528464 | 2/3 |
| d-Spin-Gewicht | -0.31528464 | 1/3 |
| $2\langle T\rangle/(3m)$ | 1.752086 | 1.178795 |

NR bezeichnet hier den nichtrelativistischen Impulsoperator, nicht den
vollstaendigen Sachs-Formfaktor. Beim Delta sind die geladenen/neutralen
Readouts Delta+ und Delta0, **nicht** Proton und Neutron. Die archivierten
generischen Schluessel `charge_p_*` / `charge_n_*` bezeichnen dort lediglich
die entsprechenden Flavorladungen. Beide Sektoren wurden bei
$S_z=I_z=1/2$ gerechnet; fuer Delta ist das keine maximale Polarisation.
Ein negativer neutraler Ladungsradius zum Quadrat ist ein vorzeichenbehaftetes
Ladungsmoment und kein negativer geometrischer Laengenradius.

Die Einheitenumrechnung verwendet
$\hbar c=0.1973269804\ \mathrm{GeV\,fm}$ nach
[NIST/CODATA 2022](https://physics.nist.gov/cgi-bin/cuu/Value?hbcmevf%7Csearch_for=c).
Die grossen $v^2$-Proxies bedeuten nicht ueberlichtschnelle reale Quarks:
$p/m$ ist die nichtrelativistische Geschwindigkeitsnaeherung, nicht die
relativistische Geschwindigkeit. Der fuer eine kontrollierte
Niedriggeschwindigkeitsentwicklung erforderliche kleine Parameter fehlt.
Ein numerischer Pass validiert diese physikalische Naeherung nicht.

Im vereinbarten additiven Momentoperator, mit $U,D$ als u/d-Spin-Gewichten
und derselben Constituent-Masse $m=0.315$ GeV, gilt fuer das Nukleon:

$$
\frac{\mu_p}{e/(2m)}=\frac{2U-D}{3}=0.98195130,\qquad
\frac{\mu_n}{e/(2m)}=\frac{2D-U}{3}=-0.64861797,
\qquad \frac{\mu_n}{\mu_p}=-0.66053985.
$$

Diese Einheit ist **nicht** das Kernmagneton $e/(2M_p)$. Das
Momentenverhaeltnis hat gegen den dokumentierten Messvergleich
$-0.6849793$ eine relative Abweichung von 3.568 Prozent. Es ist damit in
diesem Ansatz weiter entfernt als die vorherige reine Zustandsalgebra
mit $-2/3$ (2.673 Prozent). Vergleichswert und additive Momentkonvention:
[PDG 2025, Abschnitt 15.6](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-quark-model.pdf).
Diese Verschlechterung bleibt stehen; es wurde kein Parameter an das
Moment angepasst. Sie ist kein neuer Fehlernachweis fuer QCD.

### Auswertung und Bedeutung

Die [arithmetische Zusammenfassung](nucleon_al1_attempt1_summary_2026-10-28.json)
enthaelt alle sechs Loesungen je Sektor, Umrechnungen und Hashes der beiden
Eingabedateien. Ihr
[Auswertungsprogramm](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/experiments/current/reference/nucleon_al1_archive_summary.py)
importiert keinen Solver, baut keine Matrix neu auf und loest kein weiteres
Eigenproblem. Es verwendet nur die gespeicherten Observablen.
Elf neue Archivtests pruefen unter anderem die unveraenderte Abnahme,
Zustandsdimensionen, Ladungsradius-/Spin-Summenregeln, Einheiten und die
Trennung von beobachteter Sensitivitaet und Fehlerschranke. Die gespeicherte
Zusammenfassung wird mit rein arithmetischer Neuauswertung verglichen;
die Eingabehashes werden separat geprueft. Fuer diese Dateien verhindert
eine lokale Git-Attributregel die automatische Zeilenendenkonvertierung.

Verifikation am 2026-10-29: **151 betroffene Tests bestanden in 3.38 s**,
einschliesslich der elf Archivchecks und der synthetischen Solver-,
Paar- und Dokumentationsregressionen. Lint, strikter MkDocs-Bau und
Whitespacepruefung bestehen. Das ist keine vollstaendige Repository-
Testsuite und keine weitere AL1-Rechnung.

**Was erreicht ist:** Eine ausgefuehrte, endliche raeumlich gekoppelte
Dreiquark-Referenz mit gemeinsam berechneter Energie, Groesse und
magnetischer Antwort, inklusive offenem Fehlvergleich. Das ist mehr als
die vorherige reine Zustandsalgebra.

**Was nicht erreicht ist:** Keine Herleitung aus Memory; keine
vollstaendige QCD, physikalisch kontrollierte Protonpraezision,
Confinement-Herleitung, Neutron-Massendifferenz, Delta-Zerfallsbreite,
Elektronenrechnung oder Wasserstoffspektrallinie. Quarkmassen,
Quantenzahlen, Quantenmechanik, Confinement und Energieoffset sind Inputs.
Insbesondere bleibt die absolute Masse eine geerbte Modellreproduktions-
groesse, keine unabhaengige emergente Massenvorhersage.

Das Panel ist abgeschlossen. Weitere Ziellaeufe, Basisvergroesserungen,
Nachanpassungen oder ein relativistischer Ersatz sind nicht mitgenehmigt.
Die weitere Arbeitsreihenfolge steht nur in den
[Projektprioritaeten](../../docs/status/project_priorities.md).
