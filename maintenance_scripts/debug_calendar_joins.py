import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'aviario.db')

def inspect_joins():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    print("--- 1. CHECK NIDADAS WITH DATE ---")
    nidadas = cur.execute("SELECT * FROM nidadas WHERE fecha_primer_huevo IS NOT NULL").fetchall()
    print(f"Found {len(nidadas)} clutches with start date.")
    for n in nidadas:
        print(f"Nidada ID: {n['id_nidada']}, Cruce ID: {n['id_cruce']}, Date: {n['fecha_primer_huevo']}")
        
        # Check Link to Cruce
        cruce = cur.execute("SELECT * FROM cruces WHERE id_cruce = ?", (n['id_cruce'],)).fetchone()
        if not cruce:
            print(f"  -> CRITICAL: Cruce {n['id_cruce']} NOT FOUND!")
            continue
            
        print(f"  -> Linked Cruce {cruce['id_cruce']}: Hembra ID {cruce['id_hembra']}")
        
        # Check Link to Hembra
        hembra = cur.execute("SELECT * FROM pajaros WHERE id_ave = ?", (cruce['id_hembra'],)).fetchone()
        if not hembra:
            print(f"  -> CRITICAL: Hembra {cruce['id_hembra']} NOT FOUND!")
            continue
            
        print(f"  -> Linked Hembra {hembra['id_ave']}: Especie ID {hembra['id_especie']}")
        
        # Check Link to Especie
        especie = cur.execute("SELECT * FROM especies WHERE id_especie = ?", (hembra['id_especie'],)).fetchone()
        if not especie:
             print(f"  -> ERROR: Especie ID {hembra['id_especie']} NOT FOUND in especies table! Left Join will return NULL, but Inner Join would fail if used.")
        else:
             print(f"  -> Linked Especie: {especie['nombre_comun']}")

    conn.close()

if __name__ == "__main__":
    inspect_joins()
