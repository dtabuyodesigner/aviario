import sqlite3

DB_PATH = 'database/aviario.db'

def enrich_mutations():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Update Dominancia based on type_herencia
    updates = [
        ("Dominante", 2),
        ("Dominante Incompleta", 1),
        ("Recesiva Autosómica", 0),
        ("Ligada al Sexo", 0) # Usually recessive in birds (SL)
    ]

    for tipo, dom in updates:
        cur.execute("UPDATE mutaciones SET dominancia = ? WHERE tipo_herencia = ?", (dom, tipo))

    # 2. Update Loci for Agapornis (Blue Series)
    blue_series_muts = ['Azul', 'Turquesa', 'Aqua', 'AquaTurquesa', 'Violeta']
    for mut in blue_series_muts:
        cur.execute("UPDATE mutaciones SET locus = 'Serie Azul' WHERE (nombre LIKE ? OR nombre = ?) AND especie_asociada LIKE 'Agapornis%'", (f'%{mut}%', mut))

    # 3. Update Loci for Agapornis (Parblue Series overlap)
    parblue = ['Aqua', 'Turquesa']
    for p in parblue:
         cur.execute("UPDATE mutaciones SET locus = 'Serie Azul' WHERE nombre = ? AND especie_asociada LIKE 'Agapornis%'", (p,))

    # 4. Update Loci for NSL Ino
    cur.execute("UPDATE mutaciones SET locus = 'Locus NSL-Ino' WHERE nombre LIKE '%Lutino%' AND tipo_herencia = 'Recesiva Autosómica'")

    # 5. Update Loci for SL Ino 
    cur.execute("UPDATE mutaciones SET locus = 'Locus SL-Ino' WHERE nombre LIKE '%Lutino%' AND tipo_herencia = 'Ligada al Sexo'")

    conn.commit()
    print("Mutations enriched with locus and dominance data.")
    conn.close()

if __name__ == "__main__":
    enrich_mutations()
