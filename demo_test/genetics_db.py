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
        # Petición segura: intentamos leer columnas nuevas si existen
        # Si no, usaremos fallback
        
        # Primero revisamos columnas disponibles
        cur.execute("PRAGMA table_info(mutaciones)")
        columns = [row['name'] for row in cur.fetchall()]
        
        has_locus = 'locus' in columns
        has_dom = 'dominancia' in columns
        
        query = "SELECT * FROM mutaciones WHERE especie_asociada = ?"
        cur.execute(query, (species,))
        rows = cur.fetchall()

        for row in rows:
            nombre = row['nombre']
            tipo = row['tipo_herencia']
            
            # 1. Determine Locus Name
            locus_name = nombre # Default: each mutation is its own locus
            if has_locus and row['locus']:
                locus_name = row['locus']
            else:
                # Heuristic for Alletic Series if not in DB yet
                if 'Turquesa' in nombre or 'Aqua' in nombre:
                     locus_name = 'Serie Azul' # Hardcoded fallback logic just in case
                elif 'Azul' in nombre and 'Serie' not in nombre:
                     locus_name = 'Serie Azul'

            # 2. Determine Sex Linked
            is_sl = False
            if tipo and 'Ligada' in tipo: is_sl = True
            
            # 3. Determine Dominance
            dominance = 0
            if has_dom and row['dominancia'] is not None:
                dominance = row['dominancia']
            else:
                # Heuristic fallback
                if tipo == 'Dominante': dominance = 2
                elif 'Incompleta' in str(tipo): dominance = 1 # ?
                else: dominance = 0 # Recessive

            # Create or Update Locus
            if locus_name not in loci:
                loci[locus_name] = Locus(locus_name, sex_linked=is_sl)
                # Add Wildtype allele by default
                # Logic: Wild is usually Dominant to Recessive (2 vs 0)
                # But Recessive to Dominant Mutation? (0 vs 2)
                
                # Standard convention in this engine:
                # Alleles compete by number.
                # If Mut is Recessive (0), Wild should be Dominant (2).
                # If Mut is Dominant (2), Wild should be Recessive (0).
                
                # Complex case: Locus with both Dom and Rec mutations?
                # For safety, let's assume Wild is 1 (Neutral?) or 2 (Dominant)?
                # User snippet used:
                # blue_series.add_allele("wild", 2) (Wild > Blue(0))
                
                # Let's verify dominance relation of the FIRST mutation added to this locus.
                wild_dom = 2
                if dominance == 2: # Found a dominant mutation
                    wild_dom = 0
                    
                loci[locus_name].add_allele("wild", wild_dom)

            loci[locus_name].add_allele(nombre, dominance)

    except sqlite3.Error as e:
        print(f"Error loading genetics DB: {e}")
        return {}
    finally:
        conn.close()

    return loci
