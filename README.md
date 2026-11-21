# terminal-themes

Drei Farbprofile für das **macOS Terminal.app** – zwei helle Cremetöne und ein dunkles Olivgrün. Alle drei teilen dieselben Einstellungen: Cascadia Mono SemiLight, 16 pt, Fenster 97×25, 96 % Deckkraft, kein Fettdruck.

## Themes

| Name | Hintergrund | Text | Kontrast Text/Hintergrund |
|---|---|---|---|
| **Cornsilk** | `#FFF8DC` | `#000000` | 19,7 : 1 |
| **Moccasin** | `#FFE4B5` | `#000000` | 17,0 : 1 |
| **Dunkelgruen** | `#1A1F14` | `#DCD9C6` | 11,8 : 1 |

Die hellen Profile (Cornsilk, Moccasin) nutzen eine abgedunkelte, gesättigte Palette; die ANSI-Farben haben auf dem Hintergrund mindestens etwa 5 : 1 Kontrast. Dunkelgruen verwendet eine helle Palette im Stil von GitHub Dark.

## Installation

1. Die gewünschte Datei aus `themes/` per Doppelklick öffnen. Terminal importiert sie als Profil.
2. In *Terminal → Einstellungen → Profile* das Profil auswählen und unten auf **Standard** setzen.
3. Ein altes Profil mit gleichem Namen vorher löschen, sonst entsteht ein Duplikat.

Oder per Kommandozeile:

```sh
open themes/Cornsilk.terminal
```

## Schrift

Die Profile verwenden **Cascadia Mono SemiLight** (PostScript-Name `CascadiaMono-SemiLight`). Ist die Schrift nicht installiert, nimmt Terminal eine Ersatzschrift. Installation z. B. mit Homebrew:

```sh
brew install --cask font-cascadia-mono
```

Alternativ in *Profile → Text → Schrift* eine andere Schrift wählen.

## Profile selbst erzeugen

`tools/generate.py` schreibt die `.terminal`-Dateien neu (nur Python 3, keine Abhängigkeiten):

```sh
python3 tools/generate.py
```

Farben, Schrift, Fenstergröße und Deckkraft stehen oben im Skript und lassen sich dort ändern. Neue Themes entstehen durch einen weiteren Eintrag in `THEMES`.

## Hinweise

- Die Deckkraft (96 %) wird als Alphawert der Hintergrundfarbe gespeichert. Ob sie nach dem Import stimmt, zeigt *Profile → Fenster → Hintergrund*.
- „Fette Schrift verwenden" und „Helle Farben für fetten Text" sind ausgeschaltet; fetter Text hat dieselbe Farbe wie normaler Text.

## Herkunft

Die Palette der hellen Themes ist von GitHub Light High Contrast, die von Dunkelgruen von GitHub Dark ([Primer](https://github.com/primer/github-vscode-theme), MIT) inspiriert, die Werte wurden aber angepasst.

## Lizenz

MIT, siehe [LICENSE](LICENSE).
