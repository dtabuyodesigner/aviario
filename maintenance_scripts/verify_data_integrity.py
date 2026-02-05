import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'aviario.db')

def debug_data():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    print("--- NIDADAS (Raw) ---")
    nidadas = cur.execute("SELECT * FROM nidadas").fetchall()
    for n in nidadas:
        print(dict(n))

    print("\n--- CRUCES (Raw) ---")
    cruces = cur.execute("SELECT * FROM cruces").fetchall()
    for c in cruces:
        print(dict(c))
        
    print("\n--- PAJAROS (Sample) ---")
    birds = cur.execute("SELECT id_ave, anilla, especie, id_especie FROM pajaros LIMIT 5").fetchall()
    for b in birds:
        print(dict(b))

    print("\n--- TEST QUERY (LEFT JOIN) ---")
    sql = '''
        SELECT 
            n.id_nidada, 
            n.id_cruce,
            n.fecha_primer_huevo
        FROM nidadas n
        LEFT JOIN cruces c ON n.id_cruce = c.id_cruce
        LEFT JOIN pajaros ph ON c.id_hembra = ph.id_ave
    '''
    res = cur.execute(sql).fetchall()
    for r in res:
        print(dict(r))

    conn.close()

if __name__ == "__main__":
    debug_data()
