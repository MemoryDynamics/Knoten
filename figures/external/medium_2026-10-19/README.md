# Images for the Medium essay

Date: 2026-10-19. Article: [Ein Traum von Knoten](https://medium.com/@haukeh/ein-traum-von-knoten-9232412d4ff8).

## Dream illustration

`dream_flight_memory_hero.png` is a conceptual illustration generated with
the built-in image-generation tool. It illustrates the author's dream;
it is not simulation output, a topological construction, or scientific evidence.
The original generated image was copied without visual modification.

German caption: *Eine Flugbahn, die sich in ihrer eigenen Vergangenheit
verfängt. KI-generierte Illustration zur Traumerinnerung.*

English caption: *A flight path caught in its own past. AI-generated
illustration of the dream recollection.*

Generation prompt, verbatim:

```text
Use case: illustration-story. Asset type: wide editorial cover image for a personal Medium essay called 'A Dream of Knots', about Memory Dynamics. Create an evocative, sophisticated artwork of one continuous fine filament tracing a flight path through a quiet, spacious, deep indigo atmosphere. The filament makes broad free curves, becomes caught in its own path in a dense but beautiful intricate knot, then emerges into another open curve. Faint, fading echoes of the same path suggest memory. Make the path feel weightless and dreamlike; the knot should be tangible and spatial, not a flat scribble. Warm copper and pale golden light on the filament, subtle silver-blue traces, restrained painterly grain and soft depth. Elegant contemporary magazine illustration with a sculptural, handmade quality, no glossy generic sci-fi look. Wide landscape composition around 16:9; the knot and the two open curves must read well at thumbnail size and within a central crop. No text, no letters, no logo, no equations, no people, no stars, no brains, no particles or scientific diagram. This is a poetic conceptual illustration of a dream, not a depiction of experimental results. Opaque background.
```

## Historical trajectory figure

`fig3_knot_trajectory_historical.png` is a raster rendering of the tracked
PDF `figures/paper/fig3_knot_trajectory.pdf`, at a maximum edge of 2400 pixels.
The original page, plotted data, title, axes, and color scale are preserved.
No new simulation was run and no scientific image generation was used.

Conversion command:

```powershell
pdftoppm -singlefile -scale-to 2400 -png figures/paper/fig3_knot_trajectory.pdf figures/external/medium_2026-10-19/fig3_knot_trajectory_historical
```

The original PDF is a historical communication example. The publication
decision in `paper/paper_i/manuscript/README.md` explicitly excludes it from
current Paper-I evidence. Two historical scripts,
`experiments/current/knot_stability/Knoten3D.py` and `Knoten3D_prism.py`,
contain a producer for the same basename but use different memory rules.
The precise generating revision of this PDF was not independently verified;
the existing tracked PDF is the source of this rendering. Do not infer
current model parameters, topological knot transitions, formation, physical
particles, or the current rotating-wave stability result from this image.

German caption: *Eine frühe Modellsimulation: Die Linie verbindet
aufeinanderfolgende Positionen, die Farbe läuft von frühen (violett) zu
späten Schritten (gelb). Die Verdichtungen machen die Idee anschaulich;
diese historische Grafik ist kein aktueller Stabilitäts- oder Teilchennachweis.*

English caption: *An early model simulation: the line joins successive
positions, and the color runs from early (purple) to late steps (yellow).
The clusters illustrate the idea; this historical figure does not establish
the current stability result or physical particles.*
