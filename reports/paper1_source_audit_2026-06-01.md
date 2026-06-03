# Paper I Source Audit

Datum: 2026-06-01.

Quelle beim ersten Audit:

- `C:\Users\Hauke\Documents\Hobby\Weltformel\EmergenteRaumzeit\1.tex`
- `C:\Users\Hauke\Documents\Hobby\Weltformel\EmergenteRaumzeit\1.pdf`
- `C:\Users\Hauke\Documents\Hobby\Weltformel\EmergenteRaumzeit\references.bib`

Aktuelle Workspace-Quelle:

- `C:\Users\Hauke\Documents\Emergenz_Knoten\docs\EmergenteRaumzeit\1.tex`
- `C:\Users\Hauke\Documents\Emergenz_Knoten\docs\EmergenteRaumzeit\references.bib`

## Status

- Titel: `Minimal Point-Process Dynamics with Memory: Emergent Time and Metastable Structures`
- Format: `revtex4-2`, PRD-like.
- PDF: 9 Seiten, erzeugt am 2026-06-01 15:44:52.
- Paper-Fokus: Minimalmodell, irreversible Memory-Dynamik, emergente Zeit,
  dynamische Knoten, mass-like Relaxationsskala.

## Struktur

- Introduction
- Minimalist motivation: from directed updates to effective geometry
- Minimal Dynamical Model
- Irreversible Memory and Emergent Time
- Emergence of Mass and Dynamical Knots
- Discussion and Outlook

## Gute Punkte

- Der Abstract ist vorsichtig und paperfaehig formuliert.
- Die Nicht-Annahmen werden explizit benannt.
- `Omega` bleibt klar ein abstrakter Zustandsraum.
- Masse wird als operationaler Proxy statt als fertige physikalische
  Identifikation formuliert.
- Der Text verschiebt Relativitaet, Standardmodell und Kalibrierung in
  Companion Work, was Paper I stabiler macht.

## Konkrete technische Befunde

### 1. Formel fuer Memory Potential sah fehlerhaft gesetzt aus

Vor dem Fix stand in `1.tex`:

```tex
\Phi_n(x) := \int_ dy\,\Omega K(x,y)\,\rho_n(y),
```

Das ist sehr wahrscheinlich ein Satzfehler. Gemeint ist vermutlich:

```tex
\Phi_n(x) := \int_\Omega K(x,y)\,\rho_n(y)\,dy.
```

Diese Korrektur sollte direkt in Paper I gemacht werden, sobald Schreibzugriff
auf den Paper-Ordner freigegeben ist.

Status 2026-06-01: im Workspace korrigiert zu:

```tex
\Phi_n(x) := \int_\Omega K(x,y)\,\rho_n(y)\,dy.
```

### 2. LaTeX-Log zeigt undefinierte Zitate

`1.log` enthaelt viele `Package natbib Warning: Citation ... undefined`.
Das kann schlicht bedeuten, dass nach dem letzten Edit kein kompletter
Build-Zyklus `xelatex -> bibtex -> xelatex -> xelatex` gelaufen ist.

Vor einem inhaltlichen Review sollte der Build einmal sauber durchlaufen.

Status 2026-06-01 nach Workspace-Build:

- `bibtex 1.aux`: erfolgreich
- `xelatex -interaction=nonstopmode -halt-on-error 1.tex`: erfolgreich
- zweiter `xelatex`-Lauf: erfolgreich
- keine undefinierten Zitate mehr
- keine Overfull-Hbox-Warnungen
- verbleibend: vier Underfull-Hbox-Warnungen in Zeilenbereichen 219--222,
  389--391, 440--441 und 511--514
- Output: `docs/EmergenteRaumzeit/1.pdf`, 9 Seiten

### 3. Build/Edition ausserhalb Workspace

Der Paper-Ordner liegt ausserhalb des aktuellen schreibbaren Workspaces. Ich
kann ihn lesen und auditieren, aber direkte Aenderungen oder ein Build, der
Artefakte dort schreibt, brauchen Freigabe.

## Wissenschaftliche Naechstpunkte fuer Paper I

- Die verwendeten Diagnostiken sollten jeweils auf eine konkrete
  Referenzimplementierung im Repo zeigen.
- Fuer `Gamma_rel`, `D`, `widehat{Gamma}` und Residence sollte es eine
  klare "how measured from trajectory" Box oder Appendix-Notiz geben.
- Die OU-Linearisierung sollte explizit als quasi-stationaere frozen-memory
  Approximation markiert bleiben.
- Der Begriff "mass" ist gut abgesichert, solange er strikt als
  relaxation/stability proxy gelesen wird.
