import sqlite3
from genetics_engine import Locus

def load_loci_from_db(db_path, species):
    """
    Loads mutations from DB and constructs Locus objects.
    Adapts to missing columns gracefully if schema isn't fully migrated yet.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    loci = {}

    try:
        # Robust query matching species through varieties
        query = """
            SELECT DISTINCT m.* 
            FROM mutaciones m
            JOIN variedad_mutaciones vm ON m.uuid = vm.mutacion_uuid
            JOIN variedades v ON vm.variedad_uuid = v.uuid
            JOIN especies e ON v.especie_uuid = e.uuid
            WHERE LOWER(e.nombre_comun) = LOWER(?) OR e.uuid = ?
        """
        cur.execute(query, (species, species))
        rows = cur.fetchall()

        for row in rows:
            nombre = row['nombre']
            tipo = row['tipo_herencia']
            
            # 1. Determine Locus Name
            locus_name = row['locus'] if 'locus' in row.keys() and row['locus'] else nombre

            # 2. Determine Sex Linked
            is_sl = False
            if tipo and 'Ligada' in tipo: is_sl = True
            
            # 3. Determine Dominance
            # Map 'dominante' from new schema
            dominance = row['dominante'] if 'dominante' in row.keys() and row['dominante'] is not None else 0

            # Create or Update Locus
            if locus_name not in loci:
                loci[locus_name] = Locus(locus_name, sex_linked=is_sl)
                # Add Wildtype allele as baseline
                loci[locus_name].add_allele("wild", 2) 
            elif is_sl:
                # If ANY mutation in this locus is sex-linked, the whole locus is.
                loci[locus_name].sex_linked = True

            # If we find a dominant mutation (2), wild must be recessive (0) for this locus
            if dominance == 2:
                loci[locus_name].alleles["wild"] = 0
                
            loci[locus_name].add_allele(nombre, dominance)

    except sqlite3.Error as e:
        print(f"Error loading genetics DB: {e}")
        return {}
    finally:
        conn.close()

    return loci

def load_combinations_from_db(db_path):
    """
    Loads custom mutation combinations (e.g. Ino + Opalino = Lacewing).
    Returns a dict: { (mut1_lower, mut2_lower): "Special Name" }
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    combinations = {}
    
    try:
        # Check if table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='genetic_combinations'")
        if not cur.fetchone():
            return {}

        cur.execute("""
            SELECT gc.*, m1.nombre as n1, m2.nombre as n2 
            FROM genetic_combinations gc
            JOIN mutaciones m1 ON gc.mutacion1_uuid = m1.uuid
            JOIN mutaciones m2 ON gc.mutacion2_uuid = m2.uuid
        """)
        rows = cur.fetchall()
        
        for row in rows:
            pair = tuple(sorted([row['n1'].lower(), row['n2'].lower()]))
            combinations[pair] = row['nombre_resultado']
            
    except sqlite3.Error as e:
        print(f"Error loading genetic combinations: {e}")
    finally:
        conn.close()
        
    return combinations
