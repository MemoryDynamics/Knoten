# Kindle Reader Pack

Dieser Ordner enthaelt Kindle-freundliche PDF-Fassungen der aktuellen Paper.
Der wissenschaftliche Text wird nicht umgeschrieben; das Build-Skript passt nur
Seitenformat, Raender, Zeilenabstand, Abbildungszugriff und Ueberschriften fuer
ein e-ink-Display an.

## Dateien

- `paper_0_kindle.pdf`: mathematisches Anchor-Paper.
- `paper_i_long_kindle.pdf`: volle Paper-I-Fassung.
- `paper_i_compact_kindle.pdf`: kompakte Paper-I-Fassung.
- `paper_ii_kindle.pdf`: Paper-II-Entwurf.
- `build_kindle_pdfs.ps1`: reproduziert die Kindle-PDFs aus den LaTeX-Quellen.

## Rebuild

Aus dem Repository-Root:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\paper\kindle\build_kindle_pdfs.ps1
```

## Auf den Kindle bringen

Der eleganteste Weg ist Amazons Web-Upload:

```text
https://www.amazon.com/sendtokindle
```

Dort die gewuenschten `*_kindle.pdf`-Dateien hochladen. Danach den Kindle per
WLAN synchronisieren; die Dateien erscheinen als persoenliche Dokumente in der
Bibliothek.

Falls Amazon auf eine regionale Domain weiterleitet, einfach diese regionale
Send-to-Kindle-Seite verwenden.