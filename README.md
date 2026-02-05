# 🐦 Proyecto Aviario

Sistema de gestión integral para criadores de aves, desarrollado con Flask y JavaScript vanilla.

## 📋 Características

### Módulos Principales
- **Gestión de Pájaros**: Inventario completo con fotos, genética, y seguimiento
- **Cría**: Control de nidos, puestas y desarrollo de polluelos
- **Contactos**: Gestión de criadores, clientes y proveedores
- **Salud**: Registro de tratamientos y vacunaciones
- **Economía**: Control de gastos e ingresos
- **Calendario**: Planificación de tareas y eventos
- **Genética**: Calculadora de mutaciones y genealogía

### Funcionalidades PRO
- ✅ Badges de disponibilidad (DISPONIBLE / RESERVADO)
- ✅ Gestión de precios
- ✅ Historial de movimientos
- ✅ Filtros avanzados
- ✅ Búsqueda en tiempo real

## 🚀 Instalación

### Requisitos
- Python 3.8+
- Flask
- SQLite3

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/TU_USUARIO/AVIARIO.git
cd AVIARIO
```

2. **Crear entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias**
```bash
pip install flask
```

4. **Inicializar la base de datos**
```bash
python3 init_db.py
```

5. **Ejecutar la aplicación**
```bash
python3 app.py
```

6. **Abrir en el navegador**
```
http://localhost:8080
```

## 📁 Estructura del Proyecto

```
AVIARIO/
├── app.py                 # Servidor Flask principal
├── init_db.py            # Script de inicialización de BD
├── aviario.db            # Base de datos SQLite (no incluida en git)
├── index.html            # Página principal
├── css/
│   └── styles.css        # Estilos globales
├── js/
│   ├── app.js           # Aplicación principal
│   ├── core/
│   │   ├── db.js        # Gestión de base de datos
│   │   └── router.js    # Sistema de rutas
│   └── modules/
│       ├── birds.js     # Módulo de pájaros
│       ├── breeding.js  # Módulo de cría
│       ├── contacts.js  # Módulo de contactos
│       └── ...
└── uploads/             # Fotos de pájaros (no incluido en git)
```

## 🔧 Tecnologías

- **Backend**: Python Flask
- **Frontend**: JavaScript ES6+ (Vanilla)
- **Base de datos**: SQLite3
- **Estilos**: CSS3 con variables CSS

## 📝 Notas de Desarrollo

### Base de Datos
La base de datos `aviario.db` NO está incluida en el repositorio por seguridad. Se creará automáticamente al ejecutar `init_db.py`.

### Fotos
Las fotos de los pájaros se almacenan en `/uploads/` y tampoco están en el repositorio.

## 🤝 Contribuir

Este es un proyecto personal, pero si encuentras bugs o tienes sugerencias, siéntete libre de abrir un issue.

## 📄 Licencia

Proyecto de uso personal.

## ✨ Créditos

Desarrollado por [Tu Nombre]
