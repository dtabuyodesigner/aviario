import sqlite3
import os
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'aviario.db')

def populate():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("Cleaning database...")
    cur.execute("DELETE FROM pajaros")
    cur.execute("DELETE FROM bird_mutations")
    cur.execute("DELETE FROM nidadas")

    # Species IDs from DB (Integers for better consistency)
    SP_PERIQUITO = 40
    SP_CANARIO = 4
    SP_NINFA = 198
    
    VAR_CANARIO_COLOR = 'var-canario-color'

    def add_bird(anilla, sexo, species, variety=None, p_uuid=None, m_uuid=None, fecha='2024-05-10'):
        u = str(uuid.uuid4())
        cur.execute("""
            INSERT INTO pajaros (uuid, anilla, sexo, id_especie, variety_uuid, padre_uuid, madre_uuid, estado, fecha_nacimiento, anio_nacimiento)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Activo', ?, ?)
        """, (u, anilla, sexo, species, variety, p_uuid, m_uuid, fecha, int(fecha[:4])))
        return u

    def add_mut(bird_uuid, mut_name, genotipo='Homocigoto'):
        cur.execute("SELECT id_ave FROM pajaros WHERE uuid = ?", (bird_uuid,))
        id_ave = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO bird_mutations (id, id_ave, id_mutacion, genotipo)
            VALUES (?, ?, ?, ?)
        """, (str(uuid.uuid4()), id_ave, mut_name, genotipo))

    print("Inserting Periquito Genealogical Tree...")
    # Grandparents Paternos
    ap_uuid = add_bird("GP-M-001", "M", SP_PERIQUITO, None, None, None, '2022-03-15')
    aa_uuid = add_bird("GP-H-002", "H", SP_PERIQUITO, None, None, None, '2022-04-20')
    
    # Grandparents Maternos
    amp_uuid = add_bird("GM-M-003", "M", SP_PERIQUITO, None, None, None, '2022-02-10')
    ama_uuid = add_bird("GM-H-004", "H", SP_PERIQUITO, None, None, None, '2022-05-05')

    # Parents
    padre_uuid = add_bird("P-M-2023", "M", SP_PERIQUITO, None, ap_uuid, aa_uuid, '2023-06-12')
    madre_uuid = add_bird("P-H-2023", "H", SP_PERIQUITO, None, amp_uuid, ama_uuid, '2023-07-18')

    # Target Bird
    hijo_uuid = add_bird("EXPO-2024-01", "M", SP_PERIQUITO, None, padre_uuid, madre_uuid, '2024-05-24')

    print("Adding mutations to Periquitos...")
    add_mut(hijo_uuid, "Opalino")
    add_mut(hijo_uuid, "Azul", "Portador")
    add_mut(ap_uuid, "Opalino")
    add_mut(aa_uuid, "Lutino", "Portador")

    print("Inserting other species...")
    # Canario
    c_uuid = add_bird("CAN-COL-01", "H", SP_CANARIO, VAR_CANARIO_COLOR, None, None, '2024-01-30')
    add_mut(c_uuid, "Intenso")
    
    # Ninfas
    add_bird("NIN-01", "M", SP_NINFA, None, None, None, '2023-11-20')
    n2_uuid = add_bird("NIN-02-ALB", "H", SP_NINFA, None, None, None, '2024-02-14')
    add_mut(n2_uuid, "Ino")
    add_mut(n2_uuid, "Cara Blanca")

    conn.commit()
    conn.close()
    print("Database reset and populated successfully!")

if __name__ == "__main__":
    populate()
