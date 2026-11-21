# terminal-themes

Farbprofile für das **macOS Terminal.app** mit passender Shell-Konfiguration: vier Themes, eine `dircolors`-Datei für farbiges `ls` und eine `.bashrc` mit vi-Modus, Git-Prompt und History-Einstellungen.

Alle Profile teilen dieselben Einstellungen: Cascadia Mono SemiLight, 16 pt, Fenster 97×25, 96 % Deckkraft, kein Fettdruck.

## Inhalt

```
terminal-themes/
├── themes/              Terminal.app-Profile (.terminal)
├── dotfiles/            bash_profile, bashrc, dircolors
├── tools/generate.py    erzeugt die Profile neu
├── install-dotfiles.sh  installiert die Dotfiles nach ~
├── README.md
└── LICENSE
```

## Themes

| Name | Hintergrund | Text | Kontrast Text/Hintergrund |
|---|---|---|---|
| **Cornsilk** | `#FFF8DC` | `#000000` | 19,7 : 1 |
| **Moccasin** | `#FFE4B5` | `#000000` | 17,0 : 1 |
| **Dunkelgruen** | `#42483F` | `#DCD9C6` | 6,6 : 1 |
| **Kaffee** | `#322416` | `#DCD9C6` | 10,6 : 1 |
| **Backstein** | `#702E22` | `#DCD9C6` | 7,0 : 1 |

Die hellen Profile (Cornsilk, Moccasin) nutzen eine abgedunkelte, gesättigte Palette: Die normalen ANSI-Farben haben etwa 6 : 1 bis 10 : 1 Kontrast, die hellen Varianten sind deutlich kräftiger, aber noch mit mindestens 4,5 : 1.

Dunkelgruen, Kaffee und Backstein verwenden helle Paletten im Stil von GitHub Dark. Die normalen Farben sind dabei bewusst dunkler als die hellen Varianten (Abstand ΔE meist etwa 20 oder mehr), damit sich beide in `ls` und anderen Tools klar unterscheiden. Kaffee und Backstein haben dunklere Hintergründe und daher die etwas dunkleren Farben; Dunkelgruen hat einen helleren Hintergrund und deshalb hellere Farben.

### Installation der Profile

1. Die gewünschte Datei aus `themes/` per Doppelklick öffnen. Terminal importiert sie als Profil.
2. In *Terminal → Einstellungen → Profile* das Profil auswählen und unten auf **Standard** setzen.
3. Ein altes Profil mit gleichem Namen vorher löschen, sonst entsteht ein Duplikat.

```sh
open themes/Cornsilk.terminal
```

### Schrift

Die Profile verwenden **Cascadia Mono SemiLight** (PostScript-Name `CascadiaMono-SemiLight`). Ist die Schrift nicht installiert, nimmt Terminal eine Ersatzschrift:

```sh
brew install --cask font-cascadia-mono
```

Alternativ in *Profile → Text → Schrift* eine andere Schrift wählen.

## Dotfiles und farbiges ls

```sh
./install-dotfiles.sh
```

Das Skript kopiert `dotfiles/bash_profile`, `dotfiles/bashrc` und `dotfiles/dircolors` nach `~/.bash_profile`, `~/.bashrc` und `~/.dircolors`. Bestehende Dateien werden vorher nach `~/.terminal-themes-backup/<Datum>` gesichert. Danach ein neues Terminal-Fenster öffnen.

Die `.bashrc` bringt mit: vi-Modus auf der Kommandozeile, Prompt `user@host:pfad (branch) $` (das `$` wird rot bei Fehlern), große History ohne Duplikate sowie nützliche Aliase.

### dircolors

`ls` mit Farben nach Dateityp, Rechten und Endung braucht GNU-`ls`:

```sh
brew install coreutils
```

Die `.bashrc` aktiviert GNU-`ls` und lädt `~/.dircolors` automatisch, sobald `coreutils` installiert ist. Ohne `coreutils` gelten weiter die einfachen Farben der macOS-`ls`.

Die `dircolors` verwendet nur Vordergrundfarben, ohne Fettdruck und Hintergründe. Die Farben kommen aus der ANSI-Palette des jeweiligen Profils:

| Merkmal | Code | Slot |
|---|---|---|
| Verzeichnis | `34` | blau |
| Symlink | `36` | cyan |
| kaputter Symlink | `31` | rot |
| ausführbare Datei | `32` | grün |
| Pipe | `33` | gelb |
| Socket | `35` | magenta |
| Block-/Char-Device | `37` | weiß |
| setuid | `91` | helles Rot |
| setgid | `95` | helles Magenta |
| Sticky-Verzeichnis | `94` | helles Blau |
| Verzeichnis für alle schreibbar | `93` | helles Gelb |
| Sticky und für alle schreibbar (`/tmp`) | `92` | helles Grün |
| Archive (`.zip`, `.tar`, `.gz` …) | `31` | rot |
| Bilder und Video | `35` | magenta |
| Audio | `00;36` | cyan |
| Backup, temporär (`.bak`, `.tmp`, `~`) | `00;90` | helles Schwarz |

Eigene Anpassungen gehören in `dotfiles/dircolors` (Format wie bei `dircolors -p`).

## Profile selbst erzeugen

`tools/generate.py` schreibt die `.terminal`-Dateien neu (nur Python 3, keine Abhängigkeiten):

```sh
python3 tools/generate.py
```

Farben, Schrift, Fenstergröße und Deckkraft stehen oben im Skript. Neue Themes entstehen durch einen weiteren Eintrag in `THEMES`.

## Hinweise

- Die Deckkraft (96 %) wird als Alphawert der Hintergrundfarbe gespeichert. Ob sie nach dem Import stimmt, zeigt *Profile → Fenster → Hintergrund*.
- „Fette Schrift verwenden" und „Helle Farben für fetten Text" sind ausgeschaltet; fetter Text hat dieselbe Farbe wie normaler Text.
- Bei Deckkraft unter 100 % wirkt der Hintergrund je nach Fensterinhalt dahinter minimal anders als der Hexwert.

## Herkunft

Die Palette der hellen Themes ist von GitHub Light High Contrast, die der dunklen von GitHub Dark ([Primer](https://github.com/primer/github-vscode-theme), MIT) inspiriert, die Werte wurden aber angepasst.

## Lizenz

MIT, siehe [LICENSE](LICENSE).
