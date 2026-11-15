# Ejemplo: registro de clientes con documentación fuente

**Ejemplo ficticio.** Ninguno de los documentos representa legislación, clientes reales o requisitos regulatorios.

1. Instala el framework en tu proyecto: `bash /ruta/scrum-sdd/install.sh /ruta/mi-proyecto`.
2. Copia el contenido de `fuentes/` a las subcarpetas correspondientes bajo `mi-proyecto/docs/00-fuentes/`.
3. Dentro del agente ejecuta `/descubrir Construir un módulo para registrar clientes según los documentos aportados`. El skill inventaría documentos y registra la contradicción de campos obligatorios.
4. Revisa `docs/01-descubrimiento/analisis-fuentes.md`: el manual y el formulario discrepan respecto del teléfono obligatorio. **No lo resuelvas de forma automática.**
5. Resuelve la contradicción indicando explícitamente cuál será la regla válida; después revisa y aprueba descubrimiento mediante `/aprobar descubrimiento --por "Tu Nombre"`.
6. Ejecuta `/dercas`; revisa RF, RN, CA, fuentes y ubicación en `docs/02-requisitos/matriz-trazabilidad-documental.md`. Aprueba requisitos solo cuando reflejen tu decisión.
7. Ejecuta `/diseno`, `/arquitectura`, `/backlog`, `/setup` para continuar el ciclo completo.

La plantilla `resultado-esperado.md` ilustra el formato; **no es una ejecución real del agente**.

## Instalar el framework para ejecutar este ejemplo (v0.4.0)

Después de instalar la CLI una sola vez con `install-cli.sh` o `install-cli.ps1`, desde el directorio del proyecto usa `scrum-sdd init`. Copia los archivos de `fuentes/` a las categorías correspondientes de `docs/00-fuentes/` y ejecuta `/descubrir`. No se requiere instalación adicional.
