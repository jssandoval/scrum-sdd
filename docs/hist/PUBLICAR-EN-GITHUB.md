# Publicar SSDD (Scrum-SDD) en GitHub

Repositorio oficial: https://github.com/jssandoval/scrum-sdd

## Primera publicación (desde la carpeta `scrum-sdd`)

**Importante:** GitHub ya debe tener creado el repositorio vacío. Instala Git en tu equipo para subir código (no es necesario para los usuarios que instalan SSDD (Scrum-SDD)).

```bash
git init
git branch -M main
git remote add origin https://github.com/jssandoval/scrum-sdd.git
git add .
git commit -m "Publicar SSDD (Scrum-SDD) v0.4.7 y distribución desde GitHub"
git push -u origin main
```

Si el repositorio ya tiene commits o un README propio, primero integra esos cambios antes de hacer push; no utilices `--force`.

## Primera versión descargable

```bash
git tag -a v0.4.7 -m "SSDD (Scrum-SDD) v0.4.7"
git push origin v0.4.7
```

La acción `.github/workflows/release.yml` verifica pruebas y crea automáticamente el Release con ZIP y `SHA256SUMS.txt` cuando se publica la etiqueta. Revisa **Actions** y **Releases** en GitHub. El instalador remoto requiere que exista la etiqueta `v0.4.7`.

## Instalación para terceros

macOS / Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.sh | sh
```

Windows (PowerShell):

```powershell
irm https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.ps1 | iex
```

Requisitos de instalación: Python 3.9+; un agente de IA compatible para utilizar el framework. Los scripts remotos descargan la etiqueta `v0.4.7`, no la versión cambiante de `main`. Antes de usar scripts remotos es recomendable revisar su contenido.

## Versiones anteriores

Conserva los ZIP originales de las versiones 0.2.0 y 0.3.0 como archivos adjuntos en sus respectivos **Releases** (puedes crear los Releases desde la interfaz de GitHub). En 0.1.0 solo se cuenta con el documento original, no con un ZIP ejecutable verificable. No es necesario incorporar el historial de archivos binarios al árbol de `main`.

## Nueva versión futura

1. Actualiza `VERSION`, README y CHANGELOG.
2. Cambia la versión predeterminada en `install-remote.sh` y `install-remote.ps1`.
3. Ejecuta las pruebas y publica los cambios en `main`.
4. Crea y publica la etiqueta nueva `vX.Y.Z`.

Los instaladores locales `install-cli.sh` y `install-cli.ps1` siguen funcionando sin GitHub, desde el ZIP descargado.
