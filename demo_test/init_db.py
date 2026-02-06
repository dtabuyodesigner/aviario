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
        
        with open(SCHEMA_PATH, encoding='utf-8') as f:
            connection.executescript(f.read())
            
        # Crear tabla de usuarios si no existe (opcional, por si la demo lo requiere)
        # connection.execute("...")
        
        connection.commit()
        # connection.close() -- Keeping open for migration check below
        # MIGRACIÓN AUTOMÁTICA (Para añadir columnas nuevas sin borrar datos)
        # Check for new columns in 'pajaros'
        # Re-open or reuse connection? It is still open now.
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(pajaros)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'precio_compra' not in columns:
            print("⚠️ Aplicando migración: Añadiendo columnas de compra a 'pajaros'...")
            try:
                cursor.execute("ALTER TABLE pajaros ADD COLUMN precio_compra REAL DEFAULT 0")
                cursor.execute("ALTER TABLE pajaros ADD COLUMN fecha_compra DATE")
                cursor.execute("ALTER TABLE pajaros ADD COLUMN tipo_compra TEXT")
                print("✅ Migración completada.")
            except Exception as e:
                print(f"❌ Error en migración: {e}")

        connection.commit()
        connection.close()
        print("✅ Base de datos verificada/actualizada.")
        
    except Exception as e:
        print(f"❌ Error inicializando BD: {e}")

if __name__ == '__main__':
    init_db()
