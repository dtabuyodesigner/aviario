
import sqlite3
import os

DB_PATH = 'aviario.db'

def seed_contacts():
    if not os.path.exists(DB_PATH):
        print(f"Error: {DB_PATH} not found. Run app.py first to init DB.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    contacts = [
        # 3 Criadores
        {
            'tipo': 'Criador',
            'nombre_razon_social': 'Aviario del Sur (M. González)',
            'dni_cif': '12345678A',
            'n_criador': 'E-555',
            'telefono': '652-598-125',
            'email': 'gonzalez@aves.com',
            'direccion': 'Calle Las Flores 12, Sevilla'
        },
        {
            'tipo': 'Criador',
            'nombre_razon_social': 'Canarios de Postura S.L.',
            'dni_cif': 'B98765432',
            'n_criador': 'CN-230',
            'telefono': '910-222-333',
            'email': 'info@canariospostura.es',
            'direccion': 'Av. Industria 5, Madrid'
        },
        {
            'tipo': 'Criador',
            'nombre_razon_social': 'Pedro Martínez (Amateur)',
            'dni_cif': '87654321Z',
            'n_criador': 'K-100',
            'telefono': '611-222-333',
            'email': 'pedro@gmail.com',
            'direccion': 'Plaza Mayor 1, Pueblo'
        },
        # 1 Veterinario
        {
            'tipo': 'Veterinario',
            'nombre_razon_social': 'Clínica Veterinaria Las Alas',
            'dni_cif': 'B11223344',
            'n_criador': '',
            'telefono': '900-800-700',
            'email': 'urgencias@lasalas.vet',
            'direccion': 'C/ Sanidad 45, Barcelona'
        },
        # 1 Otro
        {
            'tipo': 'Otro',
            'nombre_razon_social': 'Alimentos y Semillas Pajarito',
            'dni_cif': 'A55667788',
            'n_criador': '',
            'telefono': '956-111-222',
            'email': 'pedidos@pajarito.com',
            'direccion': 'Polígono Industrial Norte, Nave 3'
        }
    ]

    print("Seeding contacts...")
    for c in contacts:
        # Check if exists to avoid duplicates
        cur.execute('SELECT id_contacto FROM contactos WHERE nombre_razon_social = ?', (c['nombre_razon_social'],))
        exists = cur.fetchone()
        
        if not exists:
            keys = ', '.join(c.keys())
            placeholders = ', '.join(['?'] * len(c))
            values = list(c.values())
            
            sql = f"INSERT INTO contactos ({keys}) VALUES ({placeholders})"
            cur.execute(sql, values)
            print(f"Added: {c['nombre_razon_social']}")
        else:
            print(f"Skipped (exists): {c['nombre_razon_social']}")

    conn.commit()
    conn.close()
    print("Contacts seeding complete.")

if __name__ == '__main__':
    seed_contacts()
