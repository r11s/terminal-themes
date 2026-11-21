#!/usr/bin/env python3
"""Erzeugt die Terminal.app-Profile (.terminal) im Ordner ../themes
und die Farbtabelle der dircolors als docs/dircolors.svg.

Nur Python 3 (Standardbibliothek), läuft auf macOS und Linux:
    python3 tools/generate.py
"""
import plistlib
from pathlib import Path
from plistlib import UID

# ---------- gemeinsame Einstellungen ----------
FONT_NAME = "CascadiaMono-SemiLight"   # PostScript-Name der Schrift
FONT_SIZE = 16
COLUMNS, ROWS = 97, 25
OPACITY = 0.96                         # Deckkraft des Hintergrunds

ANSI_NAMES = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]

# ---------- Paletten ----------
LIGHT_ANSI = ["#1a1a1a", "#a00000", "#005a14", "#6b3a00",
              "#0033a8", "#6a0dad", "#00565f", "#44484f"]
LIGHT_BRIGHT = ["#5a6068", "#c4140a", "#0a7512", "#a24d00",
                "#1a56d6", "#b01c92", "#0a7088", "#626870"]

THEMES = {
    "Cornsilk": dict(
        bg="#fff8dc", fg="#000000", bold="#000000", cursor="#0033a8", selection="#b3d3f5",
        ansi=LIGHT_ANSI, bright=LIGHT_BRIGHT),
    "Moccasin": dict(
        bg="#ffe4b5", fg="#000000", bold="#000000", cursor="#0033a8", selection="#b3d3f5",
        ansi=LIGHT_ANSI, bright=LIGHT_BRIGHT),
    "Dunkelgruen": dict(
        bg="#42483f", fg="#dcd9c6", bold="#dcd9c6", cursor="#f0f6fc", selection="#566252",
        ansi=["#8a968f", "#eea09e", "#51cb68", "#e9aa0e",
              "#8fb8e8", "#c3a8e5", "#24c6d1", "#bac2cb"],
        bright=["#afb7b2", "#ffd2ce", "#adeab4", "#f1d9a0",
                "#bee0ff", "#e8d3ff", "#a2e8ed", "#f0f6fc"]),
    "Kaffee": dict(
        bg="#322416", fg="#dcd9c6", bold="#dcd9c6", cursor="#f0f6fc", selection="#58442f",
        ansi=["#7a8780", "#eb8d8a", "#39bf52", "#d69c0d",
              "#78a9e3", "#b898e0", "#21b8c2", "#b1bac4"],
        bright=["#9fa8a2", "#ffc6c1", "#9be5a3", "#eed08a",
                "#acd8ff", "#e3c9ff", "#8be2e8", "#f0f6fc"]),
    "Backstein": dict(
        bg="#702e22", fg="#dcd9c6", bold="#dcd9c6", cursor="#f0f6fc", selection="#83493c",
        ansi=["#85918a", "#ed9998", "#43c75c", "#e2a50d",
              "#86b2e6", "#bfa2e3", "#22c0cb", "#b4bdc6"],
        bright=["#a8b1ab", "#ffc8c4", "#9fe6a7", "#efd391",
                "#b1daff", "#e4ccff", "#8fe3e9", "#f0f6fc"]),
}


# ---------- Archivierung wie macOS (NSKeyedArchiver) ----------
def _archive(objects):
    return plistlib.dumps(
        {"$archiver": "NSKeyedArchiver", "$version": 100000,
         "$top": {"root": UID(1)}, "$objects": ["$null"] + objects},
        fmt=plistlib.FMT_BINARY)


def color(hex_color, alpha=None):
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    rgb = "%.6f %.6f %.6f" % (r, g, b)
    if alpha is not None:
        rgb += " %.2f" % alpha
    return _archive([
        {"$class": UID(2), "NSColorSpace": 1, "NSRGB": rgb.encode() + b"\x00"},
        {"$classes": ["NSColor", "NSObject"], "$classname": "NSColor"}])


def font(name, size):
    return _archive([
        {"$class": UID(3), "NSName": UID(2), "NSSize": float(size), "NSfFlags": 16},
        name,
        {"$classes": ["NSFont", "NSObject"], "$classname": "NSFont"}])


def build(name, t):
    p = {
        "name": name, "type": "Window Settings", "ProfileCurrentVersion": 2.07,
        "BackgroundColor": color(t["bg"], OPACITY),
        "TextColor": color(t["fg"]), "TextBoldColor": color(t["bold"]),
        "CursorColor": color(t["cursor"]), "SelectionColor": color(t["selection"]),
        "Font": font(FONT_NAME, FONT_SIZE), "FontAntialias": True,
        "UseBoldFonts": False, "UseBrightBold": False,
        "columnCount": COLUMNS, "rowCount": ROWS,
        "CursorType": 0, "shellExitAction": 1,
        "BackgroundBlur": 0.0, "BackgroundAlphaInactiveWindows": 1.0,
    }
    for i, n in enumerate(ANSI_NAMES):
        p["ANSI%sColor" % n] = color(t["ansi"][i])
        p["ANSIBright%sColor" % n] = color(t["bright"][i])
    return p


# ---------- Farbtabelle der dircolors als Bild (docs/dircolors.svg) ----------
# (Beschriftung, Beispieldatei, Farbcode aus dotfiles/dircolors)
DIRCOLOR_ROWS = [
    ("Typen", None, None),
    ("Verzeichnis", "Documents", "34"),
    ("Symlink", "link", "36"),
    ("Kaputter Symlink", "kaputt", "31"),
    ("Ausführbare Datei", "prog.sh", "32"),
    ("Pipe", "pipe", "33"),
    ("Socket", "socket", "35"),
    ("Block-/Char-Device", "disk0", "37"),
    ("Sonderrechte", None, None),
    ("setuid", "setuid", "91"),
    ("setgid", "setgid", "95"),
    ("Sticky-Verzeichnis", "sticky", "94"),
    ("Verzeichnis für alle schreibbar", "ow", "93"),
    ("Sticky und für alle schreibbar (/tmp)", "tmp", "92"),
    ("Endungen", None, None),
    ("Archive (.zip .tar .gz .7z .deb)", "backup.zip", "31"),
    ("Bilder, Video (.jpg .png .mp4 .mkv)", "foto.jpg", "35"),
    ("Audio (.mp3 .flac .wav)", "song.mp3", "00;36"),
    ("Backup, temporär (.bak .tmp .swp ~)", "notiz.bak", "00;90"),
    ("Alles andere", None, None),
    ("Normale Datei", "notiz.txt", None),
]


def _slot_color(theme, code):
    """Farbe für einen ANSI-Code (30-37 normal, 90-97 hell) aus der Palette des Themes."""
    if code is None:
        return theme["fg"]
    n = int(code.split(";")[-1])
    return theme["ansi"][n - 30] if n < 90 else theme["bright"][n - 90]


def build_dircolors_svg():
    from xml.sax.saxutils import escape
    names = list(THEMES)
    x_label, x_code, x_cells, cell_w, row_h = 8, 262, 322, 118, 26
    width = x_cells + cell_w * len(names) + 8
    y = 30
    parts = []
    for i, n in enumerate(names):
        parts.append('<text x="%d" y="20" class="h">%s</text>' % (x_cells + i * cell_w + 8, escape(n)))
    parts.append('<text x="%d" y="20" class="h">Eintrag</text>' % x_label)
    parts.append('<text x="%d" y="20" class="h">Code</text>' % x_code)
    for label, example, code in DIRCOLOR_ROWS:
        if example is None:
            y += 10
            parts.append('<text x="%d" y="%d" class="g">%s</text>' % (x_label, y + 16, escape(label)))
            y += row_h
            continue
        parts.append('<text x="%d" y="%d" class="l">%s</text>' % (x_label, y + 17, escape(label)))
        parts.append('<text x="%d" y="%d" class="c">%s</text>' % (x_code, y + 17, code or "–"))
        for i, n in enumerate(names):
            t = THEMES[n]
            x = x_cells + i * cell_w
            parts.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, y, cell_w, row_h, t["bg"]))
            parts.append('<text x="%d" y="%d" class="m" style="fill:%s">%s</text>' % (
                x + 8, y + 17, _slot_color(t, code), escape(example)))
        y += row_h
    height = y + 10
    style = (
        "text{font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;font-size:13px;fill:#1f2328}"
        ".h{font-weight:600;fill:#59636e}.g{font-weight:600}.c{font-family:ui-monospace,Menlo,Consolas,monospace;"
        "font-size:12px;fill:#59636e}.m{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}"
        "@media (prefers-color-scheme: dark){text{fill:#e6edf3}.h,.c{fill:#9198a1}}"
    )
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
            'role="img" aria-label="Farbtabelle der dircolors in allen Profilen">'
            '<style>%s</style>%s</svg>\n') % (width, height, width, height, style, "".join(parts))


def main():
    out = Path(__file__).resolve().parent.parent / "themes"
    out.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        with open(out / ("%s.terminal" % name), "wb") as f:
            plistlib.dump(build(name, t), f, fmt=plistlib.FMT_XML)
        print("geschrieben:", out / ("%s.terminal" % name))
    docs_dir = out.parent / "docs"
    docs_dir.mkdir(exist_ok=True)
    (docs_dir / "dircolors.svg").write_text(build_dircolors_svg(), encoding="utf-8")
    print("geschrieben:", docs_dir / "dircolors.svg")


if __name__ == "__main__":
    main()
