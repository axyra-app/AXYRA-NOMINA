#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Sistema de Nómina - Dev Environment Setup
.DESCRIPTION
    Inicializa todas las dependencias y prepara el ambiente de desarrollo
    para el Sistema de Nómina (Backend + Frontend)
.AUTHOR
    Dev Team
.VERSION
    1.0.0
#>

param(
    [switch]$AutoStart = $false,
    [switch]$BackendOnly = $false,
    [switch]$FrontendOnly = $false,
    [switch]$SkipInstall = $false,
    [int]$BackendPort = 8000,
    [int]$FrontendPort = 5173
)

# Configurar colores
function Write-Header { Write-Host "================================================" -ForegroundColor Cyan }
function Write-Title { param([string]$Text) Write-Host $Text -ForegroundColor Cyan -BackgroundColor Black }
function Write-Success { param([string]$Text) Write-Host "✓ $Text" -ForegroundColor Green }
function Write-Error { param([string]$Text) Write-Host "✗ $Text" -ForegroundColor Red }
function Write-Warning { param([string]$Text) Write-Host "! $Text" -ForegroundColor Yellow }
function Write-Info { param([string]$Text) Write-Host "→ $Text" -ForegroundColor Cyan }

Clear-Host
Write-Header
Write-Title "  SISTEMA DE NÓMINA AXYRA - SETUP"
Write-Header
Write-Host ""

# Obtener ruta del script
$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Info "Raíz del proyecto: $PROJECT_ROOT"

# Verificar estructura
Write-Info "Verificando estructura de directorios..."
if (-not (Test-Path "$PROJECT_ROOT\backend")) {
    Write-Error "Carpeta 'backend' no encontrada"
    exit 1
}
if (-not (Test-Path "$PROJECT_ROOT\frontend")) {
    Write-Error "Carpeta 'frontend' no encontrada"
    exit 1
}
Write-Success "Estructura de directorios correcta"
Write-Host ""

# Verificar herramientas requeridas
Write-Title "VERIFICANDO HERRAMIENTAS REQUERIDAS"
Write-Host ""

# Python
Write-Info "Buscando Python..."
try {
    $pythonVersion = python --version 2>&1
    Write-Success $pythonVersion
} catch {
    Write-Error "Python no está instalado o no está en PATH"
    exit 1
}

# Node.js
Write-Info "Buscando Node.js..."
try {
    $nodeVersion = node --version
    Write-Success "Node.js $nodeVersion"
} catch {
    Write-Error "Node.js no está instalado"
    exit 1
}

# npm
Write-Info "Buscando npm..."
try {
    $npmVersion = npm --version
    Write-Success "npm $npmVersion"
} catch {
    Write-Error "npm no está instalado"
    exit 1
}
Write-Host ""

# Instalar dependencias
if (-not $SkipInstall) {
    Write-Title "INSTALANDO DEPENDENCIAS"
    Write-Host ""
    
    # Backend
    if (-not $FrontendOnly) {
        Write-Info "[1/2] Backend - pip install"
        Push-Location "$PROJECT_ROOT\backend"
        
        if (Test-Path "requirements.txt") {
            pip install -q -r requirements.txt
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Dependencias de backend instaladas"
            } else {
                Write-Error "Error instalando dependencias de backend"
                exit 1
            }
        } else {
            Write-Warning "requirements.txt no encontrado"
        }
        
        Pop-Location
    }
    
    # Frontend
    if (-not $BackendOnly) {
        Write-Info "[2/2] Frontend - npm install"
        Push-Location "$PROJECT_ROOT\frontend"
        
        if (-not (Test-Path "node_modules")) {
            Write-Warning "Primera instalación - puede tardar 2-3 minutos"
            npm install --legacy-peer-deps
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Dependencias de frontend instaladas"
            } else {
                Write-Error "Error instalando dependencias de frontend"
                exit 1
            }
        } else {
            Write-Success "node_modules ya existe"
        }
        
        Pop-Location
    }
    
    Write-Host ""
}

# Verificar .env files
Write-Title "VERIFICANDO CONFIGURACIÓN"
Write-Host ""

$backendEnv = "$PROJECT_ROOT\backend\.env"
$frontendEnv = "$PROJECT_ROOT\frontend\.env"

if (Test-Path $backendEnv) {
    Write-Success "backend\.env encontrado"
} else {
    Write-Warning "backend\.env no encontrado - copiar de .env.example si existe"
}

if (Test-Path $frontendEnv) {
    Write-Success "frontend\.env encontrado"
} else {
    Write-Warning "frontend\.env no encontrado - copiar de .env.example si existe"
}
Write-Host ""

# Mostrar instrucciones
Write-Header
Write-Title "  CONFIGURACIÓN COMPLETADA"
Write-Header
Write-Host ""

Write-Info "Para iniciar el ambiente de desarrollo:"
Write-Host ""

if (-not $FrontendOnly) {
    Write-Title "TERMINAL 1 - BACKEND"
    Write-Host "  cd backend" -ForegroundColor Green
    Write-Host "  python main.py" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Backend estará en: http://localhost:$BackendPort" -ForegroundColor Yellow
    Write-Host ""
}

if (-not $BackendOnly) {
    Write-Title "TERMINAL 2 - FRONTEND"
    Write-Host "  cd frontend" -ForegroundColor Green
    Write-Host "  npm run dev" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Frontend estará en: http://localhost:$FrontendPort" -ForegroundColor Yellow
    Write-Host ""
}

Write-Info "Notas importantes:"
Write-Host "  • Ambos servidores deben ejecutarse simultáneamente" -ForegroundColor White
Write-Host "  • El backend debe estar corriendo antes de usar el frontend" -ForegroundColor White
Write-Host "  • Para desarrollo, mantén ambos servidores activos" -ForegroundColor White
Write-Host "  • Los cambios se recargan automáticamente (HMR)" -ForegroundColor White
Write-Host ""

# Opción de iniciar automáticamente
if ($AutoStart) {
    Write-Warning "Iniciando servidores automáticamente..."
    Write-Host ""
    
    if (-not $FrontendOnly) {
        Write-Info "Abriendo Backend en nueva ventana..."
        Start-Process pwsh -ArgumentList "-NoExit -Command `"cd '$PROJECT_ROOT\backend'; python main.py`"" `
            -WindowStyle Normal
        Start-Sleep -Seconds 2
    }
    
    if (-not $BackendOnly) {
        Write-Info "Abriendo Frontend en nueva ventana..."
        Start-Process pwsh -ArgumentList "-NoExit -Command `"cd '$PROJECT_ROOT\frontend'; npm run dev`"" `
            -WindowStyle Normal
    }
    
    Write-Success "Servidores iniciados. Las ventanas se abrieron."
}

Write-Host ""
Write-Header
Write-Success "¡Setup completado!"
Write-Header
Write-Host ""

# Mantener ventana abierta si se ejecutó desde explorer
Read-Host "Presiona Enter para salir"
