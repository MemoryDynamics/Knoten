# Paper I Patch Report

Datum: 2026-06-01

## Relevante Dateien

- `docs/EmergenteRaumzeit/1.tex`
- `docs/EmergenteRaumzeit/references.bib`
- `docs/EmergenteRaumzeit/1.pdf`
- `reports/paper1_source_audit_2026-06-01.md`

## Aktueller Status

- `1.tex` ist lesbar und Teil des Workspace.
- Der bestehende Audit-Report dokumentiert bereits einen korrigierten Ausdruck für die Memory-Potential-Definition.
- Die Paper-Quelle ist ein 9-seitiges `revtex4-2`-Dokument mit klarem Abstract, Motivationsabschnitt und Modellbeschreibung.
- Ein sauberer Build mit `xelatex`/`bibtex` wurde offenbar vorbereitet; es gibt noch Underfull-Hbox-Warnungen, aber keine offenkundigen LaTeX-Fehler.

## Wichtige Befunde

1. **Memory-Potential-Formel**
   - Die Notation `\int_\Omega K(x,y)\,\rho_n(y)\,dy` ist korrekt und kann in einer kompakten Darstellungsweise auch als `\int dy\,\Omega K(x,y)\,\rho_n(y)` verstanden werden.
   - Wichtig ist, dass die Darstellung in `1.tex` klar bleibt und keine Verwirrung über die Rolle des Integrationsmaßes entsteht.

2. **Gradienten und Koordinatenstruktur**
   - Die Notation `\nabla\Phi_n` ist in Ordnung, muss aber klar als "effektive, koordinatenabhängige Beschreibung" formuliert werden.
   - Vorschlag: Eine kurze Klarstellung hinzufügen, dass `\Omega` hier als wirksamer Zustandstraum mit Referenzmaß benutzt wird, nicht als postulierte physikalische Metrik.

3. **Emergente Zeit**
   - Die Definition `t = \alpha n` ist gut, muss aber stärker als "Hilfsparametrisierung auf der Gedächtnis-Persistenzskala" betont werden.
   - Wichtig: in Textpassagen deutlich machen, dass `t` nicht als fundamentale physikalische Zeit eingeführt wird.

4. **"Mass" als Betriebsgröße**
   - Der Begriff wird gut als Relaxations-Proxy genutzt. Er sollte aber in einer Fußnote oder einem Absatz nochmals ausdrücklich als operationaler Begriff und nicht als physikalische Masse erklärt werden.

5. **Diagnostik und Messbarkeit**
   - Es fehlen präzise Rekonstruktionen, wie `\Gamma_{\mathrm{rel}}`, `D`, `\widehat{\Gamma}`, und `M_n(\mathcal{K})` aus Simulationsdaten gemessen werden.
   - Vorschlag: Eine kurze "Operational Diagnostics"-Box mit den jeweiligen Messrezepten einfügen.

6. **Begrenzte Kontinuumsannahme**
   - Der Abschnitt zur quasi-stationären OU-Approximation ist sinnvoll, sollte aber klar als Approximation unter der Annahme einer klaren Skalenhierarchie markiert werden.

7. **Formale Klarheit bei Metastabilität**
   - Begriffe wie "dynamische Knoten" und "Metastabilität" sind aktuell eher konzeptionell als formal definiert.
   - Vorschlag: Eine präzisere Definition von `M_n(\mathcal{K})` und einem entsprechenden Schwellwert- oder Vergleichs-Kriterium ergänzen.

## Empfohlene Patch-Schritte

- [ ] `1.tex` um einen kurzen Präzisierungstext ergänzen: "`\nabla` and Hessian notation refer to an effective coordinate structure on `\Omega`, not to a fundamental spacetime metric."
- [ ] In der Einleitung oder im Abschnitt "Emergent time" einen Satz ergänzen: "The parameter `t=\alpha n` is a coarse-grained update parameter tied to the model's internal memory persistence scale."
- [ ] Eine kleine "Operational Diagnostics"-Box einfügen, z. B.:
  - `\alpha` via exponential decay of memory kernel weights
  - `D \sim \varepsilon^2/(2\alpha)` from noise scaling
  - `\Gamma_{\mathrm{rel}}` from in-knot autocorrelation decay
  - `\widehat{\Gamma} = (\sigma^2/D)\,\Gamma_{\mathrm{rel}}`
- [ ] Einen Absatz zur Interpretation von "mass" als Relaxations- oder Konfinierungsproxy hinzufügen.
- [ ] Die Diskussion um Erwartungen aus dem Kontinuums-Limit stärker als "deferred to future work" markieren.

## Priorität für Olaf

- Schnellster Gewinn: Klarstellung von `t=\alpha n` und `\nabla` als effektive Beschreibung.
- Mittelfristig wichtig: Operationalisierung der Knotendiagnostik und der Relaxationsmasse.
- Optional, wenn Zeit bleibt: Text zur möglichen Limes-Interpretation und zur physikalischen Kalibrierung von `D`/`\Gamma` konsolidieren.
- Für Olaf direkt als nächste Maßnahme: kurze Anfrage für einen Folgetermin zur Diskussion der konzeptionellen Richtung.

## Vorschlag

Ich kann nun direkt einen Patch-Entwurf in `docs/EmergenteRaumzeit/1.tex` einfügen oder weiterhin nur Vorschläge im Bericht liefern. Falls Du möchtest, mache ich die Änderungen in der aktuellen Workspace-Version des Papers gleich selbst.
