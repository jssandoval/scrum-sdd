# Ejemplo: registro de clientes con documentación fuente

**Ejemplo ficticio.** Ninguno de los documentos representa legislación, clientes reales o requisitos regulatorios.

1. Instala el framework en tu proyecto: `bash /ruta/scrum-sdd/install.sh /ruta/mi-proyecto`.
2. Copia el contenido de `fuentes/` a las subcarpetas correspondientes bajo `mi-proyecto/docs/00-fuentes/`.
3. Dentro del agente ejecuta `/ssdd-descubrir Construir un módulo para registrar clientes según los documentos aportados`. El skill inventaría documentos y registra la contradicción de campos obligatorios.
4. Revisa `docs/01-descubrimiento/analisis-fuentes.md`: el manual y el formulario discrepan respecto del teléfono obligatorio. **No lo resuelvas de forma automática.**
5. Resuelve la contradicción indicando explícitamente cuál será la regla válida; después revisa y aprueba descubrimiento mediante `/ssdd-aprobar descubrimiento --por "Tu Nombre"`.
6. Ejecuta `/ssdd-dercas`; revisa RF, RN, CA, fuentes y ubicación en `docs/02-requisitos/matriz-trazabilidad-documental.md`. Aprueba requisitos solo cuando reflejen tu decisión.
7. Ejecuta `/ssdd-diseno`, `/ssdd-arquitectura`, `/ssdd-backlog`, `/ssdd-setup` para continuar el ciclo completo.

La plantilla `resultado-esperado.md` ilustra el formato; **no es una ejecución real del agente**.

## Instalar el framework para ejecutar este ejemplo (v0.4.5)

Después de instalar la CLI una sola vez con `install-cli.sh` o `install-cli.ps1`, desde el directorio del proyecto usa `ssdd init`. Copia los archivos de `fuentes/` a las categorías correspondientes de `docs/00-fuentes/` y ejecuta `/ssdd-descubrir`. No se requiere instalación adicional.


### SSDD v0.4.6: selección del stack y reversión

Tras `/ssdd-diseno`, llama a `/ssdd-arquitectura` y responde qué usarás en frontend, backend, interoperabilidad, persistencia e infraestructura. El agente muestra recomendaciones, pero **tú eliges**. Si luego necesitas reconsiderar la arquitectura ya aprobada, invoca `/ssdd-revertir arquitectura --por "Nombre" --motivo "Nueva decisión"`, inspecciona `docs/historico-fases/`, actualiza el ADR y vuelve a aprobar.


### SSDD 0.4.7: decisiones arquitectónicas y dos reversiones

En `/ssdd-arquitectura`, el agente debe proponer un stack **completo y proporcional** al problema (incluyendo estilos, autenticación, integraciones, caché, cola o tareas si corresponde, pruebas, CI/CD y operación) y pedir confirmación por componente. El desarrollador puede aceptar la propuesta o modificarla. Si el requisito no necesita mensajería o caché, se anota «no aplica», no se obliga a usarla.

Tras aprobar arquitectura, prueba `/ssdd-revertir arquitectura --modo aprobacion --por "Persona" --motivo "Revisar elección"`: conserva los documentos. La alternativa `--modo paso` retira la carpeta `docs/04-arquitectura/` **después de respaldarla en `docs/historico-fases/` y confirmar humanamente**. Nunca retira el código de la aplicación.
