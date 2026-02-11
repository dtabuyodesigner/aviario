import sqlite3

DB_PATH = '/home/danito73/Documentos/AVIARIO/database/aviario.db'

def test_query():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        
        species_filter = "Canario"
        print(f"Testing query for species: {species_filter}")
        
        # Original Query
        sql = '''
            SELECT DISTINCT m.* 
            FROM mutaciones m
            JOIN variedad_mutaciones vm ON m.uuid = vm.mutacion_uuid
            JOIN variedades v ON vm.variedad_uuid = v.uuid
            JOIN especies e ON v.especie_uuid = e.uuid
            WHERE LOWER(e.nombre_comun) = LOWER(?)
            ORDER BY m.nombre
        '''
        
        cursor = conn.execute(sql, (species_filter,))
        rows = cursor.fetchall()
        
        print(f"Found {len(rows)} mutations.")
        for row in rows:
            print(dict(row))
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_query()
