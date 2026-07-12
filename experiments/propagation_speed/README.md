# Propagation Speed

Skripte fuer die Analyse von Light-Cone-Struktur, retardierten Effekten und
propagation speed. Diese Dateien sind eng mit dem Paper-II-Thema verbunden.

Wichtige Dateien:

- `PaperII3D_4Plots.py`, `PaperII3D_5Plots*.py`: historische Plot-Skripte fuer Paper II.
- `ballistic_kernel_probe.py`: negativer Kontrollpfad fuer skalare Ballistik-/Photon-Analogien.

Ziel: Neue Reproduktionen sollten Daten aus `data/raw/` generieren und in
`data/processed/` ablegen.

## Theoretical Mapping

Siehe [docs/reference/THEORETICAL_CONTEXT.md](../../docs/reference/THEORETICAL_CONTEXT.md). Dieser
Ordner testet direkt Aussagen zur "Emergence of space & kinematics" und zur
operationalen Lichtkegel-Definition, etwa emergentes `c` oder Time-of-Flight.

## Ballistische MSD-/Autokorrelationsprobe

Ein erster, kleiner Experimentpfad fuer den analytisch motivierten Ballistik-Test
liegt in [ballistic_kernel_probe.py](ballistic_kernel_probe.py). Er startet mit
einem ein-skalierten Gaussian-Memory-Kernel und misst:

- `C_u(k)` ueber Vektorautokorrelationen des Schritts `u_n = x_{n+1} - x_n`;
- `MSD(k) = <|x_{n+k} - x_n|^2>`;
- einen log-log-Slope fuer das MSD-Fenster.

Die Auswertung ist bewusst konservativ: Ballistik wird nur dann als Hinweis
gewertet, wenn ein echtes Skalenfenster mit Slope nahe `2` sichtbar wird. Der
korrigierte Ein-Kernel-Pilot vom 2026-07-07 bleibt negativ: maximaler MSD-Slope
etwa `1.138`, also keine photonartige Ballistik im skalaren overdamped Modell.