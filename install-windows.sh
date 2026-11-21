#!/bin/bash
# Windows (Git Bash): installiert die Windows-Terminal-Profile und die mintty-Themen.
# Es werden nur neue Dateien angelegt, settings.json und ~/.minttyrc bleiben unberührt.
set -e
root="$(cd "$(dirname "$0")" && pwd)"

if [ -z "$LOCALAPPDATA" ] || [ -z "$APPDATA" ]; then
  echo "LOCALAPPDATA/APPDATA nicht gesetzt – bitte in Git Bash unter Windows ausführen." >&2
  exit 1
fi

# Windows Terminal: JSON-Fragment (Farbschemata + Profile "Git Bash <Name>")
frag="$(cygpath -u "$LOCALAPPDATA")/Microsoft/Windows Terminal/Fragments/terminal-themes"
mkdir -p "$frag"
cp "$root/windows-terminal/terminal-themes.json" "$frag/terminal-themes.json"
echo "installiert: $frag/terminal-themes.json"

# mintty: Themendateien
mt="$(cygpath -u "$APPDATA")/mintty/themes"
mkdir -p "$mt"
for f in "$root"/mintty/*; do
  cp "$f" "$mt/$(basename "$f")"
  echo "installiert: $mt/$(basename "$f")"
done

echo
echo "Windows Terminal neu starten: die Profile 'Git Bash <Name>' erscheinen im Menü."
echo "mintty: in ~/.minttyrc ThemeFile=<Name> eintragen (siehe README)."
