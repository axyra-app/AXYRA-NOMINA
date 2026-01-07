# Script para ejecutar el servidor backend
Write-Host "[STARTUP] Iniciando Sistema de Nomina Backend..." -ForegroundColor Green
Write-Host "[INFO] Puerto: 8000" -ForegroundColor Cyan
Write-Host "[INFO] Host: 0.0.0.0" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del backend
Set-Location $PSScriptRoot

# Ejecutar el servidor
python main.py
