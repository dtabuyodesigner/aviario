import sqlite3

DB_PATH = 'database/aviario.db'

def normalize_species():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Mapping based on previous audits
    mapping = [
        ('Agapornis Roseicollis', 'Agapornis cara rosada'),
        ('Agapornis Personatus', 'Agapornis enmascarado'),
        ('Agapornis Fischeri', 'Agapornis de Fischer'),
        ('Ninfas', 'Ninfa'),
        ('Domestic Canary', 'Canario'),
        ('Canario de Color', 'Canario'),
        ('Canario de Postura', 'Canario'),
        ('Canario de Canto', 'Canario')
    ]

    for old, new in mapping:
        cur.execute("UPDATE mutaciones SET especie_asociada = ? WHERE especie_asociada = ?", (new, old))
        print(f"Normalized '{old}' to '{new}' in mutaciones table.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    normalize_species()
