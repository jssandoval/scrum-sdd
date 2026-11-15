# Uso: irm https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.ps1 | iex
# Solo necesita Python 3.9+ y PowerShell; no requiere Node, npm, pip o uv.
$ErrorActionPreference = 'Stop'
$version = if ($env:SSDD_VERSION) { $env:SSDD_VERSION } else { 'v0.4.7' }
if ($version -notmatch '^v\d+\.\d+\.\d+$') { throw 'Versión inválida. Ejemplo: v0.4.7' }
$command = if (Get-Command py -ErrorAction SilentlyContinue) { 'py' } elseif (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { throw 'Instala Python 3.9 o superior.' }
$pythonArgs = if ($command -eq 'py') { @('-3') } else { @() }
& $command @pythonArgs -c 'import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)'
if ($LASTEXITCODE -ne 0) { throw 'Se necesita Python 3.9 o superior.' }
$temp = Join-Path ([IO.Path]::GetTempPath()) ('scrum-sdd-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $temp | Out-Null
try {
  $url = "https://github.com/jssandoval/scrum-sdd/archive/refs/tags/$version.zip"
  $archive = Join-Path $temp 'framework.zip'
  Write-Host "Descargando SSDD (Scrum-SDD) $version..."
  Invoke-WebRequest -Uri $url -OutFile $archive -UseBasicParsing
  Expand-Archive -LiteralPath $archive -DestinationPath $temp
  $root = Join-Path $temp ('scrum-sdd-' + $version.Substring(1))
  $installedVersion = (Get-Content -Raw (Join-Path $root 'VERSION')).Trim()
  if ($installedVersion -ne $version.Substring(1)) { throw 'La versión descargada no coincide.' }
  & (Join-Path $root 'install-cli.ps1')
  if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) { throw 'El instalador local falló.' }
  Write-Host 'Instalación finalizada. Abre una terminal nueva y ejecuta ssdd doctor.'
} finally {
  Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue
}
