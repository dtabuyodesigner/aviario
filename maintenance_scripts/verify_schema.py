import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'aviario.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(pajaros)")
columns = cursor.fetchall()

print("Columns in pajaros:")
for col in columns:
    print(f"{col[1]} ({col[2]})")

conn.close()
