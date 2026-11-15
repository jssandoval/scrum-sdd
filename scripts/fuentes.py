#!/usr/bin/env python3
"""Inventario reproducible de documentación fuente; no interpreta contenido."""
import argparse
import hashlib
import json
from pathlib import Path

BASE = Path('docs/00-fuentes')
MANIFEST = Path('docs/01-descubrimiento/inventario-fuentes.json')
REPORT = Path('docs/01-descubrimiento/inventario-fuentes.md')
CATEGORIES = ('manuales', 'lineamientos', 'formularios', 'matrices', 'requerimientos', 'otros')


def inventory():
    entries = []
    for f in sorted(BASE.rglob('*')) if BASE.exists() else []:
        if not f.is_file() or f.name.startswith('.') or f.is_symlink():
            continue
        relative = f.relative_to(BASE).as_posix()
        content = f.read_bytes()
        identifier = 'F-' + hashlib.sha256(relative.encode('utf-8')).hexdigest()[:10].upper()
        entries.append({'id': identifier, 'ruta': relative, 'sha256': hashlib.sha256(content).hexdigest(), 'bytes': len(content)})
    return entries


def render(entries):
    out = ['# Inventario de fuentes', '', 'Generado automáticamente por `fuentes.py`. No se edita a mano.', '',
           '| ID | Ruta bajo `docs/00-fuentes/` | Tamaño (bytes) | SHA-256 |', '| --- | --- | ---: | --- |']
    for e in entries:
        out.append('| {} | `{}` | {} | `{}` |'.format(e['id'], e['ruta'].replace('|', r'\|'), e['bytes'], e['sha256']))
    if not entries:
        out.append('| — | No se encontraron archivos fuente | 0 | — |')
    out += ['', 'Los identificadores dependen de la ruta; mover archivos cambia su ID. Los SHA-256 detectan cambios.',
            'Este inventario **no garantiza** extracción de contenido, interpretación de imágenes ni validación legal.']
    return '\n'.join(out) + '\n'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('accion', choices=('scan', 'check'))
    args = p.parse_args()
    entries = inventory()
    if args.accion == 'scan':
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        REPORT.write_text(render(entries), encoding='utf-8')
        print(f'OK: {len(entries)} fuente(s) inventariada(s).')
        return 0
    if not MANIFEST.exists() or not REPORT.exists():
        print('ERROR: falta inventario; ejecuta fuentes.py scan')
        return 1
    try:
        saved = json.loads(MANIFEST.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError):
        print('ERROR: inventario JSON ilegible')
        return 1
    if saved != entries or REPORT.read_text(encoding='utf-8') != render(entries):
        print('ERROR: fuentes cambiadas o inventario alterado; ejecuta fuentes.py scan y revisa impactos.')
        return 1
    print(f'OK: {len(entries)} fuente(s), inventario vigente.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
