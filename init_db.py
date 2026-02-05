import sqlite3
import os

DB_PATH = 'aviario.db'
SCHEMA_PATH = os.path.join('database', 'schema.sql')

def init_db():
    try:
        if os.path.exists(DB_PATH):
            print(f"⚠️  La base de datos '{DB_PATH}' ya existe.")
            # Opcional: preguntar si borrar. Para demo de distribución, mejor no destruir si ya existe.
            # Pero si es primera instalación limpia, no existe.
        
        print("⚙️  Inicializando base de datos...")
        connection = sqlite3.connect(DB_PATH)
        
        with open(SCHEMA_PATH) as f:
            connection.executescript(f.read())
            
        # Crear tabla de usuarios si no existe (opcional, por si la demo lo requiere)
        # connection.execute("...")
        
        connection.commit()
        connection.close()
        print("✅ Base de datos creada correctamente.")
        
    except Exception as e:
        print(f"❌ Error inicializando BD: {e}")

if __name__ == '__main__':
    init_db()
