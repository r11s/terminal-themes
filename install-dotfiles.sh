#!/bin/bash
# Installiert bash_profile, bashrc, dircolors und vimrc aus ./dotfiles nach ~
# Vorhandene Dateien werden vorher nach ~/.terminal-themes-backup/<Datum> gesichert.
set -e
src="$(cd "$(dirname "$0")" && pwd)/dotfiles"
bak="$HOME/.terminal-themes-backup/$(date +%Y%m%d-%H%M%S)"
saved=0

backup() {   # backup <Datei>: kopiert eine vorhandene Datei in den Sicherungsordner
  [ -f "$1" ] || return 0
  mkdir -p "$bak"
  cp -p "$1" "$bak/$(basename "$1")"
  saved=1
}

install_file() {   # install_file <Quelle> <Ziel>
  [ -f "$src/$1" ] || { echo "fehlt:       $src/$1"; return; }
  backup "$2"
  cp "$src/$1" "$2" && echo "installiert: $2"
}

install_file bash_profile "$HOME/.bash_profile"
install_file bashrc       "$HOME/.bashrc"
install_file dircolors    "$HOME/.dircolors"

# vimrc nur anlegen, wenn noch keine vorhanden ist (eine eigene wird nicht überschrieben)
if [ -e "$HOME/.vimrc" ]; then
  echo "übersprungen: $HOME/.vimrc existiert schon (Zeilen aus dotfiles/vimrc bei Bedarf übernehmen)"
else
  install_file vimrc "$HOME/.vimrc"
fi

[ "$saved" = 1 ] && echo "Sicherung der alten Dateien: $bak"
echo "Neues Terminal-Fenster öffnen oder: source ~/.bash_profile"
