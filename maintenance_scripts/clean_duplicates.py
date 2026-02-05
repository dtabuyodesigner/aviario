
import sqlite3
import os

DB_PATH = 'aviario.db'

def clean_duplicates():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    print("=== Scanning for Duplicates ===")
    
    # 1. Helper to find duplicates by field
    def find_groups(field):
        sql = f'''
            SELECT {field}, GROUP_CONCAT(id_contacto) as ids, COUNT(*) as count
            FROM contactos 
            WHERE {field} IS NOT NULL AND {field} != ''
            GROUP BY {field}
            HAVING count > 1
        '''
        return cur.execute(sql).fetchall()

    duplicate_groups = []
    
    # Check Phone
    for row in find_groups('telefono'):
        ids = row['ids'].split(',')
        duplicate_groups.append({'field': 'telefono', 'value': row['telefono'], 'ids': ids})
        
    # Check Email
    for row in find_groups('email'):
        ids = row['ids'].split(',')
        # Avoid re-processing if already caught by phone (simple check)
        ids.sort()
        is_new = True
        for g in duplicate_groups:
            existing_ids = g['ids']
            existing_ids.sort()
            if ids == existing_ids:
                is_new = False
                break
        if is_new:
            duplicate_groups.append({'field': 'email', 'value': row['email'], 'ids': ids})

    if not duplicate_groups:
        print("No duplicates found.")
        conn.close()
        return

    print(f"Found {len(duplicate_groups)} groups of duplicates.")

    # 2. Process Fusion
    for group in duplicate_groups:
        print(f"\nProcessing group ({group['field']}={group['value']}): IDs {group['ids']}")
        
        # Get full records
        placeholders = ','.join(['?']*len(group['ids']))
        records = cur.execute(f"SELECT * FROM contactos WHERE id_contacto IN ({placeholders})", group['ids']).fetchall()
        
        # Strategy: Keep the one with highest ID (most recent) or lowest? 
        # Usually keep oldest (lowest ID) to preserve history, OR keep newest if data is better.
        # Let's keep the one with most non-null fields.
        
        sorted_records = sorted(records, key=lambda r: sum(1 for x in r if x), reverse=True)
        primary = sorted_records[0]
        secondary_records = sorted_records[1:]
        
        pid = primary['id_contacto']
        print(f"  -> Merging into Primary ID: {pid} ({primary['nombre_razon_social']})")
        
        for sec in secondary_records:
            sid = sec['id_contacto']
            print(f"     -> Processing Secondary ID: {sid} ({sec['nombre_razon_social']})")
            
            # Update Foreign Keys
            # Pajaros (id_criador_externo)
            cur.execute("UPDATE pajaros SET id_criador_externo = ? WHERE id_criador_externo = ?", (pid, sid))
            if cur.rowcount > 0:
                print(f"        Updated {cur.rowcount} birds.")
                
            # Movimientos (id_contacto) - Assuming table exists or will exist. 
            # Checking if table exists first to avoid error
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='movimientos'")
            if cur.fetchone():
                cur.execute("UPDATE movimientos SET id_contacto = ? WHERE id_contacto = ?", (pid, sid))
                if cur.rowcount > 0:
                     print(f"        Updated {cur.rowcount} movements.")

            # Delete Secondary
            cur.execute("DELETE FROM contactos WHERE id_contacto = ?", (sid,))
            print("        Deleted secondary record.")

    conn.commit()
    conn.close()
    print("\n=== Cleanup Complete ===")

if __name__ == '__main__':
    clean_duplicates()
