import sqlite3

DB_PATH = 'database/aviario.db'

UPDATES = [
    # (Name, New Subgroup)
    ('Violet factor', 'Factor Oscuro'),
    ('Violeta', 'Factor Oscuro'), # Handle Spanish name too if present
    ('Grey factor', 'Factor Oscuro'), 
    ('Gris', 'Factor Oscuro'),
    ('Anthracite', 'Factor Oscuro'),
    ('Dark factor', 'Factor Oscuro'),
    ('Dark factor (1F)', 'Factor Oscuro'), # Keep these just in case
    ('Dark factor (2F)', 'Factor Oscuro')
]

def run():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("Updating Budgerigar Dark Factors...")

    # 1. Update existing
    for name, subgroup in UPDATES:
        cur.execute("UPDATE mutaciones SET subgrupo = ? WHERE nombre = ? AND (especie_asociada = 'Periquito' OR uuid LIKE 'mut-bud-%')", (subgroup, name))
        if cur.rowcount > 0:
            print(f"Updated {name} -> {subgroup}")
        
    # 2. Ensure "Dark factor", "Violet factor", "Grey factor", "Anthracite" exist if they were missing or named differently
    # The user lists English names "Dark factor", "Violet factor"...
    # My previous script inserted 'Verde', 'Azul', 'Gris', 'Violeta' (Spanish) AND 'Dark factor (1F)'.
    # I should probably ensure the English names exist if the user wants them specifically, 
    # OR map the Spanish ones if that's what the user meant (User text was mixed: "periquito factores oscuros" title, but English items in table).
    # I'll enable the English ones as requested in the table.

    NEW_ENTRIES = [
        ('Dark factor', 'Dominante', 'Factor Oscuro'),
        ('Violet factor', 'Dominante', 'Factor Oscuro'),
        ('Grey factor', 'Dominante', 'Factor Oscuro'),
        ('Anthracite', 'Dominante', 'Factor Oscuro')
    ]
    
    VARIETY_UUID = 'var-budgie-stand' # Ensure linked

    for name, inheritance, subgroup in NEW_ENTRIES:
        slug = name.lower().replace(' ', '-')
        mut_uuid = f"mut-bud-{slug}"
        
        # Insert/Update
        try:
            cur.execute('''
                INSERT INTO mutaciones (uuid, nombre, tipo_herencia, subgrupo, dominante, created_at, updated_at)
                VALUES (?, ?, ?, ?, 1, DATETIME('now'), DATETIME('now'))
                ON CONFLICT(uuid) DO UPDATE SET subgrupo=excluded.subgrupo, updated_at=DATETIME('now')
            ''', (mut_uuid, name, inheritance, subgroup))
            
            # Link
            link_uuid = f"vm-bud-{slug}"
            cur.execute('''
                INSERT INTO variedad_mutaciones (uuid, variedad_uuid, mutacion_uuid)
                VALUES (?, ?, ?)
                ON CONFLICT(uuid) DO NOTHING
            ''', (link_uuid, VARIETY_UUID, mut_uuid))
            print(f"Ensured {name}")
        except Exception as e:
            print(f"Error {name}: {e}")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    run()
