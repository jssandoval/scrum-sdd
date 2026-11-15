#!/usr/bin/env sh
# Instala SSDD (Scrum-SDD) desde una etiqueta estable. Solo requiere Python 3.9+.
# Ejemplo: curl -fsSL https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.sh | sh
set -eu
VERSION="${SSDD_VERSION:-v0.4.6}"
case "$VERSION" in v[0-9]*.[0-9]*.[0-9]*) ;; *) echo 'Versión inválida (usa v0.4.6).' >&2; exit 1 ;; esac
if command -v python3 >/dev/null 2>&1; then PY=python3
elif command -v python >/dev/null 2>&1; then PY=python
else echo 'Falta Python 3.9 o superior.' >&2; exit 1; fi
"$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)' || { echo 'Requiere Python 3.9+.' >&2; exit 1; }
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT HUP INT TERM
URL="https://github.com/jssandoval/scrum-sdd/archive/refs/tags/${VERSION}.zip"
echo "Descargando SSDD (Scrum-SDD) ${VERSION}..."
if command -v curl >/dev/null 2>&1; then curl -fLsS --retry 2 "$URL" -o "$TMP_DIR/framework.zip"
elif command -v wget >/dev/null 2>&1; then wget -q "$URL" -O "$TMP_DIR/framework.zip"
else echo 'Necesitas curl o wget.' >&2; exit 1; fi
"$PY" - "$TMP_DIR/framework.zip" "$TMP_DIR" "$VERSION" <<'PY'
import pathlib, sys, zipfile
archive, folder, version = sys.argv[1:]
with zipfile.ZipFile(archive) as z:
    z.extractall(folder)
roots = [p for p in pathlib.Path(folder).iterdir() if p.is_dir() and (p/'install-cli.py').is_file()]
if len(roots) != 1:
    sys.exit('ERROR: paquete de instalación inválido')
if (roots[0]/'VERSION').read_text().strip() != version.lstrip('v'):
    sys.exit('ERROR: versión del paquete no coincide con la solicitada')
print(roots[0])
PY
ROOT="$TMP_DIR/scrum-sdd-${VERSION#v}"
if [ ! -f "$ROOT/install-cli.sh" ]; then echo 'ERROR: no se encontró instalador.' >&2; exit 1; fi
sh "$ROOT/install-cli.sh"
echo "Instalado ${VERSION}. Abre otra terminal y ejecuta: ssdd doctor"
