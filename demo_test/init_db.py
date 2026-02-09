import sqlite3
import uuid
from datetime import datetime

DB_NAME = "aviario.db"

def now():
    return datetime.utcnow().isoformat()

def new_uuid():
    return str(uuid.uuid4())

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # ================= USERS =================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        nombre TEXT,
        email TEXT,
        password_hash TEXT,
        created_at TEXT,
        updated_at TEXT,
        deleted_at TEXT
    )
    """)

    # Usuario inicial
    user_id = new_uuid()
    cursor.execute("""
    INSERT OR IGNORE INTO users 
    (id, nombre, email, created_at)
    VALUES (?, ?, ?, ?)
    """, (user_id, "Usuario Principal", "local@aviario", now()))

    # ================= EVENTS =================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id TEXT PRIMARY KEY,
        entity_type TEXT,
        entity_id TEXT,
        event_type TEXT,
        event_date TEXT,
        estimated_date TEXT,
        owner_id TEXT,
        created_at TEXT,
        updated_at TEXT,
        deleted_at TEXT
    )
    """)

    # ================= QR =================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qr_entities (
        id TEXT PRIMARY KEY,
        entity_type TEXT,
        entity_id TEXT,
        qr_code TEXT,
        created_at TEXT
    )
    """)

    # ================= OWNERSHIP =================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bird_ownership_history (
        id TEXT PRIMARY KEY,
        bird_id TEXT,
        owner_id TEXT,
        start_date TEXT,
        end_date TEXT,
        transfer_type TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()

