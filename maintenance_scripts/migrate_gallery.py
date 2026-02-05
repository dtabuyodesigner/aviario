import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'aviario.db')

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        print("Migrating Database: Adding bird_photos table...")
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bird_photos'")
        if cursor.fetchone():
            print("Table 'bird_photos' already exists.")
        else:
            cursor.execute('''
                CREATE TABLE bird_photos (
                    id_photo INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_bird INTEGER NOT NULL,
                    file_path TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(id_bird) REFERENCES birds(id_ave) ON DELETE CASCADE
                )
            ''')
            print("Table 'bird_photos' created successfully.")
            
        conn.commit()
        print("Migration complete.")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
