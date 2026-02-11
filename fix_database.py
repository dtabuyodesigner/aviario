import sqlite3
import os

DB_PATH = 'database/aviario.db'

def patch_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("Checking 'especies' for timestamps...")
    try:
        cur.execute("SELECT created_at FROM especies LIMIT 1")
        print(" - 'created_at' exists.")
    except sqlite3.OperationalError:
        print(" - Adding 'created_at'...")
        cur.execute("ALTER TABLE especies ADD COLUMN created_at TEXT")
        
    try:
        cur.execute("SELECT updated_at FROM especies LIMIT 1")
        print(" - 'updated_at' exists.")
    except sqlite3.OperationalError:
        print(" - Adding 'updated_at'...")
        cur.execute("ALTER TABLE especies ADD COLUMN updated_at TEXT")

    # While we are here, let's check sync_version too as per requirements
    try:
        cur.execute("SELECT sync_version FROM especies LIMIT 1")
    except sqlite3.OperationalError:
        print(" - Adding 'sync_version'...")
        cur.execute("ALTER TABLE especies ADD COLUMN sync_version INTEGER DEFAULT 1")
        
    conn.commit()
    conn.close()
    print("Database patched.")

if __name__ == '__main__':
    patch_db()
