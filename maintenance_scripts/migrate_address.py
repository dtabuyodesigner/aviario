import sqlite3
import os

DB_PATH = 'aviario.db'

def migrate_address():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        # Add new columns if they don't exist
        columns = ['direccion_calle', 'direccion_poblacion', 'direccion_provincia', 'direccion_cp']
        
        # Check existing columns
        cur.execute("PRAGMA table_info(configuracion)")
        existing = [row[1] for row in cur.fetchall()]

        for col in columns:
            if col not in existing:
                print(f"Adding column {col}...")
                cur.execute(f"ALTER TABLE configuracion ADD COLUMN {col} TEXT")
        
        print("Migration complete.")
        conn.commit()
    except Exception as e:
        print(f"Error migrating: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_address()
