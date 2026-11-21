#!/bin/bash
# Windows (Git Bash): installiert die Windows-Terminal-Profile und die mintty-Themen.
# Vorhandene Dateien werden vorher nach ~/.terminal-themes-backup/<Datum> gesichert.
# settings.json und ~/.minttyrc werden nicht angefasst.
set -e
root="$(cd "$(dirname "$0")" && pwd)"
bak="$HOME/.terminal-themes-backup/$(date +%Y%m%d-%H%M%S)-windows"
saved=0

if [ -z "$LOCALAPPDATA" ] || [ -z "$APPDATA" ]; then
  echo "LOCALAPPDATA/APPDATA nicht gesetzt – bitte in Git Bash unter Windows ausführen." >&2
  exit 1
fi

install_file() {   # install_file <Quelle> <Zielordner> <Sicherungs-Unterordner>
  local dest="$2/$(basename "$1")"
  if [ -f "$dest" ]; then
    mkdir -p "$bak/$3"
    cp -p "$dest" "$bak/$3/"
    saved=1
  fi
  mkdir -p "$2"
  cp "$1" "$dest"
  echo "installiert: $dest"
}

# Windows Terminal: JSON-Fragment (Farbschemata + Profile "Git Bash <Name>")
frag="$(cygpath -u "$LOCALAPPDATA")/Microsoft/Windows Terminal/Fragments/terminal-themes"
install_file "$root/windows-terminal/terminal-themes.json" "$frag" windows-terminal

# mintty: Themendateien
mt="$(cygpath -u "$APPDATA")/mintty/themes"
for f in "$root"/mintty/*; do
  install_file "$f" "$mt" mintty
done

echo
[ "$saved" = 1 ] && echo "Sicherung der alten Dateien: $bak"
echo "Windows Terminal neu starten: die Profile 'Git Bash <Name>' erscheinen im Menü."
echo "mintty: in ~/.minttyrc ThemeFile=<Name> eintragen (siehe README)."
