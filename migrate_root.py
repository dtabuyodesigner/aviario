import sqlite3
import os

DB_PATH = 'aviario.db'

def migrate_root_db():
    print(f"Running migration on root DB: {DB_PATH}")
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    # Ensure tables exist first (in case init_db only created demo_test/aviario.db)
    # Actually, init_db.py inside demo_test creates 'aviario.db' in demo_test folder by default unless path is absolute.
    # But app.py looks in BASE_DIR.
    # Let's fix this mess by manually initializing the root DB properly.
    
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

if __name__ == '__main__':
    migrate_root_db()
