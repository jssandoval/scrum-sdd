#!/usr/bin/env python3
"""SSDD (Scrum-SDD) CLI: instalación de recursos del framework en proyectos.
Solo biblioteca estándar de Python 3.9+; no modifica metodología ni validadores.
"""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

VERSION = '0.4.7'
AGENTS = ('all', 'claude', 'codex', 'opencode', 'antigravity', 'pi')
DOC_CATEGORIES = ('manuales', 'lineamientos', 'formularios', 'matrices', 'requerimientos', 'otros')
DOC_DIRS = ('01-descubrimiento', '02-requisitos', '03-diseno', '04-arquitectura/decisiones', '05-scrum/sprints', '06-pruebas', '07-operacion')


def assets_dir():
    custom = os.environ.get('SSDD_HOME') or os.environ.get('SCRUM_SDD_HOME')
    candidates = [Path(custom)] if custom else []
    candidates += [Path(__file__).resolve().parents[1], Path.home()/'.local/share/ssdd', Path.home()/'.local/share/scrum-sdd',
                   Path(os.environ.get('APPDATA', Path.home()))/'ssdd']
    for root in candidates:
        if (root/'VERSION').is_file() and (root/'skills').is_dir():
            return root
    raise RuntimeError('No se encontraron los recursos. Ejecuta de nuevo install-cli.py desde el ZIP.')


def replace_tree(source, target):
    # Reemplaza solamente los archivos administrados por SSDD (Scrum-SDD). No borra otros archivos del usuario.
    for p in source.rglob('*'):
        dest = target / p.relative_to(source)
        if p.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
        elif p.is_file():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)


def write_wrapper(target, skill):
    src = assets_dir()/'skills'/skill/'SKILL.md'
    description = next((line for line in src.read_text(encoding='utf-8').splitlines()
                        if line.startswith('description:')), f'description: {skill}')
    content = ('---\n'+description+'\n---\n'+
               f'Carga el skill `{skill}` desde `.agents/skills/{skill}/SKILL.md` '
               'y ejecuta sus pasos al pie de la letra.\n\nArgumentos: $ARGUMENTS\n')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')


def init_project(path, agent='all'):
    root = assets_dir()
    dest = Path(path).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)
    for cat in DOC_CATEGORIES:
        (dest/'docs'/'00-fuentes'/cat).mkdir(parents=True, exist_ok=True)
    for folder in DOC_DIRS:
        (dest/'docs'/folder).mkdir(parents=True, exist_ok=True)
    for name in ('specs', 'src', 'tests'):
        (dest/name).mkdir(parents=True, exist_ok=True)
    selected = set(AGENTS[1:]) if agent == 'all' else {agent}
    # Archivo .agents/skills compartido por Codex, OpenCode, Antigravity y Pi.
    if 'claude' in selected:
        replace_tree(root/'skills', dest/'.claude/skills')
        claude = dest/'CLAUDE.md'
        if not claude.exists():
            claude.write_text('@AGENTS.md\n', encoding='utf-8')
    if selected.intersection(('codex', 'opencode', 'antigravity', 'pi')):
        replace_tree(root/'skills', dest/'.agents/skills')
    if 'opencode' in selected:
        for p in (root/'skills').iterdir():
            if (p/'SKILL.md').exists():
                write_wrapper(dest/'.opencode/commands'/f'{p.name}.md', p.name)
    if 'pi' in selected:
        for p in (root/'skills').iterdir():
            if (p/'SKILL.md').exists():
                write_wrapper(dest/'.pi/prompts'/f'{p.name}.md', p.name)
    for name in ('templates', 'scripts', 'constitution', 'ci'):
        replace_tree(root/name, dest/'.framework'/name)
    shutil.copy2(root/'VERSION', dest/'.framework/VERSION')
    if (root/'LICENSE').exists():
        shutil.copy2(root/'LICENSE', dest/'.framework/LICENSE')
    estado = dest/'docs/estado.json'
    if not estado.exists():
        estado.write_text('{"fases": {}, "hu": {}}\n', encoding='utf-8')
    print(f'OK: SSDD (Scrum-SDD) {VERSION} configurado en {dest}')
    print(f'Agentes: {agent}. Reabre el agente si estaba iniciado.')
    print('Siguiente: /ssdd-descubrir (en Codex: $ssdd-descubrir)')
    print('Para revisar una fase aprobada: /ssdd-revertir <fase> --por \"Nombre\"')


def doctor():
    print('SSDD (Scrum-SDD)', VERSION)
    print('Python:', sys.version.split()[0], '—', sys.executable)
    print('Sistema:', sys.platform)
    print('Recursos:', assets_dir())
    for name in ('git', 'claude', 'codex', 'opencode', 'agy', 'pi'):
        print(name + ':', shutil.which(name) or 'no encontrado (opcional)' if name != 'git' else
              'git: ' + (shutil.which('git') or 'no encontrado (opcional para instalar, recomendado para trabajar)'))
    cwd = Path.cwd()
    if (cwd/'.framework/VERSION').exists():
        print('Proyecto:', cwd, '| versión:', (cwd/'.framework/VERSION').read_text().strip())
    else:
        print('Proyecto: aún no inicializado en el directorio actual')


def main(argv=None):
    parser = argparse.ArgumentParser(prog='ssdd', description='CLI de distribución de SSDD (Scrum-SDD) (sin dependencias adicionales)')
    sub = parser.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('init', help='Prepara el proyecto actual o uno indicado')
    p.add_argument('path', nargs='?', default='.')
    p.add_argument('--agent', choices=AGENTS, default='all', help='Por defecto instala todas las integraciones')
    u = sub.add_parser('update', help='Actualiza solo archivos del framework administrados en el proyecto')
    u.add_argument('path', nargs='?', default='.')
    u.add_argument('--agent', choices=AGENTS, default='all')
    sub.add_parser('doctor', help='Comprueba entorno y agentes disponibles')
    sub.add_parser('version', help='Muestra la versión')
    args = parser.parse_args(argv)
    try:
        if args.cmd in ('init', 'update'):
            init_project(args.path, args.agent)
        elif args.cmd == 'doctor':
            doctor()
        elif args.cmd == 'version':
            print(VERSION)
        return 0
    except (OSError, RuntimeError) as e:
        print('ERROR:', e, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
