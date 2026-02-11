import sqlite3

DB_PATH = 'database/aviario.db'

# Mutations to move to 'Alas y Patrones'
PATTERNS = [
    'Spangle',
    'Spangle (Perlado)', # Handle my previous naming
    'Dominant pied',
    'Pio Dominante',
    'Recessive pied',
    'Pio Recesivo',
    'Clearwing',
    'Alas Claras',
    'Greywing',
    'Alas Grises',
    'Dilute',
    'Diluido'
]

def run():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("Grouping Budgerigar Wings and Patterns...")

    target_subgroup = 'Alas y Patrones'

    for name in PATTERNS:
        # Update subgroup
        cur.execute("UPDATE mutaciones SET subgrupo = ? WHERE nombre = ? AND uuid LIKE 'mut-bud-%'", (target_subgroup, name))
        if cur.rowcount > 0:
            print(f"Updated {name} -> {target_subgroup}")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    run()
