#!/usr/bin/env python3
"""Valida la trazabilidad RF -> CA -> HU -> prueba."""
import argparse
import pathlib
import re
import sys
import ast

DERCAS = pathlib.Path("docs/02-requisitos/DERCAS.md")
BACKLOG = pathlib.Path("docs/05-scrum/product-backlog.md")
TEST_DIRS = [pathlib.Path("tests"), pathlib.Path("src")]
TEST_NAME = re.compile(r"(test|spec)", re.I)
HEAD = re.compile(r"^#{2,4}\s+((?:RF|CA|HU)-\d{3})\b")
PRIORITY = re.compile(r"Prioridad:\W*(Must|Should|Could|Won.t)")


def sections(path, errors):
    """Devuelve {ID: texto de su sección}."""
    out, current = {}, None
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        m = HEAD.match(line)
        if m:
            current = m.group(1)
            if current in out:
                errors.append(f"{current} está definido más de una vez en {path}")
            out[current] = line
        elif line.startswith("#"):
            current = None
        elif current:
            out[current] += "\n" + line
    return out


def refs(text, prefix, own):
    return {r for r in re.findall(rf"\b{prefix}-\d{{3}}\b", text) if r != own}


def tested_criteria():
    """Solo cuenta referencias dentro de pruebas con comprobaciones ejecutables.

    No sustituye correr la suite ni revisar la semántica de cada aserción.
    """
    found = set()
    for root in TEST_DIRS:
        if not root.exists():
            continue
        for f in root.rglob("*"):
            if not f.is_file() or not TEST_NAME.search(f.name):
                continue
            if f.suffix not in (".py", ".js", ".jsx", ".ts", ".tsx", ".cs"):
                continue
            try:
                content = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if f.suffix == ".py":
                try:
                    tree = ast.parse(content)
                except SyntaxError:
                    continue
                for n in ast.walk(tree):
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and (n.name.startswith("test_") or n.name.endswith("_test")):
                        segment = ast.get_source_segment(content, n) or ""
                        assertions = [x for x in ast.walk(n) if isinstance(x, ast.Assert)]
                        meaningful = any(not isinstance(a.test, ast.Constant) or a.test.value is not True for a in assertions)
                        meaningful |= any(isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute) and x.func.attr.startswith("assert") for x in ast.walk(n))
                        if meaningful:
                            found.update(re.findall(r"\bCA-\d{3}\b", segment))
            else:
                # Comprobación estructural mínima. Ejecutar las pruebas es obligatorio.
                checks = re.search(r"\b(expect\s*\(|assert\s*\(|Assert\s*\.|Should\s*\(|toEqual\s*\(|toBe\s*\()", content)
                if checks:
                    found.update(re.findall(r"\bCA-\d{3}\b", content))
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hu", action="append", default=[],
                        help="Exige pruebas para los criterios de esta historia (repetible)")
    args = parser.parse_args()

    errors, warnings = [], []
    if not DERCAS.exists():
        print(f"ERROR: no existe {DERCAS}")
        sys.exit(1)

    d = sections(DERCAS, errors)
    b = sections(BACKLOG, errors)
    rf = {k: v for k, v in d.items() if k.startswith("RF-")}
    ca = {k: v for k, v in d.items() if k.startswith("CA-")}
    hu = {k: v for k, v in b.items() if k.startswith("HU-")}

    prio = {}
    for k, v in rf.items():
        m = PRIORITY.search(v)
        if not m:
            errors.append(f"{k} no declara prioridad MoSCoW")
        prio[k] = m.group(1) if m else "Must"
    active = {k for k in rf if not prio[k].startswith("Won")}

    ca_rf = {}
    for k, v in ca.items():
        linked = refs(v.splitlines()[0], "RF", k) or refs(v, "RF", k)
        valid = linked & set(rf)
        if not valid:
            errors.append(f"{k} no referencia ningún RF existente")
        ca_rf[k] = valid

    for k in sorted(active):
        if not any(k in linked for linked in ca_rf.values()):
            errors.append(f"{k} no tiene criterios de aceptación")

    hu_rf = {}
    if BACKLOG.exists():
        for k, v in hu.items():
            valid = refs(v, "RF", k) & set(rf)
            if not valid:
                errors.append(f"{k} no referencia ningún RF existente")
            hu_rf[k] = valid
        covered = set().union(*hu_rf.values()) if hu_rf else set()
        for k in sorted(active - covered):
            msg = f"{k} ({prio[k]}) no está cubierto por ninguna historia"
            (errors if prio[k] == "Must" else warnings).append(msg)

    for h, description in hu.items():
        declared = refs(description, "CA", h)
        for c in declared - set(ca):
            errors.append(f"{h} referencia {c} inexistente")
    tested = tested_criteria()
    for h in args.hu:
        if h not in hu:
            errors.append(f"{h} no existe en el backlog")
            continue
        declared = refs(hu[h], "CA", h)
        related = {k for k, linked in ca_rf.items() if linked & hu_rf.get(h, set())}
        for c in declared - set(ca):
            errors.append(f"{h} referencia el criterio inexistente {c}")
        for c in declared & set(ca):
            if not ca_rf[c] & hu_rf.get(h, set()):
                errors.append(f"{h}: {c} no corresponde a los RF declarados")
        if not declared:
            errors.append(f"{h} no declara criterios de aceptación")
        for c in sorted(declared & related):
            if c not in tested:
                errors.append(f"{c} (de {h}) no aparece en ninguna prueba")

    print(f"RF: {len(rf)} ({len(active)} activos) | CA: {len(ca)} | HU: {len(hu)} | "
          f"CA con prueba: {len(tested & set(ca))}/{len(ca)}")
    for w in warnings:
        print(f"  AVISO: {w}")
    for e in errors:
        print(f"  ERROR: {e}")
    if errors:
        print(f"FALLA: {len(errors)} error(es) de trazabilidad.")
        sys.exit(1)
    print("OK: trazabilidad completa.")


if __name__ == "__main__":
    main()
