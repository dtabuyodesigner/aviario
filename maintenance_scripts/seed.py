import sqlite3
import os

DB_PATH = 'aviario.db'
SCHEMA_PATH = 'database/schema.sql'

def reset_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Eliminada base de datos anterior: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    
    # 1. Crear Tablas
    with open(SCHEMA_PATH, 'r') as f:
        conn.executescript(f.read())
    print("Tablas creadas correctamente.")

    # 2. Insertar Pájaros de Prueba
    birds = [
        ('E2-001', 1, 'Ancestral', 'M', 2024, 'Activo', 'Propio'),
        ('E2-002', 2, 'Lutino', 'H', 2025, 'Activo', 'Propio'),
        ('E2-003', 3, 'Azul DD', 'M', 2024, 'Activo', 'Externo')
    ]
    
    sql = '''
        INSERT INTO pajaros (
            anilla, id_especie, mutacion_visual, sexo, anio_nacimiento, estado, origen
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    
    try:
        cur = conn.cursor()
        cur.executemany(sql, birds)
        conn.commit()
        print(f"Insertados {cur.rowcount} pájaros de prueba.")
    except sqlite3.Error as e:
        print(f"Error insertando datos: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    reset_db()
