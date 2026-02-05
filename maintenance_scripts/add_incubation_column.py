import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'aviario.db')

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    try:
        # Check if column exists
        cur.execute("PRAGMA table_info(nidadas)")
        columns = [column[1] for column in cur.fetchall()]
        
        if 'fecha_inicio_incubacion' not in columns:
            print("Adding 'fecha_inicio_incubacion' to 'nidadas' table...")
            cur.execute("ALTER TABLE nidadas ADD COLUMN fecha_inicio_incubacion DATE")
            conn.commit()
            print("Migration successful.")
        else:
            print("Column 'fecha_inicio_incubacion' already exists.")
            
    except sqlite3.Error as e:
        print(f"Error during migration: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
