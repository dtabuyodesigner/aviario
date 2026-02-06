@echo off
setlocal
title Lanzador Proyecto Aviario

echo ==========================================
echo      PROYECTO AVIARIO - V1.0 (DEMO)
echo ==========================================
echo.

REM 0. Buscar Ejecutable Standalone (Prioridad)
if exist "dist\Aviario.exe" (
    echo [INFO] Ejecutable detectado.
    echo Iniciando version Standalone...
    start dist\Aviario.exe
    
    REM Esperar un poco a que arranque el servidor interno del exe
    timeout /t 5 /nobreak >nul
    echo [INFO] Abriendo navegador...
    start http://localhost:8080
    
    goto END
)

REM Si estamos en la raiz y el exe esta ahi
if exist "Aviario.exe" (
    echo [INFO] Ejecutable detectado.
    echo Iniciando version Standalone...
    start Aviario.exe
    
    timeout /t 5 /nobreak >nul
    echo [INFO] Abriendo navegador...
    start http://localhost:8080
    
    goto END
)


REM 1. Comprobar Python (Metodo Tradicional)
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado.
    echo.
    echo NO SE PUEDE INICIAR EL MODO DESARROLLADOR.
    echo.
    echo SOLUCION:
    echo 1. Ejecuta 'demo_test\crear_ejecutable.bat' en una maquina con Python
    echo    para crear una version portable.
    echo 2. O instala Python desde python.org
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
echo [INFO] Iniciando servidor (Modo Python)...
start /B python app.py > app_log.txt 2>&1

REM 4. Esperar un momento y abrir navegador
timeout /t 3 /nobreak >nul
echo [INFO] Abriendo navegador...
start http://localhost:8080

:END
echo.
echo ==========================================
echo    SISTEMA INICIADO
echo ==========================================
echo No cierres esta ventana mientras uses la aplicacion.
echo.
pause
