import sqlite3

DB_PATH = 'database/aviario.db'

# Updates to Subgroups
UPDATES_SUBGROUP = [
    ('Violet factor', 'Factor Oscuro'),
    ('Violeta', 'Factor Oscuro'), 
    ('Grey factor', 'Factor Oscuro'), 
    ('Gris', 'Factor Oscuro'),
    ('Anthracite', 'Factor Oscuro'),
    ('Dark factor', 'Factor Oscuro'),
    ('Dark factor (1F)', 'Factor Oscuro'),
    ('Dark factor (2F)', 'Factor Oscuro'),
    
    # Sex Linked
    ('Lutino', 'Ligadas al Sexo'),
    ('Albino', 'Ligadas al Sexo'),
    ('Opalino', 'Ligadas al Sexo'),
    ('Canela', 'Ligadas al Sexo'),
    ('Texas Clearbody', 'Ligadas al Sexo'), # Also 'Texas clearbody' lower
    ('Texas clearbody', 'Ligadas al Sexo')
]

# Name Corrections
UPDATES_NAME = [
    ('Verde', 'Verde ancestral')
]

NEW_ENTRIES = [
    # Dark Factors
    ('Dark factor', 'Dominante', 'Factor Oscuro'),
    ('Violet factor', 'Dominante', 'Factor Oscuro'),
    ('Grey factor', 'Dominante', 'Factor Oscuro'),
    ('Anthracite', 'Dominante', 'Factor Oscuro'),
    
    # Sex Linked specific (ensure existence)
    ('Lutino', 'Ligada al Sexo', 'Ligadas al Sexo'),
    ('Albino', 'Ligada al Sexo', 'Ligadas al Sexo'),
    ('Opalino', 'Ligada al Sexo', 'Ligadas al Sexo'),
    ('Canela', 'Ligada al Sexo', 'Ligadas al Sexo'),
    ('Texas clearbody', 'Ligada al Sexo', 'Ligadas al Sexo')
]

def run():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("Refining Budgerigar Mutations...")
    
    VARIETY_UUID = 'var-budgie-stand' 

    # 1. Update Subgroups
    for name, subgroup in UPDATES_SUBGROUP:
        # Use UUID prefix and Name
        cur.execute("UPDATE mutaciones SET subgrupo = ? WHERE nombre = ? AND uuid LIKE 'mut-bud-%'", (subgroup, name))
        
    # 2. Update Names
    for old, new in UPDATES_NAME:
        cur.execute("UPDATE mutaciones SET nombre = ? WHERE nombre = ? AND uuid LIKE 'mut-bud-%'", (new, old))

    # 3. Ensure Entries
    for name, inheritance, subgroup in NEW_ENTRIES:
        slug = name.lower().replace(' ', '-').replace('/','-').replace('(','').replace(')','')
        mut_uuid = f"mut-bud-{slug}"
        
        try:
            cur.execute('''
                INSERT INTO mutaciones (uuid, nombre, tipo_herencia, subgrupo, dominante, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, DATETIME('now'), DATETIME('now'))
                ON CONFLICT(uuid) DO UPDATE SET 
                    subgrupo=excluded.subgrupo,
                    tipo_herencia=excluded.tipo_herencia,
                    updated_at=DATETIME('now')
            ''', (mut_uuid, name, inheritance, subgroup, 1 if 'Dominante' in inheritance else 0))
            
            # Link
            link_uuid = f"vm-bud-{slug}"
            cur.execute('''
                INSERT INTO variedad_mutaciones (uuid, variedad_uuid, mutacion_uuid)
                VALUES (?, ?, ?)
                ON CONFLICT(uuid) DO NOTHING
            ''', (link_uuid, VARIETY_UUID, mut_uuid))
        except Exception as e:
            print(f"Error {name}: {e}")

    conn.commit()
    conn.close()
    print("Done.")

if __name__ == '__main__':
    run()
