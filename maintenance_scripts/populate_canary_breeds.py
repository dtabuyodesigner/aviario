import sqlite3
import uuid

DB_PATH = 'database/aviario.db'

# Full catalog from user tables
canary_breeds = [
    # Color
    {'raza': 'Canario rojo', 'tipo': 'Color'},
    {'raza': 'Canario amarillo', 'tipo': 'Color'},
    {'raza': 'Canario mosaico', 'tipo': 'Color'},
    {'raza': 'Canario melánico', 'tipo': 'Color'},
    # Canto
    {'raza': 'Harz Roller', 'tipo': 'Canto'},
    {'raza': 'Malinois', 'tipo': 'Canto'},
    {'raza': 'Timbrado español', 'tipo': 'Canto'},
    {'raza': 'Waterslager', 'tipo': 'Canto'},
    # Postura
    {'raza': 'Gloster', 'tipo': 'Postura'},
    {'raza': 'Yorkshire', 'tipo': 'Postura'},
    {'raza': 'Border', 'tipo': 'Postura'},
    {'raza': 'Fife Fancy', 'tipo': 'Postura'},
    {'raza': 'Lizard', 'tipo': 'Postura'},
    {'raza': 'Norwich', 'tipo': 'Postura'},
    {'raza': 'Lancashire', 'tipo': 'Postura'},
    {'raza': 'Rizado parisino', 'tipo': 'Postura'},
    {'raza': 'Padovano', 'tipo': 'Postura'},
    {'raza': 'Gibber Italicus', 'tipo': 'Postura'}
]

def populate_breeds():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Get Canario ID
    cur.execute("SELECT id_especie FROM especies WHERE nombre_comun = 'Canario' OR nombre_comun = 'Domestic Canary'")
    row = cur.fetchone()
    if not row:
        print("Error: Especie 'Canario' no encontrada.")
        return
    
    canario_id = row[0]
    count = 0
    
    for breed in canary_breeds:
        # Avoid duplicates by name and species
        cur.execute("SELECT id FROM canary_breeds WHERE nombre_raza = ? AND id_especie = ?", (breed['raza'], canario_id))
        if not cur.fetchone():
            breed_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO canary_breeds (id, id_especie, nombre_raza, tipo)
                VALUES (?, ?, ?, ?)
            """, (breed_id, canario_id, breed['raza'], breed['tipo']))
            count += 1
            
    conn.commit()
    conn.close()
    print(f"Added/Verified {len(canary_breeds)} canary breeds. {count} new breeds inserted.")

if __name__ == "__main__":
    populate_breeds()
