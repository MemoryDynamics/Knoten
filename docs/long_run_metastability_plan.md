# Long-Run Metastability Plan

Stand: 2026-06-29.

## Zweck

Diese Kampagne prueft die empirische Aussage, dass metastabile Knoten erst in
langen Laeufen, typischerweise bei `n > 10^7`, verlaesslich sichtbar werden.
Sie ist keine Voraussetzung fuer die strukturellen Aussagen von Paper 0.
Sie ist aber zentral fuer Paper I, sobald dort robuste Knotenexistenz oder
lange Verweildauern als numerischer Befund gezeigt werden sollen.

## Aktuelle Leitentscheidung

Paper 0 wird als mathematischer Anker bzw. moegliches Supplement eingefroren:
Modell, exponentielles Gedaechtnis, Markov-Einbettung, kontraktive
Gedaechtnisfaser und Diagnose-Rahmen. Die Long-Run-Kampagne laeuft daneben,
damit Paper I spaeter nicht auf Kurzlaufbildern oder Einzelfiguren ruht.

## Kanonischer Entry-Point

```powershell
python experiments/long_run_metastability.py `
  --steps 10000000 `
  --seeds 1 `
  --conditions baseline `
  --dim 3 `
  --alpha 0.01 `
  --sample-every 1000 `
  --burn-in 1000000 `
  --max-memory 800 `
  --output-dir data/processed/long_run_metastability/2026-06-29_initial
```

Das Script nutzt eine Numba-beschleunigte zirkulaere Speicherimplementierung
der normierten Konvention `beta=lambda_m=alpha`. Es schreibt pro Fall eine
Case-JSON und am Ende eine `summary.json` in das Ausgabeverzeichnis.

## Diagnostik

Pro Fall werden mindestens ausgewertet:

- Anzahl gespeicherter Samples und Sample-Abstand in Updates;
- `alpha^{-1}` als Speicherpersistenz in Updates;
- Residence-Statistik fuer mehrere Voxelgroessen;
- maximale Residence-Zeit in Einheiten von `alpha^{-1}`;
- Kovarianz- und Occupancy-Dimension als Nebenbefunde;
- grobe Vektor-Autokorrelation der sichtbaren Samples;
- Laufzeit und effektive Steps pro Sekunde.

Ein Kandidat fuer langlebige Metastabilitaet liegt erst vor, wenn die maximale
Residence-Zeit ueber mehrere Speicherzeiten reicht. Der aktuelle Startwert
verwendet `10 * alpha^{-1}` als konservative Schwelle.

## Kontrollen

Phase 1 startet bewusst klein:

1. `baseline`, ein Seed, `n=10^7`.
2. Danach gleiche Parameter mit `eta_zero`.
3. Danach `single_scale` mit deaktiviertem attraktivem Anteil.
4. Danach mehrere Seeds und ggf. `n=3*10^7` oder groesser.

Die Reihenfolge verhindert, dass lange Hintergrundlaeufe die Paper-Arbeit
blockieren, liefert aber frueh eine reale Laufzeit- und Skalenmessung.

## Akzeptanzkriterien fuer Paper I

Ein Paper-I-Befund sollte erst aufgenommen werden, wenn mindestens vorliegt:

- gleiche Parameter ueber mehrere Seeds;
- klare Trennung gegen `eta_zero` und `single_scale`;
- Residence-Ratios stabil gegen Voxelgroesse;
- Laufparameter, Git-Revision, Seeds, Burn-in und Sampling im JSON;
- kein Claim auf physikalische Masse, Teilchenidentitaet, `d=3`-Selektion oder
  Lorentzkinematik aus diesen Laeufen.

## Nicht-Claims

Diese Kampagne beweist keine Existenz metastabiler Mengen im mathematischen
Sinn. Sie misst numerische Kandidaten. Die Uebersetzung in
Transferoperator-Slow-Modes, PCCA/HMM oder robuste Markov-State-Models bleibt
der naechste Ausbauschritt nach den ersten Long-Run-Ergebnissen.
