@echo off
setlocal
title Lanzador Proyecto Aviario

echo ==========================================
echo      PROYECTO AVIARIO - V1.0 (DEMO)
echo ==========================================
echo.

REM 1. Comprobar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado.
    echo Por favor, instala Python desde la Microsoft Store o python.org
    echo.
    pause
    exit /b
)

REM 2. Crear entorno virtual si no existe
if not exist "venv" (
    echo [INFO] Creando entorno virtual...
    python -m venv venv
    
    echo [INFO] Activando entorno...
    call venv\Scripts\activate.bat
    
    echo [INFO] Instalando dependencias...
    pip install flask flask-cors
    
    echo [INFO] Inicializando base de datos...
    python init_db.py
) else (
    call venv\Scripts\activate.bat
)

REM 3. Iniciar servidor en segundo plano
echo.
echo [INFO] Iniciando servidor...
start /B python app.py > app_log.txt 2>&1

REM 4. Esperar un momento y abrir navegador
timeout /t 3 /nobreak >nul
echo [INFO] Abriendo navegador...
start http://localhost:8080

echo.
echo ==========================================
echo    SISTEMA FUNCIONANDO CORRECTAMENTE
echo ==========================================
echo No cierres esta ventana mientras uses la aplicacion.
echo.
pause
