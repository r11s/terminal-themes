#!/usr/bin/env python3
"""Erzeugt die Terminal.app-Profile (.terminal) im Ordner ../themes.

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


def main():
    out = Path(__file__).resolve().parent.parent / "themes"
    out.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        with open(out / ("%s.terminal" % name), "wb") as f:
            plistlib.dump(build(name, t), f, fmt=plistlib.FMT_XML)
        print("geschrieben:", out / ("%s.terminal" % name))


if __name__ == "__main__":
    main()
