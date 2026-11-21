#!/bin/bash
# Installiert bash_profile, bashrc und dircolors aus ./dotfiles nach ~
# Vorhandene Dateien werden vorher nach ~/.terminal-themes-backup/<Datum> gesichert.
set -e
src="$(cd "$(dirname "$0")" && pwd)/dotfiles"
bak="$HOME/.terminal-themes-backup/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$bak"

install_file() {   # install_file <Quelle> <Ziel>
  [ -f "$src/$1" ] || { echo "fehlt:       $src/$1"; return; }
  [ -f "$2" ] && cp "$2" "$bak/$(basename "$2")"
  cp "$src/$1" "$2" && echo "installiert: $2"
}

install_file bash_profile "$HOME/.bash_profile"
install_file bashrc       "$HOME/.bashrc"
install_file dircolors    "$HOME/.dircolors"

echo "Sicherung der alten Dateien: $bak"
echo "Neues Terminal-Fenster öffnen oder: source ~/.bash_profile"
