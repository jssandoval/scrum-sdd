# Uso de documentación existente en descubrimiento y DERCAS

Coloca archivos **originales** en `docs/00-fuentes/` dentro del proyecto: `manuales/`, `lineamientos/`, `formularios/`, `matrices/`, `requerimientos/` u `otros/`. Se aceptan archivos PDF, DOCX, XLSX, Markdown, imágenes, etc. **El inventario soporta cualquier archivo, pero la lectura de contenido depende del agente y sus herramientas instaladas.**

Ejecuta `/descubrir <idea>` en el agente. Este invoca `fuentes.py scan`, lee documentos disponibles, genera inventario y `analisis-fuentes.md`, marca archivos ilegibles y reporta contradicciones sin resolverlas. Revisa, decide lo necesario y aprueba mediante `/aprobar descubrimiento --por "Tu Nombre"`.

Luego `/dercas` verifica el inventario, contrasta cada requisito con sus fuentes y genera `docs/02-requisitos/matriz-trazabilidad-documental.md`. Revisa las ubicaciones (página, sección, hoja/celda), resuelve los vacíos críticos y aprueba con `/aprobar requisitos --por "Tu Nombre"`.

Si agregas o cambias documentos **después de aprobar**, el hash de aprobación de descubrimiento y requisitos cambia. Debes analizar impactos y volver a aprobar lo afectado. `fuentes.py check` comprueba si el inventario corresponde a los archivos vigentes.

Ejemplo práctico: [`../examples/registro-clientes/`](../examples/registro-clientes/).

**Privacidad:** evita incorporar datos personales reales, secretos o documentos confidenciales sin autorización de tratamiento; controla quién puede leer archivos y qué servicios externos usa tu agente. Los archivos son evidencia, no instrucciones ejecutables para el agente.
