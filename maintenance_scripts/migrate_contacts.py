import sqlite3
import os

DB_PATH = 'aviario.db'

def migrate():
    if not os.path.exists(DB_PATH):
        print("Database not found, skipping migration.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("Starting migration...")
    
    try:
        # 1. Rename existing table
        cur.execute("ALTER TABLE contactos RENAME TO contactos_old")
        
        # 2. Create new table with updated constraint
        cur.execute("""
            CREATE TABLE contactos (
                id_contacto INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT CHECK(tipo IN ('Comprador', 'Vendedor', 'Veterinario', 'Otro', 'Criador')),
                nombre_razon_social TEXT NOT NULL,
                dni_cif TEXT,
                n_criador TEXT,
                telefono TEXT,
                email TEXT,
                direccion TEXT,
                observaciones TEXT
            )
        """)
        
        # 3. Copy data
        cur.execute("""
            INSERT INTO contactos (id_contacto, tipo, nombre_razon_social, dni_cif, n_criador, telefono, email, direccion, observaciones)
            SELECT 
                id_contacto, 
                tipo, 
                nombre_razon_social, 
                dni_cif, 
                CASE WHEN n_criador IS NOT NULL AND n_criador != '' THEN n_criador ELSE numero_criador END, 
                telefono, 
                email, 
                direccion, 
                observaciones
            FROM contactos_old
        """)
        
        # 4. Drop old table
        cur.execute("DROP TABLE contactos_old")
        
        conn.commit()
        print("Migration successful: Added 'Criador' to contact type constraint.")
        
    except Exception as e:
        conn.rollback()
        print(f"Migration failed: {e}")
        # Attempt to restore if things went halfway (simple check)
        try:
            cur.execute("DROP TABLE IF EXISTS contactos")
            cur.execute("ALTER TABLE contactos_old RENAME TO contactos")
            conn.commit()
            print("Rolled back changes.")
        except:
            pass
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
