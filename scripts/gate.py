#!/usr/bin/env python3
"""Puertas de control del framework. Estado en docs/estado.json."""
import argparse
import datetime
import hashlib
import json
import pathlib
import sys
import re
import subprocess
import shutil
import uuid

STATE = pathlib.Path("docs/estado.json")
PHASES = [
    ("descubrimiento", "docs/01-descubrimiento/vision-producto.md"),
    ("requisitos", "docs/02-requisitos/DERCAS.md"),
    ("diseno", "docs/03-diseno/inventario-pantallas.md"),
    ("arquitectura", "docs/04-arquitectura/arquitectura-c4.md"),
    ("backlog", "docs/05-scrum/product-backlog.md"),
    ("setup", "AGENTS.md"),
]
ORDER = [name for name, _ in PHASES]
ARTIFACT = dict(PHASES)
REQUIRED = {
    "completo": ORDER,
    "feature": ["requisitos", "setup"],
    "hotfix": ["setup"],
}
HU_STATES = ["especificada", "implementada", "auditada", "aceptada"]
HU_PATTERN = re.compile(r"^HU-\d{3}$")

TARGETS = ORDER + ["sprint", "release"]


def load():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"fases": {}, "hu": {}}


def save(state):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def digest(path):
    p = pathlib.Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def phase_digest(phase):
    """Incluye entradas documentales en aprobación de descubrimiento y requisitos."""
    original = digest(ARTIFACT[phase])
    if original is None:
        return None
    if phase not in ('descubrimiento', 'requisitos'):
        return original
    h = hashlib.sha256()
    h.update(original.encode('ascii'))
    paths = [pathlib.Path('docs/00-fuentes')]
    if phase == 'descubrimiento':
        paths += [pathlib.Path('docs/01-descubrimiento/inventario-fuentes.json'),
                  pathlib.Path('docs/01-descubrimiento/analisis-fuentes.md')]
    if phase == 'requisitos':
        paths += [pathlib.Path('docs/02-requisitos/matriz-trazabilidad-documental.md')]
    for path in paths:
        files = sorted(path.rglob('*')) if path.is_dir() else ([path] if path.exists() else [])
        for f in files:
            if f.is_file() and not f.is_symlink() and not f.name.startswith('.'):
                h.update(f.as_posix().encode('utf-8'))
                h.update(hashlib.sha256(f.read_bytes()).digest())
    return h.hexdigest()


def problem(state, phase):
    entry = state["fases"].get(phase)
    if not entry:
        return "no aprobada"
    if phase_digest(phase) != entry["sha256"]:
        return "el artefacto cambió después de la aprobación; requiere nueva aprobación"
    return None


def blockers(state, target, carril):
    upto = ORDER if target in ("sprint", "release") else ORDER[: ORDER.index(target)]
    out = []
    for phase in upto:
        if phase in REQUIRED[carril]:
            p = problem(state, phase)
            if p:
                out.append(f"{phase}: {p}")
    if target == "release":
        if not state["hu"]:
            out.append("no hay historias registradas")
        for hu, entry in sorted(state["hu"].items()):
            if entry["estado"] != "aceptada":
                out.append(f"{hu}: está '{entry['estado']}', debe estar 'aceptada'")
    return out


def cmd_status(state, args):
    print("FASES")
    for phase in ORDER:
        p = problem(state, phase)
        entry = state["fases"].get(phase)
        if p is None:
            print(f"  [ok] {phase:<15} aprobó {entry['por']} el {entry['fecha']}")
        else:
            print(f"  [--] {phase:<15} {p}")
    print("HISTORIAS")
    for hu, entry in sorted(state["hu"].items()):
        print(f"  {hu}  {entry['estado']}")
    if not state["hu"]:
        print("  (ninguna)")
    return 0


def cmd_check(state, args):
    found = blockers(state, args.objetivo, args.carril)
    if found:
        print(f"BLOQUEADO: no se puede iniciar '{args.objetivo}' (carril {args.carril}).")
        for line in found:
            print(f"  - {line}")
        return 1
    print(f"OK: '{args.objetivo}' puede iniciar (carril {args.carril}).")
    return 0


def cmd_approve(state, args):
    sha = phase_digest(args.fase)
    if sha is None:
        print(f"ERROR: no existe {ARTIFACT[args.fase]}")
        return 1
    found = blockers(state, args.fase, args.carril)
    if found:
        print(f"BLOQUEADO: hay fases previas pendientes.")
        for line in found:
            print(f"  - {line}")
        return 1
    state["fases"][args.fase] = {
        "por": args.por,
        "fecha": datetime.date.today().isoformat(),
        "sha256": sha,
    }
    save(state)
    print(f"OK: '{args.fase}' aprobada por {args.por}.")
    return 0


def validate_hu_transition(hu, target):
    """Fail closed for missing implementation/audit evidence; acceptance stays human-operated."""
    spec = pathlib.Path(f"specs/{hu}.md")
    audit = pathlib.Path(f"docs/06-pruebas/auditoria-{hu}.md")
    if target == "especificada":
        if not spec.is_file() or not spec.read_text(encoding="utf-8").strip():
            return f"falta la especificación {spec}"
    elif target == "implementada":
        if not spec.is_file():
            return f"falta la especificación {spec}"
        script = pathlib.Path(".framework/scripts/trace.py")
        if not script.is_file():
            script = pathlib.Path(__file__).with_name("trace.py")
        result = subprocess.run([sys.executable, str(script), "--hu", hu], capture_output=True, text=True)
        if result.returncode:
            return "trazabilidad incompleta: " + (result.stdout + result.stderr).strip()[-700:]
        # La ejecución real del test suite es una obligación del skill y del CI.
    elif target == "auditada":
        if not audit.is_file():
            return f"falta el informe independiente {audit}"
        content = audit.read_text(encoding="utf-8")
        if not re.search(r"(?im)^\s*(?:\*\*)?Veredicto(?:\*\*)?\s*:\s*Aprobado(?:\s|$)", content):
            return f"{audit} debe contener 'Veredicto: Aprobado' sin hallazgos altos/críticos"
        if re.search(r"(?im)^\s*\|\s*(?:Crítica|Alta)\s*\|\s*[1-9]\d*\s*\|", content):
            return f"{audit} contiene hallazgos críticos o altos"
    return None


def cmd_hu(state, args):
    if not HU_PATTERN.fullmatch(args.id):
        print("ERROR: el identificador debe tener formato HU-001")
        return 1
    current = state["hu"].get(args.id, {}).get("estado")
    new = HU_STATES.index(args.estado)
    old = HU_STATES.index(current) if current else -1
    if new != old + 1:
        print(f"ERROR: {args.id} está '{current or 'sin registrar'}'; "
              f"el siguiente estado válido es '{HU_STATES[old + 1]}'.")
        return 1
    if args.estado == "aceptada" and not args.por:
        print("ERROR: 'aceptada' requiere --por con el nombre de quien acepta.")
        return 1
    issue = validate_hu_transition(args.id, args.estado)
    if issue:
        print(f"BLOQUEADO: {issue}")
        return 1
    entry = {"estado": args.estado, "fecha": datetime.date.today().isoformat()}
    if args.por:
        entry["por"] = args.por
    state["hu"][args.id] = entry
    save(state)
    print(f"OK: {args.id} -> {args.estado}")
    return 0


def cmd_revert(state, args):
    """Archiva la fase; opcionalmente retira sus entregables tras confirmación."""
    phase = args.fase
    if not state.get('fases', {}).get(phase):
        print(f"ERROR: fase '{phase}' no está aprobada; no hay aprobación que revertir.")
        return 1
    if args.modo == 'paso' and not args.confirmar_eliminar_paso:
        print('BLOQUEADO: eliminar el paso requiere --confirmar-eliminar-paso tras confirmación humana.')
        return 1
    # La identidad es declarativa; la invocación humana se exige en el skill.
    stamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S%f')
    archive = pathlib.Path('docs/historico-fases') / f'{stamp}-{phase}-{uuid.uuid4().hex[:8]}'
    archive.mkdir(parents=True, exist_ok=False)
    idx = ORDER.index(phase)
    invalidated = ORDER[idx:]
    previous = {p: state.get('fases', {}).get(p) for p in invalidated if p in state.get('fases', {})}
    # Guardar evidencia documental completa de la fase y el estado previo.
    folder_map = {
        'descubrimiento': 'docs/01-descubrimiento', 'requisitos': 'docs/02-requisitos',
        'diseno': 'docs/03-diseno', 'arquitectura': 'docs/04-arquitectura',
        'backlog': 'docs/05-scrum', 'setup': None,
    }
    folder = folder_map[phase]
    source = pathlib.Path(folder) if folder else pathlib.Path(ARTIFACT[phase])
    if args.modo == 'paso' and (not source.exists() or source.is_symlink()):
        print(f'ERROR: no existe una fuente válida para retirar: {source}')
        shutil.rmtree(archive)
        return 1
    if source.exists():
        dest = archive / source
        if source.is_dir():
            if any(p.is_symlink() for p in source.rglob('*')):
                print('BLOQUEADO: no se retiran fases que contienen enlaces simbólicos.')
                shutil.rmtree(archive)
                return 1
            shutil.copytree(source, dest)
            if sorted(p.relative_to(source) for p in source.rglob('*') if p.is_file()) != sorted(p.relative_to(dest) for p in dest.rglob('*') if p.is_file()):
                print('ERROR: copia de respaldo incompleta; no se retira el paso.')
                shutil.rmtree(archive)
                return 1
            for f in source.rglob('*'):
                if f.is_file() and digest(f) != digest(dest / f.relative_to(source)):
                    print('ERROR: el respaldo no coincide; no se retira el paso.')
                    shutil.rmtree(archive)
                    return 1
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            if digest(source) != digest(dest):
                print('ERROR: respaldo no coincide; no se retira el paso.')
                shutil.rmtree(archive)
                return 1
    # Si se revierten requisitos, no tocar documentación fuente de terceros.
    old_state = json.dumps(state, ensure_ascii=False, indent=2) + '\n'
    (archive / 'estado-anterior.json').write_text(old_state, encoding='utf-8')
    record = {
        'fase': phase, 'modo': args.modo, 'por': args.por, 'motivo': args.motivo,
        'fecha': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'aprobaciones_invalidadas': list(previous),
        'hu_conservadas': len(state.get('hu', {})),
        'nota': ('Se archiva y retira únicamente el entregable de la fase; el resto del proyecto y las HU se conservan.' if args.modo == 'paso' else 'Solo se revocan aprobaciones; documentos, código y HU conservados.'),
        'entregables': str(source),
    }
    (archive / 'reversion.json').write_text(json.dumps(record, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    if args.modo == 'paso' and source.exists():
        if source.is_dir():
            shutil.rmtree(source)
        else:
            source.unlink()
    for p in invalidated:
        state.get('fases', {}).pop(p, None)
    state.setdefault('reversiones', []).append({**record, 'ruta': archive.as_posix()})
    save(state)
    print(f'OK: fase {phase} revertida por {args.por}. Histórico: {archive}')
    print('Aprobaciones invalidadas:', ', '.join(previous))
    print('Paso archivado y retirado del proyecto activo.' if args.modo == 'paso' else 'Entregables conservados; solo se retiraron aprobaciones.')
    print('Código, historias, fuentes originales y archivos de otras fases preservados.')
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status").set_defaults(fn=cmd_status)

    p = sub.add_parser("check")
    p.add_argument("objetivo", choices=TARGETS)
    p.add_argument("--carril", choices=list(REQUIRED), default="completo")
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("approve")
    p.add_argument("fase", choices=ORDER)
    p.add_argument("--por", required=True)
    p.add_argument("--carril", choices=list(REQUIRED), default="completo")
    p.set_defaults(fn=cmd_approve)

    p = sub.add_parser("hu")
    p.add_argument("id")
    p.add_argument("estado", choices=HU_STATES)
    p.add_argument("--por")
    p.set_defaults(fn=cmd_hu)

    p = sub.add_parser('revert', help='Archiva una fase aprobada y revoca esta y las posteriores')
    p.add_argument('fase', choices=ORDER)
    p.add_argument('--por', required=True)
    p.add_argument('--motivo', required=True)
    p.add_argument('--modo', choices=['aprobacion', 'paso'], default='aprobacion')
    p.add_argument('--confirmar-eliminar-paso', action='store_true')
    p.set_defaults(fn=cmd_revert)

    args = parser.parse_args()
    sys.exit(args.fn(load(), args))


if __name__ == "__main__":
    main()
