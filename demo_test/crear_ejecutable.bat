@echo off
title Imprimir Ejecutable - Proyecto Aviario
echo ==========================================
echo    CREACION DE EJECUTABLE (SOLO WINDOWS)
echo ==========================================
echo.
echo NOTA: Para CREAR el ejecutable, este ordenador NECESITA tener Python instalado.
echo Una vez creado, el archivo .exe funcionara en cualquier ordenador sin Python.
echo.

REM 1. Comprobar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado.
    echo.
    echo Para GENERAR el ejecutable, necesitas instalar Python en este ordenador.
    echo Por favor:
    echo 1. Ve a https://www.python.org/downloads/
    echo 2. Descarga e instala Python.
    echo 3. IMPORTANTE: Marca la casilla "Add Python to PATH" al instalar.
    echo 4. Vuelve a ejecutar este archivo.
    echo.
    pause
    exit /b
)

REM 2. Comprobar/Crear entorno virtual
if not exist "..\venv" (
    echo [INFO] No se encontro entorno virtual. Creandolo para la compilacion...
    
    python -m venv ..\venv
    if %errorlevel% neq 0 (
        echo [ERROR] Fallo al crear el entorno virtual.
        pause
        exit /b
    )
    
    echo [INFO] Activando entorno...
    call ..\venv\Scripts\activate.bat
    
    echo [INFO] Instalando dependencias necesarias...
    pip install flask flask-cors pyinstaller
    
    echo [INFO] Inicializando base de datos...
    pushd ..
    python init_db.py
    popd
) else (
    echo [INFO] Usando entorno virtual existente...
    call ..\venv\Scripts\activate.bat
    
    echo [INFO] Asegurando que PyInstaller este instalado...
    pip install pyinstaller
)

REM 3. Crear Ejecutable
echo.
echo [INFO] Creando ejecutable...
echo Esto puede tardar unos minutos...
echo.

pyinstaller --noconfirm --onefile --windowed --name "Aviario" ^
    --add-data "..\index.html;." ^
    --add-data "..\css;css" ^
    --add-data "..\js;js" ^
    --add-data "..\database;database" ^
    --add-data "..\genetics_engine.py;." ^
    --add-data "..\genetics_api.py;." ^
    --add-data "..\genetics_db.py;." ^
    --hidden-import engineio.async_drivers.threading ^
    ..\app.py

echo.
echo ==========================================
echo    PROCESO COMPLETADO
echo ==========================================
echo.
if exist "dist\Aviario.exe" (
    echo [EXITO] El ejecutable se ha creado en la carpeta 'dist'.
    echo.
    echo AHORA:
    echo 1. Si ejecutas 'iniciar_aviario.bat', usara este nuevo ejecutable.
    echo 2. Puedes copiar toda la carpeta 'demo_test' a otro PC sin Python y funcionara.
) else (
    echo [ERROR] Algo fallo. Revisa los mensajes de error arriba.
)
echo.
pause
