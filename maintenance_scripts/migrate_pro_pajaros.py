import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'aviario.db')

def migrate():
    print(f"Migrating database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Columns to add
    cols = [
        ("reservado", "BOOLEAN DEFAULT 0"),
        ("fecha_salida", "DATE"),
        ("motivo_salida", "TEXT"),
        ("id_contacto_salida", "INTEGER"),
        ("precio", "REAL DEFAULT 0")
    ]
    
    for col_name, col_type in cols:
        try:
            print(f"Adding column {col_name}...")
            cur.execute(f"ALTER TABLE pajaros ADD COLUMN {col_name} {col_type}")
            print(f"Column {col_name} added successfully.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"Column {col_name} already exists. Skipping.")
            else:
                print(f"Error adding {col_name}: {e}")
                
    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
