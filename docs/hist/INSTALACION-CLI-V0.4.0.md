# Instalación simple de SSDD (Scrum-SDD) 0.4.5

1. Descomprime el ZIP y entra en `scrum-sdd`.
2. macOS/Linux: `sh install-cli.sh`. Windows PowerShell: `powershell -ExecutionPolicy Bypass -File .\install-cli.ps1`.
3. Abre una nueva terminal, entra al proyecto y ejecuta `ssdd init`.
4. Verifica con `ssdd doctor` y abre tu agente.

No se necesita Node.js, npm, uv, pip ni crear entornos virtuales. Se requiere Python 3.9+ (ya utilizado por el framework) y el agente elegido.

| Comando | Descripción |
| --- | --- |
| `ssdd init [ruta]` | Inicializa/actualiza integraciones en el proyecto |
| `ssdd init --agent codex` | Solo integración Codex |
| `ssdd update [ruta]` | Sincroniza archivos del framework del proyecto |
| `ssdd version` | Muestra versión global |
| `ssdd doctor` | Diagnostica entorno y agentes |

**Actualizar la CLI global:** descomprime una nueva versión y repite su instalador. `update` solo sincroniza proyectos; no consulta Internet.

**Precauciones:** el instalador de CLI configura PATH del usuario. `init` no reemplaza los documentos, código, specs ni aprobaciones. Los archivos administrados en `.framework/` y los skills pueden actualizarse; no personalices esos archivos sin hacer copia. El instalador Bash heredado `install.sh` continúa disponible en macOS/Linux.

**Limitación:** los instaladores requieren disponer previamente de Python 3.9+. En Windows, una terminal ya abierta puede requerir reiniciarse tras modificar PATH. No se anuncia ningún enlace remoto de descarga todavía.
