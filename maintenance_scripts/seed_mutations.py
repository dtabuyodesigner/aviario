import sqlite3
import os

DB_PATH = 'aviario.db'
SCHEMA_PATH = 'database/schema.sql'

def seed_mutations():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Ensure Schema is updated (Create mutaciones table if not exists)
    # Simple check if table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mutaciones'")
    if not cur.fetchone():
        print("Creando tabla 'mutaciones'...")
        with open(SCHEMA_PATH, 'r') as f:
            script = f.read()
            # Execute only the create table part manually or just run the whole thing safely?
            # Running executemany with IF NOT EXISTS is safe.
            cur.executescript(script)

    # 2. Check for CITES columns in pajaros
    cur.execute("PRAGMA table_info(pajaros)")
    columns = [row[1] for row in cur.fetchall()]
    if 'cites_numero' not in columns:
        print("Añadiendo columnas CITES a tabla pajaros...")
        try:
            cur.execute("ALTER TABLE pajaros ADD COLUMN cites_numero TEXT")
            cur.execute("ALTER TABLE pajaros ADD COLUMN documento_cesion TEXT")
        except Exception as e:
            print(f"Nota: {e}")

    # 3. Clear existing mutations to avoid duplicates during dev
    cur.execute("DELETE FROM mutaciones")
    
    mutation_data = []

    # --- AGAPORNIS PERSONATUS ---
    sp = 'Agapornis Personatus'
    mutation_data.extend([
        (sp, 'Ancestral (Verde)', 'Dominante', None),
        (sp, 'Azul', 'Recesiva Autosómica', None),
        (sp, 'Cobalto', 'Dominante Incompleta', None),
        (sp, 'Malva', 'Dominante Incompleta', None),
        (sp, 'Violeta SF', 'Dominante Incompleta', None),
        (sp, 'Violeta DF', 'Dominante Incompleta', None),
        (sp, 'Ino', 'Recesiva Autosómica', None),
        (sp, 'Arlequín Dominante', 'Dominante', None)
    ])

    # --- AGAPORNIS FISCHERI ---
    sp = 'Agapornis Fischeri'
    mutation_data.extend([
        (sp, 'Ancestral', 'Dominante', None),
        (sp, 'Ino (Lutino/Albino)', 'Recesiva Autosómica', None), # Ojo: Diferente al Roseicollis
        (sp, 'Dec (Ojos Negros)', 'Recesiva Autosómica', None),
        (sp, 'Euwing', 'Dominante', None),
        (sp, 'Pastel', 'Recesiva Autosómica', None),
        (sp, 'Diluido', 'Recesiva Autosómica', None),
        (sp, 'Slaty (Pizarra)', 'Dominante', None),
        (sp, 'Misty', 'Dominante Incompleta', None),
        (sp, 'Sable', 'Selección', None)
    ])

    # --- AGAPORNIS ROSEICOLLIS ---
    sp = 'Agapornis Roseicollis'
    mutation_data.extend([
        (sp, 'Verde Ancestral', 'Dominante', None),
        (sp, 'Lutino (Ino)', 'Recesiva Ligada al Sexo', None),
        (sp, 'Opalino', 'Recesiva Ligada al Sexo', None),
        (sp, 'Canela', 'Recesiva Ligada al Sexo', None),
        (sp, 'Pallid', 'Recesiva Ligada al Sexo', None),
        (sp, 'Turquesa', 'Recesiva Autosómica', None),
        (sp, 'Aqua', 'Recesiva Autosómica', None),
        (sp, 'Cara Naranja', 'Recesiva Autosómica', None),
        (sp, 'Marbled', 'Recesiva Autosómica', None),
        (sp, 'Arlequín Dominante', 'Dominante', None),
        (sp, 'Violeta', 'Dominante', None), 
        (sp, 'Factor Oscuro (Jade/Oliva)', 'Dominante Incompleta', None),
        (sp, 'Edge', 'Dominante Incompleta', None)
    ])

    # --- NINFAS (CAROLINAS) ---
    sp = 'Ninfas'
    mutation_data.extend([
        (sp, 'Gris Ancestral', 'Dominante', None),
        (sp, 'Lutina', 'Recesiva Ligada al Sexo', None),
        (sp, 'Canela', 'Recesiva Ligada al Sexo', None),
        (sp, 'Perlada (Opalina)', 'Recesiva Ligada al Sexo', None),
        (sp, 'Carablanca', 'Recesiva Autosómica', None),
        (sp, 'Manchado (Pío)', 'Recesiva Autosómica', None),
        (sp, 'Albina', 'Combinación', None),
        (sp, 'Fallow', 'Recesiva Autosómica', None),
        (sp, 'Plata Dominante', 'Dominante', None),
        (sp, 'Plata Recesivo', 'Recesiva Autosómica', None),
        (sp, 'Pastelface', 'Recesiva Autosómica', None),
        (sp, 'Face Amarilla', 'Recesiva Autosómica', None)
    ])

    # --- CANARIOS DE COLOR (Triple Entrada) ---
    sp = 'Canario de Color'
    # TIpo (Melaninas)
    mutation_data.extend([
        (sp, 'Negro', 'Autosómica', 'Tipo'),
        (sp, 'Bruno', 'Autosómica', 'Tipo'),
        (sp, 'Ágata', 'Autosómica', 'Tipo'),
        (sp, 'Isabela', 'Autosómica', 'Tipo')
    ])
    # Mutación Adjunta
    mutation_data.extend([
        (sp, 'Clásico', 'N/A', 'Mutación Adjunta'),
        (sp, 'Pastel', 'Ligada Sexo', 'Mutación Adjunta'),
        (sp, 'Opalo', 'Autosómica', 'Mutación Adjunta'),
        (sp, 'Phaeo', 'Autosómica', 'Mutación Adjunta'),
        (sp, 'Satiné', 'Ligada Sexo', 'Mutación Adjunta'),
        (sp, 'Topacio', 'Autosómica', 'Mutación Adjunta'),
        (sp, 'Eumo', 'Autosómica', 'Mutación Adjunta'),
        (sp, 'Cobalto', 'Autosómica', 'Mutación Adjunta'),
        (sp, 'Jaspe', 'Dominante Inc.', 'Mutación Adjunta'),
        (sp, 'Onix', 'Autosómica', 'Mutación Adjunta')
    ])
    # Variedad (Lipocromo)
    mutation_data.extend([
        (sp, 'Blanco Recesivo', 'Recesiva', 'Variedad'),
        (sp, 'Blanco Dominante', 'Dominante', 'Variedad'),
        (sp, 'Amarillo', 'N/A', 'Variedad'),
        (sp, 'Rojo', 'N/A', 'Variedad'),
        (sp, 'Marfil', 'Ligada Sexo', 'Variedad')
    ])
    # Categoría
    mutation_data.extend([
        (sp, 'Intenso', 'N/A', 'Categoría'),
        (sp, 'Nevado', 'N/A', 'Categoría'),
        (sp, 'Mosaico', 'N/A', 'Categoría')
    ])

    # --- CANARIOS DE CANTO ---
    sp = 'Canario de Canto'
    mutation_data.extend([
        (sp, 'Timbrado Español', 'Selección', None),
        (sp, 'Roller (Harzer)', 'Selección', None),
        (sp, 'Malinois (Waterslager)', 'Selección', None),
        (sp, 'American Singer', 'Selección', None),
        (sp, 'Cantor Ruso', 'Selección', None)
    ])

    # --- CANARIOS DE POSTURA ---
    # Convertimos los subgrupos en "Subgrupos" reales o simplemente lista plana si el usuario solo elige la raza.
    # El usuario dijo: "Rizados", "De Forma", etc. Lo pondré en subgrupo para agrupar si es necesario.
    sp = 'Canario de Postura'
    mutation_data.extend([
        # Rizados
        (sp, 'Rizado de París', 'Postura', 'Rizados'),
        (sp, 'Rizado del Norte', 'Postura', 'Rizados'),
        (sp, 'Rizado del Sur', 'Postura', 'Rizados'),
        (sp, 'Fiorino', 'Postura', 'Rizados'),
        (sp, 'Gigante Italiano', 'Postura', 'Rizados'),
        # Posición
        (sp, 'Giboso Español', 'Postura', 'Posición'),
        (sp, 'Llarguet Español', 'Postura', 'Posición'),
        (sp, 'Hosso Japonés', 'Postura', 'Posición'),
        (sp, 'Melado Tinerfeño', 'Postura', 'Posición'),
        # Forma
        (sp, 'Norwich', 'Postura', 'Forma'),
        (sp, 'Yorkshire', 'Postura', 'Forma'),
        (sp, 'Border', 'Postura', 'Forma'),
        (sp, 'Fife Fancy', 'Postura', 'Forma'),
        # Moñudos
        (sp, 'Gloster Corona', 'Postura', 'Moñudos'),
        (sp, 'Gloster Consort', 'Postura', 'Moñudos'),
        (sp, 'Crested', 'Postura', 'Moñudos'),
        (sp, 'Moña Alemana', 'Postura', 'Moñudos'),
        # Diseño
        (sp, 'Lizard Oro', 'Postura', 'Diseño'),
        (sp, 'Lizard Plata', 'Postura', 'Diseño'),
        (sp, 'Lizard Azul', 'Postura', 'Diseño')
    ])

    # --- EXÓTICOS: DIAMANTE DE GOULD ---
    sp = 'Diamante de Gould'
    # Cabeza
    mutation_data.extend([
        (sp, 'Roja', 'Dominante', 'Cabeza'),
        (sp, 'Negra', 'Recesiva', 'Cabeza'),
        (sp, 'Naranja', 'Recesiva', 'Cabeza')
    ])
    # Pecho
    mutation_data.extend([
        (sp, 'Violeta', 'Ancestral', 'Pecho'),
        (sp, 'Blanco', 'Recesiva', 'Pecho'),
        (sp, 'Lila', 'Recesiva', 'Pecho')
    ])
    # Manto
    mutation_data.extend([
        (sp, 'Verde', 'Ancestral', 'Manto'),
        (sp, 'Amarillo', 'Dominante/Recesiva', 'Manto'),
        (sp, 'Azul', 'Recesiva', 'Manto'),
        (sp, 'Pastel', 'Ligada Sexo', 'Manto')
    ])

    sql = 'INSERT INTO mutaciones (especie_asociada, nombre, tipo_herencia, subgrupo) VALUES (?, ?, ?, ?)'
    
    cur.executemany(sql, mutation_data)
    conn.commit()
    print(f"Insertadas {cur.rowcount} mutaciones maestras.")
    conn.close()

if __name__ == '__main__':
    seed_mutations()
