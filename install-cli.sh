#!/usr/bin/env sh
# Uso: sh install-cli.sh (desde la carpeta del ZIP). Requiere solo Python 3.9+.
set -eu
SRC=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if command -v python3 >/dev/null 2>&1; then PY=python3
elif command -v python >/dev/null 2>&1; then PY=python
else echo 'Python 3.9+ no encontrado; es el único requisito de ejecución de Scrum-SDD.' >&2; exit 1
fi
"$PY" "$SRC/install-cli.py"
BIN="$HOME/.local/bin"
case ":$PATH:" in *":$BIN:"*) ;; *)
  case "${SHELL:-}" in
    */zsh) CONFIG="$HOME/.zshrc" ;;
    */bash) CONFIG="$HOME/.bashrc" ;;
    *) CONFIG="$HOME/.profile" ;;
  esac
  if [ ! -f "$CONFIG" ] || ! grep -Fq 'export PATH="$HOME/.local/bin:$PATH"' "$CONFIG"; then
    printf '\n# Scrum-SDD CLI\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$CONFIG"
    echo "PATH configurado en $CONFIG; abre otra terminal para usar scrum-sdd."
  fi
;; esac
printf 'Para esta terminal: export PATH="$HOME/.local/bin:$PATH"\n'
