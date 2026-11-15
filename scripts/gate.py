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

    args = parser.parse_args()
    sys.exit(args.fn(load(), args))


if __name__ == "__main__":
    main()
