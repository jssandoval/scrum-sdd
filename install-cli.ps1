# Uso: powershell -ExecutionPolicy Bypass -File .\install-cli.ps1
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = $null
if (Get-Command py -ErrorAction SilentlyContinue) { $python = 'py'; $pyArgs = @('-3') }
elseif (Get-Command python -ErrorAction SilentlyContinue) { $python = 'python'; $pyArgs = @() }
else { throw 'Se necesita Python 3.9+; no se requiere Node.js, uv ni paquetes adicionales.' }
& $python @pyArgs (Join-Path $root 'install-cli.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$bin = Join-Path $env:LOCALAPPDATA 'Programs\ssdd\bin'
$userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
if (($userPath -split ';') -notcontains $bin) {
  [Environment]::SetEnvironmentVariable('Path', (($userPath.TrimEnd(';') + ';' + $bin).TrimStart(';')), 'User')
  Write-Host 'PATH del usuario actualizado. Abre una nueva terminal para usar scrum-sdd.'
}
$env:Path += ';' + $bin
Write-Host 'Prueba con: ssdd doctor'
