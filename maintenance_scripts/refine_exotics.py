import sqlite3

DB_PATH = 'database/aviario.db'

# Specific data from user table
exotic_data = [
    {
        'sci_name': 'Taeniopygia guttata',
        'common_name': 'Diamante mandarín',
        'category': 'Exótico',
        'continent': 'Oceanía',
        'incubation': 13,
        'ringing': 18
    },
    {
        'sci_name': 'Erythrura gouldiae',
        'common_name': 'Diamante de Gould',
        'category': 'Exótico',
        'continent': 'Oceanía',
        'incubation': 14,
        'ringing': 18
    },
    {
        'sci_name': 'Lonchura striata domestica',
        'common_name': 'Isabelita del Japón',
        'category': 'Exótico',
        'continent': 'Asia',
        'incubation': 14,
        'ringing': 18
    },
    {
        'sci_name': 'Padda oryzivora',
        'common_name': 'Diamante de Java',
        'category': 'Exótico',
        'continent': 'Asia',
        'incubation': 14,
        'ringing': 18
    },
    {
        'sci_name': 'Lonchura punctulata',
        'common_name': 'Capuchino tricolor',
        'category': 'Exótico',
        'continent': 'Asia',
        'incubation': 13,
        'ringing': 18
    }
]

def refine_exotics():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    count = 0
    for bird in exotic_data:
        # Check by scientific name first as common name might have changed
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
            # If not found (unlikely), insert it
            import uuid
            cur.execute("""
                INSERT INTO especies (nombre_comun, nombre_cientifico, categoria, continente, dias_incubacion, dias_anillado, uuid)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (bird['common_name'], bird['sci_name'], bird['category'], bird['continent'], bird['incubation'], bird['ringing'], str(uuid.uuid4())))
            count += 1
            
    conn.commit()
    conn.close()
    print(f"Refined {count} exotic species.")

if __name__ == "__main__":
    refine_exotics()
