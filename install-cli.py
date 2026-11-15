#!/usr/bin/env python3
"""Instalador local del comando global scrum-sdd; Python estándar, sin pip."""
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent

def main():
    if sys.version_info < (3, 9):
        raise SystemExit('Se necesita Python 3.9 o superior.')
    if os.name == 'nt':
        home = Path(os.environ.get('APPDATA', Path.home()))/'scrum-sdd'
        bin_dir = Path(os.environ.get('LOCALAPPDATA', Path.home()))/'Programs'/'scrum-sdd'/'bin'
    else:
        home = Path.home()/'.local/share/scrum-sdd'
        bin_dir = Path.home()/'.local/bin'
    bin_dir.mkdir(parents=True, exist_ok=True)
    # Instalar únicamente los recursos necesarios; no altera los documentos de proyectos.
    for name in ('skills', 'templates', 'constitution', 'scripts', 'ci', 'cli'):
        source, dest = ROOT/name, home/name
        for p in source.rglob('*'):
            target = dest / p.relative_to(source)
            if p.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, target)
    for file in ('VERSION', 'LICENSE'):
        shutil.copy2(ROOT/file, home/file)
    if os.name == 'nt':
        cmd = bin_dir/'scrum-sdd.cmd'
        cmd.write_text('@echo off\r\n"'+sys.executable+'" "'+str(home/'cli/scrum_sdd.py')+'" %*\r\n', encoding='utf-8')
    else:
        cmd = bin_dir/'scrum-sdd'
        cmd.write_text('#!/bin/sh\nexec "'+sys.executable+'" "'+str(home/'cli/scrum_sdd.py')+'" "$@"\n', encoding='utf-8')
        cmd.chmod(0o755)
    print('Instalación terminada: Scrum-SDD', (home/'VERSION').read_text().strip())
    print('Ejecutable:', cmd)
    print('Para iniciar un proyecto: scrum-sdd init')
    print('Para revisar el entorno: scrum-sdd doctor')
    if str(bin_dir) not in os.environ.get('PATH', '').split(os.pathsep):
        print('IMPORTANTE: el directorio de comandos no está en PATH:', bin_dir)
        print('Usa install-cli.sh (macOS/Linux) o install-cli.ps1 (Windows) para configurarlo automáticamente.')

if __name__ == '__main__':
    main()
