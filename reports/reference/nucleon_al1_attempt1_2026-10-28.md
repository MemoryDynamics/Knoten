# AL1-Referenz, Versuch 1: Freigabe und Ergebnisprotokoll

Stand vor Start: 2026-10-28, 22:41 UTC. Status: **genehmigt, noch nicht gestartet**.

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
Kein Prozess wurde zum Zeitpunkt dieses Vorabprotokolls gestartet.

## Ergebnis

Wird nach dem einmaligen Panel ergaenzt. Keine vorweggenommene
Konvergenz-, Teilchen- oder Emergenzaussage.
