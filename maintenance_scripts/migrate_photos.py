import sqlite3
import os

DB_PATH = 'aviario.db'

def migrate_photos():
    if not os.path.exists(DB_PATH):
        print("Database not found, skipping migration.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("Starting photo migration...")
    
    try:
        # Check if column exists
        cur.execute("PRAGMA table_info(pajaros)")
        columns = [info[1] for info in cur.fetchall()]
        
        if 'foto_path' in columns:
            print("'foto_path' already exists. Skipping.")
            return

        # Add column
        cur.execute("ALTER TABLE pajaros ADD COLUMN foto_path TEXT")
        
        conn.commit()
        print("Migration successful: Added 'foto_path' to pajaros table.")
        
    except Exception as e:
        conn.rollback()
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_photos()
