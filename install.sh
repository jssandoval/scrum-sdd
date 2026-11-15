#!/usr/bin/env bash
# Instala el framework en un proyecto. Uso: ./install.sh <ruta-del-proyecto>
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="${1:?Uso: install.sh <ruta-del-proyecto>}"

mkdir -p "$DEST"/.claude/skills "$DEST"/.agents/skills \
         "$DEST"/.opencode/commands "$DEST"/.pi/prompts \
         "$DEST"/.framework "$DEST"/specs "$DEST"/src "$DEST"/tests
for category in manuales lineamientos formularios matrices requerimientos otros; do
  mkdir -p "$DEST/docs/00-fuentes/$category"
done
mkdir -p "$DEST"/docs/01-descubrimiento "$DEST"/docs/02-requisitos "$DEST"/docs/03-diseno \
         "$DEST"/docs/04-arquitectura/decisiones "$DEST"/docs/05-scrum/sprints \
         "$DEST"/docs/06-pruebas "$DEST"/docs/07-operacion

# Skills: Claude Code lee .claude/skills; Codex, OpenCode, Antigravity y Pi leen .agents/skills
cp -R "$SRC"/skills/. "$DEST"/.claude/skills/
cp -R "$SRC"/skills/. "$DEST"/.agents/skills/

# Comandos de barra para OpenCode y Pi: un envoltorio por skill
for dir in "$SRC"/skills/*/; do
  name="$(basename "$dir")"
  desc="$(grep -m1 '^description:' "$dir/SKILL.md" || echo "description: $name")"
  for target in "$DEST/.opencode/commands" "$DEST/.pi/prompts"; do
    printf -- '---\n%s\n---\nCarga el skill `%s` desde `.agents/skills/%s/SKILL.md` y ejecuta sus pasos al pie de la letra.\n\nArgumentos: $ARGUMENTS\n' \
      "$desc" "$name" "$name" > "$target/$name.md"
  done
done

for dir in templates scripts constitution ci; do
  rm -rf "$DEST/.framework/$dir"
  cp -R "$SRC/$dir" "$DEST/.framework/$dir"
done
cp "$SRC"/VERSION "$DEST"/.framework/VERSION
[ -f "$SRC/LICENSE" ] && cp "$SRC"/LICENSE "$DEST"/.framework/LICENSE

[ -f "$DEST/CLAUDE.md" ] || echo "@AGENTS.md" > "$DEST/CLAUDE.md"
[ -f "$DEST/docs/estado.json" ] || echo '{"fases": {}, "hu": {}}' > "$DEST/docs/estado.json"

echo "ssdd $(cat "$SRC"/VERSION) instalado en $DEST"
echo "Harnesses: Claude Code, Codex, OpenCode, Antigravity, Pi"
echo "Siguiente paso: abre tu agente en el proyecto y ejecuta /ssdd-descubrir (en Codex: \$ssdd-descubrir)"
