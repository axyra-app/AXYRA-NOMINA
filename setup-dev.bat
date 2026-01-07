@echo off
REM Script para iniciar Backend y Frontend del Sistema de Nómina

setlocal enabledelayedexpansion

REM Definir colores para output (PowerShell)
set "BLUE=[94m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "RESET=[0m"

echo.
echo %BLUE%================================================%RESET%
echo %BLUE%   SISTEMA DE NOMINA - STARTUP%RESET%
echo %BLUE%================================================%RESET%
echo.

REM Obtener ruta del proyecto
set "PROJECT_ROOT=%~dp0"
echo %YELLOW%Raíz del proyecto: %PROJECT_ROOT%%RESET%
echo.

REM Verificar que estamos en el directorio correcto
if not exist "%PROJECT_ROOT%backend" (
    echo %RED%ERROR: Carpeta 'backend' no encontrada%RESET%
    exit /b 1
)

if not exist "%PROJECT_ROOT%frontend" (
    echo %RED%ERROR: Carpeta 'frontend' no encontrada%RESET%
    exit /b 1
)

echo %GREEN%✓ Estructura de directorios verificada%RESET%
echo.

REM Verificar Python
echo %YELLOW%Verificando Python...%RESET%
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%ERROR: Python no está instalado o no está en PATH%RESET%
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo %GREEN%✓ %PYTHON_VERSION% encontrado%RESET%

REM Verificar Node.js
echo %YELLOW%Verificando Node.js...%RESET%
node --version >nul 2>&1
if errorlevel 1 (
    echo %RED%ERROR: Node.js no está instalado o no está en PATH%RESET%
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo %GREEN%✓ Node.js %NODE_VERSION% encontrado%RESET%

REM Verificar npm
echo %YELLOW%Verificando npm...%RESET%
npm --version >nul 2>&1
if errorlevel 1 (
    echo %RED%ERROR: npm no está instalado%RESET%
    exit /b 1
)
for /f "tokens=*" %%i in ('npm --version') do set NPM_VERSION=%%i
echo %GREEN%✓ npm %NPM_VERSION% encontrado%RESET%
echo.

REM Opción: Instalar dependencias
echo %YELLOW%Instalando/Actualizando dependencias...%RESET%
echo.

REM Backend
echo %BLUE%[1/2] Backend - pip install%RESET%
cd /d "%PROJECT_ROOT%backend"
if exist "requirements.txt" (
    pip install -q -r requirements.txt
    if errorlevel 1 (
        echo %RED%✗ Error instalando dependencias de backend%RESET%
        exit /b 1
    )
    echo %GREEN%✓ Dependencias de backend instaladas%RESET%
) else (
    echo %YELLOW%! requirements.txt no encontrado%RESET%
)

REM Frontend
echo %BLUE%[2/2] Frontend - npm install%RESET%
cd /d "%PROJECT_ROOT%frontend"
if not exist "node_modules" (
    echo %YELLOW%Primera vez - npm install puede tardar 2-3 minutos%RESET%
    npm install --legacy-peer-deps
    if errorlevel 1 (
        echo %RED%✗ Error instalando dependencias de frontend%RESET%
        exit /b 1
    )
    echo %GREEN%✓ Dependencias de frontend instaladas%RESET%
) else (
    echo %GREEN%✓ node_modules ya existe%RESET%
)
echo.

REM Instrucciones finales
echo %BLUE%================================================%RESET%
echo %BLUE%   PROXIMOS PASOS%RESET%
echo %BLUE%================================================%RESET%
echo.
echo Para iniciar los servidores, abre DOS terminales:
echo.
echo %GREEN%Terminal 1 - BACKEND:%RESET%
echo   cd backend
echo   python main.py
echo.
echo   Backend estará en: %GREEN%http://localhost:8000%RESET%
echo.
echo %GREEN%Terminal 2 - FRONTEND:%RESET%
echo   cd frontend
echo   npm run dev
echo.
echo   Frontend estará en: %GREEN%http://localhost:5173%RESET%
echo.
echo %YELLOW%NOTA:%RESET%
echo   - Backend debe estar corriendo antes de usar el frontend
echo   - Para desarrollo, mantén ambos servidores activos
echo   - Los cambios se recargan automáticamente (HMR)
echo.
echo %BLUE%================================================%RESET%
echo %GREEN%✓ Configuración completada!%RESET%
echo %BLUE%================================================%RESET%
echo.

REM Opción: Ejecutar automáticamente (comentado por defecto)
REM echo %YELLOW%Iniciando servidores automáticamente...%RESET%
REM 
REM start "Backend - Sistema de Nómina" cmd /k "cd backend && python main.py"
REM timeout /t 2 /nobreak
REM start "Frontend - Sistema de Nómina" cmd /k "cd frontend && npm run dev"

pause
