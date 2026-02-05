#!/bin/bash

# Aviario Launcher

echo "🐦 Iniciando Proyecto Aviario..."

# 1. Comprobar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado."
    echo "Por favor, instala Python 3 desde https://width.python.org/downloads/"
    read -p "Presiona Enter para salir..."
    exit 1
fi

# 2. Configurar entorno virtual
if [ ! -d "venv" ]; then
    echo "⚙️  Creando entorno virtual..."
    python3 -m venv venv
    
    echo "📦 Instalando dependencias..."
    source venv/bin/activate
    pip install -r requirements.txt
    
    echo "🗄️  Inicializando base de datos..."
    python3 init_db.py
else
    source venv/bin/activate
fi

# 3. Iniciar Servidor en segundo plano
echo "🚀 Arrancando servidor..."
python3 app.py > app_log.txt 2>&1 &
SERVER_PID=$!

# Esperar unos segundos a que arranque
sleep 2

# 4. Abrir navegador
echo "🌐 Abriendo navegador..."
URL="http://localhost:8080"

if command -v xdg-open &> /dev/null; then
    xdg-open "$URL"
elif command -v brave-browser &> /dev/null; then
    brave-browser "$URL"
elif command -v google-chrome &> /dev/null; then
    google-chrome "$URL"
elif command -v firefox &> /dev/null; then
    firefox "$URL"
elif command -v start &> /dev/null; then
    start "$URL" # Windows/WSL
else
    echo "⚠️  No se pudo abrir el navegador automáticamente."
fi

echo ""
echo "============================================="
echo "   ✅ SERVIDOR LISTO Y CORRIENDO"
echo "============================================="
echo "👉 Si no se abrió el navegador, entra en:"
echo ""
echo "   $URL"
echo ""
echo "============================================="
echo "⚠️  Cierra esta ventana para detener el programa."

wait $SERVER_PID
