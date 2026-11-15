---
name: ssdd-trazabilidad
description: 'Valida la cadena requisito, criterio, historia y prueba. Uso: /ssdd-trazabilidad [HU-001]'
argument-hint: '[HU-XXX]'
---

Argumentos recibidos: $ARGUMENTS

## Pasos
1. Sin argumentos ejecuta: `python3 .framework/scripts/trace.py`
   Con una historia ejecuta: `python3 .framework/scripts/trace.py --hu <HU>`
2. Muestra el resumen y agrupa los errores por tipo.
3. Por cada error indica el archivo a corregir y el skill que corresponde (`/ssdd-dercas`, `/ssdd-backlog` o `/ssdd-implementar`).

Solo lectura: no corrijas nada sin que el usuario lo pida.
