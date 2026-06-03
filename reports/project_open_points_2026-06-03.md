# Offene Punkte und Entscheidungen

Datum: 2026-06-03

## 1. Reproduzierbare Kernfragen

- Einen kanonischen Referenzlauf für die behauptete Dimensionsmessung `D_occ ≈ 2.8` definieren.
- Sicherstellen, welche Simulationsparameter (alpha, memory_factor, burn_in, sample_every) für die wichtigsten Aussagen zu verwenden sind.
- Prüfen, ob die Ergebnisse gegen zufällige Kontrollen und alternative Dimensionstests robust sind.

## 2. Projektstruktur und Migration

- Klarheit schaffen, welche historischen `experiments/*`-Skripte in die modulare Bibliothek übernommen werden sollen.
- Einheitliche Speicherung der Ergebnisse in `data/processed/` definieren.
- Eine zentrale Pipeline für das Exportformat `.npz` / `.json` und zugehörige Visualisierungen etablieren.

## 3. Dokumentation und Übergabe

- Einen klaren Review-Workflow mit Olaf abstimmen: Code, Daten, Paper-Claims.
- Die bestehenden Audit-Reports (`reports/paper1_delivery_package_2026-06-01.md`) als Grundlage nutzen.
- Zusätzliche Entscheidungsdokumente erstellen, falls Olaf Varianten-Tests oder Risikobewertungen verlangt.

## 4. Technische Details

- `numba` ist installiert, aber die Bibliothek ist nicht zwingend; der Code sollte daher weiterhin ohne Numba laufen.
- Versionssperren für Abhängigkeiten sind jetzt dokumentiert in `requirements.txt` und `requirements-dev.txt`.
- Es gibt derzeit kein eigenes CI/Workflow-Setup im Repository.
