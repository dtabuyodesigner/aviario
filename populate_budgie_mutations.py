import sqlite3
import uuid

DB_PATH = 'database/aviario.db'
# We will use a main "Periquito" species. 
# Check if "Periquito" exists or create it.
SPECIES_NAME = 'Periquito'
SPECIES_UUID = 'species-periquito' # We'll enforce this UUID for consistency

BUDGIE_DATA = {
    'Base': [
        ('Verde', 'Ancestral', 1),
        ('Azul', 'Autosómica Recesiva', 0),
        ('Gris', 'Dominante', 1),
        ('Violeta', 'Dominante', 1)
    ],
    'Factor Oscuro': [
        ('Dark factor (1F)', 'Dominante', 1),
        ('Dark factor (2F)', 'Dominante', 1)
    ],
    'Ligadas al Sexo': [
        ('Ino (Lutino/Albino)', 'Ligada al Sexo', 0), # Simplified for UI
        ('Lutino', 'Ligada al Sexo', 0),
        ('Albino', 'Ligada al Sexo', 0),
        ('Canela', 'Ligada al Sexo', 0),
        ('Opalino', 'Ligada al Sexo', 0),
        ('Texas Clearbody', 'Ligada al Sexo', 0),
        ('Slate', 'Ligada al Sexo', 0)
    ],
    'Patrones': [
        ('Pio Dominante', 'Dominante', 1),
        ('Pio Recesivo', 'Autosómica Recesiva', 0),
        ('Pio de Collar', 'Dominante', 1), # Often Combo
        ('Spangle (Perlado)', 'Dominante', 1),
        ('Clearflight', 'Dominante', 1)
    ],
    'Faciales': [
        ('Cara Amarilla Tipo I', 'Dominante', 1),
        ('Cara Amarilla Tipo II', 'Dominante', 1),
        ('Cara Dorada', 'Dominante', 1)
    ],
    'Avanzadas': [
        ('Fallow', 'Autosómica Recesiva', 0),
        ('Blackface', 'Autosómica Recesiva', 0),
        ('Mottled', 'Recesiva', 0),
        ('Half-Sider', 'Quimera', 0), # Not really a mutation but visual
        ('Diluido', 'Autosómica Recesiva', 0),
        ('Alas Claras', 'Autosómica Recesiva', 0),
        ('Alas Grises', 'Autosómica Recesiva', 0),
        ('Fullbody', 'Autosómica Recesiva', 0), # Greywing/Clearwing combo
        ('Arcoíris', 'Poligénica', 0) # Combo
    ]
}

def run():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. UPSERT Species
    # Create or genericize "Periquito"
    try:
        cur.execute("INSERT OR IGNORE INTO especies (uuid, nombre_comun, nombre_cientifico) VALUES (?, ?, 'Melopsittacus undulatus')", (SPECIES_UUID, SPECIES_NAME))
    except:
        pass # Might exist with different ID

    # 2. Populate Mutations
    # Check if we need a 'Standard' variety to link to? 
    # Or just link to species if no varieties used for Budgies (unlike Canaries).
    # Current system: birds.js `loadMutations` checks for varieties. If none, loads strict mutations for species.
    # So we don't strict need a variety, we can link to species directly via `mutaciones.especie_asociada` (if it existed) or just relies on `variedades`? 
    # Wait, `get_mutations` in app.py uses `variedad_mutaciones` -> `variedades` -> `especies`.
    # SO WE MUST HAVE A VARIETY to link mutations to, even if it's a "Standard" one.
    
    VARIETY_UUID = 'var-budgie-stand'
    try:
        cur.execute("INSERT OR IGNORE INTO variedades (uuid, especie_uuid, nombre) VALUES (?, ?, 'Estándar')", (VARIETY_UUID, SPECIES_UUID))
    except:
        pass

    for subgroup, mutations in BUDGIE_DATA.items():
        print(f"Processing group: {subgroup}")
        for name, inheritance, dom in mutations:
            slug = name.lower().replace(' ', '-').replace('/','-').replace('(','').replace(')','')
            mut_uuid = f"mut-bud-{slug}"
            
            # Insert Mutation
            try:
                cur.execute('''
                    INSERT INTO mutaciones (uuid, nombre, tipo_herencia, subgrupo, dominante, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, DATETIME('now'), DATETIME('now'))
                    ON CONFLICT(uuid) DO UPDATE SET 
                        subgrupo=excluded.subgrupo,
                        tipo_herencia=excluded.tipo_herencia,
                        dominante=excluded.dominante,
                        updated_at=DATETIME('now')
                ''', (mut_uuid, name, inheritance, subgroup, dom))
            except Exception as e:
                print(f"Error inserting {name}: {e}")

            # Link to Standard Variety
            link_uuid = f"vm-bud-{slug}"
            try:
                cur.execute('''
                    INSERT INTO variedad_mutaciones (uuid, variedad_uuid, mutacion_uuid, created_at, updated_at)
                    VALUES (?, ?, ?, DATETIME('now'), DATETIME('now'))
                    ON CONFLICT(uuid) DO UPDATE SET updated_at=DATETIME('now')
                ''', (link_uuid, VARIETY_UUID, mut_uuid))
            except Exception as e:
                print(f"Error linking {name}: {e}")

    conn.commit()
    conn.close()
    print("Budgerigar mutations populated.")

if __name__ == '__main__':
    run()
