import sqlite3
import uuid

DB_PATH = 'database/aviario.db'

# Specific data from user table for European Fauna
fauna_data = [
    {
        'sci_name': 'Carduelis carduelis',
        'common_name': 'Jilguero',
        'category': 'Fauna europea',
        'continent': 'Europa',
        'incubation': 13,
        'ringing': 20
    },
    {
        'sci_name': 'Chloris chloris',
        'common_name': 'Verderón',
        'category': 'Fauna europea',
        'continent': 'Europa',
        'incubation': 13,
        'ringing': 20
    },
    {
        'sci_name': 'Serinus serinus',
        'common_name': 'Verdecillo',
        'category': 'Fauna europea',
        'continent': 'Europa',
        'incubation': 13,
        'ringing': 20
    },
    {
        'sci_name': 'Spinus spinus',
        'common_name': 'Lúgano',
        'category': 'Fauna europea',
        'continent': 'Europa',
        'incubation': 13,
        'ringing': 20
    }
]

def refine_fauna():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    count = 0
    for bird in fauna_data:
        # Check by scientific name
        cur.execute("SELECT id_especie FROM especies WHERE nombre_cientifico = ?", (bird['sci_name'],))
        row = cur.fetchone()
        
        if row:
            cur.execute("""
                UPDATE especies SET 
                    nombre_comun = ?,
                    categoria = ?,
                    continente = ?,
                    dias_incubacion = ?,
                    dias_anillado = ?
                WHERE id_especie = ?
            """, (bird['common_name'], bird['category'], bird['continent'], bird['incubation'], bird['ringing'], row[0]))
            count += 1
        else:
            # If not found, insert it
            cur.execute("""
                INSERT INTO especies (nombre_comun, nombre_cientifico, categoria, continente, dias_incubacion, dias_anillado, uuid)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (bird['common_name'], bird['sci_name'], bird['category'], bird['continent'], bird['incubation'], bird['ringing'], str(uuid.uuid4())))
            count += 1
            
    conn.commit()
    conn.close()
    print(f"Refined {count} European fauna species.")

if __name__ == "__main__":
    refine_fauna()
