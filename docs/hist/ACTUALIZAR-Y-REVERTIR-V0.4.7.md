# SSDD 0.4.7 — Actualización, arquitectura y reversión

## Actualizar
Descarga la versión publicada v0.4.7 y vuelve a ejecutar el instalador global (`sh install-cli.sh` en macOS/Linux o `install-cli.ps1` en Windows). En cada proyecto ejecuta `ssdd update`; conserva código, documentos y estados.

## Decisión arquitectónica integral
`/ssdd-arquitectura` propone cada componente justificado por requisitos, incluyendo UI y estilos, frontend, backend, APIs, interoperabilidad, persistencia, seguridad, colas, eventos, caché, despliegue, continuidad y observabilidad. No impone componentes innecesarios. Expone una recomendación y consulta al programador componente por componente; puede aceptar todo o modificar elecciones individuales. Detiene el proceso hasta recibir respuesta explícita.

## Revertir aprobaciones o retirar una fase completa
- `/ssdd-revertir arquitectura --modo aprobacion --por "Nombre" --motivo "Cambiar decisión"`: respalda y retira aprobaciones; conserva los documentos.
- `/ssdd-revertir arquitectura --modo paso --por "Nombre" --motivo "Rehacer arquitectura"`: exige **confirmación adicional del usuario**, respalda, verifica y retira documentos de la fase activa. Los documentos de fases posteriores permanecen pero sus aprobaciones se revocan.

Histórico: `docs/historico-fases/<fecha>-<fase>-<id>/`. No elimina código, HU, documentos fuente ni commits Git. En `setup`, el único archivo que puede retirar es `AGENTS.md`.
